# 前端 Dockerfile - Vue3 + Vite 多阶段构建

# 阶段 1: 构建阶段
FROM node:24-alpine AS builder

# 设置工作目录
WORKDIR /app

# 复制 package.json 和 package-lock.json（如果存在）
COPY package.json package-lock.json* pnpm-lock.yaml* ./

# 安装 pnpm（如果使用 pnpm）或 npm
RUN npm install -g pnpm@latest && pnpm install || npm install

# 复制源代码
COPY . .

# 构建生产版本
RUN pnpm run build || npm run build

# 阶段 2: 生产阶段 - 使用 nginx 提供静态文件服务
FROM nginx:alpine

# 复制自定义 nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 从构建阶段复制构建产物
COPY --from=builder /app/dist /usr/share/nginx/html

# 暴露端口
EXPOSE 80

# 启动 nginx
CMD ["nginx", "-g", "daemon off;"]
