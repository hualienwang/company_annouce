export interface Announcement {
  id: number
  title: string
  content: string
  type: 'announcement' | 'inquiry'
  file_key?: string
  file_name?: string
  created_at: string
  updated_at?: string
}

export interface AnnouncementCreate {
  title: string
  content: string
  type?: 'announcement' | 'inquiry'
}

export interface Response {
  id: number
  announcement_id: number
  colleague_name: string
  content: string
  file_key?: string
  file_name?: string
  created_at: string
  announcement_title?: string  // 可选字段，用于同事回复列表
}

export interface ResponseCreate {
  announcement_id: number
  colleague_name: string
  content: string
}

export interface User {
  id: number
  username: string
  email: string
  full_name: string
  role: 'admin' | 'user'
  is_active: boolean
  created_at: string
}

export interface UserCreate {
  username: string
  email: string
  password: string
  full_name: string
}
