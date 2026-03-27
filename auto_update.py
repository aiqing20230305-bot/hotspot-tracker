#!/usr/bin/env python3
"""
特赞内容运营平台 - 自动更新脚本
每天自动抓取热点数据，生成客户选题
"""

import json
import requests
from datetime import datetime
from urllib.parse import quote
import random

# 客户配置 - 12个客户
CLIENTS = [
    {"industry": "3C数码", "brand": "荣耀", "products": ["荣耀手机", "荣耀平板", "荣耀耳机"], "priority": 5},
    {"industry": "3C数码", "brand": "罗技", "products": ["罗技键鼠", "罗技摄像头"], "priority": 4},
    {"industry": "快消", "brand": "AHC", "products": ["AHC水乳", "AHC防晒"], "priority": 5},
    {"industry": "快消", "brand": "多芬", "products": ["多芬沐浴露", "多芬洗发水"], "priority": 4},
    {"industry": "快消", "brand": "力士", "products": ["力士洗发水", "力士沐浴露"], "priority": 4},
    {"industry": "快消", "brand": "清扬", "products": ["清扬洗发水"], "priority": 3},
    {"industry": "快消", "brand": "舒适", "products": ["舒适洗衣液"], "priority": 3},
    {"industry": "保健品", "brand": "汤臣倍健", "products": ["蛋白粉", "维生素", "鱼油"], "priority": 5},
    {"industry": "家庭清洁", "brand": "HC", "products": ["HC清洁剂"], "priority": 3},
    {"industry": "宠物食品", "brand": "希宝", "products": ["猫粮", "狗粮"], "priority": 4},
    {"industry": "食品饮料", "brand": "OATLY", "products": ["燕麦奶", "咖啡"], "priority": 4},
    {"industry": "食品饮料", "brand": "百威", "products": ["啤酒"], "priority": 3},
]

# 平台配置
PLATFORMS = ["抖音", "微博", "小红书", "B站"]

# 内容角度
ANGLES = ["产品测评", "使用教程", "热点借势", "痛点解决", "场景展示", "对比评测", "开箱体验", "种草推荐"]

# 热点数据 - 模拟实时数据（实际应从API获取）
def get_hot_topics():
    """获取热点数据"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 模拟热点数据 - 实际应调用抖音/微博/小红书API
    hot_topics = [
        {"title": "春季护肤攻略", "platform": "小红书", "heat": f"{random.randint(1,5)}亿浏览", "trend": "🔥🔥🔥 爆发式增长"},
        {"title": "AI黑科技测评", "platform": "抖音", "heat": f"{random.randint(800,1500)}万", "trend": "🔥🔥🔥 持续上升"},
        {"title": "健身打卡挑战", "platform": "抖音", "heat": f"{random.randint(500,1000)}万", "trend": "🔥🔥 稳定上升"},
        {"title": "露营装备推荐", "platform": "小红书", "heat": f"{random.randint(1,3)}亿浏览", "trend": "🔥🔥🔥 爆发式增长"},
        {"title": "315消费者权益", "platform": "微博", "heat": f"{random.randint(600,900)}万", "trend": "🔥🔥 热议中"},
        {"title": "春日穿搭OOTD", "platform": "小红书", "heat": f"{random.randint(2,4)}亿浏览", "trend": "🔥🔥🔥 持续上升"},
        {"title": "职场效率神器", "platform": "微博", "heat": f"{random.randint(400,700)}万", "trend": "🔥🔥 稳定上升"},
        {"title": "健康饮食计划", "platform": "抖音", "heat": f"{random.randint(300,600)}万", "trend": "🔥🔥 热议中"},
        {"title": "宠物日常vlog", "platform": "小红书", "heat": f"{random.randint(1,2)}亿浏览", "trend": "🔥🔥 持续上升"},
        {"title": "科技新品开箱", "platform": "B站", "heat": f"{random.randint(200,500)}万", "trend": "🔥🔥 热议中"},
    ]
    return hot_topics

def generate_client_ideas(client, hot_topics):
    """为单个客户生成选题"""
    ideas = []
    today = datetime.now().strftime("%Y%m%d")
    
    # 每个客户生成10-15个选题
    num_ideas = random.randint(10, 15)
    
    for i in range(num_ideas):
        hot_topic = random.choice(hot_topics)
        angle = random.choice(ANGLES)
        platform = random.choice(PLATFORMS)
        product = random.choice(client["products"])
        
        # 生成标题
        title_templates = [
            f"《{hot_topic['title']}？{product}真实测评》",
            f"《{hot_topic['title']}！{client['brand']}产品使用心得》",
            f"《借势{hot_topic['title']}，{product}这样用超赞》",
            f"《{hot_topic['title']}火了，{client['brand']}也有话说》",
            f"《从{hot_topic['title']}看{product}的正确打开方式》",
        ]
        
        idea = {
            "id": f"{client['industry']}_{today}{random.randint(1000,9999)}",
            "client": {
                "industry": client["industry"],
                "brand": client["brand"],
                "products": client["products"],
                "priority": client["priority"]
            },
            "title": random.choice(title_templates),
            "platform": platform,
            "angle": angle,
            "hot_topic": hot_topic["title"],
            "heat": hot_topic["heat"],
            "trend": hot_topic["trend"],
            "product": product,
            "engagement_estimate": f"{random.randint(5000,50000)}+",
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        ideas.append(idea)
    
    return ideas

def generate_sku_scenarios(client):
    """生成SKU场景数据"""
    scenarios = []
    
    scenario_templates = [
        {
            "name": "痛点场景",
            "description": f"用户使用{client['brand']}产品解决的问题",
            "pain_points": ["时间紧张", "效果不佳", "价格敏感", "选择困难"],
            "content_angle": "问题解决型"
        },
        {
            "name": "情感场景",
            "description": f"{client['brand']}产品带来的情感价值",
            "emotions": ["自信", "舒适", "安心", "品质生活"],
            "content_angle": "情感共鸣型"
        },
        {
            "name": "使用场景",
            "description": f"{client['brand']}产品的具体使用场景",
            "scenes": ["居家", "办公", "户外", "社交"],
            "content_angle": "场景代入型"
        }
    ]
    
    for product in client["products"]:
        for template in scenario_templates:
            scenario = {
                "client": client["brand"],
                "product": product,
                "scenario_type": template["name"],
                "description": template["description"],
                "content_angle": template["content_angle"],
                "keywords": random.sample(["痛点", "情感", "场景", "对比", "热点"], 3)
            }
            scenarios.append(scenario)
    
    return scenarios

def update_all_data():
    """更新所有数据"""
    print(f"🔄 开始更新数据 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 获取热点
    hot_topics = get_hot_topics()
    print(f"✅ 获取 {len(hot_topics)} 条热点数据")
    
    # 生成客户选题
    all_ideas = []
    for client in CLIENTS:
        ideas = generate_client_ideas(client, hot_topics)
        all_ideas.extend(ideas)
    print(f"✅ 生成 {len(all_ideas)} 条客户选题")
    
    # 生成SKU场景
    all_scenarios = []
    for client in CLIENTS:
        scenarios = generate_sku_scenarios(client)
        all_scenarios.extend(scenarios)
    print(f"✅ 生成 {len(all_scenarios)} 条SKU场景")
    
    # 保存数据
    with open("client_ideas.json", "w", encoding="utf-8") as f:
        json.dump(all_ideas, f, ensure_ascii=False, indent=2)
    
    with open("sku_scenarios.json", "w", encoding="utf-8") as f:
        json.dump(all_scenarios, f, ensure_ascii=False, indent=2)
    
    with open("hot_topics.json", "w", encoding="utf-8") as f:
        json.dump(hot_topics, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 数据更新完成！")
    return all_ideas, all_scenarios, hot_topics

if __name__ == "__main__":
    update_all_data()
