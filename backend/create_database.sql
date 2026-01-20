-- PostgreSQL 数据库初始化脚本
-- 如果需要手动创建数据库和表，可以使用此脚本

-- 1. 创建数据库（如果不存在）
-- 注意：执行此语句前需要连接到 PostgreSQL
CREATE DATABASE announcements
    ENCODING 'UTF8'
    LC_COLLATE = 'zh_CN.UTF-8'
    LC_CTYPE = 'zh_CN.UTF-8'
    TEMPLATE template0;

-- 连接到新创建的数据库
\c announcements

-- 2. 创建表（SQLModel 会自动创建，这里仅作参考）
-- announcements 表
CREATE TABLE IF NOT EXISTS announcement (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    content TEXT NOT NULL,
    type VARCHAR NOT NULL DEFAULT 'announcement',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- responses 表
CREATE TABLE IF NOT EXISTS response (
    id SERIAL PRIMARY KEY,
    announcement_id INTEGER NOT NULL,
    colleague_name VARCHAR NOT NULL,
    content TEXT NOT NULL,
    file_key VARCHAR,
    file_name VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (announcement_id) REFERENCES announcement(id) ON DELETE CASCADE
);

-- 3. 创建索引（提高查询性能）
CREATE INDEX IF NOT EXISTS idx_announcement_created_at ON announcement(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_announcement_type ON announcement(type);
CREATE INDEX IF NOT EXISTS idx_response_announcement_id ON response(announcement_id);
CREATE INDEX IF NOT EXISTS idx_response_colleague_name ON response(colleague_name);
CREATE INDEX IF NOT EXISTS idx_response_created_at ON response(created_at DESC);

-- 4. 插入测试数据（可选）
-- 插入一条示例公告
INSERT INTO announcement (title, content, type)
VALUES ('欢迎使用公告系统', '这是第一条公告内容，欢迎使用本系统！', 'announcement');

-- 5. 查询验证
SELECT '数据库初始化完成！' AS status;
SELECT COUNT(*) AS announcement_count FROM announcement;
SELECT COUNT(*) AS response_count FROM response;
