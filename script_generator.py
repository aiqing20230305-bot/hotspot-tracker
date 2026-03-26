#!/usr/bin/env python3
"""
🎬 专业内容脚本生成器 - 结合热点+方法论
基于内容运营专业方法论生成脚本
"""

import json
from typing import Dict, List

class ContentMethodology:
    """内容运营方法论"""
    
    # AIDA模型
    AIDA = {
        "name": "AIDA模型",
        "description": "注意力→兴趣→欲望→行动",
        "steps": [
            {"step": "Attention", "chinese": "注意力", "action": "用热点/痛点吸引注意"},
            {"step": "Interest", "chinese": "兴趣", "action": "展示产品特点引发兴趣"},
            {"step": "Desire", "chinese": "欲望", "action": "描绘使用场景激发欲望"},
            {"step": "Action", "chinese": "行动", "action": "CTA引导购买/互动"}
        ]
    }
    
    # SCQA模型
    SCQA = {
        "name": "SCQA模型",
        "description": "情境→冲突→问题→答案",
        "steps": [
            {"step": "Situation", "chinese": "情境", "action": "描述背景/场景"},
            {"step": "Conflict", "chinese": "冲突", "action": "指出矛盾/痛点"},
            {"step": "Question", "chinese": "问题", "action": "提出疑问"},
            {"step": "Answer", "chinese": "答案", "action": "给出解决方案"}
        ]
    }
    
    # 痛点-解决方案模型
    PAIN_SOLUTION = {
        "name": "痛点-解决方案",
        "description": "痛点放大→解决方案→效果证明",
        "steps": [
            {"step": "Pain", "chinese": "痛点", "action": "放大痛点，引发共鸣"},
            {"step": "Agitate", "chinese": "激化", "action": "强调不解决的后果"},
            {"step": "Solution", "chinese": "方案", "action": "介绍产品解决方案"},
            {"step": "Proof", "chinese": "证明", "action": "效果证明/案例"}
        ]
    }

class ScriptGenerator:
    """专业脚本生成器"""
    
    def __init__(self):
        self.methodology = ContentMethodology()
    
    def generate_video_script(self, title: str, product: str, hot_topic: str, 
                             platform: str = "抖音", duration: int = 30) -> Dict:
        """生成视频脚本 - 结合热点和方法论"""
        
        # 根据热点类型选择方法论
        if "教程" in title or "攻略" in title:
            method = self.methodology.SCQA
        elif "测评" in title or "对比" in title:
            method = self.methodology.PAIN_SOLUTION
        else:
            method = self.methodology.AIDA
        
        script = {
            "title": title,
            "platform": platform,
            "duration": f"{duration}秒",
            "methodology": method["name"],
            "hook": f"{hot_topic}？看完这篇不踩坑！",
            "scenes": []
        }
        
        # 根据时长分配场景
        if duration == 30:
            script["scenes"] = [
                {
                    "time": "0-3秒",
                    "method_step": method["steps"][0]["chinese"],
                    "content": f"热点引入：{hot_topic}火了！但你是不是也遇到了XXX问题？",
                    "visual": f"{hot_topic}相关画面+困惑表情",
                    "tips": "前3秒必须抓住注意力，用热点+痛点双重钩子"
                },
                {
                    "time": "3-8秒",
                    "method_step": method["steps"][1]["chinese"],
                    "content": f"产品介绍：今天用{product}解决你的问题",
                    "visual": f"{product}特写+使用场景",
                    "tips": "快速展示产品，建立信任"
                },
                {
                    "time": "8-20秒",
                    "method_step": method["steps"][2]["chinese"],
                    "content": f"核心卖点：①XXX ②XXX ③XXX，亲测有效！",
                    "visual": "使用过程+效果对比",
                    "tips": "3个卖点最易于记忆，用数字强化"
                },
                {
                    "time": "20-25秒",
                    "method_step": method["steps"][3]["chinese"],
                    "content": f"效果展示：用了{product}后，效果惊艳！",
                    "visual": "前后对比图/使用前后",
                    "tips": "视觉化效果，增强说服力"
                },
                {
                    "time": "25-30秒",
                    "method_step": "CTA",
                    "content": "你也有同样问题吗？评论区告诉我！",
                    "visual": "手持产品+指向评论区",
                    "tips": "引导互动，提升完播率"
                }
            ]
        elif duration == 60:
            # 60秒版本，更详细
            pass
        
        script["bgm"] = "热门卡点音乐（节奏感强）"
        script["text_overlay"] = [
            f"{hot_topic[:8]}...",
            "痛点问题",
            f"{product[:6]}",
            "卖点1",
            "卖点2", 
            "卖点3",
            "效果对比",
            "评论区见"
        ]
        
        return script
    
    def generate_graphic_script(self, title: str, product: str, hot_topic: str,
                               platform: str = "小红书") -> Dict:
        """生成图文脚本 - 结合热点和方法论"""
        
        script = {
            "title": title,
            "platform": platform,
            "format": "图文笔记",
            "cover": f"{hot_topic[:10]} | {product}真实测评",
            "methodology": "痛点-解决方案",
            "structure": [
                {
                    "section": "封面",
                    "content": f"{hot_topic} | {product}测评 | 不吹不黑",
                    "tips": "封面要包含热点关键词+产品+价值承诺",
                    "image": "产品图+热点元素拼贴"
                },
                {
                    "section": "标题页",
                    "content": title,
                    "tips": "标题要包含热点关键词，提高搜索权重",
                    "image": "文字标题图"
                },
                {
                    "section": "开篇引入",
                    "content": f"最近{hot_topic}很火，作为XXX，必须给大家测评一下{product}",
                    "tips": "借势热点，建立专业人设",
                    "image": "热点截图+自我介绍"
                },
                {
                    "section": "痛点共鸣",
                    "content": "相信很多人都有这个困扰：XXX（痛点描述）",
                    "tips": "描述用户痛点，引发共鸣",
                    "image": "痛点场景图/表情包"
                },
                {
                    "section": "产品展示",
                    "content": f"今天测评的是{product}，先看外观/成分/质地",
                    "tips": "展示产品细节，建立信任",
                    "image": "产品外观3-5张（不同角度）"
                },
                {
                    "section": "使用体验",
                    "content": "优点：XXX\n缺点：XXX\n适合人群：XXX",
                    "tips": "客观评价，不夸大",
                    "image": "使用过程图"
                },
                {
                    "section": "效果对比",
                    "content": "使用前后对比，效果很明显",
                    "tips": "同光线同角度拍摄",
                    "image": "Before/After对比图"
                },
                {
                    "section": "总结建议",
                    "content": f"值得买吗？我的建议是：XXX\n性价比：⭐⭐⭐⭐\n推荐度：⭐⭐⭐⭐⭐",
                    "tips": "给出明确结论，方便决策",
                    "image": "总结文字图"
                },
                {
                    "section": "CTA",
                    "content": f"你用过{product}吗？觉得怎么样？评论区聊聊~\n\n#测评 #{hot_topic[:10]} #{product} #真实体验",
                    "tips": "引导互动，增加标签",
                    "image": "产品图+提问"
                }
            ],
            "tags": [
                f"#{hot_topic[:10]}",
                f"#{product}",
                "#测评",
                "#真实体验",
                "#好物推荐",
                "#不踩坑"
            ],
            "image_count": "6-9张",
            "image_tips": [
                "封面要吸睛，用拼图展示对比",
                "每页文字不要太多，重点突出",
                "使用emoji增加可读性",
                "图片风格保持一致"
            ]
        }
        
        return script
    
    def generate_bilibili_script(self, title: str, product: str, hot_topic: str) -> Dict:
        """生成B站中长视频脚本"""
        
        return {
            "title": title,
            "platform": "B站",
            "duration": "5-8分钟",
            "methodology": "SCQA+深度测评",
            "structure": [
                {
                    "time": "0:00-0:30",
                    "section": "片头",
                    "content": f"开场白+{hot_topic}引入，快速抓住注意力",
                    "tips": "黄金30秒，决定完播率"
                },
                {
                    "time": "0:30-1:00",
                    "section": "背景介绍",
                    "content": f"为什么{hot_topic}值得关注？背景信息补充",
                    "tips": "建立专业度，增加信息量"
                },
                {
                    "time": "1:00-2:00",
                    "section": "产品介绍",
                    "content": f"{product}详细介绍：外观、参数、功能",
                    "tips": "全方位展示，不遗漏细节"
                },
                {
                    "time": "2:00-4:00",
                    "section": "实测环节",
                    "content": "真实使用场景测试，多场景对比",
                    "tips": "实测是B站用户最爱看的部分"
                },
                {
                    "time": "4:00-5:00",
                    "section": "优缺点分析",
                    "content": "客观分析优缺点，用表格对比更清晰",
                    "tips": "保持中立，赢得信任"
                },
                {
                    "time": "5:00-6:00",
                    "section": "购买建议",
                    "content": "适合谁？不值得谁买？明确推荐",
                    "tips": "给出明确结论，降低决策成本"
                },
                {
                    "time": "6:00-7:00",
                    "section": "总结",
                    "content": "回顾要点+关注引导",
                    "tips": "留下互动问题，引导评论"
                },
                {
                    "time": "7:00-8:00",
                    "section": "片尾",
                    "content": "彩蛋/预告/致谢",
                    "tips": "增加完播率，培养粉丝粘性"
                }
            ],
            "bgm": "轻音乐/无音乐",
            "editing_tips": [
                "多机位拍摄，增加画面丰富度",
                "关键信息加字幕，方便理解",
                "适当加速无聊部分，保持节奏",
                "插入表情包增加趣味性",
                "章节标记，方便观众跳转"
            ],
            "cover_design": "标题大字+产品图+UP主形象+热点关键词",
            "tags": [hot_topic, product, "测评", "数码", "科技"]
        }

# 导出函数供HTML使用
def get_script_generator():
    return ScriptGenerator()

if __name__ == "__main__":
    generator = ScriptGenerator()
    
    # 测试生成
    video = generator.generate_video_script(
        "春日粉彩妆容公式｜AHC水乳测评",
        "AHC水乳",
        "春日粉彩妆容公式"
    )
    
    graphic = generator.generate_graphic_script(
        "春日粉彩妆容公式｜AHC水乳测评",
        "AHC水乳",
        "春日粉彩妆容公式"
    )
    
    print("=" * 60)
    print("🎬 视频脚本")
    print("=" * 60)
    print(json.dumps(video, ensure_ascii=False, indent=2))
    
    print("\n" + "=" * 60)
    print("📝 图文脚本")
    print("=" * 60)
    print(json.dumps(graphic, ensure_ascii=False, indent=2))
