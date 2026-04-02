import json
import random
import string
from datetime import datetime

# 读取热点数据
with open('hot_topics.json', 'r', encoding='utf-8') as f:
    hot_topics = json.load(f)

# 读取现有选题
with open('client_ideas.json', 'r', encoding='utf-8') as f:
    client_ideas = json.load(f)

# 客户配置
clients_config = {
    "荣耀": {"industry": "3C数码", "products": ["荣耀手机", "荣耀平板", "荣耀手表", "荣耀折叠屏"]},
    "罗技": {"industry": "3C数码", "products": ["罗技鼠标", "罗技键盘", "罗技耳机", "罗技游戏手柄"]},
    "小米": {"industry": "3C数码", "products": ["小米手机", "小米平板", "小米手环", "小米智能家居"]},
    "索尼": {"industry": "3C数码", "products": ["索尼相机", "索尼耳机", "索尼游戏机", "索尼电视"]},
    "AHC": {"industry": "美妆", "products": ["AHC面膜", "AHC精华", "AHC眼霜", "AHC防晒霜"]},
    "多芬": {"industry": "护肤", "products": ["多芬洗面奶", "多芬沐浴露", "多芬洗发水", "多芬身体乳"]},
    "力士": {"industry": "护肤", "products": ["力士香皂", "力士沐浴露", "力士洗发水", "力士护发素"]},
    "清扬": {"industry": "护肤", "products": ["清扬洗发水", "清扬护发素", "清扬去屑洗发水", "清扬控油洗发水"]},
    "玉兰油": {"industry": "美妆", "products": ["玉兰油面霜", "玉兰油精华", "玉兰油眼霜", "玉兰油防晒"]},
    "汤臣倍健": {"industry": "保健", "products": ["汤臣倍健维生素", "汤臣倍健钙片", "汤臣倍健蛋白粉", "汤臣倍健鱼油"]},
    "善存": {"industry": "保健", "products": ["善存维生素", "善存矿物质", "善存复合营养", "善存钙片"]},
    "HC": {"industry": "护肤", "products": ["HC面膜", "HC精华液", "HC护肤套装", "HC眼霜"]},
    "威猛先生": {"industry": "清洁", "products": ["威猛先生清洁剂", "威猛先生消毒液", "威猛先生洁厕灵", "威猛先生厨房清洁"]},
    "舒适": {"industry": "日用", "products": ["舒适纸巾", "舒适卷纸", "舒适湿巾", "舒适抽纸"]},
    "希宝": {"industry": "母婴", "products": ["希宝奶粉", "希宝纸尿裤", "希宝婴儿护肤", "希宝辅食"]},
    "皇家": {"industry": "宠物", "products": ["皇家狗粮", "皇家猫粮", "皇家宠物零食", "皇家宠物营养品"]},
    "OATLY": {"industry": "食品", "products": ["OATLY燕麦奶", "OATLY冰淇淋", "OATLY酸奶", "OATLY咖啡伴侣"]},
    "百威": {"industry": "酒饮", "products": ["百威啤酒", "百威精酿", "百威无醇", "百威果啤"]},
    "元气森林": {"industry": "饮料", "products": ["元气森林气泡水", "元气森林燃茶", "元气森林外星人", "元气森林有矿"]},
    "农夫山泉": {"industry": "饮料", "products": ["农夫山泉矿泉水", "农夫山泉茶π", "农夫山泉尖叫", "农夫山泉NFC"]}
}

# 平台和角度选项
platforms = ["微博", "小红书", "抖音", "B站"]
angles = ["创意借势", "趋势分析", "生活方式", "场景种草", "情感共鸣"]

# 获取前10个热点
top_hotspots = hot_topics[:10]

def gen_id():
    return ''.join(random.choices(string.hexdigits.lower(), k=8))

now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

# 为每个客户生成新选题
new_ideas = []
for client_name, config in clients_config.items():
    # 选择与客户相关的热点
    relevant_hotspots = [ht for ht in top_hotspots if any(c in ht.get('c', []) or ht.get('c', []) == [] for c in [client_name])]
    if not relevant_hotspots:
        relevant_hotspots = top_hotspots[:3]  # 默认选前3个
    
    # 为每个客户生成3-5条选题
    num_ideas = random.randint(3, 5)
    for i in range(num_ideas):
        hotspot = random.choice(relevant_hotspots)
        product = random.choice(config['products'])
        platform = random.choice(platforms)
        angle = random.choice(angles)
        
        idea = {
            "id": f"{client_name}_{gen_id()}",
            "client": {
                "brand": client_name,
                "industry": config['industry'],
                "products": config['products']
            },
            "title": f"《{product}借势{hotspot['title'][:15]}的{angle}玩法》",
            "platform": platform,
            "angle": angle,
            "hot_topic": hotspot['title'],
            "hot_topic_id": hotspot['id'],
            "heat": "热搜前十" if hotspot['rank'] <= 10 else "高热",
            "trend": hotspot['trends'][0] if hotspot.get('trends') else "热",
            "product": product,
            "keywords": hotspot.get('keywords', [])[:5],
            "quality_score": round(random.uniform(0.65, 0.85), 3),
            "quality_level": "B级-良好",
            "engagement_estimate": f"{random.randint(15000, 60000)}+",
            "status": "pending",
            "created_at": now
        }
        new_ideas.append(idea)

# 合并到现有选题（保留最近的）
all_ideas = new_ideas + client_ideas
# 按时间排序，保留最新的100条
all_ideas = sorted(all_ideas, key=lambda x: x.get('created_at', ''), reverse=True)[:100]

# 保存
with open('client_ideas.json', 'w', encoding='utf-8') as f:
    json.dump(all_ideas, f, ensure_ascii=False, indent=2)

print(f"更新完成，共 {len(all_ideas)} 条选题，新增 {len(new_ideas)} 条")
