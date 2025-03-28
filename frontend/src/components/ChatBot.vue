<template>
  <div class="chat-container">
    <!-- 侧边栏抽屉 -->
    <div class="drawer" :class="{ 'drawer-open': isDrawerOpen }">
      <div class="drawer-header">
        <h3>对话历史</h3>
        <div class="close-drawer" @click="toggleDrawer">&times;</div>
      </div>
      <div class="drawer-content">
        <!-- 新建对话按钮 -->
        <div class="new-chat-button" @click="createNewChat">
          <img src="@/assets/images/新对话图标.png" alt="新对话">
          <span>开启新对话</span>
        </div>
        <!-- 历史对话列表 -->
        <div class="history-list">
          <div 
            v-for="(history, index) in chatHistory" 
            :key="index"
            class="history-item"
            :class="{ 'active': selectedHistoryIndex === index }"
          >
            <div class="history-content" @click="selectHistory(index)">
              <div class="history-icon">
                <img :src="selectedHistoryIndex === index ? require('@/assets/images/侧边栏历史对话图标（选择）.png') : require('@/assets/images/历史对话图标（未选中）.png')" alt="历史对话">
              </div>
              <div class="history-title">{{ history.title }}</div>
            </div>
            <div class="delete-button" @click.stop="deleteHistory(index)">
              <img src="@/assets/images/清除图标.png" alt="删除" class="delete-icon">
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 遮罩层 -->
    <div class="drawer-mask" v-if="isDrawerOpen" @click="toggleDrawer"></div>
    
    <!-- 头部标题 -->
    <div class="chat-header">
      <div class="menu-icon" @click="toggleDrawer">
        <img src="@/assets/images/侧边框图标.png" alt="菜单" class="menu-img">
      </div>
      <img src="@/assets/images/智融千问.png" alt="智融千问" class="logo">
      <div class="new-chat-icon" @click="createNewChat">
        <img src="@/assets/images/新对话图标.png" alt="新对话" class="new-chat-img">
      </div>
    </div>
    
    <!-- 聊天内容区域 -->
    <div class="chat-content" ref="chatContent">
      <!-- 机器人自我介绍 -->
      <div class="intro-message">
        <div class="avatar-container">
          <img src="@/assets/images/机器人头像.png" alt="机器人" class="robot-avatar">
        </div>
        <div class="intro-box">
          <p style="text-align: left;">您好，我是智融千问，您的智能助手。我可以回答关于学校的各种问题，包括历史、专业设置、师资力量等。请问有什么可以帮助您的吗？</p>
        </div>
      </div>
      
      <!-- 聊天记录 -->
      <div v-for="(message, index) in messages" :key="index" class="message-container" :class="message.type">
        <!-- 用户消息 -->
        <template v-if="message.type === 'user'">
          <div class="message user-message">
            <div class="message-content">{{ message.content }}</div>
          </div>
        </template>
        
        <!-- 机器人消息 -->
        <template v-else>
          <div class="avatar-container">
            <img src="@/assets/images/机器人头像.png" alt="机器人" class="robot-avatar">
          </div>
          <div class="message bot-message">
            <div class="message-content" style="text-align: left;">{{ message.content }}</div>
          </div>
        </template>
      </div>
      
      <!-- 机器人回答中的加载状态 -->
      <div class="message-container bot" v-if="isLoading && messages.length > 0 && messages[messages.length-1].type === 'user'">
        <div class="avatar-container">
          <img src="@/assets/images/机器人头像.png" alt="机器人" class="robot-avatar">
        </div>
        <div class="message bot-message">
          <div class="message-content typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 猜你想问区域 -->
    <div class="suggestions-container" v-if="suggestions.length > 0 && !hasConversationStarted">
      <div class="suggestions-header">
        <div class="header-content">
          <span>猜你想问</span>
          <div class="refresh-button" @click="refreshSuggestions">
            <span>换一换</span>
            <img src="@/assets/images/猜你想问刷新图标.png" alt="刷新" class="refresh-icon">
          </div>
        </div>
      </div>
      <div class="suggestions-list">
        <div 
          v-for="(suggestion, index) in suggestions" 
          :key="index" 
          class="suggestion-item"
          @click="selectSuggestion(suggestion)"
        >
          <span>{{ suggestion }}</span>
          <img src="@/assets/images/猜你想问跳转图标.png" alt="跳转" class="jump-icon">
        </div>
      </div>
    </div>
    
    <!-- 输入区域 -->
    <div class="input-container">
      <div class="input-box">
        <input 
          type="text" 
          v-model="inputMessage" 
          placeholder="请输入您的问题"
          @keyup.enter="sendMessage"
          @focus="handleInputFocus"
          @blur="handleInputBlur"
        >
      </div>
      <div class="send-button" @click="sendMessage">
        <img src="@/assets/images/发送.png" alt="发送" class="send-icon">
      </div>
    </div>
  </div>
</template>

<script>
import chatApi from '@/api/chatApi';
import userApi from '@/api/userApi';

export default {
  name: 'ChatBot',
  data() {
    return {
      inputMessage: '',
      messages: [],
      suggestions: [],
      isDrawerOpen: false,
      chatHistory: [],
      selectedHistoryIndex: -1,
      currentConversationId: null,
      isLoading: false,
      currentUser: null,
      hasConversationStarted: false
    }
  },
  created() {
    // 获取当前用户信息
    this.currentUser = userApi.getCurrentUser();
    // 获取推荐问题
    this.fetchSuggestions();
    // 获取对话历史
    this.fetchConversations();
  },
  
  // 监听消息数组变化，自动滚动到底部
  watch: {
    messages: {
      handler() {
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      },
      deep: true
    }
  },
  methods: {
    // 退出登录
    handleLogout() {
      userApi.logout();
      this.$router.push('/login');
    },
    
    // 监听消息变化，自动滚动到底部
    updated() {
      this.scrollToBottom();
    },
    
    // 处理输入框获得焦点事件（输入法弹出）
    handleInputFocus() {
      // 当输入框获得焦点时，隐藏"猜你想问"区域
      this.hasConversationStarted = true;
      
      // 防止输入法弹出时页面被顶上去
      setTimeout(() => {
        window.scrollTo(0, 0);
        document.body.scrollTop = 0;
        document.documentElement.scrollTop = 0;
        
        // 确保聊天内容区域滚动到底部
        this.scrollToBottom();
      }, 100);
    },
    
    // 处理输入框失去焦点事件
    handleInputBlur() {
      // 如果没有对话开始，恢复显示"猜你想问"区域
      if (this.messages.length === 0) {
        this.hasConversationStarted = false;
      }
      
      // 防止输入法收起时页面布局异常
      setTimeout(() => {
        window.scrollTo(0, 0);
        document.body.scrollTop = 0;
        document.documentElement.scrollTop = 0;
      }, 100);
    },
    async fetchSuggestions() {
      try {
        const response = await chatApi.getSuggestions();
        this.suggestions = response.suggestions;
      } catch (error) {
        console.error('获取推荐问题失败:', error);
        // 使用默认推荐问题生成
        this.generateDefaultSuggestions();
      }
    },
    async fetchConversations() {
      try {
        // 使用chatApi获取所有对话，不需要token
        const conversations = await chatApi.getChatHistory();
        
        this.chatHistory = conversations.map(conv => ({
          id: conv._id,
          title: conv.title,
          messages: []
        }));
      } catch (error) {
        console.error('获取对话历史失败:', error);
      }
    },
    async loadConversationMessages(conversationId) {
      try {
        const messages = await chatApi.getConversationMessages(conversationId);
        const mappedMessages = messages.map(msg => ({
          content: msg.content,
          type: msg.role === 'user' ? 'user' : 'bot'
        }));
        
        // 如果有消息，设置对话已开始，隐藏"猜你想问"区域
        if (mappedMessages.length > 0) {
          this.hasConversationStarted = true;
        }
        
        return mappedMessages;
      } catch (error) {
        console.error('获取对话消息失败:', error);
        return [];
      }
    },
    toggleDrawer() {
      this.isDrawerOpen = !this.isDrawerOpen;
    },
    async selectHistory(index) {
      this.selectedHistoryIndex = index;
      this.currentConversationId = this.chatHistory[index].id;
      // 加载历史对话内容
      this.isLoading = true;
      this.messages = await this.loadConversationMessages(this.currentConversationId);
      this.isLoading = false;
      this.toggleDrawer();
    },
    async deleteHistory(index) {
      // 删除历史对话
      const conversationId = this.chatHistory[index].id;
      try {
        // 调用chatApi中的deleteConversation方法
        await chatApi.deleteConversation(conversationId);
        
        this.chatHistory.splice(index, 1);
        if (this.selectedHistoryIndex === index) {
          this.messages = [];
          this.selectedHistoryIndex = -1;
          this.currentConversationId = null;
        } else if (this.selectedHistoryIndex > index) {
          this.selectedHistoryIndex--;
        }
      } catch (error) {
        console.error('删除对话失败:', error);
      }
    },
    createNewChat() {
      // 创建新对话
      this.messages = [];
      this.selectedHistoryIndex = -1;
      this.currentConversationId = null;
      // 重置对话状态，显示"猜你想问"区域
      this.hasConversationStarted = false;
      // 刷新推荐问题
      this.refreshSuggestions();
      // 如果抽屉是打开的，则关闭它
      if (this.isDrawerOpen) {
        this.toggleDrawer();
      }
    },
    async sendMessage() {
      if (this.inputMessage.trim() === '') return;
      
      // 添加用户消息
      this.messages.push({
        content: this.inputMessage,
        type: 'user'
      });
      
      // 设置对话已开始，隐藏"猜你想问"区域
      this.hasConversationStarted = true;
      
      // 保存用户输入
      const question = this.inputMessage;
      
      // 清空输入框
      this.inputMessage = '';
      
      // 显示加载状态
      this.isLoading = true;
      
      try {
        // 调用API发送问题
        const response = await chatApi.sendQuestion({
          question: question,
          conversation_id: this.currentConversationId
        });
        
        // 如果是新对话，保存对话ID
        if (!this.currentConversationId && response.conversation_id) {
          this.currentConversationId = response.conversation_id;
          // 刷新对话列表
          this.fetchConversations();
        }
        
        // 添加机器人回复
        this.messages.push({
          content: response.answer,
          type: 'bot'
        });
      } catch (error) {
        console.error('发送问题失败:', error);
        // 添加错误消息
        this.messages.push({
          content: '抱歉，发送问题时出现错误，请稍后再试。',
          type: 'bot'
        });
      } finally {
        this.isLoading = false;
        
        // 滚动到底部 - 确保在DOM更新后执行
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      }
    }},
    clearInput() {
      this.inputMessage = '';
    },
    selectSuggestion(suggestion) {
      this.inputMessage = suggestion;
      this.sendMessage();
    },
    async refreshSuggestions() {
      try {
        // 从后端获取新的推荐问题
        const response = await chatApi.getSuggestions();
        this.suggestions = response.suggestions;
      } catch (error) {
        console.error('刷新推荐问题失败:', error);
        // 使用本地随机生成
        const allSuggestions = [
          '学校有哪些专业？',
          '学校的历史是怎样的？',
          '学校有哪些校区？',
          '学校的师资力量如何？',
          '学校有哪些荣誉？',
          '学校的就业情况如何？',
          '学校有哪些实验室？',
          '学校的图书馆藏书量是多少？',
          '学校的国际交流项目有哪些？',
          '学校的奖学金政策是什么？'
        ];
        
        // 随机选择5个问题
        this.suggestions = [];
        const usedIndices = new Set();
        
        while (this.suggestions.length < 3 && usedIndices.size < allSuggestions.length) {
          const randomIndex = Math.floor(Math.random() * allSuggestions.length);
          if (!usedIndices.has(randomIndex)) {
            usedIndices.add(randomIndex);
            this.suggestions.push(allSuggestions[randomIndex]);
          }
        }
      }
    },
    scrollToBottom() {
      if (this.$refs.chatContent) {
        // 使用setTimeout确保在DOM完全更新后执行滚动
        setTimeout(() => {
          this.$refs.chatContent.scrollTop = this.$refs.chatContent.scrollHeight;
          
          // 防止iOS输入法弹出时页面滚动问题
          window.scrollTo(0, 0);
          document.body.scrollTop = 0;
          document.documentElement.scrollTop = 0;
        }, 150); // 增加延迟时间，确保在键盘弹出后也能正确滚动
      }
    }
  }
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100%;
  max-width: 100%;
  margin: 0 auto;
  background-color: #f5f5f5;
  position: relative;
  overflow-x: hidden;
  /* 防止输入法弹出时页面被顶上去 */
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

/* 菜单图标样式 */
.chat-header {
  background-color: #a8d0ff;
  padding: 10px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 10;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.menu-icon {
  cursor: pointer;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.menu-img {
  width: 24px;
  height: 24px;
}

.logo {
  height: 30px;
  margin: 0 auto;
}

.new-chat-icon {
  width: 32px;
  height: 32px;
  background-color: #007AFF;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.new-chat-icon:hover {
  transform: scale(1.05);
}

.new-chat-icon:active {
  transform: scale(0.95);
}

.new-chat-icon .new-chat-img {
  width: 20px;
  height: 20px;
}

.new-chat-span {
  color: white;
  font-size: 24px;
  font-weight: bold;
  line-height: 1;
}

/* 抽屉组件样式 */
.drawer {
  position: fixed;
  top: 0;
  left: -85%;
  width: 85%;
  height: 100%;
  background-color: #f8f8f8;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  transition: left 0.3s ease;
  display: flex;
  flex-direction: column;
}

@media (max-width: 480px) {
  .drawer {
    left: -80%;
    width: 80%;
  }
}

.drawer-open {
  left: 0;
}

.drawer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #e0e0e0;
  background-color: #a8d0ff;
}

.drawer-header h3 {
  margin: 0;
  font-size: 18px;
  color: #333;
  font-weight: 500;
}

.close-drawer {
  font-size: 24px;
  cursor: pointer;
  color: #333;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.drawer-content {
  flex: 1;
  overflow-y: auto;
  padding: 15px;
  display: flex;
  flex-direction: column;
}

.history-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0;
  margin-top: 15px;
  overflow-y: auto;
}

.history-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px 10px;
  transition: background-color 0.2s;
  border-bottom: 1px solid #eaeaea;
}

.history-item:hover {
  background-color: #f0f0f0;
}

.history-item.active {
  background-color: #e6f2ff;
  position: relative;
}

.history-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: 4px;
  background-color: #4a90e2;
}

.history-content {
  display: flex;
  align-items: center;
  flex: 1;
  cursor: pointer;
}

.history-icon {
  margin-right: 12px;
}

.history-icon img {
  width: 24px;
  height: 24px;
}

.history-title {
  font-size: 15px;
  color: #333;
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.delete-button {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  opacity: 0.7;
  transition: opacity 0.2s;
}

.delete-button:hover {
  opacity: 1;
}

.delete-icon {
  width: 16px;
  height: 16px;
}

.new-chat-button {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px 15px;
  background-color: #ffffff;
  border-radius: 30px;
  cursor: pointer;
  margin-bottom: 15px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  border: 1px solid #e0e0e0;
}

.new-chat-button:hover {
  background-color: #f8f8f8;
}

.new-chat-button img {
  width: 20px;
  height: 20px;
  margin-right: 8px;
}

.new-chat-button span {
  color: #4a90e2;
  font-weight: 500;
  font-size: 15px;
}

.drawer-mask {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.4);
  z-index: 999;
}

.chat-content {
  flex: 1;
  overflow-y: auto;
  padding: 15px;
  padding-bottom: 120px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  -webkit-overflow-scrolling: touch; /* 增强iOS滚动体验 */
  /* 防止输入法弹出时内容区域被推上去 */
  position: absolute;
  top: 50px; /* 头部标题高度 */
  left: 0;
  right: 0;
  bottom: 70px; /* 输入框高度 */
  height: auto;
  padding-top: 25px; /* 增加顶部内边距，确保第一条消息不被覆盖 */
}

.message-container {
  display: flex;
  margin-bottom: 15px;
}

.message-container.user {
  justify-content: flex-end;
}

.message-container.bot {
  justify-content: flex-start;
}

.avatar-container {
  margin-right: 10px;
}

.robot-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
}

.message {
  max-width: 75%;
  padding: 10px 14px;
  border-radius: 10px;
  position: relative;
  word-break: break-word;
  box-sizing: border-box;
}

.user-message {
  background-color: #007AFF;
  color: white;
  border-radius: 18px 4px 18px 18px;
  align-self: flex-end;
}

.bot-message {
  background-color: white;
  color: #333;
  border-radius: 4px 18px 18px 18px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  align-self: flex-start;
}

.feedback-buttons {
  display: none;
}

.feedback-btn {
  display: none;
}

.intro-message {
  display: flex;
  margin-bottom: 20px;
}

.intro-box {
  background-color: white;
  padding: 15px;
  border-radius: 4px 18px 18px 18px;
  max-width: 80%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.suggestions-container {
  background-color: white;
  padding: 15px;
  margin-bottom: 0; /* 紧贴输入栏 */
  border-radius: 10px 10px 0 0;
  box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.05);
  width: 100%;
  box-sizing: border-box;
  position: absolute;
  bottom: 70px; /* 与输入框的高度保持一致，确保紧贴输入栏 */
  left: 0;
  z-index: 10;
}

.suggestions-header {
  margin-bottom: 15px;
  position: relative;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(to right, #4a90e2, #67b8ff);
  border-radius: 8px;
  padding: 10px 15px;
  color: white;
}

.suggestions-header span {
  font-weight: bold;
  color: white;
}

.refresh-button {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.refresh-button span {
  margin-right: 5px;
  font-size: 14px;
}

.refresh-icon {
  width: 16px;
  height: 16px;
  transition: transform 0.3s ease;
}

.refresh-button:hover .refresh-icon {
  transform: rotate(180deg);
}

.suggestions-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.suggestion-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 15px;
  background-color: #f5f5f5;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  cursor: pointer;
  color: #333;
  transition: background-color 0.2s ease;
  text-align: left;
}

.suggestion-item:hover {
  background-color: #e8e8e8;
}

.jump-icon {
  width: 16px;
  height: 16px;
}

.input-container {
  display: flex;
  padding: 15px;
  background-color: white;
  border-top: 1px solid #eee;
  align-items: center;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 1001;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
  max-height: 70px;
  transition: transform 0.3s ease;
  /* 防止输入法弹出时页面被顶上去 */
  position: absolute;
  bottom: 0;
}

.input-box {
  flex: 1;
  position: relative;
  display: flex;
  align-items: center;
  background-color: #f5f5f5;
  border-radius: 25px;
  padding: 0 15px;
  margin: 0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

input {
  flex: 1;
  width: 100%;
  padding: 12px 40px 12px 0;
  border: none;
  background: transparent;
  font-size: 15px;
  outline: none;
}

.clear-icon {
  position: absolute;
  right: 60px;
  cursor: pointer;
  width: 16px;
  height: 16px;
  z-index: 2;
}

.send-button {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  margin-left: 8px;
  transition: transform 0.2s ease;
}

.send-button:hover {
  transform: scale(1.05);
}

.send-button:active {
  transform: scale(0.95);
}

.send-icon {
  width: 24px;
  height: 24px;
}

/* 打字指示器样式 */
.typing-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 6px 10px;
  min-width: 40px;
}

.typing-indicator span {
  height: 8px;
  width: 8px;
  float: left;
  margin: 0 1px;
  background-color: #9E9EA1;
  display: block;
  border-radius: 50%;
  opacity: 0.4;
}

.typing-indicator span:nth-of-type(1) {
  animation: 1s blink infinite 0.3333s;
}

.typing-indicator span:nth-of-type(2) {
  animation: 1s blink infinite 0.6666s;
}

.typing-indicator span:nth-of-type(3) {
  animation: 1s blink infinite 0.9999s;
}

@keyframes blink {
  50% {
    opacity: 1;
  }
}

@media (max-width: 768px) {
  .chat-container {
    max-width: 100%;
  }
  
  .message {
    max-width: 75%;
  }
  
  .chat-header {
    padding: 8px;
  }
  
  .logo {
    height: 26px;
  }
  
  .chat-content {
    padding: 12px;
    gap: 12px;
    padding-bottom: 120px; /* 增加底部内边距，确保最后一条消息不被输入框遮挡 */
  }
  
  .suggestions-container {
    padding: 12px;
    margin-bottom: 70px; /* 增加底部边距 */
  }
  
  .suggestion-item {
    padding: 8px 12px;
    font-size: 14px;
  }
  
  .input-container {
    padding: 10px;
  }
  
  .input-box {
    padding: 0 10px;
  }
  
  input {
    padding: 10px 10px 10px 0;
    font-size: 14px;
  }
}

@media (max-width: 480px) {
  .message {
    max-width: 80%;
  }
  
  .intro-box {
    max-width: 80%;
    padding: 12px;
    font-size: 14px;
  }
  
  .message-content {
    font-size: 14px;
  }
  
  .drawer-header h3 {
    font-size: 16px;
  }
  
  .history-title {
    font-size: 13px;
  }
  
  .feedback-btn {
    width: 20px;
    height: 20px;
  }
  
  .robot-avatar {
    width: 32px;
    height: 32px;
  }
  
  .avatar-container {
    margin-right: 8px;
  }
  
  .send-button {
    width: 28px;
    height: 28px;
  }
  
  .send-icon {
    width: 20px;
    height: 20px;
  }
  
  .new-chat-icon {
    width: 28px;
    height: 28px;
  }
  
  .new-chat-icon .new-chat-img {
    width: 18px;
    height: 18px;
  }
  
  /* 移动端键盘弹出时的适配 */
  .chat-content {
    padding-bottom: 140px; /* 增加更多底部内边距 */
  }
  
  /* 确保抽屉在移动端不会太宽 */
  .drawer-content {
    padding: 10px;
  }
  
  /* 优化移动端滚动体验 */
  .history-list {
    -webkit-overflow-scrolling: touch;
  }
}

/* 处理iOS键盘弹出的特殊情况 */
@supports (-webkit-touch-callout: none) {
  .chat-content {
    padding-bottom: 160px; /* iOS设备额外增加底部内边距 */
  }
}
</style>