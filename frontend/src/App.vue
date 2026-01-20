<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <!-- 导航栏 -->
    <nav style="background: white; border-bottom: 1px solid #e5e7eb; padding: 16px;">
      <div style="max-width: 1280px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center;">
        <div style="display: flex; align-items: center; gap: 16px;">
          <RouterLink to="/" style="color: #374151; font-weight: 500; text-decoration: none;">
            📢 公司公告
          </RouterLink>
          <RouterLink
            v-if="authStore?.isAdmin"
            to="/admin"
            style="color: #6b7280; text-decoration: none;"
          >
            管理后台
          </RouterLink>
        </div>

        <div style="display: flex; align-items: center; gap: 16px;">
          <template v-if="authStore?.isAuthenticated">
            <span style="font-weight: 500;">{{ authStore.user?.full_name || '用户' }}</span>
            <button
              @click="handleLogout"
              style="padding: 8px 16px; background: #dc2626; color: white; border: none; border-radius: 6px; cursor: pointer;"
            >
              退出登录
            </button>
          </template>
          <RouterLink
            v-else
            to="/login"
            style="padding: 8px 16px; background: #2563eb; color: white; border-radius: 6px; text-decoration: none;"
          >
            登录
          </RouterLink>
        </div>
      </div>
    </nav>

    <!-- 主要内容 -->
    <main style="max-width: 1280px; margin: 0 auto; padding: 32px 16px;">
      <RouterView />
    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { RouterLink, RouterView, useRoute } from 'vue-router'
import { useAuthStore } from './stores/auth'

const authStore = useAuthStore()
const route = useRoute()

onMounted(() => {
  console.log('App.vue onMounted 触发')
  console.log('认证状态:', authStore.isAuthenticated)
  console.log('当前路由:', route.path)
  console.log('用户信息:', authStore.user)
})

const handleLogout = () => {
  if (confirm('确定要退出登录吗？')) {
    authStore.logout()
    window.location.href = '/login'
  }
}
</script>
