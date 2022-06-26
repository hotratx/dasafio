<template>
  <q-layout>
    <q-page-container>
      <q-page class="flex flex-center">
        <div class="row justify-center">
          <p class="col-12 text-h8 text-center">
            Para ativar sua conta clique no link enviado para seu email.
          </p>
          <div class="col-md-4 col-sm-6 col-xs-6 q-gutter-y-sm">
            <div class="full-width q-gutter-y-sm">
            <q-btn
              label="Login"
              color="primary"
              class="full-width"
              type="submit"
              :to="{ name: 'login' }"
            />
            </div>
          </div>
        </div>
     </q-page>
  </q-page-container>
</q-layout>
</template>

<script setup lang="ts">

</script>
