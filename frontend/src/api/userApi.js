import axios from 'axios';

// 创建axios实例
const api = axios.create({
  // baseURL: 'http://backend:5001/api',
  // baseURL: 'http://localhost:5001/api',
  baseURL: 'api',
  // baseURL: 'http://39.107.159.184:5001/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 用户相关API
const userApi = {
  // 用户注册
  register: async (userData) => {
    try {
      const response = await api.post('/user/register', userData);
      return response.data;
    } catch (error) {
      console.error('注册失败:', error);
      throw error;
    }
  },
  
  // 用户登录
  login: async (credentials) => {
    try {
      const response = await api.post('/user/login', credentials);
      return response.data;
    } catch (error) {
      console.error('登录失败:', error);
      throw error;
    }
  },
  
  // 获取当前用户信息
  getCurrentUser: () => {
    const userStr = localStorage.getItem('user');
    if (userStr) {
      return JSON.parse(userStr);
    }
    return null;
  },
  
  // 退出登录
  logout: () => {
    localStorage.removeItem('user');
  }
};

export default userApi;