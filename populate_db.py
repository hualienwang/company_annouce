"""
獨立的數據庫填充腳本，用於向現有的數據庫中添加測試數據
"""
import sys
from pathlib import Path
from datetime import datetime, timedelta
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


# 測試數據
USER_NAMES = [
    "张伟", "李娜", "王强", "刘洋", "陈静",
    "杨杰", "赵敏", "黄磊", "周婷", "吴刚",
    "徐明", "孙丽", "马超", "朱燕", "郭伟",
    "何静", "林涛", "高飞", "谢芳", "郑军"
]

USERNAMES = [
    "zhangwei", "lina", "wangqiang", "liuyang", "chenjing",
    "yangjie", "zhaomin", "huanglei", "zhouting", "wugang",
    "xuming", "sunli", "machao", "zhuyan", "guowei",
    "hejing", "lintao", "gaofei", "xiefang", "zhengjun"
]

ANNOUNCEMENT_TITLES = [
    "2025年第一季度工作计划安排",
    "关于公司组织架构调整的通知",
    "新员工入职培训安排",
    "年度绩效评估开始通知",
    "系统升级维护公告",
    "办公室搬迁通知",
    "节假日放假安排",
    "新项目启动说明",
    "关于加强安全管理的通知",
    "员工福利调整通知",
    "关于考勤制度变更的通知",
    "团队建设活动通知",
    "技能培训报名通知",
    "客户满意度调查结果",
    "公司年度总结报告",
    "新产品发布计划",
    "市场拓展策略讨论",
    "技术研发方向更新",
    "财务报销流程优化",
    "内部沟通平台升级"
]

ANNOUNCEMENT_CONTENTS = [
    "为了更好地推进公司业务发展，现将2025年第一季度工作计划安排如下，请各部门认真执行。",
    "根据公司发展需要，经研究决定，对部分部门的组织架构进行调整，具体方案见附件。",
    "本周将举行新员工入职培训，请各部门配合做好相关工作安排。",
    "年度绩效评估工作正式开始，请各位员工准备好相关材料，按时提交。",
    "系统将于本周六凌晨进行升级维护，预计耗时4小时，期间将暂停服务。",
    "办公室将于下月搬迁至新地址，请各部门做好搬迁准备工作。",
    "春节放假安排如下：除夕至初六放假，共7天，初七正常上班。",
    "经过前期的充分准备，新项目将于下月正式启动，详情请关注后续通知。",
    "为加强公司安全管理，现要求各部门严格执行安全检查制度，确保无安全隐患。",
    "经公司研究决定，从下月起调整员工福利待遇，具体调整方案已发送至各部门。",
    "为提高工作效率，公司决定调整考勤制度，实行弹性工作制，详情见内部通知。",
    "为增强团队凝聚力，公司将于下月组织团队建设活动，请大家积极参与。",
    "为提升员工专业技能，公司将举办系列培训课程，欢迎各位同事踊跃报名。",
    "本次客户满意度调查结果显示，整体满意度达95%，感谢大家的努力。",
    "2024年度公司总体业绩良好，各项指标均达到预期目标，详情请见年度报告。",
    "经过研发团队的努力，新产品将于下季度正式发布，敬请期待。",
    "针对当前市场环境，公司制定了新的市场拓展策略，重点开发华东地区市场。",
    "根据行业发展趋势，公司将对技术研发方向进行调整，加大人工智能领域的投入。",
    "为简化报销流程，提高财务工作效率，现对财务报销流程进行优化。",
    "内部沟通平台将于下周进行升级，新功能包括在线会议、文件共享等。"
]

RESPONSE_CONTENTS = [
    "收到通知，我会按照要求做好相关工作。",
    "请问具体的执行时间是什么时候？",
    "这个方案非常好，我完全支持。",
    "关于这个问题，我有以下几点建议...",
    "已收到通知，会尽快安排。",
    "需要准备哪些材料？请告知。",
    "这个变化对我们部门有什么影响？",
    "我同意这个安排，会配合执行。",
    "有什么需要我协助的吗？",
    "建议增加相关培训课程。",
    "收到，已转发给团队成员。",
    "能否提供更详细的说明？",
    "这个安排很合理，支持。",
    "请问截止日期是什么时候？",
    "已了解情况，会及时反馈。",
    "这对我们工作很有帮助。",
    "需要召开一个会议讨论吗？",
    "我有一些想法想分享一下。",
    "会按照要求完成相关任务。",
    "有什么特别的注意事项吗？",
    "收到，谢谢通知。"
]

def get_password_hash(password: str) -> str:
    """简单密碼哈希實現（僅用於測試）"""
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()

def populate_database():
    print("=" * 60)
    print("開始填充數據庫...")
    print("=" * 60)

    # 使用SQLite數據庫
    DATABASE_URL = f"sqlite:///data/company.db"
    engine = create_engine(DATABASE_URL)
    
    with Session(engine) as session:
        # 檢查是否已經有公告數據
        existing_announcements = session.exec(select(Announcement)).all()
        if len(existing_announcements) > 0:
            print(f"發現 {len(existing_announcements)} 條現有公告，跳過填充。")
            return
        
        # 檢查是否已經有回覆數據
        existing_responses = session.exec(select(Response)).all()
        if len(existing_responses) > 0:
            print(f"發現 {len(existing_responses)} 條現有回覆，跳過填充。")
            return

        # 創建公告數據
        print("\n=== 創建公告數據 ===")
        for i in range(20):
            # 前10條為公告，後10條為意見詢問
            ann_type = AnnouncementType.ANNOUNCEMENT if i < 10 else AnnouncementType.INQUIRY
            
            announcement = Announcement(
                title=ANNOUNCEMENT_TITLES[i],
                content=ANNOUNCEMENT_CONTENTS[i],
                type=ann_type
            )
            session.add(announcement)
            print(f"  創建公告[{i+1}]: {announcement.title[:30]}...")
        
        session.commit()
        print("✓ 公告數據創建完成")

        # 創建回覆數據
        print("\n=== 創建回覆數據 ===")
        announcements = session.exec(select(Announcement)).all()
        
        for i in range(20):
            # 隨機選擇一個公告
            announcement = random.choice(announcements)
            # 隨機選擇一個用戶名
            colleague_name = random.choice(USER_NAMES)

            response = Response(
                announcement_id=announcement.id,
                colleague_name=colleague_name,
                content=RESPONSE_CONTENTS[i]
            )
            session.add(response)
            print(f"  創建回覆[{i+1}]: {colleague_name} -> {announcement.title[:20]}...")

        session.commit()
        print("✓ 回覆數據創建完成")

    print("\n" + "=" * 60)
    print("✓✓✓ 數據庫填充完成！✓✓✓")
    print("=" * 60)
    
    # 顯示統計信息
    with Session(engine) as session:
        announcement_count = session.exec(select(Announcement)).count()
        response_count = session.exec(select(Response)).count()
        user_count = session.exec(select(User)).count()
        notification_count = session.exec(select(Notification)).count()
        
        print(f"\n數據統計：")
        print(f"  用戶數: {user_count}")
        print(f"  公告數: {announcement_count}")
        print(f"  回覆數: {response_count}")
        print(f"  通知數: {notification_count}")


if __name__ == "__main__":
    populate_database()