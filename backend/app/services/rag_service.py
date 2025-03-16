from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
import os
import requests
from typing import Optional, List
import logging
import aiohttp
import asyncio

class RAGService:
    def __init__(self):
        self.data_dir = Path("backend/data")
        self.index_dir = Path("backend/storage")
        # 指定模型缓存目录到宿主机
        
        model_path = "backend/emd_model"

        # model_path = "/Users/dxj/.cache/huggingface/hub/models--BAAI--bge-m3/snapshots/5617a9f61b028005a4858fdac845db406aefb181"
        
        self.embed_model = HuggingFaceEmbeddings(
            model_name=model_path
        )
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=512)
        
        # DeepSeek配置
        self.deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
        self.deepseek_url = "https://api.deepseek.com/v1/chat/completions"
        self.deepseek_model = "deepseek-chat"
        
        # 初始化 Chroma 存储
        self.vector_store = None
        # 确保索引目录存在
        self.index_dir.mkdir(parents=True, exist_ok=True)
        
        # 如果索引已存在，则加载它
        if (self.index_dir / "chroma.sqlite3").exists():
            self.vector_store = Chroma(
                persist_directory=str(self.index_dir),
                embedding_function=self.embed_model,
                client_settings={
                    "chroma_server_host": "localhost",
                    "chroma_server_http_port": 2345
                }
            )
    
    async def build_index(self) -> str:
        """构建文档索引"""
        try:
            logging.info("开始构建文档索引...")
            
            # 检查数据目录是否存在
            if not self.data_dir.exists():
                raise ValueError(f"数据目录不存在: {self.data_dir}")
            
            # 加载文档
            loader = DirectoryLoader(
                self.data_dir,
                glob="**/*.docx",  # 加载所有docx文件
                show_progress=True
            )
            documents = loader.load()
            logging.info(f"加载了 {len(documents)} 个文档")
            
            # 分割文档
            texts = self.text_splitter.split_documents(documents)
            logging.info(f"文档被分割为 {len(texts)} 个文本块")
            
            # 创建向量存储
            self.vector_store = Chroma.from_documents(
                documents=texts,
                embedding=self.embed_model,
                persist_directory=str(self.index_dir),
                client_settings={
                    "chroma_server_host": "localhost",
                    "chroma_server_http_port": 2345
                }
            )
            
            # 持久化存储
            self.vector_store.persist()
            logging.info(f"索引已成功构建并保存到 {self.index_dir}")
            
            return str(self.index_dir)
        
        except Exception as e:
            logging.error(f"构建索引失败: {str(e)}")
            raise
    
    async def query(self, question: str) -> Optional[str]:
        """执行RAG查询并调用DeepSeek生成回答"""
        try:
            if not self.vector_store:
                raise ValueError("向量存储未初始化，请先调用 build_index()")
            
            # 本地索引检索
            retriever = self.vector_store.as_retriever()
            local_results = retriever.get_relevant_documents(question)
            
            # 提取文档内容，格式化为上下文
            context = "\n\n".join([doc.page_content for doc in local_results])
            
            # 异步调用DeepSeek API
            headers = {
                "Authorization": f"Bearer {self.deepseek_api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "messages": [
                    {
                        "role": "system",
                        "content": f"基于以下上下文回答问题:\n\n{context}"
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ],
                "model": self.deepseek_model,
                "temperature": 0.3
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.deepseek_url, json=payload, headers=headers) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"API请求失败: {response.status}, {error_text}")
                    
                    response_json = await response.json()
                    return response_json["choices"][0]["message"]["content"]
        
        except Exception as e:
            logging.error(f"RAG查询失败: {str(e)}")
            return None
            
    async def get_sources(self, question: str) -> List[str]:
        """获取问题的相关文档来源"""
        try:
            if not self.vector_store:
                raise ValueError("向量存储未初始化，请先调用 build_index()")
            
            # 本地索引检索
            retriever = self.vector_store.as_retriever()
            local_results = retriever.get_relevant_documents(question)
            
            # 提取文档来源
            sources = []
            for doc in local_results:
                if hasattr(doc, 'metadata') and 'source' in doc.metadata:
                    sources.append(doc.metadata['source'])
            
            return list(set(sources))  # 去重
        
        except Exception as e:
            logging.error(f"获取来源失败: {str(e)}")
            return []