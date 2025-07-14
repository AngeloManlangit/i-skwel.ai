import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import {VueFlow} from '@vue-flow/core';
import router from './router/index';

const app = createApp(App)
app.use(router);
createApp(App).mount('#app')
app.component('VueFlow', VueFlow);