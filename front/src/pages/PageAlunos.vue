<template>
 <q-page padding>
    <div class="q-pa-md">
      <q-table
        style="height: 400px"
        title="Tabela de Alunos"
        :rows="data.alunos"
        :columns="columns"
        row-key="index"
        virtual-scroll
        v-model:pagination="pagination"
        :rows-per-page-options="[0]"
      />
    </div>



  <div class="q-pa-md" v-if="store.user.type_user == 'staff'">
    <div class="div">
      Adicionar novo aluno:
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
import { ICreateAluno } from 'components/models'

const store = useAuth()
const data = useData()

const form = ref<ICreateAluno>({
  email: '',
  nome: '',
  type_user: '',
  password: '',
})

const getAlunos = async () => {
  try {
    await data.getAlunos()
  } catch(erro) {
    console.log('erro busca alunos')
  }
}

const onSubmit = async () => {
  try {
    await store.new_aluno(form.value)
    console.log('create new aluno')
    await getAlunos()
  } catch (error) {
    notifyError(error)
    console.log('erro no store.loging', error)
  }
}

onMounted(async () => {
    await getAlunos()
    console.log('sucessso na busca pelos alunos')
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
