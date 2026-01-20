#!/usr/bin/env python3
"""
檢查數據庫內容的腳本
"""

import sys
from pathlib import Path
from datetime import datetime
import random
from sqlmodel import SQLModel, Session, select, create_engine
from typing import Optional

# 添加項目根目錄到 Python 路徑
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 創建模型類（避免與已有的模型衝突）
from enum import Enum
from datetime import datetime
from sqlmodel import Field

class UserRole(str, Enum):
    """用户角色"""
    ADMIN = "admin"
    USER = "user"

class AnnouncementType(str, Enum):
    """公告类型"""
    ANNOUNCEMENT = "announcement"
    INQUIRY = "inquiry"

class NotificationType(str, Enum):
    """通知类型"""
    NEW_ANNOUNCEMENT = "new_announcement"
    NEW_RESPONSE = "new_response"
    SYSTEM = "system"

# 定義模型類（使用extend_existing=True處理已存在表）
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, Enum as SQLEnum

class User(SQLModel, table=True):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(sa_column=Column(String, unique=True, index=True))
    email: str = Field(sa_column=Column(String, unique=True, index=True))
    hashed_password: str = Field(sa_column=Column(String))
    full_name: str = Field(sa_column=Column(String))
    role: UserRole = Field(sa_column=Column(SQLEnum(UserRole), default=UserRole.USER, index=True))
    is_active: bool = Field(sa_column=Column(Boolean, default=True))
    created_at: datetime = Field(sa_column=Column(DateTime, default=datetime.utcnow))
    updated_at: Optional[datetime] = Field(sa_column=Column(DateTime, nullable=True))

class Announcement(SQLModel, table=True):
    __tablename__ = 'announcement'
    __table_args__ = {'extend_existing': True}

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(sa_column=Column(String, index=True))
    content: str = Field(sa_column=Column(Text))
    type: AnnouncementType = Field(sa_column=Column(SQLEnum(AnnouncementType), default=AnnouncementType.ANNOUNCEMENT, index=True))
    created_at: datetime = Field(sa_column=Column(DateTime, default=datetime.utcnow))
    updated_at: Optional[datetime] = Field(sa_column=Column(DateTime, nullable=True))

class Response(SQLModel, table=True):
    __tablename__ = 'response'
    __table_args__ = {'extend_existing': True}

    id: Optional[int] = Field(default=None, primary_key=True)
    announcement_id: int = Field(sa_column=Column(Integer, ForeignKey("announcement.id"), index=True))
    colleague_name: str = Field(sa_column=Column(String, index=True))
    content: str = Field(sa_column=Column(Text))
    file_key: Optional[str] = Field(sa_column=Column(String, index=True, nullable=True))
    file_name: Optional[str] = Field(sa_column=Column(String, nullable=True))
    created_at: datetime = Field(sa_column=Column(DateTime, default=datetime.utcnow))

class Notification(SQLModel, table=True):
    __tablename__ = 'notification'
    __table_args__ = {'extend_existing': True}

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(sa_column=Column(Integer, ForeignKey("user.id"), index=True))
    type: NotificationType = Field(sa_column=Column(SQLEnum(NotificationType), default=NotificationType.SYSTEM))
    title: str = Field(sa_column=Column(String))
    content: str = Field(sa_column=Column(Text))
    is_read: bool = Field(sa_column=Column(Boolean, default=False, index=True))
    related_id: Optional[int] = Field(sa_column=Column(Integer, nullable=True))
    created_at: datetime = Field(sa_column=Column(DateTime, default=datetime.utcnow, index=True))

def check_database():
    print("=" * 60)
    print("檢查數據庫內容...")
    print("=" * 60)

    # 使用SQLite數據庫（使用絕對路徑）
    DATABASE_URL = f"sqlite:////workspace/data/company.db"
    engine = create_engine(DATABASE_URL)
    
    with Session(engine) as session:
        # 檢查公告數量
        announcements_all = session.exec(select(Announcement)).all()
        announcement_count = len(announcements_all)
        print(f"\n✓ 公告總數: {announcement_count}")
        
        if announcement_count > 0:
            print("\n前5條公告:")
            for ann in announcements_all[:5]:
                print(f"  - ID: {ann.id}, Title: {ann.title[:50]}..., Type: {ann.type}")

        # 檢查回覆數量
        responses_all = session.exec(select(Response)).all()
        response_count = len(responses_all)
        print(f"\n✓ 回覆總數: {response_count}")
        
        if response_count > 0:
            print("\n前5條回覆:")
            for resp in responses_all[:5]:
                print(f"  - ID: {resp.id}, Colleague: {resp.colleague_name}, Announcement ID: {resp.announcement_id}")

        # 檢查用戶數量
        users_all = session.exec(select(User)).all()
        user_count = len(users_all)
        print(f"\n✓ 用戶總數: {user_count}")
        
        # 檢查通知數量
        notifications_all = session.exec(select(Notification)).all()
        notification_count = len(notifications_all)
        print(f"\n✓ 通知總數: {notification_count}")

    print("\n" + "=" * 60)
    print("✓ 數據庫檢查完成！")
    print("=" * 60)

if __name__ == "__main__":
    check_database()