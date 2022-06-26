<template>
 <q-page padding>
  <div class="row justify-center">
    <p class="col-12 text-h8 text-center">
        Email confirmado!
        {{ token }}
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
</template>

<script setup lang="ts">
import { useAuth } from 'store/userAuth'
import { computed, onMounted, onActivated } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const store = useAuth()
const route = useRoute()
const token = computed(() => route.params.token)

console.log("token", token)


const confirmEmail = async () => {
  try {
    console.log('vai vai')
    await store.handleConfirmEmail(token.value)
  } catch (error) {
    console.log('erro no store.loging', error)
  }
}

onMounted(() => {
  confirmEmail()
})
</script>
