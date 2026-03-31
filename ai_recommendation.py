#!/usr/bin/env python3
"""
🔥 AI选题推荐引擎 - Phase 3 核心功能
基于热点和客户画像的智能选题匹配系统

功能:
- 多维度匹配算法（热点关联、行业匹配、关键词相似度）
- 历史数据权重（互动量、转化率）
- 推荐结果API接口
- 热点趋势关联分析
"""

import json
import math
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict
from pathlib import Path
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 项目根目录
PROJECT_ROOT = Path(__file__).parent


@dataclass
class RecommendationScore:
    """推荐评分详情"""
    total_score: float
    hot_topic_relevance: float  # 热点关联度
    industry_match: float       # 行业匹配度
    keyword_similarity: float   # 关键词相似度
    history_weight: float       # 历史数据权重
    trend_score: float          # 趋势得分
    explanation: str            # 推荐理由


@dataclass
class RecommendationResult:
    """推荐结果"""
    id: str
    title: str
    client: str
    industry: str
    product: str
    platform: str
    angle: str
    hot_topic: str
    heat: str
    trend: str
    score: float
    score_details: Dict[str, float]
    explanation: str
    matched_keywords: List[str]
    engagement_estimate: str


class AIRecommendationEngine:
    """AI选题推荐引擎"""
    
    # 权重配置
    WEIGHTS = {
        'hot_topic_relevance': 0.30,    # 热点关联度权重
        'industry_match': 0.25,          # 行业匹配度权重
        'keyword_similarity': 0.20,      # 关键词相似度权重
        'history_weight': 0.15,          # 历史数据权重
        'trend_score': 0.10              # 趋势得分权重
    }
    
    # 行业映射（用于跨行业推荐）
    INDUSTRY_MAPPING = {
        '3C数码': ['科技', '数码', '电子', '手机', '电脑'],
        '美妆护肤': ['化妆品', '护肤', '美容', '彩妆'],
        '食品饮料': ['饮品', '零食', '美食', '食品'],
        '服饰穿搭': ['服装', '时尚', '穿搭', '服饰'],
        '家居清洁': ['家居', '清洁', '生活', '日用品'],
        '母婴育儿': ['母婴', '育儿', '宝宝', '儿童'],
        '健身运动': ['运动', '健身', '体育', '健康'],
        '宠物用品': ['宠物', '猫', '狗', '萌宠'],
    }
    
    def __init__(self, data_dir: Optional[Path] = None):
        """初始化推荐引擎"""
        self.data_dir = data_dir or PROJECT_ROOT
        self.hot_topics: List[Dict] = []
        self.client_ideas: List[Dict] = []
        self.sku_scenes: List[Dict] = []
        self.client_profiles: Dict[str, Dict] = {}
        self.keyword_index: Dict[str, List[str]] = defaultdict(list)
        
        # 加载数据
        self._load_data()
        self._build_indices()
        
        logger.info(f"✅ AI推荐引擎初始化完成")
        logger.info(f"   热点数据: {len(self.hot_topics)} 条")
        logger.info(f"   选题数据: {len(self.client_ideas)} 条")
        logger.info(f"   SKU场景: {len(self.sku_scenes)} 条")
        logger.info(f"   客户画像: {len(self.client_profiles)} 个")
    
    def _load_data(self):
        """加载所有数据"""
        # 加载热点数据
        hot_topics_file = self.data_dir / 'hot_topics.json'
        if hot_topics_file.exists():
            with open(hot_topics_file, 'r', encoding='utf-8') as f:
                self.hot_topics = json.load(f)
        
        # 加载选题数据
        ideas_file = self.data_dir / 'client_ideas.json'
        if ideas_file.exists():
            with open(ideas_file, 'r', encoding='utf-8') as f:
                self.client_ideas = json.load(f)
        
        # 加载SKU场景数据
        sku_file = self.data_dir / 'sku_scenes.json'
        if sku_file.exists():
            with open(sku_file, 'r', encoding='utf-8') as f:
                self.sku_scenes = json.load(f)
        
        # 构建客户画像
        self._build_client_profiles()
    
    def _build_client_profiles(self):
        """构建客户画像"""
        for idea in self.client_ideas:
            client_info = idea.get('client', {})
            brand = client_info.get('brand', '')
            
            if brand and brand not in self.client_profiles:
                self.client_profiles[brand] = {
                    'brand': brand,
                    'industry': client_info.get('industry', ''),
                    'products': client_info.get('products', []),
                    'ideas_count': 0,
                    'platforms': set(),
                    'angles': set(),
                    'hot_topics': set(),
                    'avg_engagement': 0
                }
            
            if brand:
                self.client_profiles[brand]['ideas_count'] += 1
                self.client_profiles[brand]['platforms'].add(idea.get('platform', ''))
                self.client_profiles[brand]['angles'].add(idea.get('angle', ''))
                self.client_profiles[brand]['hot_topics'].add(idea.get('hot_topic', ''))
        
        # 转换set为list以便JSON序列化
        for profile in self.client_profiles.values():
            profile['platforms'] = list(profile['platforms'])
            profile['angles'] = list(profile['angles'])
            profile['hot_topics'] = list(profile['hot_topics'])
    
    def _build_indices(self):
        """构建索引以加速查询"""
        # 构建关键词索引
        for idea in self.client_ideas:
            keywords = idea.get('keywords', [])
            idea_id = idea.get('id', '')
            for keyword in keywords:
                self.keyword_index[keyword.lower()].append(idea_id)
        
        # 构建热点关键词索引
        self.hot_keyword_index = defaultdict(list)
        for topic in self.hot_topics:
            keywords = topic.get('keywords', [])
            title = topic.get('title', '')
            for keyword in keywords:
                self.hot_keyword_index[keyword.lower()].append(topic)
            # 也索引标题
            self.hot_keyword_index[title.lower()].append(topic)
    
    def calculate_hot_topic_relevance(self, idea: Dict, hot_topic: Dict) -> float:
        """计算选题与热点的关联度"""
        score = 0.0
        
        # 1. 关键词匹配
        idea_keywords = set([k.lower() for k in idea.get('keywords', [])])
        hot_keywords = set([k.lower() for k in hot_topic.get('keywords', [])])
        
        if idea_keywords and hot_keywords:
            intersection = idea_keywords & hot_keywords
            union = idea_keywords | hot_keywords
            if union:
                jaccard = len(intersection) / len(union)
                score += jaccard * 0.5
        
        # 2. 标题包含热点关键词
        title = idea.get('title', '').lower()
        hot_title = hot_topic.get('title', '').lower()
        
        for kw in hot_keywords:
            if kw in title:
                score += 0.2
        
        # 3. 热点标题在选题标题中
        if hot_title and hot_title in title:
            score += 0.3
        
        return min(score, 1.0)
    
    def calculate_industry_match(self, idea: Dict, client_profile: Dict) -> float:
        """计算行业匹配度"""
        idea_industry = idea.get('client', {}).get('industry', '')
        client_industry = client_profile.get('industry', '')
        
        if not idea_industry or not client_industry:
            return 0.5  # 未知行业给中等分
        
        # 完全匹配
        if idea_industry == client_industry:
            return 1.0
        
        # 检查行业映射关系
        for main_industry, related in self.INDUSTRY_MAPPING.items():
            if client_industry in main_industry or main_industry in client_industry:
                for rel in related:
                    if rel in idea_industry:
                        return 0.8
        
        return 0.3
    
    def calculate_keyword_similarity(self, idea: Dict, query_keywords: List[str]) -> float:
        """计算关键词相似度"""
        if not query_keywords:
            return 0.5
        
        idea_keywords = set([k.lower() for k in idea.get('keywords', [])])
        query_set = set([k.lower() for k in query_keywords])
        
        if not idea_keywords:
            return 0.0
        
        intersection = idea_keywords & query_set
        return len(intersection) / len(query_set) if query_set else 0.0
    
    def calculate_history_weight(self, idea: Dict) -> float:
        """计算历史数据权重"""
        # 从互动预估中提取数值
        engagement = idea.get('engagement_estimate', '0')
        
        # 提取数字
        match = re.search(r'(\d+)', str(engagement).replace(',', ''))
        if match:
            value = int(match.group(1))
            # 归一化到0-1，假设最大值为100000
            return min(value / 100000, 1.0)
        
        return 0.5  # 默认中等权重
    
    def calculate_trend_score(self, idea: Dict) -> float:
        """计算趋势得分"""
        trend = idea.get('trend', '')
        heat = idea.get('heat', '')
        
        score = 0.0
        
        # 趋势判断
        if '快速上升' in trend or '🔥🔥🔥' in trend:
            score += 0.5
        elif '上升' in trend or '🔥🔥' in trend:
            score += 0.3
        elif '🔥' in trend:
            score += 0.1
        
        # 热度判断
        if '爆' in heat:
            score += 0.5
        elif '高热' in heat:
            score += 0.3
        elif '热' in heat:
            score += 0.2
        
        return min(score, 1.0)
    
    def generate_explanation(self, idea: Dict, scores: RecommendationScore) -> str:
        """生成推荐理由"""
        reasons = []
        
        if scores.hot_topic_relevance > 0.5:
            reasons.append(f"与热点【{idea.get('hot_topic', '')}】高度关联")
        
        if scores.industry_match > 0.7:
            reasons.append(f"符合{idea.get('client', {}).get('brand', '')}品牌调性")
        
        if scores.keyword_similarity > 0.5:
            reasons.append("关键词匹配度高")
        
        if scores.history_weight > 0.5:
            reasons.append(f"预估互动量{idea.get('engagement_estimate', '')}")
        
        if scores.trend_score > 0.5:
            reasons.append(f"当前处于{idea.get('heat', '热门')}状态")
        
        return '；'.join(reasons) if reasons else "综合推荐"
    
    def recommend(
        self,
        client_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        platform: Optional[str] = None,
        industry: Optional[str] = None,
        hot_topic: Optional[str] = None,
        limit: int = 20,
        min_score: float = 0.3
    ) -> List[RecommendationResult]:
        """
        生成推荐选题
        
        Args:
            client_id: 客户ID/品牌名
            tags: 标签列表（关键词）
            platform: 平台筛选
            industry: 行业筛选
            hot_topic: 关联热点
            limit: 返回数量限制
            min_score: 最低推荐分数
        
        Returns:
            推荐结果列表
        """
        results = []
        
        # 获取客户画像
        client_profile = self.client_profiles.get(client_id, {}) if client_id else {}
        
        # 获取关联热点
        related_hot_topics = []
        if hot_topic:
            for topic in self.hot_topics:
                if hot_topic.lower() in topic.get('title', '').lower():
                    related_hot_topics.append(topic)
        elif tags:
            # 根据标签找相关热点
            for tag in tags:
                if tag.lower() in self.hot_keyword_index:
                    related_hot_topics.extend(self.hot_keyword_index[tag.lower()])
        
        # 如果没有指定热点，使用当前热点
        if not related_hot_topics and not hot_topic:
            related_hot_topics = self.hot_topics[:10]  # 取前10个热点
        
        # 去重热点
        seen_topics = set()
        unique_hot_topics = []
        for topic in related_hot_topics:
            title = topic.get('title', '')
            if title not in seen_topics:
                seen_topics.add(title)
                unique_hot_topics.append(topic)
        
        # 评分每个选题
        for idea in self.client_ideas:
            # 筛选条件
            if client_id and idea.get('client', {}).get('brand', '') != client_id:
                continue
            
            if platform and idea.get('platform', '') != platform:
                continue
            
            if industry and idea.get('client', {}).get('industry', '') != industry:
                continue
            
            # 计算各维度得分
            hot_topic_relevance = 0.0
            matched_keywords = []
            
            for topic in unique_hot_topics:
                relevance = self.calculate_hot_topic_relevance(idea, topic)
                if relevance > hot_topic_relevance:
                    hot_topic_relevance = relevance
                    # 提取匹配的关键词
                    idea_kw = set([k.lower() for k in idea.get('keywords', [])])
                    topic_kw = set([k.lower() for k in topic.get('keywords', [])])
                    matched_keywords = list(idea_kw & topic_kw)
            
            industry_match = self.calculate_industry_match(idea, client_profile)
            keyword_similarity = self.calculate_keyword_similarity(idea, tags or [])
            history_weight = self.calculate_history_weight(idea)
            trend_score = self.calculate_trend_score(idea)
            
            # 计算总分
            total_score = (
                hot_topic_relevance * self.WEIGHTS['hot_topic_relevance'] +
                industry_match * self.WEIGHTS['industry_match'] +
                keyword_similarity * self.WEIGHTS['keyword_similarity'] +
                history_weight * self.WEIGHTS['history_weight'] +
                trend_score * self.WEIGHTS['trend_score']
            )
            
            # 过滤低分选题
            if total_score < min_score:
                continue
            
            # 创建评分对象
            scores = RecommendationScore(
                total_score=total_score,
                hot_topic_relevance=hot_topic_relevance,
                industry_match=industry_match,
                keyword_similarity=keyword_similarity,
                history_weight=history_weight,
                trend_score=trend_score,
                explanation=""
            )
            
            # 生成推荐理由
            explanation = self.generate_explanation(idea, scores)
            
            # 创建结果对象
            result = RecommendationResult(
                id=idea.get('id', ''),
                title=idea.get('title', ''),
                client=idea.get('client', {}).get('brand', ''),
                industry=idea.get('client', {}).get('industry', ''),
                product=idea.get('product', ''),
                platform=idea.get('platform', ''),
                angle=idea.get('angle', ''),
                hot_topic=idea.get('hot_topic', ''),
                heat=idea.get('heat', ''),
                trend=idea.get('trend', ''),
                score=round(total_score, 4),
                score_details={
                    'hot_topic_relevance': round(hot_topic_relevance, 4),
                    'industry_match': round(industry_match, 4),
                    'keyword_similarity': round(keyword_similarity, 4),
                    'history_weight': round(history_weight, 4),
                    'trend_score': round(trend_score, 4)
                },
                explanation=explanation,
                matched_keywords=matched_keywords,
                engagement_estimate=idea.get('engagement_estimate', '')
            )
            
            results.append(result)
        
        # 按分数排序
        results.sort(key=lambda x: x.score, reverse=True)
        
        # 返回Top N
        return results[:limit]
    
    def get_hot_topic_analysis(self, hot_topic_title: str) -> Dict[str, Any]:
        """
        分析热点与选题的关联关系
        
        Args:
            hot_topic_title: 热点标题
        
        Returns:
            热点分析结果
        """
        # 查找热点详情
        topic_detail = None
        for topic in self.hot_topics:
            if hot_topic_title.lower() in topic.get('title', '').lower():
                topic_detail = topic
                break
        
        if not topic_detail:
            return {"error": f"未找到热点: {hot_topic_title}"}
        
        # 统计关联选题
        related_ideas = []
        client_distribution = defaultdict(int)
        industry_distribution = defaultdict(int)
        platform_distribution = defaultdict(int)
        angle_distribution = defaultdict(int)
        
        for idea in self.client_ideas:
            relevance = self.calculate_hot_topic_relevance(idea, topic_detail)
            if relevance > 0.1:  # 有关联
                related_ideas.append({
                    'id': idea.get('id'),
                    'title': idea.get('title'),
                    'client': idea.get('client', {}).get('brand', ''),
                    'relevance': round(relevance, 4)
                })
                client_distribution[idea.get('client', {}).get('brand', '')] += 1
                industry_distribution[idea.get('client', {}).get('industry', '')] += 1
                platform_distribution[idea.get('platform', '')] += 1
                angle_distribution[idea.get('angle', '')] += 1
        
        # 排序
        related_ideas.sort(key=lambda x: x['relevance'], reverse=True)
        
        return {
            'hot_topic': topic_detail,
            'total_related_ideas': len(related_ideas),
            'top_ideas': related_ideas[:10],
            'client_distribution': dict(sorted(client_distribution.items(), key=lambda x: x[1], reverse=True)),
            'industry_distribution': dict(sorted(industry_distribution.items(), key=lambda x: x[1], reverse=True)),
            'platform_distribution': dict(sorted(platform_distribution.items(), key=lambda x: x[1], reverse=True)),
            'angle_distribution': dict(sorted(angle_distribution.items(), key=lambda x: x[1], reverse=True))
        }
    
    def get_client_recommendations(
        self,
        client_id: str,
        top_n: int = 10
    ) -> Dict[str, Any]:
        """
        获取客户专属推荐
        
        Args:
            client_id: 客户ID/品牌名
            top_n: 返回数量
        
        Returns:
            客户推荐结果
        """
        profile = self.client_profiles.get(client_id)
        if not profile:
            return {"error": f"未找到客户: {client_id}"}
        
        # 获取推荐
        recommendations = self.recommend(
            client_id=client_id,
            limit=top_n
        )
        
        # 获取相关热点
        hot_topics_for_client = []
        for topic in self.hot_topics[:20]:
            for idea in self.client_ideas:
                if idea.get('client', {}).get('brand', '') == client_id:
                    relevance = self.calculate_hot_topic_relevance(idea, topic)
                    if relevance > 0.2:
                        hot_topics_for_client.append({
                            'title': topic.get('title'),
                            'relevance': round(relevance, 4),
                            'hot_value': topic.get('hot_value', 0)
                        })
                        break
        
        # 去重并排序
        seen = set()
        unique_hot_topics = []
        for ht in hot_topics_for_client:
            if ht['title'] not in seen:
                seen.add(ht['title'])
                unique_hot_topics.append(ht)
        unique_hot_topics.sort(key=lambda x: x['relevance'], reverse=True)
        
        return {
            'client_profile': profile,
            'recommendations': [asdict(r) for r in recommendations],
            'related_hot_topics': unique_hot_topics[:5],
            'generated_at': datetime.now().isoformat()
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取推荐系统统计信息"""
        return {
            'total_hot_topics': len(self.hot_topics),
            'total_ideas': len(self.client_ideas),
            'total_sku_scenes': len(self.sku_scenes),
            'total_clients': len(self.client_profiles),
            'clients': [
                {
                    'brand': p['brand'],
                    'industry': p['industry'],
                    'ideas_count': p['ideas_count']
                }
                for p in sorted(self.client_profiles.values(), key=lambda x: x['ideas_count'], reverse=True)
            ],
            'index_size': len(self.keyword_index),
            'hot_keyword_index_size': len(self.hot_keyword_index)
        }


# ============== Flask API ==============

def create_flask_app():
    """创建Flask应用"""
    from flask import Flask, jsonify, request
    from flask_cors import CORS
    
    app = Flask(__name__)
    CORS(app)
    
    # 初始化推荐引擎
    engine = AIRecommendationEngine()
    
    @app.route('/api/recommend', methods=['GET', 'POST'])
    def recommend():
        """推荐接口"""
        if request.method == 'POST':
            data = request.get_json() or {}
        else:
            data = request.args.to_dict()
        
        client_id = data.get('client_id') or data.get('brand')
        tags = data.get('tags', [])
        if isinstance(tags, str):
            tags = tags.split(',')
        
        platform = data.get('platform')
        industry = data.get('industry')
        hot_topic = data.get('hot_topic')
        limit = int(data.get('limit', 20))
        min_score = float(data.get('min_score', 0.3))
        
        results = engine.recommend(
            client_id=client_id,
            tags=tags,
            platform=platform,
            industry=industry,
            hot_topic=hot_topic,
            limit=limit,
            min_score=min_score
        )
        
        return jsonify({
            'success': True,
            'count': len(results),
            'results': [asdict(r) for r in results],
            'query': {
                'client_id': client_id,
                'tags': tags,
                'platform': platform,
                'industry': industry,
                'hot_topic': hot_topic
            }
        })
    
    @app.route('/api/hot_topic_analysis/<path:title>')
    def hot_topic_analysis(title):
        """热点分析接口"""
        result = engine.get_hot_topic_analysis(title)
        return jsonify(result)
    
    @app.route('/api/client/<client_id>')
    def client_recommendations(client_id):
        """客户推荐接口"""
        top_n = int(request.args.get('top_n', 10))
        result = engine.get_client_recommendations(client_id, top_n)
        return jsonify(result)
    
    @app.route('/api/statistics')
    def statistics():
        """统计信息接口"""
        return jsonify(engine.get_statistics())
    
    @app.route('/api/clients')
    def list_clients():
        """列出所有客户"""
        return jsonify({
            'clients': list(engine.client_profiles.keys()),
            'count': len(engine.client_profiles)
        })
    
    @app.route('/api/hot_topics')
    def list_hot_topics():
        """列出热点"""
        limit = int(request.args.get('limit', 20))
        topics = engine.hot_topics[:limit]
        return jsonify({
            'count': len(topics),
            'topics': topics
        })
    
    @app.route('/health')
    def health():
        """健康检查"""
        return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})
    
    return app


def run_server(port: int = 5001):
    """运行API服务器"""
    app = create_flask_app()
    logger.info(f"🚀 AI推荐引擎API启动在端口 {port}")
    app.run(host='0.0.0.0', port=port, debug=True)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'serve':
        # 运行API服务
        port = int(sys.argv[2]) if len(sys.argv) > 2 else 5001
        run_server(port)
    else:
        # 测试模式
        engine = AIRecommendationEngine()
        
        print("\n" + "="*60)
        print("🔥 AI选题推荐引擎 - 测试模式")
        print("="*60)
        
        # 显示统计
        stats = engine.get_statistics()
        print(f"\n📊 系统统计:")
        print(f"   热点数量: {stats['total_hot_topics']}")
        print(f"   选题数量: {stats['total_ideas']}")
        print(f"   SKU场景: {stats['total_sku_scenes']}")
        print(f"   客户数量: {stats['total_clients']}")
        
        # 测试推荐
        print("\n🎯 测试推荐（客户：荣耀）:")
        results = engine.recommend(client_id='荣耀', limit=5)
        for i, r in enumerate(results, 1):
            print(f"\n{i}. {r.title}")
            print(f"   分数: {r.score} | 平台: {r.platform}")
            print(f"   理由: {r.explanation}")
