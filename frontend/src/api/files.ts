import api from './client'

export const filesApi = {
  // 获取文件下载 URL
  async getDownloadUrl(fileKey: string) {
    const response = await api.get<{ success: boolean; url: string }>(
      '/file/download',
      { params: { key: fileKey } }
    )
    return response.data.url
  },

  // 下载文件
  async download(fileKey: string, fileName: string) {
    const url = await this.getDownloadUrl(fileKey)

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
      const response = await fetch(url)
      const blob = await response.blob()
      const blobUrl = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = blobUrl
      link.download = fileName
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(blobUrl)
    }
  },
}
