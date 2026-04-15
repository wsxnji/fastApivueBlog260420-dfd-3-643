<template>
  <div class="admin">
    <h1 class="page-title">文章管理</h1>
    <div class="admin-header">
      <router-link to="/admin/create" class="btn btn-primary">新建文章</router-link>
    </div>
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="posts-table">
      <table v-if="posts.length > 0">
        <thead>
          <tr>
            <th>标题</th>
            <th>创建时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="post in posts" :key="post.id">
            <td>{{ post.title }}</td>
            <td>{{ formatDate(post.created_at) }}</td>
            <td class="actions">
              <router-link :to="`/admin/edit/${post.id}`" class="btn btn-sm">编辑</router-link>
              <button @click="handleDelete(post.id)" class="btn btn-sm btn-danger">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="no-posts">
        <p>暂无文章，点击"新建文章"创建第一篇</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { postApi } from '../api'

const router = useRouter()
const posts = ref([])
const loading = ref(true)
const error = ref(null)

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const loadPosts = async () => {
  try {
    loading.value = true
    error.value = null
    const response = await postApi.getPosts({ limit: 100 })
    posts.value = response.data
  } catch (err) {
    error.value = '加载文章列表失败'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const handleDelete = async (id) => {
  if (!confirm('确定要删除这篇文章吗？')) return
  
  try {
    await postApi.deletePost(id)
    await loadPosts()
    alert('删除成功')
  } catch (err) {
    alert('删除失败')
    console.error(err)
  }
}

onMounted(() => {
  loadPosts()
})
</script>

<style scoped>
.page-title {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: #2c3e50;
}

.admin-header {
  margin-bottom: 2rem;
}

.btn {
  padding: 0.5rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  transition: all 0.3s;
  font-size: 0.9rem;
}

.btn-primary {
  background-color: #3498db;
  color: #fff;
}

.btn-primary:hover {
  background-color: #2980b9;
}

.btn-sm {
  padding: 0.3rem 0.8rem;
  font-size: 0.85rem;
}

.btn-danger {
  background-color: #e74c3c;
  color: #fff;
}

.btn-danger:hover {
  background-color: #c0392b;
}

.posts-table {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  overflow: hidden;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 1rem 1.5rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

th {
  background-color: #f8f9fa;
  font-weight: 600;
  color: #2c3e50;
}

tr:hover {
  background-color: #f8f9fa;
}

.actions {
  display: flex;
  gap: 0.5rem;
}

.loading, .error, .no-posts {
  text-align: center;
  padding: 3rem;
  color: #666;
}

.error {
  color: #e74c3c;
}
</style>
