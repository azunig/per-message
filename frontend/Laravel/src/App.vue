<template>
  <v-app>
    <v-main class="bg-grey-lighten-4">
      <router-view></router-view>
    </v-main>
    <GlobalChatPanel />
    <InquiryFormDialog />
  </v-app>
</template>

<script setup>
  import InquiryFormDialog from '@/components/InquiryFormDialog.vue';
  import GlobalChatPanel from '@/components/GlobalChatPanel.vue';
</script>