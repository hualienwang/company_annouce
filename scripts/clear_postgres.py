#!/usr/bin/env python3
"""
清空 PostgreSQL 数据库中的所有数据（保留表结构）
"""
import os
import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# 加载环境变量
load_dotenv(project_root / "backend" / ".env")

# PostgreSQL 连接字符串
postgres_url = os.getenv("DATABASE_URL")

if not postgres_url:
    print("错误：未配置 DATABASE_URL 环境变量")
    sys.exit(1)


def clear_postgres():
    """清空 PostgreSQL 中的所有数据"""
    print("="*60)
    print("清空 PostgreSQL 数据")
    print("="*60)

    print(f"\n连接 PostgreSQL: {postgres_url.split('@')[1]}")

    # 创建引擎
    engine = create_engine(postgres_url)

    # 表的清空顺序（考虑外键约束：先清空有外键的表）
    tables_to_clear = [
        ('notification', False),  # 引用 user
        ('response', False),       # 引用 announcement
        ('announcement', False),   # 引用 user (author_id 在某些版本可能存在)
        ('user', True)            # 主表，user 是保留字需要引号
    ]

    with engine.begin() as conn:
        # 清空所有表
        for table, is_reserved_word in tables_to_clear:
            try:
                if is_reserved_word:
                    result = conn.execute(text(f'DELETE FROM "{table}"'))
                else:
                    result = conn.execute(text(f"DELETE FROM {table}"))
                print(f"  清空表 {table}: {result.rowcount} 行")
            except Exception as e:
                print(f"  清空表 {table} 失败: {e}")

        # 重置序列
        for table, is_reserved_word in tables_to_clear:
            try:
                if is_reserved_word:
                    conn.execute(text(f'ALTER SEQUENCE "{table}_id_seq" RESTART WITH 1'))
                else:
                    conn.execute(text(f"ALTER SEQUENCE {table}_id_seq RESTART WITH 1"))
                print(f"  重置序列 {table}_id_seq")
            except Exception as e:
                # 序列可能不存在，忽略错误
                pass

    print("\n" + "="*60)
    print("数据清空完成！")
    print("="*60)


if __name__ == "__main__":
    clear_postgres()
