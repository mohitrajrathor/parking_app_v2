// axios.js
import axios from 'axios'
import store from '../store'
import router from '../router'

const api = axios.create({
  baseURL: import.meta.env.VITE_BASE_URL,
  withCredentials: true,
})

// Add access token to each request
api.interceptors.request.use(
  config => {
    const token = store.getters.getToken
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => Promise.reject(error)
)


api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      store.dispatch('logout', { sessionExpired: true })
      router.push({ name: 'Home' })
    }
    return Promise.reject(error)
  }
)

export default api
