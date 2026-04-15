<template>
  <div class="admin-layout">
    <!-- 左侧导航栏 -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <h2>后台管理</h2>
      </div>
      <nav class="sidebar-nav">
        <ul class="nav-list">
          <li 
            v-for="menu in menus" 
            :key="menu.id"
            class="nav-item"
            :class="{ active: isActive(menu.path) }"
          >
            <router-link :to="menu.path" class="nav-link">
              <span class="nav-icon">{{ getIcon(menu.icon) }}</span>
              <span class="nav-name">{{ menu.name }}</span>
            </router-link>
          </li>
        </ul>
      </nav>
      <div class="sidebar-footer">
        <div class="user-info">
          <span class="username">{{ user?.username }}</span>
          <span class="role">{{ user?.role === 'admin' ? '超级管理员' : '普通用户' }}</span>
        </div>
        <button class="btn-logout" @click="handleLogout">
          退出登录
        </button>
      </div>
    </aside>

    <!-- 主内容区 -->
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { authApi } from '../../api'

const router = useRouter()
const route = useRoute()
const menus = ref([])
const user = ref(null)

// 图标映射
const iconMap = {
  document: '📄',
  user: '👤'
}

const getIcon = (iconName) => {
  return iconMap[iconName] || '📋'
}

const isActive = (path) => {
  return route.path.startsWith(path)
}

const loadMenus = async () => {
  try {
    const response = await authApi.getMenus()
    menus.value = response.data.menus
  } catch (err) {
    console.error('加载菜单失败:', err)
  }
}

const loadUserInfo = () => {
  const userStr = localStorage.getItem('user')
  if (userStr) {
    user.value = JSON.parse(userStr)
  }
}

const handleLogout = () => {
  // 清除登录信息
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  // 跳转到登录页
  router.push('/admin/login')
}

onMounted(() => {
  loadUserInfo()
  loadMenus()
})
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
}

/* 侧边栏 */
.sidebar {
  width: 240px;
  background-color: #2c3e50;
  color: #fff;
  display: flex;
  flex-direction: column;
  position: fixed;
  height: 100vh;
  left: 0;
  top: 0;
}

.sidebar-header {
  padding: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-header h2 {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 600;
}

.sidebar-nav {
  flex: 1;
  padding: 1rem 0;
  overflow-y: auto;
}

.nav-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-item {
  margin: 0.25rem 0;
}

.nav-link {
  display: flex;
  align-items: center;
  padding: 0.875rem 1.5rem;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: all 0.3s;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.nav-item.active .nav-link {
  background-color: #3498db;
  color: #fff;
}

.nav-icon {
  margin-right: 0.75rem;
  font-size: 1.1rem;
}

.nav-name {
  font-size: 0.95rem;
}

/* 侧边栏底部 */
.sidebar-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.user-info {
  margin-bottom: 0.75rem;
}

.username {
  display: block;
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.role {
  display: block;
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.6);
}

.btn-logout {
  width: 100%;
  padding: 0.5rem;
  background-color: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  color: rgba(255, 255, 255, 0.8);
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.85rem;
}

.btn-logout:hover {
  background-color: rgba(231, 76, 60, 0.8);
  border-color: rgba(231, 76, 60, 0.8);
  color: #fff;
}

/* 主内容区 */
.main-content {
  flex: 1;
  margin-left: 240px;
  padding: 2rem;
  background-color: #f5f5f5;
  min-height: 100vh;
}
</style>
