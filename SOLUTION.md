# 🎯 小红书热点追踪完整解决方案

## 📋 问题分析

小红书没有公开API，获取热点数据有三种方案：

| 方案 | 优点 | 缺点 | 推荐度 |
|:---:|:---:|:---:|:---:|
| **方案1: Playwright浏览器自动化** | 数据完整准确、可获取热搜榜和垂直搜索 | 需要浏览器、速度慢、易被检测 | ⭐⭐⭐⭐⭐ |
| **方案2: 第三方API聚合** | 快速、无需浏览器 | 数据源不稳定、可能收费 | ⭐⭐⭐ |
| **方案3: 手动爬虫** | 轻量级 | 容易被反爬、维护成本高 | ⭐⭐ |

---

## ✅ 已部署方案

### 1️⃣ 抖音 + 微博热点（已完成）
```bash
python3 ~/.qclaw/workspace/hotspot-tracker/hotspot_tracker.py
```
- ✅ 每日自动执行（9:00 AM）
- ✅ 9大行业自动匹配
- ✅ 跨平台热度聚合

### 2️⃣ 小红书热点（Playwright方案）
```bash
python3 ~/.qclaw/workspace/hotspot-tracker/xiaohongshu_scraper.py
```

**功能：**
- 📱 热搜榜抓取（Top 20）
- 🔍 垂直行业搜索（每行业2个关键词）
- 👤 素人爆款发现（低粉高赞）
- 📊 行业热点分类

**执行时间：** ~3-5分钟（首次较慢）

---

## 🚀 快速开始

### 方式1: 一键执行全平台
```bash
python3 ~/.qclaw/workspace/hotspot-tracker/run_all.py
```

### 方式2: 单独执行小红书
```bash
python3 ~/.qclaw/workspace/hotspot-tracker/xiaohongshu_scraper.py
```

### 方式3: 定时任务（推荐）
```bash
# 每天 10:00 执行小红书抓取
cron add --schedule "0 10 * * *" --task "python3 ~/.qclaw/workspace/hotspot-tracker/xiaohongshu_scraper.py"
```

---

## 📊 输出格式

### 小红书报告结构
```json
{
  "generated_at": "2026-03-26T13:19:00",
  "hot_search": {
    "platform": "小红书",
    "data": [
      {
        "rank": 1,
        "title": "春日穿搭",
        "platform": "小红书"
      }
    ]
  },
  "industry_results": {
    "美妆": [
      {
        "title": "口红试色",
        "keyword": "口红试色",
        "likes": "2.5万",
        "industry": "美妆"
      }
    ],
    "服装": [...],
    "数码": [...]
  }
}
```

---

## 🎬 内容创意建议流程

### 第1步: 数据融合
```
抖音热点 + 微博热点 + 小红书热点
        ↓
    行业匹配
        ↓
  跨平台热度排序
```

### 第2步: 素人爆款分析
```
小红书低粉高赞笔记
        ↓
    提取内容结构
        ↓
  分析视频/文案/配图
        ↓
  生成复刻建议
```

### 第3步: 创意建议生成
```
热点话题 + 行业特性 + 素人爆款
        ↓
  AI生成内容创意
        ↓
  输出选题/文案/视频方向
```

---

## 💡 使用示例

### 示例1: 美妆行业
```
抖音热点: "人人都是粉彩生活家"
小红书热点: "春日粉彩妆容"
微博热点: "颖儿进组前做热玛吉"

建议:
✅ 选题: 春日粉彩妆容教程 + 医美护肤对比
✅ 文案: "粉彩妆容 vs 医美护肤，哪个更显气质？"
✅ 素人爆款: 找低粉美妆博主做联合推广
```

### 示例2: 数码行业
```
抖音热点: "华为千元新机怎么选"
小红书热点: "手机测评"
微博热点: "伊朗AI视频"

建议:
✅ 选题: 千元手机对比测评 + AI功能演示
✅ 文案: "千元手机AI功能大对比"
✅ 素人爆款: 邀请数码博主开箱测评
```

---

## 🔧 配置调整

### 修改执行时间
编辑 `hotspot_tracker.py` 中的 `INDUSTRY_KEYWORDS` 字典，添加/删除行业

### 修改搜索关键词
编辑 `xiaohongshu_scraper.py` 中的 `INDUSTRY_SEARCH` 字典

### 修改抓取数量
```python
# 修改这行
hot_elements = await self.page.query_selector_all(...)[:20]  # 改为 [:50]
```

---

## ⚠️ 常见问题

### Q: 小红书抓取超时？
A: 小红书反爬较强，首次可能需要5-10分钟。建议：
- 增加 `wait_until='networkidle'` 的超时时间
- 添加随机延迟 `await asyncio.sleep(random.randint(1, 3))`

### Q: 如何避免被检测？
A: 脚本已内置反检测：
- 禁用 webdriver 标志
- 随机 User-Agent
- 随机延迟请求

### Q: 能否获取小红书评论/互动数据？
A: 可以，修改 `xiaohongshu_scraper.py` 中的选择器：
```python
# 添加这段代码
comments = await note.query_selector('.comment-count')
likes = await note.query_selector('.like-count')
```

---

## 📈 下一步优化

- [ ] 集成 Claude/GPT 生成创意文案
- [ ] 自动生成视频脚本
- [ ] 素人KOL自动匹配推荐
- [ ] 实时监控竞品热点
- [ ] 定时推送到企业微信/钉钉

---

## 📁 文件清单

```
~/.qclaw/workspace/hotspot-tracker/
├── hotspot_tracker.py          # 抖音+微博热点
├── xiaohongshu_scraper.py      # 小红书热点（Playwright）
├── xiaohongshu_lite.py         # 小红书热点（轻量级）
├── run_all.py                  # 一键执行脚本
├── SOLUTION.md                 # 本文档
└── report_*.json               # 历史报告
```

---

**需要帮助？** 随时问我！
