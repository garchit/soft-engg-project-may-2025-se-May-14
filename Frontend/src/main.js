
import { createApp } from 'vue'
import App from './App.vue'
import router from './components/Routes/index.js'


import '@coreui/coreui/dist/css/coreui.min.css'
import 'bootstrap/dist/css/bootstrap.min.css'
createApp(App).use(router).mount('#app')

