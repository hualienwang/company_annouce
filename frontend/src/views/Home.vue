<template>
  <div>
    <div style="margin-bottom: 1.5rem;">
      <h1 style="font-size: 1.875rem; font-weight: 700; color: #111827;">
        公司公告
      </h1>
      <p style="margin-top: 0.5rem; color: #4b5563;">
        查看最新的公司公告和意见询问
      </p>
    </div>

    <!-- 搜索框 -->
    <div style="margin-bottom: 1.5rem;">
      <div style="position: relative;">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="搜索公告或意见询问..."
          style="width: 100%; padding: 0.75rem 1rem 0.75rem 2.5rem; border: 1px solid #d1d5db; border-radius: 0.5rem; font-size: 0.875rem;"
        />
        <svg
          style="position: absolute; left: 0.75rem; top: 50%; transform: translateY(-50%); width: 1.25rem; height: 1.25rem; color: #9ca3af;"
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
    </div>

    <!-- 筛选按钮 -->
    <div style="display: flex; gap: 0.5rem; margin-bottom: 1.5rem;">
      <button
        @click="filterType = null"
        style="padding: 0.5rem 1rem; border-radius: 0.5rem; font-weight: 500; cursor: pointer; border: none;"
        :style="{
          backgroundColor: filterType === null ? '#2563eb' : 'white',
          color: filterType === null ? 'white' : '#374151'
        }"
      >
        全部
      </button>
      <button
        @click="filterType = 'announcement'"
        style="padding: 0.5rem 1rem; border-radius: 0.5rem; font-weight: 500; cursor: pointer; border: none;"
        :style="{
          backgroundColor: filterType === 'announcement' ? '#2563eb' : 'white',
          color: filterType === 'announcement' ? 'white' : '#374151'
        }"
      >
        公告
      </button>
      <button
        @click="filterType = 'inquiry'"
        style="padding: 0.5rem 1rem; border-radius: 0.5rem; font-weight: 500; cursor: pointer; border: none;"
        :style="{
          backgroundColor: filterType === 'inquiry' ? '#2563eb' : 'white',
          color: filterType === 'inquiry' ? 'white' : '#374151'
        }"
      >
        意见询问
      </button>
    </div>

    <!-- 管理员快捷操作 -->
    <div v-if="authStore.isAdmin" style="display: flex; gap: 0.5rem; margin-bottom: 1.5rem;">
      <button
        @click="showCreateForm = true; form.type = 'announcement'"
        style="padding: 0.5rem 1rem; border-radius: 0.5rem; font-weight: 500; cursor: pointer; border: none; background-color: #2563eb; color: white;"
      >
        ➕ 新增公告
      </button>
      <button
        @click="showCreateForm = true; form.type = 'inquiry'"
        style="padding: 0.5rem 1rem; border-radius: 0.5rem; font-weight: 500; cursor: pointer; border: none; background-color: #9333ea; color: white;"
      >
        💡 新增意见询问
      </button>
    </div>

    <!-- 创建公告表单 -->
    <div v-if="showCreateForm" style="background: white; border: 1px solid #e5e7eb; border-radius: 0.5rem; padding: 1.5rem; margin-bottom: 1.5rem;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
        <h2 style="font-size: 1.25rem; font-weight: 600; color: #111827;">
          {{ form.type === 'announcement' ? '创建新公告' : '创建意见询问' }}
        </h2>
        <button
          @click="showCreateForm = false; resetForm()"
          style="background: none; border: none; cursor: pointer; color: #6b7280; font-size: 1.25rem;"
        >
          ✕
        </button>
      </div>
      <form @submit.prevent="createAnnouncement" style="display: flex; flex-direction: column; gap: 1rem;">
        <div>
          <label style="display: block; font-size: 0.875rem; font-weight: 500; color: #374151; margin-bottom: 0.25rem;">
            标题 *
          </label>
          <input
            v-model="form.title"
            type="text"
            required
            style="width: 100%; padding: 0.5rem 0.75rem; border: 1px solid #d1d5db; border-radius: 0.375rem;"
            placeholder="请输入标题"
          />
        </div>
        <div>
          <label style="display: block; font-size: 0.875rem; font-weight: 500; color: #374151; margin-bottom: 0.25rem;">
            内容 *
          </label>
          <textarea
            v-model="form.content"
            required
            rows="6"
            style="width: 100%; padding: 0.5rem 0.75rem; border: 1px solid #d1d5db; border-radius: 0.375rem; resize: vertical;"
            placeholder="请输入内容"
          />
        </div>
        <div>
          <label style="display: block; font-size: 0.875rem; font-weight: 500; color: #374151; margin-bottom: 0.25rem;">
            附件
          </label>
          <input
            type="file"
            @change="handleFileChange"
            style="width: 100%; padding: 0.5rem 0.75rem; border: 1px solid #d1d5db; border-radius: 0.375rem;"
            accept=".pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx,.txt,.zip,.rar,.jpg,.jpeg,.png,.gif"
          />
          <div v-if="selectedFile" style="margin-top: 0.5rem; font-size: 0.875rem; color: #6b7280;">
            已选择文件: {{ selectedFile.name }} ({{ (selectedFile.size / 1024).toFixed(2) }} KB)
          </div>
        </div>
        <div style="display: flex; gap: 0.5rem;">
          <button
            type="submit"
            :disabled="submitting"
            style="flex: 1; padding: 0.5rem 1rem; border-radius: 0.375rem; font-weight: 500; cursor: pointer; border: none; background-color: #2563eb; color: white;"
            :style="{ opacity: submitting ? 0.5 : 1, cursor: submitting ? 'not-allowed' : 'pointer' }"
          >
            {{ submitting ? '创建中...' : '确认发布' }}
          </button>
          <button
            type="button"
            @click="showCreateForm = false; resetForm()"
            style="padding: 0.5rem 1rem; border: 1px solid #d1d5db; border-radius: 0.375rem; background: white; cursor: pointer; color: #374151;"
          >
            取消
          </button>
        </div>
      </form>
    </div>

    <!-- 加载中 -->
    <div v-if="loading" style="text-align: center; padding: 3rem; color: #6b7280;">
      加载中...
    </div>

    <!-- 空状态 -->
    <div v-else-if="!loading && displayedAnnouncements.length === 0" style="text-align: center; padding: 3rem; background: white; border-radius: 0.5rem; border: 1px solid #e5e7eb;">
      <div style="font-size: 3rem; margin-bottom: 1rem;">📭</div>
      <h3 style="font-size: 1.125rem; font-weight: 600; color: #111827; margin-bottom: 0.5rem;">
        暂无公告
      </h3>
      <p style="color: #6b7280;">
        {{ searchQuery ? '没有找到匹配的公告或意见询问' : (filterType === null ? '还没有任何公告或意见询问' : '没有' + (filterType === 'announcement' ? '公告' : '意见询问')) }}
      </p>
    </div>

    <!-- 公告列表 -->
    <div v-else>
      <div
        v-for="announcement in displayedAnnouncements"
        :key="announcement.id"
        style="background: white; border: 1px solid #e5e7eb; border-radius: 0.5rem; padding: 1.5rem; margin-bottom: 1rem; cursor: pointer; transition: box-shadow 0.2s;"
        @click="router.push(`/announcement/${announcement.id}`)"
      >
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.75rem;">
          <div style="display: flex; align-items: center; gap: 0.75rem; flex: 1;">
            <span
              style="padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600;"
              :style="{
                backgroundColor: announcement.type === 'announcement' ? '#dbeafe' : '#d1fae5',
                color: announcement.type === 'announcement' ? '#1e40af' : '#065f46'
              }"
            >
              {{ announcement.type === 'announcement' ? '公告' : '意见询问' }}
            </span>
            <h2 style="font-size: 1.25rem; font-weight: 600; color: #111827; margin: 0;">
              {{ announcement.title }}
            </h2>
            <button
              @click.stop="router.push(`/announcement/${announcement.id}#reply-form`)"
              style="background: #f3f4f6; border: 1px solid #e5e7eb; cursor: pointer; color: #6b7280; padding: 0.25rem 0.75rem; border-radius: 0.375rem; font-size: 0.75rem; font-weight: 500; transition: all 0.2s;"
              title="回复"
              @mouseover="$event.target.style.backgroundColor = '#dbeafe'; $event.target.style.color = '#2563eb'; $event.target.style.borderColor = '#93c5fd'"
              @mouseout="$event.target.style.backgroundColor = '#f3f4f6'; $event.target.style.color = '#6b7280'; $event.target.style.borderColor = '#e5e7eb'"
            >
              Answer
            </button>
          </div>
          <div style="display: flex; align-items: center; gap: 1rem;">
            <span style="font-size: 0.875rem; color: #6b7280;">
              {{ formatDate(announcement.created_at) }}
            </span>
            <button
              v-if="authStore.isAdmin"
              @click.stop="deleteAnnouncement(announcement.id, announcement.type)"
              style="background-color: #dc2626; color: white; padding: 0.375rem 0.75rem; border-radius: 0.375rem; font-size: 0.75rem; font-weight: 500; cursor: pointer; border: none;"
            >
              🗑️ 删除
            </button>
          </div>
        </div>

        <p style="color: #4b5563; margin-bottom: 1rem; overflow: hidden; text-overflow: ellipsis; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;">
          {{ announcement.content }}
        </p>

        <!-- 文件附件 -->
        <div v-if="announcement.file_name" style="margin-bottom: 1rem;">
          <div style="display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.5rem 0.75rem; background-color: #f3f4f6; border-radius: 0.375rem; border: 1px solid #e5e7eb;">
            <span style="font-size: 1.25rem;">📎</span>
            <span style="font-size: 0.875rem; color: #374151;">{{ announcement.file_name }}</span>
            <button
              @click.stop="downloadFile(announcement.file_key, announcement.file_name)"
              style="background-color: #2563eb; color: white; padding: 0.25rem 0.75rem; border-radius: 0.25rem; font-size: 0.75rem; font-weight: 500; cursor: pointer; border: none; margin-left: 0.5rem; transition: background-color 0.2s;"
              @mouseover="$event.target.style.backgroundColor = '#1d4ed8'"
              @mouseout="$event.target.style.backgroundColor = '#2563eb'"
            >
              下载
            </button>
          </div>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: center; padding-top: 1rem; border-top: 1px solid #f3f4f6;">
          <div style="display: flex; align-items: center; gap: 0.5rem; color: #6b7280; font-size: 0.875rem;">
            <span>👤 {{ announcement.author_name }}</span>
          </div>
          <div style="display: flex; align-items: center; gap: 1.5rem; font-size: 0.875rem; color: #6b7280;">
            <span>💬 {{ announcement.response_count || 0 }} 回复</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 分页 -->
    <div v-if="!loading && totalPages > 1" style="display: flex; justify-content: center; gap: 0.5rem; margin-top: 2rem;">
      <button
        @click="currentPage--"
        :disabled="currentPage === 1"
        style="padding: 0.5rem 1rem; border: 1px solid #d1d5db; border-radius: 0.375rem; background: white; cursor: pointer;"
        :style="{ opacity: currentPage === 1 ? 0.5 : 1 }"
      >
        上一页
      </button>
      <span style="padding: 0.5rem 1rem; color: #4b5563;">
        第 {{ currentPage }} / {{ totalPages }} 页
      </span>
      <button
        @click="currentPage++"
        :disabled="currentPage === totalPages"
        style="padding: 0.5rem 1rem; border: 1px solid #d1d5db; border-radius: 0.375rem; background: white; cursor: pointer;"
        :style="{ opacity: currentPage === totalPages ? 0.5 : 1 }"
      >
        下一页
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../api/client'
import { announcementsApi } from '../api/announcements'
import type { AnnouncementCreate } from '../types'

console.log('[Home.vue] 组件开始加载')

const router = useRouter()
const authStore = useAuthStore()

const loading = ref(true)
const searchQuery = ref('')
const filterType = ref<'announcement' | 'inquiry' | null>(null)
const currentPage = ref(1)
const pageSize = 5
const allData = ref<any[]>([])
const showCreateForm = ref(false)
const submitting = ref(false)
const selectedFile = ref<File | undefined>()

const form = ref<AnnouncementCreate>({
  title: '',
  content: '',
  type: 'announcement',
})

// 过滤后的数据
const filteredData = computed(() => {
  let data = allData.value

  // 搜索过滤
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase()
    data = data.filter(announcement =>
      announcement.title.toLowerCase().includes(query) ||
      announcement.content.toLowerCase().includes(query)
    )
  }

  // 类型过滤
  if (filterType.value) {
    data = data.filter(announcement => announcement.type === filterType.value)
  }

  return data
})

// 总页数
const totalPages = computed(() => Math.ceil(filteredData.value.length / pageSize))

// 当前页数据
const displayedAnnouncements = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  const end = start + pageSize
  return filteredData.value.slice(start, end)
})

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const loadAnnouncements = async () => {
  console.log('[Home.vue] 加载公告列表')
  loading.value = true
  try {
    const response = await api.get('/announcements', {
      params: { skip: 0, limit: 100 }
    })
    console.log('[Home.vue] 公告列表加载成功, 总数:', response.data.length)
    allData.value = response.data
  } catch (error) {
    console.error('[Home.vue] 加载公告列表失败:', error)
    allData.value = []
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  form.value = {
    title: '',
    content: '',
    type: 'announcement',
  }
  selectedFile.value = undefined
}

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    selectedFile.value = target.files[0]
  } else {
    selectedFile.value = undefined
  }
}

const createAnnouncement = async () => {
  submitting.value = true
  try {
    // 创建 FormData 对象
    const formData = new FormData()
    formData.append('title', form.value.title)
    formData.append('content', form.value.content)
    formData.append('type', form.value.type)

    // 如果选择了文件，添加到 FormData
    if (selectedFile.value) {
      formData.append('file', selectedFile.value)
    }

    // 使用 API 客户端发送 FormData 请求
    await api.post('/announcements', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
    })

    resetForm()
    showCreateForm.value = false
    await loadAnnouncements()
    alert(form.value.type === 'announcement' ? '公告发布成功！' : '意见询问发布成功！')
  } catch (error) {
    console.error('创建失败:', error)
    alert('创建失败，请重试')
  } finally {
    submitting.value = false
  }
}

const downloadFile = async (fileKey: string, fileName: string) => {
  if (!fileKey) {
    alert('文件不存在')
    return
  }

  try {
    // 获取下载 URL
    const response = await api.get('/file/download', {
      params: { key: fileKey }
    })

    if (response.data.success && response.data.url) {
      const url = response.data.url

      // 检查是否是本地文件（路径包含 /api/file/local/）
      if (url.includes('/api/file/local/')) {
        // 本地文件：添加 file_name 查询参数
        const separator = url.includes('?') ? '&' : '?'
        const downloadUrl = `${url}${separator}file_name=${encodeURIComponent(fileName)}`

        // 创建临时链接并下载
        const link = document.createElement('a')
        link.href = downloadUrl
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
      } else {
        // S3 签名 URL：使用 fetch + blob 方式下载
        const fetchResponse = await fetch(url)
        const blob = await fetchResponse.blob()
        const blobUrl = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = blobUrl
        link.download = fileName
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(blobUrl)
      }
    } else {
      alert('获取下载链接失败')
    }
  } catch (error) {
    console.error('下载文件失败:', error)
    alert('下载文件失败，请重试')
  }
}

const deleteAnnouncement = async (id: number, type: string) => {
  const typeName = type === 'announcement' ? '公告' : '意见询问'
  if (!confirm(`确定要删除此${typeName}吗？删除后无法恢复！`)) {
    return
  }
  try {
    await announcementsApi.delete(id)
    await loadAnnouncements()
    alert(`${typeName}删除成功！`)
  } catch (error) {
    console.error('删除失败:', error)
    alert('删除失败，请重试')
  }
}

// 监听搜索和筛选变化，重置到第一页
watch([searchQuery, filterType], () => {
  currentPage.value = 1
})

onMounted(() => {
  console.log('[Home.vue] onMounted 触发')
  loadAnnouncements()
})
</script>
