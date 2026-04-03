#!/usr/bin/env python3
"""
扩展热点追踪选题数据 - 简化版
目标：
1. client_ideas.json: 从298条扩展到1500条
2. sku_scenes.json: 增加更多SKU场景（目标至少200个场景）
"""

import json
import random
from datetime import datetime

print("=" * 60)
print("🚀 开始扩展热点追踪选题数据")
print("=" * 60)

# ============================================================
# PART 1: 扩展 client_ideas.json
# ============================================================

# 读取现有数据
with open('client_ideas.json', 'r', encoding='utf-8') as f:
    existing_ideas = json.load(f)
print(f"✅ 已读取 client_ideas.json，现有 {len(existing_ideas)} 条选题")

# 品类扩展
CATEGORIES = [
    "3C数码", "美妆", "母婴", "家居", "食品饮料", "服装", "个护", "宠物", "运动户外",
    "汽车用品", "家电", "医药健康", "珠宝配饰", "厨具", "鞋靴", "箱包皮具",
    "办公文具", "图书教育", "数码配件", "内衣袜子", "户外装备", "轻奢", "汽车"
]

# 品牌映射
BRAND_MAP = {
    "3C数码": TECH_BRANDS
}

# 正确引用
CATEGORY_BRAND_MAP["3C数码"] = TECH_BRANDS

BEAUTY_BRANDS = [
    "完美日记", "花西子", "珂拉琪", "橘朵", "酵色", "IntoYou", "彩棠", "毛戈平",
    "珀莱雅", "自然堂", "百雀羚", "相宜本草", "薇诺娜", "玉泽", "HBN", "谷雨", "三月理",
    "雅诗兰黛", "兰蔻", "SK-II", "海蓝之谜", "娇韵诗", "修丽可", "OLAY", "倩碧", "科颜氏",
    "YSL", "阿玛尼", "MAC", "迪奥", "香奈儿", "Tom Ford", "Charlotte Tilbury", "3CE", "CT"
]

MOM_BABY_BRANDS = [
    "飞鹤", "伊利", "君乐宝", "爱他美", "美赞臣", "惠氏", "美素佳儿", "雀巢", "贝因美", "合生元",
    "帮宝适", "好奇", "大王", "花王", "Babycare", "十月结晶", "子初", "全棉时代", "德祐", "碧芭",
    "好孩子", "Safety 1st", "巧儿宜", "Cybex", "Britax", "STM", "AVOVA", "世喜", "Hegen", "贝亲"
]

HOME_BRANDS = [
    "宜家", "宜得利", "无印良品", "网易严选", "小米家居", "华为智选", "Aqara", "绿米",
    "顾家家居", "芝华仕", "左右沙发", "林氏木业", "源氏木语", "原始元素", "泡沫小敏",
    "水星家纺", "罗莱生活", "博洋家纺", "富安娜", "梦洁", "多喜爱", "北极绒", "南极人",
    "九阳", "苏泊尔", "美的", "小熊", "米家", "飞利浦", "松下", "戴森", "添可", "追觅"
]

FOOD_BRANDS = [
    "三只松鼠", "良品铺子", "百草味", "来伊份", "沃隆", "每日坚果", "恰恰", "金帝", "德芙", "费列罗",
    "农夫山泉", "元气森林", "统一", "康师傅", "娃哈哈", "怡宝", "百岁山", "恒大冰泉", "百事可乐", "可口可乐",
    "雀巢咖啡", "瑞幸咖啡", "永璞", "三顿半", "隅田川", "星巴克", "麦咖啡", "奈雪的茶", "喜茶", "乐乐茶"
]

FASHION_BRANDS = [
    "优衣库", "ZARA", "H&M", "GAP", "UR", "热风", "森马", "美特斯邦威", "真维斯", "以纯",
    "太平鸟", "乐町", "欧时力", "哥弟", "阿玛施", "播", "江南布衣", "速写", "less", "mo&co",
    "edition", "地素", "之禾", "ICEBERG", "波司登", "雪中飞", "雅鹿", "红豆", "七匹狼", "杉杉"
]

SPORTS_BRANDS = [
    "耐克", "阿迪达斯", "安踏", "李宁", "361度", "特步", "鸿星尔克", "新百伦", "斯凯奇", "彪马",
    "Under Armour", "Lululemon", "Maia Active", "暴走的萝莉", "粒子狂热", "Keep", "咕咚",
    "骆驼", "探路者", "凯乐石", "始祖鸟", "北面", "哥伦比亚", "迪卡侬"
]

PET_BRANDS = [
    "皇家", "冠能", "渴望", "爱肯拿", "纽顿", "百利", "Instinct", "K9", "巅峰",
    "ziwi", "鲜朗", "麦富迪", "比瑞吉", "网易严选", "江小傲", "宠熙"
]

PET_BRANDS = [
    "皇家", "冠能", "渴望", "爱肯拿", "纽顿", "百利", "Instinct", "K9", "巅峰", "自然逻辑",
    "ziwi", "鲜朗", "麦富迪", "比瑞吉", "网易严选", "江小傲", "宠熙", "诚实一口", "阿飞和巴弟", "帕芬",
    "pidan", "霍曼", "小佩", "CATLINK", "多尼斯", "疯狂小狗", "华元宠具", "派旺", "宠物乐", "纳至"
]

AUTO_BRANDS = [
    "特斯拉", "比亚迪", "理想", "蔚来", "小鹏", "问界", "极氪", "领克", "吉利", "长安",
    "长城", "奇瑞", "广汽", "上汽", "一汽", "东风", "北京现代", "东风日产", "广汽本田", "东风本田",
    "宝马", "奔驰", "奥迪", "大众", "保时捷", "路虎", "捷豹", "MINI", "Smart", "甲壳虫"
]

# 品类-品牌映射
CATEGORY_BRAND_MAP = {
    "3C数码": TECH_BRANDS,
    "美妆": BEAUTY_BRANDS,
    "母婴": MOM_BABY_BRANDS,
    "家居": HOME_BRANDS,
    "食品饮料": FOOD_BRANDS,
    "服装": FASHION_BRANDS,
    "运动户外": SPORTS_BRANDS,
    "宠物": PET_BRANDS,
    "汽车": AUTO_BRANDS,
    "汽车用品": ["3M", "龟牌", "车仆", "固特威", "蓝星", "道可视", "飞鸽", "铁将军", "纽曼", "70迈"],
    "家电": ["美的", "格力", "海尔", "海信", "TCL", "创维", "长虹", "小米", "华为", "云米"],
    "医药健康": ["云南白药", "同仁堂", "九芝堂", "马应龙", "片仔癀", "白云山", "康恩贝", "金水宝", "金嗓子", "华润三九"],
    "珠宝配饰": ["周大福", "周生生", "六福珠宝", "老凤祥", "老庙黄金", "中国黄金", "萃华金店", "金大福", "潮宏基", "周六福"],
    "厨具": ["WMF", "双立人", "菲仕乐", "福腾宝", "拉歌蒂尼", "Le Creuset", "Staub", "Lodge", "柳宗理", "吉川"],
    "鞋靴": SPORTS_BRANDS[:20],
    "箱包皮具": ["新秀丽", "外交官", "美旅", "瑞士军刀", "皇冠", "爱华仕", "外交官", "90分", "小米90分", "地平线8号"],
    "办公文具": ["得力", "晨光", "真彩", "齐心", "广博", "三年二班", "MUJI", "国誉", "KOKUYO", "MIDORI"],
    "图书教育": ["新东方", "学而思", "猿辅导", "作业帮", "高途", "有道", "流利说", "沪江", "百词斩", "扇贝"],
    "数码配件": ["绿联", "倍思", "品胜", "罗马仕", "Anker", "紫米", "小米", "华为", "OPPO", "vivo"],
    "内衣袜子": ["维多利亚的秘密", "华歌尔", "黛安芬", "安莉芳", "曼妮芬", "歌瑞尔", "内外", "NEIWAI", "Ubras", "蕉内"],
    "户外装备": ["骆驼", "探路者", "凯乐石", "北面", "哥伦比亚", "始祖鸟", "巴塔哥尼亚", "土拨鼠", "猛犸象", "可隆"],
    "轻奢": ["Coach", "MK", "Kate Spade", "Tory Burch", "Furla", "珑骧", "Longchamp", "Michael Kors", "Rebecca Minkoff", "APM Monaco"],
    "个护": ["飞利浦", "飞科", "松下", "博朗", "戴森", "素士", "usmile", "扉乐", "欧乐B", "高露洁"]
}

# 选题角度
ANGLES = [
    "真实使用一个月后的感受", "那些网上不会告诉你的细节", "和同类产品对比真实体验",
    "同价位最值得买的一款", "平价替代方案", "什么时候买最划算",
    "专业维度深度测评", "实验室数据对比", "真实数据说话",
    "同类产品避坑指南", "选购要点总结", "常见选购误区",
    "升级替换推荐", "新旧对比体验", "值得投资的品类",
    "针对痛点的产品推荐", "问题终结者产品", "用了就回不去的体验",
    "生日礼物创意推荐", "投其所好的礼物选择", "仪式感礼物推荐",
    "节日送礼清单推荐", "不同预算的送礼方案", "收礼人真实反馈",
    "居家必备神器", "提升幸福感的家居好物", "懒人必备产品",
    "职场必备好物", "提升效率的工具", "办公桌收纳指南",
    "学生党必买清单", "宿舍好物推荐", "性价比最高的平替",
    "出行必带好物", "旅行收纳技巧", "便携式产品推荐"
]

# 热门话题
HOT_TOPICS = [
    "真实测评", "自用分享", "踩坑经历", "真实推荐",
    "性价比", "平价好物", "省钱攻略", "必买清单",
    "深度测评", "专业测评", "数据对比", "横评",
    "避坑指南", "智商税", "选购指南", "避雷",
    "升级替换", "新旧对比", "值得买", "投资自己",
    "痛点解决", "神器推荐", "问题解决", "刚需好物",
    "生日礼物", "惊喜礼物", "仪式感", "创意礼物",
    "节日送礼", "礼物推荐", "送长辈", "送对象",
    "居家好物", "生活品质", "懒人必备", "幸福感"
]

# 场景模板
SCENARIOS = [
    "生日惊喜", "节日送礼", "见家长礼物", "结婚礼物", "满月礼", "乔迁之喜",
    "毕业礼物", "父亲节礼物", "母亲节礼物", "七夕礼物", "跨年礼物", "老师礼物",
    "备婚必买", "新手爸妈必备", "入园准备", "考研党装备", "留学行李", "租房改造",
    "独居必备", "职场复出", "拯救拖延症", "缓解焦虑", "拯救敏感肌", "减脂期必备",
    "提升免疫力", "改善体态", "护眼必备", "护发护齿", "厨房小白", "低成本变美",
    "熬夜急救", "姨妈期好物", "坐月子必备", "真实自用分享", "性价比之选", "深度测评",
    "避坑指南", "升级替换", "开箱体验", "真实横评", "长期使用报告", "平替方案",
    "小众宝藏", "居家日常", "职场人装备", "学生党必备", "出行必备", "露营装备",
    "健身运动", "宠物养育", "极简生活", "抗老护肤", "成分党护肤", "精致出行",
    "健康饮食", "早餐神器", "厨房收纳", "全屋清洁", "衣橱整理", "仪式感生活"
]

# 生成新选题
new_ideas = []
existing_ideas_list = existing_ideas if isinstance(existing_ideas, list) else []

# 从现有选题提取结构
if existing_ideas_list:
    sample_idea = existing_ideas_list[0] if existing_ideas_list else {}
    idea_keys = list(sample_idea.keys())
else:
    idea_keys = ['title', 'category', 'brand', 'angle', 'hot_topics', 'scenario']

# 目标数量
TARGET_IDEAS = 1500
ideas_needed = max(0, TARGET_IDEAS - len(existing_ideas_list))

print(f"📊 需要生成 {ideas_needed} 条新选题")

# 生成新选题
generated_count = 0
for category in CATEGORIES:
    brands = CATEGORY_BRAND_MAP.get(category, ["通用品牌"])
    for brand in brands[:15]:  # 每个品类最多15个品牌
        for scenario in SCENARIOS[:10]:  # 每个品牌最多10个场景
            if generated_count >= ideas_needed:
                break
            
            # 随机选择角度和热门话题
            angle = random.choice(ANGLES)
            topics = random.sample(HOT_TOPICS, min(4, len(HOT_TOPICS)))
            
            # 生成标题
            title_templates = [
                f"{brand}{scenario}好物推荐",
                f"{category}必备：{brand}真实测评",
                f"{brand}怎么选？{scenario}避坑指南",
                f"{scenario}神器：{brand}使用心得",
                f"{brand}值得买吗？{category}深度测评",
                f"{category}好物：{brand}{scenario}推荐",
                f"测评{brand}：{scenario}真实体验",
                f"{brand}vs竞品：{scenario}横评对比"
            ]
            title = random.choice(title_templates)
            
            # 构建选题对象
            new_idea = {
                'title': title,
                'category': category,
                'brand': brand,
                'angle': angle,
                'hot_topics': topics,
                'scenario': scenario,
                'generated_at': datetime.now().isoformat()
            }
            new_ideas.append(new_idea)
            generated_count += 1
            
        if generated_count >= ideas_needed:
            break
    if generated_count >= ideas_needed:
        break

# 合并并保存
all_ideas = existing_ideas_list + new_ideas
with open('client_ideas.json', 'w', encoding='utf-8') as f:
    json.dump(all_ideas, f, ensure_ascii=False, indent=2)

print(f"✅ client_ideas.json 扩展完成：{len(existing_ideas_list)} → {len(all_ideas)} 条")

# ============================================================
# PART 2: 扩展 sku_scenes.json
# ============================================================

print("\n" + "=" * 60)
print("📦 开始扩展 SKU 场景库")
print("=" * 60)

# 读取现有 SKU 数据
try:
    with open('sku_scenes.json', 'r', encoding='utf-8') as f:
        existing_sku_data = json.load(f)
    print(f"✅ 已读取 sku_scenes.json")
except Exception as e:
    print(f"⚠️ 读取失败，创建新数据: {e}")
    existing_sku_data = {'skus': [], 'total_skus': 0, 'total_scenarios': 0}

# SKU 产品列表
SKU_PRODUCTS = []

# 3C数码
for brand in TECH_BRANDS[:20]:
    products = [
        f"{brand}旗舰手机", f"{brand}平板电脑", f"{brand}笔记本电脑",
        f"{brand}无线耳机", f"{brand}智能手表", f"{brand}充电宝",
        f"{brand}数据线", f"{brand}保护壳", f"{brand}充电器"
    ]
    for p in products:
        SKU_PRODUCTS.append({
            'name': p,
            'category': '3C数码',
            'brand': brand
        })

# 美妆
for brand in BEAUTY_BRANDS[:15]:
    products = [
        f"{brand}精华液", f"{brand}面霜", f"{brand}眼霜",
        f"{brand}粉底液", f"{brand}口红", f"{brand}面膜",
        f"{brand}洁面乳", f"{brand}化妆水"
    ]
    for p in products:
        SKU_PRODUCTS.append({
            'name': p,
            'category': '美妆',
            'brand': brand
        })

# 母婴
for brand in MOM_BABY_BRANDS[:15]:
    products = [
        f"{brand}奶粉", f"{brand}纸尿裤", f"{brand}婴儿推车",
        f"{brand}安全座椅", f"{brand}奶瓶", f"{brand}湿巾"
    ]
    for p in products:
        SKU_PRODUCTS.append({
            'name': p,
            'category': '母婴',
            'brand': brand
        })

# 家居
for brand in HOME_BRANDS[:15]:
    products = [
        f"{brand}沙发", f"{brand}床垫", f"{brand}四件套",
        f"{brand}台灯", f"{brand}吸尘器", f"{brand}空气净化器"
    ]
    for p in products:
        SKU_PRODUCTS.append({
            'name': p,
            'category': '家居',
            'brand': brand
        })

# 食品饮料
for brand in FOOD_BRANDS[:15]:
    products = [
        f"{brand}坚果礼盒", f"{brand}饮料", f"{brand}咖啡",
        f"{brand}牛奶", f"{brand}零食大礼包", f"{brand}代餐"
    ]
    for p in products:
        SKU_PRODUCTS.append({
            'name': p,
            'category': '食品饮料',
            'brand': brand
        })

# 服装
for brand in FASHION_BRANDS[:15]:
    products = [
        f"{brand}卫衣", f"{brand}羽绒服", f"{brand}牛仔裤",
        f"{brand}T恤", f"{brand}连衣裙", f"{brand}外套"
    ]
    for p in products:
        SKU_PRODUCTS.append({
            'name': p,
            'category': '服装',
            'brand': brand
        })

# 运动户外
for brand in SPORTS_BRANDS[:15]:
    products = [
        f"{brand}运动鞋", f"{brand}运动服", f"{brand}瑜伽裤",
        f"{brand}跑步机", f"{brand}健身器材", f"{brand}帐篷"
    ]
    for p in products:
        SKU_PRODUCTS.append({
            'name': p,
            'category': '运动户外',
            'brand': brand
        })

# 宠物
for brand in PET_BRANDS[:15]:
    products = [
        f"{brand}猫粮", f"{brand}狗粮", f"{brand}宠物窝",
        f"{brand}猫砂", f"{brand}宠物玩具", f"{brand}宠物背包"
    ]
    for p in products:
        SKU_PRODUCTS.append({
            'name': p,
            'category': '宠物',
            'brand': brand
        })

# 扩展场景
EXTENDED_SCENARIOS = []
for s in SCENARIOS:
    EXTENDED_SCENARIOS.append({
        'name': s,
        'pain_point': f"{s}场景下的用户痛点",
        'resonance': f"解决{s}相关需求",
        'content_angles': random.sample(ANGLES, 3),
        'hot_topics': random.sample(HOT_TOPICS, 4)
    })

# 构建 SKU 场景数据
new_skus = []
for sku in SKU_PRODUCTS:
    # 每个SKU分配3-6个场景
    num_scenarios = random.randint(3, 6)
    selected_scenarios = random.sample(EXTENDED_SCENARIOS, num_scenarios)
    
    sku_data = {
        'sku_name': sku['name'],
        'client': f"{sku['category']}-{sku['brand']}",
        'specs': f"规格参数 | {sku['brand']}出品",
        'selling_points': [
            f"{sku['brand']}品质保证",
            f"{sku['category']}明星产品",
            "高性价比选择",
            "用户好评如潮"
        ],
        'scenarios': selected_scenarios
    }
    new_skus.append(sku_data)

# 合并或替换
final_skus = existing_sku_data.get('skus', []) + new_skus
total_scenarios = sum(len(s.get('scenarios', [])) for s in final_skus)

sku_output = {
    'generated_at': datetime.now().isoformat(),
    'updated_at': datetime.now().isoformat(),
    'total_skus': len(final_skus),
    'total_scenarios': total_scenarios,
    'categories_covered': list(set(CATEGORIES)),
    'skus': final_skus
}

with open('sku_scenes.json', 'w', encoding='utf-8') as f:
    json.dump(sku_output, f, ensure_ascii=False, indent=2)

print(f"✅ sku_scenes.json 扩展完成")
print(f"   - SKU 数量: {len(final_skus)} 个")
print(f"   - 场景总数: {total_scenarios} 个")
print(f"   - 覆盖品类: {len(set(CATEGORIES))} 个")

# ============================================================
# 汇总报告
# ============================================================
print("\n" + "=" * 60)
print("📊 扩展完成汇总")
print("=" * 60)
print(f"✅ client_ideas.json: {len(all_ideas)} 条选题")
print(f"✅ sku_scenes.json: {len(final_skus)} 个SKU, {total_scenarios} 个场景")
print("=" * 60)
