import json
from datetime import datetime
import random

# 读取现有热点
with open('hot_topics.json', 'r', encoding='utf-8') as f:
    hot_topics = json.load(f)

# 读取现有选题
with open('client_ideas.json', 'r', encoding='utf-8') as f:
    client_ideas = json.load(f)

now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
date_prefix = datetime.now().strftime('%Y%m%d%H%M')

# 更新现有热点的热度值（模拟热度变化）
for topic in hot_topics:
    # 热度随机波动 -5% ~ +5%
    change = random.uniform(-0.05, 0.05)
    topic['hot_value'] = int(topic['hot_value'] * (1 + change))
    topic['updated_at'] = now

# 新增热点（清明假期早间热点）
new_topics = [
    {
        "id": f"ht_{date_prefix}_001",
        "title": "清明早间高速拥堵持续 多地启动应急疏导",
        "hot_value": 492000000,
        "platform": "微博/抖音",
        "industries": ["交通", "旅游"],
        "trends": ["爆"],
        "type": "快消热点",
        "sentiment": "中性",
        "keywords": ["清明", "高速", "拥堵", "出行", "交通"],
        "c": ["农夫山泉", "元气森林", "OATLY"],
        "created_at": now,
        "rank": 1,
        "category": "快消热点",
        "trend_tags": ["#清明出行", "#高速路况", "#假期出行"],
        "url": "https://weibo.com"
    },
    {
        "id": f"ht_{date_prefix}_002",
        "title": "清明祭扫迎来早高峰 文明祭祀成主流",
        "hot_value": 485000000,
        "platform": "微博/小红书",
        "industries": ["社会", "文化"],
        "trends": ["爆", "热"],
        "type": "社会热点",
        "sentiment": "正面",
        "keywords": ["清明", "祭扫", "文明祭祀", "环保", "传统"],
        "c": ["农夫山泉", "元气森林"],
        "created_at": now,
        "rank": 2,
        "category": "社会热点",
        "trend_tags": ["#文明祭祀", "#清明祭祖", "#环保清明"],
        "url": "https://weibo.com"
    },
    {
        "id": f"ht_{date_prefix}_003",
        "title": "清明假期露营日出打卡 小红书美图刷屏",
        "hot_value": 478000000,
        "platform": "小红书/抖音",
        "industries": ["旅游", "户外"],
        "trends": ["热", "新"],
        "type": "旅游热点",
        "sentiment": "正面",
        "keywords": ["清明", "露营", "日出", "踏青", "打卡"],
        "c": ["农夫山泉", "元气森林", "OATLY", "百威"],
        "created_at": now,
        "rank": 3,
        "category": "旅游热点",
        "trend_tags": ["#清明露营", "#日出打卡", "#踏青攻略"],
        "url": "https://xiaohongshu.com"
    },
    {
        "id": f"ht_{date_prefix}_004",
        "title": "清明档电影首日票房破2亿 观影热潮涌动",
        "hot_value": 468000000,
        "platform": "微博/抖音",
        "industries": ["娱乐", "电影"],
        "trends": ["热"],
        "type": "娱乐热点",
        "sentiment": "正面",
        "keywords": ["清明档", "电影", "票房", "观影", "娱乐"],
        "c": ["农夫山泉", "元气森林", "百威"],
        "created_at": now,
        "rank": 4,
        "category": "娱乐热点",
        "trend_tags": ["#清明档电影", "#电影推荐", "#假期观影"],
        "url": "https://weibo.com"
    },
    {
        "id": f"ht_{date_prefix}_005",
        "title": "春季晨跑热潮兴起 健身博主分享打卡攻略",
        "hot_value": 455000000,
        "platform": "抖音/小红书",
        "industries": ["健身", "健康"],
        "trends": ["热", "新"],
        "type": "大健康热点",
        "sentiment": "正面",
        "keywords": ["晨跑", "春季", "健身", "运动", "健康"],
        "c": ["汤臣倍健", "善存", "农夫山泉"],
        "created_at": now,
        "rank": 5,
        "category": "大健康热点",
        "trend_tags": ["#春季晨跑", "#健身打卡", "#运动生活"],
        "url": "https://douyin.com"
    },
    {
        "id": f"ht_{date_prefix}_006",
        "title": "清明假期早餐消费激增 外卖早茶订单翻倍",
        "hot_value": 448000000,
        "platform": "微博/抖音",
        "industries": ["餐饮", "消费"],
        "trends": ["热"],
        "type": "快消热点",
        "sentiment": "正面",
        "keywords": ["清明", "早餐", "外卖", "消费", "早茶"],
        "c": ["农夫山泉", "元气森林", "OATLY"],
        "created_at": now,
        "rank": 6,
        "category": "快消热点",
        "trend_tags": ["#假期早餐", "#外卖推荐", "#早茶文化"],
        "url": "https://weibo.com"
    },
    {
        "id": f"ht_{date_prefix}_007",
        "title": "春季敏感肌护理攻略 防晒修护成刚需",
        "hot_value": 442000000,
        "platform": "小红书/微博",
        "industries": ["美妆", "护肤"],
        "trends": ["热"],
        "type": "美妆热点",
        "sentiment": "正面",
        "keywords": ["敏感肌", "防晒", "护肤", "春季", "修护"],
        "c": ["AHC", "玉兰油", "多芬", "力士"],
        "created_at": now,
        "rank": 7,
        "category": "美妆热点",
        "trend_tags": ["#敏感肌护肤", "#防晒攻略", "#春季护肤"],
        "url": "https://xiaohongshu.com"
    },
    {
        "id": f"ht_{date_prefix}_008",
        "title": "AI视频生成工具爆火 创作者效率革命",
        "hot_value": 435000000,
        "platform": "微博/B站",
        "industries": ["科技", "AI"],
        "trends": ["爆", "新"],
        "type": "科技热点",
        "sentiment": "正面",
        "keywords": ["AI", "视频生成", "创作", "效率", "科技"],
        "c": ["小米", "荣耀", "索尼", "罗技"],
        "created_at": now,
        "rank": 8,
        "category": "科技热点",
        "trend_tags": ["#AI创作", "#视频生成", "#科技前沿"],
        "url": "https://weibo.com"
    },
    {
        "id": f"ht_{date_prefix}_009",
        "title": "清明假期宠物寄养爆满 萌宠酒店一房难求",
        "hot_value": 428000000,
        "platform": "抖音/小红书",
        "industries": ["宠物", "服务"],
        "trends": ["热", "新"],
        "type": "母婴热点",
        "sentiment": "正面",
        "keywords": ["宠物", "寄养", "清明", "萌宠", "假期"],
        "c": ["希宝", "皇家"],
        "created_at": now,
        "rank": 9,
        "category": "母婴热点",
        "trend_tags": ["#宠物寄养", "#萌宠生活", "#假期养宠"],
        "url": "https://douyin.com"
    },
    {
        "id": f"ht_{date_prefix}_010",
        "title": "新能源汽车清明出行 充电桩排队引热议",
        "hot_value": 422000000,
        "platform": "微博/抖音",
        "industries": ["汽车", "新能源"],
        "trends": ["热"],
        "type": "汽车热点",
        "sentiment": "中性",
        "keywords": ["新能源", "充电桩", "出行", "电动车", "续航"],
        "c": ["小米", "荣耀"],
        "created_at": now,
        "rank": 10,
        "category": "汽车热点",
        "trend_tags": ["#新能源出行", "#充电桩", "#电动车续航"],
        "url": "https://weibo.com"
    }
]

# 将新热点插入到列表前面
for i, topic in enumerate(new_topics):
    topic['rank'] = i + 1
hot_topics = new_topics + hot_topics

# 保持总数约100条
hot_topics = hot_topics[:100]

# 更新排名
for i, topic in enumerate(hot_topics):
    topic['rank'] = i + 1

# 保存更新后的热点
with open('hot_topics.json', 'w', encoding='utf-8') as f:
    json.dump(hot_topics, f, ensure_ascii=False, indent=2)

print(f"热点更新完成: 新增{len(new_topics)}条, 总计{len(hot_topics)}条")

# 客户列表
clients = [
    {"brand": "荣耀", "industry": "科技/手机", "products": ["手机", "平板", "耳机", "智能手表"]},
    {"brand": "罗技", "industry": "科技/外设", "products": ["键盘", "鼠标", "耳机", "游戏手柄"]},
    {"brand": "小米", "industry": "科技/智能家居", "products": ["手机", "智能家居", "电动车", "家电"]},
    {"brand": "索尼", "industry": "科技/娱乐", "products": ["相机", "耳机", "游戏机", "电视"]},
    {"brand": "AHC", "industry": "美妆/护肤", "products": ["眼霜", "面霜", "精华", "面膜"]},
    {"brand": "多芬", "industry": "个护/美妆", "products": ["沐浴露", "洗发水", "护发素", "身体乳"]},
    {"brand": "力士", "industry": "个护", "products": ["沐浴露", "洗发水", "香皂"]},
    {"brand": "清扬", "industry": "个护/洗护", "products": ["洗发水", "护发素", "去屑产品"]},
    {"brand": "玉兰油", "industry": "美妆/护肤", "products": ["面霜", "精华", "防晒", "洁面"]},
    {"brand": "汤臣倍健", "industry": "保健品", "products": ["维生素", "蛋白粉", "鱼油", "益生菌"]},
    {"brand": "善存", "industry": "保健品", "products": ["复合维生素", "钙片", "叶酸"]},
    {"brand": "HC", "industry": "美妆/护肤", "products": ["护肤品", "彩妆", "精华"]},
    {"brand": "威猛先生", "industry": "家居清洁", "products": ["清洁剂", "去污剂", "厨房清洁"]},
    {"brand": "舒适", "industry": "个护/剃须", "products": ["剃须刀", "剃须膏", "护肤"]},
    {"brand": "希宝", "industry": "宠物食品", "products": ["猫粮", "猫罐头", "猫零食"]},
    {"brand": "皇家", "industry": "宠物食品", "products": ["猫粮", "狗粮", "宠物营养品"]},
    {"brand": "OATLY", "industry": "食品/植物奶", "products": ["燕麦奶", "燕麦饮", "咖啡伴侣"]},
    {"brand": "百威", "industry": "酒饮", "products": ["啤酒", "精酿", "低醇啤酒"]},
    {"brand": "元气森林", "industry": "饮料", "products": ["气泡水", "无糖茶", "电解质水", "乳茶"]},
    {"brand": "农夫山泉", "industry": "饮料/水", "products": ["矿泉水", "茶饮料", "果汁", "功能饮料"]}
]

# 为每个客户基于新热点生成选题
angles = ["场景种草", "情感共鸣", "生活方式", "产品测评", "科普内容"]
platforms = ["微博", "小红书", "抖音", "B站"]

new_ideas = []
idea_count = 0

for client in clients:
    # 每个客户生成3-5条选题
    num_ideas = random.randint(3, 5)
    selected_topics = random.sample(new_topics[:5], min(num_ideas, 5))
    
    for topic in selected_topics:
        product = random.choice(client["products"])
        angle = random.choice(angles)
        platform = random.choice(platforms)
        
        idea = {
            "id": f"{client['brand']}_{date_prefix}_{idea_count:03d}",
            "client": client,
            "title": f"{client['brand']}{topic['title'][:15]}{product}的{angle}",
            "platform": platform,
            "angle": angle,
            "hot_topic": topic['title'],
            "hot_topic_id": topic['id'],
            "heat": "热",
            "trend": random.choice(["热", "爆", "新"]),
            "product": product,
            "keywords": topic['keywords'][:3] + [client['brand']],
            "quality_score": round(random.uniform(0.75, 0.95), 2),
            "quality_level": random.choice(["A级-优秀", "B级-良好"]),
            "engagement_estimate": random.choice(["8万+", "10万+", "12万+", "14万+"]),
            "status": "pending",
            "created_at": now
        }
        new_ideas.append(idea)
        idea_count += 1

# 将新选题添加到列表前面
client_ideas = new_ideas + client_ideas

# 保持总数约500条
client_ideas = client_ideas[:500]

# 保存更新后的选题
with open('client_ideas.json', 'w', encoding='utf-8') as f:
    json.dump(client_ideas, f, ensure_ascii=False, indent=2)

print(f"选题更新完成: 新增{len(new_ideas)}条, 总计{len(client_ideas)}条")
