#!/usr/bin/env python3
"""
添加文件字段到 announcement 表
"""
import sys
from pathlib import Path
from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# 加载环境变量
env_path = Path(__file__).parent.parent / "backend" / ".env"
load_dotenv(env_path)

def add_file_fields():
    """添加 file_key 和 file_name 字段到 announcement 表"""
    import os
    DATABASE_URL = os.getenv("DATABASE_URL")

    if not DATABASE_URL:
        print("错误: 未找到 DATABASE_URL 环境变量")
        return False

    # 解析 DATABASE_URL
    # 格式: postgresql://用户名:密码@主机:端口/数据库名
    import re
    match = re.match(r'postgresql://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)', DATABASE_URL)
    if not match:
        print(f"错误: 无法解析 DATABASE_URL: {DATABASE_URL}")
        return False

    username, password, host, port, dbname = match.groups()

    try:
        # 连接数据库
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=dbname,
            user=username,
            password=password
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # 检查字段是否已存在
        cursor.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'announcement'
            AND column_name = 'file_key'
        """)

        if cursor.fetchone():
            print("字段 file_key 已存在，跳过迁移")
        else:
            # 添加 file_key 字段
            cursor.execute("""
                ALTER TABLE announcement
                ADD COLUMN file_key VARCHAR(255)
            """)
            print("✓ 成功添加 file_key 字段")

        # 检查 file_name 字段是否已存在
        cursor.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'announcement'
            AND column_name = 'file_name'
        """)

        if cursor.fetchone():
            print("字段 file_name 已存在，跳过迁移")
        else:
            # 添加 file_name 字段
            cursor.execute("""
                ALTER TABLE announcement
                ADD COLUMN file_name VARCHAR(255)
            """)
            print("✓ 成功添加 file_name 字段")

        cursor.close()
        conn.close()
        print("\n✅ 数据库迁移完成！")
        return True

    except Exception as e:
        print(f"❌ 迁移失败: {e}")
        return False

if __name__ == "__main__":
    add_file_fields()
