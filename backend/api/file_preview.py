"""
文件预览 API 路由
提供文件预览功能
"""
from fastapi import APIRouter, HTTPException, Query
from utils.s3_storage import s3_storage

router = APIRouter(prefix="/api/file", tags=["文件"])


@router.get("/download")
async def get_download_url(
    key: str = Query(..., description="文件在S3中的键"),
):
    """获取文件下载的签名 URL"""
    if not key:
        raise HTTPException(status_code=400, detail="缺少文件key")

    # 生成签名 URL（24小时有效）
    signed_url = await s3_storage.generate_presigned_url(key, expire_time=86400)

    if not signed_url:
        raise HTTPException(status_code=500, detail="获取下载链接失败")

    return {
        "success": True,
        "url": signed_url
    }


@router.get("/preview")
async def get_preview_url(
    key: str = Query(..., description="文件在S3中的键"),
):
    """获取文件预览 URL（用于常见文件类型）"""
    if not key:
        raise HTTPException(status_code=400, detail="缺少文件key")

    # 生成签名 URL（1小时有效，用于预览）
    signed_url = await s3_storage.generate_presigned_url(key, expire_time=3600)

    if not signed_url:
        raise HTTPException(status_code=500, detail="获取预览链接失败")

    return {
        "success": True,
        "url": signed_url,
        "preview_type": get_preview_type(key)
    }


def get_preview_type(filename: str) -> str:
    """根据文件名判断预览类型"""
    filename_lower = filename.lower()

    # 图片类型
    if filename_lower.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg')):
        return 'image'

    # PDF
    if filename_lower.endswith('.pdf'):
        return 'pdf'

    # 文本类型
    if filename_lower.endswith(('.txt', '.md', '.json', '.xml', '.html', '.css', '.js', '.ts')):
        return 'text'

    # 视频类型
    if filename_lower.endswith(('.mp4', '.webm', '.ogg', '.avi', '.mov')):
        return 'video'

    # 音频类型
    if filename_lower.endswith(('.mp3', '.wav', '.ogg', '.flac', '.aac')):
        return 'audio'

    # Office 文档（需要外部服务）
    if filename_lower.endswith(('.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx')):
        return 'office'

    # 压缩文件
    if filename_lower.endswith(('.zip', '.rar', '.7z', '.tar', '.gz')):
        return 'archive'

    # 其他
    return 'unknown'
