<template>
  <div class="admin-layout">
    <aside class="sidebar">
      <div class="sidebar-header">
        <h2>后台管理</h2>
      </div>
      <nav class="sidebar-nav">
        <router-link
          v-for="menu in menus"
          :key="menu.path"
          :to="menu.path"
          class="nav-item"
          active-class="nav-item-active"
        >
          <span class="nav-icon">{{ menu.icon }}</span>
          <span>{{ menu.title }}</span>
        </router-link>
      </nav>
      <div class="sidebar-footer">
        <div class="user-info">
          <span class="username">{{ user?.username }}</span>
          <span class="role-badge">{{ userRoleLabel }}</span>
        </div>
        <button @click="handleLogout" class="btn btn-logout">退出登录</button>
      </div>
    </aside>
    <main class="admin-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const user = computed(() => {
  try {
    return JSON.parse(localStorage.getItem('user'))
  } catch {
    return null
  }
})

const userRoleLabel = computed(() => {
  return user.value?.role === 'admin' ? '超级管理员' : '普通用户'
})

const allMenus = [
  {
    path: '/admin/dashboard',
    title: '文章管理',
    icon: '📝',
    roles: ['admin', 'user']
  },
  {
    path: '/admin/users',
    title: '用户管理',
    icon: '👥',
    roles: ['admin']
  }
]

const menus = computed(() => {
  return allMenus.filter(menu => menu.roles.includes(user.value?.role))
})

const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  router.push('/admin/login')
}

onMounted(() => {
  const token = localStorage.getItem('token')
  if (!token) {
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
  width: 240px;
  background: #2c3e50;
  color: #fff;
  display: flex;
  flex-direction: column;
  border-radius: 8px;
}

.sidebar-header {
  padding: 1.5rem;
  border-bottom: 1px solid #34495e;
}

.sidebar-header h2 {
  font-size: 1.25rem;
  margin: 0;
}

.sidebar-nav {
  flex: 1;
  padding: 1rem 0;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1.5rem;
  color: #bdc3c7;
  text-decoration: none;
  transition: all 0.3s;
}

.nav-item:hover {
  background: #34495e;
  color: #fff;
}

.nav-item-active {
  background: #3498db;
  color: #fff;
}

.nav-icon {
  font-size: 1.1rem;
}

.sidebar-footer {
  padding: 1rem;
  border-top: 1px solid #34495e;
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  margin-bottom: 1rem;
}

.username {
  font-weight: 500;
}

.role-badge {
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
  background: #34495e;
  border-radius: 4px;
  display: inline-block;
  width: fit-content;
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

.btn-logout {
  width: 100%;
  background: #e74c3c;
  color: #fff;
}

.btn-logout:hover {
  background: #c0392b;
}

.admin-content {
  flex: 1;
  padding: 0 0 0 1.5rem;
}
</style>
