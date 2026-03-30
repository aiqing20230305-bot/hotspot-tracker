#!/usr/bin/env python3
"""
🧠 增强版效果反馈与自学习系统 v2.0
功能：
1. 更细粒度的评分规则（时间段、竞品词、情绪词）
2. 基于已有数据的置信度提升逻辑
3. 多维度交叉分析
4. 智能权重调整
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict
import statistics
import re

class EnhancedLearningSystem:
    """增强版自学习系统"""
    
    def __init__(self):
        self.workspace = Path("/Users/zhangjingwei/.qclaw/workspace/hotspot-tracker")
        self.feedback_file = self.workspace / "content_feedback.json"
        self.learning_file = self.workspace / "learning_data.json"
        self.insights_file = self.workspace / "optimization_insights.md"
        
        self.feedback_data = self._load_feedback()
        self.learning_data = self._load_learning()
        
        # 定义评分规则常量
        self._init_scoring_rules()
    
    def _init_scoring_rules(self):
        """初始化评分规则"""
        # 时间段评分权重（基于历史数据）
        self.time_slot_weights = {
            "morning": {"start": 6, "end": 12, "weight": 1.0, "label": "早间(6-12点)"},
            "afternoon": {"start": 12, "end": 18, "weight": 1.1, "label": "午间(12-18点)"},
            "evening": {"start": 18, "end": 22, "weight": 1.3, "label": "晚间(18-22点)"},
            "night": {"start": 22, "end": 2, "weight": 0.9, "label": "深夜(22-2点)"},
            "dawn": {"start": 2, "end": 6, "weight": 0.7, "label": "凌晨(2-6点)"}
        }
        
        # 竞品关键词（影响评分）
        self.competitor_keywords = {
            "3C数码": ["华为", "小米", "OPPO", "vivo", "苹果", "荣耀", "三星", "realme"],
            "快消": ["宝洁", "联合利华", "欧莱雅", "资生堂", "完美日记", "花西子"],
            "保健品": ["汤臣倍健", "Swisse", "GNC", "养生堂", "白云山"],
            "家庭清洁": ["立白", "蓝月亮", "威露士", "滴露", "奥妙"]
        }
        
        # 情绪词评分权重
        self.emotion_weights = {
            "positive": {
                "keywords": ["推荐", "好用", "必买", "宝藏", "神器", "绝绝子", "yyds", "真香", "心动", "爱了"],
                "weight": 1.15
            },
            "negative": {
                "keywords": ["踩雷", "避坑", "后悔", "智商税", "翻车", "失望", "差评"],
                "weight": 0.85
            },
            "neutral": {
                "keywords": ["测评", "分享", "体验", "开箱", "教程", "攻略"],
                "weight": 1.0
            },
            "urgent": {
                "keywords": ["限时", "秒杀", "最后", "错过", "手慢无", "紧急"],
                "weight": 1.2
            }
        }
        
        # 平台特性权重
        self.platform_characteristics = {
            "抖音": {
                "optimal_duration": (15, 60),  # 最佳时长（秒）
                "peak_hours": [12, 18, 20, 21, 22],
                "content_types": ["剧情", "效果展示", "挑战", "教程"],
                "base_weight": 1.0
            },
            "小红书": {
                "optimal_duration": None,  # 图文为主
                "peak_hours": [8, 12, 18, 21, 22],
                "content_types": ["种草", "测评", "攻略", "对比"],
                "base_weight": 1.0
            },
            "视频号": {
                "optimal_duration": (30, 180),
                "peak_hours": [7, 12, 18, 20, 21],
                "content_types": ["知识", "生活", "情感", "搞笑"],
                "base_weight": 0.95
            },
            "B站": {
                "optimal_duration": (180, 600),
                "peak_hours": [12, 18, 20, 21, 22, 23],
                "content_types": ["科普", "测评", "剧情", "知识"],
                "base_weight": 0.9
            }
        }
        
        # 置信度计算参数
        self.confidence_params = {
            "min_samples_for_confidence": 3,  # 最少样本数才能计算置信度
            "high_confidence_samples": 10,  # 高置信度所需样本数
            "confidence_boost_per_sample": 0.05,  # 每增加一个样本的置信度提升
            "max_confidence": 0.95,  # 最大置信度上限
            "score_variance_penalty": 0.1  # 分数波动惩罚系数
        }
    
    def _load_feedback(self) -> List[Dict]:
        """加载反馈数据"""
        if self.feedback_file.exists():
            with open(self.feedback_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _load_learning(self) -> Dict:
        """加载学习数据"""
        if self.learning_file.exists():
            with open(self.learning_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self._init_learning_data()
    
    def _init_learning_data(self) -> Dict:
        """初始化增强版学习数据结构"""
        return {
            "version": "2.0",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            
            # 基础表现数据
            "industry_performance": {},
            "platform_performance": {},
            "angle_performance": {},
            "hot_topic_performance": {},
            
            # 新增：时间段表现
            "time_slot_performance": {
                "morning": {"count": 0, "total_score": 0, "avg_score": 0, "scores": []},
                "afternoon": {"count": 0, "total_score": 0, "avg_score": 0, "scores": []},
                "evening": {"count": 0, "total_score": 0, "avg_score": 0, "scores": []},
                "night": {"count": 0, "total_score": 0, "avg_score": 0, "scores": []},
                "dawn": {"count": 0, "total_score": 0, "avg_score": 0, "scores": []}
            },
            
            # 新增：竞品词效果
            "competitor_keyword_performance": {},
            
            # 新增：情绪词效果
            "emotion_keyword_performance": {
                "positive": {"count": 0, "total_score": 0, "avg_score": 0, "examples": []},
                "negative": {"count": 0, "total_score": 0, "avg_score": 0, "examples": []},
                "neutral": {"count": 0, "total_score": 0, "avg_score": 0, "examples": []},
                "urgent": {"count": 0, "total_score": 0, "avg_score": 0, "examples": []}
            },
            
            # 新增：交叉分析数据
            "cross_analysis": {
                "industry_platform": {},  # 行业+平台组合效果
                "industry_angle": {},     # 行业+角度组合效果
                "platform_angle": {},     # 平台+角度组合效果
                "time_platform": {}       # 时间段+平台组合效果
            },
            
            # 增强的优化规则
            "optimization_rules": {
                "industry_rules": [],
                "platform_rules": [],
                "angle_rules": [],
                "time_rules": [],
                "competitor_rules": [],
                "emotion_rules": [],
                "combination_rules": []
            },
            
            # 新增：置信度数据
            "confidence_scores": {
                "industry": {},
                "platform": {},
                "angle": {},
                "time_slot": {},
                "overall": 0.0
            },
            
            # 新增：趋势数据
            "trends": {
                "daily_scores": [],
                "weekly_improvement": 0.0,
                "momentum": "stable"  # rising, falling, stable
            },
            
            "brand_performance": {},
            "product_performance": {},
            "summary": {}
        }
    
    def _get_time_slot(self, hour: int) -> str:
        """根据小时获取时间段"""
        for slot_name, slot_info in self.time_slot_weights.items():
            start, end = slot_info["start"], slot_info["end"]
            if start <= end:
                if start <= hour < end:
                    return slot_name
            else:  # 跨天的情况（如 22-2点）
                if hour >= start or hour < end:
                    return slot_name
        return "morning"
    
    def _detect_competitor_keywords(self, text: str, industry: str) -> List[str]:
        """检测竞品关键词"""
        found = []
        if industry in self.competitor_keywords:
            for keyword in self.competitor_keywords[industry]:
                if keyword in text:
                    found.append(keyword)
        return found
    
    def _detect_emotion_keywords(self, text: str) -> Dict[str, List[str]]:
        """检测情绪关键词"""
        found = {}
        for emotion_type, emotion_data in self.emotion_weights.items():
            keywords_found = [kw for kw in emotion_data["keywords"] if kw in text]
            if keywords_found:
                found[emotion_type] = keywords_found
        return found
    
    def _calculate_confidence(self, scores: List[float], count: int) -> float:
        """计算置信度"""
        params = self.confidence_params
        
        if count < params["min_samples_for_confidence"]:
            return 0.0
        
        # 基础置信度（基于样本数）
        base_confidence = min(
            count * params["confidence_boost_per_sample"],
            params["max_confidence"]
        )
        
        # 波动惩罚（如果分数波动大，降低置信度）
        if len(scores) >= 3:
            try:
                variance = statistics.variance(scores)
                avg_score = statistics.mean(scores)
                coefficient_of_variation = variance / (avg_score ** 2) if avg_score > 0 else 0
                penalty = min(coefficient_of_variation * params["score_variance_penalty"], 0.3)
                base_confidence *= (1 - penalty)
            except:
                pass
        
        return min(base_confidence, params["max_confidence"])
    
    def _calculate_enhanced_engagement(self, metrics: Dict, 
                                        competitor_keywords: List[str],
                                        emotion_keywords: Dict[str, List[str]],
                                        time_slot: str) -> Tuple[float, Dict]:
        """计算增强版互动分数"""
        # 基础互动分
        likes = metrics.get('likes', 0)
        comments = metrics.get('comments', 0) * 3
        shares = metrics.get('shares', 0) * 5
        views = metrics.get('views', 1)
        
        if views == 0:
            views = 1
        
        base_engagement = (likes + comments + shares) / views * 100
        
        # 时间段权重调整
        time_weight = self.time_slot_weights.get(time_slot, {}).get("weight", 1.0)
        adjusted_score = base_engagement * time_weight
        
        # 竞品词影响
        competitor_boost = 1.0
        if competitor_keywords:
            competitor_boost = 1.0 + (len(competitor_keywords) * 0.05)  # 每个竞品词+5%
            adjusted_score *= competitor_boost
        
        # 情绪词影响
        emotion_multiplier = 1.0
        emotion_breakdown = {}
        for emotion_type, keywords in emotion_keywords.items():
            weight = self.emotion_weights.get(emotion_type, {}).get("weight", 1.0)
            emotion_multiplier *= weight
            emotion_breakdown[emotion_type] = {
                "keywords": keywords,
                "weight": weight
            }
        adjusted_score *= emotion_multiplier
        
        # 限制上限
        final_score = min(adjusted_score, 100)
        
        # 返回分数和详细的计算分解
        score_breakdown = {
            "base_engagement": round(base_engagement, 4),
            "time_adjustment": {
                "slot": time_slot,
                "weight": time_weight
            },
            "competitor_adjustment": {
                "keywords": competitor_keywords,
                "boost": round(competitor_boost, 4)
            },
            "emotion_adjustment": emotion_breakdown,
            "emotion_multiplier": round(emotion_multiplier, 4),
            "final_score": round(final_score, 4)
        }
        
        return final_score, score_breakdown
    
    def add_enhanced_feedback(self, content_id: str, industry: str, platform: str,
                              angle: str, hot_topic: str, metrics: Dict[str, Any],
                              publish_time: Optional[str] = None,
                              content_text: Optional[str] = None):
        """添加增强版内容效果反馈"""
        
        # 解析发布时间
        if publish_time:
            try:
                dt = datetime.fromisoformat(publish_time)
                hour = dt.hour
                time_slot = self._get_time_slot(hour)
            except:
                time_slot = "morning"
                hour = 10
        else:
            time_slot = "morning"
            hour = 10
        
        # 检测竞品词
        competitor_keywords = []
        if content_text:
            competitor_keywords = self._detect_competitor_keywords(content_text, industry)
        
        # 检测情绪词
        emotion_keywords = {}
        if content_text:
            emotion_keywords = self._detect_emotion_keywords(content_text)
        
        # 计算增强版互动分
        engagement_score, score_breakdown = self._calculate_enhanced_engagement(
            metrics, competitor_keywords, emotion_keywords, time_slot
        )
        
        # 构建反馈记录
        feedback = {
            "id": content_id,
            "date": datetime.now().strftime("%Y%m%d"),
            "timestamp": datetime.now().isoformat(),
            "industry": industry,
            "platform": platform,
            "angle": angle,
            "hot_topic": hot_topic,
            "metrics": metrics,
            "publish_time": publish_time or datetime.now().isoformat(),
            "time_slot": time_slot,
            "competitor_keywords": competitor_keywords,
            "emotion_keywords": emotion_keywords,
            "engagement_score": round(engagement_score, 4),
            "score_breakdown": score_breakdown
        }
        
        self.feedback_data.append(feedback)
        self._save_feedback()
        
        # 更新学习数据
        self._update_enhanced_learning(feedback)
        
        print(f"✅ 增强反馈已记录: {content_id}")
        print(f"   互动分: {engagement_score:.2f} | 时间段: {time_slot} | 竞品词: {len(competitor_keywords)} | 情绪词: {len(emotion_keywords)}")
    
    def _update_enhanced_learning(self, feedback: Dict):
        """更新增强版学习数据"""
        
        # 1. 更新基础表现数据
        self._update_basic_performance(feedback)
        
        # 2. 更新时间段表现
        self._update_time_slot_performance(feedback)
        
        # 3. 更新竞品词表现
        self._update_competitor_performance(feedback)
        
        # 4. 更新情绪词表现
        self._update_emotion_performance(feedback)
        
        # 5. 更新交叉分析
        self._update_cross_analysis(feedback)
        
        # 6. 更新置信度
        self._update_confidence_scores()
        
        # 7. 更新趋势数据
        self._update_trends(feedback)
        
        # 8. 生成优化规则
        self._generate_optimization_rules()
        
        # 9. 更新汇总数据
        self._update_summary()
        
        self.learning_data['updated_at'] = datetime.now().isoformat()
        self._save_learning()
    
    def _update_basic_performance(self, feedback: Dict):
        """更新基础表现数据"""
        for perf_type in ['industry', 'platform', 'angle', 'hot_topic']:
            key = feedback[perf_type] if perf_type != 'hot_topic' else feedback['hot_topic']
            perf_key = f"{perf_type}_performance"
            
            if key not in self.learning_data[perf_key]:
                self.learning_data[perf_key][key] = {
                    'count': 0, 'total_score': 0, 'avg_score': 0, 'scores': []
                }
            
            self.learning_data[perf_key][key]['count'] += 1
            self.learning_data[perf_key][key]['total_score'] += feedback['engagement_score']
            self.learning_data[perf_key][key]['scores'].append(feedback['engagement_score'])
            self.learning_data[perf_key][key]['avg_score'] = (
                self.learning_data[perf_key][key]['total_score'] / 
                self.learning_data[perf_key][key]['count']
            )
    
    def _update_time_slot_performance(self, feedback: Dict):
        """更新时间段表现"""
        time_slot = feedback.get('time_slot', 'morning')
        
        perf = self.learning_data['time_slot_performance'][time_slot]
        perf['count'] += 1
        perf['total_score'] += feedback['engagement_score']
        perf['scores'].append(feedback['engagement_score'])
        perf['avg_score'] = perf['total_score'] / perf['count']
    
    def _update_competitor_performance(self, feedback: Dict):
        """更新竞品词表现"""
        for keyword in feedback.get('competitor_keywords', []):
            if keyword not in self.learning_data['competitor_keyword_performance']:
                self.learning_data['competitor_keyword_performance'][keyword] = {
                    'count': 0, 'total_score': 0, 'avg_score': 0, 'scores': [],
                    'industry': feedback['industry']
                }
            
            perf = self.learning_data['competitor_keyword_performance'][keyword]
            perf['count'] += 1
            perf['total_score'] += feedback['engagement_score']
            perf['scores'].append(feedback['engagement_score'])
            perf['avg_score'] = perf['total_score'] / perf['count']
    
    def _update_emotion_performance(self, feedback: Dict):
        """更新情绪词表现"""
        for emotion_type, keywords in feedback.get('emotion_keywords', {}).items():
            perf = self.learning_data['emotion_keyword_performance'][emotion_type]
            perf['count'] += 1
            perf['total_score'] += feedback['engagement_score']
            perf['avg_score'] = perf['total_score'] / perf['count'] if perf['count'] > 0 else 0
            
            # 记录示例
            for kw in keywords:
                example = {
                    'keyword': kw,
                    'content_id': feedback['id'],
                    'score': feedback['engagement_score'],
                    'date': feedback['date']
                }
                if len(perf['examples']) < 10:  # 只保留最近10个示例
                    perf['examples'].append(example)
    
    def _update_cross_analysis(self, feedback: Dict):
        """更新交叉分析数据"""
        cross = self.learning_data['cross_analysis']
        
        # 行业+平台
        ip_key = f"{feedback['industry']}|{feedback['platform']}"
        if ip_key not in cross['industry_platform']:
            cross['industry_platform'][ip_key] = {'count': 0, 'scores': [], 'avg_score': 0}
        cross['industry_platform'][ip_key]['count'] += 1
        cross['industry_platform'][ip_key]['scores'].append(feedback['engagement_score'])
        cross['industry_platform'][ip_key]['avg_score'] = statistics.mean(cross['industry_platform'][ip_key]['scores'])
        
        # 行业+角度
        ia_key = f"{feedback['industry']}|{feedback['angle']}"
        if ia_key not in cross['industry_angle']:
            cross['industry_angle'][ia_key] = {'count': 0, 'scores': [], 'avg_score': 0}
        cross['industry_angle'][ia_key]['count'] += 1
        cross['industry_angle'][ia_key]['scores'].append(feedback['engagement_score'])
        cross['industry_angle'][ia_key]['avg_score'] = statistics.mean(cross['industry_angle'][ia_key]['scores'])
        
        # 平台+角度
        pa_key = f"{feedback['platform']}|{feedback['angle']}"
        if pa_key not in cross['platform_angle']:
            cross['platform_angle'][pa_key] = {'count': 0, 'scores': [], 'avg_score': 0}
        cross['platform_angle'][pa_key]['count'] += 1
        cross['platform_angle'][pa_key]['scores'].append(feedback['engagement_score'])
        cross['platform_angle'][pa_key]['avg_score'] = statistics.mean(cross['platform_angle'][pa_key]['scores'])
        
        # 时间段+平台
        tp_key = f"{feedback.get('time_slot', 'morning')}|{feedback['platform']}"
        if tp_key not in cross['time_platform']:
            cross['time_platform'][tp_key] = {'count': 0, 'scores': [], 'avg_score': 0}
        cross['time_platform'][tp_key]['count'] += 1
        cross['time_platform'][tp_key]['scores'].append(feedback['engagement_score'])
        cross['time_platform'][tp_key]['avg_score'] = statistics.mean(cross['time_platform'][tp_key]['scores'])
    
    def _update_confidence_scores(self):
        """更新置信度分数"""
        conf = self.learning_data['confidence_scores']
        
        # 行业置信度
        for industry, data in self.learning_data['industry_performance'].items():
            conf['industry'][industry] = self._calculate_confidence(data['scores'], data['count'])
        
        # 平台置信度
        for platform, data in self.learning_data['platform_performance'].items():
            conf['platform'][platform] = self._calculate_confidence(data['scores'], data['count'])
        
        # 角度置信度
        for angle, data in self.learning_data['angle_performance'].items():
            conf['angle'][angle] = self._calculate_confidence(data['scores'], data['count'])
        
        # 时间段置信度
        for slot, data in self.learning_data['time_slot_performance'].items():
            conf['time_slot'][slot] = self._calculate_confidence(data['scores'], data['count'])
        
        # 整体置信度
        total_samples = len(self.feedback_data)
        if total_samples >= self.confidence_params['high_confidence_samples']:
            conf['overall'] = self.confidence_params['max_confidence']
        else:
            conf['overall'] = min(
                total_samples * self.confidence_params['confidence_boost_per_sample'],
                self.confidence_params['max_confidence']
            )
    
    def _update_trends(self, feedback: Dict):
        """更新趋势数据"""
        trends = self.learning_data['trends']
        
        # 添加每日分数
        trends['daily_scores'].append({
            'date': feedback['date'],
            'score': feedback['engagement_score'],
            'content_id': feedback['id']
        })
        
        # 只保留最近30天的数据
        if len(trends['daily_scores']) > 30:
            trends['daily_scores'] = trends['daily_scores'][-30:]
        
        # 计算周提升率
        if len(trends['daily_scores']) >= 14:
            recent_week = [d['score'] for d in trends['daily_scores'][-7:]]
            previous_week = [d['score'] for d in trends['daily_scores'][-14:-7]]
            
            recent_avg = statistics.mean(recent_week)
            previous_avg = statistics.mean(previous_week)
            
            if previous_avg > 0:
                trends['weekly_improvement'] = (recent_avg - previous_avg) / previous_avg * 100
        
        # 判断趋势
        if trends['weekly_improvement'] > 5:
            trends['momentum'] = 'rising'
        elif trends['weekly_improvement'] < -5:
            trends['momentum'] = 'falling'
        else:
            trends['momentum'] = 'stable'
    
    def _generate_optimization_rules(self):
        """生成优化规则"""
        rules = self.learning_data['optimization_rules']
        
        # 清空旧规则
        for rule_type in rules:
            rules[rule_type] = []
        
        # 1. 行业规则
        industry_sorted = sorted(
            self.learning_data['industry_performance'].items(),
            key=lambda x: x[1]['avg_score'],
            reverse=True
        )
        for i, (industry, data) in enumerate(industry_sorted[:3]):
            confidence = self.learning_data['confidence_scores']['industry'].get(industry, 0)
            rules['industry_rules'].append({
                "rule_id": f"ind_{i+1:03d}",
                "rank": i + 1,
                "industry": industry,
                "action": f"优先推荐 '{industry}' 行业选题",
                "score_boost": round(data['avg_score'], 2),
                "confidence": round(confidence, 2),
                "sample_count": data['count'],
                "recommendation": "强烈推荐" if confidence > 0.7 else "推荐" if confidence > 0.4 else "待验证"
            })
        
        # 2. 平台规则
        platform_sorted = sorted(
            self.learning_data['platform_performance'].items(),
            key=lambda x: x[1]['avg_score'],
            reverse=True
        )
        for i, (platform, data) in enumerate(platform_sorted):
            confidence = self.learning_data['confidence_scores']['platform'].get(platform, 0)
            rules['platform_rules'].append({
                "rule_id": f"plat_{i+1:03d}",
                "platform": platform,
                "action": f"优先在 {platform} 发布",
                "score_boost": round(data['avg_score'], 2),
                "confidence": round(confidence, 2),
                "sample_count": data['count']
            })
        
        # 3. 角度规则
        angle_sorted = sorted(
            self.learning_data['angle_performance'].items(),
            key=lambda x: x[1]['avg_score'],
            reverse=True
        )
        for i, (angle, data) in enumerate(angle_sorted[:3]):
            confidence = self.learning_data['confidence_scores']['angle'].get(angle, 0)
            rules['angle_rules'].append({
                "rule_id": f"angle_{i+1:03d}",
                "angle": angle,
                "action": f"多使用 '{angle}' 内容角度",
                "score_boost": round(data['avg_score'], 2),
                "confidence": round(confidence, 2),
                "sample_count": data['count']
            })
        
        # 4. 时间规则
        time_sorted = sorted(
            self.learning_data['time_slot_performance'].items(),
            key=lambda x: x[1]['avg_score'],
            reverse=True
        )
        for i, (slot, data) in enumerate(time_sorted):
            if data['count'] > 0:
                confidence = self.learning_data['confidence_scores']['time_slot'].get(slot, 0)
                slot_label = self.time_slot_weights.get(slot, {}).get('label', slot)
                rules['time_rules'].append({
                    "rule_id": f"time_{i+1:03d}",
                    "time_slot": slot,
                    "label": slot_label,
                    "action": f"建议在 {slot_label} 发布",
                    "score_boost": round(data['avg_score'], 2),
                    "confidence": round(confidence, 2),
                    "sample_count": data['count']
                })
        
        # 5. 竞品词规则
        comp_sorted = sorted(
            self.learning_data['competitor_keyword_performance'].items(),
            key=lambda x: x[1]['avg_score'],
            reverse=True
        )
        for i, (keyword, data) in enumerate(comp_sorted[:5]):
            rules['competitor_rules'].append({
                "rule_id": f"comp_{i+1:03d}",
                "keyword": keyword,
                "industry": data['industry'],
                "action": f"提及 '{keyword}' 可能有助提升效果",
                "score_boost": round(data['avg_score'], 2),
                "sample_count": data['count']
            })
        
        # 6. 情绪词规则
        for emotion_type, data in self.learning_data['emotion_keyword_performance'].items():
            if data['count'] > 0:
                weight = self.emotion_weights.get(emotion_type, {}).get('weight', 1.0)
                rules['emotion_rules'].append({
                    "rule_id": f"emotion_{emotion_type}",
                    "emotion_type": emotion_type,
                    "keywords": self.emotion_weights.get(emotion_type, {}).get('keywords', [])[:5],
                    "action": f"使用{emotion_type}情绪词可带来 {weight:.2f}x 效果乘数",
                    "avg_score": round(data['avg_score'], 2),
                    "sample_count": data['count']
                })
        
        # 7. 组合规则（基于交叉分析）
        cross = self.learning_data['cross_analysis']
        
        # 最佳行业+平台组合
        ip_sorted = sorted(
            cross['industry_platform'].items(),
            key=lambda x: x[1]['avg_score'],
            reverse=True
        )[:3]
        for i, (key, data) in enumerate(ip_sorted):
            industry, platform = key.split('|')
            rules['combination_rules'].append({
                "rule_id": f"combo_ip_{i+1:03d}",
                "type": "industry_platform",
                "combination": f"{industry} + {platform}",
                "action": f"推荐 '{industry}' 内容发布到 {platform}",
                "score_boost": round(data['avg_score'], 2),
                "confidence": round(self._calculate_confidence(data['scores'], data['count']), 2),
                "sample_count": data['count']
            })
        
        # 最佳平台+角度组合
        pa_sorted = sorted(
            cross['platform_angle'].items(),
            key=lambda x: x[1]['avg_score'],
            reverse=True
        )[:3]
        for i, (key, data) in enumerate(pa_sorted):
            platform, angle = key.split('|')
            rules['combination_rules'].append({
                "rule_id": f"combo_pa_{i+1:03d}",
                "type": "platform_angle",
                "combination": f"{platform} + {angle}",
                "action": f"在 {platform} 使用 '{angle}' 角度效果好",
                "score_boost": round(data['avg_score'], 2),
                "confidence": round(self._calculate_confidence(data['scores'], data['count']), 2),
                "sample_count": data['count']
            })
    
    def _update_summary(self):
        """更新汇总数据"""
        summary = self.learning_data['summary']
        
        total = len(self.feedback_data)
        if total == 0:
            return
        
        # 最佳表现
        summary['total_feedback_analyzed'] = total
        
        if self.learning_data['industry_performance']:
            summary['top_performing_industry'] = max(
                self.learning_data['industry_performance'].items(),
                key=lambda x: x[1]['avg_score']
            )[0]
        
        if self.learning_data['platform_performance']:
            summary['top_performing_platform'] = max(
                self.learning_data['platform_performance'].items(),
                key=lambda x: x[1]['avg_score']
            )[0]
        
        if self.learning_data['angle_performance']:
            summary['top_performing_angle'] = max(
                self.learning_data['angle_performance'].items(),
                key=lambda x: x[1]['avg_score']
            )[0]
        
        # 平均互动分
        all_scores = [f['engagement_score'] for f in self.feedback_data]
        summary['avg_engagement_all'] = round(statistics.mean(all_scores), 2)
        
        # 置信度
        summary['overall_confidence'] = round(self.learning_data['confidence_scores']['overall'], 2)
        
        # 趋势
        summary['momentum'] = self.learning_data['trends']['momentum']
        summary['weekly_improvement'] = round(self.learning_data['trends']['weekly_improvement'], 2)
    
    def _save_feedback(self):
        """保存反馈数据"""
        with open(self.feedback_file, 'w', encoding='utf-8') as f:
            json.dump(self.feedback_data, f, ensure_ascii=False, indent=2)
    
    def _save_learning(self):
        """保存学习数据"""
        with open(self.learning_file, 'w', encoding='utf-8') as f:
            json.dump(self.learning_data, f, ensure_ascii=False, indent=2)
    
    def show_enhanced_dashboard(self):
        """显示增强版仪表盘"""
        print("\n" + "=" * 70)
        print("🧠 增强版自学习系统仪表盘 v2.0")
        print("=" * 70)
        
        print(f"\n📊 数据概览:")
        print(f"  总反馈数: {len(self.feedback_data)}")
        print(f"  系统版本: {self.learning_data.get('version', '1.0')}")
        print(f"  整体置信度: {self.learning_data['confidence_scores']['overall']*100:.0f}%")
        print(f"  趋势: {self.learning_data['trends']['momentum']}")
        
        # 置信度矩阵
        print(f"\n🎯 置信度矩阵:")
        for category in ['industry', 'platform', 'angle', 'time_slot']:
            scores = self.learning_data['confidence_scores'][category]
            if scores:
                print(f"  {category}:")
                for key, conf in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]:
                    print(f"    - {key}: {conf*100:.0f}%")
        
        # TOP表现
        if self.learning_data['industry_performance']:
            print(f"\n🏆 TOP3 行业 (按平均分):")
            top_industries = sorted(
                self.learning_data['industry_performance'].items(),
                key=lambda x: x[1]['avg_score'],
                reverse=True
            )[:3]
            for i, (industry, data) in enumerate(top_industries, 1):
                conf = self.learning_data['confidence_scores']['industry'].get(industry, 0)
                print(f"  {i}. {industry}: {data['avg_score']:.2f}分 (置信度: {conf*100:.0f}%)")
        
        # 最佳组合
        print(f"\n🔗 最佳组合推荐:")
        cross = self.learning_data['cross_analysis']
        if cross['industry_platform']:
            best_combo = max(
                cross['industry_platform'].items(),
                key=lambda x: x[1]['avg_score']
            )
            industry, platform = best_combo[0].split('|')
            print(f"  行业+平台: {industry} + {platform} ({best_combo[1]['avg_score']:.2f}分)")
        
        if cross['platform_angle']:
            best_combo = max(
                cross['platform_angle'].items(),
                key=lambda x: x[1]['avg_score']
            )
            platform, angle = best_combo[0].split('|')
            print(f"  平台+角度: {platform} + {angle} ({best_combo[1]['avg_score']:.2f}分)")
        
        print("\n" + "=" * 70)
    
    def generate_enhanced_insights(self) -> str:
        """生成增强版洞察报告"""
        if not self.feedback_data:
            return "暂无反馈数据，请先添加内容效果反馈。"
        
        lines = []
        
        lines.append("# 🧠 增强版自学习优化报告 v2.0\n")
        lines.append(f"> 生成时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}")
        lines.append(f"> 反馈样本数: {len(self.feedback_data)}")
        lines.append(f"> 整体置信度: {self.learning_data['confidence_scores']['overall']*100:.0f}%")
        lines.append(f"> 系统趋势: {self.learning_data['trends']['momentum']}\n")
        
        # 1. �