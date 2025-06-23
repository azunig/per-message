<template>
  <v-dialog :model-value="dialogStore.isOpen" @update:model-value="handleClose" max-width="800px">
    <v-card>
      <v-card-title class="pa-4">
        <span class="text-h5">Crear Consulta para el Proceso #{{ dialogStore.processId }}</span>
      </v-card-title>

      <v-card-text class="pa-4">
        <v-form ref="form">
          <v-row>
            <v-col cols="12">
              <p class="mb-2 font-weight-medium">Tipo de Consulta</p>
              <v-radio-group v-model="inquiryForm.type" inline>
                <v-radio label="Pregunta General" value="pregunta"></v-radio>
                <v-radio label="Reportar un Problema" value="problema"></v-radio>
                <v-radio label="Otro" value="otro"></v-radio>
              </v-radio-group>
            </v-col>
            <v-col cols="12">
              <v-textarea
                v-model="inquiryForm.message"
                label="Mensaje de la consulta"
                variant="outlined"
                rows="4"
                :rules="[v => !!v || 'El mensaje es requerido']"
              ></v-textarea>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>

      <v-card-actions class="pa-4">
        <v-spacer></v-spacer>
        <v-btn color="blue-darken-1" variant="text" @click="dialogStore.close()">
          Cancelar
        </v-btn>
        <v-btn color="blue-darken-1" variant="flat" @click="submitInquiry">
          Enviar Consulta
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'; // <--- LA CORRECCIÓN
import { useInquiryDialogStore } from '@/stores/inquiryDialogStore';

onMounted(() => {
  console.log("✅ COMPONENTE DIÁLOGO: ¡Montado y listo para recibir órdenes!");
});

const dialogStore = useInquiryDialogStore();

watch(() => dialogStore.isOpen, (newValue) => {
  console.log(`👂 COMPONENTE DIÁLOGO: He escuchado un cambio. 'isOpen' ahora es: ${newValue}`);
});

const form = ref(null);
const inquiryForm = ref({
  type: 'pregunta',
  message: ''
});

function handleClose(value) {
  if (!value) {
    dialogStore.close();
  }
}

async function submitInquiry() {
  const { valid } = await form.value.validate();
  if (!valid) return;

  console.log('Enviando consulta para el proceso ID:', dialogStore.processId);
  console.log('Datos de la consulta:', inquiryForm.value);
  
  // await api.createInquiry(dialogStore.processId, inquiryForm.value);

  alert('¡Consulta enviada! (Simulación)');
  dialogStore.close();
}
</script>

<style scoped>
:global(.v-overlay__scrim) {
  backdrop-filter: blur(4px);
}
</style>