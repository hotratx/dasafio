import { IUser, ICredentials, ICreateProf, ICreateAluno } from 'components/models';
import { boot } from 'quasar/wrappers';
import axios, { AxiosInstance, AxiosResponse } from 'axios';

declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $axios: AxiosInstance;
  }
}

// Be careful when using SSR for cross-request state pollution
// due to creating a Singleton instance here;
// If any client changes this (global) instance, it might be a
// good idea to move this instance creation inside of the
// 'export default () => {}' function below (which runs individually
// for each client)
const apiClient: AxiosInstance = axios.create({
  baseURL: 'http://localhost:5000/',
  timeout: 15000,
  withCredentials: true,
});

apiClient.interceptors.request.use((config) => {
  // Do something before request is sent
  return config;
})

apiClient.interceptors.response.use((response) => {
  // Any status code that lie within the range of 2xx cause this function to trigger
  // Do something with response data
  return response;
  },
  // Any status codes that falls outside the range of 2xx cause this function to trigger
  // Do something with response error
  async (error) => {
    if (error.response.status === 401) {
      if (error.response.data) {
        return Promise.reject(error)
      }
      const response = await axios.get(
        'auth/refresh-token',
        {
          withCredentials: true,
        }
      )
      .catch((err) => {
        const store = useAuth()
        store.logout()
        router.push({ name: 'login'})
        return Promise.reject(err);
      });
      if(response && response.data){
        return axios(error.config);
      }
      else{
        return Promise.reject(error);
      }
    } else {
      return Promise.reject(error);
    }
  }
)

const responseBody = (response: AxiosResponse) => response;
//const responseError = (response: AxiosError) => response;

const requests = {
  get: (url: string): Promise<AxiosResponse> => apiClient.get(url).then(responseBody),
  post: (url: string, body: ICredentials): Promise<AxiosResponse> => apiClient.post(url, body).then(responseBody),
  profile: (url: string, body: IUser): Promise<AxiosResponse> => apiClient.post(url, body).then(responseBody),
  newprof: (url: string, body: ICreateProf): Promise<AxiosResponse> => apiClient.post(url, body).then(responseBody),
  newaluno: (url: string, body: ICreateAluno): Promise<AxiosResponse> => apiClient.post(url, body).then(responseBody),
  put: (url: string, body: IUser): Promise<AxiosResponse> => apiClient.put(url, body).then(responseBody),
  delete: (url: string): Promise<AxiosResponse> => apiClient.delete(url).then(responseBody),
};

export const Auth = {
  getPosts: (): Promise<AxiosResponse> => requests.get('posts'),

  getAPost: (id: number): Promise<AxiosResponse> => requests.get(`posts/${id}`),

  getProfessores: (): Promise<AxiosResponse> => requests.get('professores'),

  getAlunos: (): Promise<AxiosResponse> => requests.get('alunos'),

  register: (post: ICredentials): Promise<AxiosResponse> => 
    requests.post('auth/register', post),

  login: (post: ICredentials): Promise<AxiosResponse> =>
    requests.post('auth/login', post),

  update_profile: (post: IUser): Promise<AxiosResponse> =>
    requests.profile('auth/profile', post),

  new_prof: (post: ICreateProf): Promise<AxiosResponse> =>
    requests.newprof('auth/register', post),

  new_aluno: (post: ICreateAluno): Promise<AxiosResponse> =>
    requests.newprof('auth/register', post),

  me: (): Promise<AxiosResponse> => requests.get('auth/me'),

  confirmEmail: (token: string): Promise<AxiosResponse> => requests.get(`auth/confirm/?token=${token}`),

  updatePost: (post: IUser, id: number): Promise<AxiosResponse> =>
    requests.put(`posts/${id}`, post),

  deletePost: (id: number): Promise<AxiosResponse> => requests.delete(`posts/${id}`),
};


export default boot(({ app }) => {
  // for use inside Vue files (Options API) through this.$axios and this.$api

  app.config.globalProperties.$axios = axios;
  // ^ ^ ^ this will allow you to use this.$axios (for Vue Options API form)
  //       so you won't necessarily have to import axios in each vue file

  app.config.globalProperties.$api = apiClient;
  // ^ ^ ^ this will allow you to use this.$api (for Vue Options API form)
  //       so you can easily perform requests against your app's API
});

export { apiClient };
