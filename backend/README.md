# 学校知识问答系统后端

这是一个基于Flask和LangChain构建的RAG（检索增强生成）系统，用于回答关于学校的各种问题。

## 功能特点

- 基于Flask框架的轻量级后端服务
- 使用LangChain构建RAG逻辑
- 使用ChromaDB存储和管理知识库的向量信息
- 使用BGE-M3作为向量模型
- 调用DeepSeek API作为大模型生成回复
- 使用MongoDB存储对话历史

## 系统架构

- `app.py`: 应用入口，配置Flask应用
- `config.py`: 配置文件，管理环境变量和应用配置
- `services/`: 服务模块
  - `db_service.py`: 数据库服务，管理MongoDB连接
  - `vector_store.py`: 向量存储服务，管理ChromaDB连接和知识库处理
  - `llm_service.py`: 大模型服务，调用DeepSeek API生成回复
  - `chat_service.py`: 聊天服务，处理聊天相关的业务逻辑
- `routes/`: 路由模块
  - `chat_routes.py`: 聊天相关的API路由

## 安装与运行

### 前提条件

- Python 3.8+
- MongoDB
- ChromaDB

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置环境变量

复制`.env.example`文件为`.env`，并根据实际情况修改配置：

```
# MongoDB配置
MONGO_URI=mongodb://admin:password@localhost:27017
MONGO_DB_NAME=school_chat

# ChromaDB配置
CHROMA_HOST=localhost
CHROMA_PORT=8000
CHROMA_COLLECTION=school_knowledge

# 向量模型配置
EMBEDDING_MODEL=BAAI/bge-m3

# DeepSeek API配置
DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_API_URL=https://api.deepseek.com/v1/chat/completions

# 知识库配置
DATA_DIR=../data

# 分块配置
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

### 启动服务

```bash
python app.py
```

服务将在 http://localhost:5001 上运行。

### 使用Docker Compose启动

项目根目录下已提供`docker-compose.yaml`文件，可以使用Docker Compose启动MongoDB和ChromaDB：

```bash
docker-compose up -d
```

## API接口

### 发送问题

- URL: `/api/chat/question`
- 方法: `POST`
- 请求体:
  ```json
  {
    "question": "学校有哪些专业？",
    "conversation_id": "可选，对话ID"
  }
  ```
- 响应:
  ```json
  {
    "answer": "回答内容",
    "conversation_id": "对话ID"