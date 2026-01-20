# Docker 部署指南

## 目录结构

```
.
├── docker-compose.yml          # Docker Compose 配置文件
├── .env.docker.example        # 环境变量配置示例
├── frontend/
│   ├── Dockerfile             # 前端 Docker 镜像
│   ├── nginx.conf             # Nginx 配置
│   └── .dockerignore          # Docker 忽略文件
└── backend/
    ├── Dockerfile             # 后端 Docker 镜像
    └── .dockerignore          # Docker 忽略文件
```

## 前提条件

1. 安装 Docker 和 Docker Compose
2. 配置 SMTP 邮件服务（可选，用于邮件发送功能）

## 快速开始

### 1. 配置环境变量

复制环境变量示例文件并配置：

```bash
cp .env.docker.example .env
```

编辑 `.env` 文件，填写 SMTP 配置（如果需要邮件发送功能）：

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_FROM_EMAIL=your_email@gmail.com
```

### 2. 构建并启动服务

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 3. 访问应用

- **前端页面**: http://localhost
- **后端 API**: http://localhost:8000/api
- **API 文档**: http://localhost:8000/docs

## 服务说明

### PostgreSQL (数据库)
- 端口: 5432
- 用户名: postgres
- 密码: postgres
- 数据库名: announcements
- 数据持久化: `postgres_data` 卷

### Backend (FastAPI 后端)
- 端口: 8000
- 依赖: PostgreSQL
- 健康检查: `/health`
- 数据持久化: `./backend/file_uploads` 目录映射

### Frontend (Vue3 前端)
- 端口: 80
- 依赖: Backend
- 静态文件服务: Nginx

## 常用命令

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 停止服务并删除数据卷（⚠️ 会删除数据库数据）
docker-compose down -v

# 重启服务
docker-compose restart

# 查看日志
docker-compose logs -f backend
docker-compose logs -f frontend

# 进入后端容器
docker-compose exec backend bash

# 进入数据库容器
docker-compose exec postgres psql -U postgres -d announcements

# 重新构建并启动
docker-compose up -d --build

# 仅构建镜像
docker-compose build

# 仅启动后端
docker-compose up -d backend

# 仅启动前端
docker-compose up -d frontend
```

## 生产环境部署建议

### 1. 修改默认密码

修改 `docker-compose.yml` 中的 PostgreSQL 默认密码：

```yaml
environment:
  POSTGRES_USER: ${POSTGRES_USER:-admin}
  POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-your_strong_password}
  POSTGRES_DB: announcements
```

### 2. 配置数据持久化

确保数据库和文件上传目录正确挂载到宿主机：

```yaml
volumes:
  - postgres_data:/var/lib/postgresql/data  # 数据持久化

volumes:
  - ./backend/file_uploads:/app/file_uploads  # 文件上传持久化
```

### 3. 使用外部 PostgreSQL

如果使用云数据库服务，修改后端环境变量：

```yaml
backend:
  environment:
    DATABASE_URL: ${EXTERNAL_DATABASE_URL}
```

### 4. 启用 HTTPS

使用 Nginx 反向代理或 Let's Encrypt 证书：

```yaml
frontend:
  ports:
    - "443:443"
  volumes:
    - ./certs:/etc/nginx/certs
```

### 5. 配置健康检查和自动重启

已在 `docker-compose.yml` 中配置健康检查和自动重启策略：

```yaml
restart: unless-stopped
healthcheck:
  test: [...]
  interval: 30s
  timeout: 10s
  retries: 3
```

### 6. 项目下载文件

生产环境部署后，以下下载文件将自动可用：

- **下载页面**: `http://your-domain/download.html`
- **项目压缩包**: `http://your-domain/project.tar.gz`

这些文件包含完整的项目源码，方便用户下载后在本地运行或部署。

#### 构建时自动包含

在构建前端时，下载文件会自动复制到 dist 目录：

```bash
cd frontend
pnpm build  # 自动复制 download.html 和 project.tar.gz 到 dist/
```

#### 手动包含下载文件

如果需要手动更新下载文件：

```bash
# 更新项目压缩包
tar -czf frontend/public/project.tar.gz \
  --exclude='node_modules' \
  --exclude='frontend/node_modules' \
  --exclude='frontend/dist' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='.git' \
  .

# 重新构建前端
cd frontend
pnpm build
```

## 故障排查

### 1. 容器无法启动

```bash
# 查看详细日志
docker-compose logs backend
docker-compose logs frontend

# 检查容器状态
docker-compose ps
```

### 2. 数据库连接失败

确保 PostgreSQL 已启动并可访问：

```bash
docker-compose exec postgres psql -U postgres -d announcements
```

### 3. 前端无法访问后端 API

检查容器网络和端口映射：

```bash
docker-compose exec frontend wget -O- http://backend:8000/health
```

### 4. 文件上传失败

检查文件上传目录权限：

```bash
docker-compose exec backend ls -la /app/file_uploads
```

### 5. 邮件发送失败

检查 SMTP 配置和网络连接：

```bash
docker-compose exec backend python -c "import smtplib; smtplib.SMTP('smtp.gmail.com', 587)"
```

## 性能优化

### 1. 调整资源限制

```yaml
backend:
  deploy:
    resources:
      limits:
        cpus: '2'
        memory: 2G
      reservations:
        cpus: '1'
        memory: 1G
```

### 2. 使用 Nginx 缓存

已在 `frontend/nginx.conf` 中配置静态资源缓存：

```nginx
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### 3. 数据库优化

在 PostgreSQL 中创建索引并调整配置参数。

## 安全建议

1. 使用强密码和密钥
2. 定期更新基础镜像
3. 限制容器权限（避免使用 root 用户）
4. 配置防火墙规则
5. 启用 HTTPS
6. 定期备份数据库

## 备份和恢复

### 备份数据库

```bash
docker-compose exec postgres pg_dump -U postgres announcements > backup.sql
```

### 恢复数据库

```bash
docker-compose exec -T postgres psql -U postgres announcements < backup.sql
```

## 监控和日志

### 查看容器资源使用

```bash
docker stats
```

### 导出日志

```bash
docker-compose logs --since="1h" > logs.txt
```

## 更新部署

```bash
# 拉取最新代码
git pull

# 重新构建并启动
docker-compose up -d --build

# 清理未使用的镜像
docker image prune -a
```

## 支持和帮助

如有问题，请查看：
- Docker 文档: https://docs.docker.com
- Docker Compose 文档: https://docs.docker.com/compose
