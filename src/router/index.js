import { createRouter, createWebHistory } from 'vue-router';
// Corrected import paths
import Navbar from '../components/Navbar.vue';
import MainPage from '../components/MainPage.vue';
import RoadMapPage from '../components/RoadMapPage.vue'; 

const routes = [
  {
    path: '/',
    name: 'Home',
    component: MainPage,
  },
  {
    path:'/navbar',
    name:'NavbarRoute',
    component: Navbar,
  },
  {
    path: '/roadmap',
    name: 'Roadmap',
    component: RoadMapPage,
    props: (route) => ({
      userInput: route.query.userInput ? JSON.parse(route.query.userInput) : {},
    }),
  },
  {
    path:'/roadmap1',
    name:'roadmapw',
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else if (to.hash) {
        return new Promise((resolve) => {
            setTimeout(() => {
                const el = document.querySelector(to.hash);
                if (el) {
                    resolve({ el: el, behavior: 'smooth' });
                } else {
                    resolve({ top: 0, behavior: 'smooth' });
                }
            }, 100);
          });
    } else {
      return { top: 0, behavior: 'smooth' };
    }
  },
});

export default router;
