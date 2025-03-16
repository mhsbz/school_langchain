import { createRouter, createWebHistory } from 'vue-router';
import ChatBot from '@/components/ChatBot.vue';
import HelloWorld from '@/components/HelloWorld.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: ChatBot
  },
  {
    path: '/hello',
    name: 'HelloWorld',
    component: HelloWorld
  }
];

const router = createRouter({
  history: createWebHistory('/'),
  routes
});

export default router;