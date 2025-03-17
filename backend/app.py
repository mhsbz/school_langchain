import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# 导入自定义模块
from config import Config
from routes.chat_routes import chat_bp
from services.db_service import init_db
from services.vector_store import init_vector_store

# 加载环境变量
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # 配置跨域
    CORS(app)
    
    # 注册蓝图
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    
    # 初始化数据库连接
    init_db()
    
    # 初始化向量存储
    init_vector_store()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=3000, debug=True)