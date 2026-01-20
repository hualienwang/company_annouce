import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import './style.css'

console.log('[main.ts] 开始初始化应用...')

// 更新加载状态
const updateLoadingStatus = (message: string) => {
  const statusEl = document.getElementById('loading-status')
  if (statusEl) {
    statusEl.textContent = message
  }
  console.log(`[main.ts] ${message}`)
}

updateLoadingStatus('正在初始化应用...')

// 创建 Pinia（必须先创建，因为路由守卫需要使用 store）
const pinia = createPinia()

// 创建 Vue 应用
const app = createApp(App)

// 先安装 Pinia
updateLoadingStatus('正在安装 Pinia...')
app.use(pinia)

// 安装路由
updateLoadingStatus('正在安装 Router...')
app.use(router)

// 添加全局错误处理
app.config.errorHandler = (err, _instance, info) => {
  console.error('[main.ts] 全局错误:', err, info)

  const errorsEl = document.getElementById('loading-errors')
  if (errorsEl) {
    errorsEl.innerHTML += `<br>全局错误: ${(err as Error).message}<br>${info}`
  }
}

// 挂载应用
updateLoadingStatus('正在挂载应用...')
app.mount('#app')

console.log('[main.ts] 应用初始化完成并已挂载')

// 隐藏加载指示器
setTimeout(() => {
  const loading = document.getElementById('loading')
  if (loading) {
    loading.style.display = 'none'
  }
}, 100)


