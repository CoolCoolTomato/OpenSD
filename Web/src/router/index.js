import { createRouter, createWebHistory } from 'vue-router'
import Login from "@/views/Login.vue";
import Base from "@/components/Base.vue";
import Index from "@/views/Index.vue";
import Text2Img from "@/views/Text2Img.vue";
import Images from "@/views/Images.vue";
import Img2Img from "@/views/Img2Img.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'base',
      component: Base,
      meta: { requiresAuth: true },
      children: [
        {
          path: 'index',
          name: 'index',
          component: Images,
        },
        {
          path: 'text2img',
          name: 'text2img',
          component: Text2Img,
        },
        {
          path: 'img2img',
          name: 'img2img',
          component: Img2Img,
        },
        {
          path: 'images',
          name: 'images',
          component: Images,
        },
      ],
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
  ]
})
router.beforeEach((to, from, next) => {
  const isLoggedIn = !!localStorage.getItem('access_token');

  if (to.matched.some(record => record.meta.requiresAuth) && !isLoggedIn) {
    next({ name: 'login' });
  } else {
    next();
  }
});
export default router
