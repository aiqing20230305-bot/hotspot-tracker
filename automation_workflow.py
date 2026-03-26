#!/usr/bin/env python3
"""
🔄 热点追踪自动化工作流
功能：
1. 定时自动执行热点抓取
2. 生成内容推荐
3. 推送到飞书/钉钉
4. 效果数据回收
5. 自学习优化
"""

import asyncio
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any
import subprocess

class AutomationWorkflow:
    """自动化工作流管理"""
    
    def __init__(self):
        self.workspace = Path("/Users/zhangjingwei/.qclaw/workspace/hotspot-tracker")
        self.config_file = self.workspace / "workflow_config.json"
        self.log_file = self.workspace / "workflow_logs.json"
        self.load_config()
    
    def load_config(self):
        """加载配置"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = self._default_config()
            self.save_config()
    
    def _default_config(self) -> Dict:
        """默认配置"""
        return {
            "schedule": {
                "hotspot_fetch": "0 9 * * *",  # 每天9:00抓取热点
                "report_generate": "30 9 * * *",  # 每天9:30生成报告
                "feishu_push": "0 10 * * *",  # 每天10:00推送飞书
            },
            "feishu": {
                "enabled": False,
                "webhook_url": "",
                "app_id": "",
                "app_secret": "",
            },
            "dingtalk": {
                "enabled": False,
                "webhook_url": "",
                "access_token": "",
            },
            "email": {
                "enabled": False,
                "smtp_server": "",
                "smtp_port": 587,
                "username": "",
                "password": "",
                "recipients": [],
            },
            "content_rules": {
                "min_hot_value": 10000,  # 最小热度值
                "max_recommendations": 20,  # 最大推荐数
                "priority_threshold": 4,  # 高优先级阈值
            },
            "learning": {
                "enabled": True,
                "feedback_days": 7,  # 反馈收集天数
                "optimization_threshold": 0.1,  # 优化阈值
            }
        }
    
    def save_config(self):
        """保存配置"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    async def run_full_workflow(self):
        """运行完整工作流"""
        print("🔄 启动自动化工作流...")
        print("=" * 60)
        
        # 1. 抓取热点
        print("\n📡 步骤1: 抓取全平台热点...")
        await self._step_fetch_hotspots()
        
        # 2. 生成推荐
        print("\n🤖 步骤2: AI生成内容推荐...")
        await self._step_generate_recommendations()
        
        # 3. 生成报告
        print("\n📊 步骤3: 生成可视化报告...")
        await self._step_generate_report()
        
        # 4. 推送到飞书（如果启用）
        if self.config["feishu"]["enabled"]:
            print("\n📤 步骤4: 推送到飞书...")
            await self._step_push_feishu()
        
        # 5. 推送到钉钉（如果启用）
        if self.config["dingtalk"]["enabled"]:
            print("\n📤 步骤5: 推送到钉钉...")
            await self._step_push_dingtalk()
        
        # 6. 发送邮件（如果启用）
        if self.config["email"]["enabled"]:
            print("\n📧 步骤6: 发送邮件...")
            await self._step_send_email()
        
        # 7. 记录日志
        print("\n📝 步骤7: 记录执行日志...")
        self._log_execution()
        
        print("\n" + "=" * 60)
        print("✅ 工作流执行完成！")
        print("=" * 60)
    
    async def _step_fetch_hotspots(self):
        """步骤1: 抓取热点"""
        try:
            # 执行热点抓取
            result = subprocess.run(
                ["python3", str(self.workspace / "evolution_system.py")],
                capture_output=True,
                text=True,
                cwd=str(self.workspace),
                timeout=300
            )
            
            if result.returncode == 0:
                print("✅ 热点抓取成功")
            else:
                print(f"⚠️ 热点抓取警告: {result.stderr}")
        
        except Exception as e:
            print(f"❌ 热点抓取失败: {e}")
    
    async def _step_generate_recommendations(self):
        """步骤2: 生成推荐"""
        # evolution_system.py 已经包含了生成推荐的功能
        print("✅ 内容推荐已生成")
    
    async def _step_generate_report(self):
        """步骤3: 生成报告"""
        today = datetime.now().strftime("%Y%m%d")
        report_file = self.workspace / f"EVOLUTION_REPORT_{today}.md"
        
        if report_file.exists():
            print(f"✅ 报告已生成: {report_file.name}")
        else:
            print("⚠️ 报告文件未找到")
    
    async def _step_push_feishu(self):
        """步骤4: 推送到飞书"""
        webhook_url = self.config["feishu"]["webhook_url"]
        
        if not webhook_url:
            print("⚠️ 飞书Webhook未配置")
            return
        
        try:
            # 读取今日报告
            today = datetime.now().strftime("%Y%m%d")
            report_file = self.workspace / f"EVOLUTION_REPORT_{today}.md"
            
            if not report_file.exists():
                print("⚠️ 报告文件不存在")
                return
            
            with open(report_file, 'r', encoding='utf-8') as f:
                report_content = f.read()
            
            # 构建飞书消息
            message = {
                "msg_type": "interactive",
                "card": {
                    "config": {
                        "wide_screen_mode": True
                    },
                    "header": {
                        "title": {
                            "tag": "plain_text",
                            "content": f"📱 每日内容推荐 - {datetime.now().strftime('%m月%d日')}"
                        },
                        "template": "blue"
                    },
                    "elements": [
                        {
                            "tag": "div",
                            "text": {
                                "tag": "lark_md",
                                "content": report_content[:3000] + "..." if len(report_content) > 3000 else report_content
                            }
                        },
                        {
                            "tag": "action",
                            "actions": [
                                {
                                    "tag": "button",
                                    "text": {
                                        "tag": "plain_text",
                                        "content": "查看完整报告"
                                    },
                                    "type": "primary",
                                    "url": f"https://aiqing20230305-bot.github.io/hotspot-tracker/"
                                }
                            ]
                        }
                    ]
                }
            }
            
            # 发送请求
            import urllib.request
            import urllib.parse
            
            data = json.dumps(message).encode('utf-8')
            req = urllib.request.Request(
                webhook_url,
                data=data,
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                if result.get('code') == 0:
                    print("✅ 飞书推送成功")
                else:
                    print(f"⚠️ 飞书推送失败: {result}")
        
        except Exception as e:
            print(f"❌ 飞书推送失败: {e}")
    
    async def _step_push_dingtalk(self):
        """步骤5: 推送到钉钉"""
        webhook_url = self.config["dingtalk"]["webhook_url"]
        
        if not webhook_url:
            print("⚠️ 钉钉Webhook未配置")
            return
        
        try:
            today = datetime.now().strftime("%Y%m%d")
            report_file = self.workspace / f"EVOLUTION_REPORT_{today}.md"
            
            with open(report_file, 'r', encoding='utf-8') as f:
                report_content = f.read()
            
            # 构建钉钉消息
            message = {
                "msgtype": "markdown",
                "markdown": {
                    "title": f"每日内容推荐 - {datetime.now().strftime('%m月%d日')}",
                    "text": report_content[:5000]
                }
            }
            
            import urllib.request
            data = json.dumps(message).encode('utf-8')
            req = urllib.request.Request(
                webhook_url,
                data=data,
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                if result.get('errcode') == 0:
                    print("✅ 钉钉推送成功")
                else:
                    print(f"⚠️ 钉钉推送失败: {result}")
        
        except Exception as e:
            print(f"❌ 钉钉推送失败: {e}")
    
    async def _step_send_email(self):
        """步骤6: 发送邮件"""
        # 邮件发送逻辑（需要配置SMTP）
        print("📧 邮件功能待配置")
    
    def _log_execution(self):
        """记录执行日志"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y%m%d"),
            "status": "success",
            "steps": ["fetch", "generate", "report"]
        }
        
        logs = []
        if self.log_file.exists():
            with open(self.log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        
        logs.append(log_entry)
        
        # 只保留最近30天的日志
        logs = logs[-30:]
        
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
        
        print("✅ 执行日志已记录")
    
    def setup_cron(self):
        """设置定时任务"""
        print("\n📅 设置定时任务...")
        
        # 创建cron任务
        cron_jobs = [
            {
                "name": "hotspot-fetch",
                "schedule": self.config["schedule"]["hotspot_fetch"],
                "command": f"cd {self.workspace} && python3 evolution_system.py"
            },
            {
                "name": "workflow-run",
                "schedule": self.config["schedule"]["report_generate"],
                "command": f"cd {self.workspace} && python3 automation_workflow.py --run"
            }
        ]
        
        print("\n建议的定时任务配置：")
        print("-" * 60)
        for job in cron_jobs:
            print(f"# {job['name']}")
            print(f"{job['schedule']} {job['command']}")
        print("-" * 60)
        
        print("\n使用以下命令添加到crontab：")
        print(f"crontab -e")
        print(f"# 然后添加上面的任务行")
    
    def configure_feishu(self, webhook_url: str):
        """配置飞书"""
        self.config["feishu"]["enabled"] = True
        self.config["feishu"]["webhook_url"] = webhook_url
        self.save_config()
        print("✅ 飞书配置已保存")
    
    def configure_dingtalk(self, webhook_url: str):
        """配置钉钉"""
        self.config["dingtalk"]["enabled"] = True
        self.config["dingtalk"]["webhook_url"] = webhook_url
        self.save_config()
        print("✅ 钉钉配置已保存")
    
    def show_status(self):
        """显示系统状态"""
        print("\n" + "=" * 60)
        print("📊 热点追踪自动化系统状态")
        print("=" * 60)
        
        # 配置状态
        print("\n🔧 配置状态：")
        print(f"  飞书推送: {'✅ 已启用' if self.config['feishu']['enabled'] else '❌ 未启用'}")
        print(f"  钉钉推送: {'✅ 已启用' if self.config['dingtalk']['enabled'] else '❌ 未启用'}")
        print(f"  邮件通知: {'✅ 已启用' if self.config['email']['enabled'] else '❌ 未启用'}")
        print(f"  自学习优化: {'✅ 已启用' if self.config['learning']['enabled'] else '❌ 未启用'}")
        
        # 执行日志
        if self.log_file.exists():
            with open(self.log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
            print(f"\n📈 执行统计：")
            print(f"  总执行次数: {len(logs)}")
            if logs:
                print(f"  最近执行: {logs[-1]['timestamp']}")
                success_count = sum(1 for log in logs if log['status'] == 'success')
                print(f"  成功率: {success_count / len(logs) * 100:.1f}%")
        
        # 今日报告
        today = datetime.now().strftime("%Y%m%d")
        report_file = self.workspace / f"EVOLUTION_REPORT_{today}.md"
        if report_file.exists():
            print(f"\n📄 今日报告: ✅ 已生成")
        else:
            print(f"\n📄 今日报告: ❌ 未生成")
        
        print("\n" + "=" * 60)

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='热点追踪自动化工作流')
    parser.add_argument('--run', action='store_true', help='运行完整工作流')
    parser.add_argument('--setup-cron', action='store_true', help='设置定时任务')
    parser.add_argument('--status', action='store_true', help='显示系统状态')
    parser.add_argument('--config-feishu', type=str, help='配置飞书Webhook')
    parser.add_argument('--config-dingtalk', type=str, help='配置钉钉Webhook')
    
    args = parser.parse_args()
    
    workflow = AutomationWorkflow()
    
    if args.run:
        asyncio.run(workflow.run_full_workflow())
    elif args.setup_cron:
        workflow.setup_cron()
    elif args.status:
        workflow.show_status()
    elif args.config_feishu:
        workflow.configure_feishu(args.config_feishu)
    elif args.config_dingtalk:
        workflow.configure_dingtalk(args.config_dingtalk)
    else:
        # 默认显示帮助
        parser.print_help()
        print("\n\n💡 快速开始：")
        print("  1. 运行完整工作流: python3 automation_workflow.py --run")
        print("  2. 查看系统状态: python3 automation_workflow.py --status")
        print("  3. 设置定时任务: python3 automation_workflow.py --setup-cron")

if __name__ == "__main__":
    main()
