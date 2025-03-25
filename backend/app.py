import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# 导入自定义模块
from config import Config
from routes.chat_routes import chat_bp
from routes.user_routes import user_bp
from services.db_service import init_db
from services.vector_store import init_vector_store
from utils.logger import app_logger

# 加载环境变量
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # 配置跨域
    CORS(app)
    
    # 注册蓝图
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    
    # 初始化数据库连接
    init_db()
    
    # 初始化向量存储
    init_vector_store()
    
    # 记录应用启动日志
    app_logger.info('应用启动成功')
    app_logger.info(f'服务运行在 http://0.0.0.0:5001')
    app_logger.info(f'环境: {"开发" if app.debug else "生产"}')
    app_logger.info(f'MongoDB URI: {Config.MONGO_URI}')
    app_logger.info(f'向量模型: {Config.EMBEDDING_MODEL}')
    app_logger.info(f'数据目录: {Config.DATA_DIR}')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5001, debug=True)