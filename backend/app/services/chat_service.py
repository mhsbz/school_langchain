from typing import List, Optional
from datetime import datetime
import random

from ..models.chat import QuestionRequest, AnswerResponse, ChatMessage, SuggestionsResponse
from ..repositories.chat_repository import ChatRepository
from ..services.rag_service import RAGService

class ChatService:
    """
    聊天服务，处理聊天相关的业务逻辑
    """
    
    # 初始化RAG服务
    rag_service = RAGService()
    
    @staticmethod
    async def get_chat_history(user_id: str, conversation_id: Optional[str] = None) -> List[ChatMessage]:
        """
        获取用户的聊天历史
        如果提供了conversation_id，则获取特定对话的消息
        否则获取用户的所有消息
        """
        return await ChatRepository.get_user_chat_history(user_id, conversation_id)
    
    @staticmethod
    async def save_message(user_id: str, role: str, content: str, conversation_id: Optional[str] = None) -> ChatMessage:
        """
        保存聊天消息
        """
        message_data = {
            "user_id": user_id,
            "role": role,
            "content": content,
            "timestamp": int(datetime.now().timestamp() * 1000)
        }
        
        if conversation_id:
            message_data["conversation_id"] = conversation_id
        
        return await ChatRepository.create_message(message_data)
    
    @staticmethod
    async def process_question(user_id: str, question: str, conversation_id: Optional[str] = None) -> AnswerResponse:
        """
        处理用户问题，生成回答
        """
        # 如果没有提供conversation_id，创建一个新的对话
        if not conversation_id:
            # 使用问题的前20个字符作为对话标题
            title = question[:20] + "..." if len(question) > 20 else question
            conversation_id = await ChatRepository.create_conversation(user_id, title)
            
        # 保存用户问题
        await ChatService.save_message(user_id, "user", question, conversation_id)
        
        # 调用RAG系统生成回答
        try:
            # 使用RAG服务查询答案
            answer = await ChatService.rag_service.query(question)
            if not answer:
                answer = "抱歉，我无法回答这个问题。请尝试询问关于学校的其他问题。"
            
            # 获取文档来源
            sources = await ChatService.rag_service.get_sources(question)
            
            # 保存系统回答
            await ChatService.save_message(user_id, "assistant", answer, conversation_id)
            
            return AnswerResponse(answer=answer, sources=sources)
        except Exception as e:
            # 异常处理
            error_message = f"处理问题时发生错误: {str(e)}"
            fallback_answer = "抱歉，系统暂时无法处理您的问题，请稍后再试。"
            
            # 保存系统回答（使用备用回答）
            await ChatService.save_message(user_id, "assistant", fallback_answer, conversation_id)
            
            return AnswerResponse(answer=fallback_answer, sources=[])
    
    @staticmethod
    async def clear_chat_history(user_id: str, conversation_id: Optional[str] = None) -> bool:
        """
        清除用户的聊天历史
        如果提供了conversation_id，则只清除特定对话的消息
        否则清除用户的所有消息
        """
        return await ChatRepository.delete_user_chat_history(user_id, conversation_id)
        
    @staticmethod
    async def get_suggestions() -> List[str]:
        """
        获取推荐问题列表
        """
        # 预设的推荐问题列表
        all_suggestions = [
            '学校有哪些专业？',
            '学校的历史是怎样的？',
            '学校有哪些校区？',
            '学校的师资力量如何？',
            '学校有哪些荣誉？',
            '学校的就业情况如何？',
            '学校有哪些实验室？',
            '学校的图书馆藏书量是多少？',
            '学校的国际交流项目有哪些？',
            '学校的奖学金政策是什么？'
        ]
        
        # 随机选择5个问题
        suggestions = []
        indices = random.sample(range(len(all_suggestions)), min(5, len(all_suggestions)))
        for i in indices:
            suggestions.append(all_suggestions[i])
            
        return suggestions