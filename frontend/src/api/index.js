// axios.js
import axios from 'axios'
import store from '../store'
import router from '../router'

const api = axios.create({
  baseURL: 'http://localhost:1234',
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

let isRefreshing = false
let failedQueue = []

function processQueue(error, token = null) {
  failedQueue.forEach(p => {
    if (error) {
      p.reject(error)
    } else {
      p.resolve(token)
    }
  })
  failedQueue = []
}

api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject })
        }).then(token => {
          originalRequest.headers['Authorization'] = 'Bearer ' + token
          return api(originalRequest)
        }).catch(err => Promise.reject(err))
      }

      isRefreshing = true

      const refreshToken = store.getters.getRefreshToken
      if (!refreshToken) {
        store.dispatch('logout')
        router.push({ name: 'Home' })
        return Promise.reject(error)
      }

      try {
        const res = await axios.post('/api_v1/auth/refresh', {
          refreshToken: refreshToken
        })

        const newToken = await res.data.accessToken;
        store.dispatch('setToken', newToken)

        api.defaults.headers.common['Authorization'] = 'Bearer ' + newToken
        originalRequest.headers['Authorization'] = 'Bearer ' + newToken

        processQueue(null, newToken)
        return api(originalRequest)
      } catch (err) {
        processQueue(err, null)
        store.dispatch('logout')
        router.push({ name: 'Home' })
        return Promise.reject(err)
      } finally {
        isRefreshing = false
      }
    }

    return Promise.reject(error)
  }
)

export default api
