#!/usr/bin/env python3
"""
热点趋势预测模块 - Trend Predictor
分析热点热度变化趋势，预测未来走势，识别潜在爆发热点
"""

import json
import os
import glob
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Tuple, Optional
import re


class TrendPredictor:
    """热点趋势预测器"""
    
    # 趋势阈值配置
    RISING_THRESHOLD = 0.15  # 增长率>15%视为上升
    DECLINING_THRESHOLD = -0.15  # 增长率<-15%视为下降
    EXPLOSION_THRESHOLD = 0.20  # 增长率>20%视为潜在爆发
    STABLE_RANGE = 0.10  # 波动<10%视为稳定
    
    # 权重配置（用于预测算法）
    WEIGHTS = {
        'historical_trend': 0.25,      # 历史趋势权重
        'social_signal': 0.30,          # 社交信号权重
        'event_boost': 0.20,            # 事件推动权重
        'seasonal_factor': 0.15,        # 季节因素权重
        'competitive_index': 0.10       # 竞争指数权重
    }
    
    def __init__(self, data_dir: str = None):
        """初始化预测器"""
        if data_dir is None:
            data_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = data_dir
        self.historical_data = {}
        self.trend_cache = {}
        
    def load_historical_reports(self, days: int = 7) -> Dict[str, List[dict]]:
        """
        加载历史报告数据
        
        Args:
            days: 加载最近N天的数据
            
        Returns:
            按日期组织的历史数据
        """
        reports = {}
        report_files = sorted(glob.glob(os.path.join(self.data_dir, 'report_*.json')))
        
        # 只取最近的报告文件
        recent_files = report_files[-(days*3):] if len(report_files) > days*3 else report_files
        
        for filepath in recent_files:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # 提取日期
                filename = os.path.basename(filepath)
                date_match = re.search(r'report_(\d{8})', filename)
                if date_match:
                    date_str = date_match.group(1)
                    reports[date_str] = data
            except Exception as e:
                print(f"加载报告失败 {filepath}: {e}")
                continue
                
        self.historical_data = reports
        return reports
    
    def extract_topic_history(self, topic_title: str) -> List[dict]:
        """
        提取某个话题的历史热度数据
        
        Args:
            topic_title: 话题标题（支持模糊匹配）
            
        Returns:
            该话题的历史热度记录列表
        """
        history = []
        title_lower = topic_title.lower()
        title_short = topic_title[:10]  # 取前10字符用于模糊匹配
        
        for date_str, report in self.historical_data.items():
            platforms = report.get('platforms', {})
            
            for platform_key, platform_data in platforms.items():
                if not platform_data.get('success'):
                    continue
                    
                for item in platform_data.get('data', []):
                    item_title = item.get('title', '')
                    
                    # 精确匹配或模糊匹配
                    if item_title == topic_title or \
                       title_short in item_title or \
                       item_title.lower() == title_lower:
                        history.append({
                            'date': date_str,
                            'platform': platform_data.get('platform', platform_key),
                            'title': item_title,
                            'hot_value': item.get('hot_value', 0),
                            'rank': item.get('rank', 0)
                        })
        
        # 按日期排序
        history.sort(key=lambda x: x['date'])
        return history
    
    def calculate_trend(self, history: List[dict]) -> dict:
        """
        计算趋势状态和增长率
        
        Args:
            history: 话题历史数据
            
        Returns:
            趋势分析结果
        """
        if len(history) < 2:
            return {
                'trend': 'unknown',
                'growth_rate': 0,
                'confidence': 0.1,
                'description': '数据不足，无法判断趋势'
            }
        
        # 获取最近的数据点
        recent = history[-3:] if len(history) >= 3 else history
        hot_values = [h['hot_value'] for h in recent]
        
        # 计算增长率
        if hot_values[0] > 0:
            growth_rate = (hot_values[-1] - hot_values[0]) / hot_values[0]
        else:
            growth_rate = 0
        
        # 计算趋势稳定性（方差）
        if len(hot_values) > 1:
            mean_val = sum(hot_values) / len(hot_values)
            variance = sum((v - mean_val) ** 2 for v in hot_values) / len(hot_values)
            stability = 1 / (1 + variance / (mean_val ** 2)) if mean_val > 0 else 0.5
        else:
            stability = 0.5
        
        # 判断趋势
        if growth_rate > self.EXPLOSION_THRESHOLD:
            trend = 'explosion'  # 爆发
            description = f"热度快速增长（+{growth_rate*100:.1f}%），潜在爆发热点"
        elif growth_rate > self.RISING_THRESHOLD:
            trend = 'rising'  # 上升
            description = f"热度稳步上升（+{growth_rate*100:.1f}%）"
        elif growth_rate < self.DECLINING_THRESHOLD:
            trend = 'declining'  # 下降
            description = f"热度正在衰减（{growth_rate*100:.1f}%）"
        elif abs(growth_rate) <= self.STABLE_RANGE:
            trend = 'stable'  # 稳定
            description = f"热度保持稳定（{growth_rate*100:.1f}%）"
        else:
            trend = 'fluctuating'  # 波动
            description = f"热度波动中（{growth_rate*100:.1f}%）"
        
        # 计算置信度（基于数据点数量和稳定性）
        confidence = min(0.95, stability * 0.6 + min(len(history) / 10, 0.4))
        
        return {
            'trend': trend,
            'growth_rate': growth_rate,
            'stability': stability,
            'confidence': confidence,
            'description': description,
            'avg_hot_value': mean_val if 'mean_val' in dir() else hot_values[-1]
        }
    
    def predict_future(self, history: List[dict], days: int = 3) -> dict:
        """
        预测未来N天的热度走势
        
        Args:
            history: 历史数据
            days: 预测天数
            
        Returns:
            预测结果
        """
        if len(history) < 2:
            return {
                'success': False,
                'message': '数据不足，无法预测'
            }
        
        trend_result = self.calculate_trend(history)
        hot_values = [h['hot_value'] for h in history[-5:]] if len(history) >= 5 else [h['hot_value'] for h in history]
        
        # 使用加权移动平均进行预测
        weights = [1, 2, 3, 4, 5][-len(hot_values):]
        weighted_avg = sum(v * w for v, w in zip(hot_values, weights)) / sum(weights)
        
        # 基于趋势计算预测值
        growth_rate = trend_result['growth_rate']
        predictions = []
        
        current_value = hot_values[-1]
        for i in range(1, days + 1):
            # 应用衰减的增长率（热度增长会逐渐放缓）
            decay_factor = 0.85 ** i
            predicted_growth = growth_rate * decay_factor
            predicted_value = current_value * (1 + predicted_growth * i / days)
            
            # 计算置信区间
            confidence_range = predicted_value * (0.15 + 0.05 * i)  # 越远越不确定
            
            predictions.append({
                'day': i,
                'predicted_value': max(0, int(predicted_value)),
                'confidence_lower': max(0, int(predicted_value - confidence_range)),
                'confidence_upper': int(predicted_value + confidence_range),
                'confidence': max(0.5, trend_result['confidence'] - 0.1 * i)
            })
            
            current_value = predicted_value
        
        # 找出预测峰值日
        peak_day = max(predictions, key=lambda x: x['predicted_value'])
        
        return {
            'success': True,
            'current_hot_value': hot_values[-1],
            'predictions': predictions,
            'peak_day': peak_day['day'],
            'peak_value': peak_day['predicted_value'],
            'trend': trend_result['trend'],
            'growth_rate': growth_rate,
            'confidence': trend_result['confidence']
        }
    
    def identify_explosion_candidates(self, min_growth: float = None) -> List[dict]:
        """
        识别潜在爆发热点
        
        Args:
            min_growth: 最小增长率阈值，默认使用EXPLOSION_THRESHOLD
            
        Returns:
            潜在爆发热点列表
        """
        if min_growth is None:
            min_growth = self.EXPLOSION_THRESHOLD
            
        candidates = []
        
        # 从最新报告中提取所有话题
        if not self.historical_data:
            self.load_historical_reports()
            
        if not self.historical_data:
            return candidates
            
        latest_date = max(self.historical_data.keys())
        latest_report = self.historical_data[latest_date]
        
        # 收集所有话题
        all_topics = set()
        for platform_key, platform_data in latest_report.get('platforms', {}).items():
            if not platform_data.get('success'):
                continue
            for item in platform_data.get('data', []):
                all_topics.add(item.get('title', ''))
        
        # 分析每个话题
        for topic in all_topics:
            if not topic:
                continue
                
            history = self.extract_topic_history(topic)
            if len(history) < 2:
                continue
                
            trend_result = self.calculate_trend(history)
            
            if trend_result['growth_rate'] >= min_growth:
                candidates.append({
                    'title': topic,
                    'trend': trend_result['trend'],
                    'growth_rate': trend_result['growth_rate'],
                    'current_hot': history[-1]['hot_value'] if history else 0,
                    'confidence': trend_result['confidence'],
                    'platforms': list(set(h['platform'] for h in history)),
                    'history_count': len(history)
                })
        
        # 按增长率排序
        candidates.sort(key=lambda x: x['growth_rate'], reverse=True)
        return candidates
    
    def get_decay_warnings(self) -> List[dict]:
        """
        获取热度衰减预警
        
        Returns:
            衰减中的热点列表
        """
        warnings = []
        
        if not self.historical_data:
            self.load_historical_reports()
            
        if not self.historical_data:
            return warnings
            
        latest_date = max(self.historical_data.keys())
        latest_report = self.historical_data[latest_date]
        
        # 收集所有话题
        all_topics = set()
        for platform_key, platform_data in latest_report.get('platforms', {}).items():
            if not platform_data.get('success'):
                continue
            for item in platform_data.get('data', []):
                all_topics.add(item.get('title', ''))
        
        # 分析每个话题
        for topic in all_topics:
            if not topic:
                continue
                
            history = self.extract_topic_history(topic)
            if len(history) < 2:
                continue
                
            trend_result = self.calculate_trend(history)
            
            if trend_result['trend'] == 'declining':
                warnings.append({
                    'title': topic,
                    'current_hot': history[-1]['hot_value'] if history else 0,
                    'decay_rate': abs(trend_result['growth_rate']),
                    'platforms': list(set(h['platform'] for h in history)),
                    'description': trend_result['description']
                })
        
        # 按衰减率排序
        warnings.sort(key=lambda x: x['decay_rate'], reverse=True)
        return warnings
    
    def analyze_by_industry(self) -> Dict[str, dict]:
        """
        按行业分析趋势分布
        
        Returns:
            各行业的趋势分析
        """
        industry_analysis = {}
        
        if not self.historical_data:
            self.load_historical_reports()
            
        if not self.historical_data:
            return industry_analysis
        
        # 行业关键词（与主模块保持一致）
        INDUSTRY_KEYWORDS = {
            "美妆": ["美妆", "护肤", "口红", "粉底", "面膜", "化妆", "眼影", "防晒", "精华", "洁面", "医美", "玻尿酸", "彩妆", "卸妆", "遮瑕"],
            "母婴": ["母婴", "宝宝", "奶粉", "纸尿裤", "孕妇", "婴儿", "亲子", "育儿", "备孕", "新生儿", "儿童", "辅食", "玩具", "童装"],
            "数码": ["手机", "电脑", "数码", "iPhone", "华为", "小米", "苹果", "芯片", "显卡", "耳机", "平板", "笔记本", "智能", "AI", "科技", "游戏"],
            "服装": ["穿搭", "服装", "时尚", "衣服", "卫衣", "牛仔裤", "运动鞋", "潮牌", "女装", "男装", "童装", "汉服", "JK", "风衣"],
            "食品": ["食品", "美食", "零食", "饮料", "奶茶", "火锅", "烧烤", "预制菜", "健康食品", "减肥餐", "咖啡", "茶叶", "水果", "生鲜"],
            "汽车": ["汽车", "新能源", "电车", "特斯拉", "比亚迪", "理想", "蔚来", "小鹏", "燃油车", "自驾", "驾照", "汽车用品", "车载"],
            "大健康": ["健康", "养生", "保健品", "维生素", "医疗", "体检", "减肥", "健身", "睡眠", "心理健康", "中医药", "药店", "医院"],
            "快消": ["洗发水", "牙膏", "洗衣液", "纸巾", "沐浴露", "洗面奶", "卫生巾", "湿巾", "清洁", "日用", "日化", "快消"],
            "家电": ["家电", "冰箱", "空调", "洗衣机", "电视", "扫地机", "空气净化器", "净水器", "热水器", "厨房电器", "智能家居"]
        }
        
        # 收集各行业话题
        industry_topics = defaultdict(list)
        
        latest_date = max(self.historical_data.keys())
        latest_report = self.historical_data[latest_date]
        
        for platform_key, platform_data in latest_report.get('platforms', {}).items():
            if not platform_data.get('success'):
                continue
            for item in platform_data.get('data', []):
                title = item.get('title', '')
                desc = item.get('desc', '')
                text = f"{title} {desc}"
                
                for industry, keywords in INDUSTRY_KEYWORDS.items():
                    for kw in keywords:
                        if kw in text:
                            industry_topics[industry].append({
                                'title': title,
                                'hot_value': item.get('hot_value', 0),
                                'platform': platform_data.get('platform', platform_key)
                            })
                            break
        
        # 分析各行业趋势
        for industry, topics in industry_topics.items():
            if not topics:
                continue
                
            # 计算行业总热度
            total_hot = sum(t['hot_value'] for t in topics)
            avg_hot = total_hot / len(topics) if topics else 0
            
            # 分析行业话题的趋势
            rising_count = 0
            declining_count = 0
            stable_count = 0
            
            for topic in topics:
                history = self.extract_topic_history(topic['title'])
                if len(history) >= 2:
                    trend_result = self.calculate_trend(history)
                    if trend_result['trend'] in ['rising', 'explosion']:
                        rising_count += 1
                    elif trend_result['trend'] == 'declining':
                        declining_count += 1
                    else:
                        stable_count += 1
            
            # 确定行业整体趋势
            if rising_count > declining_count and rising_count > stable_count:
                industry_trend = 'rising'
            elif declining_count > rising_count and declining_count > stable_count:
                industry_trend = 'declining'
            else:
                industry_trend = 'stable'
            
            industry_analysis[industry] = {
                'total_hot': total_hot,
                'avg_hot': avg_hot,
                'topic_count': len(topics),
                'rising_count': rising_count,
                'declining_count': declining_count,
                'stable_count': stable_count,
                'trend': industry_trend,
                'top_topics': sorted(topics, key=lambda x: x['hot_value'], reverse=True)[:5]
            }
        
        return industry_analysis
    
    def generate_prediction_report(self) -> dict:
        """
        生成完整的趋势预测报告
        
        Returns:
            预测报告字典
        """
        # 加载历史数据
        self.load_historical_reports(days=7)
        
        if not self.historical_data:
            return {
                'success': False,
                'message': '无历史数据可供分析',
                'generated_at': datetime.now().isoformat()
            }
        
        # 获取最新报告日期
        latest_date = max(self.historical_data.keys())
        latest_report = self.historical_data[latest_date]
        
        # 统计各趋势类型数量
        trend_stats = {
            'rising': 0,
            'declining': 0,
            'stable': 0,
            'explosion': 0,
            'fluctuating': 0,
            'unknown': 0
        }
        
        # 收集所有话题并分析趋势
        all_topics = set()
        topic_trends = []
        
        for platform_key, platform_data in latest_report.get('platforms', {}).items():
            if not platform_data.get('success'):
                continue
            for item in platform_data.get('data', []):
                all_topics.add(item.get('title', ''))
        
        for topic in all_topics:
            if not topic:
                continue
            history = self.extract_topic_history(topic)
            if len(history) >= 1:
                trend_result = self.calculate_trend(history)
                trend_stats[trend_result['trend']] += 1
                
                topic_trends.append({
                    'title': topic,
                    'trend': trend_result['trend'],
                    'growth_rate': trend_result['growth_rate'],
                    'current_hot': history[-1]['hot_value'] if history else 0,
                    'confidence': trend_result['confidence']
                })
        
        # 识别爆发热点
        explosion_candidates = self.identify_explosion_candidates()
        
        # 获取衰减预警
        decay_warnings = self.get_decay_warnings()
        
        # 行业趋势分析
        industry_analysis = self.analyze_by_industry()
        
        # 生成报告
        report = {
            'success': True,
            'generated_at': datetime.now().isoformat(),
            'data_range': {
                'start_date': min(self.historical_data.keys()) if self.historical_data else None,
                'end_date': latest_date,
                'report_count': len(self.historical_data)
            },
            'overview': {
                'total_topics': len(all_topics),
                'trend_distribution': trend_stats,
                'rising_count': trend_stats['rising'] + trend_stats['explosion'],
                'declining_count': trend_stats['declining'],
                'stable_count': trend_stats['stable']
            },
            'explosion_candidates': explosion_candidates[:20],  # Top 20
            'decay_warnings': decay_warnings[:20],  # Top 20
            'industry_analysis': industry_analysis,
            'best_publish_time': self._get_best_publish_time(),
            'topic_predictions': self._get_top_topic_predictions(topic_trends[:10])
        }
        
        return report
    
    def _get_best_publish_time(self) -> dict:
        """
        获取最佳发布时间推荐
        
        Returns:
            各平台的最佳发布时间
        """
        return {
            'douyin': {
                'name': '抖音',
                'best_slots': ['18:00-22:00', '12:00-14:00', '7:00-9:00'],
                'peak_time': '18:00-22:00',
                'tip': '晚间黄金时段流量最大'
            },
            'xiaohongshu': {
                'name': '小红书',
                'best_slots': ['20:00-23:00', '12:00-13:00', '8:00-10:00'],
                'peak_time': '20:00-23:00',
                'tip': '睡前刷小红书是用户习惯'
            },
            'weibo': {
                'name': '微博',
                'best_slots': ['12:00-14:00', '17:00-19:00', '7:00-9:00'],
                'peak_time': '12:00-14:00',
                'tip': '午休时段互动率最高'
            },
            'kuaishou': {
                'name': '快手',
                'best_slots': ['19:00-22:00', '11:00-13:00', '6:00-8:00'],
                'peak_time': '19:00-22:00',
                'tip': '快手用户活跃在晚间'
            },
            'bilibili': {
                'name': 'B站',
                'best_slots': ['20:00-23:00', '17:00-19:00'],
                'peak_time': '20:00-23:00',
                'tip': 'B站用户活跃在夜间'
            },
            'shipinhao': {
                'name': '视频号',
                'best_slots': ['18:00-21:00', '7:00-9:00'],
                'peak_time': '18:00-21:00',
                'tip': '视频号与微信生态联动'
            }
        }
    
    def _get_top_topic_predictions(self, top_topics: List[dict]) -> List[dict]:
        """
        获取热门话题的未来预测
        
        Args:
            top_topics: 热门话题列表
            
        Returns:
            带预测的话题列表
        """
        predictions = []
        
        for topic in top_topics:
            history = self.extract_topic_history(topic['title'])
            if len(history) >= 2:
                prediction = self.predict_future(history, days=3)
                if prediction['success']:
                    predictions.append({
                        'title': topic['title'],
                        'current_hot': topic['current_hot'],
                        'trend': topic['trend'],
                        'growth_rate': topic['growth_rate'],
                        'predictions': prediction['predictions'],
                        'peak_day': prediction['peak_day'],
                        'peak_value': prediction['peak_value'],
                        'confidence': prediction['confidence']
                    })
        
        return predictions
    
    def save_report(self, report: dict = None, output_path: str = None) -> str:
        """
        保存预测报告
        
        Args:
            report: 报告内容，如果为None则自动生成
            output_path: 输出路径，如果为None则自动生成
            
        Returns:
            保存的文件路径
        """
        if report is None:
            report = self.generate_prediction_report()
        
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = os.path.join(self.data_dir, f'trend_prediction_{timestamp}.json')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 趋势预测报告已保存: {output_path}")
        return output_path


def main():
    """主函数"""
    predictor = TrendPredictor()
    
    print("📊 开始热点趋势预测分析...")
    
    # 加载历史数据
    reports = predictor.load_historical_reports(days=7)
    print(f"✅ 已加载 {len(reports)} 份历史报告")
    
    # 生成预测报告
    report = predictor.generate_prediction_report()
    
    if report['success']:
        print(f"\n📈 趋势分布:")
        for trend, count in report['overview']['trend_distribution'].items():
            if count > 0:
                print(f"  - {trend}: {count} 个话题")
        
        print(f"\n🚀 潜在爆发热点 ({len(report['explosion_candidates'])} 个):")
        for i, item in enumerate(report['explosion_candidates'][:5], 1):
            print(f"  {i}. {item['title'][:20]}... 增长率: +{item['growth_rate']*100:.1f}%")
        
        print(f"\n⚠️ 热度衰减预警 ({len(report['decay_warnings'])} 个):")
        for i, item in enumerate(report['decay_warnings'][:5], 1):
            print(f"  {i}. {item['title'][:20]}... 衰减率: -{item['decay_rate']*100:.1f}%")
        
        print(f"\n📁 行业趋势分析:")
        for industry, data in report['industry_analysis'].items():
            trend_emoji = {'rising': '📈', 'declining': '📉', 'stable': '📊'}.get(data['trend'], '📊')
            print(f"  {trend_emoji} {industry}: {data['topic_count']} 个话题, 趋势: {data['trend']}")
        
        # 保存报告
        output_path = predictor.save_report(report)
        
        return report
    else:
        print(f"❌ {report.get('message', '预测失败')}")
        return report


if __name__ == "__main__":
    main()
