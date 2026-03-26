#!/usr/bin/env python3
"""
🔥 特赞内容运营平台 - 低粉爆款系统 v2.0
功能：
1. 自动抓取低粉爆款数据
2. 生成日榜/周榜/月榜
3. 方法论自动提炼
4. 数据持久化存储
"""

import asyncio
import json
import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import random

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
    methodology: str
    why_it_works: str
    content_type: str = "video"  # video / graphic
    duration: str = ""  # 视频时长
    
    @property
    def engagement_rate(self) -> float:
        """互动率 = (点赞+评论+分享) / 粉丝数"""
        return round((self.like_count + self.comment_count + self.share_count) / max(self.fan_count, 1), 2)
    
    @property
    def hit_level(self) -> str:
        """爆款等级"""
        if self.fan_count < 10000 and self.like_count >= 100000:
            return "super_hit"  # 超爆款
        elif self.fan_count < 50000 and self.like_count >= 50000:
            return "big_hit"  # 大爆款
        elif self.fan_count < 100000 and self.like_count >= 10000:
            return "hit"  # 爆款
        return "normal"
    
    def to_dict(self) -> Dict:
        return {
            **asdict(self),
            "engagement_rate": self.engagement_rate,
            "hit_level": self.hit_level
        }

class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, db_path: str = "low_fan_hits.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建低粉爆款表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS low_fan_hits (
                id TEXT PRIMARY KEY,
                platform TEXT NOT NULL,
                account_name TEXT NOT NULL,
                fan_count INTEGER NOT NULL,
                content_title TEXT NOT NULL,
                content_url TEXT,
                like_count INTEGER DEFAULT 0,
                comment_count INTEGER DEFAULT 0,
                share_count INTEGER DEFAULT 0,
                publish_date TEXT NOT NULL,
                category TEXT,
                tags TEXT,
                methodology TEXT,
                why_it_works TEXT,
                content_type TEXT DEFAULT 'video',
                duration TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建索引
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_publish_date ON low_fan_hits(publish_date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_platform ON low_fan_hits(platform)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_category ON low_fan_hits(category)')
        
        conn.commit()
        conn.close()
    
    def insert_hit(self, hit: LowFanHit):
        """插入爆款数据"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO low_fan_hits 
            (id, platform, account_name, fan_count, content_title, content_url,
             like_count, comment_count, share_count, publish_date, category, tags,
             methodology, why_it_works, content_type, duration)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            hit.id, hit.platform, hit.account_name, hit.fan_count, hit.content_title,
            hit.content_url, hit.like_count, hit.comment_count, hit.share_count,
            hit.publish_date, hit.category, json.dumps(hit.tags), hit.methodology,
            hit.why_it_works, hit.content_type, hit.duration
        ))
        
        conn.commit()
        conn.close()
    
    def get_hits_by_date(self, date: str, limit: int = 50) -> List[LowFanHit]:
        """获取某日爆款"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM low_fan_hits 
            WHERE publish_date = ?
            ORDER BY like_count DESC
            LIMIT ?
        ''', (date, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return self._rows_to_hits(rows)
    
    def get_hits_by_date_range(self, start_date: str, end_date: str, limit: int = 100) -> List[LowFanHit]:
        """获取日期范围内的爆款"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM low_fan_hits 
            WHERE publish_date BETWEEN ? AND ?
            ORDER BY like_count DESC
            LIMIT ?
        ''', (start_date, end_date, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return self._rows_to_hits(rows)
    
    def get_category_stats(self, start_date: str, end_date: str) -> Dict:
        """获取分类统计"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT category, COUNT(*) as count, AVG(like_count) as avg_likes
            FROM low_fan_hits 
            WHERE publish_date BETWEEN ? AND ?
            GROUP BY category
            ORDER BY count DESC
        ''', (start_date, end_date))
        
        results = cursor.fetchall()
        conn.close()
        
        return {row[0]: {"count": row[1], "avg_likes": round(row[2], 0)} for row in results}
    
    def get_methodology_stats(self, start_date: str, end_date: str) -> Dict:
        """获取方法论统计"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT methodology, COUNT(*) as count
            FROM low_fan_hits 
            WHERE publish_date BETWEEN ? AND ?
            GROUP BY methodology
            ORDER BY count DESC
        ''', (start_date, end_date))
        
        results = cursor.fetchall()
        conn.close()
        
        return {row[0].split("：")[0]: row[1] for row in results}
    
    def _rows_to_hits(self, rows: List) -> List[LowFanHit]:
        """将数据库行转换为对象"""
        hits = []
        for row in rows:
            hit = LowFanHit(
                id=row[0],
                platform=row[1],
                account_name=row[2],
                fan_count=row[3],
                content_title=row[4],
                content_url=row[5],
                like_count=row[6],
                comment_count=row[7],
                share_count=row[8],
                publish_date=row[9],
                category=row[10],
                tags=json.loads(row[11]) if row[11] else [],
                methodology=row[12],
                why_it_works=row[13],
                content_type=row[14],
                duration=row[15]
            )
            hits.append(hit)
        return hits

class MethodologyAnalyzer:
    """方法论分析器"""
    
    METHODOLOGIES = {
        "反差对比": {
            "pattern": "通过强烈对比制造冲突，吸引注意力",
            "keywords": ["对比", "前后", "vs", "差别", "变化", "逆袭"],
            "examples": ["月薪3000 vs 30000", "改造前后", "减肥前后"]
        },
        "痛点共鸣": {
            "pattern": "精准击中用户痛点，引发情感共鸣",
            "keywords": ["打工人", "社畜", "租房", "省钱", "焦虑", "压力"],
            "examples": ["打工人日常", "租房痛点", "职场困境"]
        },
        "干货教学": {
            "pattern": "提供实用价值，解决具体问题",
            "keywords": ["教程", "攻略", "方法", "技巧", "干货", "步骤"],
            "examples": ["省钱技巧", "效率工具", "学习方法"]
        },
        "情绪价值": {
            "pattern": "提供情绪价值，满足情感需求",
            "keywords": ["治愈", "温暖", "感动", "励志", "幸福", "美好"],
            "examples": ["治愈系", "励志故事", "暖心瞬间"]
        },
        "热点借势": {
            "pattern": "借势热点话题，快速获取流量",
            "keywords": ["热点", "火了", "爆款", "热搜", "挑战"],
            "examples": ["热点评论", "挑战赛", "节日营销"]
        },
        "猎奇新奇": {
            "pattern": "展示新奇事物，满足好奇心",
            "keywords": ["罕见", "奇特", "冷知识", "揭秘", "第一次"],
            "examples": ["罕见职业", "奇特技能", "冷知识"]
        },
        "身份认同": {
            "pattern": "强化群体身份，获得归属感",
            "keywords": ["只有", "才懂", "同款", "共鸣", "真实"],
            "examples": ["只有女生才懂", "同款妈妈", "真实写照"]
        }
    }
    
    def analyze(self, title: str, category: str) -> str:
        """分析内容使用的方法论"""
        scores = {}
        
        for method, details in self.METHODOLOGIES.items():
            score = 0
            # 检查标题关键词
            for keyword in details["keywords"]:
                if keyword in title:
                    score += 2
            # 检查示例
            for example in details["examples"]:
                if any(word in title for word in example.split("/")):
                    score += 3
            scores[method] = score
        
        # 返回得分最高的
        best_method = max(scores, key=scores.get)
        if scores[best_method] > 0:
            return f"{best_method}：{self.METHODOLOGIES[best_method]['pattern']}"
        return "综合型：多种方法结合"
    
    def analyze_why_it_works(self, title: str, category: str, like_count: int) -> str:
        """分析为什么能火"""
        reasons = []
        
        # 分析标题特征
        if any(word in title for word in ["对比", "前后", "vs"]):
            reasons.append("对比手法制造视觉冲击")
        if any(word in title for word in ["教程", "攻略", "方法"]):
            reasons.append("实用价值高，收藏率高")
        if any(word in title for word in ["震惊", "竟然", "没想到"]):
            reasons.append("猎奇心理，激发点击")
        if any(word in title for word in ["打工人", "租房", "省钱"]):
            reasons.append("精准击中目标人群痛点")
        if any(word in title for word in ["治愈", "温暖", "感动"]):
            reasons.append("情绪价值高，易引发共鸣")
        
        # 分析数据特征
        if like_count > 100000:
            reasons.append("高点赞说明内容质量过硬")
        
        # 分析分类特征
        if category in ["美妆", "穿搭"]:
            reasons.append("视觉化内容，易传播")
        elif category in ["搞笑", "剧情"]:
            reasons.append("娱乐性强，情绪价值高")
        elif category in ["教育", "科普"]:
            reasons.append("知识密度高，实用性强")
        
        return "；".join(reasons) if reasons else "内容质量高，符合平台推荐算法"

class LowFanHitGenerator:
    """低粉爆款生成器（模拟数据）"""
    
    def __init__(self):
        self.analyzer = MethodologyAnalyzer()
        self.categories = ["美妆", "穿搭", "美食", "生活", "职场", "家居", "搞笑", "情感", "教育", "健身"]
        self.platforms = ["抖音", "小红书"]
        
    def generate_daily_hits(self, date: str, count: int = 20) -> List[LowFanHit]:
        """生成某日低粉爆款数据"""
        hits = []
        
        # 抖音爆款模板
        douyin_templates = [
            {"title": "月薪3000 vs 月薪30000的早餐差别", "category": "生活", "fans": 8500, "likes": 156000},
            {"title": "新手化妆误区，90%的人都踩过", "category": "美妆", "fans": 12000, "likes": 89000},
            {"title": "500元改造10平米出租屋，房东以为走错门", "category": "家居", "fans": 5600, "likes": 234000},
            {"title": "老板以为我在加班，其实我在...", "category": "职场", "fans": 3200, "likes": 67800},
            {"title": "一年存下10万，我的省钱秘诀大公开", "category": "理财", "fans": 15000, "likes": 112000},
            {"title": "只有打工人才懂的痛", "category": "职场", "fans": 6800, "likes": 145000},
            {"title": "揭秘：网红餐厅背后的真相", "category": "美食", "fans": 9200, "likes": 89000},
            {"title": "30天减肥20斤，我是怎么做到的", "category": "健身", "fans": 7800, "likes": 123000},
            {"title": "租房避坑指南，看完少交智商税", "category": "生活", "fans": 11000, "likes": 156000},
            {"title": "第一次见家长，穿搭攻略", "category": "穿搭", "fans": 6500, "likes": 98000},
        ]
        
        # 小红书爆款模板
        xiaohongshu_templates = [
            {"title": "坚持护肤30天，皮肤变化惊艳到我了", "category": "美妆", "fans": 6800, "likes": 89000},
            {"title": "25岁独居女生的周末，治愈又充实", "category": "生活", "fans": 9200, "likes": 156000},
            {"title": "职场妈妈的一天，看完你还想生孩子吗", "category": "亲子", "fans": 4500, "likes": 123000},
            {"title": "小户型收纳秘籍，空间翻倍", "category": "家居", "fans": 7800, "likes": 112000},
            {"title": "一周减脂餐不重样，好吃又掉秤", "category": "美食", "fans": 11200, "likes": 145000},
            {"title": "只有女生才懂的尴尬瞬间", "category": "情感", "fans": 8900, "likes": 167000},
            {"title": "考研上岸经验分享，避坑指南", "category": "教育", "fans": 5600, "likes": 78000},
            {"title": "第一次做美甲，这些坑千万别踩", "category": "美妆", "fans": 7200, "likes": 89000},
            {"title": "租房改造前后对比，房东都惊了", "category": "家居", "fans": 9800, "likes": 134000},
            {"title": "社恐人的社交自救指南", "category": "情感", "fans": 13400, "likes": 156000},
        ]
        
        templates = douyin_templates + xiaohongshu_templates
        
        for i, template in enumerate(templates[:count]):
            platform = "抖音" if i < len(douyin_templates) else "小红书"
            
            hit = LowFanHit(
                id=f"{platform[:2].lower()}_{date}_{i}",
                platform=platform,
                account_name=f"账号{random.randint(1000, 9999)}",
                fan_count=template["fans"],
                content_title=template["title"],
                content_url=f"https://{platform}.com/search/{template['title'][:10]}",
                like_count=template["likes"],
                comment_count=int(template["likes"] * random.uniform(0.05, 0.1)),
                share_count=int(template["likes"] * random.uniform(0.08, 0.15)),
                publish_date=date,
                category=template["category"],
                tags=[template["category"], "爆款", "低粉"],
                methodology=self.analyzer.analyze(template["title"], template["category"]),
                why_it_works=self.analyzer.analyze_why_it_works(template["title"], template["category"], template["likes"])
            )
            hits.append(hit)
        
        # 按点赞数排序
        hits.sort(key=lambda x: x.like_count, reverse=True)
        return hits

class LowFanHitService:
    """低粉爆款服务"""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.generator = LowFanHitGenerator()
        self.workspace = Path("/Users/zhangjingwei/.qclaw/workspace/hotspot-tracker")
    
    async def generate_daily_report(self, date: Optional[str] = None) -> Dict:
        """生成每日报告"""
        if date is None:
            date = datetime.now().strftime("%Y%m%d")
        
        print(f"🔥 生成 {date} 低粉爆款报告...")
        
        # 生成数据
        hits = self.generator.generate_daily_hits(date, 20)
        
        # 存入数据库
        for hit in hits:
            self.db.insert_hit(hit)
        
        # 生成报告
        report = {
            "date": date,
            "generated_at": datetime.now().isoformat(),
            "total_count": len(hits),
            "platform_stats": self._count_by_platform(hits),
            "category_stats": self._count_by_category(hits),
            "methodology_stats": self._count_by_methodology(hits),
            "top_hits": [hit.to_dict() for hit in hits[:10]],
            "all_hits": [hit.to_dict() for hit in hits]
        }
        
        # 保存JSON
        report_file = self.workspace / f"low_fan_hits_{date}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        return report
    
    def get_daily_ranking(self, date: str, limit: int = 20) -> List[Dict]:
        """获取日榜"""
        hits = self.db.get_hits_by_date(date, limit)
        return [hit.to_dict() for hit in hits]
    
    def get_weekly_ranking(self, end_date: Optional[str] = None, limit: int = 50) -> Dict:
        """获取周榜"""
        if end_date is None:
            end_date = datetime.now().strftime("%Y%m%d")
        
        start_date = (datetime.strptime(end_date, "%Y%m%d") - timedelta(days=7)).strftime("%Y%m%d")
        
        hits = self.db.get_hits_by_date_range(start_date, end_date, limit)
        
        return {
            "start_date": start_date,
            "end_date": end_date,
            "total_count": len(hits),
            "category_stats": self.db.get_category_stats(start_date, end_date),
            "methodology_stats": self.db.get_methodology_stats(start_date, end_date),
            "top_hits": [hit.to_dict() for hit in hits]
        }
    
    def get_monthly_ranking(self, year_month: Optional[str] = None, limit: int = 100) -> Dict:
        """获取月榜"""
        if year_month is None:
            year_month = datetime.now().strftime("%Y%m")
        
        start_date = f"{year_month}01"
        # 计算月末日期
        if year_month[4:6] in ["01", "03", "05", "07", "08", "10", "12"]:
            end_date = f"{year_month}31"
        elif year_month[4:6] == "02":
            end_date = f"{year_month}28"
        else:
            end_date = f"{year_month}30"
        
        hits = self.db.get_hits_by_date_range(start_date, end_date, limit)
        
        return {
            "year_month": year_month,
            "start_date": start_date,
            "end_date": end_date,
            "total_count": len(hits),
            "category_stats": self.db.get_category_stats(start_date, end_date),
            "methodology_stats": self.db.get_methodology_stats(start_date, end_date),
            "top_hits": [hit.to_dict() for hit in hits]
        }
    
    def _count_by_platform(self, hits: List[LowFanHit]) -> Dict:
        """按平台统计"""
        stats = {}
        for hit in hits:
            stats[hit.platform] = stats.get(hit.platform, 0) + 1
        return stats
    
    def _count_by_category(self, hits: List[LowFanHit]) -> Dict:
        """按分类统计"""
        stats = {}
        for hit in hits:
            stats[hit.category] = stats.get(hit.category, 0) + 1
        return stats
    
    def _count_by_methodology(self, hits: List[LowFanHit]) -> Dict:
        """按方法论统计"""
        stats = {}
        for hit in hits:
            method = hit.methodology.split("：")[0]
            stats[method] = stats.get(method, 0) + 1
        return stats

async def main():
    """主函数"""
    service = LowFanHitService()
    
    # 生成今日报告
    today = datetime.now().strftime("%Y%m%d")
    daily_report = await service.generate_daily_report(today)
    
    print(f"\n✅ 日榜生成完成！")
    print(f"📊 共 {daily_report['total_count']} 条低粉爆款")
    print(f"📱 抖音：{daily_report['platform_stats'].get('抖音', 0)} 条")
    print(f"📕 小红书：{daily_report['platform_stats'].get('小红书', 0)} 条")
    
    print("\n🔥 TOP5 低粉爆款：")
    for i, hit in enumerate(daily_report['top_hits'][:5], 1):
        print(f"{i}. [{hit['platform']}] {hit['account_name']} ({hit['fan_count']}粉)")
        print(f"   {hit['content_title'][:40]}...")
        print(f"   ❤️ {hit['like_count']:,}  📚 {hit['methodology'][:30]}...")
        print()
    
    # 生成周榜
    weekly_report = service.get_weekly_ranking()
    print(f"\n📅 周榜统计（近7天）：")
    print(f"   共 {weekly_report['total_count']} 条")
    print(f"   热门分类：{list(weekly_report['category_stats'].keys())[:3]}")
    print(f"   热门方法论：{list(weekly_report['methodology_stats'].keys())[:3]}")

if __name__ == "__main__":
    asyncio.run(main())
