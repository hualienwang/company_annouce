#!/bin/bash

# GitHub Secrets 设置脚本
# 使用 gh CLI 快速配置 GitHub Actions Secrets

set -e

echo "🚀 GitHub Actions Secrets 设置脚本"
echo "======================================"
echo ""

# 检查 gh CLI 是否安装
if ! command -v gh &> /dev/null; then
    echo "❌ 错误: 未找到 gh CLI"
    echo "请先安装 GitHub CLI: https://cli.github.com/"
    exit 1
fi

# 检查是否已登录
if ! gh auth status &> /dev/null; then
    echo "❌ 错误: 未登录 GitHub"
    echo "请先运行: gh auth login"
    exit 1
fi

# 获取当前仓库信息
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
echo "📦 当前仓库: $REPO"
echo ""

# 设置 Docker Hub Secrets
echo "🔐 设置 Docker Hub Secrets..."
read -p "输入 Docker Hub 用户名: " DOCKER_USERNAME
read -s -p "输入 Docker Hub 密码/Token: " DOCKER_PASSWORD
echo ""

gh secret set DOCKER_USERNAME -b"$DOCKER_USERNAME" -R "$REPO"
gh secret set DOCKER_PASSWORD -b"$DOCKER_PASSWORD" -R "$REPO"
echo "✅ Docker Hub Secrets 设置完成"
echo ""

# 设置 Render.com Secrets
echo "🔐 设置 Render.com Secrets..."
read -p "是否要配置 Render.com Secrets? (y/n): " SETUP_RENDER

if [ "$SETUP_RENDER" = "y" ] || [ "$SETUP_RENDER" = "Y" ]; then
    read -p "输入 Render Service ID: " RENDER_SERVICE_ID
    read -s -p "输入 Render API Key: " RENDER_API_KEY
    echo ""

    gh secret set RENDER_SERVICE_ID -b"$RENDER_SERVICE_ID" -R "$REPO"
    gh secret set RENDER_API_KEY -b"$RENDER_API_KEY" -R "$REPO"
    echo "✅ Render.com Secrets 设置完成"
    echo ""
fi

echo "🎉 所有 Secrets 设置完成！"
echo ""
echo "查看已设置的 Secrets:"
gh secret list -R "$REPO"
