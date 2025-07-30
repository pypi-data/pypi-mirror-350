import datetime

import pytest

from util_common.mongo_util import AsyncMongoTool


@pytest.fixture
def mongo_settings():
    """Fixture providing test MongoDB connection settings."""
    return {
        "username": "test_user",
        "password": "test_pass",
        "host": "localhost:27017",
        "db_name": "test_db",
        "replica_set": "rs0",
        "auth_source": "admin",
    }


class MockAdmin:
    async def command(self, cmd):
        if cmd == 'ping':
            return {"ok": 1}
        return None


class MockCollection:
    async def find_one(self, query, projection=None):
        return {"_id": "123", "name": "test"}

    def find(self, filter, projection=None):
        class MockCursor:
            async def __aiter__(self):
                docs = [{"_id": "1", "name": "doc1"}, {"_id": "2", "name": "doc2"}]
                for doc in docs:
                    yield doc

            def sort(self, *args):
                return self

            def limit(self, *args):
                return self

            def skip(self, *args):
                return self

        return MockCursor()

    async def count_documents(self, filter):
        return 2

    async def insert_one(self, document):
        class MockResult:
            acknowledged = True
            inserted_id = "123"

        return MockResult()

    async def insert_many(self, documents):
        class MockResult:
            acknowledged = True
            inserted_ids = ["123", "124"]

        return MockResult()

    async def update_one(self, filter, update, upsert=False):
        class MockResult:
            matched_count = 1
            modified_count = 1
            upserted_id = None if not upsert else "123"

        return MockResult()

    async def update_many(self, filter, update):
        class MockResult:
            matched_count = 2
            modified_count = 2

        return MockResult()

    async def delete_one(self, filter):
        class MockResult:
            deleted_count = 1

        return MockResult()


class MockDatabase:
    def __getitem__(self, name):
        return MockCollection()


class MockMotorClient:
    def __init__(self, *args, **kwargs):
        self.admin = MockAdmin()
        self._closed = False

    def __getitem__(self, name):
        return MockDatabase()

    def close(self):
        self._closed = True


@pytest.mark.asyncio
class TestAsyncMongoTool:
    """Test suite for AsyncMongoTool."""

    async def test_singleton_pattern(self, mongo_settings, monkeypatch):
        """Test that AsyncMongoTool follows singleton pattern."""
        monkeypatch.setattr("motor.motor_asyncio.AsyncIOMotorClient", MockMotorClient)

        instance1 = AsyncMongoTool.instance(**mongo_settings)
        instance2 = AsyncMongoTool.instance()

        assert instance1 is instance2

    async def test_connection_closing(self, mongo_settings, monkeypatch):
        """Test MongoDB connection is properly closed."""
        # This test needs to directly patch the client attribute instead of patching the import
        monkeypatch.setattr("motor.motor_asyncio.AsyncIOMotorClient", MockMotorClient)

        mongo_tool = AsyncMongoTool.instance(**mongo_settings)
        await mongo_tool.close()

        assert mongo_tool.client is None, "client should be None after closing"

    async def test_find_one(self, mongo_settings, monkeypatch):
        """Test find_one operation."""
        # Create a mock instance first, then monkeypatch internal _db attribute
        monkeypatch.setattr("motor.motor_asyncio.AsyncIOMotorClient", MockMotorClient)
        mongo_tool = AsyncMongoTool.instance(**mongo_settings)
        mongo_tool._db = MockDatabase()  # type: ignore

        result = await mongo_tool.find_one(
            "test_collection", filters={"name": "test"}, projection_fields={"_id": 0}
        )

        assert result is not None
        assert result["name"] == "test"

    async def test_find_many(self, mongo_settings, monkeypatch):
        """Test find_many operation."""
        monkeypatch.setattr("motor.motor_asyncio.AsyncIOMotorClient", MockMotorClient)
        mongo_tool = AsyncMongoTool.instance(**mongo_settings)
        mongo_tool._db = MockDatabase()  # type: ignore

        results = await mongo_tool.find_many(
            "test_collection", filter={"name": "test"}, sort=[("name", 1)], limit=2
        )

        assert len(results) == 2
        assert results[0]["name"] == "doc1"

    async def test_find_total(self, mongo_settings, monkeypatch):
        """Test find_total operation."""
        monkeypatch.setattr("motor.motor_asyncio.AsyncIOMotorClient", MockMotorClient)
        mongo_tool = AsyncMongoTool.instance(**mongo_settings)
        mongo_tool._db = MockDatabase()  # type: ignore

        total = await mongo_tool.find_total("test_collection", filter={"name": "test"})

        assert total == 2

    async def test_find_page(self, mongo_settings, monkeypatch):
        """Test find_page operation."""
        monkeypatch.setattr("motor.motor_asyncio.AsyncIOMotorClient", MockMotorClient)
        mongo_tool = AsyncMongoTool.instance(**mongo_settings)
        mongo_tool._db = MockDatabase()  # type: ignore

        results = await mongo_tool.find_page(
            "test_collection", filter={"name": "test"}, skip=0, size=2
        )

        assert len(results) == 2

    async def test_insert_one(self, mongo_settings, monkeypatch):
        """Test insert_one operation."""
        monkeypatch.setattr("motor.motor_asyncio.AsyncIOMotorClient", MockMotorClient)
        mongo_tool = AsyncMongoTool.instance(**mongo_settings)
        mongo_tool._db = MockDatabase()  # type: ignore

        success, error = await mongo_tool.insert_one("test_collection", {"name": "test_doc"})

        assert success is True
        assert error == ""

    async def test_insert_one_with_expiry(self, mongo_settings, monkeypatch):
        """Test insert_one with expiry days."""
        inserted_doc = {}

        class CustomMockCollection:
            async def insert_one(self, document):
                nonlocal inserted_doc
                inserted_doc = document

                class MockResult:
                    acknowledged = True

                return MockResult()

        class CustomMockDB:
            def __getitem__(self, name):
                return CustomMockCollection()

        monkeypatch.setattr("motor.motor_asyncio.AsyncIOMotorClient", MockMotorClient)
        mongo_tool = AsyncMongoTool.instance(**mongo_settings)
        mongo_tool._db = CustomMockDB()  # type: ignore

        await mongo_tool.insert_one("test_collection", {"name": "expiring_doc"}, days=7)

        assert "expireAt" in inserted_doc
        assert isinstance(inserted_doc["expireAt"], datetime.datetime)

    async def test_insert_many(self, mongo_settings, monkeypatch):
        """Test insert_many operation."""
        monkeypatch.setattr("motor.motor_asyncio.AsyncIOMotorClient", MockMotorClient)
        mongo_tool = AsyncMongoTool.instance(**mongo_settings)
        mongo_tool._db = MockDatabase()  # type: ignore

        success, error = await mongo_tool.insert_many(
            "test_collection", [{"name": "doc1"}, {"name": "doc2"}]
        )

        assert success is True
        assert error == ""

    async def test_update_one(self, mongo_settings, monkeypatch):
        """Test update_one operation."""
        monkeypatch.setattr("motor.motor_asyncio.AsyncIOMotorClient", MockMotorClient)
        mongo_tool = AsyncMongoTool.instance(**mongo_settings)
        mongo_tool._db = MockDatabase()  # type: ignore

        success = await mongo_tool.update_one(
            "test_collection", filter={"name": "test"}, update_data={"status": "updated"}
        )

        assert success is True

    async def test_update_many(self, mongo_settings, monkeypatch):
        """Test update_many operation."""
        monkeypatch.setattr("motor.motor_asyncio.AsyncIOMotorClient", MockMotorClient)
        mongo_tool = AsyncMongoTool.instance(**mongo_settings)
        mongo_tool._db = MockDatabase()  # type: ignore

        success = await mongo_tool.update_many(
            "test_collection", filter={"name": "test"}, update_data={"$set": {"status": "updated"}}
        )

        assert success is True

    async def test_delete_one(self, mongo_settings, monkeypatch):
        """Test delete_one operation."""
        monkeypatch.setattr("motor.motor_asyncio.AsyncIOMotorClient", MockMotorClient)
        mongo_tool = AsyncMongoTool.instance(**mongo_settings)
        mongo_tool._db = MockDatabase()  # type: ignore

        success = await mongo_tool.delete_one("test_collection", filter={"name": "test"})

        assert success is True

    async def test_is_connected(self, mongo_settings, monkeypatch):
        """Test is_connected method."""
        monkeypatch.setattr("motor.motor_asyncio.AsyncIOMotorClient", MockMotorClient)

        mongo_tool = AsyncMongoTool.instance(**mongo_settings)

        assert mongo_tool.is_connected() is True

        await mongo_tool.close()

        assert mongo_tool.is_connected() is False

    async def test_ensure_connected(self, mongo_settings, monkeypatch):
        """Test ensure_connected method."""
        ping_called = False

        class PingMockAdmin:
            async def command(self, cmd):
                nonlocal ping_called
                if cmd == 'ping':
                    ping_called = True
                return {"ok": 1}

        class PingMockClient(MockMotorClient):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.admin = PingMockAdmin()

        # Set up initial instance
        monkeypatch.setattr("motor.motor_asyncio.AsyncIOMotorClient", PingMockClient)
        mongo_tool = AsyncMongoTool.instance(**mongo_settings)
        await mongo_tool.close()

        assert mongo_tool.is_connected() is False

        # Force reconnect to avoid actual MongoDB connection
        def mock_connect():
            mongo_tool.client = PingMockClient()  # type: ignore
            mongo_tool._db = MockDatabase()  # type: ignore

        monkeypatch.setattr(mongo_tool, "connect", mock_connect)

        await mongo_tool.ensure_connected()

        assert mongo_tool.is_connected() is True
        assert ping_called is True
