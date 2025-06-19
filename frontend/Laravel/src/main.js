import { createApp } from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import router from './router' // Asegúrate de que esta línea esté activa

const app = createApp(App)

app.use(vuetify)
app.use(router) // Y esta también

app.mount('#app')