import { createApp } from 'vue'
import { createPinia } from 'pinia' // (Piña) importanding.
import App from './App.vue'
import vuetify from './plugins/vuetify'
import router from './router' // wea que me da n problemas!


const app = createApp(App)
const pinia = createPinia()  // (Piña) instancia 

app.use(vuetify)
app.use(router) // Y esta se me pierde.
app.use(pinia) // piña se usa.

app.mount('#app')