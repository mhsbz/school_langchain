from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, List
from pydantic import BaseModel
import os
from pathlib import Path

# 导入数据库连接
from .database import Database

# 导入路由
from .routers import chat, rag_router

# 配置日志
import logging.handlers

# 创建日志目录
log_dir = Path(__file__).parent.parent.parent / 'logs'
log_dir.mkdir(exist_ok=True, parents=True)

# 配置日志
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 日志格式
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# 文件处理器（10MB轮转，保留5个备份）
file_handler = logging.handlers.RotatingFileHandler(
    filename=log_dir / 'app.log',
    maxBytes=10*1024*1024,
    backupCount=5,
    encoding='utf-8'
)
file_handler.setFormatter(formatter)

# 控制台处理器
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

# 创建FastAPI应用
app = FastAPI(title="RAG API", description="RAG应用的后端API服务")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置为特定的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(chat.router)
app.include_router(rag_router.router, prefix="/api/rag")

# 启动事件
@app.on_event("startup")
async def startup_db_client():
    await Database.connect_to_mongodb()

# 关闭事件
@app.on_event("shutdown")
async def shutdown_db_client():
    await Database.close_mongodb_connection()

@app.get("/")
async def root():
    return {"message": "RAG API 服务正在运行"}

# 启动服务器
if __name__ == "__main__":
    import uvicorn
    print("RAG API 服务启动")
    uvicorn.run("app.main:app", host="0.0.0.0", port=3030, reload=True)