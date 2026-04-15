import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import PostDetail from '../views/PostDetail.vue'
import Admin from '../views/Admin.vue'
import CreatePost from '../views/CreatePost.vue'
import EditPost from '../views/EditPost.vue'
import AdminLogin from '../views/admin/Login.vue'
import AdminLayout from '../views/admin/Layout.vue'
import AdminDashboard from '../views/admin/Dashboard.vue'
import AdminUsers from '../views/admin/Users.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/post/:id',
    name: 'PostDetail',
    component: PostDetail
  },
  {
    path: '/admin',
    name: 'Admin',
    component: Admin
  },
  {
    path: '/admin/create',
    name: 'CreatePost',
    component: CreatePost
  },
  {
    path: '/admin/edit/:id',
    name: 'EditPost',
    component: EditPost
  },
  {
    path: '/admin/login',
    name: 'AdminLogin',
    component: AdminLogin
  },
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: AdminLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: AdminDashboard
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: AdminUsers,
        meta: { requiresAdmin: true }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const userStr = localStorage.getItem('user')
  const user = userStr ? JSON.parse(userStr) : null

  if (to.meta.requiresAuth && !token) {
    next('/admin/login')
  } else if (to.meta.requiresAdmin && user?.role !== '超级管理员') {
    next('/admin/dashboard')
  } else if (to.path === '/admin/login' && token) {
    next('/admin/dashboard')
  } else {
    next()
  }
})

export default router
