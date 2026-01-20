"""
认证相关 API 路由
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import timedelta
from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from models import User, UserRole
from database import get_session
from utils.auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_current_active_user,
    get_current_admin_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(prefix="/api/auth", tags=["认证"])


class UserInfo(BaseModel):
    """用户信息"""
    id: int
    username: str
    email: str
    full_name: str
    role: UserRole
    is_active: bool


class TokenResponse(BaseModel):
    """令牌响应"""
    access_token: str
    token_type: str = "bearer"
    user: UserInfo


class UserCreateRequest(BaseModel):
    """创建用户请求"""
    username: str
    email: str
    password: str
    full_name: str
    role: UserRole = UserRole.USER


class UserUpdateRequest(BaseModel):
    """更新用户请求"""
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None


class UserResponse(BaseModel):
    """用户信息响应"""
    id: int
    username: str
    email: str
    full_name: str
    role: UserRole
    is_active: bool
    created_at: str


class EmailRequest(BaseModel):
    """发送邮件请求"""
    to_email: str
    subject: str
    body: str


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    """用户登录"""
    user = authenticate_user(session, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户已被禁用"
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return TokenResponse(
        access_token=access_token,
        user=UserInfo(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            role=user.role,
            is_active=user.is_active,
        )
    )


@router.post("/register")
async def register(
    user_data: UserCreateRequest,
    session: Session = Depends(get_session)
):
    """用户注册（公开接口，需管理员审核）"""
    # 检查用户名是否已存在
    existing_user = session.exec(
        select(User).where(User.username == user_data.username)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )

    # 检查邮箱是否已存在
    existing_email = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被注册"
        )

    # 创建用户（默认未激活，需要管理员审核）
    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        full_name=user_data.full_name,
        role=user_data.role,
        is_active=False,  # 新注册用户默认未激活
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return {"message": "注册成功，请等待管理员审核"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """获取当前用户信息"""
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role,
        is_active=current_user.is_active,
        created_at=current_user.created_at.isoformat(),
    )


@router.get("/users")
async def list_users(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取用户列表（仅管理员，支持分页）"""
    # 获取总数
    count_statement = select(User.id)
    total_count = len(session.exec(count_statement).all())

    # 获取用户列表
    users = session.exec(
        select(User).offset(skip).limit(limit)
    ).all()

    return {
        "total": total_count,
        "skip": skip,
        "limit": limit,
        "users": [
            UserResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                full_name=user.full_name,
                role=user.role,
                is_active=user.is_active,
                created_at=user.created_at.isoformat(),
            )
            for user in users
        ]
    }


@router.patch("/users/{user_id}/role")
async def update_user_role(
    user_id: int,
    role: UserRole,
    session: Session = Depends(get_session),
    current_admin: User = Depends(get_current_admin_user)
):
    """更新用户角色（仅管理员）"""
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )

    # 不允许修改自己的角色
    if user.id == current_admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能修改自己的角色"
        )

    user.role = role
    session.add(user)
    session.commit()

    return {"message": "角色更新成功"}


@router.patch("/users/{user_id}/status")
async def toggle_user_status(
    user_id: int,
    is_active: bool,
    session: Session = Depends(get_session),
    current_admin: User = Depends(get_current_admin_user)
):
    """切换用户状态（仅管理员）"""
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )

    # 不允许禁用自己
    if user.id == current_admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能禁用自己"
        )

    user.is_active = is_active
    session.add(user)
    session.commit()

    return {"message": "状态更新成功"}


@router.patch("/users/{user_id}")
async def update_user(
    user_id: int,
    user_update: UserUpdateRequest,
    session: Session = Depends(get_session),
    current_admin: User = Depends(get_current_admin_user)
):
    """更新用户信息（仅管理员）"""
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )

    # 不允许修改自己的角色和状态
    if user.id == current_admin.id:
        if user_update.role is not None and user_update.role != user.role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="不能修改自己的角色"
            )

    # 如果要更新用户名，检查是否已存在
    if user_update.username and user_update.username != user.username:
        existing_username = session.exec(
            select(User).where(User.username == user_update.username).where(User.id != user_id)
        ).first()

        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已存在"
            )

        user.username = user_update.username

    # 如果要更新邮箱，检查是否已被其他用户使用
    if user_update.email and user_update.email != user.email:
        existing_email = session.exec(
            select(User).where(User.email == user_update.email).where(User.id != user_id)
        ).first()

        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已被其他用户使用"
            )

        user.email = user_update.email

    # 更新其他字段
    if user_update.full_name is not None:
        user.full_name = user_update.full_name

    if user_update.role is not None:
        user.role = user_update.role

    session.add(user)
    session.commit()

    return {"message": "用户信息更新成功"}


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_admin: User = Depends(get_current_admin_user)
):
    """删除用户（仅管理员）"""
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )

    # 不允许删除自己
    if user.id == current_admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能删除自己"
        )

    # 删除用户（关联的回复、通知等会通过数据库级联删除或保留，取决于数据库配置）
    session.delete(user)
    session.commit()

    return {"message": "用户删除成功"}


@router.post("/send-email")
async def send_email(
    email_request: EmailRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    发送邮件
    注意：此功能需要配置SMTP服务器。
    在实际生产环境中，应该使用环境变量配置SMTP服务器信息。

    支持通过环境变量配置：
    - SMTP_SERVER: SMTP 服务器地址（默认：smtp.gmail.com）
    - SMTP_PORT: SMTP 端口（默认：587）
    - SMTP_USERNAME: SMTP 用户名
    - SMTP_PASSWORD: SMTP 密码
    - SMTP_FROM_EMAIL: 发件人邮箱（默认：SMTP_USERNAME）
    """

    # 从环境变量读取配置
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_username = os.getenv("SMTP_USERNAME", "your_email@gmail.com")
    smtp_password = os.getenv("SMTP_PASSWORD", "your_app_password")
    smtp_from_email = os.getenv("SMTP_FROM_EMAIL", smtp_username)

    # 模拟模式：如果配置未修改，则模拟发送成功
    is_mock_mode = smtp_username == "your_email@gmail.com" and \
                   smtp_password == "your_app_password"

    try:
        if is_mock_mode:
            # 模拟模式：在控制台输出邮件信息，模拟发送成功
            print("=" * 50)
            print("【邮件发送模拟模式】")
            print(f"发送人: {smtp_from_email}")
            print(f"收件人: {email_request.to_email}")
            print(f"主题: {email_request.subject}")
            print(f"内容:\n{email_request.body}")
            print("=" * 50)

            return {
                "message": "邮件发送成功（模拟模式）",
                "mock_mode": True,
                "to": email_request.to_email,
                "subject": email_request.subject
            }
        else:
            # 真实模式：通过SMTP发送邮件
            # 创建邮件
            msg = MIMEMultipart()
            msg['From'] = smtp_from_email
            msg['To'] = email_request.to_email
            msg['Subject'] = email_request.subject

            # 添加邮件正文
            body = email_request.body
            msg.attach(MIMEText(body, 'plain', 'utf-8'))

            # 连接SMTP服务器并发送邮件
            # 连接SMTP服务器并发送邮件
            server = smtplib.SMTP(smtp_server, smtp_port, timeout=60)
            server.starttls()  # 启用TLS加密
            server.set_debuglevel(0)  # 设置为1可查看详细调试信息
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_from_email, email_request.to_email, msg.as_string())
            server.quit()

            return {"message": "邮件发送成功"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"邮件发送失败: {str(e)}"
        )

