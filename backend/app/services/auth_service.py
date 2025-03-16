from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import os

from ..models.user import UserCreate, UserInDB, User
from ..repositories.user_repository import UserRepository

# 密码加密和JWT配置
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")  # 在生产环境中应该使用环境变量
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    """
    认证服务，处理用户注册、登录和认证相关的业务逻辑
    """
    
    # 创建OAuth2PasswordBearer实例，用于获取token
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        验证密码
        """
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        获取密码哈希
        """
        return pwd_context.hash(password)
    
    @staticmethod
    async def get_user(username: str) -> Optional[UserInDB]:
        """
        根据用户名获取用户
        """
        return await UserRepository.find_by_username(username)
    
    @staticmethod
    async def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
        """
        认证用户
        """
        user = await AuthService.get_user(username)
        if not user:
            return None
        if not AuthService.verify_password(password, user.hashed_password):
            return None
        return user
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        创建访问令牌
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    async def register_user(user_data: UserCreate) -> User:
        """
        注册新用户
        """
        # 检查用户名是否已存在
        existing_user = await AuthService.get_user(user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已存在"
            )
        
        # 创建新用户
        hashed_password = AuthService.get_password_hash(user_data.password)
        user_dict = {
            "username": user_data.username,
            "hashed_password": hashed_password
        }
        
        created_user = await UserRepository.create(user_dict)
        return User(
            _id=str(created_user.id),
            username=created_user.username,
            created_at=created_user.created_at,
            updated_at=created_user.updated_at
        )
    
    @staticmethod
    async def login_user(username: str, password: str) -> dict:
        """
        用户登录
        """
        user = await AuthService.authenticate_user(username, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = AuthService.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        
        return {"token": access_token, "token_type": "bearer"}