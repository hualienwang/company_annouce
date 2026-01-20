from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, UploadFile, File, Form, Depends
from sqlmodel import Session, select

from models import (
    Response,
    ResponseCreate,
    ResponsePublic,
    ResponseWithAnnouncement,
    User,
    Announcement,
)
from database import get_session
from utils.s3_storage import s3_storage
from utils.auth import get_current_admin_user

router = APIRouter(prefix="/api/responses", tags=["回复"])


@router.post("", response_model=ResponsePublic)
async def create_response(
    announcement_id: int = Form(...),
    colleague_name: str = Form(...),
    content: str = Form(...),
    file: Optional[UploadFile] = File(None),
    session: Session = Depends(get_session),
):
    """创建回复（支持文件上传）"""
    # 验证公告是否存在
    # from backend.models import Announcement
    announcement = session.get(Announcement, announcement_id)
    if not announcement:
        raise HTTPException(status_code=404, detail="公告不存在")

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
            # 文件上传失败不影响回复提交

    # 创建回复
    db_response = Response(
        announcement_id=announcement_id,
        colleague_name=colleague_name,
        content=content,
        file_key=file_key,
        file_name=file_name,
    )
    session.add(db_response)
    session.commit()
    session.refresh(db_response)

    return db_response


@router.get("/announcement/{announcement_id}", response_model=List[ResponsePublic])
async def list_responses_by_announcement(
    announcement_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    session: Session = Depends(get_session),
):
    """获取指定公告的所有回复"""
    statement = (
        select(Response)
        .where(Response.announcement_id == announcement_id)
        .order_by(Response.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    responses = session.exec(statement).all()
    return responses


@router.get("/colleague/{colleague_name}", response_model=List[ResponseWithAnnouncement])
async def list_responses_by_colleague(
    colleague_name: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    session: Session = Depends(get_session),
):
    """获取指定同事的所有回复（包含公告标题）"""
    # 使用join查询，获取回复及其对应的公告标题
    statement = (
        select(Response, Announcement.title)
        .join(Announcement, Response.announcement_id == Announcement.id)
        .where(Response.colleague_name == colleague_name)
        .order_by(Response.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    results = session.exec(statement).all()

    # 构建返回数据
    responses = []
    for response, title in results:
        response_dict = response.dict()
        response_dict["announcement_title"] = title
        responses.append(ResponseWithAnnouncement(**response_dict))

    return responses


@router.get("", response_model=List[ResponsePublic])
async def list_all_responses(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    announcement_id: Optional[int] = Query(None),
    colleague_name: Optional[str] = Query(None),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_admin_user)
):
    """获取所有回复（仅管理员，支持筛选）"""
    statement = select(Response)

    if announcement_id:
        statement = statement.where(Response.announcement_id == announcement_id)

    if colleague_name:
        statement = statement.where(Response.colleague_name == colleague_name)

    statement = statement.order_by(Response.created_at.desc()).offset(skip).limit(limit)

    responses = session.exec(statement).all()
    return responses
