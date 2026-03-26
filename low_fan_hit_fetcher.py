#!/usr/bin/env python3
"""
🔥 低粉爆款抓取器
抓取粉丝少但点赞高的爆款内容，提炼可复用的方法论
"""

import json
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class LowFanHit:
    """低粉爆款数据模型"""
    id: str
    platform: str
    account_name: str
    fan_count: int
    content_title: str
    content_url: str
    like_count: int
    comment_count: int
    share_count: int
    publish_date: str
    category: str
    tags: List[str]
    methodology: str  # 方法论提炼
    why_it_works: str  # 为什么能火
    
    def to_dict(self):
        return {
            "id": self.id,
            "platform": self.platform,
            "account_name": self.account_name,
            "fan_count": self.fan_count,
            "content_title": self.content_title,
            "content_url": self.content_url,
            "like_count": self.like_count,
            "comment_count": self.comment_count,
            "share_count": self.share_count,
            "publish_date": self.publish_date,
            "category": self.category,
            "tags": self.tags,
            "methodology": self.methodology,
            "why_it_works": self.why_it_works,
            "engagement_rate": round((self.like_count + self.comment_count + self.share_count) / max(self.fan_count, 1), 2)
        }

class LowFanHitAnalyzer:
    """低粉爆款分析器"""
    
    # 低粉爆款定义
    CRITERIA = {
        "super_hit": {"max_fans": 10000, "min_likes": 100000},    # 超爆款：万粉以下，10万+赞
        "big_hit": {"max_fans": 50000, "min_likes": 50000},      # 大爆款：5万粉以下，5万+赞
        "hit": {"max_fans": 100000, "min_likes": 10000},         # 爆款：10万粉以下，1万+赞
    }
    
    # 方法论模板
    METHODOLOGY_TEMPLATES = {
        "反差对比": {
            "pattern": "通过强烈对比制造冲突，吸引注意力",
            "examples": ["前后对比", "贫富差距", "理想vs现实"],
            "applicable": ["美妆", "家居", "健身", "美食"]
        },
        "痛点共鸣": {
            "pattern": "精准击中用户痛点，引发情感共鸣",
            "examples": ["打工人日常", "租房痛点", "社恐经历"],
            "applicable": ["职场", "生活", "情感", "搞笑"]
        },
        "干货教学": {
            "pattern": "提供实用价值，解决具体问题",
            "examples": ["省钱技巧", "效率工具", "学习方法"],
            "applicable": ["教育", "职场", "生活", "科技"]
        },
        "情绪价值": {
            "pattern": "提供情绪价值，满足情感需求",
            "examples": ["治愈系", "励志故事", "暖心瞬间"],
            "applicable": ["情感", "生活", "宠物", "亲子"]
        },
        "热点借势": {
            "pattern": "借势热点话题，快速获取流量",
            "examples": ["节日营销", "热点评论", "挑战赛"],
            "applicable": ["全品类"]
        },
        "猎奇新奇": {
            "pattern": "展示新奇事物，满足好奇心",
            "examples": ["罕见职业", "奇特技能", "冷知识"],
            "applicable": ["科普", "生活", "搞笑", "旅游"]
        }
    }
    
    def analyze_why_it_works(self, content: Dict) -> str:
        """分析为什么这个内容能火"""
        reasons = []
        
        # 分析标题
        title = content.get("title", "")
        if any(word in title for word in ["对比", "前后", "vs", "差别"]):
            reasons.append("使用对比手法，制造视觉/心理冲击")
        if any(word in title for word in ["教程", "攻略", "方法", "技巧"]):
            reasons.append("提供实用价值，解决具体问题")
        if any(word in title for word in ["震惊", "竟然", "没想到"]):
            reasons.append("利用猎奇心理，激发点击欲望")
        if any(word in title for word in ["打工人", "社畜", "租房", "省钱"]):
            reasons.append("精准击中目标人群痛点")
            
        # 分析数据
        like_count = content.get("like_count", 0)
        comment_count = content.get("comment_count", 0)
        if comment_count > like_count * 0.1:
            reasons.append("高评论率，说明内容引发强烈共鸣/争议")
            
        # 分析内容类型
        category = content.get("category", "")
        if category in ["美妆", "穿搭"]:
            reasons.append("视觉化内容，易传播")
        elif category in ["搞笑", "剧情"]:
            reasons.append("娱乐性强，情绪价值高")
        elif category in ["教育", "科普"]:
            reasons.append("知识密度高，收藏率高")
            
        return "；".join(reasons) if reasons else "内容质量高，符合平台算法推荐"
    
    def identify_methodology(self, content: Dict) -> str:
        """识别内容使用的方法论"""
        title = content.get("title", "")
        desc = content.get("description", "")
        
        scores = {}
        for method, details in self.METHODOLOGY_TEMPLATES.items():
            score = 0
            # 检查标题关键词
            for example in details["examples"]:
                if any(word in title for word in example.split("/")):
                    score += 2
            # 检查适用领域
            if content.get("category") in details["applicable"]:
                score += 1
            scores[method] = score
            
        # 返回得分最高的方法论
        best_method = max(scores, key=scores.get)
        if scores[best_method] > 0:
            return f"{best_method}：{self.METHODOLOGY_TEMPLATES[best_method]['pattern']}"
        return "综合型：多种方法结合"

class LowFanHitFetcher:
    """低粉爆款抓取器"""
    
    def __init__(self):
        self.analyzer = LowFanHitAnalyzer()
        self.today = datetime.now().strftime("%Y%m%d")
        
    async def fetch_douyin_low_fan_hits(self) -> List[LowFanHit]:
        """抓取抖音低粉爆款"""
        # 模拟数据（实际使用时需要爬虫抓取）
        mock_data = [
            {
                "account_name": "小王爱测评",
                "fan_count": 8500,
                "title": "月薪3000 vs 月薪30000的早餐差别",
                "like_count": 156000,
                "comment_count": 8900,
                "share_count": 12000,
                "category": "生活",
                "tags": ["贫富差距", "早餐", "生活对比"]
            },
            {
                "account_name": "美妆小白",
                "fan_count": 12000,
                "title": "新手化妆误区，90%的人都踩过",
                "like_count": 89000,
                "comment_count": 5600,
                "share_count": 7800,
                "category": "美妆",
                "tags": ["新手教程", "化妆误区", "干货"]
            },
            {
                "account_name": "租房改造家",
                "fan_count": 5600,
                "title": "500元改造10平米出租屋，房东以为走错门",
                "like_count": 234000,
                "comment_count": 12000,
                "share_count": 25000,
                "category": "家居",
                "tags": ["租房改造", "低成本", "前后对比"]
            },
            {
                "account_name": "职场老油条",
                "fan_count": 3200,
                "title": "老板以为我在加班，其实我在...",
                "like_count": 67800,
                "comment_count": 4500,
                "share_count": 5600,
                "category": "职场",
                "tags": ["打工人", "职场", "搞笑"]
            },
            {
                "account_name": "省钱小能手",
                "fan_count": 15000,
                "title": "一年存下10万，我的省钱秘诀大公开",
                "like_count": 112000,
                "comment_count": 7800,
                "share_count": 15000,
                "category": "理财",
                "tags": ["省钱", "理财", "干货"]
            }
        ]
        
        results = []
        for i, item in enumerate(mock_data):
            hit = LowFanHit(
                id=f"dy_{self.today}_{i}",
                platform="抖音",
                account_name=item["account_name"],
                fan_count=item["fan_count"],
                content_title=item["title"],
                content_url=f"https://www.douyin.com/search/{item['title'][:10]}",
                like_count=item["like_count"],
                comment_count=item["comment_count"],
                share_count=item["share_count"],
                publish_date=self.today,
                category=item["category"],
                tags=item["tags"],
                methodology=self.analyzer.identify_methodology(item),
                why_it_works=self.analyzer.analyze_why_it_works(item)
            )
            results.append(hit)
            
        return results
    
    async def fetch_xiaohongshu_low_fan_hits(self) -> List[LowFanHit]:
        """抓取小红书低粉爆款"""
        mock_data = [
            {
                "account_name": "护肤小白成长记",
                "fan_count": 6800,
                "title": "坚持护肤30天，皮肤变化惊艳到我了",
                "like_count": 89000,
                "comment_count": 6700,
                "share_count": 12000,
                "category": "美妆",
                "tags": ["护肤打卡", "30天挑战", "前后对比"]
            },
            {
                "account_name": "独居生活家",
                "fan_count": 9200,
                "title": "25岁独居女生的周末，治愈又充实",
                "like_count": 156000,
                "comment_count": 8900,
                "share_count": 23000,
                "category": "生活",
                "tags": ["独居", "治愈", "生活方式"]
            },
            {
                "account_name": "职场妈妈",
                "fan_count": 4500,
                "title": "职场妈妈的一天，看完你还想生孩子吗",
                "like_count": 123000,
                "comment_count": 15000,
                "share_count": 18000,
                "category": "亲子",
                "tags": ["职场妈妈", "育儿", "真实生活"]
            }
        ]
        
        results = []
        for i, item in enumerate(mock_data):
            hit = LowFanHit(
                id=f"xhs_{self.today}_{i}",
                platform="小红书",
                account_name=item["account_name"],
                fan_count=item["fan_count"],
                content_title=item["title"],
                content_url=f"https://www.xiaohongshu.com/search/{item['title'][:10]}",
                like_count=item["like_count"],
                comment_count=item["comment_count"],
                share_count=item["share_count"],
                publish_date=self.today,
                category=item["category"],
                tags=item["tags"],
                methodology=self.analyzer.identify_methodology(item),
                why_it_works=self.analyzer.analyze_why_it_works(item)
            )
            results.append(hit)
            
        return results
    
    async def generate_daily_report(self) -> Dict:
        """生成每日低粉爆款报告"""
        print("🔥 开始抓取低粉爆款数据...")
        
        douyin_hits = await self.fetch_douyin_low_fan_hits()
        xiaohongshu_hits = await self.fetch_xiaohongshu_low_fan_hits()
        
        all_hits = douyin_hits + xiaohongshu_hits
        
        # 按互动率排序
        all_hits.sort(key=lambda x: x.like_count / max(x.fan_count, 1), reverse=True)
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "date": self.today,
            "total_count": len(all_hits),
            "platform_stats": {
                "抖音": len(douyin_hits),
                "小红书": len(xiaohongshu_hits)
            },
            "category_stats": self._category_stats(all_hits),
            "methodology_stats": self._methodology_stats(all_hits),
            "top_hits": [hit.to_dict() for hit in all_hits[:10]],
            "all_hits": [hit.to_dict() for hit in all_hits]
        }
        
        return report
    
    def _category_stats(self, hits: List[LowFanHit]) -> Dict:
        """分类统计"""
        stats = {}
        for hit in hits:
            stats[hit.category] = stats.get(hit.category, 0) + 1
        return stats
    
    def _methodology_stats(self, hits: List[LowFanHit]) -> Dict:
        """方法论统计"""
        stats = {}
        for hit in hits:
            method = hit.methodology.split("：")[0]
            stats[method] = stats.get(method, 0) + 1
        return stats

async def main():
    """主函数"""
    fetcher = LowFanHitFetcher()
    report = await fetcher.generate_daily_report()
    
    # 保存报告
    import json
    from pathlib import Path
    
    workspace = Path("/Users/zhangjingwei/.qclaw/workspace/hotspot-tracker")
    report_file = workspace / f"low_fan_hits_{report['date']}.json"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 报告已生成：{report_file}")
    print(f"📊 共抓取 {report['total_count']} 条低粉爆款")
    print(f"📱 抖音：{report['platform_stats']['抖音']} 条")
    print(f"📕 小红书：{report['platform_stats']['小红书']} 条")
    
    print("\n🔥 TOP5 低粉爆款：")
    for i, hit in enumerate(report['top_hits'][:5], 1):
        print(f"{i}. [{hit['platform']}] {hit['account_name']} ({hit['fan_count']}粉)")
        print(f"   {hit['content_title'][:40]}...")
        print(f"   ❤️ {hit['like_count']:,}  💬 {hit['comment_count']:,}  📤 {hit['share_count']:,}")
        print(f"   📚 方法论：{hit['methodology'][:30]}...")
        print()

if __name__ == "__main__":
    asyncio.run(main())
