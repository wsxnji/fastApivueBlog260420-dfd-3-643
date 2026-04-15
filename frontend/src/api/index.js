import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器 - 添加token
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

// 响应拦截器 - 处理401错误
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // 清除登录信息并跳转到登录页
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/admin/login'
    }
    return Promise.reject(error)
  }
)

export const postApi = {
  // 获取所有文章
  getPosts(params) {
    return api.get('/posts', { params })
  },

  // 获取单篇文章
  getPost(id) {
    return api.get(`/posts/${id}`)
  },

  // 创建文章
  createPost(data) {
    return api.post('/posts', data)
  },

  // 更新文章
  updatePost(id, data) {
    return api.put(`/posts/${id}`, data)
  },

  // 删除文章
  deletePost(id) {
    return api.delete(`/posts/${id}`)
  }
}

export const authApi = {
  // 登录
  login(data) {
    return api.post('/admin/login', data)
  },

  // 获取当前用户信息
  getMe() {
    return api.get('/admin/me')
  },

  // 获取菜单
  getMenus() {
    return api.get('/admin/menus')
  },

  // 获取用户列表
  getUsers() {
    return api.get('/admin/users')
  },

  // 创建用户
  createUser(data) {
    return api.post('/admin/users', data)
  },

  // 更新用户
  updateUser(id, data) {
    return api.put(`/admin/users/${id}`, data)
  },

  // 删除用户
  deleteUser(id) {
    return api.delete(`/admin/users/${id}`)
  }
}
