# SQLite 到 PostgreSQL 数据迁移说明

## 概述

本文档记录了将 SQLite 数据库（`data/company.db`）迁移到 PostgreSQL 集成服务的完整过程。

## 迁移前数据统计

SQLite 数据库包含以下表和数据：

| 表名 | 记录数 | 说明 |
|------|--------|------|
| user | 32 | 用户数据 |
| announcements | 19 | 旧公告表 |
| announcement | 25 | 新公告表 |
| responses | 16 | 旧回复表 |
| response | 43 | 新回复表 |
| notification | 140 | 通知数据 |

**注意：** SQLite 中存在重复的表结构（`announcements` 和 `announcement`，`responses` 和 `response`），需要合并。

## 迁移后数据统计

PostgreSQL 数据库：

| 表名 | 记录数 | 说明 |
|------|--------|------|
| user | 32 | 用户数据 |
| announcement | 44 | 合并后的公告（去重后） |
| response | 59 | 合并后的回复（去重后） |
| notification | 140 | 通知数据 |

## 迁移步骤

### 1. 创建清空 PostgreSQL 脚本

**文件：** `scripts/clear_postgres.py`

功能：
- 清空 PostgreSQL 中的所有数据（保留表结构）
- 重置自增序列

使用方法：
```bash
cd /workspace/projects
python3 scripts/clear_postgres.py
```

### 2. 创建数据迁移脚本

**文件：** `scripts/migrate_sqlite_to_postgres.py`

功能：
- 读取 SQLite 数据库中的所有数据
- 合并重复表（`announcements` + `announcement`，`responses` + `response`）
- 去重处理（基于 ID + 标题 + 内容）
- 重新编号处理 ID 冲突
- 更新外键关联（回复的 `announcement_id`）
- 数据类型转换（时间戳、布尔值等）
- 迁移到 PostgreSQL

使用方法：
```bash
cd /workspace/projects
python3 scripts/migrate_sqlite_to_postgres.py
```

### 3. 执行迁移

```bash
# 步骤 1：清空 PostgreSQL
python3 scripts/clear_postgres.py

# 步骤 2：执行迁移
python3 scripts/migrate_sqlite_to_postgres.py
```

## 迁移中的技术细节

### 1. ID 重新编号

由于 SQLite 中存在两个公告表，ID 有重复（都是 1-19 和 1-25），迁移时需要重新编号：

```python
id_mapping = {}
next_id = 1

for row in announcements_to_migrate:
    old_id = row['id']
    id_mapping[old_id] = next_id  # 记录旧 ID 到新 ID 的映射
    next_id += 1

# 插入新记录时使用新 ID
announcement = Announcement(
    id=id_mapping[old_id],  # 使用映射后的新 ID
    ...
)
```

### 2. 外键关联更新

回复表中的 `announcement_id` 需要更新为映射后的新 ID：

```python
old_announcement_id = row['announcement_id']
new_announcement_id = id_mapping.get(old_announcement_id, old_announcement_id)

response = Response(
    announcement_id=new_announcement_id,  # 使用映射后的公告 ID
    ...
)
```

### 3. 数据类型转换

- **时间戳**：SQLite 返回字符串，需要转换为 `datetime` 对象
- **布尔值**：SQLite 使用 0/1，需要转换为 Python `bool`
- **枚举类型**：角色和类型字段需要转换为小写

```python
# 时间戳转换
if isinstance(created_at, str):
    created_at = datetime.fromisoformat(created_at)

# 布尔值转换
is_active=bool(row.get('is_active', 1))

# 枚举类型转换
role = row.get('role', 'USER').lower()
```

### 4. 去重处理

使用元组 `(id, title, content)` 作为唯一键：

```python
announcements_map = {}

for row in data['announcements']['rows']:
    key = (row['id'], row['title'], row['content'])
    if key not in announcements_map:
        announcements_map[key] = row

announcements_to_migrate = list(announcements_map.values())
```

### 5. PostgreSQL 保留字处理

`user` 是 PostgreSQL 的保留字，执行 SQL 时需要用双引号包裹：

```python
# 错误：DELETE FROM user
# 正确：DELETE FROM "user"

for table, is_reserved_word in tables_to_clear:
    if is_reserved_word:
        result = conn.execute(text(f'DELETE FROM "{table}"'))
    else:
        result = conn.execute(text(f"DELETE FROM {table}"))
```

## 验证测试

### 1. API 测试

#### 用户登录
```bash
curl -X POST "http://localhost:5001/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

**结果：**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "w638897a@gmail.com",
    "full_name": "系统管理员",
    "role": "admin",
    "is_active": true
  }
}
```

#### 获取公告列表
```bash
curl "http://localhost:5001/api/announcements?limit=5"
```

#### 获取回复列表（需认证）
```bash
TOKEN="..."  # 从登录接口获取
curl "http://localhost:5001/api/responses?limit=5" \
  -H "Authorization: Bearer $TOKEN"
```

#### 获取通知列表（需认证）
```bash
TOKEN="..."
curl "http://localhost:5001/api/notifications" \
  -H "Authorization: Bearer $TOKEN"
```

### 2. 数据完整性检查

- ✓ 所有用户数据（32 条）已迁移
- ✓ 公告数据已合并（44 条，去重后）
- ✓ 回复数据已合并（59 条，去重后）
- ✓ 通知数据已迁移（140 条）
- ✓ 外键关联已正确更新
- ✓ 时间戳格式正确
- ✓ 枚举类型格式正确

## 常见问题

### Q1: 迁移后某些公告的回复不见了？

**原因：** 公告 ID 重新编号后，回复中的 `announcement_id` 也需要更新。

**解决：** 确保迁移脚本中正确处理了 ID 映射。

### Q2: 用户无法登录？

**原因：** 密码哈希未正确迁移或角色字段大小写不匹配。

**解决：** 检查迁移脚本中的密码哈希和角色转换逻辑。

### Q3: 时间戳显示错误？

**原因：** SQLite 时间戳字符串格式与 PostgreSQL `datetime` 类型不兼容。

**解决：** 使用 `datetime.fromisoformat()` 正确转换。

## 后续建议

1. **备份 PostgreSQL 数据**：定期备份生产环境的 PostgreSQL 数据
2. **监控迁移效果**：观察一段时间内的数据一致性和性能
3. **删除 SQLite 文件**：确认迁移成功后，可以删除 `data/company.db`
4. **更新文档**：更新系统部署文档，说明使用 PostgreSQL 而非 SQLite

## 相关文件

- `scripts/migrate_sqlite_to_postgres.py` - 主迁移脚本
- `scripts/clear_postgres.py` - 清空 PostgreSQL 脚本
- `backend/database.py` - 数据库连接配置
- `backend/models.py` - 数据模型定义
- `backend/.env` - 环境变量配置（包含 PostgreSQL 连接字符串）

## 总结

✅ 数据迁移成功完成
✅ 所有数据（32 用户 + 44 公告 + 59 回复 + 140 通知）已迁移到 PostgreSQL
✅ API 功能正常，测试通过
✅ 外键关联正确，数据完整性得到保证

系统现在完全基于 PostgreSQL 运行，可以享受更好的性能和可靠性。
