# Render.com 部署检查清单

使用此清单确保项目已准备好部署到 Render.com。

## 📋 部署前准备

### 1. 代码准备

- [ ] 项目代码已推送到 GitHub 仓库
- [ ] `render.yaml` 文件存在于项目根目录
- [ ] 所有文件已提交到 Git（未提交的更改不会被部署）

**验证命令：**
```bash
git status
git remote -v
```

### 2. 配置文件检查

- [ ] `render.yaml` 配置正确（env: docker）
- [ ] `Dockerfile` 存在于项目根目录
- [ ] `backend/requirements.txt` 包含所有必需依赖
- [ ] `frontend/package.json` 配置正确
- [ ] `.gitignore` 排除了敏感文件（.env、node_modules 等）

**验证命令：**
```bash
cat render.yaml
cat Dockerfile
cat backend/requirements.txt
cat .gitignore
```

### 3. 本地测试

**方式一：Docker 测试（推荐）**
- [ ] Docker 镜像可以正常构建
- [ ] Docker 容器可以正常运行
- [ ] API 端点正常响应（`/health` 端点返回 `{"status": "healthy"}`）

**验证命令：**
```bash
# Docker 构建测试
docker build -t announcement-system .

# Docker 运行测试
docker run -d -p 10000:10000 announcement-system
curl http://localhost:10000/health
```

**方式二：传统测试（可选）**
- [ ] 后端可以正常启动（`uvicorn backend.main:app`）
- [ ] 前端可以正常构建（`npm run build`）
- [ ] 数据库连接正常

**验证命令：**
```bash
# 后端测试
cd backend
uvicorn main:app &
curl http://localhost:8000/health

# 前端构建测试
cd frontend
npm run build
```

### 4. SMTP 配置准备

- [ ] Gmail 账号已启用两步验证
- [ ] 已生成应用专用密码
- [ ] 准备好 SMTP 配置信息：
  - `SMTP_SERVER`: `smtp.gmail.com`
  - `SMTP_PORT`: `587`
  - `SMTP_USERNAME`: `your_email@gmail.com`
  - `SMTP_PASSWORD`: `your_app_password`（16位密码）
  - `SMTP_FROM_EMAIL`: `your_email@gmail.com`

**Gmail 应用专用密码生成：**
1. Google 账户 > 安全性 > 两步验证
2. 应用专用密码 > 生成新密码
3. 选择"邮件"和"其他"
4. 复制生成的 16 位密码

### 5. 运行预部署检查

- [ ] 运行 `pre-deploy-check.sh` 脚本
- [ ] 所有必需检查通过
- [ ] 处理所有警告信息

**验证命令：**
```bash
./pre-deploy-check.sh
```

## 🚀 部署步骤

### 1. 推送代码到 GitHub

```bash
git add .
git commit -m "准备部署到 Render"
git push origin main
```

### 2. 在 Render.com 创建服务

1. 访问 [dashboard.render.com](https://dashboard.render.com/)
2. 点击 **"New +"** > **"Web Service"**
3. 点击 **"Connect GitHub"**（首次需要授权）
4. 选择你的仓库和分支（通常是 `main`）
5. Render 会自动检测 `render.yaml` 配置
6. 点击 **"Create Web Service"**

### 3. 配置环境变量

部署完成后，在 Render Dashboard 中配置：

**必需配置：**
- `SMTP_USERNAME`: `your_email@gmail.com`
- `SMTP_PASSWORD`: `your_app_password`
- `SMTP_FROM_EMAIL`: `your_email@gmail.com`

**可选配置：**
- `COZE_BUCKET_ENDPOINT_URL`: S3 端点 URL
- `COZE_BUCKET_NAME`: S3 存储桶名称

**配置步骤：**
1. 进入 `announcement-system` 服务
2. 点击 **"Environment"** 标签
3. 点击 **"+ Add Environment Variable"**
4. 逐个添加上述环境变量
5. 点击 **"Save Changes"**

### 4. 触发重新部署

配置环境变量后，触发重新部署：

1. 点击 **"Manual Deploy"**
2. 选择 **"Clear build cache & deploy"**
3. 等待部署完成

### 5. 验证部署

- [ ] 访问应用 URL：`https://announcement-system.onrender.com`
- [ ] 页面正常加载
- [ ] 可以注册新用户
- [ ] 可以使用管理员账号登录：
  - 邮箱：`admin@example.com`
  - 密码：`admin123`
- [ ] 可以发布公告
- [ ] 可以提交回复
- [ ] 文件上传功能正常

## 🔍 部署后验证

### 1. 检查服务状态

- [ ] Web Service 状态为 `Live`
- [ ] Database 状态为 `Available`
- [ ] 无错误日志

### 2. 检查日志

1. 进入 `announcement-system` 服务
2. 点击 **"Logs"** 标签
3. 查看日志中是否有错误信息

### 3. 功能测试

- [ ] 用户注册功能正常
- [ ] 登录功能正常
- [ ] 发布公告功能正常
- [ ] 提交回复功能正常
- [ ] 文件上传功能正常
- [ ] 搜索功能正常
- [ ] 分页功能正常

### 4. 邮件功能测试

- [ ] 注册邮件发送成功
- [ ] 通知邮件发送成功
- [ ] 邮件内容正确

## 📊 监控和维护

### 日常检查

- [ ] 定期检查应用状态
- [ ] 查看应用日志
- [ ] 监控数据库连接数
- [ ] 检查磁盘使用情况

### 更新应用

- [ ] 测试代码变更
- [ ] 推送到 GitHub
- [ ] Render 自动部署
- [ ] 验证部署结果

### 数据库备份

- [ ] 确认自动备份启用
- [ ] 定期检查备份状态
- [ ] 测试备份恢复

## 🆘 故障处理

### 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 部署失败 | 依赖安装失败 | 检查 `requirements.txt` 和 `package.json` |
| 应用无法访问 | 服务未启动 | 查看应用日志 |
| 数据库连接失败 | 连接字符串错误 | 检查 `DATABASE_URL` 环境变量 |
| 邮件发送失败 | SMTP 配置错误 | 验证 SMTP 配置信息 |
| 文件上传失败 | 磁盘空间不足 | 升级磁盘容量或清理文件 |

### 获取帮助

- [故障排查指南](./TROUBLESHOOTING.md)
- [Render 文档](https://render.com/docs)
- [Render 社区](https://community.render.com)

## 📝 备注

- **首次部署时间**: 约 5-10 分钟（Docker 构建需要更长时间）
- **后续更新时间**: 约 3-5 分钟（缓存后速度会更快）
- **免费计划限制**: 256MB 内存，单实例
- **推荐计划**: Starter（$7/月，512MB 内存）
- **生产环境建议**: Standard（$25/月，2GB 内存）
- **Docker 优势**: 环境一致、依赖管理更好、本地可测试

## ✅ 完成部署

恭喜！你已成功将应用部署到 Render.com。

**下一步：**
1. 配置自定义域名（可选）
2. 启用自动缩放（Standard 计划及以上）
3. 配置监控告警
4. 设置数据库备份策略

---

**最后更新**: 2025-01-25
**检查清单版本**: 2.0.0 (Docker 部署)
