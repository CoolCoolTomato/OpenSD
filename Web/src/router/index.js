import { createRouter, createWebHistory } from 'vue-router'
import Login from "@/views/Login.vue";
import Base from "@/components/Base.vue";
import Index from "@/views/Index.vue";

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
          component: Index,
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
