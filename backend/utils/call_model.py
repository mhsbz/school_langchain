from openai import OpenAI
from config import Config
import requests

def call_deepseek(messages: list) -> str:

    """
    使用OpenAI调用deepseek模型
    
    Args:
        messages: 对话消息列表,包含多轮对话历史
        api_key: OpenAI API密钥
        model: 模型名称,默认为deepseek-chat
        
    Returns:
        str: 模型返回的响应文本
    """
    api_key = Config.DEEPSEEK_API_KEY
    api_url = Config.DEEPSEEK_API_URL
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # 初始化OpenAI客户端
            client = OpenAI(api_key=api_key,base_url="https://api.deepseek.com")
            
            # 调用模型生成响应
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                temperature=0.1,
                stream=False,
                max_tokens=1000
            )
            
            # 返回生成的文本
            return response.choices[0].message.content
            
        except Exception as e:
            retry_count += 1
            # 错误处理
            print(f"调用deepseek模型时发生错误 (尝试 {retry_count}/{max_retries}): {str(e)}")
            if retry_count == max_retries:
                return ""

def call_sharegpt(conv_id: str, message: str) -> str:
    url = "http://39.107.159.184:3000/api/v1/chat/completions"

    headers = {
        "Authorization": "Bearer fastgpt-cYz8Kx2D5eeGj34UKDhg8LzZ1SDx6iAA5aiUNLVrkK131wSgNOfC0HuEJ",
        "Content-Type": "application/json"
    }

    payload = {
        "chatId": conv_id,
        "messages": [
            {
                "role": "user",
                "content": message
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)

    response = response.json()

    return response["choices"][0]["message"]["content"]
# 打印响应
    # print(response.status_code)
    # print(response.)