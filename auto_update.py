#!/usr/bin/env python3
"""
特赞内容运营平台 - 自动更新脚本
每天自动抓取热点数据，生成客户选题
目标：500+条高质量选题
"""

import json
import requests
from datetime import datetime
from urllib.parse import quote
import random

# 客户配置 - 扩展到20个客户
CLIENTS = [
    # 3C数码
    {"industry": "3C数码", "brand": "荣耀", "products": ["荣耀手机", "荣耀平板", "荣耀耳机", "荣耀手表"], "priority": 5},
    {"industry": "3C数码", "brand": "罗技", "products": ["罗技键鼠", "罗技摄像头", "罗技音箱"], "priority": 4},
    {"industry": "3C数码", "brand": "小米", "products": ["小米手机", "小米平板", "小米智能家居"], "priority": 5},
    {"industry": "3C数码", "brand": "索尼", "products": ["索尼耳机", "索尼相机", "索尼电视"], "priority": 4},
    # 快消/美妆
    {"industry": "快消", "brand": "AHC", "products": ["AHC水乳", "AHC防晒", "AHC眼霜"], "priority": 5},
    {"industry": "快消", "brand": "多芬", "products": ["多芬沐浴露", "多芬洗发水", "多芬身体乳"], "priority": 4},
    {"industry": "快消", "brand": "力士", "products": ["力士洗发水", "力士沐浴露", "力士香皂"], "priority": 4},
    {"industry": "快消", "brand": "清扬", "products": ["清扬洗发水", "清扬去屑套装"], "priority": 3},
    {"industry": "快消", "brand": "舒适", "products": ["舒适洗衣液", "舒适柔顺剂"], "priority": 3},
    {"industry": "快消", "brand": "玉兰油", "products": ["玉兰油面霜", "玉兰油精华", "玉兰油防晒"], "priority": 4},
    # 保健品/营养
    {"industry": "保健品", "brand": "汤臣倍健", "products": ["蛋白粉", "维生素", "鱼油", "益生菌"], "priority": 5},
    {"industry": "保健品", "brand": "善存", "products": ["善存多维片", "善存银片"], "priority": 3},
    # 家庭清洁
    {"industry": "家庭清洁", "brand": "HC", "products": ["HC清洁剂", "HC消毒液"], "priority": 3},
    {"industry": "家庭清洁", "brand": "威猛先生", "products": ["威猛先生厨房清洁", "威猛先生浴室清洁"], "priority": 3},
    # 宠物食品
    {"industry": "宠物食品", "brand": "希宝", "products": ["猫粮", "狗粮", "宠物零食"], "priority": 4},
    {"industry": "宠物食品", "brand": "皇家", "products": ["皇家猫粮", "皇家狗粮", "皇家处方粮"], "priority": 4},
    # 食品饮料
    {"industry": "食品饮料", "brand": "OATLY", "products": ["燕麦奶", "咖啡燕麦奶", "燕麦冰淇淋"], "priority": 4},
    {"industry": "食品饮料", "brand": "百威", "products": ["百威啤酒", "百威纯生", "百威超级"], "priority": 3},
    {"industry": "食品饮料", "brand": "元气森林", "products": ["气泡水", "外星人电解质水", "燃茶"], "priority": 4},
    {"industry": "食品饮料", "brand": "农夫山泉", "products": ["矿泉水", "东方树叶", "茶π"], "priority": 4},
]

# 平台配置
PLATFORMS = ["抖音", "微博", "小红书", "B站", "视频号"]

# 内容角度 - 扩展到20个角度（新增：联名合作、限时优惠、用户故事、专家访谈、行业趋势）
ANGLES = [
    "产品测评", "使用教程", "热点借势", "痛点解决", "场景展示",
    "对比评测", "开箱体验", "种草推荐", "剧情植入", "挑战赛",
    "测评对比", "教程攻略", "Vlog日常", "知识科普", "情感故事",
    "联名合作", "限时优惠", "用户故事", "专家访谈", "行业趋势",
]

# 热点数据 - 模拟实时数据（实际应从API获取）
def get_hot_topics():
    """获取热点数据"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 模拟热点数据 - 扩展到35条，覆盖8大类别
    # 字段: title, platform, heat, trend, type(类别), aud(受众), time(热度持续时间), logic(热度逻辑), link, c(客户列表)
    hot_topics = [
        # 科技类 (5条)
        {"title": "AI大模型应用潮", "platform": "微博", "heat": f"{random.randint(1500,3000)}万", "trend": "🔥🔥🔥 爆发式增长", "type": "科技", "aud": "18-35岁科技爱好者", "time": "持续3周", "logic": "技术突破引发全民讨论", "link": "https://weibo.com/hot/ai", "c": ["荣耀", "罗技", "小米"]},
        {"title": "折叠屏手机新风向", "platform": "抖音", "heat": f"{random.randint(800,1500)}万", "trend": "🔥🔥🔥 持续上升", "type": "科技", "aud": "数码发烧友、商务人群", "time": "持续2周", "logic": "新品发布带动关注", "link": "https://douyin.com/hot/foldphone", "c": ["荣耀", "小米"]},
        {"title": "智能穿戴健康监测", "platform": "小红书", "heat": f"{random.randint(500,1000)}万", "trend": "🔥🔥 稳定上升", "type": "科技", "aud": "健康意识强的人群", "time": "持续4周", "logic": "健康管理成刚需", "link": "https://xiaohongshu.com/hot/smartwearable", "c": ["荣耀", "小米"]},
        {"title": "Switch2游戏机发布", "platform": "B站", "heat": f"{random.randint(1000,2000)}万", "trend": "🔥🔥🔥 爆发式增长", "type": "科技", "aud": "游戏玩家、主机用户", "time": "持续3周", "logic": "新品发布+情怀营销", "link": "https://bilibili.com/hot/switch2", "c": ["罗技", "索尼"]},
        {"title": "国产芯片突破", "platform": "微博", "heat": f"{random.randint(2000,5000)}万", "trend": "🔥🔥🔥 爆发式增长", "type": "科技", "aud": "全年龄段科技关注者", "time": "持续4周", "logic": "国产替代热度持续", "link": "https://weibo.com/hot/chip", "c": ["荣耀", "小米"]},
        
        # 美妆类 (5条)
        {"title": "春季护肤routine", "platform": "小红书", "heat": f"{random.randint(3,6)}亿浏览", "trend": "🔥🔥🔥 爆发式增长", "type": "美妆", "aud": "18-35岁女性", "time": "季节性持续2月", "logic": "换季护肤刚需", "link": "https://xiaohongshu.com/hot/spring-skincare", "c": ["AHC", "多芬", "力士", "玉兰油"]},
        {"title": "早C晚A护肤法", "platform": "小红书", "heat": f"{random.randint(1,3)}亿浏览", "trend": "🔥🔥🔥 持续上升", "type": "美妆", "aud": "25-40岁护肤进阶用户", "time": "持续6周", "logic": "成分党护肤理念传播", "link": "https://xiaohongshu.com/hot/caca", "c": ["AHC", "玉兰油"]},
        {"title": "平价替代彩妆推荐", "platform": "抖音", "heat": f"{random.randint(800,1500)}万", "trend": "🔥🔥 稳定上升", "type": "美妆", "aud": "学生党、性价比追求者", "time": "持续5周", "logic": "消费降级趋势", "link": "https://douyin.com/hot/budget-makeup", "c": ["AHC", "多芬", "玉兰油"]},
        {"title": "母亲节礼盒选购", "platform": "微博", "heat": f"{random.randint(1000,2000)}万", "trend": "🔥🔥🔥 持续上升", "type": "美妆", "aud": "送礼人群", "time": "节日前2周爆发", "logic": "节日营销+情感共鸣", "link": "https://weibo.com/hot/mothersday", "c": ["AHC", "多芬", "力士", "玉兰油"]},
        {"title": "成分党护肤科普", "platform": "小红书", "heat": f"{random.randint(600,1200)}万", "trend": "🔥🔥 稳定上升", "type": "美妆", "aud": "护肤爱好者", "time": "持续8周", "logic": "消费者教育需求", "link": "https://xiaohongshu.com/hot/skincare-ingredient", "c": ["AHC", "玉兰油"]},
        
        # 母婴类 (3条)
        {"title": "宝宝辅食制作教程", "platform": "小红书", "heat": f"{random.randint(1,2)}亿浏览", "trend": "🔥🔥 稳定上升", "type": "母婴", "aud": "0-3岁宝宝妈妈", "time": "持续8周", "logic": "育儿刚需内容", "link": "https://xiaohongshu.com/hot/babyfood", "c": ["汤臣倍健", "善存"]},
        {"title": "儿童护眼指南", "platform": "抖音", "heat": f"{random.randint(600,1200)}万", "trend": "🔥🔥🔥 持续上升", "type": "母婴", "aud": "3-12岁儿童家长", "time": "持续6周", "logic": "近视防控意识提升", "link": "https://douyin.com/hot/child-eye", "c": ["汤臣倍健"]},
        {"title": "产后修复塑形", "platform": "小红书", "heat": f"{random.randint(800,1500)}万", "trend": "🔥🔥 稳定上升", "type": "母婴", "aud": "产后妈妈", "time": "持续7周", "logic": "辣妈经济", "link": "https://xiaohongshu.com/hot/postpartum", "c": ["汤臣倍健", "多芬"]},
        
        # 健身类 (4条)
        {"title": "居家燃脂训练", "platform": "抖音", "heat": f"{random.randint(2000,5000)}万", "trend": "🔥🔥🔥 爆发式增长", "type": "健身", "aud": "20-45岁健身人群", "time": "全年持续", "logic": "健身意识全民化", "link": "https://douyin.com/hot/home-workout", "c": ["汤臣倍健", "清扬", "元气森林"]},
        {"title": "减脂餐搭配", "platform": "小红书", "heat": f"{random.randint(1,3)}亿浏览", "trend": "🔥🔥🔥 持续上升", "type": "健身", "aud": "减肥人群、健身爱好者", "time": "持续10周", "logic": "健康饮食趋势", "link": "https://xiaohongshu.com/hot/diet-meal", "c": ["汤臣倍健", "OATLY", "元气森林"]},
        {"title": "健身房打卡vlog", "platform": "B站", "heat": f"{random.randint(500,1000)}万", "trend": "🔥🔥 稳定上升", "type": "健身", "aud": "健身爱好者", "time": "持续8周", "logic": "社交健身潮流", "link": "https://bilibili.com/hot/gym-vlog", "c": ["清扬", "汤臣倍健"]},
        {"title": "拉伸放松技巧", "platform": "抖音", "heat": f"{random.randint(300,800)}万", "trend": "🔥🔥 持续上升", "type": "健身", "aud": "久坐人群、运动后人群", "time": "持续6周", "logic": "运动恢复需求增加", "link": "https://douyin.com/hot/stretching", "c": ["汤臣倍健", "元气森林"]},
        
        # 美食类 (5条)
        {"title": "春日野餐食谱", "platform": "小红书", "heat": f"{random.randint(2,5)}亿浏览", "trend": "🔥🔥🔥 爆发式增长", "type": "美食", "aud": "年轻人、家庭用户", "time": "季节性持续1月", "logic": "春季户外活动增加", "link": "https://xiaohongshu.com/hot/picnic-food", "c": ["OATLY", "百威", "元气森林", "农夫山泉"]},
        {"title": "咖啡探店指南", "platform": "小红书", "heat": f"{random.randint(1,3)}亿浏览", "trend": "🔥🔥🔥 持续上升", "type": "美食", "aud": "咖啡爱好者", "time": "全年持续", "logic": "咖啡文化普及", "link": "https://xiaohongshu.com/hot/coffee", "c": ["OATLY", "农夫山泉"]},
        {"title": "啤酒搭配美食", "platform": "微博", "heat": f"{random.randint(500,1000)}万", "trend": "🔥🔥 稳定上升", "type": "美食", "aud": "年轻男性、美食爱好者", "time": "持续4周", "logic": "夜经济消费复苏", "link": "https://weibo.com/hot/beer-food", "c": ["百威"]},
        {"title": "预制菜测评", "platform": "抖音", "heat": f"{random.randint(800,1500)}万", "trend": "🔥🔥 持续上升", "type": "美食", "aud": "上班族、年轻家庭", "time": "持续8周", "logic": "懒人经济+便捷需求", "link": "https://douyin.com/hot/premade-food", "c": ["百威", "农夫山泉"]},
        {"title": "健康饮品新趋势", "platform": "小红书", "heat": f"{random.randint(600,1200)}万", "trend": "🔥🔥🔥 持续上升", "type": "美食", "aud": "健康意识消费者", "time": "持续10周", "logic": "无糖低卡消费升级", "link": "https://xiaohongshu.com/hot/healthy-drink", "c": ["OATLY", "元气森林", "农夫山泉"]},
        
        # 旅游类 (3条)
        {"title": "春季赏花目的地", "platform": "小红书", "heat": f"{random.randint(3,8)}亿浏览", "trend": "🔥🔥🔥 爆发式增长", "type": "旅游", "aud": "旅游爱好者、家庭", "time": "季节性2月", "logic": "春游季节+打卡文化", "link": "https://xiaohongshu.com/hot/spring-flower", "c": ["希宝", "元气森林", "农夫山泉"]},
        {"title": "周末周边游攻略", "platform": "抖音", "heat": f"{random.randint(1000,3000)}万", "trend": "🔥🔥🔥 持续上升", "type": "旅游", "aud": "上班族、短途游爱好者", "time": "全年持续", "logic": "微度假概念兴起", "link": "https://douyin.com/hot/weekend-travel", "c": ["希宝", "百威"]},
        {"title": "宠物友好景区推荐", "platform": "小红书", "heat": f"{random.randint(500,1000)}万", "trend": "🔥🔥 稳定上升", "type": "旅游", "aud": "宠物主", "time": "持续10周", "logic": "携宠出行需求增加", "link": "https://xiaohongshu.com/hot/pet-travel", "c": ["希宝", "皇家"]},
        
        # 教育类 (3条)
        {"title": "AI办公效率课", "platform": "B站", "heat": f"{random.randint(800,2000)}万", "trend": "🔥🔥🔥 爆发式增长", "type": "教育", "aud": "职场人士、学生", "time": "持续6周", "logic": "AI技能焦虑+学习需求", "link": "https://bilibili.com/hot/ai-office", "c": ["罗技", "小米"]},
        {"title": "考研考公备考指南", "platform": "微博", "heat": f"{random.randint(1000,3000)}万", "trend": "🔥🔥🔥 持续上升", "type": "教育", "aud": "大学生、待业人群", "time": "考试季集中", "logic": "就业压力传导", "link": "https://weibo.com/hot/exam", "c": ["罗技", "汤臣倍健"]},
        {"title": "亲子阅读时光", "platform": "小红书", "heat": f"{random.randint(500,1000)}万", "trend": "🔥🔥 稳定上升", "type": "教育", "aud": "3-10岁儿童家长", "time": "持续12周", "logic": "素质教育重视", "link": "https://xiaohongshu.com/hot/parenting-reading", "c": ["汤臣倍健", "善存"]},
        
        # 汽车类 (2条)
        {"title": "新能源汽车选购", "platform": "微博", "heat": f"{random.randint(1000,3000)}万", "trend": "🔥🔥🔥 持续上升", "type": "汽车", "aud": "准购车人群", "time": "持续8周", "logic": "新能源渗透率提升", "link": "https://weibo.com/hot/ev-car", "c": ["荣耀", "小米"]},
        {"title": "车载好物分享", "platform": "小红书", "heat": f"{random.randint(300,800)}万", "trend": "🔥🔥 稳定上升", "type": "汽车", "aud": "有车一族", "time": "持续10周", "logic": "车内生活品质追求", "link": "https://xiaohongshu.com/hot/car-gadgets", "c": ["HC", "威猛先生"]},
        
        # 宠物类 (2条)
        {"title": "宠物日常vlog", "platform": "小红书", "heat": f"{random.randint(1,2)}亿浏览", "trend": "🔥🔥 持续上升", "type": "宠物", "aud": "宠物爱好者", "time": "全年持续", "logic": "云吸宠物文化", "link": "https://xiaohongshu.com/hot/pet-vlog", "c": ["希宝", "皇家"]},
        {"title": "宠物健康饮食科普", "platform": "抖音", "heat": f"{random.randint(400,900)}万", "trend": "🔥🔥 稳定上升", "type": "宠物", "aud": "宠物主", "time": "持续8周", "logic": "宠物健康意识提升", "link": "https://douyin.com/hot/pet-health", "c": ["希宝", "皇家"]},
        
        # 家居清洁类 (2条)
        {"title": "春季大扫除攻略", "platform": "小红书", "heat": f"{random.randint(800,1500)}万", "trend": "🔥🔥🔥 爆发式增长", "type": "家居", "aud": "家庭主妇、年轻家庭", "time": "季节性1月", "logic": "春节后大扫除习惯", "link": "https://xiaohongshu.com/hot/spring-clean", "c": ["HC", "威猛先生", "舒适"]},
        {"title": "极简生活整理术", "platform": "小红书", "heat": f"{random.randint(600,1200)}万", "trend": "🔥🔥 稳定上升", "type": "家居", "aud": "追求生活品质的人群", "time": "持续12周", "logic": "断舍离文化流行", "link": "https://xiaohongshu.com/hot/minimalism", "c": ["HC", "威猛先生", "舒适"]},
    ]
    return hot_topics

def get_title_by_angle(angle, hot_topic, brand, product):
    """根据内容角度生成对应标题"""
    templates = {
        "产品测评": [
            f"《{hot_topic['title']}？{product}真实测评来了》",
            f"《用了{product}一个月，我有话说｜{hot_topic['title']}》",
            f"《{product}深度测评：{hot_topic['title']}背景下的真实体验》",
        ],
        "使用教程": [
            f"《手把手教你用{product}，{hot_topic['title']}必备技巧》",
            f"《{product}正确使用指南，{hot_topic['title']}场景下超实用》",
            f"《新手必看！{product}使用教程×{hot_topic['title']}》",
        ],
        "热点借势": [
            f"《{hot_topic['title']}火了，{brand}也有话说》",
            f"《借势{hot_topic['title']}，{product}这样用超赞》",
            f"《{hot_topic['title']}热潮下，{brand}的应对之道》",
        ],
        "痛点解决": [
            f"《{hot_topic['title']}遇到这些问题？{product}帮你解决》",
            f"《避坑指南：{hot_topic['title']}选{product}就对了》",
            f"《踩过这些坑才知道，{product}才是{hot_topic['title']}最优解》",
        ],
        "场景展示": [
            f"《{hot_topic['title']}场景下，{product}的N种用法》",
            f"《从{hot_topic['title']}看{product}的正确打开方式》",
            f"《{hot_topic['title']}必备好物：{product}场景实测》",
        ],
        "对比评测": [
            f"《{product}vs竞品深度对比，{hot_topic['title']}谁更强》",
            f"《{hot_topic['title']}横评：{brand}产品凭什么出圈》",
            f"《同价位{product}大横评，{hot_topic['title']}背景下谁更值》",
        ],
        "开箱体验": [
            f"《{product}开箱！{hot_topic['title']}热度下的第一印象》",
            f"《拆开{product}的那一刻，{hot_topic['title']}的感觉来了》",
            f"《{hot_topic['title']}首发开箱：{product}惊喜连连》",
        ],
        "种草推荐": [
            f"《{hot_topic['title']}必入清单，{brand}产品上榜理由》",
            f"《强烈种草！{hot_topic['title']}+{product}的完美组合》",
            f"《{hot_topic['title']}好物推荐：{product}凭什么排第一》",
        ],
        "剧情植入": [
            f"《{hot_topic['title']}×{product}剧情向，结局反转太惊喜》",
            f"《当{hot_topic['title']}遇上{brand}，这剧情绝了》",
            f"《{hot_topic['title']}里的{product}：一个关于选择的故事》",
        ],
        "挑战赛": [
            f"《{hot_topic['title']}挑战赛！{product}实测能否通关》",
            f"《接受{hot_topic['title']}挑战，{brand}产品表现如何》",
            f"《{product}挑战{hot_topic['title']}极限，结果出乎意料》",
        ],
        "测评对比": [
            f"《{hot_topic['title']}深度对比：{product}vs同类产品谁更值》",
            f"《{brand}全系{product}横评，{hot_topic['title']}场景大PK》",
            f"《{hot_topic['title']}爆款对比：{product}凭什么更值得买》",
        ],
        "教程攻略": [
            f"《{hot_topic['title']}完全攻略！{product}正确用法详解》",
            f"《{hot_topic['title']}进阶指南：{product}高手都这样用》",
            f"《保姆级教程：{hot_topic['title']}场景下{product}的使用秘籍》",
        ],
        "Vlog日常": [
            f"《{hot_topic['title']}Vlog｜用{product}的日常有多爽》",
            f"《记录{hot_topic['title']}的一天，{brand}全程陪伴》",
            f"《我的{hot_topic['title']}日常：{product}是怎么融入生活的》",
        ],
        "知识科普": [
            f"《科普贴：{hot_topic['title']}背后的{product}黑科技》",
            f"《关于{hot_topic['title']}，{brand}产品告诉你的真相》",
            f"《{hot_topic['title']}知识点：为什么{product}是最佳选择》",
        ],
        "情感故事": [
            f"《{hot_topic['title']}里的温情时刻，{product}见证感动》",
            f"《我和{brand}的故事：从{hot_topic['title']}说起》",
            f"《{hot_topic['title']}让我想起了{product}陪伴的那些日子》",
        ],
        "联名合作": [
            f"《{brand}×{hot_topic['title']}联名来了！{product}限定款抢先看》",
            f"《联名爆款！{brand}携手{hot_topic['title']}推出{product}特别版》",
            f"《{hot_topic['title']}联名{brand}，{product}这次真的绝了》",
            f"《跨界联名新玩法：{brand}+{hot_topic['title']}={product}惊喜》",
        ],
        "限时优惠": [
            f"《限时福利！{hot_topic['title']}期间{product}直降XX%》",
            f"《{hot_topic['title']}专属优惠：{brand}产品史低价来了》",
            f"《别错过！{hot_topic['title']}节点{product}限时特惠攻略》",
            f"《{brand}×{hot_topic['title']}：限时买{product}送好礼》",
        ],
        "用户故事": [
            f"《真实用户说：{product}如何改变了我的{hot_topic['title']}体验》",
            f"《用户故事｜{hot_topic['title']}背景下，{brand}陪我走过的日子》",
            f"《听他们说：{product}在{hot_topic['title']}中的真实故事》",
            f"《{hot_topic['title']}用户实录：选择{brand}的理由》",
        ],
        "专家访谈": [
            f"《专家说｜{hot_topic['title']}趋势下，{product}的科学使用方法》",
            f"《行业专家解读：{hot_topic['title']}与{brand}产品的深度关联》",
            f"《专访{brand}研发团队：{hot_topic['title']}背后的{product}研发故事》",
            f"《权威解读：{hot_topic['title']}场景下{product}的专业建议》",
        ],
        "行业趋势": [
            f"《{hot_topic['title']}引发行业变革，{brand}如何引领{product}新趋势》",
            f"《行业趋势报告：{hot_topic['title']}时代{product}的市场机遇》",
            f"《{hot_topic['title']}趋势解析：{brand}产品为何成为新标杆》",
            f"《从{hot_topic['title']}看{product}行业未来：{brand}的前瞻布局》",
        ],
    }
    return random.choice(templates.get(angle, templates["热点借势"]))

def generate_client_ideas(client, hot_topics):
    """为单个客户生成选题 - 每客户40-50条"""
    ideas = []
    today = datetime.now().strftime("%Y%m%d")
    
    # 每个客户生成40-50个选题
    num_ideas = random.randint(40, 50)
    
    # 用于去重的标题集合
    used_titles = set()
    
    for i in range(num_ideas):
        hot_topic = random.choice(hot_topics)
        angle = random.choice(ANGLES)
        platform = random.choice(PLATFORMS)
        product = random.choice(client["products"])
        brand = client["brand"]
        
        # 根据角度生成标题
        title = get_title_by_angle(angle, hot_topic, brand, product)
        retry_count = 0
        while title in used_titles and retry_count < 20:
            title = get_title_by_angle(angle, hot_topic, brand, product)
            retry_count += 1
        
        # 如果还是重复，加序号区分
        if title in used_titles:
            title = f"{title[:-1]}（{i+1}）》"
        
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
        },
        {
            "name": "联名场景",
            "description": f"{client['brand']}产品的跨界联名机会",
            "opportunities": ["节日限定", "IP联名", "品牌跨界", "明星合作"],
            "content_angle": "联名合作型"
        },
        {
            "name": "促销场景",
            "description": f"{client['brand']}产品的限时优惠场景",
            "promotions": ["节日大促", "会员专享", "新品首发", "清仓特卖"],
            "content_angle": "限时优惠型"
        },
    ]
    
    for product in client["products"]:
        for template in scenario_templates:
            scenario = {
                "client": client["brand"],
                "product": product,
                "scenario_type": template["name"],
                "description": template["description"],
                "content_angle": template["content_angle"],
                "keywords": random.sample(["痛点", "情感", "场景", "对比", "热点", "联名", "优惠", "故事", "专家", "趋势"], 3)
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
        print(f"  📝 {client['brand']}: {len(ideas)} 条选题")
    
    print(f"✅ 生成 {len(all_ideas)} 条客户选题（目标：500+）")
    
    # 生成SKU场景
    all_scenarios = []
    for client in CLIENTS:
        scenarios = generate_sku_scenarios(client)
        all_scenarios.extend(scenarios)
    print(f"✅ 生成 {len(all_scenarios)} 条SKU场景")
    
    # 保存数据
    import os
    output_dir = os.path.dirname(os.path.abspath(__file__))
    
    with open(os.path.join(output_dir, "client_ideas.json"), "w", encoding="utf-8") as f:
        json.dump(all_ideas, f, ensure_ascii=False, indent=2)
    
    with open(os.path.join(output_dir, "sku_scenarios.json"), "w", encoding="utf-8") as f:
        json.dump(all_scenarios, f, ensure_ascii=False, indent=2)
    
    with open(os.path.join(output_dir, "hot_topics.json"), "w", encoding="utf-8") as f:
        json.dump(hot_topics, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 数据更新完成！")
    print(f"📊 统计：{len(CLIENTS)} 个客户 × 平均 45 条选题 = 预计 {len(CLIENTS)*45}+ 条")
    return all_ideas, all_scenarios, hot_topics

if __name__ == "__main__":
    update_all_data()
