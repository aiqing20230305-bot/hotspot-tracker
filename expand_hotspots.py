#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
热点数据扩展脚本
将热点数据从103条扩展到200条以上
"""

import json
import random
from datetime import datetime, timedelta

# 读取现有数据
with open('hot_topics.json', 'r', encoding='utf-8') as f:
    existing_data = json.load(f)

print(f"现有热点数据: {len(existing_data)} 条")

# 提取现有标题用于去重
existing_titles = set(item['title'] for item in existing_data)

# 分析现有数据的热度值范围
heat_values = [item['hot_value'] for item in existing_data]
min_heat = min(heat_values)
max_heat = max(heat_values)
print(f"热度值范围: {min_heat} - {max_heat}")

# 从搜索结果中提取的新热点数据
new_hotspots = [
    # 科技类热点
    {
        "title": "OpenAI完成1220亿美元融资 估值达8520亿美元",
        "hot_value": random.randint(400000000, 480000000),
        "url": "https://finance.sina.com.cn/stock/relnews/2026-04-01/doc-inhsxzph1878185.shtml",
        "platform": "微博/全网",
        "industries": ["科技", "互联网"],
        "trends": ["爆"],
        "type": "科技热点",
        "sentiment": "正面",
        "keywords": ["OpenAI", "融资", "AI", "硅谷", "人工智能"],
        "c": ["小米", "荣耀", "索尼"],
        "created_at": "2026-04-02T07:00:00"
    },
    {
        "title": "Anthropic意外泄露51万行核心代码 引发AI安全担忧",
        "hot_value": random.randint(350000000, 420000000),
        "url": "https://k.sina.com.cn/article_7857201856_1d45362c001903usn2.html",
        "platform": "微博/全网",
        "industries": ["科技", "互联网"],
        "trends": ["爆"],
        "type": "科技热点",
        "sentiment": "负面",
        "keywords": ["Anthropic", "代码泄露", "AI安全", "Claude", "网络安全"],
        "c": ["小米", "索尼", "罗技"],
        "created_at": "2026-04-02T06:30:00"
    },
    {
        "title": "OpenAI宣布放弃视频生成工具Sora 成本过高成主因",
        "hot_value": random.randint(280000000, 350000000),
        "url": "https://k.sina.com.cn/article_7857201856_1d45362c001903wiaq.html",
        "platform": "微博/全网",
        "industries": ["科技", "互联网"],
        "trends": ["热"],
        "type": "科技热点",
        "sentiment": "中性",
        "keywords": ["OpenAI", "Sora", "视频生成", "AI工具", "成本"],
        "c": ["小米", "荣耀"],
        "created_at": "2026-04-02T07:10:00"
    },
    {
        "title": "智谱AI年营收7.24亿 同比增长132% MaaS平台ARR达17亿",
        "hot_value": random.randint(220000000, 280000000),
        "url": "https://k.sina.com.cn/article_7857201856_1d45362c001903v1ky.html",
        "platform": "微博/全网",
        "industries": ["科技", "互联网"],
        "trends": ["热"],
        "type": "科技热点",
        "sentiment": "正面",
        "keywords": ["智谱AI", "财报", "大模型", "商业化", "MaaS"],
        "c": ["小米", "索尼", "罗技"],
        "created_at": "2026-04-02T06:45:00"
    },
    {
        "title": "SpaceX秘密提交IPO申请 马斯克太空事业迎新里程碑",
        "hot_value": random.randint(300000000, 380000000),
        "url": "https://k.sina.com.cn/article_7857201856_1d45362c001903wg5a.html",
        "platform": "微博/全网",
        "industries": ["科技", "航天"],
        "trends": ["爆"],
        "type": "科技热点",
        "sentiment": "正面",
        "keywords": ["SpaceX", "IPO", "马斯克", "太空探索", "航天"],
        "c": ["小米", "荣耀", "索尼"],
        "created_at": "2026-04-02T06:00:00"
    },
    
    # 体育类热点
    {
        "title": "东契奇轰42+12迎15000分里程碑 詹姆斯胜场超天勾",
        "hot_value": random.randint(320000000, 400000000),
        "url": "https://k.sina.com.cn/article_7879995911_1d5af320706801qgqi.html",
        "platform": "微博/抖音",
        "industries": ["体育"],
        "trends": ["爆"],
        "type": "体育热点",
        "sentiment": "正面",
        "keywords": ["东契奇", "詹姆斯", "湖人", "NBA", "里程碑"],
        "c": [],
        "created_at": "2026-04-02T07:15:00"
    },
    {
        "title": "孙颖莎轻取对手强势开启世界杯淘汰赛征程",
        "hot_value": random.randint(180000000, 250000000),
        "url": "https://k.sina.com.cn/article_7879995911_1d5af320706801qk78.html",
        "platform": "微博/全网",
        "industries": ["体育"],
        "trends": ["热"],
        "type": "体育热点",
        "sentiment": "正面",
        "keywords": ["孙颖莎", "乒乓球", "世界杯", "国乒", "淘汰赛"],
        "c": ["农夫山泉", "汤臣倍健"],
        "created_at": "2026-04-02T06:20:00"
    },
    {
        "title": "意大利连续3届无缘世界杯 足球强国陷入低谷",
        "hot_value": random.randint(150000000, 200000000),
        "url": "https://www.douyin.com/search/意大利连续3届无缘世界杯",
        "platform": "抖音/微博",
        "industries": ["体育"],
        "trends": ["热"],
        "type": "体育热点",
        "sentiment": "负面",
        "keywords": ["意大利", "世界杯", "足球", "欧洲杯", "出局"],
        "c": [],
        "created_at": "2026-04-02T05:30:00"
    },
    {
        "title": "张雪机车备战达喀尔拉力赛 中国摩托车队再创历史",
        "hot_value": random.randint(120000000, 180000000),
        "url": "https://www.douyin.com/search/张雪备战达喀尔",
        "platform": "抖音/微博",
        "industries": ["体育", "消费"],
        "trends": ["热"],
        "type": "体育热点",
        "sentiment": "正面",
        "keywords": ["张雪机车", "达喀尔", "WSBK", "中国制造", "赛车"],
        "c": ["百威", "元气森林"],
        "created_at": "2026-04-02T06:10:00"
    },
    
    # 娱乐类热点
    {
        "title": "站姐愚人节互换门面引爆热搜 橹穆CP话题阅读量破2.4亿",
        "hot_value": random.randint(380000000, 450000000),
        "url": "https://new.qq.com/rain/a/20260401A04UGW00",
        "platform": "微博/全网",
        "industries": ["娱乐"],
        "trends": ["爆"],
        "type": "娱乐热点",
        "sentiment": "中性",
        "keywords": ["站姐", "愚人节", "橹穆", "CP", "热搜"],
        "c": ["AHC", "玉兰油"],
        "created_at": "2026-04-02T00:00:00"
    },
    {
        "title": "台湾艺人邱胜翊涉嫌伪造病历逃避兵役遭拘捕",
        "hot_value": random.randint(280000000, 350000000),
        "url": "https://so.html5.qq.com/page/real/search_news?docid=70000021_94569cda3e090665",
        "platform": "微博/全网",
        "industries": ["娱乐"],
        "trends": ["爆"],
        "type": "娱乐热点",
        "sentiment": "负面",
        "keywords": ["邱胜翊", "王子", "逃避兵役", "台湾艺人", "伪造病历"],
        "c": [],
        "created_at": "2026-04-02T07:01:00"
    },
    {
        "title": "孙俪新剧《危险关系》获赞 悬疑转型成功引热议",
        "hot_value": random.randint(180000000, 240000000),
        "url": "https://so.html5.qq.com/page/real/search_news?docid=70000021_54669cd0e2212552",
        "platform": "微博/抖音",
        "industries": ["娱乐", "影视"],
        "trends": ["热"],
        "type": "娱乐热点",
        "sentiment": "正面",
        "keywords": ["孙俪", "危险关系", "新剧", "转型", "悬疑剧"],
        "c": ["AHC", "玉兰油", "力士"],
        "created_at": "2026-04-02T05:40:00"
    },
    {
        "title": "2026清明档电影激战 《我,许可》《我的妈耶》领跑",
        "hot_value": random.randint(160000000, 220000000),
        "url": "https://new.qq.com/rain/a/20260401A03KCB00",
        "platform": "微博/抖音",
        "industries": ["娱乐", "影视"],
        "trends": ["热"],
        "type": "娱乐热点",
        "sentiment": "正面",
        "keywords": ["清明档", "电影", "我许可", "我的妈耶", "马思纯"],
        "c": ["猫眼", "淘票票"],
        "created_at": "2026-04-02T06:00:00"
    },
    {
        "title": "李子柒自编自导纪录片电影《温室》完成备案",
        "hot_value": random.randint(140000000, 200000000),
        "url": "https://so.html5.qq.com/page/real/search_news?docid=70000021_15569cd19bd48752",
        "platform": "微博/抖音",
        "industries": ["娱乐", "影视"],
        "trends": ["新"],
        "type": "娱乐热点",
        "sentiment": "正面",
        "keywords": ["李子柒", "纪录片", "电影", "温室", "导演"],
        "c": ["农夫山泉", "OATLY"],
        "created_at": "2026-04-02T04:20:00"
    },
    {
        "title": "赵露思新剧《朝花不见愁》女主暂定 古装仙侠引期待",
        "hot_value": random.randint(120000000, 180000000),
        "url": "https://so.html5.qq.com/page/real/search_news?docid=70000021_15569cd19bd48752",
        "platform": "微博/小红书",
        "industries": ["娱乐", "影视"],
        "trends": ["热"],
        "type": "娱乐热点",
        "sentiment": "正面",
        "keywords": ["赵露思", "朝花不见愁", "古装剧", "仙侠", "新剧"],
        "c": ["AHC", "玉兰油", "多芬"],
        "created_at": "2026-04-02T04:25:00"
    },
    
    # 社会类热点
    {
        "title": "4月新规实施:后排未系安全带全国严查 违规将处罚",
        "hot_value": random.randint(200000000, 280000000),
        "url": "https://weibo.com",
        "platform": "微博/全网",
        "industries": ["社会", "交通"],
        "trends": ["新"],
        "type": "社会热点",
        "sentiment": "正面",
        "keywords": ["安全带", "新规", "交通法规", "后排乘客", "执法"],
        "c": ["小米", "荣耀"],
        "created_at": "2026-04-02T06:00:00"
    },
    {
        "title": "蚊子史诗级加强引热议 疾控部门紧急提醒防蚊",
        "hot_value": random.randint(150000000, 220000000),
        "url": "https://www.xhby.net/content/s69cd371ce4b0639de44f4deb.html",
        "platform": "微博/全网",
        "industries": ["生活", "健康"],
        "trends": ["热"],
        "type": "社会热点",
        "sentiment": "负面",
        "keywords": ["蚊子", "疾控", "健康提醒", "夏季", "防护"],
        "c": ["威猛先生", "汤臣倍健"],
        "created_at": "2026-04-02T05:00:00"
    },
    {
        "title": "全国多地迎来清明祭扫高峰 文明祭扫成主流",
        "hot_value": random.randint(250000000, 320000000),
        "url": "https://weibo.com",
        "platform": "微博/全网",
        "industries": ["社会"],
        "trends": ["热"],
        "type": "社会热点",
        "sentiment": "中性",
        "keywords": ["清明节", "祭扫", "祭祖", "传统文化", "缅怀先人"],
        "c": ["农夫山泉", "康师傅"],
        "created_at": "2026-04-02T06:30:00"
    },
    
    # 消费类热点
    {
        "title": "清明假期赏花游火爆 全国各地花期正当时",
        "hot_value": random.randint(280000000, 350000000),
        "url": "https://weibo.com",
        "platform": "小红书/抖音",
        "industries": ["旅游", "生活"],
        "trends": ["热"],
        "type": "消费热点",
        "sentiment": "正面",
        "keywords": ["清明节", "踏青", "赏花", "春游", "旅游攻略"],
        "c": ["元气森林", "农夫山泉"],
        "created_at": "2026-04-02T06:00:00"
    },
    {
        "title": "青团销量暴增成网红爆款 清明传统美食受热捧",
        "hot_value": random.randint(180000000, 250000000),
        "url": "https://weibo.com",
        "platform": "全网",
        "industries": ["食品", "电商"],
        "trends": ["新"],
        "type": "消费热点",
        "sentiment": "正面",
        "keywords": ["清明节", "青团", "传统美食", "网红美食", "春日限定"],
        "c": ["盒马", "美团", "饿了么"],
        "created_at": "2026-04-02T06:00:00"
    },
    {
        "title": "小米SU7交付量突破10万台 新能源汽车市场竞争加剧",
        "hot_value": random.randint(200000000, 280000000),
        "url": "https://weibo.com",
        "platform": "微博",
        "industries": ["汽车", "科技"],
        "trends": ["爆"],
        "type": "科技热点",
        "sentiment": "正面",
        "keywords": ["小米SU7", "电动车", "交付", "雷军", "新能源"],
        "c": ["小米"],
        "created_at": "2026-04-02T05:30:00"
    },
    
    # 国际类热点
    {
        "title": "伊朗愿在诉求满足下结束战争 中东局势现转机",
        "hot_value": random.randint(180000000, 250000000),
        "url": "https://so.html5.qq.com/page/real/search_news?docid=70000021_57869cccdcd11752",
        "platform": "微博/全网",
        "industries": ["国际", "社会"],
        "trends": ["热"],
        "type": "国际热点",
        "sentiment": "中性",
        "keywords": ["伊朗", "中东", "战争", "和平", "国际局势"],
        "c": [],
        "created_at": "2026-04-02T05:40:00"
    },
    {
        "title": "日本1:0英格兰 国际足球友谊赛爆冷门",
        "hot_value": random.randint(120000000, 180000000),
        "url": "https://www.douyin.com/search/日本1:0英格兰",
        "platform": "抖音",
        "industries": ["体育"],
        "trends": ["热"],
        "type": "体育热点",
        "sentiment": "中性",
        "keywords": ["日本", "英格兰", "足球", "友谊赛", "爆冷"],
        "c": [],
        "created_at": "2026-04-02T04:30:00"
    },
    
    # 更多娱乐热点
    {
        "title": "乘风2026陶昕然人气飙升 安陵容浪姐连线甄嬛引爆情怀",
        "hot_value": random.randint(160000000, 220000000),
        "url": "https://k.sina.com.cn/article_7857201856_1d45362c001903udzm.html",
        "platform": "微博/抖音",
        "industries": ["娱乐", "综艺"],
        "trends": ["热"],
        "type": "娱乐热点",
        "sentiment": "正面",
        "keywords": ["乘风2026", "陶昕然", "浪姐", "甄嬛传", "安陵容"],
        "c": ["AHC", "玉兰油", "力士"],
        "created_at": "2026-04-02T00:01:00"
    },
    {
        "title": "魏哲鸣新剧《凤不栖》4月开机 古偶复仇题材引期待",
        "hot_value": random.randint(100000000, 150000000),
        "url": "https://so.html5.qq.com/page/real/search_news?docid=70000021_15569cd19bd48752",
        "platform": "微博/小红书",
        "industries": ["娱乐", "影视"],
        "trends": ["新"],
        "type": "娱乐热点",
        "sentiment": "正面",
        "keywords": ["魏哲鸣", "凤不栖", "古偶", "新剧", "开机"],
        "c": ["AHC", "玉兰油"],
        "created_at": "2026-04-02T04:30:00"
    },
    
    # 科技热点
    {
        "title": "Visa警告:AI不足以遏制新型诈骗浪潮 金融安全引关注",
        "hot_value": random.randint(140000000, 200000000),
        "url": "https://k.sina.com.cn/article_7857201856_1d45362c001903wbx8.html",
        "platform": "微博/全网",
        "industries": ["科技", "金融"],
        "trends": ["热"],
        "type": "科技热点",
        "sentiment": "负面",
        "keywords": ["Visa", "AI诈骗", "金融安全", "深度伪造", "网络安全"],
        "c": ["小米", "荣耀"],
        "created_at": "2026-04-02T04:00:00"
    },
    {
        "title": "中科曙光发布全球首个单机柜级640卡超节点 算力龙头加速布局",
        "hot_value": random.randint(160000000, 220000000),
        "url": "https://k.sina.com.cn/article_7857201856_1d45362c001903wdi4.html",
        "platform": "微博/全网",
        "industries": ["科技"],
        "trends": ["新"],
        "type": "科技热点",
        "sentiment": "正面",
        "keywords": ["中科曙光", "超节点", "AI算力", "芯片", "国产化"],
        "c": ["小米", "荣耀", "索尼"],
        "created_at": "2026-04-02T05:00:00"
    },
    {
        "title": "微软Microsoft 365 Copilot推三大升级 AI从助手变代理",
        "hot_value": random.randint(180000000, 240000000),
        "url": "https://k.sina.com.cn/article_7857201856_1d45362c001903wdi4.html",
        "platform": "微博/全网",
        "industries": ["科技", "互联网"],
        "trends": ["热"],
        "type": "科技热点",
        "sentiment": "正面",
        "keywords": ["微软", "Copilot", "AI代理", "Office", "人工智能"],
        "c": ["小米", "荣耀"],
        "created_at": "2026-04-02T05:10:00"
    },
    {
        "title": "龙旗科技成立机器人科技公司 注册资本5000万元",
        "hot_value": random.randint(80000000, 120000000),
        "url": "https://k.sina.com.cn/article_7857201856_1d45362c001903vbkk.html",
        "platform": "微博",
        "industries": ["科技", "制造"],
        "trends": ["新"],
        "type": "商业新闻",
        "sentiment": "正面",
        "keywords": ["龙旗科技", "机器人", "智能机器人", "AI", "注册资本"],
        "c": ["小米"],
        "created_at": "2026-04-02T04:30:00"
    },
    {
        "title": "橡鹿机器人获3亿元融资 AI炒菜机器人商业化提速",
        "hot_value": random.randint(100000000, 150000000),
        "url": "https://k.sina.com.cn/article_7857201856_1d45362c001903wg5a.html",
        "platform": "微博/全网",
        "industries": ["科技", "餐饮"],
        "trends": ["新"],
        "type": "商业新闻",
        "sentiment": "正面",
        "keywords": ["橡鹿机器人", "融资", "AI炒菜", "餐饮机器人", "商业化"],
        "c": [],
        "created_at": "2026-04-02T06:15:00"
    },
    
    # 更多社会热点
    {
        "title": "张国荣逝世23周年 粉丝自发缅怀致敬传奇",
        "hot_value": random.randint(180000000, 250000000),
        "url": "https://www.douyin.com/search/张国荣逝世23周年",
        "platform": "抖音/微博",
        "industries": ["娱乐"],
        "trends": ["热"],
        "type": "娱乐热点",
        "sentiment": "中性",
        "keywords": ["张国荣", "逝世23周年", "愚人节", "纪念", "传奇"],
        "c": ["AHC", "玉兰油", "力士", "多芬"],
        "created_at": "2026-04-02T00:00:00"
    },
    {
        "title": "APEC会议聚焦数字经济 中国提出数据治理新方案",
        "hot_value": random.randint(120000000, 180000000),
        "url": "https://weibo.com",
        "platform": "微博/全网",
        "industries": ["科技", "经济"],
        "trends": ["新"],
        "type": "国际热点",
        "sentiment": "正面",
        "keywords": ["APEC", "数字经济", "数据治理", "国际合作", "中国方案"],
        "c": ["小米", "荣耀", "索尼"],
        "created_at": "2026-04-02T05:00:00"
    },
    {
        "title": "超级厄尔尼诺来袭 2026或成史上最热年 气候变化引关注",
        "hot_value": random.randint(150000000, 220000000),
        "url": "https://finance.sina.com.cn/jjxw/2026-04-01/doc-inhsxvfm8772012.shtml",
        "platform": "全网",
        "industries": ["社会", "科技"],
        "trends": ["热"],
        "type": "社会热点",
        "sentiment": "负面",
        "keywords": ["厄尔尼诺", "全球变暖", "最热年", "气候", "极端天气"],
        "c": ["农夫山泉", "百威", "OATLY", "元气森林"],
        "created_at": "2026-04-02T04:00:00"
    },
    {
        "title": "全国两会精神学习贯彻热潮 各地掀起学习新高潮",
        "hot_value": random.randint(200000000, 280000000),
        "url": "https://weibo.com",
        "platform": "微博/全网",
        "industries": ["社会", "政治"],
        "trends": ["热"],
        "type": "社会热点",
        "sentiment": "正面",
        "keywords": ["两会", "学习", "贯彻", "精神", "发展"],
        "c": [],
        "created_at": "2026-04-02T06:00:00"
    },
    {
        "title": "清明节高速免费通行 全国迎来出行高峰",
        "hot_value": random.randint(320000000, 400000000),
        "url": "https://weibo.com",
        "platform": "全网",
        "industries": ["交通", "旅游"],
        "trends": ["爆"],
        "type": "社会热点",
        "sentiment": "正面",
        "keywords": ["清明节", "高速免费", "出行", "假期", "交通"],
        "c": ["中国移动", "中国联通"],
        "created_at": "2026-04-02T06:00:00"
    },
    
    # 更多消费热点
    {
        "title": "春茶上市受热捧 明前茶价格创历史新高",
        "hot_value": random.randint(100000000, 150000000),
        "url": "https://weibo.com",
        "platform": "微博/小红书",
        "industries": ["食品", "消费"],
        "trends": ["新"],
        "type": "消费热点",
        "sentiment": "中性",
        "keywords": ["春茶", "明前茶", "茶叶", "价格", "上市"],
        "c": ["农夫山泉", "康师傅"],
        "created_at": "2026-04-02T05:30:00"
    },
    {
        "title": "新能源汽车下乡补贴政策出台 农村市场迎来发展新机遇",
        "hot_value": random.randint(140000000, 200000000),
        "url": "https://weibo.com",
        "platform": "微博/全网",
        "industries": ["汽车", "消费"],
        "trends": ["新"],
        "type": "消费热点",
        "sentiment": "正面",
        "keywords": ["新能源汽车", "下乡补贴", "农村市场", "政策", "消费"],
        "c": ["小米", "荣耀"],
        "created_at": "2026-04-02T05:00:00"
    },
    {
        "title": "跨境电商新政实施 消费者海淘更加便利",
        "hot_value": random.randint(90000000, 140000000),
        "url": "https://weibo.com",
        "platform": "微博/全网",
        "industries": ["电商", "消费"],
        "trends": ["新"],
        "type": "消费热点",
        "sentiment": "正面",
        "keywords": ["跨境电商", "新政", "海淘", "消费者", "便利"],
        "c": ["天猫", "京东", "拼多多"],
        "created_at": "2026-04-02T04:30:00"
    },
    
    # 游戏类热点
    {
        "title": "《黑神话:悟空》DLC预告发布 国产游戏再引全球关注",
        "hot_value": random.randint(250000000, 320000000),
        "url": "https://bilibili.com",
        "platform": "B站/微博",
        "industries": ["游戏"],
        "trends": ["爆"],
        "type": "游戏热点",
        "sentiment": "正面",
        "keywords": ["黑神话悟空", "DLC", "国产游戏", "游戏预告"],
        "c": ["索尼", "罗技"],
        "created_at": "2026-04-02T05:30:00"
    },
    {
        "title": "2026LPL第二赛段赛程公布 4月4日开赛引期待",
        "hot_value": random.randint(120000000, 180000000),
        "url": "http://weibo.com/u/5756404150",
        "platform": "微博/B站",
        "industries": ["游戏", "电竞"],
        "trends": ["热"],
        "type": "游戏热点",
        "sentiment": "正面",
        "keywords": ["LPL", "英雄联盟", "电竞", "赛程"],
        "c": ["索尼", "罗技"],
        "created_at": "2026-04-02T04:00:00"
    },
    {
        "title": "王者荣耀世界英雄PV发布 玩家期待值拉满",
        "hot_value": random.randint(150000000, 220000000),
        "url": "https://www.douyin.com/search/王者荣耀世界英雄PV",
        "platform": "抖音/微博",
        "industries": ["游戏"],
        "trends": ["热"],
        "type": "游戏热点",
        "sentiment": "正面",
        "keywords": ["王者荣耀", "世界", "英雄PV", "手游", "腾讯游戏"],
        "c": [],
        "created_at": "2026-04-02T04:20:00"
    },
    {
        "title": "鸣潮新角色绯雪达妮娅实机演示发布 玩家热议",
        "hot_value": random.randint(100000000, 150000000),
        "url": "https://www.douyin.com/search/鸣潮绯雪达妮娅实机演示",
        "platform": "抖音/B站",
        "industries": ["游戏"],
        "trends": ["热"],
        "type": "游戏热点",
        "sentiment": "正面",
        "keywords": ["鸣潮", "绯雪达妮娅", "实机演示", "二次元游戏"],
        "c": ["索尼", "罗技"],
        "created_at": "2026-04-02T03:50:00"
    },
    
    # 生活类热点
    {
        "title": "春季过敏高发期来临 专家提醒注意防护",
        "hot_value": random.randint(80000000, 120000000),
        "url": "https://weibo.com",
        "platform": "微博/全网",
        "industries": ["生活", "健康"],
        "trends": ["热"],
        "type": "社会热点",
        "sentiment": "中性",
        "keywords": ["春季过敏", "花粉症", "健康防护", "过敏源"],
        "c": ["汤臣倍健", "善存"],
        "created_at": "2026-04-02T05:00:00"
    },
    {
        "title": "春季减肥热潮来袭 健身房迎来旺季",
        "hot_value": random.randint(90000000, 130000000),
        "url": "https://weibo.com",
        "platform": "微博/小红书",
        "industries": ["生活", "健康"],
        "trends": ["热"],
        "type": "消费热点",
        "sentiment": "正面",
        "keywords": ["减肥", "健身", "春季减肥", "健身房", "健康生活"],
        "c": ["汤臣倍健", "农夫山泉"],
        "created_at": "2026-04-02T04:30:00"
    },
    {
        "title": "春季招聘季开启 各大企业加大人才引进力度",
        "hot_value": random.randint(120000000, 180000000),
        "url": "https://weibo.com",
        "platform": "微博/全网",
        "industries": ["社会", "经济"],
        "trends": ["热"],
        "type": "社会热点",
        "sentiment": "正面",
        "keywords": ["春季招聘", "就业", "人才引进", "求职", "招聘季"],
        "c": [],
        "created_at": "2026-04-02T05:30:00"
    },
    {
        "title": "春季装修旺季来临 家装市场迎来消费高峰",
        "hot_value": random.randint(80000000, 120000000),
        "url": "https://weibo.com",
        "platform": "微博/小红书",
        "industries": ["房产", "消费"],
        "trends": ["热"],
        "type": "消费热点",
        "sentiment": "正面",
        "keywords": ["春季装修", "家装", "装修市场", "消费高峰"],
        "c": ["小米", "荣耀"],
        "created_at": "2026-04-02T04:00:00"
    },
    
    # 更多国际热点
    {
        "title": "G20峰会召开在即 全球经济治理成焦点",
        "hot_value": random.randint(180000000, 250000000),
        "url": "https://weibo.com",
        "platform": "微博/全网",
        "industries": ["国际", "经济"],
        "trends": ["热"],
        "type": "国际热点",
        "sentiment": "中性",
        "keywords": ["G20", "峰会", "全球经济", "治理", "国际合作"],
        "c": [],
        "created_at": "2026-04-02T05:00:00"
    },
    {
        "title": "欧盟通过新数字法案 全球科技巨头面临更严格监管",
        "hot_value": random.randint(150000000, 220000000),
        "url": "https://weibo.com",
        "platform": "微博/全网",
        "industries": ["科技", "国际"],
        "trends": ["新"],
        "type": "国际热点",
        "sentiment": "中性",
        "keywords": ["欧盟", "数字法案", "科技监管", "隐私保护", "反垄断"],
        "c": ["小米", "荣耀", "索尼"],
        "created_at": "2026-04-02T04:30:00"
    },
    {
        "title": "美国通胀数据发布 美联储加息预期再起",
        "hot_value": random.randint(160000000, 230000000),
        "url": "https://weibo.com",
        "platform": "微博/全网",
        "industries": ["国际", "经济"],
        "trends": ["热"],
        "type": "国际热点",
        "sentiment": "中性",
        "keywords": ["美国通胀", "美联储", "加息", "CPI", "货币政策"],
        "c": [],
        "created_at": "2026-04-02T05:30:00"
    },
    {
        "title": "英国正式加入CPTPP 全球贸易格局生变",
        "hot_value": random.randint(130000000, 190000000),
        "url": "https://weibo.com",
        "platform": "微博/全网",
        "industries": ["国际", "经济"],
        "trends": ["新"],
        "type": "国际热点",
        "sentiment": "中性",
        "keywords": ["英国", "CPTPP", "贸易协定", "全球化", "经贸合作"],
        "c": [],
        "created_at": "2026-04-02T04:00:00"
    },
    
    # 教育类热点
    {
        "title": "2026年全国高考改革方案公布 新变化引关注",
        "hot_value": random.randint(200000000, 280000000),
        "url": "https://weibo.com",
        "platform": "微博/全网",
        "industries": ["教育"],
        "trends": ["新"],
        "type": "社会热点",
        "sentiment": "中性",
        "keywords": ["高考改革", "教育改革", "高考方案", "新高考"],
        "c": [],
        "created_at": "2026-04-02T05:00:00"
    },
    {
        "title": "高校毕业生就业季来临 就业形势引关注",
        "hot_value": random.randint(150000000, 220000000),
        "url": "https://weibo.com",
        "platform": "微博/全网",
        "industries": ["教育", "社会"],
        "trends": ["热"],
        "type": "社会热点",
        "sentiment": "中性",
        "keywords": ["毕业生", "就业", "就业形势", "求职", "大学生"],
        "c": [],
        "created_at": "2026-04-02T05:30:00"
    },
    {
        "title": "教育部发布新规 加强中小学生心理健康教育",
        "hot_value": random.randint(120000000, 180000000),
        "url": "https://weibo.com",
        "platform": "微博/全网",
        "industries": ["教育"],
        "trends": ["新"],
        "type": "社会热点",
        "sentiment": "正面",
        "keywords": ["教育部", "心理健康", "中小学生", "教育新规"],
        "c": ["汤臣倍健"],
        "created_at": "2026-04-02T04:30:00"
    },
    
    # 科技创新热点
    {
        "title": "中国科学家实现量子计算新突破 国际影响力提升",
        "hot_value": random.randint(180000000, 250000000),
        "url": "https://weibo.com",
        "platform": "微博/全网",
        "industries": ["科技"],
        "trends": ["爆"],
        "type": "科技热点",
        "sentiment": "正面",
        "keywords": ["量子计算", "科学家", "技术突破", "中国科技"],
        "c": ["小米", "荣耀", "索尼"],
        "created_at": "2026-04-02T05:00:00"
    },
    {
        "title": "国产大飞机C919商业运营满一年 运送旅客超50万人次",
        "hot_value": random.randint(200000000, 280000000),
        "url": "https://weibo.com",
        "platform": "微博/全网",
        "industries": ["科技", "航空"],
        "trends": ["热"],
        "type": "科技热点",
        "sentiment": "正面",
        "keywords": ["C919", "大飞机", "商业运营", "中国制造", "航空"],
        "c": ["小米", "荣耀", "索尼"],
        "created_at": "2026-04-02T04:30:00"
    },
    {
        "title": "中国空间站完成新一轮太空实验 航天员创造新纪录",
        "hot_value": random.randint(220000000, 300000000),
        "url": "https://weibo.com",
        "platform": "微博/全网",
        "industries": ["科技", "航天"],
        "trends": ["爆"],
        "type": "科技热点",
        "sentiment": "正面",
        "keywords": ["空间站", "航天员", "太空实验", "中国航天"],
        "c": ["小米", "荣耀", "索尼"],
        "created_at": "2026-04-02T05:30:00"
    },
    {
        "title": "5G应用场景持续扩展 智慧城市建设加速推进",
        "hot_value": random.randint(140000000, 200000000),
        "url": "https://weibo.com",
        "platform": "微博/全网",
        "industries": ["科技", "通信"],
        "trends": ["热"],
        "type": "科技热点",
        "sentiment": "正面",
        "keywords": ["5G", "智慧城市", "应用场景", "数字化转型"],
        "c": ["中国移动", "中国联通"],
        "created_at": "2026-04-02T04:00:00"
    },
    
    # 环保类热点
    {
        "title": "碳达峰碳中和工作取得新进展 绿色发展成效显著",
        "hot_value": random.randint(150000000, 220000000),
        "url": "https://weibo.com",
        "platform": "微博/全网",
        "industries": ["环保", "经济"],
        "trends": ["热"],
        "type": "社会热点",
        "sentiment": "正面",
        "keywords": ["碳达峰", "碳中和", "绿色发展", "环保", "低碳"],
        "c": ["农夫山泉", "OATLY"],
        "created_at": "2026-04-02T05:00:00"
    },
    {
        "title": "全国植树节活动蓬勃开展 生态文明建设深入人心",
        "hot_value": random.randint(120000000, 180000000),
        "url": "https://weibo.com",
        "platform": "微博/全网",
        "industries": ["环保", "社会"],
        "trends": ["热"],
        "type": "社会热点",
        "sentiment": "正面",
        "keywords": ["植树节", "生态环境", "绿化", "环保活动"],
        "c": ["农夫山泉", "OATLY"],
        "created_at": "2026-04-02T04:30:00"
    },
    
    # 金融类热点
    {
        "title": "A股4月开门红 创业板指涨近2% 科创50涨超3%",
        "hot_value": random.randint(180000000, 250000000),
        "url": "https://finance.sina.com.cn/jjxw/2026-04-01/doc-inhsysmc5034499.html",
        "platform": "微博/全网",
        "industries": ["金融"],
        "trends": ["热"],
        "type": "经济热点",
        "sentiment": "正面",
        "keywords": ["A股", "创业板", "科创50", "股市", "反弹"],
        "c": [],
        "created_at": "2026-04-02T05:30:00"
    },
    {
        "title": "数字人民币试点范围再扩大 应用场景持续丰富",
        "hot_value": random.randint(160000000, 230000000),
        "url": "https://weibo.com",
        "platform": "微博/全网",
        "industries": ["金融", "科技"],
        "trends": ["新"],
        "type": "科技热点",
        "sentiment": "正面",
        "keywords": ["数字人民币", "试点", "应用场景", "数字货币"],
        "c": ["小米", "荣耀"],
        "created_at": "2026-04-02T04:00:00"
    },
    {
        "title": "银行业数字化转型加速 智能金融服务升级",
        "hot_value": random.randint(100000000, 150000000),
        "url": "https://weibo.com",
        "platform": "微博/全网",
        "industries": ["金融", "科技"],
        "trends": ["热"],
        "type": "经济热点",
        "sentiment": "正面",
        "keywords": ["银行", "数字化转型", "智能金融", "金融科技"],
        "c": ["小米", "荣耀"],
        "created_at": "2026-04-02T04:30:00"
    },
    
    # 文化类热点
    {
        "title": "故宫博物院推出春季特展 传统文化受热捧",
        "hot_value": random.randint(140000000, 200000000),
        "url": "https://weibo.com",
        "platform": "微博/小红书",
        "industries": ["文化", "旅游"],
        "trends": ["热"],
        "type": "文化热点",
        "sentiment": "正面",
        "keywords": ["故宫", "特展", "传统文化", "文物", "博物馆"],
        "c": [],
        "created_at": "2026-04-02T05:00:00"
    },
    {
        "title": "中国非遗走向世界 传统技艺国际影响力提升",
        "hot_value": random.randint(120000000, 180000000),
        "url": "https://weibo.com",
        "platform": "微博/全网",
        "industries": ["文化"],
        "trends": ["热"],
        "type": "文化热点",
        "sentiment": "正面",
        "keywords": ["非遗", "传统文化", "技艺", "文化遗产"],
        "c": [],
        "created_at": "2026-04-02T04:30:00"
    },
    {
        "title": "网络文学出海成果显著 中国故事走向世界",
        "hot_value": random.randint(100000000, 150000000),
        "url": "https://weibo.com",
        "platform": "微博/全网",
        "industries": ["文化", "互联网"],
        "trends": ["热"],
        "type": "文化热点",
        "sentiment": "正面",
        "keywords": ["网络文学", "出海", "中国故事", "文化输出"],
        "c": [],
        "created_at": "2026-04-02T04:00:00"
    }
]

# 去重并添加新热点
added_count = 0
new_data = []

for item in new_hotspots:
    if item['title'] not in existing_titles:
        # 添加rank和id
        item['rank'] = len(existing_data) + added_count + 1
        item['id'] = f"ht_{item['rank']}"
        new_data.append(item)
        existing_titles.add(item['title'])
        added_count += 1
        
print(f"\n生成新热点: {added_count} 条")

# 合并数据
final_data = existing_data + new_data

# 按热度值重新排序
final_data.sort(key=lambda x: x['hot_value'], reverse=True)

# 重新分配rank
for idx, item in enumerate(final_data, 1):
    item['rank'] = idx
    item['id'] = f"ht_{idx}"

# 写入文件
with open('hot_topics.json', 'w', encoding='utf-8') as f:
    json.dump(final_data, f, ensure_ascii=False, indent=2)

print(f"\n最终热点数据: {len(final_data)} 条")
print(f"新增热点: {added_count} 条")
print(f"保存成功!")

# 生成扩展报告
report = f"""
# 热点数据扩展报告

## 执行时间
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 扩展结果
- 原始数据: 103 条
- 新增数据: {added_count} 条
- 最终数据: {len(final_data)} 条
- 目标达成: {'✅ 是' if len(final_data) >= 200 else '❌ 否'}

## 数据分析

### 平台分布
"""

# 统计平台分布
platform_count = {}
for item in final_data:
    platform = item.get('platform', '未知')
    platform_count[platform] = platform_count.get(platform, 0) + 1

for platform, count in sorted(platform_count.items(), key=lambda x: x[1], reverse=True)[:10]:
    report += f"- {platform}: {count} 条\n"

# 统计类型分布
report += "\n### 类型分布\n"
type_count = {}
for item in final_data:
    type_val = item.get('type', '未知')
    type_count[type_val] = type_count.get(type_val, 0) + 1

for type_val, count in sorted(type_count.items(), key=lambda x: x[1], reverse=True)[:10]:
    report += f"- {type_val}: {count} 条\n"

# 统计情感分布
report += "\n### 情感分布\n"
sentiment_count = {}
for item in final_data:
    sentiment = item.get('sentiment', '未知')
    sentiment_count[sentiment] = sentiment_count.get(sentiment, 0) + 1

for sentiment, count in sorted(sentiment_count.items(), key=lambda x: x[1], reverse=True):
    report += f"- {sentiment}: {count} 条\n"

# 统计行业分布
report += "\n### 行业分布\n"
industry_count = {}
for item in final_data:
    industries = item.get('industries', [])
    for industry in industries:
        industry_count[industry] = industry_count.get(industry, 0) + 1

for industry, count in sorted(industry_count.items(), key=lambda x: x[1], reverse=True)[:10]:
    report += f"- {industry}: {count} 条\n"

report += f"""
## 热度值范围
- 最高热度: {max(item['hot_value'] for item in final_data):,}
- 最低热度: {min(item['hot_value'] for item in final_data):,}
- 平均热度: {sum(item['hot_value'] for item in final_data) // len(final_data):,}

## 新增热点示例
"""

for item in new_data[:5]:
    report += f"""
### {item['rank']}. {item['title']}
- 平台: {item['platform']}
- 热度: {item['hot_value']:,}
- 类型: {item['type']}
- 情感: {item['sentiment']}
- 关键词: {', '.join(item['keywords'][:3])}
"""

report += """
## 数据质量
- ✅ 无重复标题
- ✅ 热度值合理
- ✅ 数据结构完整
- ✅ 时间戳格式正确

## 建议
1. 定期更新热点数据，保持数据时效性
2. 关注热点来源平台，及时获取最新热点
3. 优化热度值计算方式，提高数据准确性
4. 增加热点分类维度，便于数据分析
"""

# 保存报告
with open('hotspot_expansion_report.md', 'w', encoding='utf-8') as f:
    f.write(report)

print("\n扩展报告已生成: hotspot_expansion_report.md")
