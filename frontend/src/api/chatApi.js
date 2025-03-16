import axios from 'axios';

// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:3000',
  timeout: 10000,
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
  // 获取聊天历史
  getChatHistory: async () => {
    try {
      const response = await api.get('/api/chat/history');
      return response.data;
    } catch (error) {
      console.error('获取聊天历史失败:', error);
      throw error;
    }
  },
  
  // 发送问题
  sendQuestion: async (data) => {
    try {
      const response = await api.post('/api/chat/question', data);
      return response.data;
    } catch (error) {
      console.error('发送问题失败:', error);
      throw error;
    }
  },
  
  // 清除聊天历史
  clearChatHistory: async () => {
    try {
      const response = await api.delete('/api/chat/history');
      return response.data;
    } catch (error) {
      console.error('清除聊天历史失败:', error);
      throw error;
    }
  },
  
  // 获取推荐问题
  getSuggestions: async () => {
    try {
      const response = await api.get('/api/chat/suggestions');
      return response.data;
    } catch (error) {
      console.error('获取推荐问题失败:', error);
      throw error;
    }
  }
};

export default chatApi;