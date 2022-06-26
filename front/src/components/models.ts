export interface IProfile {
  username: string
  email: string
}

export interface ICredentials {
  email: string
  nome?: string
  password: string
}

export interface ICreateProf {
  email: string
  nome: string,
  type_user: string,
  password: string,
}

export interface ICreateAluno {
  email: string
  nome: string,
  type_user: string,
  password: string,
}

export interface IUser {
  id: string
  email: string
  nome: string,
  sobrenome: string,
  type_user: string,
  estado: string,
  cidade: string,
  endereco: string,
  tel_fixo: number,
  tel_movel: number
}

export interface IMe {
  Authenticated: boolean
  username: string
}

export interface IProfessores {
  professores: Array<IUser | null>
}

export interface IAlunos {
  alunos: Array<IUser | null>
}
