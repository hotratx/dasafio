<template>
  <q-layout view="hHh Lpr lff"  class="shadow-2 rounded-borders">
    <q-header elevated>
      <q-toolbar>
      <q-btn flat @click="drawer = !drawer" round dense icon="menu" />
        <q-toolbar-title>
          Cursos do desafio
        </q-toolbar-title>

        <dark-mode-toggle />
        <div>
          <q-btn-dropdown fab-mini flat color="white" icon="person">
            <q-list>
              <q-item clickable v-close-popup :to="{ name: 'profile' }">
                <q-item-section side>
                  <q-icon name="mdi-account" color="primary" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>Profile</q-item-label>
                </q-item-section>
              </q-item>

              <q-item clickable v-close-popup  @click="Logout">
                <q-item-section side>
                  <q-icon name="mdi-logout" color="primary" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>Logout</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </q-btn-dropdown>
        </div>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="drawer"
      show-if-above
      bordered

      :width="170"
      :breakpoint="500"
    >
        <EssentialLink
          :data="linksList"
        />
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import EssentialLink from 'components/EssentialLink.vue'
import { useRouter } from 'vue-router'
import { useAuth } from 'stores/userAuth'
import { ref } from 'vue'
import { useQuasar } from 'quasar'
import DarkModeToggle from 'components/DarkModeToggle.vue'


const linksList = [
  {
    title: 'Admin',
    icon: 'mdi-account-supervisor',
    routeName: 'calendar'
  },
  {
    title: 'Home',
    icon: 'mdi-home',
    routeName: 'me'
  },
  {
    title: 'Cursos',
    icon: 'mdi-calendar-month',
    routeName: 'cursos'
  },
  {
    title: 'Professores',
    icon: 'mdi-account-supervisor',
    routeName: 'professores'
  },
  {
    title: 'Alunos',
    icon: 'mdi-account-supervisor',
    routeName: 'alunos'
  },
];

const $q = useQuasar()
const router = useRouter()
const auth = useAuth()

const drawer = ref(false)


const deslogar: () => void = async () => {
  try {
    await auth.logout()
    await router.replace({
      name: 'home'
    })
  } catch (error) {
    console.log('Error no logout')
    return
  }
}

const Logout = async () => {
  $q.dialog({
    title: 'Logout',
    message: 'Você quer deslogar?',
    cancel: true,
    persistent: true
  }).onOk(deslogar)
}
</script>
