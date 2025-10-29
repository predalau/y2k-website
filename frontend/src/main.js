import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Import global styles
import './styles/reset.css'
import './styles/variables.css'
import './styles/animations.css'
import './styles/global.css'

const app = createApp(App)

app.use(router)
app.mount('#app')
