#!/usr/bin/env python3
"""
热点追踪器更新脚本 - 2026-04-04 16:10
自动生成完整字段：platforms, heat, isNew, logic, trend
"""
import json
import uuid
from datetime import datetime, timedelta
from pathlib import Path

now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

# ============ 新抓取的实时热点数据 ============
# 微博热搜 TOP9
weibo_trends = [
    {"title": "孙颖莎4比3险胜高达 乒乓球世界杯激战", "heat": 1040000, "platform": "微博", "industries": ["体育", "乒乓球"], "type": "体育热点", "sentiment": "正面", "keywords": ["孙颖莎", "乒乓球", "世界杯", "高达", "体育"]},
    {"title": "清明上山扫墓却发现母亲的墓不见了 家属崩溃", "heat": 730000, "platform": "微博", "industries": ["社会", "民生"], "type": "社会热点", "sentiment": "负面", "keywords": ["清明", "扫墓", "墓碑", "社会事件"]},
    {"title": "多巴胺花海惊艳上线 各地公园迎赏花高峰", "heat": 600000, "platform": "微博/小红书", "industries": ["旅游", "摄影"], "type": "旅游热点", "sentiment": "正面", "keywords": ["多巴胺", "花海", "赏花", "公园", "打卡"]},
    {"title": "高达哭了 全网热议机甲动漫情怀", "heat": 340000, "platform": "微博/抖音", "industries": ["动漫", "娱乐"], "type": "娱乐热点", "sentiment": "正面", "keywords": ["高达", "机甲", "动漫", "情怀", "童年"]},
    {"title": "浪姐改赛制给齐思钧苦得都掐眉头了", "heat": 330000, "platform": "微博/抖音", "industries": ["娱乐", "综艺"], "type": "娱乐热点", "sentiment": "中性", "keywords": ["浪姐", "齐思钧", "综艺", "赛制", "明星"]},
    {"title": "当你以为回县城老家是退路时 引发年轻人共鸣", "heat": 330000, "platform": "微博", "industries": ["社会", "职场"], "type": "社会热点", "sentiment": "中性", "keywords": ["县城", "回老家", "年轻人", "职场", "退路"]},
    {"title": "十日终焉 肖战剧版超话开通引爆热搜", "heat": 160000, "platform": "微博/B站", "industries": ["娱乐", "影视"], "type": "娱乐热点", "sentiment": "正面", "keywords": ["十日终焉", "肖战", "剧版", "影视", "明星"]},
    {"title": "文旅共绘诗与远方新画卷 各地文旅局长出圈", "heat": 160000, "platform": "微博/抖音", "industries": ["旅游", "文化"], "type": "旅游热点", "sentiment": "正面", "keywords": ["文旅", "诗和远方", "旅游", "局长", "出圈"]},
    {"title": "AirPods Max 2首发体验 苹果音频产品大更新", "heat": 1200000, "platform": "微博/小红书", "industries": ["科技", "数码"], "type": "科技热点", "sentiment": "正面", "keywords": ["AirPods Max 2", "苹果", "耳机", "科技", "数码"]},
]

# B站热门 TOP10
bilibili_trends = [
    {"title": "对子战神2 鬼畜视频全网刷屏", "heat": 5497000, "platform": "B站", "industries": ["娱乐", "鬼畜"], "type": "娱乐热点", "sentiment": "正面", "keywords": ["对子战神", "鬼畜", "B站", "视频", "梗"]},
    {"title": "凶手一句话 造就十年悬案 悬疑剧情解析", "heat": 3017000, "platform": "B站", "industries": ["娱乐", "悬疑"], "type": "娱乐热点", "sentiment": "正面", "keywords": ["悬案", "悬疑", "剧情", "推理", "故事"]},
    {"title": "崩坏星穹铁道动画短片发布 玩家沸腾", "heat": 3428000, "platform": "B站/微博", "industries": ["游戏", "动漫"], "type": "娱乐热点", "sentiment": "正面", "keywords": ["崩坏星穹铁道", "米哈游", "游戏", "动画", "玩家"]},
    {"title": "一切都来的太突然了 情感故事触动人心", "heat": 3004000, "platform": "B站", "industries": ["情感", "社会"], "type": "社会热点", "sentiment": "正面", "keywords": ["情感", "故事", "触动", "突然", "共鸣"]},
    {"title": "鸟为什么会飞 趣味科普视频走红", "heat": 3401000, "platform": "B站/抖音", "industries": ["教育", "科普"], "type": "教育热点", "sentiment": "正面", "keywords": ["鸟", "飞行", "科普", "知识", "趣味"]},
    {"title": "谁命苦 讽刺喜剧引发共鸣", "heat": 3578000, "platform": "B站", "industries": ["娱乐", "喜剧"], "type": "娱乐热点", "sentiment": "正面", "keywords": ["喜剧", "讽刺", "谁命苦", "幽默", "共鸣"]},
    {"title": "明日方舟SideStory活动PV发布 玩家期待", "heat": 2389000, "platform": "B站", "industries": ["游戏", "动漫"], "type": "娱乐热点", "sentiment": "正面", "keywords": ["明日方舟", "游戏", "PV", "活动", "玩家"]},
    {"title": "猿神有谁能懂的 攻略合订本爆火", "heat": 2649000, "platform": "B站", "industries": ["游戏", "娱乐"], "type": "娱乐热点", "sentiment": "正面", "keywords": ["猿神", "黑神话", "游戏攻略", "B站", "玩家"]},
    {"title": "我被开除了那就去旅行 辞职旅行风潮", "heat": 2025000, "platform": "B站/小红书", "industries": ["旅游", "生活方式"], "type": "旅游热点", "sentiment": "正面", "keywords": ["辞职", "旅行", "裸辞", "旅行风潮", "生活方式"]},
    {"title": "教室黑板脱落两男生眼疾手快救人 正能量刷屏", "heat": 4406000, "platform": "B站/微博", "industries": ["教育", "社会"], "type": "社会热点", "sentiment": "正面", "keywords": ["正能量", "教室", "救人", "学生", "社会"]},
]

# 知乎热榜 TOP10
zhihu_trends = [
    {"title": "优思益声明已无力进行售后整体崩溃边缘 消费者维权", "heat": 5420000, "platform": "知乎", "industries": ["消费", "维权"], "type": "社会热点", "sentiment": "负面", "keywords": ["优思益", "消费者", "维权", "售后", "崩溃"]},
    {"title": "华谊兄弟超5600万债务逾期 王氏兄弟持股全被冻结", "heat": 5350000, "platform": "知乎", "industries": ["财经", "影视"], "type": "财经热点", "sentiment": "负面", "keywords": ["华谊兄弟", "债务", "逾期", "影视", "财经"]},
    {"title": "华南F3祖坟为什么建在高山上 后代如何精准找到祖坟", "heat": 3590000, "platform": "知乎", "industries": ["文化", "社会"], "type": "社会热点", "sentiment": "中性", "keywords": ["华南F3", "祖坟", "清明", "文化", "祭祀"]},
    {"title": "伊朗宣称击落美国先进战斗机 飞行员或被俘虏", "heat": 2340000, "platform": "知乎", "industries": ["国际", "军事"], "type": "国际热点", "sentiment": "负面", "keywords": ["伊朗", "美国", "战斗机", "军事", "国际"]},
    {"title": "42岁面试被嫌弃年纪大该如何回答 职场年龄歧视引热议", "heat": 2070000, "platform": "知乎", "industries": ["职场", "社会"], "type": "社会热点", "sentiment": "负面", "keywords": ["职场", "年龄歧视", "面试", "就业", "社会"]},
    {"title": " Anthropic封杀OpenClaw踢出Claude订阅服务白名单", "heat": 2060000, "platform": "知乎", "industries": ["科技", "AI"], "type": "科技热点", "sentiment": "负面", "keywords": ["Anthropic", "Claude", "AI", "科技", "争议"]},
    {"title": "与辉同行就带货优思益致歉 将全额退款", "heat": 2060000, "platform": "知乎", "industries": ["电商", "消费"], "type": "快消热点", "sentiment": "负面", "keywords": ["与辉同行", "直播带货", "优思益", "退款", "电商"]},
]

# 虎嗅/科技热榜 TOP10
huxiu_trends = [
    {"title": "比亚迪狼真的来了 新能源市场竞争加剧", "heat": 1400000, "platform": "虎嗅", "industries": ["汽车", "新能源"], "type": "汽车热点", "sentiment": "中性", "keywords": ["比亚迪", "新能源", "汽车", "市场竞争", "电动车"]},
    {"title": "涨价茅台凭什么 白酒品牌定价引发争议", "heat": 718000, "platform": "虎嗅", "industries": ["食品", "消费"], "type": "美食热点", "sentiment": "中性", "keywords": ["茅台", "涨价", "白酒", "品牌", "定价"]},
    {"title": "被中国淘汰的车却在印度杀疯了 中国车印度热销", "heat": 493000, "platform": "虎嗅", "industries": ["汽车", "出海"], "type": "汽车热点", "sentiment": "正面", "keywords": ["中国车", "印度", "出海", "汽车", "新能源"]},
    {"title": "不要对发达国家生活水平有滤镜 海外生活真相", "heat": 451000, "platform": "虎嗅", "industries": ["社会", "国际"], "type": "社会热点", "sentiment": "中性", "keywords": ["发达国家", "生活水平", "留学", "海外", "滤镜"]},
    {"title": "智谱一边狂奔一边失血 AI大模型商业化困境", "heat": 393000, "platform": "虎嗅", "industries": ["科技", "AI"], "type": "科技热点", "sentiment": "负面", "keywords": ["智谱", "AI", "大模型", "商业化", "科技"]},
    {"title": "甲骨文血洗3万人 47人团队仅留3人 科技裁员风暴", "heat": 395000, "platform": "虎嗅", "industries": ["科技", "职场"], "type": "科技热点", "sentiment": "负面", "keywords": ["甲骨文", "裁员", "职场", "科技", "就业"]},
    {"title": "雷军的考验还没完 小米造车面临的挑战", "heat": 421000, "platform": "虎嗅", "industries": ["科技", "汽车"], "type": "汽车热点", "sentiment": "中性", "keywords": ["雷军", "小米", "造车", "新能源", "挑战"]},
    {"title": "武汉三环线萝卜快跑集体抛锚 自动驾驶安全引关注", "heat": 292000, "platform": "虎嗅", "industries": ["科技", "汽车"], "type": "汽车热点", "sentiment": "负面", "keywords": ["萝卜快跑", "自动驾驶", "武汉", "抛锚", "安全"]},
    {"title": "电子垃圾iPhone4成打脸AI审美的回旋镖", "heat": 318000, "platform": "虎嗅", "industries": ["科技", "社会"], "type": "科技热点", "sentiment": "中性", "keywords": ["iPhone4", "AI审美", "电子垃圾", "苹果", "回旋镖"]},
]

# 合并所有新热点
all_new_trends = weibo_trends + bilibili_trends + zhihu_trends + huxiu_trends

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
    {"brand": "农夫山泉", "industry": "饮料/水", "products": ["矿泉水", "茶饮料", "果汁", "功能饮料"]},
]

# 热点与客户的关联映射
trend_client_map = {
    "孙颖莎": ["汤臣倍健", "善存", "荣耀", "小米"],
    "高达": ["索尼", "罗技", "小米"],
    "浪姐": ["农夫山泉", "元气森林", "OATLY"],
    "县城老家": ["汤臣倍健", "善存", "OATLY"],
    "十日终焉": ["索尼", "小米"],
    "AirPods": ["索尼", "荣耀", "罗技"],
    "对子战神": ["罗技", "小米", "荣耀"],
    "崩坏": ["索尼", "罗技", "小米"],
    "鸟为什么会飞": ["汤臣倍健", "善存", "荣耀"],
    "谁命苦": ["元气森林", "农夫山泉", "OATLY"],
    "辞职旅行": ["农夫山泉", "元气森林", "OATLY", "百威"],
    "教室救人": ["汤臣倍健", "善存", "玉兰油", "AHC"],
    "优思益": ["汤臣倍健", "善存"],
    "华谊兄弟": ["农夫山泉", "元气森林", "百威"],
    "华南F3": ["农夫山泉", "元气森林", "OATLY"],
    "伊朗": ["小米", "荣耀"],
    "年龄歧视": ["汤臣倍健", "善存", "清扬", "多芬"],
    "Anthropic": ["小米", "荣耀", "索尼"],
    "比亚迪": ["小米", "荣耀"],
    "茅台": ["百威", "元气森林"],
    "智谱": ["小米", "荣耀", "索尼", "罗技"],
    "甲骨文": ["荣耀", "小米", "罗技"],
    "雷军": ["小米", "荣耀", "罗技"],
    "萝卜快跑": ["小米", "荣耀", "索尼"],
    "iPhone4": ["小米", "荣耀", "索尼"],
    "多巴胺花海": ["索尼", "荣耀", "小米"],
    "文旅": ["农夫山泉", "元气森林", "百威"],
    "祖坟": ["农夫山泉", "元气森林"],
    "电子垃圾": ["小米", "荣耀", "索尼"],
    "清明": ["农夫山泉", "元气森林", "OATLY", "希宝", "皇家"],
    "悬案": ["小米", "荣耀"],
    "游戏": ["罗技", "索尼", "小米"],
    "教室": ["汤臣倍健", "善存"],
    "中国车": ["小米", "荣耀"],
}

angles = ["场景种草", "情感共鸣", "科普内容", "生活方式", "产品测评"]

# ============ 数据处理辅助函数 ============

def format_heat(hot_value):
    """格式化热度值为人类可读格式"""
    if hot_value >= 100000000:  # 1亿
        return f"{hot_value / 100000000:.1f}亿"
    elif hot_value >= 10000000:  # 1000万
        return f"{hot_value / 10000000:.0f}万"
    elif hot_value >= 1000000:  # 100万
        return f"{hot_value / 1000000:.0f}万"
    elif hot_value >= 10000:  # 1万
        return f"{hot_value / 10000:.0f}万"
    else:
        return str(hot_value)

def parse_platforms(platform_str):
    """将平台字符串解析为数组"""
    if not platform_str:
        return []
    platforms = []
    for sep in ["/", "|", "，", ","]:
        if sep in platform_str:
            platforms = [p.strip() for p in platform_str.split(sep) if p.strip()]
            break
    if not platforms:
        platforms = [platform_str.strip()]
    return platforms

def generate_logic(topic, clients):
    """生成逻辑分析字段"""
    title = topic.get("title", "")
    industries = topic.get("industries", [])
    keywords = topic.get("keywords", [])
    
    logic_templates = {
        "旅游": "假日经济效应显著，出行/文旅消费场景丰富，适合饮料、休闲食品品牌植入",
        "交通": "出行场景刚需，适合功能饮料、快消品牌场景营销",
        "美妆": "换季护肤/妆容需求旺盛，美妆品牌可借势种草推广",
        "健康": "健康意识提升，保健品/功能食品品牌可切入养生话题",
        "科技": "科技热点关注度高，数码品牌可借势产品推广",
        "娱乐": "娱乐话题热度高，适合饮料/零食品牌娱乐营销",
        "美食": "美食话题自带流量，食品饮料品牌可直接借势",
        "家居": "家居生活方式升级，家电/清洁品牌可切入场景",
        "宠物": "宠物经济持续升温，宠物食品品牌机会明显",
        "健身": "运动健身热潮，功能饮料/保健品品牌契合",
        "汽车": "汽车出行话题，新能源/科技品牌可借势",
        "电影": "档期票房效应，饮料/零食品牌观影场景营销",
        "教育": "教育话题社会关注度高，保健品/文具品牌可借势",
        "财经": "财经热点关注度强，适合品牌联名或话题营销",
        "国际": "国际话题引发讨论，适合科技品牌借势",
        "职场": "职场话题引发共鸣，保健品/个护品牌可切入",
    }
    
    for industry in industries:
        if industry in logic_templates:
            return logic_templates[industry]
    
    for kw in keywords:
        if kw in ["清明", "假期", "返程", "出行"]:
            return "假日出行高峰，适合饮料/快消品牌场景营销"
        if kw in ["春季", "换季", "护肤"]:
            return "换季护肤刚需，美妆个护品牌种草窗口"
        if kw in ["AI", "科技", "智能"]:
            return "科技热点关注度高，数码品牌可借势推广"
        if kw in ["游戏", "玩家"]:
            return "游戏热点热度高，电竞外设品牌机会明显"
    
    return "话题传播度广，可根据品牌调性选择借势角度"

def load_history():
    """加载历史数据用于趋势判断"""
    try:
        history_file = Path(__file__).parent / "hotspot_history.json"
        if history_file.exists():
            with open(history_file, "r", encoding="utf-8") as f:
                return json.load(f)
    except:
        pass
    return {}

def generate_trend(topic, history_data):
    """生成趋势标记"""
    title = topic.get("title", "")
    current_value = topic.get("heat", 0)
    trends = topic.get("trends", [])
    
    if title in history_data:
        prev_value = history_data[title].get("hot_value", 0)
        if current_value > prev_value * 1.2:
            return "🔥🔥🔥 持续上升"
        elif current_value > prev_value * 1.05:
            return "🔥🔥 稳定上升"
        elif current_value < prev_value * 0.8:
            return "📉 明显下降"
        elif current_value < prev_value * 0.95:
            return "🔥 下降"
        else:
            return "🔥🔥 稳定"
    
    if "爆" in trends:
        return "🔥🔥🔥 爆发式增长"
    if "新" in trends:
        return "🔥🔥🔥 新晋热点"
    if "热" in trends:
        return "🔥🔥🔥 持续上升"
    
    if current_value > 500000000:
        return "🔥🔥🔥 爆发式增长"
    elif current_value > 100000000:
        return "🔥🔥🔥 持续上升"
    else:
        return "🔥🔥 稳定"

def check_is_new(topic, history_data):
    """判断是否为新增热点"""
    title = topic.get("title", "")
    if title not in history_data:
        return True
    return False

# ============ 原有函数 ============

def get_related_clients(title, keywords):
    related = set()
    for kw, client_list in trend_client_map.items():
        if any(kw in title or kw in keywords for kw in [kw]):
            related.update(client_list)
    if not related:
        related = {"农夫山泉", "元气森林"}
    return list(related)[:3]

# 加载历史数据用于趋势判断
history_data = load_history()

# 生成热点（含完整字段）
new_hot_topics = []
for i, trend in enumerate(all_new_trends):
    hot_id = f"ht_202604041610_{i+1:03d}"
    related_clients = get_related_clients(trend["title"], trend["keywords"])
    
    # 生成完整字段
    platforms = parse_platforms(trend["platform"])
    heat_formatted = format_heat(trend["heat"])
    is_new = check_is_new(trend, history_data)
    logic = generate_logic(trend, related_clients)
    trend_mark = generate_trend(trend, history_data)
    
    new_hot_topics.append({
        "id": hot_id,
        "title": trend["title"],
        "hot_value": trend["heat"],
        "platform": trend["platform"],
        "platforms": platforms,  # 新增：数组格式
        "heat": heat_formatted,   # 新增：格式化热度
        "isNew": is_new,          # 新增：新增标记
        "logic": logic,           # 新增：逻辑分析
        "trend": trend_mark,      # 新增：趋势标记
        "industries": trend["industries"],
        "trends": ["热", "新"],
        "type": trend["type"],
        "sentiment": trend["sentiment"],
        "keywords": trend["keywords"],
        "c": related_clients,
        "created_at": now,
        "rank": i + 1,
        "category": trend["type"],
        "trend_tags": [f"#{kw}" for kw in trend["keywords"][:3]],
        "url": "https://weibo.com",
        "updated_at": now
    })

# 读取现有热点，保留近期的并更新
try:
    with open("hot_topics.json", "r", encoding="utf-8") as f:
        existing_topics = json.load(f)
except:
    existing_topics = []

# 更新旧热点的updated_at
for topic in existing_topics:
    if "updated_at" not in topic:
        topic["updated_at"] = now

# 合并新热点到现有，保持100条左右
updated_topics = new_hot_topics + existing_topics[:90]
updated_topics.sort(key=lambda x: x.get("hot_value", 0), reverse=True)
for i, t in enumerate(updated_topics[:100]):
    t["rank"] = i + 1

print(f"热点总数: {len(updated_topics)}")
print(f"新增热点: {len(new_hot_topics)}")

# ============ 生成新客户选题 ============
new_ideas = []
for i, client in enumerate(clients):
    brand = client["brand"]
    products = client["products"]
    
    # 为每个客户选取2-3个最相关的新热点
    relevant_trends = []
    for trend in all_new_trends:
        related = get_related_clients(trend["title"], trend["keywords"])
        if brand in related:
            relevant_trends.append(trend)
    
    # 如果没有特别相关的，随机选几个
    if not relevant_trends:
        import random
        relevant_trends = random.sample(all_new_trends, min(3, len(all_new_trends)))
    
    for j, trend in enumerate(relevant_trends[:4]):
        idea_id = f"{brand}_{now.replace(':', '').replace('-', '').replace(' ', 'T')}_{i*4+j+1:03d}"
        product = products[j % len(products)]
        angle = angles[j % len(angles)]
        
        new_ideas.append({
            "id": idea_id,
            "client": {
                "brand": brand,
                "industry": client["industry"],
                "products": products
            },
            "title": f"{brand}{trend['title'].split()[0] if trend['title'] else '今日'}{product}的{angle}",
            "platform": trend["platform"].split("/")[0] if "/" in trend["platform"] else trend["platform"],
            "angle": angle,
            "hot_topic": trend["title"],
            "hot_topic_id": new_hot_topics[all_new_trends.index(trend)]["id"] if trend in all_new_trends else "",
            "heat": "热",
            "trend": "新",
            "product": product,
            "keywords": trend["keywords"],
            "quality_score": round(0.80 + (i * j % 20) / 100, 2),
            "quality_level": "A级-优秀",
            "engagement_estimate": f"{int(50000 + i * j * 1000)}",
            "status": "pending",
            "created_at": now
        })

print(f"新增选题: {len(new_ideas)}")

# 保存热点
with open("hot_topics.json", "w", encoding="utf-8") as f:
    json.dump(updated_topics[:100], f, ensure_ascii=False, indent=2)

print("hot_topics.json 已更新")

# 更新历史数据
history_file = Path("hotspot_history.json")
try:
    existing_history = json.loads(history_file.read_text(encoding="utf-8")) if history_file.exists() else {}
except:
    existing_history = {}

# 追加当前热点到历史
for topic in updated_topics[:100]:
    history_key = topic.get("title", "")
    existing_history[history_key] = {
        "hot_value": topic.get("hot_value", 0),
        "platform": topic.get("platform", ""),
        "updated_at": now,
        "trend": topic.get("trend", "")
    }

# 只保留最近7天的热点历史（按updated_at清理）
import datetime as dt
seven_days_ago = (dt.datetime.now() - dt.timedelta(days=7)).isoformat()
cleaned_history = {
    k: v for k, v in existing_history.items()
    if v.get("updated_at", "") > seven_days_ago
}

with open("hotspot_history.json", "w", encoding="utf-8") as f:
    json.dump(cleaned_history, f, ensure_ascii=False, indent=2)
print(f"热点历史已更新（保留{len(cleaned_history)}条）")

# 读取并追加选题
try:
    with open("client_ideas.json", "r", encoding="utf-8") as f:
        existing_ideas = json.load(f)
except:
    existing_ideas = []

all_ideas = new_ideas + existing_ideas
print(f"选题总数: {len(all_ideas)}")

with open("client_ideas.json", "w", encoding="utf-8") as f:
    json.dump(all_ideas, f, ensure_ascii=False, indent=2)

print("client_ideas.json 已更新")
print("更新完成!")
