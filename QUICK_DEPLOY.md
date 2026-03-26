# 🚀 快速部署 - 只需 3 步

## 📋 你需要做的

### 步骤1️⃣: 生成 GitHub Personal Access Token

1. 访问: https://github.com/settings/tokens
2. 点击 "Generate new token" → "Generate new token (classic)"
3. 填写:
   - Token name: `hotspot-tracker-deploy`
   - Expiration: `No expiration`
   - Scopes: 勾选 `repo`
4. 点击 "Generate token"
5. **复制 token**（只显示一次！）

### 步骤2️⃣: 创建 GitHub 仓库

1. 访问: https://github.com/new
2. 填写:
   - Repository name: `hotspot-tracker`
   - Description: `Content Operations Daily Report`
   - Public (选择公开)
3. 点击 "Create repository"

### 步骤3️⃣: 告诉我信息

告诉我：
- 你的 **GitHub 用户名** (例如: zhangjingwei)
- 你的 **Personal Access Token** (刚才复制的)

---

## 🎯 然后我会执行

```bash
# 我会自动执行这个命令
git remote add origin https://YOUR_USERNAME:YOUR_TOKEN@github.com/YOUR_USERNAME/hotspot-tracker.git
git branch -M main
git push -u origin main
```

---

## ✅ 完成后

你会获得外网链接：
```
https://YOUR_USERNAME.github.io/hotspot-tracker/daily_report.html
```

---

**准备好了吗？告诉我你的用户名和 token！** 🚀
