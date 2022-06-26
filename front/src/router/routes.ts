import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/HomeLayout.vue'),
    children: [
      { path: '', name: 'homeraiz', component: () => import('pages/home/PageHomePage.vue') },
      { path: 'home', name: 'home', component: () => import('pages/home/PageHomePage.vue') },
    ],
  },  
  {
    path: '/',
    component: () => import('layouts/LoginLayout.vue'),
    children: [
      { path: 'login', name: 'login', component: () => import('pages/register/PageLogin.vue') },
      { path: 'register', name: 'register', component: () => import('pages/register/PageRegister.vue') },
      // { path: 'confirm-email', name: 'confirm-email', component: () => import('pages/register/PageConfirmEmail.vue') },
      // { path: 'confirm/:token', name: 'confirm', component: () => import('pages/register/PageConfirm.vue') },
      // { path: 'forgot-password', name: 'forgot-password', component: () => import('pages/PageForgotPassword.vue') },
      // { path: 'reset-password', name: 'reset-password', component: () => import('pages/PageResetPassword.vue') },
    ],
  },  
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: 'me', name: 'me', component: () => import('pages/PageMe.vue') },
      { path: 'professores', name: 'professores', component: () => import('pages/PageProfessores.vue') },
      { path: 'alunos', name: 'alunos', component: () => import('pages/PageAlunos.vue') },
      { path: 'cursos', name: 'cursos', component: () => import('pages/PageCursos.vue') },
      { path: 'profile', name: 'profile', component: () => import('pages/register/PageProfile.vue') },
    ],
    meta: {
  //     // estas rotas precisam estar com isLogging true
  //     // as rotas de cima que não tem este meta o resultado será sempre falso
  //     // logo o primeiro if fo Router.beforeEach será falso, levando a página de login.
      requiresAuth: true
    }
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/PageErrorNotFound.vue'),
  },
];

export default routes;
