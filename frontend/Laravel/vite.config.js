// frontend/Laravel/vite.config.js

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vuetify from 'vite-plugin-vuetify'

// 1. Importamos herramientas de Node.js para manejar URLs
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [
    vue(),
    vuetify({ autoImport: true }),
  ],
  // 2. Esta es la nueva sección 'resolve' corregida
  resolve: {
    alias: {
      // Le decimos que '@' es un alias para la carpeta 'src' de este proyecto
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
    extensions: [
      '.js',
      '.json',
      '.jsx',
      '.mjs',
      '.ts',
      '.tsx',
      '.vue',
    ],
  },
  server: {
    // configuración de proxy
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000', // Asumiendo puerto API
        changeOrigin: true,
        //rewrite: (path) => path.replace(/^\/api/, ''),
      },
    }
  }
})