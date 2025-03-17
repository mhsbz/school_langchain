import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    # MongoDB配置
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://admin:password@localhost:27017')
    MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'school_chat')
    
    # ChromaDB配置
    CHROMA_HOST = os.getenv('CHROMA_HOST', 'localhost')
    CHROMA_PORT = os.getenv('CHROMA_PORT', '8000')
    CHROMA_COLLECTION = os.getenv('CHROMA_COLLECTION', 'school_knowledge')
    
    # 向量模型配置
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'BAAI/bge-m3')
    
    # DeepSeek API配置
    DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')
    DEEPSEEK_API_URL = os.getenv('DEEPSEEK_API_URL', 'https://api.deepseek.com/v1/chat/completions')
    
    # 知识库配置
    DATA_DIR = os.getenv('DATA_DIR', './data')
    
    # 分块配置
    CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', '1000'))
    CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', '200'))