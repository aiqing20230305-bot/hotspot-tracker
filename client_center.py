#!/usr/bin/env python3
"""
🎯 特赞内容运营平台 - 客户选题中心 v3.0
功能：
1. 客户管理（12行业/22品牌/70+SKU）
2. 智能选题匹配（热点+SKU+场景）
3. 选题效果追踪
4. 个性化推荐
"""

import json
import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import yaml

@dataclass
class Client:
    """客户数据模型"""
    id: str
    industry: str
    brand: str
    sku_count: int
    priority: int  # 1-5
    platforms: List[str]
    content_angles: List[str]
    status: str = "active"  # active/paused/archived
    
    def to_dict(self) -> Dict:
        return asdict(self)

@dataclass
class SKU:
    """SKU数据模型"""
    id: str
    client_id: str
    name: str
    specs: str
    core_selling_points: List[str]
    scenarios: List[Dict]  # 使用场景列表
    
    def to_dict(self) -> Dict:
        return {
            **asdict(self),
            "scenario_count": len(self.scenarios)
        }

@dataclass
class ContentIdea:
    """内容选题数据模型"""
    id: str
    client_id: str
    sku_id: Optional[str]
    title: str
    platform: str
    content_type: str  # video/graphic
    angle: str
    hot_topic: str
    scenario: str
    pain_point: str
    emotional_resonance: str
    cta: str
    priority: int
    status: str = "pending"  # pending/approved/producing/published
    created_at: str = ""
    
    def to_dict(self) -> Dict:
        return asdict(self)

class ClientDatabase:
    """客户数据库"""
    
    def __init__(self, db_path: str = "client_center.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 客户表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id TEXT PRIMARY KEY,
                industry TEXT NOT NULL,
                brand TEXT NOT NULL,
                sku_count INTEGER DEFAULT 0,
                priority INTEGER DEFAULT 3,
                platforms TEXT,
                content_angles TEXT,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # SKU表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS skus (
                id TEXT PRIMARY KEY,
                client_id TEXT NOT NULL,
                name TEXT NOT NULL,
                specs TEXT,
                core_selling_points TEXT,
                scenarios TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (client_id) REFERENCES clients(id)
            )
        ''')
        
        # 选题表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS content_ideas (
                id TEXT PRIMARY KEY,
                client_id TEXT NOT NULL,
                sku_id TEXT,
                title TEXT NOT NULL,
                platform TEXT NOT NULL,
                content_type TEXT DEFAULT 'video',
                angle TEXT,
                hot_topic TEXT,
                scenario TEXT,
                pain_point TEXT,
                emotional_resonance TEXT,
                cta TEXT,
                priority INTEGER DEFAULT 3,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (client_id) REFERENCES clients(id),
                FOREIGN KEY (sku_id) REFERENCES skus(id)
            )
        ''')
        
        # 选题效果表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS idea_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idea_id TEXT NOT NULL,
                views INTEGER DEFAULT 0,
                likes INTEGER DEFAULT 0,
                comments INTEGER DEFAULT 0,
                shares INTEGER DEFAULT 0,
                conversion_rate REAL DEFAULT 0,
                published_date TEXT,
                FOREIGN KEY (idea_id) REFERENCES content_ideas(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def insert_client(self, client: Client):
        """插入客户"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO clients 
            (id, industry, brand, sku_count, priority, platforms, content_angles, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            client.id, client.industry, client.brand, client.sku_count,
            client.priority, json.dumps(client.platforms), json.dumps(client.content_angles),
            client.status
        ))
        
        conn.commit()
        conn.close()
    
    def insert_sku(self, sku: SKU):
        """插入SKU"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO skus 
            (id, client_id, name, specs, core_selling_points, scenarios)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            sku.id, sku.client_id, sku.name, sku.specs,
            json.dumps(sku.core_selling_points), json.dumps(sku.scenarios)
        ))
        
        conn.commit()
        conn.close()
    
    def insert_idea(self, idea: ContentIdea):
        """插入选题"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO content_ideas 
            (id, client_id, sku_id, title, platform, content_type, angle, hot_topic,
             scenario, pain_point, emotional_resonance, cta, priority, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            idea.id, idea.client_id, idea.sku_id, idea.title, idea.platform,
            idea.content_type, idea.angle, idea.hot_topic, idea.scenario,
            idea.pain_point, idea.emotional_resonance, idea.cta,
            idea.priority, idea.status, idea.created_at
        ))
        
        conn.commit()
        conn.close()
    
    def get_all_clients(self) -> List[Client]:
        """获取所有客户"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM clients WHERE status = "active" ORDER BY priority DESC')
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_client(row) for row in rows]
    
    def get_client_by_id(self, client_id: str) -> Optional[Client]:
        """获取单个客户"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM clients WHERE id = ?', (client_id,))
        row = cursor.fetchone()
        conn.close()
        
        return self._row_to_client(row) if row else None
    
    def get_skus_by_client(self, client_id: str) -> List[SKU]:
        """获取客户的所有SKU"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM skus WHERE client_id = ?', (client_id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_sku(row) for row in rows]
    
    def get_ideas_by_client(self, client_id: str, date: Optional[str] = None) -> List[ContentIdea]:
        """获取客户的选题"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if date:
            cursor.execute('''
                SELECT * FROM content_ideas 
                WHERE client_id = ? AND date(created_at) = date(?)
                ORDER BY priority DESC
            ''', (client_id, date))
        else:
            cursor.execute('''
                SELECT * FROM content_ideas 
                WHERE client_id = ?
                ORDER BY created_at DESC
                LIMIT 50
            ''', (client_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_idea(row) for row in rows]
    
    def _row_to_client(self, row) -> Client:
        return Client(
            id=row[0],
            industry=row[1],
            brand=row[2],
            sku_count=row[3],
            priority=row[4],
            platforms=json.loads(row[5]) if row[5] else [],
            content_angles=json.loads(row[6]) if row[6] else [],
            status=row[7]
        )
    
    def _row_to_sku(self, row) -> SKU:
        return SKU(
            id=row[0],
            client_id=row[1],
            name=row[2],
            specs=row[3],
            core_selling_points=json.loads(row[4]) if row[4] else [],
            scenarios=json.loads(row[5]) if row[5] else []
        )
    
    def _row_to_idea(self, row) -> ContentIdea:
        return ContentIdea(
            id=row[0],
            client_id=row[1],
            sku_id=row[2],
            title=row[3],
            platform=row[4],
            content_type=row[5],
            angle=row[6],
            hot_topic=row[7],
            scenario=row[8],
            pain_point=row[9],
            emotional_resonance=row[10],
            cta=row[11],
            priority=row[12],
            status=row[13],
            created_at=row[14]
        )

class ClientDataLoader:
    """客户数据加载器"""
    
    def __init__(self, db: ClientDatabase):
        self.db = db
        self.workspace = Path("/Users/zhangjingwei/.qclaw/workspace/hotspot-tracker")
    
    def load_all_clients(self):
        """加载所有客户数据"""
        print("🎯 加载客户数据...")
        
        # 从YAML加载SKU场景数据
        sku_data = self._load_sku_scenarios()
        
        # 客户基础数据
        clients_data = [
            {
                "id": "3c_digital",
                "industry": "3C数码",
                "brand": "荣耀海外/罗技/荣耀中国",
                "sku_count": 53,
                "priority": 5,
                "platforms": ["抖音", "小红书", "B站"],
                "content_angles": ["产品测评", "选购指南", "使用技巧", "科技热点"]
            },
            {
                "id": "fmcg",
                "industry": "快消",
                "brand": "舒适/清扬/AHC/多芬/力士/VSL/nexxus",
                "sku_count": 7,
                "priority": 5,
                "platforms": ["小红书", "抖音"],
                "content_angles": ["产品测评", "使用教程", "场景植入", "效果对比"]
            },
            {
                "id": "healthcare",
                "industry": "保健品",
                "brand": "汤臣倍健",
                "sku_count": 5,
                "priority": 5,
                "platforms": ["小红书", "抖音"],
                "content_angles": ["科普知识", "养生攻略", "产品推荐", "健康提醒"]
            },
            {
                "id": "home_cleaning",
                "industry": "家庭清洁",
                "brand": "HC",
                "sku_count": 15,
                "priority": 4,
                "platforms": ["抖音", "小红书"],
                "content_angles": ["清洁教程", "效果展示", "好物推荐", "场景解决"]
            },
            {
                "id": "pet_food",
                "industry": "宠物食品",
                "brand": "通用磨坊/希宝",
                "sku_count": 2,
                "priority": 3,
                "platforms": ["小红书", "抖音"],
                "content_angles": ["萌宠日常", "喂养攻略", "产品测评", "营养科普"]
            },
            {
                "id": "food_beverage",
                "industry": "食品饮料",
                "brand": "家乐",
                "sku_count": 1,
                "priority": 3,
                "platforms": ["抖音", "小红书"],
                "content_angles": ["美食教程", "快手菜", "场景植入", "食谱分享"]
            }
        ]
        
        # 保存客户数据
        for client_data in clients_data:
            client = Client(**client_data)
            self.db.insert_client(client)
            print(f"  ✅ {client.industry} - {client.brand}")
        
        # 保存SKU数据
        for sku_item in sku_data:
            sku = SKU(**sku_item)
            self.db.insert_sku(sku)
        
        print(f"\n📊 共加载 {len(clients_data)} 个客户，{len(sku_data)} 个SKU")
    
    def _load_sku_scenarios(self) -> List[Dict]:
        """从YAML加载SKU场景"""
        yaml_path = self.workspace / "sku_scenarios.yaml"
        
        if not yaml_path.exists():
            return []
        
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        skus = []
        for item in data.get('skus', []):
            client_id = self._get_client_id_by_name(item['client'])
            
            for i, scenario in enumerate(item.get('scenarios', [])):
                sku_id = f"{client_id}_{i}"
                skus.append({
                    "id": sku_id,
                    "client_id": client_id,
                    "name": item['sku_name'],
                    "specs": item['sku_specs'],
                    "core_selling_points": item['core_selling_points'],
                    "scenarios": [scenario]
                })
        
        return skus
    
    def _get_client_id_by_name(self, client_name: str) -> str:
        """根据名称获取客户ID"""
        mapping = {
            "3C数码-荣耀": "3c_digital",
            "快消-AHC": "fmcg",
            "快消-多芬": "fmcg",
            "快消-力士": "fmcg",
            "保健品-汤臣倍健": "healthcare",
            "家庭清洁-HC": "home_cleaning"
        }
        return mapping.get(client_name, "unknown")

class ContentIdeaGenerator:
    """内容选题生成器"""
    
    def __init__(self, db: ClientDatabase):
        self.db = db
        self.today = datetime.now().strftime("%Y%m%d")
    
    def generate_daily_ideas(self, client_id: str, hot_topics: List[Dict]) -> List[ContentIdea]:
        """为单个客户生成每日选题"""
        client = self.db.get_client_by_id(client_id)
        if not client:
            return []
        
        skus = self.db.get_skus_by_client(client_id)
        ideas = []
        
        # 为每个SKU生成1-2个选题
        for i, sku in enumerate(skus[:3]):  # 最多3个SKU
            for j, scenario in enumerate(sku.scenarios[:2]):  # 每个SKU最多2个场景
                # 匹配热点
                matched_topic = self._match_hot_topic(scenario, hot_topics)
                
                idea = self._create_idea(client, sku, scenario, matched_topic, i*2+j)
                ideas.append(idea)
                
                # 保存到数据库
                self.db.insert_idea(idea)
        
        return ideas
    
    def _match_hot_topic(self, scenario: Dict, hot_topics: List[Dict]) -> Dict:
        """匹配热点"""
        scenario_tags = scenario.get('hot_topics_match', [])
        
        for topic in hot_topics:
            topic_title = topic.get('title', '')
            if any(tag in topic_title for tag in scenario_tags):
                return topic
        
        # 默认返回第一个热点
        return hot_topics[0] if hot_topics else {'title': '热门话题', 'hot_value': 1000000}
    
    def _create_idea(self, client: Client, sku: SKU, scenario: Dict, 
                     hot_topic: Dict, index: int) -> ContentIdea:
        """创建选题"""
        platform = client.platforms[index % len(client.platforms)]
        angle = client.content_angles[index % len(client.content_angles)]
        
        # 生成标题
        title = self._generate_title(sku.name, hot_topic.get('title', ''), angle, platform)
        
        return ContentIdea(
            id=f"idea_{self.today}_{client.id}_{index}",
            client_id=client.id,
            sku_id=sku.id,
            title=title,
            platform=platform,
            content_type="video" if platform == "抖音" else "graphic",
            angle=angle,
            hot_topic=hot_topic.get('title', ''),
            scenario=scenario.get('name', ''),
            pain_point=scenario.get('pain_point', ''),
            emotional_resonance=scenario.get('resonance', ''),
            cta=f"你也有{scenario.get('pain_point', '这个问题')}吗？评论区聊聊~",
            priority=client.priority,
            created_at=datetime.now().isoformat()
        )
    
    def _generate_title(self, sku_name: str, hot_topic: str, angle: str, platform: str) -> str:
        """生成标题"""
        templates = {
            "抖音": {
                "产品测评": f"《{hot_topic}？{sku_name}真实测评》",
                "使用教程": f"《{hot_topic}教程，{sku_name}手把手教你》",
                "场景植入": f"《{hot_topic}的救星，{sku_name}实测》",
                "效果对比": f"《{hot_topic}对比，{sku_name}效果惊艳》"
            },
            "小红书": {
                "产品测评": f"《{hot_topic}｜{sku_name}真实测评》",
                "使用教程": f"《{hot_topic}｜{sku_name}教程》",
                "场景植入": f"《{hot_topic}｜{sku_name}场景实测》",
                "效果对比": f"《{hot_topic}｜{sku_name}效果对比》"
            },
            "B站": {
                "产品测评": f"《【深度测评】{hot_topic}？{sku_name}全面测试》",
                "选购指南": f"《【选购指南】{hot_topic}，{sku_name}值得买吗？》",
                "科技热点": f"《【科技前沿】{hot_topic}，{sku_name}体验》"
            }
        }
        
        platform_templates = templates.get(platform, templates["抖音"])
        return platform_templates.get(angle, f"《{hot_topic} - {sku_name}》")

def main():
    """主函数"""
    print("=" * 60)
    print("🎯 特赞内容运营平台 - 客户选题中心 v3.0")
    print("=" * 60)
    
    # 初始化数据库
    db = ClientDatabase()
    
    # 加载客户数据
    loader = ClientDataLoader(db)
    loader.load_all_clients()
    
    # 模拟热点数据
    hot_topics = [
        {"title": "春日粉彩妆容公式", "hot_value": 12100000},
        {"title": "中国机器狼群巷战", "hot_value": 11660000},
        {"title": "春日穿搭OOTD", "hot_value": 320000000},
        {"title": "春季护肤攻略", "hot_value": 210000000},
        {"title": "春日减脂计划", "hot_value": 150000000}
    ]
    
    # 为每个客户生成选题
    generator = ContentIdeaGenerator(db)
    clients = db.get_all_clients()
    
    print("\n📝 生成每日选题...")
    for client in clients:
        ideas = generator.generate_daily_ideas(client.id, hot_topics)
        print(f"  ✅ {client.industry} - 生成 {len(ideas)} 个选题")
    
    print("\n✅ 客户选题中心初始化完成！")
    print(f"📊 共为 {len(clients)} 个客户生成选题")

if __name__ == "__main__":
    main()
