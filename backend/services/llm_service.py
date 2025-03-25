import requests
import json
from config import Config
from utils.logger import llm_logger

def generate_answer(question, context):
    """调用DeepSeek API生成回答
    
    Args:
        question: 用户问题
        context: 检索到的相关上下文
        
    Returns:
        生成的回答文本
    """
    try:
        # 构建提示词
        prompt = f"""你是一个学校知识问答助手，请根据以下提供的上下文信息，回答用户的问题。
        如果上下文中没有相关信息，请回答你不知道，不要编造信息。
        
        上下文信息：
        {context}
        
        用户问题：{question}
        
        请提供准确、简洁的回答："""
        
        # 构建请求数据
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 800,
            "stream": False,
        }

        print(Config.DEEPSEEK_API_KEY)
        
        # 设置请求头
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {Config.DEEPSEEK_API_KEY}"
        }
        
        # 发送请求
        response = requests.post(
            Config.DEEPSEEK_API_URL,
            headers=headers,
            data=json.dumps(payload)
        )
        
        # 解析响应
        if response.status_code == 200:
            result = response.json()
            answer = result['choices'][0]['message']['content']
            return answer
        else:
            print(f"DeepSeek API请求失败: {response.status_code} {response.text}")
            return "抱歉，我暂时无法回答您的问题，请稍后再试。"
    
    except Exception as e:
        print(f"生成回答时出错: {e}")
        return "抱歉，生成回答时出现错误，请稍后再试。"