import { IUser, ICredentials, IMe } from '@/types/global'
import axios, { AxiosInstance, AxiosResponse, AxiosError } from "axios";
import { useAuth } from '@/store/userAuth'
import router from '@/router'



const apiClient: AxiosInstance = axios.create({
  baseURL: "http://localhost:5000/",
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
        "auth/refresh-token",
        {
          withCredentials: true,
        }
      )
      .catch((err) => {
        const store = useAuth()
        store.logout()
        router.push({ name: 'login' })
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
  get: (url: string) => apiClient.get(url).then(responseBody),
  post: (url: string, body: {}) => apiClient.post(url, body).then(responseBody),
  put: (url: string, body: {}) => apiClient.put(url, body).then(responseBody),
  delete: (url: string) => apiClient.delete(url).then(responseBody),
};

export const Auth = {
  getPosts: (): Promise<any> => requests.get('posts'),

  getProfessores: (): Promise<any> => requests.get('professores'),

  register: (post: ICredentials): Promise<any> => 
    requests.post('auth/register', post),

  login: (post: ICredentials): Promise<any> =>
    requests.post('auth/login', post),

  me: (): Promise<any> => requests.get('auth/me'),

  confirmEmail: (token: string): Promise<any> => requests.get(`auth/confirm/?token=${token}`),

  updatePost: (post: IUser, id: number): Promise<any> =>
  requests.put(`posts/${id}`, post),

  deletePost: (id: number): Promise<any> => requests.delete(`posts/${id}`),
};


export default apiClient
