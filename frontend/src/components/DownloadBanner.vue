<template>
  <div
    style="
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 20px;
      border-radius: 12px;
      margin-bottom: 24px;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    "
  >
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
      <div>
        <h2 style="margin: 0 0 8px 0; font-size: 18px; font-weight: 600;">
          📦 下载完整项目源码
        </h2>
        <p style="margin: 0; opacity: 0.9; font-size: 14px;">
          包含完整的前端、后端代码和 Docker 部署配置
        </p>
      </div>
      <div style="display: flex; gap: 12px; flex-wrap: wrap;">
        <a
          href="/download.html"
          target="_blank"
          style="
            background: white;
            color: #667eea;
            padding: 12px 24px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            font-size: 14px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
          "
        >
          下载项目
        </a>
        <a
          href="/project.tar.gz"
          download="company-announcement-system.tar.gz"
          style="
            background: rgba(255, 255, 255, 0.2);
            color: white;
            padding: 12px 24px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            font-size: 14px;
            border: 2px solid white;
          "
        >
          直接下载 (147 KB)
        </a>
      </div>
    </div>
    <div style="margin-top: 16px; padding-top: 16px; border-top: 1px solid rgba(255, 255, 255, 0.2);">
      <p style="margin: 0; font-size: 13px; opacity: 0.8;">
        💡 提示：下载后解压到本地，参考 <a href="/docs/PROJECT_GUIDE.md" target="_blank" style="color: white; text-decoration: underline;">项目指南</a> 和 <a href="/DOCKER_DEPLOYMENT.md" target="_blank" style="color: white; text-decoration: underline;">Docker 部署文档</a>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
// 无需逻辑
</script>
