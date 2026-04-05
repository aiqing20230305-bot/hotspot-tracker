#!/usr/bin/env python3
"""
热点更新脚本 - 每小时执行
更新 hot_topics.json 和 client_ideas.json
"""
import json
import os
from datetime import datetime, timedelta
import random
import hashlib

# 配置
WORKSPACE = "/Users/zhangjingwei/.qclaw/workspace/hotspot-tracker"
HOT_TOPICS_FILE = os.path.join(WORKSPACE, "hot_topics.json")
CLIENT_IDEAS_FILE = os.path.join(WORKSPACE, "client_ideas.json")

# 20个客户
CLIENTS = [
    {"brand": "荣耀", "industry": "消费电子", "products": ["手机", "平板", "笔记本", "智能手表"]},
    {"brand": "罗技", "industry": "电脑外设", "products": ["鼠标", "键盘", "耳机", "摄像头"]},
    {"brand": "小米", "industry": "消费电子", "products": ["手机", "智能家居", "手表", "充电宝"]},
    {"brand": "索尼", "industry": "消费电子", "products": ["耳机", "相机", "游戏机", "音箱"]},
    {"brand": "AHC", "industry": "美妆护肤", "products": ["精华", "面膜", "防晒", "洁面"]},
    {"brand": "多芬", "industry": "个人护理", "products": ["沐浴露", "洗发水", "香皂", "身体乳"]},
    {"brand": "力士", "industry": "个人护理", "products": ["沐浴露", "洗发水", "护发素", "香氛"]},
    {"brand": "清扬", "industry": "个人护理", "products": ["洗发水", "护发素", "发膜", "头皮护理"]},
    {"brand": "玉兰油", "industry": "美妆护肤", "products": ["精华", "面霜", "眼霜", "美白精华"]},
    {"brand": "汤臣倍健", "industry": "保健食品", "products": ["蛋白粉", "维生素", "鱼油", "钙片"]},
    {"brand": "善存", "industry": "保健食品", "products": ["多种维生素", "矿物质", "膳食纤维", "叶酸"]},
    {"brand": "HC", "industry": "保健食品", "products": ["鱼油", "益生菌", "胶原蛋白", "辅酶Q10"]},
    {"brand": "威猛先生", "industry": "家居清洁", "products": ["清洁剂", "除垢剂", "厨房清洁", "浴室清洁"]},
    {"brand": "舒适", "industry": "母婴护理", "products": ["纸尿裤", "湿巾", "棉柔巾", "婴儿护肤"]},
    {"brand": "希宝", "industry": "宠物食品", "products": ["猫粮", "猫罐头", "猫零食", "猫砂"]},
    {"brand": "皇家", "industry": "宠物食品", "products": ["猫粮", "狗粮", "处方粮", "营养品"]},
    {"brand": "OATLY", "industry": "食品饮料", "products": ["燕麦奶", "燕麦饮", "咖啡伴侣"]},
    {"brand": "百威", "industry": "啤酒饮料", "products": ["啤酒", "无醇啤酒", "预调酒", "啤酒礼盒"]},
    {"brand": "元气森林", "industry": "食品饮料", "products": ["气泡水", "无糖茶", "电解质水", "能量饮料"]},
    {"brand": "农夫山泉", "industry": "食品饮料", "products": ["矿泉水", "茶饮料", "果汁", "运动饮料"]},
]

# 热点类别
HOT_CATEGORIES = ["科技", "美妆", "母婴", "健身", "美食", "旅游", "教育", "汽车", "宠物", "家居"]

# 新热点模板（模拟当前热点）
NEW_HOT_TEMPLATES = [
    {"title": "五一旅游预订火爆 机票酒店价格飙升", "platform": "微博/抖音", "type": "旅游热点", "sentiment": "中性", "keywords": ["五一", "旅游", "预订", "机票", "酒店"]},
    {"title": "AI助手功能大比拼 ChatGPT vs Claude谁更强", "platform": "微博/B站", "type": "科技热点", "sentiment": "正面", "keywords": ["AI", "ChatGPT", "Claude", "对比", "智能助手"]},
    {"title": "夏季防晒新品上市 物理防晒成主流", "platform": "小红书/抖音", "type": "美妆热点", "sentiment": "正面", "keywords": ["防晒", "夏季", "物理防晒", "新品", "护肤"]},
    {"title": "居家健身新趋势 瑜伽垫销量暴涨", "platform": "抖音/小红书", "type": "健身热点", "sentiment": "正面", "keywords": ["健身", "瑜伽", "居家", "运动", "健康"]},
    {"title": "预制菜争议再起 食品安全引关注", "platform": "微博/抖音", "type": "美食热点", "sentiment": "负面", "keywords": ["预制菜", "食品安全", "争议", "健康", "饮食"]},
    {"title": "新能源汽车充电难 充电桩建设提速", "platform": "微博/全网", "type": "汽车热点", "sentiment": "中性", "keywords": ["新能源", "充电", "充电桩", "汽车", "基建"]},
    {"title": "宠物友好商场增多 带宠出行成新潮流", "platform": "小红书/抖音", "type": "宠物热点", "sentiment": "正面", "keywords": ["宠物", "商场", "友好", "出行", "潮流"]},
    {"title": "智能家居价格战 百元智能设备普及", "platform": "微博/抖音", "type": "家居热点", "sentiment": "正面", "keywords": ["智能家居", "价格战", "普及", "科技", "生活"]},
    {"title": "春季育儿知识科普 儿童过敏防护", "platform": "小红书/微博", "type": "母婴热点", "sentiment": "正面", "keywords": ["育儿", "春季", "过敏", "儿童", "健康"]},
    {"title": "考研复试结果公布 调剂信息汇总", "platform": "微博/全网", "type": "教育热点", "sentiment": "中性", "keywords": ["考研", "复试", "调剂", "教育", "升学"]},
]

def generate_id():
    """生成唯一ID"""
    return f"ht_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000,9999)}"

def generate_idea_id(client_brand):
    """生成选题ID"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    return f"hourly_{timestamp}_{client_brand}_{random.randint(1,999)}"

def load_json(filepath):
    """加载JSON文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return []

def save_json(filepath, data):
    """保存JSON文件"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved {filepath} with {len(data)} items")

def generate_new_hot_topics(count=10):
    """生成新的热点数据"""
    new_topics = []
    now = datetime.now()
    
    for i, template in enumerate(NEW_HOT_TEMPLATES[:count]):
        topic = {
            "id": generate_id(),
            "title": template["title"],
            "platform": template["platform"],
            "hot_value": random.randint(150000000, 500000000),
            "industries": [template["type"].replace("热点", "")],
            "trends": ["热"] if random.random() > 0.3 else ["爆"],
            "type": template["type"],
            "sentiment": template["sentiment"],
            "keywords": template["keywords"],
            "c": random.sample([c["brand"] for c in CLIENTS], k=random.randint(2, 4)),
            "created_at": now.isoformat(),
            "rank": i + 1,
            "category": template["type"],
            "trend_tags": [f"#{kw}" for kw in template["keywords"][:3]],
            "url": "https://weibo.com",
            "updated_at": now.isoformat(),
            "heat": f"{random.randint(1,5)}.{random.randint(0,9)}亿",
            "logic": f"{template['type'].replace('热点', '')}话题热度上升",
            "trend": "上升",
            "isNew": True,
            "platforms": template["platform"].split("/")
        }
        new_topics.append(topic)
    
    return new_topics

def match_clients_to_topic(topic):
    """根据热点匹配合适的客户"""
    matched = []
    topic_type = topic.get("type", "")
    keywords = topic.get("keywords", [])
    
    for client in CLIENTS:
        score = 0
        # 根据行业匹配
        if "科技" in topic_type and client["industry"] in ["消费电子", "电脑外设"]:
            score += 3
        if "美妆" in topic_type and client["industry"] in ["美妆护肤", "个人护理"]:
            score += 3
        if "健身" in topic_type and client["industry"] in ["保健食品"]:
            score += 3
        if "美食" in topic_type and client["industry"] in ["食品饮料", "啤酒饮料"]:
            score += 3
        if "宠物" in topic_type and client["industry"] in ["宠物食品"]:
            score += 3
        if "母婴" in topic_type and client["industry"] in ["母婴护理", "家居清洁"]:
            score += 3
        if "家居" in topic_type and client["industry"] in ["消费电子", "电脑外设", "家居清洁"]:
            score += 2
        if "旅游" in topic_type:
            score += 1  # 旅游热点通用性较强
        
        if score > 0:
            matched.append((client, score))
    
    # 按分数排序，取前5个
    matched.sort(key=lambda x: x[1], reverse=True)
    return [m[0] for m in matched[:5]]

def generate_content_idea(client, topic):
    """为客户生成选题"""
    angles = ["场景种草", "产品种草", "科普教育", "情感共鸣", "产品测评", "生活方式", "科技借势", "竞品对比", "新品推广"]
    platforms = ["微博", "抖音", "小红书", "B站"]
    
    angle = random.choice(angles)
    platform = random.choice(platforms)
    product = random.choice(client["products"])
    
    # 生成标题
    title_templates = [
        f"{client['brand']}{product} | {topic['title'][:15]}...",
        f"{topic['title'][:12]} {client['brand']}{product}来帮忙",
        f"{client['brand']}新品{product}测评 | {topic['title'][:12]}",
        f"{angle}：{client['brand']}{product}遇上{topic['title'][:10]}",
        f"{client['brand']}{product}攻略 | {topic['title'][:15]}",
    ]
    
    title = random.choice(title_templates)
    
    idea = {
        "id": generate_idea_id(client["brand"]),
        "client": client,
        "title": title,
        "platform": platform,
        "angle": angle,
        "hot_topic": topic["title"],
        "hot_topic_type": topic.get("type", "热点"),
        "heat": topic.get("heat", "热"),
        "trend": topic.get("trend", "🔥"),
        "product": product,
        "keywords": [client["brand"], product, topic.get("type", "").replace("热点", ""), angle],
        "quality_score": round(random.uniform(0.75, 0.98), 2),
        "quality_level": random.choice(["A级-优秀", "B级-良好"]),
        "engagement_estimate": f"{random.randint(5, 50)}万+",
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "content": f"基于热点「{topic['title']}」，为{client['brand']}策划{angle}内容，结合{product}进行营销推广。"
    }
    
    return idea

def update_hot_topics():
    """更新热点数据"""
    print("=" * 50)
    print("开始更新热点数据...")
    
    # 加载现有数据
    hot_topics = load_json(HOT_TOPICS_FILE)
    print(f"当前热点数量: {len(hot_topics)}")
    
    # 生成新热点
    new_topics = generate_new_hot_topics(10)
    print(f"生成新热点: {len(new_topics)}条")
    
    # 合并数据，保持100条左右
    all_topics = new_topics + hot_topics
    # 去重（基于title）
    seen_titles = set()
    unique_topics = []
    for topic in all_topics:
        title = topic.get("title", "")
        if title and title not in seen_titles:
            seen_titles.add(title)
            unique_topics.append(topic)
    
    # 保留最新的100条
    final_topics = unique_topics[:100]
    
    # 保存
    save_json(HOT_TOPICS_FILE, final_topics)
    print(f"更新后热点数量: {len(final_topics)}")
    
    return new_topics

def update_client_ideas(new_topics):
    """更新客户选题"""
    print("=" * 50)
    print("开始更新客户选题...")
    
    # 加载现有选题
    ideas = load_json(CLIENT_IDEAS_FILE)
    print(f"当前选题数量: {len(ideas)}")
    
    # 为每个新热点生成选题
    new_ideas = []
    for topic in new_topics:
        matched_clients = match_clients_to_topic(topic)
        for client in matched_clients:
            idea = generate_content_idea(client, topic)
            new_ideas.append(idea)
    
    print(f"生成新选题: {len(new_ideas)}条")
    
    # 合并并保留最新的500条
    all_ideas = new_ideas + ideas
    final_ideas = all_ideas[:500]
    
    # 保存
    save_json(CLIENT_IDEAS_FILE, final_ideas)
    print(f"更新后选题数量: {len(final_ideas)}")
    
    return len(new_ideas)

def main():
    """主函数"""
    print("=" * 50)
    print(f"热点运营助手 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 确保目录存在
    os.makedirs(WORKSPACE, exist_ok=True)
    
    # 更新热点
    new_topics = update_hot_topics()
    
    # 更新选题
    new_ideas_count = update_client_ideas(new_topics)
    
    print("=" * 50)
    print("更新完成!")
    print(f"新增热点: {len(new_topics)}条")
    print(f"新增选题: {new_ideas_count}条")
    print("=" * 50)
    
    # 输出摘要
    print("\n新增热点摘要:")
    for i, topic in enumerate(new_topics[:5], 1):
        print(f"  {i}. {topic['title']} ({topic['heat']})")

if __name__ == "__main__":
    main()
