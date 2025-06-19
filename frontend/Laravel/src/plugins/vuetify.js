// src/plugins/vuetify.js

// Vuetify y los iconos de Material Design
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Importa la función para crear la instancia de Vuetify
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

// Crea la instancia de Vuetify con componentes, directivas y un tema básico
const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'light', // Puedes cambiarlo a 'dark' si lo prefieres
    themes: {
      light: {
        dark: false,
        colors: {
          primary: '#1867C0',
          secondary: '#5CBBF6',
        },
      },
    },
  },
})

// Exporta la instancia para que main.js pueda usarla
export default vuetify