#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能选题生成系统 V2 - Phase 5核心功能
基于热点+客户画像+质量评分的智能选题生成

Author: Agent-5 (AI工程师)
Date: 2026-04-02
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Tuple
import hashlib
import sys

# 导入质量评分系统
sys.path.insert(0, '.')
from quality_scorer import QualityScorer


class IntelligentIdeaGenerator:
    """智能选题生成器"""
    
    def __init__(self, config: Dict = None):
        """初始化生成器
        
        Args:
            config: 生成配置
        """
        self.config = config or {
            'ideas_per_client': 8,        # 每个客户生成选题数
            'min_hot_value': 100000000,   # 最低热度阈值
            'max_total_ideas': 2000,      # 最大选题总数
            'quality_threshold': 0.5,     # 质量分阈值
            'dedup_enabled': True         # 是否去重
        }
        
        self.scorer = QualityScorer()
        
        # 角度模板 - 更丰富
        self.angle_templates = {
            '科技热点': [
                ('创意借势', '从创意角度解读{product}如何借势{hotspot}'),
                ('趋势分析', '深度分析{hotspot}对{industry}的影响及{product}的机遇'),
                ('科技科普', '用{product}解读{hotspot}背后的科技原理'),
                ('产品评测', '{product}实测：{hotspot}场景下的表现'),
                ('对比测评', '{product} vs 竞品：{hotspot}视角下的优劣势'),
            ],
            '消费热点': [
                ('生活方式', '{hotspot}潮流下，{product}如何提升生活品质'),
                ('场景种草', '{hotspot}必备好物：{product}的N种用法'),
                ('情感共鸣', '{hotspot}引发的思考：{product}陪伴的日常'),
                ('用户故事', '真实用户分享：{product}与{hotspot}的故事'),
                ('避坑指南', '{hotspot}期间，{product}选购避坑指南'),
            ],
            '社会热点': [
                ('情感共鸣', '{hotspot}：{product}如何传递温度'),
                ('趋势分析', '{hotspot}背后的社会趋势，{product}如何响应'),
                ('价值观营销', '{hotspot}启示：{product}的品牌态度'),
                ('公益行动', '{hotspot}相关，{product}在行动'),
            ],
            '体育热点': [
                ('激情时刻', '{hotspot}激情时刻，{product}与你同在'),
                ('运动生活', '{hotspot}启示：{product}助力运动生活'),
                ('冠军精神', '{hotspot}背后的坚持，{product}致敬'),
            ],
            'default': [
                ('创意借势', '{product}借势{hotspot}的创意玩法'),
                ('趋势分析', '{hotspot}趋势下{product}的机会'),
                ('生活方式', '{product}与{hotspot}的生活场景'),
            ]
        }
        
        # 平台适配
        self.platform_mapping = {
            '美妆': ['小红书', '抖音', 'B站'],
            '护肤': ['小红书', '抖音', '微博'],
            '3C数码': ['B站', '抖音', '微博', '知乎'],
            '保健': ['小红书', '抖音', '公众号'],
            '清洁': ['小红书', '抖音'],
            '日用': ['小红书', '抖音'],
            '母婴': ['小红书', '抖音', '公众号'],
            '宠物': ['小红书', '抖音', 'B站'],
            '食品': ['小红书', '抖音', '微博'],
            '饮品': ['小红书', '抖音', '微博'],
        }
        
        # 客户画像扩展
        self.client_profiles = {
            '荣耀': {'tone': '科技感', 'target': '年轻科技爱好者', 'key卖点': ['创新', '性能', '性价比']},
            '罗技': {'tone': '专业', 'target': '办公/游戏人群', 'key卖点': ['精准', '舒适', '专业']},
            '小米': {'tone': '亲民', 'target': '大众消费者', 'key卖点': ['性价比', '智能生态', '品质']},
            '索尼': {'tone': '高端', 'target': '影音发烧友', 'key卖点': ['画质', '音质', '黑科技']},
            'AHC': {'tone': '专业护肤', 'target': '年轻女性', 'key卖点': ['补水', '修护', '玻尿酸']},
            '多芬': {'tone': '温和', 'target': '家庭用户', 'key卖点': ['滋润', '温和', '真实美']},
            '力士': {'tone': '时尚', 'target': '年轻女性', 'key卖点': ['香氛', '丝滑', '自信']},
            '清扬': {'tone': '专业', 'target': '男士/家庭', 'key卖点': ['去屑', '控油', '专业']},
            '玉兰油': {'tone': '高端护肤', 'target': '成熟女性', 'key卖点': ['抗老', '美白', '科技护肤']},
            '汤臣倍健': {'tone': '专业健康', 'target': '家庭/中老年', 'key卖点': ['科学配方', '品质', '健康']},
            '善存': {'tone': '专业', 'target': '全家', 'key卖点': ['全面营养', '科学', '国际品牌']},
            'HC': {'tone': '轻奢护肤', 'target': '都市女性', 'key卖点': ['高效', '科技', '品质']},
            '威猛先生': {'tone': '专业清洁', 'target': '家庭主妇', 'key卖点': ['强力去污', '专业', '安全']},
            '舒适': {'tone': '亲肤', 'target': '家庭', 'key卖点': ['柔软', '亲肤', '品质']},
            '希宝': {'tone': '温馨', 'target': '宝妈', 'key卖点': ['营养', '安全', '成长']},
            '皇家': {'tone': '专业宠物', 'target': '宠物主人', 'key卖点': ['营养均衡', '专业', '品质']},
            'OATLY': {'tone': '潮流健康', 'target': '年轻白领', 'key卖点': ['植物基', '环保', '健康']},
            '百威': {'tone': '激情', 'target': '年轻人群', 'key卖点': ['畅爽', '聚会', '品质']},
            '元气森林': {'tone': '年轻活力', 'target': 'Z世代', 'key卖点': ['0糖', '健康', '好喝']},
            '农夫山泉': {'tone': '自然', 'target': '大众', 'key卖点': ['天然', '健康', '品质']},
        }
    
    def load_data(self) -> Tuple[List[Dict], List[Dict]]:
        """加载热点和选题数据"""
        with open('hot_topics.json', 'r', encoding='utf-8') as f:
            hot_topics = json.load(f)
        
        with open('client_ideas.json', 'r', encoding='utf-8') as f:
            client_ideas = json.load(f)
        
        return hot_topics, client_ideas
    
    def generate_idea_id(self, client_brand: str, hot_topic_id: str, product: str) -> str:
        """生成唯一选题ID"""
        base = f"{client_brand}_{hot_topic_id}_{product}_{datetime.now().isoformat()}"
        hash_suffix = hashlib.md5(base.encode()).hexdigest()[:8]
        return f"{client_brand}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{hash_suffix}"
    
    def get_angle_templates(self, topic_type: str) -> List[Tuple[str, str]]:
        """根据热点类型获取角度模板"""
        # 类型映射
        type_mapping = {
            '科技热点': '科技热点',
            '消费趋势': '消费热点',
            '消费热点': '消费热点',
            '社会热点': '社会热点',
            '体育热点': '体育热点',
        }
        
        mapped_type = type_mapping.get(topic_type, 'default')
        return self.angle_templates.get(mapped_type, self.angle_templates['default'])
    
    def select_best_platform(self, industry: str, angle: str) -> str:
        """选择最佳平台"""
        platforms = self.platform_mapping.get(industry, ['小红书', '抖音'])
        
        # 根据角度调整
        if angle in ['科技科普', '产品评测', '对比测评']:
            if 'B站' in platforms:
                return 'B站'
        elif angle in ['生活方式', '场景种草']:
            if '小红书' in platforms:
                return '小红书'
        
        return platforms[0]
    
    def calculate_engagement_estimate(self, hot_value: int, quality_score: float, client_brand: str) -> str:
        """估算互动量"""
        # 基础互动量（根据热度）
        base = hot_value / 10000  # 热度转互动
        
        # 质量系数
        quality_factor = 0.5 + quality_score
        
        # 品牌系数
        brand_factors = {
            '小米': 1.2, '荣耀': 1.1, '索尼': 1.0,
            '元气森林': 1.3, '农夫山泉': 1.1,
            '多芬': 1.0, '玉兰油': 1.1,
        }
        brand_factor = brand_factors.get(client_brand, 1.0)
        
        estimated = int(base * quality_factor * brand_factor)
        return f"{min(estimated, 100000)}+"
    
    def check_duplicate(self, new_idea: Dict, existing_ideas: List[Dict]) -> bool:
        """检查是否与现有选题重复"""
        new_title = new_idea['title']
        new_hotspot = new_idea.get('hot_topic', '')
        new_product = new_idea.get('product', '')
        new_client = new_idea.get('client', {})
        if isinstance(new_client, dict):
            new_client = new_client.get('brand', '')
        
        for existing in existing_ideas:
            # 检查标题相似度
            if new_title == existing.get('title'):
                return True
            
            # 检查同一客户+同一热点+同一产品
            existing_client = existing.get('client', {})
            if isinstance(existing_client, dict):
                existing_client = existing_client.get('brand', '')
            
            if (new_client == existing_client and 
                new_hotspot == existing.get('hot_topic') and 
                new_product == existing.get('product')):
                return True
        
        return False
    
    def generate_ideas_for_client(self, client: Dict, hot_topics: List[Dict], 
                                   existing_ideas: List[Dict]) -> List[Dict]:
        """为单个客户生成选题"""
        new_ideas = []
        brand = client['brand']
        industry = client['industry']
        products = client['products']
        
        # 获取客户画像
        profile = self.client_profiles.get(brand, {})
        
        # 筛选高相关度热点
        relevant_topics = []
        for topic in hot_topics:
            # 检查客户关联
            c_clients = topic.get('c', [])
            if brand in c_clients:
                relevant_topics.append((topic, 1.0))  # 高相关
            elif topic.get('hot_value', 0) >= self.config['min_hot_value']:
                relevant_topics.append((topic, 0.7))  # 高热度
        
        # 按相关度和热度排序
        relevant_topics.sort(key=lambda x: (x[1], x[0].get('hot_value', 0)), reverse=True)
        
        # 为每个相关热点生成选题
        ideas_generated = 0
        for topic, relevance in relevant_topics:
            if ideas_generated >= self.config['ideas_per_client']:
                break
            
            # 获取角度模板
            templates = self.get_angle_templates(topic.get('type', ''))
            
            for angle, template in templates[:2]:  # 每个热点最多2个角度
                if ideas_generated >= self.config['ideas_per_client']:
                    break
                
                # 选择产品
                product = products[ideas_generated % len(products)]
                
                # 生成标题
                title = template.format(
                    product=product,
                    hotspot=topic['title'][:20],
                    industry=industry
                )
                title = f"《{title}》"
                
                # 选择平台
                platform = self.select_best_platform(industry, angle)
                
                # 计算质量分
                quality_result = self.scorer.calculate_topic_score(topic, {
                    'client_industries': [industry]
                })
                quality_score = quality_result['total_score']
                
                # 质量分过滤
                if quality_score < self.config['quality_threshold']:
                    continue
                
                # 构建选题对象
                idea = {
                    'id': self.generate_idea_id(brand, topic.get('id', ''), product),
                    'client': client,
                    'title': title,
                    'platform': platform,
                    'angle': angle,
                    'hot_topic': topic['title'],
                    'hot_topic_id': topic.get('id', ''),
                    'heat': self._format_heat(topic.get('hot_value', 0)),
                    'trend': self._format_trend(topic.get('trends', [])),
                    'product': product,
                    'keywords': topic.get('keywords', [])[:5],
                    'quality_score': round(quality_score, 3),
                    'quality_level': quality_result['quality_level'],
                    'engagement_estimate': self.calculate_engagement_estimate(
                        topic.get('hot_value', 0), quality_score, brand
                    ),
                    'status': 'pending',
                    'created_at': datetime.now().isoformat(),
                    'profile_tags': {
                        'tone': profile.get('tone', ''),
                        'target': profile.get('target', ''),
                        'selling_points': profile.get('key卖点', [])
                    }
                }
                
                # 去重检查
                if self.config['dedup_enabled'] and self.check_duplicate(idea, existing_ideas + new_ideas):
                    continue
                
                new_ideas.append(idea)
                ideas_generated += 1
        
        return new_ideas
    
    def _format_heat(self, hot_value: int) -> str:
        """格式化热度标签"""
        if hot_value >= 400000000:
            return '热搜第一'
        elif hot_value >= 300000000:
            return '热搜前三'
        elif hot_value >= 200000000:
            return '热搜前十'
        elif hot_value >= 100000000:
            return '高热'
        else:
            return '温热'
    
    def _format_trend(self, trends: List[str]) -> str:
        """格式化趋势标签"""
        if not trends:
            return '🔥 稳定'
        
        trend = trends[0]
        trend_map = {
            '爆': '🔥🔥🔥 爆发式增长',
            '热': '🔥🔥 快速上升',
            '新': '🔥 新晋热点',
        }
        return trend_map.get(trend, '🔥 稳步上升')
    
    def run(self) -> Dict:
        """执行智能选题生成"""
        print("=" * 60)
        print("智能选题生成系统 V2 - Phase 5")
        print("=" * 60)
        
        # 加载数据
        hot_topics, existing_ideas = self.load_data()
        print(f"\n加载完成:")
        print(f"  热点数: {len(hot_topics)}")
        print(f"  现有选题数: {len(existing_ideas)}")
        
        # 客户列表
        clients = [
            {"brand": "荣耀", "industry": "3C数码", "products": ["荣耀手机", "荣耀平板", "荣耀手表", "荣耀折叠屏", "荣耀笔记本", "荣耀耳机", "荣耀智慧屏"]},
            {"brand": "罗技", "industry": "3C数码", "products": ["罗技鼠标", "罗技键盘", "罗技耳机", "罗技摄像头", "罗技游戏手柄", "罗技音箱", "罗技会议设备"]},
            {"brand": "小米", "industry": "3C数码", "products": ["小米手机", "小米平板", "小米手环", "小米智能家居", "小米电视", "小米路由器", "小米充电器", "小米耳机"]},
            {"brand": "索尼", "industry": "3C数码", "products": ["索尼相机", "索尼耳机", "索尼游戏机", "索尼电视", "索尼手机", "索尼音箱", "索尼播放器"]},
            {"brand": "AHC", "industry": "美妆", "products": ["AHC面膜", "AHC精华", "AHC眼霜", "AHC防晒霜", "AHC水乳", "AHC面霜", "AHC卸妆水"]},
            {"brand": "多芬", "industry": "护肤", "products": ["多芬洗面奶", "多芬护肤霜", "多芬沐浴露", "多芬身体乳", "多芬洗发水", "多芬护发素", "多芬香皂"]},
            {"brand": "力士", "industry": "护肤", "products": ["力士香皂", "力士沐浴露", "力士洗发水", "力士护发素", "力士身体乳", "力士香氛"]},
            {"brand": "清扬", "industry": "护肤", "products": ["清扬洗发水", "清扬护发素", "清扬头皮护理", "清扬去屑洗发水", "清扬控油洗发水"]},
            {"brand": "玉兰油", "industry": "美妆", "products": ["玉兰油面霜", "玉兰油精油", "玉兰油眼霜", "玉兰油精华", "玉兰油防晒", "玉兰油面膜"]},
            {"brand": "汤臣倍健", "industry": "保健", "products": ["汤臣倍健维生素", "汤臣倍健钙片", "汤臣倍健蛋白粉", "汤臣倍健鱼油", "汤臣倍健益生菌"]},
            {"brand": "善存", "industry": "保健", "products": ["善存维生素", "善存矿物质", "善存复合营养", "善存钙片", "善存锌片"]},
            {"brand": "HC", "industry": "护肤", "products": ["HC面膜", "HC精华液", "HC护肤套装", "HC眼霜", "HC面霜"]},
            {"brand": "威猛先生", "industry": "清洁", "products": ["威猛先生清洁剂", "威猛先生消毒液", "威猛先生洗涤剂", "威猛先生洁厕灵", "威猛先生厨房清洁"]},
            {"brand": "舒适", "industry": "日用", "products": ["舒适纸巾", "舒适卷纸", "舒适湿巾", "舒适抽纸", "舒适手帕纸"]},
            {"brand": "希宝", "industry": "母婴", "products": ["希宝奶粉", "希宝纸尿裤", "希宝婴儿护肤", "希宝辅食", "希宝湿巾"]},
            {"brand": "皇家", "industry": "宠物", "products": ["皇家狗粮", "皇家猫粮", "皇家宠物零食", "皇家宠物营养品"]},
            {"brand": "OATLY", "industry": "食品", "products": ["OATLY燕麦奶", "OATLY冰淇淋", "OATLY酸奶", "OATLY咖啡伴侣"]},
            {"brand": "百威", "industry": "饮品", "products": ["百威啤酒", "百威无醇啤酒", "百威精酿", "百威白啤"]},
            {"brand": "元气森林", "industry": "饮品", "products": ["元气森林气泡水", "元气森林茶饮", "元气森林果汁", "元气森林矿泉水"]},
            {"brand": "农夫山泉", "industry": "饮品", "products": ["农夫山泉矿泉水", "农夫山泉茶饮", "农夫山泉果汁", "农夫山泉功能饮料"]},
        ]
        
        # 为每个客户生成选题
        all_new_ideas = []
        stats = {'total': 0, 'by_client': {}, 'by_quality': {}}
        
        print(f"\n开始生成选题...")
        
        for client in clients:
            client_ideas = self.generate_ideas_for_client(
                client, hot_topics, existing_ideas + all_new_ideas
            )
            all_new_ideas.extend(client_ideas)
            
            stats['by_client'][client['brand']] = len(client_ideas)
            stats['total'] += len(client_ideas)
            
            if client_ideas:
                print(f"  {client['brand']}: {len(client_ideas)}条选题")
        
        # 质量分布统计
        for idea in all_new_ideas:
            level = idea.get('quality_level', '未评分')
            stats['by_quality'][level] = stats['by_quality'].get(level, 0) + 1
        
        # 合并到现有选题（新选题在前）
        final_ideas = all_new_ideas + existing_ideas
        final_ideas = final_ideas[:self.config['max_total_ideas']]
        
        # 保存
        with open('client_ideas.json', 'w', encoding='utf-8') as f:
            json.dump(final_ideas, f, ensure_ascii=False, indent=2)
        
        # 生成报告
        report = {
            'generated_at': datetime.now().isoformat(),
            'stats': stats,
            'sample_ideas': all_new_ideas[:10],
            'hot_topics_used': len(set(i['hot_topic_id'] for i in all_new_ideas))
        }
        
        # 打印摘要
        print(f"\n" + "=" * 60)
        print(f"选题生成完成!")
        print(f"=" * 60)
        print(f"新增选题: {stats['total']}条")
        print(f"选题总数: {len(final_ideas)}条")
        print(f"使用热点: {report['hot_topics_used']}个")
        print(f"\n质量分布:")
        for level, count in sorted(stats['by_quality'].items()):
            print(f"  {level}: {count}条")
        
        print(f"\n示例选题 (前5条):")
        for i, idea in enumerate(all_new_ideas[:5], 1):
            print(f"  {i}. [{idea['client']['brand']}] {idea['title'][:50]}...")
            print(f"     质量: {idea['quality_level']} ({idea['quality_score']})")
        
        return report


if __name__ == '__main__':
    generator = IntelligentIdeaGenerator({
        'ideas_per_client': 8,
        'min_hot_value': 100000000,
        'quality_threshold': 0.45,
        'dedup_enabled': True,
        'max_total_ideas': 2000
    })
    report = generator.run()
    
    # 保存报告
    with open('idea_generation_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n报告已保存: idea_generation_report.json")
