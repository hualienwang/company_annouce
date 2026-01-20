# 公司公告与意见收集系统 (Vue3 + FastAPI + SQLModel + PostgreSQL)

基于 Vue3 前端和 FastAPI 后端的公司内部公告和意见收集平台。

## 📥 下载项目

### 快速下载
访问应用首页：`http://localhost:5000`，点击顶部**"📥 下载项目"**链接或下载横幅即可下载完整项目源码。

详细下载说明请参考：[下载指南](DOWNLOAD_GUIDE.md)

## 功能特性

- ✅ 发布公告（普通公告、意见询问）
- ✅ 提交回复（支持文件上传）
- ✅ 查看公告及其回复
- ✅ 管理后台（删除公告、查看所有回复）
- ✅ 查看单一同事的所有回复
- ✅ 文件上传和下载（S3 对象存储）
- ✅ 分页功能（所有列表页）
- ✅ 类型筛选（公告/意见询问）
- ✅ 用户认证和权限管理
- ✅ 员工管理（新增、修改、删除、审核/禁用）
- ✅ 邮件发送功能（支持模拟模式和真实发送）
- ✅ 站内信通知

## 技术栈

### 后端
- **框架**: FastAPI
- **ORM**: SQLModel (基于 Pydantic + SQLAlchemy)
- **数据库**: PostgreSQL
- **文件存储**: S3 对象存储

### 前端
- **框架**: Vue 3
- **构建工具**: Vite
- **状态管理**: Pinia
- **UI 框架**: Tailwind CSS

## 功能特性

- 发布公告（普通公告、意见询问）
- 提交回复（支持文件上传）
- 查看公告及其回复
- 管理后台（删除公告、查看所有回复）
- 查看单一同事的所有回复
- 文件上传和下载
- 分页功能

## 项目结构

```
.
├── .coze                    # 项目配置
├── backend/                 # FastAPI 后端
│   ├── main.py             # 主应用入口
│   ├── requirements.txt    # Python 依赖
│   ├── database.py         # 数据库连接
│   ├── models.py           # SQLModel 模型
│   ├── api/                # API 路由
│   └── utils/              # 工具类
└── frontend/               # Vue3 前端
    ├── src/
    │   ├── main.ts
    │   ├── App.vue
    │   ├── components/    # 组件
    │   ├── views/         # 页面
    │   └── api/           # API 调用
    └── package.json
```

## 快速开始

### 1. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，配置数据库和 S3 存储信息
```

### 2. 配置邮件发送（可选）

系统默认使用**模拟模式**发送邮件（仅在控制台输出）。如需启用真实邮件发送，请查看：

- 📄 [邮件发送配置快速指南](docs/邮件发送配置快速指南.md) - 快速配置说明
- 📖 [邮件发送配置详细文档](docs/邮件发送配置说明.md) - 完整配置指南

**快速配置：**
```bash
# 在 .env 文件中添加以下配置
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_FROM_EMAIL=your_email@gmail.com
```

### 3. 测试数据库连接（推荐）

```bash
cd backend
python test_db_connection.py
```

### 4. 启动开发环境

**方式一：使用启动脚本（同时启动前后端）**
```bash
# 自动启动后端(5000端口)和前端(5173端口)
bash .cozeproj/scripts/dev_run.sh
```

**方式二：手动启动**

后端启动:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 5000
```

前端启动:
```bash
cd frontend
npm install
npm run dev
```

### 4. 访问应用

- 前端地址: http://localhost:5173
- 后端 API: http://localhost:5000
- API 文档: http://localhost:5000/docs
- 数据库表会自动创建

## 环境变量配置

### 数据库配置

在 `backend/.env` 文件中配置 PostgreSQL 连接：

```env
DATABASE_URL=postgresql://用户名:密码@主机:端口/数据库名
```

**默认配置**:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/announcements
```

### 文件存储配置

```env
COZE_BUCKET_ENDPOINT_URL=https://s3.example.com
COZE_BUCKET_NAME=your-bucket-name
```

### 测试数据库连接

```bash
cd backend
python test_db_connection.py
```

## 🚀 部署指南

项目提供两种 Render.com 部署方式，详见：[部署方式选择指南](./DEPLOYMENT_CHOICE.md)

### 方式一：Python 环境部署（默认，推荐新手）

适用于快速部署，配置简单，Render 自动管理依赖。

详细步骤请参考：[Render 部署指南](RENDER_DEPLOYMENT.md)

**快速部署：**
1. 将代码推送到 GitHub
2. 在 Render.com 创建 Web Service（会自动使用 env: python）
3. 配置 SMTP 环境变量
4. 访问应用

**访问地址：** `https://announcement-system.onrender.com`

### 方式二：Docker 环境部署（推荐生产环境）

适用于需要环境一致性和本地测试的场景。

详细步骤请参考：
- 📘 [Docker 部署说明](DOCKER_DEPLOYMENT_GUIDE.md) - Docker 部署详解
- 📖 [部署方式选择指南](DEPLOYMENT_CHOICE.md) - 两种方式对比

**快速部署：**
```bash
# 切换到 Docker 配置
mv render-docker.yaml render.yaml

# 推送代码
git add . && git commit -m "Switch to Docker" && git push
```

### Docker Compose 部署（自有服务器）

适用于服务器部署，使用 Docker Compose 一键部署。

详细步骤请参考：[Docker 部署指南](DOCKER_DEPLOYMENT.md)

**快速启动：**
```bash
docker-compose up -d
```

### 部署对比

| 部署方式 | 适用场景 | 优势 | 劣势 |
|---------|---------|------|------|
| **Render Python** | 云平台快速部署 | 配置简单，零维护 | 需要付费，依赖 Render 环境 |
| **Render Docker** | 云平台生产部署 | 环境一致，可本地测试 | 构建时间稍长 |
| **Docker Compose** | 自有服务器 | 完全控制，成本可控 | 需要维护服务器 |

## 📚 文档

- [部署方式选择指南](./DEPLOYMENT_CHOICE.md) - Python vs Docker 部署对比
- [下载指南](DOWNLOAD_GUIDE.md) - 如何下载和部署项目
- [Docker 部署指南](DOCKER_DEPLOYMENT.md) - Docker Compose 部署
- [Docker 部署说明](DOCKER_DEPLOYMENT_GUIDE.md) - Docker 部署详解
- [Render 部署指南](RENDER_DEPLOYMENT.md) - Render.com 云平台部署
- [Render 快速参考](RENDER_QUICKREF.md) - Render 快速部署参考
- [Render 部署检查清单](RENDER_CHECKLIST.md) - Render 部署前检查清单
- [故障排查指南](TROUBLESHOOTING.md) - 常见问题和解决方案
- [快速修复指南](QUICK_FIX.md) - 快速修复常见问题

## 🔧 工具和脚本

- [预部署检查脚本](./pre-deploy-check.sh) - 部署前自动检查项目配置

使用方法：
```bash
./pre-deploy-check.sh
```
