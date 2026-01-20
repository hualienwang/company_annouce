import api from './client'
import type { User, UserCreate } from '../types'

export const authApi = {
  // 获取用户列表
  async list(params?: {
    skip?: number
    limit?: number
  }) {
    const response = await api.get<{
      total: number
      skip: number
      limit: number
      users: User[]
    }>('/auth/users', { params })
    return response.data
  },

  // 创建用户
  async create(data: UserCreate) {
    const response = await api.post('/auth/register', data)
    return response.data
  },

  // 删除用户
  async delete(id: number) {
    await api.delete(`/auth/users/${id}`)
  },

  // 更新用户角色
  async updateRole(id: number, role: 'admin' | 'user') {
    const response = await api.patch(`/auth/users/${id}/role`, { role })
    return response.data
  },

  // 切换用户状态
  async toggleStatus(id: number, is_active: boolean) {
    const response = await api.patch(`/auth/users/${id}/status`, null, {
      params: { is_active }
    })
    return response.data
  },

  // 发送邮件
  async sendEmail(data: {
    to_email: string
    subject: string
    body: string
  }) {
    const response = await api.post('/auth/send-email', data)
    return response.data
  },

  // 更新用户信息
  async updateUser(userId: number, data: {
    username?: string
    full_name?: string
    email?: string
    role?: 'admin' | 'user'
  }) {
    const response = await api.patch(`/auth/users/${userId}`, data)
    return response.data
  }
}
