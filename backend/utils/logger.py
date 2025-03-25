import os
import logging
import datetime
from logging.handlers import TimedRotatingFileHandler
from config import Config

# 创建日志目录
def ensure_log_dir():
    """确保日志目录存在"""
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return log_dir

# 配置日志格式
log_format = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 创建日志处理器
def get_file_handler(log_name='app'):
    """获取文件日志处理器
    
    Args:
        log_name: 日志文件名前缀
        
    Returns:
        TimedRotatingFileHandler: 按日期滚动的文件处理器
    """
    log_dir = ensure_log_dir()
    log_file = os.path.join(log_dir, f'{log_name}.log')
    
    # 创建TimedRotatingFileHandler，按天滚动日志
    file_handler = TimedRotatingFileHandler(
        filename=log_file,
        when='midnight',  # 每天午夜滚动
        interval=1,       # 间隔为1天
        backupCount=30,   # 保留30天的日志
        encoding='utf-8'
    )
    
    # 设置日志后缀格式为日期
    file_handler.suffix = "%Y-%m-%d"
    file_handler.setFormatter(log_format)
    
    return file_handler

# 创建控制台处理器
def get_console_handler():
    """获取控制台日志处理器
    
    Returns:
        StreamHandler: 控制台处理器
    """
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    return console_handler

# 获取日志记录器
def get_logger(name, level=logging.INFO):
    """获取日志记录器
    
    Args:
        name: 日志记录器名称
        level: 日志级别，默认为INFO
        
    Returns:
        Logger: 日志记录器
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 避免重复添加处理器
    if not logger.handlers:
        # 添加文件处理器
        logger.addHandler(get_file_handler(name))
        
        # 添加控制台处理器
        logger.addHandler(get_console_handler())
    
    return logger

# 创建应用主日志记录器
app_logger = get_logger('app')

# 创建各模块日志记录器
db_logger = get_logger('db')
llm_logger = get_logger('llm')
chat_logger = get_logger('chat')
user_logger = get_logger('user')
vector_logger = get_logger('vector')