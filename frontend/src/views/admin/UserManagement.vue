<template>
  <div class="user-management">
    <h1 class="page-title">用户管理</h1>
    <div class="admin-header">
      <button class="btn btn-primary" @click="showCreateModal = true">新建用户</button>
    </div>
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="users-table">
      <table v-if="users.length > 0">
        <thead>
          <tr>
            <th>ID</th>
            <th>用户名</th>
            <th>角色</th>
            <th>状态</th>
            <th>创建时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.username }}</td>
            <td>
              <span class="role-badge" :class="user.role">
                {{ user.role === 'admin' ? '超级管理员' : '普通用户' }}
              </span>
            </td>
            <td>
              <span class="status-badge" :class="user.is_active ? 'active' : 'inactive'">
                {{ user.is_active ? '启用' : '禁用' }}
              </span>
            </td>
            <td>{{ formatDate(user.created_at) }}</td>
            <td class="actions">
              <button class="btn btn-sm" @click="handleEdit(user)">编辑</button>
              <button 
                v-if="user.id !== currentUserId" 
                class="btn btn-sm btn-danger" 
                @click="handleDelete(user.id)"
              >
                删除
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="no-users">
        <p>暂无用户</p>
      </div>
    </div>

    <!-- 创建用户弹窗 -->
    <div v-if="showCreateModal" class="modal-overlay" @click.self="showCreateModal = false">
      <div class="modal">
        <h3>新建用户</h3>
        <form @submit.prevent="handleCreate">
          <div class="form-group">
            <label>用户名</label>
            <input v-model="createForm.username" type="text" required />
          </div>
          <div class="form-group">
            <label>密码</label>
            <input v-model="createForm.password" type="password" required />
          </div>
          <div class="form-group">
            <label>角色</label>
            <select v-model="createForm.role" required>
              <option value="user">普通用户</option>
              <option value="admin">超级管理员</option>
            </select>
          </div>
          <div class="modal-actions">
            <button type="button" class="btn" @click="showCreateModal = false">取消</button>
            <button type="submit" class="btn btn-primary" :disabled="createLoading">
              {{ createLoading ? '创建中...' : '创建' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- 编辑用户弹窗 -->
    <div v-if="showEditModal" class="modal-overlay" @click.self="showEditModal = false">
      <div class="modal">
        <h3>编辑用户</h3>
        <form @submit.prevent="handleUpdate">
          <div class="form-group">
            <label>用户名</label>
            <input v-model="editForm.username" type="text" />
          </div>
          <div class="form-group">
            <label>密码（留空则不修改）</label>
            <input v-model="editForm.password" type="password" />
          </div>
          <div class="form-group">
            <label>角色</label>
            <select v-model="editForm.role">
              <option value="user">普通用户</option>
              <option value="admin">超级管理员</option>
            </select>
          </div>
          <div class="form-group">
            <label>状态</label>
            <select v-model="editForm.is_active">
              <option :value="true">启用</option>
              <option :value="false">禁用</option>
            </select>
          </div>
          <div class="modal-actions">
            <button type="button" class="btn" @click="showEditModal = false">取消</button>
            <button type="submit" class="btn btn-primary" :disabled="editLoading">
              {{ editLoading ? '保存中...' : '保存' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { authApi } from '../../api'

const users = ref([])
const loading = ref(true)
const error = ref(null)
const currentUserId = ref(null)

// 创建用户
const showCreateModal = ref(false)
const createLoading = ref(false)
const createForm = ref({
  username: '',
  password: '',
  role: 'user'
})

// 编辑用户
const showEditModal = ref(false)
const editLoading = ref(false)
const editForm = ref({
  id: null,
  username: '',
  password: '',
  role: 'user',
  is_active: true
})

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const loadUsers = async () => {
  try {
    loading.value = true
    error.value = null
    const response = await authApi.getUsers()
    users.value = response.data
  } catch (err) {
    error.value = '加载用户列表失败'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const handleCreate = async () => {
  createLoading.value = true
  try {
    await authApi.createUser(createForm.value)
    showCreateModal.value = false
    createForm.value = { username: '', password: '', role: 'user' }
    await loadUsers()
    alert('创建成功')
  } catch (err) {
    alert(err.response?.data?.detail || '创建失败')
  } finally {
    createLoading.value = false
  }
}

const handleEdit = (user) => {
  editForm.value = {
    id: user.id,
    username: user.username,
    password: '',
    role: user.role,
    is_active: user.is_active
  }
  showEditModal.value = true
}

const handleUpdate = async () => {
  editLoading.value = true
  try {
    const data = { ...editForm.value }
    if (!data.password) {
      delete data.password
    }
    await authApi.updateUser(data.id, data)
    showEditModal.value = false
    await loadUsers()
    alert('更新成功')
  } catch (err) {
    alert(err.response?.data?.detail || '更新失败')
  } finally {
    editLoading.value = false
  }
}

const handleDelete = async (id) => {
  if (!confirm('确定要删除这个用户吗？')) return

  try {
    await authApi.deleteUser(id)
    await loadUsers()
    alert('删除成功')
  } catch (err) {
    alert(err.response?.data?.detail || '删除失败')
  }
}

onMounted(() => {
  // 获取当前登录用户ID
  const userStr = localStorage.getItem('user')
  if (userStr) {
    const user = JSON.parse(userStr)
    currentUserId.value = user.id
  }
  loadUsers()
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

.users-table {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
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

.role-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
}

.role-badge.admin {
  background-color: #e74c3c;
  color: #fff;
}

.role-badge.user {
  background-color: #3498db;
  color: #fff;
}

.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
}

.status-badge.active {
  background-color: #27ae60;
  color: #fff;
}

.status-badge.inactive {
  background-color: #95a5a6;
  color: #fff;
}

.loading,
.error,
.no-users {
  text-align: center;
  padding: 3rem;
  color: #666;
}

.error {
  color: #e74c3c;
}

/* 弹窗样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: #fff;
  border-radius: 8px;
  padding: 2rem;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.modal h3 {
  margin-bottom: 1.5rem;
  color: #2c3e50;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 1.5rem;
}
</style>
