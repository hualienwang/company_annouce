from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, UploadFile, File, Form, Depends
from sqlmodel import Session, select

from models import (
    Announcement,
    AnnouncementCreate,
    AnnouncementPublic,
    AnnouncementWithResponses,
    AnnouncementType,
    Response,
    ResponsePublic,
    User,
    NotificationType,
)
from database import get_session
from utils.auth import get_current_active_user, get_current_admin_user
from utils.notification import notification_service
from utils.s3_storage import s3_storage

router = APIRouter(prefix="/api/announcements", tags=["公告"])


@router.post("", response_model=AnnouncementPublic)
async def create_announcement(
    title: str = Form(...),
    content: str = Form(...),
    type: AnnouncementType = Form(AnnouncementType.ANNOUNCEMENT),
    file: Optional[UploadFile] = File(None),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """创建公告（支持文件上传）"""
    # 处理文件上传
    file_key: Optional[str] = None
    file_name: Optional[str] = None

    if file and file.filename:
        try:
            file_content = await file.read()
            file_key = await s3_storage.upload_file(
                file_content=file_content,
                file_name=file.filename,
                content_type=file.content_type or "application/octet-stream",
            )
            file_name = file.filename
            print(f"文件上传成功: {file_key}")
        except Exception as e:
            print(f"文件上传失败: {e}")
            # 文件上传失败不影响公告创建

    # 创建公告
    db_announcement = Announcement(
        title=title,
        content=content,
        type=type,
        file_key=file_key,
        file_name=file_name,
    )
    session.add(db_announcement)
    session.commit()
    session.refresh(db_announcement)

    # 发送通知给所有用户
    notification_type = (
        NotificationType.NEW_ANNOUNCEMENT
        if type == AnnouncementType.ANNOUNCEMENT
        else NotificationType.NEW_RESPONSE
    )

    notification_service.broadcast_notification(
        session=session,
        type=notification_type,
        title=f"新{type.value}：{title}",
        content=f"{current_user.full_name} 发布了一条新{type.value}",
        related_id=db_announcement.id,
        exclude_user_id=current_user.id  # 不通知自己
    )

    return db_announcement


@router.get("", response_model=List[AnnouncementPublic])
async def list_announcements(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(10, ge=1, le=100, description="每页记录数"),
    type: Optional[AnnouncementType] = Query(None, description="公告类型筛选"),
    session: Session = Depends(get_session),
):
    """获取公告列表（分页）"""
    statement = select(Announcement)

    # 类型筛选
    if type:
        statement = statement.where(Announcement.type == type)

    # 分页
    statement = statement.order_by(Announcement.created_at.desc()).offset(skip).limit(limit)

    announcements = session.exec(statement).all()
    return announcements


@router.get("/{announcement_id}", response_model=AnnouncementWithResponses)
async def get_announcement(
    announcement_id: int, session: Session = Depends(get_session)
):
    """获取公告详情（包含回复）"""
    announcement = session.get(Announcement, announcement_id)
    if not announcement:
        raise HTTPException(status_code=404, detail="公告不存在")

    # 获取回复
    responses = session.exec(
        select(Response)
        .where(Response.announcement_id == announcement_id)
        .order_by(Response.created_at.desc())
    ).all()

    # 构建响应
    return AnnouncementWithResponses(
        **announcement.dict(),
        responses=[ResponsePublic.from_orm(r) for r in responses]
    )


@router.delete("/{announcement_id}")
async def delete_announcement(
    announcement_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_admin_user)
):
    """删除公告（仅管理员）"""
    announcement = session.get(Announcement, announcement_id)
    if not announcement:
        raise HTTPException(status_code=404, detail="公告不存在")

    # 删除关联的回复
    responses = session.exec(
        select(Response).where(Response.announcement_id == announcement_id)
    ).all()
    for response in responses:
        session.delete(response)

    # 删除公告
    session.delete(announcement)
    session.commit()

    return {"message": "删除成功"}
