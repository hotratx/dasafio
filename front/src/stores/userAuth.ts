import { defineStore } from 'pinia' 
import { Auth } from 'boot/axios'
import { ICredentials, IUser, ICreateProf } from 'components/models'


interface IState {
  isLogging: boolean
  user: IUser
}

export const useAuth = defineStore('authUser', {
  state: (): IState => ({
    user: {
      id: '',
      email: '',
      nome: '',
      sobrenome: '',
      type_user: '',
      estado: '',
      cidade: '',
      endereco: '',
      tel_fixo: 0,
      tel_movel: 0 
    },
    isLogging: false,
  }),
  actions: {
    async login(credentials: ICredentials) {
      try {
        const api = await Auth.login({
          email: credentials.email,
          password: credentials.password
        })
        console.log('API: ', api)
        if (api) {
          this.user = api.data
          this.isLogging = true
          localStorage.setItem('user', JSON.stringify(api.data))
        }
      } catch (error) {
        console.log('error.message: ', error.message) // resposta de error do servidor
        throw error.response.data.detail
      }
    },

    async update_profile(credentials: IUser) {
      try {
        const api = await Auth.update_profile({
          id: credentials.id,
          email: credentials.email,
          nome:  credentials.nome,
          sobrenome: credentials.sobrenome,
          type_user: credentials.type_user,
          estado: credentials.estado,
          cidade: credentials.cidade,
          endereco: credentials.endereco,
          tel_fixo: credentials.tel_fixo,
          tel_movel: credentials.tel_movel,
        })
        console.log('API: ', api)
        if (api) {
          this.user = api.data
          this.isLogging = true
          localStorage.setItem('arbi', JSON.stringify(api))
        }
      } catch (error) {
        console.log('error.message: ', error.message) // resposta de error do servidor
        throw error.response.data.detail
      }
    },

    async new_prof(credentials: ICreateProf) {
      try {
        const api = await Auth.new_prof({
          email: credentials.email,
          nome:  credentials.nome,
          type_user: credentials.type_user,
          password: credentials.password,
        })
        console.log('API: ', api)
      } catch (error) {
        console.log('error.message: ', error.message) // resposta de error do servidor
        throw error.response.data.detail
      }
    },
    async new_aluno(credentials: ICreateProf) {
      try {
        const api = await Auth.new_aluno({
          email: credentials.email,
          nome:  credentials.nome,
          type_user: credentials.type_user,
          password: credentials.password,
        })
        console.log('API: ', api)
      } catch (error) {
        console.log('error.message: ', error.message) // resposta de error do servidor
        throw error.response.data.detail
      }
    },
    // após registrar deve aparecer página pedindo para registrar email
    // para só depois armazenar dados como logado, por isso o back não deve 
    // retornar user após o registro
    async register(credentials: ICredentials) {
      try {
        const api = await Auth.register({...credentials})
        this.user = api
        console.log('Register: ', api)
      } catch (error) {
        console.log('error.response.data: ', error.response.data.detail) // resposta de error do servidor
        throw error
      }
    },

    async verifyAutorization() {
        console.log('entrou no me')
        const api = await Auth.me()
        console.log('/me :', api)
    },

    async handleConfirmEmail(token: string) {
      try {
        console.log('entrou no handleConfirmEmail ', token)
        const api = await Auth.confirmEmail(token)
        console.log('confirm email status :', api)
      } catch (error) {
        console.log('error.response.data ')
        throw error
      }
    },
    // posso enviar msg pro back para bloquear os tokens 
    async logout() {
      console.log('deslogar, remover localStorage')
      this.isLogging = false
      this.user = {
        id: '',
        email: '',
        username: '',
        id_active: '',
        id_admin: ''
      }
      localStorage.clear()
    }
  }
})
