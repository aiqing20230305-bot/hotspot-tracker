#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
内容效果反馈闭环系统
Phase 5 - 建立内容效果反馈机制

功能：
1. 记录内容发布效果（点赞、评论、分享数）
2. 分析选题与效果的关联
3. 生成优化建议
4. 支持模拟数据用于测试
"""

import json
import os
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import random


@dataclass
class ContentMetrics:
    """内容指标数据结构"""
    views: int = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0
    saves: int = 0  # 收藏数
    clicks: int = 0  # 点击数


@dataclass
class ContentFeedback:
    """内容反馈数据模型"""
    content_id: str
    idea_id: str
    publish_time: str
    platform: str
    metrics: Dict[str, int]
    performance_score: float
    optimization_tips: List[str]
    
    # 扩展字段
    title: str = ""
    category: str = ""
    methodology: str = ""
    hot_topic: str = ""
    client: str = ""
    product: str = ""
    engagement_rate: float = 0.0
    viral_coefficient: float = 0.0  # 传播系数
    
    # 时间维度
    publish_date: str = ""
    hour_of_day: int = 0
    day_of_week: str = ""
    
    # 对比维度
    baseline_engagement: float = 0.0
    performance_vs_baseline: float = 0.0  # 相对基准的表现


class ContentFeedbackSystem:
    """内容效果反馈闭环系统"""
    
    def __init__(self, data_dir: str = "."):
        self.data_dir = data_dir
        self.feedback_db = os.path.join(data_dir, "content_feedback.db")
        self.feedback_json = os.path.join(data_dir, "content_feedback_data.json")
        self.low_fan_hits_file = os.path.join(data_dir, "low_fan_hits_data.json")
        self.client_ideas_file = os.path.join(data_dir, "client_ideas.json")
        
        self._init_database()
    
    def _init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.feedback_db)
        cursor = conn.cursor()
        
        # 内容反馈表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS content_feedback (
            content_id TEXT PRIMARY KEY,
            idea_id TEXT,
            publish_time TEXT,
            platform TEXT,
            title TEXT,
            category TEXT,
            methodology TEXT,
            hot_topic TEXT,
            client TEXT,
            product TEXT,
            views INTEGER DEFAULT 0,
            likes INTEGER DEFAULT 0,
            comments INTEGER DEFAULT 0,
            shares INTEGER DEFAULT 0,
            saves INTEGER DEFAULT 0,
            clicks INTEGER DEFAULT 0,
            performance_score REAL DEFAULT 0,
            engagement_rate REAL DEFAULT 0,
            viral_coefficient REAL DEFAULT 0,
            baseline_engagement REAL DEFAULT 0,
            performance_vs_baseline REAL DEFAULT 0,
            optimization_tips TEXT,
            created_at TEXT,
            updated_at TEXT
        )
        """)
        
        # 效果分析表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS performance_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            analysis_date TEXT,
            platform TEXT,
            category TEXT,
            methodology TEXT,
            avg_engagement REAL,
            avg_performance_score REAL,
            top_content_ids TEXT,
            insights TEXT,
            created_at TEXT
        )
        """)
        
        # 优化建议表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS optimization_suggestions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            suggestion_type TEXT,
            platform TEXT,
            category TEXT,
            suggestion TEXT,
            priority INTEGER,
            based_on_content_ids TEXT,
            created_at TEXT,
            applied_at TEXT,
            result TEXT
        )
        """)
        
        conn.commit()
        conn.close()
    
    def record_content_performance(
        self,
        content_id: str,
        idea_id: str,
        platform: str,
        metrics: ContentMetrics,
        title: str = "",
        category: str = "",
        methodology: str = "",
        hot_topic: str = "",
        client: str = "",
        product: str = "",
        publish_time: Optional[str] = None
    ) -> ContentFeedback:
        """
        记录内容发布效果
        
        Args:
            content_id: 内容ID
            idea_id: 选题ID
            platform: 发布平台
            metrics: 内容指标
            title: 内容标题
            category: 内容分类
            methodology: 创作方法
            hot_topic: 关联热点
            client: 客户品牌
            product: 产品名称
            publish_time: 发布时间
            
        Returns:
            ContentFeedback: 反馈数据对象
        """
        if publish_time is None:
            publish_time = datetime.now().isoformat()
        
        # 计算效果评分
        performance_score = self._calculate_performance_score(metrics, platform)
        
        # 计算互动率
        engagement_rate = self._calculate_engagement_rate(metrics, platform)
        
        # 计算传播系数
        viral_coefficient = self._calculate_viral_coefficient(metrics)
        
        # 获取基准互动率
        baseline = self._get_baseline_engagement(platform, category, methodology)
        
        # 计算相对表现
        performance_vs_baseline = (
            (engagement_rate - baseline) / baseline * 100
            if baseline > 0 else 0
        )
        
        # 生成优化建议
        optimization_tips = self._generate_optimization_tips(
            metrics, platform, category, methodology, performance_score
        )
        
        # 提取时间维度
        publish_dt = datetime.fromisoformat(publish_time.replace('Z', '+00:00'))
        
        feedback = ContentFeedback(
            content_id=content_id,
            idea_id=idea_id,
            publish_time=publish_time,
            platform=platform,
            metrics=asdict(metrics),
            performance_score=performance_score,
            optimization_tips=optimization_tips,
            title=title,
            category=category,
            methodology=methodology,
            hot_topic=hot_topic,
            client=client,
            product=product,
            engagement_rate=engagement_rate,
            viral_coefficient=viral_coefficient,
            publish_date=publish_dt.strftime("%Y%m%d"),
            hour_of_day=publish_dt.hour,
            day_of_week=publish_dt.strftime("%A"),
            baseline_engagement=baseline,
            performance_vs_baseline=performance_vs_baseline
        )
        
        # 保存到数据库
        self._save_feedback_to_db(feedback)
        
        return feedback
    
    def _calculate_performance_score(
        self, 
        metrics: ContentMetrics, 
        platform: str
    ) -> float:
        """
        计算效果评分 (0-100)
        
        不同平台有不同的权重配置
        """
        # 平台权重配置
        platform_weights = {
            "抖音": {"likes": 1.0, "comments": 1.5, "shares": 2.0, "views": 0.1},
            "小红书": {"likes": 1.0, "comments": 1.2, "shares": 1.5, "saves": 1.8, "views": 0.05},
            "微信视频号": {"likes": 1.0, "comments": 1.5, "shares": 2.5, "views": 0.1},
            "微博": {"likes": 1.0, "comments": 1.3, "shares": 2.0, "views": 0.05}
        }
        
        weights = platform_weights.get(platform, platform_weights["抖音"])
        
        # 计算加权得分
        score = 0.0
        for metric, weight in weights.items():
            value = getattr(metrics, metric, 0)
            score += value * weight
        
        # 归一化到0-100
        # 假设10000分对应100分
        normalized_score = min(score / 10000 * 100, 100)
        
        return round(normalized_score, 2)
    
    def _calculate_engagement_rate(
        self, 
        metrics: ContentMetrics, 
        platform: str
    ) -> float:
        """
        计算互动率
        
        互动率 = (点赞 + 评论*2 + 分享*3) / 观看数 * 100
        """
        if metrics.views == 0:
            return 0.0
        
        engagement = (
            metrics.likes + 
            metrics.comments * 2 + 
            metrics.shares * 3 +
            metrics.saves * 2.5  # 收藏权重较高
        )
        
        rate = engagement / metrics.views * 100
        return round(rate, 2)
    
    def _calculate_viral_coefficient(self, metrics: ContentMetrics) -> float:
        """
        计算传播系数 (K因子)
        
        K = 分享数 / 观看数
        K > 1 表示病毒式传播
        """
        if metrics.views == 0:
            return 0.0
        
        coefficient = metrics.shares / metrics.views * 100
        return round(coefficient, 4)
    
    def _get_baseline_engagement(
        self, 
        platform: str, 
        category: str, 
        methodology: str
    ) -> float:
        """
        获取基准互动率
        
        基于历史数据计算同类内容的平均表现
        """
        conn = sqlite3.connect(self.feedback_db)
        cursor = conn.cursor()
        
        # 查询同类内容的平均互动率
        cursor.execute("""
        SELECT AVG(engagement_rate) 
        FROM content_feedback 
        WHERE platform = ? AND category = ?
        """, (platform, category))
        
        result = cursor.fetchone()
        conn.close()
        
        if result and result[0]:
            return round(result[0], 2)
        
        # 返回默认基准值
        default_baselines = {
            "抖音": 8.0,
            "小红书": 12.0,
            "微信视频号": 5.0,
            "微博": 3.0
        }
        
        return default_baselines.get(platform, 8.0)
    
    def _generate_optimization_tips(
        self,
        metrics: ContentMetrics,
        platform: str,
        category: str,
        methodology: str,
        performance_score: float
    ) -> List[str]:
        """
        生成优化建议
        
        基于内容表现生成针对性的优化建议
        """
        tips = []
        
        # 互动率分析
        engagement_rate = self._calculate_engagement_rate(metrics, platform)
        
        if engagement_rate < 5:
            tips.append("💡 互动率偏低，建议优化内容开头3秒吸引注意力")
            tips.append("💡 可尝试使用悬念式开头或冲突性标题")
        
        elif engagement_rate > 20:
            tips.append("✅ 互动率优秀，此内容方向可持续深耕")
        
        # 传播分析
        if metrics.shares > metrics.likes * 0.1:
            tips.append("✅ 传播性良好，用户愿意主动分享")
        
        if metrics.shares < metrics.views * 0.01:
            tips.append("💡 分享率较低，建议增加实用价值或情绪共鸣点")
        
        # 评论分析
        if metrics.comments > metrics.likes * 0.1:
            tips.append("✅ 评论率高，内容引发讨论，可增加互动引导")
        
        if metrics.comments < metrics.views * 0.005:
            tips.append("💡 评论较少，可在结尾增加提问引导评论")
        
        # 平台特定建议
        if platform == "抖音" and metrics.views < metrics.likes * 20:
            tips.append("💡 抖音完播率可能较低，建议精简内容时长")
        
        if platform == "小红书" and metrics.saves < metrics.likes * 0.3:
            tips.append("💡 收藏率偏低，建议增加干货内容和实用价值")
        
        # 方法论建议
        methodology_tips = {
            "反差对比": "对比手法效果良好，可尝试更极端的对比场景",
            "情绪价值": "情绪共鸣到位，建议延续情感路线",
            "痛点共鸣": "痛点抓取精准，可继续深挖同类痛点",
            "综合型": "综合策略有效，建议保持多元化内容"
        }
        
        if methodology in methodology_tips:
            tips.append(f"📝 {methodology_tips[methodology]}")
        
        # 效果评分建议
        if performance_score > 80:
            tips.append("🌟 内容表现优秀，可作为标杆案例参考")
        elif performance_score < 40:
            tips.append("⚠️ 内容表现不佳，建议重新评估选题方向")
        
        return tips if tips else ["📊 内容表现正常，持续观察数据变化"]
    
    def _save_feedback_to_db(self, feedback: ContentFeedback):
        """保存反馈数据到数据库"""
        conn = sqlite3.connect(self.feedback_db)
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        
        cursor.execute("""
        INSERT OR REPLACE INTO content_feedback 
        (content_id, idea_id, publish_time, platform, title, category, 
         methodology, hot_topic, client, product, views, likes, comments, 
         shares, saves, clicks, performance_score, engagement_rate, 
         viral_coefficient, baseline_engagement, performance_vs_baseline,
         optimization_tips, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            feedback.content_id,
            feedback.idea_id,
            feedback.publish_time,
            feedback.platform,
            feedback.title,
            feedback.category,
            feedback.methodology,
            feedback.hot_topic,
            feedback.client,
            feedback.product,
            feedback.metrics.get("views", 0),
            feedback.metrics.get("likes", 0),
            feedback.metrics.get("comments", 0),
            feedback.metrics.get("shares", 0),
            feedback.metrics.get("saves", 0),
            feedback.metrics.get("clicks", 0),
            feedback.performance_score,
            feedback.engagement_rate,
            feedback.viral_coefficient,
            feedback.baseline_engagement,
            feedback.performance_vs_baseline,
            json.dumps(feedback.optimization_tips, ensure_ascii=False),
            now,
            now
        ))
        
        conn.commit()
        conn.close()
    
    def analyze_topic_performance(
        self,
        days: int = 7,
        platform: Optional[str] = None,
        category: Optional[str] = None
    ) -> Dict:
        """
        分析选题与效果的关联
        
        Args:
            days: 分析天数
            platform: 平台筛选
            category: 分类筛选
            
        Returns:
            分析结果字典
        """
        conn = sqlite3.connect(self.feedback_db)
        cursor = conn.cursor()
        
        # 构建查询条件
        conditions = []
        params = []
        
        if platform:
            conditions.append("platform = ?")
            params.append(platform)
        
        if category:
            conditions.append("category = ?")
            params.append(category)
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        
        # 查询近期内容
        cursor.execute(f"""
        SELECT 
            hot_topic,
            methodology,
            category,
            platform,
            COUNT(*) as content_count,
            AVG(performance_score) as avg_score,
            AVG(engagement_rate) as avg_engagement,
            AVG(viral_coefficient) as avg_viral,
            SUM(views) as total_views,
            SUM(likes) as total_likes,
            SUM(comments) as total_comments,
            SUM(shares) as total_shares
        FROM content_feedback
        WHERE {where_clause}
        GROUP BY hot_topic, methodology, category, platform
        ORDER BY avg_score DESC
        """, params)
        
        results = cursor.fetchall()
        
        # 整理分析结果
        analysis = {
            "analysis_date": datetime.now().isoformat(),
            "period_days": days,
            "filters": {
                "platform": platform,
                "category": category
            },
            "topic_performance": [],
            "methodology_ranking": [],
            "category_ranking": [],
            "platform_ranking": [],
            "top_content": [],
            "optimization_insights": []
        }
        
        # 热点表现
        for row in results:
            analysis["topic_performance"].append({
                "hot_topic": row[0],
                "methodology": row[1],
                "category": row[2],
                "platform": row[3],
                "content_count": row[4],
                "avg_performance_score": round(row[5], 2),
                "avg_engagement_rate": round(row[6], 2),
                "avg_viral_coefficient": round(row[7], 4),
                "total_views": row[8],
                "total_likes": row[9],
                "total_comments": row[10],
                "total_shares": row[11]
            })
        
        # 方法论排名
        cursor.execute(f"""
        SELECT 
            methodology,
            COUNT(*) as count,
            AVG(performance_score) as avg_score,
            AVG(engagement_rate) as avg_engagement
        FROM content_feedback
        WHERE {where_clause}
        GROUP BY methodology
        ORDER BY avg_score DESC
        """, params)
        
        for row in cursor.fetchall():
            analysis["methodology_ranking"].append({
                "methodology": row[0],
                "content_count": row[1],
                "avg_performance_score": round(row[2], 2),
                "avg_engagement_rate": round(row[3], 2)
            })
        
        # 分类排名
        cursor.execute(f"""
        SELECT 
            category,
            COUNT(*) as count,
            AVG(performance_score) as avg_score,
            AVG(engagement_rate) as avg_engagement
        FROM content_feedback
        WHERE {where_clause}
        GROUP BY category
        ORDER BY avg_score DESC
        """, params)
        
        for row in cursor.fetchall():
            analysis["category_ranking"].append({
                "category": row[0],
                "content_count": row[1],
                "avg_performance_score": round(row[2], 2),
                "avg_engagement_rate": round(row[3], 2)
            })
        
        # 平台排名
        cursor.execute(f"""
        SELECT 
            platform,
            COUNT(*) as count,
            AVG(performance_score) as avg_score,
            AVG(engagement_rate) as avg_engagement
        FROM content_feedback
        WHERE {where_clause}
        GROUP BY platform
        ORDER BY avg_score DESC
        """, params)
        
        for row in cursor.fetchall():
            analysis["platform_ranking"].append({
                "platform": row[0],
                "content_count": row[1],
                "avg_performance_score": round(row[2], 2),
                "avg_engagement_rate": round(row[3], 2)
            })
        
        # Top内容
        cursor.execute(f"""
        SELECT content_id, title, hot_topic, methodology, performance_score,
               engagement_rate, viral_coefficient
        FROM content_feedback
        WHERE {where_clause}
        ORDER BY performance_score DESC
        LIMIT 10
        """, params)
        
        for row in cursor.fetchall():
            analysis["top_content"].append({
                "content_id": row[0],
                "title": row[1],
                "hot_topic": row[2],
                "methodology": row[3],
                "performance_score": row[4],
                "engagement_rate": row[5],
                "viral_coefficient": row[6]
            })
        
        conn.close()
        
        # 生成优化洞察
        analysis["optimization_insights"] = self._generate_insights(analysis)
        
        return analysis
    
    def _generate_insights(self, analysis: Dict) -> List[str]:
        """生成优化洞察"""
        insights = []
        
        # 方法论洞察
        if analysis["methodology_ranking"]:
            top_method = analysis["methodology_ranking"][0]
            insights.append(
                f"🎯 最佳方法论：{top_method['methodology']} "
                f"(平均效果评分: {top_method['avg_performance_score']})"
            )
        
        # 分类洞察
        if analysis["category_ranking"]:
            top_category = analysis["category_ranking"][0]
            insights.append(
                f"📊 最佳分类：{top_category['category']} "
                f"(平均互动率: {top_category['avg_engagement_rate']}%)"
            )
        
        # 平台洞察
        if analysis["platform_ranking"]:
            top_platform = analysis["platform_ranking"][0]
            insights.append(
                f"🚀 最佳平台：{top_platform['platform']} "
                f"(平均效果评分: {top_platform['avg_performance_score']})"
            )
        
        # 传播洞察
        if analysis["topic_performance"]:
            viral_contents = [
                t for t in analysis["topic_performance"]
                if t["avg_viral_coefficient"] > 1.0
            ]
            if viral_contents:
                insights.append(
                    f"🔥 发现{len(viral_contents)}个病毒式传播话题，可重点跟进"
                )
        
        return insights
    
    def generate_optimization_report(
        self,
        days: int = 7,
        output_file: Optional[str] = None
    ) -> str:
        """
        生成优化报告
        
        Args:
            days: 分析天数
            output_file: 输出文件路径
            
        Returns:
            报告内容
        """
        analysis = self.analyze_topic_performance(days)
        
        report = f"""# 内容效果反馈闭环报告

生成时间: {analysis['analysis_date']}
分析周期: 近{days}天

## 📊 整体表现

### 方法论效果排名

| 排名 | 方法论 | 内容数 | 平均效果评分 | 平均互动率 |
|------|--------|--------|--------------|------------|
"""
        
        for i, method in enumerate(analysis["methodology_ranking"], 1):
            report += f"| {i} | {method['methodology']} | {method['content_count']} | "
            report += f"{method['avg_performance_score']} | {method['avg_engagement_rate']}% |\n"
        
        report += """
### 分类效果排名

| 排名 | 分类 | 内容数 | 平均效果评分 | 平均互动率 |
|------|------|--------|--------------|------------|
"""
        
        for i, cat in enumerate(analysis["category_ranking"], 1):
            report += f"| {i} | {cat['category']} | {cat['content_count']} | "
            report += f"{cat['avg_performance_score']} | {cat['avg_engagement_rate']}% |\n"
        
        report += """
### 平台效果排名

| 排名 | 平台 | 内容数 | 平均效果评分 | 平均互动率 |
|------|------|--------|--------------|------------|
"""
        
        for i, plat in enumerate(analysis["platform_ranking"], 1):
            report += f"| {i} | {plat['platform']} | {plat['content_count']} | "
            report += f"{plat['avg_performance_score']} | {plat['avg_engagement_rate']}% |\n"
        
        report += """
## 🏆 Top 10 内容

| 排名 | 标题 | 热点 | 方法论 | 效果评分 | 互动率 |
|------|------|------|--------|----------|--------|
"""
        
        for i, content in enumerate(analysis["top_content"], 1):
            title = content['title'][:30] + "..." if len(content['title']) > 30 else content['title']
            report += f"| {i} | {title} | {content['hot_topic']} | "
            report += f"{content['methodology']} | {content['performance_score']} | "
            report += f"{content['engagement_rate']}% |\n"
        
        report += """
## 💡 优化洞察

"""
        
        for insight in analysis["optimization_insights"]:
            report += f"- {insight}\n"
        
        report += """
## 📝 下一步行动建议

1. **延续成功模式**：继续使用效果最佳的方法论和选题方向
2. **优化弱势环节**：针对互动率低的内容类型进行优化
3. **测试新方向**：尝试排名靠前但使用较少的组合
4. **数据监控**：持续跟踪效果，建立数据驱动的内容迭代流程
"""
        
        # 保存报告
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
        
        return report
    
    def generate_mock_data(self, count: int = 20):
        """
        生成模拟数据用于测试
        
        Args:
            count: 生成数据条数
        """
        platforms = ["抖音", "小红书", "微信视频号", "微博"]
        categories = ["生活", "美妆", "职场", "亲子", "家居", "理财", "3C数码"]
        methodologies = ["反差对比", "情绪价值", "痛点共鸣", "综合型"]
        
        hot_topics = [
            "春季护肤攻略", "打工人日常", "独居生活", "育儿心得",
            "租房改造", "省钱秘籍", "科技测评", "健身打卡"
        ]
        
        for i in range(count):
            # 随机生成指标
            views = random.randint(10000, 500000)
            likes = random.randint(int(views * 0.02), int(views * 0.15))
            comments = random.randint(int(likes * 0.05), int(likes * 0.3))
            shares = random.randint(int(likes * 0.02), int(likes * 0.2))
            saves = random.randint(int(likes * 0.1), int(likes * 0.5))
            
            metrics = ContentMetrics(
                views=views,
                likes=likes,
                comments=comments,
                shares=shares,
                saves=saves
            )
            
            platform = random.choice(platforms)
            category = random.choice(categories)
            methodology = random.choice(methodologies)
            hot_topic = random.choice(hot_topics)
            
            # 随机生成发布时间（近7天内）
            days_ago = random.randint(0, 7)
            publish_time = datetime.now() - timedelta(days=days_ago)
            publish_time = publish_time.replace(
                hour=random.randint(8, 22),
                minute=random.randint(0, 59)
            )
            
            self.record_content_performance(
                content_id=f"mock_{datetime.now().strftime('%Y%m%d%H%M%S')}_{i}",
                idea_id=f"idea_{random.randint(1000, 9999)}",
                platform=platform,
                metrics=metrics,
                title=f"测试内容{i+1}: {hot_topic}相关分享",
                category=category,
                methodology=methodology,
                hot_topic=hot_topic,
                client="测试客户",
                product="测试产品",
                publish_time=publish_time.isoformat()
            )
        
        print(f"✅ 已生成{count}条模拟数据")
    
    def export_to_json(self, output_file: Optional[str] = None):
        """导出反馈数据为JSON"""
        if output_file is None:
            output_file = self.feedback_json
        
        conn = sqlite3.connect(self.feedback_db)
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT 
            content_id, idea_id, publish_time, platform, title, category,
            methodology, hot_topic, client, product, views, likes, comments,
            shares, saves, clicks, performance_score, engagement_rate,
            viral_coefficient, baseline_engagement, performance_vs_baseline,
            optimization_tips
        FROM content_feedback
        ORDER BY publish_time DESC
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        data = []
        for row in rows:
            data.append({
                "content_id": row[0],
                "idea_id": row[1],
                "publish_time": row[2],
                "platform": row[3],
                "title": row[4],
                "category": row[5],
                "methodology": row[6],
                "hot_topic": row[7],
                "client": row[8],
                "product": row[9],
                "metrics": {
                    "views": row[10],
                    "likes": row[11],
                    "comments": row[12],
                    "shares": row[13],
                    "saves": row[14],
                    "clicks": row[15]
                },
                "performance_score": row[16],
                "engagement_rate": row[17],
                "viral_coefficient": row[18],
                "baseline_engagement": row[19],
                "performance_vs_baseline": row[20],
                "optimization_tips": json.loads(row[21]) if row[21] else []
            })
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 已导出{len(data)}条反馈数据到 {output_file}")
        
        return data


def main():
    """主函数"""
    print("=" * 60)
    print("内容效果反馈闭环系统")
    print("=" * 60)
    
    # 初始化系统
    system = ContentFeedbackSystem()
    
    # 生成模拟数据（如果数据库为空）
    conn = sqlite3.connect(system.feedback_db)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM content_feedback")
    count = cursor.fetchone()[0]
    conn.close()
    
    if count == 0:
        print("\n📊 数据库为空，生成模拟数据...")
        system.generate_mock_data(30)
    
    # 分析选题与效果的关联
    print("\n📈 分析选题效果...")
    analysis = system.analyze_topic_performance(days=7)
    
    print(f"\n分析结果:")
    print(f"- 方法论排名: {len(analysis['methodology_ranking'])}个")
    print(f"- 分类排名: {len(analysis['category_ranking'])}个")
    print(f"- 平台排名: {len(analysis['platform_ranking'])}个")
    print(f"- Top内容: {len(analysis['top_content'])}条")
    
    # 生成优化报告
    print("\n📝 生成优化报告...")
    report = system.generate_optimization_report(
        days=7,
        output_file="content_feedback_report.md"
    )
    
    print("\n✅ 报告已保存到 content_feedback_report.md")
    
    # 导出JSON数据
    print("\n💾 导出反馈数据...")
    system.export_to_json()
    
    print("\n" + "=" * 60)
    print("反馈闭环系统运行完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
