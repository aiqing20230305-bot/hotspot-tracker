#!/usr/bin/env python3
"""
🚀 热点追踪系统 - 统一启动器
一键启动完整工作流
"""

import argparse
import asyncio
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

def show_banner():
    """显示系统横幅"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           🔥 热点追踪系统 v2.0 - 智能进化版 🔥               ║
║                                                              ║
║     自动抓取热点 → AI内容推荐 → 效果反馈学习                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)

def show_menu():
    """显示主菜单"""
    print("\n📋 功能菜单:")
    print("-" * 60)
    print("  1. 🔄 运行完整工作流 (抓取+推荐+报告)")
    print("  2. 📊 查看系统状态")
    print("  3. 📝 添加内容效果反馈")
    print("  4. 🧠 查看自学习洞察")
    print("  5. ⚙️  配置推送渠道")
    print("  6. 📅 设置定时任务")
    print("  7. 🌐 部署到GitHub Pages")
    print("  0. ❌ 退出")
    print("-" * 60)

async def run_workflow():
    """运行完整工作流"""
    from automation_workflow import AutomationWorkflow
    workflow = AutomationWorkflow()
    await workflow.run_full_workflow()

def show_status():
    """显示系统状态"""
    from automation_workflow import AutomationWorkflow
    workflow = AutomationWorkflow()
    workflow.show_status()

def add_feedback():
    """添加反馈"""
    import json
    from self_learning import SelfLearningSystem
    
    print("\n📝 添加内容效果反馈")
    print("-" * 60)
    
    content_id = input("内容ID: ")
    industry = input("行业 (如: 3C数码/快消/保健品): ")
    platform = input("平台 (如: 抖音/小红书/B站): ")
    angle = input("内容角度 (如: 产品测评/使用教程): ")
    hot_topic = input("借势热点: ")
    
    print("\n输入互动数据:")
    likes = int(input("  点赞数: ") or 0)
    comments = int(input("  评论数: ") or 0)
    shares = int(input("  分享数: ") or 0)
    views = int(input("  浏览量: ") or 1)
    
    metrics = {"likes": likes, "comments": comments, "shares": shares, "views": views}
    
    learning = SelfLearningSystem()
    learning.add_feedback(content_id, industry, platform, angle, hot_topic, metrics)
    print("\n✅ 反馈已添加！")

def show_insights():
    """显示自学习洞察"""
    from self_learning import SelfLearningSystem
    learning = SelfLearningSystem()
    learning.show_dashboard()
    
    print("\n📊 生成详细报告...")
    report = learning.generate_insights()
    print(f"\n报告已保存: {learning.insights_file}")
    
    # 显示优化规则
    rules = learning.get_optimization_rules()
    if rules:
        print("\n🎯 系统优化建议:")
        for i, rule in enumerate(rules, 1):
            print(f"{i}. {rule['rule']}")

def configure_push():
    """配置推送渠道"""
    from automation_workflow import AutomationWorkflow
    workflow = AutomationWorkflow()
    
    print("\n⚙️  配置推送渠道")
    print("-" * 60)
    print("1. 飞书Webhook")
    print("2. 钉钉Webhook")
    print("3. 返回")
    
    choice = input("\n选择: ")
    
    if choice == "1":
        webhook = input("输入飞书Webhook URL: ")
        if webhook:
            workflow.configure_feishu(webhook)
    elif choice == "2":
        webhook = input("输入钉钉Webhook URL: ")
        if webhook:
            workflow.configure_dingtalk(webhook)

def setup_cron():
    """设置定时任务"""
    from automation_workflow import AutomationWorkflow
    workflow = AutomationWorkflow()
    workflow.setup_cron()

def deploy_github():
    """部署到GitHub"""
    import subprocess
    from datetime import datetime
    
    print("\n🌐 部署到GitHub Pages")
    print("-" * 60)
    
    workspace = Path("/Users/zhangjingwei/.qclaw/workspace/hotspot-tracker")
    
    try:
        # 检查git状态
        result = subprocess.run(
            ["git", "status", "--short"],
            capture_output=True,
            text=True,
            cwd=str(workspace)
        )
        
        if result.stdout.strip():
            print("📤 检测到变更，开始推送...")
            
            # 添加所有变更
            subprocess.run(["git", "add", "."], cwd=str(workspace), check=True)
            
            # 提交
            today = datetime.now().strftime("%Y%m%d_%H%M")
            subprocess.run(
                ["git", "commit", "-m", f"Update: Evolution system v2.0 - {today}"],
                cwd=str(workspace),
                check=True
            )
            
            # 推送
            subprocess.run(["git", "push", "origin", "main"], cwd=str(workspace), check=True)
            
            print("✅ 部署成功！")
            print(f"\n🌐 访问地址: https://aiqing20230305-bot.github.io/hotspot-tracker/")
        else:
            print("ℹ️ 没有需要推送的变更")
    
    except Exception as e:
        print(f"❌ 部署失败: {e}")

async def main():
    """主函数"""
    show_banner()
    
    while True:
        show_menu()
        choice = input("\n请选择功能 (0-7): ").strip()
        
        if choice == "1":
            await run_workflow()
        elif choice == "2":
            show_status()
        elif choice == "3":
            add_feedback()
        elif choice == "4":
            show_insights()
        elif choice == "5":
            configure_push()
        elif choice == "6":
            setup_cron()
        elif choice == "7":
            deploy_github()
        elif choice == "0":
            print("\n👋 再见！")
            break
        else:
            print("\n⚠️ 无效选择，请重试")

if __name__ == "__main__":
    asyncio.run(main())
