#!/usr/bin/env python3
"""
将 SQLite 数据迁移到 PostgreSQL 的脚本
"""
import os
import sys
from pathlib import Path
from datetime import datetime

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import sqlite3
from sqlalchemy import create_engine
from dotenv import load_dotenv

# 加载环境变量
load_dotenv(project_root / "backend" / ".env")

# SQLite 数据库路径
sqlite_db_path = project_root / "data" / "company.db"

# PostgreSQL 连接字符串
postgres_url = os.getenv("DATABASE_URL")

if not postgres_url:
    print("错误：未配置 DATABASE_URL 环境变量")
    sys.exit(1)


def read_sqlite_data():
    """读取 SQLite 数据库中的所有数据"""
    print(f"读取 SQLite 数据库: {sqlite_db_path}")

    if not sqlite_db_path.exists():
        print(f"错误：SQLite 数据库文件不存在: {sqlite_db_path}")
        return {}

    conn = sqlite3.connect(str(sqlite_db_path))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 获取所有表名（排除系统表）
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tables = [row[0] for row in cursor.fetchall()]

    print(f"找到表: {tables}")

    data = {}
    for table in tables:
        print(f"\n读取表: {table}")
        cursor.execute(f"SELECT * FROM {table}")
        columns = [desc[0] for desc in cursor.description]
        print(f"  列: {columns}")

        rows = cursor.fetchall()
        print(f"  数据行数: {len(rows)}")

        # 将行转换为字典列表
        table_data = []
        for row in rows:
            row_dict = {col: row[col] for col in columns}
            table_data.append(row_dict)

        data[table] = {
            'columns': columns,
            'rows': table_data
        }

    conn.close()
    return data


def migrate_to_postgres(data):
    """将数据迁移到 PostgreSQL"""
    print(f"\n连接 PostgreSQL: {postgres_url.split('@')[1]}")

    # 导入模型
    from backend.models import User, Announcement, Response, Notification
    from sqlmodel import SQLModel

    # 创建 PostgreSQL 引擎
    pg_engine = create_engine(postgres_url)

    # 创建表结构
    print("\n创建 PostgreSQL 表结构...")
    SQLModel.metadata.create_all(pg_engine)
    print("表结构创建成功")

    # 插入数据
    from sqlalchemy.orm import sessionmaker

    Session = sessionmaker(bind=pg_engine)
    session = Session()

    try:
        # 1. 迁移用户数据
        if 'user' in data:
            print(f"\n迁移 user 表...")
            users_data = data['user']['rows']
            inserted_count = 0

            for row in users_data:
                try:
                    # 处理时间戳
                    created_at = row.get('created_at')
                    updated_at = row.get('updated_at')

                    if isinstance(created_at, str):
                        created_at = datetime.fromisoformat(created_at)
                    if updated_at and isinstance(updated_at, str):
                        updated_at = datetime.fromisoformat(updated_at)

                    # 处理 role 字段大小写
                    role = row.get('role', 'USER')
                    if isinstance(role, str):
                        role = role.lower()

                    user = User(
                        id=row['id'],
                        username=row['username'],
                        full_name=row['full_name'],
                        email=row['email'],
                        hashed_password=row['hashed_password'],
                        role=role,
                        is_active=bool(row.get('is_active', 1)),
                        created_at=created_at,
                        updated_at=updated_at
                    )
                    session.add(user)
                    session.flush()  # 立即插入并获取新 ID
                    inserted_count += 1
                except Exception as e:
                    print(f"  插入用户失败: {row.get('username', 'unknown')} - {e}")
                    session.rollback()

            session.commit()
            print(f"  成功插入 {inserted_count} 个用户")

        # 2. 迁移公告数据（合并两个表）
        print(f"\n迁移 announcements 表...")

        # 合并两个公告表的数据并去重
        announcements_map = {}

        if 'announcements' in data:
            for row in data['announcements']['rows']:
                key = (row['id'], row['title'], row['content'])
                if key not in announcements_map:
                    announcements_map[key] = row

        if 'announcement' in data:
            for row in data['announcement']['rows']:
                key = (row['id'], row['title'], row['content'])
                if key not in announcements_map:
                    announcements_map[key] = row

        announcements_to_migrate = list(announcements_map.values())
        print(f"  合并后有 {len(announcements_to_migrate)} 条唯一记录")

        # 创建 ID 映射（处理重复 ID）
        id_mapping = {}
        next_id = 1

        for row in announcements_to_migrate:
            try:
                # 处理时间戳
                created_at = row.get('created_at')
                updated_at = row.get('updated_at')

                if isinstance(created_at, str):
                    created_at = datetime.fromisoformat(created_at)
                if updated_at and isinstance(updated_at, str):
                    updated_at = datetime.fromisoformat(updated_at)

                # 处理 type 字段
                announcement_type = row.get('type', 'announcement')
                if isinstance(announcement_type, str):
                    announcement_type = announcement_type.lower()

                # 记录 ID 映射
                old_id = row['id']
                id_mapping[old_id] = next_id
                new_id = next_id
                next_id += 1

                announcement = Announcement(
                    id=new_id,  # 使用新 ID
                    title=row['title'],
                    content=row['content'],
                    type=announcement_type,
                    created_at=created_at,
                    updated_at=updated_at
                )
                session.add(announcement)
                session.flush()  # 立即插入
            except Exception as e:
                print(f"  插入公告失败: {row.get('title', 'unknown')} - {e}")
                session.rollback()

        session.commit()
        print(f"  成功插入 {len(id_mapping)} 个公告")

        # 3. 迁移回复数据（合并两个表）
        print(f"\n迁移 responses 表...")

        # 合并两个回复表的数据并去重
        responses_map = {}

        if 'responses' in data:
            for row in data['responses']['rows']:
                key = (row['id'], row['announcement_id'], row['colleague_name'], row['content'])
                if key not in responses_map:
                    responses_map[key] = row

        if 'response' in data:
            for row in data['response']['rows']:
                key = (row['id'], row['announcement_id'], row['colleague_name'], row['content'])
                if key not in responses_map:
                    responses_map[key] = row

        responses_to_migrate = list(responses_map.values())
        print(f"  合并后有 {len(responses_to_migrate)} 条唯一记录")

        # 创建回复 ID 映射
        response_id_mapping = {}
        next_response_id = 1

        for row in responses_to_migrate:
            try:
                # 处理时间戳
                created_at = row.get('created_at')
                if isinstance(created_at, str):
                    created_at = datetime.fromisoformat(created_at)

                # 分配新的回复 ID
                old_id = row['id']
                response_id_mapping[old_id] = next_response_id
                new_id = next_response_id
                next_response_id += 1

                # 映射 announcement_id
                old_announcement_id = row['announcement_id']
                new_announcement_id = id_mapping.get(old_announcement_id, old_announcement_id)

                response = Response(
                    id=new_id,
                    content=row['content'],
                    colleague_name=row['colleague_name'],
                    announcement_id=new_announcement_id,
                    file_key=row.get('file_key'),
                    file_name=row.get('file_name'),
                    created_at=created_at
                )
                session.add(response)
                session.flush()
            except Exception as e:
                print(f"  插入回复失败: {row.get('colleague_name', 'unknown')} - {e}")
                session.rollback()

        session.commit()
        print(f"  成功插入 {len(response_id_mapping)} 个回复")

        # 4. 迁移通知数据
        if 'notification' in data:
            print(f"\n迁移 notification 表...")
            notifications_data = data['notification']['rows']
            inserted_count = 0

            for row in notifications_data:
                try:
                    # 处理时间戳
                    created_at = row.get('created_at')
                    if isinstance(created_at, str):
                        created_at = datetime.fromisoformat(created_at)

                    # 处理 type 字段
                    notification_type = row.get('type', 'system')
                    if isinstance(notification_type, str):
                        notification_type = notification_type.lower()

                    notification = Notification(
                        id=row['id'],
                        user_id=row['user_id'],
                        title=row['title'],
                        content=row['content'],
                        is_read=bool(row.get('is_read', 0)),
                        type=notification_type,
                        related_id=row.get('related_id'),
                        created_at=created_at
                    )
                    session.add(notification)
                    session.flush()
                    inserted_count += 1
                except Exception as e:
                    print(f"  插入通知失败: {row.get('title', 'unknown')} - {e}")
                    session.rollback()

            session.commit()
            print(f"  成功插入 {inserted_count} 个通知")

        print("\n" + "="*60)
        print("数据迁移完成！")
        print("="*60)

        # 显示迁移统计
        print("\n迁移统计：")
        print(f"  - 用户: {len(session.query(User).all())}")
        print(f"  - 公告: {len(session.query(Announcement).all())}")
        print(f"  - 回复: {len(session.query(Response).all())}")
        print(f"  - 通知: {len(session.query(Notification).all())}")

    except Exception as e:
        print(f"\n迁移过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        session.rollback()
        raise
    finally:
        session.close()


def main():
    """主函数"""
    print("="*60)
    print("SQLite 到 PostgreSQL 数据迁移脚本")
    print("="*60)

    # 步骤 1: 读取 SQLite 数据
    data = read_sqlite_data()

    if not data:
        print("SQLite 数据库中没有数据或读取失败")
        return

    # 步骤 2: 迁移到 PostgreSQL
    migrate_to_postgres(data)


if __name__ == "__main__":
    main()
