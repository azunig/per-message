// src/views/IndexView.vue

<template>
  <v-container class="fill-height d-flex justify-center align-center">
    <v-card width="600" class="pa-4" rounded="lg">
      <v-card-title class="text-h4 font-weight-bold text-center mb-4">
        Índice de Prototipos
      </v-card-title>
      <v-card-text>
        <p class="text-center text-body-1 mb-6">
          Selecciona uno de los prototipos a continuación para navegar a la página correspondiente.
        </p>
        <v-divider></v-divider>
        <v-list lines="three">
          <v-list-item
            :to="{ name: 'Profile' }"
            prepend-icon="mdi-account-box-outline"
            rounded="lg"
          >
            <v-list-item-title class="font-weight-bold">Prototipo de Perfil</v-list-item-title>
            <v-list-item-subtitle>Layout de dos columnas con perfil y detalles.</v-list-item-subtitle>
          </v-list-item>

          <v-list-item
            :to="{ name: 'Dashboard' }"
            prepend-icon="mdi-view-dashboard-outline"
            rounded="lg"
          >
            <v-list-item-title class="font-weight-bold">Prototipo de Dashboard</v-list-item-title>
            <v-list-item-subtitle>Layout con panel de navegación lateral fijo.</v-list-item-subtitle>
          </v-list-item>
          
          <v-list-item
            :to="{ name: 'Customers' }"
            prepend-icon="mdi-view-dashboard-outline"
            rounded="lg"
          >
            <v-list-item-title class="font-weight-bold">Prototipo de Customers</v-list-item-title>
            <v-list-item-subtitle>Layout de grilla.</v-list-item-subtitle>
          </v-list-item>
        </v-list>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
</script>