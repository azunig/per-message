import { defineStore } from 'pinia';
import axios from 'axios'; // axios para el login
import api from '@/services/api';

const API_URL = 'http://127.0.0.1:8000';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  actions: {
    async login(credentials) {
      try {
        //const response = await axios.post('/api/login', credentials);
        const params = new URLSearchParams();
        params.append('username', credentials.email); 
        params.append('password', credentials.password);

        const response = await api.login(params);
      
        const token = response.data.access_token;

        if (!token) {
          console.error("La respuesta de la API no contenía un token.");
          throw new Error("Token no recibido");
        }
        console.log("✅ LOGIN EXITOSO: Token recibido y guardado:", token);
        this.token = token;
        localStorage.setItem('token', token);
        return true;

      } catch (error) {
        // Si algo falla, limpiamos todo.
        this.token = null;
        localStorage.removeItem('token');
        console.error('Error en la acción de login:', error);
        return false;
      }
    },
    logout() {
      this.token = null;
      this.user = null;
      localStorage.removeItem('token');
      // La redirección se manejará en el componente que llame a logout
    },
  },
});