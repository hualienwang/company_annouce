# PostgreSQL 数据库操作指南

## 数据库表结构

### announcements (公告表)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INTEGER | PRIMARY KEY | 公告ID，自增 |
| title | VARCHAR | NOT NULL | 公告标题 |
| content | TEXT | NOT NULL | 公告内容 |
| type | VARCHAR | NOT NULL | 类型：'announcement' 或 'inquiry' |
| created_at | TIMESTAMP | NOT NULL | 创建时间 |
| updated_at | TIMESTAMP | - | 更新时间 |

### responses (回复表)

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | INTEGER | PRIMARY KEY | 回复ID，自增 |
| announcement_id | INTEGER | NOT NULL, FK | 关联公告ID |
| colleague_name | VARCHAR | NOT NULL | 同事姓名 |
| content | TEXT | NOT NULL | 回复内容 |
| file_key | VARCHAR | - | 文件在S3中的键 |
| file_name | VARCHAR | - | 原始文件名 |
| created_at | TIMESTAMP | NOT NULL | 创建时间 |

---

## 常用 SQL 查询

### 1. 公告相关查询

#### 查询所有公告（按创建时间倒序）
```sql
SELECT * FROM announcement
ORDER BY created_at DESC;
```

#### 查询指定类型的公告
```sql
SELECT * FROM announcement
WHERE type = 'announcement'
ORDER BY created_at DESC;
```

#### 查询最新 N 条公告
```sql
SELECT * FROM announcement
ORDER BY created_at DESC
LIMIT 10;
```

#### 按标题搜索公告
```sql
SELECT * FROM announcement
WHERE title LIKE '%关键词%'
ORDER BY created_at DESC;
```

---

### 2. 回复相关查询

#### 查询指定公告的所有回复
```sql
SELECT * FROM response
WHERE announcement_id = 1
ORDER BY created_at DESC;
```

#### 查询某同事的所有回复
```sql
SELECT * FROM response
WHERE colleague_name = '张三'
ORDER BY created_at DESC;
```

#### 查询某同事的回复统计
```sql
SELECT
    colleague_name,
    COUNT(*) as response_count,
    MAX(created_at) as latest_response
FROM response
GROUP BY colleague_name
ORDER BY response_count DESC;
```

#### 查询带附件的回复
```sql
SELECT * FROM response
WHERE file_key IS NOT NULL
ORDER BY created_at DESC;
```

---

### 3. 关联查询

#### 查询公告及其回复数量
```sql
SELECT
    a.id,
    a.title,
    a.type,
    COUNT(r.id) as response_count
FROM announcement a
LEFT JOIN response r ON a.id = r.announcement_id
GROUP BY a.id
ORDER BY a.created_at DESC;
```

#### 查询某同事的回复及关联的公告标题
```sql
SELECT
    r.id as response_id,
    r.colleague_name,
    r.content as response_content,
    r.created_at as response_time,
    a.id as announcement_id,
    a.title as announcement_title,
    a.type as announcement_type
FROM response r
JOIN announcement a ON r.announcement_id = a.id
WHERE r.colleague_name = '张三'
ORDER BY r.created_at DESC;
```

#### 查询意见询问及其回复
```sql
SELECT
    a.*,
    r.id as response_id,
    r.colleague_name,
    r.content as response_content
FROM announcement a
LEFT JOIN response r ON a.id = r.announcement_id
WHERE a.type = 'inquiry'
ORDER BY a.created_at DESC, r.created_at DESC;
```

---

### 4. 统计分析

#### 公告类型统计
```sql
SELECT
    type,
    COUNT(*) as count
FROM announcement
GROUP BY type;
```

#### 每日公告数量统计
```sql
SELECT
    DATE(created_at) as date,
    COUNT(*) as count
FROM announcement
GROUP BY DATE(created_at)
ORDER BY date DESC;
```

#### 每日回复数量统计
```sql
SELECT
    DATE(created_at) as date,
    COUNT(*) as count
FROM response
GROUP BY DATE(created_at)
ORDER BY date DESC;
```

#### 回复最多的公告 TOP 10
```sql
SELECT
    a.id,
    a.title,
    COUNT(r.id) as response_count
FROM announcement a
LEFT JOIN response r ON a.id = r.announcement_id
GROUP BY a.id, a.title
ORDER BY response_count DESC
LIMIT 10;
```

---

### 5. 数据维护

#### 清理指定时间之前的数据
```sql
-- 删除 30 天前的公告
DELETE FROM announcement
WHERE created_at < NOW() - INTERVAL '30 days';

-- 删除 30 天前的回复
DELETE FROM response
WHERE created_at < NOW() - INTERVAL '30 days';
```

#### 更新公告
```sql
UPDATE announcement
SET title = '新标题',
    content = '新内容',
    updated_at = NOW()
WHERE id = 1;
```

#### 删除公告（级联删除关联回复）
```sql
DELETE FROM announcement WHERE id = 1;
-- 注意：由于外键设置了 ON DELETE CASCADE，关联的回复会自动删除
```

---

### 6. 性能优化

#### 检查索引使用情况
```sql
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan as index_scans,
    idx_tup_read as tuples_read,
    idx_tup_fetch as tuples_fetched
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan DESC;
```

#### 分析表统计信息
```sql
ANALYZE announcement;
ANALYZE response;
```

#### 重建索引
```sql
REINDEX TABLE announcement;
REINDEX TABLE response;
```

---

### 7. 数据备份与恢复

#### 导出数据（备份）
```bash
# 仅导出数据
pg_dump -U postgres -d announcements -t announcement -t response > backup_data.sql

# 导出整个数据库
pg_dump -U postgres announcements > full_backup.sql
```

#### 导入数据（恢复）
```bash
# 恢复数据
psql -U postgres -d announcements < backup_data.sql

# 恢复整个数据库
psql -U postgres < full_backup.sql
```

---

### 8. 数据库连接信息

查看当前连接信息：
```sql
SELECT
    current_database() as database_name,
    current_user as user_name,
    inet_server_addr() as server_address,
    inet_server_port() as server_port,
    version() as postgres_version;
```

---

## 使用 Python 操作数据库

### 示例1: 创建公告
```python
from sqlmodel import Session, select
from backend.database import get_session
from backend.models import Announcement

def create_announcement(title: str, content: str, type: str = 'announcement'):
    with Session(engine) as session:
        announcement = Announcement(
            title=title,
            content=content,
            type=type
        )
        session.add(announcement)
        session.commit()
        session.refresh(announcement)
        return announcement
```

### 示例2: 查询公告
```python
from sqlmodel import Session, select
from backend.database import get_session
from backend.models import Announcement

def get_announcements(skip: int = 0, limit: int = 10):
    with Session(engine) as session:
        statement = (
            select(Announcement)
            .order_by(Announcement.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return session.exec(statement).all()
```

### 示例3: 统计回复
```python
from sqlmodel import Session, select, func
from backend.database import get_session
from backend.models import Announcement, Response

def get_response_statistics():
    with Session(engine) as session:
        statement = (
            select(
                Announcement.id,
                Announcement.title,
                func.count(Response.id).label('response_count')
            )
            .join(Response, Announcement.id == Response.announcement_id, isouter=True)
            .group_by(Announcement.id, Announcement.title)
            .order_by(func.count(Response.id).desc())
        )
        return session.exec(statement).all()
```

---

## 故障排查

### 检查表是否存在
```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public';
```

### 检查表结构
```sql
\d announcement
\d response
```

### 查看表大小
```sql
SELECT
    pg_size_pretty(pg_total_relation_size('announcement')) as size,
    pg_size_pretty(pg_relation_size('announcement')) as data_size,
    pg_size_pretty(pg_indexes_size('announcement')) as index_size;
```

### 查看活跃连接
```sql
SELECT
    pid,
    usename,
    application_name,
    client_addr,
    state,
    query_start,
    state_change,
    query
FROM pg_stat_activity
WHERE datname = 'announcements';
```
