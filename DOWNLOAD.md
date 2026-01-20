# 项目下载指南

## 快速下载

### 方式一：通过浏览器下载（推荐）

**当前服务运行在 http://localhost:5000**

1. 访问下载页面：`http://localhost:5000/download.html`
2. 点击"下载项目文件"按钮
3. 保存文件到本地（例如：`D:\develop\company-announcement-system.tar.gz`）
4. 使用 tar、WinRAR 或 7-Zip 解压文件

### 方式二：直接下载

如果后端服务正在运行，可以直接访问：
```
http://localhost:5000/project.tar.gz
```
浏览器会自动下载文件。

### 方式三：使用命令行下载

```bash
# Linux/Mac
curl -O http://localhost:5000/project.tar.gz

# Windows PowerShell
Invoke-WebRequest -Uri "http://localhost:5000/project.tar.gz" -OutFile "company-announcement-system.tar.gz"

# Windows (使用 wget, 需要先安装)
wget http://localhost:5000/project.tar.gz -O company-announcement-system.tar.gz
```

## 本地解压

### Windows (使用 PowerShell)

```powershell
cd D:\develop
tar -xzf company-announcement-system.tar.gz
```

### Windows (使用命令提示符)

```cmd
cd D:\develop
tar -xzf company-announcement-system.tar.gz
```

### Windows (使用 WinRAR 或 7-Zip)

1. 右键点击 `company-announcement-system.tar.gz` 文件
2. 选择"解压到..."
3. 选择 `D:\develop` 目录
4. 点击"确定"

## 项目结构

解压后，项目结构如下：

```
company-announcement-system/
├── frontend/                 # Vue 3 前端项目
│   ├── src/                 # 源代码
│   ├── public/              # 静态资源
│   ├── package.json        # 依赖配置
│   └── vite.config.ts      # Vite 配置
├── backend/                 # FastAPI 后端项目
│   ├── api/                # API 路由
│   ├── models.py           # 数据模型
│   ├── database.py         # 数据库配置
│   ├── main.py             # 主应用入口
│   └── requirements.txt    # Python 依赖
├── docker-compose.yml       # Docker 编排配置
├── DOCKER_DEPLOYMENT.md    # Docker 部署文档
└── README.md               # 项目说明
```

## 快速开始

### 使用 Docker（推荐）

1. 安装 Docker Desktop for Windows
2. 在项目根目录执行：
   ```bash
   docker-compose up -d
   ```
3. 访问 `http://localhost:5000`

### 手动启动

#### 后端启动

```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 5001
```

#### 前端启动

```powershell
cd frontend
pnpm install
pnpm dev
```

访问 `http://localhost:5000`

## 默认账号

- 管理员账号：`admin`
- 管理员密码：`admin123`

## 详细文档

- [项目指南](docs/PROJECT_GUIDE.md) - 项目功能和使用说明
- [Docker 部署](DOCKER_DEPLOYMENT.md) - Docker 完整部署文档
- [数据库设置](docs/DATABASE_SETUP.md) - 数据库配置和迁移
- [邮件配置](docs/邮件发送配置说明.md) - 邮件服务配置

## 注意事项

1. 首次运行前，请确保已安装：
   - Python 3.12 或更高版本
   - Node.js 18 或更高版本
   - pnpm (使用 `npm install -g pnpm` 安装)

2. 开发环境使用 SQLite 数据库，无需额外配置

3. 生产环境建议使用 PostgreSQL，通过 Docker Compose 启动

4. 配置文件 `backend/.env.example` 提供了环境变量模板，请根据实际情况修改

## 技术栈

- **前端**：Vue 3、Vite、Tailwind CSS、Pinia
- **后端**：FastAPI、SQLModel、PostgreSQL
- **部署**：Docker、Nginx

## 获取帮助

如遇到问题，请查看：
- [故障排查](DOCKER_DEPLOYMENT.md#故障排查)
- [常见问题](docs/PROJECT_GUIDE.md#常见问题)

---

**项目版本**：v1.0.0
**最后更新**：2025-01-09
