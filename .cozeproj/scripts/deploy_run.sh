#!/bin/bash

# 部署环境启动脚本
# 使用生产模式启动
# 后端同时提供 API 和前端静态文件服务

# 创建日志目录
mkdir -p logs

echo "启动后端 FastAPI (端口 5000)，同时提供 API 和前端静态文件..."
nohup python -m uvicorn backend.main:app --host 0.0.0.0 --port 5000 > logs/backend.log 2>&1 &
BACKEND_PID=$!

echo "后端进程 PID: $BACKEND_PID"
echo "后端日志: logs/backend.log"

# 保存 PID 到文件
echo "$BACKEND_PID" > logs/backend.pid

echo ""
echo "========================================"
echo "服务已启动！"
echo "前端地址: http://localhost:5000"
echo "后端 API: http://localhost:5000/api"
echo "API 文档: http://localhost:5000/docs"
echo "========================================"
