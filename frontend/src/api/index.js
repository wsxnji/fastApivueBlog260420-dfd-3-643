import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

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
