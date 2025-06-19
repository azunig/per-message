<template>
  <div class="message-item" :style="{ 'margin-left': (depth * 20) + 'px' }">
    <div class="message-content">
      <p><strong>{{ message.user.name }}:</strong> {{ message.content }}</p>
      <v-btn size="x-small" variant="text" @click="$emit('reply', message.id)">
        Reply
      </v-btn>
    </div>
    
    <div v-if="message.replies && message.replies.length > 0" class="replies">
      <message-component
        v-for="reply in message.replies"
        :key="reply.id"
        :message="reply"
        :depth="depth + 1"
        @reply="$emit('reply', $event)"
      />
    </div>
  </div>
</template>

<script>
export default {
  name: 'MessageComponent', // El 'name' es crucial para la recursión
  props: {
    message: {
      type: Object,
      required: true
    },
    // Añadimos la propiedad 'depth'
    depth: {
      type: Number,
      required: true
    }
  },
  emits: ['reply'] // Buena práctica declarar los eventos que se emiten
}
</script>

<style scoped>
.message-item {
  margin-top: 10px;
  border-left: 2px solid transparent;
}
.message-content {
  padding-left: 10px;
}
.replies {
  margin-top: 10px;
  border-left: 2px solid #e0e0e0;
}
</style>