# Render.com 部署方式选择指南

项目提供两种 Render.com 部署方式，可根据需求选择：

## 部署方式对比

| 特性 | Python 环境部署 (默认) | Docker 环境部署 (备选) |
|------|----------------------|---------------------|
| **配置文件** | `render.yaml` | `render-docker.yaml` |
| **环境类型** | env: python | env: docker |
| **构建时间** | 首次约 3-5 分钟 | 首次约 5-10 分钟 |
| **更新时间** | 约 1-3 分钟 | 约 3-5 分钟 |
| **环境一致性** | 依赖 Render 环境 | 完全一致 |
| **本地测试** | 需要手动配置依赖 | Docker 一致测试 |
| **镜像大小** | 不适用 | 约 500MB |
| **依赖管理** | Render 自动管理 | Dockerfile 管理 |
| **复杂度** | 简单 | 稍复杂 |

## 方式一：Python 环境部署（推荐新手）

### 优势
- 配置简单，开箱即用
- 无需 Docker 知识
- Render 自动管理依赖
- 首次部署更快

### 使用方法
1. 使用默认的 `render.yaml` 配置文件
2. 推送代码到 GitHub
3. 在 Render.com 创建 Web Service
4. Render 会自动使用 env: python 部署

### 文件配置
```yaml
services:
  - type: web
    name: announcement-system
    env: python
    runtime: "3.11"

    buildCommand: |
      pip install --upgrade pip &&
      pip install -r backend/requirements.txt &&
      cd frontend &&
      npm install &&
      npm run build &&
      cd ..

    startCommand: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

## 方式二：Docker 环境部署（推荐生产环境）

### 优势
- 环境完全一致（开发、测试、生产）
- 本地可完全模拟生产环境
- 更好的依赖管理
- 更高的安全性
- 支持版本回滚

### 使用方法

#### 方法 A：重命名配置文件（推荐）
```bash
mv render-docker.yaml render.yaml
git add render.yaml
git commit -m "Switch to Docker deployment"
git push
```

#### 方法 B：手动选择环境
1. 推送代码到 GitHub（保持 `render.yaml` 为 env: python）
2. 在 Render.com 创建 Web Service
3. 在 "Environment" 中选择 **"Docker"**
4. Render 会自动使用根目录的 `Dockerfile`

### 文件配置
```yaml
services:
  - type: web
    name: announcement-system
    env: docker

    # Render 会自动使用 Dockerfile
```

### Dockerfile 说明
```dockerfile
# 多阶段构建
阶段 1: 构建前端（Node.js 24-alpine）
阶段 2: 安装后端依赖（Python 3.12-slim）
阶段 3: 合并镜像（FastAPI + 静态文件）
```

## 本地测试对比

### Python 环境部署
```bash
# 需要手动安装依赖
pip install -r backend/requirements.txt
cd frontend && npm install && npm run build

# 启动服务
uvicorn backend.main:app --host 0.0.0.0 --port 10000
```

### Docker 环境部署
```bash
# 一键构建和运行
docker build -t announcement-system .
docker run -p 10000:10000 announcement-system
```

## 切换部署方式

### 从 Python 切换到 Docker
```bash
# 备份原配置
cp render.yaml render-python.yaml.bak

# 使用 Docker 配置
mv render-docker.yaml render.yaml

# 提交并推送
git add .
git commit -m "Switch to Docker deployment"
git push
```

### 从 Docker 切换到 Python
```bash
# 恢复 Python 配置
cp render-python.yaml.bak render.yaml

# 提交并推送
git add .
git commit -m "Switch to Python deployment"
git push
```

## 推荐选择

### 选择 Python 环境部署，如果：
- ✅ 你是新手，不熟悉 Docker
- ✅ 快速原型开发
- ✅ 测试环境部署
- ✅ 不需要本地完全模拟生产环境

### 选择 Docker 环境部署，如果：
- ✅ 生产环境部署
- ✅ 需要环境一致性
- ✅ 需要本地完全模拟生产
- ✅ 需要更好的依赖管理
- ✅ 团队协作，避免环境差异

## 常见问题

### Q: 可以两种方式都保留吗？
A: 可以！保持 `render.yaml` 为 Python 部署，`render-docker.yaml` 为 Docker 部署，根据需要切换使用。

### Q: 切换部署方式会影响已有部署吗？
A: 切换配置文件后，重新部署会使用新的方式。数据不会丢失（数据库是独立的）。

### Q: 哪种方式更稳定？
A: 两种方式都经过测试，都很稳定。Docker 方式在环境一致性方面更有优势。

### Q: 首次部署选哪个？
A: 新手推荐 Python 方式，快速上手。有经验者可以直接选择 Docker 方式。

## 相关文档

- [Render 部署指南](./RENDER_DEPLOYMENT.md) - Python 部署详解
- [Docker 部署说明](./DOCKER_DEPLOYMENT_GUIDE.md) - Docker 部署详解
- [Render 快速参考](./RENDER_QUICKREF.md) - 快速部署参考
- [部署检查清单](./RENDER_CHECKLIST.md) - 部署前检查

---

**最后更新**: 2025-01-25
**文档版本**: 1.0.0
