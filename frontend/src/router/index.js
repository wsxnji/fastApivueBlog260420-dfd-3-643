import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import PostDetail from '../views/PostDetail.vue'

// 后台相关页面
import AdminLayout from '../views/admin/AdminLayout.vue'
import Login from '../views/admin/Login.vue'
import Dashboard from '../views/admin/Dashboard.vue'
import UserManagement from '../views/admin/UserManagement.vue'
import CreatePost from '../views/CreatePost.vue'
import EditPost from '../views/EditPost.vue'

// 路由守卫 - 检查是否已登录
const requireAuth = (to, from, next) => {
  const token = localStorage.getItem('token')
  if (!token) {
    next('/admin/login')
  } else {
    next()
  }
}

// 路由守卫 - 检查是否未登录（用于登录页）
const requireGuest = (to, from, next) => {
  const token = localStorage.getItem('token')
  if (token) {
    next('/admin/dashboard')
  } else {
    next()
  }
}

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
  // 后台登录页
  {
    path: '/admin/login',
    name: 'AdminLogin',
    component: Login,
    beforeEnter: requireGuest
  },
  // 后台布局（需要登录）
  {
    path: '/admin',
    component: AdminLayout,
    beforeEnter: requireAuth,
    children: [
      {
        path: '',
        redirect: '/admin/dashboard'
      },
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: Dashboard
      },
      {
        path: 'posts',
        name: 'AdminPosts',
        component: Dashboard
      },
      {
        path: 'posts/create',
        name: 'AdminCreatePost',
        component: CreatePost
      },
      {
        path: 'posts/edit/:id',
        name: 'AdminEditPost',
        component: EditPost
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: UserManagement
      }
    ]
  },
  // 兼容旧路由
  {
    path: '/admin/create',
    redirect: '/admin/posts/create'
  },
  {
    path: '/admin/edit/:id',
    redirect: to => `/admin/posts/edit/${to.params.id}`
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router