#!/usr/bin/env python3
"""
修复热点数据缺失字段脚本
- 添加 platforms 数组字段
- 添加 heat 格式化热度字段
- 添加 isNew 新增热点标记
- 增强 logic 逻辑分析字段
- 增强 trend 趋势标记字段
"""
import json
from datetime import datetime
from pathlib import Path

# 项目路径
PROJECT_DIR = Path("/Users/zhangjingwei/.qclaw/workspace/hotspot-tracker")
HOT_TOPICS_FILE = PROJECT_DIR / "hot_topics.json"
HISTORY_FILE = PROJECT_DIR / "hotspot_history.json"

def format_heat(hot_value):
    """格式化热度值为人类可读格式"""
    if hot_value >= 100000000:  # 1亿
        return f"{hot_value / 100000000:.1f}亿"
    elif hot_value >= 10000000:  # 1000万
        return f"{hot_value / 10000000:.0f}万"
    elif hot_value >= 1000000:  # 100万
        return f"{hot_value / 1000000:.0f}万"
    elif hot_value >= 10000:  # 1万
        return f"{hot_value / 10000:.0f}万"
    else:
        return str(hot_value)

def parse_platforms(platform_str):
    """将平台字符串解析为数组"""
    if not platform_str:
        return []
    # 处理多种分隔符：/、|、、
    platforms = []
    for sep in ["/", "|", "，", ","]:
        if sep in platform_str:
            platforms = [p.strip() for p in platform_str.split(sep) if p.strip()]
            break
    if not platforms:
        platforms = [platform_str.strip()]
    return platforms

def generate_logic(topic, clients):
    """生成逻辑分析字段"""
    title = topic.get("title", "")
    industries = topic.get("industries", [])
    keywords = topic.get("keywords", [])
    
    # 根据行业和关键词生成逻辑分析
    logic_templates = {
        "旅游": "假日经济效应显著，出行/文旅消费场景丰富，适合饮料、休闲食品品牌植入",
        "交通": "出行场景刚需，适合功能饮料、快消品牌场景营销",
        "美妆": "换季护肤/妆容需求旺盛，美妆品牌可借势种草推广",
        "健康": "健康意识提升，保健品/功能食品品牌可切入养生话题",
        "科技": "科技热点关注度高，数码品牌可借势产品推广",
        "娱乐": "娱乐话题热度高，适合饮料/零食品牌娱乐营销",
        "美食": "美食话题自带流量，食品饮料品牌可直接借势",
        "家居": "家居生活方式升级，家电/清洁品牌可切入场景",
        "宠物": "宠物经济持续升温，宠物食品品牌机会明显",
        "健身": "运动健身热潮，功能饮料/保健品品牌契合",
        "汽车": "汽车出行话题，新能源/科技品牌可借势",
        "电影": "档期票房效应，饮料/零食品牌观影场景营销",
    }
    
    # 匹配行业逻辑
    for industry in industries:
        if industry in logic_templates:
            return logic_templates[industry]
    
    # 关键词匹配
    for kw in keywords:
        if kw in ["清明", "假期", "返程", "出行"]:
            return "假日出行高峰，适合饮料/快消品牌场景营销"
        if kw in ["春季", "换季", "护肤"]:
            return "换季护肤刚需，美妆个护品牌种草窗口"
        if kw in ["AI", "科技", "智能"]:
            return "科技热点关注度高，数码品牌可借势推广"
    
    # 默认逻辑
    return "热点话题传播度高，可根据品牌定位选择借势角度"

def generate_trend(topic, history_data):
    """生成趋势标记"""
    title = topic.get("title", "")
    current_value = topic.get("hot_value", 0)
    trends = topic.get("trends", [])
    
    # 检查是否有历史数据
    if title in history_data:
        prev_value = history_data[title].get("hot_value", 0)
        if current_value > prev_value * 1.2:
            return "🔥🔥🔥 持续上升"
        elif current_value > prev_value * 1.05:
            return "🔥🔥 稳定上升"
        elif current_value < prev_value * 0.8:
            return "📉 明显下降"
        elif current_value < prev_value * 0.95:
            return "🔥 下降"
        else:
            return "🔥🔥 稳定"
    
    # 无历史数据时，根据趋势标签判断
    if "爆" in trends:
        return "🔥🔥🔥 爆发式增长"
    if "新" in trends:
        return "🔥🔥🔥 新晋热点"
    if "热" in trends:
        return "🔥🔥🔥 持续上升"
    
    # 根据热度值判断
    if current_value > 500000000:
        return "🔥🔥🔥 爆发式增长"
    elif current_value > 100000000:
        return "🔥🔥🔥 持续上升"
    else:
        return "🔥🔥 稳定"

def check_is_new(topic, history_data):
    """判断是否为新增热点"""
    title = topic.get("title", "")
    created_at = topic.get("created_at", "")
    
    # 如果标题不在历史数据中，则为新热点
    if title not in history_data:
        return True
    
    # 如果创建时间在今天附近（24小时内），也算新
    if created_at:
        try:
            created_dt = datetime.fromisoformat(created_at.replace("Z", ""))
            now = datetime.now()
            hours_diff = (now - created_dt).total_seconds() / 3600
            if hours_diff < 24:
                return True
        except:
            pass
    
    return False

def main():
    print("=" * 50)
    print("热点数据字段修复脚本")
    print("=" * 50)
    
    # 加载热点数据
    with open(HOT_TOPICS_FILE, "r", encoding="utf-8") as f:
        hot_topics = json.load(f)
    
    print(f"加载热点数量: {len(hot_topics)}")
    
    # 加载历史数据
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history_data = json.load(f)
    except:
        history_data = {}
    print(f"历史数据条数: {len(history_data)}")
    
    # 修复每个热点
    fixed_count = 0
    for topic in hot_topics:
        # 1. 添加 platforms 数组
        if "platforms" not in topic or not topic["platforms"]:
            topic["platforms"] = parse_platforms(topic.get("platform", ""))
            fixed_count += 1
        
        # 2. 添加 heat 格式化热度
        if "heat" not in topic or not topic["heat"]:
            topic["heat"] = format_heat(topic.get("hot_value", 0))
            fixed_count += 1
        
        # 3. 添加 isNew 标记
        if "isNew" not in topic:
            topic["isNew"] = check_is_new(topic, history_data)
            fixed_count += 1
        
        # 4. 增强 logic 字段（如果为空或太短）
        if not topic.get("logic") or len(topic.get("logic", "")) < 10:
            topic["logic"] = generate_logic(topic, topic.get("c", []))
            fixed_count += 1
        
        # 5. 增强 trend 字段（如果为空或格式不对）
        if not topic.get("trend") or "🔥" not in topic.get("trend", ""):
            topic["trend"] = generate_trend(topic, history_data)
            fixed_count += 1
    
    print(f"修复字段数: {fixed_count}")
    
    # 保存修复后的热点数据
    with open(HOT_TOPICS_FILE, "w", encoding="utf-8") as f:
        json.dump(hot_topics, f, ensure_ascii=False, indent=2)
    print(f"已保存: {HOT_TOPICS_FILE}")
    
    # 更新历史数据（保存当前状态供下次对比）
    new_history = {}
    for topic in hot_topics:
        title = topic.get("title", "")
        new_history[title] = {
            "hot_value": topic.get("hot_value", 0),
            "platform": topic.get("platform", ""),
            "updated_at": datetime.now().isoformat(),
            "trend": topic.get("trend", "")
        }
    
    # 合并历史（保留旧数据）
    for title, data in history_data.items():
        if title not in new_history:
            new_history[title] = data
    
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(new_history, f, ensure_ascii=False, indent=2)
    print(f"已更新历史: {HISTORY_FILE}")
    
    # 验证修复结果
    print("\n" + "=" * 50)
    print("修复验证")
    print("=" * 50)
    
    # 统计字段覆盖率
    fields_stats = {
        "platforms": 0,
        "heat": 0,
        "isNew": 0,
        "logic": 0,
        "trend": 0
    }
    
    for topic in hot_topics:
        for field in fields_stats:
            if field in topic and topic[field]:
                fields_stats[field] += 1
    
    print(f"热点总数: {len(hot_topics)}")
    for field, count in fields_stats.items():
        coverage = count / len(hot_topics) * 100 if hot_topics else 0
        print(f"  {field}: {count}/{len(hot_topics)} ({coverage:.1f}%)")
    
    # 显示示例热点
    print("\n示例热点（前3条）：")
    for topic in hot_topics[:3]:
        print(f"\n标题: {topic.get('title', '')[:30]}...")
        print(f"  platforms: {topic.get('platforms', [])}")
        print(f"  heat: {topic.get('heat', '')}")
        print(f"  isNew: {topic.get('isNew', False)}")
        print(f"  logic: {topic.get('logic', '')[:40]}...")
        print(f"  trend: {topic.get('trend', '')}")
    
    print("\n修复完成!")

if __name__ == "__main__":
    main()