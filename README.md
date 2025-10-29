# 智融千问 - 智能学校问答系统

<div align="center">

一个基于 LangChain 和 RAG（检索增强生成）技术的智能学校问答助手系统

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.x-green.svg)](https://vuejs.org)
[![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey.svg)](https://flask.palletsprojects.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-latest-brightgreen.svg)](https://www.mongodb.com)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://www.docker.com)

</div>

## 📋 项目简介

智融千问是一个面向学校的智能问答系统，通过整合学校的各类文档资料（办校历史、师资力量、专业设置、校区分布等），利用大语言模型和向量检索技术，为用户提供准确、及时的学校信息查询服务。

### ✨ 核心特性

- 🤖 **智能问答**：基于 RAG 技术，从知识库中检索相关信息并生成准确答案
- 💬 **对话管理**：支持多轮对话，保存对话历史记录
- 📚 **知识库管理**：自动处理和索引 Word 文档，构建向量知识库
- 🎯 **意图识别**：智能识别用户问题意图，提供针对性回答
- 🔍 **语义检索**：使用先进的嵌入模型进行语义相似度搜索
- 📊 **数据持久化**：基于 MongoDB 存储对话历史和用户信息
- 🐳 **容器化部署**：完整的 Docker Compose 配置，一键启动

## 🏗️ 技术架构

### 后端技术栈

- **Web 框架**：Flask + Flask-CORS
- **AI 框架**：LangChain + LangChain Community
- **向量数据库**：ChromaDB / FAISS
- **数据库**：MongoDB
- **嵌入模型**：BAAI/bge-m3 (Sentence Transformers)
- **大语言模型**：DeepSeek API
- **文档处理**：python-docx, docx2txt, BeautifulSoup4

### 前端技术栈

- **框架**：Vue.js 3.x
- **路由**：Vue Router 4.x
- **HTTP 客户端**：Axios
- **构建工具**：Vue CLI

### 基础设施

- **容器化**：Docker + Docker Compose
- **Web 服务器**：Nginx (前端)
- **Python 版本**：3.8+

## 📁 项目结构

```
school_langchain/
├── backend/                    # 后端服务
│   ├── app.py                 # Flask 应用入口
│   ├── config.py              # 配置文件
│   ├── requirements.txt       # Python 依赖
│   ├── Dockerfile            # 后端 Docker 配置
│   ├── data/                 # 知识库文档（Word 文件）
│   ├── routes/               # API 路由
│   │   ├── chat_routes.py   # 对话相关接口
│   │   └── user_routes.py   # 用户相关接口
│   ├── services/             # 业务逻辑层
│   │   ├── chat_service.py  # 对话服务
│   │   ├── db_service.py    # 数据库服务
│   │   ├── llm_service.py   # 大模型服务
│   │   ├── vector_store.py  # 向量存储服务
│   │   └── user_service.py  # 用户服务
│   └── utils/                # 工具模块
│       ├── call_model.py    # 模型调用工具
│       └── logger.py        # 日志工具
├── frontend/                  # 前端应用
│   ├── src/
│   │   ├── App.vue          # 根组件
│   │   ├── main.js          # 入口文件
│   │   ├── api/             # API 接口封装
│   │   ├── components/      # Vue 组件
│   │   │   ├── ChatBot.vue # 聊天机器人组件
│   │   │   └── Login.vue   # 登录组件
│   │   ├── router/          # 路由配置
│   │   └── assets/          # 静态资源
│   ├── public/              # 公共资源
│   ├── Dockerfile          # 前端 Docker 配置
│   ├── nginx.conf          # Nginx 配置
│   └── package.json        # Node 依赖
├── docker-compose.yaml      # Docker Compose 配置
└── README.md               # 项目说明文档
```

## 🚀 快速开始

### 前置要求

- Docker 和 Docker Compose
- 或者本地环境：
  - Python 3.8+
  - Node.js 14+
  - MongoDB

### 使用 Docker Compose（推荐）

1. **克隆项目**

```bash
git clone <repository-url>
cd school_langchain
```

2. **配置环境变量**

创建 `.env` 文件（可选，Docker Compose 已有默认配置）：

```bash
# MongoDB 配置
MONGO_URI=mongodb://admin:password@mongodb:27017
MONGO_DB_NAME=school_chat

# DeepSeek API 配置
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_API_URL=https://api.deepseek.com/chat/completions

# 向量模型配置
EMBEDDING_MODEL=/app/model_cache
VECTOR_STORE_DIR=/app/vector_store

# 数据目录
DATA_DIR=/app/data
```

3. **启动服务**

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

4. **访问应用**

- 前端界面：http://localhost:8080
- 后端 API：http://localhost:5001

### 本地开发环境

#### 后端启动

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 启动 MongoDB（如果未使用 Docker）
# 方式1: 使用 Homebrew（macOS）
brew services start mongodb-community

# 方式2: 使用 Docker
docker run -d -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=password \
  mongo:latest

# 配置环境变量
export MONGO_URI=mongodb://admin:password@localhost:27017
export DEEPSEEK_API_KEY=your_api_key_here

# 启动后端服务
python app.py
```

#### 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 开发模式启动
npm run serve

# 构建生产版本
npm run build
```

## 📖 API 文档

### 对话接口

#### POST `/api/chat/message`
发送消息并获取回复

**请求体：**
```json
{
  "message": "学校有哪些专业？",
  "conversation_id": "optional-conversation-id",
  "user_id": "user123"
}
```

**响应：**
```json
{
  "answer": "学校开设以下专业：...",
  "conversation_id": "conv-uuid",
  "sources": [...],
  "timestamp": "2025-10-29T12:00:00"
}
```

#### GET `/api/chat/history`
获取对话历史

**查询参数：**
- `user_id`: 用户ID（可选）

#### GET `/api/chat/conversation/<conversation_id>`
获取指定对话的消息列表

#### DELETE `/api/chat/conversation/<conversation_id>`
删除指定对话

### 用户接口

#### POST `/api/user/login`
用户登录

#### POST `/api/user/register`
用户注册

## 🔧 配置说明

### 后端配置 (config.py)

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| MONGO_URI | MongoDB 连接字符串 | mongodb://admin:password@localhost:27017 |
| MONGO_DB_NAME | 数据库名称 | school_chat |
| EMBEDDING_MODEL | 嵌入模型路径 | BAAI/bge-m3 |
| DEEPSEEK_API_KEY | DeepSeek API 密钥 | - |
| DATA_DIR | 知识库文档目录 | ./data |
| CHUNK_SIZE | 文档分块大小 | 1000 |
| CHUNK_OVERLAP | 分块重叠大小 | 200 |

### 知识库文档

将学校相关的 Word 文档（.docx）放入 `backend/data/` 目录，系统会自动：
1. 读取文档内容
2. 进行文本分块
3. 生成向量嵌入
4. 存储到向量数据库

支持的文档类型：
- 办校历史
- 学校荣誉
- 师资力量
- 专业设置
- 校区分布
- 教师简介
- 学生活动
- 等等

## 🎨 功能特点

### 1. 智能检索增强生成 (RAG)

系统采用 RAG 架构，结合了检索和生成两个阶段：
- **检索阶段**：使用向量相似度搜索找到相关文档
- **生成阶段**：基于检索到的内容，使用 LLM 生成准确答案

### 2. 多轮对话支持

- 维护对话上下文
- 支持对话历史查询
- 会话管理和持久化

### 3. 向量化知识库

- 自动处理 Word 文档
- 使用高性能嵌入模型（bge-m3）
- 支持语义相似度检索

### 4. 响应式前端界面

- 美观的聊天界面
- 对话历史侧边栏
- 实时消息更新
- 移动端适配

## 🔍 工作流程

```
用户提问
    ↓
意图识别
    ↓
向量检索（检索相关文档）
    ↓
上下文增强
    ↓
LLM 生成回答
    ↓
返回答案 + 保存对话历史
```

## 📊 数据库设计

### MongoDB Collections

**conversations** - 对话记录
```javascript
{
  _id: ObjectId,
  user_id: String,
  title: String,
  created_at: DateTime,
  updated_at: DateTime
}
```

**messages** - 消息记录
```javascript
{
  _id: ObjectId,
  conversation_id: String,
  role: String,  // "user" | "assistant"
  content: String,
  timestamp: DateTime,
  sources: Array  // 引用的知识库来源
}
```

**users** - 用户信息
```javascript
{
  _id: ObjectId,
  username: String,
  email: String,
  created_at: DateTime
}
```

## 🛠️ 开发指南

### 添加新的知识文档

1. 将 Word 文档放入 `backend/data/` 目录
2. 重启后端服务，系统会自动加载新文档
3. 或调用向量库重建接口

### 自定义 Prompt

编辑 `backend/services/llm_service.py` 中的提示词模板：

```python
PROMPT_TEMPLATE = """
你是学校的智能助手，请基于以下信息回答问题：

上下文：
{context}

问题：{question}

请提供准确、友好的回答。
"""
```

### 更换 LLM 模型

在 `config.py` 中修改 API 配置，或在 `llm_service.py` 中更换模型调用逻辑。

## 📝 日志管理

日志文件位置：`backend/logs/`

- `app.log` - 应用日志
- `chat.log` - 对话日志
- `error.log` - 错误日志

