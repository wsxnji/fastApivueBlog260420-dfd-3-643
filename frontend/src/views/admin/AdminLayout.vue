<template>
  <div class="admin-layout">
    <aside class="sidebar">
      <div class="sidebar-header">
        <h2>后台管理</h2>
        <div class="user-info">
          <span class="username">{{ user?.username }}</span>
          <span class="role-badge">{{ user?.role }}</span>
        </div>
      </div>
      <nav class="nav-menu">
        <p class="nav-title">导航列表</p>
        <router-link
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          class="nav-item"
          active-class="nav-item-active"
        >
          <span>{{ item.name }}</span>
        </router-link>
      </nav>
      <div class="sidebar-footer">
        <button @click="handleLogout" class="btn btn-logout">退出登录</button>
      </div>
    </aside>
    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const user = ref(null)

const menuItems = computed(() => {
  const menus = [
    { name: '文章管理', path: '/admin/posts' }
  ]
  if (user.value?.role === '超级管理员') {
    menus.push({ name: '用户管理', path: '/admin/users' })
  }
  return menus
})

const handleLogout = () => {
  localStorage.removeItem('user')
  router.push('/admin/login')
}

onMounted(() => {
  const userData = localStorage.getItem('user')
  if (userData) {
    user.value = JSON.parse(userData)
  } else {
    router.push('/admin/login')
  }
})
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: calc(100vh - 80px);
}

.sidebar {
  width: 250px;
  background: #2c3e50;
  color: #fff;
  display: flex;
  flex-direction: column;
  border-radius: 8px;
}

.sidebar-header {
  padding: 1.5rem;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}

.sidebar-header h2 {
  font-size: 1.3rem;
  margin-bottom: 1rem;
  color: #3498db;
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.username {
  font-size: 0.95rem;
}

.role-badge {
  font-size: 0.8rem;
  background: rgba(52, 152, 219, 0.2);
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  display: inline-block;
  width: fit-content;
}

.nav-menu {
  flex: 1;
  padding: 1rem 0;
}

.nav-title {
  padding: 0.5rem 1.5rem;
  font-size: 0.8rem;
  color: rgba(255,255,255,0.5);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 0.5rem;
}

.nav-item {
  display: block;
  padding: 0.9rem 1.5rem;
  color: rgba(255,255,255,0.8);
  text-decoration: none;
  transition: all 0.3s;
  cursor: pointer;
}

.nav-item:hover {
  background: rgba(52, 152, 219, 0.2);
  color: #fff;
}

.nav-item-active {
  background: #3498db;
  color: #fff;
}

.sidebar-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid rgba(255,255,255,0.1);
}

.btn-logout {
  width: 100%;
  background: rgba(231, 76, 60, 0.8);
  color: #fff;
}

.btn-logout:hover {
  background: #e74c3c;
}

.content {
  flex: 1;
  padding: 0 2rem;
}
</style>
