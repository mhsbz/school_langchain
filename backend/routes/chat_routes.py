from flask import Blueprint, request, jsonify
from services.chat_service import (
    process_question,
    get_chat_history,
    get_conversation_messages,
    delete_conversation,
    clear_all_history,
    get_suggestions
)

# 创建蓝图
chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/question', methods=['POST'])
def handle_question():
    """处理用户问题
    
    请求体:
    {
        "question": "用户问题",
        "conversation_id": "可选，对话ID",
        "user_id": "可选，用户ID"
    }
    
    响应:
    {
        "answer": "回答内容",
        "conversation_id": "对话ID"
    }
    """
    try:
        data = request.get_json()
        
        # 验证请求数据
        if not data or 'question' not in data:
            return jsonify({'error': '缺少必要参数'}), 400
        
        question = data['question']
        conversation_id = data.get('conversation_id')
        user_id = data.get('user_id')  # 获取用户ID
        
        # 处理问题
        result = process_question(question, conversation_id, user_id)
        print(result)
        
        return jsonify(result)
    except Exception as e:
        print(f"处理问题请求失败: {e}")
        return jsonify({'error': '服务器内部错误'}), 500

@chat_bp.route('/history', methods=['GET'])
def handle_get_history():
    """获取对话历史
    
    查询参数:
    conversation_id: 可选，对话ID，如果提供则返回该对话的所有消息，否则返回所有对话
    user_id: 可选，用户ID，如果提供则只返回该用户的对话
    
    响应:
    如果提供conversation_id，返回消息列表
    否则返回对话列表
    """
    try:
        conversation_id = request.args.get('conversation_id')
        user_id = request.args.get('user_id')  # 获取用户ID
        
        if conversation_id:
            # 获取指定对话的所有消息
            messages = get_conversation_messages(conversation_id)
            return jsonify(messages)
        else:
            # 获取对话历史，如果提供了用户ID则只返回该用户的对话
            conversations = get_chat_history(user_id)
            return jsonify(conversations)
    except Exception as e:
        print(f"获取历史请求失败: {e}")
        return jsonify({'error': '服务器内部错误'}), 500

@chat_bp.route('/history', methods=['DELETE'])
def handle_delete_history():
    """删除对话历史
    
    查询参数:
    conversation_id: 可选，对话ID，如果提供则删除该对话，否则清除所有对话历史
    user_id: 可选，用户ID，如果提供则只删除该用户的对话历史
    
    响应:
    {
        "success": true/false
    }
    """
    try:
        conversation_id = request.args.get('conversation_id')
        user_id = request.args.get('user_id')  # 获取用户ID
        
        if conversation_id:
            # 删除指定对话，如果提供了用户ID则只删除该用户的对话
            success = delete_conversation(conversation_id, user_id)
        else:
            # 清除对话历史，如果提供了用户ID则只清除该用户的对话历史
            success = clear_all_history(user_id)
        
        return jsonify({'success': success})
    except Exception as e:
        print(f"删除历史请求失败: {e}")
        return jsonify({'error': '服务器内部错误'}), 500

@chat_bp.route('/suggestions', methods=['GET'])
def handle_get_suggestions():
    """获取推荐问题
    
    响应:
    {
        "suggestions": ["问题1", "问题2", ...]
    }
    """
    try:
        result = get_suggestions()
        return jsonify(result)
    except Exception as e:
        print(f"获取推荐问题请求失败: {e}")
        return jsonify({'error': '服务器内部错误'}), 500