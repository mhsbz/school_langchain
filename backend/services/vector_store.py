from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from config import Config
import os
import pickle
import shutil

# 全局向量存储实例
vector_store = None

# 本地向量存储目录
VECTOR_STORE_DIR = "./vector_store"

def init_vector_store():
    """初始化向量存储"""
    print("正在初始化向量存储...")
    global vector_store
    try:
        # 初始化向量模型
        embeddings = HuggingFaceEmbeddings(model_name=Config.EMBEDDING_MODEL)
        
        # 检查本地向量存储目录是否存在
        if os.path.exists(VECTOR_STORE_DIR) and os.path.isdir(VECTOR_STORE_DIR) and len(os.listdir(VECTOR_STORE_DIR)) > 0:
            # 如果向量存储目录存在且不为空，直接从本地加载
            print(f"本地向量存储目录 {VECTOR_STORE_DIR} 已存在，正在加载...")
            try:
                vector_store = FAISS.load_local(VECTOR_STORE_DIR, embeddings, allow_dangerous_deserialization=True)
                print("从本地加载向量存储成功")
            except Exception as load_error:
                print(f"从本地加载向量存储失败: {load_error}，将重新创建")
                # 如果加载失败，清空目录并重新创建
                shutil.rmtree(VECTOR_STORE_DIR, ignore_errors=True)
                os.makedirs(VECTOR_STORE_DIR, exist_ok=True)
                vector_store = FAISS.from_texts(["初始化文档"], embeddings)
                vector_store.save_local(VECTOR_STORE_DIR)
                # 加载知识库
                load_knowledge_base(vector_store, embeddings)
        else:
            # 如果向量存储目录不存在或为空，创建并加载知识库
            print(f"本地向量存储目录 {VECTOR_STORE_DIR} 不存在或为空，正在创建并加载知识库...")
            os.makedirs(VECTOR_STORE_DIR, exist_ok=True)
            vector_store = FAISS.from_texts(["初始化文档"], embeddings)
            vector_store.save_local(VECTOR_STORE_DIR)
            # 加载知识库
            load_knowledge_base(vector_store, embeddings)
        
        print("向量存储初始化成功")
        return True
    except Exception as e:
        print(f"向量存储初始化失败: {e}")
        return False

def load_knowledge_base(vector_store, embeddings):
    """加载知识库"""
    try:
        # 检查数据目录是否存在
        if not os.path.exists(Config.DATA_DIR):
            print(f"数据目录 {Config.DATA_DIR} 不存在")
            return False
        
        # 加载文档
        documents = []
        
        # 加载Word文档
        docx_loader = DirectoryLoader(
            Config.DATA_DIR,
            glob="**/*.docx",
            loader_cls=Docx2txtLoader
        )
        docx_documents = docx_loader.load()
        documents.extend(docx_documents)
        
        # 加载文本文档
        text_loader = DirectoryLoader(
            Config.DATA_DIR,
            glob="**/*.txt",
            loader_cls=TextLoader
        )
        text_documents = text_loader.load()
        documents.extend(text_documents)
        
        print(f"共加载 {len(documents)} 个文档")
        
        # 文档分块
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP
        )
        chunks = text_splitter.split_documents(documents)
        
        print(f"文档分块完成，共 {len(chunks)} 个块")
        
        # 将分块添加到向量存储
        if len(chunks) > 0:
            # 创建新的向量存储
            new_vector_store = FAISS.from_documents(chunks, embeddings)
            # 合并到现有向量存储
            if hasattr(vector_store, 'docstore') and hasattr(vector_store, 'index'):
                vector_store.merge_from(new_vector_store)
            else:
                vector_store = new_vector_store
            # 保存到本地
            vector_store.save_local(VECTOR_STORE_DIR)
        
        print("知识库加载完成")
        return True
    except Exception as e:
        print(f"知识库加载失败: {e}")
        return False

def get_vector_store():
    """获取向量存储实例"""
    global vector_store
    if vector_store is None:
        init_vector_store()
    return vector_store