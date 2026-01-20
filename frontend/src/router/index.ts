import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import Home from '../views/Home.vue'
import AnnouncementDetail from '../views/AnnouncementDetail.vue'
import Admin from '../views/Admin.vue'
import ColleagueResponses from '../views/ColleagueResponses.vue'
import Login from '../views/Login.vue'


const routes = [
  {
    path: '/login',
    name: 'login',
    component: Login,
    meta: { requiresAuth: false },
  },
  
  {
    path: '/',
    name: 'home',
    component: Home,
    meta: { requiresAuth: true },
  },
  
  {
    path: '/announcement/:id',
    name: 'announcement-detail',
    component: AnnouncementDetail,
    props: true,
    meta: { requiresAuth: true },
  },
  {
    path: '/admin',
    name: 'admin',
    component: Admin,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/responses/:colleagueName',
    name: 'colleague-responses',
    component: ColleagueResponses,
    props: true,
    meta: { requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 路由守卫
router.beforeEach((to, _from, next) => {
  try {
    const authStore = useAuthStore()

    console.log('路由守卫:', to.path, 'isAuthenticated:', authStore?.isAuthenticated, 'isAdmin:', authStore?.isAdmin, 'isInitialized:', authStore?.isInitialized)

    // 如果store还没有初始化，直接通过（等待store从localStorage加载）
    if (!authStore?.isInitialized) {
      console.warn('Auth store not initialized yet, allowing navigation')
      next()
      return
    }

    // 检查是否需要认证
    if (to.meta.requiresAuth && !authStore.isAuthenticated) {
      console.log('需要认证，跳转到登录页')
      next({ name: 'login' })
      return
    }

    // 检查管理员权限
    if (to.meta.requiresAdmin && !authStore.isAdmin) {
      console.log('需要管理员权限，跳转到首页')
      next({ name: 'home' })
      return
    }

    // 如果已登录且访问登录页，跳转到首页
    if (to.name === 'login' && authStore.isAuthenticated) {
      console.log('已登录，跳转到首页')
      next({ name: 'home' })
      return
    }

    console.log('允许导航到:', to.path)
    next()
  } catch (error) {
    console.error('路由守卫错误:', error)
    next() // 出错时也允许通过
  }
})

export default router
