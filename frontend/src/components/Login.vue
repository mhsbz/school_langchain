<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-header">
        <h2>登录</h2>
      </div>
      
      <div class="login-form">
        
        <!-- 手机号输入框 -->
        <div class="form-item">
          <label for="phone" class="centered-label">手机号</label>
          <div class="input-container">
            <input 
              type="text" 
              id="phone" 
              v-model="phone" 
              placeholder="请输入手机号"
              class="centered-input"
            >
          </div>
          <div class="error-message" v-if="errors.phone">{{ errors.phone }}</div>
        </div>
        
        <!-- 密码输入框已移除 -->
        
        <!-- 登录按钮 -->
        <div class="form-item button-container">
          <button class="submit-button" @click="handleSubmit">登录</button>
        </div>
        
        <!-- 全局错误/成功消息 -->
        <div class="form-item" v-if="errors.general">
          <div class="error-message">{{ errors.general }}</div>
        </div>
        <div class="form-item" v-if="errors.success">
          <div class="success-message">{{ errors.success }}</div>
        </div>
        
        <!-- 切换登录/注册已移除 -->
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Login',
  data() {
    return {
      phone: '',
      errors: {
        phone: '',
        general: '',
        success: ''
      }
    }
  },
  methods: {
    // 清空表单
    clearForm() {
      this.phone = '';
      this.errors = {
        phone: '',
        general: '',
        success: ''
      };
    },
    
    // 验证表单
    validateForm() {
      let isValid = true;
      this.errors = {
        phone: '',
        general: '',
        success: ''
      };
      
      // 验证手机号
      if (!this.phone.trim()) {
        this.errors.phone = '请输入手机号';
        isValid = false;
      } else if (!/^1[3-9]\d{9}$/.test(this.phone)) {
        this.errors.phone = '请输入正确的手机号';
        isValid = false;
      }
      
      return isValid;
    },
    
    // 处理登录
    async handleSubmit() {
      if (!this.validateForm()) {
        return;
      }
      
      try {
        // 登录请求
        const response = await axios.post('http://localhost:5000/api/user/login', {
          phone: this.phone
        });
        
        if (response.data.success) {
          // 保存用户信息到本地存储
          localStorage.setItem('user', JSON.stringify(response.data.user));
          
          // 跳转到首页
          this.$router.push('/');
        }
      } catch (error) {
        console.error('请求失败:', error);
        
        // 处理错误响应
        if (error.response && error.response.data) {
          this.errors.general = error.response.data.message || '操作失败，请稍后再试';
        } else {
          this.errors.general = '网络错误，请检查网络连接';
        }
        
        // 3秒后清除错误消息
        setTimeout(() => {
          this.errors.general = '';
        }, 5000);
      }
    }
  }
}
</script>

<style scoped>
/* 添加居中样式 */
.centered-.form-item .error-message {
  color: #ff4d4f;
  font-size: 12px;
  margin-top: 6px;
  display: block;
  font-weight: 500;
  animation: fadeIn 0.3s ease;
  text-align: center;
}

.form-item .success-message {
  color: #52c41a;
  font-size: 12px;
  margin-top: 6px;
  display: block;
  font-weight: 500;
  animation: fadeIn 0.3s ease;
  text-align: center;
}

label {
  text-align: center;
}

.centered-input {
  text-align: center;
}

.input-container {
  display: flex;
  justify-content: center;
}

.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
  background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
  overflow: hidden;
  position: relative;
}

.login-container::before {
  content: '';
  position: absolute;
  width: 200%;
  height: 200%;
  top: -50%;
  left: -50%;
  z-index: 0;
  background: radial-gradient(ellipse at center, rgba(255,255,255,0.3) 0%, rgba(255,255,255,0) 70%);
  animation: pulse 15s infinite;
}

@keyframes pulse {
  0% { transform: scale(1); opacity: 0.8; }
  50% { transform: scale(1.05); opacity: 0.5; }
  100% { transform: scale(1); opacity: 0.8; }
}

.login-box {
  width: 420px;
  padding: 40px;
  background-color: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(5px);
  position: relative;
  z-index: 1;
  transition: all 0.3s ease;
}

.login-header {
  text-align: center;
  margin-bottom: 35px;
}

.login-header h2 {
  color: #2c3e50;
  font-weight: 600;
  font-size: 28px;
  letter-spacing: 1px;
  margin: 0;
  position: relative;
  display: inline-block;
}

.login-header h2::after {
  content: '';
  position: absolute;
  width: 40px;
  height: 3px;
  background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  border-radius: 3px;
}

.form-item {
  margin-bottom: 24px;
  position: relative;
  text-align: center;
}

.form-item .error-message {
  color: #ff4d4f;
  font-size: 12px;
  margin-top: 6px;
  display: block;
  font-weight: 500;
  animation: fadeIn 0.3s ease;
  text-align: center;
}

.form-item .success-message {
  color: #52c41a;
  font-size: 12px;
  margin-top: 6px;
  display: block;
  font-weight: 500;
  animation: fadeIn 0.3s ease;
  text-align: center;
}

label {
  display: block;
  margin-bottom: 10px;
  font-size: 14px;
  color: #2c3e50;
  font-weight: 500;
  transition: all 0.3s;
}

input {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #e8e8e8;
  border-radius: 8px;
  font-size: 15px;
  transition: all 0.3s ease;
  background-color: rgba(255, 255, 255, 0.8);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.02);
}

input:focus {
  border-color: #4facfe;
  outline: none;
  box-shadow: 0 4px 12px rgba(79, 172, 254, 0.15);
  background-color: #fff;
}

input::placeholder {
  color: #b3b3b3;
  font-size: 14px;
}

.error-message {
  color: #ff4d4f;
  font-size: 12px;
  margin-top: 6px;
  display: block;
  font-weight: 500;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-5px); }
  to { opacity: 1; transform: translateY(0); }
}

.button-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.submit-button {
  width: 60%;
  padding: 14px;
  background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(79, 172, 254, 0.3);
  letter-spacing: 0.5px;
  position: relative;
  overflow: hidden;
}

.submit-button:hover {
  background: linear-gradient(90deg, #4facfe 0%, #00f2fe 70%);
  box-shadow: 0 6px 20px rgba(79, 172, 254, 0.4);
  transform: translateY(-2px);
}

.submit-button:active {
  transform: translateY(1px);
  box-shadow: 0 2px 10px rgba(79, 172, 254, 0.3);
}

.switch-mode {
  text-align: center;
  margin-top: 20px;
  padding-top: 15px;
  position: relative;
}

.switch-mode::before {
  content: '';
  position: absolute;
  top: 0;
  left: 25%;
  width: 50%;
  height: 1px;
  background: linear-gradient(90deg, rgba(230, 230, 230, 0) 0%, rgba(230, 230, 230, 1) 50%, rgba(230, 230, 230, 0) 100%);
}

.switch-mode span {
  color: #4facfe;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
  padding: 5px 10px;
  border-radius: 4px;
}

.switch-mode span:hover {
  color: #00f2fe;
  background-color: rgba(79, 172, 254, 0.05);
}
</style>