# 如何在无法访问 localhost 时下载项目

## 问题：无法访问 http://localhost:5000

如果浏览器显示 "localhost 拒绝连接"，可以尝试以下方法：

## 方法一：使用离线下载工具

1. 在沙箱中，找到文件：`/workspace/projects/frontend/public/download-offline.html`
2. 下载此文件到本地
3. 在浏览器中打开 `download-offline.html`
4. 按照页面提示下载项目

## 方法二：直接使用命令行下载

### Windows PowerShell
```powershell
cd D:\develop
Invoke-WebRequest -Uri "http://localhost:5000/project.tar.gz" -OutFile "company-announcement-system.tar.gz"
```

### Windows CMD
```cmd
cd D:\develop
curl -o company-announcement-system.tar.gz http://localhost:5000/project.tar.gz
```

### Linux / Mac
```bash
cd ~/Downloads
curl -O http://localhost:5000/project.tar.gz
```

## 方法三：从沙箱文件系统复制

项目压缩包位于以下位置：

1. `/workspace/projects/frontend/public/project.tar.gz`
2. `/workspace/projects/frontend/dist/project.tar.gz`

请使用沙箱的文件下载功能下载此文件。

## 方法四：手动创建项目

如果以上方法都无法使用，可以手动创建项目结构：

### 1. 创建项目目录
```bash
mkdir D:\develop\company-announcement-system
cd D:\develop\company-announcement-system
```

### 2. 创建后端目录和文件
```bash
mkdir backend
cd backend
```

创建以下文件（内容可以从当前沙箱中复制）：

- `main.py` - FastAPI 主应用
- `models.py` - 数据模型
- `database.py` - 数据库配置
- `requirements.txt` - Python 依赖
- `api/` - API 路由目录
  - `auth.py` - 认证相关
  - `announcements.py` - 公告相关
  - `responses.py` - 回复相关
  - 等等...

### 3. 创建前端目录和文件
```bash
cd ..
mkdir frontend
cd frontend
```

创建以下文件：

- `package.json` - Node.js 依赖配置
- `vite.config.ts` - Vite 配置
- `index.html` - 入口 HTML
- `src/` - 源代码目录
  - `App.vue` - 主组件
  - `main.ts` - 入口文件
  - 等等...

## 验证服务是否运行

在沙箱中执行以下命令：

```bash
# 检查端口
ss -tuln | grep :5000

# 测试服务
curl -I http://localhost:5000

# 查看服务日志
tail -50 /workspace/projects/backend.log
```

## 故障排查

如果服务正在运行但浏览器无法连接，请参考：[TROUBLESHOOTING.md](TROUBLESHOOTING.md)

常见原因：
1. 浏览器缓存问题 → 清除缓存，强制刷新（Ctrl+Shift+R）
2. 防火墙拦截 → 允许 Python 或 uvicorn 通过防火墙
3. 代理设置 → 禁用浏览器或系统代理
4. 扩展冲突 → 使用无痕模式访问

## 快速获取完整项目

最简单的方法是直接从沙箱下载项目压缩包：

**文件位置**：`/workspace/projects/frontend/public/project.tar.gz`  
**文件大小**：约 147 KB

使用沙箱的文件下载功能下载此文件，然后解压到本地。

## 联系支持

如果所有方法都无法使用，请提供以下信息：
- 操作系统版本
- 浏览器类型和版本
- 错误截图
- 已尝试的方法

---

**提示**：大多数情况下，使用命令行下载（方法二）是最可靠的方式。
