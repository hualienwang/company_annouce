"""
搜索相关 API 路由
使用 PostgreSQL 全文搜索功能
"""
from typing import List, Optional
from fastapi import APIRouter, Query, Depends
from sqlmodel import Session, text

from models import Announcement, Response, AnnouncementPublic, ResponsePublic
from database import get_session
from utils.auth import get_current_active_user, User

router = APIRouter(prefix="/api/search", tags=["搜索"])


@router.get("/announcements", response_model=List[dict])
async def search_announcements(
    q: str = Query(..., min_length=1, description="搜索关键词"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """全文搜索公告"""
    # 使用 PostgreSQL 全文搜索
    search_query = text("""
        SELECT
            id,
            title,
            content,
            type,
            created_at,
            updated_at,
            ts_rank(
                to_tsvector('chinese', title || ' ' || content),
                plainto_tsquery('chinese', :query)
            ) as rank
        FROM announcement
        WHERE to_tsvector('chinese', title || ' ' || content) @@ plainto_tsquery('chinese', :query)
        ORDER BY rank DESC
        LIMIT :limit OFFSET :skip
    """)

    results = session.exec(search_query, {
        'query': q,
        'limit': limit,
        'skip': skip,
    }).all()

    return [
        {
            'id': row.id,
            'title': row.title,
            'content': row.content,
            'type': row.type,
            'created_at': row.created_at.isoformat(),
            'updated_at': row.updated_at.isoformat() if row.updated_at else None,
            'relevance': row.rank,
        }
        for row in results
    ]


@router.get("/responses", response_model=List[dict])
async def search_responses(
    q: str = Query(..., min_length=1, description="搜索关键词"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """全文搜索回复"""
    # 使用 PostgreSQL 全文搜索
    search_query = text("""
        SELECT
            r.id,
            r.announcement_id,
            r.colleague_name,
            r.content,
            r.file_key,
            r.file_name,
            r.created_at,
            a.title as announcement_title,
            ts_rank(
                to_tsvector('chinese', r.colleague_name || ' ' || r.content),
                plainto_tsquery('chinese', :query)
            ) as rank
        FROM response r
        LEFT JOIN announcement a ON r.announcement_id = a.id
        WHERE to_tsvector('chinese', r.colleague_name || ' ' || r.content) @@ plainto_tsquery('chinese', :query)
        ORDER BY rank DESC
        LIMIT :limit OFFSET :skip
    """)

    results = session.exec(search_query, {
        'query': q,
        'limit': limit,
        'skip': skip,
    }).all()

    return [
        {
            'id': row.id,
            'announcement_id': row.announcement_id,
            'announcement_title': row.announcement_title,
            'colleague_name': row.colleague_name,
            'content': row.content,
            'file_key': row.file_key,
            'file_name': row.file_name,
            'created_at': row.created_at.isoformat(),
            'relevance': row.rank,
        }
        for row in results
    ]


@router.get("/all", response_model=dict)
async def search_all(
    q: str = Query(..., min_length=1, description="搜索关键词"),
    skip: int = Query(0, ge=0),
    limit: int = Query(5, ge=1, le=50),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """全文搜索公告和回复"""
    # 搜索公告
    announcement_query = text("""
        SELECT
            'announcement' as type,
            id,
            title as display_title,
            content as display_content,
            NULL as announcement_title,
            created_at,
            ts_rank(
                to_tsvector('chinese', title || ' ' || content),
                plainto_tsquery('chinese', :query)
            ) as rank
        FROM announcement
        WHERE to_tsvector('chinese', title || ' ' || content) @@ plainto_tsquery('chinese', :query)
        ORDER BY rank DESC
        LIMIT :limit OFFSET :skip
    """)

    announcements = session.exec(announcement_query, {
        'query': q,
        'limit': limit,
        'skip': skip,
    }).all()

    # 搜索回复
    response_query = text("""
        SELECT
            'response' as type,
            r.id,
            a.title as display_title,
            r.content as display_content,
            a.title as announcement_title,
            r.created_at,
            ts_rank(
                to_tsvector('chinese', r.colleague_name || ' ' || r.content),
                plainto_tsquery('chinese', :query)
            ) as rank
        FROM response r
        LEFT JOIN announcement a ON r.announcement_id = a.id
        WHERE to_tsvector('chinese', r.colleague_name || ' ' || r.content) @@ plainto_tsquery('chinese', :query)
        ORDER BY rank DESC
        LIMIT :limit OFFSET :skip
    """)

    responses = session.exec(response_query, {
        'query': q,
        'limit': limit,
        'skip': skip,
    }).all()

    # 合并结果并按相关性排序
    all_results = []
    all_results.extend([
        {
            'type': row.type,
            'id': row.id,
            'display_title': row.display_title,
            'display_content': row.display_content,
            'announcement_title': row.announcement_title,
            'created_at': row.created_at.isoformat(),
            'relevance': row.rank,
        }
        for row in announcements
    ])
    all_results.extend([
        {
            'type': row.type,
            'id': row.id,
            'display_title': row.display_title,
            'display_content': row.display_content,
            'announcement_title': row.announcement_title,
            'created_at': row.created_at.isoformat(),
            'relevance': row.rank,
        }
        for row in responses
    ])

    # 按相关性排序
    all_results.sort(key=lambda x: x['relevance'], reverse=True)

    return {
        'query': q,
        'total_count': len(all_results),
        'results': all_results,
    }
