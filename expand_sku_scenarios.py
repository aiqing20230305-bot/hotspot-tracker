#!/usr/bin/env python3
"""
SKU场景扩展脚本
目标：从285条扩展到8200+条
方法：为每个客户SKU生成多种场景变体
"""

import json
import random
from datetime import datetime
from itertools import product as iter_product

# 4个核心场景模板
SCENARIO_TEMPLATES = {
    "开箱测评": {
        "description": "产品开箱体验与第一印象分享",
        "content_angles": [
            "惊喜开箱型", "专业评测型", "情感共鸣型", "对比展示型",
            "细节解读型", "价值分析型", "使用期待型", "包装设计型"
        ]
    },
    "产品讲解": {
        "description": "深入介绍产品功能与卖点",
        "content_angles": [
            "功能演示型", "卖点提炼型", "场景应用型", "痛点解决型",
            "技术解析型", "用户故事型", "专家背书型", "创新亮点型"
        ]
    },
    "使用教程": {
        "description": "手把手教用户如何使用产品",
        "content_angles": [
            "新手入门型", "进阶技巧型", "常见问题型", "隐藏功能型",
            "效率提升型", "最佳实践型", "避坑指南型", "专业级用法型"
        ]
    },
    "产品对比": {
        "description": "与竞品或前代产品对比分析",
        "content_angles": [
            "同价位对比型", "功能对比型", "性价比分析型", "优劣势解析型",
            "升级必要性型", "品牌差异型", "用户画像对比型", "长期使用对比型"
        ]
    }
}

# 场景细分维度（用于生成更多变体）
SCENARIO_DIMENSIONS = {
    "风格": ["专业严谨", "轻松幽默", "情感走心", "数据驱动", "故事叙述", "视觉冲击", "互动参与"],
    "人群": ["学生党", "上班族", "家庭用户", "专业人士", "科技发烧友", "精致生活族", "性价比追求者"],
    "场景": ["居家日常", "办公场景", "户外出行", "社交聚会", "休闲娱乐", "学习工作", "特殊节日"],
    "卖点": ["性价比", "颜值设计", "功能创新", "品质保障", "品牌口碑", "用户口碑", "服务体验"]
}

# 关键词库（用于丰富场景）
KEYWORD_POOL = [
    ["热点", "趋势", "话题", "爆款"],
    ["情感", "故事", "共鸣", "温度"],
    ["痛点", "需求", "解决", "改善"],
    ["场景", "体验", "沉浸", "代入"],
    ["专家", "权威", "专业", "深度"],
    ["对比", "选择", "决策", "参考"],
    ["优惠", "福利", "性价比", "价值"],
    ["联名", "跨界", "创新", "突破"],
    ["细节", "品质", "匠心", "精致"],
    ["效率", "便捷", "智能", "省心"]
]

def generate_variety_keywords():
    """生成多样化的关键词组合"""
    keywords = []
    # 从每个关键词组中随机选择1-2个
    for group in KEYWORD_POOL:
        selected = random.sample(group, min(2, len(group)))
        keywords.extend(selected)
    # 随机选择3个
    return random.sample(keywords, 3)

def generate_scenarios():
    """生成所有SKU场景"""
    # 读取客户数据
    with open('/Users/zhangjingwei/.qclaw/workspace/hotspot-tracker/client_ideas.json', 'r', encoding='utf-8') as f:
        client_data = json.load(f)
    
    # 提取所有唯一的 client+product 组合及其行业信息
    client_products = {}
    for item in client_data:
        client_info = item.get('client', {})
        client = client_info.get('brand', '')
        industry = client_info.get('industry', '其他')
        product = item.get('product', '')
        if client and product:
            key = (client, product)
            if key not in client_products:
                client_products[key] = {
                    'client': client,
                    'product': product,
                    'industry': industry
                }
    
    print(f"发现 {len(client_products)} 个唯一客户+产品组合")
    
    # 计算每个SKU需要生成的场景数，确保覆盖所有SKU
    # 目标8200条，120个SKU组合，每个需要约68条场景
    # 4个场景类型 x 8个角度 x 7种风格 x 7个人群 = 1568种组合
    # 我们需要从中选择合适的组合，确保每个SKU至少68条
    
    all_scenarios = []
    scenario_id = 1
    
    # 先遍历所有SKU，确保每个都有基础覆盖
    for (client, product), info in client_products.items():
        industry = info['industry']
        
        # 为每个核心场景模板生成变体
        for scenario_type, template in SCENARIO_TEMPLATES.items():
            base_description = template['description']
            
            # 为每个内容角度生成变体
            for angle in template['content_angles']:
                # 风格和人群的笛卡尔积
                styles = SCENARIO_DIMENSIONS['风格']
                audiences = SCENARIO_DIMENSIONS['人群']
                
                # 使用zip确保覆盖所有风格和人群的组合
                for i, (style, audience) in enumerate(zip(styles, audiences)):
                    scenario = {
                        "id": scenario_id,
                        "client": client,
                        "product": product,
                        "industry": industry,
                        "scenario_type": scenario_type,
                        "description": f"{base_description}，{style}风格，面向{audience}",
                        "content_angle": angle,
                        "style": style,
                        "target_audience": audience,
                        "keywords": generate_variety_keywords()
                    }
                    all_scenarios.append(scenario)
                    scenario_id += 1
    
    print(f"基础生成完成: {len(all_scenarios)} 条场景")
    
    # 如果还没达到目标，继续添加更多变体
    if len(all_scenarios) < 8200:
        # 第二轮：添加更多场景+卖点组合
        for (client, product), info in client_products.items():
            industry = info['industry']
            
            for scenario_type, template in SCENARIO_TEMPLATES.items():
                base_description = template['description']
                
                for angle in template['content_angles']:
                    for scene in SCENARIO_DIMENSIONS['场景']:
                        for selling_point in SCENARIO_DIMENSIONS['卖点']:
                            if len(all_scenarios) >= 8200:
                                break
                            
                            scenario = {
                                "id": scenario_id,
                                "client": client,
                                "product": product,
                                "industry": industry,
                                "scenario_type": scenario_type,
                                "description": f"{base_description}，{scene}场景，突出{selling_point}",
                                "content_angle": angle,
                                "style": random.choice(SCENARIO_DIMENSIONS['风格']),
                                "target_audience": random.choice(SCENARIO_DIMENSIONS['人群']),
                                "usage_scene": scene,
                                "selling_point": selling_point,
                                "keywords": generate_variety_keywords()
                            }
                            all_scenarios.append(scenario)
                            scenario_id += 1
                        if len(all_scenarios) >= 8200:
                            break
                    if len(all_scenarios) >= 8200:
                        break
                if len(all_scenarios) >= 8200:
                    break
            if len(all_scenarios) >= 8200:
                break
    
    print(f"生成场景总数: {len(all_scenarios)}")
    return all_scenarios

def main():
    print("开始扩展SKU场景数据...")
    start_time = datetime.now()
    
    scenarios = generate_scenarios()
    
    # 构建输出数据结构
    output = {
        "generated_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "total_count": len(scenarios),
        "expansion_info": {
            "original_count": 285,
            "target_count": 8200,
            "actual_count": len(scenarios),
            "templates_used": list(SCENARIO_TEMPLATES.keys())
        },
        "scenarios": scenarios
    }
    
    # 保存到文件
    output_path = '/Users/zhangjingwei/.qclaw/workspace/hotspot-tracker/sku_scenarios.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print(f"\n=== 扩展完成 ===")
    print(f"原始数量: 285")
    print(f"目标数量: 8200")
    print(f"实际生成: {len(scenarios)}")
    print(f"耗时: {duration:.2f} 秒")
    print(f"保存路径: {output_path}")
    
    # 统计信息
    clients = set(s['client'] for s in scenarios)
    products = set(s['product'] for s in scenarios)
    types = {}
    for s in scenarios:
        t = s['scenario_type']
        types[t] = types.get(t, 0) + 1
    
    print(f"\n=== 统计信息 ===")
    print(f"客户数: {len(clients)}")
    print(f"产品数: {len(products)}")
    print(f"场景类型分布:")
    for t, count in types.items():
        print(f"  - {t}: {count}")

if __name__ == '__main__':
    main()
