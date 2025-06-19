import { createRouter, createWebHistory } from 'vue-router';
import IndexView from '../views/IndexView.vue';
import ProfileView from '../views/ProfileView.vue';
import DashboardView from '../views/DashboardView.vue';


const routes = [
  {
    path: '/',
    name: 'Index',
    component: IndexView 
  },
  {
    path: '/profile',
    name: 'Profile',
    component: ProfileView
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardView
  }
];

const router = createRouter({
  history: createWebHistory(), // Usando la versión corregida que no da error para vite
  routes
});

export default router;