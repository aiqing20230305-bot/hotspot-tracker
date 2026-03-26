#!/usr/bin/env python3
"""
🚀 热点追踪系统 - 智能进化版 v2.1
功能升级：
1. 每个客户生成3个选题（可扩展更多）
2. 一键生成视频脚本
3. 智能脚本生成器（分镜+文案+BGM建议）
"""

import asyncio
import json
import os
import sys
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

@dataclass
class ContentIdea:
    """内容选题"""
    title: str
    platform: str
    format: str
    angle: str
    hot_topic: str
    cta: str
    estimated_engagement: str
    script: Optional[Dict] = None

@dataclass
class ClientContent:
    """客户内容包"""
    industry: str
    brand: str
    priority: int
    ideas: List[ContentIdea]

class ScriptGenerator:
    """视频脚本生成器"""
    
    @staticmethod
    def generate_script(title: str, platform: str, product: str, angle: str, hot_topic: str) -> Dict:
        """生成视频脚本"""
        if platform == "抖音":
            return ScriptGenerator._generate_douyin_script(title, product, angle, hot_topic)
        elif platform == "小红书":
            return ScriptGenerator._generate_xiaohongshu_script(title, product, angle, hot_topic)
        elif platform == "B站":
            return ScriptGenerator._generate_bilibili_script(title, product, angle, hot_topic)
        else:
            return ScriptGenerator._generate_default_script(title, product, angle, hot_topic)
    
    @staticmethod
    def _generate_douyin_script(title: str, product: str, angle: str, hot_topic: str) -> Dict:
        """生成抖音脚本"""
        scripts = {
            "产品测评": {
                "duration": "30秒",
                "scenes": [
                    {"time": "0-3秒", "content": f"痛点引入：你是不是也在为{hot_topic}纠结？", "visual": "困惑表情+产品特写"},
                    {"time": "3-8秒", "content": f"产品展示：今天测评{product}", "visual": "产品360度展示"},
                    {"time": "8-20秒", "content": "核心卖点：快速展示3个优点", "visual": "使用场景+效果对比"},
                    {"time": "20-25秒", "content": "真实体验：亲测XX天，效果XXX", "visual": "前后对比图"},
                    {"time": "25-30秒", "content": "CTA：你用过吗？评论区分享", "visual": "手持产品+引导关注"}
                ],
                "bgm": "热门卡点音乐（节奏感强）",
                "text_overlay": ["痛点问题", "产品名称", "核心卖点1", "核心卖点2", "核心卖点3", "实测效果"],
                "hook": f"{hot_topic}？看完这篇不踩坑！"
            },
            "使用教程": {
                "duration": "45秒",
                "scenes": [
                    {"time": "0-3秒", "content": f"问题引入：{hot_topic}很多人做错了", "visual": "错误示范"},
                    {"time": "3-10秒", "content": f"正确方法：用{product}只需3步", "visual": "步骤分解"},
                    {"time": "10-30秒", "content": "详细演示：Step1...Step2...Step3...", "visual": "分步骤展示"},
                    {"time": "30-40秒", "content": "效果展示：看看这效果", "visual": "前后对比"},
                    {"time": "40-45秒", "content": "CTA：学会了吗？评论区交作业", "visual": "成品展示+引导"}
                ],
                "bgm": "轻快节奏音乐",
                "text_overlay": ["错误做法❌", "正确做法✅", "Step 1", "Step 2", "Step 3", "最终效果"],
                "hook": f"{hot_topic}的正确打开方式！"
            }
        }
        return scripts.get(angle, scripts.get("产品测评", {"duration": "30秒", "scenes": []}))
    
    @staticmethod
    def _generate_xiaohongshu_script(title: str, product: str, angle: str, hot_topic: str) -> Dict:
        """生成小红书脚本"""
        return {
            "format": "图文笔记",
            "cover": f"{product}真实测评 | 不吹不黑",
            "structure": [
                {"section": "标题", "content": title},
                {"section": "开篇", "content": f"最近{hot_topic}很火，必须给大家测评一下{product}"},
                {"section": "产品展示", "content": "产品外观+细节图（3-5张）"},
                {"section": "使用感受", "content": "优点：XXX\n缺点：XXX\n适合人群：XXX"},
                {"section": "效果对比", "content": "使用前后对比图"},
                {"section": "总结", "content": "值得买吗？我的建议是XXX"},
                {"section": "CTA", "content": "你用过吗？评论区聊聊~"}
            ],
            "tags": [f"#{hot_topic}", f"#{product}", "#测评", "#真实体验"],
            "image_count": "6-9张"
        }
    
    @staticmethod
    def _generate_bilibili_script(title: str, product: str, angle: str, hot_topic: str) -> Dict:
        """生成B站脚本"""
        return {
            "duration": "5-8分钟",
            "structure": [
                {"time": "0-30秒", "section": "片头", "content": f"开场白+{hot_topic}引入"},
                {"time": "30秒-1分", "section": "问题背景", "content": f"为什么{hot_topic}很重要？"},
                {"time": "1-3分", "section": "产品介绍", "content": f"{product}详细介绍"},
                {"time": "3-5分", "section": "实测环节", "content": "真实使用场景测试"},
                {"time": "5-6分", "section": "优缺点总结", "content": "客观分析优缺点"},
                {"time": "6-7分", "section": "购买建议", "content": "适合谁？不值得谁买？"},
                {"time": "7-8分", "section": "片尾", "content": "总结+关注引导"}
            ],
            "bgm": "轻音乐",
            "cover_design": "标题大字+产品图"
        }
    
    @staticmethod
    def _generate_default_script(title: str, product: str, angle: str, hot_topic: str) -> Dict:
        return {"duration": "30-60秒", "tips": "根据平台特点调整"}

# 客户数据库
CLIENT_DATABASE = {
    "3C数码": {"brand": "荣耀海外/罗技/荣耀中国", "sku_count": 53, "priority": 5, 
               "content_angles": ["产品测评", "选购指南", "科技热点"], "platforms": ["抖音", "小红书", "B站"], "products": ["荣耀手机", "罗技键鼠"]},
    "快消": {"brand": "舒适/清扬/AHC/多芬/力士", "sku_count": 7, "priority": 5,
            "content_angles": ["产品测评", "使用教程", "场景植入"], "platforms": ["小红书", "抖音"], "products": ["AHC水乳", "多芬沐浴露", "力士洗发水"]},
    "家庭清洁": {"brand": "HC", "sku_count": 15, "priority": 4,
                "content_angles": ["清洁教程", "效果展示", "好物推荐"], "platforms": ["抖音", "小红书"], "products": ["HC清洁剂", "HC除菌喷雾"]},
    "保健品": {"brand": "汤臣倍健", "sku_count": 1, "priority": 5,
              "content_angles": ["科普知识", "养生攻略", "产品推荐"], "platforms": ["小红书", "抖音"], "products": ["汤臣倍健维C", "汤臣倍健蛋白粉"]},
    "宠物食品": {"brand": "通用磨坊/希宝", "sku_count": 2, "priority": 3,
               "content_angles": ["萌宠日常", "喂养攻略", "产品测评"], "platforms": ["小红书", "抖音"], "products": ["希宝罐头", "通用磨坊猫粮"]},
    "食品饮料": {"brand": "家乐", "sku_count": 1, "priority": 3,
               "content_angles": ["美食教程", "快手菜", "场景植入"], "platforms": ["抖音", "小红书"], "products": ["家乐调味料", "家乐汤底"]},
    "电池": {"brand": "传应/南孚/益圆", "sku_count": 3, "priority": 3,
            "content_angles": ["产品测评", "使用场景", "对比测试"], "platforms": ["抖音", "小红书"], "products": ["传应电池", "南孚聚能环"]},
    "家居用品": {"brand": "碧然德", "sku_count": 1, "priority": 3,
               "content_angles": ["产品测评", "使用教程", "场景解决"], "platforms": ["小红书", "抖音"], "products": ["碧然德净水壶"]},
    "医药": {"brand": "华润三九", "sku_count": 1, "priority": 3,
           "content_angles": ["健康科普", "用药指南", "家庭常备"], "platforms": ["小红书", "抖音"], "products": ["999感冒灵"]},
    "汽车": {"brand": "大通房车", "sku_count": 1, "priority": 2,
           "content_angles": ["生活方式", "旅行攻略", "产品体验"], "platforms": ["小红书", "抖音"], "products": ["大通房车"]},
    "互联网金融": {"brand": "度小满", "sku_count": 1, "priority": 2,
                 "content_angles": ["理财科普", "产品推荐", "避坑指南"], "platforms": ["B站", "小红书"], "products": ["度小满理财"]},
    "宠物服务": {"brand": "宠胖胖", "sku_count": 1, "priority": 2,
               "content_angles": ["APP教程", "服务推荐", "萌宠社交"], "platforms": ["抖音", "小红书"], "products": ["宠胖胖APP"]},
}

class HotspotEvolutionSystem:
    """热点追踪进化系统"""
    
    def __init__(self):
        self.workspace = Path("/Users/zhangjingwei/.qclaw/workspace/hotspot-tracker")
        self.today = datetime.now().strftime("%Y%m%d")
        self.hot_topics = []
        self.client_contents = []
        
    async def fetch_all_hotspots(self):
        """抓取热点"""
        subprocess.run(["python3", str(self.workspace / "hotspot_tracker.py")], 
                      capture_output=True, cwd=str(self.workspace))
        report_files = list(self.workspace.glob(f"report_{self.today}*.json"))
        if report_files:
            with open(report_files[0], 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    async def fetch_xiaohongshu(self):
        """抓取小红书"""
        subprocess.run(["python3", str(self.workspace / "xiaohongshu_enhanced.py")],
                      capture_output=True, cwd=str(self.workspace))
        report_files = list(self.workspace.glob(f"xiaohongshu_detailed_{self.today}*.json"))
        if report_files:
            with open(report_files[0], 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def match_hot_topics(self, industry):
        """匹配热点"""
        keywords = {
            "3C数码": ["科技", "数码", "手机", "AI", "机器狼"],
            "快消": ["护肤", "美妆", "妆容", "穿搭"],
            "家庭清洁": ["清洁", "家电", "焕新"],
            "保健品": ["健康", "养生", "健身", "心血管"],
            "宠物食品": ["宠物", "猫咪", "萌宠"],
            "食品饮料": ["美食", "减脂", "养生食谱"],
            "电池": ["数码", "续航", "电池"],
            "家居用品": ["家居", "家电", "净水"],
            "医药": ["健康", "药品", "感冒"],
            "汽车": ["汽车", "新能源", "房车"],
            "互联网金融": ["理财", "金融", "消费"],
            "宠物服务": ["宠物", "APP", "服务"],
        }
        
        matched = []
        for topic in self.hot_topics:
            if any(kw in topic.get("title", "") for kw in keywords.get(industry, [])):
                matched.append(topic)
        return matched[:3] if matched else self.hot_topics[:3]
    
    def generate_client_content(self, industry, client_data, hot_topics):
        """生成客户内容"""
        ideas = []
        angles = client_data["content_angles"]
        platforms = client_data["platforms"]
        products = client_data["products"]
        
        for i in range(3):
            angle = angles[i % len(angles)]
            platform = platforms[i % len(platforms)]
            product = products[i % len(products)]
            hot_topic = hot_topics[i % len(hot_topics)] if hot_topics else {"title": "热门话题", "hot_value": 1000000}
            
            title = self._generate_title(product, hot_topic.get("title", ""), angle, platform)
            cta = self._generate_cta(angle)
            estimated = self._estimate_engagement(platform, client_data["priority"])
            script = ScriptGenerator.generate_script(title, platform, product, angle, hot_topic.get("title", ""))
            
            ideas.append(ContentIdea(title, platform, self._get_format(platform), angle, 
                                    hot_topic.get("title", ""), cta, estimated, script))
        
        return ClientContent(industry, client_data["brand"], client_data["priority"], ideas)
    
    def _generate_title(self, product, hot_topic, angle, platform):
        templates = {
            "抖音": {"产品测评": f"《{hot_topic}？{product}真实测评》", "使用教程": f"《{hot_topic}教程，{product}教你》"},
            "小红书": {"产品测评": f"《{hot_topic}｜{product}测评》", "使用教程": f"《{hot_topic}｜{product}教程》"},
            "B站": {"产品测评": f"《【测评】{hot_topic}？{product}测试》", "选购指南": f"《【指南】{hot_topic}，{product}值得买吗？》"}
        }
        return templates.get(platform, {}).get(angle, f"《{hot_topic} - {product}》")
    
    def _generate_cta(self, angle):
        ctas = {"产品测评": "你用过吗？评论区分享", "使用教程": "学会了吗？评论区交作业", "场景植入": "评论区聊聊"}
        return ctas.get(angle, "评论区见")
    
    def _get_format(self, platform):
        return {"抖音": "短视频", "小红书": "图文/视频", "B站": "中长视频"}.get(platform, "图文")
    
    def _estimate_engagement(self, platform, priority):
        base = {"抖音": 10000, "小红书": 5000, "B站": 3000}
        return f"{int(base.get(platform, 1000) * priority / 3):,}+"
    
    async def run(self):
        """运行"""
        print("=" * 70)
        print("🚀 热点追踪进化系统 v2.1")
        print("=" * 70)
        
        hotspots = await self.fetch_all_hotspots()
        xiaohongshu = await self.fetch_xiaohongshu()
        
        # 整理热点
        self._organize_hot_topics(hotspots, xiaohongshu)
        
        print("\n🤖 为每个客户生成3个选题+视频脚本...")
        for industry, client_data in CLIENT_DATABASE.items():
            hot_topics = self.match_hot_topics(industry)
            client_content = self.generate_client_content(industry, client_data, hot_topics)
            self.client_contents.append(client_content)
            print(f"  ✅ {industry} - 3个选题已生成")
        
        report = self.generate_report()
        self._save_data(report)
        
        print(f"\n✅ 完成！共生成 {len(self.client_contents)} 个客户 × 3 = {len(self.client_contents) * 3} 个选题")
        return report
    
    def _organize_hot_topics(self, hotspots, xiaohongshu):
        """整理热点"""
        all_topics = []
        
        if "platforms" in hotspots:
            if "douyin" in hotspots["platforms"]:
                for item in hotspots["platforms"]["douyin"].get("data", [])[:20]:
                    all_topics.append({"title": item.get("title", ""), "hot_value": item.get("hot_value", 0), "platform": "抖音"})
            if "weibo" in hotspots["platforms"]:
                for item in hotspots["platforms"]["weibo"].get("data", [])[:20]:
                    all_topics.append({"title": item.get("title", ""), "hot_value": item.get("hot_value", 0), "platform": "微博"})
        
        if "hot_list" in xiaohongshu:
            for item in xiaohongshu["hot_list"][:10]:
                all_topics.append({"title": item.get("title", ""), "hot_value": item.get("hot_value", 0) // 1000, "platform": "小红书"})
        
        all_topics.sort(key=lambda x: x["hot_value"], reverse=True)
        self.hot_topics = all_topics
        
        print(f"\n📊 抓取 {len(all_topics)} 条热点")
        for i, topic in enumerate(all_topics[:3], 1):
            print(f"  {i}. {topic['platform']} | {topic['title'][:30]}... | {topic['hot_value']:,}")
    
    def generate_report(self):
        """生成报告"""
        today_str = datetime.now().strftime("%Y年%m月%d日")
        
        report = f"# 📱 智能内容推荐日报 - {today_str}\n\n"
        report += "> 🤖 热点追踪进化系统 v2.1 自动生成\n"
        report += "> 🎯 每个客户3个选题 + 视频脚本\n\n"
        report += "---\n\n## 🔥 今日热点TOP5\n\n"
        
        for i, topic in enumerate(self.hot_topics[:5], 1):
            report += f"{i}. **{topic['platform']}** | {topic['title'][:40]} | {topic['hot_value']:,}\n"
        
        # 按优先级分组
        high = [c for c in self.client_contents if c.priority >= 4]
        mid = [c for c in self.client_contents if c.priority == 3]
        low = [c for c in self.client_contents if c.priority <= 2]
        
        report += "\n---\n\n## 🔴 高优先级客户\n\n"
        for client in high:
            report += self._generate_client_section(client)
        
        report += "\n---\n\n## 🟡 中优先级客户\n\n"
        for client in mid:
            report += self._generate_client_section(client)
        
        report += "\n---\n\n## 🟢 低优先级客户\n\n"
        for client in low:
            report += self._generate_client_section(client)
        
        report += f"\n---\n\n*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}* | *系统版本: v2.1*\n"
        return report
    
    def _generate_client_section(self, client):
        """生成客户区块"""
        section = f"### {client.industry} - {client.brand}\n\n"
        for i, idea in enumerate(client.ideas, 1):
            section += f"**选题{i}：** {idea.title}\n"
            section += f"- 平台：{idea.platform} | 形式：{idea.format} | 角度：{idea.angle}\n"
            section += f"- 借势：{idea.hot_topic} | 预估：{idea.estimated_engagement}\n"
            section += f"- CTA：{idea.cta}\n"
            if idea.script:
                section += f"- 📹 **视频脚本：** （已生成，见JSON数据）\n"
            section += "\n"
        return section
    
    def _save_data(self, report):
        """保存数据"""
        # 保存Markdown报告
        report_file = self.workspace / f"DAILY_REPORT_{self.today}.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        # 保存JSON数据
        json_data = {
            "generated_at": datetime.now().isoformat(),
            "hot_topics": self.hot_topics[:10],
            "clients": [
                {
                    "industry": c.industry,
                    "brand": c.brand,
                    "priority": c.priority,
                    "ideas": [
                        {"title": i.title, "platform": i.platform, "angle": i.angle, 
                         "hot_topic": i.hot_topic, "script": i.script}
                        for i in c.ideas
                    ]
                }
                for c in self.client_contents
            ]
        }
        json_file = self.workspace / f"daily_data_{self.today}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 报告已保存: {report_file}")
        print(f"💾 数据已保存: {json_file}")

async def main():
    system = HotspotEvolutionSystem()
    report = await system.run()
    print("\n" + "=" * 70)
    print("报告预览（前1500字符）：")
    print("=" * 70)
    print(report[:1500])

if __name__ == "__main__":
    asyncio.run(main())
