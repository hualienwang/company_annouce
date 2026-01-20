# Docker 部署说明

本文档详细说明如何使用 Docker 部署公司公告与意见收集系统到 Render.com。

## 为什么选择 Docker 部署？

### 优势

1. **环境一致性**
   - 开发环境、测试环境和生产环境完全一致
   - 避免"在我机器上能运行"的问题
   - 消除版本依赖冲突

2. **更好的依赖管理**
   - 所有依赖打包在 Docker 镜像中
   - 不会因系统更新导致服务中断
   - 便于版本回滚

3. **本地测试**
   - 可以在本地完全模拟生产环境
   - 无需安装复杂的依赖
   - 一键运行和停止

4. **快速部署**
   - Render 自动构建和推送镜像
   - 利用 Docker 层缓存加速构建
   - 支持蓝绿部署

5. **安全性**
   - 隔离运行环境
   - 最小化攻击面
   - 便于安全审计

## Dockerfile 结构

### 多阶段构建

我们的 Dockerfile 使用多阶段构建策略：

```
阶段 1: 前端构建 (Node.js 24-alpine)
  ├── 安装 npm 依赖
  ├── 复制源代码
  └── 构建前端 (npm run build)

阶段 2: 后端依赖安装 (Python 3.12-slim)
  ├── 安装系统依赖 (gcc, postgresql-client)
  └── 安装 Python 包 (pip install)

阶段 3: 生产镜像 (Python 3.12-slim)
  ├── 从阶段 2 复制 Python 依赖
  ├── 从阶段 1 复制前端构建产物
  ├── 复制后端源代码
  └── 启动 FastAPI 服务
```

### 关键设计决策

1. **多阶段构建**
   - 最终镜像只包含运行时需要的文件
   - 减小镜像大小（约 500MB）
   - 提高部署速度

2. **使用 alpine 镜像**
   - 更小的镜像大小
   - 更少的安全漏洞
   - 更快的启动时间

3. **环境变量配置**
   - 端口通过 `PORT` 环境变量配置
   - 支持本地测试和生产部署

4. **健康检查**
   - 内置健康检查机制
   - Render 自动监控服务状态
   - 自动重启失败的容器

## 本地测试

### 前置要求

- Docker 已安装（[下载地址](https://www.docker.com/get-started)）
- Docker Compose 已安装（可选）

### 测试步骤

1. **构建 Docker 镜像**

```bash
docker build -t announcement-system .
```

预期输出：
```
[+] Building 300.5s (12/12) FINISHED
 => => naming to docker.io/library/announcement-system
```

2. **运行 Docker 容器**

```bash
docker run -d \
  --name announcement-test \
  -p 10000:10000 \
  -e DATABASE_URL="postgresql://user:pass@host:5432/db" \
  -e SMTP_SERVER="smtp.gmail.com" \
  -e SMTP_PORT="587" \
  -e SMTP_USERNAME="your_email@gmail.com" \
  -e SMTP_PASSWORD="your_app_password" \
  -e SMTP_FROM_EMAIL="your_email@gmail.com" \
  -e FILE_STORAGE_TYPE="local" \
  -e FILE_UPLOAD_DIR="/app/file_uploads" \
  -v $(pwd)/file_uploads:/app/file_uploads \
  announcement-system
```

**参数说明：**
- `-d`: 后台运行
- `--name`: 容器名称
- `-p`: 端口映射（主机:容器）
- `-e`: 环境变量
- `-v`: 卷挂载（用于文件上传）

3. **查看日志**

```bash
docker logs -f announcement-test
```

4. **测试服务**

```bash
# 健康检查
curl http://localhost:10000/health

# 访问应用
open http://localhost:10000
```

5. **停止容器**

```bash
docker stop announcement-test
docker rm announcement-test
```

### 清理

```bash
# 删除容器
docker rm -f announcement-test

# 删除镜像
docker rmi announcement-system

# 删除所有未使用的镜像
docker image prune -a
```

## Render.com 部署

### 1. 推送代码到 GitHub

```bash
git add .
git commit -m "Update to Docker deployment"
git push origin main
```

### 2. 在 Render 创建服务

1. 访问 [dashboard.render.com](https://dashboard.render.com/)
2. New > Web Service > Connect GitHub
3. 选择仓库和分支
4. Render 会自动检测 `render.yaml` 和 `Dockerfile`
5. 点击 "Create Web Service"

### 3. 部署过程

Render 会自动执行以下步骤：

```
1. 拉取代码
   ↓
2. 构建 Docker 镜像
   ├─ 阶段 1: 构建前端 (约 2-3 分钟)
   ├─ 阶段 2: 安装后端依赖 (约 1-2 分钟)
   └─ 阶段 3: 合并镜像 (约 1 分钟)
   ↓
3. 推送镜像到容器注册表
   ↓
4. 运行容器
   ↓
5. 健康检查
   ↓
6. 完成部署
```

**总时间**: 首次约 5-10 分钟，后续约 3-5 分钟

### 4. 配置环境变量

在 Render Dashboard 中配置：

**必需配置：**
```
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_FROM_EMAIL=your_email@gmail.com
```

**可选配置：**
```
COZE_BUCKET_ENDPOINT_URL=https://s3.amazonaws.com
COZE_BUCKET_NAME=your-bucket-name
```

### 5. 验证部署

- 访问: https://announcement-system.onrender.com
- 检查: `/health` 端点返回 `{"status": "healthy"}`
- 测试: 注册用户、发布公告等核心功能

## 故障排查

### 构建失败

**问题**: Docker 构建失败

**原因**:
- 依赖安装失败
- 网络问题
- Dockerfile 语法错误

**解决方案**:
```bash
# 查看构建日志
docker build -t announcement-system . 2>&1 | tee build.log

# 单独测试前端构建
cd frontend
docker run --rm -v $(pwd):/app -w /app node:24-alpine npm install
docker run --rm -v $(pwd):/app -w /app node:24-alpine npm run build

# 单独测试后端依赖
cd backend
docker run --rm -v $(pwd):/app -w /app python:3.12-slim pip install -r requirements.txt
```

### 运行失败

**问题**: 容器启动失败

**原因**:
- 端口冲突
- 环境变量缺失
- 数据库连接失败

**解决方案**:
```bash
# 查看容器日志
docker logs announcement-test

# 进入容器调试
docker exec -it announcement-test bash

# 检查进程
docker exec announcement-test ps aux

# 测试网络
docker exec announcement-test ping google.com
```

### 健康检查失败

**问题**: 健康检查失败

**原因**:
- 服务未正常启动
- 健康检查端点错误
- 端口配置错误

**解决方案**:
```bash
# 手动测试健康检查
docker exec announcement-test curl http://localhost:10000/health

# 检查服务进程
docker exec announcement-test ps aux | grep uvicorn

# 查看环境变量
docker exec announcement-test env | grep PORT
```

## 性能优化

### 镜像优化

1. **减小镜像大小**
```dockerfile
# 使用多阶段构建（已实现）
# 使用 alpine 基础镜像（已实现）
# 清理不必要的文件
RUN apt-get clean && rm -rf /var/lib/apt/lists/*
```

2. **利用构建缓存**
```bash
# 排除不必要的文件
echo "node_modules/" >> .dockerignore
echo ".git/" >> .dockerignore
echo "*.log" >> .dockerignore
```

3. **并行构建**
```dockerfile
# Render 自动优化并行构建
# 多阶段构建利用 Docker 缓存
```

### 运行时优化

1. **资源限制**
```yaml
# render.yaml
plan: standard  # 2 CPU, 2GB 内存
```

2. **自动扩容**
```yaml
# Standard 计划及以上可用
autoscale:
  max_instances: 5
  min_instances: 1
  target_memory: 80  # 当内存使用超过 80% 时扩容
```

## 安全最佳实践

1. **使用环境变量**
   - 不要在代码中硬编码敏感信息
   - 使用 Render Dashboard 管理环境变量
   - 定期轮换密钥

2. **最小化镜像**
   - 只安装必要的依赖
   - 使用 alpine 基础镜像
   - 定期更新基础镜像

3. **扫描漏洞**
```bash
# 扫描镜像漏洞
docker scan announcement-system
```

4. **限制权限**
```dockerfile
# 不要以 root 用户运行
RUN useradd -m appuser
USER appuser
```

## 相关文档

- [Render 部署指南](./RENDER_DEPLOYMENT.md)
- [Render 快速参考](./RENDER_QUICKREF.md)
- [部署检查清单](./RENDER_CHECKLIST.md)
- [Docker 官方文档](https://docs.docker.com/)
- [Render Docker 文档](https://render.com/docs/deploy-docker-images)

---

**最后更新**: 2025-01-25
**文档版本**: 1.0.0
