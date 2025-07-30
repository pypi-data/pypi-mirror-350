from math import ceil
from fastapi import status
from typing import Union, List, Dict, Any, Optional
import aiomysql
from ..base_dao import BaseDAO
from ..exceptions import HttpException

class AsyncMySQLDAO(BaseDAO):
    def __init__(self, db: aiomysql.Pool, collection_name: str, entity_cls=None, tenant_id: str = None, tenant_field: str = "tenant_id", is_deleted_field: Optional[str] = "is_deleted"):
        """
        DAO for MySQL with async support.

        :param db: Connection pool to the database.
        :param collection_name: Name of the table in the database.
        :param entity_cls: Entity class for automatic serialization/deserialization.
        :param tenant_id: Tenant ID for multi-tenant logic.
        :param tenant_field: Name of the field used for tenant filtering (default: "tenant_id").
        :param is_deleted_field: Name of the field used for deletion filtering (default: "is_deleted"). If None, no deletion filter will be applied.
        """
        super().__init__(db, collection_name, tenant_id, tenant_field, is_deleted_field)
        self.entity_cls = entity_cls

    def _from_mysql(self, row: dict):
        """Convert MySQL row to an entity instance."""
        if row is None:
            return None
        return self.entity_cls(**row) if self.entity_cls else row

    @staticmethod
    def _to_mysql(entity):
        """Convert an entity instance to a MySQL row."""
        if isinstance(entity, dict):
            return entity
        return entity.model_dump(by_alias=True)

    def _build_where_clause(self, filter_query: dict) -> tuple:
        """Build WHERE clause from filter query."""
        if not filter_query:
            return "", []

        filter_query = self._apply_tenant_filter(filter_query)
        where_clauses = []
        params = []

        for key, value in filter_query.items():
            where_clauses.append(f"{key} = %s")
            params.append(value)

        where_clause = " AND ".join(where_clauses)
        return where_clause, params

    async def insert(self, data):
        """Insert a new row in MySQL with tenant_id filter if necessary."""
        try:
            data = self._apply_tenant_filter(self._to_mysql(data))
            columns = ", ".join(data.keys())
            placeholders = ", ".join(["%s"] * len(data))
            values = list(data.values())

            query = f"INSERT INTO {self._collection_name} ({columns}) VALUES ({placeholders})"

            async with self._db.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, values)
                    await conn.commit()
                    return cursor.lastrowid
        except Exception as e:
            raise HttpException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    async def find_all(self):
        """Get all rows in MySQL without filter"""
        try:
            where_clause, params = self._build_where_clause({})
            query = f"SELECT * FROM {self._collection_name}"
            if where_clause:
                query += f" WHERE {where_clause}"

            async with self._db.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute(query, params)
                    rows = await cursor.fetchall()
                    return [self._from_mysql(row) for row in rows]
        except Exception as e:
            raise HttpException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    async def find_all_by_query(self, filter_query: dict):
        """Find all rows by query"""
        try:
            where_clause, params = self._build_where_clause(filter_query)
            query = f"SELECT * FROM {self._collection_name}"
            if where_clause:
                query += f" WHERE {where_clause}"

            async with self._db.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute(query, params)
                    rows = await cursor.fetchall()
                    return [self._from_mysql(row) for row in rows]
        except Exception as e:
            raise HttpException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    async def query_raw(self, sql: str, params: Optional[list] = None) -> List[dict]:
        """
        Executes a raw SQL query with optional parameters and returns results as a list of dictionaries.
        Useful for complex joins and subqueries not supported by basic DAO methods.
        """
        try:
            async with self._db.context() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute(sql, params or [])
                    rows = await cursor.fetchall()
                    return rows
        except Exception as e:
            raise HttpException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    async def execute_raw(self, sql: str, params: Optional[list] = None) -> int:
        """
        Executes an INSERT, UPDATE or DELETE query.
        Returns the number of affected rows.
        """
        try:
            async with self._db.context() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(sql, params or [])
                    await conn.commit()
                    return cursor.rowcount
        except Exception as e:
            raise HttpException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    async def execute_and_return_id(self, sql: str, params: Optional[list] = None) -> int:
        """
        Executes an INSERT query and returns the last inserted ID.
        """
        try:
            async with self._db.context() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(sql, params or [])
                    await conn.commit()
                    return cursor.lastrowid
        except Exception as e:
            raise HttpException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    async def find_by_id(self, item_id: Union[str, int]):
        """Search for a row by ID in MySQL."""
        try:
            filter_query = {"id": item_id}
            where_clause, params = self._build_where_clause(filter_query)
            query = f"SELECT * FROM {self._collection_name} WHERE {where_clause}"

            async with self._db.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute(query, params)
                    row = await cursor.fetchone()
                    return self._from_mysql(row) if row else None
        except Exception as e:
            raise HttpException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    async def find_by_filter(self, filter_query: dict):
        """Search for a row by query in MySQL."""
        try:
            where_clause, params = self._build_where_clause(filter_query)
            query = f"SELECT * FROM {self._collection_name}"
            if where_clause:
                query += f" WHERE {where_clause}"

            async with self._db.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute(query, params)
                    row = await cursor.fetchone()
                    return self._from_mysql(row) if row else None
        except Exception as e:
            raise HttpException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    async def find_paginated(self, filter_query: dict, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """Retrieve paginated rows."""
        try:
            where_clause, params = self._build_where_clause(filter_query)

            # Count total items
            count_query = f"SELECT COUNT(*) as count FROM {self._collection_name}"
            if where_clause:
                count_query += f" WHERE {where_clause}"

            # Get paginated data
            query = f"SELECT * FROM {self._collection_name}"
            if where_clause:
                query += f" WHERE {where_clause}"

            skip = (page - 1) * page_size
            query += f" LIMIT {page_size} OFFSET {skip}"

            async with self._db.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cursor:
                    # Get total count
                    await cursor.execute(count_query, params)
                    count_result = await cursor.fetchone()
                    total_items = count_result['count']

                    # Get paginated data
                    await cursor.execute(query, params)
                    rows = await cursor.fetchall()
                    items = [self._from_mysql(row) for row in rows]

                    total_pages = ceil(total_items / page_size)

                    return {
                        "results": items,
                        "pagination": {
                            "current_page": page,
                            "total_pages": total_pages,
                            "page_size": page_size,
                            "total_results": total_items,
                        }
                    }
        except Exception as e:
            raise HttpException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    async def update(self, item_id: Union[str, int], update_data):
        """Updates a row in MySQL."""
        try:
            update_data = self._to_mysql(update_data)
            set_clause = ", ".join([f"{key} = %s" for key in update_data.keys()])
            values = list(update_data.values())

            filter_query = {"id": item_id}
            where_clause, where_params = self._build_where_clause(filter_query)

            query = f"UPDATE {self._collection_name} SET {set_clause} WHERE {where_clause}"

            async with self._db.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, values + where_params)
                    await conn.commit()
                    return cursor.rowcount > 0
        except Exception as e:
            raise HttpException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    async def update_by_query(self, query: dict, update_data):
        """Updates a row by query in MySQL."""
        try:
            update_data = self._to_mysql(update_data)
            set_clause = ", ".join([f"{key} = %s" for key in update_data.keys()])
            values = list(update_data.values())

            where_clause, where_params = self._build_where_clause(query)

            query = f"UPDATE {self._collection_name} SET {set_clause}"
            if where_clause:
                query += f" WHERE {where_clause}"

            async with self._db.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, values + where_params)
                    await conn.commit()
                    return cursor.rowcount > 0
        except Exception as e:
            raise HttpException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    async def delete(self, item_id: Union[str, int]):
        """Delete a row in MySQL."""
        try:
            filter_query = {"id": item_id}
            where_clause, params = self._build_where_clause(filter_query)

            query = f"DELETE FROM {self._collection_name} WHERE {where_clause}"

            async with self._db.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, params)
                    await conn.commit()
                    return cursor.rowcount > 0
        except Exception as e:
            raise HttpException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    async def insert_many(self, data_list):
        """Insert multiple rows in MySQL with tenant_id filter if necessary."""
        try:
            if not data_list:
                return []

            # Apply tenant filter and convert to MySQL format for each item
            processed_data_list = [self._apply_tenant_filter(self._to_mysql(data)) for data in data_list]

            # Ensure all items have the same keys
            keys = processed_data_list[0].keys()
            columns = ", ".join(keys)
            placeholders = ", ".join(["%s"] * len(keys))

            # Create a single query for all rows
            query = f"INSERT INTO {self._collection_name} ({columns}) VALUES ({placeholders})"

            # Prepare values for all rows
            values_list = []
            for data in processed_data_list:
                values_list.append(list(data.values()))

            # Execute the query for each row
            inserted_ids = []
            async with self._db.acquire() as conn:
                async with conn.cursor() as cursor:
                    for values in values_list:
                        await cursor.execute(query, values)
                        inserted_ids.append(cursor.lastrowid)
                    await conn.commit()

            return inserted_ids
        except Exception as e:
            raise HttpException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))
