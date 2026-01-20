# Render.com 部署快速参考

## 📋 一分钟快速部署

### 1. 推送代码到 GitHub
```bash
git add .
git commit -m "Add Render deployment configuration"
git push origin main
```

### 2. 在 Render.com 创建服务
1. 登录 [dashboard.render.com](https://dashboard.render.com/)
2. New > Web Service > Connect GitHub
3. 选择仓库和分支 > 点击 "Create Web Service"

### 3. 配置环境变量（必需）
在 Render Dashboard > Environment 中配置：

```
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_FROM_EMAIL=your_email@gmail.com
```

**Gmail 应用专用密码生成：**
- Google 账户 > 安全性 > 两步验证
- 应用专用密码 > 生成并复制

### 4. 访问应用
```
https://announcement-system.onrender.com
```

**默认管理员：**
- 邮箱：`admin@example.com`
- 密码：`admin123`

---

## 📁 项目结构

```
project/
├── render.yaml              # Render 配置文件
├── Dockerfile              # Docker 构建文件（多阶段构建）
├── backend/
│   ├── main.py             # FastAPI 入口
│   ├── requirements.txt    # Python 依赖
│   └── .env               # 后端环境变量
└── frontend/
    ├── src/                # Vue 源码
    ├── package.json        # 前端依赖
    └── dist/              # 构建输出（自动生成）
```

---

## ⚙️ 关键配置

### Web Service
```yaml
type: web
name: announcement-system
env: docker  # 使用 Dockerfile
plan: starter
```

### Dockerfile（多阶段构建）
```dockerfile
# 阶段 1: 构建前端
FROM node:24-alpine AS frontend-builder
# ... 构建前端

# 阶段 2: 构建后端
FROM python:3.12-slim AS backend-builder
# ... 安装后端依赖

# 阶段 3: 合并镜像
FROM python:3.12-slim
# ... 合并前后端
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "${PORT:-10000}"]
```

### 端口配置
```
PORT: 10000（Dockerfile 中默认值）
```

### 磁盘挂载
```
路径: /app/file_uploads
容量: 1GB
```

### Database
```yaml
type: postgresql
name: announcement-db
version: "16"
plan: starter
```

---

## 🔧 环境变量说明

| 变量名 | 必需 | 说明 | 示例 |
|--------|------|------|------|
| `DATABASE_URL` | ✅ | 数据库连接串 | 自动注入 |
| `SMTP_SERVER` | ✅ | SMTP 服务器 | `smtp.gmail.com` |
| `SMTP_PORT` | ✅ | SMTP 端口 | `587` |
| `SMTP_USERNAME` | ✅ | SMTP 用户名 | `your_email@gmail.com` |
| `SMTP_PASSWORD` | ✅ | SMTP 密码 | `app_password` |
| `SMTP_FROM_EMAIL` | ✅ | 发件人邮箱 | `your_email@gmail.com` |
| `COZE_BUCKET_ENDPOINT_URL` | ❌ | S3 端点 | `https://s3.amazonaws.com` |
| `COZE_BUCKET_NAME` | ❌ | S3 存储桶 | `my-bucket` |

---

## 🚀 部署流程

```
┌─────────────┐
│  代码推送    │
│   GitHub    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Render 检测│
│  render.yaml│
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Docker 构建│
│  ├─ 前端构建│
│  ├─ 后端构建│
│  └─ 镜像合并│
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  部署完成    │
│  访问 URL   │
└─────────────┘
```

---

## 📊 监控和日志

### 查看日志
```
Render Dashboard > announcement-system > Logs
```

### 健康检查
```
URL: https://announcement-system.onrender.com/health
频率: 每 30 秒
超时: 10 秒
```

### 数据库备份
```
自动备份: 每天 1 次
保留天数: 7 天
最大备份数: 3 个
```

---

## 💰 成本估算

### 小型应用（10-50 用户）
- Web Service: Starter - $7/月
- Database: Starter - $7/月
- **总计: $14/月**

### 中型应用（50-200 用户）
- Web Service: Standard - $25/月
- Database: Standard - $20/月
- **总计: $45/月**

### 大型应用（200-1000 用户）
- Web Service: Pro - $100/月
- Database: Pro - $100/月
- **总计: $200/月**

---

## 🛠️ 常用命令

### 本地 Docker 测试（模拟 Render 环境）
```bash
# 构建 Docker 镜像
docker build -t announcement-system .

# 运行容器（模拟 Render 环境）
docker run -d \
  -p 10000:10000 \
  -e DATABASE_URL="postgresql://user:pass@host:5432/db" \
  -e PORT=10000 \
  -v $(pwd)/file_uploads:/app/file_uploads \
  announcement-system

# 查看日志
docker logs -f <container_id>

# 停止容器
docker stop <container_id>
```

### 传统方式测试（不推荐）
```bash
# 安装依赖
pip install -r backend/requirements.txt
cd frontend && npm install && npm run build

# 启动服务（模拟 Render 端口）
DATABASE_URL="postgresql://..." \
uvicorn backend.main:app --host 0.0.0.0 --port 10000
```

### 更新应用（自动部署）
```bash
git add .
git commit -m "Update application"
git push origin main
# Render 会自动重新部署
```

### 手动触发部署
```
Render Dashboard > announcement-system > Manual Deploy
```

---

## ❓ 故障排查

### 部署失败
1. 查看部署日志
2. 检查 `requirements.txt` 和 `package.json`
3. 验证环境变量配置

### 应用无法访问
1. 检查服务状态（Dashboard）
2. 查看应用日志
3. 验证 `PORT` 环境变量

### 数据库连接失败
1. 检查数据库状态
2. 验证 `DATABASE_URL`
3. 查看数据库日志

### 邮件发送失败
1. 验证 SMTP 配置
2. 检查应用专用密码
3. 尝试不同的 SMTP 服务

---

## 🔐 安全检查清单

- [ ] 使用环境变量存储敏感信息
- [ ] 启用 HTTPS（Render 自动提供）
- [ ] 配置数据库 IP 白名单
- [ ] 定期备份数据
- [ ] 更新依赖包
- [ ] 启用审计日志
- [ ] 限制 API 访问频率

---

## 📚 相关链接

- [完整部署指南](./RENDER_DEPLOYMENT.md)
- [项目 README](./README.md)
- [Docker 部署](./DOCKER_DEPLOYMENT.md)
- [故障排查](./TROUBLESHOOTING.md)
- [Render 官方文档](https://render.com/docs)
- [Render 状态页](https://status.render.com)

---

## 📞 获取帮助

- **文档**: [Render Docs](https://render.com/docs)
- **社区**: [Render Community](https://community.render.com)
- **支持**: [render.com/support](https://render.com/support)
- **GitHub Issues**: 提交问题到项目仓库

---

**提示**: 首次部署后，记得在 Render Dashboard 中配置 SMTP 环境变量！

**最后更新**: 2025-01-25
