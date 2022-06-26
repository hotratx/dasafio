<template>
 <q-page padding>
      <h4 style="line-height:4.125rem;">Bem vindo: 
        <span style="color:#1414dc;">{{ store.user.nome }}</span>
      </h4>
      <h4 style="">Status: 
        <span style="color:#1414dc;">{{ store.user.type_user }}</span>
      </h4>
    {{ store.user }}
 </q-page>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useAuth } from 'stores/userAuth'
import { useData } from 'stores/useData'


const store = useAuth()
const data = useData()


</script>
