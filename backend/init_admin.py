"""
初始化默认管理员用户
"""
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.database import engine, init_db
from sqlmodel import Session, select
from backend.models import User, UserRole
from backend.utils.auth import get_password_hash


def create_admin_user():
    """创建默认管理员用户"""
    with Session(engine) as session:
        # 检查是否已有管理员
        existing_admin = session.exec(
            select(User).where(User.username == "admin")
        ).first()

        if existing_admin:
            print("管理员用户已存在")
            print(f"用户名: {existing_admin.username}")
            print(f"邮箱: {existing_admin.email}")
            print(f"角色: {existing_admin.role.value}")
            return

        # 创建管理员
        admin = User(
            username="admin",
            email="admin@company.com",
            hashed_password=get_password_hash("admin123"),
            full_name="系统管理员",
            role=UserRole.ADMIN,
            is_active=True,
        )

        session.add(admin)
        session.commit()
        session.refresh(admin)

        print("管理员用户创建成功！")
        print(f"用户名: {admin.username}")
        print(f"密码: admin123")
        print(f"邮箱: {admin.email}")
        print(f"角色: {admin.role.value}")


if __name__ == "__main__":
    # 初始化数据库表
    init_db()
    # 创建管理员
    create_admin_user()
