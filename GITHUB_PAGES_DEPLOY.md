# 🚀 GitHub Pages 部署 - 一步一步指南

## 📋 前置准备

### 1️⃣ 创建 GitHub 账号（如果没有）
```
访问: https://github.com/signup
邮箱: 你的邮箱
用户名: 例如 zhangjingwei
密码: 设置强密码
```

### 2️⃣ 配置本地 Git
```bash
# 配置你的 Git 用户名和邮箱
git config --global user.name "你的名字"
git config --global user.email "你的邮箱@example.com"

# 例如:
git config --global user.name "Zhang Jingwei"
git config --global user.email "zhangjingwei@example.com"
```

---

## 🎯 部署步骤

### 步骤1️⃣: 初始化本地仓库
```bash
cd ~/.qclaw/workspace/hotspot-tracker

# 初始化 git
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: Content Operations Daily Report"
```

### 步骤2️⃣: 创建 GitHub 仓库
```
1. 访问: https://github.com/new
2. Repository name: hotspot-tracker
3. Description: Content Operations Daily Report
4. Public (选择公开)
5. 点击 "Create repository"
```

### 步骤3️⃣: 连接远程仓库并推送
```bash
# 替换 YOUR_USERNAME 为你的 GitHub 用户名
git remote add origin https://github.com/YOUR_USERNAME/hotspot-tracker.git

# 重命名分支为 main
git branch -M main

# 推送到 GitHub
git push -u origin main
```

### 步骤4️⃣: 启用 GitHub Pages
```
1. 进入仓库: https://github.com/YOUR_USERNAME/hotspot-tracker
2. 点击 Settings (设置)
3. 左侧菜单找到 "Pages"
4. Source 选择: "Deploy from a branch"
5. Branch 选择: main / (root)
6. 点击 Save
7. 等待 1-2 分钟
```

### 步骤5️⃣: 获得外网链接
```
你的日报链接:
https://YOUR_USERNAME.github.io/hotspot-tracker/daily_report.html

例如:
https://zhangjingwei.github.io/hotspot-tracker/daily_report.html
```

---

## 📱 分享链接

部署完成后，你可以：

✅ **分享给团队**
```
早上 9:30 发送到企业微信/钉钉:
https://YOUR_USERNAME.github.io/hotspot-tracker/daily_report.html
```

✅ **分享给客户**
```
在邮件中附上链接，客户可直接查看
```

✅ **分享给管理层**
```
在周报中引用链接
```

---

## 🔄 每天自动更新

部署完成后，每天自动更新日报：

```bash
# 每天 9:30 AM 自动执行
cd ~/.qclaw/workspace/hotspot-tracker

# 1. 生成新报告（自动）
# 2. 更新 HTML（自动）
# 3. 推送到 GitHub
git add daily_report.html
git commit -m "Daily update: $(date +%Y-%m-%d)"
git push origin main

# 完成！外网链接自动更新
```

---

## ❓ 常见问题

**Q: 我没有 GitHub 账号怎么办？**
A: 访问 https://github.com/signup 免费注册一个。

**Q: 如何获得 GitHub 的 Personal Access Token？**
A: 如果 git push 要求认证，访问 https://github.com/settings/tokens 生成 token。

**Q: 链接会过期吗？**
A: 不会。GitHub Pages 链接永久有效。

**Q: 如何更新日报内容？**
A: 每天 9:30 自动生成新报告，git push 即可更新外网链接。

---

## 🎯 下一步

1. ✅ 创建 GitHub 账号
2. ✅ 配置本地 Git
3. ✅ 按照步骤部署
4. ✅ 获得外网链接
5. ✅ 分享给团队

---

**需要帮助？告诉我你卡在哪一步！** 😊
