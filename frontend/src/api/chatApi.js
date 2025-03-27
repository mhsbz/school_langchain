import axios from 'axios';

// 创建axios实例
const api = axios.create({
  // baseURL: 'api',
  // baseURL: 'http://39.107.159.184:5001/api',
  baseURL: 'http://localhost:5001/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 请求拦截器 - 简化版本，不添加token
api.interceptors.request.use(
  config => {
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// 响应拦截器 - 处理错误
api.interceptors.response.use(
  response => response,
  error => {
    console.error('API请求错误:', error);
    return Promise.reject(error);
  }
);

// 聊天相关API
const chatApi = {
  // 获取对话消息
  getConversationMessages: async (conversationId) => {
    try {
      // 从localStorage获取当前用户信息
      const userStr = localStorage.getItem('user');
      let userId = null;
      
      if (userStr) {
        const user = JSON.parse(userStr);
        userId = user.user_id;
      }
      
      // 添加user_id参数到请求URL
      const response = await api.get(`/chat/messages?conversation_id=${conversationId}${userId ? `&user_id=${userId}` : ''}`);
      return response.data;
    } catch (error) {
      console.error('获取对话消息失败:', error);
      throw error;
    }
  },
  
  // 获取聊天历史
  getChatHistory: async () => {
    try {
      // 从localStorage获取当前用户信息
      const userStr = localStorage.getItem('user');
      let userId = null;
      
      if (userStr) {
        const user = JSON.parse(userStr);
        userId = user.user_id;
      }
      
      // 添加user_id参数到请求URL
      const response = await api.get(`/chat/history${userId ? `?user_id=${userId}` : ''}`);
      return response.data;
    } catch (error) {
      console.error('获取聊天历史失败:', error);
      throw error;
    }
  },
  
  // 发送问题
  sendQuestion: async (data) => {
    try {
      // 从localStorage获取当前用户信息
      const userStr = localStorage.getItem('user');
      if (userStr) {
        const user = JSON.parse(userStr);
        // 添加user_id到请求数据中
        data.user_id = user.user_id;
      }
      
      const response = await api.post('/chat/question', data);
      console.log("sendQuestion response",response)
      return response.data;
    } catch (error) {
      console.error('发送问题失败:', error);
      throw error;
    }
  },
  
  // 清除聊天历史
  clearChatHistory: async () => {
    try {
      const response = await api.delete('/chat/history');
      return response.data;
    } catch (error) {
      console.error('清除聊天历史失败:', error);
      throw error;
    }
  },
  
  // 获取推荐问题
  getSuggestions: async () => {
    try {
      const response = await api.get('/chat/suggestions');
      return response.data;
    } catch (error) {
      console.error('获取推荐问题失败:', error);
      throw error;
    }
  },
  
  // 删除指定对话
  deleteConversation: async (conversationId) => {
    try {
      // 从localStorage获取当前用户信息
      const userStr = localStorage.getItem('user');
      let userId = null;
      
      if (userStr) {
        const user = JSON.parse(userStr);
        userId = user.user_id;
      }
      
      // 添加user_id参数到请求URL
      const response = await api.delete(`/chat/history?conversation_id=${conversationId}${userId ? `&user_id=${userId}` : ''}`);
      return response.data;
    } catch (error) {
      console.error('删除对话失败:', error);
      throw error;
    }
  }
};

export default chatApi;