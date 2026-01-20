# 连接问题排查指南

## 问题描述
浏览器显示：`localhost 拒绝连接 (ERR_CONNECTION_REFUSED)`

## 可能的原因和解决方案

### 1. 浏览器缓存问题

**症状**：服务正常运行，但浏览器显示无法连接

**解决方案**：

#### Chrome / Edge
1. 按 `Ctrl + Shift + Delete` 打开清除浏览数据
2. 选择"缓存的图片和文件"
3. 点击"清除数据"
4. 关闭所有浏览器窗口，重新打开
5. 访问 `http://localhost:5000`

#### Firefox
1. 按 `Ctrl + Shift + Delete` 打开清除最近的历史记录
2. 选择"缓存"
3. 点击"立即清除"
4. 刷新页面

#### 强制刷新
- Windows: `Ctrl + F5`
- Mac: `Cmd + Shift + R`

### 2. 防火墙或杀毒软件拦截

**症状**：本地应用被安全软件阻止

**解决方案**：

#### Windows 防火墙
1. 打开"Windows Defender 防火墙"
2. 点击"允许应用或功能通过 Windows Defender 防火墙"
3. 找到 Python 或相关应用
4. 确保"专用"和"公用"都勾选

#### 杀毒软件
1. 临时关闭杀毒软件
2. 测试是否能访问 `http://localhost:5000`
3. 如果可以，将应用添加到白名单

### 3. 代理设置问题

**症状**：浏览器通过代理无法访问本地服务

**解决方案**：

#### Chrome / Edge
1. 设置 → 系统 → 打开计算机的代理设置
2. 确保"使用代理服务器"未勾选
3. 或添加 `localhost` 到"不使用代理服务器"列表

#### Firefox
1. 设置 → 常规 → 网络设置
2. 选择"不使用代理"
3. 或在"不使用代理"中添加 `localhost`

### 4. 端口被占用

**症状**：5000 端口被其他程序占用

**解决方案**：

#### Windows
```cmd
# 查看占用 5000 端口的进程
netstat -ano | findstr :5000

# 结束占用端口的进程（替换 PID）
taskkill /PID <进程ID> /F
```

#### Mac / Linux
```bash
# 查看占用 5000 端口的进程
lsof -i :5000

# 结束占用端口的进程
kill -9 <PID>
```

### 5. 服务未启动

**症状**：沙箱服务没有正常运行

**解决方案**：

#### 检查服务状态
```bash
# 检查 5000 端口是否监听
netstat -an | findstr :5000  # Windows
ss -tuln | grep :5000        # Linux/Mac
```

#### 重启服务
```bash
# 在沙箱中执行
cd /workspace/projects
bash .cozeproj/scripts/dev_run.sh
```

### 6. IPv6/IPv4 问题

**症状**：浏览器尝试使用 IPv6 连接失败

**解决方案**：

#### 尝试不同的地址
```
http://localhost:5000
http://127.0.0.1:5000
http://0.0.0.0:5000
```

#### Windows Hosts 文件
1. 以管理员身份打开记事本
2. 打开 `C:\Windows\System32\drivers\etc\hosts`
3. 添加或确认以下行：
   ```
   127.0.0.1 localhost
   ::1 localhost
   ```
4. 保存文件

### 7. 浏览器扩展冲突

**症状**：某些浏览器扩展拦截了本地连接

**解决方案**：

1. 打开浏览器无痕/隐私模式
2. 访问 `http://localhost:5000`
3. 如果可以访问，说明是扩展问题
4. 禁用扩展，逐个排查

### 8. 系统级代理

**症状**：系统级代理影响本地访问

**解决方案**：

#### Windows
1. 设置 → 网络和 Internet → 代理
2. 关闭"使用代理服务器"
3. 关闭"自动检测设置"
4. 点击"保存"

#### Mac
1. 系统设置 → 网络
2. 选择当前网络 → 详情
3. 代理 → 取消所有勾选

## 替代访问方式

如果以上方法都无法解决，可以尝试以下替代方案：

### 方案一：使用命令行下载

如果无法访问网页，可以直接使用命令行下载项目：

#### Windows PowerShell
```powershell
# 切换到目标目录
cd D:\develop

# 下载项目
Invoke-WebRequest -Uri "http://localhost:5000/project.tar.gz" -OutFile "company-announcement-system.tar.gz"
```

#### Windows CMD
```cmd
cd D:\develop
curl -o company-announcement-system.tar.gz http://localhost:5000/project.tar.gz
```

#### Linux / Mac
```bash
cd ~/Downloads
curl -O http://localhost:5000/project.tar.gz
```

### 方案二：从沙箱复制文件

如果网络无法访问，可以直接从沙箱复制文件：

#### 查看文件位置
```bash
# 在沙箱中执行
ls -lh /workspace/projects/frontend/public/project.tar.gz
```

#### 使用沙箱的文件传输功能（如果支持）
- 下载 `/workspace/projects/frontend/public/project.tar.gz`
- 或 `/workspace/projects/frontend/dist/project.tar.gz`

### 方案三：手动创建项目

如果完全无法下载，可以手动创建项目：

1. 创建项目目录
```bash
cd D:\develop
mkdir company-announcement-system
cd company-announcement-system
```

2. 手动复制代码（从文档或其他来源）

## 验证服务是否运行

在沙箱中执行以下命令验证服务状态：

```bash
# 检查端口
ss -tuln | grep :5000

# 测试服务响应
curl -I http://localhost:5000

# 查看服务日志
tail -50 /workspace/projects/backend.log
```

## 快速诊断流程

1. **清除缓存** → 强制刷新页面
2. **检查代理** → 禁用所有代理设置
3. **尝试其他地址** → `http://127.0.0.1:5000`
4. **使用无痕模式** → 排除扩展干扰
5. **命令行测试** → 使用 curl 或 PowerShell
6. **从沙箱复制** → 绕过网络问题

## 获取更多帮助

如果问题仍未解决，请提供以下信息：

1. 操作系统版本
2. 浏览器类型和版本
3. 错误信息完整截图
4. 已尝试的解决方案

---

**提示**：大多数连接问题可以通过清除浏览器缓存和禁用代理设置解决。
