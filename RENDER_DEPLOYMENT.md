# Render.com 部署指南

本文档介绍如何将公司公告与意见收集系统部署到 Render.com 平台。

## 前置准备

### 1. 准备工作

- [ ] 拥有 Render.com 账号（[注册地址](https://render.com/register)）
- [ ] GitHub 账号（用于代码仓库连接）
- [ ] Gmail 账号或其他 SMTP 服务账号（用于邮件发送）
- [ ] 可选：S3 对象存储服务账号（用于文件存储）

### 2. 代码准备

确保项目包含以下文件：
- `render.yaml` - Render 部署配置文件
- `Dockerfile` - Docker 构建文件（多阶段构建）
- `backend/` - 后端代码目录
- `frontend/` - 前端代码目录
- `backend/requirements.txt` - Python 依赖
- `frontend/package.json` - 前端依赖

## 部署步骤

### 第一步：连接 GitHub 仓库

1. 登录 [Render.com](https://dashboard.render.com/)
2. 点击 **"New +"** 按钮
3. 选择 **"Web Service"**
4. 点击 **"Connect GitHub"**（首次需要授权）
5. 选择你的项目仓库
6. 选择要部署的分支（通常是 `main` 或 `master`）

### 第二步：配置部署选项

Render 会自动检测 `render.yaml` 文件，配置如下：

**Web Service 配置：**
- **Name**: `announcement-system`
- **Environment**: `Docker`（使用 Dockerfile）
- **Region**: `Oregon`（推荐）
- **Branch**: `main`

**说明：**
- Render 会使用项目根目录的 `Dockerfile` 进行构建
- Dockerfile 采用多阶段构建：先构建前端，再构建后端
- 最终镜像包含 FastAPI 服务和前端静态文件

**数据库配置：**
- **Name**: `announcement-db`
- **Database**: `PostgreSQL 16`
- **Region**: `Oregon`（与 Web Service 相同）

### 第三步：配置环境变量

部署完成后，需要配置以下环境变量：

#### 必需配置

| 变量名 | 说明 | 示例值 |
|--------|------|--------|
| `SMTP_USERNAME` | SMTP 用户名 | `your_email@gmail.com` |
| `SMTP_PASSWORD` | SMTP 密码 | `your_app_password` |
| `SMTP_FROM_EMAIL` | 发件人邮箱 | `your_email@gmail.com` |

#### 可选配置

| 变量名 | 说明 | 示例值 |
|--------|------|--------|
| `COZE_BUCKET_ENDPOINT_URL` | S3 端点 URL | `https://s3.amazonaws.com` |
| `COZE_BUCKET_NAME` | S3 存储桶名称 | `my-bucket` |

#### Gmail SMTP 配置示例

1. 登录 Gmail 账户
2. 进入 **账户设置** > **安全性**
3. 启用 **两步验证**
4. 生成 **应用专用密码**：
   - 点击"应用专用密码"
   - 选择"邮件"和"其他"
   - 输入密码名称（如 `Render-App`）
   - 复制生成的 16 位密码
5. 在 Render Dashboard 中配置：
   ```
   SMTP_SERVER: smtp.gmail.com
   SMTP_PORT: 587
   SMTP_USERNAME: your_email@gmail.com
   SMTP_PASSWORD: your_app_password
   SMTP_FROM_EMAIL: your_email@gmail.com
   ```

### 第四步：部署应用

1. 点击 **"Create Web Service"** 按钮
2. Render 会自动开始部署：
   - 拉取代码
   - 构建 Docker 镜像（多阶段构建）
     - 阶段 1: 构建前端（Node.js + npm install + npm run build）
     - 阶段 2: 安装后端依赖（Python + pip install）
     - 阶段 3: 合并镜像，启动 FastAPI 服务
   - 启动容器
   - 健康检查
3. 等待部署完成（约 5-10 分钟，Docker 构建需要更长时间）
4. 部署成功后，会显示应用 URL：`https://announcement-system.onrender.com`

**Docker 部署优势：**
- 构建环境一致，避免本地和服务器差异
- 更好的依赖管理
- 更快的热重载和部署速度
- 支持本地测试：`docker build -t announcement-system . && docker run -p 10000:10000 announcement-system`

### 第五步：验证部署

1. 访问应用 URL：`https://announcement-system.onrender.com`
2. 检查页面是否正常加载
3. 尝试注册新用户
4. 使用默认管理员账号登录：
   - 邮箱：`admin@example.com`
   - 密码：`admin123`

## 部署架构

```
┌─────────────────────────────────────────┐
│         Render.com Platform              │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────────────────────────┐   │
│  │  Web Service (announcement-     │   │
│  │  system.onrender.com)           │   │
│  │  - Docker Container              │   │
│  │  - FastAPI (Python 3.12)        │   │
│  │  - 前端静态文件 (Vue3 + Vite)    │   │
│  │  - Port: 10000                  │   │
│  └─────────────────────────────────┘   │
│           │                             │
│           │                             │
│  ┌─────────────────────────────────┐   │
│  │  PostgreSQL (announcement-db)   │   │
│  │  - Version: 16                  │   │
│  │  - Database: announcements      │   │
│  └─────────────────────────────────┘   │
│                                         │
└─────────────────────────────────────────┘
```

## 监控和维护

### 查看日志

1. 进入 Render Dashboard
2. 选择 `announcement-system` 服务
3. 点击 **"Logs"** 标签
4. 查看实时日志和历史日志

### 健康检查

Render 会定期访问 `/health` 端点检查应用状态：
- 检查间隔：30 秒
- 超时时间：10 秒
- 重试次数：3 次
- 启动宽限期：40 秒

### 数据库备份

PostgreSQL 数据库会自动备份：
- **备份频率**：每天一次
- **保留天数**：7 天
- **最大备份数**：3 个

手动备份：
1. 进入 Render Dashboard
2. 选择 `announcement-db` 数据库
3. 点击 **"Backups"** 标签
4. 点击 **"Backup Now"**

### 更新应用

**自动部署（推荐）：**
- 推送代码到 GitHub
- Render 自动检测并重新部署

**手动部署：**
1. 进入 Render Dashboard
2. 选择 `announcement-system` 服务
3. 点击 **"Manual Deploy"** > **"Clear build cache & deploy"**

## 性能优化

### Web Service 升级

| 计划 | CPU | 内存 | 带宽 | 价格 |
|------|-----|------|------|------|
| Free | 0.5 | 256MB | 100GB | $0/月 |
| Starter | 0.5 | 512MB | 100GB | $7/月 |
| Standard | 2 | 2GB | 500GB | $25/月 |
| Pro | 8 | 8GB | 1TB | $100/月 |

**建议：**
- 开发/测试：Free 或 Starter 计划
- 生产环境：Standard 或 Pro 计划
- 高流量：Pro 或 Pro-X 计划

### 数据库升级

| 计划 | 内存 | 连接数 | 存储 | 价格 |
|------|------|--------|------|------|
| Free | 256MB | 90 | 1GB | $0/月 |
| Starter | 1GB | 90 | 10GB | $7/月 |
| Standard | 2GB | 120 | 25GB | $20/月 |
| Pro | 8GB | 500 | 100GB | $100/月 |

**建议：**
- 开发/测试：Free 或 Starter 计划
- 生产环境：Standard 或 Pro 计划

## 自定义域名

### 添加自定义域名

1. 进入 Render Dashboard
2. 选择 `announcement-system` 服务
3. 点击 **"Settings"** > **"Domains"**
4. 点击 **"Add Custom Domain"**
5. 输入域名（如 `app.example.com`）

### 配置 DNS 记录

Render 会显示需要添加的 DNS 记录：

**A 记录：**
```
Type: A
Name: app
Value: 216.24.57.1
TTL: 3600
```

**CNAME 记录（推荐）：**
```
Type: CNAME
Name: app
Value: cname.render.com
TTL: 3600
```

### 自动 HTTPS

Render 会自动为自定义域名配置 SSL 证书（Let's Encrypt）。

## 故障排查

### 常见问题

**1. 部署失败**

**原因：**
- 依赖安装失败
- 构建超时
- 环境变量缺失

**解决方案：**
- 查看部署日志
- 检查 `requirements.txt` 和 `package.json`
- 增加构建超时时间（`buildTimeout`）

**2. 应用无法访问**

**原因：**
- 服务未启动
- 端口配置错误
- 健康检查失败

**解决方案：**
- 检查服务状态
- 验证 `PORT` 环境变量
- 查看应用日志

**3. 数据库连接失败**

**原因：**
- 数据库未启动
- 连接字符串错误
- 网络问题

**解决方案：**
- 检查数据库状态
- 验证 `DATABASE_URL` 环境变量
- 查看数据库日志

**4. 邮件发送失败**

**原因：**
- SMTP 配置错误
- 认证失败
- 端口被阻止

**解决方案：**
- 验证 SMTP 环境变量
- 检查应用专用密码
- 尝试不同的 SMTP 服务

### 获取帮助

- [Render 文档](https://render.com/docs)
- [Render 状态页](https://status.render.com)
- [Render 社区](https://community.render.com)
- [Render 支持](https://render.com/support)

## 成本估算

### 典型配置（月费用）

**小型应用（10-50 用户）：**
- Web Service: Starter - $7/月
- Database: Starter - $7/月
- **总计: $14/月**

**中型应用（50-200 用户）：**
- Web Service: Standard - $25/月
- Database: Standard - $20/月
- **总计: $45/月**

**大型应用（200-1000 用户）：**
- Web Service: Pro - $100/月
- Database: Pro - $100/月
- **总计: $200/月**

### 优化建议

1. **使用 Free 计划进行测试**
2. **根据实际使用量选择计划**
3. **启用自动缩放（Standard 计划及以上）**
4. **定期清理备份数据**
5. **监控资源使用情况**

## 安全建议

1. **环境变量管理**
   - 不要在代码中硬编码敏感信息
   - 使用 Render Dashboard 管理环境变量
   - 定期轮换密钥和密码

2. **数据库安全**
   - 限制数据库 IP 白名单（生产环境）
   - 定期备份数据
   - 启用 SSL 连接

3. **应用安全**
   - 启用 HTTPS（Render 自动提供）
   - 实施 CORS 策略
   - 定期更新依赖包

4. **访问控制**
   - 启用用户认证
   - 实施角色权限管理
   - 审计访问日志

## 相关文档

- [项目 README.md](./README.md)
- [Docker 部署指南](./DOCKER_DEPLOYMENT.md)
- [故障排查指南](./TROUBLESHOOTING.md)
- [快速修复指南](./QUICK_FIX.md)
- [Render.com 官方文档](https://render.com/docs)

## 联系方式

如有问题或建议，请：
- 提交 [GitHub Issue](https://github.com/your-repo/issues)
- 发送邮件至：support@example.com

---

**最后更新**: 2025-01-25
**文档版本**: 1.0.0
