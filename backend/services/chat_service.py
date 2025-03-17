import datetime
import uuid
from services.db_service import get_db
from services.vector_store import get_vector_store
from services.llm_service import generate_answer

def get_chat_history():
    """获取所有对话历史
    
    Returns:
        对话历史列表
    """
    try:
        db = get_db()
        conversations = db['conversations']
        
        # 获取所有对话，按时间倒序排列
        result = list(conversations.find().sort('created_at', -1))
        
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

def create_conversation(title):
    """创建新对话
    
    Args:
        title: 对话标题
        
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
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now()
        }
        
        conversations.insert_one(conversation)
        
        return conversation['_id']
    except Exception as e:
        print(f"创建对话失败: {e}")
        return None

def save_message(conversation_id, content, role):
    """保存消息
    
    Args:
        conversation_id: 对话ID
        content: 消息内容
        role: 角色（user或assistant）
        
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

def delete_conversation(conversation_id):
    """删除对话及其所有消息
    
    Args:
        conversation_id: 对话ID
        
    Returns:
        是否删除成功
    """
    try:
        db = get_db()
        conversations = db['conversations']
        messages = db['messages']
        
        # 删除对话
        conversations.delete_one({'_id': conversation_id})
        
        # 删除对话的所有消息
        messages.delete_many({'conversation_id': conversation_id})
        
        return True
    except Exception as e:
        print(f"删除对话失败: {e}")
        return False

def clear_all_history():
    """清除所有对话历史
    
    Returns:
        是否清除成功
    """
    try:
        db = get_db()
        conversations = db['conversations']
        messages = db['messages']
        
        # 删除所有对话和消息
        conversations.delete_many({})
        messages.delete_many({})
        
        return True
    except Exception as e:
        print(f"清除所有对话历史失败: {e}")
        return False

def process_question(question, conversation_id=None):
    """处理用户问题
    
    Args:
        question: 用户问题
        conversation_id: 对话ID，如果为None则创建新对话
        
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
            conversation_id = create_conversation(title)
        
        # 保存用户问题和系统回答
        save_message(conversation_id, question, 'user')
        save_message(conversation_id, answer, 'assistant')
        
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
        
        return {
            'suggestions': suggestions
        }
    except Exception as e:
        print(f"获取推荐问题失败: {e}")
        return {
            'suggestions': []
        }