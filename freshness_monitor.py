#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据新鲜度监控脚本 - Phase 4.4
监控各数据集的最后更新时间，标记过期数据

Author: Agent-2 (数据工程师)
Date: 2026-04-02
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any
import hashlib


class FreshnessMonitor:
    """数据新鲜度监控器"""
    
    def __init__(self, stale_threshold_hours: int = 24):
        """初始化监控器
        
        Args:
            stale_threshold_hours: 过期阈值（小时），默认24小时
        """
        self.stale_threshold = timedelta(hours=stale_threshold_hours)
        self.data_files = {
            'hot_topics': {
                'path': 'hot_topics.json',
                'description': '热点数据',
                'critical': True
            },
            'client_ideas': {
                'path': 'client_ideas.json',
                'description': '客户选题数据',
                'critical': True
            },
            'sku_scenarios': {
                'path': 'sku_scenarios.json',
                'description': 'SKU场景数据',
                'critical': False
            },
            'sku_scenes': {
                'path': 'sku_scenes.json',
                'description': 'SKU场景精简数据',
                'critical': False
            },
            'low_fan_hits': {
                'path': 'low_fan_hits_data.json',
                'description': '低粉爆款数据',
                'critical': False
            },
            'learning_data': {
                'path': 'learning_data.json',
                'description': '学习数据',
                'critical': False
            },
            'dashboard_data': {
                'path': 'dashboard_data.json',
                'description': '仪表盘数据',
                'critical': False
            }
        }
        self.content_hashes = {}
        self.previous_hashes_file = '.freshness_hashes.json'
    
    def get_file_mtime(self, filepath: str) -> datetime:
        """获取文件修改时间
        
        Args:
            filepath: 文件路径
            
        Returns:
            修改时间
        """
        try:
            mtime = os.path.getmtime(filepath)
            return datetime.fromtimestamp(mtime)
        except FileNotFoundError:
            return None
    
    def get_file_content_hash(self, filepath: str) -> str:
        """计算文件内容哈希
        
        Args:
            filepath: 文件路径
            
        Returns:
            MD5哈希值
        """
        try:
            with open(filepath, 'rb') as f:
                content = f.read()
                return hashlib.md5(content).hexdigest()
        except (FileNotFoundError, json.JSONDecodeError):
            return None
    
    def load_previous_hashes(self) -> Dict:
        """加载上次的哈希值
        
        Returns:
            上次的哈希值字典
        """
        try:
            if os.path.exists(self.previous_hashes_file):
                with open(self.previous_hashes_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
        return {}
    
    def save_current_hashes(self, hashes: Dict):
        """保存当前哈希值
        
        Args:
            hashes: 当前哈希值字典
        """
        try:
            with open(self.previous_hashes_file, 'w', encoding='utf-8') as f:
                json.dump(hashes, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"警告: 无法保存哈希文件: {e}")
    
    def get_record_timestamp(self, data: Any, data_type: str) -> datetime:
        """从数据记录中提取最新时间戳
        
        Args:
            data: 数据内容
            data_type: 数据类型
            
        Returns:
            最新时间戳
        """
        if not data:
            return None
        
        timestamps = []
        
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    # 尝试多个可能的时间字段
                    for field in ['created_at', 'updated_at', 'timestamp', 'generated_at']:
                        if field in item:
                            try:
                                ts = datetime.fromisoformat(str(item[field]).replace('Z', '+00:00'))
                                timestamps.append(ts)
                            except (ValueError, TypeError):
                                pass
        elif isinstance(data, dict):
            # 对于字典类型数据（如 sku_scenes.json）
            for field in ['generated_at', 'updated_at', 'timestamp']:
                if field in data:
                    try:
                        ts = datetime.fromisoformat(str(data[field]).replace('Z', '+00:00'))
                        timestamps.append(ts)
                    except (ValueError, TypeError):
                        pass
            
            # 检查嵌套数据
            for key in ['scenarios', 'skus', 'topics', 'ideas']:
                if key in data and isinstance(data[key], list):
                    for item in data[key]:
                        if isinstance(item, dict):
                            for field in ['created_at', 'updated_at']:
                                if field in item:
                                    try:
                                        ts = datetime.fromisoformat(str(item[field]).replace('Z', '+00:00'))
                                        timestamps.append(ts)
                                    except (ValueError, TypeError):
                                        pass
        
        return max(timestamps) if timestamps else None
    
    def check_dataset_freshness(self, dataset_name: str, config: Dict) -> Dict:
        """检查单个数据集的新鲜度
        
        Args:
            dataset_name: 数据集名称
            config: 数据集配置
            
        Returns:
            新鲜度检查结果
        """
        filepath = config['path']
        result = {
            'name': dataset_name,
            'description': config['description'],
            'path': filepath,
            'exists': False,
            'status': 'unknown',
            'file_mtime': None,
            'record_timestamp': None,
            'hours_since_update': None,
            'is_stale': False,
            'content_changed': False,
            'record_count': 0,
            'critical': config['critical']
        }
        
        # 检查文件是否存在
        if not os.path.exists(filepath):
            result['status'] = 'missing'
            result['is_stale'] = True
            return result
        
        result['exists'] = True
        
        # 获取文件修改时间
        file_mtime = self.get_file_mtime(filepath)
        result['file_mtime'] = file_mtime.isoformat() if file_mtime else None
        
        # 计算文件修改时间距离现在的小时数
        if file_mtime:
            hours_since_file_update = (datetime.now() - file_mtime).total_seconds() / 3600
            result['hours_since_file_update'] = round(hours_since_file_update, 2)
        
        # 加载数据并检查内容
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 计算记录数
            if isinstance(data, list):
                result['record_count'] = len(data)
            elif isinstance(data, dict):
                if 'total_count' in data:
                    result['record_count'] = data['total_count']
                elif 'scenarios' in data:
                    result['record_count'] = len(data.get('scenarios', []))
                elif 'skus' in data:
                    result['record_count'] = len(data.get('skus', []))
                elif 'topics' in data:
                    result['record_count'] = len(data.get('topics', []))
                else:
                    result['record_count'] = 1
            
            # 获取记录内的时间戳
            record_ts = self.get_record_timestamp(data, dataset_name)
            if record_ts:
                result['record_timestamp'] = record_ts.isoformat()
                hours_since_record = (datetime.now() - record_ts.replace(tzinfo=None)).total_seconds() / 3600
                result['hours_since_update'] = round(hours_since_record, 2)
            
            # 检查内容是否变化
            current_hash = self.get_file_content_hash(filepath)
            previous_hashes = self.load_previous_hashes()
            result['content_changed'] = previous_hashes.get(dataset_name) != current_hash
            self.content_hashes[dataset_name] = current_hash
            
            # 判断新鲜度状态
            hours_to_check = result['hours_since_update'] or result['hours_since_file_update']
            
            if hours_to_check is not None:
                if hours_to_check > self.stale_threshold.total_seconds() / 3600:
                    result['status'] = 'stale'
                    result['is_stale'] = True
                elif hours_to_check > self.stale_threshold.total_seconds() / 3600 * 0.8:
                    result['status'] = 'warning'
                else:
                    result['status'] = 'fresh'
            else:
                result['status'] = 'no_timestamp'
        
        except json.JSONDecodeError as e:
            result['status'] = 'corrupted'
            result['error'] = str(e)
        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)
        
        return result
    
    def run_freshness_check(self) -> Dict:
        """运行完整的新鲜度检查
        
        Returns:
            完整的新鲜度报告
        """
        check_time = datetime.now()
        results = {}
        
        for dataset_name, config in self.data_files.items():
            results[dataset_name] = self.check_dataset_freshness(dataset_name, config)
        
        # 保存当前哈希值
        self.save_current_hashes(self.content_hashes)
        
        # 汇总统计
        summary = {
            'total_datasets': len(self.data_files),
            'fresh': sum(1 for r in results.values() if r['status'] == 'fresh'),
            'warning': sum(1 for r in results.values() if r['status'] == 'warning'),
            'stale': sum(1 for r in results.values() if r['status'] == 'stale'),
            'missing': sum(1 for r in results.values() if r['status'] == 'missing'),
            'error': sum(1 for r in results.values() if r['status'] in ['error', 'corrupted']),
            'critical_stale': sum(1 for r in results.values() if r['is_stale'] and r['critical'])
        }
        
        # 生成告警
        alerts = []
        for name, result in results.items():
            if result['status'] == 'stale':
                severity = 'critical' if result['critical'] else 'warning'
                alerts.append({
                    'dataset': name,
                    'severity': severity,
                    'message': f"{result['description']}已超过{result['hours_since_update']:.1f}小时未更新",
                    'action': '请检查数据更新流程'
                })
            elif result['status'] == 'missing':
                alerts.append({
                    'dataset': name,
                    'severity': 'critical' if result['critical'] else 'warning',
                    'message': f"{result['description']}文件不存在",
                    'action': '请检查数据采集流程'
                })
            elif result['status'] == 'corrupted':
                alerts.append({
                    'dataset': name,
                    'severity': 'critical',
                    'message': f"{result['description']}文件已损坏",
                    'action': '请修复或恢复数据文件'
                })
        
        report = {
            'check_time': check_time.isoformat(),
            'stale_threshold_hours': self.stale_threshold.total_seconds() / 3600,
            'summary': summary,
            'datasets': results,
            'alerts': alerts,
            'status': 'ok' if summary['critical_stale'] == 0 and summary['error'] == 0 else 'issue'
        }
        
        return report
    
    def generate_report(self, output_format: str = 'json') -> str:
        """生成新鲜度报告
        
        Args:
            output_format: 输出格式 (json, markdown)
            
        Returns:
            报告内容
        """
        report = self.run_freshness_check()
        
        if output_format == 'json':
            return json.dumps(report, ensure_ascii=False, indent=2)
        
        elif output_format == 'markdown':
            lines = [
                "# 数据新鲜度监控报告",
                "",
                f"**检查时间**: {report['check_time']}",
                f"**过期阈值**: {report['stale_threshold_hours']}小时",
                "",
                "## 汇总统计",
                "",
                f"| 状态 | 数量 |",
                f"|------|------|",
                f"| ✅ 新鲜 | {report['summary']['fresh']} |",
                f"| ⚠️ 即将过期 | {report['summary']['warning']} |",
                f"| ❌ 已过期 | {report['summary']['stale']} |",
                f"| 📁 文件缺失 | {report['summary']['missing']} |",
                f"| ⚠️ 错误 | {report['summary']['error']} |",
                "",
                "## 数据集详情",
                "",
                "| 数据集 | 状态 | 记录数 | 最后更新 | 过期时长 |",
                "|--------|------|--------|----------|----------|"
            ]
            
            for name, result in report['datasets'].items():
                status_icon = {
                    'fresh': '✅',
                    'warning': '⚠️',
                    'stale': '❌',
                    'missing': '📁',
                    'error': '⚠️',
                    'corrupted': '💥',
                    'no_timestamp': '❓'
                }.get(result['status'], '❓')
                
                hours = result.get('hours_since_update') or result.get('hours_since_file_update')
                hours_str = f"{hours:.1f}h" if hours else 'N/A'
                
                lines.append(
                    f"| {result['description']} | {status_icon} {result['status']} | "
                    f"{result['record_count']} | {result.get('record_timestamp', 'N/A')[:19] if result.get('record_timestamp') else 'N/A'} | "
                    f"{hours_str} |"
                )
            
            if report['alerts']:
                lines.extend([
                    "",
                    "## 告警信息",
                    ""
                ])
                for alert in report['alerts']:
                    severity_icon = '🔴' if alert['severity'] == 'critical' else '🟡'
                    lines.append(f"- {severity_icon} **{alert['dataset']}**: {alert['message']}")
                    lines.append(f"  - 建议: {alert['action']}")
            
            return '\n'.join(lines)
        
        return json.dumps(report, ensure_ascii=False, indent=2)


def main():
    """主函数"""
    print("=" * 60)
    print("数据新鲜度监控 - Phase 4.4")
    print("=" * 60)
    
    monitor = FreshnessMonitor(stale_threshold_hours=24)
    
    # 生成JSON报告
    report = monitor.run_freshness_check()
    
    # 保存JSON报告
    with open('freshness_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ JSON报告已保存: freshness_report.json")
    
    # 生成Markdown报告
    md_report = monitor.generate_report('markdown')
    with open('freshness_report.md', 'w', encoding='utf-8') as f:
        f.write(md_report)
    
    print(f"✅ Markdown报告已保存: freshness_report.md")
    
    # 控制台输出摘要
    print("\n" + "=" * 60)
    print("监控摘要")
    print("=" * 60)
    print(f"检查时间: {report['check_time']}")
    print(f"总体状态: {'✅ 正常' if report['status'] == 'ok' else '⚠️ 存在问题'}")
    print(f"\n数据集状态:")
    print(f"  - 新鲜: {report['summary']['fresh']}")
    print(f"  - 即将过期: {report['summary']['warning']}")
    print(f"  - 已过期: {report['summary']['stale']}")
    print(f"  - 文件缺失: {report['summary']['missing']}")
    print(f"  - 错误: {report['summary']['error']}")
    
    if report['alerts']:
        print(f"\n⚠️ 告警 ({len(report['alerts'])}条):")
        for alert in report['alerts']:
            icon = '🔴' if alert['severity'] == 'critical' else '🟡'
            print(f"  {icon} {alert['dataset']}: {alert['message']}")
    
    print("\n" + "=" * 60)
    
    return report


if __name__ == '__main__':
    main()
