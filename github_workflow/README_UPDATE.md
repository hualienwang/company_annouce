# 更新项目 README.md 添加徽章说明

## 在项目根目录的 README.md 中添加以下内容

### 1. 在标题下方添加徽章

```markdown
# 公司公告与意见收集系统

[![CI](https://github.com/your-username/your-repo/actions/workflows/ci.yml/badge.svg)](https://github.com/your-username/your-repo/actions/workflows/ci.yml)
[![Docker Build](https://github.com/your-username/your-repo/actions/workflows/docker-build.yml/badge.svg)](https://github.com/your-username/your-repo/actions/workflows/docker-build.yml)
[![Code Quality](https://github.com/your-username/your-repo/actions/workflows/code-quality.yml/badge.svg)](https://github.com/your-username/your-repo/actions/workflows/code-quality.yml)
[![Dependency Check](https://github.com/your-username/your-repo/actions/workflows/dependency-check.yml/badge.svg)](https://github.com/your-username/your-repo/actions/workflows/dependency-check.yml)
```

**重要**: 记得将 `your-username/your-repo` 替换为你的实际仓库路径！

### 2. 在项目简介后添加 CI/CD 章节

```markdown
## 🔄 CI/CD

本项目使用 GitHub Actions 实现自动化 CI/CD 流程：

- ✅ **持续集成**: 自动运行测试和代码检查
- 🐳 **Docker 构建**: 自动构建和推送 Docker 镜像
- 🚀 **自动部署**: 自动部署到 Render.com
- 🔍 **代码质量**: 自动分析代码质量
- 🔒 **安全扫描**: 自动扫描安全漏洞

详见 [GitHub Actions 文档](.github/README.md)。
```

### 3. 在贡献指南中添加说明

```markdown
## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发流程

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

### 提交前检查

- [ ] 代码通过本地测试
- [ ] 代码格式符合规范
- [ ] 更新了相关文档
- [ ] 添加了必要的测试
- [ ] GitHub Actions CI 通过

### 使用模板

- [Bug 报告](.github/ISSUE_TEMPLATE/bug_report.md)
- [功能请求](.github/ISSUE_TEMPLATE/feature_request.md)
- [问题咨询](.github/ISSUE_TEMPLATE/question.md)
- [Pull Request](.github/pull_request_template.md)
```

## 完整示例

```markdown
# 公司公告与意见收集系统

基于 Vue3 + FastAPI + SQLModel + PostgreSQL 的公司内部公告和意见收集平台

[![CI](https://github.com/your-username/your-repo/actions/workflows/ci.yml/badge.svg)](https://github.com/your-username/your-repo/actions/workflows/ci.yml)
[![Docker Build](https://github.com/your-username/your-repo/actions/workflows/docker-build.yml/badge.svg)](https://github.com/your-username/your-repo/actions/workflows/docker-build.yml)
[![Code Quality](https://github.com/your-username/your-repo/actions/workflows/code-quality.yml/badge.svg)](https://github.com/your-username/your-repo/actions/workflows/code-quality.yml)
[![Dependency Check](https://github.com/your-username/your-repo/actions/workflows/dependency-check.yml/badge.svg)](https://github.com/your-username/your-repo/actions/workflows/dependency-check.yml)

## 📋 功能特性

- ✅ 公告发布和管理
- ✅ 意见询问和收集
- ✅ 回复功能（支持公告和意见询问）
- ✅ 查看同事的所有回复
- ✅ 文件上传和下载
- ✅ 用户认证和权限管理
- ✅ 站内信通知
- ✅ 富文本编辑
- ✅ 文件在线预览
- ✅ 全文搜索

## 🚀 快速开始

### 环境要求

- Python 3.12+
- Node.js 20+
- PostgreSQL 15+ 或 SQLite

### 本地开发

1. 克隆仓库
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

2. 后端启动
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

3. 前端启动
```bash
cd frontend
npm install
npm run dev
```

## 🔄 CI/CD

本项目使用 GitHub Actions 实现自动化 CI/CD 流程：

- ✅ **持续集成**: 自动运行测试和代码检查
- 🐳 **Docker 构建**: 自动构建和推送 Docker 镜像
- 🚀 **自动部署**: 自动部署到 Render.com
- 🔍 **代码质量**: 自动分析代码质量
- 🔒 **安全扫描**: 自动扫描安全漏洞

详见 [GitHub Actions 文档](.github/README.md)。

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

详见 [贡献指南](CONTRIBUTING.md)。

## 📄 许可证

本项目采用 MIT 许可证。
```

## 替换占位符

在添加到 README.md 前，请替换以下占位符：

- `your-username/your-repo` → 你的 GitHub 用户名和仓库名

例如：
```
https://github.com/johndoe/announcement-system
```

## 验证徽章

添加徽章后，访问 README.md 查看徽章是否正常显示：

- ✅ 绿色: 通过
- ❌ 红色: 失败
- ⚪ 灰色: 未运行或跳过

点击徽章可以查看详细的 Workflow 运行日志。
