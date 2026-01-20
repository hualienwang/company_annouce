import api from './client'
import type { Response, ResponseCreate } from '../types'

export const responsesApi = {
  // 创建回复
  async create(data: ResponseCreate, file?: File) {
    const formData = new FormData()
    formData.append('announcement_id', data.announcement_id.toString())
    formData.append('colleague_name', data.colleague_name)
    formData.append('content', data.content)
    if (file) {
      formData.append('file', file)
    }

    const response = await api.post<Response>('/responses', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    
    return response.data
  },

  // 获取指定公告的回复
  async listByAnnouncement(
    announcementId: number,
    params?: { skip?: number; limit?: number }
  ) {
    const response = await api.get<Response[]>(
      `/responses/announcement/${announcementId}`,
      { params }
    )
    return response.data
  },

  // 获取指定同事的回复
  async listByColleague(
    colleagueName: string,
    params?: { skip?: number; limit?: number }
  ) {
    const response = await api.get<Response[]>(
      `/responses/colleague/${encodeURIComponent(colleagueName)}`,
      { params }
    )
    return response.data
  },

  // 获取所有回复
  async list(params?: { skip?: number; limit?: number }) {
    const response = await api.get<Response[]>('/responses', { params })
    return response.data
  },
}
