<template>
  <div class="d-flex fill-height">
    <v-navigation-drawer permanent :width="400" app>
      <v-container>
        <div class="d-flex align-center pa-4">
          <v-avatar size="80">
            <v-img src="https://i.pravatar.cc/150?u=assaf"></v-img>
          </v-avatar>
          <div class="ml-4 flex-grow-1">
            <h1 class="text-h5 font-weight-bold">Assaf Rappaport</h1>
            <p class="text-body-2 mb-1">VP of Customer Operations</p>
          </div>
        </div>
        <v-tabs v-model="tab" color="black">
          <v-tab value="posts">Posts</v-tab>
          <v-tab value="pages">Pages</v-tab>
        </v-tabs>
        <v-divider></v-divider>
      </v-container>
    </v-navigation-drawer>
    
    <div class="main-content-area flex-grow-1">
      </div>

    <v-btn icon class="timeline-toggle" @click="toggleTimelinePanel">
      <v-icon>{{ timelineDrawer ? 'mdi-chevron-right' : 'mdi-chevron-left' }}</v-icon>
    </v-btn>
    <v-btn @click="chatStore.openChat(101)">
      Abrir Chat del Proceso 101
    </v-btn>

    <div class="side-panel timeline-panel" :class="{ open: timelineDrawer }">
      </div>


  </div>
</template>

<script setup>
// ===== IMPORTS =====
import { ref, onMounted } from 'vue';
import api from '@/services/api';
// import MessageComponent from '@/components/MessageComponent.vue';

import { useChatStore } from '@/stores/chatStore';
const chatStore = useChatStore();

// ===== ESTADO DEL COMPONENTE =====
const TEMP_PROCESS_ID = 101; // <-- 

const tab = ref('posts');

const timelineDrawer = ref(false);
const chatDrawer = ref(false);

// const messages = ref([]);
// const isLoading = ref(true);
// const error = ref(null);

// const newMessage = ref('');
const isSending = ref(false);
// const replyingTo = ref(null);

const events = ref([
  { id: 1, date: '2023-01-01', title: 'Started Project', description: 'Kicked off.', icon: 'mdi-rocket', color: 'primary' },
]);


// ===== FUNCIONES =====

// 2. LA FUNCIÓN QUE OBTIENE LOS DATOS Y USA LA TRANSFORMACIÓN
/* async function fetchMessages() {
  isLoading.value = true;
  error.value = null;
  try {
    const response = await api.getMessages(TEMP_PROCESS_ID);
    
    // Asignamos directamente los datos anidados que vienen de la API
    messages.value = response.data;

    // Un log para confirmar que todo llega bien
    console.log("Datos ANIDADOS recibidos de la API:", messages.value);

  } catch (err) {
    console.error("Error al obtener mensajes:", err);
    error.value = "No se pudieron cargar las conversaciones.";
  } finally {
    isLoading.value = false;
  }
} */

/* async function handleSendMessage() {
  if (!newMessage.value.trim()) return;
  isSending.value = true;
  try {
    const payload = { content: newMessage.value };
    
    if (replyingTo.value) {
      await api.replyToMessage(replyingTo.value.id, payload);
    } else {
      await api.createMessage(payload, TEMP_PROCESS_ID);
    }
    newMessage.value = '';
    replyingTo.value = null;
    await fetchMessages();
  } catch (err) {
    console.error("Error al enviar el mensaje:", err);
    alert("Hubo un error al enviar tu mensaje.");
  } finally {
    isSending.value = false;
  }
} */


/* function handlePrepareReply(message) {
  replyingTo.value = message;
} */

/* function cancelReply() {
  replyingTo.value = null;
} */

function toggleTimelinePanel() {
  timelineDrawer.value = !timelineDrawer.value;
  if (timelineDrawer.value) { chatDrawer.value = false; }
}

function toggleChatPanel() {
  chatDrawer.value = !chatDrawer.value;
  if (chatDrawer.value) { timelineDrawer.value = false; }
}

onMounted(() => {
  fetchMessages();
});
</script>

<style scoped>
.main-content-area { background-color: #121212; }
.side-panel { position: fixed; top: 0; height: 100%; width: 50vw; max-width: 700px; min-width: 400px; background-color: #fff; box-shadow: -4px 0 10px rgba(0, 0, 0, 0.2); z-index: 1005; transition: right 0.3s ease-in-out; display: flex; flex-direction: column; right: -100%; }
.side-panel.open { right: 0; }
.timeline-toggle, .chat-toggle { position: fixed; right: 16px; z-index: 1006; background-color: white; transform: translateY(-50%); }
.timeline-toggle { top: 45%; }
.chat-toggle { top: 55%; }
.chat-in-panel { display: flex; flex-direction: column; height: 100%;}
.chat-header-panel { padding: 15px 25px; border-bottom: 1px solid #eee; flex-shrink: 0; }
.chat-title-panel { margin: 0; }
.messages-list-panel { flex-grow: 1; overflow-y: auto; padding: 20px 25px; }
.message-input-area-panel { padding: 15px 25px; border-top: 1px solid #eee; flex-shrink: 0; }
</style>