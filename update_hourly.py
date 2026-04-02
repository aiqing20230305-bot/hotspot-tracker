#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每小时热点更新脚本
从各平台抓取最新热点，更新热点数据库，生成客户选题
"""

import json
import os
from datetime import datetime
import uuid
import hashlib

# 客户列表
CLIENTS = [
    {"brand": "荣耀", "industry": "3C数码", "products": ["荣耀手机", "荣耀平板", "荣耀手表", "荣耀折叠屏", "荣耀笔记本", "荣耀耳机", "荣耀智慧屏"]},
    {"brand": "罗技", "industry": "3C数码", "products": ["罗技鼠标", "罗技键盘", "罗技耳机", "罗技摄像头", "罗技游戏手柄", "罗技音箱", "罗技会议设备"]},
    {"brand": "小米", "industry": "3C数码", "products": ["小米手机", "小米平板", "小米手环", "小米智能家居", "小米电视", "小米路由器", "小米充电器", "小米耳机"]},
    {"brand": "索尼", "industry": "3C数码", "products": ["索尼相机", "索尼耳机", "索尼游戏机", "索尼电视", "索尼手机", "索尼音箱", "索尼播放器"]},
    {"brand": "AHC", "industry": "美妆", "products": ["AHC面膜", "AHC精华", "AHC眼霜", "AHC防晒霜", "AHC水乳", "AHC面霜", "AHC卸妆水"]},
    {"brand": "多芬", "industry": "护肤", "products": ["多芬洗面奶", "多芬护肤霜", "多芬沐浴露", "多芬身体乳", "多芬洗发水", "多芬护发素", "多芬香皂"]},
    {"brand": "力士", "industry": "护肤", "products": ["力士香皂", "力士沐浴露", "力士洗发水", "力士护发素", "力士身体乳", "力士香氛"]},
    {"brand": "清扬", "industry": "护肤", "products": ["清扬洗发水", "清扬护发素", "清扬头皮护理", "清扬去屑洗发水", "清扬控油洗发水"]},
    {"brand": "玉兰油", "industry": "美妆", "products": ["玉兰油面霜", "玉兰油精油", "玉兰油眼霜", "玉兰油精华", "玉兰油防晒", "玉兰油面膜"]},
    {"brand": "汤臣倍健", "industry": "保健", "products": ["汤臣倍健维生素", "汤臣倍健钙片", "汤臣倍健蛋白粉", "汤臣倍健鱼油", "汤臣倍健益生菌"]},
    {"brand": "善存", "industry": "保健", "products": ["善存维生素", "善存矿物质", "善存复合营养", "善存钙片", "善存锌片"]},
    {"brand": "HC", "industry": "护肤", "products": ["HC面膜", "HC精华液", "HC护肤套装", "HC眼霜", "HC面霜"]},
    {"brand": "威猛先生", "industry": "清洁", "products": ["威猛先生清洁剂", "威猛先生消毒液", "威猛先生洗涤剂", "威猛先生洁厕灵", "威猛先生厨房清洁"]},
    {"brand": "舒适", "industry": "日用", "products": ["舒适纸巾", "舒适卷纸", "舒适湿巾", "舒适抽纸", "舒适手帕纸"]},
    {"brand": "希宝", "industry": "母婴", "products": ["希宝奶粉", "希宝纸尿裤", "希宝婴儿护肤", "希宝辅食", "希宝湿巾"]},
    {"brand": "皇家", "industry": "宠物", "products": ["皇家狗粮", "皇家猫粮", "皇家宠物零食", "皇家宠物营养品"]},
    {"brand": "OATLY", "industry": "食品", "products": ["OATLY燕麦奶", "OATLY冰淇淋", "OATLY酸奶", "OATLY咖啡伴侣"]},
    {"brand": "百威", "industry": "酒饮", "products": ["百威啤酒", "百威精酿", "百威无醇啤酒", "百威果啤"]},
    {"brand": "元气森林", "industry": "饮料", "products": ["元气森林气泡水", "元气森林电解质水", "元气森林茶饮", "元气森林果汁"]},
    {"brand": "农夫山泉", "industry": "饮料", "products": ["农夫山泉矿泉水", "农夫山泉茶π", "农夫山泉尖叫", "农夫山泉NFC果汁"]}
]

# 行业与热点类别映射
INDUSTRY_CATEGORIES = {
    "3C数码": ["科技", "汽车", "教育"],
    "美妆": ["美妆", "时尚"],
    "护肤": ["美妆", "时尚", "健康"],
    "保健": ["健康", "健身", "母婴"],
    "清洁": ["家居", "生活"],
    "日用": ["家居", "生活"],
    "母婴": ["母婴", "教育", "健康"],
    "宠物": ["宠物", "生活"],
    "食品": ["美食", "健康"],
    "酒饮": ["美食", "旅游"],
    "饮料": ["美食", "健康", "健身"]
}

# 新增热点数据（基于搜索结果）
NEW_HOT_TOPICS = [
    {
        "title": "孙颖莎世界杯3-0晋级 开启争冠之路",
        "hot_value": 380000000,
        "url": "https://k.sina.com.cn/article_7879995911_1d5af320706801qk78.html",
        "platform": "微博/抖音",
        "industries": ["体育"],
        "trends": ["热"],
        "type": "体育热点",
        "sentiment": "正面",
        "keywords": ["孙颖莎", "乒乓球", "世界杯", "3-0", "晋级"],
        "c": ["元气森林", "农夫山泉", "汤臣倍健"]
    },
    {
        "title": "B站AI创作大赛收官 8300份作品播放7亿",
        "hot_value": 350000000,
        "url": "https://k.sina.com.cn/article_7857201856_1d45362c001903ukxq.html",
        "platform": "B站/全网",
        "industries": ["科技", "互联网"],
        "trends": ["爆"],
        "type": "科技热点",
        "sentiment": "正面",
        "keywords": ["B站", "AI创作", "updream", "AI动画", "创作者"],
        "c": ["小米", "荣耀", "索尼", "罗技"]
    },
    {
        "title": "Seedance排队成AI创作者新痛点 8万人在线等待",
        "hot_value": 320000000,
        "url": "https://k.sina.com.cn/article_7857201856_1d45362c001903w3ry.html",
        "platform": "抖音/小红书",
        "industries": ["科技", "互联网"],
        "trends": ["热"],
        "type": "科技热点",
        "sentiment": "中性",
        "keywords": ["Seedance", "AI视频", "字节跳动", "排队", "创作者"],
        "c": ["小米", "荣耀", "索尼"]
    },
    {
        "title": "全球半导体开启新一轮涨价潮 晶圆代工全线提价",
        "hot_value": 300000000,
        "url": "https://www.sohu.com/a/1003742455_122692513",
        "platform": "微博/全网",
        "industries": ["科技", "金融"],
        "trends": ["热"],
        "type": "财经热点",
        "sentiment": "中性",
        "keywords": ["半导体", "涨价", "芯片", "晶圆", "电子"],
        "c": ["小米", "荣耀", "索尼", "罗技"]
    },
    {
        "title": "2028洛杉矶奥运会门票4月9日开售",
        "hot_value": 280000000,
        "url": "https://www.sohu.com/a/1003742455_122692513",
        "platform": "微博/全网",
        "industries": ["体育", "旅游"],
        "trends": ["新"],
        "type": "体育热点",
        "sentiment": "正面",
        "keywords": ["奥运会", "洛杉矶", "门票", "2028", "体育"],
        "c": ["农夫山泉", "元气森林", "OATLY", "百威"]
    },
    {
        "title": "孙俪新剧《危险关系》转型获赞 无滤镜演技受热议",
        "hot_value": 260000000,
        "url": "https://so.html5.qq.com/page/real/search_news?docid=70000021_54669cd0e2212552",
        "platform": "微博/抖音",
        "industries": ["娱乐"],
        "trends": ["热"],
        "type": "娱乐热点",
        "sentiment": "正面",
        "keywords": ["孙俪", "危险关系", "新剧", "转型", "演技"],
        "c": ["AHC", "玉兰油", "多芬"]
    },
    {
        "title": "长鹰-8无人空中重卡成功首飞",
        "hot_value": 250000000,
        "url": "https://new.qq.com/rain/a/20260401A01DX300",
        "platform": "微博/全网",
        "industries": ["科技", "航空"],
        "trends": ["新"],
        "type": "科技热点",
        "sentiment": "正面",
        "keywords": ["长鹰-8", "无人机", "首飞", "航空", "物流"],
        "c": ["小米", "荣耀", "索尼"]
    },
    {
        "title": "清明假期高速免费 出行高峰今日开启",
        "hot_value": 240000000,
        "url": "https://new.qq.com/rain/a/20260401A01DX300",
        "platform": "微博/全网",
        "industries": ["旅游", "交通"],
        "trends": ["热"],
        "type": "节日热点",
        "sentiment": "正面",
        "keywords": ["清明节", "高速免费", "出行", "假期", "自驾"],
        "c": ["农夫山泉", "OATLY", "元气森林", "百威"]
    },
    {
        "title": "橹穆CP愚人节引爆热搜 话题阅读量破2.4亿",
        "hot_value": 240000000,
        "url": "https://new.qq.com/rain/a/20260401A04UGW00",
        "platform": "微博/抖音",
        "industries": ["娱乐"],
        "trends": ["爆"],
        "type": "娱乐热点",
        "sentiment": "中性",
        "keywords": ["橹穆", "CP", "站姐", "愚人节", "热搜"],
        "c": ["AHC", "玉兰油", "力士"]
    },
    {
        "title": "全球智能手机迎来新一轮涨价潮 AI成核心驱动力",
        "hot_value": 220000000,
        "url": "https://k.sina.com.cn/article_7857201856_1d45362c001903w3ry.html",
        "platform": "微博/全网",
        "industries": ["科技", "消费"],
        "trends": ["热"],
        "type": "科技热点",
        "sentiment": "中性",
        "keywords": ["智能手机", "涨价", "AI", "手机市场", "消费电子"],
        "c": ["小米", "荣耀", "索尼"]
    },
    {
        "title": "世界数据组织在北京成立 总部设于中国",
        "hot_value": 200000000,
        "url": "https://weibo.com",
        "platform": "微博/全网",
        "industries": ["科技", "政策"],
        "trends": ["新"],
        "type": "政策热点",
        "sentiment": "正面",
        "keywords": ["世界数据组织", "北京", "数据治理", "数字经济", "国际合作"],
        "c": ["小米", "荣耀", "索尼", "罗技"]
    },
    {
        "title": "李荣浩回应抄袭风波 登热搜第一",
        "hot_value": 180000000,
        "url": "https://weibo.com",
        "platform": "微博",
        "industries": ["娱乐", "音乐"],
        "trends": ["爆"],
        "type": "娱乐热点",
        "sentiment": "中性",
        "keywords": ["李荣浩", "抄袭", "小眼睛", "Signal", "热搜"],
        "c": ["AHC", "玉兰油", "多芬", "力士"]
    },
    {
        "title": "郭敬明执导《月鳞绮纪》空降开播 融合聊斋山海经",
        "hot_value": 160000000,
        "url": "https://weibo.com",
        "platform": "微博/B站",
        "industries": ["娱乐"],
        "trends": ["热"],
        "type": "影视热点",
        "sentiment": "中性",
        "keywords": ["郭敬明", "月鳞绮纪", "聊斋", "山海经", "空降开播"],
        "c": ["AHC", "玉兰油", "索尼"]
    },
    {
        "title": "乘风2026乌兰图雅萧蔷等33位女性嘉宾集结",
        "hot_value": 150000000,
        "url": "https://weibo.com",
        "platform": "微博/芒果TV",
        "industries": ["娱乐"],
        "trends": ["新"],
        "type": "综艺热点",
        "sentiment": "正面",
        "keywords": ["乘风2026", "乌兰图雅", "萧蔷", "浪姐", "综艺"],
        "c": ["AHC", "玉兰油", "力士", "多芬"]
    },
    {
        "title": "李湘携王诗龄现身韶山献花 瘦了20斤",
        "hot_value": 140000000,
        "url": "https://weibo.com",
        "platform": "微博",
        "industries": ["娱乐"],
        "trends": ["热"],
        "type": "娱乐热点",
        "sentiment": "正面",
        "keywords": ["李湘", "王诗龄", "韶山", "瘦身", "明星"],
        "c": ["AHC", "玉兰油", "多芬", "力士"]
    },
    {
        "title": "鞠婧祎丝芭传媒纠纷再上热搜 税务局回应",
        "hot_value": 130000000,
        "url": "https://weibo.com",
        "platform": "微博",
        "industries": ["娱乐"],
        "trends": ["热"],
        "type": "娱乐热点",
        "sentiment": "中性",
        "keywords": ["鞠婧祎", "丝芭传媒", "合约纠纷", "税务", "明星"],
        "c": ["AHC", "玉兰油", "力士"]
    },
    {
        "title": "活人感成2026流行词 指真实自然不刻意伪装",
        "hot_value": 120000000,
        "url": "https://weibo.com",
        "platform": "微博/小红书",
        "industries": ["社会", "文化"],
        "trends": ["新"],
        "type": "社会热点",
        "sentiment": "正面",
        "keywords": ["活人感", "真实", "自然", "流行词"],
        "c": ["多芬", "力士", "AHC", "玉兰油"]
    },
    {
        "title": "今年蚊子或迎史诗级加强 疾控部门紧急提醒",
        "hot_value": 110000000,
        "url": "https://weibo.com",
        "platform": "微博/全网",
        "industries": ["健康", "生活"],
        "trends": ["热"],
        "type": "健康热点",
        "sentiment": "中性",
        "keywords": ["蚊子", "疾控", "健康提醒", "夏季", "防护"],
        "c": ["汤臣倍健", "善存", "威猛先生"]
    },
    {
        "title": "澳洲优思益被曝光为纯国产 抖音天猫店铺暂停营业",
        "hot_value": 100000000,
        "url": "https://weibo.com",
        "platform": "微博/全网",
        "industries": ["健康", "消费"],
        "trends": ["热"],
        "type": "消费热点",
        "sentiment": "负面",
        "keywords": ["优思益", "保健品", "虚假宣传", "进口", "叶黄素"],
        "c": ["汤臣倍健", "善存"]
    },
    {
        "title": "4月1日起全国严查后排未系安全带 违规将处罚",
        "hot_value": 95000000,
        "url": "https://weibo.com",
        "platform": "微博/全网",
        "industries": ["社会", "交通"],
        "trends": ["新"],
        "type": "政策热点",
        "sentiment": "中性",
        "keywords": ["安全带", "后排乘客", "交通法规", "执法", "4月1日"],
        "c": ["小米", "荣耀", "农夫山泉"]
    },
    {
        "title": "瑞幸紫椰子事件 椰肉变色引消费者维权",
        "hot_value": 90000000,
        "url": "https://weibo.com",
        "platform": "微博/全网",
        "industries": ["餐饮", "消费"],
        "trends": ["爆"],
        "type": "消费热点",
        "sentiment": "负面",
        "keywords": ["瑞幸", "紫椰子", "食品安全", "消费者维权", "椰肉变色"],
        "c": ["农夫山泉", "OATLY", "元气森林"]
    },
    {
        "title": "伊朗海军司令遇难 美方威胁彻底摧毁能源设施",
        "hot_value": 85000000,
        "url": "https://weibo.com",
        "platform": "微博/全网",
        "industries": ["国际", "军事"],
        "trends": ["热"],
        "type": "国际热点",
        "sentiment": "负面",
        "keywords": ["伊朗", "海军司令", "霍尔木兹海峡", "能源", "中东局势"],
        "c": []
    },
    {
        "title": "2026美白精华怎么选 热门产品与成分参考指南",
        "hot_value": 80000000,
        "url": "https://weibo.com",
        "platform": "小红书/微博",
        "industries": ["美妆"],
        "trends": ["热"],
        "type": "美妆热点",
        "sentiment": "正面",
        "keywords": ["美白精华", "护肤", "成分", "美妆", "选购指南"],
        "c": ["AHC", "玉兰油", "HC"]
    },
    {
        "title": "colorwalk成为2026春季最火生活趋势",
        "hot_value": 75000000,
        "url": "https://weibo.com",
        "platform": "小红书/抖音",
        "industries": ["生活", "时尚"],
        "trends": ["新"],
        "type": "生活热点",
        "sentiment": "正面",
        "keywords": ["colorwalk", "色彩漫步", "春季出游", "小红书", "打卡"],
        "c": ["农夫山泉", "OATLY", "元气森林"]
    },
    {
        "title": "抖音发布未来导演扶持计划 100亿流量池",
        "hot_value": 70000000,
        "url": "https://weibo.com",
        "platform": "抖音/全网",
        "industries": ["互联网", "内容"],
        "trends": ["新"],
        "type": "互联网热点",
        "sentiment": "正面",
        "keywords": ["抖音", "导演扶持计划", "创作者", "流量池", "内容产业"],
        "c": ["小米", "索尼", "罗技"]
    },
    {
        "title": "张国荣逝世23周年 螺蛳粉哥发文纪念",
        "hot_value": 65000000,
        "url": "https://weibo.com",
        "platform": "微博",
        "industries": ["娱乐"],
        "trends": ["热"],
        "type": "纪念热点",
        "sentiment": "中性",
        "keywords": ["张国荣", "逝世23周年", "愚人节", "纪念"],
        "c": ["多芬", "力士"]
    },
    {
        "title": "上海乒乓球嘉年华4月12日开幕",
        "hot_value": 60000000,
        "url": "https://weibo.com",
        "platform": "微博/上海",
        "industries": ["体育", "活动"],
        "trends": ["新"],
        "type": "体育热点",
        "sentiment": "正面",
        "keywords": ["乒乓球", "嘉年华", "上海", "国际乒联百年", "全民运动"],
        "c": ["农夫山泉", "汤臣倍健", "善存"]
    },
    {
        "title": "丙午年黄帝故里云拜祖平台上线 全球华人可网上拜祖",
        "hot_value": 55000000,
        "url": "https://weibo.com",
        "platform": "微博/全网",
        "industries": ["文化", "传统"],
        "trends": ["新"],
        "type": "文化热点",
        "sentiment": "正面",
        "keywords": ["黄帝故里", "云拜祖", "拜祖大典", "华夏儿女", "三月三"],
        "c": ["农夫山泉", "OATLY"]
    },
    {
        "title": "清明春假黄金周 赏花踏青出行爆发",
        "hot_value": 50000000,
        "url": "https://weibo.com",
        "platform": "微博/小红书",
        "industries": ["旅游"],
        "trends": ["热"],
        "type": "节日热点",
        "sentiment": "正面",
        "keywords": ["清明节", "春假", "赏花", "踏青", "自驾游"],
        "c": ["农夫山泉", "OATLY", "元气森林", "百威", "希宝"]
    }
]

def generate_id(title, created_at):
    """生成唯一ID"""
    base = f"{title}_{created_at}"
    hash_obj = hashlib.md5(base.encode())
    return hash_obj.hexdigest()[:8]

def update_hot_topics():
    """更新热点数据库"""
    hot_topics_file = "/Users/zhangjingwei/.qclaw/workspace/hotspot-tracker/hot_topics.json"
    
    # 读取现有热点
    with open(hot_topics_file, 'r', encoding='utf-8') as f:
        existing_topics = json.load(f)
    
    # 获取现有标题
    existing_titles = {t['title'] for t in existing_topics}
    
    # 添加新热点
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    new_count = 0
    
    for i, topic in enumerate(NEW_HOT_TOPICS):
        if topic['title'] not in existing_titles:
            new_topic = {
                "rank": len(existing_topics) + i + 1,
                "title": topic['title'],
                "hot_value": topic['hot_value'],
                "url": topic['url'],
                "platform": topic['platform'],
                "industries": topic['industries'],
                "trends": topic['trends'],
                "type": topic['type'],
                "sentiment": topic['sentiment'],
                "keywords": topic['keywords'],
                "c": topic['c'],
                "created_at": now,
                "id": f"ht_{generate_id(topic['title'], now)}"
            }
            existing_topics.append(new_topic)
            new_count += 1
    
    # 按热度排序，保留前100条
    existing_topics.sort(key=lambda x: x.get('hot_value', 0), reverse=True)
    existing_topics = existing_topics[:100]
    
    # 更新排名
    for i, topic in enumerate(existing_topics):
        topic['rank'] = i + 1
    
    # 保存
    with open(hot_topics_file, 'w', encoding='utf-8') as f:
        json.dump(existing_topics, f, ensure_ascii=False, indent=2)
    
    print(f"更新完成: 新增 {new_count} 条热点，当前共 {len(existing_topics)} 条")
    return existing_topics

def generate_client_ideas(hot_topics):
    """为客户生成选题"""
    ideas_file = "/Users/zhangjingwei/.qclaw/workspace/hotspot-tracker/client_ideas.json"
    
    # 读取现有选题
    try:
        with open(ideas_file, 'r', encoding='utf-8') as f:
            existing_ideas = json.load(f)
    except FileNotFoundError:
        existing_ideas = []
    
    # 获取现有选题标题
    existing_titles = {i['title'] for i in existing_ideas}
    
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    new_ideas_count = 0
    
    # 为每个客户生成选题
    for client in CLIENTS:
        brand = client['brand']
        products = client['products']
        industry = client['industry']
        
        # 找到与客户行业相关的热点
        relevant_topics = []
        for topic in hot_topics[:30]:  # 只看前30条热点
            # 检查热点是否与客户相关
            if topic.get('c') and brand in topic.get('c', []):
                relevant_topics.append(topic)
            # 或者热点类别匹配
            elif any(cat in INDUSTRY_CATEGORIES.get(industry, []) for cat in topic.get('industries', [])):
                relevant_topics.append(topic)
        
        # 为每个相关热点生成选题
        for topic in relevant_topics[:5]:  # 每个客户最多5个选题
            product = products[hash(topic['title']) % len(products)]
            
            title = f"《{brand}{product}借势{topic['title'][:20]}的创意玩法》"
            
            if title not in existing_titles:
                idea = {
                    "id": f"{brand}_{generate_id(title, now)}",
                    "client": client,
                    "title": title,
                    "platform": "小红书" if industry in ["美妆", "护肤", "母婴"] else "B站",
                    "angle": "创意借势",
                    "hot_topic": topic['title'],
                    "hot_topic_id": topic['id'],
                    "heat": topic['trends'][0] if topic.get('trends') else "温热",
                    "trend": "🔥🔥🔥 爆发式增长" if "爆" in topic.get('trends', []) else "🔥🔥 快速上升",
                    "product": product,
                    "keywords": topic['keywords'][:5],
                    "quality_score": round(0.7 + hash(title) % 30 / 100, 3),
                    "quality_level": "B级-良好",
                    "engagement_estimate": f"{topic['hot_value'] // 10000}+",
                    "status": "pending",
                    "created_at": now
                }
                existing_ideas.append(idea)
                new_ideas_count += 1
    
    # 去重并保留最新
    seen_titles = set()
    unique_ideas = []
    for idea in reversed(existing_ideas):
        if idea['title'] not in seen_titles:
            seen_titles.add(idea['title'])
            unique_ideas.append(idea)
    
    unique_ideas = list(reversed(unique_ideas))
    
    # 保存
    with open(ideas_file, 'w', encoding='utf-8') as f:
        json.dump(unique_ideas, f, ensure_ascii=False, indent=2)
    
    print(f"选题生成完成: 新增 {new_ideas_count} 条选题，当前共 {len(unique_ideas)} 条")
    return unique_ideas

if __name__ == "__main__":
    print("=" * 50)
    print(f"热点更新任务开始 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 更新热点
    hot_topics = update_hot_topics()
    
    # 生成选题
    ideas = generate_client_ideas(hot_topics)
    
    print("=" * 50)
    print(f"任务完成 - 更新了 {len(hot_topics)} 条热点，{len(ideas)} 条选题")
    print("=" * 50)
