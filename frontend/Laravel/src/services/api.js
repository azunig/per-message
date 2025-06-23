// src/services/api.js
import axios from 'axios';
console.log("--- CARGANDO services/api.js (VERSIÓN FINAL 3.0) ---");

const apiClient = axios.create({
  baseURL: '/', 
  headers: {
    'Accept': 'application/json',
  }
});

// INTERCEPTOR DE PETICIONES
// Esto se ejecuta ANTES de que cada petición sea enviada
apiClient.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    // Si tenemos un token, lo añadimos a la cabecera de Authorization
    console.log("INTERCEPTOR: Token encontrado en localStorage. Añadiendo a la cabecera.", token); 
   
    config.headers.Authorization = `Bearer ${token}`;
  }
  else{
    console.warn("INTERCEPTOR: No se encontró token en localStorage al hacer la petición a:", config.url);
  }
  return config;
}, error => {
  return Promise.reject(error);
});

// funciones para llamar a endpoints protegidos
export default {
  login(credentials) {
    // La URL empieza con /api para que la intercepte el proxy
    
    return apiClient.post('/api/py/token', credentials);
  },

  getMessages(processId) {
    return apiClient.get(`/api/py/processes/${processId}/thread/`); // todos los mensajes
  },

  createMessage(payload, processId) {
    console.log("(payload) Ejecutando createMessage con el payload:", payload);

    const dataToSend = {  
      message: payload.content,
      process_id: processId,
      // 👇 AÑADE ESTA LÍNEA PARA ENVIAR EL ID DEL MENSAJE PADRE 👇
      // Si payload.replyingToId existe, se envía. Si no, se envía null.
      parent_id: payload.replyingToId || null 
    };

    
    console.log("(dataToSend) Ejecutando createMessage con el payload:", dataToSend);
    return apiClient.post('/api/py/messages/', dataToSend); // Crea un mensaje nuevo
  },

  replyToMessage(messageId, payload) {
    console.log(`(payload) Ejecutando replyToMessage para el ID ${messageId} con el payload:`, payload);

    const dataToSend = { message: payload.content };

    console.log(`(dataToSend) Ejecutando replyToMessage para el ID ${messageId} con el payload:`, dataToSend);
    return apiClient.post(`/api/py/messages/${messageId}/reply`, dataToSend); // Responde a un mensaje
  },

  // revisar como agregalo a bpm
  getCustomers() {
     console.log(`(payload) Ejecutando getCustomers`);

    return apiClient.get('https://jsonplaceholder.typicode.com/users');
  }
  // ... otras API o no? 
};