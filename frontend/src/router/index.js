import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', redirect: '/login' },
  {
    path: '/login',
    name: 'Login',
    component: () => import(/* webpackChunkName: "login" */ '../views/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import(/* webpackChunkName: "register" */ '../views/Register.vue')
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import(/* webpackChunkName: "admin" */ '../views/AdminDashboard.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/student',
    name: 'Student',
    component: () => import(/* webpackChunkName: "student" */ '../views/StudentDashboard.vue'),
    meta: { requiresAuth: true, role: 'student' }
  },
  {
    path: '/superadmin',
    name: 'SuperAdmin',
    component: () => import(/* webpackChunkName: "admin" */ '../views/AdminDashboard.vue'),
    meta: { requiresAuth: true, role: 'superadmin' }
  },
  {
    path: '/user-management',
    name: 'UserManagement',
    component: () => import(/* webpackChunkName: "user-management" */ '../views/UserManagement.vue'),
    meta: { requiresAuth: true, role: 'superadmin' }
  },
  {
    path: '/feedback',
    name: 'Feedback',
    component: () => import(/* webpackChunkName: "feedback" */ '../views/Feedback.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/user-center',
    name: 'UserCenter',
    component: () => import(/* webpackChunkName: "user-center" */ '../views/UserCenter.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/simulated-selection',
    name: 'SimulatedSelection',
    component: () => import(/* webpackChunkName: "simulated-selection" */ '../views/SimulatedSelection.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/data-analysis',
    name: 'DataAnalysis',
    component: () => import(/* webpackChunkName: "data-analysis" */ '../views/DataAnalysis.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const role = localStorage.getItem('role')

  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.meta.role) {
    if (to.meta.role === 'admin' && (role === 'admin' || role === 'superadmin')) {
      next()
    } else if (to.meta.role === 'student' && (role === 'student' || role === 'admin' || role === 'superadmin')) {
      next()
    } else if (to.meta.role === 'superadmin' && role === 'superadmin') {
      next()
    } else {
      next('/login')
    }
  } else {
    next()
  }
})

export default router
