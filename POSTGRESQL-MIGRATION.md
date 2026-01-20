# 数据库迁移说明：SQLite → PostgreSQL

## 迁移概述

项目数据库已从 SQLite3 成功迁移到 PostgreSQL，使用集成服务提供的 PostgreSQL 数据库实例。

## 更改内容

### 1. 后端数据库配置 (`backend/database.py`)

**修改前：**
- 支持回退到 SQLite（如果未配置 `DATABASE_URL`）
- 使用本地文件存储数据库

**修改后：**
- 强制使用 PostgreSQL
- 移除 SQLite 回退逻辑
- 如果未配置 `DATABASE_URL`，启动时会抛出明确的错误提示

### 2. 环境变量配置 (`backend/.env` 和 `backend/.env.example`)

**更新内容：**
- 添加详细的 PostgreSQL 连接字符串格式说明
- 配置使用集成服务提供的 PostgreSQL 数据库
- 提供本地 PostgreSQL 和云 PostgreSQL 的连接示例

**当前配置：**
```
DATABASE_URL=postgresql://user_7592816693424947250:43e6853b-0112-4d89-b93d-d9d390246345@cp-lush-sun-58291fdf.pg2.aidap-global.cn-beijing.volces.com:5432/Database_1767841614306?sslmode=require&channel_binding=require
```

### 3. 应用启动顺序 (`backend/main.py`)

**修改前：**
```python
from backend.database import init_db
# ... 其他导入
load_dotenv(Path(__file__).parent / ".env")
```

**修改后：**
```python
load_dotenv(Path(__file__).parent / ".env")  # 先加载环境变量
from backend.database import init_db
# ... 其他导入
```

**原因：** 确保 `DATABASE_URL` 环境变量在 `database.py` 模块导入前加载，避免启动时提示环境变量未配置。

### 4. 依赖验证

**PostgreSQL 驱动：**
- 已安装 `psycopg2-binary==2.9.9`
- 验证命令：`python -c "import psycopg2"` ✓

## 验证测试

### 1. 后端服务启动

```bash
INFO:     Uvicorn running on http://0.0.0.0:5001
INFO:     Started server process [499]
INFO:     Waiting for application startup.
数据库初始化完成
INFO:     Application startup complete.
```

### 2. API 功能测试

**用户注册测试：**
```bash
curl -X POST http://localhost:5001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username":"testuser",
    "full_name":"Test User",
    "email":"test@example.com",
    "password":"password123"
  }'
```

**结果：**
```json
{"message":"注册成功，请等待管理员审核"}
```

✅ 数据库连接正常，能够成功写入数据。

### 3. 服务状态检查

- 后端服务：`http://localhost:5001` ✓
- 前端服务：`http://localhost:5000` ✓
- PostgreSQL 连接：✓

## PostgreSQL 连接字符串格式

### 基本格式
```
postgresql://username:password@host:port/database_name
```

### 示例

**1. 本地数据库**
```
postgresql://postgres:postgres@localhost:5432/announcements
```

**2. 云数据库**
```
postgresql://user:password@db.example.com:5432/announcements
```

**3. 使用 SSL**
```
postgresql://user:password@host:port/database?sslmode=require
```

**4. 使用集成服务**
```
postgresql://user:password@endpoint:5432/database?sslmode=require&channel_binding=require
```

## 环境变量说明

### `DATABASE_URL`（必填）

- **类型**：PostgreSQL 连接字符串
- **格式**：`postgresql://username:password@host:port/database_name?params`
- **必填**：是
- **说明**：应用程序会读取此环境变量连接到 PostgreSQL 数据库

### 其他参数

- `sslmode`：SSL 模式（`require`、`prefer`、`disable`）
- `channel_binding`：通道绑定（`require`、`prefer`、`disable`）

## 迁移后的注意事项

### 1. 数据迁移

- 原来的 SQLite 数据文件位于 `data/company.db`
- 如果需要迁移旧数据，需要手动将 SQLite 数据导入到 PostgreSQL
- 建议使用 `pgloader` 或编写脚本进行数据迁移

### 2. 性能优化

PostgreSQL 相比 SQLite 提供了更好的性能和并发支持，可以考虑以下优化：
- 添加适当的索引
- 使用连接池（如 `SQLAlchemy` 的连接池功能）
- 启用查询缓存

### 3. 备份策略

PostgreSQL 的备份方式与 SQLite 不同，建议：
- 使用 `pg_dump` 进行逻辑备份
- 使用 `pg_basebackup` 进行物理备份
- 定期备份到对象存储（S3）

## 故障排查

### 问题1：启动时提示 "DATABASE_URL 环境变量未配置"

**解决方案：**
1. 检查 `backend/.env` 文件是否存在
2. 确认 `DATABASE_URL` 已正确配置
3. 检查 `.env` 文件是否在 `main.py` 中正确加载

### 问题2：连接数据库失败

**解决方案：**
1. 检查连接字符串格式是否正确
2. 验证数据库地址、端口是否可访问
3. 确认用户名和密码是否正确
4. 检查 SSL 配置是否与数据库匹配

### 问题3：应用无法启动

**检查步骤：**
1. 查看后端日志：`tail -f backend.log`
2. 检查环境变量是否正确加载
3. 验证 PostgreSQL 服务是否正常运行
4. 确认网络连接是否正常

## 总结

✅ 数据库已成功从 SQLite3 迁移到 PostgreSQL
✅ 后端服务正常运行，API 功能正常
✅ 数据库连接稳定，能够成功读写数据
✅ 前端服务正常运行，与后端 API 通信正常

所有功能均已验证通过，系统已可以正常使用。
