import datetime
import uuid
import random
from services.db_service import get_db
from services.vector_store import get_vector_store
from services.llm_service import generate_answer

def get_chat_history(user_id=None):
    """获取对话历史
    
    Args:
        user_id: 用户ID，可选，如果提供则只返回该用户的对话
        
    Returns:
        对话历史列表
    """
    try:
        db = get_db()
        conversations = db['conversations']
        
        # 如果提供了用户ID，则只获取该用户的对话
        query = {'user_id': user_id} if user_id else {}
        
        # 获取对话，按时间倒序排列
        result = list(conversations.find(query).sort('created_at', -1))
        
        # 将ObjectId转换为字符串
        for conv in result:
            conv['_id'] = str(conv['_id'])
        
        return result
    except Exception as e:
        print(f"获取对话历史失败: {e}")
        return []

def get_conversation_messages(conversation_id):
    """获取指定对话的所有消息
    
    Args:
        conversation_id: 对话ID
        
    Returns:
        消息列表
    """
    try:
        db = get_db()
        messages = db['messages']
        
        # 获取指定对话的所有消息，按时间排序
        result = list(messages.find({'conversation_id': conversation_id}).sort('timestamp', 1))
        
        # 将ObjectId转换为字符串
        for msg in result:
            msg['_id'] = str(msg['_id'])
        
        return result
    except Exception as e:
        print(f"获取对话消息失败: {e}")
        return []

def create_conversation(title, user_id=None):
    """创建新对话
    
    Args:
        title: 对话标题
        user_id: 用户ID，可选
        
    Returns:
        新创建的对话ID
    """
    try:
        db = get_db()
        conversations = db['conversations']
        
        # 创建新对话
        conversation = {
            '_id': str(uuid.uuid4()),
            'title': title,
            'user_id': user_id,  # 添加用户ID
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now()
        }
        
        conversations.insert_one(conversation)
        
        return conversation['_id']
    except Exception as e:
        print(f"创建对话失败: {e}")
        return None

def save_message(conversation_id, content, role, user_id=None):
    """保存消息
    
    Args:
        conversation_id: 对话ID
        content: 消息内容
        role: 角色（user或assistant）
        user_id: 用户ID，可选
        
    Returns:
        保存的消息ID
    """
    try:
        db = get_db()
        messages = db['messages']
        conversations = db['conversations']
        
        # 保存消息
        message = {
            '_id': str(uuid.uuid4()),
            'conversation_id': conversation_id,
            'content': content,
            'role': role,
            'user_id': user_id,  # 添加用户ID
            'timestamp': datetime.datetime.now()
        }
        
        messages.insert_one(message)
        
        # 更新对话的更新时间
        conversations.update_one(
            {'_id': conversation_id},
            {'$set': {'updated_at': datetime.datetime.now()}}
        )
        
        return message['_id']
    except Exception as e:
        print(f"保存消息失败: {e}")
        return None

def delete_conversation(conversation_id, user_id=None):
    """删除对话及其所有消息
    
    Args:
        conversation_id: 对话ID
        user_id: 用户ID，可选，如果提供则只删除该用户的对话
        
    Returns:
        是否删除成功
    """
    try:
        db = get_db()
        conversations = db['conversations']
        messages = db['messages']
        
        # 构建查询条件，如果提供了用户ID，则只删除该用户的对话
        query = {'_id': conversation_id}
        if user_id:
            query['user_id'] = user_id
        
        # 删除对话
        result = conversations.delete_one(query)
        
        # 如果没有找到匹配的对话，返回False
        if result.deleted_count == 0:
            return False
        
        # 删除对话的所有消息
        messages.delete_many({'conversation_id': conversation_id})
        
        return True
    except Exception as e:
        print(f"删除对话失败: {e}")
        return False

def clear_all_history(user_id=None):
    """清除对话历史
    
    Args:
        user_id: 用户ID，可选，如果提供则只清除该用户的对话历史
        
    Returns:
        是否清除成功
    """
    try:
        db = get_db()
        conversations = db['conversations']
        messages = db['messages']
        
        # 如果提供了用户ID，则只清除该用户的对话历史
        query = {'user_id': user_id} if user_id else {}
        
        # 获取要删除的对话ID列表
        conversation_ids = [conv['_id'] for conv in conversations.find(query, {'_id': 1})]
        
        # 删除对话
        conversations.delete_many(query)
        
        # 删除对话的所有消息
        if conversation_ids:
            messages.delete_many({'conversation_id': {'$in': conversation_ids}})
        elif not user_id:  # 如果没有提供用户ID，则删除所有消息
            messages.delete_many({})
        
        return True
    except Exception as e:
        print(f"清除所有对话历史失败: {e}")
        return False

def process_question(question, conversation_id=None, user_id=None):
    """处理用户问题
    
    Args:
        question: 用户问题
        conversation_id: 对话ID，如果为None则创建新对话
        user_id: 用户ID，可选
        
    Returns:
        回答内容和对话ID
    """
    try:
        # 获取向量存储实例
        vector_store = get_vector_store()
        
        # 检索相关上下文
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})
        docs = retriever.get_relevant_documents(question)
        
        # 合并上下文
        context = "\n\n".join([doc.page_content for doc in docs])
        
        # 生成回答
        answer = generate_answer(question, context)
        
        # 处理对话ID
        if conversation_id is None:
            # 创建新对话，使用问题的前20个字符作为标题
            title = question[:20] + "..." if len(question) > 20 else question
            conversation_id = create_conversation(title, user_id)
        
        # 保存用户问题和系统回答
        save_message(conversation_id, question, 'user', user_id)
        save_message(conversation_id, answer, 'assistant', user_id)
        
        return {
            'answer': answer,
            'conversation_id': conversation_id
        }
    except Exception as e:
        print(f"处理问题失败: {e}")
        return {
            'answer': "抱歉，处理您的问题时出现错误，请稍后再试。",
            'conversation_id': conversation_id
        }

def get_suggestions():
    """获取推荐问题
    
    Returns:
        推荐问题列表
    """
    try:
        # 这里可以根据实际情况从数据库中获取或者固定返回一些推荐问题
        suggestions = [
            "学校有哪些专业？",
            "学校的历史是怎样的？",
            "学校有哪些校区？",
            "学校的师资力量如何？",
            "学校有哪些荣誉？"
        ]

        suggestions = random.sample(suggestions,3)
        
        return {
            'suggestions': suggestions
        }
    except Exception as e:
        print(f"获取推荐问题失败: {e}")
        return {
            'suggestions': []
        }