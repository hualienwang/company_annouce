#!/usr/bin/env python3
"""
PostgreSQL 数据库迁移脚本，用于检查和添加缺失的字段
适用于 DATABASE_URL=postgresql://postgres:1234@localhost:5432/postgres
"""
import os
import sys
from pathlib import Path
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# PostgreSQL 连接信息
DATABASE_URL = "postgresql://postgres:1234@localhost:5432/postgres"

def parse_database_url(url):
    """解析 PostgreSQL 连接 URL"""
    import re
    match = re.match(r'postgresql://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)', url)
    if not match:
        raise ValueError(f"无法解析 DATABASE_URL: {url}")
    return match.groups()

def migrate_postgresql_database():
    """迁移 PostgreSQL 数据库，添加缺失的字段"""
    print("开始迁移 PostgreSQL 数据库...")
    print(f"数据库 URL: {DATABASE_URL.replace('1234', '****')}")
    
    # 解析连接信息
    username, password, host, port, dbname = parse_database_url(DATABASE_URL)
    
    try:
        # 连接数据库
        conn = psycopg2.connect(
            host=host,
            port=int(port),
            database=dbname,
            user=username,
            password=password
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        print(f"✅ 成功连接到 PostgreSQL 数据库: {dbname}")
        
        # 检查 announcement 表是否存在
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.tables 
                WHERE table_name = 'announcement'
            )
        """)
        
        if not cursor.fetchone()[0]:
            print("❌ announcement 表不存在，请先运行应用初始化数据库")
            return False
        
        # 检查 announcement 表的字段
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'announcement'
            ORDER BY ordinal_position
        """)
        announcement_columns = [col[0] for col in cursor.fetchall()]
        
        print(f"当前 announcement 表字段: {announcement_columns}")
        
        # 检查并添加 file_key 字段
        if 'file_key' not in announcement_columns:
            print("添加 file_key 字段...")
            cursor.execute("""
                ALTER TABLE announcement 
                ADD COLUMN file_key VARCHAR(255)
            """)
            print("✓ 已添加 file_key 字段到 announcement 表")
        else:
            print("✓ file_key 字段已存在")
        
        # 检查并添加 file_name 字段
        if 'file_name' not in announcement_columns:
            print("添加 file_name 字段...")
            cursor.execute("""
                ALTER TABLE announcement 
                ADD COLUMN file_name VARCHAR(255)
            """)
            print("✓ 已添加 file_name 字段到 announcement 表")
        else:
            print("✓ file_name 字段已存在")
        
        # 检查并添加 updated_at 字段
        if 'updated_at' not in announcement_columns:
            print("添加 updated_at 字段...")
            cursor.execute("""
                ALTER TABLE announcement 
                ADD COLUMN updated_at TIMESTAMP WITH TIME ZONE
            """)
            print("✓ 已添加 updated_at 字段到 announcement 表")
        else:
            print("✓ updated_at 字段已存在")
        
        # 检查 response 表是否存在
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.tables 
                WHERE table_name = 'response'
            )
        """)
        
        if cursor.fetchone()[0]:
            # 检查 response 表的字段
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'response'
                ORDER BY ordinal_position
            """)
            response_columns = [col[0] for col in cursor.fetchall()]
            
            print(f"当前 response 表字段: {response_columns}")
            
            # 检查并添加 file_key 字段到 response 表
            if 'file_key' not in response_columns:
                print("添加 file_key 字段到 response 表...")
                cursor.execute("""
                    ALTER TABLE response 
                    ADD COLUMN file_key VARCHAR(255)
                """)
                print("✓ 已添加 file_key 字段到 response 表")
            else:
                print("✓ response 表的 file_key 字段已存在")
            
            # 检查并添加 file_name 字段到 response 表
            if 'file_name' not in response_columns:
                print("添加 file_name 字段到 response 表...")
                cursor.execute("""
                    ALTER TABLE response 
                    ADD COLUMN file_name VARCHAR(255)
                """)
                print("✓ 已添加 file_name 字段到 response 表")
            else:
                print("✓ response 表的 file_name 字段已存在")
        else:
            print("⚠️  response 表不存在，跳过 response 表字段检查")
        
        # 检查 user 表是否存在
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.tables 
                WHERE table_name = 'user'
            )
        """)
        
        if cursor.fetchone()[0]:
            # 检查 user 表的字段
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'user'
                ORDER BY ordinal_position
            """)
            user_columns = [col[0] for col in cursor.fetchall()]
            
            print(f"当前 user 表字段: {user_columns}")
            
            # 检查并添加 updated_at 字段到 user 表
            if 'updated_at' not in user_columns:
                print("添加 updated_at 字段到 user 表...")
                cursor.execute("""
                    ALTER TABLE "user" 
                    ADD COLUMN updated_at TIMESTAMP WITH TIME ZONE
                """)
                print("✓ 已添加 updated_at 字段到 user 表")
            else:
                print("✓ user 表的 updated_at 字段已存在")
        else:
            print("⚠️  user 表不存在，跳过 user 表字段检查")
        
        # 关闭连接
        cursor.close()
        conn.close()
        
        print("\n✅ PostgreSQL 数据库迁移完成！")
        return True
        
    except Exception as e:
        print(f"❌ 迁移失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_database_if_not_exists():
    """如果数据库不存在则创建"""
    print("\n检查数据库是否存在...")
    
    username, password, host, port, dbname = parse_database_url(DATABASE_URL)
    
    try:
        # 连接到默认数据库 postgres
        conn = psycopg2.connect(
            host=host,
            port=int(port),
            database="postgres",  # 连接到默认数据库
            user=username,
            password=password
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # 检查目标数据库是否存在
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (dbname,))
        if not cursor.fetchone():
            print(f"创建数据库: {dbname}")
            cursor.execute(f"CREATE DATABASE {dbname}")
            print(f"✅ 数据库 {dbname} 创建成功")
        else:
            print(f"✅ 数据库 {dbname} 已存在")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ 检查/创建数据库失败: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("PostgreSQL 数据库迁移脚本")
    print("DATABASE_URL: postgresql://postgres:****@localhost:5432/postgres")
    print("=" * 60)
    
    # 首先检查并创建数据库
    if not create_database_if_not_exists():
        sys.exit(1)
    
    # 执行迁移
    if migrate_postgresql_database():
        print("\n🎉 所有迁移任务完成！")
        print("\n您现在可以运行应用了。")
    else:
        print("\n❌ 迁移过程中出现错误，请检查上述错误信息。")
        sys.exit(1)