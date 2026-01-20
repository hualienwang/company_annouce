# 项目使用指南

## 项目概述

公司公告与意见收集系统，基于 **Vue3 + FastAPI + SQLModel + PostgreSQL** 技术栈开发。

### 技术选型

| 类别 | 技术栈 | 说明 |
|------|--------|------|
| 前端 | Vue 3 + Vite | 现代化前端框架 |
| 前端状态 | Pinia | Vue 官方状态管理 |
| 前端路由 | Vue Router | 单页应用路由 |
| 前端样式 | Tailwind CSS | 实用优先的 CSS 框架 |
| 后端 | FastAPI | 高性能 Python Web 框架 |
| ORM | SQLModel | 类型安全的 ORM（基于 Pydantic + SQLAlchemy） |
| 数据库 | PostgreSQL | 开源关系型数据库 |
| 文件存储 | S3 对象存储 | 可扩展的文件存储服务 |

---

## 功能特性

### 1. 公告管理
- ✅ 创建公告（普通公告 / 意见询问）
- ✅ 查看公告列表（支持类型筛选）
- ✅ 查看公告详情
- ✅ 删除公告（管理后台）

### 2. 回复功能
- ✅ 提交回复（支持文本 + 文件）
- ✅ 查看公告的所有回复
- ✅ 查看某同事的所有回复
- ✅ 文件上传到 S3
- ✅ 文件下载（签名 URL）

### 3. 分页功能
- ✅ 公告列表分页（每页 5 条）
- ✅ 同事回复分页（每页 5 条）
- ✅ 支持首页、上一页、下一页、末页导航

### 4. 管理后台
- ✅ 创建新公告
- ✅ 查看所有公告及回复
- ✅ 删除公告
- ✅ 下载回复附件

---

## 目录结构

```
.
├── .coze                          # 项目配置文件
├── .cozeproj/                     # 预置脚本
│   └── scripts/
│       ├── dev_run.sh            # 开发环境启动
│       ├── dev_stop.sh           # 停止服务
│       └── deploy_run.sh         # 部署环境启动
├── backend/                       # FastAPI 后端
│   ├── main.py                   # 应用入口
│   ├── database.py               # 数据库连接
│   ├── models.py                 # SQLModel 模型
│   ├── requirements.txt          # Python 依赖
│   ├── test_db_connection.py     # 数据库连接测试
│   ├── create_database.sql       # SQL 初始化脚本
│   ├── .env                      # 环境变量（需自行配置）
│   ├── api/                      # API 路由
│   │   ├── announcements.py      # 公告接口
│   │   ├── responses.py          # 回复接口
│   │   └── files.py              # 文件接口
│   └── utils/                    # 工具类
│       └── s3_storage.py         # S3 存储服务
├── frontend/                      # Vue3 前端
│   ├── index.html                # HTML 入口
│   ├── package.json              # Node 依赖
│   ├── vite.config.ts            # Vite 配置
│   ├── tsconfig.json             # TypeScript 配置
│   └── src/
│       ├── main.ts               # 应用入口
│       ├── App.vue               # 根组件
│       ├── router/               # 路由配置
│       │   └── index.ts
│       ├── api/                  # API 客户端
│       │   ├── client.ts
│       │   ├── announcements.ts
│       │   ├── responses.ts
│       │   └── files.ts
│       ├── views/                # 页面组件
│       │   ├── Home.vue          # 公告列表页
│       │   ├── AnnouncementDetail.vue  # 公告详情页
│       │   ├── Admin.vue         # 管理后台
│       │   └── ColleagueResponses.vue  # 同事回复页
│       ├── types/                # TypeScript 类型
│       │   └── index.ts
│       └── style.css             # 全局样式
├── docs/                         # 文档
│   ├── DATABASE_SETUP.md         # 数据库配置说明
│   └── DATABASE_OPERATIONS.md    # 数据库操作指南
├── setup.sh                      # 快速启动脚本
├── .gitignore                    # Git 忽略文件
└── README.md                     # 项目说明
```

---

## 快速开始

### 方式一：一键启动（推荐）

```bash
# 使用快速启动脚本
./setup.sh
```

脚本会自动执行：
1. ✅ 检查 Python 和 Node.js 环境
2. ✅ 安装后端 Python 依赖
3. ✅ 测试数据库连接
4. ✅ 安装前端 Node 依赖
5. ✅ 启动后端和前端服务

### 方式二：手动启动

#### 1. 配置环境变量

```bash
cd backend
cp .env.example .env
# 编辑 .env 文件，配置数据库连接
```

编辑 `backend/.env`：

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/announcements
COZE_BUCKET_ENDPOINT_URL=https://s3.example.com
COZE_BUCKET_NAME=your-bucket-name
```

#### 2. 测试数据库连接

```bash
cd backend
python test_db_connection.py
```

#### 3. 启动后端服务

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 5000
```

后端会自动创建数据库表，访问：
- API: http://localhost:5000
- 文档: http://localhost:5000/docs

#### 4. 启动前端服务（新终端）

```bash
cd frontend
npm install
npm run dev
```

前端会自动在浏览器打开：
- 地址: http://localhost:5173

---

## 数据库配置

### 使用集成数据库服务

如果您使用平台提供的 PostgreSQL 集成服务，数据库连接会自动配置。

### 本地 PostgreSQL 安装

如果需要在本地安装 PostgreSQL：

#### macOS
```bash
brew install postgresql@16
brew services start postgresql@16
createdb announcements
```

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo -u postgres createdb announcements
```

#### Windows
1. 下载并安装 PostgreSQL: https://www.postgresql.org/download/windows/
2. 使用 pgAdmin 创建数据库 `announcements`

---

## API 接口文档

### 公告接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/announcements` | 获取公告列表（支持分页、筛选） |
| POST | `/api/announcements` | 创建公告 |
| GET | `/api/announcements/{id}` | 获取公告详情（含回复） |
| DELETE | `/api/announcements/{id}` | 删除公告 |

**请求示例 - 创建公告**:
```bash
curl -X POST http://localhost:5000/api/announcements \
  -H "Content-Type: application/json" \
  -d '{
    "title": "测试公告",
    "content": "这是一条测试公告",
    "type": "announcement"
  }'
```

### 回复接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/responses` | 提交回复（支持文件上传） |
| GET | `/api/responses/announcement/{id}` | 获取公告的回复 |
| GET | `/api/responses/colleague/{name}` | 获取同事的回复 |
| GET | `/api/responses` | 获取所有回复 |

**请求示例 - 提交回复**:
```bash
curl -X POST http://localhost:5000/api/responses \
  -F "announcement_id=1" \
  -F "colleague_name=张三" \
  -F "content=这是回复内容" \
  -F "file=@document.pdf"
```

### 文件接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/file/download?key={key}` | 获取文件下载 URL（24小时有效） |

---

## 页面路由

| 路径 | 组件 | 说明 |
|------|------|------|
| `/` | Home | 公告列表（支持类型筛选、分页） |
| `/announcement/:id` | AnnouncementDetail | 公告详情（含回复列表、提交回复表单） |
| `/admin` | Admin | 管理后台（创建公告、删除公告、查看所有回复） |
| `/responses/:colleagueName` | ColleagueResponses | 同事的所有回复（支持分页） |

---

## 常见问题

### 1. 数据库连接失败

**错误信息**: `could not connect to server`

**解决方案**:
- 检查 `backend/.env` 中的 `DATABASE_URL` 是否正确
- 确认 PostgreSQL 服务已启动
- 验证数据库用户权限

### 2. 前端无法访问后端 API

**错误信息**: `Network Error` 或 `CORS Error`

**解决方案**:
- 确认后端服务在 5000 端口运行
- 检查 `frontend/vite.config.ts` 中的代理配置

### 3. 文件上传失败

**错误信息**: `S3 存储服务不可用`

**解决方案**:
- 确认 `coze-coding-dev-sdk` 已安装
- 检查 S3 环境变量配置是否正确

### 4. 页面显示异常

**解决方案**:
- 清除浏览器缓存
- 检查浏览器控制台是否有错误信息
- 重启前端服务：`cd frontend && npm run dev`

---

## 开发建议

### 后端开发

1. 使用 FastAPI 自动生成的 API 文档：http://localhost:5000/docs
2. 使用 `SQLModel` 的类型安全特性，减少运行时错误
3. 编写单元测试确保 API 稳定性

### 前端开发

1. 使用 Vue DevTools 调试组件状态
2. 遵循 Vue 3 Composition API 最佳实践
3. 使用 TypeScript 类型检查提高代码质量

---

## 部署

### 生产环境配置

1. 修改 `backend/.env` 使用生产数据库配置
2. 构建前端：`cd frontend && npm run build`
3. 使用 Gunicorn 或 uWSGI 启动后端
4. 使用 Nginx 反向代理前后端服务

### Docker 部署（可选）

可以创建 Dockerfile 和 docker-compose.yml 实现容器化部署。

---

## 更多文档

- [数据库配置说明](./DATABASE_SETUP.md)
- [数据库操作指南](./DATABASE_OPERATIONS.md)
- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [Vue 3 官方文档](https://vuejs.org/)
- [SQLModel 官方文档](https://sqlmodel.tiangolo.com/)

---

## 许可证

MIT License
