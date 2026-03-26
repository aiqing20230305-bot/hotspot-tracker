#!/usr/bin/env python3
"""
🚀 热点追踪系统 - 智能进化版 v2.0
功能：
1. 自动抓取抖音、微博、小红书热点
2. 智能匹配客户SKU
3. AI生成内容推荐
4. 自动推送到飞书/钉钉
5. 自学习优化（记录效果反馈）
"""

import asyncio
import json
import os
import sys
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

@dataclass
class ClientSKU:
    """客户SKU数据模型"""
    industry: str
    brand: str
    sku_count: int
    priority: int  # 1-5，5最高
    content_angles: List[str]  # 内容角度
    platforms: List[str]  # 主推平台
    
@dataclass
class HotTopic:
    """热点数据模型"""
    platform: str
    title: str
    hot_value: int
    industry: str
    url: str = ""
    content: str = ""
    
@dataclass
class ContentRecommendation:
    """内容推荐数据模型"""
    client: str
    industry: str
    title: str
    platform: str
    format: str
    angle: str
    cta: str
    priority: int
    hot_topic: str
    estimated_engagement: str

# 客户SKU数据库
CLIENT_DATABASE = {
    "3C数码": ClientSKU(
        industry="3C数码",
        brand="荣耀海外/罗技/荣耀中国",
        sku_count=53,
        priority=5,
        content_angles=["产品测评", "选购指南", "使用技巧", "场景展示"],
        platforms=["抖音", "小红书", "B站"]
    ),
    "快消": ClientSKU(
        industry="快消",
        brand="舒适/清扬/AHC/多芬/力士/VSL/nexxus",
        sku_count=7,
        priority=5,
        content_angles=["产品测评", "使用教程", "场景植入", "效果对比"],
        platforms=["小红书", "抖音"]
    ),
    "家庭清洁": ClientSKU(
        industry="家庭清洁",
        brand="HC",
        sku_count=15,
        priority=4,
        content_angles=["清洁教程", "效果展示", "好物推荐", "场景解决"],
        platforms=["抖音", "小红书"]
    ),
    "保健品": ClientSKU(
        industry="保健品",
        brand="汤臣倍健",
        sku_count=1,
        priority=5,
        content_angles=["科普知识", "养生攻略", "产品推荐", "健康提醒"],
        platforms=["小红书", "抖音"]
    ),
    "宠物食品": ClientSKU(
        industry="宠物食品",
        brand="通用磨坊/希宝",
        sku_count=2,
        priority=3,
        content_angles=["萌宠日常", "喂养攻略", "产品测评", "营养科普"],
        platforms=["小红书", "抖音"]
    ),
    "食品饮料": ClientSKU(
        industry="食品饮料",
        brand="家乐",
        sku_count=1,
        priority=3,
        content_angles=["美食教程", "快手菜", "场景植入", "食谱分享"],
        platforms=["抖音", "小红书"]
    ),
    "电池": ClientSKU(
        industry="电池",
        brand="传应/南孚/益圆",
        sku_count=3,
        priority=3,
        content_angles=["产品测评", "使用场景", "对比测试", "解决方案"],
        platforms=["抖音", "小红书"]
    ),
    "家居用品": ClientSKU(
        industry="家居用品",
        brand="碧然德",
        sku_count=1,
        priority=3,
        content_angles=["产品测评", "使用教程", "场景解决", "好物推荐"],
        platforms=["小红书", "抖音"]
    ),
    "医药": ClientSKU(
        industry="医药",
        brand="华润三九",
        sku_count=1,
        priority=3,
        content_angles=["健康科普", "用药指南", "家庭常备", "季节提醒"],
        platforms=["小红书", "抖音"]
    ),
    "汽车": ClientSKU(
        industry="汽车",
        brand="大通房车",
        sku_count=1,
        priority=2,
        content_angles=["生活方式", "旅行攻略", "产品体验", "场景展示"],
        platforms=["小红书", "抖音", "B站"]
    ),
    "互联网金融": ClientSKU(
        industry="互联网金融",
        brand="度小满",
        sku_count=1,
        priority=2,
        content_angles=["理财科普", "产品推荐", "避坑指南", "场景植入"],
        platforms=["B站", "小红书"]
    ),
    "宠物服务": ClientSKU(
        industry="宠物服务",
        brand="宠胖胖",
        sku_count=1,
        priority=2,
        content_angles=["APP教程", "服务推荐", "萌宠社交", "使用攻略"],
        platforms=["抖音", "小红书"]
    ),
}

# 行业关键词映射
INDUSTRY_KEYWORDS = {
    "3C数码": ["手机", "数码", "华为", "荣耀", "电脑", "耳机", "键盘", "鼠标", "科技", "智能"],
    "快消": ["护肤", "美妆", "洗护", "沐浴露", "洗发水", "护肤", "妆容", "口红", "香氛"],
    "家庭清洁": ["清洁", "打扫", "厨房", "油污", "除垢", "消毒", "整理"],
    "保健品": ["养生", "健康", "维生素", "免疫力", "护肝", "保健", "营养", "流感"],
    "宠物食品": ["宠物", "猫咪", "狗粮", "猫粮", "罐头", "美毛", "掉毛"],
    "食品饮料": ["美食", "烹饪", "食谱", "快手菜", "料理", "调味料", "便当"],
    "电池": ["电池", "续航", "智能门锁", "数码配件", "充电器"],
    "家居用品": ["家居", "净水", "饮水", "租房", "厨房", "生活"],
    "医药": ["感冒", "药品", "健康", "药箱", "预防", "医疗"],
    "汽车": ["汽车", "房车", "露营", "旅行", "新能源", "出行"],
    "互联网金融": ["理财", "投资", "金融", "消费", "省钱", "赚钱"],
    "宠物服务": ["宠物", "APP", "服务", "遛狗", "洗澡", "美容"],
}

class HotspotEvolutionSystem:
    """热点追踪进化系统"""
    
    def __init__(self):
        self.workspace = Path("/Users/zhangjingwei/.qclaw/workspace/hotspot-tracker")
        self.today = datetime.now().strftime("%Y%m%d")
        self.hot_topics: List[HotTopic] = []
        self.recommendations: List[ContentRecommendation] = []
        
    async def fetch_all_hotspots(self) -> Dict[str, Any]:
        """抓取所有平台热点"""
        print("🚀 开始抓取全平台热点...")
        
        # 执行热点抓取脚本
        result = subprocess.run(
            ["python3", str(self.workspace / "hotspot_tracker.py")],
            capture_output=True,
            text=True,
            cwd=str(self.workspace)
        )
        
        # 读取生成的报告
        report_files = list(self.workspace.glob(f"report_{self.today}*.json"))
        if report_files:
            with open(report_files[0], 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    async def fetch_xiaohongshu(self) -> Dict[str, Any]:
        """抓取小红书热点"""
        print("📱 抓取小红书热点...")
        
        result = subprocess.run(
            ["python3", str(self.workspace / "xiaohongshu_enhanced.py")],
            capture_output=True,
            text=True,
            cwd=str(self.workspace)
        )
        
        # 读取生成的报告
        report_files = list(self.workspace.glob(f"xiaohongshu_detailed_{self.today}*.json"))
        if report_files:
            with open(report_files[0], 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def match_industry(self, topic_title: str) -> List[str]:
        """智能匹配行业"""
        matched = []
        topic_lower = topic_title.lower()
        
        for industry, keywords in INDUSTRY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in topic_lower:
                    matched.append(industry)
                    break
        
        return matched if matched else ["其他"]
    
    def generate_recommendations(self, hotspots: Dict, xiaohongshu: Dict) -> List[ContentRecommendation]:
        """AI生成内容推荐"""
        recommendations = []
        
        # 合并所有热点
        all_topics = []
        
        # 抖音热点
        if "douyin" in hotspots:
            for item in hotspots["douyin"].get("data", [])[:10]:
                industries = self.match_industry(item.get("title", ""))
                all_topics.append({
                    "platform": "抖音",
                    "title": item.get("title", ""),
                    "hot_value": item.get("hot_value", 0),
                    "industries": industries
                })
        
        # 微博热点
        if "weibo" in hotspots:
            for item in hotspots["weibo"].get("data", [])[:10]:
                industries = self.match_industry(item.get("title", ""))
                all_topics.append({
                    "platform": "微博",
                    "title": item.get("title", ""),
                    "hot_value": item.get("hot_value", 0),
                    "industries": industries
                })
        
        # 小红书热点
        if "hot_list" in xiaohongshu:
            for item in xiaohongshu["hot_list"][:10]:
                industries = item.get("industries", ["其他"])
                all_topics.append({
                    "platform": "小红书",
                    "title": item.get("title", ""),
                    "hot_value": item.get("hot_value", 0) // 1000,  # 转换单位
                    "industries": industries
                })
        
        # 按热度排序
        all_topics.sort(key=lambda x: x["hot_value"], reverse=True)
        
        # 为每个客户生成推荐
        for industry, client in CLIENT_DATABASE.items():
            # 找到匹配的热点
            matched_topics = [
                t for t in all_topics 
                if industry in t["industries"] or any(kw in t["title"] for kw in INDUSTRY_KEYWORDS.get(industry, []))
            ]
            
            if not matched_topics:
                # 如果没有直接匹配，使用通用热点
                matched_topics = all_topics[:3]
            
            for i, topic in enumerate(matched_topics[:2]):  # 每个客户最多2条
                # 选择内容角度
                angle = client.content_angles[i % len(client.content_angles)]
                platform = client.platforms[i % len(client.platforms)]
                
                # 生成标题
                title = self._generate_title(client.brand, topic["title"], angle)
                
                # 生成CTA
                cta = self._generate_cta(angle)
                
                rec = ContentRecommendation(
                    client=client.brand,
                    industry=industry,
                    title=title,
                    platform=platform,
                    format=self._get_format(platform),
                    angle=angle,
                    cta=cta,
                    priority=client.priority,
                    hot_topic=topic["title"],
                    estimated_engagement=self._estimate_engagement(platform, client.priority)
                )
                recommendations.append(rec)
        
        # 按优先级排序
        recommendations.sort(key=lambda x: x.priority, reverse=True)
        return recommendations
    
    def _generate_title(self, brand: str, hot_topic: str, angle: str) -> str:
        """生成内容标题"""
        templates = {
            "产品测评": f"《{hot_topic}？{brand.split('/')[0]}真实测评，看完不踩坑》",
            "选购指南": f"《2025年{hot_topic}选购指南，{brand.split('/')[0]}篇》",
            "使用技巧": f"《{hot_topic}使用技巧，{brand.split('/')[0]}用户必看》",
            "场景展示": f"《{hot_topic}场景展示，{brand.split('/')[0]}体验分享》",
            "使用教程": f"《{hot_topic}教程，{brand.split('/')[0]}手把手教你》",
            "场景植入": f"《{hot_topic}，{brand.split('/')[0]}场景植入》",
            "效果对比": f"《{hot_topic}效果对比，{brand.split('/')[0]}实测》",
            "清洁教程": f"《{hot_topic}清洁教程，{brand.split('/')[0]}神器推荐》",
            "效果展示": f"《{hot_topic}效果展示，{brand.split('/')[0]}前后对比》",
            "好物推荐": f"《{hot_topic}好物推荐，{brand.split('/')[0]}清单》",
            "场景解决": f"《{hot_topic}解决方案，{brand.split('/')[0]}实测》",
            "科普知识": f"《{hot_topic}科普，{brand.split('/')[0]}健康指南》",
            "养生攻略": f"《{hot_topic}养生攻略，{brand.split('/')[0]}推荐》",
            "产品推荐": f"《{hot_topic}产品推荐，{brand.split('/')[0]}篇》",
            "健康提醒": f"《{hot_topic}健康提醒，{brand.split('/')[0]}提醒》",
        }
        return templates.get(angle, f"《{hot_topic} - {brand.split('/')[0]}》")
    
    def _generate_cta(self, angle: str) -> str:
        """生成CTA"""
        ctas = {
            "产品测评": "你用过这个产品吗？评论区分享体验",
            "选购指南": "你的选择是什么？评论区告诉我",
            "使用技巧": "还有什么技巧？评论区补充",
            "场景展示": "你的使用场景是什么？评论区晒图",
            "使用教程": "学会了吗？评论区交作业",
            "场景植入": "这个场景你也遇到过吗？评论区聊聊",
            "效果对比": "你觉得哪个更好？评论区投票",
            "清洁教程": "你的清洁难题是什么？评论区提问",
            "效果展示": "效果惊艳吗？评论区扣1",
            "好物推荐": "还有什么好物推荐？评论区分享",
            "场景解决": "你的解决方案是什么？评论区交流",
            "科普知识": "你还想知道什么？评论区提问",
            "养生攻略": "你的养生秘诀是什么？评论区分享",
            "产品推荐": "你会选择哪个？评论区讨论",
            "健康提醒": "你的健康习惯是什么？评论区分享",
        }
        return ctas.get(angle, "评论区见")
    
    def _get_format(self, platform: str) -> str:
        """获取内容格式"""
        formats = {
            "抖音": "短视频（15-60秒）",
            "小红书": "图文笔记/短视频",
            "B站": "中长视频（3-10分钟）",
            "微博": "图文/短视频",
        }
        return formats.get(platform, "图文")
    
    def _estimate_engagement(self, platform: str, priority: int) -> str:
        """预估互动量"""
        base = {"抖音": 10000, "小红书": 5000, "B站": 3000, "微博": 2000}
        multiplier = priority / 3
        estimated = int(base.get(platform, 1000) * multiplier)
        return f"{estimated:,}+"
    
    def generate_report(self, recommendations: List[ContentRecommendation]) -> str:
        """生成可视化报告"""
        today_str = datetime.now().strftime("%Y年%m月%d日")
        
        report = f"""# 📱 智能内容推荐日报 - {today_str}

> 🤖 由热点追踪进化系统自动生成
> 📊 数据来源：抖音 + 微博 + 小红书
> 🎯 匹配客户：12行业 / 22品牌 / 70+ SKU

---

## 🔥 今日热点TOP5

"""
        
        # 添加热点信息
        for i, topic in enumerate(self.hot_topics[:5], 1):
            report += f"{i}. **{topic.platform}** | {topic.title} | 热度: {topic.hot_value:,}\n"
        
        report += "\n---\n\n## 🎯 高优先级内容（必须执行）\n\n"
        
        # 高优先级
        high_priority = [r for r in recommendations if r.priority >= 4]
        for i, rec in enumerate(high_priority[:6], 1):
            report += f"""### {i}. {rec.industry} - {rec.client}
- **标题：** {rec.title}
- **平台：** {rec.platform}
- **形式：** {rec.format}
- **角度：** {rec.angle}
- **借势热点：** {rec.hot_topic}
- **预估互动：** {rec.estimated_engagement}
- **CTA：** {rec.cta}

"""
        
        report += "\n---\n\n## 📋 中优先级内容（建议执行）\n\n"
        
        # 中优先级
        mid_priority = [r for r in recommendations if r.priority == 3]
        for i, rec in enumerate(mid_priority[:4], 1):
            report += f"{i}. **{rec.industry}** | {rec.title} | {rec.platform}\n"
        
        report += "\n---\n\n## 📊 平台分配建议\n\n"
        
        # 统计平台分布
        platform_count = {}
        for rec in recommendations:
            platform_count[rec.platform] = platform_count.get(rec.platform, 0) + 1
        
        for platform, count in sorted(platform_count.items(), key=lambda x: x[1], reverse=True):
            report += f"- **{platform}：** {count}条内容\n"
        
        report += f"""

---

## ✅ 今日执行清单

### 🔴 高优先级（{len(high_priority)}条）
"""
        for rec in high_priority:
            report += f"- [ ] {rec.industry} - {rec.title[:30]}...\n"
        
        report += f"""
### 🟡 中优先级（{len(mid_priority)}条）
"""
        for rec in mid_priority[:6]:
            report += f"- [ ] {rec.industry} - {rec.title[:30]}...\n"
        
        report += """

---

## 💡 系统进化记录

- ✅ 自动热点抓取
- ✅ 智能行业匹配
- ✅ AI标题生成
- ✅ 优先级排序
- ✅ 平台分配优化
- 🔄 效果反馈学习（待接入）
- 🔄 自动推送飞书（待接入）

---

*生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M")}*
*系统版本：v2.0 进化版*
"""
        
        return report
    
    async def run(self):
        """运行完整流程"""
        print("=" * 60)
        print("🚀 热点追踪进化系统 v2.0")
        print("=" * 60)
        
        # 1. 抓取热点
        hotspots = await self.fetch_all_hotspots()
        xiaohongshu = await self.fetch_xiaohongshu()
        
        # 2. 生成推荐
        recommendations = self.generate_recommendations(hotspots, xiaohongshu)
        
        # 3. 生成报告
        report = self.generate_report(recommendations)
        
        # 4. 保存报告
        report_file = self.workspace / f"EVOLUTION_REPORT_{self.today}.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        # 5. 保存JSON数据
        json_file = self.workspace / f"evolution_data_{self.today}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                "generated_at": datetime.now().isoformat(),
                "recommendations": [asdict(r) for r in recommendations],
                "hotspots": hotspots,
                "xiaohongshu": xiaohongshu
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 报告已生成：{report_file}")
        print(f"✅ 数据已保存：{json_file}")
        print(f"\n📊 生成推荐：{len(recommendations)}条")
        print(f"🔴 高优先级：{len([r for r in recommendations if r.priority >= 4])}条")
        print(f"🟡 中优先级：{len([r for r in recommendations if r.priority == 3])}条")
        
        return report

async def main():
    """主函数"""
    system = HotspotEvolutionSystem()
    report = await system.run()
    print("\n" + "=" * 60)
    print("报告预览（前1000字符）：")
    print("=" * 60)
    print(report[:1000])

if __name__ == "__main__":
    asyncio.run(main())
