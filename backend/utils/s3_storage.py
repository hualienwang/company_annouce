import os
import re
import uuid
from typing import Optional
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

# 开发环境使用本地存储，生产环境可配置为使用 S3
USE_LOCAL_STORAGE = os.getenv("USE_LOCAL_STORAGE", "true").lower() == "true"
LOCAL_STORAGE_PATH = os.path.join(os.getenv("COZE_WORKSPACE_PATH", "/tmp"), "file_uploads")

# 确保本地存储目录存在
if USE_LOCAL_STORAGE and not os.path.exists(LOCAL_STORAGE_PATH):
    os.makedirs(LOCAL_STORAGE_PATH, exist_ok=True)
    print(f"创建本地存储目录: {LOCAL_STORAGE_PATH}")

try:
    from coze_coding_dev_sdk import S3Storage
    COZE_SDK_AVAILABLE = True
except ImportError:
    COZE_SDK_AVAILABLE = False
    if not USE_LOCAL_STORAGE:
        print("警告: coze-coding-dev-sdk 未安装且未启用本地存储，文件上传功能将不可用")


class S3StorageService:
    """文件存储服务（支持本地存储和 S3）"""

    def __init__(self):
        if USE_LOCAL_STORAGE:
            self.storage = None
            print(f"使用本地文件存储: {LOCAL_STORAGE_PATH}")
        elif COZE_SDK_AVAILABLE:
            self.storage = S3Storage(
                endpointUrl=os.getenv("COZE_BUCKET_ENDPOINT_URL"),
                accessKey="",
                secretKey="",
                bucketName=os.getenv("COZE_BUCKET_NAME"),
                region="cn-beijing",
            )
            print("使用 S3 对象存储")
        else:
            self.storage = None
            print("警告: 文件存储服务不可用")

    async def upload_file(
        self, file_content: bytes, file_name: str, content_type: str
    ) -> Optional[str]:
        """上传文件

        Args:
            file_content: 文件内容（bytes）
            file_name: 文件名
            content_type: MIME 类型

        Returns:
            文件在存储中的键（key），失败返回 None
        """
        try:
            if USE_LOCAL_STORAGE:
                # 使用本地存储
                safe_name = re.sub(r'[^a-zA-Z0-9._-]', "_", file_name)
                # 添加 UUID 避免文件名冲突
                unique_name = f"{uuid.uuid4().hex[:8]}_{safe_name}"
                file_path = os.path.join(LOCAL_STORAGE_PATH, unique_name)

                with open(file_path, 'wb') as f:
                    f.write(file_content)

                file_key = f"responses/{unique_name}"
                print(f"文件上传成功（本地存储）: {file_path}, key: {file_key}")
                return file_key

            elif COZE_SDK_AVAILABLE and self.storage:
                # 使用 S3 存储
                safe_name = re.sub(r'[^a-zA-Z0-9._-]', "_", file_name)
                file_key = await self.storage.uploadFile({
                    "fileContent": file_content,
                    "fileName": f"responses/{safe_name}",
                    "contentType": content_type or "application/octet-stream",
                })
                print(f"文件上传成功（S3）: {file_key}")
                return file_key

            else:
                print("文件存储服务不可用")
                return None

        except Exception as e:
            print(f"文件上传失败: {e}")
            return None

    async def generate_presigned_url(
        self, file_key: str, expire_time: int = 86400
    ) -> Optional[str]:
        """生成文件下载 URL

        Args:
            file_key: 文件在存储中的键
            expire_time: 有效期（秒），默认 24 小时

        Returns:
            下载 URL，失败返回 None
        """
        try:
            if USE_LOCAL_STORAGE:
                # 本地存储：返回后端下载接口的 URL
                # 需要通过后端 API 读取本地文件
                file_key_encoded = file_key.replace('/', '%2F')
                return f"/api/file/local/{file_key_encoded}"

            elif COZE_SDK_AVAILABLE and self.storage:
                # S3 存储：生成签名 URL
                signed_url = await self.storage.generatePresignedUrl({
                    "key": file_key,
                    "expireTime": expire_time,
                })
                return signed_url

            else:
                print("文件存储服务不可用")
                return None

        except Exception as e:
            print(f"生成下载 URL 失败: {e}")
            return None

    async def read_file(self, file_key: str) -> Optional[bytes]:
        """读取文件内容（用于本地存储）

        Args:
            file_key: 文件在存储中的键

        Returns:
            文件内容（bytes），失败返回 None
        """
        try:
            if USE_LOCAL_STORAGE:
                # 从本地文件系统读取
                # file_key 格式: responses/{unique_name}
                parts = file_key.split('/')
                if len(parts) != 2:
                    print(f"无效的 file_key 格式: {file_key}")
                    return None

                unique_name = parts[1]
                file_path = os.path.join(LOCAL_STORAGE_PATH, unique_name)

                if not os.path.exists(file_path):
                    print(f"文件不存在: {file_path}")
                    return None

                with open(file_path, 'rb') as f:
                    content = f.read()
                return content

            else:
                print("仅本地存储支持直接读取文件")
                return None

        except Exception as e:
            print(f"读取文件失败: {e}")
            return None


# 创建全局实例
s3_storage = S3StorageService()
