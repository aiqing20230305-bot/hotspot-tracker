#!/usr/bin/env python3
"""
📦 特赞内容运营平台 - SKU场景库 v4.0
功能：
1. SKU基础信息管理
2. 使用场景定义
3. 用户痛点分析
4. 情感共鸣提炼
5. 热点智能匹配
"""

import json
import asyncio
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

class SKU:
    """SKU数据模型"""
    def __init__(self, client: str, sku_name: str, specs: str, selling_points: List[str]):
        self.client = client
        self.sku_name = sku_name
        self.specs = specs
        self.selling_points = selling_points
    
    def to_dict(self) -> Dict:
        return {
            "client": self.client,
            "sku_name": self.sku_name,
            "specs": self.specs,
            "selling_points": self.selling_points
        }

class Scenario:
    """场景数据模型"""
    def __init__(self, name: str, pain_point: str, resonance: str, 
                 content_angles: List[str], hot_topics: List[str]):
        self.name = name
        self.pain_point = pain_point
        self.resonance = resonance
        self.content_angles = content_angles
        self.hot_topics = hot_topics
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "pain_point": self.pain_point,
            "resonance": self.resonance,
            "content_angles": self.content_angles,
            "hot_topics": self.hot_topics
        }

class SKUSceneLibrary:
    """SKU场景库"""
    
    # SKU场景数据库
    SKU_SCENES = {
        "荣耀Magic6": {
            "client": "3C数码-荣耀",
            "specs": "骁龙8 Gen3/16GB+512GB/5450mAh",
            "selling_points": [
                "AI大模型加持，智能助手更懂你",
                "鹰眼相机，抓拍更清晰",
                "青海湖电池，续航无忧",
                "鸿蒙生态，万物互联"
            ],
            "scenarios": [
                {
                    "name": "职场效率提升",
                    "pain_point": "工作消息太多，回复不过来；会议记录整理耗时",
                    "resonance": "想要工作生活平衡，不想被工作绑架",
                    "content_angles": [
                        "AI助手自动回复消息，效率翻倍",
                        "语音转文字+智能摘要，会议纪要5分钟搞定",
                        "多屏协同，手机电脑无缝切换"
                    ],
                    "hot_topics": ["打工人效率", "职场技能", "AI办公", "摸鱼技巧"]
                },
                {
                    "name": "亲子记录时光",
                    "pain_point": "孩子动作太快，拍出来都是糊的；照片太多整理麻烦",
                    "resonance": "想记录孩子每一个成长瞬间，留住美好回忆",
                    "content_angles": [
                        "鹰眼抓拍，孩子跑动也能清晰记录",
                        "AI自动分类，按时间/人物/场景整理照片",
                        "一键生成成长视频，回忆满满"
                    ],
                    "hot_topics": ["亲子时光", "宝宝成长", "拍照技巧", "带娃日常"]
                },
                {
                    "name": "商务出行必备",
                    "pain_point": "出差手机没电焦虑；境外网络不稳定",
                    "resonance": "商务人士需要可靠的工具，不能掉链子",
                    "content_angles": [
                        "青海湖电池，一天重度使用无忧",
                        "天际通，境外一键上网",
                        "隐私空间，工作生活分开"
                    ],
                    "hot_topics": ["商务出行", "出差必备", "效率工具", "移动办公"]
                }
            ]
        },
        "AHC B5水乳套装": {
            "client": "快消-AHC",
            "specs": "玻尿酸+维生素B5/120ml+120ml",
            "selling_points": [
                "98%高纯度玻尿酸，深层补水",
                "维生素B5修护屏障",
                "清爽不粘腻，吸收快",
                "平价大牌品质"
            ],
            "scenarios": [
                {
                    "name": "春日妆容打底",
                    "pain_point": "换季皮肤干燥，上妆卡粉脱妆",
                    "resonance": "想要精致妆容，但皮肤状态不好",
                    "content_angles": [
                        "春日粉彩妆容公式，AHC水乳打底是关键",
                        "妆前5分钟急救，底妆服帖一整天",
                        "学生党平价好物，百元内搞定"
                    ],
                    "hot_topics": ["春日粉彩妆容公式", "春季护肤攻略", "底妆服帖", "换季护肤"]
                },
                {
                    "name": "熬夜肌急救",
                    "pain_point": "熬夜后皮肤暗沉、干燥、没光泽",
                    "resonance": "知道熬夜不好，但不得不熬，需要急救",
                    "content_angles": [
                        "熬夜肌急救指南，AHC水乳湿敷法",
                        "3天拯救熬夜脸，恢复水光肌",
                        "打工人必备，熬夜也能有好气色"
                    ],
                    "hot_topics": ["熬夜急救", "打工人护肤", "水光肌", "夜猫子"]
                },
                {
                    "name": "学生党入门",
                    "pain_point": "预算有限，不知道买什么护肤品",
                    "resonance": "想要开始护肤，但不知道怎么选",
                    "content_angles": [
                        "第一套水乳怎么选？AHC百元内天花板",
                        "学生党护肤入门，从基础补水开始",
                        "平价不踩雷，宿舍人手一套"
                    ],
                    "hot_topics": ["学生党护肤", "平价好物", "护肤入门", "宿舍好物"]
                }
            ]
        },
        "多芬樱花沐浴露": {
            "client": "快消-多芬",
            "specs": "樱花香氛/730g/氨基酸配方",
            "selling_points": [
                "真樱花萃取，持久留香",
                "氨基酸配方，温和不刺激",
                "美少女益生元，越洗越嫩",
                "泡沫绵密，洗澡像SPA"
            ],
            "scenarios": [
                {
                    "name": "春日沐浴仪式",
                    "pain_point": "洗澡只是清洁，没有享受感",
                    "resonance": "想要生活中的小确幸，提升幸福感",
                    "content_angles": [
                        "春日沐浴仪式感，多芬樱花香氛",
                        "洗澡也能很治愈，樱花雨中的SPA",
                        "留香24小时，被子都是樱花味"
                    ],
                    "hot_topics": ["春日氛围感", "沐浴仪式感", "提升幸福感", "樱花季"]
                },
                {
                    "name": "约会前准备",
                    "pain_point": "约会前想让自己香香的，但香水太浓",
                    "resonance": "想要自然体香，给对方留下好印象",
                    "content_angles": [
                        "约会前的小心机，自然伪体香",
                        "比香水更自然的味道，靠近才能闻到",
                        "春日约会必备，樱花味太撩人"
                    ],
                    "hot_topics": ["约会准备", "伪体香", "春日约会", "撩人香"]
                },
                {
                    "name": "敏感肌护理",
                    "pain_point": "皮肤敏感，用普通沐浴露会干痒",
                    "resonance": "想要温和清洁，不伤害皮肤屏障",
                    "content_angles": [
                        "敏感肌也能用的沐浴露，氨基酸配方",
                        "洗澡不干痒，越洗皮肤越好",
                        "皮肤科医生推荐，温和清洁"
                    ],
                    "hot_topics": ["敏感肌护理", "氨基酸沐浴露", "温和清洁", "皮肤屏障"]
                }
            ]
        },
        "汤臣倍健蛋白粉": {
            "client": "保健品-汤臣倍健",
            "specs": "双蛋白配方/450g/动植物蛋白",
            "selling_points": [
                "80%高蛋白含量",
                "动植物双蛋白，营养更均衡",
                "增强免疫力",
                "术后/运动后恢复"
            ],
            "scenarios": [
                {
                    "name": "健身增肌",
                    "pain_point": "健身但肌肉增长慢，蛋白质摄入不足",
                    "resonance": "想要好身材，需要科学补充蛋白质",
                    "content_angles": [
                        "43岁vs61岁健身区别，蛋白质是关键",
                        "健身后30分钟黄金补充期",
                        "不健身的人也需要蛋白质"
                    ],
                    "hot_topics": ["健身增肌", "蛋白质补充", "运动恢复", "塑形"]
                },
                {
                    "name": "术后恢复",
                    "pain_point": "手术后身体虚弱，恢复慢",
                    "resonance": "希望家人快点康复，需要营养支持",
                    "content_angles": [
                        "术后恢复必备，蛋白质是修复基础",
                        "医生推荐的术后营养品",
                        "送长辈的最佳选择"
                    ],
                    "hot_topics": ["术后恢复", "营养补充", "送长辈", "健康礼品"]
                },
                {
                    "name": "日常免疫力",
                    "pain_point": "容易感冒，免疫力差",
                    "resonance": "想要增强体质，少生病",
                    "content_angles": [
                        "春季流感高发，免疫力是最好防护",
                        "每天一杯，免疫力UP",
                        "比吃鸡蛋更高效的蛋白质补充"
                    ],
                    "hot_topics": ["免疫力提升", "春季养生", "健康生活", "少生病"]
                }
            ]
        },
        "HC多功能清洁剂": {
            "client": "家庭清洁-HC",
            "specs": "强力去污/500ml/柠檬香型",
            "selling_points": [
                "一喷即净，去污力强",
                "不伤手不伤表面",
                "柠檬清香，不刺鼻",
                "多功能，一瓶搞定全屋"
            ],
            "scenarios": [
                {
                    "name": "春季大扫除",
                    "pain_point": "年底大扫除太累，清洁产品效果差",
                    "resonance": "想要轻松搞定清洁，省时省力",
                    "content_angles": [
                        "春季大扫除神器，30分钟搞定全屋",
                        "租房党必备，退租清洁不扣押金",
                        "一喷一擦，厨房油污轻松搞定"
                    ],
                    "hot_topics": ["春季大扫除", "租房清洁", "厨房油污", "年末大扫除"]
                },
                {
                    "name": "日常快速清洁",
                    "pain_point": "工作忙没时间打扫，家里乱糟糟",
                    "resonance": "想要保持整洁，但没时间大扫",
                    "content_angles": [
                        "每天5分钟，家里永远干净整洁",
                        "懒人清洁法，一喷一擦就干净",
                        "上班族必备，周末不用大扫除"
                    ],
                    "hot_topics": ["日常清洁", "懒人清洁", "上班族", "省时清洁"]
                },
                {
                    "name": "母婴家庭",
                    "pain_point": "有宝宝后更注重清洁，但怕化学残留",
                    "resonance": "想要安全清洁，保护宝宝健康",
                    "content_angles": [
                        "母婴家庭专用，安全无残留",
                        "宝宝爬行的地方也能用",
                        "新手妈妈必备，清洁又安心"
                    ],
                    "hot_topics": ["母婴清洁", "安全清洁", "新手妈妈", "宝宝安全"]
                }
            ]
        }
    }
    
    def __init__(self):
        self.workspace = Path("/Users/zhangjingwei/.qclaw/workspace/hotspot-tracker")
        self.data_file = self.workspace / "sku_scenes.json"
    
    def get_all_skus(self) -> List[Dict]:
        """获取所有SKU"""
        result = []
        for sku_name, data in self.SKU_SCENES.items():
            result.append({
                "sku_name": sku_name,
                **data
            })
        return result
    
    def get_sku(self, sku_name: str) -> Optional[Dict]:
        """获取单个SKU"""
        return self.SKU_SCENES.get(sku_name)
    
    def get_client_skus(self, client: str) -> List[Dict]:
        """获取客户的所有SKU"""
        return [
            {"sku_name": name, **data}
            for name, data in self.SKU_SCENES.items()
            if data["client"] == client
        ]
    
    def match_hot_topics(self, sku_name: str) -> List[str]:
        """获取SKU匹配的所有热点"""
        sku_data = self.SKU_SCENES.get(sku_name)
        if not sku_data:
            return []
        
        all_topics = []
        for scenario in sku_data.get("scenarios", []):
            all_topics.extend(scenario.get("hot_topics", []))
        
        return list(set(all_topics))  # 去重
    
    def generate_report(self) -> Dict:
        """生成SKU场景报告"""
        skus = self.get_all_skus()
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "total_skus": len(skus),
            "total_scenarios": sum(len(sku.get("scenarios", [])) for sku in skus),
            "skus": []
        }
        
        for sku in skus:
            sku_report = {
                "sku_name": sku["sku_name"],
                "client": sku["client"],
                "specs": sku["specs"],
                "selling_points": sku["selling_points"],
                "scenarios": []
            }
            
            for scenario in sku.get("scenarios", []):
                sku_report["scenarios"].append({
                    "name": scenario["name"],
                    "pain_point": scenario["pain_point"],
                    "resonance": scenario["resonance"],
                    "content_angles": scenario["content_angles"],
                    "hot_topics": scenario["hot_topics"]
                })
            
            report["skus"].append(sku_report)
        
        # 保存报告
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        return report

async def main():
    """主函数"""
    library = SKUSceneLibrary()
    
    print("=" * 60)
    print("📦 SKU场景库 - 生成报告")
    print("=" * 60)
    
    # 生成报告
    report = library.generate_report()
    
    print(f"\n✅ SKU场景库报告生成完成！")
    print(f"📊 共 {report['total_skus']} 个SKU")
    print(f"📝 共 {report['total_scenarios']} 个场景")
    
    # 展示每个SKU
    print(f"\n📦 SKU场景概览：")
    for sku in report['skus'][:3]:
        print(f"\n【{sku['sku_name']}】- {sku['client']}")
        print(f"   规格：{sku['specs']}")
        print(f"   场景：")
        for scenario in sku['scenarios'][:2]:
            print(f"   • {scenario['name']} → {scenario['pain_point'][:30]}...")

if __name__ == "__main__":
    asyncio.run(main())
