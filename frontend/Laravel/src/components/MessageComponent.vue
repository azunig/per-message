<template>
  <div :style="{ 'margin-left': (depth * 25) + 'px' }" class="message-wrapper">
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
        {{ message.message }}
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

  const emit = defineEmits(['reply']);

  function emitReply() {
    emit('reply', props.message);
  }
  
  function reEmitReply(messageFromChild) {
    emit('reply', messageFromChild);
  }
</script>

<style scoped>
.message-wrapper {
  margin-top: 16px;
}
.replies {
  border-left: 2px solid #e0e0e0;
  padding-left: 10px;
  margin-top: 10px;
}
</style>