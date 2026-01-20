# GitHub Actions Workflows 总结

## 📁 创建的文件

### Workflows (`.github/workflows/`)

1. **ci.yml** - 持续集成工作流
   - 后端代码检查和测试
   - 前端构建和检查
   - Docker 镜像构建测试
   - 安全扫描

2. **docker-build.yml** - Docker 构建和推送
   - 自动构建 Docker 镜像
   - 推送到 Docker Hub
   - 支持多架构

3. **deploy-render.yml** - 部署到 Render
   - 自动触发 Render 部署
   - 部署状态监控

4. **code-quality.yml** - 代码质量分析
   - Python 代码质量检查
   - JavaScript/TypeScript 检查
   - 代码复杂度分析

5. **issue-triage.yml** - Issue 分类
   - 自动添加标签
   - 欢迎新 Issue

6. **dependency-check.yml** - 依赖检查
   - Python 依赖安全检查
   - Node.js 依赖安全检查
   - 过时依赖检测

### 配置文件 (`.github/`)

1. **labeler.yml** - 自动标签配置
2. **README.md** - Workflows 文档
3. **BADGES.md** - 徽章使用指南
4. **WORKFLOWS_SUMMARY.md** - 本文件

### Issue 模板 (`.github/ISSUE_TEMPLATE/`)

1. **bug_report.md** - Bug 报告模板
2. **feature_request.md** - 功能请求模板
3. **question.md** - 问题咨询模板
4. **config.yml** - Issue 配置

### Pull Request 模板

1. **pull_request_template.md** - PR 模板

### 脚本 (`.scripts/`)

1. **setup-github-secrets.sh** - Secrets 设置脚本

---

## 🚀 快速开始

### 1. 推送到 GitHub

```bash
git add .
git commit -m "feat: 添加 GitHub Actions Workflows"
git push origin main
```

### 2. 配置 Secrets

#### 方式 1: 使用脚本（推荐）

```bash
chmod +x scripts/setup-github-secrets.sh
./scripts/setup-github-secrets.sh
```

#### 方式 2: 手动配置

1. 进入 GitHub 仓库
2. Settings → Secrets and variables → Actions
3. 添加以下 Secrets:

**Docker Hub (可选)**:
- `DOCKER_USERNAME`
- `DOCKER_PASSWORD`

**Render.com (可选)**:
- `RENDER_SERVICE_ID`
- `RENDER_API_KEY`

### 3. 触发 Workflows

推送到 `main` 分支会自动触发：

- ✅ CI 检查
- 🐳 Docker 构建
- 🚀 Render 部署（如果配置了 Secrets）
- 🔍 代码质量检查

---

## 📊 查看状态

### Actions 页面

1. 进入 GitHub 仓库
2. 点击 "Actions" 标签
3. 查看所有 Workflow 运行状态

### 添加徽章到 README.md

```markdown
# 项目名称

[![CI](https://github.com/your-username/your-repo/actions/workflows/ci.yml/badge.svg)](https://github.com/your-username/your-repo/actions/workflows/ci.yml)
[![Docker Build](https://github.com/your-username/your-repo/actions/workflows/docker-build.yml/badge.svg)](https://github.com/your-username/your-repo/actions/workflows/docker-build.yml)
[![Code Quality](https://github.com/your-username/your-repo/actions/workflows/code-quality.yml/badge.svg)](https://github.com/your-username/your-repo/actions/workflows/code-quality.yml)
[![Dependency Check](https://github.com/your-username/your-repo/actions/workflows/dependency-check.yml/badge.svg)](https://github.com/your-username/your-repo/actions/workflows/dependency-check.yml)
```

记得替换 `your-username/your-repo` 为你的实际仓库路径。

---

## 🔧 自定义配置

### 修改触发条件

编辑 `.github/workflows/*.yml` 文件中的 `on` 部分：

```yaml
on:
  push:
    branches: [ main, develop ]  # 修改触发分支
  pull_request:
    branches: [ main ]  # 修改 PR 目标分支
  schedule:
    - cron: '0 2 * * 1'  # 修改定时任务
  workflow_dispatch:  # 手动触发
```

### 修改 Python 版本

```yaml
- name: 设置 Python 环境
  uses: actions/setup-python@v5
  with:
    python-version: '3.12'  # 修改版本
```

### 修改 Node.js 版本

```yaml
- name: 设置 Node.js 环境
  uses: actions/setup-node@v4
  with:
    node-version: '20'  # 修改版本
```

---

## 📚 更多资源

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [Workflow 语法](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Action 市场](https://github.com/marketplace?type=actions)
- [本文档](./README.md)

---

## ✅ 检查清单

在提交代码前，确保：

- [ ] 代码通过本地测试
- [ ] 代码格式符合规范
- [ ] 更新了相关文档
- [ ] 添加了必要的测试
- [ ] 提交信息清晰明了

---

## 🆘 故障排查

### Workflow 失败

1. 查看 Actions 页面的详细日志
2. 检查依赖版本是否正确
3. 确认 Secrets 是否正确配置
4. 运行本地测试复现问题

### 部署失败

1. 检查 Render API Key 是否有效
2. 确认 Service ID 是否正确
3. 查看 Render 部署日志
4. 验证环境变量配置

---

## 📞 获取帮助

如果遇到问题：

1. 查看 `.github/README.md` 文档
2. 检查 Workflow 日志
3. 提交 Issue 寻求帮助
4. 在 Discussions 中讨论

---

**祝你使用愉快！** 🎉
