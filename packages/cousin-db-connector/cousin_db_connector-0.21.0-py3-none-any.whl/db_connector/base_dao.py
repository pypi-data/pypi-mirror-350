from abc import ABC, abstractmethod
from typing import Any, List, Optional, Dict, Union


class BaseDAO(ABC):
    def __init__(self, db, collection_name: str, tenant_id: Optional[str] = None, tenant_field: str = "tenant_id", is_deleted_field: Optional[str] = "is_deleted"):
        """
        Constructor base for all DAOs.

        :param db: Connection to the database.
        :param collection_name: Name of the collection in the database.
        :param tenant_id: ID del tenant para lógica multi-tenant.
        :param tenant_field: Name of the field used for tenant filtering (default: "tenant_id").
        :param is_deleted_field: Name of the field used for deletion filtering (default: "is_deleted"). If None, no deletion filter will be applied.
        """
        self._db = db
        self._collection_name = collection_name
        self._tenant_id = tenant_id  #If None, no tenant filter will be applied.
        self._tenant_field = tenant_field
        self._is_deleted_field = is_deleted_field

    def _apply_tenant_filter(self, query: dict) -> dict:
        """Apply the tenant filter to the query using custom field names."""
        if self._tenant_id:
            query[self._tenant_field] = self._tenant_id
            if self._is_deleted_field:
                query[self._is_deleted_field] = False
        return query

    @abstractmethod
    async def insert(self, data: dict) -> Any:
        """Insert a new document in the database."""
        pass

    @abstractmethod
    async def find_all(self) -> List[dict]:
        """Get all documents from the database."""
        pass

    @abstractmethod
    async def find_all_by_query(self, filter_query: dict) -> List[dict]:
        """Find all documents by query in the database."""
        pass

    @abstractmethod
    async def find_by_id(self, item_id: Any) -> dict:
        """Find a document by ID in the database."""
        pass

    @abstractmethod
    async def find_by_filter(self, filter_query: dict) -> dict:
        """Find a document by filter in the database."""
        pass

    @abstractmethod
    async def find_paginated(self, filter_query: dict, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """Retrieve paginated documents from the database."""
        pass

    @abstractmethod
    async def update(self, item_id: Any, update_data: dict) -> bool:
        """Update a document in the database."""
        pass

    @abstractmethod
    async def update_by_query(self, query: dict, update_data: dict) -> bool:
        """Update a document by query in the database."""
        pass

    @abstractmethod
    async def delete(self, item_id: Any) -> bool:
        """Delete a document in the database."""
        pass

    @abstractmethod
    async def insert_many(self, data_list: dict) -> Any:
        """Delete a document in the database."""
        pass