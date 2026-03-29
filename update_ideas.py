import json
from datetime import datetime

BASE = '/Users/zhangjingwei/.qclaw/workspace/hotspot-tracker'
today = '2026-03-29'
now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

with open(f'{BASE}/client_ideas.json', 'r', encoding='utf-8') as f:
    ideas = json.load(f)

# 生成新选题，基于今日热点
# 热点主题: 陈牧驰陈冰结婚、杨颖咖位话题、金价暴涨、棱镜2033游戏、清明出行、方圆脸妆容等
new_ideas = [
    # 荣耀
    {"id":"3C_202603291323001","client":{"industry":"3C数码","brand":"荣耀","products":["荣耀手机","荣耀平板","荣耀耳机","荣耀手表"],"priority":5},"title":"荣耀手机借势陈牧驰陈冰结婚：明星婚讯情感营销","platform":"小红书","angle":"情感共鸣","hot_topic":"陈牧驰陈冰发文宣布结婚生子","heat":"热搜第一","trend":"爆发式增长","product":"荣耀手机","engagement_estimate":"45230+","status":"pending","created_at":now},
    {"id":"3C_202603291323002","client":{"industry":"3C数码","brand":"荣耀","products":["荣耀手机","荣耀平板","荣耀耳机","荣耀手表"],"priority":5},"title":"荣耀手机借势杨颖咖位话题：明星时尚热度","platform":"微博","angle":"话题讨论","hot_topic":"杨颖咖位降级与韩安冉同框引热议","heat":"3亿+阅读","trend":"爆发式增长","product":"荣耀手机","engagement_estimate":"38910+","status":"pending","created_at":now},
    {"id":"3C_202603291323003","client":{"industry":"3C数码","brand":"荣耀","products":["荣耀手机","荣耀平板","荣耀耳机","荣耀手表"],"priority":5},"title":"荣耀手机借势2026中关村论坛：科技品牌调性","platform":"抖音","angle":"品牌调性","hot_topic":"2026中关村论坛年会北京举行全球关注","heat":"高热","trend":"持续上升","product":"荣耀手机","engagement_estimate":"41870+","status":"pending","created_at":now},
    {"id":"3C_202603291323004","client":{"industry":"3C数码","brand":"荣耀","products":["荣耀折叠屏"],"priority":5},"title":"荣耀折叠屏借势华为Pura X发布：竞品对比话题","platform":"B站","angle":"竞品对比","hot_topic":"华为Pura X发布鸿蒙系统新机","heat":"高热","trend":"爆发式增长","product":"荣耀折叠屏","engagement_estimate":"35620+","status":"pending","created_at":now},
    {"id":"3C_202603291323005","client":{"industry":"3C数码","brand":"荣耀","products":["荣耀平板"],"priority":5},"title":"荣耀平板借势棱镜2033游戏爆火：娱乐场景种草","platform":"B站","angle":"场景种草","hot_topic":"B站棱镜2033游戏实机展示爆火387万播放","heat":"387.5万+","trend":"爆发式增长","product":"荣耀平板","engagement_estimate":"29450+","status":"pending","created_at":now},

    # 罗技
    {"id":"3C_202603291323006","client":{"industry":"3C数码","brand":"罗技","products":["罗技键鼠","罗技摄像头","罗技音箱"],"priority":4},"title":"罗技键鼠借势棱镜2033游戏实机展示：游戏装备测评","platform":"B站","angle":"游戏测评","hot_topic":"B站棱镜2033游戏实机展示爆火387万播放","heat":"387.5万+","trend":"爆发式增长","product":"罗技键鼠","engagement_estimate":"38230+","status":"pending","created_at":now},
    {"id":"3C_202603291323007","client":{"industry":"3C数码","brand":"罗技","products":["罗技键鼠","罗技摄像头","罗技音箱"],"priority":4},"title":"罗技音箱借势2026中关村论坛：科技品牌联动","platform":"微博","angle":"品牌联动","hot_topic":"2026中关村论坛年会北京举行全球关注","heat":"高热","trend":"持续上升","product":"罗技音箱","engagement_estimate":"29580+","status":"pending","created_at":now},
    {"id":"3C_202603291323008","client":{"industry":"3C数码","brand":"罗技","products":["罗技键鼠","罗技摄像头","罗技音箱"],"priority":4},"title":"罗技摄像头借势哪吒2票房160亿：影视周边场景","platform":"小红书","angle":"场景种草","hot_topic":"哪吒2票房突破160亿持续领跑全球","heat":"高热","trend":"持续上升","product":"罗技摄像头","engagement_estimate":"26740+","status":"pending","created_at":now},
    {"id":"3C_202603291323009","client":{"industry":"3C数码","brand":"罗技","products":["罗技键鼠","罗技摄像头","罗技音箱"],"priority":4},"title":"罗技键鼠借势全球最懒国家假期话题：生活态度","platform":"抖音","angle":"生活态度","hot_topic":"全球最懒国家一年200天假期","heat":"255.4万+","trend":"快速上升","product":"罗技键鼠","engagement_estimate":"21860+","status":"pending","created_at":now},

    # 小米
    {"id":"3C_202603291323010","client":{"industry":"3C数码","brand":"小米","products":["小米手机","小米平板","小米智能家居"],"priority":5},"title":"小米手机借势国际金价暴涨：黄金投资话题情感内容","platform":"微博","angle":"情感共鸣","hot_topic":"国际金价暴涨4495美元创历史新高","heat":"高热","trend":"爆发式增长","product":"小米手机","engagement_estimate":"43170+","status":"pending","created_at":now},
    {"id":"3C_202603291323011","client":{"industry":"3C数码","brand":"小米","products":["小米手机","小米平板","小米智能家居"],"priority":5},"title":"小米手机借势陈牧驰陈冰结婚：明星婚讯热点借势","platform":"小红书","angle":"热点借势","hot_topic":"陈牧驰陈冰发文宣布结婚生子","heat":"热搜第一","trend":"爆发式增长","product":"小米手机","engagement_estimate":"38420+","status":"pending","created_at":now},
    {"id":"3C_202603291323012","client":{"industry":"3C数码","brand":"小米","products":["小米手机","小米平板","小米智能家居"],"priority":5},"title":"小米智能家居借势2026中关村论坛：科技创新","platform":"抖音","angle":"科技前沿","hot_topic":"2026中关村论坛年会北京举行全球关注","heat":"高热","trend":"持续上升","product":"小米智能家居","engagement_estimate":"35680+","status":"pending","created_at":now},
    {"id":"3C_202603291323013","client":{"industry":"3C数码","brand":"小米","products":["小米手机","小米平板","小米智能家居"],"priority":5},"title":"小米手机借势小红书封禁AI托管：真实内容价值话题","platform":"小红书","angle":"价值主张","hot_topic":"小红书全面封禁AI托管账号治理内容","heat":"高热","trend":"快速上升","product":"小米手机","engagement_estimate":"31240+","status":"pending","created_at":now},
    {"id":"3C_202603291323014","client":{"industry":"3C数码","brand":"小米","products":["小米手机","小米平板","小米智能家居"],"priority":5},"title":"小米手机借势清明出行高峰：节日场景营销","platform":"微博","angle":"节日营销","hot_topic":"清明假期临近贵阳加开多趟列车","heat":"高热","trend":"持续上升","product":"小米手机","engagement_estimate":"28950+","status":"pending","created_at":now},

    # 索尼
    {"id":"3C_202603291323015","client":{"industry":"3C数码","brand":"索尼","products":["索尼耳机","索尼相机","索尼电视"],"priority":4},"title":"索尼相机借势哪吒2票房160亿：国产动画热度","platform":"微博","angle":"话题借势","hot_topic":"哪吒2票房突破160亿持续领跑全球","heat":"高热","trend":"持续上升","product":"索尼相机","engagement_estimate":"42780+","status":"pending","created_at":now},
    {"id":"3C_202603291323016","client":{"industry":"3C数码","brand":"索尼","products":["索尼耳机","索尼相机","索尼电视"],"priority":4},"title":"索尼耳机借势杨颖咖位话题：明星同款时尚","platform":"抖音","angle":"明星同款","hot_topic":"杨颖咖位降级与韩安冉同框引热议","heat":"3亿+阅读","trend":"爆发式增长","product":"索尼耳机","engagement_estimate":"35890+","status":"pending","created_at":now},
    {"id":"3C_202603291323017","client":{"industry":"3C数码","brand":"索尼","products":["索尼耳机","索尼相机","索尼电视"],"priority":4},"title":"索尼相机借势棱镜2033游戏实机展示：游戏记录装备","platform":"B站","angle":"场景种草","hot_topic":"B站棱镜2033游戏实机展示爆火387万播放","heat":"387.5万+","trend":"爆发式增长","product":"索尼相机","engagement_estimate":"29640+","status":"pending","created_at":now},
    {"id":"3C_202603291323018","client":{"industry":"3C数码","brand":"索尼","products":["索尼耳机","索尼相机","索尼电视"],"priority":4},"title":"索尼耳机借势全球最懒国家话题：生活态度","platform":"小红书","angle":"生活态度","hot_topic":"全球最懒国家一年200天假期","heat":"255.4万+","trend":"快速上升","product":"索尼耳机","engagement_estimate":"23450+","status":"pending","created_at":now},

    # AHC
    {"id":"KC_202603291323019","client":{"industry":"快消","brand":"AHC","products":["AHC水乳","AHC防晒","AHC眼霜"],"priority":5},"title":"AHC水乳借势张子萱少女感翻车：反容貌焦虑","platform":"小红书","angle":"情感共鸣","hot_topic":"张子萱硬凹少女感翻车遭网友抵制","heat":"2亿+阅读","trend":"爆发式增长","product":"AHC水乳","engagement_estimate":"51230+","status":"pending","created_at":now},
    {"id":"KC_202603291323020","client":{"industry":"快消","brand":"AHC","products":["AHC水乳","AHC防晒","AHC眼霜"],"priority":5},"title":"AHC防晒借势杨颖咖位话题：明星生图护肤","platform":"抖音","angle":"明星同款","hot_topic":"杨颖咖位降级与韩安冉同框引热议","heat":"3亿+阅读","trend":"爆发式增长","product":"AHC防晒","engagement_estimate":"47890+","status":"pending","created_at":now},
    {"id":"KC_202603291323021","client":{"industry":"快消","brand":"AHC","products":["AHC水乳","AHC防晒","AHC眼霜"],"priority":5},"title":"AHC眼霜借势方圆脸妆容刷屏：精准护肤痛点","platform":"小红书","angle":"痛点解决","hot_topic":"小红书方圆脸妆容教程持续刷屏","heat":"57万+","trend":"持续上升","product":"AHC眼霜","engagement_estimate":"39620+","status":"pending","created_at":now},
    {"id":"KC_202603291323022","client":{"industry":"快消","brand":"AHC","products":["AHC水乳","AHC防晒","AHC眼霜"],"priority":5},"title":"AHC水乳借势陈牧驰陈冰结婚：明星婚讯护肤话题","platform":"微博","angle":"热点借势","hot_topic":"陈牧驰陈冰发文宣布结婚生子","heat":"热搜第一","trend":"爆发式增长","product":"AHC水乳","engagement_estimate":"35240+","status":"pending","created_at":now},
    {"id":"KC_202603291323023","client":{"industry":"快消","brand":"AHC","products":["AHC水乳","AHC防晒","AHC眼霜"],"priority":5},"title":"AHC防晒借势清明踏青出游：季节场景营销","platform":"小红书","angle":"场景种草","hot_topic":"清明踏青好去处","heat":"3560万","trend":"爆发式增长","product":"AHC防晒","engagement_estimate":"28970+","status":"pending","created_at":now},

    # 多芬
    {"id":"KC_202603291323024","client":{"industry":"快消","brand":"多芬","products":["多芬沐浴露","多芬洗发水","多芬身体乳"],"priority":4},"title":"多芬沐浴露借势张子萱少女感翻车：真实美","platform":"小红书","angle":"真实美","hot_topic":"张子萱硬凹少女感翻车遭网友抵制","heat":"2亿+阅读","trend":"爆发式增长","product":"多芬沐浴露","engagement_estimate":"48760+","status":"pending","created_at":now},
    {"id":"KC_202603291323025","client":{"industry":"快消","brand":"多芬","products":["多芬沐浴露","多芬洗发水","多芬身体乳"],"priority":4},"title":"多芬洗发水借势方圆脸妆容教程：头部护理联动","platform":"抖音","angle":"场景种草","hot_topic":"小红书方圆脸妆容教程持续刷屏","heat":"57万+","trend":"持续上升","product":"多芬洗发水","engagement_estimate":"31840+","status":"pending","created_at":now},
    {"id":"KC_202603291323026","client":{"industry":"快消","brand":"多芬","products":["多芬沐浴露","多芬洗发水","多芬身体乳"],"priority":4},"title":"多芬身体乳借势春季过敏护肤热潮：季节护肤","platform":"微博","angle":"季节营销","hot_topic":"春季过敏护肤指南","heat":"2100万","trend":"爆发式增长","product":"多芬身体乳","engagement_estimate":"27450+","status":"pending","created_at":now},
    {"id":"KC_202603291323027","client":{"industry":"快消","brand":"多芬","products":["多芬沐浴露","多芬洗发水","多芬身体乳"],"priority":4},"title":"多芬沐浴露借势杨颖咖位话题：自信美丽","platform":"小红书","angle":"价值主张","hot_topic":"杨颖咖位降级与韩安冉同框引热议","heat":"3亿+阅读","trend":"爆发式增长","product":"多芬沐浴露","engagement_estimate":"36520+","status":"pending","created_at":now},

    # 力士
    {"id":"KC_202603291323028","client":{"industry":"快消","brand":"力士","products":["力士洗发水","力士沐浴露","力士香皂"],"priority":4},"title":"力士香皂借势张子萱少女感翻车：真实自信","platform":"微博","angle":"真实自信","hot_topic":"张子萱硬凹少女感翻车遭网友抵制","heat":"2亿+阅读","trend":"爆发式增长","product":"力士香皂","engagement_estimate":"42680+","status":"pending","created_at":now},
    {"id":"KC_202603291323029","client":{"industry":"快消","brand":"力士","products":["力士洗发水","力士沐浴露","力士香皂"],"priority":4},"title":"力士洗发水借势方圆脸妆容教程：护发美妆联动","platform":"小红书","angle":"美妆联动","hot_topic":"小红书方圆脸妆容教程持续刷屏","heat":"57万+","trend":"持续上升","product":"力士洗发水","engagement_estimate":"28940+","status":"pending","created_at":now},
    {"id":"KC_202603291323030","client":{"industry":"快消","brand":"力士","products":["力士洗发水","力士沐浴露","力士香皂"],"priority":4},"title":"力士香皂借势陈牧驰陈冰结婚：婚讯护肤话题","platform":"抖音","angle":"热点借势","hot_topic":"陈牧驰陈冰发文宣布结婚生子","heat":"热搜第一","trend":"爆发式增长","product":"力士香皂","engagement_estimate":"31580+","status":"pending","created_at":now},
    {"id":"KC_202603291323031","client":{"industry":"快消","brand":"力士","products":["力士洗发水","力士沐浴露","力士香皂"],"priority":4},"title":"力士沐浴露借势清明踏青：户外便携护肤","platform":"小红书","angle":"场景种草","hot_topic":"清明踏青好去处","heat":"3560万","trend":"爆发式增长","product":"力士沐浴露","engagement_estimate":"25740+","status":"pending","created_at":now},

    # 清扬
    {"id":"KC_202603291323032","client":{"industry":"快消","brand":"清扬","products":["清扬洗发水","清扬去屑套装"],"priority":3},"title":"清扬洗发水借势方圆脸妆容刷屏：头皮护理联动","platform":"小红书","angle":"美妆联动","hot_topic":"小红书方圆脸妆容教程持续刷屏","heat":"57万+","trend":"持续上升","product":"清扬洗发水","engagement_estimate":"24680+","status":"pending","created_at":now},
    {"id":"KC_202603291323033","client":{"industry":"快消","brand":"清扬","products":["清扬洗发水","清扬去屑套装"],"priority":3},"title":"清扬去屑套装借势清明踏青：户外头皮清爽","platform":"抖音","angle":"场景营销","hot_topic":"清明踏青好去处","heat":"3560万","trend":"爆发式增长","product":"清扬去屑套装","engagement_estimate":"21350+","status":"pending","created_at":now},
    {"id":"KC_202603291323034","client":{"industry":"快消","brand":"清扬","products":["清扬洗发水","清扬去屑套装"],"priority":3},"title":"清扬洗发水借势杨颖咖位话题：真实自我","platform":"微博","angle":"价值主张","hot_topic":"杨颖咖位降级与韩安冉同框引热议","heat":"3亿+阅读","trend":"爆发式增长","product":"清扬洗发水","engagement_estimate":"27490+","status":"pending","created_at":now},

    # 玉兰油
    {"id":"KC_202603291323035","client":{"industry":"快消","brand":"玉兰油","products":["玉兰油面霜","玉兰油精华","玉兰油防晒"],"priority":4},"title":"玉兰油精华借势张子萱少女感翻车：反年龄焦虑","platform":"小红书","angle":"反焦虑","hot_topic":"张子萱硬凹少女感翻车遭网友抵制","heat":"2亿+阅读","trend":"爆发式增长","product":"玉兰油精华","engagement_estimate":"49230+","status":"pending","created_at":now},
    {"id":"KC_202603291323036","client":{"industry":"快消","brand":"玉兰油","products":["玉兰油面霜","玉兰油精华","玉兰油防晒"],"priority":4},"title":"玉兰油防晒借势杨颖咖位话题：明星同款护肤","platform":"抖音","angle":"明星同款","hot_topic":"杨颖咖位降级与韩安冉同框引热议","heat":"3亿+阅读","trend":"爆发式增长","product":"玉兰油防晒","engagement_estimate":"43870+","status":"pending","created_at":now},
    {"id":"KC_202603291323037","client":{"industry":"快消","brand":"玉兰油","products":["玉兰油面霜","玉兰油精华","玉兰油防晒"],"priority":4},"title":"玉兰油面霜借势方圆脸妆容教程：精准护肤","platform":"小红书","angle":"痛点解决","hot_topic":"小红书方圆脸妆容教程持续刷屏","heat":"57万+","trend":"持续上升","product":"玉兰油面霜","engagement_estimate":"35780+","status":"pending","created_at":now},
    {"id":"KC_202603291323038","client":{"industry":"快消","brand":"玉兰油","products":["玉兰油面霜","玉兰油精华","玉兰油防晒"],"priority":4},"title":"玉兰油精华借势陈牧驰陈冰结婚：明星婚讯护肤","platform":"微博","angle":"热点借势","hot_topic":"陈牧驰陈冰发文宣布结婚生子","heat":"热搜第一","trend":"爆发式增长","product":"玉兰油精华","engagement_estimate":"31540+","status":"pending","created_at":now},
    {"id":"KC_202603291323039","client":{"industry":"快消","brand":"玉兰油","products":["玉兰油面霜","玉兰油精华","玉兰油防晒"],"priority":4},"title":"玉兰油防晒借势清明踏青：户外防护","platform":"小红书","angle":"场景营销","hot_topic":"清明踏青好去处","heat":"3560万","trend":"爆发式增长","product":"玉兰油防晒","engagement_estimate":"27890+","status":"pending","created_at":now},

    # 汤臣倍健
    {"id":"BJ_202603291323040","client":{"industry":"保健品","brand":"汤臣倍健","products":["蛋白粉","维生素","鱼油","益生菌"],"priority":5},"title":"汤臣倍健维生素借势儿童长高指南：季节营养","platform":"抖音","angle":"健康科普","hot_topic":"儿童春季长高指南","heat":"1560万","trend":"爆发式增长","product":"维生素","engagement_estimate":"38420+","status":"pending","created_at":now},
    {"id":"BJ_202603291323041","client":{"industry":"保健品","brand":"汤臣倍健","products":["蛋白粉","维生素","鱼油","益生菌"],"priority":5},"title":"汤臣倍健蛋白粉借势春季减脂热潮：运动营养","platform":"微博","angle":"健身联动","hot_topic":"春季减脂计划","heat":"3200万","trend":"持续上升","product":"蛋白粉","engagement_estimate":"42680+","status":"pending","created_at":now},
    {"id":"BJ_202603291323042","client":{"industry":"保健品","brand":"汤臣倍健","products":["蛋白粉","维生素","鱼油","益生菌"],"priority":5},"title":"汤臣倍健鱼油借势全球最懒国家话题：主动健康管理","platform":"小红书","angle":"价值主张","hot_topic":"全球最懒国家一年200天假期","heat":"255.4万+","trend":"快速上升","product":"鱼油","engagement_estimate":"28930+","status":"pending","created_at":now},
    {"id":"BJ_202603291323043","client":{"industry":"保健品","brand":"汤臣倍健","products":["蛋白粉","维生素","鱼油","益生菌"],"priority":5},"title":"汤臣倍健益生菌借势清明假期：旅途肠胃健康","platform":"微博","angle":"场景营销","hot_topic":"清明假期临近贵阳加开多趟列车","heat":"高热","trend":"持续上升","product":"益生菌","engagement_estimate":"24370+","status":"pending","created_at":now},

    # 善存
    {"id":"BJ_202603291323044","client":{"industry":"保健品","brand":"善存","products":["善存多维片","善存银片"],"priority":3},"title":"善存多维片借势儿童长高指南：家庭营养","platform":"小红书","angle":"家庭健康","hot_topic":"儿童春季长高指南","heat":"1560万","trend":"爆发式增长","product":"善存多维片","engagement_estimate":"31840+","status":"pending","created_at":now},
    {"id":"BJ_202603291323045","client":{"industry":"保健品","brand":"善存","products":["善存多维片","善存银片"],"priority":3},"title":"善存银片借势春季减脂热潮：多元营养支持","platform":"抖音","angle":"健身联动","hot_topic":"春季减脂计划","heat":"3200万","trend":"持续上升","product":"善存银片","engagement_estimate":"27450+","status":"pending","created_at":now},
    {"id":"BJ_202603291323046","client":{"industry":"保健品","brand":"善存","products":["善存多维片","善存银片"],"priority":3},"title":"善存多维片借势陈牧驰陈冰结婚：备孕健康","platform":"微博","angle":"场景营销","hot_topic":"陈牧驰陈冰发文宣布结婚生子","heat":"热搜第一","trend":"爆发式增长","product":"善存多维片","engagement_estimate":"23890+","status":"pending","created_at":now},

    # HC
    {"id":"HK_202603291323047","client":{"industry":"家庭清洁","brand":"HC","products":["HC清洁剂","HC消毒液"],"priority":3},"title":"HC清洁剂借势回南天除湿刷屏：梅雨季家居防护","platform":"B站","angle":"痛点解决","hot_topic":"回南天除湿攻略全网刷屏","heat":"110万+","trend":"持续上升","product":"HC清洁剂","engagement_estimate":"35670+","status":"pending","created_at":now},
    {"id":"HK_202603291323048","client":{"industry":"家庭清洁","brand":"HC","products":["HC清洁剂","HC消毒液"],"priority":3},"title":"HC消毒液借势清明踏青：户外清洁防护","platform":"小红书","angle":"场景营销","hot_topic":"清明踏青好去处","heat":"3560万","trend":"爆发式增长","product":"HC消毒液","engagement_estimate":"21380+","status":"pending","created_at":now},
    {"id":"HK_202603291323049","client":{"industry":"家庭清洁","brand":"HC","products":["HC清洁剂","HC消毒液"],"priority":3},"title":"HC清洁剂借势国际金价暴涨：珠宝清洁保养","platform":"抖音","angle":"场景种草","hot_topic":"国际金价暴涨4495美元创历史新高","heat":"高热","trend":"爆发式增长","product":"HC清洁剂","engagement_estimate":"18290+","status":"pending","created_at":now},

    # 威猛先生
    {"id":"HK_202603291323050","client":{"industry":"家庭清洁","brand":"威猛先生","products":["威猛先生厨房清洁","威猛先生浴室清洁"],"priority":3},"title":"威猛先生厨房清洁借势回南天：厨房防潮攻略","platform":"抖音","angle":"痛点解决","hot_topic":"回南天除湿攻略全网刷屏","heat":"110万+","trend":"持续上升","product":"威猛先生厨房清洁","engagement_estimate":"32640+","status":"pending","created_at":now},
    {"id":"HK_202603291323051","client":{"industry":"家庭清洁","brand":"威猛先生","products":["威猛先生厨房清洁","威猛先生浴室清洁"],"priority":3},"title":"威猛先生浴室清洁借势清明大扫除：春季清洁","platform":"小红书","angle":"季节营销","hot_topic":"清明踏青好去处","heat":"3560万","trend":"爆发式增长","product":"威猛先生浴室清洁","engagement_estimate":"24870+","status":"pending","created_at":now},
    {"id":"HK_202603291323052","client":{"industry":"家庭清洁","brand":"威猛先生","products":["威猛先生厨房清洁","威猛先生浴室清洁"],"priority":3},"title":"威猛先生厨房清洁借势国际金价暴涨：金银首饰清洁","platform":"微博","angle":"场景种草","hot_topic":"国际金价暴涨4495美元创历史新高","heat":"高热","trend":"爆发式增长","product":"威猛先生厨房清洁","engagement_estimate":"19430+","status":"pending","created_at":now},

    # 舒适
    {"id":"KC_202603291323053","client":{"industry":"快消","brand":"舒适","products":["舒适洗衣液","舒适柔顺剂"],"priority":3},"title":"舒适洗衣液借势回南天：衣物防潮除味","platform":"小红书","angle":"痛点解决","hot_topic":"回南天除湿攻略全网刷屏","heat":"110万+","trend":"持续上升","product":"舒适洗衣液","engagement_estimate":"28750+","status":"pending","created_at":now},
    {"id":"KC_202603291323054","client":{"industry":"快消","brand":"舒适","products":["舒适洗衣液","舒适柔顺剂"],"priority":3},"title":"舒适柔顺剂借势清明踏青：户外衣物护理","platform":"抖音","angle":"场景营销","hot_topic":"清明踏青好去处","heat":"3560万","trend":"爆发式增长","product":"舒适柔顺剂","engagement_estimate":"21980+","status":"pending","created_at":now},
    {"id":"KC_202603291323055","client":{"industry":"快消","brand":"舒适","products":["舒适洗衣液","舒适柔顺剂"],"priority":3},"title":"舒适洗衣液借势全球最懒国家话题：轻松生活","platform":"微博","angle":"生活态度","hot_topic":"全球最懒国家一年200天假期","heat":"255.4万+","trend":"快速上升","product":"舒适洗衣液","engagement_estimate":"16470+","status":"pending","created_at":now},

    # 希宝
    {"id":"CW_202603291323056","client":{"industry":"宠物食品","brand":"希宝","products":["猫粮","狗粮","宠物零食"],"priority":4},"title":"希宝猫粮借势宠物用品红黑榜：消费者决策","platform":"小红书","angle":"消费决策","hot_topic":"宠物用品红黑榜成消费热点","heat":"547万+","trend":"持续上升","product":"猫粮","engagement_estimate":"29870+","status":"pending","created_at":now},
    {"id":"CW_202603291323057","client":{"industry":"宠物食品","brand":"希宝","products":["猫粮","狗粮","宠物零食"],"priority":4},"title":"希宝狗粮借势清明踏青：携宠出行场景","platform":"抖音","angle":"场景营销","hot_topic":"清明踏青好去处","heat":"3560万","trend":"爆发式增长","product":"狗粮","engagement_estimate":"23640+","status":"pending","created_at":now},
    {"id":"CW_202603291323058","client":{"industry":"宠物食品","brand":"希宝","products":["猫粮","狗粮","宠物零食"],"priority":4},"title":"希宝宠物零食借势猫咪春日护理攻略：季节关爱","platform":"小红书","angle":"季节营销","hot_topic":"猫咪春日护理攻略","heat":"1150万","trend":"持续上升","product":"宠物零食","engagement_estimate":"18420+","status":"pending","created_at":now},

    # 皇家
    {"id":"CW_202603291323059","client":{"industry":"宠物食品","brand":"皇家","products":["皇家猫粮","皇家狗粮","皇家处方粮"],"priority":4},"title":"皇家猫粮借势宠物用品红黑榜：品质认证","platform":"微博","angle":"品质背书","hot_topic":"宠物用品红黑榜成消费热点","heat":"547万+","trend":"持续上升","product":"皇家猫粮","engagement_estimate":"31560+","status":"pending","created_at":now},
    {"id":"CW_202603291323060","client":{"industry":"宠物食品","brand":"皇家","products":["皇家猫粮","皇家狗粮","皇家处方粮"],"priority":4},"title":"皇家狗粮借势清明携宠出行：户外宠物营养","platform":"小红书","angle":"场景营销","hot_topic":"清明踏青好去处","heat":"3560万","trend":"爆发式增长","product":"皇家狗粮","engagement_estimate":"24780+","status":"pending","created_at":now},
    {"id":"CW_202603291323061","client":{"industry":"宠物食品","brand":"皇家","products":["皇家猫粮","皇家狗粮","皇家处方粮"],"priority":4},"title":"皇家处方粮借势猫咪春日护理攻略：专业护理","platform":"抖音","angle":"专业科普","hot_topic":"猫咪春日护理攻略","heat":"1150万","trend":"持续上升","product":"皇家处方粮","engagement_estimate":"19340+","status":"pending","created_at":now},

    # OATLY
    {"id":"YL_202603291323062","client":{"industry":"食品饮料","brand":"OATLY","products":["燕麦奶","咖啡燕麦奶","燕麦冰淇淋"],"priority":4},"title":"OATLY燕麦奶借势清明踏青：户外健康饮品","platform":"小红书","angle":"场景营销","hot_topic":"清明踏青好去处","heat":"3560万","trend":"爆发式增长","product":"燕麦奶","engagement_estimate":"32640+","status":"pending","created_at":now},
    {"id":"YL_202603291323063","client":{"industry":"食品饮料","brand":"OATLY","products":["燕麦奶","咖啡燕麦奶","燕麦冰淇淋"],"priority":4},"title":"OATLY咖啡燕麦奶借势棱镜2033游戏：游戏搭档饮品","platform":"B站","angle":"场景种草","hot_topic":"B站棱镜2033游戏实机展示爆火387万播放","heat":"387.5万+","trend":"爆发式增长","product":"咖啡燕麦奶","engagement_estimate":"25870+","status":"pending","created_at":now},
    {"id":"YL_202603291323064","client":{"industry":"食品饮料","brand":"OATLY","products":["燕麦奶","咖啡燕麦奶","燕麦冰淇淋"],"priority":4},"title":"OATLY燕麦冰淇淋借势全球最懒国家话题：轻松享瘦","platform":"抖音","angle":"生活态度","hot_topic":"全球最懒国家一年200天假期","heat":"255.4万+","trend":"快速上升","product":"燕麦冰淇淋","engagement_estimate":"19750+","status":"pending","created_at":now},
    {"id":"YL_202603291323065","client":{"industry":"食品饮料","brand":"OATLY","products":["燕麦奶","咖啡燕麦奶","燕麦冰淇淋"],"priority":4},"title":"OATLY燕麦奶借势2026中关村论坛：科技与生活融合","platform":"微博","angle":"品牌调性","hot_topic":"2026中关村论坛年会北京举行全球关注","heat":"高热","trend":"持续上升","product":"燕麦奶","engagement_estimate":"23480+","status":"pending","created_at":now},

    # 百威
    {"id":"YL_202603291323066","client":{"industry":"食品饮料","brand":"百威","products":["百威啤酒","百威纯生","百威超级"],"priority":3},"title":"百威啤酒借势清明踏青：户外聚会搭档","platform":"小红书","angle":"场景营销","hot_topic":"清明踏青好去处","heat":"3560万","trend":"爆发式增长","product":"百威啤酒","engagement_estimate":"28760+","status":"pending","created_at":now},
    {"id":"YL_202603291323067","client":{"industry":"食品饮料","brand":"百威","products":["百威啤酒","百威纯生","百威超级"],"priority":3},"title":"百威纯生借势陈牧驰陈冰结婚：明星婚宴用酒话题","platform":"微博","angle":"热点借势","hot_topic":"陈牧驰陈冰发文宣布结婚生子","heat":"热搜第一","