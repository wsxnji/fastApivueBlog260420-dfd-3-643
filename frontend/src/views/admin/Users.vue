<template>
  <div class="users-page">
    <h1 class="page-title">用户管理</h1>
    <div class="users-table">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>用户名</th>
            <th>角色</th>
            <th>创建时间</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.username }}</td>
            <td>
              <span :class="['role-badge', user.role === '超级管理员' ? 'admin' : 'user']">
                {{ user.role }}
              </span>
            </td>
            <td>{{ formatDate(user.created_at) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const users = ref([])

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

onMounted(() => {
  users.value = [
    { id: 1, username: 'admin', role: '超级管理员', created_at: new Date().toISOString() },
    { id: 2, username: 'user1', role: '普通用户', created_at: new Date().toISOString() }
  ]
})
</script>

<style scoped>
.page-title {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: #2c3e50;
}

.users-table {
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

.role-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 500;
}

.role-badge.admin {
  background-color: #e8f4fd;
  color: #3498db;
}

.role-badge.user {
  background-color: #e8f8f0;
  color: #27ae60;
}
</style>
