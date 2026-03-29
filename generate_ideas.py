import json
from datetime import datetime

# 读取热点
with open('hot_topics.json', 'r', encoding='utf-8') as f:
    hot_topics = json.load(f)

# 读取现有选题
with open('client_ideas.json', 'r', encoding='utf-8') as f:
    client_ideas = json.load(f)

# 客户列表
clients = [
    {"brand": "荣耀", "industry": "3C数码", "products": ["荣耀手机", "荣耀平板", "荣耀手表", "荣耀折叠屏"]},
    {"brand": "罗技", "industry": "3C数码", "products": ["罗技鼠标", "罗技键盘", "罗技耳机"]},
    {"brand": "小米", "industry": "3C数码", "products": ["小米手机", "小米平板", "小米手环", "小米智能家居"]},
    {"brand": "索尼", "industry": "3C数码", "products": ["索尼相机", "索尼耳机", "索尼游戏机"]},
    {"brand": "AHC", "industry": "美妆", "products": ["AHC面膜", "AHC精华", "AHC眼霜"]},
    {"brand": "多芬", "industry": "护肤", "products": ["多芬洗面奶", "多芬护肤霜", "多芬沐浴露"]},
    {"brand": "力士", "industry": "护肤", "products": ["力士香皂", "力士沐浴露", "力士护肤品"]},
    {"brand": "清扬", "industry": "护肤", "products": ["清扬洗发水", "清扬护发素", "清扬头皮护理"]},
    {"brand": "玉兰油", "industry": "美妆", "products": ["玉兰油面霜", "玉兰油精油", "玉兰油眼霜"]},
    {"brand": "汤臣倍健", "industry": "保健", "products": ["汤臣倍健维生素", "汤臣倍健钙片", "汤臣倍健蛋白粉"]},
    {"brand": "善存", "industry": "保健", "products": ["善存维生素", "善存矿物质", "善存复合营养"]},
    {"brand": "HC", "industry": "护肤", "products": ["HC面膜", "HC精华液", "HC护肤套装"]},
    {"brand": "威猛先生", "industry": "清洁", "products": ["威猛先生清洁剂", "威猛先生消毒液", "威猛先生洗涤剂"]},
    {"brand": "舒适", "industry": "日用", "products": ["舒适纸巾", "舒适卷纸", "舒适湿巾"]},
    {"brand": "希宝", "industry": "母婴", "products": ["希宝奶粉", "希宝纸尿裤", "希宝婴儿护肤"]},
    {"brand": "皇家", "industry": "宠物", "products": ["皇家狗粮", "皇家猫粮", "皇家宠物零食"]},
    {"brand": "OATLY", "industry": "食品", "products": ["OATLY燕麦奶", "OATLY冰淇淋", "OATLY酸奶"]},
    {"brand": "百威", "industry": "饮品", "products": ["百威啤酒", "百威无醇啤酒", "百威精酿"]},
    {"brand": "元气森林", "industry": "饮品", "products": ["元气森林气泡水", "元气森林茶饮", "元气森林果汁"]},
    {"brand": "农夫山泉", "industry": "饮品", "products": ["农夫山泉矿泉水", "农夫山泉茶饮", "农夫山泉果汁"]}
]

# 角度类型
angles = ["创意借势", "趋势分析", "生活方式", "用户故事", "科技科普", "情感共鸣", "产品评测", "场景种草"]

# 生成新选题
new_ideas = []
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

# 从最新热点中选取前6个为每个客户生成选题
top_hotspots = hot_topics[:6]

for client in clients:
    for i, hotspot in enumerate(top_hotspots[:3]):  # 每个客户生成3个选题
        angle = angles[i % len(angles)]
        product = client['products'][i % len(client['products'])]
        
        idea = {
            "id": f"{client['brand']}_{timestamp}_{i+1}",
            "client": client,
            "title": f"《{angle}视角：{product}如何借势{hotspot['title'][:15]}...》",
            "platform": "全平台",
            "angle": angle,
            "hot_topic": hotspot['title'],
            "heat": hotspot['heat'],
            "trend": hotspot['trend'],
            "product": product,
            "engagement_estimate": f"{35000 + (i * 5000)}+",
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        new_ideas.append(idea)

# 添加到开头
client_ideas = new_ideas + client_ideas

# 限制总数
client_ideas = client_ideas[:200]

# 保存
with open('client_ideas.json', 'w', encoding='utf-8') as f:
    json.dump(client_ideas, f, ensure_ascii=False, indent=2)

print(f"选题更新完成，共{len(client_ideas)}条，新增{len(new_ideas)}条")
