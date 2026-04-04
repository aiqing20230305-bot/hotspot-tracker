#!/usr/bin/env python3
"""
扩展SKU场景库脚本
为每个SKU添加更多有价值的场景，目标每个SKU至少30个场景
"""

import json
from datetime import datetime

# 新增场景模板 - 按场景类型分类
NEW_SCENARIOS = [
    # ========== 节日送礼类 ==========
    {
        "name": "新年礼物",
        "pain_point": "新年不知道送什么礼物",
        "resonance": "想要送出有新年祝福意义的礼物",
        "content_angles": ["新年礼物推荐", "过年送礼清单", "新年好物"],
        "hot_topics": ["新年", "过年", "新年礼物", "跨年"]
    },
    {
        "name": "情人节限定",
        "pain_point": "情人节想送特别的限量款",
        "resonance": "想要独一无二的节日礼物",
        "content_angles": ["情人节限定推荐", "节日特别款", "浪漫礼盒"],
        "hot_topics": ["情人节", "限定", "520", "七夕"]
    },
    {
        "name": "七夕特别",
        "pain_point": "七夕想送有中国特色的礼物",
        "resonance": "想要有传统文化底蕴的礼物",
        "content_angles": ["七夕礼物推荐", "中国式浪漫", "传统节日好物"],
        "hot_topics": ["七夕", "中国情人节", "传统文化", "牛郎织女"]
    },
    {
        "name": "圣诞节礼物",
        "pain_point": "圣诞节不知道送什么",
        "resonance": "想要有节日氛围的礼物",
        "content_angles": ["圣诞礼物推荐", "圣诞限定好物", "节日氛围布置"],
        "hot_topics": ["圣诞节", "圣诞礼物", "平安夜", "跨年"]
    },
    {
        "name": "女神节专属",
        "pain_point": "三八节不知道送什么",
        "resonance": "想要送女性专属好物",
        "content_angles": ["女神节礼物", "女性专属推荐", "女王节好物"],
        "hot_topics": ["女神节", "三八节", "女王节", "女性礼物"]
    },
    {
        "name": "教师节礼物",
        "pain_point": "教师节不知道送老师什么",
        "resonance": "想要表达感谢又不失礼貌",
        "content_angles": ["教师节礼物推荐", "送老师什么好", "尊师重道好物"],
        "hot_topics": ["教师节", "送老师", "感恩老师", "老师礼物"]
    },
    {
        "name": "中秋送礼",
        "pain_point": "中秋节送礼选择困难",
        "resonance": "想要有中秋元素的礼物",
        "content_angles": ["中秋礼盒推荐", "月饼搭配好物", "团圆节送礼"],
        "hot_topics": ["中秋节", "月饼", "团圆", "中秋礼盒"]
    },
    {
        "name": "端午礼品",
        "pain_point": "端午节不知道送什么",
        "resonance": "想要有节日特色的好物",
        "content_angles": ["端午礼品推荐", "粽子礼盒搭配", "端午好物"],
        "hot_topics": ["端午节", "粽子", "龙舟", "端午礼品"]
    },

    # ========== 人生大事类 ==========
    {
        "name": "求婚钻戒配套",
        "pain_point": "求婚准备不足",
        "resonance": "想要完美的求婚场景",
        "content_angles": ["求婚好物推荐", "求婚准备清单", "浪漫求婚方案"],
        "hot_topics": ["求婚", "钻戒", "求婚准备", "浪漫"]
    },
    {
        "name": "订婚好物",
        "pain_point": "订婚不知道准备什么",
        "resonance": "想要完美订婚仪式",
        "content_angles": ["订婚必备好物", "订婚准备清单", "订婚礼物推荐"],
        "hot_topics": ["订婚", "订婚礼物", "订婚准备", "婚嫁"]
    },
    {
        "name": "新婚回门",
        "pain_point": "回门不知道带什么",
        "resonance": "想要体面又实用的回门礼",
        "content_angles": ["回门礼推荐", "婚后礼仪", "回门好物"],
        "hot_topics": ["回门", "新婚", "回门礼", "婚后"]
    },
    {
        "name": "入职礼物",
        "pain_point": "新入职不知道准备什么",
        "resonance": "想要职场开个好头",
        "content_angles": ["入职必备好物", "职场新人装备", "入职礼物推荐"],
        "hot_topics": ["入职", "职场新人", "工作准备", "新工作"]
    },
    {
        "name": "升职加薪",
        "pain_point": "升职后想奖励自己",
        "resonance": "想要犒劳自己",
        "content_angles": ["升职礼物推荐", "奖励自己好物", "成功人士装备"],
        "hot_topics": ["升职", "加薪", "奖励自己", "职场进阶"]
    },
    {
        "name": "退休礼物",
        "pain_point": "退休不知道送什么",
        "resonance": "想要表达敬意和祝福",
        "content_angles": ["退休礼物推荐", "退休生活好物", "退休准备清单"],
        "hot_topics": ["退休", "退休礼物", "退休生活", "退休准备"]
    },
    {
        "name": "纪念日惊喜",
        "pain_point": "纪念日不知道怎么庆祝",
        "resonance": "想要有仪式感的纪念",
        "content_angles": ["纪念日礼物推荐", "仪式感庆祝", "纪念日好物"],
        "hot_topics": ["纪念日", "结婚纪念", "恋爱纪念", "仪式感"]
    },
    {
        "name": "成人礼",
        "pain_point": "18岁成人礼不知道送什么",
        "resonance": "想要有纪念意义的成人礼",
        "content_angles": ["成人礼礼物推荐", "18岁礼物", "成人礼好物"],
        "hot_topics": ["成人礼", "18岁", "成年", "成人礼礼物"]
    },

    # ========== 生活场景类 ==========
    {
        "name": "早餐神器",
        "pain_point": "早上没时间做早餐",
        "resonance": "想要快速解决早餐问题",
        "content_angles": ["早餐神器推荐", "快速早餐方案", "懒人早餐好物"],
        "hot_topics": ["早餐", "早餐神器", "快手早餐", "健康早餐"]
    },
    {
        "name": "夜宵必备",
        "pain_point": "晚上饿了想吃宵夜",
        "resonance": "想要方便又美味的宵夜",
        "content_angles": ["夜宵好物推荐", "深夜食堂", "宵夜神器"],
        "hot_topics": ["夜宵", "宵夜", "深夜", "美食"]
    },
    {
        "name": "居家办公",
        "pain_point": "居家办公效率低",
        "resonance": "想要提升居家办公体验",
        "content_angles": ["居家办公好物", "WFH装备推荐", "在家办公神器"],
        "hot_topics": ["居家办公", "WFH", "在家办公", "远程办公"]
    },
    {
        "name": "阳台改造",
        "pain_point": "阳台闲置浪费空间",
        "resonance": "想要打造实用又美观的阳台",
        "content_angles": ["阳台改造好物", "阳台设计方案", "阳台利用技巧"],
        "hot_topics": ["阳台", "阳台改造", "阳台设计", "阳台好物"]
    },
    {
        "name": "浴室收纳",
        "pain_point": "浴室东西多又乱",
        "resonance": "想要整洁有序的浴室",
        "content_angles": ["浴室收纳好物", "卫生间整理技巧", "浴室神器推荐"],
        "hot_topics": ["浴室", "卫生间", "收纳", "浴室好物"]
    },
    {
        "name": "玄关设计",
        "pain_point": "玄关乱糟糟",
        "resonance": "想要进门就有好心情",
        "content_angles": ["玄关好物推荐", "玄关收纳技巧", "玄关设计灵感"],
        "hot_topics": ["玄关", "玄关设计", "玄关收纳", "入门好物"]
    },
    {
        "name": "衣帽间打造",
        "pain_point": "衣服多没地方放",
        "resonance": "想要整齐的衣帽间",
        "content_angles": ["衣帽间好物推荐", "衣柜收纳技巧", "衣帽间设计方案"],
        "hot_topics": ["衣帽间", "衣柜收纳", "衣服收纳", "衣帽间设计"]
    },
    {
        "name": "书房布置",
        "pain_point": "书房不知道怎么布置",
        "resonance": "想要舒适的书房环境",
        "content_angles": ["书房好物推荐", "书房布置方案", "阅读空间打造"],
        "hot_topics": ["书房", "书房布置", "阅读角", "书房好物"]
    },

    # ========== 兴趣爱好类 ==========
    {
        "name": "露营装备",
        "pain_point": "想露营不知道买什么",
        "resonance": "想要完美的露营体验",
        "content_angles": ["露营好物推荐", "露营装备清单", "户外露营神器"],
        "hot_topics": ["露营", "户外", "野营", "露营装备"]
    },
    {
        "name": "钓鱼爱好",
        "pain_point": "钓鱼装备不知道选什么",
        "resonance": "想要更好的钓鱼体验",
        "content_angles": ["钓鱼好物推荐", "钓鱼装备清单", "钓鱼神器分享"],
        "hot_topics": ["钓鱼", "渔具", "垂钓", "钓鱼装备"]
    },
    {
        "name": "摄影入门",
        "pain_point": "想学摄影不知道从哪开始",
        "resonance": "想要入门级摄影装备",
        "content_angles": ["摄影入门好物", "新手相机推荐", "摄影器材指南"],
        "hot_topics": ["摄影", "相机", "摄影入门", "拍照"]
    },
    {
        "name": "手工DIY",
        "pain_point": "想学手工不知道买什么材料",
        "resonance": "想要开启手工创作之旅",
        "content_angles": ["手工好物推荐", "DIY材料清单", "手工入门指南"],
        "hot_topics": ["手工", "DIY", "手作", "手工入门"]
    },
    {
        "name": "园艺种植",
        "pain_point": "想养花种草不知道从哪开始",
        "resonance": "想要打造绿色家园",
        "content_angles": ["园艺好物推荐", "养花神器", "阳台种菜指南"],
        "hot_topics": ["园艺", "养花", "种植", "阳台花园"]
    },
    {
        "name": "烘焙入门",
        "pain_point": "想学烘焙不知道买什么工具",
        "resonance": "想要在家做出美味甜点",
        "content_angles": ["烘焙好物推荐", "烘焙工具清单", "烘焙入门指南"],
        "hot_topics": ["烘焙", "蛋糕", "甜点", "烘焙入门"]
    },
    {
        "name": "品茶爱好者",
        "pain_point": "想学品茶不知道买什么茶具",
        "resonance": "想要在家享受茶文化",
        "content_angles": ["茶具推荐", "品茶好物", "茶道入门指南"],
        "hot_topics": ["品茶", "茶具", "茶道", "茶文化"]
    },
    {
        "name": "音乐发烧友",
        "pain_point": "想提升听音乐体验",
        "resonance": "想要更好的音质享受",
        "content_angles": ["音乐好物推荐", "音响设备分享", "发烧友装备"],
        "hot_topics": ["音乐", "音响", "耳机", "音质"]
    },

    # ========== 健康养生类 ==========
    {
        "name": "颈椎保护",
        "pain_point": "颈椎不舒服",
        "resonance": "想要改善颈椎问题",
        "content_angles": ["颈椎好物推荐", "颈椎保护神器", "颈椎健康指南"],
        "hot_topics": ["颈椎", "颈椎病", "脖子疼", "颈椎保护"]
    },
    {
        "name": "腰椎护理",
        "pain_point": "腰椎不好久坐腰疼",
        "resonance": "想要保护腰椎健康",
        "content_angles": ["腰椎好物推荐", "护腰神器", "腰椎健康指南"],
        "hot_topics": ["腰椎", "腰疼", "护腰", "久坐"]
    },
    {
        "name": "护肤进阶",
        "pain_point": "护肤步骤太多不知道怎么用",
        "resonance": "想要科学护肤",
        "content_angles": ["护肤步骤指南", "护肤好物推荐", "科学护肤方法"],
        "hot_topics": ["护肤", "护肤品", "护肤步骤", "美容"]
    },
    {
        "name": "抗初老",
        "pain_point": "开始担心衰老问题",
        "resonance": "想要延缓衰老",
        "content_angles": ["抗老好物推荐", "初抗老指南", "抗衰老神器"],
        "hot_topics": ["抗老", "抗衰老", "初抗老", "年轻"]
    },
    {
        "name": "瘦身塑形",
        "pain_point": "想瘦身塑形",
        "resonance": "想要健康瘦身",
        "content_angles": ["瘦身好物推荐", "塑形神器", "健康减肥方法"],
        "hot_topics": ["瘦身", "减肥", "塑形", "瘦身神器"]
    },
    {
        "name": "增肌增重",
        "pain_point": "想增肌但不知道怎么吃练",
        "resonance": "想要科学增肌",
        "content_angles": ["增肌好物推荐", "健身增肌指南", "增重饮食方案"],
        "hot_topics": ["增肌", "健身", "肌肉", "增重"]
    },
    {
        "name": "视力保护",
        "pain_point": "眼睛干涩视力下降",
        "resonance": "想要保护视力",
        "content_angles": ["护眼好物推荐", "视力保护方法", "眼睛健康指南"],
        "hot_topics": ["视力", "护眼", "眼睛", "近视"]
    },
    {
        "name": "口腔护理",
        "pain_point": "口腔问题困扰",
        "resonance": "想要健康的口腔环境",
        "content_angles": ["口腔护理好物", "牙齿保护方法", "口腔健康指南"],
        "hot_topics": ["口腔", "牙齿", "口腔护理", "牙刷"]
    },

    # ========== 旅游出行类 ==========
    {
        "name": "亲子旅行",
        "pain_point": "带孩子旅行太麻烦",
        "resonance": "想要轻松的亲子旅行",
        "content_angles": ["亲子旅行好物", "带娃出行装备", "亲子游必备"],
        "hot_topics": ["亲子旅行", "带娃出行", "亲子游", "家庭旅行"]
    },
    {
        "name": "商务出行",
        "pain_point": "商务出差装备选择困难",
        "resonance": "想要专业又高效的出差体验",
        "content_angles": ["商务出行好物", "出差装备推荐", "商务旅行神器"],
        "hot_topics": ["商务出差", "出差装备", "商务旅行", "差旅"]
    },
    {
        "name": "自驾游",
        "pain_point": "自驾游不知道准备什么",
        "resonance": "想要完美的自驾之旅",
        "content_angles": ["自驾游好物推荐", "自驾装备清单", "自驾游攻略"],
        "hot_topics": ["自驾游", "自驾", "自驾装备", "公路旅行"]
    },
    {
        "name": "海岛度假",
        "pain_point": "去海岛不知道带什么",
        "resonance": "想要完美的海边假期",
        "content_angles": ["海岛度假好物", "海边装备清单", "海滩必备神器"],
        "hot_topics": ["海岛", "海边", "度假", "沙滩"]
    },
    {
        "name": "滑雪装备",
        "pain_point": "想滑雪不知道买什么装备",
        "resonance": "想要安全的滑雪体验",
        "content_angles": ["滑雪好物推荐", "滑雪装备清单", "滑雪入门指南"],
        "hot_topics": ["滑雪", "滑雪装备", "雪场", "冬季运动"]
    },
    {
        "name": "登山徒步",
        "pain_point": "想登山不知道准备什么",
        "resonance": "想要安全的登山体验",
        "content_angles": ["登山好物推荐", "徒步装备清单", "登山入门指南"],
        "hot_topics": ["登山", "徒步", "爬山", "户外运动"]
    },
    {
        "name": "境外旅行",
        "pain_point": "出国旅行准备复杂",
        "resonance": "想要顺利的出境之旅",
        "content_angles": ["出境旅行好物", "出国必备清单", "境外旅游攻略"],
        "hot_topics": ["出国", "境外游", "出境", "签证"]
    },
    {
        "name": "邮轮度假",
        "pain_point": "坐邮轮不知道准备什么",
        "resonance": "想要完美的邮轮体验",
        "content_angles": ["邮轮度假好物", "邮轮必备清单", "邮轮旅行攻略"],
        "hot_topics": ["邮轮", "游轮", "海上度假", "邮轮旅行"]
    },

    # ========== 科技数码类 ==========
    {
        "name": "智能家居",
        "pain_point": "想打造智能家居不知道从哪开始",
        "resonance": "想要智能化的生活",
        "content_angles": ["智能家居好物", "智能设备推荐", "智能家居入门"],
        "hot_topics": ["智能家居", "智能设备", "IoT", "智能生活"]
    },
    {
        "name": "桌面美学",
        "pain_point": "桌面太乱想要美化",
        "resonance": "想要高颜值的桌面",
        "content_angles": ["桌面美学好物", "桌面改造指南", "极简桌面打造"],
        "hot_topics": ["桌面", "桌面改造", "桌面美学", "书房布置"]
    },
    {
        "name": "电竞房打造",
        "pain_point": "想打造电竞房",
        "resonance": "想要专业的电竞环境",
        "content_angles": ["电竞房好物", "电竞装备推荐", "游戏房设计方案"],
        "hot_topics": ["电竞房", "游戏房", "电竞装备", "玩家"]
    },
    {
        "name": "直播设备",
        "pain_point": "想直播不知道买什么设备",
        "resonance": "想要专业的直播效果",
        "content_angles": ["直播好物推荐", "直播设备清单", "主播装备指南"],
        "hot_topics": ["直播", "主播", "直播设备", "网红"]
    },
    {
        "name": "短视频创作",
        "pain_point": "想拍短视频不知道用什么设备",
        "resonance": "想要高质量的短视频",
        "content_angles": ["短视频创作好物", "拍摄设备推荐", "视频创作指南"],
        "hot_topics": ["短视频", "抖音", "视频创作", "拍摄"]
    },
    {
        "name": "远程会议",
        "pain_point": "远程会议体验差",
        "resonance": "想要专业的远程会议体验",
        "content_angles": ["远程会议好物", "视频会议设备", "线上办公神器"],
        "hot_topics": ["远程会议", "视频会议", "线上会议", "Zoom"]
    },

    # ========== 美妆时尚类 ==========
    {
        "name": "约会妆容",
        "pain_point": "约会不知道化什么妆",
        "resonance": "想要完美的约会形象",
        "content_angles": ["约会妆容教程", "约会好物推荐", "约会必备单品"],
        "hot_topics": ["约会", "约会妆容", "化妆", "约会准备"]
    },
    {
        "name": "通勤妆",
        "pain_point": "上班化妆太费时间",
        "resonance": "想要快速自然的通勤妆",
        "content_angles": ["通勤妆容教程", "快速化妆技巧", "上班族美妆好物"],
        "hot_topics": ["通勤妆", "上班化妆", "快速化妆", "职业妆"]
    },
    {
        "name": "聚会派对",
        "pain_point": "聚会不知道穿什么",
        "resonance": "想要在聚会中出众",
        "content_angles": ["聚会穿搭推荐", "派对造型好物", "聚会必备单品"],
        "hot_topics": ["聚会", "派对", "派对穿搭", "聚会造型"]
    },
    {
        "name": "面试穿搭",
        "pain_point": "面试不知道穿什么",
        "resonance": "想要专业的面试形象",
        "content_angles": ["面试穿搭推荐", "面试形象指南", "求职好物"],
        "hot_topics": ["面试", "面试穿搭", "求职", "找工作"]
    },
    {
        "name": "健身穿搭",
        "pain_point": "健身房不知道穿什么",
        "resonance": "想要舒适时尚的运动装",
        "content_angles": ["健身穿搭推荐", "运动服选购指南", "健身房好物"],
        "hot_topics": ["健身穿搭", "运动服", "健身房", "瑜伽服"]
    },

    # ========== 母婴育儿类 ==========
    {
        "name": "孕期护理",
        "pain_point": "怀孕不知道需要准备什么",
        "resonance": "想要科学度过孕期",
        "content_angles": ["孕期好物推荐", "孕妇必备清单", "孕期护理指南"],
        "hot_topics": ["孕期", "孕妇", "怀孕", "孕期护理"]
    },
    {
        "name": "新生儿护理",
        "pain_point": "新生儿护理手忙脚乱",
        "resonance": "想要科学护理宝宝",
        "content_angles": ["新生儿护理好物", "宝宝护理技巧", "新手父母必备"],
        "hot_topics": ["新生儿", "宝宝护理", "新手爸妈", "育儿"]
    },
    {
        "name": "辅食添加",
        "pain_point": "宝宝添加辅食不知道从哪开始",
        "resonance": "想要科学喂养宝宝",
        "content_angles": ["辅食好物推荐", "辅食制作工具", "宝宝辅食指南"],
        "hot_topics": ["辅食", "宝宝辅食", "辅食工具", "婴儿辅食"]
    },
    {
        "name": "早教启蒙",
        "pain_point": "不知道怎么给宝宝早教",
        "resonance": "想要科学早教",
        "content_angles": ["早教好物推荐", "早教玩具选择", "宝宝启蒙指南"],
        "hot_topics": ["早教", "宝宝早教", "早教玩具", "启蒙"]
    },
    {
        "name": "二胎准备",
        "pain_point": "二胎不知道需要准备什么",
        "resonance": "想要科学准备二胎",
        "content_angles": ["二胎好物推荐", "二胎准备清单", "二胎家庭必备"],
        "hot_topics": ["二胎", "二胎准备", "二宝", "多孩家庭"]
    },

    # ========== 宠物类 ==========
    {
        "name": "新手养猫",
        "pain_point": "第一次养猫不知道准备什么",
        "resonance": "想要科学养猫",
        "content_angles": ["养猫好物推荐", "新手养猫指南", "猫咪必备清单"],
        "hot_topics": ["养猫", "新手养猫", "猫咪", "养猫指南"]
    },
    {
        "name": "新手养狗",
        "pain_point": "第一次养狗不知道准备什么",
        "resonance": "想要科学养狗",
        "content_angles": ["养狗好物推荐", "新手养狗指南", "狗狗必备清单"],
        "hot_topics": ["养狗", "新手养狗", "狗狗", "养狗指南"]
    },
    {
        "name": "宠物健康",
        "pain_point": "宠物健康问题困扰",
        "resonance": "想要宠物健康生活",
        "content_angles": ["宠物健康好物", "宠物护理技巧", "宠物医院指南"],
        "hot_topics": ["宠物健康", "宠物护理", "宠物医院", "宠物保健"]
    },
    {
        "name": "宠物美容",
        "pain_point": "宠物美容太贵想自己来",
        "resonance": "想要在家给宠物美容",
        "content_angles": ["宠物美容好物", "在家宠物美容", "宠物洗护指南"],
        "hot_topics": ["宠物美容", "宠物洗护", "宠物造型", "狗狗美容"]
    },

    # ========== 购物决策类 ==========
    {
        "name": "省钱攻略",
        "pain_point": "想省钱不知道怎么买划算",
        "resonance": "想要最优惠的价格",
        "content_angles": ["省钱攻略分享", "优惠券使用技巧", "如何省钱购物"],
        "hot_topics": ["省钱", "省钱攻略", "优惠", "省钱技巧"]
    },
    {
        "name": "拼单攻略",
        "pain_point": "想拼单但不知道怎么组织",
        "resonance": "想要更优惠的价格",
        "content_angles": ["拼单攻略分享", "拼单好物推荐", "组团购物技巧"],
        "hot_topics": ["拼单", "团购", "拼团", "团购优惠"]
    },
    {
        "name": "海淘攻略",
        "pain_point": "想海淘但流程复杂",
        "resonance": "想要买到海外好货",
        "content_angles": ["海淘攻略分享", "海淘好物推荐", "海外购物指南"],
        "hot_topics": ["海淘", "海外购物", "跨境电商", "代购"]
    },
    {
        "name": "二手好物",
        "pain_point": "想买二手但怕踩坑",
        "resonance": "想要性价比高的二手好物",
        "content_angles": ["二手好物推荐", "二手购物指南", "闲鱼淘货技巧"],
        "hot_topics": ["二手", "闲鱼", "二手好物", "闲置"]
    },

    # ========== 职场进阶类 ==========
    {
        "name": "副业赚钱",
        "pain_point": "想做副业增加收入",
        "resonance": "想要开启副业之路",
        "content_angles": ["副业好物推荐", "副业工具分享", "赚钱神器"],
        "hot_topics": ["副业", "赚钱", "副业推荐", "兼职"]
    },
    {
        "name": "技能提升",
        "pain_point": "想提升职场技能",
        "resonance": "想要职场进阶",
        "content_angles": ["技能提升好物", "学习工具推荐", "职场进阶指南"],
        "hot_topics": ["技能提升", "职场技能", "学习", "职场进阶"]
    },
    {
        "name": "考证备考",
        "pain_point": "想考证不知道怎么准备",
        "resonance": "想要顺利通过考试",
        "content_angles": ["考证好物推荐", "备考工具分享", "考试准备指南"],
        "hot_topics": ["考证", "备考", "考试", "证书"]
    },
    {
        "name": "跳槽准备",
        "pain_point": "想跳槽不知道怎么准备",
        "resonance": "想要找到更好的工作",
        "content_angles": ["跳槽好物推荐", "求职准备指南", "面试技巧分享"],
        "hot_topics": ["跳槽", "求职", "找工作", "换工作"]
    },

    # ========== 四季场景类 ==========
    {
        "name": "春季过敏",
        "pain_point": "春天过敏难受",
        "resonance": "想要缓解过敏症状",
        "content_angles": ["过敏好物推荐", "春季过敏防护", "过敏体质护理"],
        "hot_topics": ["春季过敏", "过敏", "花粉过敏", "换季过敏"]
    },
    {
        "name": "夏季防暑",
        "pain_point": "夏天太热受不了",
        "resonance": "想要清凉过夏天",
        "content_angles": ["防暑好物推荐", "夏日清凉神器", "避暑指南"],
        "hot_topics": ["夏天", "防暑", "避暑", "清凉"]
    },
    {
        "name": "秋季保湿",
        "pain_point": "秋天皮肤干燥",
        "resonance": "想要滋润保湿",
        "content_angles": ["秋季保湿好物", "换季护肤指南", "秋季护肤推荐"],
        "hot_topics": ["秋天", "保湿", "换季护肤", "皮肤干燥"]
    },
    {
        "name": "冬季护肤",
        "pain_point": "冬天皮肤干裂",
        "resonance": "想要滋润过冬",
        "content_angles": ["冬季护肤好物", "冬天护肤指南", "保湿滋润推荐"],
        "hot_topics": ["冬天", "冬季护肤", "护肤", "保湿"]
    },

    # ========== 特殊人群类 ==========
    {
        "name": "学生宿舍",
        "pain_point": "宿舍空间小条件有限",
        "resonance": "想要提升宿舍生活品质",
        "content_angles": ["宿舍好物推荐", "宿舍改造指南", "大学生必备"],
        "hot_topics": ["宿舍", "大学宿舍", "宿舍好物", "大学生"]
    },
    {
        "name": "租房党",
        "pain_point": "租房条件有限不能大改",
        "resonance": "想要舒适的租房生活",
        "content_angles": ["租房好物推荐", "租房改造指南", "租房必备清单"],
        "hot_topics": ["租房", "租房好物", "租房改造", "出租屋"]
    },
    {
        "name": "独居青年",
        "pain_point": "一个人住需要考虑很多",
        "resonance": "想要安全舒适的独居生活",
        "content_angles": ["独居好物推荐", "独居安全指南", "一个人住必备"],
        "hot_topics": ["独居", "一个人住", "独居好物", "单身生活"]
    },
    {
        "name": "丁克家庭",
        "pain_point": "丁克家庭生活方式选择",
        "resonance": "想要享受二人世界",
        "content_angles": ["丁克好物推荐", "二人生活指南", "丁克家庭必备"],
        "hot_topics": ["丁克", "二人世界", "丁克家庭", "不生孩子"]
    },
]

def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_existing_scenario_names(sku):
    return {s['name'] for s in sku['scenarios']}

def expand_sku_scenarios(data, min_scenarios=30):
    """
    为每个SKU扩展场景，确保每个SKU至少有min_scenarios个场景
    """
    total_added = 0

    for sku in data['skus']:
        existing_names = get_existing_scenario_names(sku)
        current_count = len(sku['scenarios'])

        if current_count >= min_scenarios:
            print(f"  {sku['sku_name']}: 已有 {current_count} 个场景，跳过")
            continue

        needed = min_scenarios - current_count
        added = 0

        for scenario in NEW_SCENARIOS:
            if scenario['name'] not in existing_names:
                sku['scenarios'].append(scenario)
                existing_names.add(scenario['name'])
                added += 1
                total_added += 1

                if added >= needed:
                    break

        print(f"  {sku['sku_name']}: 新增 {added} 个场景，共 {len(sku['scenarios'])} 个")

    # 更新统计信息
    total_scenarios = sum(len(sku['scenarios']) for sku in data['skus'])
    data['total_scenarios'] = total_scenarios
    data['updated_at'] = datetime.now().isoformat()

    return total_added, total_scenarios

def main():
    filepath = '/Users/zhangjingwei/.qclaw/workspace/hotspot-tracker/sku_scenes.json'

    print("加载现有数据...")
    data = load_data(filepath)

    print(f"当前状态: {data['total_skus']} 个SKU, {data['total_scenarios']} 个场景")
    print()

    print("开始扩展场景...")
    total_added, total_scenarios = expand_sku_scenarios(data)

    print()
    print(f"扩展完成!")
    print(f"  - 新增场景: {total_added}")
    print(f"  - 总场景数: {total_scenarios}")

    print()
    print("保存数据...")
    save_data(filepath, data)

    print("完成!")

if __name__ == '__main__':
    main()
