from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List

from ..services.rag_service import RAGService
from ..models.user import User
from .auth import get_current_user

# 请求和响应模型
class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: Optional[List[str]] = None

router = APIRouter(tags=["RAG"])
rag_service = RAGService()

@router.post("/build-index")
async def build_index(current_user: User = Depends(get_current_user)):
    """构建文档索引（需要管理员权限）"""
    try:
        # 这里可以添加管理员权限检查
        index_path = await rag_service.build_index()
        return {"status": "success", "index_path": index_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query", response_model=QueryResponse)
async def query_question(query_req: QueryRequest, current_user: User = Depends(get_current_user)):
    """查询问题并获取回答"""
    try:
        # 获取回答
        answer = await rag_service.query(query_req.question)
        if not answer:
            raise HTTPException(status_code=500, detail="无法生成回答")
        
        # 获取来源
        sources = await rag_service.get_sources(query_req.question)
        
        return {"answer": answer, "sources": sources}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")