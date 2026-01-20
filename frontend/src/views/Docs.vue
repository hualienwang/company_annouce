<template>
  <div class="max-w-4xl mx-auto p-6">
    <div class="mb-6">
      <h1 class="text-3xl font-bold text-gray-900">帮助文档</h1>
      <p class="mt-2 text-gray-600">系统使用说明和配置指南</p>
    </div>

    <!-- 邮件发送配置快速指南 -->
    <div class="bg-white rounded-lg shadow-sm border p-6 mb-6">
      <h2 class="text-2xl font-semibold text-gray-900 mb-4">
        📧 邮件发送配置快速指南
      </h2>

      <div class="prose prose-sm max-w-none text-gray-700 space-y-4">
        <section>
          <h3 class="text-lg font-semibold text-gray-900">当前状态：已配置</h3>
          <p class="text-sm">系统当前使用<strong>Gmail SMTP</strong>发送邮件，邮件会真实发送到收件人。</p>

          <div class="bg-green-50 border-l-4 border-green-400 p-4 mt-3">
            <p class="text-sm text-green-700"><strong>配置信息</strong></p>
            <ul class="list-disc list-inside text-sm text-green-600 mt-2 space-y-1">
              <li>SMTP 服务器：smtp.gmail.com</li>
              <li>端口：587 (TLS 加密)</li>
              <li>发件人邮箱：w638897a@gmail.com</li>
              <li>状态：✅ 正常工作</li>
            </ul>
          </div>
        </section>

        <section>
          <h3 class="text-lg font-semibold text-gray-900">快速配置（3 步）</h3>

          <div class="space-y-4">
            <div class="border rounded-lg p-4">
              <h4 class="font-medium text-gray-900">第 1 步：准备 SMTP 配置</h4>
              <p class="text-sm mt-1">以 Gmail 为例：</p>
              <code class="block bg-gray-100 p-2 rounded text-xs mt-2">
                SMTP_SERVER=smtp.gmail.com<br>
                SMTP_PORT=587<br>
                SMTP_USERNAME=your_email@gmail.com<br>
                SMTP_PASSWORD=your_app_password<br>
                SMTP_FROM_EMAIL=your_email@gmail.com
              </code>
            </div>

            <div class="border rounded-lg p-4">
              <h4 class="font-medium text-gray-900">第 2 步：设置环境变量</h4>
              <p class="text-sm mt-1">方式 A：使用 .env 文件</p>
              <code class="block bg-gray-100 p-2 rounded text-xs mt-1">
                cp .env.example .env<br>
                nano .env
              </code>
              <p class="text-sm mt-3">方式 B：直接设置环境变量</p>
              <code class="block bg-gray-100 p-2 rounded text-xs mt-1">
                export SMTP_USERNAME="your_email@gmail.com"<br>
                export SMTP_PASSWORD="your_app_password"<br>
                export SMTP_SERVER="smtp.gmail.com"<br>
                export SMTP_PORT="587"
              </code>
            </div>

            <div class="border rounded-lg p-4">
              <h4 class="font-medium text-gray-900">第 3 步：重启后端服务</h4>
              <p class="text-sm mt-1">重启后端服务使配置生效</p>
            </div>
          </div>
        </section>

        <section>
          <h3 class="text-lg font-semibold text-gray-900">常用 SMTP 配置</h3>

          <div class="space-y-3">
            <div class="border-l-4 border-green-400 bg-green-50 p-4">
              <h4 class="font-medium text-gray-900">Gmail</h4>
              <ul class="list-disc list-inside text-sm text-gray-700 mt-2 space-y-1">
                <li>SMTP_SERVER=smtp.gmail.com</li>
                <li>SMTP_PORT=587</li>
                <li>需要开启两步验证</li>
                <li>使用应用专用密码（<a href="https://myaccount.google.com/apppasswords" target="_blank" class="text-blue-600 hover:underline">获取应用专用密码</a>）</li>
              </ul>
            </div>

            <div class="border-l-4 border-blue-400 bg-blue-50 p-4">
              <h4 class="font-medium text-gray-900">163 邮箱</h4>
              <ul class="list-disc list-inside text-sm text-gray-700 mt-2 space-y-1">
                <li>SMTP_SERVER=smtp.163.com</li>
                <li>SMTP_PORT=465</li>
                <li>需要开启 POP3/SMTP 服务</li>
                <li>使用邮箱密码</li>
              </ul>
            </div>

            <div class="border-l-4 border-purple-400 bg-purple-50 p-4">
              <h4 class="font-medium text-gray-900">QQ 邮箱</h4>
              <ul class="list-disc list-inside text-sm text-gray-700 mt-2 space-y-1">
                <li>SMTP_SERVER=smtp.qq.com</li>
                <li>SMTP_PORT=587</li>
                <li>需要开启 POP3/IMAP/SMTP 服务</li>
                <li>使用授权码（邮箱设置 → 账户 → POP3/IMAP/SMTP）</li>
              </ul>
            </div>
          </div>
        </section>

        <section>
          <h3 class="text-lg font-semibold text-gray-900">使用邮件功能</h3>
          <ol class="list-decimal list-inside text-sm space-y-2 text-gray-700">
            <li>登录系统（管理员账号）</li>
            <li>访问管理后台（/admin）</li>
            <li>点击员工的"📧 Email"按钮</li>
            <li>填写邮件内容并发送</li>
          </ol>
        </section>

        <section>
          <h3 class="text-lg font-semibold text-gray-900">模拟模式 vs 真实模式</h3>
          <table class="min-w-full divide-y divide-gray-200 border text-sm">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-3 py-2 text-left text-gray-500 font-medium">特性</th>
                <th class="px-3 py-2 text-left text-gray-500 font-medium">模拟模式</th>
                <th class="px-3 py-2 text-left text-gray-500 font-medium">真实模式</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr>
                <td class="px-3 py-2 text-gray-700">配置难度</td>
                <td class="px-3 py-2 text-gray-700">无需配置</td>
                <td class="px-3 py-2 text-gray-700">需要 SMTP 配置</td>
              </tr>
              <tr>
                <td class="px-3 py-2 text-gray-700">邮件发送</td>
                <td class="px-3 py-2 text-gray-700">控制台输出</td>
                <td class="px-3 py-2 text-gray-700">真实发送</td>
              </tr>
              <tr>
                <td class="px-3 py-2 text-gray-700">适合场景</td>
                <td class="px-3 py-2 text-gray-700">开发测试</td>
                <td class="px-3 py-2 text-gray-700">生产环境</td>
              </tr>
            </tbody>
          </table>
        </section>

        <section>
          <h3 class="text-lg font-semibold text-gray-900">故障排除</h3>

          <div class="space-y-3">
            <div class="bg-red-50 border-l-4 border-red-400 p-4">
              <h4 class="font-medium text-gray-900">问题：邮件发送失败</h4>
              <p class="text-sm text-gray-700 mt-2"><strong>检查清单：</strong></p>
              <ul class="list-disc list-inside text-sm text-gray-600 mt-1 space-y-1">
                <li>✅ 环境变量是否正确设置？</li>
                <li>✅ SMTP 用户名和密码是否正确？</li>
                <li>✅ 网络是否能访问 SMTP 服务器？</li>
                <li>✅ 防火墙是否允许 SMTP 连接？</li>
              </ul>
              <p class="text-sm text-gray-700 mt-2"><strong>解决方法：</strong></p>
              <p class="text-sm text-gray-600 mt-1">运行测试脚本：<code class="bg-gray-100 px-1 py-0.5 rounded">python scripts/test_smtp.py</code></p>
            </div>

            <div class="bg-orange-50 border-l-4 border-orange-400 p-4">
              <h4 class="font-medium text-gray-900">问题：Gmail 认证失败</h4>
              <p class="text-sm text-gray-700 mt-2"><strong>错误信息：</strong> AuthenticationError</p>
              <p class="text-sm text-gray-600 mt-2"><strong>解决方法：</strong></p>
              <ul class="list-disc list-inside text-sm text-gray-600 mt-1 space-y-1">
                <li>确保已开启两步验证</li>
                <li>使用应用专用密码（<a href="https://myaccount.google.com/apppasswords" target="_blank" class="text-blue-600 hover:underline">获取</a>）</li>
                <li>不要使用 Gmail 账户密码</li>
              </ul>
            </div>
          </div>
        </section>
      </div>
    </div>

    <!-- 返回按钮 -->
    <div class="mt-6">
      <router-link
        to="/admin"
        class="inline-flex items-center text-blue-600 hover:text-blue-800 font-medium"
      >
        ← 返回管理后台
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
// 文档页面，无需额外逻辑
</script>

<style scoped>
.prose h3 {
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  font-weight: 600;
}

.prose p {
  margin-bottom: 0.75rem;
}

.prose code {
  background-color: #f3f4f6;
  padding: 0.125rem 0.25rem;
  border-radius: 0.25rem;
  font-size: 0.875rem;
}
</style>
