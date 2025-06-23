<template>
  <div class="message-thread" :class="{ 'is-current-user-thread': isCurrentUser }">
    <div class="message-bubble" :class="{ 'current-user-bubble': isCurrentUser, 
    'other-user-bubble': !isCurrentUser }">
      <p v-if="!isCurrentUser" class="font-weight-bold author-name mb-1">
        {{ message.owner?.name ?? 'Usuario Desconocido' }}
      </p>
      
      <p class="mb-1 message-text">{{ message.message }}</p>

      <p class="mb-0 message-time">{{ messageTime }}</p>
    </div>
    
    <v-btn
      icon="mdi-reply"
      variant="text"
      size="x-small"
      class="reply-button"
      @click="$emit('reply-to', message)"
    />
  </div>

  <div v-if="message.children && message.children.length > 0" class="replies-container">
    <ChatMessage
      v-for="child in message.children"
      :key="child.id"
      :message="child"
      :is-current-user="isCurrentUser" 
      @reply-to="$emit('reply-to', $event)"
    />
  </div>
</template>


<script setup>
import { computed } from 'vue';

// Este componente necesita saber el 'mensaje' a mostrar y si es del 'usuario actual'
const props = defineProps({
  message: {
    type: Object,
    required: true,
  },
  isCurrentUser: {
    type: Boolean,
    required: true,
  },
});

// Definimos que este componente puede "emitir" un evento llamado 'reply-to'
defineEmits(['reply-to']);

// Un pequeño detalle: formatear la hora para que se vea más limpia
const messageTime = computed(() => {
  return new Date(props.message.created_at).toLocaleTimeString('es-ES', {
    hour: '2-digit',
    minute: '2-digit',
  });
});
</script>

<style scoped>
.message-thread {
  display: flex;
  align-items: center; /* Alinea verticalmente la burbuja y el botón de responder */
  max-width: 85%;
  margin-top: 8px;
}

/* Alinea a la derecha los mensajes del usuario actual */
.is-current-user-thread {
  align-self: flex-end;
  flex-direction: row-reverse; /* Pone el botón de responder a la izquierda */
}

.message-bubble {
  padding: 10px 15px;
  border-radius: 18px;
  position: relative;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.current-user-bubble {
  background-color: #005c4b; /* Color tipo WhatsApp para "yo" */
  color: white;
  border-bottom-right-radius: 4px;
}

.other-user-bubble {
  background-color: #ffffff; /* Blanco o gris muy claro para "los demás" */
  color: #333;
  border-bottom-left-radius: 4px;
  border: 1px solid #f0f0f0;
}

.author-name {
  color: #0088cc; /* Color para destacar el nombre del autor */
  font-size: 0.9em;
}

.message-text {
  white-space: pre-wrap; /* Respeta saltos de línea y espacios */
  word-wrap: break-word; /* Evita que el texto se desborde */
}

.message-time {
  font-size: 0.75em;
  text-align: right;
  opacity: 0.8;
  margin-top: 4px;
}

.replies-container {
  /* La línea del hilo sigue siendo clave */
  padding-left: 20px;
  margin-left: 32px;
  border-left: 2px solid #e9e9e9;
}

/* El botón de responder aparece al pasar el mouse sobre el hilo */
.reply-button {
  opacity: 0;
  transition: opacity 0.2s ease-in-out;
}
.message-thread:hover .reply-button {
  opacity: 1;
}
</style>