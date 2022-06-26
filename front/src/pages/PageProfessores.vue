<template>
 <q-page padding>
    <div class="q-pa-md">
      <q-table
        style="height: 400px"
        title="Tabela de Professores"
        :rows="data.professores"
        :columns="columns"
        row-key="index"
        virtual-scroll
        v-model:pagination="pagination"
        :rows-per-page-options="[0]"
      />
    </div>



  <div class="q-pa-md" v-if="store.user.type_user == 'staff'">
    <div class="div">
      Adicionar novo professor:
    </div>
    <div class="q-gutter-xs" style="max-width: 300px">
      <q-form
        @submit="onSubmit"
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
          v-model="form.password"
          label="Password"
          lazy-rules
        />

      <div>
        <q-btn label="Submit" type="submit" color="primary"/>
      </div>
    </q-form>

    </div>
    </div>
 </q-page>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useAuth } from 'stores/userAuth'
import { useData } from 'stores/useData'
import { ICreateProf } from 'components/models'

const store = useAuth()
const data = useData()

const form = ref<ICreateProf>({
  email: '',
  nome: '',
  type_user: '',
  password: '',
})

const getProfessores = async () => {
  try {
    await data.getProfessores()
  } catch(erro) {
    console.log('erro busca professores')
  }
}

const onSubmit = async () => {
  try {
    await store.new_prof(form.value)
    console.log('update profile success')
    await getProfessores()
  } catch (error) {
    notifyError(error)
    console.log('erro no store.loging', error)
  }
}

onMounted(async () => {
    await getProfessores()
    console.log('sucessso na busca pelos professores')
})

const columns = [
  { name: 'nome', align: 'left', label: 'Nome', field: 'nome', sortable: true },
  { name: 'email', align: 'left', label: 'Email', field: 'email', sortable: true },
  { name: 'cidade', align: 'left', label: 'Cidade', field: 'cidade' },
]

const pagination = ref({
  rowsPerPage: 0
})

</script>
