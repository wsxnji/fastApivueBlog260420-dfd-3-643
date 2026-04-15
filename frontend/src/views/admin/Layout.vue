<template>
  <div class="admin-layout">
    <aside class="sidebar">
      <div class="sidebar-header">
        <h2>后台管理</h2>
      </div>
      <nav class="sidebar-nav">
        <div class="nav-section">
          <div class="nav-section-title">导航列表</div>
          <router-link to="/admin/dashboard" class="nav-item" active-class="active">
            <span class="nav-icon">📄</span>
            <span>文章管理</span>
          </router-link>
          <router-link
            v-if="isAdmin"
            to="/admin/users"
            class="nav-item"
            active-class="active"
          >
            <span class="nav-icon">👥</span>
            <span>用户管理</span>
          </router-link>
        </div>
      </nav>
      <div class="sidebar-footer">
        <div class="user-info">
          <span class="user-name">{{ user?.username }}</span>
          <span class="user-role">{{ user?.role }}</span>
        </div>
        <button @click="handleLogout" class="btn-logout">退出登录</button>
      </div>
    </aside>
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const user = ref(null)

const isAdmin = computed(() => user.value?.role === '超级管理员')

const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  router.push('/admin/login')
}

onMounted(() => {
  const userStr = localStorage.getItem('user')
  if (userStr) {
    user.value = JSON.parse(userStr)
  }
})
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.sidebar {
  width: 240px;
  background-color: #2c3e50;
  color: #fff;
  display: flex;
  flex-direction: column;
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
}

.sidebar-header {
  padding: 1.5rem;
  border-bottom: 1px solid #34495e;
}

.sidebar-header h2 {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
}

.sidebar-nav {
  flex: 1;
  padding: 1rem 0;
  overflow-y: auto;
}

.nav-section {
  margin-bottom: 1rem;
}

.nav-section-title {
  padding: 0.5rem 1.5rem;
  font-size: 0.75rem;
  color: #95a5a6;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 0.75rem 1.5rem;
  color: #ecf0f1;
  text-decoration: none;
  transition: all 0.3s;
}

.nav-item:hover {
  background-color: #34495e;
}

.nav-item.active {
  background-color: #3498db;
  color: #fff;
}

.nav-icon {
  margin-right: 0.75rem;
  font-size: 1rem;
}

.sidebar-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #34495e;
}

.user-info {
  display: flex;
  flex-direction: column;
  margin-bottom: 0.75rem;
}

.user-name {
  font-weight: 500;
  font-size: 0.9rem;
}

.user-role {
  font-size: 0.75rem;
  color: #95a5a6;
}

.btn-logout {
  width: 100%;
  padding: 0.5rem;
  background-color: #e74c3c;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: background-color 0.3s;
}

.btn-logout:hover {
  background-color: #c0392b;
}

.main-content {
  flex: 1;
  margin-left: 240px;
  padding: 2rem;
}
</style>
