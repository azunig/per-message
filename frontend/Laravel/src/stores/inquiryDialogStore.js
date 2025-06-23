import { defineStore } from 'pinia';

export const useInquiryDialogStore = defineStore('inquiryDialog', {
  // EL ESTADO: ¿Está abierto? ¿Para qué proceso?
  state: () => ({
    isOpen: false,
    processId: null,
  }),

  // LAS ACCIONES: Órdenes para la tienda
  actions: {
    /**
     * Abre el diálogo para un processId específico.
     * @param {number} processId - El ID del proceso sobre el que se hará la consulta.
     */
    open(processId) {
      if (!processId) {
        console.error("Se intentó abrir el diálogo de consulta sin un processId.");
        return;
      }
      this.processId = processId;
      this.isOpen = true;
      
      console.log(`✅ TIENDA PINIA: Estado cambiado a 'abierto' (isOpen: ${this.isOpen}) para el proceso ID: ${this.processId}`);
    },

    /**
     * Cierra el diálogo y resetea el estado.
     */
    close() {
      this.isOpen = false;
      // Reseteamos el ID después de un momento para que no desaparezca bruscamente
      setTimeout(() => {
        this.processId = null;
      }, 300);
    },
  },
});