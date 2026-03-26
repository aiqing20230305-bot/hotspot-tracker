# 🚀 GitHub Pages 部署 - 完整方案

## ⚠️ 当前状态

✅ 本地仓库已初始化  
✅ 所有文件已提交  
❌ 需要推送到 GitHub

---

## 🎯 推送到 GitHub 的方式

### 方式1️⃣: 使用 GitHub CLI（推荐 - 最简单）

```bash
# 1. 安装 GitHub CLI
brew install gh

# 2. 登录 GitHub
gh auth login

# 3. 创建仓库并推送
cd ~/.qclaw/workspace/hotspot-tracker
gh repo create hotspot-tracker --public --source=. --remote=origin --push
```

### 方式2️⃣: 使用 HTTPS + Personal Access Token

```bash
# 1. 生成 Personal Access Token
# 访问: https://github.com/settings/tokens
# 创建新 token，勾选 "repo" 权限
# 复制 token

# 2. 推送到 GitHub
cd ~/.qclaw/workspace/hotspot-tracker

git remote add origin https://YOUR_USERNAME:YOUR_TOKEN@github.com/YOUR_USERNAME/hotspot-tracker.git
git branch -M main
git push -u origin main
```

### 方式3️⃣: 手动创建仓库后推送

```bash
# 1. 访问 https://github.com/new
# 2. 创建仓库 "hotspot-tracker"
# 3. 复制 HTTPS 链接

# 4. 推送
cd ~/.qclaw/workspace/hotspot-tracker

git remote add origin https://github.com/YOUR_USERNAME/hotspot-tracker.git
git branch -M main
git push -u origin main
```

---

## 📋 你需要提供的信息

为了完成部署，请告诉我：

1. **你的 GitHub 用户名** (例如: zhangjingwei)
2. **你的 GitHub Personal Access Token** (或者我帮你生成)

---

## 🔐 如何生成 Personal Access Token

1. 访问: https://github.com/settings/tokens
2. 点击 "Generate new token" → "Generate new token (classic)"
3. Token name: `hotspot-tracker-deploy`
4. Expiration: 选择 "No expiration" 或 "90 days"
5. Scopes: 勾选 `repo` (完整控制私有和公开仓库)
6. 点击 "Generate token"
7. **复制 token**（只显示一次！）

---

## 🚀 一键部署脚本

当你提供了用户名和 token 后，我会执行：

```bash
#!/bin/bash

GITHUB_USERNAME="YOUR_USERNAME"
GITHUB_TOKEN="YOUR_TOKEN"
REPO_NAME="hotspot-tracker"

cd ~/.qclaw/workspace/hotspot-tracker

# 添加远程仓库
git remote add origin https://${GITHUB_USERNAME}:${GITHUB_TOKEN}@github.com/${GITHUB_USERNAME}/${REPO_NAME}.git

# 推送
git branch -M main
git push -u origin main

# 启用 GitHub Pages
# (需要在 GitHub 网页上手动操作)

echo "✅ 推送完成！"
echo "🌐 你的日报链接:"
echo "https://${GITHUB_USERNAME}.github.io/${REPO_NAME}/daily_report.html"
```

---

## 📍 下一步

**选择一个方式：**

1. **方式1** - 安装 GitHub CLI（最简单）
   ```bash
   brew install gh
   gh auth login
   ```

2. **方式2** - 生成 Personal Access Token（推荐）
   - 访问 https://github.com/settings/tokens
   - 生成 token
   - 告诉我 token 和用户名

3. **方式3** - 手动创建仓库
   - 访问 https://github.com/new
   - 创建仓库
   - 告诉我仓库 URL

---

**告诉我你选择哪个方式，我来帮你完成！** 🚀
