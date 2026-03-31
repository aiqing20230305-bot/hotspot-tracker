#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
选题质量评分系统 - Phase 4数据质量优化
用于评估选题的时效性、热度、匹配度等多维度指标

Author: Agent-5 (AI工程师)
Date: 2026-04-01
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
import math


class QualityScorer:
    """选题质量评分系统"""
    
    def __init__(self, config: Dict = None):
        """初始化评分系统
        
        Args:
            config: 评分配置参数
        """
        self.config = config or {
            'weights': {
                'timeliness': 0.25,      # 时效性权重
                'heat': 0.30,            # 热度权重
                'relevance': 0.25,       # 匹配度权重
                'diversity': 0.10,       # 多样性权重
                'actionability': 0.10    # 可执行性权重
            },
            'heat_thresholds': {
                'viral': 2000000,        # 爆款阈值
                'hot': 1000000,          # 热门阈值
                'warm': 500000,          # 温热阈值
                'normal': 100000         # 普通阈值
            },
            'timeliness_decay': {
                'half_life_hours': 24,   # 半衰期（小时）
                'min_score': 0.3         # 最低分
            }
        }
    
    def calculate_timeliness_score(self, created_at: str) -> float:
        """计算时效性得分
        
        基于热点创建时间，采用指数衰减模型
        新热点得分高，旧热点得分逐渐降低
        
        Args:
            created_at: ISO格式的时间字符串
            
        Returns:
            时效性得分 (0.3-1.0)
        """
        try:
            created_time = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            now = datetime.now(created_time.tzinfo) if created_time.tzinfo else datetime.now()
            
            hours_elapsed = (now - created_time).total_seconds() / 3600
            
            # 指数衰减公式: score = e^(-ln(2) * hours / half_life)
            half_life = self.config['timeliness_decay']['half_life_hours']
            min_score = self.config['timeliness_decay']['min_score']
            
            decay_factor = math.exp(-math.log(2) * hours_elapsed / half_life)
            score = max(min_score, min(1.0, decay_factor))
            
            return round(score, 3)
        except Exception:
            return 0.5
    
    def calculate_heat_score(self, hot_value: int, trend: str = None) -> float:
        """计算热度得分
        
        基于热点数值和趋势标签
        
        Args:
            hot_value: 热度数值
            trend: 趋势标签（爆、热、新等）
            
        Returns:
            热度得分 (0.0-1.0)
        """
        thresholds = self.config['heat_thresholds']
        
        # 基础热度得分
        if hot_value >= thresholds['viral']:
            base_score = 1.0
        elif hot_value >= thresholds['hot']:
            base_score = 0.8 + (hot_value - thresholds['hot']) / (thresholds['viral'] - thresholds['hot']) * 0.2
        elif hot_value >= thresholds['warm']:
            base_score = 0.6 + (hot_value - thresholds['warm']) / (thresholds['hot'] - thresholds['warm']) * 0.2
        elif hot_value >= thresholds['normal']:
            base_score = 0.4 + (hot_value - thresholds['normal']) / (thresholds['warm'] - thresholds['normal']) * 0.2
        else:
            base_score = max(0.2, hot_value / thresholds['normal'] * 0.4)
        
        # 趋势加成
        trend_bonus = {
            '爆': 0.15,
            '热': 0.10,
            '新': 0.08,
            '涨': 0.05
        }
        
        if trend and trend in trend_bonus:
            base_score = min(1.0, base_score + trend_bonus[trend])
        
        return round(base_score, 3)
    
    def calculate_relevance_score(self, topic: Dict, client_industries: List[str] = None) -> float:
        """计算匹配度得分
        
        基于热点与客户行业的匹配程度
        
        Args:
            topic: 热点数据
            client_industries: 客户所属行业列表
            
        Returns:
            匹配度得分 (0.0-1.0)
        """
        if not client_industries:
            return 0.5
        
        topic_industries = topic.get('industries', [])
        
        if not topic_industries:
            return 0.3
        
        # 计算行业交集
        intersection = set(topic_industries) & set(client_industries)
        
        if intersection:
            # 完全匹配
            if len(intersection) == len(topic_industries):
                return 1.0
            # 部分匹配
            match_ratio = len(intersection) / len(topic_industries)
            return round(0.5 + match_ratio * 0.5, 3)
        
        # 无匹配，但热点有明确行业
        return 0.2
    
    def calculate_diversity_score(self, topic: Dict, existing_topics: List[Dict] = None) -> float:
        """计算多样性得分
        
        基于与已有选题的差异程度，避免同质化
        
        Args:
            topic: 当前热点
            existing_topics: 已有选题列表
            
        Returns:
            多样性得分 (0.0-1.0)
        """
        if not existing_topics:
            return 1.0
        
        topic_type = topic.get('type', '')
        topic_keywords = set(topic.get('keywords', []))
        
        # 统计同类型选题数量
        same_type_count = sum(1 for t in existing_topics if t.get('type') == topic_type)
        
        # 统计关键词重复度
        keyword_overlap = 0
        for existing in existing_topics:
            existing_keywords = set(existing.get('keywords', []))
            if topic_keywords & existing_keywords:
                keyword_overlap += 1
        
        # 计算多样性得分
        type_diversity = max(0.3, 1.0 - same_type_count * 0.1)
        keyword_diversity = max(0.3, 1.0 - keyword_overlap * 0.05)
        
        score = (type_diversity + keyword_diversity) / 2
        return round(score, 3)
    
    def calculate_actionability_score(self, topic: Dict) -> float:
        """计算可执行性得分
        
        基于热点的可操作性（是否有明确切入点、素材丰富度等）
        
        Args:
            topic: 热点数据
            
        Returns:
            可执行性得分 (0.0-1.0)
        """
        score = 0.5  # 基础分
        
        # 有关键词
        if topic.get('keywords') and len(topic['keywords']) >= 3:
            score += 0.15
        
        # 有明确类型
        if topic.get('type'):
            score += 0.10
        
        # 有行业标签
        if topic.get('industries') and len(topic['industries']) > 0:
            score += 0.10
        
        # 有客户关联
        if topic.get('c') and len(topic['c']) > 0:
            score += 0.10
        
        # 有情绪标签（便于内容创作）
        if topic.get('sentiment'):
            score += 0.05
        
        return round(min(1.0, score), 3)
    
    def calculate_topic_score(self, topic: Dict, context: Dict = None) -> Dict:
        """计算选题综合质量得分
        
        Args:
            topic: 热点数据
            context: 上下文信息（客户行业、已有选题等）
            
        Returns:
            包含各项得分和综合得分的字典
        """
        context = context or {}
        weights = self.config['weights']
        
        # 计算各维度得分
        timeliness = self.calculate_timeliness_score(topic.get('created_at', ''))
        heat = self.calculate_heat_score(topic.get('hot_value', 0), topic.get('trends', [''])[0])
        relevance = self.calculate_relevance_score(topic, context.get('client_industries'))
        diversity = self.calculate_diversity_score(topic, context.get('existing_topics'))
        actionability = self.calculate_actionability_score(topic)
        
        # 计算加权综合得分
        total_score = (
            timeliness * weights['timeliness'] +
            heat * weights['heat'] +
            relevance * weights['relevance'] +
            diversity * weights['diversity'] +
            actionability * weights['actionability']
        )
        
        # 确定质量等级
        if total_score >= 0.8:
            quality_level = 'A级-优质'
        elif total_score >= 0.6:
            quality_level = 'B级-良好'
        elif total_score >= 0.4:
            quality_level = 'C级-一般'
        else:
            quality_level = 'D级-待优化'
        
        return {
            'topic_title': topic.get('title'),
            'scores': {
                'timeliness': timeliness,
                'heat': heat,
                'relevance': relevance,
                'diversity': diversity,
                'actionability': actionability
            },
            'total_score': round(total_score, 3),
            'quality_level': quality_level,
            'recommendation': self._generate_recommendation(total_score, {
                'timeliness': timeliness,
                'heat': heat,
                'relevance': relevance,
                'diversity': diversity,
                'actionability': actionability
            })
        }
    
    def _generate_recommendation(self, total_score: float, scores: Dict) -> str:
        """生成选题建议
        
        Args:
            total_score: 综合得分
            scores: 各维度得分
            
        Returns:
            选题建议文本
        """
        if total_score >= 0.8:
            return '强烈推荐，建议优先采纳并快速执行'
        elif total_score >= 0.6:
            weak_points = [k for k, v in scores.items() if v < 0.5]
            if weak_points:
                return f'建议采纳，注意提升{", ".join(weak_points)}'
            return '建议采纳'
        elif total_score >= 0.4:
            return '可选，建议优化后采纳'
        else:
            return '不推荐，建议寻找更优质选题'
    
    def batch_score_topics(self, topics: List[Dict], context: Dict = None) -> List[Dict]:
        """批量评分选题
        
        Args:
            topics: 热点列表
            context: 上下文信息
            
        Returns:
            评分结果列表
        """
        results = []
        context = context or {}
        
        # 为每个选题评分
        for i, topic in enumerate(topics):
            # 更新上下文中的已有选题
            context['existing_topics'] = topics[:i]
            
            score_result = self.calculate_topic_score(topic, context)
            score_result['rank'] = topic.get('rank', i + 1)
            results.append(score_result)
        
        # 按综合得分排序
        results.sort(key=lambda x: x['total_score'], reverse=True)
        
        return results
    
    def generate_quality_report(self, topics: List[Dict], context: Dict = None) -> Dict:
        """生成选题质量报告
        
        Args:
            topics: 热点列表
            context: 上下文信息
            
        Returns:
            质量报告字典
        """
        scored_topics = self.batch_score_topics(topics, context)
        
        # 统计分析
        level_counts = {'A级-优质': 0, 'B级-良好': 0, 'C级-一般': 0, 'D级-待优化': 0}
        avg_scores = {'timeliness': 0, 'heat': 0, 'relevance': 0, 'diversity': 0, 'actionability': 0}
        
        for result in scored_topics:
            level_counts[result['quality_level']] += 1
            for key in avg_scores:
                avg_scores[key] += result['scores'][key]
        
        n = len(scored_topics)
        if n > 0:
            avg_scores = {k: round(v / n, 3) for k, v in avg_scores.items()}
        
        return {
            'generated_at': datetime.now().isoformat(),
            'total_topics': n,
            'quality_distribution': level_counts,
            'average_scores': avg_scores,
            'top_recommendations': scored_topics[:10],
            'all_scores': scored_topics
        }


def deduplicate_topics(topics: List[Dict]) -> tuple:
    """热点去重
    
    保留热度最高、信息最完整的版本
    
    Args:
        topics: 热点列表
        
    Returns:
        (去重后的列表, 删除的重复项列表)
    """
    seen_titles = {}
    duplicates = []
    
    for topic in topics:
        title = topic.get('title', '')
        
        if title not in seen_titles:
            seen_titles[title] = topic
        else:
            # 比较热度，保留更高的
            existing = seen_titles[title]
            if topic.get('hot_value', 0) > existing.get('hot_value', 0):
                duplicates.append(existing)
                seen_titles[title] = topic
            else:
                duplicates.append(topic)
    
    return list(seen_titles.values()), duplicates


def optimize_topic_categories(topics: List[Dict]) -> Dict:
    """优化热点分类标签
    
    Args:
        topics: 热点列表
        
    Returns:
        分类优化建议
    """
    # 统计现有分类
    type_counts = {}
    type_keywords = {}
    
    for topic in topics:
        tp = topic.get('type', '未分类')
        type_counts[tp] = type_counts.get(tp, 0) + 1
        
        if tp not in type_keywords:
            type_keywords[tp] = []
        type_keywords[tp].extend(topic.get('keywords', []))
    
    # 提取各类别的核心关键词
    from collections import Counter
    type_core_keywords = {}
    for tp, keywords in type_keywords.items():
        keyword_counts = Counter(keywords)
        type_core_keywords[tp] = [k for k, v in keyword_counts.most_common(5)]
    
    return {
        'type_distribution': type_counts,
        'type_core_keywords': type_core_keywords,
        'recommendations': {
            'merge_similar': '网络热梗和热点事件可考虑合并为"网络热点"',
            'add_categories': ['科技热点', '体育热点', '教育热点'],
            'refine_rules': '建议基于关键词自动分类，减少人工标注误差'
        }
    }


def check_sku_tag_completeness(scenes: List[Dict]) -> Dict:
    """检查SKU场景标签完整性
    
    Args:
        scenes: SKU场景列表
        
    Returns:
        标签完整性报告
    """
    required_fields = ['id', 'industry', 'platform', 'scene_type', 'scenario', 'trigger_keywords', 'heat_score']
    
    field_stats = {f: {'complete': 0, 'empty': 0, 'missing': 0} for f in required_fields}
    
    for scene in scenes:
        for field in required_fields:
            if field not in scene:
                field_stats[field]['missing'] += 1
            elif not scene[field] and scene[field] != 0:
                field_stats[field]['empty'] += 1
            else:
                field_stats[field]['complete'] += 1
    
    # 计算完整率
    completeness = {}
    for field, stats in field_stats.items():
        total = sum(stats.values())
        completeness[field] = round(stats['complete'] / total * 100, 1) if total > 0 else 0
    
    return {
        'total_scenes': len(scenes),
        'field_stats': field_stats,
        'completeness_rate': completeness,
        'issues': [
            f"{field}字段缺失{stats['missing']}条, 为空{stats['empty']}条"
            for field, stats in field_stats.items()
            if stats['missing'] > 0 or stats['empty'] > 0
        ]
    }


if __name__ == '__main__':
    # 演示用法
    import sys
    
    # 加载热点数据
    try:
        with open('hot_topics.json', 'r', encoding='utf-8') as f:
            topics = json.load(f)
    except FileNotFoundError:
        print("未找到 hot_topics.json")
        sys.exit(1)
    
    print("=" * 60)
    print("选题质量评分系统 - Phase 4数据质量优化")
    print("=" * 60)
    
    # 1. 热点去重
    print("\n【任务4.1】热点去重与分类优化")
    print("-" * 40)
    deduped, duplicates = deduplicate_topics(topics)
    print(f"原始热点数: {len(topics)}")
    print(f"去重后数量: {len(deduped)}")
    print(f"删除重复项: {len(duplicates)}")
    
    if duplicates:
        print("\n重复热点:")
        for d in duplicates:
            print(f"  - {d['title']} (热度: {d.get('hot_value', 'N/A')})")
    
    # 分类优化
    category_opt = optimize_topic_categories(topics)
    print(f"\n分类统计:")
    for tp, count in sorted(category_opt['type_distribution'].items(), key=lambda x: -x[1]):
        print(f"  {tp}: {count}条")
    
    # 2. 质量评分
    print("\n【任务4.2】选题质量评分")
    print("-" * 40)
    
    scorer = QualityScorer()
    report = scorer.generate_quality_report(deduped)
    
    print(f"总选题数: {report['total_topics']}")
    print(f"\n质量分布:")
    for level, count in report['quality_distribution'].items():
        print(f"  {level}: {count}条")
    
    print(f"\n平均得分:")
    for key, value in report['average_scores'].items():
        print(f"  {key}: {value}")
    
    print(f"\nTOP 5 推荐选题:")
    for i, rec in enumerate(report['top_recommendations'][:5], 1):
        print(f"  {i}. {rec['topic_title']} - {rec['quality_level']} ({rec['total_score']})")
    
    # 3. SKU标签检查
    print("\n【任务4.3】SKU场景标签检查")
    print("-" * 40)
    
    try:
        with open('sku_scenes.json', 'r', encoding='utf-8') as f:
            scenes = json.load(f)
        
        tag_report = check_sku_tag_completeness(scenes)
        print(f"总场景数: {tag_report['total_scenes']}")
        print(f"\n字段完整率:")
        for field, rate in tag_report['completeness_rate'].items():
            status = "✓" if rate == 100 else "✗"
            print(f"  {status} {field}: {rate}%")
        
        if tag_report['issues']:
            print(f"\n待解决问题:")
            for issue in tag_report['issues']:
                print(f"  - {issue}")
    except FileNotFoundError:
        print("未找到 sku_scenes.json")
    
    print("\n" + "=" * 60)
    print("质量评分系统运行完成")
    print("=" * 60)
