<template>
  <q-layout view="lHh Lpr lFf" class="bg-white">
      <q-toolbar class="GNL__toolbar">
        <q-toolbar-title v-if="$q.screen.gt.xs" shrink class="row items-center no-wrap">
          <span class="q-ml-sm">Cursos do Desafio</span>
        </q-toolbar-title>

        <q-space />

        <div class="q-gutter-sm row items-center no-wrap">
          <q-btn 
            class="text-weight-bolder" 
            flat color="primary text-black" 
            size="15px" 
            to="/login"
            label="Login"
            no-caps
          >
          </q-btn>
          <q-btn 
            class="text-weight-bolder" 
            color="primary" 
            size="15px" 
            to="/register"
            label="Registro"
            no-caps
          >
          </q-btn>
        </div>
      </q-toolbar>
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>

</template>

<script setup lang="ts">

</script>

<style lang="scss">
.router-link-active {
  text-decoration: none;
  color: grey;
}
.GNL {
  &__toolbar {
    height: 84px;
  }
  &__drawer-item {
    line-height: 24px;
    border-radius: 0 24px 24px 0;
    margin-right: 12px;
    .q-item__section--avatar {
      .q-icon {
        color: #5f6368;
      }
    }
    .q-item__label {
      color: #3c4043;
      letter-spacing: .01785714em;
      font-size: .875rem;
      font-weight: 500;
      line-height: 1.25rem;
    }
  }
  &__drawer-footer-link {
    color: inherit;
    text-decoration: none;
    font-weight: 500;
    font-size: .75rem;
    &:hover {
      color: #000;
    }
  }
}
</style>
