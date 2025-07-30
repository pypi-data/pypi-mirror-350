import datetime
from typing import Dict, List, Optional

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError

from util_common.singleton import SingletonMixin


class AsyncMongoTool(SingletonMixin):
    def __init__(
        self,
        username: str,
        password: str,
        host: str,
        db_name: str,
        replica_set: str | None = None,
        auth_source: str | None = None,
    ):
        self.client: AsyncIOMotorClient | None = None
        self.username = username
        self.password = password
        self.host = host
        self.db_name = db_name
        self.replica_set = replica_set
        self.auth_source = auth_source
        self.connect()

    def connect(self):
        url = (
            f"mongodb://{self.username}:{self.password}@{self.host}/"
            f"?replicaSet={self.replica_set}&authSource={self.auth_source}"
        )
        self.client = AsyncIOMotorClient(url)
        self._db = self.client[self.db_name]

    async def close(self) -> None:
        """Close the MongoDB connection if it exists."""
        if self.client:
            self.client.close()
            self.client = None  # Set to None to indicate it's closed

    async def find_one(
        self,
        collection_name: str,
        filters: Optional[Dict] = None,
        projection_fields: Optional[Dict] = None,
    ) -> Optional[Dict]:
        """
        查询单条数据
        :param collection_name:
        :param filters:
        :param projection_fields: 查询过滤条件  {"_id": 0, "expireAt": 0}
        :return:
        """
        collection = self._db[collection_name]
        query = {}
        # 如果提供了过滤条件，则更新查询条件
        if filters:
            query.update(filters)
        result = await collection.find_one(query, projection=projection_fields)
        return result

    async def find_page(
        self, collection_name: str, filter: Dict, skip: int, size: int
    ) -> List[Dict]:
        collection = self._db[collection_name]
        query = collection.find(filter)
        query = query.skip(skip).limit(size)
        result = []
        async for doc in query:
            result.append(doc)
        return result

    async def find_many(
        self,
        collection_name: str,
        filter: Dict,
        projection_fields: Optional[Dict] = None,
        sort: Optional[List[tuple]] = None,
        limit: Optional[int] = None,
    ) -> List[Dict]:
        collection = self._db[collection_name]
        query = collection.find(filter, projection=projection_fields)
        # 如果提供了排序条件，则应用排序
        if sort:
            query = query.sort(sort)

        # 如果提供了限制条数，则应用限制
        if limit:
            query = query.limit(limit)
        result = []
        async for doc in query:
            result.append(doc)
        return result

    async def find_total(self, collection_name: str, filter: Dict) -> int:
        collection = self._db[collection_name]
        total = await collection.count_documents(filter)
        return total

    async def insert_one(
        self, collection_name: str, document: Dict, days: Optional[int] = None
    ) -> tuple[bool, str]:
        collection = self._db[collection_name]
        try:
            # 仅当 days 参数被提供且大于0时，才添加过期时间
            if days is not None and days > 0:
                expire_at = datetime.datetime.now() + datetime.timedelta(days=days)
                document['expireAt'] = expire_at
            result = await collection.insert_one(document)
            return result.acknowledged, ""
        except Exception as e:
            print(f"Insert operation failed: {e}")
            return False, str(e)

    async def insert_many(self, collection_name: str, documents: List[Dict]):
        collection = self._db[collection_name]
        try:
            result = await collection.insert_many(documents)
            return result.acknowledged, ""
        except PyMongoError as e:
            print(f"Insert many operation failed: {e}")
            return False, str(e)

    async def update_one(
        self, collection_name: str, filter: Dict, update_data: Dict, upsert=True
    ) -> bool:
        """
        更新数据基于复杂过滤条件
        :param collection_name: 集合名称
        :param filter: 用于过滤文档的字典
        :param update_data: 包含更新数据的字典
        :param upsert: 如果设置为 True，当找不到匹配的文档时会插入新文档
        :return: 更新或插入操作的成功与否
        """
        collection = self._db[collection_name]
        try:
            result = await collection.update_one(
                filter=filter,
                update={'$set': update_data},
                upsert=upsert,
            )
            return result.matched_count > 0 or result.upserted_id is not None
        except KeyError:
            print("Missing required fields in filter or update_data")
            return False
        except PyMongoError as e:
            print(f"Update operation failed: {e}")
            return False

    async def update_many(self, collection_name: str, filter: Dict, update_data: Dict) -> bool:
        collection = self._db[collection_name]

        try:
            result = await collection.update_many(filter, update_data)
            return result.matched_count > 0
        except PyMongoError as e:
            print(f"Update many operation failed: {e}")
            return False

    async def delete_one(self, collection_name: str, filter: Dict) -> bool:
        collection = self._db[collection_name]

        try:
            result = await collection.delete_one(filter)
            return result.deleted_count > 0
        except PyMongoError as e:
            print(f"Delete operation failed: {e}")
            return False

    def is_connected(self) -> bool:
        """Check if the client is connected."""
        return self.client is not None

    async def ensure_connected(self):
        """Ensure the client is connected, reconnecting if necessary."""
        if not self.is_connected():
            self.connect()
            # Optionally: Perform a simple operation to test the connection
            try:
                if self.client:
                    await self.client.admin.command('ping')
            except Exception as e:
                self.client = None
                raise ConnectionError(f"Failed to connect to MongoDB: {e}")
