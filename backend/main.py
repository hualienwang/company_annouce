from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from pathlib import Path

# 加载环境变量（指定.env文件路径）
load_dotenv(Path(__file__).parent / ".env")

from database import init_db
from api import announcements, responses, file_preview, auth, notifications, search, files

# 创建 FastAPI 应用
app = FastAPI(
    title="公司公告与意见收集系统",
    description="基于 FastAPI + SQLModel + PostgreSQL 的公告和回复管理系统",
    version="2.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://localhost:5432", "http://localhost:3000", "http://localhost:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router)
app.include_router(search.router)
app.include_router(announcements.router)
app.include_router(responses.router)
app.include_router(file_preview.router)
app.include_router(notifications.router)
app.include_router(files.router)

# 挂载前端静态文件（用于生产环境）
frontend_dist = Path(__file__).parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="frontend")


@app.on_event("startup")
async def startup_event():
    """应用启动时初始化数据库"""
    init_db()
    print("数据库初始化完成")


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "公司公告与意见收集系统 API",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}
