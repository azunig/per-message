// src/stores/chatStore.js
import { defineStore } from 'pinia';
import api from '@/services/api';

export const useChatStore = defineStore('chat', {
  state: () => ({
    isPanelOpen: false,
    processId: null,
    messages: [],
    isLoading: false,
    error: null,
  }),
  actions: {
    
  async sendMessage(messageData) {
    if (!this.processId) {
      console.error("No se puede enviar un mensaje: no hay un processId activo.");
      this.error = "Error: No se ha seleccionado ninguna conversación.";
      return;
    }
    
    this.error = null;

    try {
      // 👇 ESTA ES LA LÍNEA QUE CAMBIA 👇
      // Llamamos a la función de la API con los dos argumentos que espera:
      // 1. El objeto con el contenido (messageData)
      // 2. El ID del proceso (this.processId)
      await api.createMessage(messageData, this.processId);

      // Al tener éxito, refrescamos los mensajes para ver el nuevo
      await this.fetchMessages();
      
    } catch (err) {
      console.error("Error al enviar el mensaje:", err);
      this.error = "No se pudo enviar el mensaje. Inténtalo de nuevo.";
    }
  },

  async openChat(processId) {
    // Verificamos que recibimos un ID
    if (!processId) {
      console.error("Se necesita un processId para abrir el chat.");
      return;
    }
    
    console.log(`Tienda Pinia: Abriendo chat para el proceso ID ${processId}`);
    
    // Guardamos el estado
    this.isPanelOpen = true;
    this.processId = processId;
    
    // Llamamos a la función para cargar los mensajes para ESE proceso
    await this.fetchMessages();
  },

  closeChat() {
    this.isPanelOpen = false;
    setTimeout(() => {
      this.processId = null;
      this.messages = [];
      this.error = null;
    }, 300);
  },

    async fetchMessages() {
      if (!this.processId) return;
      this.isLoading = true;
      this.error = null;
      try {
        const response = await api.getMessages(this.processId);
        console.log(`Respuesta de la API (ya anidada) para el proceso ID ${this.processId}:`, response.data);
        
        // ANTES: this.messages = this.buildThreadedMessages(response.data);
        // AHORA: Simplemente asignamos los datos directamente. ¡Listo!
        this.messages = response.data;

      } catch (err) {
        console.error("Error al obtener mensajes:", err);
        this.error = "No se pudieron cargar las conversaciones.";
      } finally {
        this.isLoading = false;
      }
    },
 /* 
buildThreadedMessages(messagesList) {
    const messageMap = {};
    // Primero, preparamos cada mensaje y lo guardamos en un mapa para acceso rápido
    messagesList.forEach(message => {
      message.children = []; // Aseguramos que cada mensaje tenga un array para sus hijos
      messageMap[message.id] = message;
    });

    const threadedMessages = [];
    messagesList.forEach(message => {
      // Si el mensaje tiene un 'parent_id' y su padre existe en el mapa...
      if (message.parent_id && messageMap[message.parent_id]) {
        // ...lo añadimos al array 'children' de su padre.
        messageMap[message.parent_id].children.push(message);
      } else {
        // Si no tiene padre, es un mensaje de nivel raíz.
        threadedMessages.push(message);
      }
    });
    return threadedMessages;
  }
*/

  },
});