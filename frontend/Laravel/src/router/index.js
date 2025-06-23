import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

import IndexView from '../views/IndexView.vue';
import ProfileView from '../views/ProfileView.vue';
import DashboardView from '../views/DashboardView.vue';
import LoginView from '../views/LoginView.vue';
import CustomersView from '../views/CustomersView.vue';
import TestPanelView from '../views/TestPanelView.vue';

const routes = [
  { path: '/', name: 'Index', component: IndexView  },
  { path: '/profile', name: 'Profile', component: ProfileView },
  { path: '/dashboard', name: 'Dashboard', component: DashboardView },
  { path: '/customers', name: 'Customers', component: CustomersView },
  { path: '/login', name: 'Login', component: LoginView },
  { path: '/test-panel', name: 'TestPanel', component: TestPanelView },
];


 // Usando la versión corregida que no da error para vite
const router = createRouter({history: createWebHistory(), routes });


router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const requiresAuth = ['Dashboard', 'Profile'];

  // CASO 1: La ruta requiere autenticación y el usuario NO está logueado
  if (requiresAuth.includes(to.name) && !authStore.isAuthenticated) {
    // Lo mandamos al login
    next({ name: 'Login' });
  } 
  // CASO 2: La ruta es 'Login' y el usuario SÍ está logueado
  else if (to.name === 'Login' && authStore.isAuthenticated) {
    // Lo mandamos al dashboard para que no vea el login de nuevo
    next({ name: 'Dashboard' });
  } 
  // CASO 3: Todos los demás casos (rutas públicas, o rutas protegidas con usuario logueado)
  else {
    // Lo dejamos pasar
    next();
  }
});

export default router;