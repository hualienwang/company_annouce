#!/bin/bash

# GitHub Actions Workflow 验证脚本
# 检查所有 workflow 文件的语法和基本配置

set -e

echo "🔍 验证 GitHub Actions Workflows"
echo "======================================"
echo ""

WORKFLOW_DIR=".github/workflows"
VALID=true

# 检查 workflow 目录是否存在
if [ ! -d "$WORKFLOW_DIR" ]; then
    echo "❌ 错误: 未找到 workflow 目录: $WORKFLOW_DIR"
    exit 1
fi

# 检查 gh CLI 是否安装
if command -v gh &> /dev/null; then
    GH_AVAILABLE=true
else
    GH_AVAILABLE=false
    echo "⚠️  警告: 未找到 gh CLI，将跳过在线验证"
    echo ""
fi

# 遍历所有 workflow 文件
for workflow in "$WORKFLOW_DIR"/*.yml "$WORKFLOW_DIR"/*.yaml; do
    if [ -f "$workflow" ]; then
        echo "📄 检查文件: $workflow"

        # 检查 YAML 语法
        if ! python3 -c "import yaml; yaml.safe_load(open('$workflow'))" 2>/dev/null; then
            echo "  ❌ YAML 语法错误"
            VALID=false
        else
            echo "  ✅ YAML 语法正确"
        fi

        # 检查必要字段
        NAME=$(grep "^name:" "$workflow" | head -1 | cut -d: -f2 | xargs)
        if [ -z "$NAME" ]; then
            echo "  ❌ 缺少 name 字段"
            VALID=false
        else
            echo "  ✅ Workflow 名称: $NAME"
        fi

        # 检查触发条件
        if ! grep -q "^on:" "$workflow"; then
            echo "  ❌ 缺少触发条件 (on)"
            VALID=false
        else
            echo "  ✅ 包含触发条件"
        fi

        # 检查 jobs
        if ! grep -q "^jobs:" "$workflow"; then
            echo "  ❌ 缺少 jobs 定义"
            VALID=false
        else
            JOB_COUNT=$(grep "^  [a-zA-Z_-]*:" "$workflow" | grep -v "^  [a-zA-Z_-]*:$" | wc -l)
            echo "  ✅ 包含 $JOB_COUNT 个作业"
        fi

        # 使用 gh CLI 进行在线验证（如果可用）
        if [ "$GH_AVAILABLE" = true ]; then
            echo "  🔄 在线验证中..."
            if gh workflow view "$workflow" --json path,name,state 2>/dev/null; then
                echo "  ✅ Workflow 验证通过"
            else
                echo "  ⚠️  Workflow 可能未推送到 GitHub，跳过在线验证"
            fi
        fi

        echo ""
    fi
done

# 检查 labeler 配置
if [ -f ".github/labeler.yml" ]; then
    echo "📄 检查文件: .github/labeler.yml"
    if python3 -c "import yaml; yaml.safe_load(open('.github/labeler.yml'))" 2>/dev/null; then
        echo "  ✅ labeler.yml 语法正确"
    else
        echo "  ❌ labeler.yml 语法错误"
        VALID=false
    fi
    echo ""
fi

# 检查 Issue 模板
if [ -d ".github/ISSUE_TEMPLATE" ]; then
    echo "📁 检查 Issue 模板目录"
    TEMPLATE_COUNT=$(find .github/ISSUE_TEMPLATE -name "*.md" | wc -l)
    echo "  ✅ 找到 $TEMPLATE_COUNT 个 Issue 模板"
    echo ""
fi

# 总结
if [ "$VALID" = true ]; then
    echo "✅ 所有验证通过！"
    exit 0
else
    echo "❌ 发现错误，请修复后重试"
    exit 1
fi
