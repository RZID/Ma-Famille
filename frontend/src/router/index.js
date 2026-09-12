import { createRouter, createWebHistory } from 'vue-router'

import HealthView from '../views/HealthView.vue'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/health', name: 'health', component: HealthView },
  ],
})

export default router
