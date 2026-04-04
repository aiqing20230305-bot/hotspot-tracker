import json
from datetime import datetime
import random
import os

# ============================================================
# logic 字段生成：基于热点类型/行业/关键词组合生成热点逻辑描述
# ============================================================
LOGIC_TEMPLATES = {
    "旅游热点": [
        "假期出行需求+景区消费热潮",
        "季节性旅游高峰+社交打卡传播",
        "假日经济带动+文旅消费升级",
        "出行高峰+配套消费场景",
        "旅游旺季+户外休闲需求",
    ],
    "社会热点": [
        "社会民生关注+全民讨论热度",
        "传统节日文化+公众情感共鸣",
        "公共政策热点+社会舆论关注",
        "季节性社会现象+媒体聚焦",
    ],
    "娱乐热点": [
        "影视作品热度+粉丝传播效应",
        "娱乐事件发酵+全网话题讨论",
        "档期票房效应+观影消费热潮",
        "明星效应+社交平台传播",
    ],
    "科技热点": [
        "技术创新突破+产业关注",
        "AI持续火热+全民讨论",
        "科技产品发布+用户期待",
        "前沿科技趋势+行业变革",
        "科技热点+消费电子需求",
    ],
    "美妆热点": [
        "换季护肤需求+美妆消费旺季",
        "成分党护肤理念深化+产品种草",
        "季节性护肤刚需+品牌营销推广",
        "美妆趋势+社交平台种草",
    ],
    "大健康热点": [
        "健康管理意识提升+运动消费",
        "季节性健康需求+养生话题",
        "全民健身趋势+健康消费升级",
        "健康生活方式+营养品需求",
    ],
    "快消热点": [
        "假期消费场景+饮品需求激增",
        "季节性消费+快消品促销",
        "场景化消费+品牌联动营销",
        "生活刚需+消费升级",
    ],
    "母婴热点": [
        "育儿话题+宝妈社群传播",
        "宠物经济崛起+消费升级",
        "母婴消费升级+品质需求",
        "宠物消费+假期寄养需求",
    ],
    "汽车热点": [
        "新能源趋势+出行话题",
        "汽车消费旺季+技术革新",
        "智能驾驶热点+购车需求",
        "绿色出行+新能源话题讨论",
    ],
}

# 默认逻辑模板（当类型不匹配时使用）
DEFAULT_LOGIC_TEMPLATES = [
    "热点事件发酵+全网关注",
    "行业趋势+消费者关注",
    "话题传播+社交裂变",
    "事件驱动+舆论热议",
]

def generate_logic(topic):
    """基于热点类型、行业和关键词生成逻辑描述"""
    topic_type = topic.get('type', '') or topic.get('category', '')
    industries = topic.get('industries', [])
    keywords = topic.get('keywords', [])
    trends = topic.get('trends', [])

    # 优先根据类型匹配模板
    templates = LOGIC_TEMPLATES.get(topic_type, DEFAULT_LOGIC_TEMPLATES)

    # 如果有"新"标记，偏向新品/新趋势逻辑
    if '新' in trends:
        extra_new = ["新品发布+市场关注", "新趋势兴起+用户好奇", "新概念传播+话题裂变"]
        if random.random() < 0.5:
            templates = extra_new

    # 如果有"爆"标记，偏向爆发逻辑
    if '爆' in trends:
        extra_hot = ["突发热点+全网刷屏", "爆款内容+病毒式传播", "事件爆发+舆论热议"]
        if random.random() < 0.5:
            templates = extra_hot

    return random.choice(templates)


# ============================================================
# trend 字段生成：基于历史热度数据计算趋势
# ============================================================
HISTORY_FILE = 'hotspot_history.json'

def load_history():
    """加载历史热度数据"""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_history(history):
    """保存历史热度数据"""
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def calculate_trend(topic, history):
    """
    基于历史数据计算趋势方向。
    使用 title 哈希作为 key 来跟踪同一主题的热度变化。
    返回格式：emoji + 趋势描述
    """
    topic_key = topic.get('title', topic.get('id', ''))
    current_hot = topic.get('hot_value', 0)

    if topic_key in history:
        prev_hot = history[topic_key].get('hot_value', 0)
        if prev_hot > 0:
            change_pct = (current_hot - prev_hot) / prev_hot

            if change_pct > 0.03:
                return "🔥🔥🔥 爆发式增长"
            elif change_pct > 0.01:
                return "🔥🔥🔥 持续上升"
            elif change_pct > -0.01:
                return "🔥🔥 稳定"
            elif change_pct > -0.03:
                return "🔥 下降"
            else:
                return "📉 明显下降"
    else:
        # 没有历史数据的新热点，根据 trends 标记和排名推断
        trends = topic.get('trends', [])
        rank = topic.get('rank', 50)

        if '爆' in trends:
            if rank <= 5:
                return "🔥🔥🔥 爆发式增长"
            else:
                return "🔥🔥🔥 持续上升"
        elif '新' in trends:
            return "🔥🔥🔥 新晋热点"
        elif '热' in trends:
            if rank <= 10:
                return "🔥🔥 持续上升"
            else:
                return "🔥🔥 稳定上升"
        else:
            return "🔥 稳定"

    return "🔥🔥 稳定"


# ============================================================
# 读取现有数据
# ============================================================
with open('hot_topics.json', 'r', encoding='utf-8') as f:
    hot_topics = json.load(f)

with open('client_ideas.json', 'r', encoding='utf-8') as f:
    client_ideas = json.load(f)

now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
date_prefix = datetime.now().strftime('%Y%m%d%H%M')

# 加载历史热度数据
history = load_history()

# 更新现有热点的热度值（模拟热度变化）
for topic in hot_topics:
    # 保存当前热度到历史（用于下次计算趋势）
    topic_key = topic.get('title', topic.get('id', ''))
    history[topic_key] = {
        'hot_value': topic.get('hot_value', 0),
        'updated_at': now
    }

    # 热度随机波动 -5% ~ +5%
    change = random.uniform(-0.05, 0.05)
    topic['hot_value'] = int(topic['hot_value'] * (1 + change))
    topic['updated_at'] = now

    # 补充缺失的 logic 字段
    if 'logic' not in topic or not topic.get('logic'):
        topic['logic'] = generate_logic(topic)

    # 补充缺失的 trend 字段
    if 'trend' not in topic or not topic.get('trend'):
        topic['trend'] = calculate_trend(topic, history)

# 新增热点（清明假期早间热点）
new_topics = [
    {
        "id": f"ht_{date_prefix}_001",
        "title": "清明早间高速拥堵持续 多地启动应急疏导",
        "hot_value": 492000000,
        "platform": "微博/抖音",
        "industries": ["交通", "旅游"],
        "trends": ["爆"],
        "type": "旅游热点",
        "sentiment": "中性",
        "keywords": ["清明", "高速", "拥堵", "出行", "交通"],
        "c": ["农夫山泉", "元气森林", "OATLY"],
        "created_at": now,
        "rank": 1,
        "category": "旅游热点",
        "trend_tags": ["#清明出行", "#高速路况", "#假期出行"],
        "url": "https://weibo.com",
        "logic": "假期出行高峰+交通拥堵引发关注",
        "trend": "🔥🔥🔥 爆发式增长"
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
        "url": "https://weibo.com",
        "logic": "传统节日+文明祭祀观念升级",
        "trend": "🔥🔥🔥 持续上升"
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
        "url": "https://xiaohongshu.com",
        "logic": "户外生活方式兴起+假期社交打卡",
        "trend": "🔥🔥🔥 新晋热点"
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
        "url": "https://weibo.com",
        "logic": "档期票房爆发+观影社交需求",
        "trend": "🔥🔥 持续上升"
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
        "url": "https://douyin.com",
        "logic": "全民健身热潮+季节性运动需求",
        "trend": "🔥🔥🔥 新晋热点"
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
        "url": "https://weibo.com",
        "logic": "假期消费场景+餐饮外卖需求激增",
        "trend": "🔥🔥 稳定上升"
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
        "url": "https://xiaohongshu.com",
        "logic": "换季护肤刚需+敏感肌护理需求",
        "trend": "🔥🔥 稳定上升"
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
        "url": "https://weibo.com",
        "logic": "AI技术突破+创作效率变革",
        "trend": "🔥🔥🔥 爆发式增长"
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
        "url": "https://douyin.com",
        "logic": "宠物经济崛起+假期寄养需求爆发",
        "trend": "🔥🔥🔥 新晋热点"
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
        "url": "https://weibo.com",
        "logic": "新能源出行普及+假期出行痛点",
        "trend": "🔥🔥 稳定"
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

# 保存历史热度数据（用于下次趋势计算）
save_history(history)

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
