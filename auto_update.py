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
ANGLES = [
    "产品测评", "使用教程", "热点借势", "痛点解决", "场景展示", "对比评测", "开箱体验", "种草推荐",
    "剧情植入", "挑战赛", "测评对比", "教程攻略", "Vlog日常", "知识科普", "情感故事"
]

# 热点数据 - 模拟实时数据（实际应从API获取）
def get_hot_topics():
    """获取热点数据"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 模拟热点数据 - 扩展到30条，覆盖8大类别
    # 字段: title, platform, heat, trend, type(类别), aud(受众), time(热度持续时间), logic(热度逻辑), link, c(客户列表)
    hot_topics = [
        # 科技类 (5条)
        {"title": "AI大模型应用潮", "platform": "微博", "heat": f"{random.randint(1500,3000)}万", "trend": "🔥🔥🔥 爆发式增长", "type": "科技", "aud": "18-35岁科技爱好者", "time": "持续3周", "logic": "技术突破引发全民讨论", "link": "https://weibo.com/hot/ai", "c": ["荣耀", "罗技"]},
        {"title": "折叠屏手机新风向", "platform": "抖音", "heat": f"{random.randint(800,1500)}万", "trend": "🔥🔥🔥 持续上升", "type": "科技", "aud": "数码发烧友、商务人群", "time": "持续2周", "logic": "新品发布带动关注", "link": "https://douyin.com/hot/foldphone", "c": ["荣耀"]},
        {"title": "智能穿戴健康监测", "platform": "小红书", "heat": f"{random.randint(500,1000)}万", "trend": "🔥🔥 稳定上升", "type": "科技", "aud": "健康意识强的人群", "time": "持续4周", "logic": "健康管理成刚需", "link": "https://xiaohongshu.com/hot/smartwearable", "c": ["荣耀"]},
        {"title": "Switch2游戏机发布", "platform": "B站", "heat": f"{random.randint(1000,2000)}万", "trend": "🔥🔥🔥 爆发式增长", "type": "科技", "aud": "游戏玩家、主机用户", "time": "持续3周", "logic": "新品发布+情怀营销", "link": "https://bilibili.com/hot/switch2", "c": ["罗技"]},
        {"title": "国产芯片突破", "platform": "微博", "heat": f"{random.randint(2000,5000)}万", "trend": "🔥🔥🔥 爆发式增长", "type": "科技", "aud": "全年龄段科技关注者", "time": "持续4周", "logic": "国产替代热度持续", "link": "https://weibo.com/hot/chipse突破", "c": ["荣耀"]},
        
        # 美妆类 (4条)
        {"title": "春季护肤routine", "platform": "小红书", "heat": f"{random.randint(3,6)}亿浏览", "trend": "🔥🔥🔥 爆发式增长", "type": "美妆", "aud": "18-35岁女性", "time": "季节性持续2月", "logic": "换季护肤刚需", "link": "https://xiaohongshu.com/hot/spring-skincare", "c": ["AHC", "多芬", "力士"]},
        {"title": "早C晚A护肤法", "platform": "小红书", "heat": f"{random.randint(1,3)}亿浏览", "trend": "🔥🔥🔥 持续上升", "type": "美妆", "aud": "25-40岁护肤进阶用户", "time": "持续6周", "logic": "成分党护肤理念传播", "link": "https://xiaohongshu.com/hot/caca", "c": ["AHC"]},
        {"title": "平价替代彩妆推荐", "platform": "抖音", "heat": f"{random.randint(800,1500)}万", "trend": "🔥🔥 稳定上升", "type": "美妆", "aud": "学生党、性价比追求者", "time": "持续5周", "logic": "消费降级趋势", "link": "https://douyin.com/hot/budget-makeup", "c": ["AHC", "多芬"]},
        {"title": "母亲节礼盒选购", "platform": "微博", "heat": f"{random.randint(1000,2000)}万", "trend": "🔥🔥🔥 持续上升", "type": "美妆", "aud": "送礼人群", "time": "节日前2周爆发", "logic": "节日营销+情感共鸣", "link": "https://weibo.com/hot/mothersday", "c": ["AHC", "多芬", "力士"]},
        
        # 母婴类 (3条)
        {"title": "宝宝辅食制作教程", "platform": "小红书", "heat": f"{random.randint(1,2)}亿浏览", "trend": "🔥🔥 稳定上升", "type": "母婴", "aud": "0-3岁宝宝妈妈", "time": "持续8周", "logic": "育儿刚需内容", "link": "https://xiaohongshu.com/hot/babyfood", "c": ["汤臣倍健"]},
        {"title": "儿童护眼指南", "platform": "抖音", "heat": f"{random.randint(600,1200)}万", "trend": "🔥🔥🔥 持续上升", "type": "母婴", "aud": "3-12岁儿童家长", "time": "持续6周", "logic": "近视防控意识提升", "link": "https://douyin.com/hot/child-eye", "c": ["汤臣倍健"]},
        {"title": "产后修复塑形", "platform": "小红书", "heat": f"{random.randint(800,1500)}万", "trend": "🔥🔥 稳定上升", "type": "母婴", "aud": "产后妈妈", "time": "持续7周", "logic": "辣妈经济", "link": "https://xiaohongshu.com/hot/postpartum", "c": ["汤臣倍健"]},
        
        # 健身类 (4条)
        {"title": "居家燃脂训练", "platform": "抖音", "heat": f"{random.randint(2000,5000)}万", "trend": "🔥🔥🔥 爆发式增长", "type": "健身", "aud": "20-45岁健身人群", "time": "全年持续", "logic": "健身意识全民化", "link": "https://douyin.com/hot/home-workout", "c": ["汤臣倍健", "清扬"]},
        {"title": "减脂餐搭配", "platform": "小红书", "heat": f"{random.randint(1,3)}亿浏览", "trend": "🔥🔥🔥 持续上升", "type": "健身", "aud": "减肥人群、健身爱好者", "time": "持续10周", "logic": "健康饮食趋势", "link": "https://xiaohongshu.com/hot/diet-meal", "c": ["汤臣倍健", "OATLY"]},
        {"title": "健身房打卡vlog", "platform": "B站", "heat": f"{random.randint(500,1000)}万", "trend": "🔥🔥 稳定上升", "type": "健身", "aud": "健身爱好者", "time": "持续8周", "logic": "社交健身潮流", "link": "https://bilibili.com/hot/gym-vlog", "c": ["清扬"]},
        {"title": "拉伸放松技巧", "platform": "抖音", "heat": f"{random.randint(300,800)}万", "trend": "🔥🔥 持续上升", "type": "健身", "aud": "久坐人群、运动后人群", "time": "持续6周", "logic": "运动恢复需求增加", "link": "https://douyin.com/hot/stretching", "c": ["汤臣倍健"]},
        
        # 美食类 (4条)
        {"title": "春日野餐食谱", "platform": "小红书", "heat": f"{random.randint(2,5)}亿浏览", "trend": "🔥🔥🔥 爆发式增长", "type": "美食", "aud": "年轻人、家庭用户", "time": "季节性持续1月", "logic": "春季户外活动增加", "link": "https://xiaohongshu.com/hot/picnic-food", "c": ["OATLY", "百威"]},
        {"title": "咖啡探店指南", "platform": "小红书", "heat": f"{random.randint(1,3)}亿浏览", "trend": "🔥🔥🔥 持续上升", "type": "美食", "aud": "咖啡爱好者", "time": "全年持续", "logic": "咖啡文化普及", "link": "https://xiaohongshu.com/hot/coffee", "c": ["OATLY"]},
        {"title": "啤酒搭配美食", "platform": "微博", "heat": f"{random.randint(500,1000)}万", "trend": "🔥🔥 稳定上升", "type": "美食", "aud": "年轻男性、美食爱好者", "time": "持续4周", "logic": "夜经济消费复苏", "link": "https://weibo.com/hot/beer-food", "c": ["百威"]},
        {"title": "预制菜测评", "platform": "抖音", "heat": f"{random.randint(800,1500)}万", "trend": "🔥🔥 持续上升", "type": "美食", "aud": "上班族、年轻家庭", "time": "持续8周", "logic": "懒人经济+便捷需求", "link": "https://douyin.com/hot/premade-food", "c": ["百威"]},
        
        # 旅游类 (3条)
        {"title": "春季赏花目的地", "platform": "小红书", "heat": f"{random.randint(3,8)}亿浏览", "trend": "🔥🔥🔥 爆发式增长", "type": "旅游", "aud": "旅游爱好者、家庭", "time": "季节性2月", "logic": "春游季节+打卡文化", "link": "https://xiaohongshu.com/hot/spring-flower", "c": ["希宝"]},
        {"title": "周末周边游攻略", "platform": "抖音", "heat": f"{random.randint(1000,3000)}万", "trend": "🔥🔥🔥 持续上升", "type": "旅游", "aud": "上班族、短途游爱好者", "time": "全年持续", "logic": "微度假概念兴起", "link": "https://douyin.com/hot/weekend-travel", "c": ["希宝"]},
        {"title": "宠物友好景区推荐", "platform": "小红书", "heat": f"{random.randint(500,1000)}万", "trend": "🔥🔥 稳定上升", "type": "旅游", "aud": "宠物主", "time": "持续10周", "logic": "携宠出行需求增加", "link": "https://xiaohongshu.com/hot/pet-travel", "c": ["希宝"]},
        
        # 教育类 (3条)
        {"title": "AI办公效率课", "platform": "B站", "heat": f"{random.randint(800,2000)}万", "trend": "🔥🔥🔥 爆发式增长", "type": "教育", "aud": "职场人士、学生", "time": "持续6周", "logic": "AI技能焦虑+学习需求", "link": "https://bilibili.com/hot/ai-office", "c": ["罗技"]},
        {"title": "考研考公备考指南", "platform": "微博", "heat": f"{random.randint(1000,3000)}万", "trend": "🔥🔥🔥 持续上升", "type": "教育", "aud": "大学生、待业人群", "time": "考试季集中", "logic": "就业压力传导", "link": "https://weibo.com/hot/exam", "c": ["罗技"]},
        {"title": "亲子阅读时光", "platform": "小红书", "heat": f"{random.randint(500,1000)}万", "trend": "🔥🔥 稳定上升", "type": "教育", "aud": "3-10岁儿童家长", "time": "持续12周", "logic": "素质教育重视", "link": "https://xiaohongshu.com/hot/parenting-reading", "c": ["汤臣倍健"]},
        
        # 汽车类 (2条)
        {"title": "新能源汽车选购", "platform": "微博", "heat": f"{random.randint(1000,3000)}万", "trend": "🔥🔥🔥 持续上升", "type": "汽车", "aud": "准购车人群", "time": "持续8周", "logic": "新能源渗透率提升", "link": "https://weibo.com/hot/ev-car", "c": ["荣耀"]},
        {"title": "车载好物分享", "platform": "小红书", "heat": f"{random.randint(300,800)}万", "trend": "🔥🔥 稳定上升", "type": "汽车", "aud": "有车一族", "time": "持续10周", "logic": "车内生活品质追求", "link": "https://xiaohongshu.com/hot/car-gadgets", "c": ["HC"]},
        
        # 原有热点保留并扩展字段 (2条补充)
        {"title": "春季护肤攻略", "platform": "小红书", "heat": f"{random.randint(3,6)}亿浏览", "trend": "🔥🔥🔥 爆发式增长", "type": "美妆", "aud": "18-35岁女性", "time": "换季持续1月", "logic": "换季护肤刚需", "link": "https://xiaohongshu.com/hot/spring-skincare", "c": ["AHC", "多芬", "力士"]},
        {"title": "宠物日常vlog", "platform": "小红书", "heat": f"{random.randint(1,2)}亿浏览", "trend": "🔥🔥 持续上升", "type": "宠物", "aud": "宠物爱好者", "time": "全年持续", "logic": "云吸宠物文化", "link": "https://xiaohongshu.com/hot/pet-vlog", "c": ["希宝"]},
    ]
    return hot_topics

def generate_client_ideas(client, hot_topics):
    """为单个客户生成选题"""
    ideas = []
    today = datetime.now().strftime("%Y%m%d")
    
    # 每个客户生成20-25个选题
    num_ideas = random.randint(20, 25)
    
    # 用于去重的标题集合
    used_titles = set()
    
    for i in range(num_ideas):
        hot_topic = random.choice(hot_topics)
        angle = random.choice(ANGLES)
        platform = random.choice(PLATFORMS)
        product = random.choice(client["products"])
        
        # 生成多样化的标题模板
        title_templates = [
            f"《{hot_topic['title']}？{product}真实测评》",
            f"《{hot_topic['title']}！{client['brand']}产品使用心得》",
            f"《借势{hot_topic['title']}，{product}这样用超赞》",
            f"《{hot_topic['title']}火了，{client['brand']}也有话说》",
            f"《从{hot_topic['title']}看{product}的正确打开方式》",
            # 新增标题模板 - 剧情植入
            f"《{hot_topic['title']}×{product}剧情向，结局反转太惊喜》",
            f"《当{hot_topic['title']}遇上{client['brand']}，这剧情绝了》",
            # 新增标题模板 - 挑战赛
            f"《{hot_topic['title']}挑战赛！{product}实测能否通关》",
            f"《接受{hot_topic['title']}挑战，{client['brand']}产品表现如何》",
            # 新增标题模板 - 测评对比
            f"《{product}vs竞品深度对比，{hot_topic['title']}谁更强》",
            f"《{hot_topic['title']}横评：{client['brand']}产品凭什么出圈》",
            # 新增标题模板 - 教程攻略
            f"《{hot_topic['title']}完全攻略！{product}正确用法详解》",
            f"《手把手教你{hot_topic['title']}，{client['brand']}产品必备技巧》",
            # 新增标题模板 - Vlog日常
            f"《{hot_topic['title']}Vlog｜用{product}的日常有多爽》",
            f"《记录{hot_topic['title']}的一天，{client['brand']}全程陪伴》",
            # 新增标题模板 - 知识科普
            f"《科普贴：{hot_topic['title']}背后的{product}黑科技》",
            f"《关于{hot_topic['title']}，{client['brand']}产品告诉你的真相》",
            # 新增标题模板 - 情感故事
            f"《{hot_topic['title']}里的温情时刻，{product}见证感动》",
            f"《我和{client['brand']}的故事：从{hot_topic['title']}说起》",
            # 更多创意标题
            f"《揭秘{hot_topic['title']}，{product}的隐藏功能大公开》",
            f"《{hot_topic['title']}必入清单，{client['brand']}产品上榜理由》",
            f"《避坑指南：{hot_topic['title']}选{product}就对了》",
            f"《{hot_topic['title']}测评官：{client['brand']}产品真实体验》",
        ]
        
        # 确保标题不重复
        title = random.choice(title_templates)
        retry_count = 0
        while title in used_titles and retry_count < 10:
            title = random.choice(title_templates)
            retry_count += 1
        
        used_titles.add(title)
        
        idea = {
            "id": f"{client['industry']}_{today}{random.randint(1000,9999)}",
            "client": {
                "industry": client["industry"],
                "brand": client["brand"],
                "products": client["products"],
                "priority": client["priority"]
            },
            "title": title,
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
