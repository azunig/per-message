<template>
  <div :style="{ 'margin-left': (depth * 20) + 'px' }" class="message-wrapper">
    
    <v-card variant="text" class="message-item">
      <v-card-item>
        <template #prepend>
          <v-avatar>
            <v-img 
              :src="`https://i.pravatar.cc/40?u=${message.owner.name}`" 
              :alt="message.owner.name">
            </v-img>
          </v-avatar>
        </template>
        
        <v-card-title class="font-weight-bold pa-0">{{ message.owner.name }}</v-card-title>
        <v-card-subtitle class="pa-0">{{ new Date(message.created_at).toLocaleString() }}</v-card-subtitle>
      </v-card-item>

      <v-card-text class="py-2">
        {{ message.content }}
      </v-card-text>

      <v-card-actions>
        <v-btn size="small" variant="text" @click="emitReply">Responder</v-btn>
      </v-card-actions>
    </v-card>

    <div v-if="message.children && message.children.length > 0" class="replies">
      <MessageComponent
        v-for="reply in message.children"
        :key="reply.id"
        :message="reply"
        :depth="depth + 1"
        @reply="reEmitReply"
      />
    </div>
  </div>
</template>

<script setup>
  // Un único bloque de script moderno
  // Con <script setup>, Vue infiere el nombre del componente del nombre del archivo,
  // por lo que la recursividad funciona automáticamente.

  // 1. Definimos las props que el componente recibe
  const props = defineProps({
    message: {
      type: Object,
      required: true
    },
    depth: {
      type: Number,
      required: true
    }
  });

  // 2. Definimos el evento 'reply' que este componente puede emitir hacia su padre
  const emit = defineEmits(['reply']);

  // 3. Función que se ejecuta al hacer clic en el botón "Responder"
  function emitReply() {
    // Emite el evento 'reply' con el objeto completo del mensaje actual
    emit('reply', props.message);
  }
  
  // 4. Función que "re-emite" un evento que viene de un hijo más anidado
  function reEmitReply(messageFromChild) {
    // Esto asegura que el evento 'reply' suba por todo el árbol hasta el GlobalChatPanel
    emit('reply', messageFromChild);
  }
</script>

<style scoped>
.message-wrapper {
  margin-top: 16px;
}
.replies {
  border-left: 2px solid #e0e0e0;
  padding-left: 15px; /* Un poco de padding para que se vea la línea */
  margin-top: 10px;
}
</style>