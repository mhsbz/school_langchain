import uuid
import datetime
import hashlib
import re
from services.db_service import get_db

def hash_password(password):
    """
    对密码进行哈希处理
    """
    return hashlib.sha256(password.encode()).hexdigest()

def validate_phone(phone):
    """
    验证手机号格式是否正确
    """
    pattern = re.compile(r'^1[3-9]\d{9}$')  # 中国大陆手机号格式
    return bool(pattern.match(phone))

def register_user(username, phone, password):
    """
    注册新用户
    
    Args:
        username: 用户名
        phone: 手机号
        password: 密码
        
    Returns:
        成功返回用户ID，失败返回错误信息
    """
    try:
        # 验证手机号格式
        if not validate_phone(phone):
            return {'success': False, 'message': '手机号格式不正确'}
        
        db = get_db()
        users = db['users']
        
        # 检查手机号是否已存在
        if users.find_one({'phone': phone}):
            return {'success': False, 'message': '该手机号已被注册'}
        
        # 检查用户名是否已存在
        if users.find_one({'username': username}):
            return {'success': False, 'message': '该用户名已被使用'}
        
        # 创建新用户
        user_id = str(uuid.uuid4())
        user = {
            '_id': user_id,
            'username': username,
            'phone': phone,
            'password': hash_password(password),
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now()
        }
        
        users.insert_one(user)
        
        return {'success': True, 'user_id': user_id}
    except Exception as e:
        print(f"注册用户失败: {e}")
        return {'success': False, 'message': '服务器内部错误'}

def login_user(phone, password=None):
    """
    用户登录（简化版）
    
    Args:
        phone: 手机号
        password: 密码（可选，不再验证）
        
    Returns:
        成功返回用户信息，失败返回错误信息
    """
    try:
        # 验证手机号格式
        if not validate_phone(phone):
            return {'success': False, 'message': '手机号格式不正确'}
            
        db = get_db()
        users = db['users']
        
        # 查找用户
        user = users.find_one({'phone': phone})
        
        # 如果用户不存在，自动创建新用户
        if not user:
            # 创建新用户
            user_id = str(uuid.uuid4())
            username = f'用户_{phone[-4:]}' # 使用手机号后四位作为用户名
            
            user = {
                '_id': user_id,
                'username': username,
                'phone': phone,
                'password': hash_password('123456'), # 设置默认密码
                'created_at': datetime.datetime.now(),
                'updated_at': datetime.datetime.now()
            }
            
            users.insert_one(user)
        
        # 返回用户信息（不包含密码）
        user_info = {
            'user_id': user['_id'],
            'username': user['username'],
            'phone': user['phone']
        }
        
        return {'success': True, 'user': user_info}
    except Exception as e:
        print(f"用户登录失败: {e}")
        return {'success': False, 'message': '服务器内部错误'}

def get_user_by_id(user_id):
    """
    根据用户ID获取用户信息
    
    Args:
        user_id: 用户ID
        
    Returns:
        用户信息
    """
    try:
        db = get_db()
        users = db['users']
        
        user = users.find_one({'_id': user_id})
        if not user:
            return None
        
        # 不返回密码
        user.pop('password', None)
        
        return user
    except Exception as e:
        print(f"获取用户信息失败: {e}")
        return None