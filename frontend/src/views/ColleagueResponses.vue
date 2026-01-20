<template>
  <div>
    <button
      @click="router.back()"
      class="mb-4 text-gray-600 hover:text-gray-900 flex items-center gap-1"
    >
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
      </svg>
      返回
    </button>

    <div class="mb-6">
      <h1 class="text-3xl font-bold text-gray-900">
        {{ colleagueName }} 的回复
      </h1>
      <p class="mt-2 text-gray-600">
        查看该同事的所有回复记录 <span v-if="!loading && allData.length > 0" class="font-medium">（共 {{ allData.length }} 条）</span>
      </p>
    </div>

    <div v-if="loading" class="text-center py-8">
      <div class="text-gray-500">加载中...</div>
    </div>

    <div v-else-if="responses.length === 0" class="text-center py-12 bg-white rounded-lg border">
      <div class="text-gray-500">暂无回复</div>
    </div>

    <div v-else class="space-y-4">
      <div
        v-for="response in responses"
        :key="response.id"
        class="bg-white rounded-lg shadow-sm border p-4"
      >
        <div class="flex items-start justify-between">
          <div class="flex-1">
            <RouterLink
              :to="`/announcement/${response.announcement_id}`"
              class="text-sm font-medium text-gray-900 hover:text-blue-600"
            >
              {{ response.announcement_title }}
            </RouterLink>
            <div class="text-sm text-gray-500 mt-1">
              {{ formatDate(response.created_at) }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 分页 -->
    <div v-if="totalPages > 1" class="flex justify-center items-center gap-2 mt-8">
      <button
        @click="goToPage(1)"
        :disabled="currentPage === 1"
        class="px-3 py-1 rounded border disabled:opacity-50 disabled:cursor-not-allowed"
      >
        首页
      </button>
      <button
        @click="goToPage(currentPage - 1)"
        :disabled="currentPage === 1"
        class="px-3 py-1 rounded border disabled:opacity-50 disabled:cursor-not-allowed"
      >
        上一页
      </button>
      <span class="px-2">
        第 {{ currentPage }} / {{ totalPages }} 页
      </span>
      <button
        @click="goToPage(currentPage + 1)"
        :disabled="currentPage === totalPages"
        class="px-3 py-1 rounded border disabled:opacity-50 disabled:cursor-not-allowed"
      >
        下一页
      </button>
      <button
        @click="goToPage(totalPages)"
        :disabled="currentPage === totalPages"
        class="px-3 py-1 rounded border disabled:opacity-50 disabled:cursor-not-allowed"
      >
        末页
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { responsesApi } from '../api/responses'
import type { Response } from '../types'

const route = useRoute()
const router = useRouter()

const colleagueName = computed(() => decodeURIComponent(route.params.colleagueName as string))
const allData = ref<Response[]>([])
const responses = ref<Response[]>([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = 5
const totalPages = ref(0)

const loadResponses = async () => {
  loading.value = true
  try {
    console.log('[ColleagueResponses.vue] 开始加载回复列表，同事:', colleagueName.value)
    // 获取所有回复（客户端分页）
    const allResponses = await responsesApi.listByColleague(colleagueName.value, {
      limit: 100,  // 后端限制最大100条
    })
    console.log('[ColleagueResponses.vue] 获取到回复列表:', allResponses.length, '条')
    
    // 保存所有回复
    allData.value = allResponses
    
    // 计算总页数
    totalPages.value = Math.ceil(allData.value.length / pageSize)
    console.log('[ColleagueResponses.vue] 总数据:', allData.value.length, '总页数:', totalPages.value)
    
    // 计算当前页数据
    const start = (currentPage.value - 1) * pageSize
    const end = start + pageSize
    responses.value = allData.value.slice(start, end)
  } catch (error) {
    console.error('加载回复失败:', error)
    responses.value = []
    allData.value = []
    totalPages.value = 0
  } finally {
    loading.value = false
  }
}

const goToPage = (page: number) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    const start = (currentPage.value - 1) * pageSize
    const end = start + pageSize
    responses.value = allData.value.slice(start, end)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

onMounted(() => {
  loadResponses()
})
</script>
