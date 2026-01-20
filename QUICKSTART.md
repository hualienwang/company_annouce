# 快速开始指南

## 一键启动

```bash
./setup.sh
```

---

## 手动启动

### 1. 配置数据库

```bash
cd backend
cp .env.example .env
# 编辑 .env 文件，配置 DATABASE_URL
```

**数据库连接格式**:
```
postgresql://用户名:密码@主机:端口/数据库名
```

**默认配置**:
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/announcements
```

### 2. 测试数据库连接

```bash
cd backend
python test_db_connection.py
```

### 3. 启动服务

**方式一：使用启动脚本**
```bash
bash .cozeproj/scripts/dev_run.sh
```

**方式二：手动启动**

后端:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 5000
```

前端:
```bash
cd frontend
npm install
npm run dev
```

---

## 访问地址

- 前端: http://localhost:5173
- 后端 API: http://localhost:5000
- API 文档: http://localhost:5000/docs

---

## 停止服务

```bash
bash .cozeproj/scripts/dev_stop.sh
```

---

## 主要功能

| 功能 | 说明 |
|------|------|
| 发布公告 | 普通公告、意见询问 |
| 提交回复 | 支持文本 + 文件上传 |
| 查看回复 | 公告回复、同事所有回复 |
| 管理后台 | 创建/删除公告、查看所有回复 |
| 文件管理 | S3 对象存储、下载（24小时签名URL） |
| 分页 | 公告列表、同事回复 |

---

## 技术栈

- 前端: Vue 3 + Vite + Pinia + Tailwind CSS
- 后端: FastAPI + SQLModel
- 数据库: PostgreSQL
- 文件存储: S3 对象存储

---

## 详细文档

- [项目使用指南](./docs/PROJECT_GUIDE.md)
- [数据库配置说明](./docs/DATABASE_SETUP.md)
- [数据库操作指南](./docs/DATABASE_OPERATIONS.md)
