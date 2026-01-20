<template>
  <div class="file-preview-container">
    <button
      @click="openPreview"
      class="inline-flex items-center gap-1 px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded text-sm text-gray-700"
    >
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
        />
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
        />
      </svg>
      {{ fileName }}
    </button>

    <!-- 预览弹窗 -->
    <div
      v-if="isOpen"
      class="fixed inset-0 z-50 flex items-center justify-center"
      style="background-color: rgba(0, 0, 0, 0.9)"
    >
      <button
        @click="closePreview"
        class="absolute top-4 right-4 text-white hover:text-gray-300"
      >
        <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M6 18L18 6M6 6l12 12"
          />
        </svg>
      </button>

      <div class="w-full max-w-6xl max-h-[90vh] overflow-auto">
        <div v-if="loading" class="flex items-center justify-center h-full">
          <div class="text-white">加载中...</div>
        </div>

        <div v-else-if="previewUrl && previewType" class="preview-content">
          <!-- 图片预览 -->
          <div v-if="previewType === 'image'" class="flex justify-center">
            <img :src="previewUrl" class="max-w-full max-h-[80vh] object-contain" />
          </div>

          <!-- PDF 预览 -->
          <div v-else-if="previewType === 'pdf'" class="h-[80vh]">
            <iframe :src="previewUrl" class="w-full h-full" frameborder="0"></iframe>
          </div>

          <!-- 视频预览 -->
          <div v-else-if="previewType === 'video'" class="flex justify-center">
            <video :src="previewUrl" controls class="max-w-full max-h-[80vh]"></video>
          </div>

          <!-- 音频预览 -->
          <div v-else-if="previewType === 'audio'" class="flex justify-center p-8">
            <audio :src="previewUrl" controls class="w-full max-w-md"></audio>
          </div>

          <!-- 文本预览 -->
          <div v-else-if="previewType === 'text'" class="bg-white p-8 rounded">
            <iframe :src="previewUrl" class="w-full h-[80vh]"></iframe>
          </div>

          <!-- Office 文档提示 -->
          <div v-else-if="previewType === 'office'" class="text-center text-white p-8">
            <div class="text-6xl mb-4">📄</div>
            <h3 class="text-2xl font-bold mb-2">Office 文档</h3>
            <p class="mb-4">该文件类型不支持在线预览</p>
            <button
              @click="downloadFile"
              class="px-6 py-3 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              下载文件
            </button>
          </div>

          <!-- 压缩文件提示 -->
          <div v-else-if="previewType === 'archive'" class="text-center text-white p-8">
            <div class="text-6xl mb-4">📦</div>
            <h3 class="text-2xl font-bold mb-2">压缩文件</h3>
            <p class="mb-4">该文件类型不支持在线预览</p>
            <button
              @click="downloadFile"
              class="px-6 py-3 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              下载文件
            </button>
          </div>

          <!-- 未知类型 -->
          <div v-else class="text-center text-white p-8">
            <div class="text-6xl mb-4">❓</div>
            <h3 class="text-2xl font-bold mb-2">无法预览</h3>
            <p class="mb-4">该文件类型不支持在线预览</p>
            <button
              @click="downloadFile"
              class="px-6 py-3 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              下载文件
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import api from '../api/client'
import { filesApi } from '../api/files'

interface Props {
  fileKey: string
  fileName: string
}

const props = defineProps<Props>()

const isOpen = ref(false)
const loading = ref(false)
const previewUrl = ref('')
const previewType = ref('')

const openPreview = async () => {
  isOpen.value = true
  loading.value = true

  try {
    const response = await api.get('/file/preview', {
      params: { key: props.fileKey },
    })
    previewUrl.value = response.data.url
    previewType.value = response.data.preview_type
  } catch (error) {
    console.error('获取预览链接失败:', error)
    alert('获取预览链接失败')
    isOpen.value = false
  } finally {
    loading.value = false
  }
}

const closePreview = () => {
  isOpen.value = false
  previewUrl.value = ''
  previewType.value = ''
}

const downloadFile = async () => {
  try {
    await filesApi.download(props.fileKey, props.fileName)
  } catch (error) {
    console.error('下载失败:', error)
    alert('下载失败，请重试')
  }
}
</script>

<style scoped>
.preview-content :deep(iframe) {
  background-color: white;
  border-radius: 8px;
}
</style>
