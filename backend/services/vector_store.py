from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import Config
import os
import chromadb

# 全局向量存储实例
vector_store = None

def init_vector_store():
    """初始化向量存储"""
    global vector_store
    try:
        # 初始化向量模型
        embeddings = HuggingFaceEmbeddings(model_name=Config.EMBEDDING_MODEL)
        
        # 连接ChromaDB
        client = chromadb.HttpClient(
            host=Config.CHROMA_HOST,
            port=Config.CHROMA_PORT
        )
        
        # 检查集合是否存在
        collections = client.list_collections()
        collection_names = [collection.name for collection in collections]
        
        if Config.CHROMA_COLLECTION not in collection_names:
            # 如果集合不存在，创建并加载知识库
            print(f"集合 {Config.CHROMA_COLLECTION} 不存在，正在创建并加载知识库...")
            vector_store = Chroma(
                collection_name=Config.CHROMA_COLLECTION,
                embedding_function=embeddings,
                client=client,
                persist_directory="./chroma_db"
            )
            
            # 加载知识库
            load_knowledge_base(vector_store, embeddings)
        else:
            # 如果集合已存在，直接连接
            print(f"集合 {Config.CHROMA_COLLECTION} 已存在，正在连接...")
            vector_store = Chroma(
                collection_name=Config.CHROMA_COLLECTION,
                embedding_function=embeddings,
                client=client,
                persist_directory="./chroma_db"
            )
        
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
            loader_cls=DocxLoader
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
        vector_store.add_documents(chunks)
        vector_store.persist()
        
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