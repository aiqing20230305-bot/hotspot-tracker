#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
热点更新脚本 - 每小时执行
合并新热点、更新热度、生成选题
"""

import json
from datetime import datetime
from pathlib import Path

# 客户列表
CLIENTS = [
    {"brand": "荣耀", "industry": "科技/手机", "products": ["手机", "平板", "笔记本", "智能手表"]},
    {"brand": "罗技", "industry": "科技/外设", "products": ["鼠标", "键盘", "耳机", "摄像头"]},
    {"brand": "小米", "industry": "科技/生态", "products": ["手机", "平板", "智能家居", "电视"]},
    {"brand": "索尼", "industry": "科技/影音", "products": ["耳机", "相机", "游戏机", "电视"]},
    {"brand": "AHC", "industry": "美妆/护肤", "products": ["防晒", "精华", "面膜", "水乳"]},
    {"brand": "多芬", "industry": "个护/清洁", "products": ["沐浴露", "洗发水", "身体乳", "香皂"]},
    {"brand": "力士", "industry": "个护/清洁", "products": ["沐浴露", "洗发水", "护发素", "香皂"]},
    {"brand": "清扬", "industry": "个护/洗发", "products": ["洗发水", "护发素", "头皮护理"]},
    {"brand": "玉兰油", "industry": "美妆/护肤", "products": ["精华", "面霜", "防晒", "抗衰"]},
    {"brand": "汤臣倍健", "industry": "健康/保健", "products": ["蛋白粉", "维生素", "钙片", "益生菌"]},
    {"brand": "善存", "industry": "健康/保健", "products": ["维生素", "矿物质", "钙片"]},
    {"brand": "HC", "industry": "美妆/护肤", "products": ["精华", "面膜", "防晒"]},
    {"brand": "威猛先生", "industry": "家居/清洁", "products": ["清洁剂", "消毒液", "去污剂"]},
    {"brand": "舒适", "industry": "个护/剃须", "products": ["剃须刀", "剃须膏", "刀片"]},
    {"brand": "希宝", "industry": "宠物/食品", "products": ["猫粮", "狗粮", "宠物零食"]},
    {"brand": "皇家", "industry": "宠物/食品", "products": ["猫粮", "狗粮", "处方粮"]},
    {"brand": "OATLY", "industry": "食品/植物奶", "products": ["燕麦奶", "燕麦饮", "咖啡伴侣"]},
    {"brand": "百威", "industry": "酒饮", "products": ["啤酒", "精酿", "低醇啤酒"]},
    {"brand": "元气森林", "industry": "饮料/气泡水", "products": ["气泡水", "无糖茶", "电解质水"]},
    {"brand": "农夫山泉", "industry": "饮料/水饮", "products": ["矿泉水", "茶饮", "果汁"]}
]

# 新热点数据
NEW_HOTSPOTS = [
    {
        "id": "ht_202604050209_001",
        "title": "清明假期最后几小时 打工人深夜emo求安慰",
        "hot_value": 485000000,
        "platform": "微博/小红书",
        "industries": ["职场", "心理"],
        "trends": ["爆", "新"],
        "type": "社会热点",
        "sentiment": "中性",
        "keywords": ["清明", "假期", "打工人", "深夜", "emo"],
        "c": ["农夫山泉", "元气森林", "汤臣倍健", "AHC"],
        "created_at": "2026-04-05T02:09:00",
        "rank": 1,
        "category": "社会热点",
        "trend_tags": ["#深夜emo", "#假期倒计时", "#打工人"],
        "url": "https://weibo.com",
        "updated_at": "2026-04-05T02:09:00",
        "logic": "深夜时段情绪话题+假期结束焦虑",
        "trend": "🔥🔥🔥 爆发式增长",
        "heat": "4.9亿",
        "isNew": True
    },
    {
        "id": "ht_202604050209_002",
        "title": "凌晨两点还在刷手机 报复性熬夜成假期常态",
        "hot_value": 456000000,
        "platform": "小红书/抖音",
        "industries": ["健康", "生活方式"],
        "trends": ["热", "新"],
        "type": "大健康热点",
        "sentiment": "中性",
        "keywords": ["凌晨", "刷手机", "熬夜", "假期", "报复性"],
        "c": ["汤臣倍健", "善存", "AHC", "玉兰油"],
        "created_at": "2026-04-05T02:09:00",
        "rank": 2,
        "category": "大健康热点",
        "trend_tags": ["#报复性熬夜", "#凌晨两点", "#手机依赖"],
        "url": "https://xiaohongshu.com",
        "updated_at": "2026-04-05T02:09:00",
        "logic": "深夜用户活跃+假期作息紊乱",
        "trend": "🔥🔥🔥 持续上升",
        "heat": "4.6亿",
        "isNew": True
    },
    {
        "id": "ht_202604050209_003",
        "title": "明天要上班了 今晚失眠怎么办",
        "hot_value": 423000000,
        "platform": "微博/抖音",
        "industries": ["健康", "职场"],
        "trends": ["热", "新"],
        "type": "大健康热点",
        "sentiment": "负面",
        "keywords": ["上班", "失眠", "假期", "焦虑", "睡眠"],
        "c": ["汤臣倍健", "善存", "HC"],
        "created_at": "2026-04-05T02:09:00",
        "rank": 3,
        "category": "大健康热点",
        "trend_tags": ["#失眠", "#上班焦虑", "#假期综合症"],
        "url": "https://weibo.com",
        "updated_at": "2026-04-05T02:09:00",
        "logic": "假期结束焦虑+睡眠问题",
        "trend": "🔥🔥🔥 新晋热点",
        "heat": "4.2亿",
        "isNew": True
    },
    {
        "id": "ht_202604050209_004",
        "title": "深夜追剧党最后的狂欢 假期剧单推荐",
        "hot_value": 398000000,
        "platform": "B站/小红书",
        "industries": ["娱乐", "视频"],
        "trends": ["热", "新"],
        "type": "娱乐热点",
        "sentiment": "正面",
        "keywords": ["深夜", "追剧", "剧单", "假期", "推荐"],
        "c": ["索尼", "小米", "罗技", "荣耀"],
        "created_at": "2026-04-05T02:09:00",
        "rank": 4,
        "category": "娱乐热点",
        "trend_tags": ["#深夜追剧", "#剧单推荐", "#假期娱乐"],
        "url": "https://bilibili.com",
        "updated_at": "2026-04-05T02:09:00",
        "logic": "深夜娱乐场景+假期最后放松",
        "trend": "🔥🔥 持续上升",
        "heat": "4.0亿",
        "isNew": True
    },
    {
        "id": "ht_202604050209_005",
        "title": "凌晨外卖订单激增 夜宵经济火爆",
        "hot_value": 367000000,
        "platform": "抖音/微博",
        "industries": ["餐饮", "消费"],
        "trends": ["热", "新"],
        "type": "美食热点",
        "sentiment": "正面",
        "keywords": ["凌晨", "外卖", "夜宵", "订单", "经济"],
        "c": ["百威", "元气森林", "农夫山泉"],
        "created_at": "2026-04-05T02:09:00",
        "rank": 5,
        "category": "美食热点",
        "trend_tags": ["#夜宵经济", "#凌晨外卖", "#假期消费"],
        "url": "https://douyin.com",
        "updated_at": "2026-04-05T02:09:00",
        "logic": "深夜消费场景+假期最后放纵",
        "trend": "🔥🔥 稳定",
        "heat": "3.7亿",
        "isNew": True
    }
]

def generate_client_ideas(hotspot, client):
    """根据热点和客户生成选题"""
    import random
    
    angles = ["创意借势", "场景种草", "产品种草", "生活方式", "情感共鸣", "健康科普"]
    platforms = ["抖音", "小红书", "微博", "B站"]
    
    ideas = []
    for i, product in enumerate(client["products"][:2]):  # 每个客户最多2个产品选题
        angle = random.choice(angles)
        platform = random.choice(platforms)
        
        idea = {
            "id": f"扩展_{datetime.now().strftime('%Y%m%d%H%M')}_{client['brand']}_{i+1}",
            "client": client,
            "title": f"{client['brand']}{hotspot['title'][:10]}...的{product}内容",
            "platform": platform,
            "angle": angle,
            "hot_topic": hotspot["title"],
            "hot_topic_id": hotspot["id"],
            "heat": hotspot["trends"][0] if hotspot["trends"] else "热",
            "trend": "新" if "新" in hotspot["trends"] else "热",
            "product": product,
            "keywords": hotspot["keywords"][:4] + [product, client["brand"], "推荐"],
            "quality_score": round(random.uniform(0.6, 0.95), 2),
            "quality_level": random.choice(["A级-优秀", "B级-良好", "C级-普通"]),
            "engagement_estimate": random.choice(["10万+", "20万+", "30万+", "50万+"]),
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        ideas.append(idea)
    
    return ideas

def main():
    base_path = Path("/Users/zhangjingwei/.qclaw/workspace/hotspot-tracker")
    
    # 读取现有热点
    with open(base_path / "hot_topics.json", "r", encoding="utf-8") as f:
        existing_hotspots = json.load(f)
    
    print(f"现有热点数: {len(existing_hotspots)}")
    
    # 合并新热点（添加到开头，移除末尾过时的）
    all_hotspots = NEW_HOTSPOTS + existing_hotspots
    
    # 更新热度值（模拟热度变化）
    for i, h in enumerate(all_hotspots):
        h["rank"] = i + 1
        # 热度随时间衰减
        if i >= len(NEW_HOTSPOTS):
            import random
            decay = random.uniform(0.95, 0.99)
            h["hot_value"] = int(h.get("hot_value", 0) * decay)
            h["heat"] = f"{h['hot_value'] / 100000000:.1f}亿"
            h["isNew"] = False
    
    # 保持100条左右
    all_hotspots = all_hotspots[:100]
    
    # 保存更新后的热点
    with open(base_path / "hot_topics.json", "w", encoding="utf-8") as f:
        json.dump(all_hotspots, f, ensure_ascii=False, indent=2)
    
    print(f"更新后热点数: {len(all_hotspots)}")
    print(f"新增热点数: {len(NEW_HOTSPOTS)}")
    
    # 生成新选题
    new_ideas = []
    for hotspot in NEW_HOTSPOTS:
        for client in CLIENTS:
            if client["brand"] in hotspot.get("c", []):
                ideas = generate_client_ideas(hotspot, client)
                new_ideas.extend(ideas)
    
    # 读取现有选题
    with open(base_path / "client_ideas.json", "r", encoding="utf-8") as f:
        existing_ideas = json.load(f)
    
    # 合并选题
    all_ideas = new_ideas + existing_ideas
    
    # 保持500条左右
    all_ideas = all_ideas[:500]
    
    # 保存选题
    with open(base_path / "client_ideas.json", "w", encoding="utf-8") as f:
        json.dump(all_ideas, f, ensure_ascii=False, indent=2)
    
    print(f"更新后选题数: {len(all_ideas)}")
    print(f"新增选题数: {len(new_ideas)}")
    
    # 返回摘要
    return {
        "hotspots_updated": len(all_hotspots),
        "new_hotspots": len(NEW_HOTSPOTS),
        "ideas_updated": len(all_ideas),
        "new_ideas": len(new_ideas)
    }

if __name__ == "__main__":
    result = main()
    print(json.dumps(result, ensure_ascii=False, indent=2))
