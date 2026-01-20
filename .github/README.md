# GitHub Actions Workflows 文档

本项目使用 GitHub Actions 实现自动化 CI/CD 流程。

## 工作流列表

### 1. CI (持续集成)
**文件**: `.github/workflows/ci.yml`

**触发条件**:
- 推送到 `main` 或 `develop` 分支
- 创建 Pull Request 到 `main` 或 `develop` 分支

**功能**:
- 后端代码检查（Black, Flake8, mypy）
- 后端单元测试
- 前端代码检查（ESLint, Prettier）
- 前端 TypeScript 类型检查
- 前端构建测试
- Docker 镜像构建测试
- 安全扫描（Trivy）

**作业**:
- `backend-test`: 后端测试
- `frontend-test`: 前端构建测试
- `docker-build-test`: Docker 镜像构建测试
- `security-scan`: 安全漏洞扫描

---

### 2. Docker Build and Push
**文件**: `.github/workflows/docker-build.yml`

**触发条件**:
- 推送到 `main` 分支
- 推送标签（如 `v1.0.0`）
- 手动触发

**功能**:
- 构建 Docker 镜像
- 推送到 Docker Hub
- 支持多架构（linux/amd64, linux/arm64）
- 自动生成镜像标签和摘要

**必需的 Secrets**:
- `DOCKER_USERNAME`: Docker Hub 用户名
- `DOCKER_PASSWORD`: Docker Hub 密码或 Access Token

**配置 Secrets**:
1. 进入 GitHub 仓库设置
2. Settings → Secrets and variables → Actions
3. 添加 `DOCKER_USERNAME` 和 `DOCKER_PASSWORD`

---

### 3. Deploy to Render
**文件**: `.github/workflows/deploy-render.yml`

**触发条件**:
- 推送到 `main` 分支
- 手动触发

**功能**:
- 自动触发 Render.com 部署
- 等待部署完成并验证

**必需的 Secrets**:
- `RENDER_SERVICE_ID`: Render 服务 ID
- `RENDER_API_KEY`: Render API Key

**获取 Render API Key**:
1. 登录 Render.com
2. 进入 Account Settings → API Keys
3. 创建新的 API Key

**获取 Render Service ID**:
1. 在 Render 中找到你的服务
2. Service ID 在服务页面的 URL 中（如 `srv-xxxxx`）

---

### 4. Code Quality (代码质量)
**文件**: `.github/workflows/code-quality.yml`

**触发条件**:
- 推送到 `main` 或 `develop` 分支
- 创建 Pull Request
- 每天凌晨 2 点（定时任务）

**功能**:
- Python 代码质量分析（Black, Flake8, Pylint, Bandit）
- JavaScript/TypeScript 代码质量分析（ESLint, Prettier）
- 代码复杂度分析（Radon, Lizard）

**作业**:
- `python-quality`: Python 代码质量
- `javascript-quality`: JS/TS 代码质量
- `complexity-analysis`: 代码复杂度分析

**生成报告**:
- `bandit-security-report.json`: 安全漏洞报告
- `eslint-report.json`: ESLint 报告
- `radon-report.txt`: 复杂度报告
- `lizard-report.json`: Lizard 复杂度报告

---

### 5. Issue Triage
**文件**: `.github/workflows/issue-triage.yml`

**触发条件**:
- 创建新的 Issue
- Issue 被添加/移除标签
- 创建新的 Pull Request

**功能**:
- 自动添加标签（根据 `.github/labeler.yml` 配置）
- 为新 Issue 添加欢迎评论

**标签规则**:
- `bug`: Bug 修复
- `feature`: 新功能
- `documentation`: 文档
- `backend`: 后端相关
- `frontend`: 前端相关
- `security`: 安全相关
- 等等...

---

### 6. Dependency Check
**文件**: `.github/workflows/dependency-check.yml`

**触发条件**:
- 每周一凌晨 3 点（定时任务）
- 手动触发

**功能**:
- Python 依赖安全检查（Safety, Pip Audit）
- Node.js 依赖安全检查（npm audit）
- 检测过时的依赖
- 生成依赖更新建议报告

**作业**:
- `python-dependencies`: Python 依赖检查
- `nodejs-dependencies`: Node.js 依赖检查
- `dependency-update-suggestions`: 生成更新建议

---

## 快速开始

### 1. 配置 Docker Hub（可选）

如果要自动构建和推送 Docker 镜像：

```bash
# 在 GitHub 仓库中添加 Secrets
DOCKER_USERNAME=your_dockerhub_username
DOCKER_PASSWORD=your_dockerhub_password
```

### 2. 配置 Render.com（可选）

如果要自动部署到 Render：

```bash
# 在 GitHub 仓库中添加 Secrets
RENDER_SERVICE_ID=your_render_service_id
RENDER_API_KEY=your_render_api_key
```

### 3. 本地测试 Workflow

在提交前本地测试：

```bash
# 运行后端测试
cd backend
pytest -v

# 运行前端构建
cd frontend
npm run build

# 构建 Docker 镜像
docker build -t announcement-system:test .
```

---

## Workflow 状态徽章

在 README.md 中添加这些徽章显示 Workflow 状态：

```markdown
![CI](https://github.com/your-username/your-repo/actions/workflows/ci.yml/badge.svg)
![Docker Build](https://github.com/your-username/your-repo/actions/workflows/docker-build.yml/badge.svg)
![Code Quality](https://github.com/your-username/your-repo/actions/workflows/code-quality.yml/badge.svg)
```

---

## 故障排查

### CI 失败

1. 查看失败的作业日志
2. 检查依赖是否正确安装
3. 确认代码格式是否符合规范
4. 运行本地测试复现问题

### Docker 构建失败

1. 检查 Dockerfile 语法
2. 确认依赖文件是否存在
3. 验证环境变量配置
4. 查看 Docker 构建日志

### 部署失败

1. 检查 Render API Key 是否有效
2. 确认 Service ID 是否正确
3. 查看 Render 部署日志
4. 验证环境变量配置

---

## 最佳实践

1. **频繁提交**: 小步快跑，频繁提交代码，及早发现问题
2. **编写测试**: 为新功能编写测试用例
3. **代码审查**: 提交 PR 前进行代码审查
4. **关注日志**: 定期查看 Workflow 运行日志
5. **更新依赖**: 及时更新依赖，修复安全漏洞

---

## 自定义 Workflow

如需修改 Workflow：

1. 编辑对应的 `.yml` 文件
2. 遵循 YAML 语法规范
3. 在本地测试修改
4. 提交并推送
5. 查看 Actions 页面验证

---

## 相关资源

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [Workflow 语法](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Docker Hub](https://hub.docker.com/)
- [Render.com 文档](https://render.com/docs)
