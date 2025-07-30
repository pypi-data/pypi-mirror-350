from math import ceil
from fastapi import status
from typing import Union, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from ..base_dao import BaseDAO
from ..exceptions import HttpException

class AsyncMongoDAO(BaseDAO):
    def __init__(self, db: AsyncIOMotorDatabase, collection_name: str, entity_cls=None, tenant_id: str = None, tenant_field: str = "tenant_id", is_deleted_field: Optional[str] = "is_deleted"):
        """
        DAO for MongoDB with async support.

        :param db: Connection to the database.
        :param collection_name: Name of the collection in the database.
        :param entity_cls: Entity class for automatic serialization/deserialization.
        :param tenant_id: Tenant ID for multi-tenant logic.
        :param tenant_field: Name of the field used for tenant filtering (default: "tenant_id").
        :param is_deleted_field: Name of the field used for deletion filtering (default: "is_deleted"). If None, no deletion filter will be applied.
        """
        super().__init__(db, collection_name, tenant_id, tenant_field, is_deleted_field)
        self.entity_cls = entity_cls

    def _from_mongo(self, doc: dict):
        """Convert MongoDB document to an entity instance."""
        if doc is None:
            return None
        doc["id"] = str(doc.pop("_id", None))
        return self.entity_cls(**doc) if self.entity_cls else doc

    @staticmethod
    def _to_mongo(entity):
        """Convert an entity instance to a MongoDB document."""
        if isinstance(entity, dict):
            return entity
        data = entity.model_dump(by_alias=True, exclude={"id"})
        if "id" in data:
            data["_id"] = ObjectId(data.pop("id"))
        return data

    async def insert(self, data, session=None):
        """Insert a new document in MongoDB with tenant_id filter if necessary."""
        try:
            data = self._apply_tenant_filter(self._to_mongo(data))
            result = await self._db[self._collection_name].insert_one(data, session=session)
            return str(result.inserted_id)
        except Exception as e:
            raise HttpException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    async def insert_many(self, data_list: list[dict], session=None) -> list[str]:
        """Insert multiple documents in MongoDB."""
        try:
            data_list = [self._apply_tenant_filter(self._to_mongo(data)) for data in data_list]
            result = await self._db[self._collection_name].insert_many(data_list, session=session)
            return [str(inserted_id) for inserted_id in result.inserted_ids]
        except Exception as e:
            raise HttpException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    async def find_all(self):
        """Get all documents in MongoDB without filter"""
        try:
            query = self._apply_tenant_filter({})
            cursor = self._db[self._collection_name].find(query)
            documents = await cursor.to_list(length=None)
            return [self._from_mongo(doc) for doc in documents]
        except Exception as e:
            raise HttpException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    async def find_all_by_query(self, filter_query: dict):
        """Find all document by query without tenant id"""
        try:
            query = self._apply_tenant_filter(filter_query)
            cursor = self._db[self._collection_name].find(query)
            documents = await cursor.to_list(length=None)
            return [self._from_mongo(doc) for doc in documents]
        except Exception as e:
            raise HttpException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    async def find_by_id(self, item_id: Union[str, int]):
        """Search for a document by ID in MongoDB."""
        try:
            if isinstance(item_id, int):
                filter_query = {"_id": item_id}
            else:
                filter_query = {"_id": ObjectId(item_id)}

            query = self._apply_tenant_filter(filter_query)
            document = await self._db[self._collection_name].find_one(query)
            return self._from_mongo(document) if document else None
        except Exception as e:
            raise HttpException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    async def find_by_filter(self, filter_query: dict):
        """Search for a document by query in MongoDB."""
        try:
            query = self._apply_tenant_filter(filter_query)
            document = await self._db[self._collection_name].find_one(query)
            return self._from_mongo(document) if document else None
        except Exception as e:
            raise HttpException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    async def find_paginated(self, filter_query: dict, page: int = 1, page_size: int = 10) -> dict:
        """Retrieve paginated documents."""
        try:
            query = self._apply_tenant_filter(filter_query)
            total_items = await self._db[self._collection_name].count_documents(query)
            total_pages = ceil(total_items / page_size)
            skip = (page - 1) * page_size

            cursor = self._db[self._collection_name].find(query).skip(skip).limit(page_size)
            items = [self._from_mongo(doc) for doc in await cursor.to_list(length=page_size)]

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

    async def update(self, item_id: str, update_data, session=None):
        """Updates a document in MongoDB."""
        try:
            query = self._apply_tenant_filter({"_id": ObjectId(item_id)})
            update_data = self._to_mongo(update_data)
            result = await self._db[self._collection_name].update_one(query, {"$set": update_data}, session=session)
            return result.modified_count > 0
        except Exception as e:
            raise HttpException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    async def update_by_query(self, query: dict, update_data, session=None):
        """Updates a document by query in MongoDB."""
        try:
            query = self._apply_tenant_filter(query)
            update_data = self._to_mongo(update_data)
            result = await self._db[self._collection_name].update_one(query, {"$set": update_data}, session=session)
            return result.modified_count > 0
        except Exception as e:
            raise HttpException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    async def update_many(self, filter_query: dict, update_data, session=None) :
        """Update multiple documents in MongoDB."""
        try:
            query = self._apply_tenant_filter(filter_query)
            update_data = self._to_mongo(update_data)
            result = await self._db[self._collection_name].update_many(query, {"$set": update_data}, session=session)
            return result.modified_count > 0
        except Exception as e:
            raise HttpException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))

    async def delete(self, item_id: str, session=None):
        """Delete a document in MongoDB."""
        try:
            query = self._apply_tenant_filter({"_id": ObjectId(item_id)})
            result = await self._db[self._collection_name].delete_one(query, session=session)
            return result.deleted_count > 0
        except Exception as e:
            raise HttpException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))