#!/usr/bin/env python3
"""
小红书热点抓取器 - Playwright 自动化方案
支持：热搜榜、垂直行业搜索、素人爆款发现
"""

import asyncio
import json
import re
from datetime import datetime
from playwright.async_api import async_playwright

# 9大垂直领域搜索关键词
INDUSTRY_SEARCH = {
    "美妆": ["口红试色", "粉底测评", "护肤心得", "妆教教程"],
    "母婴": ["宝宝用品", "孕妇必备", "育儿经验", "婴儿辅食"],
    "数码": ["手机测评", "数码好物", "耳机推荐", "笔记本"],
    "服装": ["穿搭分享", "春日穿搭", "显瘦穿搭", "通勤穿搭"],
    "食品": ["零食推荐", "健康饮食", "减脂餐", "美食探店"],
    "汽车": ["新能源车", "提车日记", "汽车用品", "自驾游"],
    "大健康": ["养生日常", "体检攻略", "减肥打卡", "健身教程"],
    "快消": ["日用品分享", "洗护好物", "家居好物", "平价好物"],
    "家电": ["家电推荐", "智能家居", "厨房电器", "清洁电器"]
}

class XiaohongshuScraper:
    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None
        
    async def init_browser(self, headless=True):
        """初始化浏览器"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=headless,
            args=['--disable-blink-features=AutomationControlled']
        )
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        self.page = await self.context.new_page()
        
        # 注入反检测脚本
        await self.page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            window.chrome = {runtime: {}};
        """)
        
    async def close(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
            
    async def get_hot_search(self):
        """获取小红书热搜榜"""
        print("📱 正在获取小红书热搜榜...")
        
        try:
            await self.page.goto('https://www.xiaohongshu.com/explore', wait_until='networkidle', timeout=30000)
            await asyncio.sleep(2)
            
            # 尝试多种选择器
            hot_items = []
            
            # 方案1: 搜索热点榜单
            try:
                search_input = await self.page.query_selector('input[placeholder*="搜索"]')
                if search_input:
                    await search_input.click()
                    await asyncio.sleep(1)
                    # 查找热搜列表
                    hot_elements = await self.page.query_selector_all('.hot-item, .search-hot-item, [class*="hot"]')
                    for i, el in enumerate(hot_elements[:20]):
                        text = await el.inner_text()
                        if text.strip():
                            hot_items.append({
                                "rank": i + 1,
                                "title": text.strip(),
                                "platform": "小红书"
                            })
            except Exception as e:
                print(f"热搜获取方式1失败: {e}")
                
            # 方案2: 从页面提取热门话题
            if not hot_items:
                try:
                    topics = await self.page.query_selector_all('[class*="title"], [class*="topic"], a[href*="/search_result"]')
                    for i, el in enumerate(topics[:20]):
                        text = await el.inner_text()
                        if text.strip() and len(text.strip()) > 2:
                            hot_items.append({
                                "rank": i + 1,
                                "title": text.strip()[:50],
                                "platform": "小红书"
                            })
                except Exception as e:
                    print(f"热搜获取方式2失败: {e}")
            
            return {"platform": "小红书", "data": hot_items, "success": len(hot_items) > 0}
            
        except Exception as e:
            print(f"获取热搜失败: {e}")
            return {"platform": "小红书", "data": [], "success": False, "error": str(e)}
    
    async def search_industry(self, industry, keywords):
        """搜索垂直行业内容"""
        print(f"🔍 搜索 {industry} 相关内容...")
        
        results = []
        for keyword in keywords[:2]:  # 每个行业搜索2个关键词
            try:
                search_url = f'https://www.xiaohongshu.com/search_result?keyword={keyword}'
                await self.page.goto(search_url, wait_until='networkidle', timeout=20000)
                await asyncio.sleep(2)
                
                # 提取笔记卡片
                notes = await self.page.query_selector_all('[class*="note-item"], [class*="card"], a[href*="/explore/"]')
                
                for i, note in enumerate(notes[:10]):
                    try:
                        text = await note.inner_text()
                        # 提取标题和互动数据
                        lines = text.strip().split('\n')
                        title = lines[0] if lines else ""
                        
                        # 提取点赞数
                        likes_match = re.search(r'(\d+(?:\.\d+)?[万]?)\s*赞', text)
                        likes = likes_match.group(1) if likes_match else "0"
                        
                        if title and len(title) > 5:
                            results.append({
                                "title": title[:100],
                                "keyword": keyword,
                                "likes": likes,
                                "industry": industry,
                                "platform": "小红书"
                            })
                    except:
                        continue
                        
                await asyncio.sleep(1)  # 避免频繁请求
                
            except Exception as e:
                print(f"搜索 {keyword} 失败: {e}")
                continue
        
        return results

async def main():
    """主函数"""
    scraper = XiaohongshuScraper()
    
    try:
        await scraper.init_browser(headless=True)
        
        # 1. 获取热搜榜
        hot_search = await scraper.get_hot_search()
        
        # 2. 搜索各行业内容
        all_industry_results = {}
        for industry, keywords in INDUSTRY_SEARCH.items():
            results = await scraper.search_industry(industry, keywords)
            all_industry_results[industry] = results
            print(f"✅ {industry}: {len(results)} 条")
        
        # 3. 生成报告
        report = {
            "generated_at": datetime.now().isoformat(),
            "hot_search": hot_search,
            "industry_results": all_industry_results,
            "total_notes": sum(len(v) for v in all_industry_results.values())
        }
        
        # 保存报告
        output_file = f"/Users/zhangjingwei/.qclaw/workspace/hotspot-tracker/xiaohongshu_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n📁 小红书报告已保存: {output_file}")
        return report
        
    finally:
        await scraper.close()

if __name__ == "__main__":
    asyncio.run(main())
