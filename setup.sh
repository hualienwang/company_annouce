#!/bin/bash

# 快速启动脚本 - Vue3 + FastAPI 项目

set -e

echo "=========================================="
echo "公司公告系统 - 快速启动"
echo "=========================================="
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未检测到 Python3，请先安装 Python 3.8+"
    exit 1
fi
echo "✅ Python 版本: $(python3 --version)"

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 未检测到 Node.js，请先安装 Node.js"
    exit 1
fi
echo "✅ Node.js 版本: $(node --version)"

echo ""
echo "=========================================="
echo "1. 安装后端依赖"
echo "=========================================="
cd backend
pip install -r requirements.txt

# 测试数据库连接
echo ""
echo "2. 测试数据库连接"
echo "=========================================="
python3 test_db_connection.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ 数据库连接失败！"
    echo "请检查 backend/.env 文件中的 DATABASE_URL 配置"
    echo ""
    echo "示例配置："
    echo "DATABASE_URL=postgresql://用户名:密码@主机:端口/数据库名"
    exit 1
fi

cd ..

echo ""
echo "=========================================="
echo "3. 安装前端依赖"
echo "=========================================="
cd frontend
npm install

cd ..

echo ""
echo "=========================================="
echo "4. 启动服务"
echo "=========================================="
echo "后端 (FastAPI): http://localhost:5000"
echo "前端 (Vue3):     http://localhost:5173"
echo "API 文档:        http://localhost:5000/docs"
echo ""

# 启动服务
bash .cozeproj/scripts/dev_run.sh
