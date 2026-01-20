<template>
  <div class="search-container">
    <div class="relative">
      <input
        v-model="query"
        type="text"
        @keyup.enter="handleSearch"
        placeholder="搜索公告和回复..."
        class="w-full px-4 py-2 pl-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
      />
      <svg
        class="absolute left-3 top-2.5 w-5 h-5 text-gray-400"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
        />
      </svg>
    </div>

    <!-- 搜索结果弹窗 -->
    <div
      v-if="isOpen && (query.length > 0 || results.length > 0)"
      class="absolute right-0 mt-2 w-full max-w-2xl bg-white rounded-lg shadow-lg border z-50"
    >
      <div v-if="loading" class="p-4 text-center text-gray-500">
        搜索中...
      </div>

      <div
        v-else-if="query.length < 2"
        class="p-4 text-center text-gray-500"
      >
        请输入至少2个字符
      </div>

      <div v-else-if="results.length === 0" class="p-8 text-center text-gray-500">
        未找到相关结果
      </div>

      <div v-else class="max-h-96 overflow-y-auto">
        <div
          v-for="(result, index) in results"
          :key="`${result.type}-${result.id}`"
          class="p-4 border-b hover:bg-gray-50 cursor-pointer"
          @click="handleResultClick(result)"
        >
          <div class="flex items-start gap-3">
            <!-- 类型图标 -->
            <div class="flex-shrink-0">
              <span
                :class="[
                  'px-2 py-1 text-xs rounded',
                  result.type === 'announcement'
                    ? 'bg-blue-100 text-blue-800'
                    : 'bg-green-100 text-green-800'
                ]"
              >
                {{ result.type === 'announcement' ? '公告' : '回复' }}
              </span>
            </div>

            <!-- 内容 -->
            <div class="flex-1 min-w-0">
              <h4 class="font-medium text-gray-900 truncate">
                {{ result.display_title }}
              </h4>
              <p class="text-sm text-gray-600 truncate">
                {{ result.display_content }}
              </p>
              <p v-if="result.announcement_title" class="text-xs text-gray-500 mt-1">
                公告：{{ result.announcement_title }}
              </p>
              <p class="text-xs text-gray-400 mt-1">
                {{ formatTime(result.created_at) }}
              </p>
            </div>

            <!-- 相关性 -->
            <div class="flex-shrink-0 text-xs text-gray-400">
              {{ Math.round(result.relevance * 100) }}% 匹配
            </div>
          </div>
        </div>
      </div>

      <!-- 查看更多 -->
      <div
        v-if="results.length > 0"
        class="p-3 bg-gray-50 border-t text-center"
      >
        <button
          @click="viewAllResults"
          class="text-sm text-blue-600 hover:text-blue-800"
        >
          查看全部结果
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useDebounceFn } from '@vueuse/core'
import api from '../api/client'

interface SearchResult {
  type: 'announcement' | 'response'
  id: number
  display_title: string
  display_content: string
  announcement_title?: string
  created_at: string
  relevance: number
}

const router = useRouter()

const query = ref('')
const isOpen = ref(false)
const loading = ref(false)
const results = ref<SearchResult[]>([])

// 防抖搜索
const search = useDebounceFn(async () => {
  if (query.value.length < 2) {
    results.value = []
    return
  }

  loading.value = true
  try {
    const response = await api.get('/search/all', {
      params: {
        q: query.value,
        limit: 10,
      },
    })
    results.value = response.data.results
  } catch (error) {
    console.error('搜索失败:', error)
    results.value = []
  } finally {
    loading.value = false
  }
}, 300)

// 监听查询变化
watch(query, () => {
  if (query.value.length >= 2) {
    isOpen.value = true
    search()
  } else {
    results.value = []
  }
})

const handleSearch = () => {
  if (query.value.length >= 2) {
    viewAllResults()
  }
}

const handleResultClick = (result: SearchResult) => {
  isOpen.value = false
  if (result.type === 'announcement') {
    router.push(`/announcement/${result.id}`)
  } else {
    router.push(`/announcement/${result.announcement_title || result.id}`)
  }
}

const viewAllResults = () => {
  // 跳转到搜索结果页面（可以创建专门的搜索页面）
  alert('搜索结果页面待实现')
  isOpen.value = false
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

// 点击外部关闭搜索结果
document.addEventListener('click', (e) => {
  const searchContainer = (e.target as HTMLElement).closest('.search-container')
  if (!searchContainer && isOpen.value) {
    isOpen.value = false
  }
})
</script>
