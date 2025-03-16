from fastapi import APIRouter, HTTPException
from typing import List, Optional

from ..models.chat import QuestionRequest, AnswerResponse, ChatMessage, Conversation, SuggestionsResponse
from ..services.chat_service import ChatService
from ..repositories.chat_repository import ChatRepository

router = APIRouter(prefix="/api/chat", tags=["聊天"])

@router.get("/history", response_model=List[ChatMessage])
async def get_chat_history(conversation_id: Optional[str] = None, user_id: str = "anonymous"):
    """
    获取用户的聊天历史
    如果提供了conversation_id，则获取特定对话的消息
    否则获取用户的所有消息
    """
    return await ChatService.get_chat_history(user_id, conversation_id)

@router.get("/conversations", response_model=List[Conversation])
async def get_conversations(user_id: str = "anonymous"):
    """
    获取用户的所有对话
    """
    return await ChatRepository.get_user_conversations(user_id)

@router.get("/suggestions", response_model=SuggestionsResponse)
async def get_suggestions():
    """
    获取推荐问题
    """
    suggestions = await ChatService.get_suggestions()
    return SuggestionsResponse(suggestions=suggestions)

@router.post("/question", response_model=AnswerResponse)
async def ask_question(question_req: QuestionRequest, user_id: str = "anonymous"):
    """
    提交问题并获取回答
    """
    return await ChatService.process_question(user_id, question_req.question, question_req.conversation_id)

@router.delete("/history", response_model=bool)
async def clear_chat_history(conversation_id: Optional[str] = None, user_id: str = "anonymous"):
    """
    清除用户的聊天历史
    如果提供了conversation_id，则只清除特定对话的消息
    否则清除用户的所有消息
    """
    return await ChatService.clear_chat_history(user_id, conversation_id)