import { createRouter, createWebHistory } from 'vue-router';
import ChatBot from '@/components/ChatBot.vue';
import HelloWorld from '@/components/HelloWorld.vue';
import Login from '@/components/Login.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: ChatBot,
    meta: { requiresAuth: true }
  },
  {
    path: '/hello',
    name: 'HelloWorld',
    component: HelloWorld
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  }
];

const router = createRouter({
  history: createWebHistory('/'),
  routes
});

// 路由守卫
router.beforeEach((to, from, next) => {
  // 检查路由是否需要认证
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // 检查用户是否已登录
    const userStr = localStorage.getItem('user');
    const isLoggedIn = userStr && JSON.parse(userStr).user_id;
    
    if (!isLoggedIn) {
      // 未登录，重定向到登录页
      next({ name: 'Login' });
    } else {
      // 已登录，允许访问
      next();
    }
  } else {
    // 不需要认证的路由，直接访问
    next();
  }
});

export default router;