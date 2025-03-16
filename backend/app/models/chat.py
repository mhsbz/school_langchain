from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId
from .user import PyObjectId

# 聊天请求模型
class QuestionRequest(BaseModel):
    question: str
    conversation_id: Optional[str] = None

# 聊天回答响应模型
class AnswerResponse(BaseModel):
    answer: str
    sources: Optional[List[str]] = None
    conversation_id: Optional[str] = None

# 聊天消息模型
class ChatMessage(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    role: str  # "user" 或 "assistant"
    content: str
    conversation_id: Optional[str] = None
    timestamp: int = Field(default_factory=lambda: int(datetime.now().timestamp() * 1000))
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

# 对话模型
class Conversation(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    title: str
    created_at: int = Field(default_factory=lambda: int(datetime.now().timestamp() * 1000))
    updated_at: int = Field(default_factory=lambda: int(datetime.now().timestamp() * 1000))
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

# 聊天历史响应模型
class ChatHistory(BaseModel):
    messages: List[ChatMessage]

# 推荐问题响应模型
class SuggestionsResponse(BaseModel):
    suggestions: List[str]