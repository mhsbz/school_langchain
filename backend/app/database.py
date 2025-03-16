from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
import logging
from typing import Optional
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取MongoDB连接字符串
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "rag_db")

class Database:
    client: Optional[AsyncIOMotorClient] = None
    db = None

    @classmethod
    async def connect_to_mongodb(cls):
        logging.info("正在连接到MongoDB...")
        try:
            cls.client = AsyncIOMotorClient(MONGODB_URL)
            # 验证连接
            await cls.client.admin.command('ping')
            cls.db = cls.client[MONGODB_DB_NAME]
            logging.info("成功连接到MongoDB")
        except ConnectionFailure as e:
            logging.error(f"MongoDB连接失败: {e}")
            raise

    @classmethod
    async def close_mongodb_connection(cls):
        logging.info("关闭MongoDB连接...")
        if cls.client:
            cls.client.close()
            logging.info("MongoDB连接已关闭")

    @classmethod
    def get_db(cls):
        return cls.db