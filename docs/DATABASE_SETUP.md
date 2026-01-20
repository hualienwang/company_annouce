# PostgreSQL 数据库配置说明

## 数据库连接方式

本项目使用 PostgreSQL 作为数据库，通过环境变量 `DATABASE_URL` 配置连接。

### 环境变量格式

```
postgresql://用户名:密码@主机:端口/数据库名
```

### 默认配置

```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/announcements
```

---

## 数据库初始化

### 方式1: 自动初始化（推荐）

FastAPI 应用启动时会自动创建数据库表：

```python
@app.on_event("startup")
async def startup_event():
    """应用启动时初始化数据库"""
    init_db()
    print("数据库初始化完成")
```

### 方式2: 手动初始化

创建一个初始化脚本 `backend/init_db.py`：

```python
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.database import init_db

if __name__ == "__main__":
    init_db()
    print("数据库表创建成功！")
```

运行：

```bash
cd backend
python init_db.py
```

---

## 数据库表结构

### 1. announcements 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER (PK) | 主键，自增 |
| title | VARCHAR | 公告标题 |
| content | TEXT | 公告内容 |
| type | ENUM | 公告类型：announcement / inquiry |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

### 2. responses 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER (PK) | 主键，自增 |
| announcement_id | INTEGER (FK) | 关联公告 ID |
| colleague_name | VARCHAR | 同事姓名 |
| content | TEXT | 回复内容 |
| file_key | VARCHAR | 文件在 S3 中的键 |
| file_name | VARCHAR | 原始文件名 |
| created_at | TIMESTAMP | 创建时间 |

---

## 使用集成数据库服务

如果您使用的是平台提供的 PostgreSQL 集成服务，数据库连接会自动配置。

### 验证数据库连接

运行后端服务：

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

启动日志会显示：

```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:5000
数据库初始化完成
```

如果看到 "数据库初始化完成" 说明连接成功。

---

## 常见问题

### 1. 连接失败：could not connect to server

**原因**：数据库服务未启动或连接信息错误

**解决**：
- 检查 `DATABASE_URL` 环境变量是否正确
- 确认数据库服务已启动

### 2. 权限错误：permission denied

**原因**：用户名或密码错误

**解决**：
- 检查 `DATABASE_URL` 中的用户名和密码

### 3. 数据库不存在：database "announcements" does not exist

**原因**：数据库未创建

**解决**：
```bash
# 连接到 PostgreSQL
psql -U postgres

# 创建数据库
CREATE DATABASE announcements;

# 退出
\q
```

---

## SQL 示例

### 查询所有公告

```sql
SELECT * FROM announcements ORDER BY created_at DESC;
```

### 查询指定公告的回复

```sql
SELECT * FROM responses
WHERE announcement_id = 1
ORDER BY created_at DESC;
```

### 查询某同事的所有回复

```sql
SELECT r.*, a.title as announcement_title
FROM responses r
JOIN announcements a ON r.announcement_id = a.id
WHERE r.colleague_name = '张三'
ORDER BY r.created_at DESC;
```

---

## 数据备份与恢复

### 备份

```bash
pg_dump -U postgres announcements > backup.sql
```

### 恢复

```bash
psql -U postgres announcements < backup.sql
```
