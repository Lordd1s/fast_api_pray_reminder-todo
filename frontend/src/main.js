import './assets/main.css'
import SideBar from './components/SideBar.vue'
import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.component('SideBar', SideBar)
app.mount('#app')
