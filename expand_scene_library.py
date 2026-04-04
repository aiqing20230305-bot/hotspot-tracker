#!/usr/bin/env python3
"""
SKU场景库扩展脚本
将SKU场景从6个扩展到至少150个
每个场景包含：id, name, industry, description, target_audience, keywords, content_type, hot_score
覆盖行业：美妆护肤、时尚穿搭、家居生活、母婴育儿、数码科技、食品健康、旅行出游、健身运动、职场职场、情感心理
"""

import json
import random
from datetime import datetime

# 基础场景库 - 覆盖所有行业
SCENE_LIBRARY = [
    # ========== 美妆护肤 (20个) ==========
    {
        "name": "早C晚A护肤",
        "industry": "美妆护肤",
        "description": "早晨使用维C产品抗氧化，晚上使用视黄醇抗衰老，是当前最流行的护肤公式",
        "target_audience": "追求科学护肤、25-40岁女性、对抗衰老有需求的人群",
        "keywords": ["早C晚A", "抗氧化", "抗衰老", "护肤公式", "成分党", "维C", "视黄醇"],
        "content_type": ["教程", "测评", "好物推荐"],
        "hot_score": 95
    },
    {
        "name": "敏感肌修复",
        "industry": "美妆护肤",
        "description": "针对敏感肌的修复护理方案，解决泛红、刺痛、紧绷等敏感问题",
        "target_audience": "敏感肌人群、屏障受损肌肤、换季易过敏人群",
        "keywords": ["敏感肌", "屏障修复", "泛红修复", "温和护肤", "舒缓", "皮肤屏障"],
        "content_type": ["修复指南", "产品推荐", "护肤技巧"],
        "hot_score": 92
    },
    {
        "name": "油皮控油攻略",
        "industry": "美妆护肤",
        "description": "针对油性皮肤的控油护理，从清洁到保湿的完整控油方案",
        "target_audience": "油性皮肤、混合偏油肌肤、容易长痘人群",
        "keywords": ["控油", "油皮", "清爽", "去油", "油光", "毛孔粗大"],
        "content_type": ["护肤教程", "产品测评", "日常护理"],
        "hot_score": 88
    },
    {
        "name": "抗初老入门",
        "industry": "美妆护肤",
        "description": "25岁+女性的抗初老指南，预防性抗衰老护理方案",
        "target_audience": "25-35岁女性、开始关注衰老迹象、预防性护肤人群",
        "keywords": ["抗初老", "抗衰老", "紧致", "抗皱", "淡化细纹", "胶原蛋白"],
        "content_type": ["抗老指南", "产品推荐", "成分分析"],
        "hot_score": 93
    },
    {
        "name": "刷酸焕肤",
        "industry": "美妆护肤",
        "description": "化学焕肤的正确打开方式，解决痘痘、闭口、痘印等问题",
        "target_audience": "痘痘肌、闭口粉刺、痘印困扰者、想改善肤质人群",
        "keywords": ["刷酸", "果酸", "水杨酸", "焕肤", "祛痘", "去角质", "闭口"],
        "content_type": ["教程", "注意事项", "产品推荐"],
        "hot_score": 90
    },
    {
        "name": "素颜霜测评",
        "industry": "美妆护肤",
        "description": "无需卸妆的素颜霜，懒人快速出门的底妆选择",
        "target_audience": "追求自然妆感、时间紧张、懒人护肤群体",
        "keywords": ["素颜霜", "懒人底妆", "自然妆感", "快速出门", "伪素颜"],
        "content_type": ["测评", "对比", "使用教程"],
        "hot_score": 82
    },
    {
        "name": "卸妆产品测评",
        "industry": "美妆护肤",
        "description": "卸妆油、卸妆膏、卸妆水全面测评，找到最适合的卸妆产品",
        "target_audience": "化妆人群、关注卸妆效果、追求温和清洁的用户",
        "keywords": ["卸妆", "卸妆油", "卸妆膏", "卸妆水", "清洁", "洁面"],
        "content_type": ["测评", "对比", "选购指南"],
        "hot_score": 85
    },
    {
        "name": "面膜急救护肤",
        "industry": "美妆护肤",
        "description": "熬夜后、约会前、换季时的急救面膜使用指南",
        "target_audience": "熬夜党、经常需要急救护肤、追求快速见效人群",
        "keywords": ["面膜", "急救", "熬夜修复", "补水", "镇定", "快速护肤"],
        "content_type": ["急救指南", "产品推荐", "使用技巧"],
        "hot_score": 87
    },
    {
        "name": "防晒重要性",
        "industry": "美妆护肤",
        "description": "强调防晒是抗衰老的第一步，紫外线对皮肤的伤害",
        "target_audience": "所有护肤人群、忽视防晒者、抗老需求人群",
        "keywords": ["防晒", "紫外线", "光老化", "SPF", "PA值", "防晒霜"],
        "content_type": ["科普", "选购指南", "使用方法"],
        "hot_score": 94
    },
    {
        "name": "成分党护肤",
        "industry": "美妆护肤",
        "description": "从成分角度分析护肤品，了解烟酰胺、玻尿酸、视黄醇等热门成分",
        "target_audience": "理性护肤人群、成分党、想要科学选择护肤品用户",
        "keywords": ["成分党", "烟酰胺", "玻尿酸", "视黄醇", "成分分析", "科学护肤"],
        "content_type": ["成分解析", "产品分析", "科普"],
        "hot_score": 89
    },
    {
        "name": "祛斑美白",
        "industry": "美妆护肤",
        "description": "针对色斑、痘印、肤色不均等问题的美白淡斑方案",
        "target_audience": "有色斑困扰、追求白皙肤色、肤色不均人群",
        "keywords": ["美白", "祛斑", "淡斑", "提亮肤色", "淡化痘印", "色斑"],
        "content_type": ["方案推荐", "产品测评", "护理教程"],
        "hot_score": 91
    },
    {
        "name": "男士护肤",
        "industry": "美妆护肤",
        "description": "专为男性设计的简化护肤方案，解决油光、痘痘、毛孔问题",
        "target_audience": "男性用户、护肤新手、追求简单有效男性",
        "keywords": ["男士护肤", "男性护肤", "控油", "洁面", "简约护肤"],
        "content_type": ["入门指南", "产品推荐", "护肤教程"],
        "hot_score": 78
    },
    {
        "name": "孕期护肤",
        "industry": "美妆护肤",
        "description": "孕妇可用的安全护肤成分和产品选择指南",
        "target_audience": "孕妇、备孕女性、哺乳期妈妈",
        "keywords": ["孕期护肤", "孕妇护肤", "安全成分", "护肤禁忌", "孕妇可用"],
        "content_type": ["安全指南", "产品推荐", "成分科普"],
        "hot_score": 80
    },
    {
        "name": "医美护肤搭配",
        "industry": "美妆护肤",
        "description": "医美术后如何搭配日常护肤品，加速恢复、延长效果",
        "target_audience": "医美爱好者、刚做完医美项目、追求更好效果人群",
        "keywords": ["医美", "术后护理", "护肤搭配", "光子嫩肤", "水光针", "恢复"],
        "content_type": ["护理指南", "产品搭配", "注意事项"],
        "hot_score": 86
    },
    {
        "name": "眼霜抗皱",
        "industry": "美妆护肤",
        "description": "眼部护理的重要性，选择适合自己的眼霜对抗细纹黑眼圈",
        "target_audience": "25+女性、有眼部问题困扰、预防眼周衰老人群",
        "keywords": ["眼霜", "抗皱", "黑眼圈", "眼袋", "细纹", "眼部护理"],
        "content_type": ["产品推荐", "使用方法", "测评"],
        "hot_score": 83
    },
    {
        "name": "精华液测评",
        "industry": "美妆护肤",
        "description": "各类精华液全面测评：补水、美白、抗老、修复功效",
        "target_audience": "想要进阶护肤、关注精华产品、理性消费人群",
        "keywords": ["精华", "精华液", "测评", "功效", "护肤进阶"],
        "content_type": ["测评", "对比", "选购指南"],
        "hot_score": 88
    },
    {
        "name": "换季护肤",
        "industry": "美妆护肤",
        "description": "春夏、秋冬换季时的护肤重点调整，避免敏感干燥",
        "target_audience": "换季易敏感人群、所有护肤人群",
        "keywords": ["换季护肤", "换季敏感", "季节护理", "干燥", "保湿调整"],
        "content_type": ["换季指南", "产品调整", "护肤技巧"],
        "hot_score": 84
    },
    {
        "name": "彩妆护肤双效",
        "industry": "美妆护肤",
        "description": "具有护肤功效的彩妆产品，化妆护肤两不误",
        "target_audience": "追求高效、化妆同时护肤、懒人美妆群体",
        "keywords": ["养肤彩妆", "护肤彩妆", "隔离霜", "BB霜", "气垫"],
        "content_type": ["产品推荐", "测评", "使用技巧"],
        "hot_score": 81
    },
    {
        "name": "痘痘肌护理",
        "industry": "美妆护肤",
        "description": "针对痘痘肌肤的完整护理方案，从成因到治理",
        "target_audience": "痘痘肌肤、痤疮困扰、反复长痘人群",
        "keywords": ["祛痘", "痘痘肌", "痤疮", "控油", "消炎", "战痘"],
        "content_type": ["成因分析", "护理方案", "产品推荐"],
        "hot_score": 89
    },
    {
        "name": "毛孔收缩",
        "industry": "美妆护肤",
        "description": "缩小毛孔的护肤方案，针对粗大毛孔的改善方法",
        "target_audience": "毛孔粗大人群、油性肌肤、追求细腻肤质用户",
        "keywords": ["毛孔", "收缩毛孔", "毛孔粗大", "细腻肌肤", "收敛"],
        "content_type": ["方案推荐", "产品测评", "日常护理"],
        "hot_score": 85
    },

    # ========== 时尚穿搭 (15个) ==========
    {
        "name": "职场穿搭",
        "industry": "时尚穿搭",
        "description": "职场专业穿搭指南，打造干练、得体、有气质的职场形象",
        "target_audience": "职场新人、商务人士、想要提升职场形象人群",
        "keywords": ["职场穿搭", "通勤装", "职业装", "干练", "专业形象", "商务穿搭"],
        "content_type": ["穿搭指南", "单品推荐", "搭配技巧"],
        "hot_score": 90
    },
    {
        "name": "约会穿搭",
        "industry": "时尚穿搭",
        "description": "不同类型约会的穿搭指南：第一次约会、纪念日、正式约会等",
        "target_audience": "恋爱中女性、想要提升约会魅力、约会前准备人群",
        "keywords": ["约会穿搭", "约会装", "第一次约会", "连衣裙", "女性穿搭"],
        "content_type": ["穿搭指南", "场合分析", "搭配灵感"],
        "hot_score": 92
    },
    {
        "name": "小个子显高",
        "industry": "时尚穿搭",
        "description": "155cm以下小个子的显高穿搭技巧，通过搭配视觉增高",
        "target_audience": "小个子女生、想要显高、身材娇小人群",
        "keywords": ["小个子穿搭", "显高", "增高", "小个子女生", "视觉增高"],
        "content_type": ["穿搭技巧", "单品推荐", "搭配法则"],
        "hot_score": 88
    },
    {
        "name": "微胖穿搭",
        "industry": "时尚穿搭",
        "description": "针对微胖身材的显瘦穿搭，遮肉显瘦两不误",
        "target_audience": "微胖女性、梨形身材、想要显瘦人群",
        "keywords": ["微胖穿搭", "显瘦", "遮肉", "梨形身材", "微胖女生"],
        "content_type": ["穿搭指南", "单品推荐", "显瘦技巧"],
        "hot_score": 91
    },
    {
        "name": "闺蜜出游穿搭",
        "industry": "时尚穿搭",
        "description": "和闺蜜一起出游的穿搭指南，拍照好看又舒适",
        "target_audience": "闺蜜出游、拍照需求、追求时尚好看人群",
        "keywords": ["出游穿搭", "闺蜜装", "拍照穿搭", "旅行穿搭", "度假风"],
        "content_type": ["穿搭灵感", "拍照技巧", "搭配分享"],
        "hot_score": 86
    },
    {
        "name": "法式优雅",
        "industry": "时尚穿搭",
        "description": "法式风格穿搭精髓，慵懒、优雅、高级感的法式美学",
        "target_audience": "追求法式风格、喜欢简约优雅、文艺气质女性",
        "keywords": ["法式穿搭", "法式风格", "优雅", "简约", "法式风情"],
        "content_type": ["风格解析", "单品推荐", "搭配法则"],
        "hot_score": 89
    },
    {
        "name": "美式休闲",
        "industry": "时尚穿搭",
        "description": "美式休闲风格穿搭，舒适、随性、有态度的街头风格",
        "target_audience": "追求休闲风格、年轻群体、喜欢街头风人群",
        "keywords": ["美式穿搭", "休闲风", "街头风", "卫衣", "潮流"],
        "content_type": ["风格解析", "单品推荐", "搭配灵感"],
        "hot_score": 84
    },
    {
        "name": "极简主义穿搭",
        "industry": "时尚穿搭",
        "description": "胶囊衣橱理念，用少量单品搭配多种造型",
        "target_audience": "追求简约、理性消费、断舍离爱好者",
        "keywords": ["极简穿搭", "胶囊衣橱", "少即是多", "基础款", "断舍离"],
        "content_type": ["衣橱规划", "单品选择", "搭配技巧"],
        "hot_score": 87
    },
    {
        "name": "韩系穿搭",
        "industry": "时尚穿搭",
        "description": "韩剧女主同款穿搭，韩系风格的精髓与搭配技巧",
        "target_audience": "喜欢韩系风格、追韩剧、追求时尚年轻群体",
        "keywords": ["韩系穿搭", "韩风", "韩剧穿搭", "韩式风格", "流行趋势"],
        "content_type": ["风格解析", "单品推荐", "搭配技巧"],
        "hot_score": 90
    },
    {
        "name": "轻奢质感",
        "industry": "时尚穿搭",
        "description": "轻奢品牌推荐，用合理价格获得高级质感",
        "target_audience": "追求品质、有一定消费能力、想要提升档次人群",
        "keywords": ["轻奢", "质感", "高级感", "小众品牌", "品质穿搭"],
        "content_type": ["品牌推荐", "单品测评", "购物指南"],
        "hot_score": 85
    },
    {
        "name": "平价穿搭",
        "industry": "时尚穿搭",
        "description": "高性价比平价品牌推荐，预算有限也能穿出时尚感",
        "target_audience": "学生党、预算有限、追求性价比人群",
        "keywords": ["平价穿搭", "学生党", "性价比", "高颜值平价", "省钱穿搭"],
        "content_type": ["品牌推荐", "单品推荐", "购物攻略"],
        "hot_score": 89
    },
    {
        "name": "不同体型穿搭",
        "industry": "时尚穿搭",
        "description": "根据身型选择最适合的穿搭：苹果型、梨形、沙漏、H型",
        "target_audience": "想要了解自己身型、找到最适合风格的人群",
        "keywords": ["身型穿搭", "体型分析", "扬长避短", "苹果型", "梨形身材"],
        "content_type": ["身型分析", "穿搭技巧", "单品推荐"],
        "hot_score": 88
    },
    {
        "name": "配饰点睛",
        "industry": "时尚穿搭",
        "description": "用配饰提升整体造型感，耳饰、项链、手表、包袋搭配",
        "target_audience": "想要提升穿搭细节、注重整体造型、配饰爱好者",
        "keywords": ["配饰", "首饰", "耳饰", "项链", "手表", "包袋搭配", "点睛之笔"],
        "content_type": ["搭配技巧", "单品推荐", "选购指南"],
        "hot_score": 83
    },
    {
        "name": "一衣多穿",
        "industry": "时尚穿搭",
        "description": "一件单品多种搭配方式，最大化利用衣橱单品",
        "target_audience": "追求高效搭配、衣橱有限、想要更多造型变化人群",
        "keywords": ["一衣多穿", "搭配技巧", "单品搭配", "胶囊衣橱", "高利用率"],
        "content_type": ["搭配示范", "造型灵感", "搭配教程"],
        "hot_score": 86
    },
    {
        "name": "场合穿搭指南",
        "industry": "时尚穿搭",
        "description": "不同场合的正确穿搭：面试、晚宴、聚会、旅行",
        "target_audience": "需要出席各种场合、想要得体穿搭、社交活跃人群",
        "keywords": ["场合穿搭", "着装规范", "晚宴装", "正式场合", "得体穿搭"],
        "content_type": ["场合分析", "穿搭指南", "单品推荐"],
        "hot_score": 84
    },

    # ========== 家居生活 (20个) ==========
    {
        "name": "租房改造",
        "industry": "家居生活",
        "description": "低成本改造出租屋，在有限条件下提升居住品质",
        "target_audience": "租房人群、预算有限、追求生活品质的年轻人",
        "keywords": ["租房改造", "出租屋", "低成本布置", "改造灵感", "房东不允许"],
        "content_type": ["改造指南", "好物推荐", "技巧分享"],
        "hot_score": 94
    },
    {
        "name": "小户型收纳",
        "industry": "家居生活",
        "description": "小户型空间利用最大化，收纳技巧让家更整洁",
        "target_audience": "小户型住户、收纳困难、空间有限人群",
        "keywords": ["小户型", "收纳", "空间利用", "整理技巧", "储物"],
        "content_type": ["收纳技巧", "好物推荐", "空间规划"],
        "hot_score": 91
    },
    {
        "name": "智能家居入门",
        "industry": "家居生活",
        "description": "智能家居从0到1搭建，便利生活从此开始",
        "target_audience": "科技爱好者、追求便利生活、新手入门智能家居人群",
        "keywords": ["智能家居", "IoT", "小米生态", "全屋智能", "智能设备"],
        "content_type": ["入门指南", "产品推荐", "搭建方案"],
        "hot_score": 93
    },
    {
        "name": "阳台花园",
        "industry": "家居生活",
        "description": "打造阳台小花园，绿植花卉让家更有生气",
        "target_audience": "绿植爱好者、想要美化家居、园艺新手",
        "keywords": ["阳台花园", "绿植", "园艺", "阳台布置", "室内植物"],
        "content_type": ["园艺教程", "植物推荐", "布置灵感"],
        "hot_score": 87
    },
    {
        "name": "卧室氛围感",
        "industry": "家居生活",
        "description": "打造有氛围感的卧室，灯光、软装营造舒适睡眠环境",
        "target_audience": "追求生活品质、注重睡眠环境、软装爱好者",
        "keywords": ["卧室布置", "氛围感", "软装", "灯光", "睡眠环境", "四件套"],
        "content_type": ["布置指南", "单品推荐", "氛围营造"],
        "hot_score": 89
    },
    {
        "name": "厨房收纳",
        "industry": "家居生活",
        "description": "厨房收纳整理技巧，让做饭更轻松愉悦",
        "target_audience": "热爱烹饪、厨房收纳困难、追求整洁人群",
        "keywords": ["厨房收纳", "厨房整理", "收纳神器", "厨具收纳", "调料收纳"],
        "content_type": ["收纳技巧", "好物推荐", "整理方法"],
        "hot_score": 88
    },
    {
        "name": "清洁好物",
        "industry": "家居生活",
        "description": "让家务更轻松的清洁神器，地面、厨房、卫生间全覆盖",
        "target_audience": "追求高效清洁、懒人清洁、家务繁忙人群",
        "keywords": ["清洁好物", "清洁神器", "家务", "打扫", "地面清洁", "除螨"],
        "content_type": ["好物推荐", "测评", "清洁技巧"],
        "hot_score": 92
    },
    {
        "name": "香薰蜡烛",
        "industry": "家居生活",
        "description": "提升生活幸福感的香薰产品，打造治愈系家居氛围",
        "target_audience": "追求生活仪式感、香氛爱好者、缓解压力人群",
        "keywords": ["香薰", "香薰蜡烛", "香氛", "治愈", "生活仪式感", "氛围"],
        "content_type": ["品牌推荐", "香型测评", "使用技巧"],
        "hot_score": 85
    },
    {
        "name": "一人食餐具",
        "industry": "家居生活",
        "description": "适合一人食的餐具推荐，让独居用餐也有仪式感",
        "target_audience": "独居人群、一人食爱好者、追求用餐仪式感群体",
        "keywords": ["一人食", "餐具", "碗碟", "独居", "仪式感", "高颜值餐具"],
        "content_type": ["好物推荐", "搭配技巧", "品牌推荐"],
        "hot_score": 83
    },
    {
        "name": "床上用品",
        "industry": "家居生活",
        "description": "如何选择舒适的床品四件套，提升睡眠质量",
        "target_audience": "注重睡眠质量、床品选购、追求舒适人群",
        "keywords": ["四件套", "床品", "被子", "枕头", "睡眠质量", "舒适"],
        "content_type": ["选购指南", "材质科普", "品牌推荐"],
        "hot_score": 86
    },
    {
        "name": "收纳神器",
        "industry": "家居生活",
        "description": "各种收纳神器推荐，衣柜、抽屉、冰箱收纳全覆盖",
        "target_audience": "整理爱好者、断舍离践行者、收纳困难人群",
        "keywords": ["收纳神器", "收纳盒", "收纳袋", "整理", "衣柜收纳", "冰箱收纳"],
        "content_type": ["好物推荐", "收纳技巧", "使用场景"],
        "hot_score": 90
    },
    {
        "name": "ins风家居",
        "industry": "家居生活",
        "description": "打造网红ins风家居，拍照好看又舒适的家居布置",
        "target_audience": "喜欢拍照、追求高颜值家居、社交媒体活跃群体",
        "keywords": ["ins风", "网红家居", "高颜值", "拍照背景", "家居布置"],
        "content_type": ["布置灵感", "单品推荐", "拍照技巧"],
        "hot_score": 88
    },
    {
        "name": "宠物友好家居",
        "industry": "家居生活",
        "description": "养宠物家庭的家居布置，人宠共处的舒适空间打造",
        "target_audience": "宠物主人、想要人宠和谐、养猫养狗人群",
        "keywords": ["宠物家居", "养猫", "养狗", "人宠共处", "宠物用品"],
        "content_type": ["布置指南", "好物推荐", "注意事项"],
        "hot_score": 87
    },
    {
        "name": "懒人清洁",
        "industry": "家居生活",
        "description": "解放双手的懒人清洁神器，扫地机、洗地机推荐",
        "target_audience": "懒人、繁忙上班族、想要减少家务负担人群",
        "keywords": ["扫地机器人", "洗地机", "懒人清洁", "智能家电", "解放双手"],
        "content_type": ["产品测评", "对比", "选购指南"],
        "hot_score": 93
    },
    {
        "name": "玄关设计",
        "industry": "家居生活",
        "description": "打造整洁实用的玄关空间，进门第一眼的仪式感",
        "target_audience": "注重家居细节、进门收纳困难、想要整洁玄关人群",
        "keywords": ["玄关", "玄关设计", "鞋柜", "收纳", "入户", "门厅"],
        "content_type": ["设计灵感", "收纳技巧", "好物推荐"],
        "hot_score": 82
    },
    {
        "name": "书房布置",
        "industry": "家居生活",
        "description": "打造舒适高效的书房/办公空间，居家办公必备",
        "target_audience": "居家办公、WFH人群、注重工作效率人群",
        "keywords": ["书房", "办公桌", "书房布置", "居家办公", "工作空间"],
        "content_type": ["布置指南", "好物推荐", "空间规划"],
        "hot_score": 89
    },
    {
        "name": "浴室好物",
        "industry": "家居生活",
        "description": "浴室收纳和好物推荐，打造干净舒适的沐浴空间",
        "target_audience": "注重生活品质、浴室收纳困难、追求舒适沐浴体验人群",
        "keywords": ["浴室好物", "浴室收纳", "沐浴", "洗漱", "卫生间"],
        "content_type": ["好物推荐", "收纳技巧", "品牌推荐"],
        "hot_score": 84
    },
    {
        "name": "厨房小白装备",
        "industry": "家居生活",
        "description": "厨房新手必备厨具和用品，快速上手做菜",
        "target_audience": "厨房新手、想要学做饭、刚独立生活人群",
        "keywords": ["厨房小白", "厨具", "做饭", "厨具推荐", "新手装备"],
        "content_type": ["装备清单", "好物推荐", "选购指南"],
        "hot_score": 88
    },
    {
        "name": "绿植装饰",
        "industry": "家居生活",
        "description": "适合室内的绿植推荐，让家更有生命力的装饰",
        "target_audience": "绿植爱好者、室内装饰、想要增添生机人群",
        "keywords": ["绿植", "室内植物", "装饰", "家居绿植", "INS绿植"],
        "content_type": ["植物推荐", "养护技巧", "搭配指南"],
        "hot_score": 86
    },
    {
        "name": "全屋清洁",
        "industry": "家居生活",
        "description": "从客厅到卧室的全屋清洁攻略，保持家的整洁",
        "target_audience": "注重家庭卫生、想要系统清洁、清洁困难户",
        "keywords": ["全屋清洁", "打扫", "卫生", "清洁攻略", "日常清洁"],
        "content_type": ["清洁指南", "好物推荐", "技巧分享"],
        "hot_score": 85
    },

    # ========== 母婴育儿 (15个) ==========
    {
        "name": "待产包清单",
        "industry": "母婴育儿",
        "description": "准妈妈待产包必备清单，入院生产需要的物品准备",
        "target_audience": "准妈妈、临近预产期、待产准备人群",
        "keywords": ["待产包", "入院", "待产", "准妈妈", "生产必备"],
        "content_type": ["清单", "好物推荐", "准备指南"],
        "hot_score": 95
    },
    {
        "name": "新生儿护理",
        "industry": "母婴育儿",
        "description": "0-3个月新生儿护理要点，从喂养到睡眠的全面指南",
        "target_audience": "新手爸妈、新生儿父母、育儿知识储备不足人群",
        "keywords": ["新生儿", "护理", "新手爸妈", "喂养", "婴儿护理"],
        "content_type": ["护理指南", "知识科普", "好物推荐"],
        "hot_score": 94
    },
    {
        "name": "宝宝辅食",
        "industry": "母婴育儿",
        "description": "6个月+宝宝辅食添加指南，从米粉到手指食物",
        "target_audience": "6个月以上宝宝父母、辅食添加阶段、注重营养均衡人群",
        "keywords": ["辅食", "宝宝辅食", "辅食添加", "婴儿辅食", "营养"],
        "content_type": ["辅食指南", "食谱推荐", "工具推荐"],
        "hot_score": 93
    },
    {
        "name": "儿童安全座椅",
        "industry": "母婴育儿",
        "description": "如何选择和使用儿童安全座椅，保障宝宝出行安全",
        "target_audience": "有车家庭、有宝宝出行需求、注重安全人群",
        "keywords": ["安全座椅", "儿童安全", "出行安全", "车载", "宝宝座椅"],
        "content_type": ["选购指南", "使用教程", "品牌推荐"],
        "hot_score": 91
    },
    {
        "name": "婴儿床品",
        "industry": "母婴育儿",
        "description": "婴儿床品选择指南，安全的睡眠环境营造",
        "target_audience": "新生儿父母、婴儿房布置、注重安全睡眠人群",
        "keywords": ["婴儿床", "婴儿床品", "婴儿床垫", "宝宝睡眠", "婴儿被"],
        "content_type": ["选购指南", "好物推荐", "安全指南"],
        "hot_score": 87
    },
    {
        "name": "背带腰凳",
        "industry": "母婴育儿",
        "description": "婴儿背带和腰凳推荐，解放双手的带娃神器",
        "target_audience": "独自带娃、想要解放双手、经常外出带娃人群",
        "keywords": ["背带", "腰凳", "婴儿背带", "解放双手", "带娃神器"],
        "content_type": ["好物推荐", "使用技巧", "选购指南"],
        "hot_score": 88
    },
    {
        "name": "宝宝绘本",
        "industry": "母婴育儿",
        "description": "0-6岁宝宝绘本推荐，培养阅读习惯从娃娃抓起",
        "target_audience": "重视早教、想要培养阅读习惯、0-6岁宝宝家长",
        "keywords": ["绘本", "儿童绘本", "早教", "阅读", "绘本推荐"],
        "content_type": ["推荐清单", "年龄推荐", "选购指南"],
        "hot_score": 90
    },
    {
        "name": "婴儿推车",
        "industry": "母婴育儿",
        "description": "婴儿推车选购指南，高景观、轻便、安全全方位考量",
        "target_audience": "新生儿父母、需要推车出行、选购困惑人群",
        "keywords": ["婴儿车", "推车", "婴儿推车", "高景观", "轻便"],
        "content_type": ["选购指南", "品牌对比", "使用测评"],
        "hot_score": 92
    },
    {
        "name": "哺乳期用品",
        "industry": "母婴育儿",
        "description": "哺乳期妈妈必备用品，从吸奶器到防溢乳垫",
        "target_audience": "哺乳期妈妈、母乳喂养、产后恢复人群",
        "keywords": ["哺乳期", "吸奶器", "母乳", "防溢乳垫", "哺乳内衣"],
        "content_type": ["好物推荐", "使用指南", "选购建议"],
        "hot_score": 89
    },
    {
        "name": "儿童玩具",
        "industry": "母婴育儿",
        "description": "不同年龄段儿童玩具推荐，开发智力又安全",
        "target_audience": "有儿童家庭、玩具选购困惑、早教意识强家长",
        "keywords": ["儿童玩具", "玩具推荐", "益智玩具", "安全玩具"],
        "content_type": ["年龄段推荐", "好物清单", "选购指南"],
        "hot_score": 91
    },
    {
        "name": "月子餐",
        "industry": "母婴育儿",
        "description": "科学月子餐搭配，帮助产妇恢复又保证奶水充足",
        "target_audience": "坐月子女性、产妇家属、注重产后营养人群",
        "keywords": ["月子餐", "产后营养", "坐月子", "催奶", "恢复"],
        "content_type": ["食谱推荐", "营养指南", "注意事项"],
        "hot_score": 88
    },
    {
        "name": "婴儿洗护",
        "industry": "母婴育儿",
        "description": "婴儿洗护用品推荐，温和安全是首选",
        "target_audience": "新生儿父母、注重婴儿安全、选购洗护产品困惑人群",
        "keywords": ["婴儿洗护", "沐浴露", "洗发水", "婴儿护肤", "温和"],
        "content_type": ["产品推荐", "成分分析", "选购指南"],
        "hot_score": 86
    },
    {
        "name": "早教启蒙",
        "industry": "母婴育儿",
        "description": "0-3岁早教启蒙方法，在家也能做的