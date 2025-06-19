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
      <v-window v-model="tab" class="fill-height">
        <v-window-item value="posts" class="fill-height d-flex justify-center align-center">
            <h1 class="text-grey">Contenido de Posts</h1>
        </v-window-item>
        <v-window-item value="pages" class="fill-height d-flex justify-center align-center">
            <h1 class="text-grey">Contenido de Pages</h1>
        </v-window-item>
      </v-window>
    </div>

    <v-btn icon class="timeline-toggle" @click="toggleTimelinePanel">
      <v-icon>{{ timelineDrawer ? 'mdi-chevron-right' : 'mdi-chevron-left' }}</v-icon>
    </v-btn>

    <v-btn icon class="chat-toggle" @click="toggleChatPanel">
      <v-icon>{{ chatDrawer ? 'mdi-chevron-right' : 'mdi-message-text' }}</v-icon>
    </v-btn>

    <div class="side-panel timeline-panel" :class="{ open: timelineDrawer }">
      <v-container>
        <h2 class="text-h6">Timeline</h2>
        <v-timeline side="end" density="compact">
          <v-timeline-item
            v-for="event in events"
            :key="event.id"
            :dot-color="event.color"
            :icon="event.icon"
            fill-dot
            size="small"
          >
            <template #opposite>
              <span class="font-weight-bold">{{ event.title }}</span>
              <div class="text-caption">{{ event.date }}</div>
            </template>
            <div>
              <p class="mb-0">{{ event.description }}</p>
            </div>
          </v-timeline-item>
        </v-timeline>
      </v-container>
    </div>

    <div class="side-panel chat-panel" :class="{ open: chatDrawer }">
      <div class="chat-in-panel">
        <header class="chat-header-panel">
          <h2 class="chat-title-panel">Chat with Alex Harris</h2>
        </header>
        <div class="messages-list-panel" ref="messagesListRef">
          <MessageComponent
            v-for="message in threadedMessages"
            :key="message.id"
            :message="message"
            :depth="0"
          />
        </div>
        <div class="message-input-area-panel">
          </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
// Importamos los componentes y datos necesarios para los paneles
import MessageComponent from '@/components/MessageComponent.vue';
import testMessages from '@/data/messages.json';

// --- Lógica del Dashboard (Existente) ---
const tab = ref('posts');

// --- Lógica de los Paneles Laterales (Añadida y convertida a Composition API) ---
const timelineDrawer = ref(false);
const chatDrawer = ref(false);

const events = ref([
  { id: 1, date: '2023-01-01', title: 'Started Project', description: 'Kicked off the project.', icon: 'mdi-rocket', color: 'primary' },
  { id: 2, date: '2023-02-15', title: 'Design Complete', description: 'Finished design phase.', icon: 'mdi-pencil', color: 'success' },
  { id: 3, date: '2023-03-10', title: 'First Release', description: 'Released MVP.', icon: 'mdi-star', color: 'warning' },
]);

const threadedMessages = ref([]);
const messagesListRef = ref(null); // Para hacer scroll al final

function toggleTimelinePanel() {
  timelineDrawer.value = !timelineDrawer.value;
  if (timelineDrawer.value) {
    chatDrawer.value = false;
  }
}

function toggleChatPanel() {
  chatDrawer.value = !chatDrawer.value;
  if (chatDrawer.value) {
    timelineDrawer.value = false;
  }
}

function loadTestMessages() {
  const clonedMessages = JSON.parse(JSON.stringify(testMessages));
  threadedMessages.value = clonedMessages.sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
}

// onMounted es el equivalente a 'mounted' en Composition API
onMounted(() => {
  loadTestMessages();
});
</script>

<style scoped>
/* Estilo del contenido principal del dashboard (Existente) */
.main-content-area {
  background-color: #121212;
}

/* Estilos para los paneles laterales (Añadidos) */
.side-panel {
  position: fixed;
  top: 0;
  height: 100%;
  width: 50vw;
  max-width: 700px;
  min-width: 400px;
  background-color: #fff;
  box-shadow: -4px 0 10px rgba(0, 0, 0, 0.2);
  z-index: 1005; /* Debe ser mayor que el de v-navigation-drawer */
  transition: right 0.3s ease-in-out;
  display: flex;
  flex-direction: column;
  right: -100%; 
}
.side-panel.open {
  right: 0;
}

.timeline-toggle, .chat-toggle {
  position: fixed;
  right: 16px;
  z-index: 1006;
  background-color: white;
  transform: translateY(-50%);
}
.timeline-toggle {
  top: 45%;
}
.chat-toggle {
  top: 55%; 
}

/* Estilos del chat */
.chat-in-panel { display: flex; flex-direction: column; height: 100%;}
.chat-header-panel { padding: 15px 25px; border-bottom: 1px solid #eee; flex-shrink: 0; }
.chat-title-panel { margin: 0; }
.messages-list-panel { flex-grow: 1; overflow-y: auto; padding: 20px 25px; }
.message-input-area-panel { padding: 15px 25px; border-top: 1px solid #eee; flex-shrink: 0; }
</style>