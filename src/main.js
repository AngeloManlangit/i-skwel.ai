import { createApp } from 'vue';
import './assets/style.css';
import { VueFlow } from '@vue-flow/core';
import App from './App.vue';
import router from './router/index';

const app = createApp(App)
app.use(router);
app.mount('#app')

app.component('VueFlow', VueFlow);
