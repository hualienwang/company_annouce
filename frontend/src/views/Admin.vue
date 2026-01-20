<template>
  <div>
    <div class="mb-6 flex justify-between items-start">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">管理后台</h1>
        <p class="mt-2 text-gray-600">员工管理</p>
      </div>
      <router-link
        to="/docs"
        class="text-blue-600 hover:text-blue-800 text-sm font-medium"
      >
        📚 帮助文档
      </router-link>
    </div>

    <!-- 快捷操作 -->
    <div class="flex gap-4 mb-6">
      <button
        @click="showUserForm = true"
        class="w-full bg-green-600 text-white py-3 px-6 rounded-lg hover:bg-green-700 font-medium text-center"
      >
        👥 新增员工
      </button>
    </div>

    <!-- 创建员工表单 -->
    <div v-if="showUserForm" class="bg-white rounded-lg shadow-sm border p-6 mb-6">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-semibold text-gray-900">新增员工</h2>
        <button
          @click="showUserForm = false; resetUserForm()"
          class="text-gray-500 hover:text-gray-700"
        >
          ✕
        </button>
      </div>
      <form @submit.prevent="createUser" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            用户名 *
          </label>
          <input
            v-model="userForm.username"
            type="text"
            required
            class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
            placeholder="请输入用户名"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            真实姓名 *
          </label>
          <input
            v-model="userForm.full_name"
            type="text"
            required
            class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
            placeholder="请输入真实姓名"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            邮箱 *
          </label>
          <input
            v-model="userForm.email"
            type="email"
            required
            class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
            placeholder="请输入邮箱"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            密码 *
          </label>
          <input
            v-model="userForm.password"
            type="password"
            required
            minlength="6"
            class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
            placeholder="请输入密码（至少6位）"
          />
        </div>
        <div class="flex gap-2">
          <button
            type="submit"
            :disabled="userSubmitting"
            class="flex-1 bg-green-600 text-white py-2 px-6 rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
          >
            {{ userSubmitting ? '创建中...' : '确认创建' }}
          </button>
          <button
            type="button"
            @click="showUserForm = false; resetUserForm()"
            class="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
          >
            取消
          </button>
        </div>
      </form>
    </div>

    <!-- 发送邮件表单 -->
    <div v-if="showEmailForm" class="fixed inset-0 z-50 flex items-center justify-center" style="background-color: rgba(0,0,0,0.5)">
      <div class="bg-white rounded-lg shadow-lg p-6 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-semibold text-gray-900">发送邮件</h2>
          <button
            @click="showEmailForm = false; resetEmailForm()"
            class="text-gray-500 hover:text-gray-700 text-2xl"
          >
            ✕
          </button>
        </div>
        <form @submit.prevent="sendEmail" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              收件人
            </label>
            <input
              v-model="emailForm.to_email"
              type="email"
              required
              class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-gray-50"
              placeholder="请输入收件人邮箱"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              主题 *
            </label>
            <input
              v-model="emailForm.subject"
              type="text"
              required
              class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="请输入邮件主题"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              内容 *
            </label>
            <textarea
              v-model="emailForm.body"
              required
              rows="8"
              class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none"
              placeholder="请输入邮件内容"
            ></textarea>
          </div>
          <div class="flex gap-2">
            <button
              type="submit"
              :disabled="emailSubmitting"
              class="flex-1 bg-blue-600 text-white py-2 px-6 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
            >
              {{ emailSubmitting ? '发送中...' : '发送邮件' }}
            </button>
            <button
              type="button"
              @click="showEmailForm = false; resetEmailForm()"
              class="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              取消
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- 修改员工资料表单 -->
    <div v-if="showEditUserForm" class="fixed inset-0 z-50 flex items-center justify-center" style="background-color: rgba(0,0,0,0.5)">
      <div class="bg-white rounded-lg shadow-lg p-6 max-w-md w-full mx-4">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-semibold text-gray-900">修改员工资料</h2>
          <button
            @click="showEditUserForm = false; resetEditUserForm()"
            class="text-gray-500 hover:text-gray-700 text-2xl"
          >
            ✕
          </button>
        </div>
        <form @submit.prevent="updateUser" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              用户名 *
            </label>
            <input
              v-model="editUserForm.username"
              type="text"
              required
              class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="请输入用户名"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              真实姓名 *
            </label>
            <input
              v-model="editUserForm.full_name"
              type="text"
              required
              class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="请输入真实姓名"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              邮箱 *
            </label>
            <input
              v-model="editUserForm.email"
              type="email"
              required
              class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="请输入邮箱"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              角色
            </label>
            <select
              v-model="editUserForm.role"
              class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="user">员工</option>
              <option value="admin">管理员</option>
            </select>
          </div>
          <div class="flex gap-2">
            <button
              type="submit"
              :disabled="editUserSubmitting"
              class="flex-1 bg-blue-600 text-white py-2 px-6 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
            >
              {{ editUserSubmitting ? '保存中...' : '保存' }}
            </button>
            <button
              type="button"
              @click="showEditUserForm = false; resetEditUserForm()"
              class="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              取消
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- 员工列表 -->
    <div class="mb-8">
      <h2 class="text-xl font-semibold text-gray-900 mb-4">
        员工列表
        <span v-if="usersTotal > 0" class="text-sm font-normal text-gray-500 ml-2">
          共 {{ usersTotal }} 人
        </span>
      </h2>

      <div v-if="usersLoading" class="text-center py-8">
        <div class="text-gray-500">加载中...</div>
      </div>

      <div v-else-if="users.length === 0" class="text-center py-8 bg-white rounded-lg border">
        <div class="text-gray-500">暂无员工</div>
      </div>

      <div v-else class="bg-white rounded-lg shadow-sm border overflow-hidden">
        <table class="w-full">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">用户名</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">真实姓名</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">邮箱</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">角色</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">状态</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="user in users" :key="user.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                {{ user.username }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                {{ user.full_name }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                {{ user.email }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span
                  :class="[
                    'px-2 py-1 text-xs font-medium rounded',
                    user.role === 'admin' ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'
                  ]"
                >
                  {{ user.role === 'admin' ? '管理员' : '员工' }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span
                  :class="[
                    'px-2 py-1 text-xs font-medium rounded',
                    user.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  ]"
                >
                  {{ user.is_active ? '启用' : '禁用' }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2">
                <button
                  @click="toggleUserStatus(user)"
                  :disabled="user.role === 'admin'"
                  :class="[
                    user.is_active ? 'bg-orange-600 hover:bg-orange-700' : 'bg-green-600 hover:bg-green-700',
                    'text-white px-3 py-1 rounded font-medium text-xs',
                    user.role === 'admin' ? 'opacity-50 cursor-not-allowed' : ''
                  ]"
                  :title="user.is_active ? '禁用用户' : '审核通过'"
                >
                  {{ user.is_active ? '🚫 禁用' : '✅ 审核' }}
                </button>
                <button
                  @click="openEditUserForm(user)"
                  class="bg-gray-600 text-white px-3 py-1 rounded hover:bg-gray-700 font-medium text-xs"
                  title="修改资料"
                >
                  ✏️ 修改
                </button>
                <button
                  @click="openEmailForm(user)"
                  class="bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700 font-medium text-xs"
                  title="发送邮件"
                >
                  📧 Email
                </button>
                <button
                  @click="deleteUser(user.id)"
                  :disabled="user.role === 'admin'"
                  :class="[
                    'bg-red-600 text-white px-3 py-1 rounded font-medium text-xs',
                    user.role === 'admin' ? 'opacity-50 cursor-not-allowed' : 'hover:bg-red-700'
                  ]"
                >
                  🗑️ 删除
                </button>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- 分页 -->
        <div v-if="usersTotal > usersPerPage" class="px-6 py-4 bg-gray-50 border-t flex items-center justify-between">
          <div class="text-sm text-gray-700">
            显示第 {{ (usersCurrentPage - 1) * usersPerPage + 1 }} 到
            {{ Math.min(usersCurrentPage * usersPerPage, usersTotal) }} 条，
            共 {{ usersTotal }} 条
          </div>
          <div class="flex items-center gap-2">
            <button
              @click="changeUsersPage(usersCurrentPage - 1)"
              :disabled="usersCurrentPage === 1"
              class="px-3 py-1 text-sm border rounded hover:bg-white disabled:opacity-50 disabled:cursor-not-allowed"
            >
              上一页
            </button>
            <span class="text-sm text-gray-700">
              第 {{ usersCurrentPage }} / {{ usersTotalPages }} 页
            </span>
            <button
              @click="changeUsersPage(usersCurrentPage + 1)"
              :disabled="usersCurrentPage === usersTotalPages"
              class="px-3 py-1 text-sm border rounded hover:bg-white disabled:opacity-50 disabled:cursor-not-allowed"
            >
              下一页
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { authApi } from '../api/auth'
import type { User, UserCreate } from '../types'

const users = ref<User[]>([])
const usersTotal = ref(0)
const usersCurrentPage = ref(1)
const usersPerPage = ref(10)
const currentUser = ref<User | null>(null)
const usersLoading = ref(false)
const userSubmitting = ref(false)
const showUserForm = ref(false)
const showEmailForm = ref(false)
const emailSubmitting = ref(false)
const showEditUserForm = ref(false)
const editUserSubmitting = ref(false)

// 计算总页数
const usersTotalPages = computed(() => {
  return Math.ceil(usersTotal.value / usersPerPage.value)
})

const userForm = ref<UserCreate>({
  username: '',
  full_name: '',
  email: '',
  password: '',
})

const emailForm = ref({
  to_email: '',
  subject: '',
  body: '',
})

const editUserForm = ref({
  id: 0,
  username: '',
  full_name: '',
  email: '',
  role: 'user' as 'user' | 'admin',
})

const resetUserForm = () => {
  userForm.value = {
    username: '',
    full_name: '',
    email: '',
    password: '',
  }
}

const resetEmailForm = () => {
  emailForm.value = {
    to_email: '',
    subject: '',
    body: '',
  }
}

const resetEditUserForm = () => {
  editUserForm.value = {
    id: 0,
    username: '',
    full_name: '',
    email: '',
    role: 'user',
  }
}

const openEmailForm = (user: User) => {
  emailForm.value.to_email = user.email
  showEmailForm.value = true
}

const openEditUserForm = (user: User) => {
  editUserForm.value.id = user.id
  editUserForm.value.username = user.username
  editUserForm.value.full_name = user.full_name
  editUserForm.value.email = user.email
  editUserForm.value.role = user.role
  showEditUserForm.value = true
}

const updateUser = async () => {
  editUserSubmitting.value = true
  try {
    await authApi.updateUser(editUserForm.value.id, {
      username: editUserForm.value.username,
      full_name: editUserForm.value.full_name,
      email: editUserForm.value.email,
      role: editUserForm.value.role,
    })
    // 清空表单并关闭
    resetEditUserForm()
    showEditUserForm.value = false
    // 重新加载员工列表
    await loadUsers()
    alert('员工资料修改成功！')
  } catch (error: any) {
    console.error('修改员工资料失败:', error)
    const errorMessage = error.response?.data?.detail || error.message || '修改失败，请重试'
    alert(`修改失败: ${errorMessage}`)
  } finally {
    editUserSubmitting.value = false
  }
}

const sendEmail = async () => {
  emailSubmitting.value = true
  try {
    const response = await authApi.sendEmail(emailForm.value)
    console.log('邮件发送响应:', response)
    // 清空表单并关闭
    resetEmailForm()
    showEmailForm.value = false

    // 统一显示成功提示
    alert('邮件发送成功！')
  } catch (error: any) {
    console.error('发送邮件失败:', error)
    // 显示详细的错误信息
    const errorMessage = error.response?.data?.detail || error.message || '发送失败，请重试'
    alert(`发送失败: ${errorMessage}`)
  } finally {
    emailSubmitting.value = false
  }
}

const loadUsers = async () => {
  usersLoading.value = true
  try {
    console.log('[Admin.vue] 开始加载员工列表，页码:', usersCurrentPage.value)
    const response = await authApi.list({
      skip: (usersCurrentPage.value - 1) * usersPerPage.value,
      limit: usersPerPage.value,
    })
    console.log('[Admin.vue] 获取到员工列表:', response.users.length, '条，总数:', response.total)
    users.value = response.users
    usersTotal.value = response.total
  } catch (error) {
    console.error('加载员工失败:', error)
    users.value = []
    usersTotal.value = 0
  } finally {
    usersLoading.value = false
  }
}

// 切换页码
const changeUsersPage = (page: number) => {
  if (page < 1 || page > usersTotalPages.value) return
  usersCurrentPage.value = page
  loadUsers()
}

const createUser = async () => {
  userSubmitting.value = true
  try {
    await authApi.create(userForm.value)
    // 清空表单并关闭
    resetUserForm()
    showUserForm.value = false
    // 重新加载员工列表
    await loadUsers()
    alert('员工创建成功！')
  } catch (error) {
    console.error('创建员工失败:', error)
    alert('创建失败，请重试')
  } finally {
    userSubmitting.value = false
  }
}

const deleteUser = async (id: number) => {
  // 获取要删除的用户
  const userToDelete = users.value.find(u => u.id === id)

  // 禁止删除管理员
  if (userToDelete && userToDelete.role === 'admin') {
    alert('不能删除管理员账号！')
    return
  }

  if (!confirm('确定要删除此员工吗？删除后无法恢复！')) {
    return
  }
  try {
    await authApi.delete(id)

    // 检查是否需要跳转到上一页
    if (users.value.length === 1 && usersCurrentPage.value > 1) {
      usersCurrentPage.value = usersCurrentPage.value - 1
    }

    // 重新加载员工列表
    await loadUsers()
    alert('员工删除成功！')
  } catch (error) {
    console.error('删除失败:', error)
    alert('删除失败，请重试')
  }
}

const toggleUserStatus = async (user: User) => {
  // 禁止修改管理员状态
  if (user.role === 'admin') {
    alert('不能修改管理员账号！')
    return
  }

  const action = user.is_active ? '禁用' : '审核通过'
  if (!confirm(`确定要${action}用户"${user.full_name}"吗？`)) {
    return
  }

  try {
    await authApi.toggleStatus(user.id, !user.is_active)
    // 重新加载员工列表
    await loadUsers()
    alert(`${action}成功！`)
  } catch (error) {
    console.error(`${action}失败:`, error)
    alert(`${action}失败，请重试`)
  }
}

onMounted(() => {
  // 从localStorage获取当前用户信息
  const userStr = localStorage.getItem('user')
  if (userStr) {
    currentUser.value = JSON.parse(userStr)
  }
  loadUsers()
})
</script>
