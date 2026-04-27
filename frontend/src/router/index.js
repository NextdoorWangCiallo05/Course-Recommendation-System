import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: () => import('../views/Login.vue') },
  { path: '/register', component: () => import('../views/Register.vue') },
  { path: '/admin', component: () => import('../views/AdminDashboard.vue'), meta: { requiresAuth: true, role: 'admin' } },
  { path: '/student', component: () => import('../views/StudentDashboard.vue'), meta: { requiresAuth: true, role: 'student' } },
  { path: '/superadmin', component: () => import('../views/AdminDashboard.vue'), meta: { requiresAuth: true, role: 'superadmin' } },
  { path: '/user-management', component: () => import('../views/UserManagement.vue'), meta: { requiresAuth: true, role: 'superadmin' } },
  { path: '/feedback', component: () => import('../views/Feedback.vue'), meta: { requiresAuth: true } },
  { path: '/user-center', component: () => import('../views/UserCenter.vue'), meta: { requiresAuth: true } },
  { path: '/simulated-selection', component: () => import('../views/SimulatedSelection.vue'), meta: { requiresAuth: true } }
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
    // 超管可以访问所有需要 admin 权限的页面
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
