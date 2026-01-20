# 本地开发启动指南

本文档指导如何在本地环境启动公司公告与意见收集系统。

## 前置要求

### 必需软件

1. **Node.js** (推荐 18+)
   - 下载：https://nodejs.org/
   - 验证：`node --version`

2. **Python** (3.9+)
   - 下载：https://www.python.org/
   - 验证：`python --version` 或 `python3 --version`

3. **pnpm** (包管理器)
   - 安装：`npm install -g pnpm`
   - 验证：`pnpm --version`

4. **Git**
   - 下载：https://git-scm.com/
   - 验证：`git --version`

### 数据库（二选一）

**选项 1：本地 PostgreSQL（推荐）**
1. 下载：https://www.postgresql.org/download/
2. 安装后记住以下信息：
   - 端口：默认 5432
   - 用户名：默认 postgres
   - 密码：安装时设置

**选项 2：使用远程 PostgreSQL**
- 使用项目中的集成服务 PostgreSQL（无需本地安装）
- 连接信息在 `backend/.env` 中配置

## 项目结构

```
company-announcement-system/
├── backend/          # FastAPI 后端
│   ├── api/         # API 路由
│   ├── models.py    # 数据模型
│   ├── database.py  # 数据库连接
│   ├── main.py      # 应用入口
│   └── .env        # 环境变量配置（需创建）
├── frontend/        # Vue 3 前端
│   ├── src/         # 源代码
│   ├── public/      # 静态资源
│   ├── index.html   # 入口文件
│   └── vite.config.ts # Vite 配置
└── .gitignore      # Git 忽略文件
```

## 启动步骤

### 1. 克隆项目（如果从 GitHub 克隆）

```bash
git clone https://github.com/hualienwang/company-announcement-system.git
cd company-announcement-system
```

### 2. 安装前端依赖

```bash
cd frontend
pnpm install
```

如果遇到问题，尝试删除 `node_modules` 和 `pnpm-lock.yaml` 后重新安装：

```bash
rm -rf node_modules pnpm-lock.yaml
pnpm install
```

### 3. 安装后端依赖

```bash
cd backend
pip install -r requirements.txt
```

如果遇到权限问题，使用：

```bash
pip install -r requirements.txt --user
```

### 4. 配置环境变量

#### 创建 `backend/.env` 文件

在项目根目录创建 `backend/.env` 文件：

```bash
# PostgreSQL 数据库配置
DATABASE_URL=postgresql://postgres:你的密码@localhost:5432/announcements

# 或使用远程 PostgreSQL
# DATABASE_URL=postgresql://用户名:密码@主机:端口/数据库名

# S3 对象存储配置（可选）
COZE_BUCKET_ENDPOINT_URL=
COZE_BUCKET_NAME=

# SMTP 邮件发送配置（可选）
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=你的邮箱
SMTP_PASSWORD=你的应用专用密码
SMTP_FROM_EMAIL=你的邮箱
```

#### 配置 PostgreSQL

**创建数据库：**

使用 PostgreSQL 客户端工具（如 pgAdmin、psql）执行：

```sql
CREATE DATABASE announcements;
```

**或使用命令行：**

```bash
psql -U postgres
CREATE DATABASE announcements;
\q
```

### 5. 清理 Vite 缓存（如遇到依赖扫描错误）

如果启动前端时遇到以下错误：

```
ENOENT: no such file or directory, open '...node_modules/.vite/deps/pinia.js'
```

执行以下命令清理缓存：

```bash
cd frontend
rm -rf node_modules/.vite
```

### 6. 启动后端服务

**打开新的终端窗口：**

```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 5001 --reload
```

**看到以下输出表示启动成功：**

```
INFO:     Uvicorn running on http://0.0.0.0:5001
INFO:     Started server process [xxxx]
INFO:     Waiting for application startup.
数据库初始化完成
INFO:     Application startup complete.
```

**验证后端服务：**

在浏览器访问：http://localhost:5001/docs

应该看到 FastAPI 的 Swagger UI 文档页面。

### 7. 启动前端服务

**打开另一个新的终端窗口：**

```bash
cd frontend
pnpm dev
```

**看到以下输出表示启动成功：**

```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

**访问应用：**

在浏览器打开：http://localhost:5173

### 8. 登录系统

**默认管理员账号：**
- 用户名：`admin`
- 密码：`admin123`

首次登录后，建议修改默认密码。

## 常见问题解决

### 问题 1：Vite 依赖扫描失败

**错误信息：**
```
Failed to scan for dependencies from entries:
ENOENT: no such file or directory, open '...node_modules/.vite/deps/xxx.js'
```

**解决方法：**

```bash
cd frontend
rm -rf node_modules/.vite
pnpm dev
```

### 问题 2：后端连接数据库失败

**错误信息：**
```
psycopg2.OperationalError: connection to server at "localhost", port 5432 failed
```

**解决方法：**

1. 检查 PostgreSQL 是否正在运行
   - Windows: 打开服务管理器，查看 PostgreSQL 服务状态
   - Mac/Linux: `brew services list` 或 `systemctl status postgresql`

2. 检查 `backend/.env` 中的 `DATABASE_URL` 是否正确

3. 检查数据库是否存在
   ```bash
   psql -U postgres -l
   ```

### 问题 3：前端代理后端失败

**错误信息：**
```
[vite] http proxy error: /api/auth/login
AggregateError [ECONNREFUSED]
```

**解决方法：**

1. 确认后端服务正在运行（端口 5001）

2. 检查 `frontend/vite.config.ts` 中的代理配置
   ```typescript
   server: {
     proxy: {
       '/api': {
         target: 'http://localhost:5001',
         changeOrigin: true
       }
     }
   }
   ```

3. 重启前端服务

### 问题 4：端口被占用

**错误信息：**
```
OSError: [Errno 48] Address already in use
```

**解决方法：**

**Windows:**
```cmd
netstat -ano | findstr :5001
taskkill /PID <进程ID> /F
```

**Mac/Linux:**
```bash
lsof -ti:5001 | xargs kill -9
```

或使用其他端口：
```bash
python -m uvicorn main:app --port 5002
```

### 问题 5：bcrypt 版本兼容性错误

**错误信息：**
```
AttributeError: module 'bcrypt' has no attribute '__about__'
ValueError: password cannot be longer than 72 bytes
```

**问题原因：**
`passlib 1.7.4` 与新版 bcrypt（4.1+）不兼容

**解决方法：**

```bash
cd backend
pip install bcrypt==4.0.1
```

或重新安装所有依赖（`requirements.txt` 已添加 `bcrypt==4.0.1`）：

```bash
pip install -r requirements.txt
```

然后重启后端服务。

### 问题 6：Python 模块导入错误

**错误信息：**
```
ModuleNotFoundError: No module named 'sqlmodel'
```

**解决方法：**

```bash
cd backend
pip install -r requirements.txt
```

确保在正确的虚拟环境中（如果使用虚拟环境）。

### 问题 7：前端依赖安装失败

**错误信息：**
```
ERR_PNPM_REGISTRY_ERROR  Request failed
```

**解决方法：**

1. 切换到 npm 官方源
   ```bash
   pnpm config set registry https://registry.npmmirror.com
   ```

2. 或使用淘宝镜像
   ```bash
   pnpm config set registry https://registry.npmmirror.com
   ```

3. 重新安装依赖
   ```bash
   rm -rf node_modules pnpm-lock.yaml
   pnpm install
   ```

## 开发工具推荐

### 后端开发

- **PyCharm Professional** 或 **VS Code**
- **Postman** 或 **Insomnia**：测试 API
- **pgAdmin** 或 **DBeaver**：管理 PostgreSQL 数据库

### 前端开发

- **VS Code**：推荐使用 Volar 插件
- **Vue DevTools**：浏览器插件，调试 Vue 应用
- **ESLint** + **Prettier**：代码规范

## 生产环境部署

生产环境部署请参考以下文档：

- `DOCKER_DEPLOYMENT.md` - Docker 容器化部署
- `RENDER_DEPLOYMENT.md` - Render.com 云部署
- `DEPLOYMENT_CHOICE.md` - 部署方案选择指南

## 数据迁移

如果需要从 SQLite 迁移到 PostgreSQL，请参考：

`SQLITE-TO-POSTGRESQL-MIGRATION.md`

## 技术支持

遇到问题？

1. 查看本文档的"常见问题解决"部分
2. 检查后端日志（终端输出）
3. 检查前端控制台（浏览器 F12）
4. 查看 GitHub Issues：https://github.com/hualienwang/company-announcement-system/issues

## 快速启动总结

```bash
# 终端 1：启动后端
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 5001 --reload

# 终端 2：启动前端
cd frontend
pnpm install
rm -rf node_modules/.vite  # 如遇到依赖错误
pnpm dev

# 访问应用
# 前端：http://localhost:5173
# 后端 API：http://localhost:5001/docs
```

祝你开发愉快！🚀
