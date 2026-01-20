<template>
  <div class="relative">
    <button
      @click="toggleDropdown"
      class="relative p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-full"
    >
      <svg
        class="w-6 h-6"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
        />
      </svg>
      <span
        v-if="unreadCount > 0"
        class="absolute top-0 right-0 flex items-center justify-center w-5 h-5 text-xs font-bold text-white bg-red-500 rounded-full"
      >
        {{ unreadCount > 99 ? '99+' : unreadCount }}
      </span>
    </button>

    <div
      v-if="isOpen"
      class="absolute right-0 mt-2 w-96 bg-white rounded-lg shadow-lg border z-50"
    >
      <div class="p-4 border-b flex justify-between items-center">
        <h3 class="text-lg font-semibold">通知</h3>
        <button
          @click="markAllAsRead"
          class="text-sm text-blue-600 hover:text-blue-800"
        >
          全部已读
        </button>
      </div>

      <div class="max-h-96 overflow-y-auto">
        <div
          v-if="loading"
          class="p-4 text-center text-gray-500"
        >
          加载中...
        </div>

        <div
          v-else-if="notifications.length === 0"
          class="p-8 text-center text-gray-500"
        >
          暂无通知
        </div>

        <div v-else>
          <div
            v-for="notification in notifications"
            :key="notification.id"
            class="p-4 border-b hover:bg-gray-50 cursor-pointer"
            :class="{ 'bg-blue-50': !notification.is_read }"
            @click="handleNotificationClick(notification)"
          >
            <div class="flex justify-between items-start mb-1">
              <h4 class="font-medium text-gray-900">
                {{ notification.title }}
              </h4>
              <span class="text-xs text-gray-500">
                {{ formatTime(notification.created_at) }}
              </span>
            </div>
            <p class="text-sm text-gray-600">{{ notification.content }}</p>
            <div v-if="!notification.is_read" class="mt-1">
              <span class="inline-block w-2 h-2 bg-blue-500 rounded-full"></span>
              <span class="text-xs text-blue-600">未读</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import api from '../api/client'

const authStore = useAuthStore()

const isOpen = ref(false)
const loading = ref(false)
const notifications = ref<any[]>([])
const unreadCount = ref(0)

const toggleDropdown = () => {
  isOpen.value = !isOpen.value
  if (isOpen.value) {
    loadNotifications()
  }
}

const loadNotifications = async () => {
  if (!authStore.isAuthenticated) return

  loading.value = true
  try {
    // 获取未读通知数量
    const unreadResponse = await api.get('/notifications/unread-count')
    unreadCount.value = unreadResponse.data.unread_count

    // 获取最新通知
    const response = await api.get('/notifications', {
      params: { limit: 10 },
    })
    notifications.value = response.data
  } catch (error) {
    console.error('加载通知失败:', error)
  } finally {
    loading.value = false
  }
}

const handleNotificationClick = async (notification: any) => {
  // 标记为已读
  if (!notification.is_read) {
    try {
      await api.post(`/notifications/${notification.id}/read`)
      notification.is_read = true
      unreadCount.value = Math.max(0, unreadCount.value - 1)
    } catch (error) {
      console.error('标记已读失败:', error)
    }
  }

  // 如果有关联的公告，跳转到公告详情
  if (notification.related_id) {
    isOpen.value = false
    window.location.href = `/announcement/${notification.related_id}`
  }
}

const markAllAsRead = async () => {
  try {
    await api.post('/notifications/read-all')
    notifications.value.forEach((n) => (n.is_read = true))
    unreadCount.value = 0
  } catch (error) {
    console.error('标记全部已读失败:', error)
  }
}

const formatTime = (timeString: string) => {
  const date = new Date(timeString)
  const now = new Date()
  const diff = now.getTime() - date.getTime()

  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)

  if (minutes < 1) return '刚刚'
  if (minutes < 60) return `${minutes}分钟前`
  if (hours < 24) return `${hours}小时前`
  if (days < 7) return `${days}天前`

  return date.toLocaleDateString('zh-CN')
}

onMounted(() => {
  // 定时刷新未读数量
  setInterval(() => {
    if (authStore.isAuthenticated && !isOpen.value) {
      loadUnreadCount()
    }
  }, 60000) // 每分钟刷新一次
})

const loadUnreadCount = async () => {
  if (!authStore.isAuthenticated) return

  try {
    const response = await api.get('/notifications/unread-count')
    unreadCount.value = response.data.unread_count
  } catch (error) {
    console.error('加载未读数量失败:', error)
  }
}

// 点击外部关闭下拉菜单
document.addEventListener('click', (e) => {
  if (isOpen.value && !(e.target as HTMLElement).closest('.relative')) {
    isOpen.value = false
  }
})
</script>
