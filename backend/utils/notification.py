"""
通知服务模块
处理站内信通知的发送和管理
"""
from typing import List
from sqlmodel import Session, select

from models import Notification, NotificationType, User


class NotificationService:
    """通知服务"""

    @staticmethod
    def send_notification(
        session: Session,
        user_id: int,
        type: NotificationType,
        title: str,
        content: str,
        related_id: int = None
    ) -> Notification:
        """发送通知给指定用户"""
        notification = Notification(
            user_id=user_id,
            type=type,
            title=title,
            content=content,
            related_id=related_id,
            is_read=False,
        )
        session.add(notification)
        session.commit()
        session.refresh(notification)
        return notification

    @staticmethod
    def broadcast_notification(
        session: Session,
        type: NotificationType,
        title: str,
        content: str,
        related_id: int = None,
        exclude_user_id: int = None
    ) -> List[Notification]:
        """广播通知给所有用户"""
        # 获取所有用户
        query = select(User)
        if exclude_user_id:
            query = query.where(User.id != exclude_user_id)

        users = session.exec(query).all()

        # 为每个用户创建通知
        notifications = []
        for user in users:
            if not user.is_active:
                continue

            notification = Notification(
                user_id=user.id,
                type=type,
                title=title,
                content=content,
                related_id=related_id,
                is_read=False,
            )
            session.add(notification)
            notifications.append(notification)

        session.commit()
        return notifications

    @staticmethod
    def mark_as_read(session: Session, notification_id: int) -> bool:
        """标记通知为已读"""
        notification = session.get(Notification, notification_id)
        if not notification:
            return False

        notification.is_read = True
        session.add(notification)
        session.commit()
        return True

    @staticmethod
    def mark_all_as_read(session: Session, user_id: int) -> int:
        """标记用户所有通知为已读"""
        notifications = session.exec(
            select(Notification).where(
                Notification.user_id == user_id,
                Notification.is_read == False
            )
        ).all()

        for notification in notifications:
            notification.is_read = True
            session.add(notification)

        session.commit()
        return len(notifications)

    @staticmethod
    def get_user_notifications(
        session: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 20,
        unread_only: bool = False
    ) -> List[Notification]:
        """获取用户的通知"""
        query = select(Notification).where(Notification.user_id == user_id)

        if unread_only:
            query = query.where(Notification.is_read == False)

        query = query.order_by(Notification.created_at.desc()).offset(skip).limit(limit)

        return session.exec(query).all()

    @staticmethod
    def get_unread_count(session: Session, user_id: int) -> int:
        """获取用户未读通知数量"""
        return len(
            session.exec(
                select(Notification).where(
                    Notification.user_id == user_id,
                    Notification.is_read == False
                )
            ).all()
        )

    @staticmethod
    def delete_notification(session: Session, notification_id: int) -> bool:
        """删除通知"""
        notification = session.get(Notification, notification_id)
        if not notification:
            return False

        session.delete(notification)
        session.commit()
        return True

    @staticmethod
    def delete_old_notifications(session: Session, days: int = 30) -> int:
        """删除旧通知（超过指定天数）"""
        from datetime import timedelta

        cutoff_date = datetime.utcnow() - timedelta(days=days)

        notifications = session.exec(
            select(Notification).where(Notification.created_at < cutoff_date)
        ).all()

        for notification in notifications:
            session.delete(notification)

        session.commit()
        return len(notifications)


# 创建全局实例
notification_service = NotificationService()
