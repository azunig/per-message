<template>
  <div class="pa-10">
    <h1 class="text-h4 mb-6">Página de Prueba del Panel de Chat</h1>
    <p class="mb-4">
      Esta página está completamente aislada. Al hacer clic en el botón,
      debería abrirse el panel de chat para el proceso por defecto (101).
    </p>
    <v-btn @click="openTheChat" color="primary" size="large">
      Abrir Chat (Proceso 101)
    </v-btn>
  </div>
</template>

<script setup>
import { useChatStore } from '@/stores/chatStore';

const chatStore = useChatStore();

function openTheChat() {
  console.log("Haciendo clic en el botón de la página de PRUEBA...");
  chatStore.openChat(101);
}
</script>