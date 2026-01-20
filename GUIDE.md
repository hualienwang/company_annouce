# 项目下载说明

## 📥 下载本项目

### 方式一：通过浏览器下载（推荐）

1. 确保服务正在运行（默认端口 5000）
2. 访问：`http://localhost:5000/download.html`
3. 点击"下载项目文件"按钮
4. 保存文件到本地

### 方式二：直接下载链接

直接访问：`http://localhost:5000/project.tar.gz`

### 方式三：命令行下载

```bash
# Linux/Mac
curl -O http://localhost:5000/project.tar.gz

# Windows PowerShell
Invoke-WebRequest -Uri "http://localhost:5000/project.tar.gz" -OutFile "company-announcement-system.tar.gz"
```

## 📦 解压项目

### Windows 环境

#### 使用 PowerShell
```powershell
cd D:\develop
tar -xzf company-announcement-system.tar.gz
```

#### 使用 WinRAR / 7-Zip
1. 右键点击 `company-announcement-system.tar.gz`
2. 选择"解压到..."
3. 选择目标目录（如 `D:\develop`）
4. 点击"确定"

### Linux / Mac 环境
```bash
tar -xzf company-announcement-system.tar.gz
```

## 🚀 快速开始

### 开发环境（手动启动）

#### 1. 安装后端依赖
```bash
cd backend
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
pip install -r requirements.txt
```

#### 2. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，配置数据库和邮件等信息
```

#### 3. 启动后端服务
```bash
cd backend
python -m uvicorn main:app --reload --port 5001
```

#### 4. 安装前端依赖
```bash
cd frontend
pnpm install
```

#### 5. 启动前端服务
```bash
cd frontend
pnpm dev
```

#### 6. 访问应用
打开浏览器访问：`http://localhost:5000`

### 生产环境（Docker 部署）

#### 1. 配置环境变量
```bash
cp .env.docker.example .env
# 编辑 .env 文件，填写 SMTP 配置等
```

#### 2. 启动所有服务
```bash
docker-compose up -d
```

#### 3. 访问应用
- 前端页面：`http://localhost`
- 后端 API：`http://localhost:8000/api`
- API 文档：`http://localhost:8000/docs`

## 📁 项目结构

```
company-announcement-system/
├── frontend/              # Vue 3 前端
│   ├── src/              # 源代码
│   ├── public/           # 静态资源
│   ├── package.json      # 依赖配置
│   └── vite.config.ts    # Vite 配置
├── backend/              # FastAPI 后端
│   ├── api/              # API 路由
│   ├── models.py         # 数据模型
│   ├── database.py       # 数据库配置
│   ├── main.py           # 主应用
│   └── requirements.txt  # Python 依赖
├── docker-compose.yml    # Docker 编排
├── DOCKER_DEPLOYMENT.md # Docker 部署文档
└── README.md            # 项目说明
```

## 🔑 默认账号

- 管理员用户名：`admin`
- 管理员密码：`admin123`

## 📚 详细文档

- [项目指南](docs/PROJECT_GUIDE.md) - 功能说明和使用教程
- [Docker 部署](DOCKER_DEPLOYMENT.md) - 完整的 Docker 部署文档
- [数据库设置](docs/DATABASE_SETUP.md) - 数据库配置和迁移
- [邮件配置](docs/邮件发送配置说明.md) - 邮件服务配置

## ⚠️ 注意事项

1. **前置要求**
   - Python 3.12+
   - Node.js 18+
   - pnpm（使用 `npm install -g pnpm` 安装）
   - PostgreSQL（生产环境，开发环境使用 SQLite）

2. **开发环境**
   - 使用 SQLite 数据库，无需额外配置
   - 文件存储在本地 `backend/file_uploads` 目录

3. **生产环境**
   - 使用 PostgreSQL 数据库（通过 Docker）
   - 推荐使用 S3 对象存储或挂载本地目录

4. **首次运行**
   - 首次运行会自动创建数据库
   - 管理员账号已预创建

## 🛠️ 常见问题

### Q1: 下载的文件解压失败？
A: 确保使用支持 `.tar.gz` 格式的解压工具（WinRAR、7-Zip 等）

### Q2: 后端启动失败？
A: 检查是否安装了所有依赖：`pip install -r requirements.txt`

### Q3: 前端无法连接后端？
A: 确认后端服务运行在 5001 端口，检查 CORS 配置

### Q4: 数据库连接错误？
A: 开发环境会自动创建 SQLite 数据库；生产环境需要配置 PostgreSQL

### Q5: 文件上传失败？
A: 检查 `backend/file_uploads` 目录权限和磁盘空间

## 💡 技术栈

- **前端**: Vue 3、Vite、Tailwind CSS、Pinia
- **后端**: FastAPI、SQLModel、PostgreSQL
- **部署**: Docker、Nginx
- **认证**: JWT (python-jose)
- **富文本**: Quill Editor

## 📞 获取帮助

如遇问题，请：
1. 查看项目文档
2. 检查后端日志：`tail -f backend.log`
3. 查看 Docker 日志：`docker-compose logs -f`

---

**项目版本**: v1.0.0  
**最后更新**: 2025-01-09
