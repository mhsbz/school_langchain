from bson import ObjectId
from datetime import datetime
from typing import List, Optional

from ..database import Database
from ..models.chat import ChatMessage, ChatHistory

class ChatRepository:
    """
    聊天数据访问层，负责与MongoDB数据库交互
    """
    
    collection_name = "chat_messages"
    conversation_collection = "conversations"
    
    @classmethod
    async def get_collection(cls):
        """
        获取聊天消息集合
        """
        db = Database.get_db()
        return db[cls.collection_name]
    
    @classmethod
    async def create_message(cls, message_data: dict) -> ChatMessage:
        """
        创建新的聊天消息
        """
        collection = await cls.get_collection()
        result = await collection.insert_one(message_data)
        message_data["_id"] = result.inserted_id
        
        return ChatMessage(**message_data)
    
    @classmethod
    async def get_user_chat_history(cls, user_id: str, conversation_id: Optional[str] = None) -> List[ChatMessage]:
        """
        获取用户的聊天历史
        如果提供了conversation_id，则只获取特定对话的消息
        """
        collection = await cls.get_collection()
        messages = []
        
        # 构建查询条件
        query = {"user_id": user_id}
        if conversation_id:
            query["conversation_id"] = conversation_id
            
        cursor = collection.find(query).sort("timestamp", 1)
        
        async for message in cursor:
            messages.append(ChatMessage(**message))
            
        return messages
        
    @classmethod
    async def get_user_conversations(cls, user_id: str) -> List[dict]:
        """
        获取用户的所有对话
        """
        db = Database.get_db()
        collection = db[cls.conversation_collection]
        conversations = []
        
        cursor = collection.find({"user_id": user_id}).sort("created_at", -1)
        
        async for conversation in cursor:
            conversations.append(conversation)
            
        return conversations
        
    @classmethod
    async def create_conversation(cls, user_id: str, title: str) -> str:
        """
        创建新的对话
        """
        db = Database.get_db()
        collection = db[cls.conversation_collection]
        
        conversation_data = {
            "user_id": user_id,
            "title": title,
            "created_at": int(datetime.now().timestamp() * 1000),
            "updated_at": int(datetime.now().timestamp() * 1000)
        }
        
        result = await collection.insert_one(conversation_data)
        return str(result.inserted_id)
    
    @classmethod
    async def delete_user_chat_history(cls, user_id: str, conversation_id: Optional[str] = None) -> bool:
        """
        删除用户的聊天历史
        如果提供了conversation_id，则只删除特定对话的消息
        否则删除用户的所有消息和对话
        """
        collection = await cls.get_collection()
        db = Database.get_db()
        conversation_collection = db[cls.conversation_collection]
        
        # 构建查询条件
        query = {"user_id": user_id}
        if conversation_id:
            query["conversation_id"] = conversation_id
            # 删除特定对话的消息
            result = await collection.delete_many(query)
            # 删除对话记录
            await conversation_collection.delete_one({"_id": ObjectId(conversation_id)})
            return result.deleted_count > 0
        else:
            # 删除所有消息
            result = await collection.delete_many(query)
            # 删除所有对话记录
            await conversation_collection.delete_many(query)
            return result.deleted_count > 0
    
    @classmethod
    async def get_message_by_id(cls, message_id: str) -> Optional[ChatMessage]:
        """
        根据ID获取聊天消息
        """
        collection = await cls.get_collection()
        message_data = await collection.find_one({"_id": ObjectId(message_id)})
        if message_data:
            return ChatMessage(**message_data)
        return None