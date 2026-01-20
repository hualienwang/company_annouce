#!/bin/bash

# 开发环境启动脚本
# 同时启动后端 FastAPI 和前端 Vite

# 检查端口 5001 是否被占用
if lsof -Pi :5001 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "端口 5001 已被占用，尝试停止现有服务..."
    lsof -ti :5001 -sTCP:LISTEN | xargs kill -9 2>/dev/null || true
    sleep 2
fi

# 检查端口 5000 是否被占用
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "端口 5000 已被占用，尝试停止现有服务..."
    lsof -ti :5000 -sTCP:LISTEN | xargs kill -9 2>/dev/null || true
    sleep 2
fi

# 创建日志目录
mkdir -p logs

echo "启动后端 FastAPI (端口 5001)..."
nohup uvicorn backend.main:app --host 0.0.0.0 --port 5001 --reload > logs/backend.log 2>&1 &
BACKEND_PID=$!

echo "后端进程 PID: $BACKEND_PID"
echo "后端日志: logs/backend.log"

# 等待后端启动
sleep 5

echo "启动前端 Vite (端口 5000)..."
cd frontend && nohup pnpm dev > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo "前端进程 PID: $FRONTEND_PID"
echo "前端日志: logs/frontend.log"

# 保存 PID 到文件
echo "$BACKEND_PID" > logs/backend.pid
echo "$FRONTEND_PID" > logs/frontend.pid

echo ""
echo "========================================"
echo "服务已启动！"
echo "前端地址: http://localhost:5000"
echo "后端 API: http://localhost:5001"
echo "API 文档: http://localhost:5001/docs"
echo "========================================"
echo ""
echo "停止服务: bash .cozeproj/scripts/dev_stop.sh"
echo "查看日志: tail -f logs/backend.log 或 tail -f logs/frontend.log"
