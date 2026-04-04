#!/usr/bin/env python3
"""
SKU场景扩展脚本 - 从30个场景扩展到50个
"""
import json
from datetime import datetime

# 定义新增的场景模板（覆盖展示场景、使用场景、对比场景、测评场景等）
NEW_SCENES_TEMPLATES = [
    # 展示场景
    {
        "name": "开箱展示",
        "pain_point": "想看真实的产品外观和细节",
        "resonance": "想要直观了解产品颜值和质感",
        "content_angles": ["开箱实拍展示", "产品细节特写", "颜值质感评测"],
        "hot_topics": ["开箱", "实拍", "颜值", "质感"]
    },
    {
        "name": "场景布置",
        "pain_point": "不知道产品放在家里什么位置好看",
        "resonance": "想要学习产品搭配和空间布置",
        "content_angles": ["产品摆放技巧", "空间搭配指南", "家居风格融合"],
        "hot_topics": ["家居布置", "空间搭配", "摆放技巧", "装饰"]
    },
    {
        "name": "产品对比",
        "pain_point": "同类产品太多不知道怎么选",
        "resonance": "想要客观的产品横向对比",
        "content_angles": ["同类产品横评", "优缺点对比", "选购建议"],
        "hot_topics": ["产品对比", "横评", "选购指南", "优缺点"]
    },
    {
        "name": "功能演示",
        "pain_point": "产品功能太复杂不知道怎么用",
        "resonance": "想要详细的操作演示教程",
        "content_angles": ["功能使用教程", "操作演示", "功能详解"],
        "hot_topics": ["功能演示", "教程", "操作指南", "使用技巧"]
    },
    # 使用场景
    {
        "name": "日常使用",
        "pain_point": "想知道产品日常使用体验如何",
        "resonance": "想要了解真实的使用感受",
        "content_angles": ["日常使用分享", "使用心得", "使用场景展示"],
        "hot_topics": ["日常使用", "使用体验", "心得分享", "使用场景"]
    },
    {
        "name": "旅行出行",
        "pain_point": "出行时不知道带什么装备",
        "resonance": "想要便携实用的出行好物",
        "content_angles": ["旅行必备清单", "出行装备推荐", "便携好物"],
        "hot_topics": ["旅行", "出行", "便携", "旅游装备"]
    },
    {
        "name": "户外活动",
        "pain_point": "户外活动不知道准备什么",
        "resonance": "想要适合户外使用的产品",
        "content_angles": ["户外装备推荐", "户外使用场景", "户外注意事项"],
        "hot_topics": ["户外", "露营", "徒步", "运动户外"]
    },
    {
        "name": "居家办公",
        "pain_point": "居家办公效率低下",
        "resonance": "想要提升居家办公体验",
        "content_angles": ["居家办公好物", "家庭办公室布置", "远程办公装备"],
        "hot_topics": ["居家办公", "远程办公", "家庭办公室", "WFH"]
    },
    {
        "name": "深夜加班",
        "pain_point": "加班熬夜状态差",
        "resonance": "想要缓解加班疲劳的产品",
        "content_angles": ["加班神器推荐", "熬夜必备好物", "缓解疲劳技巧"],
        "hot_topics": ["加班", "熬夜", "工作", "疲劳缓解"]
    },
    {
        "name": "周末宅家",
        "pain_point": "周末宅家不知道怎么打发时间",
        "resonance": "想要提升宅家幸福感",
        "content_angles": ["宅家好物推荐", "周末休闲装备", "提升宅家品质"],
        "hot_topics": ["宅家", "周末", "休闲", "宅家神器"]
    },
    {
        "name": "约会必备",
        "pain_point": "约会不知道怎么准备",
        "resonance": "想要约会时的加分装备",
        "content_angles": ["约会好物推荐", "约会装备清单", "约会加分技巧"],
        "hot_topics": ["约会", "情侣", "浪漫", "约会准备"]
    },
    # 对比场景
    {
        "name": "新旧对比",
        "pain_point": "不知道值不值得升级换代",
        "resonance": "想要新旧产品的真实对比",
        "content_angles": ["新旧款对比", "升级是否值得", "换代建议"],
        "hot_topics": ["新旧对比", "升级", "换代", "值得买吗"]
    },
    {
        "name": "品牌对比",
        "pain_point": "不同品牌不知道选哪个",
        "resonance": "想要客观的品牌横向对比",
        "content_angles": ["品牌对比评测", "各品牌优缺点", "品牌选择建议"],
        "hot_topics": ["品牌对比", "品牌推荐", "品牌选择", "横向评测"]
    },
    {
        "name": "价格对比",
        "pain_point": "不同价位不知道选哪款",
        "resonance": "想要同价位最佳选择",
        "content_angles": ["价格对比分析", "性价比排行", "预算推荐"],
        "hot_topics": ["价格对比", "性价比", "预算", "价位选择"]
    },
    {
        "name": "功能对比",
        "pain_point": "不同功能配置不知道怎么选",
        "resonance": "想要了解各功能的实用性",
        "content_angles": ["功能配置对比", "核心功能分析", "功能需求匹配"],
        "hot_topics": ["功能对比", "配置选择", "功能分析", "需求匹配"]
    },
    # 测评场景
    {
        "name": "耐用性测试",
        "pain_point": "担心产品质量和耐用性",
        "resonance": "想要了解产品的耐用程度",
        "content_angles": ["耐用性实测", "质量评测", "使用寿命测试"],
        "hot_topics": ["耐用性", "质量", "使用寿命", "实测"]
    },
    {
        "name": "性能跑分",
        "pain_point": "想了解产品真实性能",
        "resonance": "想要客观的性能数据",
        "content_angles": ["性能跑分测试", "跑分对比", "性能评测"],
        "hot_topics": ["跑分", "性能", "测试", "benchmark"]
    },
    {
        "name": "续航测试",
        "pain_point": "担心电池续航不够用",
        "resonance": "想要真实的续航数据",
        "content_angles": ["续航实测", "充电测试", "电池使用报告"],
        "hot_topics": ["续航", "电池", "充电", "续航测试"]
    },
    {
        "name": "防水防尘",
        "pain_point": "担心产品防水防尘性能",
        "resonance": "想要了解产品的防护能力",
        "content_angles": ["防水防尘测试", "IP等级解析", "防护性能评测"],
        "hot_topics": ["防水", "防尘", "IP等级", "防护"]
    },
    {
        "name": "温度控制",
        "pain_point": "担心产品发热问题",
        "resonance": "想要了解散热表现",
        "content_angles": ["温度测试", "散热评测", "发热控制"],
        "hot_topics": ["发热", "散热", "温度", "温控"]
    },
    # 人群场景
    {
        "name": "银发老人",
        "pain_point": "老人用起来不方便",
        "resonance": "想要适合老人使用的产品",
        "content_angles": ["老人适用产品", "适老化设计", "老年友好功能"],
        "hot_topics": ["老人", "老年人", "适老化", "银发族"]
    },
    {
        "name": "宝妈群体",
        "pain_point": "带娃没有时间精力",
        "resonance": "想要解放双手的育儿好物",
        "content_angles": ["宝妈必备好物", "育儿神器推荐", "带娃省心装备"],
        "hot_topics": ["宝妈", "育儿", "带娃", "母婴"]
    },
    {
        "name": "数码小白",
        "pain_point": "不懂技术参数不知道怎么选",
        "resonance": "想要简单易懂的选购指南",
        "content_angles": ["小白选购指南", "通俗易懂的参数解析", "新手入门推荐"],
        "hot_topics": ["小白", "新手", "入门", "零基础"]
    },
    {
        "name": "专业人士",
        "pain_point": "专业需求普通产品满足不了",
        "resonance": "想要专业级的性能和功能",
        "content_angles": ["专业级产品推荐", "性能深度评测", "专业使用场景"],
        "hot_topics": ["专业", "专业级", "高性能", "深度评测"]
    },
    {
        "name": "健身达人",
        "pain_point": "健身需要专业装备",
        "resonance": "想要提升健身体验的好物",
        "content_angles": ["健身装备推荐", "运动好物分享", "健身必备清单"],
        "hot_topics": ["健身", "运动", "健身装备", "运动好物"]
    },
    {
        "name": "二次元群体",
        "pain_point": "想要有二次元元素的产品",
        "resonance": "想要符合动漫审美的产品",
        "content_angles": ["二次元联名款", "动漫周边产品", "宅文化好物"],
        "hot_topics": ["二次元", "动漫", "宅", "联名款"]
    },
    # 节日/季节场景
    {
        "name": "双十一攻略",
        "pain_point": "双十一不知道买什么划算",
        "resonance": "想要双十一购物清单",
        "content_angles": ["双十一必买清单", "双十一攻略", "双十一优惠推荐"],
        "hot_topics": ["双十一", "购物节", "优惠", "必买清单"]
    },
    {
        "name": "618攻略",
        "pain_point": "618不知道买什么划算",
        "resonance": "想要618购物清单",
        "content_angles": ["618必买清单", "618攻略", "618优惠推荐"],
        "hot_topics": ["618", "购物节", "优惠", "必买清单"]
    },
    {
        "name": "开学季",
        "pain_point": "开学不知道准备什么",
        "resonance": "想要开学必备好物清单",
        "content_angles": ["开学必备清单", "新生入学好物", "开学装备推荐"],
        "hot_topics": ["开学", "开学季", "学生必备", "入学装备"]
    },
    {
        "name": "换季护肤",
        "pain_point": "换季皮肤问题多",
        "resonance": "想要适合换季使用的护肤产品",
        "content_angles": ["换季护肤推荐", "季节性护肤", "换季保养"],
        "hot_topics": ["换季", "护肤", "季节", "保养"]
    },
    {
        "name": "节日促销",
        "pain_point": "错过节日促销优惠",
        "resonance": "想要抓住促销时机入手",
        "content_angles": ["节日促销攻略", "优惠活动整理", "促销时机推荐"],
        "hot_topics": ["促销", "优惠", "折扣", "节日活动"]
    },
    # 其他场景
    {
        "name": "送礼指南",
        "pain_point": "送礼不知道选什么",
        "resonance": "想要有面子的礼物推荐",
        "content_angles": ["送礼推荐清单", "礼品选购指南", "送礼技巧"],
        "hot_topics": ["送礼", "礼物", "送礼指南", "礼品推荐"]
    },
    {
        "name": "收藏保值",
        "pain_point": "想要收藏有价值的产品",
        "resonance": "想要保值增值的产品",
        "content_angles": ["收藏价值分析", "保值产品推荐", "限量款介绍"],
        "hot_topics": ["收藏", "保值", "限量款", "投资"]
    },
    {
        "name": "二手市场",
        "pain_point": "想买二手但担心质量",
        "resonance": "想要二手选购指南",
        "content_angles": ["二手选购技巧", "二手市场价格", "二手避坑指南"],
        "hot_topics": ["二手", "二手市场", "闲鱼", "转转"]
    },
    {
        "name": "售后服务",
        "pain_point": "担心售后问题",
        "resonance": "想要了解品牌售后服务",
        "content_angles": ["售后服务评测", "保修政策解析", "客服体验分享"],
        "hot_topics": ["售后", "保修", "客服", "服务"]
    },
    {
        "name": "配件推荐",
        "pain_point": "买了产品不知道配什么配件",
        "resonance": "想要提升产品体验的配件",
        "content_angles": ["配件推荐清单", "必备配件", "配件选购指南"],
        "hot_topics": ["配件", "周边", "搭配", "装备"]
    },
    {
        "name": "清洁保养",
        "pain_point": "不知道怎么清洁保养产品",
        "resonance": "想要延长产品使用寿命",
        "content_angles": ["清洁保养教程", "保养技巧分享", "清洁工具推荐"],
        "hot_topics": ["清洁", "保养", "维护", "清洁技巧"]
    },
    {
        "name": "收纳整理",
        "pain_point": "产品太多不知道怎么收纳",
        "resonance": "想要整洁的收纳方案",
        "content_angles": ["收纳技巧分享", "收纳神器推荐", "空间利用方案"],
        "hot_topics": ["收纳", "整理", "收纳神器", "空间利用"]
    },
    {
        "name": "安全隐私",
        "pain_point": "担心数据安全和隐私泄露",
        "resonance": "想要保护个人隐私",
        "content_angles": ["隐私保护方法", "安全使用技巧", "数据安全建议"],
        "hot_topics": ["隐私", "安全", "数据保护", "信息安全"]
    },
    {
        "name": "环保可持续",
        "pain_point": "关注环保和可持续性",
        "resonance": "想要环保的产品选择",
        "content_angles": ["环保产品推荐", "可持续消费", "绿色生活方式"],
        "hot_topics": ["环保", "可持续", "绿色", "低碳"]
    },
    {
        "name": "省钱攻略",
        "pain_point": "预算有限想省钱",
        "resonance": "想要最优惠的购买方式",
        "content_angles": ["省钱技巧", "优惠活动汇总", "最划算的购买时机"],
        "hot_topics": ["省钱", "优惠", "折扣", "划算"]
    },
    {
        "name": "创意玩法",
        "pain_point": "不知道产品还能怎么玩",
        "resonance": "想要发掘产品的隐藏功能",
        "content_angles": ["创意使用方法", "隐藏功能介绍", "花式玩法分享"],
        "hot_topics": ["创意", "玩法", "隐藏功能", "技巧"]
    },
    {
        "name": "搭配推荐",
        "pain_point": "不知道产品怎么搭配使用",
        "resonance": "想要最佳搭配方案",
        "content_angles": ["搭配推荐清单", "配套使用指南", "组合方案"],
        "hot_topics": ["搭配", "组合", "配套", "协同"]
    },
    {
        "name": "问题解决",
        "pain_point": "使用中遇到问题不知道怎么解决",
        "resonance": "想要常见问题的解决方案",
        "content_angles": ["常见问题解答", "故障排除指南", "使用问题解决"],
        "hot_topics": ["问题解决", "故障排除", "使用技巧", "解决方案"]
    },
    {
        "name": "社区分享",
        "pain_point": "想要看更多用户真实反馈",
        "resonance": "想要了解社区口碑",
        "content_angles": ["用户口碑汇总", "社区热门话题", "用户评价分析"],
        "hot_topics": ["口碑", "用户评价", "社区", "热门话题"]
    },
    {
        "name": "新手入门",
        "pain_point": "刚接触这类产品不知道怎么入门",
        "resonance": "想要新手友好的入门指南",
        "content_angles": ["新手入门指南", "从零开始教程", "入门级推荐"],
        "hot_topics": ["新手", "入门", "教程", "零基础"]
    },
    {
        "name": "进阶技巧",
        "pain_point": "基础使用没问题想学习进阶技巧",
        "resonance": "想要提升使用水平",
        "content_angles": ["进阶使用技巧", "高级功能教程", "专业级玩法"],
        "hot_topics": ["进阶", "技巧", "高级功能", "专业玩法"]
    },
    {
        "name": "限量收藏",
        "pain_point": "喜欢限量款和收藏版",
        "resonance": "想要独特的产品版本",
        "content_angles": ["限量款介绍", "收藏价值分析", "特别版推荐"],
        "hot_topics": ["限量", "收藏", "特别版", "限定款"]
    },
    {
        "name": "会员福利",
        "pain_point": "想知道会员有什么福利",
        "resonance": "想要享受会员专属优惠",
        "content_angles": ["会员福利介绍", "会员专属活动", "会员权益解析"],
        "hot_topics": ["会员", "福利", "专属", "权益"]
    },
    {
        "name": "直播带货",
        "pain_point": "直播间买东西不知道靠谱吗",
        "resonance": "想要了解直播购物的注意事项",
        "content_angles": ["直播购物攻略", "直播间优惠对比", "直播注意事项"],
        "hot_topics": ["直播", "带货", "直播间", "主播"]
    },
    {
        "name": "国货之光",
        "pain_point": "想支持国货但不知道选哪个",
        "resonance": "想要品质好的国货产品",
        "content_angles": ["国货品牌推荐", "国货品质评测", "国货vs进口对比"],
        "hot_topics": ["国货", "国产", "国货之光", "国产品牌"]
    },
    {
        "name": "黑科技体验",
        "pain_point": "想体验最新黑科技",
        "resonance": "想要前沿科技产品",
        "content_angles": ["黑科技产品推荐", "新技术体验", "科技前沿探索"],
        "hot_topics": ["黑科技", "新技术", "创新", "科技前沿"]
    },
    {
        "name": "性价比之王",
        "pain_point": "预算有限想要最值的选择",
        "resonance": "想要同价位最好的产品",
        "content_angles": ["性价比排行", "平价好物推荐", "同价位最佳选择"],
        "hot_topics": ["性价比", "平价", "划算", "值得买"]
    },
    {
        "name": "颜值担当",
        "pain_point": "看中产品颜值和设计",
        "resonance": "想要好看又好用的产品",
        "content_angles": ["颜值推荐", "设计美学", "好看又实用"],
        "hot_topics": ["颜值", "好看", "设计", "美学"]
    },
    {
        "name": "小众精品",
        "pain_point": "不想用大众款想要独特的",
        "resonance": "想要小众有品味的产品",
        "content_angles": ["小众品牌推荐", "精品好物分享", "独特设计推荐"],
        "hot_topics": ["小众", "精品", "独特", "品味"]
    },
    {
        "name": "全家共享",
        "pain_point": "想要全家都能用的产品",
        "resonance": "想要适合家庭使用的共享产品",
        "content_angles": ["家庭共享好物", "全家适用推荐", "家庭使用场景"],
        "hot_topics": ["家庭", "全家", "共享", "家庭好物"]
    },
    {
        "name": "宠物友好",
        "pain_point": "家里有宠物担心产品对宠物不好",
        "resonance": "想要宠物友好的产品",
        "content_angles": ["宠物友好产品", "养宠家庭推荐", "宠物安全产品"],
        "hot_topics": ["宠物", "养猫", "养狗", "宠物友好"]
    },
    {
        "name": "租房神器",
        "pain_point": "租房住不能大改动",
        "resonance": "想要租房也能用的好物",
        "content_angles": ["租房必备好物", "不伤租房装备", "租客神器推荐"],
        "hot_topics": ["租房", "出租屋", "租房神器", "租客"]
    },
    {
        "name": "健康生活",
        "pain_point": "关注健康生活方式",
        "resonance": "想要促进健康的产品",
        "content_angles": ["健康好物推荐", "健康生活方式", "健康管理工具"],
        "hot_topics": ["健康", "养生", "健康生活", "健康好物"]
    },
    {
        "name": "智能互联",
        "pain_point": "想要产品能智能联动",
        "resonance": "想要智能家居生态体验",
        "content_angles": ["智能联动方案", "智能家居生态", "设备互联体验"],
        "hot_topics": ["智能", "互联", "智能家居", "联动"]
    },
    {
        "name": "专业创作",
        "pain_point": "用于专业创作需求",
        "resonance": "想要适合创作工作的高性能产品",
        "content_angles": ["创作工具推荐", "专业生产装备", "创作者必备"],
        "hot_topics": ["创作", "专业", "生产力", "创作者"]
    },
    {
        "name": "社交话题",
        "pain_point": "想要有话题性的产品",
        "resonance": "想要能成为社交话题的好物",
        "content_angles": ["热门话题产品", "社交话题好物", "网红爆款推荐"],
        "hot_topics": ["话题", "热门", "网红", "爆款"]
    },
    {
        "name": "意外惊喜",
        "pain_point": "想要意想不到的好产品",
        "resonance": "想要发掘宝藏好物",
        "content_angles": ["宝藏好物推荐", "意外发现的好物", "冷门但好用"],
        "hot_topics": ["宝藏", "惊喜", "冷门好物", "发现"]
    }
]

def expand_sku_scenes(input_file, output_file, target_count=50):
    """扩展SKU场景到指定数量"""
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total_added = 0
    sku_count = 0
    
    for sku in data['skus']:
        existing_names = set(s['name'] for s in sku['scenarios'])
        current_count = len(sku['scenarios'])
        needed = target_count - current_count
        
        if needed <= 0:
            continue
        
        # 随机选择新场景添加（确保不重复）
        added = 0
        for scene in NEW_SCENES_TEMPLATES:
            if scene['name'] in existing_names:
                continue
            if added >= needed:
                break
            
            # 创建场景副本并添加
            new_scene = {
                "name": scene['name'],
                "pain_point": scene['pain_point'],
                "resonance": scene['resonance'],
                "content_angles": scene['content_angles'].copy(),
                "hot_topics": scene['hot_topics'].copy()
            }
            sku['scenarios'].append(new_scene)
            added += 1
        
        total_added += added
        sku_count += 1
        print(f"SKU {sku['sku_name']}: 添加 {added} 个场景，总计 {len(sku['scenarios'])} 个场景")
    
    # 更新元数据
    data['updated_at'] = datetime.now().isoformat()
    total_scenarios = sum(len(sku['scenarios']) for sku in data['skus'])
    data['total_scenarios'] = total_scenarios
    
    # 保存文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n扩展完成!")
    print(f"- 处理SKU数量: {sku_count}")
    print(f"- 新增场景总数: {total_added}")
    print(f"- 场景总数: {total_scenarios}")
    
    return data

if __name__ == '__main__':
    input_file = 'sku_scenes.json'
    output_file = 'sku_scenes.json'
    
    result = expand_sku_scenes(input_file, output_file, target_count=50)
    
    # 生成报告
    report = {
        "timestamp": datetime.now().isoformat(),
        "total_skus": len(result['skus']),
        "total_scenarios": result['total_scenarios'],
        "avg_scenarios_per_sku": result['total_scenarios'] / len(result['skus']),
        "categories_covered": result['categories_covered']
    }
    
    with open('scene_expansion_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n报告已保存到 scene_expansion_report.json")
