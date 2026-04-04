#!/usr/bin/env python3
"""
SKU场景数据修复与扩展脚本
1. 补全10个SKU的scenarios（从6条扩展到20+条）
2. 为所有SKU添加industry和target_audience字段
3. 覆盖写入sku_scenes.json
"""

import json
from datetime import datetime

INPUT_PATH = '/Users/zhangjingwei/.qclaw/workspace/hotspot-tracker/sku_scenes.json'
OUTPUT_PATH = '/Users/zhangjingwei/.qclaw/workspace/hotspot-tracker/sku_scenes.json'

# 定义行业和目标受众映射
INDUSTRY_MAP = {
    "3C数码": "家电数码",
    "美妆": "美妆护肤",
    "母婴": "母婴用品",
    "家居": "家居家电",
    "食品饮料": "食品饮料",
    "服装": "服装配饰",
    "个护": "个护美妆",
    "宠物": "宠物用品",
    "运动户外": "运动户外",
    "玩具": "儿童玩具",
}

TARGET_AUDIENCE_MAP = {
    "3C数码": ["年轻消费者", "数码爱好者", "职场人士", "学生群体", "商务人群"],
    "美妆": ["年轻女性", "职场女性", "精致妈妈", "护肤新手", "成分党"],
    "母婴": ["新手妈妈", "备孕女性", "0-3岁宝宝家长", "3-6岁儿童家长", "孕妈"],
    "家居": ["新婚夫妇", "家庭主妇", "租房群体", "品质生活追求者", "懒人群体"],
    "食品饮料": ["年轻白领", "健康饮食者", "养生人群", "家庭主妇", "学生群体"],
    "服装": ["年轻女性", "职场人士", "学生群体", "运动爱好者", "潮流达人"],
    "个护": ["精致女性", "注重健康人群", "职场人士", "敏感肌人群", "全家适用"],
    "宠物": ["养宠人群", "猫奴", "狗主人", "新手铲屎官", "爱宠人士"],
    "运动户外": ["运动爱好者", "健身人群", "户外探险者", "跑步爱好者", "白领上班族"],
    "玩具": ["3-6岁儿童家长", "6-12岁儿童家长", "送礼人群", "益智教育追求者", "亲子家庭"],
}

def get_category(client):
    if not client:
        return None
    if '-' in client:
        return client.split('-')[0]
    return client

def get_industry(client):
    cat = get_category(client)
    return INDUSTRY_MAP.get(cat, cat or "综合")

def get_target_audience(client):
    cat = get_category(client)
    return TARGET_AUDIENCE_MAP.get(cat, ["大众消费者"])

# 通用场景模板（用于补全）
COMMON_SCENARIOS = [
    {"name": "送礼佳品", "pain_point": "节日/生日不知道送什么", "resonance": "想要送出有新意又实用的礼物", "content_angles": ["礼物创意推荐", "投其所好的礼物选择", "仪式感礼物推荐"], "hot_topics": ["礼物推荐", "送礼", "仪式感", "创意礼物"]},
    {"name": "性价比之选", "pain_point": "预算有限，想买最值的产品", "resonance": "想要花最少的钱买最值的东西", "content_angles": ["同价位最值得买的一款", "平价替代方案", "什么时候买最划算"], "hot_topics": ["性价比", "平价好物", "省钱攻略", "必买清单"]},
    {"name": "真实自用分享", "pain_point": "网上种草太多，不知道哪个真正好用", "resonance": "想要真实的用户体验，不想被广告骗", "content_angles": ["真实使用一个月后的感受", "那些网上不会告诉你的细节", "和同类产品对比真实体验"], "hot_topics": ["自用分享", "真实测评", "踩坑经历", "真实推荐"]},
    {"name": "避坑指南", "pain_point": "担心买到踩坑产品", "resonance": "想要避开智商税产品", "content_angles": ["同类产品避坑指南", "选购要点总结", "常见选购误区"], "hot_topics": ["避坑指南", "智商税", "选购指南", "避雷"]},
    {"name": "深度测评", "pain_point": "想了解产品真实性能", "resonance": "想要专业详尽的产品分析", "content_angles": ["专业维度深度测评", "实验室数据对比", "真实数据说话"], "hot_topics": ["深度测评", "专业测评", "数据对比", "横评"]},
    {"name": "新年礼物", "pain_point": "新年不知道送什么礼物", "resonance": "想要送出有新年祝福意义的礼物", "content_angles": ["新年礼物推荐", "过年送礼清单", "新年好物"], "hot_topics": ["新年", "过年", "新年礼物", "跨年"]},
    {"name": "情人节限定", "pain_point": "情人节想送特别的限量款", "resonance": "想要独一无二的节日礼物", "content_angles": ["情人节限定推荐", "节日特别款", "浪漫礼盒"], "hot_topics": ["情人节", "限定", "520", "七夕"]},
    {"name": "七夕特别", "pain_point": "七夕想送有中国特色的礼物", "resonance": "想要有传统文化底蕴的礼物", "content_angles": ["七夕礼物推荐", "中国式浪漫", "传统节日好物"], "hot_topics": ["七夕", "中国情人节", "传统文化", "牛郎织女"]},
    {"name": "圣诞节礼物", "pain_point": "圣诞节不知道送什么", "resonance": "想要有节日氛围的礼物", "content_angles": ["圣诞礼物推荐", "圣诞限定好物", "节日氛围布置"], "hot_topics": ["圣诞节", "圣诞礼物", "平安夜", "跨年"]},
    {"name": "女神节专属", "pain_point": "三八节不知道送什么", "resonance": "想要送女性专属好物", "content_angles": ["女神节礼物", "女性专属推荐", "女王节好物"], "hot_topics": ["女神节", "三八节", "女王节", "女性礼物"]},
    {"name": "教师节礼物", "pain_point": "教师节不知道送老师什么", "resonance": "想要表达感谢又不失礼貌", "content_angles": ["教师节礼物推荐", "送老师什么好", "尊师重道好物"], "hot_topics": ["教师节", "送老师", "感恩老师", "老师礼物"]},
    {"name": "中秋送礼", "pain_point": "中秋节送礼选择困难", "resonance": "想要有中秋元素的礼物", "content_angles": ["中秋礼盒推荐", "月饼搭配好物", "团圆节送礼"], "hot_topics": ["中秋节", "月饼", "团圆", "中秋礼盒"]},
    {"name": "端午礼品", "pain_point": "端午节不知道送什么", "resonance": "想要有节日特色的好物", "content_angles": ["端午礼品推荐", "粽子礼盒搭配", "端午好物"], "hot_topics": ["端午节", "粽子", "龙舟", "端午礼品"]},
    {"name": "开箱展示", "pain_point": "想看真实的产品外观和细节", "resonance": "想要直观了解产品颜值和质感", "content_angles": ["开箱实拍展示", "产品细节特写", "颜值质感评测"], "hot_topics": ["开箱", "实拍", "颜值", "质感"]},
]

# 每个SKU的专属场景补充
SKU_EXTRAS = {
    "iPhone 15 Pro Max": [
        {"name": "送父母长辈", "pain_point": "给父母买东西总是被说不实用", "resonance": "想要送父母真正需要又让他们开心的礼物", "content_angles": ["送父母清单", "长辈真实需求", "不踩雷的孝心礼物"], "hot_topics": ["送父母", "长辈礼物", "孝心", "送爸妈"]},
        {"name": "苹果全家桶", "pain_point": "已经买了iPhone想凑齐苹果生态", "resonance": "想要完善的苹果设备生态", "content_angles": ["苹果生态联动", "全家桶升级指南", "设备协同体验"], "hot_topics": ["苹果全家桶", "苹果生态", "设备联动", "苹果用户"]},
        {"name": "女生礼物", "pain_point": "不知道送女生什么手机好", "resonance": "想要送女生有档次又实用的礼物", "content_angles": ["送女生手机推荐", "高颜值手机", "女性用户首选"], "hot_topics": ["送女生", "女生手机", "礼物推荐", "高颜值"]},
        {"name": "摄影爱好者", "pain_point": "喜欢拍照但不想带相机", "resonance": "想要拍照最好的手机", "content_angles": ["手机摄影教程", "拍照手机对比", "计算摄影实测"], "hot_topics": ["手机摄影", "拍照手机", "摄影技巧", "iPhone拍照"]},
        {"name": "商务精英", "pain_point": "商务场合需要得体手机", "resonance": "想要高端大气的商务手机", "content_angles": ["商务手机推荐", "高端旗舰对比", "商务人士首选"], "hot_topics": ["商务手机", "高端旗舰", "商务送礼", "职场装备"]},
        {"name": "保值率", "pain_point": "担心手机掉价快不保值", "resonance": "想要保值率高的手机", "content_angles": ["手机保值率对比", "二手价格实测", "苹果手机残值分析"], "hot_topics": ["保值率", "二手价格", "手机残值", "苹果回收"]},
    ],
    "戴森V15吸尘器": [
        {"name": "新房开荒", "pain_point": "新房装修完需要彻底清洁", "resonance": "想要专业级的深度清洁", "content_angles": ["新房开荒指南", "深度清洁必备", "装修后清洁技巧"], "hot_topics": ["新房开荒", "深度清洁", "装修后清洁", "入住准备"]},
        {"name": "过敏体质", "pain_point": "过敏体质对灰尘特别敏感", "resonance": "想要彻底清除过敏原", "content_angles": ["除过敏原神器", "过敏体质清洁攻略", "家居除螨技巧"], "hot_topics": ["除过敏原", "过敏体质", "除螨", "家居清洁"]},
        {"name": "养宠必备", "pain_point": "养宠物后家里到处都是毛", "resonance": "想要彻底清理宠物毛发的工具", "content_angles": ["宠物毛清理攻略", "除毛神器推荐", "养宠家庭清洁"], "hot_topics": ["宠物毛", "养宠必备", "除毛神器", "清洁工具"]},
        {"name": "有娃家庭", "pain_point": "小孩子在地上爬担心卫生", "resonance": "想要宝宝安全健康的家居环境", "content_angles": ["宝宝安全环境", "有娃家庭清洁攻略", "婴儿房清洁技巧"], "hot_topics": ["有娃家庭", "宝宝安全", "婴儿房清洁", "儿童健康"]},
        {"name": "大户型清洁", "pain_point": "房子大清洁起来很累", "resonance": "想要省力的高效清洁工具", "content_angles": ["大户型清洁方案", "高效清洁工具", "清洁省力技巧"], "hot_topics": ["大户型", "清洁效率", "省力工具", "家居清洁"]},
        {"name": "高端送礼", "pain_point": "想送有档次的生活好物", "resonance": "想要送高端大气的礼物", "content_angles": ["高端礼品推荐", "戴森送礼清单", "品质礼物分享"], "hot_topics": ["高端礼品", "戴森送礼", "品质礼物", "生活好物"]},
    ],
    "SK-II神仙水": [
        {"name": "护肤进阶", "pain_point": "用了基础护肤品想升级", "resonance": "想要进阶到高端护肤", "content_angles": ["护肤进阶指南", "神仙水使用攻略", "高端护肤体验"], "hot_topics": ["护肤进阶", "神仙水", "高端护肤", "护肤升级"]},
        {"name": "贵妇护肤品", "pain_point": "想买贵妇护肤品但怕踩雷", "resonance": "想要了解神仙水是否值得投资", "content_angles": ["贵妇护肤品测评", "神仙水真实效果", "护肤投资回报"], "hot_topics": ["贵妇护肤", "神仙水值不值", "高端护肤", "护肤品投资"]},
        {"name": "送妈妈礼物", "pain_point": "母亲节/生日不知道送什么", "resonance": "想要送妈妈高端实用的礼物", "content_angles": ["母亲节礼物推荐", "送妈妈护肤品清单", "孝心礼物分享"], "hot_topics": ["母亲节礼物", "送妈妈", "孝心礼物", "护肤品送礼"]},
        {"name": "油皮改善", "pain_point": "皮肤出油多毛孔粗大", "resonance": "想要改善油皮问题", "content_angles": ["油皮改善攻略", "神仙水控油实测", "收敛毛孔技巧"], "hot_topics": ["油皮护肤", "控油", "毛孔粗大", "神仙水控油"]},
        {"name": "皮肤暗沉", "pain_point": "皮肤暗沉发黄没气色", "resonance": "想要提亮肤色", "content_angles": ["提亮肤色攻略", "神仙水美白实测", "改善暗沉技巧"], "hot_topics": ["提亮肤色", "美白", "改善暗沉", "神仙水效果"]},
        {"name": "成分党研究", "pain_point": "想了解PITERA成分的作用", "resonance": "想要了解神仙水的核心成分", "content_angles": ["PITERA深度解析", "神仙水成分分析", "护肤成分原理"], "hot_topics": ["PITERA", "成分党", "神仙水成分", "护肤成分"]},
    ],
    "爱他美奶粉": [
        {"name": "转奶攻略", "pain_point": "想换奶粉但不知道怎么转", "resonance": "想要科学转奶不踩坑", "content_angles": ["科学转奶方法", "爱他美转奶攻略", "转奶注意事项"], "hot_topics": ["转奶", "爱他美转奶", "换奶粉", "转奶技巧"]},
        {"name": "配方对比", "pain_point": "不同段位配方不知道区别", "resonance": "想要了解各段位营养差异", "content_angles": ["各段位配方对比", "不同月龄配方选择", "营养成分解析"], "hot_topics": ["配方对比", "奶粉段位", "营养成分", "爱他美配方"]},
        {"name": "货源渠道", "pain_point": "担心买到假奶粉", "resonance": "想要找到可靠的购买渠道", "content_angles": ["正规购买渠道", "爱他美真伪鉴别", "官方购买攻略"], "hot_topics": ["爱他美货源", "真伪鉴别", "购买渠道", "奶粉安全"]},
        {"name": "冲调技巧", "pain_point": "奶粉冲调总是有结块", "resonance": "想要掌握正确的冲调方法", "content_angles": ["正确冲调方法", "冲调技巧分享", "冲泡温度和时间"], "hot_topics": ["冲调技巧", "奶粉冲泡", "冲奶方法", "宝宝喂养"]},
        {"name": "宝宝便秘", "pain_point": "喝奶粉后宝宝便秘", "resonance": "想要了解奶粉与便秘的关系", "content_angles": ["奶粉便秘解决", "爱他美便秘反馈", "便秘调理方法"], "hot_topics": ["宝宝便秘", "奶粉便秘", "爱他美便秘", "育儿问题"]},
        {"name": "DHA含量", "pain_point": "想了解奶粉DHA含量", "resonance": "想要选DHA含量高的奶粉", "content_angles": ["DHA含量对比", "爱他美DHA分析", "智力发育营养"], "hot_topics": ["DHA", "爱他美DHA", "奶粉营养", "智力发育"]},
    ],
    "乐高积木": [
        {"name": "送礼佳品", "pain_point": "亲戚家孩子生日不知道送什么", "resonance": "想要送孩子寓教于乐的礼物", "content_angles": ["儿童玩具推荐", "乐高送礼清单", "寓教于乐礼物"], "hot_topics": ["儿童玩具推荐", "乐高送礼", "生日礼物", "寓教于乐"]},
        {"name": "大人也玩", "pain_point": "大人想玩积木但不知道选哪款", "resonance": "想要成人也能玩的积木", "content_angles": ["成人乐高推荐", "乐高收藏价值", "大人玩积木分享"], "hot_topics": ["成人乐高", "乐高收藏", "大人积木", "乐高玩家"]},
        {"name": "机械组入门", "pain_point": "对机械组感兴趣但不知道怎么入门", "resonance": "想要了解机械组积木", "content_angles": ["机械组入门指南", "乐高机械组测评", "齿轮和电机原理"], "hot_topics": ["乐高机械组", "积木入门", "机械积木", "齿轮原理"]},
        {"name": "亲子时光", "pain_point": "想陪孩子一起做点什么", "resonance": "想要通过积木增进亲子关系", "content_angles": ["亲子积木时光", "亲子手工攻略", "陪伴孩子成长"], "hot_topics": ["亲子时光", "亲子活动", "乐高亲子", "陪伴孩子"]},
        {"name": "女孩也能玩", "pain_point": "觉得乐高是男孩子的专利", "resonance": "想要给女孩推荐乐高", "content_angles": ["女孩乐高推荐", "乐高ideas女孩版", "女性玩家分享"], "hot_topics": ["女孩乐高", "乐高ideas", "女性玩家", "乐高女孩"]},
        {"name": "收纳整理", "pain_point": "积木太多不知道怎么收纳", "resonance": "想要整理积木的好方法", "content_angles": ["积木收纳技巧", "乐高整理方案", "零件管理方法"], "hot_topics": ["积木收纳", "乐高整理", "收纳技巧", "零件管理"]},
    ],
    "农夫山泉婴儿水": [
        {"name": "泡奶粉", "pain_point": "不知道用什么水泡奶粉好", "resonance": "想要了解适合泡奶的水", "content_angles": ["婴儿泡奶用水", "婴儿水测评", "冲奶粉最佳用水"], "hot_topics": ["泡奶粉", "婴儿水推荐", "冲奶粉用水", "婴儿喂养"]},
        {"name": "宝宝不爱喝水", "pain_point": "宝宝不爱喝白开水", "resonance": "想要找到宝宝愿意喝的水", "content_angles": ["宝宝爱上喝水", "婴儿水口感", "培养喝水习惯"], "hot_topics": ["宝宝喝水", "婴儿水口感", "喝水习惯", "不爱喝水"]},
        {"name": "水质安全", "pain_point": "担心自来水水质不安全", "resonance": "想要给宝宝用安全的水", "content_angles": ["婴儿水质安全", "自来水vs婴儿水", "水质检测对比"], "hot_topics": ["水质安全", "婴儿水安全", "水质检测", "宝宝用水"]},
        {"name": "性价比对比", "pain_point": "婴儿水价格贵普通水能替代吗", "resonance": "想要了解婴儿水vs普通水区别", "content_angles": ["婴儿水vs普通水", "性价比对比分析", "是否有必要买婴儿水"], "hot_topics": ["婴儿水性价比", "普通水替代", "婴儿水值不值", "冲奶用水对比"]},
        {"name": "出游携带", "pain_point": "带宝宝出行需要带水", "resonance": "想要便携的婴儿水", "content_angles": ["宝宝出行水推荐", "便携婴儿水", "外出带水攻略"], "hot_topics": ["宝宝出行", "便携婴儿水", "外出好物", "宝宝喝水"]},
        {"name": "辅食用水", "pain_point": "做辅食不知道用什么水", "resonance": "想要了解适合辅食的水", "content_angles": ["辅食用水指南", "婴儿水做辅食", "宝宝辅食攻略"], "hot_topics": ["辅食用水", "婴儿水辅食", "辅食攻略", "宝宝辅食"]},
    ],
    "优衣库联名T恤": [
        {"name": "联名收藏", "pain_point": "联名款太多不知道怎么选", "resonance": "想要收藏有价值的联名款", "content_angles": ["联名款收藏指南", "优衣库联名盘点", "值得收藏的联名"], "hot_topics": ["联名收藏", "优衣库联名", "联名T恤", "收藏价值"]},
        {"name": "夏日穿搭", "pain_point": "夏天不知道怎么穿得好看", "resonance": "想要简单好看的夏日穿搭", "content_angles": ["夏日穿搭分享", "T恤搭配技巧", "清凉夏日装扮"], "hot_topics": ["夏日穿搭", "T恤搭配", "夏天搭配", "清凉穿搭"]},
        {"name": "平价好物", "pain_point": "想要平价又好看的衣服", "resonance": "想要高性价比的时尚单品", "content_angles": ["平价穿搭分享", "优衣库性价比", "高颜值平价衣"], "hot_topics": ["平价好物", "优衣库性价比", "高性价比", "平价时尚"]},
        {"name": "情侣装", "pain_point": "想和对象穿情侣装", "resonance": "想要简约好看的情侣穿搭", "content_angles": ["情侣穿搭分享", "简约情侣装", "优衣库情侣装"], "hot_topics": ["情侣穿搭", "优衣库情侣装", "简约情侣", "约会穿搭"]},
        {"name": "职场穿搭", "pain_point": "职场不知道怎么穿得体", "resonance": "想要简单得体的职场穿搭", "content_angles": ["职场穿搭指南", "优衣库职场风", "干练日常穿搭"], "hot_topics": ["职场穿搭", "上班穿搭", "优衣库职场", "干练穿搭"]},
        {"name": "基础款推荐", "pain_point": "衣橱里总是缺一件基础款", "resonance": "想要必备的基础款T恤", "content_angles": ["基础款T恤推荐", "衣橱必备清单", "优衣库基础款"], "hot_topics": ["基础款", "T恤必备", "衣橱必备", "优衣库基础款"]},
    ],
    "舒肤佳沐浴露": [
        {"name": "全家适用", "pain_point": "想买全家都能用的沐浴露", "resonance": "想要温和不刺激的沐浴露", "content_angles": ["全家沐浴露推荐", "温和清洁分享", "适合敏感肌的沐浴露"], "hot_topics": ["全家沐浴露", "温和清洁", "敏感肌沐浴露", "家庭好物"]},
        {"name": "宝宝洗澡", "pain_point": "给宝宝洗澡不知道用什么", "resonance": "想要温和安全的宝宝沐浴露", "content_angles": ["宝宝沐浴露推荐", "婴儿洗澡好物", "温和配方分享"], "hot_topics": ["宝宝沐浴露", "婴儿洗澡", "宝宝用品", "温和配方"]},
        {"name": "抑菌需求", "pain_point": "担心细菌滋生", "resonance": "想要有抑菌效果的沐浴露", "content_angles": ["抑菌沐浴露测评", "舒肤佳抑菌效果", "清洁抑菌分享"], "hot_topics": ["抑菌沐浴露", "舒肤佳抑菌", "清洁抑菌", "抑菌效果"]},
        {"name": "敏感肌友好", "pain_point": "敏感肌不知道用什么沐浴露", "resonance": "想要温和不刺激的沐浴露", "content_angles": ["敏感肌沐浴露推荐", "温和配方测评", "不踩雷选购"], "hot_topics": ["敏感肌沐浴露", "温和配方", "敏感肌友好", "不踩雷"]},
        {"name": "香味持久", "pain_point": "想要洗澡后身上有香味", "resonance": "想要香味持久的沐浴露", "content_angles": ["香味持久沐浴露", "沐浴露香味测评", "留香效果分享"], "hot_topics": ["香味持久", "沐浴露香味", "留香效果", "好闻沐浴露"]},
        {"name": "性价比之选", "pain_point": "想要性价比高的沐浴露", "resonance": "想要便宜好用的沐浴露", "content_angles": ["平价沐浴露推荐", "大瓶装更划算", "性价比之王"], "hot_topics": ["平价沐浴露", "大瓶装", "性价比", "省钱好物"]},
    ],
    "皇家猫粮": [
        {"name": "猫咪挑食", "pain_point": "猫咪挑食不吃猫粮", "resonance": "想要找到猫咪爱吃的猫粮", "content_angles": ["挑食猫咪猫粮推荐", "皇家适口性测评", "猫咪爱吃分享"], "hot_topics": ["挑食猫咪", "猫粮适口性", "猫咪爱吃", "皇家猫粮"]},
        {"name": "猫咪健康", "pain_point": "担心猫粮营养不够", "resonance": "想要营养均衡的猫粮", "content_angles": ["猫粮营养分析", "皇家配方解析", "猫咪健康饮食"], "hot_topics": ["猫粮营养", "皇家配方", "猫咪健康", "营养均衡"]},
        {"name": "换粮攻略", "pain_point": "想给猫咪换粮但怕肠胃不适", "resonance": "想要科学换粮的方法", "content_angles": ["科学换粮方法", "皇家换粮攻略", "猫咪换粮技巧"], "hot_topics": ["换粮攻略", "猫咪换粮", "科学换粮", "皇家换粮"]},
        {"name": "幼猫猫粮", "pain_point": "幼猫不知道吃什么猫粮", "resonance": "想要适合幼猫的猫粮", "content_angles": ["幼猫猫粮推荐", "皇家幼猫粮测评", "小猫喂养指南"], "hot_topics": ["幼猫猫粮", "皇家幼猫粮", "小猫喂养", "幼猫推荐"]},
        {"name": "成猫猫粮", "pain_point": "成猫不知道吃什么猫粮", "resonance": "想要适合成猫的猫粮", "content_angles": ["成猫猫粮推荐", "皇家成猫粮测评", "成年猫喂养指南"], "hot_topics": ["成猫猫粮", "皇家成猫粮", "成年猫喂养", "成猫推荐"]},
        {"name": "进口猫粮", "pain_point": "想买进口猫粮但选择多", "resonance": "想要了解进口猫粮品牌", "content_angles": ["进口猫粮对比", "皇家vs其他品牌", "猫粮选购指南"], "hot_topics": ["进口猫粮", "皇家对比", "猫粮选购", "品牌对比"]},
    ],
    "Nike运动鞋": [
        {"name": "跑步入门", "pain_point": "刚开始跑步不知道买什么鞋", "resonance": "想要适合新手的跑鞋", "content_angles": ["新手跑鞋推荐", "Nike跑鞋测评", "跑步入门装备"], "hot_topics": ["新手跑鞋", "Nike跑鞋", "跑步入门", "跑鞋推荐"]},
        {"name": "健身训练", "pain_point": "健身不知道穿什么鞋", "resonance": "想要适合健身的运动鞋", "content_angles": ["健身鞋推荐", "训练鞋测评", "健身房装备"], "hot_topics": ["健身鞋", "训练鞋", "健身房装备", "健身推荐"]},
        {"name": "日常穿搭", "pain_point": "想买百搭的运动鞋", "resonance": "想要日常也能穿的运动鞋", "content_angles": ["百搭运动鞋推荐", "Nike穿搭分享", "日常运动风"], "hot_topics": ["百搭运动鞋", "Nike穿搭", "日常运动风", "运动穿搭"]},
        {"name": "学生党推荐", "pain_point": "学生预算有限想买运动鞋", "resonance": "想要性价比高的运动鞋", "content_angles": ["学生党运动鞋推荐", "平价Nike推荐", "学生穿搭分享"], "hot_topics": ["学生党运动鞋", "平价Nike", "学生穿搭", "性价比运动鞋"]},
        {"name": "情侣鞋", "pain_point": "想和对象穿情侣运动鞋", "resonance": "想要好看的情侣运动鞋", "content_angles": ["情侣运动鞋推荐", "Nike情侣款", "情侣穿搭分享"], "hot_topics": ["情侣运动鞋", "Nike情侣款", "情侣穿搭", "情侣鞋"]},
        {"name": "专业跑步", "pain_point": "想认真跑步需要专业跑鞋", "resonance": "想要专业级的跑鞋", "content_angles": ["专业跑鞋推荐", "Nike专业款测评", "马拉松装备"], "hot_topics": ["专业跑鞋", "Nike专业款", "马拉松装备", "跑步装备"]},
    ],
}

def main():
    # 读取现有数据
    with open(INPUT_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    skus = data.get('skus', [])
    total_scenarios = 0
    
    for sku in skus:
        sku_name = sku.get('sku_name', '')
        client = sku.get('client', '')
        
        # 添加industry和target_audience字段
        sku['industry'] = get_industry(client)
        sku['target_audience'] = get_target_audience(client)
        
        # 检查scenarios数量，如果少于20则补充
        current_scenarios = sku.get('scenarios', [])
        current_count = len(current_scenarios)
        
        if current_count < 20:
            # 先添加SKU专属场景
            extras = SKU_EXTRAS.get(sku_name, [])
            # 去重：只添加不存在的场景
            existing_names = {s['name'] for s in current_scenarios}
            for extra in extras:
                if extra['name'] not in existing_names:
                    current_scenarios.append(extra)
                    existing_names.add(extra['name'])
            
            # 如果还不够20个，用通用场景补充
            if len(current_scenarios) < 20:
                for common in COMMON_SCENARIOS:
                    if common['name'] not in existing_names:
                        current_scenarios.append(common)
                        existing_names.add(common['name'])
                    if len(current_scenarios) >= 20:
                        break
        
        sku['scenarios'] = current_scenarios
        total_scenarios += len(current_scenarios)
    
    # 更新统计信息
    data['skus'] = skus
    data['total_skus'] = len(skus)
    data['total_scenarios'] = total_scenarios
    data['updated_at'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
    
    # 确保categories_covered包含所有品类
    categories = set()
    for sku in skus:
        cat = get_category(sku.get('client', ''))
        if cat:
            categories.add(cat)
    data['categories_covered'] = sorted(list(categories))
    
    # 写入文件
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 完成！")
    print(f"   - 总SKU数: {data['total_skus']}")
    print(f"   - 总场景数: {data['total_scenarios']}")
    print(f"   - 品类覆盖: {data['categories_covered']}")
    
    # 验证每个SKU的场景数
    min_scenes = min(len(sku['scenarios']) for sku in skus)
    max_scenes = max(len(sku['scenarios']) for sku in skus)
    avg_scenes = sum(len(sku['scenarios']) for sku in skus) / len(skus)
    print(f"   - 场景数/SKU: min={min_scenes}, max={max_scenes}, avg={avg_scenes:.1f}")
    
    # 验证字段完整性
    has_industry = sum(1 for s in skus if 'industry' in s)
    has_audience = sum(1 for s in skus if 'target_audience' in s)
    print(f"   - industry字段: {has_industry}/{len(skus)}")
    print(f"   - target_audience字段: {has_audience}/{len(skus)}")

if __name__ == '__main__':
    main()
