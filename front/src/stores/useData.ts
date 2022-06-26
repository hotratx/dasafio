import { defineStore } from 'pinia' 
import { Auth } from 'boot/axios'
import { IProfessores, IAlunos } from 'components/models'

interface IState {
  professores: []
  alunos: []
}

export const useData = defineStore('handleData', {
  state: (): IState => ({
    professores: [],
    alunos: []
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
    }
  }
})
