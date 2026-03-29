import json
from datetime import datetime

# 读取现有热点
with open('hot_topics.json', 'r', encoding='utf-8') as f:
    hot_topics = json.load(f)

# 新增热点（基于搜索结果）
new_hotspots = [
    {
        "id": 1315,
        "title": "张柏芝一天连飞三地远赴西班牙陪儿打球以泡面充饥",
        "platform": "微博/抖音",
        "heat": "高热",
        "trend": "🔥🔥🔥 快速上升",
        "type": "娱乐",
        "sentiment": "正面",
        "keywords": ["张柏芝", "西班牙", "亲子", "母亲", "明星"],
        "c": ["玉兰油", "AHC", "多芬"],
        "updated": "2026-03-30"
    },
    {
        "id": 1316,
        "title": "单依纯深夜发文为侵权演唱《李白》致歉李荣浩",
        "platform": "微博",
        "heat": "热搜第一",
        "trend": "🔥🔥🔥 爆发式增长",
        "type": "娱乐",
        "sentiment": "中性",
        "keywords": ["单依纯", "李荣浩", "版权", "演唱会", "音乐"],
        "c": ["元气森林", "农夫山泉"],
        "updated": "2026-03-30"
    },
    {
        "id": 1317,
        "title": "AI芯片引发整车涨价风暴小米极氪相继释放涨价预期",
        "platform": "微博/抖音",
        "heat": "高热",
        "trend": "🔥🔥🔥 快速上升",
        "type": "科技",
        "sentiment": "中性",
        "keywords": ["AI芯片", "新能源车", "涨价", "小米SU7", "极氪"],
        "c": ["小米", "荣耀", "索尼"],
        "updated": "2026-03-30"
    },
    {
        "id": 1318,
        "title": "Claude 90分钟挖穿20年漏洞GhostCMS跌下神坛",
        "platform": "微博/抖音",
        "heat": "高热",
        "trend": "🔥🔥🔥 爆发式增长",
        "type": "科技",
        "sentiment": "正面",
        "keywords": ["Claude", "AI", "安全漏洞", "网络安全", "Anthropic"],
        "c": ["荣耀", "小米", "罗技", "索尼"],
        "updated": "2026-03-30"
    },
    {
        "id": 1319,
        "title": "全国器官捐献志愿登记人数超733万挽救20万患者",
        "platform": "微博",
        "heat": "高热",
        "trend": "🔥🔥 持续上升",
        "type": "社会",
        "sentiment": "正面",
        "keywords": ["器官捐献", "公益", "生命", "红十字会"],
        "c": ["汤臣倍健", "善存", "农夫山泉"],
        "updated": "2026-03-30"
    },
    {
        "id": 1320,
        "title": "《鬼怪》主演重聚拍10周年旅行综艺引期待",
        "platform": "微博/抖音",
        "heat": "高热",
        "trend": "🔥🔥🔥 快速上升",
        "type": "娱乐",
        "sentiment": "正面",
        "keywords": ["鬼怪", "韩剧", "综艺", "孔刘", "李栋旭"],
        "c": ["AHC", "玉兰油", "多芬"],
        "updated": "2026-03-30"
    },
    {
        "id": 1321,
        "title": "《白日提灯》开播预约破674万迪丽热巴陈飞宇引爆全网",
        "platform": "微博/抖音",
        "heat": "热搜前三",
        "trend": "🔥🔥🔥 爆发式增长",
        "type": "娱乐",
        "sentiment": "正面",
        "keywords": ["白日提灯", "迪丽热巴", "陈飞宇", "古装剧", "腾讯视频"],
        "c": ["AHC", "玉兰油", "多芬"],
        "updated": "2026-03-30"
    },
    {
        "id": 1322,
        "title": "colorwalk色彩漫步成2026春季出游顶流曝光量4.63亿",
        "platform": "小红书/抖音",
        "heat": "4.63亿+",
        "trend": "🔥🔥🔥 爆发式增长",
        "type": "旅游",
        "sentiment": "正面",
        "keywords": ["colorwalk", "色彩漫步", "春季出游", "拍照打卡", "生活方式"],
        "c": ["元气森林", "农夫山泉", "OATLY", "百威", "索尼"],
        "updated": "2026-03-30"
    },
    {
        "id": 1323,
        "title": "小红书期权一年四连涨估值达3500亿员工提前换车",
        "platform": "微博",
        "heat": "高热",
        "trend": "🔥🔥🔥 快速上升",
        "type": "科技",
        "sentiment": "正面",
        "keywords": ["小红书", "期权", "上市", "互联网", "估值"],
        "c": ["荣耀", "小米", "罗技"],
        "updated": "2026-03-30"
    },
    {
        "id": 1324,
        "title": "\"反网红穿搭\"笔记上涨320%年轻人追求真实自我",
        "platform": "小红书/抖音",
        "heat": "高热",
        "trend": "🔥🔥🔥 持续上升",
        "type": "美妆",
        "sentiment": "正面",
        "keywords": ["反网红穿搭", "真实", "自我表达", "时尚", "年轻人"],
        "c": ["多芬", "玉兰油", "力士", "AHC"],
        "updated": "2026-03-30"
    },
    {
        "id": 1325,
        "title": "\"高科技让三轮闯进来了\"成春晚热梗智能三轮车颠覆印象",
        "platform": "微博/抖音",
        "heat": "高热",
        "trend": "🔥🔥 持续上升",
        "type": "热梗",
        "sentiment": "正面",
        "keywords": ["智能三轮车", "春晚", "科技平权", "热梗", "反差萌"],
        "c": ["荣耀", "小米", "索尼"],
        "updated": "2026-03-30"
    },
    {
        "id": 1326,
        "title": "\"打一针就好了\"成2026最火网络热梗与特朗普导弹并列",
        "platform": "全平台",
        "heat": "高热",
        "trend": "🔥🔥🔥 快速上升",
        "type": "热梗",
        "sentiment": "中性",
        "keywords": ["打一针就好了", "热梗", "离谱事件", "网络用语"],
        "c": ["荣耀", "小米", "OATLY", "元气森林"],
        "updated": "2026-03-30"
    }
]

# 合并新热点，去重
existing_ids = [t['id'] for t in hot_topics]
for new in new_hotspots:
    if new['id'] not in existing_ids:
        hot_topics.insert(0, new)

# 保持100条左右
hot_topics = hot_topics[:105]

# 保存
with open('hot_topics.json', 'w', encoding='utf-8') as f:
    json.dump(hot_topics, f, ensure_ascii=False, indent=2)

print(f"热点更新完成，共{len(hot_topics)}条，新增{len(new_hotspots)}条")
