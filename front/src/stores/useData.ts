import { defineStore } from 'pinia' 
import { Auth } from 'boot/axios'

interface IState {
  professores: []
  alunos: []
  cursos: []
}

export const useData = defineStore('handleData', {
  state: (): IState => ({
    professores: [],
    alunos: [],
    cursos: []
  }),

  getters: {
  },
  actions: {
    async getProfessores() {
      try {
        const profs = await Auth.getProfessores()
        if (profs) {
          this.professores = profs.data
        }
        console.log('PROFESSORES: ', profs)
      } catch (error) {
        console.log('error.message: ', error.message) // resposta de error do servidor
        throw error.response.data.detail
      }
    },
    async getAlunos() {
      try {
        const alunos = await Auth.getAlunos()
        if (alunos) {
          console.log('ALUNOSSSSS: ', alunos.data)
          this.alunos = alunos.data
        }
        console.log('ALUNOS: ', alunos)
      } catch (error) {
        console.log('error.message: ', error.message) // resposta de error do servidor
        throw error.response.data.detail
      }
    },

    async getCursos() {
      try {
        const cursos = await Auth.getCursos()
        if (cursos) {
          console.log('CURSOS: ', cursos.data)
          this.cursos = cursos.data
        }
        console.log('CURSOS: ', cursos)
      } catch (error) {
        console.log('error.message: ', error.message) // resposta de error do servidor
        throw error.response.data.detail
      }
    }
  }
})
