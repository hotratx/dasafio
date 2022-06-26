import { route } from 'quasar/wrappers';
import {
  createMemoryHistory,
  createRouter,
  createWebHashHistory,
  createWebHistory,
} from 'vue-router';

import routes from './routes';
import { useAuth } from 'stores/userAuth';

/*
 * If not building with SSR mode, you can
 * directly export the Router instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Router instance.
 */

export default route(function (/* { store, ssrContext } */) {
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : (process.env.VUE_ROUTER_MODE === 'history' ? createWebHistory : createWebHashHistory);

  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,

    // Leave this as is and make changes in quasar.conf.js instead!
    // quasar.conf.js -> build -> vueRouterMode
    // quasar.conf.js -> build -> publicPath
    history: createHistory(process.env.VUE_ROUTER_BASE),
  });

  Router.beforeEach((to) => {
    const store = useAuth()

    console.log(`store.isLogging: ${store.isLogging}`)
    if (!store.isLogging && to.meta.requiresAuth) {
      const value = localStorage.getItem('user')
      if (typeof value === 'string') {
        const x = JSON.parse(value)
        console.log('dados obtidos do localStorage: ', x)
        store.user = x
      } else {
        console.log('resultado localStorage não é string: ', value)
        return { name: 'login' }
      }
    }
  })
  return Router;
});
