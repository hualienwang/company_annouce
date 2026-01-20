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

    <div v-if="loading" class="text-center py-8">
      <div class="text-gray-500">加载中...</div>
    </div>

    <div v-else-if="announcement" class="space-y-6">
      <!-- 公告详情 -->
      <div class="bg-white rounded-lg shadow-sm border p-6">
        <div class="flex items-center gap-2 mb-4">
          <span
            :class="[
              'px-3 py-1 text-sm font-medium rounded',
              announcement.type === 'announcement'
                ? 'bg-blue-100 text-blue-800'
                : 'bg-purple-100 text-purple-800'
            ]"
          >
            {{ announcement.type === 'announcement' ? '公告' : '意见询问' }}
          </span>
          <span class="text-sm text-gray-500">
            {{ formatDate(announcement.created_at) }}
          </span>
        </div>
        <h1 class="text-3xl font-bold text-gray-900 mb-4">
          {{ announcement.title }}
        </h1>
        <div class="prose max-w-none text-gray-700 whitespace-pre-wrap">
          {{ announcement.content }}
        </div>

        <!-- 文件附件 -->
        <div v-if="announcement.file_name" class="mt-4 pt-4 border-t border-gray-200">
          <div class="flex items-center gap-2 text-gray-600 mb-2">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
            </svg>
            <span class="font-medium">附件</span>
          </div>
          <div class="inline-flex items-center gap-2 px-4 py-2 bg-gray-50 rounded-lg border border-gray-200">
            <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <span class="text-gray-700">{{ announcement.file_name }}</span>
            <button
              @click="downloadAnnouncementFile(announcement.file_key, announcement.file_name)"
              class="px-3 py-1 bg-blue-600 text-white text-sm rounded hover:bg-blue-700 transition-colors"
            >
              下载
            </button>
          </div>
        </div>
      </div>

      <!-- 回复列表 -->
      <div>
        <h2 class="text-xl font-semibold text-gray-900 mb-4">
          回复 ({{ totalResponses }})
        </h2>

        <div v-if="loadingResponses" class="text-center py-8 bg-white rounded-lg border">
          <div class="text-gray-500">加载中...</div>
        </div>

        <div v-else-if="responses.length === 0" class="text-center py-8 bg-white rounded-lg border">
          <div class="text-gray-500">暂无回复</div>
        </div>

        <div v-else class="space-y-4">
          <div
            v-for="response in responses"
            :key="response.id"
            class="bg-white rounded-lg shadow-sm border p-4"
          >
            <div class="flex justify-between items-start mb-2">
              <div class="flex items-center gap-2">
                <span class="font-medium text-gray-900">
                  {{ response.colleague_name }}
                </span>
                <span class="text-sm text-gray-500">
                  {{ formatDate(response.created_at) }}
                </span>
              </div>
              <RouterLink
                :to="`/responses/${encodeURIComponent(response.colleague_name)}`"
                class="text-sm text-blue-600 hover:text-blue-800"
              >
                查看该同事所有回复 →
              </RouterLink>
            </div>
            <p class="text-gray-700 mb-2">{{ response.content }}</p>
            <div v-if="response.file_key && response.file_name" class="mt-3">
              <button
                @click="downloadFile(response.file_key, response.file_name)"
                class="inline-flex items-center gap-1 px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded text-sm text-gray-700"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
                  />
                </svg>
                {{ response.file_name }}
              </button>
            </div>
            <div v-else-if="response.file_name && !response.file_key" class="mt-3">
              <div class="inline-flex items-center gap-1 px-3 py-1 bg-red-50 rounded text-sm text-red-600">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                  />
                </svg>
                {{ response.file_name }} (文件上传失败)
              </div>
            </div>
          </div>
        </div>

        <!-- 回复列表分页 -->
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

      <!-- 提交回复表单 -->
      <div class="bg-white rounded-lg shadow-sm border p-6">
        <h2 class="text-xl font-semibold text-gray-900 mb-4">提交回复</h2>
        <form @submit.prevent="submitResponse" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              姓名 *
            </label>
            <input
              v-model="form.colleague_name"
              type="text"
              required
              class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="请输入您的姓名"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              回复内容 *
            </label>
            <textarea
              v-model="form.content"
              required
              rows="4"
              class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="请输入回复内容"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              附件（可选）
            </label>
            <input
              ref="fileInput"
              type="file"
              class="w-full px-3 py-2 border rounded-lg"
              @change="handleFileChange"
            />
          </div>
          <button
            type="submit"
            :disabled="submitting"
            class="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ submitting ? '提交中...' : '提交回复' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { announcementsApi } from '../api/announcements'
import { responsesApi } from '../api/responses'
import { filesApi } from '../api/files'
import type { ResponseCreate } from '../types'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const announcement = ref<any>(null)
const loading = ref(false)
const submitting = ref(false)
const fileInput = ref<HTMLInputElement>()

// 回复列表分页
const responses = ref<any[]>([])
const loadingResponses = ref(false)
const currentPage = ref(1)
const pageSize = 10
const totalResponses = ref(0)

const totalPages = computed(() => Math.ceil(totalResponses.value / pageSize))

const form = ref<ResponseCreate>({
  announcement_id: Number(route.params.id),
  colleague_name: '',
  content: '',
})
const selectedFile = ref<File | undefined>()

const loadAnnouncement = async () => {
  loading.value = true
  try {
    announcement.value = await announcementsApi.get(Number(route.params.id))
    // 加载回复列表
    await loadResponses()
  } catch (error) {
    console.error('加载公告失败:', error)
  } finally {
    loading.value = false
  }
}

const loadResponses = async () => {
  loadingResponses.value = true
  try {
    responses.value = await responsesApi.listByAnnouncement(Number(route.params.id), {
      skip: (currentPage.value - 1) * pageSize,
      limit: pageSize,
    })
    // 获取总数（使用后端支持的最大limit）
    const allResponses = await responsesApi.listByAnnouncement(Number(route.params.id), {
      skip: 0,
      limit: 100,
    })
    totalResponses.value = allResponses.length
  } catch (error) {
    console.error('加载回复失败:', error)
  } finally {
    loadingResponses.value = false
  }
}

const goToPage = (page: number) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    loadResponses()
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

// 设置默认姓名为当前登录用户
const setDefaultName = () => {
  if (authStore.user?.full_name) {
    form.value.colleague_name = authStore.user.full_name
  }
}

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    selectedFile.value = target.files[0]
  }
}

const submitResponse = async () => {
  submitting.value = true
  try {
    await responsesApi.create(form.value, selectedFile.value)
    // 清空内容，保留姓名
    form.value.content = ''
    selectedFile.value = undefined
    if (fileInput.value) {
      fileInput.value.value = ''
    }
    // 重新加载第一页的回复
    currentPage.value = 1
    await loadResponses()
    alert('提交成功！')
    // 返回首页
    router.push('/')
  } catch (error) {
    console.error('提交回复失败:', error)
    alert('提交失败，请重试')
  } finally {
    submitting.value = false
  }
}

const downloadFile = async (fileKey: string, fileName: string) => {
  try {
    await filesApi.download(fileKey, fileName)
  } catch (error) {
    console.error('下载失败:', error)
    alert('下载失败，请重试')
  }
}

const downloadAnnouncementFile = async (fileKey: string, fileName: string) => {
  try {
    await filesApi.download(fileKey, fileName)
  } catch (error) {
    console.error('下载失败:', error)
    alert('下载失败，请重试')
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
  setDefaultName()
  loadAnnouncement()
})
</script>
