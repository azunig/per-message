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
          <div class="chat-title-bubble">
            <h2 class="chat-title-panel-text">
              Conversación Proceso #{{ chatStore.processId }}
            </h2>
          </div>  
          <v-btn 
            icon="mdi-close" 
            variant="text" 
            @click="chatStore.closeChat()"
            class="chat-close-btn"
          ></v-btn>
       
          
        </header>
        <div class="chat-explanation-area">
          <p class="mb-0">
            Este es tu espacio de colaboración. Responde a los mensajes, añade comentarios y mantén toda la comunicación del proceso en un solo lugar.
          </p>
        </div>

        <div class="messages-list-container" ref="messageContainerRef">
          </div>
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
// IMPORTACIONES CORREGIDAS Y COMPLETAS
import { ref, watch, nextTick, computed } from 'vue'; // Añadimos 'computed'
import ChatMessage from './ChatMessage.vue';
import { useChatStore } from '@/stores/chatStore';
import { useAuthStore } from '@/stores/auth'; // <-- CORRECCIÓN DE RUTA

//  STORES // REFERENCIAS Y ESTADO LOCAL
const chatStore = useChatStore();
const authStore = useAuthStore();
const messageContainerRef = ref(null);
const newMessage = ref('');
const isSending = ref(false);
const replyingTo = ref(null);
const currentUserId = computed(() => authStore.user?.id);

// FUNCIONES
const scrollToBottom = () => {
  nextTick(() => {
    const container = messageContainerRef.value;
    if (container) {
      container.scrollTop = container.scrollHeight;
    }
  });
};

const scrollToMessage = (messageId) => {
  nextTick(() => {
    const messageElement = document.getElementById(`message-${messageId}`);
    if (messageElement) {
      messageElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  });
};

//watch(() => chatStore.messages, scrollToBottom, { deep: true });

watch(
  () => chatStore.messages,
  (newMessages, oldMessages) => {
    if (oldMessages.length === 0 && newMessages.length > 0) {
      nextTick(() => {
        const container = messageContainerRef.value; // Corregido: usa R mayúscula
        if (container) container.scrollTop = container.scrollHeight;
      });
    }
  },
  { deep: true }
);

function handleReply(message) {
  replyingTo.value = message;
}

function cancelReply() {
  replyingTo.value = null;
}

async function handleSendMessage() {
  if (!newMessage.value.trim()) return;
  isSending.value = true;
  
  // La variable 'createdMessage' se declara aquí y recibe el resultado del store
  const createdMessage = await chatStore.sendMessage({
    content: newMessage.value,
    replyingToId: replyingTo.value ? replyingTo.value.id : null,
  });

  isSending.value = false;
  newMessage.value = '';
  replyingTo.value = null;

  // El 'if' ahora funciona porque 'createdMessage' existe (incluso si es undefined)
  if (createdMessage) {
    scrollToMessage(createdMessage.id);
  }
}

// Suponiendo que tienes esta función para el botón flotante
function handleToggleChat() {
  // Lógica para abrir/cerrar el chat 
  // chatStore.isPanelOpen ? chatStore.closeChat() : chatStore.openChat(unIdPorDefecto);
}
</script>

<style scoped>

/* ============================================= */
/* VARIABLES DE TEMA PARA EL CHAT         */
/*  modificar todo el panel. */
/* ============================================= */
.chat-panel {
  --chat-bg-color: #f7f9fa; /* Fondo del área de mensajes */
  --chat-input-bg-color: #ffffff; /* Fondo del área de input */
  --chat-header-bg-color: #ffffff; /* Fondo del encabezado */
  --chat-explanation-bg-color: #f7f9fa; /* Fondo del texto explicativo */
  --chat-border-color: #e9edf0; /* Color de los bordes sutiles */
  --chat-title-bubble-bg-color: #e7f3ff; /* Burbuja del título */
  --chat-title-text-color: #005a9e; /* Texto del título */
}

/* ============================================= */
/* ESTILOS DEL LAYOUT                */
/* ============================================= */
.chat-in-panel {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
  background-color: var(--chat-bg-color); /* Usando variable */
}

/* Encabezado */
.chat-header-panel {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 8px 12px 16px;
  flex-shrink: 0;
  border-bottom: 1px solid var(--chat-border-color); /* Usando variable */
  background-color: var(--chat-header-bg-color); /* Usando variable */
}



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
/* Lista de mensajes */
.messages-list-container {
  flex-grow: 1;
  overflow-y: auto;
  padding: 8px 16px;
  display: flex;
  flex-direction: column;
}
.replies-container {
  /* ESTAS LÍNEAS CREAN EL HILO VISUAL */
  margin-left: 52px; /* Indentación para las respuestas */
  margin-top: 15px;
  border-left: 2px solid #e0e0e0; /* La línea vertical del hilo */
  padding-left: 15px;
}
/* Área de input */
.message-input-area-panel {
  flex-shrink: 0;
  padding: 12px 16px;
  background-color: var(--chat-input-bg-color); /* Usando variable */
  border-top: 1px solid var(--chat-border-color); /* Usando variable */
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
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: transparent;
  padding: 4px 4px 4px 12px;
  border-left: 3px solid #007bff;
  margin-bottom: 8px;
}
.cursor-pointer {
  cursor: pointer;
}

/* Encabezado del chat 
.chat-header-panel {
  display: flex; 
  justify-content: space-between;  
  align-items: center; 
  padding: 12px 8px 12px 16px; 
  flex-shrink: 0; 
  border-bottom: 1px solid #eee; 
}*/

/* La nueva "burbuja" para el título */
.chat-title-bubble {
  background-color: var(--chat-title-bubble-bg-color); /* Usando variable */
  padding: 8px 16px;
  border-radius: 20px;
}

.chat-title-panel-text {
  font-size: 1rem;
  font-weight: 600;
  margin: 0;
  color: var(--chat-title-text-color); /* Usando variable */
}

.chat-close-btn {
  /* Pequeño ajuste para el botón de cerrar */
  margin-left: 8px;
}

.chat-explanation-area {
  padding: 16px;
  background-color: var(--chat-explanation-bg-color); /* Usando variable */
  font-size: 0.875rem;
  color: #555;
  flex-shrink: 0;
  border-bottom: 1px solid var(--chat-border-color); /* Usando variable */
}
</style>