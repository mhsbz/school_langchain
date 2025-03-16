from pydantic import BaseModel
from typing import Optional

# 令牌响应模型
class Token(BaseModel):
    token: str
    token_type: str

# 令牌数据模型
class TokenData(BaseModel):
    username: Optional[str] = None