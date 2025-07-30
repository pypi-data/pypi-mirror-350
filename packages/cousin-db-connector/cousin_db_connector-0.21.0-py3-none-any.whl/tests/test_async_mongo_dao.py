import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock
from bson.objectid import ObjectId
from fastapi.openapi.models import Contact

from db_connector.mongo.async_mongo_dao import AsyncMongoDAO
from db_connector.exceptions import HttpException

@pytest_asyncio.fixture
async def mock_db():
    db = MagicMock()
    db["contacts"].insert_one = AsyncMock(return_value=MagicMock(inserted_id="123456789"))
    db["contacts"].find_one = AsyncMock(return_value={"_id": ObjectId("656ad08c4f1a2c48b0e598b5"), "name": "John Doe"})
    db["contacts"].count_documents = AsyncMock(return_value=50)
    db["contacts"].update_one = AsyncMock(return_value=MagicMock(modified_count=1))
    db["contacts"].delete_one = AsyncMock(return_value=MagicMock(deleted_count=1))

    async def find_mock(*args, **kwargs):
        length = kwargs.get("length", None)
        return [{"_id": ObjectId(f"656ad08c4f1a2c48b0e598b{i}"), "name": f"User {i}"} for i in range(length or 10)]

    class MockCursor:
        def __init__(self):
            self._skip = 0
            self._limit = 0

        def skip(self, count):
            self._skip = count
            return self

        def limit(self, count):
            self._limit = count
            return self

        async def to_list(self, length=None):
            results = await find_mock(length=length if length is not None else self._limit)
            return results[self._skip:self._skip + (self._limit or length or len(results))]

    db["contacts"].find = MagicMock(return_value=MockCursor())

    return db

@pytest.mark.asyncio
async def test_insert(mock_db):
    dao = AsyncMongoDAO(mock_db, "contacts", entity_cls=Contact)
    data = {"name": "John Doe", "email": "johndoe@example.com"}
    inserted_id = await dao.insert(data)

    assert inserted_id == "123456789"

@pytest.mark.asyncio
async def test_find_by_id(mock_db):
    dao = AsyncMongoDAO(mock_db, "contacts", entity_cls=Contact)
    result = await dao.find_by_id("656ad08c4f1a2c48b0e598b5")

    assert result is not None
    assert isinstance(result, Contact)
    assert result.id == "656ad08c4f1a2c48b0e598b5"

@pytest.mark.asyncio
async def test_find_all(mock_db):
    dao = AsyncMongoDAO(mock_db, "contacts", entity_cls=Contact)

    result = await dao.find_all()

    assert len(result) == 10
    assert result[0].model_dump()["name"] == "User 0"

@pytest.mark.asyncio
async def test_find_paginated(mock_db):
    dao = AsyncMongoDAO(mock_db, "contacts", entity_cls=Contact)
    page = 2
    page_size = 5
    result = await dao.find_paginated({}, page=page, page_size=page_size)

    assert isinstance(result, dict)
    assert "results" in result
    assert "pagination" in result
    assert len(result["results"]) == 0
    assert result["pagination"]["current_page"] == page
    assert result["pagination"]["page_size"] == page_size

@pytest.mark.asyncio
async def test_update(mock_db):
    dao = AsyncMongoDAO(mock_db, "contacts", entity_cls=Contact)
    item_id = "656ad08c4f1a2c48b0e598b5"
    update_data = {"name": "Updated Name"}

    result = await dao.update(item_id, update_data)
    assert result is True

@pytest.mark.asyncio
async def test_delete(mock_db):
    dao = AsyncMongoDAO(mock_db, "contacts", entity_cls=Contact)
    item_id = "656ad08c4f1a2c48b0e598b5"

    result = await dao.delete(item_id)
    assert result is True

@pytest.mark.asyncio
async def test_find_by_id_not_found(mock_db):
    mock_db["contacts"].find_one = AsyncMock(return_value=None)
    dao = AsyncMongoDAO(mock_db, "contacts", entity_cls=Contact)

    result = await dao.find_by_id("656ad08c4f1a2c48b0e598b9")
    assert result is None

@pytest.mark.asyncio
async def test_update_not_found(mock_db):
    mock_db["contacts"].update_one = AsyncMock(return_value=MagicMock(modified_count=0))
    dao = AsyncMongoDAO(mock_db, "contacts", entity_cls=Contact)

    result = await dao.update("656ad08c4f1a2c48b0e598b9", {"name": "New Name"})
    assert result is False

@pytest.mark.asyncio
async def test_delete_not_found(mock_db):
    mock_db["contacts"].delete_one = AsyncMock(return_value=MagicMock(deleted_count=0))
    dao = AsyncMongoDAO(mock_db, "contacts", entity_cls=Contact)

    result = await dao.delete("656ad08c4f1a2c48b0e598b9")
    assert result is False

@pytest.mark.asyncio
async def test_insert_exception(mock_db):
    mock_db["contacts"].insert_one = AsyncMock(side_effect=Exception("DB error"))
    dao = AsyncMongoDAO(mock_db, "contacts", entity_cls=Contact)

    with pytest.raises(HttpException):
        await dao.insert({"name": "Error Case"})

@pytest.mark.asyncio
async def test_find_all_exception(mock_db):

    mock_db["contacts"].find = MagicMock(side_effect=Exception("DB error"))
    dao = AsyncMongoDAO(mock_db, "contacts", entity_cls=Contact)

    with pytest.raises(HttpException):
        await dao.find_all()


@pytest.mark.asyncio
async def test_find_by_filter_found(mock_db):
    dao = AsyncMongoDAO(mock_db, "contacts", entity_cls=None)
    filter_query = {"name": "John Doe"}
    mock_document = {"_id": ObjectId(), "name": "John Doe"}

    mock_db["contacts"].find_one = AsyncMock(return_value=mock_document)

    result = await dao.find_by_filter(filter_query)

    assert result is not None
    assert result["name"] == "John Doe"

@pytest.mark.asyncio
async def test_find_by_filter_not_found(mock_db):
    dao = AsyncMongoDAO(mock_db, "contacts", entity_cls=None)
    filter_query = {"name": "Nonexistent User"}

    mock_db["contacts"].find_one = AsyncMock(return_value=None)

    result = await dao.find_by_filter(filter_query)

    assert result is None

@pytest.mark.asyncio
async def test_find_by_filter_exception(mock_db):
    dao = AsyncMongoDAO(mock_db, "contacts", entity_cls=None)
    filter_query = {"name": "John Doe"}

    mock_db["contacts"].find_one = AsyncMock(side_effect=Exception("DB error"))

    with pytest.raises(HttpException):
        await dao.find_by_filter(filter_query)


@pytest.mark.asyncio
async def test_find_all_by_query(mock_db):
    dao = AsyncMongoDAO(mock_db, "contacts", entity_cls=Contact)
    filter_query = {"name": "John Doe"}

    result = await dao.find_all_by_query(filter_query)

    assert len(result) == 10
    assert result[0].model_dump()["name"] == "User 0"


@pytest.mark.asyncio
async def test_find_all_by_query_exception(mock_db):
    dao = AsyncMongoDAO(mock_db, "contacts", entity_cls=Contact)
    filter_query = {"name": "John Doe"}

    mock_db["contacts"].find = MagicMock(side_effect=Exception("DB error"))

    with pytest.raises(HttpException):
        await dao.find_all_by_query(filter_query)


@pytest.mark.asyncio
async def test_update_by_query(mock_db):
    dao = AsyncMongoDAO(mock_db, "contacts", entity_cls=Contact)
    query = {"name": "John Doe"}
    update_data = {"name": "Updated Name"}

    result = await dao.update_by_query(query, update_data)
    assert result is True


@pytest.mark.asyncio
async def test_update_by_query_not_found(mock_db):
    mock_db["contacts"].update_one = AsyncMock(return_value=MagicMock(modified_count=0))
    dao = AsyncMongoDAO(mock_db, "contacts", entity_cls=Contact)
    query = {"name": "Nonexistent User"}
    update_data = {"name": "Updated Name"}

    result = await dao.update_by_query(query, update_data)
    assert result is False


@pytest.mark.asyncio
async def test_update_by_query_exception(mock_db):
    dao = AsyncMongoDAO(mock_db, "contacts", entity_cls=Contact)
    query = {"name": "John Doe"}
    update_data = {"name": "Updated Name"}

    mock_db["contacts"].update_one = AsyncMock(side_effect=Exception("DB error"))

    with pytest.raises(HttpException):
        await dao.update_by_query(query, update_data)


@pytest.mark.asyncio
async def test_insert_many(mock_db):
    mock_db["contacts"].insert_many = AsyncMock(return_value=MagicMock(inserted_ids=["id1", "id2", "id3"]))
    dao = AsyncMongoDAO(mock_db, "contacts", entity_cls=Contact)
    data_list = [
        {"name": "User 1", "email": "user1@example.com"},
        {"name": "User 2", "email": "user2@example.com"},
        {"name": "User 3", "email": "user3@example.com"}
    ]

    result = await dao.insert_many(data_list)

    assert len(result) == 3
    assert result == ["id1", "id2", "id3"]


@pytest.mark.asyncio
async def test_insert_many_exception(mock_db):
    mock_db["contacts"].insert_many = AsyncMock(side_effect=Exception("DB error"))
    dao = AsyncMongoDAO(mock_db, "contacts", entity_cls=Contact)
    data_list = [
        {"name": "User 1", "email": "user1@example.com"},
        {"name": "User 2", "email": "user2@example.com"}
    ]

    with pytest.raises(HttpException):
        await dao.insert_many(data_list)


@pytest.mark.asyncio
async def test_update_many(mock_db):
    mock_db["contacts"].update_many = AsyncMock(return_value=MagicMock(modified_count=3))
    dao = AsyncMongoDAO(mock_db, "contacts", entity_cls=Contact)
    filter_query = {"active": True}
    update_data = {"status": "active"}

    result = await dao.update_many(filter_query, update_data)

    assert result is True


@pytest.mark.asyncio
async def test_update_many_not_found(mock_db):
    mock_db["contacts"].update_many = AsyncMock(return_value=MagicMock(modified_count=0))
    dao = AsyncMongoDAO(mock_db, "contacts", entity_cls=Contact)
    filter_query = {"active": False}
    update_data = {"status": "inactive"}

    result = await dao.update_many(filter_query, update_data)

    assert result is False


@pytest.mark.asyncio
async def test_update_many_exception(mock_db):
    mock_db["contacts"].update_many = AsyncMock(side_effect=Exception("DB error"))
    dao = AsyncMongoDAO(mock_db, "contacts", entity_cls=Contact)
    filter_query = {"active": True}
    update_data = {"status": "active"}

    with pytest.raises(HttpException):
        await dao.update_many(filter_query, update_data)
