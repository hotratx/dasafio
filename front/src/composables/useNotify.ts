import { Notify } from 'quasar'


export default function useNotify() {

  const notifySuccess = (message?: string): void => {
    Notify.create({
      type: 'positive',
      message: message || 'Tudo Certo !'
    })
  }

  const notifyError = (message: string) => {
    Notify.create({
      type: 'negative',
      message: message || 'Falhou !'
    })
  }


  return {
    notifySuccess,
    notifyError
  }
}
