import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../api/client'

interface User {
  id: number
  username: string
  email: string
  full_name: string
  role: string
  is_active: boolean
}

interface LoginResponse {
  access_token: string
  token_type: string
  user: User
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
  const isInitialized = ref(false)

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')

  // 从 localStorage 加载
  const loadFromStorage = () => {
    try {
      const storedToken = localStorage.getItem('access_token')
      const storedUser = localStorage.getItem('user')
      if (storedToken) {
        token.value = storedToken
      }
      if (storedUser) {
        user.value = JSON.parse(storedUser)
      }
      console.log('✓ Auth loaded from storage:', { isAuthenticated: !!token.value, user: user.value?.username })
    } catch (error) {
      console.error('Failed to load auth from storage:', error)
    } finally {
      isInitialized.value = true
    }
  }

  // 保存到 localStorage
  const saveToStorage = () => {
    try {
      if (token.value) {
        localStorage.setItem('access_token', token.value)
      }
      if (user.value) {
        localStorage.setItem('user', JSON.stringify(user.value))
      }
    } catch (error) {
      console.error('Failed to save auth to storage:', error)
    }
  }

  // 清除
  const clearStorage = () => {
    try {
      localStorage.removeItem('access_token')
      localStorage.removeItem('user')
    } catch (error) {
      console.error('Failed to clear auth from storage:', error)
    }
  }

  // 登录
  const login = async (credentials: { username: string; password: string }) => {
    const formData = new FormData()
    formData.append('username', credentials.username)
    formData.append('password', credentials.password)

    const response = await api.post<LoginResponse>('/auth/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })

    token.value = response.data.access_token
    user.value = response.data.user
    saveToStorage()
  }

  // 注册
  const register = async (userData: {
    username: string
    email: string
    password: string
    full_name: string
  }) => {
    console.log('[Auth Store] 开始注册:', userData)
    try {
      const response = await api.post<{message: string}>('/auth/register', userData)
      console.log('[Auth Store] 注册成功:', response.data)
      return response.data
    } catch (error) {
      console.error('[Auth Store] 注册失败:', error)
      throw error
    }
  }

  // 登出
  const logout = () => {
    token.value = null
    user.value = null
    clearStorage()
  }

  // 获取当前用户信息
  const getCurrentUser = async () => {
    const response = await api.get('/auth/me')
    user.value = response.data
    saveToStorage()
  }

  // 初始化 - 在 store 函数内部调用
  loadFromStorage()

  return {
    user,
    token,
    isAuthenticated,
    isAdmin,
    login,
    register,
    logout,
    getCurrentUser,
    isInitialized,
  }
})
