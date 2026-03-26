#!/usr/bin/env python3
"""
👥 特赞内容运营平台 - 客户选题中心 v3.0
功能：
1. 客户选题管理
2. 智能热点匹配
3. SKU场景结合
4. 选题效果追踪
"""

import json
import asyncio
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

class Client:
    """客户数据模型"""
    def __init__(self, industry: str, brand: str, sku_count: int, priority: int, 
                 products: List[str], platforms: List[str], content_angles: List[str]):
        self.industry = industry
        self.brand = brand
        self.sku_count = sku_count
        self.priority = priority
        self.products = products
        self.platforms = platforms
        self.content_angles = content_angles
    
    def to_dict(self) -> Dict:
        return {
            "industry": self.industry,
            "brand": self.brand,
            "sku_count": self.sku_count,
            "priority": self.priority,
            "products": self.products,
            "platforms": self.platforms,
            "content_angles": self.content_angles,
            "priority_label": "高" if self.priority >= 4 else "中" if self.priority == 3 else "低"
        }

class HotTopic:
    """热点数据模型"""
    def __init__(self, platform: str, title: str, hot_value: int, category: str):
        self.platform = platform
        self.title = title
        self.hot_value = hot_value
        self.category = category
    
    def to_dict(self) -> Dict:
        return {
            "platform": self.platform,
            "title": self.title,
            "hot_value": self.hot_value,
            "category": self.category
        }

class ContentIdea:
    """选题数据模型"""
    def __init__(self, client: Client, title: str, platform: str, angle: str, 
                 hot_topic: str, script_type: str, engagement_estimate: str):
        self.client = client
        self.title = title
        self.platform = platform
        self.angle = angle
        self.hot_topic = hot_topic
        self.script_type = script_type
        self.engagement_estimate = engagement_estimate
        self.id = f"{client.industry}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.status = "pending"  # pending / in_progress / done
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "client": self.client.to_dict(),
            "title": self.title,
            "platform": self.platform,
            "angle": self.angle,
            "hot_topic": self.hot_topic,
            "script_type": self.script_type,
            "engagement_estimate": self.engagement_estimate,
            "status": self.status,
            "created_at": self.created_at
        }

class ClientContentCenter:
    """客户选题中心"""
    
    # 客户数据库
    CLIENTS = [
        Client("3C数码", "荣耀海外/罗技/荣耀中国", 53, 5, 
               ["荣耀手机", "罗技键鼠", "荣耀平板", "荣耀耳机"],
               ["抖音", "小红书", "B站"],
               ["产品测评", "选购指南", "科技热点", "使用技巧"]),
        
        Client("快消", "舒适/清扬/AHC/多芬/力士/VSL/nexxus", 7, 5,
               ["AHC水乳", "多芬沐浴露", "力士洗发水", "清扬去屑", "舒适剃须刀"],
               ["小红书", "抖音"],
               ["产品测评", "使用教程", "场景植入", "效果对比"]),
        
        Client("家庭清洁", "HC", 15, 4,
               ["HC清洁剂", "HC除菌喷雾", "HC厨房油污净", "HC多功能清洁"],
               ["抖音", "小红书"],
               ["清洁教程", "效果展示", "好物推荐", "对比测试"]),
        
        Client("保健品", "汤臣倍健", 5, 5,
               ["汤臣倍健维C", "汤臣倍健蛋白粉", "汤臣倍健辅酶Q10", "汤臣倍健护肝片"],
               ["小红书", "抖音"],
               ["科普知识", "养生攻略", "产品推荐", "成分解析"]),
        
        Client("宠物食品", "通用磨坊/希宝", 2, 3,
               ["希宝罐头", "通用磨坊猫粮", "希宝湿粮"],
               ["小红书", "抖音"],
               ["萌宠日常", "喂养攻略", "产品测评", "营养科普"]),
        
        Client("食品饮料", "家乐", 1, 3,
               ["家乐调味料", "家乐汤底", "家乐快手菜包"],
               ["抖音", "小红书"],
               ["美食教程", "快手菜", "场景植入", "食谱分享"]),
        
        Client("电池", "传应/南孚/益圆", 3, 3,
               ["传应电池", "南孚聚能环", "益圆电池"],
               ["抖音", "小红书"],
               ["产品测评", "使用场景", "对比测试", "续航测试"]),
        
        Client("家居用品", "碧然德", 1, 3,
               ["碧然德净水壶", "碧然德滤芯"],
               ["小红书", "抖音"],
               ["产品测评", "使用教程", "场景解决", "对比测试"]),
        
        Client("医药", "华润三九", 1, 3,
               ["999感冒灵", "999皮炎平", "999胃泰"],
               ["小红书", "抖音"],
               ["健康科普", "用药指南", "家庭常备", "季节提醒"]),
        
        Client("汽车", "大通房车", 1, 2,
               ["大通房车", "房车旅行"],
               ["小红书", "抖音", "B站"],
               ["生活方式", "旅行攻略", "产品体验", "场景展示"]),
        
        Client("互联网金融", "度小满", 1, 2,
               ["度小满理财", "度小满分期"],
               ["B站", "小红书"],
               ["理财科普", "产品推荐", "避坑指南", "场景植入"]),
        
        Client("宠物服务", "宠胖胖", 1, 2,
               ["宠胖胖APP", "宠物服务"],
               ["抖音", "小红书"],
               ["APP教程", "服务推荐", "萌宠社交", "功能测评"]),
    ]
    
    # 今日热点
    TODAY_HOT_TOPICS = [
        HotTopic("抖音", "我的春日粉彩妆容公式", 12100000, "美妆"),
        HotTopic("抖音", "中国机器狼群巷战画面首次公开", 11660000, "科技"),
        HotTopic("抖音", "我国又一次发射一箭双星", 10910000, "科技"),
        HotTopic("微博", "王毅：只要谈起来和平就有希望", 10840000, "时政"),
        HotTopic("小红书", "春日穿搭OOTD", 320000000, "服装"),
        HotTopic("小红书", "春季护肤攻略", 210000000, "美妆"),
        HotTopic("小红书", "春日妆容教程", 180000000, "美妆"),
        HotTopic("小红书", "春日减脂计划", 150000000, "健康"),
        HotTopic("小红书", "春季养生食谱", 98000000, "美食"),
        HotTopic("抖音", "43岁不健身和61岁健身的区别", 250000, "健康"),
    ]
    
    # 行业-热点关键词映射
    INDUSTRY_KEYWORDS = {
        "3C数码": ["科技", "数码", "手机", "智能", "AI", "机器狼", "数码好物"],
        "快消": ["护肤", "美妆", "妆容", "穿搭", "洗护", "沐浴露", "洗发水", "剃须"],
        "家庭清洁": ["清洁", "打扫", "家电", "焕新", "除菌", "厨房"],
        "保健品": ["健康", "养生", "健身", "营养", "免疫", "维生素", "蛋白"],
        "宠物食品": ["宠物", "猫咪", "狗狗", "萌宠", "猫粮", "罐头"],
        "食品饮料": ["美食", "烹饪", "食谱", "减脂", "养生", "调味料", "快手菜"],
        "电池": ["数码", "续航", "电池", "智能门锁", "配件"],
        "家居用品": ["家居", "家电", "净水", "饮水", "租房"],
        "医药": ["健康", "药品", "感冒", "医疗", "家庭药箱"],
        "汽车": ["汽车", "新能源", "房车", "出行", "购车"],
        "互联网金融": ["理财", "金融", "消费", "省钱", "分期"],
        "宠物服务": ["宠物", "APP", "服务", "遛狗", "社交"],
    }
    
    def __init__(self):
        self.workspace = Path("/Users/zhangjingwei/.qclaw/workspace/hotspot-tracker")
        self.ideas_file = self.workspace / "client_ideas.json"
        self.ideas = self._load_ideas()
    
    def _load_ideas(self) -> List[Dict]:
        """加载选题数据"""
        if self.ideas_file.exists():
            with open(self.ideas_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _save_ideas(self):
        """保存选题数据"""
        with open(self.ideas_file, 'w', encoding='utf-8') as f:
            json.dump(self.ideas, f, ensure_ascii=False, indent=2)
    
    def match_hot_topics(self, client: Client) -> List[HotTopic]:
        """匹配客户相关的热点"""
        keywords = self.INDUSTRY_KEYWORDS.get(client.industry, [])
        matched = []
        
        for topic in self.TODAY_HOT_TOPICS:
            for keyword in keywords:
                if keyword in topic.title or keyword in topic.category:
                    matched.append(topic)
                    break
        
        # 如果没有匹配，返回通用热点
        if not matched:
            matched = self.TODAY_HOT_TOPICS[:3]
        
        return matched[:5]  # 最多返回5个热点
    
    def generate_ideas(self) -> List[ContentIdea]:
        """为所有客户生成选题"""
        all_ideas = []
        
        for client in self.CLIENTS:
            # 匹配热点
            matched_topics = self.match_hot_topics(client)
            
            # 生成3个选题
            for i in range(3):
                hot_topic = matched_topics[i % len(matched_topics)]
                angle = client.content_angles[i % len(client.content_angles)]
                platform = client.platforms[i % len(client.platforms)]
                product = client.products[i % len(client.products)]
                
                # 生成标题
                title = self._generate_title(client, hot_topic, angle, platform)
                
                # 选择脚本类型
                script_type = "视频脚本" if platform == "抖音" else "图文脚本"
                
                # 预估互动
                engagement = self._estimate_engagement(platform, client.priority, hot_topic.hot_value)
                
                idea = ContentIdea(
                    client=client,
                    title=title,
                    platform=platform,
                    angle=angle,
                    hot_topic=hot_topic.title,
                    script_type=script_type,
                    engagement_estimate=engagement
                )
                all_ideas.append(idea)
        
        return all_ideas
    
    def _generate_title(self, client: Client, hot_topic: HotTopic, angle: str, platform: str) -> str:
        """生成选题标题"""
        templates = {
            "抖音": {
                "产品测评": f"《{hot_topic.title[:15]}？{client.products[0][:4]}真实测评》",
                "使用教程": f"《{hot_topic.title[:15]}，{client.products[0][:4]}教程》",
                "场景植入": f"《{hot_topic.title[:15]}，{client.products[0][:4]}场景》",
                "选购指南": f"《{hot_topic.title[:15]}选购，{client.products[0][:4]}篇》",
                "科技热点": f"《{hot_topic.title[:15]}，{client.products[0][:4]}有多强？》",
            },
            "小红书": {
                "产品测评": f"《{hot_topic.title[:15]}｜{client.products[0][:4]}测评》",
                "使用教程": f"《{hot_topic.title[:15]}｜{client.products[0][:4]}教程》",
                "场景植入": f"《{hot_topic.title[:15]}｜{client.products[0][:4]}实测》",
                "好物推荐": f"《{hot_topic.title[:15]}｜{client.products[0][:4]}推荐》",
                "科普知识": f"《{hot_topic.title[:15]}｜{client.products[0][:4]}科普》",
            },
            "B站": {
                "产品测评": f"《【测评】{hot_topic.title[:15]}？{client.products[0][:4]}测试》",
                "选购指南": f"《【指南】{hot_topic.title[:15]}，{client.products[0][:4]}值得买吗？》",
                "产品体验": f"《【体验】{hot_topic.title[:15]}，{client.products[0][:4]}》",
            }
        }
        
        platform_templates = templates.get(platform, templates["抖音"])
        return platform_templates.get(angle, f"《{hot_topic.title[:15]} - {client.products[0][:4]}》")
    
    def _estimate_engagement(self, platform: str, priority: int, hot_value: int) -> str:
        """预估互动量"""
        base = {"抖音": 10000, "小红书": 5000, "B站": 3000}
        multiplier = priority / 3
        hot_multiplier = min(hot_value / 10000000, 3)
        estimated = int(base.get(platform, 1000) * multiplier * hot_multiplier)
        return f"{estimated:,}+"
    
    def generate_daily_report(self) -> Dict:
        """生成每日选题报告"""
        ideas = self.generate_ideas()
        
        # 保存选题
        self.ideas = [idea.to_dict() for idea in ideas]
        self._save_ideas()
        
        # 按优先级分组
        high_priority = [i for i in ideas if i.client.priority >= 4]
        mid_priority = [i for i in ideas if i.client.priority == 3]
        low_priority = [i for i in ideas if i.client.priority <= 2]
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y%m%d"),
            "total_clients": len(self.CLIENTS),
            "total_ideas": len(ideas),
            "platform_stats": self._platform_stats(ideas),
            "high_priority_clients": self._format_client_ideas(high_priority),
            "mid_priority_clients": self._format_client_ideas(mid_priority),
            "low_priority_clients": self._format_client_ideas(low_priority),
            "all_ideas": [idea.to_dict() for idea in ideas]
        }
        
        return report
    
    def _platform_stats(self, ideas: List[ContentIdea]) -> Dict:
        """平台统计"""
        stats = {}
        for idea in ideas:
            stats[idea.platform] = stats.get(idea.platform, 0) + 1
        return stats
    
    def _format_client_ideas(self, ideas: List[ContentIdea]) -> List[Dict]:
        """格式化客户选题"""
        # 按客户分组
        client_ideas = {}
        for idea in ideas:
            industry = idea.client.industry
            if industry not in client_ideas:
                client_ideas[industry] = {
                    "industry": idea.client.industry,
                    "brand": idea.client.brand,
                    "priority": idea.client.priority,
                    "sku_count": idea.client.sku_count,
                    "ideas": []
                }
            client_ideas[industry]["ideas"].append(idea.to_dict())
        return list(client_ideas.values())
    
    def get_client(self, industry: str) -> Optional[Client]:
        """获取客户"""
        for client in self.CLIENTS:
            if client.industry == industry:
                return client
        return None
    
    def get_client_ideas(self, industry: str) -> List[ContentIdea]:
        """获取客户的选题"""
        return [idea for idea in self.generate_ideas() if idea.client.industry == industry]

async def main():
    """主函数"""
    center = ClientContentCenter()
    
    print("=" * 60)
    print("👥 客户选题中心 - 生成每日选题")
    print("=" * 60)
    
    # 生成报告
    report = center.generate_daily_report()
    
    print(f"\n✅ 选题生成完成！")
    print(f"📊 共 {report['total_clients']} 个客户")
    print(f"📝 共 {report['total_ideas']} 个选题")
    print(f"📱 抖音：{report['platform_stats'].get('抖音', 0)} 条")
    print(f"📕 小红书：{report['platform_stats'].get('小红书', 0)} 条")
    print(f"📺 B站：{report['platform_stats'].get('B站', 0)} 条")
    
    # 展示高优先级客户
    print(f"\n🔴 高优先级客户选题：")
    for client_data in report['high_priority_clients'][:3]:
        print(f"\n【{client_data['industry']}】- {client_data['brand']}")
        for idea in client_data['ideas'][:2]:
            print(f"  • {idea['title'][:40]}...")
            print(f"    平台：{idea['platform']} | 角度：{idea['angle']} | 预估：{idea['engagement_estimate']}")

if __name__ == "__main__":
    asyncio.run(main())
