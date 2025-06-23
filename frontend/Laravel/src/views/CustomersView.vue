<template>
  <v-container fluid>
    <v-card>
      <v-card-title class="d-flex align-center pe-2">
        <v-icon icon="mdi-account-group"></v-icon> &nbsp;
        Todos los Clientes

        <v-spacer></v-spacer>

        <v-text-field
          v-model="search"
          density="compact"
          label="Buscar"
          prepend-inner-icon="mdi-magnify"
          variant="solo-filled"
          flat
          hide-details
          single-line
        ></v-text-field>
      </v-card-title>

      <v-divider></v-divider>

      <v-data-table
        v-model:items-per-page="itemsPerPage"
        :headers="headers"
        :items="customers"
        :search="search"
        :loading="isLoading"
        loading-text="Cargando datos..."
        item-value="id"
        class="elevation-1"
      >
        <template v-slot:item.status="{ value }">
          <v-chip :color="getStatusColor(value)">
            {{ value }}
          </v-chip>
        </template>
        
        <template v-slot:item.actions="{ item }">
          <v-menu>
            <template v-slot:activator="{ props }">
              <v-icon
                icon="mdi-dots-vertical"
                v-bind="props"
              ></v-icon>
            </template>
            <v-list>
              <v-list-item @click="openInquiryForm(item)">
                <v-list-item-title>Crear Consulta</v-list-item-title>
              </v-list-item>
              <v-list-item @click="viewItem(item)">
                <v-list-item-title>Ver</v-list-item-title>
              </v-list-item>
              <v-list-item @click="editItem(item)">
                <v-list-item-title>Editar</v-list-item-title>
              </v-list-item>
              <v-list-item @click="deleteItem(item)">
                <v-list-item-title>Eliminar</v-list-item-title>
              </v-list-item>
              <v-list-item @click="showConversation(item)">
                <v-list-item-title>Ver Conversación</v-list-item-title>
              </v-list-item>
              <v-list-item @click="openInquiryForm(item)">
                <v-list-item-title>Crear Consulta</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </template>

      </v-data-table>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
// import api from '@/services/api';

import fakeCustomers from '@/data/customers.json';
import { useInquiryDialogStore } from '@/stores/inquiryDialogStore';
import { useChatStore } from '@/stores/chatStore';

const TEMP_PROCESS_ID = 101; // <-- 

// --- Estado del Componente ---
const search = ref('');
const itemsPerPage = ref(10);
const isLoading = ref(true);
const customers = ref([]);

// --- Configuración de la Tabla ---
const headers = ref([
  { title: 'Nombre del Cliente', align: 'start', key: 'name' },
  { title: 'Compañía', key: 'company.name' },
  { title: 'Teléfono', key: 'phone', sortable: false },
  { title: 'Email', key: 'email' },
  { title: 'País', key: 'address.city' }, // Usaremos la ciudad como país para el ejemplo
  { title: 'Status', key: 'status' }, // Columna para el chip de color
  { title: 'Acciones', key: 'actions', sortable: false, align: 'end' },
]);

const dialogOpen = ref(false);
const selectedItem = ref(null); // Guardará el cliente/proceso de la fila seleccionada
const form = ref(null); // Referencia al v-form

const inquiryDialogStore = useInquiryDialogStore(); // <-- 2. Crea una instancia de la tienda
const chatStore = useChatStore();

const inquiryForm = ref({
  type: 'pregunta',
  message: ''
});

// --- Lógica ---

onMounted(() => {
  fetchCustomers();
});

async function fetchCustomers() {
  isLoading.value = true;

    setTimeout(() => {
    // Asignamos los datos importados del archivo JSON
    customers.value = fakeCustomers;
    isLoading.value = false;
  }, 500);
//   try {
//     const response = await api.getCustomers();
//     // Añadimos un status aleatorio a cada cliente para el ejemplo del chip
//     customers.value = response.data.map(customer => ({
//       ...customer,
//       status: Math.random() > 0.5 ? 'Activo' : 'Inactivo'
//     }));
//   } catch (error) {
//     console.error("Error al obtener los clientes:", error);
//   } finally {
//     isLoading.value = false;
//   }
}
function getStatusColor(status) {
  return status === 'Activo' ? 'green' : 'red';
}
function viewItem(item) {
  console.log("Viendo:", item.name);
}
function editItem(item) {
  console.log("Editando:", item.name);
}
function deleteItem(item) {
  console.log("Eliminando:", item.name);
}
function openInquiryForm(item) {
  console.log(`Pidiendo abrir diálogo para el proceso ID: ${item.id}`);
  inquiryDialogStore.open(item.id);
}
function closeDialog() {
  dialogOpen.value = false;
  // Reseteamos el formulario al cerrar
  setTimeout(() => {
    selectedItem.value = null;
    inquiryForm.value = { type: 'pregunta', message: '' };
  }, 300); // Esperamos a que la animación de cierre termine
}
async function submitInquiry() {
  // Primero, validamos el formulario
  const { valid } = await form.value.validate();
  if (!valid) return;

  console.log('Enviando consulta para el proceso ID:', selectedItem.value.id);
  console.log('Datos de la consulta:', inquiryForm.value);
  
  // Aquí iría la llamada a la API
  // await api.createInquiry(selectedItem.value.id, inquiryForm.value);

  alert('¡Consulta enviada! (Simulación)');
  closeDialog();
}

function showConversation(item) {
  // Imprimimos en consola para verificar que se llama
  console.log(`Pidiendo abrir el chat para el proceso/cliente ID: ${item.id}`);
  // Le damos la orden a la tienda Pinia de que abra el panel para este ID específico
  chatStore.openChat(item.id);
}

</script>

<style scoped>
/* Estilos para que el buscador no sea tan ancho */
.v-text-field {
  max-width: 350px;
}

:global(.v-overlay__scrim) {
  backdrop-filter: blur(4px);
}
</style>