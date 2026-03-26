#!/usr/bin/env python3
"""
🧠 效果反馈与自学习系统
功能：
1. 收集内容效果数据（互动量、转化率）
2. 分析哪些热点/角度/平台效果最好
3. 自动优化推荐算法
4. 生成优化建议报告
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict
import statistics

class SelfLearningSystem:
    """自学习系统"""
    
    def __init__(self):
        self.workspace = Path("/Users/zhangjingwei/.qclaw/workspace/hotspot-tracker")
        self.feedback_file = self.workspace / "content_feedback.json"
        self.learning_file = self.workspace / "learning_data.json"
        self.insights_file = self.workspace / "optimization_insights.md"
        
        self.feedback_data = self._load_feedback()
        self.learning_data = self._load_learning()
    
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
        """初始化学习数据"""
        return {
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "industry_performance": {},
            "platform_performance": {},
            "angle_performance": {},
            "hot_topic_performance": {},
            "time_performance": {},
            "optimization_rules": []
        }
    
    def add_feedback(self, content_id: str, industry: str, platform: str, 
                     angle: str, hot_topic: str, metrics: Dict[str, Any]):
        """添加内容效果反馈"""
        feedback = {
            "id": content_id,
            "date": datetime.now().strftime("%Y%m%d"),
            "timestamp": datetime.now().isoformat(),
            "industry": industry,
            "platform": platform,
            "angle": angle,
            "hot_topic": hot_topic,
            "metrics": metrics,  # likes, comments, shares, conversion_rate, etc.
            "engagement_score": self._calculate_engagement(metrics)
        }
        
        self.feedback_data.append(feedback)
        self._save_feedback()
        
        # 实时更新学习数据
        self._update_learning(feedback)
        
        print(f"✅ 反馈已记录: {content_id} | 互动分: {feedback['engagement_score']:.2f}")
    
    def _calculate_engagement(self, metrics: Dict) -> float:
        """计算互动分数"""
        # 加权计算互动分数
        likes = metrics.get('likes', 0)
        comments = metrics.get('comments', 0) * 3  # 评论权重更高
        shares = metrics.get('shares', 0) * 5  # 分享权重最高
        views = metrics.get('views', 1)
        
        if views == 0:
            views = 1
        
        engagement_rate = (likes + comments + shares) / views * 100
        return min(engagement_rate, 100)  # 上限100分
    
    def _update_learning(self, feedback: Dict):
        """更新学习数据"""
        # 更新行业表现
        industry = feedback['industry']
        if industry not in self.learning_data['industry_performance']:
            self.learning_data['industry_performance'][industry] = {
                'count': 0, 'total_score': 0, 'avg_score': 0, 'scores': []
            }
        
        self.learning_data['industry_performance'][industry]['count'] += 1
        self.learning_data['industry_performance'][industry]['total_score'] += feedback['engagement_score']
        self.learning_data['industry_performance'][industry]['scores'].append(feedback['engagement_score'])
        self.learning_data['industry_performance'][industry]['avg_score'] = (
            self.learning_data['industry_performance'][industry]['total_score'] / 
            self.learning_data['industry_performance'][industry]['count']
        )
        
        # 更新平台表现
        platform = feedback['platform']
        if platform not in self.learning_data['platform_performance']:
            self.learning_data['platform_performance'][platform] = {
                'count': 0, 'total_score': 0, 'avg_score': 0, 'scores': []
            }
        
        self.learning_data['platform_performance'][platform]['count'] += 1
        self.learning_data['platform_performance'][platform]['total_score'] += feedback['engagement_score']
        self.learning_data['platform_performance'][platform]['scores'].append(feedback['engagement_score'])
        self.learning_data['platform_performance'][platform]['avg_score'] = (
            self.learning_data['platform_performance'][platform]['total_score'] / 
            self.learning_data['platform_performance'][platform]['count']
        )
        
        # 更新角度表现
        angle = feedback['angle']
        if angle not in self.learning_data['angle_performance']:
            self.learning_data['angle_performance'][angle] = {
                'count': 0, 'total_score': 0, 'avg_score': 0, 'scores': []
            }
        
        self.learning_data['angle_performance'][angle]['count'] += 1
        self.learning_data['angle_performance'][angle]['total_score'] += feedback['engagement_score']
        self.learning_data['angle_performance'][angle]['scores'].append(feedback['engagement_score'])
        self.learning_data['angle_performance'][angle]['avg_score'] = (
            self.learning_data['angle_performance'][angle]['total_score'] / 
            self.learning_data['angle_performance'][angle]['count']
        )
        
        # 更新热点表现
        hot_topic = feedback['hot_topic']
        if hot_topic not in self.learning_data['hot_topic_performance']:
            self.learning_data['hot_topic_performance'][hot_topic] = {
                'count': 0, 'total_score': 0, 'avg_score': 0, 'scores': []
            }
        
        self.learning_data['hot_topic_performance'][hot_topic]['count'] += 1
        self.learning_data['hot_topic_performance'][hot_topic]['total_score'] += feedback['engagement_score']
        self.learning_data['hot_topic_performance'][hot_topic]['scores'].append(feedback['engagement_score'])
        self.learning_data['hot_topic_performance'][hot_topic]['avg_score'] = (
            self.learning_data['hot_topic_performance'][hot_topic]['total_score'] / 
            self.learning_data['hot_topic_performance'][hot_topic]['count']
        )
        
        self.learning_data['updated_at'] = datetime.now().isoformat()
        self._save_learning()
    
    def _save_feedback(self):
        """保存反馈数据"""
        with open(self.feedback_file, 'w', encoding='utf-8') as f:
            json.dump(self.feedback_data, f, ensure_ascii=False, indent=2)
    
    def _save_learning(self):
        """保存学习数据"""
        with open(self.learning_file, 'w', encoding='utf-8') as f:
            json.dump(self.learning_data, f, ensure_ascii=False, indent=2)
    
    def generate_insights(self) -> str:
        """生成优化洞察报告"""
        if not self.feedback_data:
            return "暂无反馈数据，请先添加内容效果反馈。"
        
        insights = []
        
        # 1. 行业洞察
        insights.append("## 🏭 行业表现洞察\n")
        industry_perf = sorted(
            self.learning_data['industry_performance'].items(),
            key=lambda x: x[1]['avg_score'],
            reverse=True
        )
        
        for i, (industry, data) in enumerate(industry_perf[:5], 1):
            insights.append(f"{i}. **{industry}** | 平均互动分: {data['avg_score']:.2f} | 样本数: {data['count']}")
        
        # 2. 平台洞察
        insights.append("\n## 📱 平台表现洞察\n")
        platform_perf = sorted(
            self.learning_data['platform_performance'].items(),
            key=lambda x: x[1]['avg_score'],
            reverse=True
        )
        
        for i, (platform, data) in enumerate(platform_perf, 1):
            insights.append(f"{i}. **{platform}** | 平均互动分: {data['avg_score']:.2f} | 样本数: {data['count']}")
        
        # 3. 内容角度洞察
        insights.append("\n## 🎯 内容角度洞察\n")
        angle_perf = sorted(
            self.learning_data['angle_performance'].items(),
            key=lambda x: x[1]['avg_score'],
            reverse=True
        )
        
        for i, (angle, data) in enumerate(angle_perf[:5], 1):
            insights.append(f"{i}. **{angle}** | 平均互动分: {data['avg_score']:.2f} | 样本数: {data['count']}")
        
        # 4. 热点效果洞察
        insights.append("\n## 🔥 热点效果洞察\n")
        hot_perf = sorted(
            self.learning_data['hot_topic_performance'].items(),
            key=lambda x: x[1]['avg_score'],
            reverse=True
        )
        
        for i, (topic, data) in enumerate(hot_perf[:5], 1):
            insights.append(f"{i}. **{topic}** | 平均互动分: {data['avg_score']:.2f} | 样本数: {data['count']}")
        
        # 5. 优化建议
        insights.append("\n## 💡 优化建议\n")
        
        # 最佳组合
        if industry_perf and platform_perf and angle_perf:
            best_industry = industry_perf[0][0]
            best_platform = platform_perf[0][0]
            best_angle = angle_perf[0][0]
            
            insights.append(f"### 🌟 最佳组合推荐")
            insights.append(f"- **行业:** {best_industry}")
            insights.append(f"- **平台:** {best_platform}")
            insights.append(f"- **角度:** {best_angle}")
            insights.append(f"- **预期效果:** 基于历史数据，此组合平均互动分可达 {industry_perf[0][1]['avg_score']:.2f}")
        
        # 改进建议
        insights.append("\n### 📈 改进建议")
        
        if len(self.feedback_data) >= 10:
            # 计算标准差，找出波动大的领域
            industry_std = {}
            for industry, data in self.learning_data['industry_performance'].items():
                if len(data['scores']) >= 3:
                    industry_std[industry] = statistics.stdev(data['scores'])
            
            if industry_std:
                most_variable = max(industry_std.items(), key=lambda x: x[1])
                insights.append(f"- **{most_variable[0]}** 表现波动较大（标准差: {most_variable[1]:.2f}），建议多测试不同内容角度")
        
        # 生成完整报告
        report = f"""# 🧠 自学习优化报告

> 生成时间: {datetime.now().strftime("%Y年%m月%d日 %H:%M")}
> 反馈样本数: {len(self.feedback_data)}
> 系统版本: v2.0

---

{chr(10).join(insights)}

---

## 📊 数据摘要

- 总反馈数: {len(self.feedback_data)}
- 覆盖行业: {len(self.learning_data['industry_performance'])}
- 覆盖平台: {len(self.learning_data['platform_performance'])}
- 内容角度: {len(self.learning_data['angle_performance'])}
- 热点追踪: {len(self.learning_data['hot_topic_performance'])}

---

*报告由自学习系统自动生成*
"""
        
        # 保存报告
        with open(self.insights_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return report
    
    def get_optimization_rules(self) -> List[Dict]:
        """获取优化规则"""
        rules = []
        
        # 基于数据生成优化规则
        if self.learning_data['industry_performance']:
            best_industry = max(
                self.learning_data['industry_performance'].items(),
                key=lambda x: x[1]['avg_score']
            )
            rules.append({
                "type": "industry_priority",
                "rule": f"优先推荐 '{best_industry[0]}' 行业内容",
                "confidence": min(best_industry[1]['count'] / 10, 1.0),
                "expected_improvement": f"+{best_industry[1]['avg_score']:.1f}% 互动率"
            })
        
        if self.learning_data['platform_performance']:
            best_platform = max(
                self.learning_data['platform_performance'].items(),
                key=lambda x: x[1]['avg_score']
            )
            rules.append({
                "type": "platform_priority",
                "rule": f"优先选择 '{best_platform[0]}' 平台",
                "confidence": min(best_platform[1]['count'] / 10, 1.0),
                "expected_improvement": f"+{best_platform[1]['avg_score']:.1f}% 互动率"
            })
        
        if self.learning_data['angle_performance']:
            best_angle = max(
                self.learning_data['angle_performance'].items(),
                key=lambda x: x[1]['avg_score']
            )
            rules.append({
                "type": "angle_priority",
                "rule": f"多使用 '{best_angle[0]}' 内容角度",
                "confidence": min(best_angle[1]['count'] / 10, 1.0),
                "expected_improvement": f"+{best_angle[1]['avg_score']:.1f}% 互动率"
            })
        
        return rules
    
    def show_dashboard(self):
        """显示数据仪表盘"""
        print("\n" + "=" * 60)
        print("🧠 自学习系统仪表盘")
        print("=" * 60)
        
        print(f"\n📊 数据概览:")
        print(f"  总反馈数: {len(self.feedback_data)}")
        print(f"  覆盖行业: {len(self.learning_data['industry_performance'])}")
        print(f"  覆盖平台: {len(self.learning_data['platform_performance'])}")
        print(f"  内容角度: {len(self.learning_data['angle_performance'])}")
        
        if self.feedback_data:
            # 最近7天反馈
            week_ago = datetime.now() - timedelta(days=7)
            recent_feedback = [
                f for f in self.feedback_data 
                if datetime.fromisoformat(f['timestamp']) > week_ago
            ]
            print(f"  近7天反馈: {len(recent_feedback)}")
            
            # 平均互动分
            avg_score = sum(f['engagement_score'] for f in self.feedback_data) / len(self.feedback_data)
            print(f"  平均互动分: {avg_score:.2f}")
        
        # TOP表现
        if self.learning_data['industry_performance']:
            print(f"\n🏆 TOP3 行业:")
            top_industries = sorted(
                self.learning_data['industry_performance'].items(),
                key=lambda x: x[1]['avg_score'],
                reverse=True
            )[:3]
            
            for i, (industry, data) in enumerate(top_industries, 1):
                print(f"  {i}. {industry}: {data['avg_score']:.2f}分 ({data['count']}条)")
        
        print("\n" + "=" * 60)

def demo_feedback():
    """演示添加反馈"""
    learning = SelfLearningSystem()
    
    # 模拟添加一些反馈数据
    demo_data = [
        ("3C数码", "抖音", "产品测评", "华为千元新机", {"likes": 15000, "comments": 800, "shares": 300, "views": 200000}),
        ("快消", "小红书", "使用教程", "春季护肤攻略", {"likes": 8000, "comments": 1200, "shares": 500, "views": 150000}),
        ("保健品", "抖音", "科普知识", "春季养生食谱", {"likes": 12000, "comments": 600, "shares": 400, "views": 180000}),
        ("家庭清洁", "抖音", "效果展示", "春日穿搭OOTD", {"likes": 10000, "comments": 500, "shares": 200, "views": 120000}),
        ("3C数码", "小红书", "选购指南", "春季数码好物", {"likes": 6000, "comments": 400, "shares": 150, "views": 100000}),
    ]
    
    print("📝 添加演示反馈数据...\n")
    for industry, platform, angle, hot_topic, metrics in demo_data:
        content_id = f"demo_{datetime.now().strftime('%Y%m%d%H%M%S')}_{industry}"
        learning.add_feedback(content_id, industry, platform, angle, hot_topic, metrics)
    
    print("\n✅ 演示数据添加完成！")
    
    # 显示仪表盘
    learning.show_dashboard()
    
    # 生成洞察报告
    print("\n📊 生成优化洞察报告...")
    report = learning.generate_insights()
    print(f"\n报告已保存至: {learning.insights_file}")
    
    # 显示优化规则
    print("\n🎯 优化规则:")
    rules = learning.get_optimization_rules()
    for i, rule in enumerate(rules, 1):
        print(f"{i}. {rule['rule']}")
        print(f"   置信度: {rule['confidence']*100:.0f}% | 预期提升: {rule['expected_improvement']}")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='效果反馈与自学习系统')
    parser.add_argument('--demo', action='store_true', help='运行演示模式')
    parser.add_argument('--dashboard', action='store_true', help='显示仪表盘')
    parser.add_argument('--report', action='store_true', help='生成洞察报告')
    parser.add_argument('--add-feedback', type=str, help='添加反馈 (JSON格式)')
    
    args = parser.parse_args()
    
    if args.demo:
        demo_feedback()
    elif args.dashboard:
        learning = SelfLearningSystem()
        learning.show_dashboard()
    elif args.report:
        learning = SelfLearningSystem()
        report = learning.generate_insights()
        print(report)
    elif args.add_feedback:
        # 解析JSON并添加反馈
        try:
            feedback = json.loads(args.add_feedback)
            learning = SelfLearningSystem()
            learning.add_feedback(
                feedback['content_id'],
                feedback['industry'],
                feedback['platform'],
                feedback['angle'],
                feedback['hot_topic'],
                feedback['metrics']
            )
        except Exception as e:
            print(f"❌ 添加反馈失败: {e}")
    else:
        parser.print_help()
        print("\n\n💡 快速开始：")
        print("  1. 运行演示: python3 self_learning.py --demo")
        print("  2. 查看仪表盘: python3 self_learning.py --dashboard")
        print("  3. 生成报告: python3 self_learning.py --report")

if __name__ == "__main__":
    main()
