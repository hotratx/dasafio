<template>
 <q-page padding>
  <div class="div">
    Profile
  </div>
  <div class="q-pa-md">
    <div class="q-gutter-xs" style="max-width: 300px">
      <q-form
        @submit.prevent="onSubmit"
        class="q-gutter-md"
      >
        <q-input
          filled
          v-model="form.nome"
          label="Nome"
          lazy-rules
        />
        <q-input
          filled
          v-model="form.sobrenome"
          label="Sobrenome"
          lazy-rules
        />

        <q-input
          filled
          v-model="form.email"
          label="Email"
          lazy-rules
        />

        <q-input
          filled
          v-model="form.type_user"
          label="Categoria"
          lazy-rules
        />

        <q-input
          filled
          v-model="form.cidade"
          label="Cidade"
          lazy-rules
        />

        <q-input
          filled
          v-model="form.estado"
          label="Estado"
          lazy-rules
        />

        <q-input
          filled
          v-model="form.endereco"
          label="Endereco"
          lazy-rules
        />

        <q-input
          filled
          type="number"
          v-model="form.tel_fixo"
          label="Telefone fixo"
          lazy-rules
        />

        <q-input
          filled
          type="number"
          v-model="form.tel_movel"
          label="Telefone movel"
          lazy-rules
        />

      <div>
        <q-btn label="Submit" type="submit" color="primary"/>
      </div>
    </q-form>

    </div>

      {{ store.user.data}}
  </div>
 </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuth } from 'stores/userAuth'
import { useData } from 'stores/useData'
import { IUser } from 'components/models'


const store = useAuth()
const data = useData()

const form = ref<IUser>({
  id: store.user.id,
  email: store.user.email,
  nome:  store.user.nome,
  sobrenome: store.user.sobrenome,
  type_user: store.user.type_user,
  estado: store.user.estado,
  cidade: store.user.cidade,
  endereco: store.user.endereco,
  tel_fixo: store.user.tel_fixo,
  tel_movel: store.user.tel_movel,
})

const onSubmit = async () => {
  try {
    await store.update_profile(form.value)
    console.log('update profile success')
  } catch (error) {
    notifyError(error)
    console.log('erro no store.loging', error)
  }
}

</script>
