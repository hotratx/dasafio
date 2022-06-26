<template>
 <q-page padding>
    <div class="q-pa-md">
      <q-table
        style="height: 400px"
        title="Tabela de Cursos"
        :rows="data.cursos"
        :columns="columns"
        row-key="index"
        virtual-scroll
        v-model:pagination="pagination"
        :rows-per-page-options="[0]"
      />
    </div>

  <div class="q-pa-md" v-if="store.user.type_user == 'staff'">
    <div class="div">
      Adicionar novo Curso:
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
          v-model="form.professor"
          label="Professor"
          lazy-rules
        />

        <q-toggle
          filled
          v-model="form.ativo"
          label="Ativo"
        />

        <q-input
          filled
          type="date"
          v-model="form.data_inicio"
          hint="Data Inicio"
          lazy-rules
        />

        <q-input
          filled
          type="date"
          v-model="form.data_termino"
          hint="Data Termino"
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
import { ICurso } from 'components/models'

const store = useAuth()
const data = useData()

const form = ref<ICurso>({
  nome: '',
  professor: '',
  ativo: true,
  data_inicio: Date.now(),
  data_termino: Date.now(),
})

const getCursos = async () => {
  try {
    await data.getCursos()
  } catch(erro) {
    console.log('erro busca cursos')
  }
}

const onSubmit = async () => {
  try {
    await store.new_curso(form.value)
    console.log('create new curso')
    await getCursos()
  } catch (error) {
    notifyError(error)
    console.log('erro no store.loging', error)
  }
}

onMounted(async () => {
    await getCursos()
    console.log('sucessso na busca pelos cursos')
})

const columns = [
  { name: 'nome', align: 'left', label: 'Nome', field: 'nome', sortable: true },
  { name: 'professor', align: 'left', label: 'Professot', field: 'professor', sortable: true },
  { name: 'ativo', align: 'left', label: 'Ativo', field: 'ativo' },
  { name: 'data_inicio', align: 'left', label: 'Data de Inicio', field: 'data_inicio' },
  { name: 'data_termino', align: 'left', label: 'Data de Termino', field: 'data_termino' },
]

const pagination = ref({
  rowsPerPage: 0
})

</script>
