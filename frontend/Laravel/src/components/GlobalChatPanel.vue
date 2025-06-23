<template>
  <div>
    <v-btn
      v-if="!chatStore.isPanelOpen"
      icon
      class="chat-toggle"
      @click="handleToggleChat"
      color="primary"
      elevation="8"
      size="large"
    >
      <v-icon>mdi-message-text</v-icon>
    </v-btn>

    <div class="side-panel chat-panel" :class="{ open: chatStore.isPanelOpen }">
      
      <div class="chat-in-panel" v-if="chatStore.processId">
        
        <header class="chat-header-panel">
          <h2 class="chat-title-panel">Conversación Proceso #{{ chatStore.processId }}</h2>
          <v-btn icon="mdi-close" variant="text" @click="chatStore.closeChat()"></v-btn>
        </header>

        <div class="messages-list-container">
          <div v-if="chatStore.isLoading" class="d-flex justify-center align-center fill-height">
            <v-progress-circular indeterminate color="primary"></v-progress-circular>
          </div>
          <div v-else-if="chatStore.error" class="pa-4">
            <v-alert type="error" variant="tonal">{{ chatStore.error }}</v-alert>
          </div>
          <div v-else-if="!chatStore.messages || chatStore.messages.length === 0" class="d-flex justify-center align-center fill-height text-grey">
            <p>Aún no hay mensajes en esta conversación.</p>
          </div>
          
          <div v-else class="messages-list-panel">
            <ChatMessage
              v-for="message in chatStore.messages"
              :key="message.id"
              :message="message"
              :is-current-user="message.owner.id === currentUserId"
              @reply-to="handleReply"
            />
          </div>
        </div>

        <div class="message-input-area-panel">
          <v-expand-transition>
            <div v-if="replyingTo" class="replying-to-banner">
              <div>
                <p class="mb-0 text-caption">Respondiendo a:</p>
                <p class="mb-0 font-weight-bold text-body-2 text-truncate">
                  "{{ replyingTo.owner.name }}"
                </p>
              </div>
              <v-btn icon="mdi-close" variant="text" size="x-small" @click="cancelReply"></v-btn>
            </div>
          </v-expand-transition>

          <v-text-field
            v-model="newMessage"
            placeholder="Escribe un mensaje..."
            variant="solo"
            rounded
            flat
            hide-details
            autofocus
            @keydown.enter.prevent="handleSendMessage"
          >
            <template #append-inner>
              <v-icon
                v-if="newMessage.trim()"
                color="primary"
                @click="handleSendMessage"
              >
                mdi-send
              </v-icon>
            </template>
          </v-text-field>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
// 1. IMPORTACIONES CORREGIDAS Y COMPLETAS
import { ref, watch, nextTick, computed } from 'vue'; // Añadimos 'computed'
import ChatMessage from './ChatMessage.vue';
import { useChatStore } from '@/stores/chatStore';
import { useAuthStore } from '@/stores/auth'; // <-- CORRECCIÓN DE RUTA

// 2. STORES
const chatStore = useChatStore();
const authStore = useAuthStore();

// 3. REFERENCIAS Y ESTADO LOCAL
const messageContainerRef = ref(null);
const newMessage = ref('');
const isSending = ref(false);
const replyingTo = ref(null);

// 4. PROPIEDAD COMPUTADA (LA MEJORA CRUCIAL)
// Esto es más seguro. currentUserId solo tendrá un valor cuando authStore.user exista.
const currentUserId = computed(() => authStore.user?.id);

// 5. FUNCIONES (SIN CAMBIOS)
const scrollToBottom = () => {
  nextTick(() => {
    const container = messageContainerRef.value;
    if (container) {
      container.scrollTop = container.scrollHeight;
    }
  });
};

watch(() => chatStore.messages, scrollToBottom, { deep: true });

function handleReply(message) {
  replyingTo.value = message;
}

function cancelReply() {
  replyingTo.value = null;
}

async function handleSendMessage() {
  if (!newMessage.value.trim()) return;
  isSending.value = true;
  await chatStore.sendMessage({
    content: newMessage.value,
    replyingToId: replyingTo.value ? replyingTo.value.id : null,
  });
  isSending.value = false;
  newMessage.value = '';
  replyingTo.value = null;
}

// Suponiendo que tienes esta función para el botón flotante
function handleToggleChat() {
  // Lógica para abrir/cerrar el chat si la tienes aquí
  // Por ejemplo: chatStore.isPanelOpen ? chatStore.closeChat() : chatStore.openChat(unIdPorDefecto);
}
</script>

<style scoped>
.side-panel {
  position: fixed;
  top: 0;
  right: -100%; /* Inicia oculto fuera de la pantalla */
  height: 100%;
  width: 50vw;
  max-width: 700px;
  min-width: 400px;
  background-color: #fff;
  box-shadow: -4px 0 10px rgba(0,0,0,0.1);
  z-index: 1005;
  transition: right .3s ease-in-out; /* La animación de deslizamiento */
  display: flex;
  flex-direction: column;
}
.side-panel.open {
  right: 0; /* La clase 'open' lo hace visible */
}
.chat-in-panel {
  display: flex; /* ¡Activamos Flexbox! */
  flex-direction: column; /* Apilamos los elementos verticalmente */
  height: 100%; /* Ocupa toda la altura del panel */
  overflow: hidden; /* Evita que el panel entero tenga scroll */
}
/*.chat-header-panel { 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  padding: 15px 25px; 
  border-bottom: 1px solid #eee; 
  flex-shrink: 0; 
}*/
.chat-header-panel {
  flex-shrink: 0; /* Evita que el encabezado se encoja */
}
.messages-list-panel {
  flex-grow: 1; 
  overflow-y: auto; 
  padding: 20px; 
}
.message-input-area-panel { 
  padding: 15px 25px; 
  border-top: 1px solid #eee; 
  flex-shrink: 0; 
}
.message-thread {
  margin-bottom: 20px;
}
.message-container {
  display: flex;
  align-items: flex-start;
}
.message-content {
  flex-grow: 1;
}
.messages-list-container {
  flex-grow: 1; /* Hace que este elemento crezca y ocupe el espacio sobrante */
  overflow-y: auto; /* AÑADE EL SCROLL VERTICAL SOLO A ESTA ÁREA */
  padding: 16px; /* Añadimos un poco de espacio interior */
}
.replies-container {
  /* ESTAS LÍNEAS CREAN EL HILO VISUAL */
  margin-left: 52px; /* Indentación para las respuestas */
  margin-top: 15px;
  border-left: 2px solid #e0e0e0; /* La línea vertical del hilo */
  padding-left: 15px;
}
.message-input-area-panel {
  flex-shrink: 0; /* Evita que el área de input se encoja */
  padding: 16px;
  background-color: #ffffff;
  border-top: 1px solid #e0e0e0;
}
.reply-link {
  color: #888;
  cursor: pointer;
  font-size: 0.8em;
  text-transform: uppercase;
  font-weight: bold;
  margin-left: 10px; /* Un poco de espacio */
}
.reply-link:hover {
  color: #333;
}
.replying-to-banner {
  background-color: #f0f0f0;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 0.9em;
  margin-bottom: 5px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.cursor-pointer {
  cursor: pointer;
}
</style>