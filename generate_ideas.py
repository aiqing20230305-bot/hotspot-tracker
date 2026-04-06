#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, hashlib, datetime
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

clients = [
    {"brand": "荣耀", "industry": "3C数码", "products": ["荣耀手机","荣耀平板","荣耀手表","荣耀折叠屏","荣耀笔记本","荣耀耳机","荣耀智慧屏"]},
    {"brand": "罗技", "industry": "3C数码", "products": ["罗技鼠标","罗技键盘","罗技耳机","罗技摄像头","罗技游戏手柄","罗技音箱","罗技会议设备"]},
    {"brand": "小米", "industry": "3C数码", "products": ["小米手机","小米平板","小米手环","小米智能家居","小米电视","小米路由器","小米充电器","小米耳机"]},
    {"brand": "索尼", "industry": "3C数码", "products": ["索尼相机","索尼耳机","索尼游戏机","索尼电视","索尼手机","索尼音箱","索尼播放器"]},
    {"brand": "AHC", "industry": "美妆", "products": ["AHC面膜","AHC精华","AHC眼霜","AHC防晒霜","AHC水乳","AHC面霜","AHC卸妆水"]},
    {"brand": "多芬", "industry": "护肤", "products": ["多芬洗面奶","多芬护肤霜","多芬沐浴露","多芬身体乳","多芬洗发水","多芬护发素","多芬香皂"]},
    {"brand": "力士", "industry": "护肤", "products": ["力士香皂","力士沐浴露","力士洗发水","力士护发素","力士身体乳","力士香氛"]},
    {"brand": "清扬", "industry": "护肤", "products": ["清扬洗发水","清扬护发素","清扬头皮护理","清扬去屑洗发水","清扬控油洗发水"]},
    {"brand": "玉兰油", "industry": "美妆", "products": ["玉兰油面霜","玉兰油精油","玉兰油眼霜","玉兰油精华","玉兰油防晒","玉兰油面膜"]},
    {"brand": "汤臣倍健", "industry": "保健", "products": ["汤臣倍健维生素","汤臣倍健钙片","汤臣倍健蛋白粉","汤臣倍健鱼油","汤臣倍健益生菌"]},
    {"brand": "善存", "industry": "保健", "products": ["善存维生素","善存矿物质","善存复合营养","善存钙片","善存锌片"]},
    {"brand": "HC", "industry": "护肤", "products": ["HC面膜","HC精华液","HC护肤套装","HC眼霜","HC面霜"]},
    {"brand": "威猛先生", "industry": "清洁", "products": ["威猛先生清洁剂","威猛先生消毒液","威猛先生洗涤剂","威猛先生洁厕灵","威猛先生厨房清洁"]},
    {"brand": "舒适", "industry": "日用", "products": ["舒适纸巾","舒适卷纸","舒适湿巾","舒适抽纸","舒适手帕纸"]},
    {"brand": "希宝", "industry": "母婴", "products": ["希宝奶粉","希宝纸尿裤","希宝婴儿护肤","希宝辅食","希宝湿巾"]},
    {"brand": "皇家", "industry": "宠物", "products": ["皇家狗粮","皇家猫粮","皇家宠物零食","皇家宠物营养品"]},
    {"brand": "OATLY", "industry": "食品", "products": ["OATLY燕麦奶","OATLY冰淇淋","OATLY酸奶","OATLY咖啡伴侣"]},
    {"brand": "百威", "industry": "食品", "products": ["百威啤酒","百威金樽","百威纯生","百威果味酒","百威精酿"]},
    {"brand": "元气森林", "industry": "食品", "products": ["元气森林气泡水","元气森林外星人电解质水","元气森林满分气泡水","元气森林满分果汁","元气森林燃茶"]},
    {"brand": "农夫山泉", "industry": "食品", "products": ["农夫山泉矿泉水","农夫山泉茶饮","农夫山泉果汁","农夫山泉NFC","农夫山泉运动饮料"]}
]

hot_topics = [
    {"title": "清明假期后首个工作日 打工人节后综合症引热议", "keywords": ["节后","打工人","综合症","假期","周一"], "type": "社会热点"},
    {"title": "小米SU7 Ultra发布 雷军宣布百万交付目标", "keywords": ["小米","SU7","Ultra","雷军","交付"], "type": "汽车热点"},
    {"title": "GPT-5发布倒计时 AI智能体应用全面爆发", "keywords": ["GPT-5","AI","智能体","人工智能","科技"], "type": "科技热点"},
    {"title": "春季花粉过敏高峰来袭 抗敏产品搜索量激增", "keywords": ["过敏","花粉","春季","抗敏","健康"], "type": "大健康热点"},
    {"title": "低糖饮食成新趋势 代糖产品市场爆发", "keywords": ["低糖","代糖","健康","饮食","控糖"], "type": "美食热点"}
]

angles = ["创意借势", "情感共鸣", "趋势分析", "科普种草", "场景植入"]
now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

ideas = []
for client in clients:
    for topic_idx, topic in enumerate(hot_topics):
        product = client["products"][topic_idx % len(client["products"])]
        angle = angles[topic_idx % len(angles)]
        uid = hashlib.md5(f"{client['brand']}_{product}_{topic['title']}_{angle}".encode()).hexdigest()[:8]
        idea_id = f"{client['brand']}_20260406{now}_{uid}"
        
        if angle == "创意借势":
            title = f"{product}借势「{topic['title'][:20]}」的创意营销方案"
        elif angle == "情感共鸣":
            title = f"从「{topic['title'][:15]}」看{product}如何传递品牌温度"
        elif angle == "趋势分析":
            title = f"「{topic['title'][:20]}」趋势下{product}的市场机遇分析"
        elif angle == "科普种草":
            title = f"结合「{topic['title'][:15]}」热度，{product}科普种草内容方案"
        else:
            title = f"「{topic['title'][:15]}」场景下{product}的自然植入策略"
        
        platform = "小红书" if client["industry"] in ["美妆","护肤","保健","日用","母婴","宠物","食品","清洁"] else "B站"
        
        ideas.append({
            "id": idea_id,
            "client": client,
            "title": title,
            "platform": platform,
            "angle": angle,
            "hot_topic": topic["title"],
            "heat": "热搜前列",
            "trend": "🔥🔥 快速上升",
            "product": product,
            "keywords": topic["keywords"],
            "quality_score": round(0.75 + (topic_idx * 0.05), 3),
            "quality_level": "A级-优质" if topic_idx < 2 else "B级-良好",
            "engagement_estimate": f"{50000 + abs(hash(product)) % 30000}+",
            "status": "pending",
            "created_at": datetime.datetime.now().isoformat(),
            "profile_tags": {"tone": "专业", "target": "目标用户", "selling_points": ["品质", "创新"]}
        })

with open("client_ideas.json", "w", encoding="utf-8") as f:
    json.dump(ideas, f, ensure_ascii=False, indent=2)

print(f"Generated {len(ideas)} ideas for {len(clients)} clients")
