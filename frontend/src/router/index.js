import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import PostDetail from '../views/PostDetail.vue'
import CreatePost from '../views/CreatePost.vue'
import EditPost from '../views/EditPost.vue'
import Login from '../views/admin/Login.vue'
import AdminLayout from '../views/admin/AdminLayout.vue'
import Posts from '../views/admin/Posts.vue'
import Users from '../views/admin/Users.vue'

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
    path: '/admin/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/admin',
    component: AdminLayout,
    children: [
      {
        path: '',
        redirect: '/admin/posts'
      },
      {
        path: 'posts',
        name: 'Posts',
        component: Posts
      },
      {
        path: 'users',
        name: 'Users',
        component: Users
      },
      {
        path: 'create',
        name: 'CreatePost',
        component: CreatePost
      },
      {
        path: 'edit/:id',
        name: 'EditPost',
        component: EditPost
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
