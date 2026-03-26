# 🌐 外网部署指南 - 内容运营日报

## 🚀 快速部署方案

### 方案1️⃣: GitHub Pages（推荐 - 完全免费）

#### 步骤1: 创建 GitHub 仓库
```bash
# 1. 访问 https://github.com/new
# 2. 创建仓库名: hotspot-tracker
# 3. 选择 Public（公开）
# 4. 点击 Create repository
```

#### 步骤2: 上传文件
```bash
# 在本地执行
cd ~/.qclaw/workspace/hotspot-tracker

# 初始化 git
git init
git add daily_report.html CONTENT_OPERATIONS_DAILY_20260326.md fusion_report_20260326.json
git commit -m "Initial commit: Content Operations Daily Report"

# 添加远程仓库（替换 YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/hotspot-tracker.git

# 推送到 main 分支
git branch -M main
git push -u origin main
```

#### 步骤3: 启用 GitHub Pages
```
1. 进入仓库设置: Settings → Pages
2. Source 选择: Deploy from a branch
3. Branch 选择: main / (root)
4. 点击 Save
5. 等待 1-2 分钟
```

#### 步骤4: 获得外网链接
```
你的日报链接:
https://YOUR_USERNAME.github.io/hotspot-tracker/daily_report.html

例如:
https://zhangjingwei.github.io/hotspot-tracker/daily_report.html
```

---

### 方案2️⃣: Vercel 部署（最快 - 自动部署）

#### 步骤1: 安装 Vercel CLI
```bash
npm install -g vercel
```

#### 步骤2: 部署
```bash
cd ~/.qclaw/workspace/hotspot-tracker
vercel --prod
```

#### 步骤3: 获得外网链接
```
自动生成的链接:
https://hotspot-tracker-YOUR_NAME.vercel.app/daily_report.html
```

---

### 方案3️⃣: Netlify 部署（简单 - 拖拽上传）

#### 步骤1: 访问 Netlify
```
https://app.netlify.com/drop
```

#### 步骤2: 拖拽上传文件夹
```
将 ~/.qclaw/workspace/hotspot-tracker 文件夹拖到页面
```

#### 步骤3: 获得外网链接
```
自动生成的链接:
https://YOUR_SITE_NAME.netlify.app/daily_report.html
```

---

## 📋 推荐方案对比

| 方案 | 难度 | 速度 | 成本 | 推荐度 |
|:---:|:---:|:---:|:---:|:---:|
| GitHub Pages | ⭐ 简单 | ⭐⭐⭐ 快 | 免费 | ⭐⭐⭐⭐⭐ |
| Vercel | ⭐⭐ 中等 | ⭐⭐⭐⭐ 极快 | 免费 | ⭐⭐⭐⭐ |
| Netlify | ⭐ 简单 | ⭐⭐⭐ 快 | 免费 | ⭐⭐⭐⭐ |

---

## 🎯 我推荐使用 GitHub Pages

**原因:**
1. ✅ 完全免费，无需信用卡
2. ✅ 部署简单，只需 git push
3. ✅ 链接稳定，GitHub 可靠性高
4. ✅ 支持自动更新（每天推送新报告）
5. ✅ 可以邀请团队成员协作

---

## 🔄 自动更新流程

部署后，每天自动更新日报：

```bash
# 每天 9:30 AM 自动执行
cd ~/.qclaw/workspace/hotspot-tracker

# 1. 生成新报告
python3 hotspot_tracker.py

# 2. 更新 HTML
# (自动生成)

# 3. 推送到 GitHub
git add daily_report.html
git commit -m "Daily update: $(date +%Y-%m-%d)"
git push origin main

# 完成！外网链接自动更新
```

---

## 📱 分享链接

部署完成后，你可以：

✅ **分享给团队**
```
早上 9:30 发送链接到企业微信/钉钉
https://YOUR_USERNAME.github.io/hotspot-tracker/daily_report.html
```

✅ **分享给客户**
```
在邮件中附上链接
可直接在浏览器查看，无需下载
```

✅ **分享给管理层**
```
在周报中引用链接
支持手机/电脑查看
```

---

## 🆘 常见问题

**Q: 如何更新日报？**
A: 每天 9:30 自动生成新报告，git push 即可更新外网链接。

**Q: 如何邀请团队成员编辑？**
A: 在 GitHub 仓库 Settings → Collaborators 中添加成员。

**Q: 链接会过期吗？**
A: 不会。GitHub Pages 链接永久有效。

**Q: 如何自定义域名？**
A: GitHub Pages Settings 中配置自定义域名（需要自己的域名）。

---

## 🚀 立即开始

**选择方案 1（GitHub Pages）:**

1. 创建 GitHub 账号（如果没有）
2. 创建仓库 `hotspot-tracker`
3. 上传文件
4. 启用 GitHub Pages
5. 获得链接，分享给团队

**预计时间: 5 分钟** ⏱️

---

**需要帮助？** 告诉我你选择的方案，我来帮你一步步部署！
