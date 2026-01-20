import os
from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
from pathlib import Path

# 从环境变量获取数据库连接字符串（强制使用 PostgreSQL）
from dotenv import load_dotenv
load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL")

if os.getenv("DATABASE_URL"):
    DATABASE_URL = os.getenv("DATABASE_URL")
else:
    # 使用绝对路径，避免工作目录变化导致的问题
    project_root = Path(__file__).parent.parent
    db_path = project_root / "data" / "company.db"
    DATABASE_URL = f"sqlite:///{db_path}"

# if not DATABASE_URL:
#     raise ValueError(
#         "DATABASE_URL 环境变量未配置！\n"
#         "请在 backend/.env 文件中设置 DATABASE_URL。\n"
#         "示例格式：postgresql://username:password@localhost:5432/database_name\n"
#         "或使用集成服务提供的 PostgreSQL 数据库。"
#     )
print(f"使用的数据库连接字符串: {DATABASE_URL}")

# 判断是否使用 SQLite
IS_SQLITE = DATABASE_URL.startswith("sqlite://")

# 创建数据库引擎
if IS_SQLITE:
    # SQLite 配置（不支持连接池和 SSL）
    engine = create_engine(DATABASE_URL, echo=False)
else:
    # PostgreSQL 配置（添加连接池和 SSL 配置）
    engine = create_engine(
        DATABASE_URL,
        echo=False,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800,  # 30分钟后回收连接，避免SSL连接过期
        pool_pre_ping=True,  # 每次使用连接前检查连接是否有效
        connect_args={
            "connect_timeout": 10,
            "sslmode": "prefer",  # 优先使用SSL，但也允许非SSL连接
        }
    )
# 创建数据库引擎（PostgreSQL）
# engine = create_engine(DATABASE_URL, echo=False)


def init_db():
    """初始化数据库表"""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """获取数据库会话"""
    with Session(engine) as session:
        yield session
