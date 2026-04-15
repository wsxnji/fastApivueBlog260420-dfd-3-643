import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

export const postApi = {
  getPosts(params) {
    return api.get('/posts', { params })
  },
  
  getPost(id) {
    return api.get(`/posts/${id}`)
  },
  
  createPost(data) {
    return api.post('/posts', data)
  },
  
  updatePost(id, data) {
    return api.put(`/posts/${id}`, data)
  },
  
  deletePost(id) {
    return api.delete(`/posts/${id}`)
  }
}

export const adminApi = {
  login(data) {
    return api.post('/admin/login', data)
  },
  
  getCurrentUser() {
    return api.get('/admin/me')
  }
}
