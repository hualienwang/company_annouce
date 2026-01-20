"""
通知相关 API 路由
"""
from typing import List
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session

from models import Notification, NotificationType
from database import get_session
from utils.auth import get_current_active_user, User
from utils.notification import notification_service

router = APIRouter(prefix="/api/notifications", tags=["通知"])


@router.get("", response_model=List[dict])
async def get_notifications(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    unread_only: bool = Query(False, description="仅获取未读通知"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """获取当前用户的通知"""
    notifications = notification_service.get_user_notifications(
        session=session,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        unread_only=unread_only
    )

    return [
        {
            "id": n.id,
            "type": n.type.value,
            "title": n.title,
            "content": n.content,
            "is_read": n.is_read,
            "related_id": n.related_id,
            "created_at": n.created_at.isoformat(),
        }
        for n in notifications
    ]


@router.get("/unread-count")
async def get_unread_count(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """获取未读通知数量"""
    count = notification_service.get_unread_count(
        session=session,
        user_id=current_user.id
    )
    return {"unread_count": count}


@router.post("/{notification_id}/read")
async def mark_as_read(
    notification_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """标记通知为已读"""
    # 验证通知是否属于当前用户
    notification = session.get(Notification, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="通知不存在")

    if notification.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权访问此通知")

    success = notification_service.mark_as_read(session, notification_id)
    if not success:
        raise HTTPException(status_code=404, detail="通知不存在")

    return {"message": "标记成功"}


@router.post("/read-all")
async def mark_all_as_read(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """标记所有通知为已读"""
    count = notification_service.mark_all_as_read(
        session=session,
        user_id=current_user.id
    )
    return {"message": f"已标记 {count} 条通知为已读"}


@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """删除通知"""
    # 验证通知是否属于当前用户
    notification = session.get(Notification, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="通知不存在")

    if notification.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权删除此通知")

    success = notification_service.delete_notification(session, notification_id)
    if not success:
        raise HTTPException(status_code=404, detail="通知不存在")

    return {"message": "删除成功"}
