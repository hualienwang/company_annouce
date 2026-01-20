# 多阶段 Dockerfile - 用于 Render.com 部署
# 构建前端 Vue3 应用，然后运行 FastAPI 后端并提供静态文件服务

# ========================================
# 阶段 1: 构建前端 (Vue3 + Vite)
# ========================================
FROM node:24-alpine AS frontend-builder

# 设置工作目录
WORKDIR /app/frontend

# 复制前端依赖文件
COPY frontend/package.json frontend/package-lock.json* ./frontend/

# 安装依赖
WORKDIR /app
RUN cd frontend && npm install

# 复制前端源代码
COPY frontend/ ./frontend/

# 构建前端生产版本
WORKDIR /app/frontend
RUN npm run build

# ========================================
# 阶段 2: 构建后端 (FastAPI + Python)
# ========================================
FROM python:3.12-slim AS backend-builder

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# 复制后端依赖文件
COPY backend/requirements.txt ./backend/

# 安装 Python 依赖
RUN pip install --upgrade pip && \
    pip install -r backend/requirements.txt

# ========================================
# 阶段 3: 生产环境 (FastAPI + 静态文件)
# ========================================
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# 从后端构建阶段复制已安装的 Python 依赖
COPY --from=backend-builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=backend-builder /usr/local/bin /usr/local/bin

# 复制后端应用代码
COPY backend/ ./backend/

# 从前端构建阶段复制构建产物
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# 创建文件上传目录
RUN mkdir -p /app/file_uploads

# 创建日志目录
RUN mkdir -p /app/logs

# 暴露端口（Render 会使用 PORT 环境变量）
EXPOSE 10000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:10000/health')" || exit 1

# 启动命令（使用 Render 提供的 PORT 环境变量）
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-10000}"]
