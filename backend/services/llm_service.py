import requests
import json
from config import Config
from utils.logger import llm_logger
from utils.call_model import call_deepseek


def intention_recognition(question, history=None) -> dict:
    """调用DeepSeek API进行意图识别

    Args:
        question: 用户问题
        history: 对话历史，可选，格式为[{"role": "user", "content": "问题"}, {"role": "assistant", "content": "回答"}]

    Returns:
        意图识别结果
    """

    prompt = """你是一个专业的意图分类助手，需要判断用户问题是否需要通过向量检索学校知识库来回答。请结合对话历史上下文进行判断。
如果不需要检索，请直接根据上下文和常识生成合适的回答。

## 分类规则
1. 需要检索的情况比如：
   - 需要学校相关的具体信息（如"学校的地址在哪里？"）
   - 需要了解学校政策（如"学校的请假制度是什么？"）
   - 需要查询学校设施（如"图书馆开放时间是几点？"）
   - 需要了解学校课程（如"数学课的教材是什么？"）
   - 需要了解学校活动（如"什么时候举办运动会？"）

2. 不需要检索的情况：
   - 简单对话管理（如"你好"、"谢谢"）
   - 上下文已回答的问题（如针对上文的"能详细说说吗？"、"这个具体是什么意思？"）
   - 与学校无关的问题（如"今天天气怎么样？"）
   - 对已提供信息的追问或确认（如在解释了请假制度后问"那我需要找班主任吗？"）

## 对话历史
{history_text}

## 当前问题
{current_question}

## 输出格式
始终返回JSON格式：
{example}"""

    example = """{
    "need_retrieval": true/false,
    "reason": "分类理由",
    "rewritten_query": "优化后的查询(如有需要则填写，不需要则为空)",
    "direct_answer": "如果不需要检索，这里提供直接回答；需要检索则为空"
}
    """

    res = call_deepseek([{
        "role": "user",
        "content": prompt.format(
            history_text="\n".join([f"{msg['role']}: {msg['content']}" for msg in history]) if history else "无",
            current_question=question,
            example=example
        )
    }])
    res = res.replace("```json", "").replace("```", "").strip().strip("\n")
    json_data = json.loads(res)

    return json_data


def generate_answer(question, context, history=None):
    """调用DeepSeek API生成回答
    
    Args:
        question: 用户问题
        context: 检索到的相关上下文
        history: 对话历史，可选，格式为[{"role": "user", "content": "问题"}, {"role": "assistant", "content": "回答"}]
        
    Returns:
        生成的回答文本
    """
    try:
        # 构建提示词
        prompt = f"""你是一个学校知识问答助手，请根据以下提供的上下文信息，回答用户的问题，不要在回答中包含根据上下文的信息等句子。
        如果上下文中没有相关信息，请回答你不知道，不要编造信息。
        
        上下文信息：
        {context}
        
        用户问题：{question}
        
        请提供准确、简洁的回答："""
        
        # 构建消息列表
        messages = []
        
        # 如果有对话历史，先添加历史消息
        if history and isinstance(history, list):
            messages.extend(history)
        
        # 添加当前问题
        messages.append({"role": "user", "content": prompt})
        
        # 构建请求数据
        payload = {
            "model": "deepseek-v3-250324",
            "messages": messages,
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