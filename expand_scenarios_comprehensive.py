#!/usr/bin/env python3
"""
SKU场景全面扩展脚本
目标：将每个SKU的场景从6个扩展到20+个，确保覆盖多维度使用场景
"""

import json
from datetime import datetime
import random

# 通用场景模板库 - 按维度分类
SCENARIO_TEMPLATES = {
    "送礼场景": [
        {"name": "节日送礼", "pain_point": "节日不知道送什么礼物", "resonance": "想要送出既有面子又实用的礼物", "content_angles": ["节日送礼清单推荐", "不同预算的送礼方案", "收礼人真实反馈"], "hot_topics": ["节日送礼", "礼物推荐", "送长辈", "送对象"]},
        {"name": "生日惊喜", "pain_point": "朋友/对象生日不知道送什么", "resonance": "想送出有新意又实用的礼物", "content_angles": ["生日礼物创意推荐", "投其所好的礼物选择", "仪式感礼物推荐"], "hot_topics": ["生日礼物", "惊喜礼物", "仪式感", "创意礼物"]},
        {"name": "闺蜜送礼", "pain_point": "闺蜜生日/节日不知道送什么", "resonance": "想要送出既有心意又不踩雷的礼物", "content_angles": ["闺蜜礼物推荐", "闺蜜想要什么", "小众有心意的好物"], "hot_topics": ["闺蜜礼物", "送闺蜜", "女生礼物", "有心意"]},
        {"name": "送父母长辈", "pain_point": "给父母买东西总是被说不实用", "resonance": "想要送父母真正需要又让他们开心的礼物", "content_angles": ["送父母清单", "长辈真实需求", "不踩雷的孝心礼物"], "hot_topics": ["送父母", "长辈礼物", "孝心", "送爸妈"]},
        {"name": "520/情人节", "pain_point": "情侣节日不知道送什么", "resonance": "想要浪漫又有心意的礼物打动对方", "content_angles": ["情人节礼物清单", "浪漫惊喜推荐", "对象心动好物"], "hot_topics": ["情人节", "520", "送对象", "浪漫礼物", "七夕"]},
        {"name": "春节年货", "pain_point": "过年不知道买什么年货", "resonance": "想要准备丰盛又有年味的春节好物", "content_angles": ["年货清单推荐", "过年必备好物", "送礼年货选择"], "hot_topics": ["春节", "年货", "过年", "送礼清单"]},
        {"name": "母亲节专属", "pain_point": "母亲节不知道送妈妈什么", "resonance": "想要表达对妈妈的爱和感激", "content_angles": ["母亲节礼物", "妈妈需要什么", "感恩妈妈的好物"], "hot_topics": ["母亲节", "送妈妈", "感恩", "妈妈礼物"]},
        {"name": "父亲节专属", "pain_point": "父亲节送礼物总是被嫌弃", "resonance": "想要送爸爸真正需要又让他满意的礼物", "content_angles": ["父亲节礼物", "爸爸真正需要", "实用型孝心礼物"], "hot_topics": ["父亲节", "送爸爸", "爸爸礼物", "孝心"]},
        {"name": "儿童节好物", "pain_point": "想给孩子准备节日礼物", "resonance": "想要让孩子开心又有教育意义的好物", "content_angles": ["儿童节礼物", "送给孩子的礼物", "寓教于乐好物"], "hot_topics": ["儿童节", "送孩子", "六一", "孩子礼物"]},
        {"name": "新婚礼物", "pain_point": "朋友结婚不知道送什么", "resonance": "想要送既有面子又实用新婚礼物", "content_angles": ["新婚礼物推荐", "结婚礼品清单", "送新人什么好"], "hot_topics": ["新婚", "结婚礼物", "送新人", "喜礼"]},
        {"name": "满月百日宴", "pain_point": "宝宝满月/百日不知道送什么", "resonance": "想要送有新意又有心意的新生儿礼物", "content_angles": ["新生儿礼物", "满月礼物推荐", "宝宝宴送礼"], "hot_topics": ["满月", "百日", "新生儿", "宝宝礼物"]},
        {"name": "毕业礼物", "pain_point": "同学朋友毕业不知道送什么", "resonance": "想要送出有纪念意义的毕业礼物", "content_angles": ["毕业礼物清单", "同学礼物推荐", "有纪念意义的好物"], "hot_topics": ["毕业", "同学礼物", "毕业季", "升学"]},
        {"name": "送礼回礼", "pain_point": "收了别人礼物不知道回什么", "resonance": "想要礼尚往来不失礼", "content_angles": ["回礼清单", "礼尚往来推荐", "不失礼的好物"], "hot_topics": ["回礼", "送礼", "礼尚往来", "还礼"]},
        {"name": "职场送礼", "pain_point": "职场送礼场合多", "resonance": "想要合适的职场礼物", "content_angles": ["职场礼物", "送领导", "送同事"], "hot_topics": ["职场送礼", "送领导", "同事礼物"]},
        {"name": "年会抽奖", "pain_point": "公司年会奖品不知道选什么", "resonance": "想要选受欢迎又实用的年会奖品", "content_angles": ["年会奖品推荐", "员工喜欢什么", "实用奖品清单"], "hot_topics": ["年会", "抽奖", "奖品", "员工福利"]},
    ],
    "购物节点": [
        {"name": "618攻略", "pain_point": "618大促不知道买什么划算", "resonance": "想要在大促时精准薅羊毛", "content_angles": ["618必买清单", "大促攻略", "怎么买最划算"], "hot_topics": ["618", "大促", "购物攻略", "省钱"]},
        {"name": "双11清单", "pain_point": "双11规则太复杂不知道怎么做功课", "resonance": "想要在双11精准买到最划算的好物", "content_angles": ["双11必买清单", "凑单技巧", "全年最低价好物"], "hot_topics": ["双11", "购物节", "凑单", "全年最低"]},
        {"name": "囤货指南", "pain_point": "不知道什么时候该囤货", "resonance": "想要在最低价时入手最划算", "content_angles": ["必囤清单推荐", "保质期多久才囤", "囤货最佳时机"], "hot_topics": ["囤货", "必囤好物", "什么时候囤", "保质期"]},
        {"name": "送礼预算", "pain_point": "不同预算不知道买什么档次", "resonance": "想要找到合适预算内最好的选择", "content_angles": ["预算礼物推荐", "不同价位好物", "性价比vs高端"], "hot_topics": ["预算", "价位", "多少钱", "档次"]},
        {"name": "品牌日优惠", "pain_point": "错过品牌日优惠", "resonance": "想要在品牌日活动买到最划算", "content_angles": ["品牌日攻略", "会员优惠", "品牌折扣"], "hot_topics": ["品牌日", "会员日", "品牌优惠"]},
    ],
    "季节时令": [
        {"name": "换季收纳", "pain_point": "换季衣服被子不知道怎么收纳", "resonance": "想要高效整理换季衣物节省空间", "content_angles": ["换季收纳技巧", "衣物整理好物", "空间收纳方案"], "hot_topics": ["换季收纳", "衣物整理", "收纳技巧", "换季整理"]},
        {"name": "梅雨季节", "pain_point": "梅雨天家里潮湿发霉问题多", "resonance": "想要解决梅雨季的各种烦恼", "content_angles": ["梅雨季必备好物", "防潮防霉技巧", "除湿神器推荐"], "hot_topics": ["梅雨季", "防潮", "除湿", "发霉"]},
        {"name": "冬季保暖", "pain_point": "冬天手脚冰凉取暖设备不知道选哪个", "resonance": "想要温暖舒适地过冬", "content_angles": ["冬季保暖好物", "取暖设备推荐", "南方过冬神器"], "hot_topics": ["冬天", "保暖", "取暖", "过冬"]},
        {"name": "夏季清凉", "pain_point": "夏天太热空调房不舒服", "resonance": "想要凉爽舒适地度过夏天", "content_angles": ["夏季清凉好物", "避暑神器", "夏日必备"], "hot_topics": ["夏天", "清凉", "避暑", "空调房"]},
        {"name": "过敏星人", "pain_point": "过敏体质不知道用什么产品", "resonance": "想要找到不过敏又实用的产品", "content_angles": ["抗过敏好物", "过敏体质推荐", "温和无刺激产品"], "hot_topics": ["过敏", "敏感肌", "温和", "无刺激"]},
        {"name": "防晒必备", "pain_point": "夏天怕晒黑", "resonance": "想要有效防晒不被晒黑", "content_angles": ["防晒好物推荐", "防晒实测", "防晒技巧"], "hot_topics": ["防晒", "防晒霜", "防晒衣", "遮阳"]},
    ],
    "生活阶段": [
        {"name": "乔迁新居", "pain_point": "搬新家不知道买什么", "resonance": "想要打造温馨舒适的新家", "content_angles": ["新家必备清单", "搬家好物推荐", "入住必备神器"], "hot_topics": ["乔迁之喜", "新家布置", "搬家清单", "入住好物"]},
        {"name": "装修搭配", "pain_point": "装修风格不知道如何搭配", "resonance": "想要整体协调又好看的装修效果", "content_angles": ["装修风格指南", "软装搭配技巧", "配色方案推荐"], "hot_topics": ["装修", "软装", "家居搭配", "北欧风", "极简风"]},
        {"name": "租房改造", "pain_point": "出租屋条件有限没法大改", "resonance": "想要低成本改造出租屋提升幸福感", "content_angles": ["租房改造好物", "低成本家居布置", "房东不让动的改造方案"], "hot_topics": ["租房改造", "出租屋", "低成本布置", "房东不允许"]},
        {"name": "独居好物", "pain_point": "一个人住总担心安全和便利性", "resonance": "想要独居生活更安全舒适", "content_angles": ["独居必备好物", "独居安全神器", "一个人住提升幸福感"], "hot_topics": ["独居", "一个人住", "独居好物", "安全"]},
        {"name": "情侣同居", "pain_point": "情侣同居不知道准备什么", "resonance": "想要同居生活更甜蜜便利", "content_angles": ["同居必备好物", "情侣家居推荐", "提升同居民幸福感"], "hot_topics": ["情侣同居", "同居好物", "情侣家居", "一起住"]},
        {"name": "备孕育儿", "pain_point": "备孕/育儿需要准备很多东西", "resonance": "想要科学准备育儿好物", "content_angles": ["备孕好物推荐", "新生儿必备清单", "育儿神器分享"], "hot_topics": ["备孕", "育儿", "新生儿", "宝妈"]},
        {"name": "坐月子好物", "pain_point": "坐月子不知道需要准备什么", "resonance": "想要舒适科学地度过月子期", "content_angles": ["坐月子必备", "产妇好物", "科学坐月子"], "hot_topics": ["坐月子", "产妇", "月子", "宝妈"]},
        {"name": "养老规划", "pain_point": "父母年纪大了需要照顾", "resonance": "想要让父母生活更舒适", "content_angles": ["养老好物推荐", "父母护理技巧", "适老化改造"], "hot_topics": ["养老", "父母", "适老化", "照护"]},
    ],
    "兴趣圈层": [
        {"name": "露营装备", "pain_point": "想尝试户外露营不知道准备什么", "resonance": "想要轻松开启露营体验", "content_angles": ["露营入门装备", "新手露营好物", "便携露营神器"], "hot_topics": ["露营", "户外", "帐篷", "野餐"]},
        {"name": "健身打卡", "pain_point": "去健身房麻烦想在家运动", "resonance": "想要在家也能高效健身", "content_angles": ["居家健身好物", "家用健身器材", "宅家运动神器"], "hot_topics": ["健身", "居家运动", "瑜伽", "器材"]},
        {"name": "咖啡爱好者", "pain_point": "想在家做咖啡但不知道买什么设备", "resonance": "想要在家也能喝到好咖啡", "content_angles": ["家用咖啡设备", "咖啡豆推荐", "咖啡爱好者必备"], "hot_topics": ["咖啡", "咖啡机", "咖啡豆", "拿铁"]},
        {"name": "精致下午茶", "pain_point": "想在家也能享受仪式感下午茶", "resonance": "想要提升生活仪式感", "content_angles": ["下午茶好物", "仪式感神器", "精致生活好物"], "hot_topics": ["下午茶", "仪式感", "精致生活", "小资"]},
        {"name": "厨房小白", "pain_point": "厨房新手不知道需要什么工具", "resonance": "想要快速上手做菜", "content_angles": ["厨房小白必备", "做菜工具推荐", "新手厨房好物"], "hot_topics": ["厨房", "做饭", "小白", "厨具"]},
        {"name": "宠物家庭", "pain_point": "养宠物后家里味道大又乱", "resonance": "想要养宠物也不影响家居环境", "content_angles": ["宠物家居好物", "除味神器", "人宠共处好物"], "hot_topics": ["宠物", "养猫", "养狗", "除味"]},
        {"name": "游戏玩家", "pain_point": "想提升游戏体验", "resonance": "想要更好的游戏装备", "content_angles": ["游戏装备推荐", "电竞好物分享", "游戏体验提升"], "hot_topics": ["游戏", "电竞", "外设", "游戏装备"]},
        {"name": "追剧神器", "pain_point": "喜欢追剧但体验不好", "resonance": "想要更好的追剧体验", "content_angles": ["追剧好物推荐", "影视装备分享", "家庭影院"], "hot_topics": ["追剧", "影视", "投影仪", "家庭影院"]},
        {"name": "阅读爱好者", "pain_point": "喜欢读书但眼睛容易累", "resonance": "想要更好的阅读体验", "content_angles": ["阅读好物推荐", "护眼灯分享", "阅读角布置"], "hot_topics": ["阅读", "书房", "护眼", "阅读角"]},
        {"name": "摄影爱好者", "pain_point": "想提升摄影水平", "resonance": "想要更好的摄影装备", "content_angles": ["摄影装备推荐", "相机测评", "摄影技巧分享"], "hot_topics": ["摄影", "相机", "镜头", "摄影技巧"]},
    ],
    "人群需求": [
        {"name": "学生党必备", "pain_point": "学生预算有限，需要高性价比", "resonance": "想要在有限预算内买最实用的", "content_angles": ["学生党必买清单", "宿舍好物推荐", "性价比最高的平替"], "hot_topics": ["学生党", "宿舍好物", "开学必备", "平价好物"]},
        {"name": "职场人装备", "pain_point": "职场需要提升效率的工具", "resonance": "想要工作更高效，生活更品质", "content_angles": ["职场必备好物", "提升效率的工具", "办公桌收纳指南"], "hot_topics": ["职场好物", "办公效率", "打工人", "桌面改造"]},
        {"name": "新婚夫妇", "pain_point": "新婚需要准备很多家居好物", "resonance": "想要打造温馨的小家", "content_angles": ["新婚家居清单", "夫妻好物推荐", "新家必备"], "hot_topics": ["新婚", "夫妻", "新家", "婚房"]},
        {"name": "宝妈群体", "pain_point": "带娃需要很多辅助工具", "resonance": "想要让育儿更轻松", "content_angles": ["宝妈必备好物", "育儿神器推荐", "带娃技巧分享"], "hot_topics": ["宝妈", "育儿", "带娃", "母婴好物"]},
        {"name": "银发族", "pain_point": "父母年纪大了需要适老化产品", "resonance": "想要让父母生活更便利", "content_angles": ["适老化好物推荐", "父母护理技巧", "老年人必备"], "hot_topics": ["老年人", "适老化", "父母", "养老"]},
    ],
    "功能痛点": [
        {"name": "解决痛点", "pain_point": "某方面有困扰，需要产品解决", "resonance": "想要找到解决问题的产品", "content_angles": ["针对痛点的产品推荐", "问题终结者产品", "用了就回不去的体验"], "hot_topics": ["痛点解决", "神器推荐", "问题解决", "刚需好物"]},
        {"name": "升级替换", "pain_point": "旧的产品不好用，想换新的", "resonance": "想要更好的产品体验", "content_angles": ["升级替换推荐", "新旧对比体验", "值得投资的品类"], "hot_topics": ["升级替换", "新旧对比", "值得买", "投资自己"]},
        {"name": "性价比之选", "pain_point": "预算有限，想买最值的产品", "resonance": "想要花最少的钱买最值的东西", "content_angles": ["同价位最值得买的一款", "平价替代方案", "什么时候买最划算"], "hot_topics": ["性价比", "平价好物", "省钱攻略", "必买清单"]},
        {"name": "真实自用分享", "pain_point": "网上种草太多，不知道哪个真正好用", "resonance": "想要真实的用户体验，不想被广告骗", "content_angles": ["真实使用一个月后的感受", "那些网上不会告诉你的细节", "和同类产品对比真实体验"], "hot_topics": ["自用分享", "真实测评", "踩坑经历", "真实推荐"]},
        {"name": "避坑指南", "pain_point": "担心买到踩坑产品", "resonance": "想要避开智商税产品", "content_angles": ["同类产品避坑指南", "选购要点总结", "常见选购误区"], "hot_topics": ["避坑指南", "智商税", "选购指南", "避雷"]},
        {"name": "深度测评", "pain_point": "想了解产品真实性能", "resonance": "想要专业详尽的产品分析", "content_angles": ["专业维度深度测评", "实验室数据对比", "真实数据说话"], "hot_topics": ["深度测评", "专业测评", "数据对比", "横评"]},
    ],
    "场景应用": [
        {"name": "居家日常", "pain_point": "居家生活想要更舒适", "resonance": "想要提升居家幸福感", "content_angles": ["居家必备神器", "提升幸福感的家居好物", "懒人必备产品"], "hot_topics": ["居家好物", "生活品质", "懒人必备", "幸福感"]},
        {"name": "出行必备", "pain_point": "出行时总忘记带这带那", "resonance": "想要出行更轻松便捷", "content_angles": ["出行必带好物", "旅行收纳技巧", "便携式产品推荐"], "hot_topics": ["出行必备", "旅行好物", "便携", "旅行收纳"]},
        {"name": "办公桌改造", "pain_point": "办公桌太乱影响工作效率", "resonance": "想要打造高效舒适的办公桌", "content_angles": ["桌面好物", "办公效率神器", "桌面收纳技巧"], "hot_topics": ["桌面改造", "办公桌", "桌面收纳", "效率"]},
        {"name": "宿舍必备", "pain_point": "大学宿舍空间小不知道买什么", "resonance": "想要在有限空间提升宿舍生活质量", "content_angles": ["宿舍好物推荐", "小空间神器", "宿舍收纳技巧"], "hot_topics": ["宿舍", "大学", "室友", "宿舍生活"]},
        {"name": "出差必备", "pain_point": "经常出差不知道带什么", "resonance": "想要轻松应对频繁出差", "content_angles": ["出差好物", "便携神器", "商务出行装备"], "hot_topics": ["出差", "商务", "便携", "出行"]},
        {"name": "车内好物", "pain_point": "开车不舒服想要提升驾乘体验", "resonance": "想要让开车坐车更舒适", "content_angles": ["车内好物推荐", "车载神器", "提升驾乘体验"], "hot_topics": ["车内", "车载", "开车", "汽车用品"]},
    ],
    "健康生活": [
        {"name": "减肥减脂", "pain_point": "想要健康减肥不知道用什么辅助", "resonance": "想要辅助健康饮食和运动的好物", "content_angles": ["减脂期好物", "低卡健康推荐", "辅助减肥神器"], "hot_topics": ["减肥", "减脂", "低卡", "健身"]},
        {"name": "熬夜急救", "pain_point": "熬夜后状态差不知道如何急救", "resonance": "想要熬夜后快速恢复状态", "content_angles": ["熬夜急救好物", "补救方案", "熬夜后修复"], "hot_topics": ["熬夜", "急救", "补救", "恢复"]},
        {"name": "健康管理", "pain_point": "关注身体健康", "resonance": "想要更好地管理健康", "content_angles": ["健康监测", "健康生活", "养生指南"], "hot_topics": ["健康", "养生", "健康管理"]},
        {"name": "睡眠改善", "pain_point": "睡眠质量不好", "resonance": "想要改善睡眠", "content_angles": ["助眠好物推荐", "改善睡眠方法", "睡眠质量提升"], "hot_topics": ["睡眠", "失眠", "助眠", "睡眠质量"]},
        {"name": "护眼必备", "pain_point": "长时间用眼疲劳", "resonance": "想要保护眼睛", "content_angles": ["护眼好物推荐", "缓解眼疲劳", "视力保护"], "hot_topics": ["护眼", "眼疲劳", "视力", "蓝光"]},
    ],
    "生活方式": [
        {"name": "品质生活", "pain_point": "追求更高生活品质", "resonance": "想要提升生活幸福感", "content_angles": ["品质生活", "生活美学", "幸福感好物"], "hot_topics": ["品质生活", "生活美学", "幸福感"]},
        {"name": "极简生活", "pain_point": "想要简化生活方式", "resonance": "追求简单高效的生活", "content_angles": ["极简主义", "简单生活", "断舍离"], "hot_topics": ["极简生活", "断舍离", "简单生活"]},
        {"name": "懒人必备", "pain_point": "想减少家务负担", "resonance": "想要更轻松的生活", "content_angles": ["懒人神器推荐", "解放双手好物", "智能家电"], "hot_topics": ["懒人", "智能", "解放双手"]},
        {"name": "仪式感生活", "pain_point": "想要生活更有仪式感", "resonance": "想要提升生活品质", "content_angles": ["仪式感好物", "精致生活", "小确幸"], "hot_topics": ["仪式感", "精致", "小确幸"]},
        {"name": "环保生活", "pain_point": "想要更环保的生活方式", "resonance": "想要减少浪费", "content_angles": ["环保好物推荐", "可持续生活", "零废弃"], "hot_topics": ["环保", "可持续", "零废弃"]},
    ],
}


def get_relevant_scenarios(sku_name, category, selling_points):
    """根据SKU特征选择最相关的场景"""
    relevant = []
    
    # 所有人群都适用的基础场景
    base_scenarios = ["真实自用分享", "性价比之选", "避坑指南", "深度测评", "节日送礼", "生日惊喜"]
    
    # 根据类目选择特定场景
    category_specific = {
        "3C数码": ["游戏玩家", "追剧神器", "职场人装备", "学生党必备", "升级替换", "摄影爱好者"],
        "美妆": ["精致下午茶", "闺蜜送礼", "520/情人节", "真实自用分享", "换季护肤", "敏感肌护理"],
        "母婴": ["备孕育儿", "坐月子好物", "送礼推荐", "囤货指南", "儿童节好物", "新生儿礼物"],
        "家居": ["乔迁新居", "装修搭配", "租房改造", "独居好物", "情侣同居", "极简生活"],
        "食品饮料": ["囤货指南", "节日送礼", "春节年货", "送礼佳品", "健康饮食", "618攻略"],
        "服装": ["换季收纳", "出行必备", "学生党必备", "约会穿搭", "年会派对", "运动休闲"],
        "个护": ["熬夜急救", "过敏星人", "品质生活", "送父母长辈", "换季护肤", "健康管理"],
        "宠物": ["宠物家庭", "露营装备", "送礼佳品", "独居好物", "品质生活"],
        "运动户外": ["健身打卡", "露营装备", "减肥减脂", "出行必备", "健康管理"],
    }
    
    # 根据卖点匹配场景
    selling_point_keywords = {
        "性价比": ["性价比之选", "学生党必备", "平价好物"],
        "送礼": ["节日送礼", "生日惊喜", "闺蜜送礼", "送父母长辈"],
        "智能": ["懒人必备", "品质生活", "职场人装备"],
        "健康": ["健康管理", "减肥减脂", "睡眠改善"],
        "便携": ["出行必备", "出差必备", "露营装备"],
        "护肤": ["换季护肤", "过敏星人", "熬夜急救"],
        "儿童": ["儿童节好物", "学生党必备", "备孕育儿"],
        "家居": ["乔迁新居", "装修搭配", "租房改造"],
    }
    
    # 选择场景
    selected_names = set(base_scenarios[:4])  # 基础场景
    
    # 添加类目相关场景
    if category in category_specific:
        for name in category_specific[category][:4]:
            selected_names.add(name)
    
    # 根据卖点添加场景
    for point in selling_points:
        for keyword, scenarios in selling_point_keywords.items():
            if keyword in point:
                for s in scenarios[:2]:
                    selected_names.add(s)
    
    # 随机添加一些通用场景以达到目标数量
    all_scenario_names = []
    for category_scenarios in SCENARIO_TEMPLATES.values():
        for s in category_scenarios:
            all_scenario_names.append(s["name"])
    
    # 补充随机场景到20个
    while len(selected_names) < 20:
        random_name = random.choice(all_scenario_names)
        selected_names.add(random_name)
    
    # 从模板中获取完整场景数据
    result = []
    for template_category in SCENARIO_TEMPLATES.values():
        for scenario in template_category:
            if scenario["name"] in selected_names:
                result.append(scenario.copy())
                selected_names.discard(scenario["name"])
                if len(result) >= 20:
                    return result
    
    return result[:20]


def main():
    print("开始扩展SKU场景数据...")
    
    # 读取现有数据
    input_path = '/Users/zhangjingwei/.qclaw/workspace/hotspot-tracker/sku_scenes.json'
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    existing_skus = data.get('skus', [])
    print(f"现有SKU数量: {len(existing_skus)}")
    
    # 为每个SKU扩展场景
    total_new_scenarios = 0
    for sku in existing_skus:
        sku_name = sku.get('sku_name', '')
        client = sku.get('client', '')
        category = client.split('-')[0] if '-' in client else ''
        selling_points = sku.get('selling_points', [])
        
        # 获取相关场景
        new_scenarios = get_relevant_scenarios(sku_name, category, selling_points)
        sku['scenarios'] = new_scenarios
        total_new_scenarios += len(new_scenarios)
    
    # 更新统计信息
    data['updated_at'] = datetime.now().isoformat()
    data['total_scenarios'] = total_new_scenarios
    
    # 保存
    with open(input_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*50}")
    print("=== 扩展完成 ===")
    print(f"{'='*50}")
    print(f"SKU总数: {len(existing_skus)}")
    print(f"场景总数: {total_new_scenarios}")
    print(f"平均每个SKU场景数: {total_new_scenarios/len(existing_skus):.1f}")
    
    # 统计各类目场景数
    category_stats = {}
    for sku in existing_skus:
        client = sku.get('client', '')
        category = client.split('-')[0] if '-' in client else '其他'
        if category not in category_stats:
            category_stats[category] = {'sku_count': 0, 'scenario_count': 0}
        category_stats[category]['sku_count'] += 1
        category_stats[category]['scenario_count'] += len(sku.get('scenarios', []))
    
    print(f"\n=== 类目分布 ===")
    for cat, stats in category_stats.items():
        print(f"  {cat}: {stats['sku_count']} 个SKU, {stats['scenario_count']} 个场景")


if __name__ == '__main__':
    main()
