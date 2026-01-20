# 无法访问 localhost 时的解决方案

## 问题：浏览器显示 `localhost 拒绝连接 (ERR_CONNECTION_REFUSED)`

如果您的浏览器无法访问 `http://localhost:5000`，这里有几种解决方案：

---

## 🎯 方案选择指南

### 情况 1：浏览器无法连接，但服务正在运行

**推荐方案**：
1. **使用命令行下载**（最可靠）
2. **使用测试工具诊断**
3. **使用离线下载工具**

### 情况 2：服务可能未运行

**推荐方案**：
1. 先确认服务状态
2. 重启服务
3. 再尝试下载

### 情况 3：需要完整的项目文件

**推荐方案**：
1. 直接从沙箱下载压缩包
2. 解压到本地目录

---

## 📥 解决方案 1：命令行下载（推荐）

### Windows PowerShell
```powershell
# 切换到目标目录
cd D:\develop

# 下载项目
Invoke-WebRequest -Uri "http://localhost:5000/project.tar.gz" -OutFile "company-announcement-system.tar.gz"

# 解压
tar -xzf company-announcement-system.tar.gz
```

### Windows CMD
```cmd
cd D:\develop
curl -o company-announcement-system.tar.gz http://localhost:5000/project.tar.gz
tar -xzf company-announcement-system.tar.gz
```

### Linux / Mac
```bash
cd ~/Downloads
curl -O http://localhost:5000/project.tar.gz
tar -xzf project.tar.gz
```

---

## 🔍 解决方案 2：使用连接测试工具

### 步骤
1. 在浏览器中访问：`http://localhost:5000/test-connection.html`
   - **注意**：如果也无法访问此页面，请使用方案 1

2. 点击"测试连接"按钮
3. 查看测试结果
4. 根据结果选择：
   - 如果连接成功：点击"尝试下载"
   - 如果连接失败：查看故障排查建议

### 测试工具功能
- ✅ 测试单个地址连接
- 📊 测试多个地址（localhost, 127.0.0.1, 0.0.0.0）
- 📥 尝试直接下载项目
- 🔧 提供详细的故障排查建议

---

## 📦 解决方案 3：使用离线下载工具

### 步骤
1. 访问：`http://localhost:5000/download-offline.html`
2. 如果无法访问，从沙箱下载此文件
3. 在本地浏览器中打开 `download-offline.html`
4. 按照页面提示下载

### 离线下载工具功能
- 🔄 自动尝试下载
- 📥 手动指定服务器地址
- 📋 提供命令行下载代码
- 💡 故障排查提示

---

## 📂 解决方案 4：从沙箱直接下载

### 文件位置
```
/workspace/projects/frontend/public/project.tar.gz
```

### 文件信息
- **文件名**：project.tar.gz
- **大小**：约 147 KB
- **包含内容**：完整的项目源码

### 操作步骤
1. 在沙箱中找到上述文件
2. 使用沙箱的文件下载功能
3. 下载到本地
4. 解压到目标目录（如 `D:\develop`）

---

## 🔧 解决方案 5：故障排查

如果所有下载方案都无法使用，请尝试以下步骤：

### 1. 清除浏览器缓存
- Chrome/Edge: `Ctrl + Shift + Delete`
- Firefox: `Ctrl + Shift + Delete`
- 然后强制刷新：`Ctrl + Shift + R`

### 2. 检查代理设置
- 确保浏览器代理已禁用
- 或将 `localhost` 添加到"不使用代理"列表

### 3. 使用无痕模式
- 打开隐私/无痕窗口
- 尝试访问 `http://localhost:5000`

### 4. 检查防火墙
- Windows Defender 防火墙
- 确保允许 Python 或 uvicorn

### 5. 禁用浏览器扩展
- 特别是网络拦截类扩展
- 尝试无痕模式验证

---

## ✅ 验证服务是否运行

在沙箱中执行以下命令：

```bash
# 检查端口状态
ss -tuln | grep :5000

# 测试服务响应
curl -I http://localhost:5000

# 查看服务日志
tail -50 /workspace/projects/backend.log
```

如果服务未运行，启动服务：

```bash
cd /workspace/projects
bash .cozeproj/scripts/dev_run.sh
```

---

## 📞 仍然无法解决？

如果以上所有方案都无法使用，请提供以下信息：

1. **操作系统版本**
2. **浏览器类型和版本**
3. **错误信息完整截图**
4. **已尝试的方案**
5. **沙箱服务是否正在运行**

### 最后的手段

如果完全无法下载，可以：

1. **手动创建项目**（参考 `NO_LOCALHOST.md`）
2. **从其他来源获取代码**
3. **联系技术支持**

---

## 💡 最佳实践

1. **优先使用命令行下载**：最稳定可靠
2. **先使用测试工具诊断**：了解问题所在
3. **保持沙箱服务运行**：确保持续可用
4. **定期清理浏览器缓存**：避免缓存问题
5. **使用无痕模式测试**：排除扩展干扰

---

## 📚 相关文档

- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - 详细故障排查指南
- [NO_LOCALHOST.md](NO_LOCALHOST.md) - 无法访问时的具体方案
- [DOWNLOAD_GUIDE.md](DOWNLOAD_GUIDE.md) - 项目下载指南
- [GUIDE.md](GUIDE.md) - 项目使用指南

---

**提示**：命令行下载是最可靠的方式，推荐优先使用。
