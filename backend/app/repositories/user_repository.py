from bson import ObjectId
from datetime import datetime
from typing import List, Optional

from ..database import Database
from ..models.user import UserInDB, User

class UserRepository:
    """
    用户数据访问层，负责与MongoDB数据库交互
    """
    
    collection_name = "users"
    
    @classmethod
    async def get_collection(cls):
        """
        获取用户集合
        """
        db = Database.get_db()
        return db[cls.collection_name]
    
    @classmethod
    async def find_by_username(cls, username: str) -> Optional[UserInDB]:
        """
        根据用户名查找用户
        """
        collection = await cls.get_collection()
        user_data = await collection.find_one({"username": username})
        if user_data:
            return UserInDB(**user_data)
        return None
    
    @classmethod
    async def find_by_id(cls, user_id: str) -> Optional[UserInDB]:
        """
        根据ID查找用户
        """
        collection = await cls.get_collection()
        user_data = await collection.find_one({"_id": ObjectId(user_id)})
        if user_data:
            return UserInDB(**user_data)
        return None
    
    @classmethod
    async def create(cls, user_data: dict) -> UserInDB:
        """
        创建新用户
        """
        collection = await cls.get_collection()
        user_data["created_at"] = datetime.utcnow()
        user_data["updated_at"] = datetime.utcnow()
        
        result = await collection.insert_one(user_data)
        user_data["_id"] = result.inserted_id
        
        return UserInDB(**user_data)
    
    @classmethod
    async def update(cls, user_id: str, update_data: dict) -> Optional[UserInDB]:
        """
        更新用户信息
        """
        collection = await cls.get_collection()
        update_data["updated_at"] = datetime.utcnow()
        
        await collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        
        return await cls.find_by_id(user_id)
    
    @classmethod
    async def delete(cls, user_id: str) -> bool:
        """
        删除用户
        """
        collection = await cls.get_collection()
        result = await collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0
    
    @classmethod
    async def list_all(cls) -> List[UserInDB]:
        """
        获取所有用户
        """
        collection = await cls.get_collection()
        users = []
        async for user in collection.find():
            users.append(UserInDB(**user))
        return users