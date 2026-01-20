import api from './client'
import type { Announcement, AnnouncementCreate } from '../types'

export const announcementsApi = {
  // 获取公告列表
  async list(params?: {
    skip?: number
    limit?: number
    type?: 'announcement' | 'inquiry'
  }) {
    const response = await api.get<Announcement[]>('/announcements', { params })
    return response.data
  },

  // 获取公告详情
  async get(id: number) {
    const response = await api.get<Announcement & { responses: any[] }>(`/announcements/${id}`)
    return response.data
  },

  // 创建公告
  async create(data: AnnouncementCreate) {
    const response = await api.post<Announcement>('/announcements', data)
    return response.data
  },

  // 删除公告
  async delete(id: number) {
    await api.delete(`/announcements/${id}`)
  },
}
