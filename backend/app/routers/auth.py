from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from typing import Optional
from datetime import timedelta

from ..models.token import Token, TokenData
from ..models.user import UserCreate, User
from ..services.auth_service import AuthService, SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/api/auth", tags=["认证"])

@router.post("/register", response_model=Token)
async def register(user_data: UserCreate):
    """
    用户注册
    """
    # 检查手机号是否已存在
    existing_user = await AuthService.get_user_by_phone(user_data.phone_number)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='该手机号已被注册'
        )
    
    # 创建用户时添加手机号字段
    user = await AuthService.register_user(user_data)
    
    # 生成访问令牌时包含手机号
    access_token_expires = timedelta(minutes=30)
    access_token = AuthService.create_access_token(
        data={'sub': user.username, 'phone': user.phone_number},
        expires_delta=access_token_expires
    )
    
    return {'token': access_token, 'token_type': 'bearer'}

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    用户登录
    """
    # 使用手机号作为用户名
    return await AuthService.login_user(form_data.username, form_data.password)

async def get_current_user(token: str = Depends(AuthService.oauth2_scheme)):
    """
    获取当前用户
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的认证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = await AuthService.get_user_by_phone(phone=token_data.username)
    if user is None:
        raise credentials_exception
    return user