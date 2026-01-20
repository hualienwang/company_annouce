<template>
  <div style="min-height: 100vh; display: flex; align-items: center; justify-content: center; background-color: #f9fafb; padding: 12px;">
    <div style="max-width: 28rem; width: 100%; margin-top: 2rem;">
      <div>
        <h2 style="text-align: center; font-weight: 800; font-size: 1.875rem; color: #111827; margin-top: 1.5rem;">
          {{ isLogin ? '登录' : '注册' }}
        </h2>
        <p style="text-align: center; margin-top: 8px; color: #6b7280; font-size: 0.875rem;">
          {{ isLogin ? '请输入您的账号和密码' : '创建一个新账号' }}
        </p>
      </div>

      <form @submit.prevent="handleSubmit" style="margin-top: 2rem;">
        <!-- 用户名（注册时显示） -->
        <div v-if="!isLogin" style="margin-bottom: 1rem;">
          <label style="display: block; font-weight: 500; font-size: 0.875rem; color: #374151; margin-bottom: 0.25rem;">
            用户名 *
          </label>
          <input
            v-model="form.username"
            type="text"
            required
            style="width: 100%; padding: 0.5rem 0.75rem; border: 1px solid #d1d5db; border-radius: 0.375rem; font-size: 0.875rem;"
            placeholder="请输入用户名"
          />
        </div>

        <!-- 邮箱 -->
        <div style="margin-bottom: 1rem;">
          <label style="display: block; font-weight: 500; font-size: 0.875rem; color: #374151; margin-bottom: 0.25rem;">
            {{ isLogin ? '用户名' : '邮箱' }} *
          </label>
          <input
            v-model="form.email"
            type="text"
            required
            style="width: 100%; padding: 0.5rem 0.75rem; border: 1px solid #d1d5db; border-radius: 0.375rem; font-size: 0.875rem;"
            :placeholder="isLogin ? '请输入用户名' : '请输入邮箱'"
          />
        </div>

        <!-- 密码 -->
        <div style="margin-bottom: 1rem;">
          <label style="display: block; font-weight: 500; font-size: 0.875rem; color: #374151; margin-bottom: 0.25rem;">
            密码 *
          </label>
          <input
            v-model="form.password"
            type="password"
            required
            style="width: 100%; padding: 0.5rem 0.75rem; border: 1px solid #d1d5db; border-radius: 0.375rem; font-size: 0.875rem;"
            placeholder="请输入密码"
          />
        </div>

        <!-- 真实姓名（注册时显示） -->
        <div v-if="!isLogin" style="margin-bottom: 1rem;">
          <label style="display: block; font-weight: 500; font-size: 0.875rem; color: #374151; margin-bottom: 0.25rem;">
            真实姓名 *
          </label>
          <input
            v-model="form.full_name"
            type="text"
            required
            style="width: 100%; padding: 0.5rem 0.75rem; border: 1px solid #d1d5db; border-radius: 0.375rem; font-size: 0.875rem;"
            placeholder="请输入真实姓名"
          />
        </div>

        <!-- 提交按钮 -->
        <div style="margin-top: 1.5rem;">
          <button
            type="submit"
            :disabled="loading"
            style="width: 100%; display: flex; justify-content: center; padding: 0.5rem 1rem; border: none; border-radius: 0.375rem; font-size: 0.875rem; font-weight: 500; color: white; background-color: #2563eb; cursor: pointer;"
            :style="{ opacity: loading ? 0.5 : 1, cursor: loading ? 'not-allowed' : 'pointer' }"
          >
            {{ loading ? '处理中...' : (isLogin ? '登录' : '注册') }}
          </button>
        </div>

        <!-- 切换登录/注册 -->
        <div style="text-align: center; margin-top: 1rem;">
          <button
            type="button"
            @click="toggleMode"
            style="color: #2563eb; text-decoration: none; border: none; background: none; cursor: pointer; font-size: 0.875rem;"
          >
            {{ isLogin ? '没有账号？去注册' : '已有账号？去登录' }}
          </button>
        </div>

        <!-- 测试链接 -->
        <div style="text-align: center; margin-top: 0.5rem;">
          <a
            href="/test-register"
            style="color: #6b7280; text-decoration: none; border: none; background: none; cursor: pointer; font-size: 0.75rem;"
          >
            注册功能诊断
          </a>
        </div>
      </form>

      <!-- 错误提示 -->
      <div v-if="error" style="background-color: #fef2f2; border: 1px solid #fecaca; color: #b91c1c; padding: 0.75rem 1rem; border-radius: 0.375rem; margin-top: 1rem;">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

console.log('[Login.vue] 组件开始加载')

const router = useRouter()
const authStore = useAuthStore()

console.log('[Login.vue] authStore:', authStore)
console.log('[Login.vue] isAuthenticated:', authStore.isAuthenticated)

const isLogin = ref(true)
const loading = ref(false)
const error = ref('')

const form = ref({
  username: '',
  email: '',
  password: '',
  full_name: '',
})

const toggleMode = () => {
  isLogin.value = !isLogin.value
  error.value = ''
  form.value = {
    username: '',
    email: '',
    password: '',
    full_name: '',
  }
}

const handleSubmit = async () => {
  console.log('[Login.vue] 提交表单:', isLogin.value ? '登录' : '注册')
  console.log('[Login.vue] 表单数据:', form.value)
  loading.value = true
  error.value = ''

  try {
    if (isLogin.value) {
      console.log('[Login.vue] 开始登录...')
      await authStore.login({
        username: form.value.email,
        password: form.value.password,
      })
      console.log('[Login.vue] 登录成功，跳转到首页')
      router.push('/')
    } else {
      console.log('[Login.vue] 开始注册...')
      const registerData = {
        username: form.value.username,
        email: form.value.email,
        password: form.value.password,
        full_name: form.value.full_name,
      }
      console.log('[Login.vue] 注册数据:', registerData)

      const result = await authStore.register(registerData)
      console.log('[Login.vue] 注册成功:', result)
      alert('注册成功！请等待管理员审核通过后再登录。')
      isLogin.value = true
      form.value = {
        username: '',
        email: '',
        password: '',
        full_name: '',
      }
    }
  } catch (err: any) {
    console.error('[Login.vue] 操作失败:', err)
    console.error('[Login.vue] 错误详情:', {
      message: err.message,
      response: err.response?.data,
      status: err.response?.status,
    })

    let errorMessage = '操作失败'
    if (err.response?.data?.detail) {
      errorMessage = err.response.data.detail
    } else if (err.message) {
      errorMessage = err.message
    } else if (err.toString) {
      errorMessage = err.toString()
    }

    error.value = errorMessage
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  console.log('[Login.vue] onMounted 触发')
  console.log('[Login.vue] 当前路径:', router.currentRoute.value.path)
  console.log('[Login.vue] 是否已登录:', authStore.isAuthenticated)

  // 如果已登录，跳转到首页
  if (authStore.isAuthenticated) {
    console.log('[Login.vue] 已登录，跳转到首页')
    router.push('/')
  }
})
</script>
