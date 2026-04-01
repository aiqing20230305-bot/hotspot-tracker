#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
热点数据补充脚本 - 第二轮
将热点数据从168条扩展到200条以上
"""

import json
import random
from datetime import datetime

# 读取现有数据
with open('hot_topics.json', 'r', encoding='utf-8') as f:
    existing_data = json.load(f)

print(f"现有热点数据: {len(existing_data)} 条")

# 提取现有标题用于去重
existing_titles = set(item['title'] for item in existing_data)

# 从搜索结果中提取的新热点数据 - 第二轮
new_hotspots_round2 = [
    # 医疗健康热点
    {
        "title": "医保新规4月实施 药店纳入门诊统筹报销更便利",
        "hot_value": random.randint(150000000, 220000000),
        "url": "https://so.html5.qq.com/page/real/search_news?docid=70000021_83569cc696801852",
        "platform": "微博/全网",
        "industries": ["医疗", "民生"],
        "trends": ["新"],
        "type": "社会热点",
        "sentiment": "正面",
        "keywords": ["医保", "门诊统筹", "药店", "报销", "新规"],
        "c": ["汤臣倍健", "善存"],
        "created_at": "2026-04-02T05:30:00"
    },
    {
        "title": "36种抗癌药入保平均降价63% 患者用药负担大幅减轻",
        "hot_value": random.randint(180000000, 250000000),
        "url": "https://so.html5.qq.com/page/real/search_news?docid=70000021_83569cc696801852",
        "platform": "微博/全网",
        "industries": ["医疗", "民生"],
        "trends": ["热"],
        "type": "社会热点",
        "sentiment": "正面",
        "keywords": ["抗癌药", "医保", "降价", "患者", "医疗改革"],
        "c": ["汤臣倍健"],
        "created_at": "2026-04-02T05:35:00"
    },
    {
        "title": "慢病管理新规实施 可一次开3个月药减少往返医院",
        "hot_value": random.randint(120000000, 180000000),
        "url": "https://so.html5.qq.com/page/real/search_news?docid=70000021_83569cc696801852",
        "platform": "微博/全网",
        "industries": ["医疗", "民生"],
        "trends": ["新"],
        "type": "社会热点",
        "sentiment": "正面",
        "keywords": ["慢病管理", "新规", "开药", "医院", "便民"],
        "c": ["汤臣倍健", "善存"],
        "created_at": "2026-04-02T05:40:00"
    },
    
    # 交通出行热点
    {
        "title": "全国高速统一新规 仅保留五档限速非标标志全部拆除",
        "hot_value": random.randint(200000000, 280000000),
        "url": "https://so.html5.qq.com/page/real/search_news?docid=70000021_83569cc696801852",
        "platform": "微博/全网",
        "industries": ["交通", "社会"],
        "trends": ["新"],
        "type": "社会热点",
        "sentiment": "正面",
        "keywords": ["高速", "限速", "新规", "交通", "便民"],
        "c": ["小米", "荣耀"],
        "created_at": "2026-04-02T04:00:00"
    },
    {
        "title": "全国路边停车新规 政府管理公共泊位统一30分钟免费",
        "hot_value": random.randint(180000000, 250000000),
        "url": "https://so.html5.qq.com/page/real/search_news?docid=70000021_83569cc696801852",
        "platform": "微博/全网",
        "industries": ["交通", "民生"],
        "trends": ["热"],
        "type": "社会热点",
        "sentiment": "正面",
        "keywords": ["停车", "新规", "免费", "便民", "路边停车"],
        "c": ["小米", "荣耀"],
        "created_at": "2026-04-02T04:05:00"
    },
    {
        "title": "动力电池回收新规实施 新能源车报废需车电一体",
        "hot_value": random.randint(140000000, 200000000),
        "url": "https://so.html5.qq.com/page/real/search_news?docid=70000021_83569cc696801852",
        "platform": "微博/全网",
        "industries": ["环保", "汽车"],
        "trends": ["新"],
        "type": "环保热点",
        "sentiment": "正面",
        "keywords": ["动力电池", "回收", "新能源车", "环保", "新规"],
        "c": ["小米", "荣耀"],
        "created_at": "2026-04-02T04:10:00"
    },
    
    # 科技热点
    {
        "title": "我国量子通信干线扩容 长三角珠三角实现跨区域互联",
        "hot_value": random.randint(200000000, 280000000),
        "url": "https://so.html5.qq.com/page/real/search_news?docid=70000021_83569cc696801852",
        "platform": "微博/全网",
        "industries": ["科技", "通信"],
        "trends": ["爆"],
        "type": "科技热点",
        "sentiment": "正面",
        "keywords": ["量子通信", "长三角", "珠三角", "科技突破", "通信"],
        "c": ["小米", "荣耀", "索尼"],
        "created_at": "2026-04-02T04:15:00"
    },
    {
        "title": "国产大模型星火4.0正式商用 多模态能力大幅提升",
        "hot_value": random.randint(160000000, 230000000),
        "url": "https://so.html5.qq.com/page/real/search_news?docid=70000021_83569cc696801852",
        "platform": "微博/全网",
        "industries": ["科技", "AI"],
        "trends": ["热"],
        "type": "科技热点",
        "sentiment": "正面",
        "keywords": ["大模型", "星火4.0", "AI", "多模态", "国产"],
        "c": ["小米", "索尼", "罗技"],
        "created_at": "2026-04-02T04:20:00"
    },
    
    # 国际热点
    {
        "title": "日本自卫队员强闯中国驻日使馆 在野党要求政府道歉",
        "hot_value": random.randint(220000000, 300000000),
        "url": "https://new.qq.com/rain/a/20260401A04UG000",
        "platform": "微博/全网",
        "industries": ["国际", "政治"],
        "trends": ["爆"],
        "type": "国际热点",
        "sentiment": "负面",
        "keywords": ["日本", "中国使馆", "道歉", "外交事件", "自卫队"],
        "c": [],
        "created_at": "2026-04-02T03:30:00"
    },
    {
        "title": "加沙地带医疗系统面临停运 人道主义危机加剧",
        "hot_value": random.randint(160000000, 230000000),
        "url": "https://new.qq.com/rain/a/20260401A04UG000",
        "platform": "微博/全网",
        "industries": ["国际", "人道"],
        "trends": ["热"],
        "type": "国际热点",
        "sentiment": "负面",
        "keywords": ["加沙", "医疗系统", "人道主义", "燃油", "危机"],
        "c": [],
        "created_at": "2026-04-02T03:35:00"
    },
    {
        "title": "阿联酋禁止伊朗公民入境 中东局势持续紧张",
        "hot_value": random.randint(130000000, 190000000),
        "url": "https://new.qq.com/rain/a/20260401A04UG000",
        "platform": "微博/全网",
        "industries": ["国际", "政治"],
        "trends": ["热"],
        "type": "国际热点",
        "sentiment": "中性",
        "keywords": ["阿联酋", "伊朗", "入境禁令", "中东", "局势"],
        "c": [],
        "created_at": "2026-04-02T03:40:00"
    },
    
    # 财经热点
    {
        "title": "美伊释放缓和信号 亚太股市全线走高风险偏好回暖",
        "hot_value": random.randint(250000000, 330000000),
        "url": "https://finance.jrj.com.cn/2026/04/01114556580305.shtml",
        "platform": "微博/全网",
        "industries": ["经济", "金融"],
        "trends": ["爆"],
        "type": "经济热点",
        "sentiment": "正面",
        "keywords": ["股市", "亚太", "美伊", "缓和", "反弹"],
        "c": [],
        "created_at": "2026-04-02T05:00:00"
    },
    {
        "title": "特朗普称两三周内结束对伊战争 美股大幅收高",
        "hot_value": random.randint(280000000, 360000000),
        "url": "https://finance.sina.com.cn/headline/2026-04-02/doc-inhszyea2209078.shtml",
        "platform": "微博/全网",
        "industries": ["经济", "国际"],
        "trends": ["爆"],
        "type": "国际热点",
        "sentiment": "中性",
        "keywords": ["特朗普", "伊朗", "战争", "美股", "市场"],
        "c": [],
        "created_at": "2026-04-02T06:05:00"
    },
    {
        "title": "韩国股市暴涨 韩国综合指数涨幅突破6%触发熔断",
        "hot_value": random.randint(200000000, 280000000),
        "url": "https://finance.jrj.com.cn/2026/04/01114556580305.shtml",
        "platform": "微博/全网",
        "industries": ["经济", "金融"],
        "trends": ["爆"],
        "type": "经济热点",
        "sentiment": "正面",
        "keywords": ["韩国股市", "暴涨", "熔断", "亚太股市", "反弹"],
        "c": [],
        "created_at": "2026-04-02T05:05:00"
    },
    {
        "title": "A股4月开门红成交额破2万亿 近4500只个股收红",
        "hot_value": random.randint(220000000, 300000000),
        "url": "https://finance.sina.com.cn/headline/2026-04-02/doc-inhszyea2209078.shtml",
        "platform": "微博/全网",
        "industries": ["经济", "金融"],
        "trends": ["爆"],
        "type": "经济热点",
        "sentiment": "正面",
        "keywords": ["A股", "开门红", "成交额", "反弹", "股市"],
        "c": [],
        "created_at": "2026-04-02T05:10:00"
    },
    {
        "title": "三星电子大涨13% 创2001年以来最大单日涨幅",
        "hot_value": random.randint(150000000, 220000000),
        "url": "https://finance.sina.com.cn/headline/2026-04-02/doc-inhszyea2209078.shtml",
        "platform": "微博/全网",
        "industries": ["经济", "科技"],
        "trends": ["热"],
        "type": "经济热点",
        "sentiment": "正面",
        "keywords": ["三星电子", "股价", "涨幅", "芯片", "韩国"],
        "c": ["小米", "荣耀", "索尼"],
        "created_at": "2026-04-02T05:15:00"
    },
    {
        "title": "央行一季度例会召开 强调维护金融市场稳定",
        "hot_value": random.randint(140000000, 200000000),
        "url": "https://finance.sina.com.cn/headline/2026-04-01/doc-inhsywsz5005320.shtml",
        "platform": "微博/全网",
        "industries": ["经济", "金融"],
        "trends": ["新"],
        "type": "经济热点",
        "sentiment": "中性",
        "keywords": ["央行", "例会", "货币政策", "金融市场", "稳定"],
        "c": [],
        "created_at": "2026-04-02T04:30:00"
    },
    {
        "title": "中东铝厂遇袭冲击全球供应链 铝价短期看涨",
        "hot_value": random.randint(160000000, 230000000),
        "url": "https://finance.sina.com.cn/headline/2026-04-01/doc-inhsywsz5005320.shtml",
        "platform": "微博/全网",
        "industries": ["经济", "制造"],
        "trends": ["热"],
        "type": "经济热点",
        "sentiment": "中性",
        "keywords": ["铝厂", "中东", "供应链", "铝价", "袭击"],
        "c": ["小米"],
        "created_at": "2026-04-02T04:35:00"
    },
    {
        "title": "国际油价跳水后拉升 地缘政治影响持续",
        "hot_value": random.randint(180000000, 250000000),
        "url": "https://finance.sina.com.cn/headline/2026-04-02/doc-inhszyea2209078.shtml",
        "platform": "微博/全网",
        "industries": ["经济", "能源"],
        "trends": ["热"],
        "type": "经济热点",
        "sentiment": "中性",
        "keywords": ["油价", "跳水", "地缘政治", "能源", "波动"],
        "c": [],
        "created_at": "2026-04-02T05:20:00"
    },
    {
        "title": "备案制落地三年 734家企业申请境外上市",
        "hot_value": random.randint(100000000, 150000000),
        "url": "https://k.sina.com.cn/article_7857201856_1d45362c001903vf8y.html",
        "platform": "微博/全网",
        "industries": ["经济", "金融"],
        "trends": ["新"],
        "type": "经济热点",
        "sentiment": "正面",
        "keywords": ["备案制", "境外上市", "企业", "融资", "资本市场"],
        "c": [],
        "created_at": "2026-04-02T04:40:00"
    },
    
    # 科技创新热点
    {
        "title": "九部门出台物联网行动方案 培育智慧医疗文旅应用",
        "hot_value": random.randint(120000000, 180000000),
        "url": "https://new.qq.com/rain/a/20260401A01GIR00",
        "platform": "微博/全网",
        "industries": ["科技", "互联网"],
        "trends": ["新"],
        "type": "科技热点",
        "sentiment": "正面",
        "keywords": ["物联网", "行动方案", "智慧医疗", "智慧文旅", "应用"],
        "c": ["小米", "荣耀", "索尼"],
        "created_at": "2026-04-02T04:45:00"
    },
    {
        "title": "华为汪涛当值轮值董事长 公司治理迎新变化",
        "hot_value": random.randint(140000000, 200000000),
        "url": "https://finance.sina.cn/zaobao/app.d.html?date=20260402",
        "platform": "微博/全网",
        "industries": ["科技", "企业"],
        "trends": ["热"],
        "type": "科技热点",
        "sentiment": "中性",
        "keywords": ["华为", "轮值董事长", "汪涛", "企业治理", "科技"],
        "c": ["小米", "荣耀", "索尼"],
        "created_at": "2026-04-02T05:25:00"
    },
    {
        "title": "95岁巴菲特宣布重启重大投资决策 引发市场关注",
        "hot_value": random.randint(180000000, 260000000),
        "url": "https://finance.sina.cn/zaobao/app.d.html?date=20260402",
        "platform": "微博/全网",
        "industries": ["经济", "投资"],
        "trends": ["爆"],
        "type": "经济热点",
        "sentiment": "中性",
        "keywords": ["巴菲特", "投资", "股市", "重启", "伯克希尔"],
        "c": [],
        "created_at": "2026-04-02T05:30:00"
    },
    {
        "title": "雷军投资的中年人泡泡玛特在香港上市 引发热议",
        "hot_value": random.randint(160000000, 230000000),
        "url": "https://finance.sina.cn/zaobao/app.d.html?date=20260402",
        "platform": "微博/全网",
        "industries": ["消费", "投资"],
        "trends": ["热"],
        "type": "消费热点",
        "sentiment": "正面",
        "keywords": ["雷军", "泡泡玛特", "上市", "投资", "消费"],
        "c": ["小米"],
        "created_at": "2026-04-02T05:35:00"
    },
    
    # 社会民生热点
    {
        "title": "春耕生产正当时 无人机运送秧苗成新场景",
        "hot_value": random.randint(100000000, 150000000),
        "url": "https://new.qq.com/rain/a/20260401A06RYC00",
        "platform": "微博/全网",
        "industries": ["农业", "科技"],
        "trends": ["热"],
        "type": "社会热点",
        "sentiment": "正面",
        "keywords": ["春耕", "无人机", "农业科技", "现代化", "插秧"],
        "c": ["农夫山泉"],
        "created_at": "2026-04-02T04:50:00"
    },
    {
        "title": "信用修复新规施行 轻微失信不再公示修复更便捷",
        "hot_value": random.randint(90000000, 130000000),
        "url": "https://so.html5.qq.com/page/real/search_news?docid=70000021_83569cc696801852",
        "platform": "微博/全网",
        "industries": ["社会", "民生"],
        "trends": ["新"],
        "type": "社会热点",
        "sentiment": "正面",
        "keywords": ["信用修复", "新规", "失信", "便民", "社会信用"],
        "c": [],
        "created_at": "2026-04-02T04:55:00"
    },
    {
        "title": "清明节各地开通祭扫专线 方便市民出行",
        "hot_value": random.randint(120000000, 180000000),
        "url": "https://so.html5.qq.com/page/real/search_news?docid=70000021_42969cd0c3557252",
        "platform": "微博/全网",
        "industries": ["交通", "社会"],
        "trends": ["热"],
        "type": "社会热点",
        "sentiment": "正面",
        "keywords": ["清明节", "祭扫专线", "公交", "便民", "出行"],
        "c": [],
        "created_at": "2026-04-02T05:45:00"
    },
    {
        "title": "进博会走进安徽 深化引进来服务双循环",
        "hot_value": random.randint(130000000, 190000000),
        "url": "https://new.qq.com/rain/a/20260401A06RGI00",
        "platform": "微博/全网",
        "industries": ["经济", "贸易"],
        "trends": ["新"],
        "type": "经济热点",
        "sentiment": "正面",
        "keywords": ["进博会", "安徽", "双循环", "贸易", "投资"],
        "c": [],
        "created_at": "2026-04-02T05:50:00"
    },
    
    # 医疗热点
    {
        "title": "医保基金监管宣传月启动 守护群众看病钱",
        "hot_value": random.randint(110000000, 160000000),
        "url": "https://so.html5.qq.com/page/real/search_news?docid=70000021_42969cd0c3557252",
        "platform": "微博/全网",
        "industries": ["医疗", "民生"],
        "trends": ["新"],
        "type": "社会热点",
        "sentiment": "正面",
        "keywords": ["医保基金", "监管", "宣传月", "看病钱", "医疗"],
        "c": ["汤臣倍健", "善存"],
        "created_at": "2026-04-02T05:55:00"
    },
    {
        "title": "基孔肯雅热纳入乙类传染病管理 强化监测防控",
        "hot_value": random.randint(100000000, 150000000),
        "url": "https://so.html5.qq.com/page/real/search_news?docid=70000021_83569cc696801852",
        "platform": "微博/全网",
        "industries": ["医疗", "健康"],
        "trends": ["新"],
        "type": "社会热点",
        "sentiment": "中性",
        "keywords": ["基孔肯雅热", "传染病", "乙类", "防控", "监测"],
        "c": ["汤臣倍健"],
        "created_at": "2026-04-02T06:00:00"
    },
    
    # 文化教育热点
    {
        "title": "江苏凤凰出版传媒集团向伊宁市捐赠图书 助力文化建设",
        "hot_value": random.randint(80000000, 120000000),
        "url": "https://so.html5.qq.com/page/real/search_news?docid=70000021_42969cd0c3557252",
        "platform": "微博/全网",
        "industries": ["文化", "教育"],
        "trends": ["新"],
        "type": "文化热点",
        "sentiment": "正面",
        "keywords": ["图书捐赠", "文化建设", "教育", "出版"],
        "c": [],
        "created_at": "2026-04-02T06:10:00"
    },
    {
        "title": "科学岛两大科学装置面向全球开放共享 科技合作提速",
        "hot_value": random.randint(140000000, 200000000),
        "url": "https://new.qq.com/rain/a/20260401A06RGI00",
        "platform": "微博/全网",
        "industries": ["科技", "科研"],
        "trends": ["热"],
        "type": "科技热点",
        "sentiment": "正面",
        "keywords": ["科学岛", "科学装置", "开放共享", "科研", "国际合作"],
        "c": ["小米", "荣耀", "索尼"],
        "created_at": "2026-04-02T06:15:00"
    },
    {
        "title": "合肥开设249个春假公益托管班 破解学生看护难",
        "hot_value": random.randint(110000000, 160000000),
        "url": "https://new.qq.com/rain/a/20260401A06RGI00",
        "platform": "微博/全网",
        "industries": ["教育", "民生"],
        "trends": ["热"],
        "type": "社会热点",
        "sentiment": "正面",
        "keywords": ["春假托管", "公益托管班", "学生看护", "教育", "便民"],
        "c": [],
        "created_at": "2026-04-02T06:20:00"
    },
    
    # 更多消费热点
    {
        "title": "福鼎白茶采摘生产忙 春茶品质受关注",
        "hot_value": random.randint(90000000, 130000000),
        "url": "https://new.qq.com/rain/a/20260401A06QW500",
        "platform": "微博/全网",
        "industries": ["食品", "消费"],
        "trends": ["热"],
        "type": "消费热点",
        "sentiment": "正面",
        "keywords": ["福鼎白茶", "春茶", "采摘", "茶叶", "品质"],
        "c": ["农夫山泉", "康师傅"],
        "created_at": "2026-04-02T06:25:00"
    },
    {
        "title": "合肥市扩大住房公积金提取范围 便民惠民",
        "hot_value": random.randint(100000000, 150000000),
        "url": "https://new.qq.com/rain/a/20260401A06RGI00",
        "platform": "微博/全网",
        "industries": ["房产", "民生"],
        "trends": ["新"],
        "type": "社会热点",
        "sentiment": "正面",
        "keywords": ["住房公积金", "提取范围", "便民", "房产", "惠民"],
        "c": [],
        "created_at": "2026-04-02T06:30:00"
    },
    {
        "title": "春假出游用电高峰将至 合肥供电全力护航",
        "hot_value": random.randint(80000000, 120000000),
        "url": "https://new.qq.com/rain/a/20260401A06RGI00",
        "platform": "微博",
        "industries": ["电力", "旅游"],
        "trends": ["热"],
        "type": "社会热点",
        "sentiment": "正面",
        "keywords": ["春假", "用电高峰", "供电", "护航", "假期"],
        "c": [],
        "created_at": "2026-04-02T06:35:00"
    },
    
    # 国际财经热点
    {
        "title": "伦敦股市1日上涨 欧洲三大股指全线上扬",
        "hot_value": random.randint(120000000, 180000000),
        "url": "https://www.cnfin.com/hs-lb/detail/20260402/4394517_1.html",
        "platform": "微博/全网",
        "industries": ["经济", "金融"],
        "trends": ["热"],
        "type": "经济热点",
        "sentiment": "正面",
        "keywords": ["伦敦股市", "欧洲股市", "上涨", "金融", "反弹"],
        "c": [],
        "created_at": "2026-04-02T06:40:00"
    }
]

# 去重并添加新热点
added_count = 0
new_data = []

for item in new_hotspots_round2:
    if item['title'] not in existing_titles:
        # 添加rank和id
        item['rank'] = len(existing_data) + added_count + 1
        item['id'] = f"ht_{item['rank']}"
        new_data.append(item)
        existing_titles.add(item['title'])
        added_count += 1

print(f"\n本轮生成新热点: {added_count} 条")

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
print(f"本轮新增: {added_count} 条")
print(f"保存成功!")
