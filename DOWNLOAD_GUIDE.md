# 如何下载本项目

## 🎯 下载方式

### 方式一：从应用内下载（推荐）

1. 访问应用首页：`http://localhost:5000`
2. 在页面顶部会看到一个紫色的**"📦 下载完整项目源码"**横幅
3. 点击**"下载项目"**按钮会打开详细的下载页面
4. 点击**"直接下载"**按钮会直接下载项目压缩包

### 方式二：通过导航栏下载

1. 访问应用首页：`http://localhost:5000`
2. 点击导航栏右上角的**"📥 下载项目"**链接
3. 在打开的页面中点击下载按钮

### 方式三：直接访问下载页面

直接在浏览器中访问：`http://localhost:5000/download.html`

### 方式四：直接下载压缩包

直接访问下载链接：`http://localhost:5000/project.tar.gz`

## 📦 压缩包内容

下载的 `company-announcement-system.tar.gz` 文件（约 147 KB）包含：

- ✅ 完整的前端代码（Vue 3 + Vite）
- ✅ 完整的后端代码（FastAPI + SQLModel）
- ✅ Docker 部署配置文件
- ✅ 所有文档和使用说明
- ✅ 配置文件模板

## 💾 下载到本地

### Windows 环境

#### 使用 PowerShell
```powershell
# 切换到目标目录
cd D:\develop

# 下载文件
Invoke-WebRequest -Uri "http://localhost:5000/project.tar.gz" -OutFile "company-announcement-system.tar.gz"
```

#### 使用命令提示符
```cmd
# 切换到目标目录
cd D:\develop

# 使用 curl 下载（需要 Windows 10 或更高版本）
curl -o company-announcement-system.tar.gz http://localhost:5000/project.tar.gz
```

#### 直接在浏览器中下载
1. 访问 `http://localhost:5000/download.html`
2. 点击"下载项目文件"按钮
3. 选择保存位置（例如：`D:\develop`）

### Linux / Mac 环境
```bash
# 下载文件
curl -O http://localhost:5000/project.tar.gz

# 或使用 wget
wget http://localhost:5000/project.tar.gz
```

## 📂 解压项目

### Windows 环境

#### 使用 PowerShell
```powershell
cd D:\develop
tar -xzf company-announcement-system.tar.gz
```

#### 使用命令提示符
```cmd
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

## 🚀 下载后如何运行

详细的运行说明请参考解压后的文档：

- **快速开始**：`README.md`
- **项目指南**：`docs/PROJECT_GUIDE.md`
- **Docker 部署**：`DOCKER_DEPLOYMENT.md`

### 快速启动（开发环境）

#### 1. 后端启动
```bash
cd backend
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 5001
```

#### 2. 前端启动
```bash
cd frontend
pnpm install
pnpm dev
```

#### 3. 访问应用
打开浏览器：`http://localhost:5000`

## ✅ 下载验证

下载完成后，请验证文件大小：
- **预期大小**：约 147 KB
- **文件名**：`company-announcement-system.tar.gz`

解压后应该看到以下主要目录：
- `frontend/` - 前端代码
- `backend/` - 后端代码
- `docs/` - 文档目录
- `docker-compose.yml` - Docker 配置

## ❓ 常见问题

### Q1: 下载后文件损坏？
A: 重新下载，确保网络连接稳定，文件大小应该是 147 KB 左右。

### Q2: 解压失败？
A: 确保使用支持 `.tar.gz` 格式的解压工具（WinRAR、7-Zip、tar 等）。

### Q3: 找不到下载页面？
A: 确保服务正在运行（`http://localhost:5000`），如果服务停止，需要先启动服务。

### Q4: 下载速度很慢？
A: 项目压缩包只有 147 KB，如果下载速度很慢，可能是网络问题，可以稍后重试。

### Q5: 下载的项目和当前项目一样吗？
A: 是的，下载的压缩包包含完整的项目源码，和当前运行的项目完全一致。

## 📞 获取帮助

如遇到问题：
1. 检查服务是否运行：访问 `http://localhost:5000`
2. 查看项目文档：解压后的 `docs/` 目录
3. 检查文件完整性：确认下载的文件大小为 147 KB

---

**提示**：建议定期更新项目，下载最新的压缩包以获取最新的功能和修复。
