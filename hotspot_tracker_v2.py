#!/usr/bin/env python3
"""
热点追踪器 V2 - 产品层优化版
- 扩展关键词库（9大行业 × 5类词）
- 智能跨平台话题合并
- 差异化创意建议
- 简洁版/详细版输出
"""

import json
import requests
from datetime import datetime
from urllib.parse import quote
from difflib import SequenceMatcher
import re

# ============ V2 关键词库 ============
INDUSTRY_KEYWORDS_V2 = {
    "美妆": {
        "核心词": ["美妆", "护肤", "化妆", "彩妆", "化妆品", "美妆博主", "妆前妆后"],
        "产品词": ["口红", "粉底", "面膜", "眼影", "防晒", "精华", "洁面", "卸妆", "遮瑕", "腮红", "高光", "眉笔", "睫毛膏", "散粉", "定妆", "气垫", "唇釉", "唇泥", "眼线", "粉饼", "蜜粉", "隔离", "妆前乳", "定妆喷雾", "修容", "阴影", "高光", "卧蚕"],
        "成分词": ["玻尿酸", "烟酰胺", "A醇", "维C", "胶原蛋白", "水杨酸", "果酸", "神经酰胺", "视黄醇", "胜肽", "波色因", "虾青素", "角鲨烷"],
        "场景词": ["医美", "整容", "植发", "半永久", "美甲", "美睫", "化妆教程", "妆容", "上妆", "底妆", "素颜", "浓妆", "淡妆", "伪素颜", "早八妆", "约会妆", "通勤妆", "减龄", "抗老", "抗衰", "美白", "祛斑", "祛痘", "去黑头", "缩毛孔"],
        "品牌词": ["兰蔻", "雅诗兰黛", "欧莱雅", "完美日记", "花西子", "毛戈平", "橘朵", "珂拉琪", "YSL", "迪奥", "香奈儿", "MAC", "SK-II", "资生堂", "兰芝", "珀莱雅", "薇诺娜", "HBN", "夸迪"],
        "衍生词": ["伪素颜", "纯欲妆", "泰式妆", "早C晚A", "刷酸", "早八妆", "下班妆", "水光肌", "奶油肌", "妈生皮", "纯欲感", "氛围感妆容", "氛围感美女", "氛围感", "高级感", "千金妆", "富家千金", "韩系妆容", "日系妆容"]
    },
    "母婴": {
        "核心词": ["母婴", "宝宝", "婴儿", "儿童", "孕妇", "宝妈", "育儿", "带娃", "养娃", "亲子", "萌娃", "人类幼崽"],
        "产品词": ["奶粉", "纸尿裤", "辅食", "玩具", "童装", "婴儿车", "安全座椅", "奶瓶", "湿巾", "婴儿床", "学步车", "安抚", "吸奶器", "哺乳", "纸尿裤", "拉拉裤", "辅食机", "温奶器", "消毒柜"],
        "场景词": ["备孕", "新生儿", "早教", "亲子", "幼儿园", "小学", "二胎", "产检", "坐月子", "母乳", "断奶", "胎教", "启蒙", "幼小衔接", "兴趣班", "培训班", "补习", "作业", "辅导", "家庭教育", "正面管教"],
        "人群词": ["宝妈", "宝爸", "全职妈妈", "新手妈妈", "二胎妈妈", "奶奶带娃", "姥姥带娃", "隔代育儿", "奶爸", "带娃神器", "带娃日常", "育儿经"],
        "衍生词": ["辅食添加", "睡眠训练", "如厕训练", "分床睡", "第一口奶", "亲密育儿", "科学育儿", "蒙氏教育", "感统训练", "专注力", "语言发育", "大运动", "精细动作", "社交能力", "情绪管理"]
    },
    "数码": {
        "核心词": ["数码", "科技", "智能", "电子", "手机", "电脑", "黑科技", "科技感"],
        "产品词": ["手机", "电脑", "耳机", "平板", "笔记本", "显卡", "芯片", "相机", "键盘", "鼠标", "充电宝", "数据线", "显示器", "主机", "机箱", "散热器", "麦克风", "摄像头", "音响", "投影仪", "路由器", "硬盘", "内存", "SSD"],
        "品牌词": ["iPhone", "华为", "小米", "苹果", "三星", "OPPO", "vivo", "联想", "戴尔", "华硕", "英伟达", "AMD", "英特尔", "索尼", "佳能", "尼康", "大疆", "GoPro", "任天堂", "Steam"],
        "场景词": ["AI", "人工智能", "游戏", "电竞", "直播", "短视频", "编程", "办公", "远程", "元宇宙", "VR", "AR", "区块链", "Web3", "机器人", "自动驾驶", "智能助手", "大模型", "ChatGPT", "Claude", "GPT"],
        "衍生词": ["有线耳机", "蓝牙耳机", "无线耳机", "降噪耳机", "头戴式耳机", "入耳式耳机", "真无线", "电竞椅", "机械键盘", "曲面屏", "折叠屏", "全面屏", "快充", "无线充", "磁吸充电", "Type-C", "雷电", "高刷", "OLED", "Mini-LED"]
    },
    "服装": {
        "核心词": ["穿搭", "服装", "时尚", "衣服", "服饰", "时装", "潮流", "OOTD", "穿搭分享", "穿搭灵感", "穿搭技巧"],
        "产品词": ["卫衣", "牛仔裤", "运动鞋", "潮牌", "女装", "男装", "童装", "汉服", "JK", "风衣", "羽绒服", "大衣", "西装", "连衣裙", "半裙", "T恤", "衬衫", "毛衣", "针织衫", "马甲", "背心", "短裤", "阔腿裤", "瑜伽裤", "鲨鱼裤", "光腿神器"],
        "风格词": ["国潮", "复古", "街头", "通勤", "休闲", "运动风", "极简", "法式", "日系", "韩系", "欧美风", "中性风", "甜酷", "甜辣", "清纯", "性感", "优雅", "知性", "干练", "慵懒", "随性"],
        "场景词": ["穿搭教程", "搭配", "OOTD", "试穿", "开箱", "种草", "避雷", "显瘦", "显高", "显腿长", "遮肉", "微胖穿搭", "梨形身材", "苹果型身材", "小个子穿搭", "高个子穿搭"],
        "衍生词": ["老钱风", "芭蕾风", "多巴胺穿搭", "美拉德", "格雷系", "静奢风", "知识分子风", "学院风", "Y2K", "赛博朋克", "废土风", "千禧风", "千禧辣妹", "甜心辣妹", "纯欲风", "纯欲天花板"]
    },
    "食品": {
        "核心词": ["食品", "美食", "吃", "喝", "饮品", "吃货", "干饭人", "干饭", "探店", "美食探店"],
        "产品词": ["零食", "饮料", "奶茶", "火锅", "烧烤", "预制菜", "咖啡", "茶叶", "水果", "生鲜", "速食", "方便面", "螺蛳粉", "面包", "蛋糕", "甜品", "冰淇淋", "炸鸡", "披萨", "汉堡", "寿司", "拉面", "小龙虾", "大闸蟹", "三文鱼", "牛排", "红酒", "威士忌", "精酿"],
        "场景词": ["探店", "测评", "试吃", "做饭", "烹饪", "食谱", "减脂餐", "健身餐", "外卖", "下厨", "厨艺", "家常菜", "快手菜", "懒人食谱", "一人食", "便当", "野餐", "露营美食", "下午茶", "宵夜", "夜宵", "早餐", "午餐", "晚餐"],
        "品类词": ["中式", "西式", "日式", "韩式", "泰式", "川菜", "粤菜", "湘菜", "鲁菜", "苏菜", "浙菜", "闽菜", "徽菜", "火锅", "烤肉", "自助餐", "米其林", "网红店", "老字号"],
        "衍生词": ["无糖", "低卡", "0糖0卡", "植物基", "燕麦奶", "生椰拿铁", "瑞幸", "喜茶", "奈雪", "蜜雪冰城", "茶颜悦色", "霸王茶姬", "古茗", "一点点", "CoCo", "书亦烧仙草", "益禾堂", "沪上阿姨", "七分甜"]
    },
    "汽车": {
        "核心词": ["汽车", "车", "开车", "驾车", "车主", "老司机", "司机", "驾考", "驾照"],
        "产品词": ["新能源", "电车", "燃油车", "SUV", "轿车", "MPV", "跑车", "摩托车", "机车", "房车", "皮卡", "商务车", "越野车", "敞篷车", "混动", "插混", "增程"],
        "品牌词": ["特斯拉", "比亚迪", "理想", "蔚来", "小鹏", "问界", "小米汽车", "保时捷", "奔驰", "宝马", "奥迪", "丰田", "本田", "大众", "日产", "马自达", "福特", "凯迪拉克", "沃尔沃", "路虎", "Jeep", "吉利", "长城", "奇瑞", "长安"],
        "场景词": ["自驾", "驾照", "汽车用品", "车载", "充电桩", "保养", "维修", "车险", "洗车", "停车", "加油", "高速", "国道", "山路", "越野", "改装", "内饰", "座套", "脚垫", "行车记录仪", "车载好物"],
        "衍生词": ["自动驾驶", "智能座舱", "OTA升级", "续航", "快充", "换电", "辅助驾驶", "车道保持", "自适应巡航", "自动泊车", "抬头显示", "全景天窗", "空气悬挂", "四驱", "后驱", "百公里加速"]
    },
    "大健康": {
        "核心词": ["健康", "养生", "医疗", "保健", "减肥", "瘦身", "增肌", "健身", "运动", "长寿"],
        "产品词": ["维生素", "保健品", "体检", "医药", "中药", "西药", "医疗器械", "蛋白粉", "益生菌", "鱼油", "钙片", "褪黑素", "辅酶Q10", "NMN", "叶黄素", "护肝片"],
        "场景词": ["健身", "运动", "睡眠", "心理健康", "中医", "针灸", "推拿", "按摩", "理疗", "减肥", "增肌", "塑形", "康复", "体检", "问诊", "挂号", "就医", "医保", "医院", "诊所"],
        "人群词": ["老年人", "中年人", "上班族", "亚健康", "慢性病", "三高", "糖尿病", "高血压", "心血管", "肥胖", "失眠", "焦虑", "抑郁", "脱发", "秃头"],
        "衍生词": ["轻食", "代餐", "断糖", "低碳", "生酮", "间歇性断食", "正念", "冥想", "瑜伽", "普拉提", "HIIT", "有氧", "无氧", "力量训练", "撸铁", "举铁", "跑步", "游泳", "骑行", "跳绳", "帕梅拉", "刘畊宏", "减脂", "刷脂", "体脂率", "BMI"]
    },
    "快消": {
        "核心词": ["日化", "日用", "快消", "日用品", "洗护", "家居", "生活用品", "日用品好物"],
        "产品词": ["洗发水", "牙膏", "洗衣液", "纸巾", "沐浴露", "洗面奶", "卫生巾", "湿巾", "清洁", "洗洁精", "香皂", "护手霜", "身体乳", "护发素", "发膜", "护发精油", "止汗露", "漱口水", "牙线", "棉签", "卸妆棉", "洗脸巾"],
        "场景词": ["居家", "家务", "清洁", "收纳", "整理", "好物分享", "好物推荐", "居家好物", "生活小妙招", "家务神器", "清洁神器", "收纳神器", "断舍离", "极简生活"],
        "品牌词": ["宝洁", "联合利华", "蓝月亮", "立白", "威露士", "舒肤佳", "海飞丝", "飘柔", "潘婷", "沙宣", "多芬", "力士", "清扬", "欧乐B", "高露洁", "佳洁士", "云南白药", "黑人", "舒客"],
        "衍生词": ["除菌", "抑菌", "温和", "敏感肌", "氨基酸", "无硅油", "无添加", "植物配方", "天然成分", "环保", "可降解", "无塑", "零废弃", "极简护肤", "精简护肤"]
    },
    "家电": {
        "核心词": ["家电", "电器", "智能家居", "家电", "小家电", "大家电", "智能家电", "家电好物"],
        "产品词": ["冰箱", "空调", "洗衣机", "电视", "扫地机", "空气净化器", "净水器", "热水器", "油烟机", "燃气灶", "洗碗机", "烤箱", "微波炉", "破壁机", "空气炸锅", "电饭煲", "电压力锅", "电磁炉", "电水壶", "除湿机", "加湿器", "取暖器", "电风扇", "挂烫机", "吸尘器", "洗地机", "投影仪", "智能门锁", "智能窗帘", "智能音箱"],
        "场景词": ["智能家居", "全屋智能", "场景联动", "语音控制", "远程控制", "自动化", "智能化", "懒人神器", "提升幸福感", "生活品质", "居家幸福感"],
        "品牌词": ["美的", "格力", "海尔", "小米", "戴森", "科沃斯", "石头", "云鲸", "追觅", "添可", "必胜", "博世", "西门子", "松下", "索尼", "LG", "三星", "TCL", "海信", "创维", "方太", "老板", "华帝"],
        "衍生词": ["洗地机", "扫拖一体", "新风系统", "中央空调", "嵌入式", "集成灶", "蒸烤一体", "微蒸烤", "空气炸", "免手洗", "自清洁", "UV杀菌", "HEPA滤网", "静音", "变频", "一级能效", "智能投放"]
    }
}

# 热点类型关键词
HOTSPOT_TYPE_KEYWORDS = {
    "危机": ["道歉", "翻车", "塌房", "丑闻", "争议", "质疑", "被罚", "违规", "泄露", "爆料", "召回"],
    "种草": ["推荐", "测评", "开箱", "种草", "必入", "爆款", "好物", "平替", "真香", "安利"],
    "科普": ["科普", "解读", "分析", "研究", "发现", "专家", "医生", "教授", "实验", "数据"],
    "娱乐": ["明星", "演员", "歌手", "综艺", "电影", "电视剧", "演唱会", "粉丝", "八卦"],
    "社会": ["通报", "官方", "政策", "规定", "新规", "调整", "通知", "回应"]
}

# ============ 数据抓取函数 ============

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

def fetch_douyin_hot():
    """抓取抖音热搜榜"""
    try:
        url = "https://www.douyin.com/aweme/v1/hot/search/list/"
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()
        items = data.get('data', {}).get('word_list', [])
        result = []
        for item in items[:50]:
            result.append({
                "rank": len(result) + 1,
                "title": item.get('word', ''),
                "hot_value": item.get('hot_value', 0),
                "url": f"https://www.douyin.com/search/{quote(item.get('word', ''))}"
            })
        return {"platform": "抖音", "data": result, "success": True}
    except Exception as e:
        return {"platform": "抖音", "data": [], "success": False, "error": str(e)}

def fetch_weibo_hot():
    """抓取微博热搜榜"""
    try:
        url = "https://weibo.com/ajax/side/hotSearch"
        headers_weibo = headers.copy()
        headers_weibo["Referer"] = "https://weibo.com/"
        resp = requests.get(url, headers=headers_weibo, timeout=10)
        data = resp.json()
        items = data.get('data', {}).get('realtime', [])
        result = []
        for item in items[:50]:
            word = item.get('word', '').replace('#', '')
            result.append({
                "rank": len(result) + 1,
                "title": word,
                "hot_value": item.get('num', 0),
                "label": item.get('label_name', ''),
                "url": f"https://s.weibo.com/weibo?q={quote(word)}"
            })
        return {"platform": "微博", "data": result, "success": True}
    except Exception as e:
        return {"platform": "微博", "data": [], "success": False, "error": str(e)}

def fetch_baidu_hot():
    """抓取百度热搜榜"""
    try:
        url = "https://top.baidu.com/api/board?platform=wise&tab=realtime"
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()
        cards = data.get('data', {}).get('cards', [])
        items = []
        for card in cards:
            items.extend(card.get('content', []))
        result = []
        for item in items[:50]:
            result.append({
                "rank": len(result) + 1,
                "title": item.get('word', ''),
                "hot_value": item.get('hotScore', 0),
                "desc": item.get('desc', ''),
                "url": item.get('url', f"https://www.baidu.com/s?wd={quote(item.get('word', ''))}")
            })
        return {"platform": "百度", "data": result, "success": True}
    except Exception as e:
        return {"platform": "百度", "data": [], "success": False, "error": str(e)}

# ============ 分析函数 ============

def match_industry_v2(title, desc=""):
    """V2 行业匹配 - 扩展关键词库"""
    text = f"{title} {desc}".lower()
    matched = []
    
    for industry, keyword_groups in INDUSTRY_KEYWORDS_V2.items():
        for group_name, keywords in keyword_groups.items():
            for kw in keywords:
                if kw.lower() in text:
                    if industry not in matched:
                        matched.append(industry)
                    break
            if industry in matched:
                break
    
    return matched

def classify_hotspot_type(title, desc=""):
    """热点类型分类"""
    text = f"{title} {desc}".lower()
    
    for hotspot_type, keywords in HOTSPOT_TYPE_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                return hotspot_type
    
    return "其他"

def merge_cross_platform_topics(all_items):
    """智能合并跨平台话题 - V2增强版"""
    topics = []
    used_indices = set()
    
    # 预处理：提取标题关键词
    def extract_keywords(title):
        """提取标题核心关键词"""
        # 移除常见修饰词
        stop_words = ['官方', '最新', '重磅', '突发', '热搜', '上榜', '第一']
        keywords = title
        for word in stop_words:
            keywords = keywords.replace(word, '')
        return keywords.strip()
    
    for i, item in enumerate(all_items):
        if i in used_indices:
            continue
        
        similar_items = [item]
        similar_indices = {i}
        title_keywords = extract_keywords(item['title'])
        
        for j, other in enumerate(all_items):
            if j in used_indices or j == i:
                continue
            if other.get('platform') == item.get('platform'):
                continue
            
            # 多重匹配策略
            other_keywords = extract_keywords(other['title'])
            
            # 策略1：标题相似度
            ratio = SequenceMatcher(None, item['title'], other['title']).ratio()
            
            # 策略2：关键词包含
            keyword_match = False
            if len(title_keywords) >= 4 and len(other_keywords) >= 4:
                # 核心词匹配（标题前半部分）
                if title_keywords[:8] in other_keywords or other_keywords[:8] in title_keywords:
                    keyword_match = True
                # 或主体匹配（去除数字、标点后的核心）
                core1 = re.sub(r'[0-9\s\-\：:\.]', '', item['title'])[:10]
                core2 = re.sub(r'[0-9\s\-\：:\.]', '', other['title'])[:10]
                if core1 and core2 and (core1 in core2 or core2 in core1):
                    keyword_match = True
            
            # 策略3：实体匹配（人名、地名、事件名）
            entity_match = False
            # 提取可能的实体（连续的汉字，排除常见动词）
            entities1 = re.findall(r'[\u4e00-\u9fa5]{2,}', item['title'])
            entities2 = re.findall(r'[\u4e00-\u9fa5]{2,}', other['title'])
            for e1 in entities1:
                for e2 in entities2:
                    if e1 == e2 and len(e1) >= 3:
                        entity_match = True
                        break
                if entity_match:
                    break
            
            # 综合判断
            if ratio > 0.55 or keyword_match or entity_match:
                similar_items.append(other)
                similar_indices.add(j)
        
        used_indices.update(similar_indices)
        
        platforms = [s.get('platform', '') for s in similar_items]
        total_hot = sum(s.get('hot_value', 0) for s in similar_items)
        best_title = max(similar_items, key=lambda x: x.get('hot_value', 0))['title']
        
        topics.append({
            'title': best_title,
            'platforms': platforms,
            'platforms_str': '+'.join(platforms),
            'total_hot': total_hot,
            'cross_platform': len(platforms) > 1,
            'items': similar_items,
            'industries': match_industry_v2(best_title),
            'hotspot_type': classify_hotspot_type(best_title)
        })
    
    return sorted(topics, key=lambda x: x['total_hot'], reverse=True)

def analyze_hotspots_v2(hot_data_list):
    """V2 分析热点数据"""
    all_items = []
    
    for platform_data in hot_data_list:
        platform = platform_data.get('platform', '')
        for item in platform_data.get('data', []):
            item_copy = dict(item)
            item_copy['platform'] = platform
            item_copy['industries'] = match_industry_v2(item.get('title', ''), item.get('desc', ''))
            item_copy['hotspot_type'] = classify_hotspot_type(item.get('title', ''), item.get('desc', ''))
            all_items.append(item_copy)
    
    # 按行业分类
    industry_hotspots = {k: [] for k in INDUSTRY_KEYWORDS_V2.keys()}
    for item in all_items:
        for ind in item.get('industries', []):
            industry_hotspots[ind].append(item)
    
    # 跨平台话题合并
    cross_platform_topics = merge_cross_platform_topics(all_items)
    
    return {
        "industry_hotspots": industry_hotspots,
        "cross_platform_topics": cross_platform_topics,
        "all_items": all_items,
        "total_items": len(all_items)
    }

# ============ 创意建议生成 ============

def generate_smart_recommendations(industry, hotspots):
    """基于热点生成差异化建议"""
    
    if not hotspots:
        return []
    
    ideas = []
    top = hotspots[0]
    title = top['title']
    hotspot_type = top.get('hotspot_type', '其他')
    
    # 基于热点类型
    type_templates = {
        "危机": f"【危机解读】围绕「{title[:15]}」，输出行业反思/品牌避坑指南",
        "种草": f"【跟风种草】快速跟进「{title[:15]}」相关产品测评/开箱",
        "科普": f"【专业科普】用行业视角解读「{title[:15]}」，建立专业人设",
        "娱乐": f"【娱乐借势】结合「{title[:15]}」热点，制作趣味关联内容",
        "社会": f"【政策解读】从行业角度解读「{title[:15]}」带来的影响"
    }
    
    if hotspot_type in type_templates:
        ideas.append(type_templates[hotspot_type])
    
    # 基于行业特性
    industry_templates = {
        "美妆": "【教程种草】拍摄上妆教程，突出产品使用前后对比效果",
        "母婴": "【育儿干货】输出实用育儿知识，用真实案例建立信任",
        "数码": "【参数解读】用通俗语言解读技术参数，降低用户认知门槛",
        "服装": "【穿搭示范】真人上身展示，提供可复制的搭配方案",
        "食品": "【口味测评】真实试吃体验，强调口味层次/口感细节",
        "汽车": "【试驾体验】实车试驾分享，展示真实驾驶感受",
        "大健康": "【科普辟谣】用专业视角解读健康热点，破除常见误区",
        "快消": "【对比测评】同类产品横向对比，突出性价比优势",
        "家电": "【场景展示】演示产品如何解决日常生活痛点"
    }
    
    if industry in industry_templates:
        ideas.append(industry_templates[industry])
    
    # 基于平台
    platforms = list(set(h.get('platform', '') for h in hotspots[:3]))
    if len(platforms) > 1:
        ideas.append(f"【多平台布局】在{'/'.join(platforms[:2])}同步发布，扩大曝光")
    
    return ideas[:3]

# ============ 输出格式化 ============

def format_simple_report(analysis, generated_at):
    """生成简洁版报告"""
    
    lines = []
    lines.append("=" * 40)
    lines.append(f"🔥 每日热点简报 | {generated_at}")
    lines.append("=" * 40)
    
    # 1. 今日爆点（跨平台Top5）
    lines.append("\n📌 今日爆点（跨平台热度Top5）")
    lines.append("-" * 40)
    
    cross_topics = [t for t in analysis['cross_platform_topics'] if t['total_hot'] > 1000000][:5]
    
    if cross_topics:
        for i, topic in enumerate(cross_topics, 1):
            hot_str = f"{topic['total_hot']/10000:.0f}万"
            platforms_str = topic['platforms_str']
            industries_str = '/'.join(topic['industries']) if topic['industries'] else '综合'
            type_emoji = {"危机": "⚠️", "种草": "🌱", "科普": "📚", "娱乐": "🎭", "社会": "📢"}.get(topic['hotspot_type'], "📌")
            
            lines.append(f"{i}. {type_emoji} {topic['title'][:20]}")
            lines.append(f"   📊 {hot_str} | {platforms_str} | {industries_str}")
    else:
        lines.append("暂无明显爆点")
    
    # 2. 行业热点
    lines.append("\n🏭 行业热点（有匹配的行业）")
    lines.append("-" * 40)
    
    industry_with_data = [(ind, items) for ind, items in analysis['industry_hotspots'].items() if items]
    
    if industry_with_data:
        industry_emojis = {
            "美妆": "💄", "母婴": "👶", "数码": "🎧", "服装": "👗",
            "食品": "🍜", "汽车": "🚗", "大健康": "🏥", "快消": "🧴", "家电": "🏠"
        }
        
        for industry, items in sorted(industry_with_data, key=lambda x: len(x[1]), reverse=True):
            emoji = industry_emojis.get(industry, "📌")
            top_items = sorted(items, key=lambda x: x.get('hot_value', 0), reverse=True)[:3]
            
            lines.append(f"\n{emoji} {industry} | {len(items)}条")
            for item in top_items:
                hot_str = f"{item['hot_value']/10000:.0f}万" if item['hot_value'] > 10000 else str(item['hot_value'])
                lines.append(f"   · {item['title'][:18]} [{item['platform']}]")
            
            # 行业建议
            ideas = generate_smart_recommendations(industry, items)
            if ideas:
                lines.append(f"   💡 {ideas[0][:30]}...")
    else:
        lines.append("今日暂无行业热点匹配")
    
    # 3. 今日行动建议
    lines.append("\n🎯 今日行动建议（按热度排序）")
    lines.append("-" * 40)
    
    # 收集所有行动建议，按热度排序
    all_actions = []
    for industry, items in industry_with_data:
        if not items:
            continue
        ideas = generate_smart_recommendations(industry, items)
        if ideas:
            # 取行业最高热度
            max_hot = max(items, key=lambda x: x.get('hot_value', 0)).get('hot_value', 0)
            all_actions.append({
                'industry': industry,
                'idea': ideas[0],
                'hot': max_hot,
                'type': items[0].get('hotspot_type', '其他')
            })
    
    # 按热度排序，取Top3
    all_actions.sort(key=lambda x: x['hot'], reverse=True)
    
    if all_actions:
        for i, action in enumerate(all_actions[:3]):
            type_emoji = {"危机": "⚠️", "种草": "🌱", "科普": "📚", "娱乐": "🎭", "社会": "📢", "其他": "📌"}.get(action['type'], "📌")
            lines.append(f"{i+1}. {type_emoji} 【{action['industry']}】{action['idea'][:30]}")
    else:
        lines.append("暂无高优先级行动建议")
    
    # 4. 数据概览
    lines.append("\n📊 数据概览")
    lines.append("-" * 40)
    
    industry_covered = len([1 for items in analysis['industry_hotspots'].values() if items])
    cross_count = len([t for t in analysis['cross_platform_topics'] if t['cross_platform']])
    
    platform_counts = {}
    for item in analysis['all_items']:
        p = item.get('platform', '未知')
        platform_counts[p] = platform_counts.get(p, 0) + 1
    
    platform_str = ' + '.join([f"{p}({c})" for p, c in platform_counts.items()])
    
    lines.append(f"总热点: {analysis['total_items']}条")
    lines.append(f"跨平台: {cross_count}条")
    lines.append(f"行业覆盖: {industry_covered}/9")
    lines.append(f"数据源: {platform_str}")
    
    lines.append("\n" + "=" * 40)
    
    return "\n".join(lines)

def format_detailed_report(analysis, generated_at):
    """生成详细版报告（JSON + 文字）"""
    
    report = {
        "generated_at": generated_at,
        "summary": {
            "total_items": analysis['total_items'],
            "cross_platform_count": len([t for t in analysis['cross_platform_topics'] if t['cross_platform']]),
            "industry_coverage": len([1 for items in analysis['industry_hotspots'].values() if items])
        },
        "cross_platform_topics": analysis['cross_platform_topics'][:20],
        "industry_hotspots": analysis['industry_hotspots'],
        "recommendations": {}
    }
    
    for industry, items in analysis['industry_hotspots'].items():
        if items:
            report['recommendations'][industry] = generate_smart_recommendations(industry, items)
    
    return report

# ============ 主函数 ============

def main():
    """主函数"""
    import sys
    
    # 解析参数
    output_mode = "simple"  # 默认简洁版
    if len(sys.argv) > 1:
        if sys.argv[1] == "--detailed":
            output_mode = "detailed"
        elif sys.argv[1] == "--json":
            output_mode = "json"
    
    print(f"🔍 开始抓取热点数据... {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 抓取数据
    douyin = fetch_douyin_hot()
    weibo = fetch_weibo_hot()
    baidu = fetch_baidu_hot()
    
    print(f"✅ 抖音: {len(douyin.get('data', []))} 条")
    print(f"✅ 微博: {len(weibo.get('data', []))} 条")
    print(f"✅ 百度: {len(baidu.get('data', []))} 条")
    
    # 分析数据
    print("📊 分析热点...")
    analysis = analyze_hotspots_v2([douyin, weibo, baidu])
    
    # 统计
    industry_covered = len([1 for items in analysis['industry_hotspots'].values() if items])
    print(f"📈 行业覆盖: {industry_covered}/9")
    
    # 生成报告
    generated_at = datetime.now().strftime('%Y-%m-%d')
    
    if output_mode == "json":
        # JSON输出
        report = format_detailed_report(analysis, generated_at)
        output_file = f"/Users/zhangjingwei/.qclaw/workspace/hotspot-tracker/report_v2_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"📁 报告已保存: {output_file}")
    else:
        # 文字报告
        report_text = format_simple_report(analysis, generated_at)
        print("\n" + report_text)
        
        # 同时保存JSON
        report_json = format_detailed_report(analysis, generated_at)
        output_file = f"/Users/zhangjingwei/.qclaw/workspace/hotspot-tracker/report_v2_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report_json, f, ensure_ascii=False, indent=2)
        print(f"\n📁 完整报告已保存: {output_file}")
    
    return analysis

if __name__ == "__main__":
    main()
