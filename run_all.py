#!/usr/bin/env python3
"""
全平台热点追踪 - 抖音 + 微博 + 小红书
一键执行脚本
"""

import subprocess
import sys
from datetime import datetime

def run_script(script_path, name):
    """执行脚本"""
    print(f"\n{'='*50}")
    print(f"🔄 执行: {name}")
    print('='*50)
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=180
        )
        print(result.stdout)
        if result.returncode != 0:
            print(f"⚠️ 错误: {result.stderr}")
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"⚠️ {name} 执行超时")
        return False
    except Exception as e:
        print(f"⚠️ {name} 执行失败: {e}")
        return False

def main():
    """主函数"""
    print(f"📊 全平台热点追踪报告")
    print(f"📅 执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    base_dir = "/Users/zhangjingwei/.qclaw/workspace/hotspot-tracker"
    
    # 1. 抖音 + 微博热点
    run_script(f"{base_dir}/hotspot_tracker.py", "抖音/微博热点")
    
    # 2. 小红书热点（需要 Playwright）
    # 如果 Playwright 未安装，跳过
    try:
        import playwright
        run_script(f"{base_dir}/xiaohongshu_scraper.py", "小红书热点")
    except ImportError:
        print("\n⚠️ Playwright 未安装，跳过小红书抓取")
        print("💡 安装命令: pip3 install playwright && python3 -m playwright install chromium")
    
    print(f"\n{'='*50}")
    print("✅ 热点追踪完成")
    print(f"📁 报告目录: {base_dir}")
    print('='*50)

if __name__ == "__main__":
    main()
