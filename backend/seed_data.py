"""
为数据库生成测试数据
每个表20条记录
"""
import sys
from pathlib import Path
from datetime import datetime, timedelta
import random

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlmodel import Session, select
from backend.database import engine
from backend.models import (
    User, UserRole,
    Notification, NotificationType,
    Announcement, AnnouncementType,
    Response
)
from backend.utils.auth import get_password_hash


# 测试数据
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

NOTIFICATION_TITLES = [
    "新公告提醒",
    "新回复通知",
    "系统消息",
    "会议提醒",
    "任务提醒",
    "文档更新",
    "审批通知",
    "重要提醒",
    "系统维护通知",
    "公告回复提醒"
]

NOTIFICATION_CONTENTS = [
    "您有一条新的公告需要查看。",
    "您的回复收到了新的回复。",
    "系统将于今晚进行维护，请注意保存工作。",
    "您有一个会议将在30分钟后开始。",
    "您的任务即将到期，请及时完成。",
    "相关文档已更新，请查看最新版本。",
    "您的审批申请已通过。",
    "请注意，系统密码将于下周更新。",
    "系统升级已完成，请刷新页面。",
    "您关注的公告有了新的回复。"
]


def seed_users(session: Session):
    """创建用户数据（不包括已存在的admin）"""
    print("\n=== 创建用户数据 ===")

    # 检查是否已经创建过测试用户
    existing_count = len(list(session.exec(select(User).where(User.username != "admin")).all()))
    if existing_count >= 20:
        print(f"已有 {existing_count} 个测试用户，跳过创建。")
        return

    for i in range(20):
        username = USERNAMES[i]
        # 检查用户是否已存在
        existing = session.exec(select(User).where(User.username == username)).first()
        if existing:
            print(f"  跳过已存在用户: {username}")
            continue

        user = User(
            username=username,
            email=f"{username}@company.com",
            hashed_password=get_password_hash("123456"),
            full_name=USER_NAMES[i],
            role=UserRole.USER,
            is_active=True
        )
        session.add(user)
        print(f"  创建用户: {user.username} - {user.full_name}")

    session.commit()
    print(f"✓ 用户数据创建完成")


def seed_announcements(session: Session):
    """创建公告数据"""
    print("\n=== 创建公告数据 ===")

    # 检查是否已经创建过
    existing_count = len(list(session.exec(select(Announcement)).all()))
    if existing_count >= 20:
        print(f"已有 {existing_count} 条公告，跳过创建。")
        return

    # 获取所有用户
    users = session.exec(select(User)).all()

    for i in range(20):
        # 随机选择类型：前10条为公告，后10条为意见询问
        ann_type = AnnouncementType.ANNOUNCEMENT if i < 10 else AnnouncementType.INQUIRY

        announcement = Announcement(
            title=ANNOUNCEMENT_TITLES[i],
            content=ANNOUNCEMENT_CONTENTS[i],
            type=ann_type
        )
        session.add(announcement)
        print(f"  创建公告[{i+1}]: {announcement.title[:30]}...")

    session.commit()
    print(f"✓ 公告数据创建完成")


def seed_responses(session: Session):
    """创建回复数据"""
    print("\n=== 创建回复数据 ===")

    # 检查是否已经创建过
    existing_count = len(list(session.exec(select(Response)).all()))
    if existing_count >= 20:
        print(f"已有 {existing_count} 条回复，跳过创建。")
        return

    # 获取所有公告和用户
    announcements = session.exec(select(Announcement)).all()

    for i in range(20):
        # 随机选择一个公告
        announcement = random.choice(announcements)
        # 随机选择一个用户名
        colleague_name = random.choice(USER_NAMES)

        response = Response(
            announcement_id=announcement.id,
            colleague_name=colleague_name,
            content=RESPONSE_CONTENTS[i]
        )
        session.add(response)
        print(f"  创建回复[{i+1}]: {colleague_name} -> {announcement.title[:20]}...")

    session.commit()
    print(f"✓ 回复数据创建完成")


def seed_notifications(session: Session):
    """创建通知数据"""
    print("\n=== 创建通知数据 ===")

    # 检查是否已经创建过
    existing_count = len(list(session.exec(select(Notification)).all()))
    if existing_count >= 20:
        print(f"已有 {existing_count} 条通知，跳过创建。")
        return

    # 获取所有用户
    users = session.exec(select(User)).all()
    # 获取所有公告
    announcements = session.exec(select(Announcement)).all()

    for i in range(20):
        # 随机选择一个用户
        user = random.choice(users)
        # 随机选择类型
        notif_type = random.choice(list(NotificationType))
        # 随机选择标题和内容
        title_idx = i % len(NOTIFICATION_TITLES)
        content_idx = i % len(NOTIFICATION_CONTENTS)

        # 随机选择一个关联的公告
        related_id = random.choice([a.id for a in announcements]) if announcements else None

        notification = Notification(
            user_id=user.id,
            type=notif_type,
            title=NOTIFICATION_TITLES[title_idx],
            content=NOTIFICATION_CONTENTS[content_idx],
            is_read=random.choice([True, False]),
            related_id=related_id
        )
        session.add(notification)
        print(f"  创建通知[{i+1}]: {user.username} - {notification.title}")

    session.commit()
    print(f"✓ 通知数据创建完成")


def seed_all():
    """生成所有测试数据"""
    print("=" * 60)
    print("开始生成测试数据...")
    print("=" * 60)

    with Session(engine) as session:
        # 1. 创建用户
        seed_users(session)

        # 2. 创建公告
        seed_announcements(session)

        # 3. 创建回复
        seed_responses(session)

        # 4. 创建通知
        seed_notifications(session)

    print("\n" + "=" * 60)
    print("✓✓✓ 所有测试数据生成完成！✓✓✓")
    print("=" * 60)
    print("\n数据统计：")
    with Session(engine) as session:
        print(f"  用户数: {len(list(session.exec(select(User)).all()))}")
        print(f"  公告数: {len(list(session.exec(select(Announcement)).all()))}")
        print(f"  回复数: {len(list(session.exec(select(Response)).all()))}")
        print(f"  通知数: {len(list(session.exec(select(Notification)).all()))}")
    print()


if __name__ == "__main__":
    seed_all()
