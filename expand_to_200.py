#!/usr/bin/env python3
"""
热点数据扩展脚本 - 将 new_hotspots.json 从10条扩展到200条以上
"""

import json
import random
from datetime import datetime, timedelta
import uuid

# 读取现有数据
with open('new_hotspots.json', 'r', encoding='utf-8') as f:
    existing_hotspots = json.load(f)

existing_titles = {h['title'] for h in existing_hotspots}
print(f"现有热点数量: {len(existing_hotspots)}")

# 行业配置
industries_config = {
    "科技": {
        "keywords": ["AI大模型", "智能手机", "折叠屏", "芯片", "量子计算", "机器人", "VR眼镜", "智能手表", "云计算", "自动驾驶", "AI绘画", "区块链", "5G网络", "物联网设备", "超级计算机"],
        "brands": ["小米", "荣耀", "索尼", "罗技", "华为", "OPPO", "vivo", "苹果"],
        "platforms": ["微博/全网", "微博/抖音", "B站/微博"]
    },
    "美食": {
        "keywords": ["网红餐厅", "特色小吃", "新式茶饮", "预制菜", "轻食沙拉", "夜宵美食", "网红火锅", "特色烧烤", "奶茶新品", "精品咖啡", "地方美食", "节日美食"],
        "brands": ["农夫山泉", "元气森林", "OATLY", "百威", "星巴克", "瑞幸", "喜茶", "奈雪"],
        "platforms": ["小红书/抖音", "抖音/微博", "小红书"]
    },
    "美妆": {
        "keywords": ["护肤攻略", "彩妆教程", "新品测评", "抗衰老精华", "美白护肤", "防晒必备", "面膜推荐", "口红试色", "粉底测评", "眼妆技巧", "卸妆产品", "护肤成分"],
        "brands": ["AHC", "玉兰油", "多芬", "力士", "兰蔻", "雅诗兰黛", "SK-II", "资生堂"],
        "platforms": ["小红书", "微博/小红书", "抖音/小红书"]
    },
    "母婴": {
        "keywords": ["育儿经验", "宝宝护理", "孕期保健", "婴儿用品", "早教启蒙", "辅食添加", "奶粉选择", "纸尿裤测评", "童装穿搭", "益智玩具", "亲子互动", "儿童安全"],
        "brands": ["希宝", "飞鹤", "君乐宝", "贝因美", "帮宝适", "好奇", "巴拉巴拉"],
        "platforms": ["小红书", "微博/小红书", "抖音"]
    },
    "家居": {
        "keywords": ["智能家居", "装修攻略", "家居好物", "收纳整理", "软装搭配", "全屋定制", "家电选购", "清洁神器", "厨房用品", "卧室布置", "客厅设计", "阳台改造"],
        "brands": ["小米", "海尔", "美的", "格力", "戴森", "石头科技", "云鲸"],
        "platforms": ["小红书/抖音", "小红书", "微博/全网"]
    },
    "旅游": {
        "keywords": ["旅游攻略", "景点推荐", "自驾游路线", "出境旅游", "亲子游", "蜜月旅行", "穷游攻略", "民宿推荐", "酒店测评", "机票优惠", "签证攻略", "旅行好物"],
        "brands": ["携程", "飞猪", "马蜂窝", "Airbnb", "如家", "汉庭"],
        "platforms": ["小红书/抖音", "微博/小红书", "抖音"]
    },
    "体育": {
        "keywords": ["NBA季后赛", "CBA总决赛", "世界杯预选赛", "乒乓球世界杯", "羽毛球公开赛", "网球大满贯", "游泳世锦赛", "城市马拉松", "健身打卡", "瑜伽练习", "滑雪季", "户外登山"],
        "brands": ["耐克", "阿迪达斯", "安踏", "李宁", "特步", "鸿星尔克"],
        "platforms": ["微博/全网", "微博/抖音", "抖音"]
    },
    "娱乐": {
        "keywords": ["新剧开播", "电影上映", "综艺节目", "明星动态", "演唱会门票", "新歌发布", "网红主播", "短剧热播", "真人秀", "选秀节目", "颁奖典礼", "娱乐八卦"],
        "brands": ["芒果TV", "爱奇艺", "优酷", "腾讯视频", "B站"],
        "platforms": ["微博/全网", "微博/抖音", "抖音/全网"]
    },
    "汽车": {
        "keywords": ["新车发布", "新能源车", "智能驾驶", "汽车评测", "购车攻略", "用车知识", "改装文化", "车展直击", "电动车对比", "混动车型", "SUV推荐", "轿车选购"],
        "brands": ["比亚迪", "特斯拉", "蔚来", "理想", "小鹏", "小米", "华为", "吉利", "长城"],
        "platforms": ["微博/全网", "抖音", "B站"]
    },
    "游戏": {
        "keywords": ["新游上线", "游戏攻略", "电竞赛事", "游戏直播", "主机游戏", "手游推荐", "端游新作", "独立游戏", "游戏评测", "游戏周边", "cosplay", "游戏联动"],
        "brands": ["腾讯", "网易", "米哈游", "索尼", "任天堂", "微软"],
        "platforms": ["B站/微博", "微博/全网", "抖音/B站"]
    },
    "健康": {
        "keywords": ["健康科普", "养生知识", "医疗新知", "科学减肥", "心理健康", "睡眠改善", "营养膳食", "体检报告", "慢病管理", "中医养生", "运动健身", "健康生活方式"],
        "brands": ["汤臣倍健", "善存", "Swisse", "MoveFree", "同仁堂"],
        "platforms": ["微博/全网", "小红书", "抖音"]
    },
    "金融": {
        "keywords": ["股市行情", "基金定投", "理财攻略", "保险知识", "房产投资", "数字货币", "银行理财", "贷款攻略", "信用卡优惠", "财经要闻", "投资理财", "经济政策"],
        "brands": ["支付宝", "微信支付", "招商银行", "工商银行", "建设银行"],
        "platforms": ["微博/全网", "全网"]
    },
    "教育": {
        "keywords": ["高考资讯", "考研攻略", "留学申请", "职业培训", "语言学习", "在线课程", "教育政策", "学区房", "课外辅导", "素质教育", "家庭教育", "学习方法"],
        "brands": ["新东方", "好未来", "猿辅导", "作业帮", "学而思"],
        "platforms": ["微博/全网", "小红书", "全网"]
    },
    "宠物": {
        "keywords": ["萌宠日常", "宠物护理", "宠物训练", "宠物医疗", "宠物用品", "猫咪日常", "狗狗训练", "异宠饲养", "宠物领养", "宠物美容", "宠物健康", "宠物零食"],
        "brands": ["皇家", "渴望", "爱肯拿", "伟嘉", "宝路"],
        "platforms": ["小红书/抖音", "抖音", "微博/抖音"]
    },
    "时尚": {
        "keywords": ["穿搭分享", "时尚潮流", "新品首发", "时装周", "明星穿搭", "街拍灵感", "配饰搭配", "包包推荐", "鞋子测评", "珠宝首饰", "潮牌联名", "季节穿搭"],
        "brands": ["LV", "Gucci", "Prada", "Chanel", "Dior", "爱马仕"],
        "platforms": ["小红书", "微博/小红书", "抖音/小红书"]
    }
}

# 标题模板
title_templates = {
    "科技": [
        "{keyword}最新突破引发行业关注",
        "{keyword}技术革新用户期待拉满",
        "{keyword}重大升级市场反应热烈",
        "{keyword}成新风口资本竞相布局",
        "{keyword}领域再现突破国产崛起",
        "{keyword}新品发布消费者排队抢购",
        "{keyword}赛道竞争加剧格局生变",
        "{keyword}应用场景拓展商业化加速",
        "{keyword}产业链升级替代加速",
        "{keyword}迎来爆发期规模激增"
    ],
    "美食": [
        "{keyword}成新晋网红打卡排队超火爆",
        "{keyword}刷屏社交平台网友纷纷种草",
        "{keyword}引发美食热潮销量暴增",
        "{keyword}成年轻人新宠市场规模破亿",
        "{keyword}创新吃法走红网友直呼绝了",
        "{keyword}测评对比结果出人意料",
        "{keyword}隐藏菜单曝光网友疯狂安利",
        "{keyword}新品上市首日销量破纪录",
        "{keyword}成约会首选消费场景升级",
        "{keyword}跨界联名款款售罄"
    ],
    "美妆": [
        "{keyword}成年度爆款小红书刷屏",
        "{keyword}测评报告出炉结果令人意外",
        "{keyword}成分党必看专家深度解析",
        "{keyword}平替产品走红国货崛起",
        "{keyword}使用误区盘点你中招了吗",
        "{keyword}新品首发秒售罄引热议",
        "{keyword}效果对比图刷屏网友惊呆",
        "{keyword}成为护肤新宠专家解读",
        "{keyword}避坑指南消费者必看",
        "{keyword}年度榜单发布这些产品上榜"
    ],
    "母婴": [
        "{keyword}经验分享宝妈直呼太实用",
        "{keyword}避坑指南新手父母必看",
        "{keyword}引发讨论家长看法不一",
        "{keyword}新品测评结果出人意料",
        "{keyword}专家建议家长纷纷点赞",
        "{keyword}成育儿新趋势年轻父母追捧",
        "{keyword}注意事项盘点安全第一",
        "{keyword}市场乱象曝光消费者需警惕",
        "{keyword}好物推荐省钱又省心",
        "{keyword}行业标准出台消费更有保障"
    ],
    "家居": [
        "{keyword}成装修新宠设计师力荐",
        "{keyword}避坑指南装修必看",
        "{keyword}好物测评性价比超高",
        "{keyword}改造案例刷屏网友直呼羡慕",
        "{keyword}成为新趋势年轻人追捧",
        "{keyword}选购攻略专业人士解读",
        "{keyword}创新设计走红网友纷纷效仿",
        "{keyword}使用体验分享真实评价",
        "{keyword}品牌对比结果出人意料",
        "{keyword}成居家必备提升幸福感"
    ],
    "旅游": [
        "{keyword}成热门目的地游客爆满",
        "{keyword}攻略分享网友直呼太实用",
        "{keyword}隐藏玩法曝光惊喜不断",
        "{keyword}旅游季来临预订量激增",
        "{keyword}成网红打卡地拍照绝美",
        "{keyword}省钱攻略学生党必看",
        "{keyword}避坑指南游客真实体验",
        "{keyword}小众路线推荐人少景美",
        "{keyword}出行新政优惠力度大",
        "{keyword}成蜜月首选浪漫指数拉满"
    ],
    "体育": [
        "{keyword}精彩赛事球迷狂欢",
        "{keyword}选手创造历史全网祝贺",
        "{keyword}比赛结果出炉引发热议",
        "{keyword}新赛季开启期待值拉满",
        "{keyword}冠军诞生创造新纪录",
        "{keyword}赛事直播火爆观众破纪录",
        "{keyword}运动员表现亮眼获赞无数",
        "{keyword}规则变更影响深远",
        "{keyword}商业价值攀升赞助商抢滩",
        "{keyword}全民健身热潮运动成新风尚"
    ],
    "娱乐": [
        "{keyword}引爆热搜网友热议不断",
        "{keyword}口碑爆棚观众直呼过瘾",
        "{keyword}争议话题网友站队明显",
        "{keyword}官宣定档期待值拉满",
        "{keyword}幕后花絮曝光网友直呼意外",
        "{keyword}票房口碑双丰收成年度爆款",
        "{keyword}阵容官宣粉丝期待值爆表",
        "{keyword}话题刷屏全网讨论热烈",
        "{keyword}获奖引热议业内认可",
        "{keyword}回归官宣老粉泪目"
    ],
    "汽车": [
        "{keyword}正式发布市场反响热烈",
        "{keyword}销量破纪录行业格局生变",
        "{keyword}技术突破引领行业发展",
        "{keyword}用户评测出炉真实体验分享",
        "{keyword}优惠政策出台购者排队",
        "{keyword}召回事件曝光消费者关注",
        "{keyword}成市场新宠销量激增",
        "{keyword}对比测评结果出人意料",
        "{keyword}行业新规出台影响深远",
        "{keyword}品牌战略调整市场格局生变"
    ],
    "游戏": [
        "{keyword}正式上线玩家排队下载",
        "{keyword}版本更新内容诚意满满",
        "{keyword}赛事激战正酣观众热情高涨",
        "{keyword}玩家破纪录社区沸腾",
        "{keyword}新角色发布玩家期待",
        "{keyword}争议话题玩家引热议",
        "{keyword}联动官宣粉丝狂欢",
        "{keyword}攻略分享上分必看",
        "{keyword}口碑炸裂成年度黑马",
        "{keyword}电竞选手转会引发热议"
    ],
    "健康": [
        "{keyword}成热门话题专家权威解读",
        "{keyword}误区盘点你中招了吗",
        "{keyword}新研究发现改变认知",
        "{keyword}实用指南健康生活必看",
        "{keyword}产品测评结果出人意料",
        "{keyword}成健康新趋势年轻人追捧",
        "{keyword}专家建议科学养生",
        "{keyword}数据报告出炉引发关注",
        "{keyword}辟谣帖刷屏网友直呼涨知识",
        "{keyword}市场乱象曝光消费者需警惕"
    ],
    "金融": [
        "{keyword}最新动态投资者关注",
        "{keyword}政策调整市场反应明显",
        "{keyword}数据发布超出预期",
        "{keyword}投资机会专家解读",
        "{keyword}风险提示投资者需注意",
        "{keyword}市场变化操作策略调整",
        "{keyword}新规出台影响深远",
        "{keyword}行业动态格局生变",
        "{keyword}收益报告出炉表现亮眼",
        "{keyword}避坑指南投资必看"
    ],
    "教育": [
        "{keyword}政策变化家长学生关注",
        "{keyword}备考攻略学子必看",
        "{keyword}录取结果出炉梦校捷报",
        "{keyword}改革新动向影响深远",
        "{keyword}经验分享成功上岸",
        "{keyword}避坑指南少走弯路",
        "{keyword}资源推荐学习必备",
        "{keyword}行业动态市场格局生变",
        "{keyword}成绩榜单发布优秀学子受赞",
        "{keyword}新规解读专家权威分析"
    ],
    "宠物": [
        "{keyword}萌化全网网友直呼太可爱",
        "{keyword}经验分享主人直呼实用",
        "{keyword}避坑指南新手必看",
        "{keyword}好物推荐毛孩子福音",
        "{keyword}科普知识主人涨姿势",
        "{keyword}成新晋网红粉丝破百万",
        "{keyword}感人故事网友泪目",
        "{keyword}市场动态行业发展迅速",
        "{keyword}健康问题主人需注意",
        "{keyword}训练技巧效果显著"
    ],
    "时尚": [
        "{keyword}成流行趋势明星人手一件",
        "{keyword}穿搭灵感照着穿就对了",
        "{keyword}新品发布款款售罄",
        "{keyword}平替推荐性价比超高",
        "{keyword}避坑指南购买必看",
        "{keyword}明星同款引发抢购潮",
        "{keyword}品牌联名款款断货",
        "{keyword}穿搭误区你中招了吗",
        "{keyword}年度流行色发布时尚圈震动",
        "{keyword}秀场直击设计惊艳"
    ]
}

def generate_hotspot(industry, rank, base_time):
    """生成单条热点数据"""
    config = industries_config[industry]
    templates = title_templates[industry]
    
    keyword = random.choice(config["keywords"])
    template = random.choice(templates)
    title = template.format(keyword=keyword)
    
    # 热度值：排名越高热度越高
    if rank <= 20:
        hot_value = random.randint(300000000, 450000000)
    elif rank <= 50:
        hot_value = random.randint(150000000, 300000000)
    elif rank <= 100:
        hot_value = random.randint(80000000, 150000000)
    elif rank <= 150:
        hot_value = random.randint(40000000, 80000000)
    else:
        hot_value = random.randint(20000000, 40000000)
    
    # 随机选择相关品牌
    related_brands = []
    if random.random() > 0.3:
        brand_count = random.randint(1, 3)
        related_brands = random.sample(config["brands"], min(brand_count, len(config["brands"])))
    
    # 时间偏移
    time_offset = timedelta(hours=random.randint(0, 48))
    created_at = (base_time - time_offset).strftime("%Y-%m-%dT%H:%M:%S")
    
    # 生成唯一ID
    import hashlib
    id_hash = hashlib.md5(f"{title}{created_at}".encode()).hexdigest()[:8]
    
    # 行业标签
    industry_tags = [industry]
    if random.random() > 0.6:
        other_industries = [i for i in industries_config.keys() if i != industry]
        industry_tags.append(random.choice(other_industries))
    
    # 趋势标签
    if rank <= 10:
        trend = random.choice(["爆", "热"])
    elif rank <= 50:
        trend = random.choice(["热", "新"])
    else:
        trend = random.choice(["新", "热"])
    
    # 情感倾向
    if industry in ["娱乐", "体育"]:
        sentiment = random.choice(["正面", "中性"])
    elif industry in ["健康", "金融"]:
        sentiment = random.choices(["正面", "中性", "负面"], weights=[0.4, 0.4, 0.2])[0]
    else:
        sentiment = random.choices(["正面", "中性", "负面"], weights=[0.6, 0.3, 0.1])[0]
    
    return {
        "rank": rank,
        "title": title,
        "hot_value": hot_value,
        "url": f"https://weibo.com",
        "platform": random.choice(config["platforms"]),
        "industries": industry_tags,
        "trends": [trend],
        "type": industry + "热点" if industry not in ["金融", "健康"] else ("经济热点" if industry == "金融" else "健康热点"),
        "sentiment": sentiment,
        "keywords": [keyword] + random.sample(config["keywords"], min(2, len(config["keywords"]))),
        "c": related_brands,
        "created_at": created_at,
        "id": f"ht_{id_hash}"
    }

# 生成新热点
new_hotspots = list(existing_hotspots)
base_time = datetime.now()

# 计算需要生成的数量
target_count = 210
current_count = len(existing_hotspots)
need_generate = target_count - current_count

print(f"目标数量: {target_count}")
print(f"当前数量: {current_count}")
print(f"需要生成: {need_generate}")

# 按行业分配生成数量
industries = list(industries_config.keys())
per_industry = need_generate // len(industries)
extra = need_generate % len(industries)

generated_count = 0
rank_start = current_count + 1

for i, industry in enumerate(industries):
    count = per_industry + (1 if i < extra else 0)
    for j in range(count):
        rank = rank_start + generated_count
        hotspot = generate_hotspot(industry, rank, base_time)
        
        # 检查重复
        if hotspot["title"] not in existing_titles:
            new_hotspots.append(hotspot)
            existing_titles.add(hotspot["title"])
            generated_count += 1

# 按热度值排序并重新编号
new_hotspots.sort(key=lambda x: x["hot_value"], reverse=True)
for i, h in enumerate(new_hotspots):
    h["rank"] = i + 1

# 保存结果
with open('new_hotspots.json', 'w', encoding='utf-8') as f:
    json.dump(new_hotspots, f, ensure_ascii=False, indent=2)

print(f"\n========== 扩展报告 ==========")
print(f"原有热点数量: {len(existing_hotspots)}")
print(f"新增热点数量: {generated_count}")
print(f"最终热点总数: {len(new_hotspots)}")
print(f"数据已保存至 new_hotspots.json")

# 统计各行业数量
industry_counts = {}
for h in new_hotspots:
    for ind in h["industries"]:
        industry_counts[ind] = industry_counts.get(ind, 0) + 1

print(f"\n各行业热点分布:")
for ind, count in sorted(industry_counts.items(), key=lambda x: -x[1]):
    print(f"  {ind}: {count}条")
