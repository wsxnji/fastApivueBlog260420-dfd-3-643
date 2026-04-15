import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import PostDetail from '../views/PostDetail.vue'
import Admin from '../views/Admin.vue'
import CreatePost from '../views/CreatePost.vue'
import EditPost from '../views/EditPost.vue'

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
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
