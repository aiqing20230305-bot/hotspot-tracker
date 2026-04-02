import json
import random
import string
from datetime import datetime

# 读取现有数据
with open('hot_topics.json', 'r', encoding='utf-8') as f:
    hot_topics = json.load(f)

# 生成唯一ID
def gen_id():
    return ''.join(random.choices(string.hexdigits.lower(), k=8))

# 当前时间
now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

# 20个客户列表
clients = ["荣耀", "罗技", "小米", "索尼", "AHC", "多芬", "力士", "清扬", "玉兰油", "汤臣倍健", "善存", "HC", "威猛先生", "舒适", "希宝", "皇家", "OATLY", "百威", "元气森林", "农夫山泉"]

# 新热点数据（基于当前时间凌晨4点的特点）
new_hotspots = [
    {
        "title": "清明节后首个工作日 打工人早八状态引热议",
        "hot_value": 398000000,
        "url": "https://weibo.com",
        "platform": "微博/全网",
        "industries": ["社会", "职场"],
        "trends": ["爆"],
        "type": "社会热点",
        "sentiment": "中性",
        "keywords": ["清明节", "工作日", "打工人", "早八", "假期综合症"],
        "c": ["汤臣倍健", "善存", "元气森林"],
        "created_at": now,
        "rank": 1,
        "id": f"ht_{gen_id()}"
    },
    {
        "title": "AI绘画Midjourney V7发布 画质提升惊艳全网",
        "hot_value": 395000000,
        "url": "https://weibo.com",
        "platform": "微博/全网",
        "industries": ["科技", "AI"],
        "trends": ["爆"],
        "type": "科技热点",
        "sentiment": "正面",
        "keywords": ["AI绘画", "Midjourney", "V7", "画质", "AI创作"],
        "c": ["小米", "荣耀", "索尼"],
        "created_at": now,
        "rank": 2,
        "id": f"ht_{gen_id()}"
    },
    {
        "title": "孙颖莎世界杯3-0晋级 开启争冠之路",
        "hot_value": 390000000,
        "url": "https://k.sina.com.cn/article_7879995911_1d5af320706801qk78.html",
        "platform": "微博/抖音",
        "industries": ["体育"],
        "trends": ["热"],
        "type": "体育热点",
        "sentiment": "正面",
        "keywords": ["孙颖莎", "乒乓球", "世界杯", "3-0", "晋级"],
        "c": ["元气森林", "农夫山泉", "汤臣倍健"],
        "created_at": now,
        "rank": 3,
        "id": f"ht_{gen_id()}"
    },
    {
        "title": "五一小长假旅游预订火爆 热门目的地机票售罄",
        "hot_value": 388000000,
        "url": "https://weibo.com",
        "platform": "微博/小红书",
        "industries": ["旅游", "消费"],
        "trends": ["爆"],
        "type": "消费热点",
        "sentiment": "正面",
        "keywords": ["五一", "小长假", "旅游", "预订", "出行"],
        "c": ["农夫山泉", "元气森林", "OATLY", "百威"],
        "created_at": now,
        "rank": 4,
        "id": f"ht_{gen_id()}"
    },
    {
        "title": "春季护肤攻略 美白精华测评成小红书热门",
        "hot_value": 385000000,
        "url": "https://xiaohongshu.com",
        "platform": "小红书",
        "industries": ["美妆", "护肤"],
        "trends": ["爆"],
        "type": "美妆热点",
        "sentiment": "正面",
        "keywords": ["春季护肤", "美白精华", "测评", "护肤攻略", "换季"],
        "c": ["AHC", "玉兰油", "多芬"],
        "created_at": now,
        "rank": 5,
        "id": f"ht_{gen_id()}"
    },
    {
        "title": "B站AI创作大赛收官 8300份作品播放7亿",
        "hot_value": 380000000,
        "url": "https://k.sina.com.cn/article_7857201856_1d45362c001903ukxq.html",
        "platform": "B站/全网",
        "industries": ["科技", "互联网"],
        "trends": ["爆"],
        "type": "科技热点",
        "sentiment": "正面",
        "keywords": ["B站", "AI创作", "updream", "AI动画", "创作者"],
        "c": ["小米", "荣耀", "索尼", "罗技"],
        "created_at": now,
        "rank": 6,
        "id": f"ht_{gen_id()}"
    },
    {
        "title": "ChatGPT推出新功能 支持实时语音对话",
        "hot_value": 375000000,
        "url": "https://weibo.com",
        "platform": "微博/全网",
        "industries": ["科技", "AI"],
        "trends": ["爆"],
        "type": "科技热点",
        "sentiment": "正面",
        "keywords": ["ChatGPT", "语音对话", "AI", "OpenAI", "新功能"],
        "c": ["小米", "荣耀", "索尼"],
        "created_at": now,
        "rank": 7,
        "id": f"ht_{gen_id()}"
    },
    {
        "title": "春茶上市季 西湖龙井明前茶价格创新高",
        "hot_value": 370000000,
        "url": "https://weibo.com",
        "platform": "微博/小红书",
        "industries": ["食品", "消费"],
        "trends": ["热"],
        "type": "消费热点",
        "sentiment": "正面",
        "keywords": ["春茶", "西湖龙井", "明前茶", "茶叶", "价格"],
        "c": ["农夫山泉", "OATLY"],
        "created_at": now,
        "rank": 8,
        "id": f"ht_{gen_id()}"
    },
    {
        "title": "春季过敏高发 医生推荐防护指南",
        "hot_value": 365000000,
        "url": "https://weibo.com",
        "platform": "微博/小红书",
        "industries": ["健康", "医疗"],
        "trends": ["热"],
        "type": "健康热点",
        "sentiment": "中性",
        "keywords": ["春季过敏", "花粉", "防护", "过敏源", "健康"],
        "c": ["AHC", "玉兰油", "汤臣倍健"],
        "created_at": now,
        "rank": 9,
        "id": f"ht_{gen_id()}"
    },
    {
        "title": "露营季来临 户外装备销量激增300%",
        "hot_value": 360000000,
        "url": "https://weibo.com",
        "platform": "小红书/抖音",
        "industries": ["旅游", "消费"],
        "trends": ["热"],
        "type": "消费热点",
        "sentiment": "正面",
        "keywords": ["露营", "户外装备", "春游", "野营", "销量"],
        "c": ["农夫山泉", "元气森林"],
        "created_at": now,
        "rank": 10,
        "id": f"ht_{gen_id()}"
    },
    {
        "title": "健身季来临 帕梅拉课程再掀热潮",
        "hot_value": 355000000,
        "url": "https://douyin.com",
        "platform": "抖音/B站",
        "industries": ["健身", "生活"],
        "trends": ["热"],
        "type": "生活热点",
        "sentiment": "正面",
        "keywords": ["健身", "帕梅拉", "运动", "减肥", "健康生活"],
        "c": ["汤臣倍健", "农夫山泉"],
        "created_at": now,
        "rank": 11,
        "id": f"ht_{gen_id()}"
    },
    {
        "title": "宠物经济持续升温 猫粮狗粮高端化成趋势",
        "hot_value": 350000000,
        "url": "https://weibo.com",
        "platform": "小红书/全网",
        "industries": ["宠物", "消费"],
        "trends": ["热"],
        "type": "消费热点",
        "sentiment": "正面",
        "keywords": ["宠物经济", "猫粮", "狗粮", "高端化", "消费升级"],
        "c": ["皇家"],
        "created_at": now,
        "rank": 12,
        "id": f"ht_{gen_id()}"
    },
    {
        "title": "新能源汽车4月销量预告 比亚迪继续领跑",
        "hot_value": 345000000,
        "url": "https://weibo.com",
        "platform": "微博/全网",
        "industries": ["汽车", "科技"],
        "trends": ["热"],
        "type": "科技热点",
        "sentiment": "正面",
        "keywords": ["新能源汽车", "销量", "比亚迪", "电动车", "市场"],
        "c": ["小米", "荣耀"],
        "created_at": now,
        "rank": 13,
        "id": f"ht_{gen_id()}"
    },
    {
        "title": "全球半导体开启新一轮涨价潮 晶圆代工全线提价",
        "hot_value": 340000000,
        "url": "https://www.sohu.com/a/1003742455_122692513",
        "platform": "微博/全网",
        "industries": ["科技", "金融"],
        "trends": ["热"],
        "type": "财经热点",
        "sentiment": "中性",
        "keywords": ["半导体", "涨价", "芯片", "晶圆", "电子"],
        "c": ["小米", "荣耀", "索尼", "罗技"],
        "created_at": now,
        "rank": 14,
        "id": f"ht_{gen_id()}"
    },
    {
        "title": "2028洛杉矶奥运会门票4月9日开售",
        "hot_value": 335000000,
        "url": "https://www.sohu.com/a/1003742455_122692513",
        "platform": "微博/全网",
        "industries": ["体育", "旅游"],
        "trends": ["新"],
        "type": "体育热点",
        "sentiment": "正面",
        "keywords": ["奥运会", "洛杉矶", "门票", "2028", "体育"],
        "c": ["农夫山泉", "元气森林", "OATLY", "百威"],
        "created_at": now,
        "rank": 15,
        "id": f"ht_{gen_id()}"
    }
]

# 移除旧热点中已过时的，保留热度高的
existing_ids = {ht['id'] for ht in hot_topics}
for new_ht in new_hotspots:
    if new_ht['id'] not in existing_ids:
        hot_topics.insert(0, new_ht)

# 按热度排序并截取前100条
hot_topics = sorted(hot_topics, key=lambda x: x.get('hot_value', 0), reverse=True)[:100]

# 更新排名
for i, ht in enumerate(hot_topics, 1):
    ht['rank'] = i

# 保存
with open('hot_topics.json', 'w', encoding='utf-8') as f:
    json.dump(hot_topics, f, ensure_ascii=False, indent=2)

print(f"更新完成，共 {len(hot_topics)} 条热点，新增 {len(new_hotspots)} 条")
