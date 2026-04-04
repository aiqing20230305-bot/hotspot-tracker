#!/usr/bin/env python3
"""
热点数据字段补全脚本
为 hot_topics.json 补全 logic/trend/heat/isNew 字段
"""

import json
import os
from datetime import datetime

# 文件路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HOT_TOPICS_FILE = os.path.join(BASE_DIR, "hot_topics.json")
HISTORY_FILE = os.path.join(BASE_DIR, "hotspot_history.json")
OUTPUT_FILE = os.path.join(BASE_DIR, "hot_topics.json")


def format_heat_value(value):
    """将数值格式化为 '766万' 形式"""
    if value >= 100000000:
        return f"{value / 100000000:.1f}亿"
    elif value >= 10000000:
        return f"{value / 10000000:.1f}千万"
    elif value >= 1000000:
        return f"{value / 1000000:.1f}百万"
    elif value >= 10000:
        return f"{value / 10000:.0f}万"
    else:
        return str(value)


def generate_logic(title, industries):
    """基于热点标题和行业生成简短分析（50字以内）"""
    # 行业特征关键词映射
    industry_features = {
        "旅游": "假期出游",
        "文化": "文旅融合",
        "美食": "餐饮消费",
        "社交": "社交生活",
        "健康": "健康关注",
        "医疗": "医疗服务",
        "零售": "零售消费",
        "消费": "消费升级",
        "科技": "科技创新",
        "AI": "人工智能",
        "宠物": "宠物经济",
        "母婴": "母婴育儿",
        "美妆": "美妆护肤",
        "护肤": "护肤需求",
        "健身": "健身运动",
        "食品": "食品饮料",
        "汽车": "汽车出行",
        "新能源": "新能源车",
        "家居": "家居生活",
        "游戏": "游戏娱乐",
        "娱乐": "娱乐休闲",
        "个护": "个人护理",
        "时尚": "时尚潮流",
        "酒店": "酒店住宿",
        "教育": "教育培训",
        "互联网": "互联网服务",
        "服装": "服饰穿搭",
        "户外": "户外运动"
    }
    
    # 提取行业特征
    features = []
    for ind in industries:
        if ind in industry_features:
            features.append(industry_features[ind])
    
    # 根据标题关键词生成分析
    analysis_patterns = []
    
    if any(kw in title for kw in ["假期", "清明", "周末", "出行", "旅游"]):
        analysis_patterns.append("节假日出行热度攀升")
    if any(kw in title for kw in ["新能源", "充电", "续航"]):
        analysis_patterns.append("新能源汽车充电痛点受关注")
    if any(kw in title for kw in ["AI", "视频生成", "工具"]):
        analysis_patterns.append("AI工具赋能内容创作")
    if any(kw in title for kw in ["护肤", "精华", "美妆", "防晒"]):
        analysis_patterns.append("护肤品类进入季节性旺季")
    if any(kw in title for kw in ["brunch", "咖啡", "美食"]):
        analysis_patterns.append("休闲餐饮消费持续升温")
    if any(kw in title for kw in ["宠物", "寄养", "美容"]):
        analysis_patterns.append("宠物服务需求快速增长")
    if any(kw in title for kw in ["过敏", "花粉", "健康"]):
        analysis_patterns.append("季节性健康问题引发关注")
    if any(kw in title for kw in ["智能", "家居", "设备"]):
        analysis_patterns.append("智能家居渗透率持续提升")
    if any(kw in title for kw in ["运动", "骑行", "户外"]):
        analysis_patterns.append("户外运动参与度显著上升")
    if any(kw in title for kw in ["青团", "节令", "传统"]):
        analysis_patterns.append("传统节令食品创新热销")
    
    # 如果没有匹配的模式，使用通用分析
    if not analysis_patterns:
        if features:
            analysis_patterns.append(f"{'、'.join(features[:2])}需求旺盛")
        else:
            analysis_patterns.append("话题热度持续攀升")
    
    logic = analysis_patterns[0]
    if features and features[0] not in logic:
        logic = f"{features[0]}话题热度上升"
    
    # 限制在50字以内
    if len(logic) > 50:
        logic = logic[:47] + "..."
    
    return logic


def calculate_trend(current_value, history_value, rank=1):
    """根据当前值与历史值对比，判断趋势"""
    if history_value is None:
        # 没有历史数据，根据排名判断
        if rank <= 5:
            return "爆发"
        elif rank <= 15:
            return "上升"
        else:
            return "稳定"
    
    # 计算变化率
    if history_value == 0:
        return "爆发"
    
    change_rate = (current_value - history_value) / history_value
    
    if change_rate > 0.20:  # 增长超过20%
        return "爆发"
    elif change_rate > 0.10:  # 增长超过10%
        return "上升"
    elif change_rate < -0.10:  # 下降超过10%
        return "下降"
    else:
        return "稳定"


def check_is_new(title, history_data):
    """与历史对比，新出现的标记为 true"""
    # 标准化标题进行匹配
    normalized_title = title.lower().strip()
    
    for history_title in history_data.keys():
        # 简化匹配：检查关键部分
        if normalized_title in history_title.lower() or history_title.lower() in normalized_title:
            return False
    
    return True


def load_history():
    """加载历史数据"""
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ 加载历史数据失败: {e}")
        return {}


def main():
    """主函数"""
    print("📂 加载热点数据...")
    
    # 加载当前数据
    with open(HOT_TOPICS_FILE, 'r', encoding='utf-8') as f:
        hot_topics = json.load(f)
    
    print(f"✅ 加载 {len(hot_topics)} 条热点")
    
    # 加载历史数据
    history_data = load_history()
    print(f"✅ 加载 {len(history_data)} 条历史热点")
    
    # 补全字段
    updated_count = 0
    
    for i, topic in enumerate(hot_topics):
        title = topic.get('title', '')
        hot_value = topic.get('hot_value', 0)
        industries = topic.get('industries', [])
        
        # 1. 添加 heat 字段（格式化热度值）
        topic['heat'] = format_heat_value(hot_value)
        
        # 2. 添加 logic 字段（简短分析）
        topic['logic'] = generate_logic(title, industries)
        
        # 3. 添加 trend 字段（趋势判断）
        history_value = None
        for history_title, history_info in history_data.items():
            if title in history_title or history_title in title:
                history_value = history_info.get('hot_value')
                break
        
        topic['trend'] = calculate_trend(hot_value, history_value, rank=i+1)
        
        # 4. 添加 isNew 字段（新热点标记）
        topic['isNew'] = check_is_new(title, history_data)
        
        updated_count += 1
    
    print(f"✅ 补全 {updated_count} 条数据字段")
    
    # 保存更新后的数据
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(hot_topics, f, ensure_ascii=False, indent=2)
    
    print(f"📁 已保存到: {OUTPUT_FILE}")
    
    # 打印示例
    print("\n📋 示例数据（前3条）:")
    for topic in hot_topics[:3]:
        print(f"  • {topic['title'][:20]}...")
        print(f"    heat: {topic.get('heat')}")
        print(f"    logic: {topic.get('logic')}")
        print(f"    trend: {topic.get('trend')}")
        print(f"    isNew: {topic.get('isNew')}")
        print()


if __name__ == "__main__":
    main()