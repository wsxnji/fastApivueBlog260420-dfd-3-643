<template>
  <div class="home">
    <h1 class="page-title">最新文章</h1>
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="posts-grid">
      <div v-for="post in posts" :key="post.id" class="post-card">
        <h2 class="post-title">
          <router-link :to="`/post/${post.id}`">{{ post.title }}</router-link>
        </h2>
        <p class="post-summary">{{ post.summary || post.content.substring(0, 150) + '...' }}</p>
        <div class="post-meta">
          <span class="post-date">{{ formatDate(post.created_at) }}</span>
        </div>
      </div>
    </div>
    <div v-if="posts.length === 0 && !loading" class="no-posts">
      <p>暂无文章</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { postApi } from '../api'

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
    const response = await postApi.getPosts({ limit: 20 })
    posts.value = response.data
  } catch (err) {
    error.value = '加载文章失败，请稍后重试'
    console.error(err)
  } finally {
    loading.value = false
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

.posts-grid {
  display: grid;
  gap: 2rem;
}

.post-card {
  background: #fff;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.post-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.post-title {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.post-title a {
  color: #2c3e50;
  text-decoration: none;
  transition: color 0.3s;
}

.post-title a:hover {
  color: #3498db;
}

.post-summary {
  color: #666;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.post-meta {
  color: #999;
  font-size: 0.9rem;
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
