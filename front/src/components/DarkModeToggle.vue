<template>
  <q-toggle
    v-model="darkMode"
    checked-icon="mdi-weather-night"
    color="blue"
    unchecked-icon="mdi-white-balance-sunny"
    size="sm"
  /> 
</template>

<script setup lang="ts">
import { useQuasar } from 'quasar'
import { ref, watch, onMounted } from 'vue'

const darkMode = ref(false)
const $q = useQuasar()

watch(darkMode, (darkMode) => {
  $q.dark.set(darkMode)
  console.log($q.dark)
  $q.localStorage.set('darkMode', darkMode)
  console.log('dardmode', darkMode)
})

onMounted(() => {
  const darkModeIsActive = $q.localStorage.getItem('darkMode')
  if (darkModeIsActive) {
    darkMode.value = true
  }
})

</script>

<style>
body.body--dark {
  background: #000
}
</style>
