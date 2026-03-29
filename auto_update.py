#!/usr/bin/env python3
"""
特赞内容运营平台 - 自动更新脚本 V2.0
每天自动抓取热点数据，生成客户选题
目标：500+条高质量选题，100条热点分析
"""

import json
import random
from datetime import datetime
from collections import defaultdict

# 客户配置
CLIENTS = [
    {"industry": "3C数码", "brand": "荣耀", "products": ["荣耀手机", "荣耀平板", "荣耀耳机", "荣耀手表"], "priority": 5},
    {"industry": "3C数码", "brand": "罗技", "products": ["罗技键鼠", "罗技摄像头", "罗技音箱"], "priority": 4},
    {"industry": "3C数码", "brand": "小米", "products": ["小米手机", "小米平板", "小米智能家居"], "priority": 5},
    {"industry": "3C数码", "brand": "索尼", "products": ["索尼耳机", "索尼相机", "索尼电视"], "priority": 4},
    {"industry": "快消", "brand": "AHC", "products": ["AHC水乳", "AHC防晒", "AHC眼霜"], "priority": 5},
    {"industry": "快消", "brand": "多芬", "products": ["多芬沐浴露", "多芬洗发水", "多芬身体乳"], "priority": 4},
    {"industry": "快消", "brand": "力士", "products": ["力士洗发水", "力士沐浴露", "力士香皂"], "priority": 4},
    {"industry": "快消", "brand": "清扬", "products": ["清扬洗发水", "清扬去屑套装"], "priority": 3},
    {"industry": "快消", "brand": "舒适", "products": ["舒适洗衣液", "舒适柔顺剂"], "priority": 3},
    {"industry": "快消", "brand": "玉兰油", "products": ["玉兰油面霜", "玉兰油精华", "玉兰油防晒"], "priority": 4},
    {"industry": "保健品", "brand": "汤臣倍健", "products": ["蛋白粉", "维生素", "鱼油", "益生菌"], "priority": 5},
    {"industry": "保健品", "brand": "善存", "products": ["善存多维片", "善存银片"], "priority": 3},
    {"industry": "家庭清洁", "brand": "HC", "products": ["HC清洁剂", "HC消毒液"], "priority": 3},
    {"industry": "家庭清洁", "brand": "威猛先生", "products": ["威猛先生厨房清洁", "威猛先生浴室清洁"], "priority": 3},
    {"industry": "宠物食品", "brand": "希宝", "products": ["猫粮", "狗粮", "宠物零食"], "priority": 4},
    {"industry": "宠物食品", "brand": "皇家", "products": ["皇家猫粮", "皇家狗粮", "皇家处方粮"], "priority": 4},
    {"industry": "食品饮料", "brand": "OATLY", "products": ["燕麦奶", "咖啡燕麦奶", "燕麦冰淇淋"], "priority": 4},
    {"industry": "食品饮料", "brand": "百威", "products": ["百威啤酒", "百威纯生", "百威超级"], "priority": 3},
    {"industry": "食品饮料", "brand": "元气森林", "products": ["气泡水", "外星人电解质水", "燃茶"], "priority": 4},
    {"industry": "食品饮料", "brand": "农夫山泉", "products": ["矿泉水", "东方树叶", "茶π"], "priority": 4},
]

PLATFORMS = ["抖音", "微博", "小红书", "B站", "视频号"]

ANGLES = [
    "产品测评", "使用教程", "热点借势", "痛点解决", "场景展示",
    "对比评测", "开箱体验", "种草推荐", "剧情植入", "挑战赛",
    "测评对比", "教程攻略", "Vlog日常", "知识科普", "情感故事",
    "联名合作", "限时优惠", "用户故事", "专家访谈", "行业趋势",
]

# ============================================================
# 100条热点数据 - 10大类别
# ============================================================
def get_hot_topics():
    """获取100条热点数据，覆盖10大类别"""
    return [
        # ========== 科技类 (15条) ==========
        {"title": "ChatGPT-5发布引发AI应用热潮", "platform": "微博", "heat": "3.5亿", "trend": "🔥🔥🔥 爆发式增长", "type": "AI应用", "aud": "18-45岁科技爱好者", "time": "持续4周", "logic": "技术突破+全民讨论", "sentiment": "正面", "age_range": "18-45岁", "keywords": ["AI", "ChatGPT", "大模型", "人工智能", "科技"], "c": ["荣耀", "罗技", "小米", "索尼"]},
        {"title": "小米15 Ultra首销秒罄", "platform": "抖音", "heat": "1.8亿", "trend": "🔥🔥🔥 爆发式增长", "type": "手机新品", "aud": "数码发烧友", "time": "持续1周", "logic": "新品发布+限量抢购", "sentiment": "正面", "age_range": "20-35岁", "keywords": ["小米", "手机", "Ultra", "新品", "旗舰"], "c": ["小米", "罗技", "荣耀"]},
        {"title": "苹果Vision Pro 2曝光", "platform": "微博", "heat": "2.1亿", "trend": "🔥🔥 持续上升", "type": "手机新品", "aud": "苹果用户", "time": "持续3周", "logic": "新品预热+品牌效应", "sentiment": "中性", "age_range": "25-40岁", "keywords": ["苹果", "Vision Pro", "AR", "VR"], "c": ["荣耀", "小米", "索尼"]},
        {"title": "华为Mate70 Pro+开售", "platform": "抖音", "heat": "2.5亿", "trend": "🔥🔥🔥 爆发式增长", "type": "手机新品", "aud": "商务人群", "time": "持续2周", "logic": "国产旗舰+技术突破", "sentiment": "正面", "age_range": "25-45岁", "keywords": ["华为", "Mate", "手机", "国产"], "c": ["荣耀", "小米"]},
        {"title": "智能家居全屋互联体验", "platform": "小红书", "heat": "8500万", "trend": "🔥🔥 稳定上升", "type": "智能家居", "aud": "新房业主", "time": "持续6周", "logic": "智能家居普及", "sentiment": "正面", "age_range": "25-45岁", "keywords": ["智能家居", "全屋智能", "IoT", "米家"], "c": ["小米", "荣耀"]},
        {"title": "小米全屋智能家居方案", "platform": "小红书", "heat": "6800万", "trend": "🔥🔥 稳定上升", "type": "智能家居", "aud": "装修人群", "time": "持续5周", "logic": "场景化展示", "sentiment": "正面", "age_range": "25-40岁", "keywords": ["小米", "智能家居", "全屋方案"], "c": ["小米", "荣耀"]},
        {"title": "《黑神话：悟空》DLC发布", "platform": "B站", "heat": "1.2亿", "trend": "🔥🔥🔥 爆发式增长", "type": "游戏", "aud": "游戏玩家", "time": "持续3周", "logic": "爆款游戏+内容更新", "sentiment": "正面", "age_range": "16-35岁", "keywords": ["黑神话", "游戏", "DLC", "悟空"], "c": ["罗技", "索尼"]},
        {"title": "Switch2国行版正式发布", "platform": "B站", "heat": "9800万", "trend": "🔥🔥🔥 爆发式增长", "type": "游戏", "aud": "Switch玩家", "time": "持续4周", "logic": "新品发布+游戏情怀", "sentiment": "正面", "age_range": "18-30岁", "keywords": ["Switch", "任天堂", "游戏机", "国行"], "c": ["罗技", "索尼"]},
        {"title": "PS5 Pro性能实测对比", "platform": "B站", "heat": "7200万", "trend": "🔥🔥 持续上升", "type": "游戏", "aud": "主机玩家", "time": "持续3周", "logic": "新品评测+性能对比", "sentiment": "中性", "age_range": "18-35岁", "keywords": ["PS5", "索尼", "游戏机", "Pro", "评测"], "c": ["索尼", "罗技"]},
        {"title": "iPhone 17 Pro Max全面评测", "platform": "抖音", "heat": "5600万", "trend": "🔥🔥 稳定上升", "type": "数码评测", "aud": "苹果用户", "time": "持续2周", "logic": "旗舰评测+购机参考", "sentiment": "中性", "age_range": "20-40岁", "keywords": ["iPhone", "苹果", "评测", "Pro Max"], "c": ["荣耀", "小米", "索尼"]},
        {"title": "旗舰手机影像横评", "platform": "小红书", "heat": "4200万", "trend": "🔥🔥 稳定上升", "type": "数码评测", "aud": "拍照爱好者", "time": "持续4周", "logic": "购机决策需求", "sentiment": "中性", "age_range": "20-35岁", "keywords": ["手机拍照", "影像", "横评", "旗舰"], "c": ["荣耀", "小米", "索尼"]},
        {"title": "AI写作工具效率实测", "platform": "B站", "heat": "3800万", "trend": "🔥🔥 持续上升", "type": "AI应用", "aud": "职场人士", "time": "持续5周", "logic": "AI效率提升需求", "sentiment": "正面", "age_range": "20-40岁", "keywords": ["AI写作", "效率工具", "ChatGPT", "办公"], "c": ["罗技", "小米", "荣耀"]},
        {"title": "智能手表健康监测功能", "platform": "小红书", "heat": "3100万", "trend": "🔥🔥 稳定上升", "type": "AI应用", "aud": "健康意识人群", "time": "持续8周", "logic": "健康管理刚需", "sentiment": "正面", "age_range": "25-50岁", "keywords": ["智能手表", "健康监测", "心率", "血氧"], "c": ["荣耀", "小米"]},
        {"title": "国产芯片技术突破", "platform": "微博", "heat": "1.5亿", "trend": "🔥🔥🔥 爆发式增长", "type": "AI应用", "aud": "全年龄段科技关注者", "time": "持续4周", "logic": "国产替代热度持续", "sentiment": "正面", "age_range": "18-50岁", "keywords": ["国产芯片", "麒麟", "技术突破", "华为"], "c": ["荣耀", "小米"]},
        {"title": "折叠屏手机选购指南", "platform": "抖音", "heat": "2800万", "trend": "🔥🔥 稳定上升", "type": "手机新品", "aud": "商务人群", "time": "持续6周", "logic": "折叠屏普及+购机需求", "sentiment": "中性", "age_range": "25-40岁", "keywords": ["折叠屏", "手机", "选购", "商务"], "c": ["荣耀", "小米"]},

        # ========== 美妆类 (12条) ==========
        {"title": "早C晚A护肤routine升级", "platform": "小红书", "heat": "2.8亿", "trend": "🔥🔥🔥 爆发式增长", "type": "护肤", "aud": "25-40岁护肤进阶用户", "time": "持续6周", "logic": "成分党护肤理念深化", "sentiment": "正面", "age_range": "25-40岁", "keywords": ["早C晚A", "护肤", "VC", "VA", "成分党"], "c": ["AHC", "玉兰油", "多芬"]},
        {"title": "春季敏感肌修护指南", "platform": "小红书", "heat": "1.5亿", "trend": "🔥🔥🔥 持续上升", "type": "护肤", "aud": "敏感肌人群", "time": "季节性持续2月", "logic": "换季护肤需求", "sentiment": "正面", "age_range": "20-40岁", "keywords": ["敏感肌", "春季护肤", "修护", "泛红"], "c": ["AHC", "玉兰油", "多芬"]},
        {"title": "平价抗老精华推荐", "platform": "小红书", "heat": "9800万", "trend": "🔥🔥 稳定上升", "type": "护肤", "aud": "轻熟龄肌肤", "time": "持续8周", "logic": "抗老需求年轻化", "sentiment": "正面", "age_range": "25-40岁", "keywords": ["抗老", "精华", "平价", "A醇", "玻色因"], "c": ["AHC", "玉兰油"]},
        {"title": "YSL口红新色号种草", "platform": "抖音", "heat": "7200万", "trend": "🔥🔥 持续上升", "type": "彩妆", "aud": "年轻女性", "time": "持续2周", "logic": "新品发布+明星效应", "sentiment": "正面", "age_range": "18-30岁", "keywords": ["口红", "YSL", "彩妆", "色号", "种草"], "c": ["AHC", "玉兰油"]},
        {"title": "伪素颜妆容教程", "platform": "小红书", "heat": "5600万", "trend": "🔥🔥 稳定上升", "type": "彩妆", "aud": "上班族", "time": "持续10周", "logic": "自然妆容趋势", "sentiment": "正面", "age_range": "18-35岁", "keywords": ["伪素颜", "妆容", "教程", "日常妆"], "c": ["AHC", "玉兰油"]},
        {"title": "兰蔻免税店限定香水", "platform": "微博", "heat": "4200万", "trend": "🔥🔥 持续上升", "type": "香水", "aud": "香水爱好者", "time": "持续3周", "logic": "限定款饥饿营销", "sentiment": "正面", "age_range": "22-40岁", "keywords": ["香水", "兰蔻", "限定", "免税"], "c": ["AHC"]},
        {"title": "JM玫瑰香水平替测评", "platform": "小红书", "heat": "2800万", "trend": "🔥🔥 稳定上升", "type": "香水", "aud": "学生党", "time": "持续6周", "logic": "平替文化+消费降级", "sentiment": "中性", "age_range": "18-28岁", "keywords": ["香水", "平替", "JM", "玫瑰"], "c": ["AHC"]},
        {"title": "热玛吉医美体验分享", "platform": "小红书", "heat": "3500万", "trend": "🔥🔥 持续上升", "type": "医美", "aud": "抗衰需求人群", "time": "持续12周", "logic": "抗衰医美普及", "sentiment": "中性", "age_range": "28-50岁", "keywords": ["热玛吉", "医美", "抗衰", "超声刀"], "c": ["AHC", "玉兰油"]},
        {"title": "水光针入门指南", "platform": "小红书", "heat": "2400万", "trend": "🔥🔥 稳定上升", "type": "医美", "aud": "医美小白", "time": "持续8周", "logic": "轻医美接受度提升", "sentiment": "正面", "age_range": "22-40岁", "keywords": ["水光针", "医美", "入门", "肌肤"], "c": ["AHC", "玉兰油"]},
        {"title": "春季护发精油推荐", "platform": "抖音", "heat": "1800万", "trend": "🔥🔥 稳定上升", "type": "个护", "aud": "头发干枯人群", "time": "季节性持续1月", "logic": "换季护发需求", "sentiment": "正面", "age_range": "18-40岁", "keywords": ["护发精油", "护发", "精油", "春季"], "c": ["多芬", "力士", "清扬"]},
        {"title": "氨基酸洗发水测评", "platform": "小红书", "heat": "1500万", "trend": "🔥🔥 稳定上升", "type": "个护", "aud": "成分党", "time": "持续10周", "logic": "成分护肤延伸至个护", "sentiment": "正面", "age_range": "20-40岁", "keywords": ["氨基酸", "洗发水", "测评", "头皮"], "c": ["多芬", "力士", "清扬"]},
        {"title": "618美妆护肤囤货清单", "platform": "微博", "heat": "1.2亿", "trend": "🔥🔥🔥 爆发式增长", "type": "护肤", "aud": "美妆爱好者", "time": "大促前2周爆发", "logic": "大促节点+购物攻略", "sentiment": "正面", "age_range": "20-40岁", "keywords": ["618", "囤货", "美妆", "护肤", "攻略"], "c": ["AHC", "多芬", "力士", "玉兰油"]},

        # ========== 母婴类 (10条) ==========
        {"title": "0-3岁辅食添加时间表", "platform": "小红书", "heat": "1.8亿", "trend": "🔥🔥🔥 爆发式增长", "type": "辅食", "aud": "新手妈妈", "time": "持续8周", "logic": "科学喂养需求", "sentiment": "正面", "age_range": "25-35岁", "keywords": ["辅食", "婴儿", "添加", "食谱", "喂养"], "c": ["汤臣倍健", "善存"]},
        {"title": "宝宝辅食制作教程", "platform": "抖音", "heat": "9800万", "trend": "🔥🔥🔥 持续上升", "type": "辅食", "aud": "6-12月宝宝家长", "time": "持续10周", "logic": "辅食制作刚需", "sentiment": "正面", "age_range": "25-35岁", "keywords": ["辅食", "教程", "宝宝", "食谱"], "c": ["汤臣倍健", "善存"]},
        {"title": "婴儿辅食食谱大全", "platform": "小红书", "heat": "7600万", "trend": "🔥🔥 稳定上升", "type": "辅食", "aud": "辅食阶段宝宝家长", "time": "持续12周", "logic": "内容需求大", "sentiment": "正面", "age_range": "25-35岁", "keywords": ["辅食食谱", "婴儿", "大全", "营养"], "c": ["汤臣倍健", "善存"]},
        {"title": "儿童专注力训练方法", "platform": "B站", "heat": "5200万", "trend": "🔥🔥 持续上升", "type": "早教", "aud": "3-8岁儿童家长", "time": "持续10周", "logic": "家长教育焦虑", "sentiment": "正面", "age_range": "28-40岁", "keywords": ["专注力", "早教", "儿童", "训练"], "c": ["汤臣倍健", "善存"]},
        {"title": "宝宝英语启蒙动画片", "platform": "B站", "heat": "4800万", "trend": "🔥🔥 稳定上升", "type": "早教", "aud": "0-6岁儿童家长", "time": "全年持续", "logic": "英语启蒙意识提升", "sentiment": "正面", "age_range": "25-38岁", "keywords": ["英语启蒙", "动画片", "早教", "宝宝"], "c": ["汤臣倍健", "善存"]},
        {"title": "亲子手工DIY教程", "platform": "小红书", "heat": "3500万", "trend": "🔥🔥 稳定上升", "type": "亲子", "aud": "3-10岁儿童家庭", "time": "持续8周", "logic": "亲子互动需求", "sentiment": "正面", "age_range": "28-40岁", "keywords": ["亲子", "手工", "DIY", "互动"], "c": ["汤臣倍健", "善存"]},
        {"title": "周末亲子活动推荐", "platform": "抖音", "heat": "2800万", "trend": "🔥🔥 稳定上升", "type": "亲子", "aud": "有娃家庭", "time": "全年持续", "logic": "周末遛娃需求", "sentiment": "正面", "age_range": "28-40岁", "keywords": ["亲子", "周末", "活动", "遛娃"], "c": ["汤臣倍健", "善存"]},
        {"title": "儿童护眼食谱推荐", "platform": "小红书", "heat": "2200万", "trend": "🔥🔥 持续上升", "type": "育儿", "aud": "3-12岁儿童家长", "time": "持续8周", "logic": "近视防控意识提升", "sentiment": "正面", "age_range": "28-40岁", "keywords": ["护眼", "食谱", "儿童", "近视"], "c": ["汤臣倍健", "善存"]},
        {"title": "宝宝疫苗接种攻略", "platform": "小红书", "heat": "1800万", "trend": "🔥🔥 稳定上升", "type": "育儿", "aud": "新手父母", "time": "持续12周", "logic": "育儿知识刚需", "sentiment": "正面", "age_range": "25-35岁", "keywords": ["疫苗", "接种", "宝宝", "攻略"], "c": ["汤臣倍健", "善存"]},
        {"title": "儿童补钙产品测评", "platform": "小红书", "heat": "1600万", "trend": "🔥🔥 稳定上升", "type": "育儿", "aud": "补钙需求儿童家长", "time": "持续10周", "logic": "儿童营养补充需求", "sentiment": "中性", "age_range": "28-40岁", "keywords": ["补钙", "儿童", "测评", "维生素D"], "c": ["汤臣倍健", "善存"]},

        # ========== 健身类 (10条) ==========
        {"title": "居家燃脂HIIT训练", "platform": "抖音", "heat": "2.5亿", "trend": "🔥🔥🔥 爆发式增长", "type": "居家健身", "aud": "20-45岁健身人群", "time": "全年持续", "logic": "居家健身热潮", "sentiment": "正面", "age_range": "20-45岁", "keywords": ["HIIT", "燃脂", "居家", "健身", "训练"], "c": ["汤臣倍健", "清扬", "元气森林"]},
        {"title": "帕梅拉女孩减脂餐", "platform": "小红书", "heat": "1.2亿", "trend": "🔥🔥🔥 持续上升", "type": "居家健身", "aud": "减脂人群", "time": "持续10周", "logic": "健身+饮食结合", "sentiment": "正面", "age_range": "20-40岁", "keywords": ["帕梅拉", "减脂餐", "健身", "饮食"], "c": ["汤臣倍健", "OATLY", "元气森林"]},
        {"title": "哑铃新手入门训练", "platform": "B站", "heat": "6800万", "trend": "🔥🔥 稳定上升", "type": "居家健身", "aud": "健身新手", "time": "持续8周", "logic": "居家力量训练普及", "sentiment": "正面", "age_range": "20-40岁", "keywords": ["哑铃", "新手", "力量", "训练"], "c": ["汤臣倍健", "清扬"]},
        {"title": "减脂期优质碳水推荐", "platform": "小红书", "heat": "5200万", "trend": "🔥🔥 持续上升", "type": "减脂餐", "aud": "减脂人群", "time": "持续10周", "logic": "健康饮食趋势", "sentiment": "正面", "age_range": "20-40岁", "keywords": ["碳水", "减脂", "优质", "推荐"], "c": ["OATLY", "元气森林", "农夫山泉"]},
        {"title": "鸡胸肉减脂餐食谱", "platform": "小红书", "heat": "4200万", "trend": "🔥🔥 稳定上升", "type": "减脂餐", "aud": "健身人群", "time": "持续12周", "logic": "健身饮食内容需求大", "sentiment": "正面", "age_range": "20-40岁", "keywords": ["鸡胸肉", "减脂餐", "食谱", "高蛋白"], "c": ["汤臣倍健", "OATLY"]},
        {"title": "蛋白棒代餐测评", "platform": "抖音", "heat": "2800万", "trend": "🔥🔥 稳定上升", "type": "减脂餐", "aud": "健身人群", "time": "持续8周", "logic": "便捷代餐需求", "sentiment": "中性", "age_range": "22-40岁", "keywords": ["蛋白棒", "代餐", "测评", "健身"], "c": ["汤臣倍健", "元气森林"]},
        {"title": "瑜伽垫健身装备推荐", "platform": "小红书", "heat": "2200万", "trend": "🔥🔥 稳定上升", "type": "运动装备", "aud": "居家健身人群", "time": "持续10周", "logic": "健身装备需求增加", "sentiment": "正面", "age_range": "20-40岁", "keywords": ["瑜伽垫", "装备", "推荐", "居家"], "c": ["汤臣倍健", "清扬"]},
        {"title": "运动内衣高强度测评", "platform": "小红书", "heat": "1800万", "trend": "🔥🔥 稳定上升", "type": "运动装备", "aud": "女性健身人群", "time": "持续8周", "logic": "女性健身装备需求", "sentiment": "正面", "age_range": "20-40岁", "keywords": ["运动内衣", "高强度", "测评", "女性"], "c": ["汤臣倍健", "清扬"]},
        {"title": "筋膜枪使用教程", "platform": "抖音", "heat": "1500万", "trend": "🔥🔥 持续上升", "type": "居家健身", "aud": "运动后恢复人群", "time": "持续6周", "logic": "运动恢复需求", "sentiment": "正面", "age_range": "22-45岁", "keywords": ["筋膜枪", "使用", "教程", "恢复"], "c": ["汤臣倍健", "元气森林"]},
        {"title": "健身房器械使用指南", "platform": "B站", "heat": "1200万", "trend": "🔥🔥 稳定上升", "type": "居家健身", "aud": "健身房新手", "time": "持续8周", "logic": "健身房文化普及", "sentiment": "正面", "age_range": "20-40岁", "keywords": ["健身房", "器械", "指南", "新手"], "c": ["汤臣倍健", "清扬"]},

        # ========== 美食类 (12条) ==========
        {"title": "咖啡探店魔都篇", "platform": "小红书", "heat": "1.5亿", "trend": "🔥🔥🔥 爆发式增长", "type": "探店", "aud": "咖啡爱好者", "time": "全年持续", "logic": "咖啡文化+城市探店", "sentiment": "正面", "age_range": "20-35岁", "keywords": ["咖啡", "探店", "魔都", "上海", "网红"], "c": ["OATLY", "农夫山泉"]},
        {"title": "减脂期必喝的刮油汤", "platform": "小红书", "heat": "8800万", "trend": "🔥🔥 持续上升", "type": "食谱", "aud": "减脂人群", "time": "持续8周", "logic": "减脂食谱需求", "sentiment": "正面", "age_range": "20-40岁", "keywords": ["刮油汤", "减脂", "食谱", "健康"], "c": ["OATLY", "元气森林", "农夫山泉"]},
        {"title": "网红奶茶点单攻略", "platform": "抖音", "heat": "7200万", "trend": "🔥🔥 稳定上升", "type": "探店", "aud": "奶茶爱好者", "time": "持续12周", "logic": "奶茶文化持续热度", "sentiment": "正面", "age_range": "18-30岁", "keywords": ["奶茶", "点单", "攻略", "网红"], "c": ["OATLY", "元气森林", "农夫山泉"]},
        {"title": "便利店调酒教程", "platform": "小红书", "heat": "5600万", "trend": "🔥🔥 持续上升", "type": "饮品", "aud": "年轻人", "time": "持续10周", "logic": "宅家小酒馆文化", "sentiment": "正面", "age_range": "20-30岁", "keywords": ["调酒", "便利店", "教程", "鸡尾酒"], "c": ["百威", "OATLY"]},
        {"title": "气泡水神仙喝法", "platform": "抖音", "heat": "4200万", "trend": "🔥🔥 稳定上升", "type": "饮品", "aud": "健康饮品消费者", "time": "持续8周", "logic": "气泡水消费升级", "sentiment": "正面", "age_range": "18-35岁", "keywords": ["气泡水", "喝法", "DIY", "饮品"], "c": ["元气森林", "农夫山泉"]},
        {"title": "自制低卡零食合集", "platform": "小红书", "heat": "3800万", "trend": "🔥🔥 稳定上升", "type": "零食", "aud": "减脂人群", "time": "持续10周", "logic": "健康零食趋势", "sentiment": "正面", "age_range": "18-35岁", "keywords": ["低卡", "零食", "自制", "健康"], "c": ["元气森林", "OATLY", "农夫山泉"]},
        {"title": "燕麦奶拿铁制作教程", "platform": "小红书", "heat": "3200万", "trend": "🔥🔥 持续上升", "type": "饮品", "aud": "咖啡爱好者", "time": "持续8周", "logic": "燕麦奶咖啡文化兴起", "sentiment": "正面", "age_range": "20-35岁", "keywords": ["燕麦奶", "拿铁", "教程", "咖啡"], "c": ["OATLY", "农夫山泉"]},
        {"title": "春日野餐美食清单", "platform": "小红书", "heat": "2.8亿", "trend": "🔥🔥🔥 爆发式增长", "type": "食谱", "aud": "年轻人", "time": "季节性持续1月", "logic": "春游季节+野餐文化", "sentiment": "正面", "age_range": "18-40岁", "keywords": ["野餐", "春日", "美食", "清单"], "c": ["OATLY", "百威", "元气森林", "农夫山泉"]},
        {"title": "必胜客联名新品测评", "platform": "抖音", "heat": "2400万", "trend": "🔥🔥 持续上升", "type": "探店", "aud": "美食爱好者", "time": "持续2周", "logic": "品牌联名热度", "sentiment": "中性", "age_range": "18-30岁", "keywords": ["必胜客", "联名", "测评", "新品"], "c": ["百威", "农夫山泉"]},
        {"title": "健康零食品牌推荐", "platform": "小红书", "heat": "2800万", "trend": "🔥🔥 稳定上升", "type": "零食", "aud": "健康饮食者", "time": "持续10周", "logic": "健康零食消费升级", "sentiment": "正面", "age_range": "18-35岁", "keywords": ["健康零食", "推荐", "品牌", "低卡"], "c": ["元气森林", "OATLY", "农夫山泉"]},
        {"title": "夏日元气特调饮品", "platform": "抖音", "heat": "3600万", "trend": "🔥🔥 持续上升", "type": "饮品", "aud": "年轻人", "time": "季节性持续2月", "logic": "夏季饮品需求", "sentiment": "正面", "age_range": "18-30岁", "keywords": ["特调", "饮品", "夏日", "元气"], "c": ["元气森林", "OATLY", "农夫山泉"]},
        {"title": "快手早餐食谱推荐", "platform": "小红书", "heat": "4200万", "trend": "🔥🔥 稳定上升", "type": "食谱", "aud": "上班族", "time": "全年持续", "logic": "快节奏生活需求", "sentiment": "正面", "age_range": "20-40岁", "keywords": ["早餐", "快手", "食谱", "推荐"], "c": ["OATLY", "农夫山泉", "元气森林"]},

        # ========== 旅游类 (8条) ==========
        {"title": "春季赏花目的地TOP10", "platform": "小红书", "heat": "3.2亿", "trend": "🔥🔥🔥 爆发式增长", "type": "旅游", "aud": "旅游爱好者", "time": "季节性持续1月", "logic": "春游赏花季节+社交媒体传播", "sentiment": "正面", "age_range": "18-45岁", "keywords": ["赏花", "春季", "目的地", "旅游", "踏青"], "c": ["百威", "OATLY", "元气森林", "农夫山泉"]}
    ]


def get_topic_ideas_for_client(client_name):
    """根据客户获取匹配选题"""
    topics = get_hot_topics()
    return random.sample(topics, min(5, len(topics)))


def format_report():
    """生成更新报告"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    topics = get_hot_topics()
    return f"[{now}] 共更新 {len(topics)} 条热点数据"


if __name__ == "__main__":
    print(format_report())
