from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, SQLModel
from enum import Enum


class UserRole(str, Enum):
    """用户角色"""
    ADMIN = "admin"
    USER = "user"


class AnnouncementType(str, Enum):
    """公告类型"""
    ANNOUNCEMENT = "announcement"
    INQUIRY = "inquiry"


class User(SQLModel, table=True):
    """用户模型"""
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True, description="用户名")
    email: str = Field(unique=True, index=True, description="邮箱")
    hashed_password: str = Field(description="加密后的密码")
    full_name: str = Field(description="真实姓名")
    role: UserRole = Field(default=UserRole.USER, index=True, description="角色")
    is_active: bool = Field(default=True, description="是否激活")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="创建时间")
    updated_at: Optional[datetime] = Field(default=None, description="更新时间")


class NotificationType(str, Enum):
    """通知类型"""
    NEW_ANNOUNCEMENT = "new_announcement"
    NEW_RESPONSE = "new_response"
    SYSTEM = "system"


class Notification(SQLModel, table=True):
    """通知模型"""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True, description="用户ID")
    type: NotificationType = Field(default=NotificationType.SYSTEM, description="通知类型")
    title: str = Field(description="通知标题")
    content: str = Field(description="通知内容")
    is_read: bool = Field(default=False, index=True, description="是否已读")
    related_id: Optional[int] = Field(default=None, description="关联ID（如公告ID）")
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True, description="创建时间")


class Announcement(SQLModel, table=True):
    """公告模型"""
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, description="公告标题")
    content: str = Field(description="公告内容")
    type: AnnouncementType = Field(default=AnnouncementType.ANNOUNCEMENT, index=True, description="公告类型")
    file_key: Optional[str] = Field(default=None, index=True, description="文件在S3中的键")
    file_name: Optional[str] = Field(default=None, description="原始文件名")
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True, description="创建时间")
    updated_at: Optional[datetime] = Field(default=None, description="更新时间")


class Response(SQLModel, table=True):
    """回复模型"""
    id: Optional[int] = Field(default=None, primary_key=True)
    announcement_id: int = Field(foreign_key="announcement.id", index=True, description="公告ID")
    colleague_name: str = Field(index=True, description="同事姓名")
    content: str = Field(description="回复内容")
    file_key: Optional[str] = Field(default=None, index=True, description="文件在S3中的键")
    file_name: Optional[str] = Field(default=None, description="原始文件名")
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True, description="创建时间")


# API 请求/响应模型

class AnnouncementCreate(SQLModel):
    """创建公告请求"""
    title: str
    content: str
    type: AnnouncementType = AnnouncementType.ANNOUNCEMENT


class AnnouncementUpdate(SQLModel):
    """更新公告请求"""
    title: Optional[str] = None
    content: Optional[str] = None
    type: Optional[AnnouncementType] = None


class AnnouncementPublic(SQLModel):
    """公告公开信息"""
    id: int
    title: str
    content: str
    type: AnnouncementType
    file_key: Optional[str] = None
    file_name: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime]


class AnnouncementWithResponses(AnnouncementPublic):
    """公告及其回复"""
    responses: list["ResponsePublic"] = []


class ResponseCreate(SQLModel):
    """创建回复请求"""
    announcement_id: int
    colleague_name: str
    content: str


class ResponseUpdate(SQLModel):
    """更新回复请求"""
    content: Optional[str] = None


class ResponsePublic(SQLModel):
    """回复公开信息"""
    id: int
    announcement_id: int
    colleague_name: str
    content: str
    file_key: Optional[str] = None
    file_name: Optional[str] = None
    created_at: datetime


class ResponseWithAnnouncement(ResponsePublic):
    """回复及公告信息"""
    announcement_title: str
