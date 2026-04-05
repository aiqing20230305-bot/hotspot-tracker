#!/usr/bin/env python3
"""
扩展SKU场景数据 - 为场景数量不足的SKU补充更多场景
"""

import json
from datetime import datetime

# 通用场景模板库
SCENARIO_TEMPLATES = [
    # 节日送礼类
    {"name": "新年礼物", "pain_point": "新年不知道送什么礼物", "resonance": "想要送出有新年祝福意义的礼物", "content_angles": ["新年礼物推荐", "过年送礼清单", "新年好物"], "hot_topics": ["新年", "过年", "新年礼物", "跨年"]},
    {"name": "情人节限定", "pain_point": "情人节想送特别的礼物", "resonance": "想要独一无二的节日礼物", "content_angles": ["情人节礼物推荐", "节日特别款", "浪漫礼盒"], "hot_topics": ["情人节", "限定", "520", "七夕"]},
    {"name": "七夕特别", "pain_point": "七夕想送有中国特色的礼物", "resonance": "想要有传统文化底蕴的礼物", "content_angles": ["七夕礼物推荐", "中国式浪漫", "传统节日好物"], "hot_topics": ["七夕", "中国情人节", "传统文化", "牛郎织女"]},
    {"name": "圣诞节礼物", "pain_point": "圣诞节不知道送什么", "resonance": "想要有节日氛围的礼物", "content_angles": ["圣诞礼物推荐", "圣诞限定好物", "节日氛围布置"], "hot_topics": ["圣诞节", "圣诞礼物", "平安夜", "跨年"]},
    {"name": "女神节专属", "pain_point": "三八节不知道送什么", "resonance": "想要送女性专属好物", "content_angles": ["女神节礼物", "女性专属推荐", "女王节好物"], "hot_topics": ["女神节", "三八节", "女王节", "女性礼物"]},
    {"name": "母亲节礼物", "pain_point": "母亲节不知道送什么", "resonance": "想送妈妈有意义又实用的礼物", "content_angles": ["母亲节礼物推荐", "送妈妈什么好", "感恩母亲"], "hot_topics": ["母亲节", "送妈妈", "妈妈礼物", "感恩"]},
    {"name": "父亲节礼物", "pain_point": "父亲节不知道送什么", "resonance": "想送爸爸实用又有品质的礼物", "content_angles": ["父亲节礼物推荐", "送爸爸什么好", "老爸的心意"], "hot_topics": ["父亲节", "送爸爸", "爸爸礼物", "父爱"]},
    {"name": "儿童节礼物", "pain_point": "儿童节不知道送孩子什么", "resonance": "想送孩子喜欢又有意义的礼物", "content_angles": ["儿童节礼物推荐", "孩子喜欢的礼物", "六一礼物清单"], "hot_topics": ["儿童节", "六一", "孩子礼物", "亲子"]},
    {"name": "教师节礼物", "pain_point": "教师节不知道送老师什么", "resonance": "想要表达感谢又不失礼貌", "content_angles": ["教师节礼物推荐", "送老师什么好", "尊师重道好物"], "hot_topics": ["教师节", "送老师", "感恩老师", "老师礼物"]},
    {"name": "中秋送礼", "pain_point": "中秋节送礼选择困难", "resonance": "想要有中秋元素的礼物", "content_angles": ["中秋礼盒推荐", "月饼搭配好物", "团圆节送礼"], "hot_topics": ["中秋节", "月饼", "团圆", "中秋礼盒"]},
    {"name": "春节年货", "pain_point": "过年不知道买什么年货", "resonance": "想要有年味又实用的年货", "content_angles": ["年货清单推荐", "过年必备好物", "年味满满"], "hot_topics": ["春节", "年货", "过年", "新年好物"]},
    
    # 人生节点类
    {"name": "生日惊喜", "pain_point": "朋友/对象生日不知道送什么", "resonance": "想送出有新意又实用的礼物", "content_angles": ["生日礼物创意推荐", "投其所好的礼物选择", "仪式感礼物推荐"], "hot_topics": ["生日礼物", "惊喜礼物", "仪式感", "创意礼物"]},
    {"name": "毕业礼物", "pain_point": "同学朋友毕业不知道送什么", "resonance": "想要送出有纪念意义的毕业礼物", "content_angles": ["毕业礼物清单", "同学礼物推荐", "有纪念意义的好物"], "hot_topics": ["毕业", "同学礼物", "毕业季", "升学"]},
    {"name": "乔迁新居", "pain_point": "搬新家不知道买什么", "resonance": "想要打造温馨舒适的新家", "content_angles": ["新家必备清单", "搬家好物推荐", "入住必备神器"], "hot_topics": ["乔迁之喜", "新家布置", "搬家清单", "入住好物"]},
    {"name": "新婚礼物", "pain_point": "朋友结婚不知道送什么", "resonance": "想送实用又有心意的新婚礼物", "content_angles": ["新婚礼物推荐", "结婚好物分享", "新婚祝福礼"], "hot_topics": ["新婚礼物", "结婚好物", "新婚祝福", "婚礼礼物"]},
    {"name": "宝宝出生", "pain_point": "朋友生宝宝不知道送什么", "resonance": "想送实用又安全的母婴礼物", "content_angles": ["新生儿礼物推荐", "满月礼物清单", "母婴好物分享"], "hot_topics": ["新生儿礼物", "满月礼", "宝宝礼物", "母婴好物"]},
    {"name": "升职加薪", "pain_point": "升职了想犒劳自己", "resonance": "想要奖励自己更有品质的生活", "content_angles": ["升职奖励自己", "职场进阶好物", "品质生活分享"], "hot_topics": ["升职", "加薪", "犒劳自己", "职场好物"]},
    
    # 生活场景类
    {"name": "日常通勤", "pain_point": "每天通勤需要实用好物", "resonance": "想要提升通勤体验", "content_angles": ["通勤必备好物", "上班族推荐", "日常实用清单"], "hot_topics": ["通勤", "上班族", "日常好物", "实用推荐"]},
    {"name": "居家办公", "pain_point": "在家办公需要好装备", "resonance": "想要提升居家办公效率", "content_angles": ["居家办公装备", "WFH好物推荐", "远程办公神器"], "hot_topics": ["居家办公", "WFH", "远程办公", "在家工作"]},
    {"name": "运动健身", "pain_point": "想培养运动习惯", "resonance": "想要适合新手的运动装备", "content_angles": ["健身入门装备", "运动好物推荐", "运动打卡分享"], "hot_topics": ["健身", "运动", "减肥", "健康生活"]},
    {"name": "旅行出游", "pain_point": "旅行不知道带什么", "resonance": "想要旅行必备好物", "content_angles": ["旅行好物清单", "出游必备神器", "旅行装备分享"], "hot_topics": ["旅行", "出游", "旅行好物", "出行必备"]},
    {"name": "宅家必备", "pain_point": "喜欢宅家但想提升生活品质", "resonance": "想要让宅家生活更舒适", "content_angles": ["宅家好物推荐", "居家生活神器", "幸福感提升"], "hot_topics": ["宅家", "居家好物", "生活品质", "幸福感"]},
    {"name": "夜猫子必备", "pain_point": "经常熬夜需要护肝护肤", "resonance": "想要减少熬夜伤害", "content_angles": ["熬夜党必备", "护肝养颜好物", "熬夜补救方案"], "hot_topics": ["熬夜", "护肝", "护肤", "养生"]},
    {"name": "学生党必备", "pain_point": "学生预算有限需要高性价比", "resonance": "想要在有限预算内买最实用的", "content_angles": ["学生党必买清单", "宿舍好物推荐", "性价比最高的平替"], "hot_topics": ["学生党", "宿舍好物", "开学必备", "平价好物"]},
    {"name": "租房一族", "pain_point": "租房想布置但怕浪费", "resonance": "想要便宜又好用的租房好物", "content_angles": ["租房好物推荐", "出租屋改造", "搬家必带清单"], "hot_topics": ["租房", "出租屋", "搬家好物", "租房改造"]},
    {"name": "养宠家庭", "pain_point": "养宠物需要好物", "resonance": "想要让宠物更舒适健康", "content_angles": ["宠物好物推荐", "养猫狗必备", "宠物用品测评"], "hot_topics": ["养宠", "宠物好物", "猫咪", "狗狗"]},
    {"name": "宝爸宝妈", "pain_point": "带娃需要实用好物", "resonance": "想要让带娃更轻松", "content_angles": ["带娃好物分享", "育儿神器推荐", "新手爸妈必看"], "hot_topics": ["带娃", "育儿", "新手爸妈", "母婴好物"]},
    {"name": "独居生活", "pain_point": "独居需要安全便利好物", "resonance": "想要独居生活更安心", "content_angles": ["独居好物推荐", "一人居必备", "独居安全清单"], "hot_topics": ["独居", "一人居", "独居好物", "安全生活"]},
    {"name": "情侣日常", "pain_point": "情侣想一起用好玩的东西", "resonance": "想要增进感情的好物", "content_angles": ["情侣好物分享", "恋爱必备", "甜蜜日常"], "hot_topics": ["情侣", "恋爱", "情侣好物", "甜蜜日常"]},
    
    # 消费决策类
    {"name": "性价比之选", "pain_point": "预算有限想买最值的产品", "resonance": "想要花最少的钱买最值的东西", "content_angles": ["同价位最值得买的一款", "平价替代方案", "什么时候买最划算"], "hot_topics": ["性价比", "平价好物", "省钱攻略", "必买清单"]},
    {"name": "真实自用分享", "pain_point": "网上种草太多不知道哪个真正好用", "resonance": "想要真实的用户体验", "content_angles": ["真实使用一个月后的感受", "网上不会告诉你的细节", "和同类产品对比真实体验"], "hot_topics": ["自用分享", "真实测评", "踩坑经历", "真实推荐"]},
    {"name": "避坑指南", "pain_point": "担心买到踩坑产品", "resonance": "想要避开智商税产品", "content_angles": ["同类产品避坑指南", "选购要点总结", "常见选购误区"], "hot_topics": ["避坑指南", "智商税", "选购指南", "避雷"]},
    {"name": "深度测评", "pain_point": "想了解产品真实性能", "resonance": "想要专业详尽的产品分析", "content_angles": ["专业维度深度测评", "实验室数据对比", "真实数据说话"], "hot_topics": ["深度测评", "专业测评", "数据对比", "横评"]},
    {"name": "开箱体验", "pain_point": "想了解产品开箱第一印象", "resonance": "想要看到真实的产品细节", "content_angles": ["惊喜开箱分享", "第一眼感受", "包装细节展示"], "hot_topics": ["开箱", "开箱测评", "新品开箱", "开箱分享"]},
    {"name": "好物推荐", "pain_point": "想找值得买的好物", "resonance": "想要不踩雷的购买建议", "content_angles": ["真心推荐的好物", "回购率超高的单品", "用过都说好的产品"], "hot_topics": ["好物推荐", "必买清单", "回购好物", "真心推荐"]},
    {"name": "省钱攻略", "pain_point": "想省钱买好东西", "resonance": "想要最优惠的购买渠道", "content_angles": ["省钱购买技巧", "优惠券攻略", "最低价入手时间"], "hot_topics": ["省钱", "优惠", "攻略", "薅羊毛"]},
    {"name": "品牌对比", "pain_point": "在几个品牌间纠结", "resonance": "想了解各品牌的优缺点", "content_angles": ["品牌横向对比", "各品牌差异分析", "选购建议"], "hot_topics": ["对比", "品牌对比", "横评", "选购"]},
    {"name": "新手入门", "pain_point": "刚接触这类产品不知道怎么选", "resonance": "想要新手友好的入门推荐", "content_angles": ["新手入门指南", "小白必看选购", "从零开始推荐"], "hot_topics": ["新手", "入门", "小白必看", "新手推荐"]},
    
    # 季节时令类
    {"name": "换季必备", "pain_point": "换季不知道买什么", "resonance": "想要应对换季的好物", "content_angles": ["换季好物清单", "季节更替必备", "换季护肤攻略"], "hot_topics": ["换季", "季节", "春夏必备", "秋冬好物"]},
    {"name": "夏季清凉", "pain_point": "夏天太热想要清凉好物", "resonance": "想要夏天降温神器", "content_angles": ["夏季清凉好物", "避暑神器推荐", "夏天必备清单"], "hot_topics": ["夏天", "清凉", "避暑", "夏日好物"]},
    {"name": "冬季保暖", "pain_point": "冬天太冷想要保暖好物", "resonance": "想要冬天取暖神器", "content_angles": ["冬季保暖好物", "取暖神器推荐", "过冬必备清单"], "hot_topics": ["冬天", "保暖", "取暖", "过冬好物"]},
    {"name": "开学季", "pain_point": "开学不知道买什么", "resonance": "想要开学必备好物", "content_angles": ["开学必备清单", "学生党开学好物", "新学期装备"], "hot_topics": ["开学", "学生党", "开学季", "新学期"]},
    {"name": "双11攻略", "pain_point": "双11不知道买什么最划算", "resonance": "想要双11凑单好物", "content_angles": ["双11必买清单", "双十一凑单攻略", "大促省钱指南"], "hot_topics": ["双11", "双十一", "大促", "购物节"]},
    {"name": "618攻略", "pain_point": "618不知道买什么最划算", "resonance": "想要618凑单好物", "content_angles": ["618必买清单", "年中大促攻略", "618省钱指南"], "hot_topics": ["618", "年中大促", "购物节", "省钱攻略"]},
    
    # 社交场景类
    {"name": "送礼面子足", "pain_point": "想送礼有面子但预算有限", "resonance": "想送看起来高端但不贵的礼物", "content_angles": ["送礼有面子推荐", "小预算大面子", "送礼不踩雷"], "hot_topics": ["送礼", "面子", "高端礼物", "送礼攻略"]},
    {"name": "闺蜜分享", "pain_point": "想和闺蜜分享好物", "resonance": "想要闺蜜一起用的好东西", "content_angles": ["闺蜜同款好物", "姐妹一起入坑", "闺蜜礼物推荐"], "hot_topics": ["闺蜜", "姐妹", "闺蜜同款", "姐妹好物"]},
    {"name": "情侣同款", "pain_point": "想和对象用情侣款", "resonance": "想要情侣一起用好物", "content_angles": ["情侣同款推荐", "情侣必备好物", "甜蜜同款分享"], "hot_topics": ["情侣同款", "情侣好物", "甜蜜日常", "情侣必备"]},
    {"name": "父母孝心", "pain_point": "想给父母买好东西", "resonance": "想要实用又能表达孝心的礼物", "content_angles": ["送父母好物推荐", "孝心礼物清单", "爸妈喜欢的好物"], "hot_topics": ["送父母", "孝心", "父母礼物", "孝敬长辈"]},
    {"name": "领导送礼", "pain_point": "想送领导得体的礼物", "resonance": "想要正式又有品质的商务礼物", "content_angles": ["送领导礼物推荐", "商务礼品指南", "体面送礼"], "hot_topics": ["送领导", "商务送礼", "职场礼物", "正式场合"]},
]

def expand_sku_scenarios(sku, target_count=50):
    """为SKU扩展场景"""
    existing_names = {s.get('name') for s in sku.get('scenarios', [])}
    current_count = len(sku.get('scenarios', []))
    
    if current_count >= target_count:
        return sku
    
    # 添加新场景直到达到目标数量
    for template in SCENARIO_TEMPLATES:
        if len(sku.get('scenarios', [])) >= target_count:
            break
        if template['name'] not in existing_names:
            if 'scenarios' not in sku:
                sku['scenarios'] = []
            sku['scenarios'].append(template.copy())
            existing_names.add(template['name'])
    
    return sku

def main():
    input_path = '/Users/zhangjingwei/.qclaw/workspace/hotspot-tracker/sku_scenes.json'
    output_path = '/Users/zhangjingwei/.qclaw/workspace/hotspot-tracker/sku_scenes.json'
    
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    skus = data.get('skus', [])
    
    # Remove duplicates - keep the one with more scenarios
    unique_skus = {}
    for s in skus:
        name = s.get('sku_name')
        scenarios = s.get('scenarios', [])
        if name not in unique_skus:
            unique_skus[name] = s
        else:
            if len(scenarios) > len(unique_skus[name].get('scenarios', [])):
                unique_skus[name] = s
    
    # Expand scenarios for SKUs with fewer than 50 scenarios
    expanded_count = 0
    for name, sku in unique_skus.items():
        original_count = len(sku.get('scenarios', []))
        if original_count < 50:
            sku = expand_sku_scenarios(sku, target_count=50)
            new_count = len(sku.get('scenarios', []))
            if new_count > original_count:
                expanded_count += 1
                print(f"Expanded {name}: {original_count} -> {new_count} scenarios")
    
    # Update data
    cleaned_skus = list(unique_skus.values())
    total_scenarios = sum(len(s.get('scenarios', [])) for s in cleaned_skus)
    
    data['skus'] = cleaned_skus
    data['total_skus'] = len(cleaned_skus)
    data['total_scenarios'] = total_scenarios
    data['updated_at'] = datetime.now().isoformat()
    
    # Save
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n=== Expansion Complete ===")
    print(f"Total unique SKUs: {len(cleaned_skus)}")
    print(f"Total scenarios: {total_scenarios}")
    print(f"SKUs expanded: {expanded_count}")

if __name__ == '__main__':
    main()
