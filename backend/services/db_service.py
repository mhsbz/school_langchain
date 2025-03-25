import pymongo
from config import Config
from utils.logger import db_logger

# 全局MongoDB客户端和数据库实例
mongo_client = None
db = None

def init_db():
    """初始化MongoDB连接"""
    global mongo_client, db
    try:
        # 连接MongoDB
        mongo_client = pymongo.MongoClient(Config.MONGO_URI)
        db = mongo_client[Config.MONGO_DB_NAME]
        
        # 创建必要的集合和索引
        conversations = db['conversations']
        messages = db['messages']
        
        # 为messages集合创建索引
        messages.create_index('conversation_id')
        messages.create_index('timestamp')
        
        print("MongoDB连接成功")
        return True
    except Exception as e:
        print(f"MongoDB连接失败: {e}")
        return False

def get_db():
    """获取数据库实例"""
    global db
    if db is None:
        init_db()
    return db

def close_db():
    """关闭MongoDB连接"""
    global mongo_client
    if mongo_client:
        mongo_client.close()
        print("MongoDB连接已关闭")