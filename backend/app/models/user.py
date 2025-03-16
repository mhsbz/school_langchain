from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

# 用户基础模型
class UserBase(BaseModel):
    username: str
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

# 自定义ObjectId字段，用于MongoDB的_id字段
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

# 创建用户请求模型
PHONE_REGEX = r'^1[3-9]\d{9}$'
class UserCreate(UserBase):
    phone_number: str = Field(..., pattern=PHONE_REGEX)
    password: str

# 创建用户请求模型
PHONE_REGEX = r'^1[3-9]\d{9}$'
class UserCreate(UserBase):
    phone_number: str = Field(..., pattern=PHONE_REGEX)
    password: str

# 数据库中的用户模型
class UserInDB(UserBase):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "username": "johndoe",
                "hashed_password": "..."
            }
        }

# API响应中的用户模型
class User(UserBase):
    id: Optional[str] = Field(None, alias="_id")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

# 聊天消息模型
class ChatMessage(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    role: str
    content: str
    timestamp: int = Field(default_factory=lambda: int(datetime.now().timestamp() * 1000))
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

