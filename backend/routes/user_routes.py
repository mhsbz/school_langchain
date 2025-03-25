from flask import Blueprint, request, jsonify
from services.user_service import register_user, login_user
from utils.logger import user_logger

# 创建用户蓝图
user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
def handle_register():
    """
    处理用户注册
    
    请求体:
    {
        "username": "用户名",
        "phone": "手机号",
        "password": "密码"
    }
    
    响应:
    成功:
    {
        "success": true,
        "user_id": "用户ID"
    }
    
    失败:
    {
        "success": false,
        "message": "错误信息"
    }
    """
    try:
        data = request.get_json()
        
        # 验证请求数据
        if not data or 'username' not in data or 'phone' not in data or 'password' not in data:
            user_logger.warning('注册请求缺少必要参数')
            return jsonify({'success': False, 'message': '缺少必要参数'}), 400
        
        username = data['username']
        phone = data['phone']
        password = data['password']
        
        user_logger.info(f'收到用户注册请求: username={username}, phone={phone[:3]}****{phone[-4:]}')
        
        # 调用注册服务
        result = register_user(username, phone, password)
        
        if result['success']:
            user_logger.info(f'用户注册成功: username={username}, user_id={result["user_id"]}')
            return jsonify(result), 201
        else:
            user_logger.warning(f'用户注册失败: username={username}, 原因={result["message"]}')
            return jsonify(result), 400
    except Exception as e:
        user_logger.error(f"处理注册请求失败: {e}", exc_info=True)
        return jsonify({'success': False, 'message': '服务器内部错误'}), 500

@user_bp.route('/login', methods=['POST'])
def handle_login():
    """
    处理用户登录（简化版）
    
    请求体:
    {
        "phone": "手机号"
    }
    
    响应:
    成功:
    {
        "success": true,
        "user": {
            "user_id": "用户ID",
            "username": "用户名",
            "phone": "手机号"
        }
    }
    
    失败:
    {
        "success": false,
        "message": "错误信息"
    }
    """
    try:
        data = request.get_json()
        
        # 验证请求数据
        if not data or 'phone' not in data:
            return jsonify({'success': False, 'message': '缺少手机号参数'}), 400
        
        phone = data['phone']
        
        # 调用登录服务
        result = login_user(phone)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 401
    except Exception as e:
        print(f"处理登录请求失败: {e}")
        return jsonify({'success': False, 'message': '服务器内部错误'}), 500