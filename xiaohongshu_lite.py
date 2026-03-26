#!/usr/bin/env python3
"""
小红书热点抓取 - 轻量级方案
通过第三方数据源获取小红书热榜
"""

import json
import requests
from datetime import datetime
import re

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15",
    "Accept": "application/json",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

# 9大垂直领域关键词
INDUSTRY_KEYWORDS = {
    "美妆": ["口红", "粉底", "护肤", "妆教", "美妆"],
    "母婴": ["宝宝", "孕妇", "育儿", "辅食", "童装"],
    "数码": ["手机", "耳机", "数码", "笔记本", "智能"],
    "服装": ["穿搭", "衣服", "卫衣", "裙子", "时尚"],
    "食品": ["零食", "美食", "减脂", "咖啡", "奶茶"],
    "汽车": ["汽车", "新能源", "电车", "自驾", "提车"],
    "大健康": ["养生", "体检", "减肥", "健身", "健康"],
    "快消": ["洗发水", "牙膏", "洗衣液", "日用品", "家居"],
    "家电": ["家电", "冰箱", "空调", "扫地机", "智能家电"]
}

def fetch_xiaohongshu_hot_from_weixin():
    """从微信公众号文章获取小红书热榜（第三方聚合）"""
    try:
        # 使用公开的热点聚合接口
        url = "https://api.vvhan.com/api/hotlist/xiaohongshu"
        resp = requests.get(url, headers=headers, timeout=10)
        
        if resp.status_code == 200:
            data = resp.json()
            if data.get('success'):
                items = data.get('data', [])
                result = []
                for i, item in enumerate(items[:30]):
                    result.append({
                        "rank": i + 1,
                        "title": item.get('title', ''),
                        "hot_value": item.get('hot', 0),
                        "url": item.get('url', ''),
                        "platform": "小红书"
                    })
                return {"platform": "小红书", "data": result, "success": True, "source": "聚合API"}
    except Exception as e:
        print(f"聚合API失败: {e}")
    
    return {"platform": "小红书", "data": [], "success": False}

def fetch_from_tophub():
    """从 TopHub 获取小红书热榜"""
    try:
        url = "https://tophub.today/n/KqndgxeLl9.json"  # 小红书热榜
        resp = requests.get(url, headers=headers, timeout=10)
        
        if resp.status_code == 200:
            data = resp.json()
            items = data.get('data', {}).get('list', [])
            result = []
            for i, item in enumerate(items[:30]):
                result.append({
                    "rank": i + 1,
                    "title": item.get('Title', ''),
                    "hot_value": item.get('Extra', {}).get('read', 0),
                    "url": f"https://www.xiaohongshu.com/search_result?keyword={item.get('Title', '')}",
                    "platform": "小红书"
                })
            return {"platform": "小红书", "data": result, "success": True, "source": "TopHub"}
    except Exception as e:
        print(f"TopHub失败: {e}")
    
    return {"platform": "小红书", "data": [], "success": False}

def match_industry(title):
    """匹配行业标签"""
    text = title.lower()
    matched = []
    for industry, keywords in INDUSTRY_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in text:
                if industry not in matched:
                    matched.append(industry)
                break
    return matched

def analyze_xiaohongshu(data):
    """分析小红书数据"""
    industry_hotspots = {k: [] for k in INDUSTRY_KEYWORDS.keys()}
    
    for item in data:
        industries = match_industry(item.get('title', ''))
        item['industries'] = industries
        for ind in industries:
            industry_hotspots[ind].append(item)
    
    return industry_hotspots

def main():
    """主函数"""
    print(f"📱 开始抓取小红书热点... {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 尝试多个数据源
    result = fetch_xiaohongshu_hot_from_weixin()
    
    if not result.get('success'):
        result = fetch_from_tophub()
    
    if result.get('success'):
        items = result.get('data', [])
        print(f"✅ 获取 {len(items)} 条小红书热点")
        
        # 行业分析
        industry_analysis = analyze_xiaohongshu(items)
        
        # 统计
        print("\n📊 行业分布:")
        for industry, hot_items in industry_analysis.items():
            if hot_items:
                print(f"  {industry}: {len(hot_items)} 条")
        
        # 保存报告
        report = {
            "generated_at": datetime.now().isoformat(),
            "source": result.get('source', 'unknown'),
            "hot_list": items,
            "industry_analysis": industry_analysis
        }
        
        output_file = f"/Users/zhangjingwei/.qclaw/workspace/hotspot-tracker/xiaohongshu_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n📁 报告已保存: {output_file}")
        
        return report
    else:
        print("❌ 所有数据源均失败")
        print("💡 建议：使用 Playwright 浏览器自动化方案")
        return None

if __name__ == "__main__":
    main()
