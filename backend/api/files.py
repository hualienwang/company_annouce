from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response
from urllib.parse import unquote, quote
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


@router.get("/local/{path:path}")
async def download_local_file(
    path: str,
    file_name: str = Query("download", description="原始文件名（可选）"),
):
    """下载本地存储的文件"""
    if not path:
        raise HTTPException(status_code=400, detail="缺少文件key")

    # URL 解码
    file_key = unquote(path)
    decoded_file_name = unquote(file_name)

    # 读取文件内容
    file_content = await s3_storage.read_file(file_key)

    if not file_content:
        raise HTTPException(status_code=404, detail="文件不存在")

    # 处理文件名编码（支持中文）
    # 检查文件名是否包含非 ASCII 字符
    try:
        decoded_file_name.encode('ascii')
        # 文件名只包含 ASCII 字符
        content_disposition = f"attachment; filename=\"{decoded_file_name}\""
    except UnicodeEncodeError:
        # 文件名包含非 ASCII 字符，使用 RFC 5987 编码
        encoded_filename = quote(decoded_file_name, safe='')
        content_disposition = f"attachment; filename*=UTF-8''{encoded_filename}"

    # 返回文件，使用原始文件名
    return Response(
        content=file_content,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": content_disposition
        }
    )
