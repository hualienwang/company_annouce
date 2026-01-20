import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import './style.css'

console.log('[main.js] 开始初始化应用...')

// 更新加载状态
const updateLoadingStatus = (message) => {
  const statusEl = document.getElementById('status')
  if (statusEl) {
    statusEl.innerHTML += '<div>' + new Date().toLocaleTimeString() + ' - ' + message + '</div>'
  }
  console.log(`[main.js] ${message}`)
}

updateLoadingStatus('正在加载模块...')

// 创建 Pinia（必须先创建，因为路由守卫需要使用 store）
updateLoadingStatus('正在初始化 Pinia...')
const pinia = createPinia()

// 创建 Vue 应用
updateLoadingStatus('正在创建 Vue 应用...')
const app = createApp(App)

// 先安装 Pinia
updateLoadingStatus('正在安装 Pinia...')
app.use(pinia)

// 现在创建并配置路由
updateLoadingStatus('正在初始化 Router...')

// 延迟导入路由组件和 store，避免循环依赖
const setupRouter = async () => {
  try {
    // 动态导入 store 和组件
    const { useAuthStore } = await import('./stores/auth.ts')
    const Home = (await import('./views/Home.vue')).default
    const AnnouncementDetail = (await import('./views/AnnouncementDetail.vue')).default
    const Admin = (await import('./views/Admin.vue')).default
    const ColleagueResponses = (await import('./views/ColleagueResponses.vue')).default
    const Login = (await import('./views/Login.vue')).default

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

    // 路由守卫 - 现在 Pinia 已经安装了
    router.beforeEach((to, _from, next) => {
      try {
        const authStore = useAuthStore()

        console.log('路由守卫:', to.path, 'isAuthenticated:', authStore?.isAuthenticated, 'isAdmin:', authStore?.isAdmin)

        // 如果store还没有初始化，直接通过
        if (!authStore) {
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

        next()
      } catch (error) {
        console.error('路由守卫错误:', error)
        // 出错时允许导航，避免页面卡住
        next()
      }
    })

    return router
  } catch (error) {
    console.error('[main.js] Router setup failed:', error)
    throw error
  }
}

// 设置路由
setupRouter().then(router => {
  updateLoadingStatus('正在安装 Router...')
  app.use(router)

  // 添加全局错误处理
  app.config.errorHandler = (err, _instance, info) => {
    console.error('[main.js] 全局错误:', err, info)

    const errorsEl = document.getElementById('error')
    if (errorsEl) {
      errorsEl.style.display = 'block'
      errorsEl.innerHTML += `<br>全局错误: ${err.message}<br>${info}`
    }
  }

  // 挂载应用
  updateLoadingStatus('正在挂载应用...')
  app.mount('#app')

  console.log('[main.js] 应用初始化完成并已挂载')

  // 隐藏加载指示器
  setTimeout(() => {
    const loading = document.getElementById('loading')
    if (loading) {
      loading.style.display = 'none'
    }
  }, 100)
}).catch(error => {
  console.error('[main.js] 初始化失败:', error)

  const errorsEl = document.getElementById('error')
  if (errorsEl) {
    errorsEl.style.display = 'block'
    errorsEl.innerHTML += `<br>初始化失败: ${error.message}`
  }

  updateLoadingStatus('初始化失败!')
})
