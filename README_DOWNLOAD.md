# 如何下载本项目到本地

## 快速下载步骤

1. **访问下载页面**
   ```
   http://localhost:5000/download.html
   ```

2. **点击下载按钮**
   - 页面上有一个明显的"点击下载项目文件"按钮
   - 点击后会自动下载 `company-announcement-system.tar.gz` 文件

3. **解压到本地目录**
   - 下载完成后，将文件解压到你想要的目录
   - 例如：`D:\develop`

## Windows 环境下解压

### 使用 PowerShell
```powershell
cd D:\develop
tar -xzf company-announcement-system.tar.gz
```

### 使用命令提示符
```cmd
cd D:\develop
tar -xzf company-announcement-system.tar.gz
```

### 使用 WinRAR 或 7-Zip
1. 右键点击 `company-announcement-system.tar.gz`
2. 选择"解压到..."
3. 选择目标目录（例如 `D:\develop`）
4. 点击"确定"

## 直接下载链接

如果你想直接下载而不查看页面，可以访问：
```
http://localhost:5000/project.tar.gz
```

## 项目包含内容

解压后，项目包含：
- ✅ 完整的前端代码（Vue 3 + Vite）
- ✅ 完整的后端代码（FastAPI + SQLModel）
- ✅ Docker 部署配置文件
- ✅ 所有文档和使用说明
- ✅ 配置文件模板

## 下载后如何运行

详细的部署说明请查看项目中的：
- `DOCKER_DEPLOYMENT.md` - Docker 完整部署指南
- `README.md` - 项目概述和快速开始

## 技术支持

如果遇到问题，请：
1. 检查服务是否正常运行：`http://localhost:5000`
2. 查看相关文档：项目目录下的 `docs/` 文件夹
3. 确认下载的文件完整性：147 KB

---

**提示**：建议下载后立即验证文件完整性，确保下载过程中没有损坏。
