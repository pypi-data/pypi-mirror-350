from math import ceil
from fastapi import status
from typing import Union, List, Dict, Any, Optional
import pymysql
from pymysql.cursors import DictCursor
from ..base_dao import BaseDAO
from ..exceptions import HttpException

class SyncMySQLDAO(BaseDAO):
    def __init__(self, db: pymysql.connections.Connection, collection_name: str, entity_cls=None, tenant_id: str = None, tenant_field: str = "tenant_id", is_deleted_field: Optional[str] = "is_deleted"):
        """
        DAO for MySQL with sync support.

        :param db: Connection to the database.
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

    # Override async methods with sync implementations that are wrapped in async methods
    async def insert(self, data):
        """Insert a new row in MySQL with tenant_id filter if necessary."""
        try:
            return self._insert_sync(data)
        except Exception as e:
            raise HttpException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    def _insert_sync(self, data):
        """Synchronous implementation of insert."""
        data = self._apply_tenant_filter(self._to_mysql(data))
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        values = list(data.values())

        query = f"INSERT INTO {self._collection_name} ({columns}) VALUES ({placeholders})"

        with self._db.cursor() as cursor:
            cursor.execute(query, values)
            self._db.commit()
            return cursor.lastrowid

    async def find_all(self):
        """Get all rows in MySQL without filter"""
        try:
            return self._find_all_sync()
        except Exception as e:
            raise HttpException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    def _find_all_sync(self):
        """Synchronous implementation of find_all."""
        where_clause, params = self._build_where_clause({})
        query = f"SELECT * FROM {self._collection_name}"
        if where_clause:
            query += f" WHERE {where_clause}"

        with self._db.cursor(DictCursor) as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [self._from_mysql(row) for row in rows]

    async def find_all_by_query(self, filter_query: dict):
        """Find all rows by query"""
        try:
            return self._find_all_by_query_sync(filter_query)
        except Exception as e:
            raise HttpException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    def _find_all_by_query_sync(self, filter_query: dict):
        """Synchronous implementation of find_all_by_query."""
        where_clause, params = self._build_where_clause(filter_query)
        query = f"SELECT * FROM {self._collection_name}"
        if where_clause:
            query += f" WHERE {where_clause}"

        with self._db.cursor(DictCursor) as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [self._from_mysql(row) for row in rows]

    async def find_by_id(self, item_id: Union[str, int]):
        """Search for a row by ID in MySQL."""
        try:
            return self._find_by_id_sync(item_id)
        except Exception as e:
            raise HttpException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    def _find_by_id_sync(self, item_id: Union[str, int]):
        """Synchronous implementation of find_by_id."""
        filter_query = {"id": item_id}
        where_clause, params = self._build_where_clause(filter_query)
        query = f"SELECT * FROM {self._collection_name} WHERE {where_clause}"

        with self._db.cursor(DictCursor) as cursor:
            cursor.execute(query, params)
            row = cursor.fetchone()
            return self._from_mysql(row) if row else None

    async def find_by_filter(self, filter_query: dict):
        """Search for a row by query in MySQL."""
        try:
            return self._find_by_filter_sync(filter_query)
        except Exception as e:
            raise HttpException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    def _find_by_filter_sync(self, filter_query: dict):
        """Synchronous implementation of find_by_filter."""
        where_clause, params = self._build_where_clause(filter_query)
        query = f"SELECT * FROM {self._collection_name}"
        if where_clause:
            query += f" WHERE {where_clause}"

        with self._db.cursor(DictCursor) as cursor:
            cursor.execute(query, params)
            row = cursor.fetchone()
            return self._from_mysql(row) if row else None

    async def find_paginated(self, filter_query: dict, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """Retrieve paginated rows."""
        try:
            return self._find_paginated_sync(filter_query, page, page_size)
        except Exception as e:
            raise HttpException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    def _find_paginated_sync(self, filter_query: dict, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """Synchronous implementation of find_paginated."""
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

        with self._db.cursor(DictCursor) as cursor:
            # Get total count
            cursor.execute(count_query, params)
            count_result = cursor.fetchone()
            total_items = count_result['count']

            # Get paginated data
            cursor.execute(query, params)
            rows = cursor.fetchall()
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

    async def update(self, item_id: Union[str, int], update_data):
        """Updates a row in MySQL."""
        try:
            return self._update_sync(item_id, update_data)
        except Exception as e:
            raise HttpException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    def _update_sync(self, item_id: Union[str, int], update_data):
        """Synchronous implementation of update."""
        update_data = self._to_mysql(update_data)
        set_clause = ", ".join([f"{key} = %s" for key in update_data.keys()])
        values = list(update_data.values())

        filter_query = {"id": item_id}
        where_clause, where_params = self._build_where_clause(filter_query)

        query = f"UPDATE {self._collection_name} SET {set_clause} WHERE {where_clause}"

        with self._db.cursor() as cursor:
            cursor.execute(query, values + where_params)
            self._db.commit()
            return cursor.rowcount > 0

    async def update_by_query(self, query: dict, update_data):
        """Updates a row by query in MySQL."""
        try:
            return self._update_by_query_sync(query, update_data)
        except Exception as e:
            raise HttpException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    def _update_by_query_sync(self, query: dict, update_data):
        """Synchronous implementation of update_by_query."""
        update_data = self._to_mysql(update_data)
        set_clause = ", ".join([f"{key} = %s" for key in update_data.keys()])
        values = list(update_data.values())

        where_clause, where_params = self._build_where_clause(query)

        query_str = f"UPDATE {self._collection_name} SET {set_clause}"
        if where_clause:
            query_str += f" WHERE {where_clause}"

        with self._db.cursor() as cursor:
            cursor.execute(query_str, values + where_params)
            self._db.commit()
            return cursor.rowcount > 0

    async def delete(self, item_id: Union[str, int]):
        """Delete a row in MySQL."""
        try:
            return self._delete_sync(item_id)
        except Exception as e:
            raise HttpException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    def _delete_sync(self, item_id: Union[str, int]):
        """Synchronous implementation of delete."""
        filter_query = {"id": item_id}
        where_clause, params = self._build_where_clause(filter_query)

        query = f"DELETE FROM {self._collection_name} WHERE {where_clause}"

        with self._db.cursor() as cursor:
            cursor.execute(query, params)
            self._db.commit()
            return cursor.rowcount > 0

    async def insert_many(self, data_list):
        """Insert multiple rows in MySQL with tenant_id filter if necessary."""
        try:
            return self._insert_many_sync(data_list)
        except Exception as e:
            raise HttpException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    def _insert_many_sync(self, data_list):
        """Synchronous implementation of insert_many."""
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
        with self._db.cursor() as cursor:
            for values in values_list:
                cursor.execute(query, values)
                inserted_ids.append(cursor.lastrowid)
            self._db.commit()

        return inserted_ids
