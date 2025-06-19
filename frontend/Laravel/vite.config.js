// vite.config.js
import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vuetify from 'vite-plugin-vuetify' // <-- Importa el plugin

export default defineConfig({
  plugins: [
    vue(),
    vuetify({ autoImport: true }), // <-- Añade Vuetify a los plugins
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})