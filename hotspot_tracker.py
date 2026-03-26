#!/usr/bin/env python3
"""
热点追踪器 - 抖音/微博/百度热搜 + 9大垂直行业分析
支持定时执行，输出JSON报告
"""

import json
import requests
from datetime import datetime
from urllib.parse import quote
import re

# 9大垂直领域关键词库
INDUSTRY_KEYWORDS = {
    "美妆": ["美妆", "护肤", "口红", "粉底", "面膜", "化妆", "眼影", "防晒", "精华", "洁面", "医美", "玻尿酸", "彩妆", "卸妆", "遮瑕"],
    "母婴": ["母婴", "宝宝", "奶粉", "纸尿裤", "孕妇", "婴儿", "亲子", "育儿", "备孕", "新生儿", "儿童", "辅食", "玩具", "童装"],
    "数码": ["手机", "电脑", "数码", "iPhone", "华为", "小米", "苹果", "芯片", "显卡", "耳机", "平板", "笔记本", "智能", "AI", "科技", "游戏"],
    "服装": ["穿搭", "服装", "时尚", "衣服", "卫衣", "牛仔裤", "运动鞋", "潮牌", "女装", "男装", "童装", "汉服", "JK", "风衣"],
    "食品": ["食品", "美食", "零食", "饮料", "奶茶", "火锅", "烧烤", "预制菜", "健康食品", "减肥餐", "咖啡", "茶叶", "水果", "生鲜"],
    "汽车": ["汽车", "新能源", "电车", "特斯拉", "比亚迪", "理想", "蔚来", "小鹏", "燃油车", "自驾", "驾照", "汽车用品", "车载"],
    "大健康": ["健康", "养生", "保健品", "维生素", "医疗", "体检", "减肥", "健身", "睡眠", "心理健康", "中医药", "药店", "医院"],
    "快消": ["洗发水", "牙膏", "洗衣液", "纸巾", "沐浴露", "洗面奶", "卫生巾", "湿巾", "清洁", "日用", "日化", "快消"],
    "家电": ["家电", "冰箱", "空调", "洗衣机", "电视", "扫地机", "空气净化器", "净水器", "热水器", "厨房电器", "智能家居"]
}

# 热梗/趋势关键词
TREND_KEYWORDS = ["挑战", "教程", "测评", "开箱", "种草", "避雷", "平替", "黑科技", "神操作", "绝了", "爆款", "必入", "yyds", "真香", "翻车", "踩坑"]

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

def fetch_douyin_hot():
    """抓取抖音热搜榜"""
    try:
        url = "https://www.douyin.com/aweme/v1/hot/search/list/"
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()
        items = data.get('data', {}).get('word_list', [])
        result = []
        for item in items[:50]:
            result.append({
                "rank": len(result) + 1,
                "title": item.get('word', ''),
                "hot_value": item.get('hot_value', 0),
                "url": f"https://www.douyin.com/search/{quote(item.get('word', ''))}"
            })
        return {"platform": "抖音", "data": result, "success": True}
    except Exception as e:
        return {"platform": "抖音", "data": [], "success": False, "error": str(e)}

def fetch_weibo_hot():
    """抓取微博热搜榜"""
    try:
        url = "https://weibo.com/ajax/side/hotSearch"
        headers_weibo = headers.copy()
        headers_weibo["Referer"] = "https://weibo.com/"
        resp = requests.get(url, headers=headers_weibo, timeout=10)
        data = resp.json()
        items = data.get('data', {}).get('realtime', [])
        result = []
        for item in items[:50]:
            word = item.get('word', '').replace('#', '')
            result.append({
                "rank": len(result) + 1,
                "title": word,
                "hot_value": item.get('num', 0),
                "label": item.get('label_name', ''),
                "url": f"https://s.weibo.com/weibo?q={quote(word)}"
            })
        return {"platform": "微博", "data": result, "success": True}
    except Exception as e:
        return {"platform": "微博", "data": [], "success": False, "error": str(e)}

def fetch_baidu_hot():
    """抓取百度热搜榜"""
    try:
        url = "https://top.baidu.com/api/board?platform=wise&tab=realtime"
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()
        cards = data.get('data', {}).get('cards', [])
        items = []
        for card in cards:
            items.extend(card.get('content', []))
        result = []
        for item in items[:50]:
            result.append({
                "rank": len(result) + 1,
                "title": item.get('word', ''),
                "hot_value": item.get('hotScore', 0),
                "desc": item.get('desc', ''),
                "url": item.get('url', f"https://www.baidu.com/s?wd={quote(item.get('word', ''))}")
            })
        return {"platform": "百度", "data": result, "success": True}
    except Exception as e:
        return {"platform": "百度", "data": [], "success": False, "error": str(e)}

def match_industry(title, desc=""):
    """匹配行业标签"""
    text = f"{title} {desc}".lower()
    matched = []
    for industry, keywords in INDUSTRY_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in text:
                if industry not in matched:
                    matched.append(industry)
                break
    return matched

def match_trends(title, desc=""):
    """匹配热梗/趋势标签"""
    text = f"{title} {desc}".lower()
    matched = []
    for trend in TREND_KEYWORDS:
        if trend.lower() in text:
            matched.append(trend)
    return matched

def analyze_hotspots(hot_data_list):
    """分析热点数据，生成行业洞察"""
    all_items = []
    for platform_data in hot_data_list:
        platform = platform_data.get('platform', '')
        for item in platform_data.get('data', []):
            item['platform'] = platform
            item['industries'] = match_industry(item.get('title', ''), item.get('desc', ''))
            item['trends'] = match_trends(item.get('title', ''), item.get('desc', ''))
            all_items.append(item)
    
    # 按行业分类
    industry_hotspots = {k: [] for k in INDUSTRY_KEYWORDS.keys()}
    for item in all_items:
        for ind in item.get('industries', []):
            industry_hotspots[ind].append(item)
    
    # 跨平台热度（同一话题出现在多个平台）
    cross_platform = {}
    for item in all_items:
        title_key = item.get('title', '').replace('#', '').strip()[:10]  # 取前10字作为key
        if title_key not in cross_platform:
            cross_platform[title_key] = {"platforms": [], "total_hot": 0, "title": item.get('title', '')}
        if item.get('platform') not in cross_platform[title_key]["platforms"]:
            cross_platform[title_key]["platforms"].append(item.get('platform'))
        cross_platform[title_key]["total_hot"] += item.get('hot_value', 0)
    
    cross_platform = sorted(cross_platform.values(), key=lambda x: x["total_hot"], reverse=True)[:20]
    
    return {
        "industry_hotspots": industry_hotspots,
        "cross_platform": cross_platform,
        "total_items": len(all_items)
    }

def generate_recommendations(analysis):
    """生成创意建议"""
    recommendations = {}
    
    for industry, items in analysis['industry_hotspots'].items():
        if not items:
            continue
        
        top_items = sorted(items, key=lambda x: x.get('hot_value', 0), reverse=True)[:5]
        trends = set()
        for item in items:
            trends.update(item.get('trends', []))
        
        # 生成建议
        ideas = []
        if trends:
            trends_list = list(trends)[:3]
            ideas.append(f"结合{'/'.join(trends_list)}热点，制作相关内容")
        
        if top_items:
            hot_topic = top_items[0].get('title', '')
            ideas.append(f"蹭热点「{hot_topic}」话题，制作行业相关解读")
            ideas.append(f"找素人KOC测评/开箱相关产品，贴合热点话题")
        
        ideas.append(f"关注竞品动态，及时跟进行业趋势")
        ideas.append(f"挖掘垂类素人爆款，分析其内容结构进行复刻")
        
        recommendations[industry] = {
            "top_hotspots": top_items,
            "trend_tags": list(trends),
            "content_ideas": ideas
        }
    
    return recommendations

def main():
    """主函数"""
    print(f"🔍 开始抓取热点数据... {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 抓取各平台数据
    douyin = fetch_douyin_hot()
    weibo = fetch_weibo_hot()
    baidu = fetch_baidu_hot()
    
    print(f"✅ 抖音: {len(douyin.get('data', []))} 条")
    print(f"✅ 微博: {len(weibo.get('data', []))} 条")
    print(f"✅ 百度: {len(baidu.get('data', []))} 条")
    
    # 分析数据
    print("📊 分析行业关联...")
    analysis = analyze_hotspots([douyin, weibo, baidu])
    
    # 生成建议
    print("💡 生成创意建议...")
    recommendations = generate_recommendations(analysis)
    
    # 生成报告
    report = {
        "generated_at": datetime.now().isoformat(),
        "platforms": {
            "douyin": douyin,
            "weibo": weibo,
            "baidu": baidu
        },
        "analysis": analysis,
        "recommendations": recommendations
    }
    
    # 保存报告
    output_file = f"/Users/zhangjingwei/.qclaw/workspace/hotspot-tracker/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"📁 报告已保存: {output_file}")
    
    return report

if __name__ == "__main__":
    main()
