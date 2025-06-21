<template>
  <v-container class="fill-height justify-center">
    <v-card width="400" class="pa-4" rounded="lg">
      <v-card-title class="text-h5 font-weight-bold text-center mb-4">
        Iniciar Sesión
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="handleLogin">
          <v-text-field
            v-model="email"
            label="Email"
            type="email"
            required
            class="mb-2"
            variant="outlined"
          ></v-text-field>
          <v-text-field
            v-model="password"
            label="Contraseña"
            type="password"
            required
            variant="outlined"
          ></v-text-field>
          
          <v-alert v-if="error" type="error" dense class="my-4">
            {{ error }}
          </v-alert>

          <v-btn
            type="submit"
            color="primary"
            block
            :loading="loading"
            size="large"
          >
            Entrar
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

const email = ref('');
const password = ref('');
const error = ref(null);
const loading = ref(false);

const authStore = useAuthStore();
const router = useRouter();

async function handleLogin() {
  loading.value = true;
  error.value = null;
  
  const success = await authStore.login({
    email: email.value,
    password: password.value,
  });

  loading.value = false;

  if (success) {
    router.push('/dashboard');
  } else {
    error.value = 'Email o contraseña incorrectos, o ha ocurrido un error.';
  }
}
</script>

<style scoped>
/* Puedes añadir estilos específicos aquí si lo necesitas */
</style>