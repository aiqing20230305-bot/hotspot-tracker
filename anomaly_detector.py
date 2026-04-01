#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
异常数据自动检测脚本 - Phase 4.5
检测标题过短、数据缺失、格式错误等问题，支持自动修复

Author: Agent-2 (数据工程师)
Date: 2026-04-02
"""

import json
import re
import os
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class Anomaly:
    """异常数据结构"""
    dataset: str
    index: int
    record_id: str
    type: str
    severity: str  # critical, warning, info
    field: str
    value: Any
    message: str
    auto_fixable: bool = False
    fixed: bool = False
    fix_action: str = ""


class AnomalyDetector:
    """异常数据检测器"""
    
    def __init__(self, auto_fix: bool = True):
        """初始化检测器
        
        Args:
            auto_fix: 是否自动修复可修复的问题
        """
        self.auto_fix = auto_fix
        self.anomalies: List[Anomaly] = []
        self.fixed_count = 0
        
        # 配置规则
        self.rules = {
            'hot_topics': {
                'required_fields': ['title', 'hot_value', 'platform'],
                'title_min_length': 5,
                'title_max_length': 100,
                'valid_platforms': ['微博', '抖音', '知乎', 'B站', '小红书', '微博/全网', '抖音/全网', '全网', '其他'],
                'hot_value_min': 0,
                'hot_value_max': 10000000000  # 100亿
            },
            'client_ideas': {
                'required_fields': ['title', 'client', 'platform', 'status'],
                'title_min_length': 10,
                'title_max_length': 200,
                'valid_status': ['pending', 'approved', 'rejected', 'published', 'draft'],
                'valid_platforms': ['全平台', '抖音', '小红书', '微博', 'B站', '知乎', '微信公众号']
            },
            'sku_scenarios': {
                'required_fields': ['id', 'client', 'product', 'scenario_type'],
                'description_min_length': 10,
                'valid_scenario_types': ['开箱测评', '产品讲解', '使用教程', '产品对比', '场景应用', '问题解决']
            },
            'sku_scenes': {
                'required_fields': ['sku_name', 'client', 'scenarios']
            },
            'low_fan_hits': {
                'required_fields': ['title', 'likes', 'platform']
            }
        }
    
    def detect_title_too_short(self, title: str, min_length: int) -> Tuple[bool, int]:
        """检测标题是否过短
        
        Args:
            title: 标题
            min_length: 最小长度
            
        Returns:
            (是否过短, 实际长度)
        """
        if not title:
            return True, 0
        actual_length = len(str(title).strip())
        return actual_length < min_length, actual_length
    
    def detect_title_too_long(self, title: str, max_length: int) -> Tuple[bool, int]:
        """检测标题是否过长
        
        Args:
            title: 标题
            max_length: 最大长度
            
        Returns:
            (是否过长, 实际长度)
        """
        if not title:
            return False, 0
        actual_length = len(str(title).strip())
        return actual_length > max_length, actual_length
    
    def detect_missing_fields(self, record: Dict, required_fields: List[str]) -> List[str]:
        """检测缺失字段
        
        Args:
            record: 数据记录
            required_fields: 必需字段列表
            
        Returns:
            缺失的字段列表
        """
        missing = []
        for field in required_fields:
            if field not in record:
                missing.append(field)
            elif record[field] is None:
                missing.append(field)
            elif isinstance(record[field], str) and record[field].strip() == '':
                missing.append(field)
            elif isinstance(record[field], (list, dict)) and len(record[field]) == 0:
                # 空列表或空字典也视为缺失
                if field in ['keywords', 'industries', 'scenarios']:
                    pass  # 这些字段允许为空
                else:
                    missing.append(field)
        return missing
    
    def detect_format_error(self, value: Any, field: str, rules: Dict) -> Tuple[bool, str]:
        """检测格式错误
        
        Args:
            value: 字段值
            field: 字段名
            rules: 检测规则
            
        Returns:
            (是否有错误, 错误信息)
        """
        if field == 'hot_value':
            if not isinstance(value, (int, float)):
                return True, f"hot_value应为数字，实际为{type(value).__name__}"
            if 'hot_value_min' in rules and value < rules['hot_value_min']:
                return True, f"hot_value {value} 小于最小值 {rules['hot_value_min']}"
            if 'hot_value_max' in rules and value > rules['hot_value_max']:
                return True, f"hot_value {value} 大于最大值 {rules['hot_value_max']}"
        
        elif field == 'platform':
            if 'valid_platforms' in rules:
                valid = rules['valid_platforms']
                # 处理多平台情况（如 "微博/全网"）
                platforms = str(value).split('/') if value else []
                for p in platforms:
                    p_clean = p.strip()
                    if p_clean and p_clean not in valid and '其他' not in valid:
                        # 允许未知平台，但记录警告
                        return False, f"平台 '{p_clean}' 不在预设列表中"
        
        elif field == 'status':
            if 'valid_status' in rules and value not in rules['valid_status']:
                return True, f"status '{value}' 不是有效值，应为 {rules['valid_status']}"
        
        elif field == 'scenario_type':
            if 'valid_scenario_types' in rules and value not in rules['valid_scenario_types']:
                return False, f"scenario_type '{value}' 不在预设列表中"
        
        elif field == 'url':
            if value and not str(value).startswith(('http://', 'https://', 'www.')):
                return True, f"url格式错误: {value}"
        
        elif field == 'created_at' or field == 'updated_at':
            if value:
                try:
                    # 尝试解析ISO格式
                    datetime.fromisoformat(str(value).replace('Z', '+00:00'))
                except (ValueError, TypeError):
                    return True, f"时间格式错误: {value}"
        
        return False, ""
    
    def detect_duplicates(self, records: List[Dict], key_field: str = 'title') -> List[Tuple[int, int, Any]]:
        """检测重复数据
        
        Args:
            records: 数据列表
            key_field: 用于判断重复的字段
            
        Returns:
            重复项列表 [(index1, index2, key_value), ...]
        """
        seen = {}
        duplicates = []
        
        for i, record in enumerate(records):
            key_value = record.get(key_field, '')
            if key_value:
                if key_value in seen:
                    duplicates.append((seen[key_value], i, key_value))
                else:
                    seen[key_value] = i
        
        return duplicates
    
    def detect_invalid_references(self, record: Dict, ref_data: Dict) -> List[str]:
        """检测无效引用
        
        Args:
            record: 数据记录
            ref_data: 引用数据
            
        Returns:
            无效引用列表
        """
        invalid_refs = []
        
        # 检查 hot_topic_id 是否有效
        if 'hot_topic_id' in record:
            hot_topic_id = record['hot_topic_id']
            if hot_topic_id and ref_data.get('hot_topic_ids'):
                if hot_topic_id not in ref_data['hot_topic_ids']:
                    invalid_refs.append(f"hot_topic_id '{hot_topic_id}' 不存在")
        
        return invalid_refs
    
    def analyze_hot_topics(self, topics: List[Dict]) -> List[Anomaly]:
        """分析热点数据
        
        Args:
            topics: 热点列表
            
        Returns:
            异常列表
        """
        anomalies = []
        rules = self.rules['hot_topics']
        
        for i, topic in enumerate(topics):
            record_id = topic.get('id', f'index_{i}')
            
            # 检查标题长度
            title = topic.get('title', '')
            is_short, actual_len = self.detect_title_too_short(title, rules['title_min_length'])
            if is_short:
                severity = 'critical' if actual_len < 3 else 'warning'
                anomalies.append(Anomaly(
                    dataset='hot_topics',
                    index=i,
                    record_id=record_id,
                    type='标题过短',
                    severity=severity,
                    field='title',
                    value=title,
                    message=f"标题长度 {actual_len} 小于最小值 {rules['title_min_length']}",
                    auto_fixable=False,
                    fix_action="需要人工补充标题内容"
                ))
            
            is_long, actual_len = self.detect_title_too_long(title, rules['title_max_length'])
            if is_long:
                anomalies.append(Anomaly(
                    dataset='hot_topics',
                    index=i,
                    record_id=record_id,
                    type='标题过长',
                    severity='warning',
                    field='title',
                    value=title,
                    message=f"标题长度 {actual_len} 大于最大值 {rules['title_max_length']}",
                    auto_fixable=True,
                    fix_action=f"建议截断到 {rules['title_max_length']} 字符"
                ))
            
            # 检查缺失字段
            missing = self.detect_missing_fields(topic, rules['required_fields'])
            for field in missing:
                anomalies.append(Anomaly(
                    dataset='hot_topics',
                    index=i,
                    record_id=record_id,
                    type='字段缺失',
                    severity='critical',
                    field=field,
                    value=None,
                    message=f"必需字段 '{field}' 缺失",
                    auto_fixable=False,
                    fix_action="需要人工补充字段值"
                ))
            
            # 检查格式错误
            for field in ['hot_value', 'platform', 'url', 'created_at']:
                if field in topic:
                    has_error, error_msg = self.detect_format_error(topic[field], field, rules)
                    if has_error:
                        anomalies.append(Anomaly(
                            dataset='hot_topics',
                            index=i,
                            record_id=record_id,
                            type='格式错误',
                            severity='warning',
                            field=field,
                            value=topic[field],
                            message=error_msg,
                            auto_fixable=False,
                            fix_action="需要人工修正格式"
                        ))
            
            # 检查关键词是否为空
            if 'keywords' in topic and not topic['keywords']:
                anomalies.append(Anomaly(
                    dataset='hot_topics',
                    index=i,
                    record_id=record_id,
                    type='关键词为空',
                    severity='info',
                    field='keywords',
                    value=[],
                    message="关键词列表为空，可能影响推荐效果",
                    auto_fixable=True,
                    fix_action="可从标题中提取关键词"
                ))
        
        # 检查重复
        duplicates = self.detect_duplicates(topics, 'title')
        for idx1, idx2, title in duplicates:
            anomalies.append(Anomaly(
                dataset='hot_topics',
                index=idx2,
                record_id=topics[idx2].get('id', f'index_{idx2}'),
                type='重复数据',
                severity='warning',
                field='title',
                value=title,
                message=f"与索引 {idx1} 的标题重复",
                auto_fixable=True,
                fix_action="建议删除重复项"
            ))
        
        return anomalies
    
    def analyze_client_ideas(self, ideas: List[Dict]) -> List[Anomaly]:
        """分析客户选题数据
        
        Args:
            ideas: 选题列表
            
        Returns:
            异常列表
        """
        anomalies = []
        rules = self.rules['client_ideas']
        
        for i, idea in enumerate(ideas):
            record_id = idea.get('id', f'index_{i}')
            
            # 检查标题
            title = idea.get('title', '')
            is_short, actual_len = self.detect_title_too_short(title, rules['title_min_length'])
            if is_short:
                severity = 'critical' if actual_len < 5 else 'warning'
                anomalies.append(Anomaly(
                    dataset='client_ideas',
                    index=i,
                    record_id=record_id,
                    type='标题过短',
                    severity=severity,
                    field='title',
                    value=title,
                    message=f"选题标题长度 {actual_len} 小于最小值 {rules['title_min_length']}",
                    auto_fixable=False
                ))
            
            # 检查缺失字段
            missing = self.detect_missing_fields(idea, rules['required_fields'])
            for field in missing:
                # client 可能是嵌套对象
                if field == 'client' and 'client' in idea and isinstance(idea['client'], dict):
                    continue
                anomalies.append(Anomaly(
                    dataset='client_ideas',
                    index=i,
                    record_id=record_id,
                    type='字段缺失',
                    severity='critical',
                    field=field,
                    value=None,
                    message=f"必需字段 '{field}' 缺失",
                    auto_fixable=False
                ))
            
            # 检查状态值
            if 'status' in idea:
                has_error, error_msg = self.detect_format_error(idea['status'], 'status', rules)
                if has_error:
                    anomalies.append(Anomaly(
                        dataset='client_ideas',
                        index=i,
                        record_id=record_id,
                        type='状态值无效',
                        severity='warning',
                        field='status',
                        value=idea['status'],
                        message=error_msg,
                        auto_fixable=True,
                        fix_action=f"建议设置为 'pending'"
                    ))
            
            # 检查平台
            if 'platform' in idea:
                has_error, error_msg = self.detect_format_error(idea['platform'], 'platform', rules)
                if has_error:
                    anomalies.append(Anomaly(
                        dataset='client_ideas',
                        index=i,
                        record_id=record_id,
                        type='平台值无效',
                        severity='info',
                        field='platform',
                        value=idea['platform'],
                        message=error_msg,
                        auto_fixable=False
                    ))
        
        return anomalies
    
    def analyze_sku_scenarios(self, scenarios: List[Dict]) -> List[Anomaly]:
        """分析SKU场景数据
        
        Args:
            scenarios: SKU场景列表
            
        Returns:
            异常列表
        """
        anomalies = []
        rules = self.rules['sku_scenarios']
        
        for i, scenario in enumerate(scenarios):
            record_id = scenario.get('id', f'index_{i}')
            
            # 检查缺失字段
            missing = self.detect_missing_fields(scenario, rules['required_fields'])
            for field in missing:
                anomalies.append(Anomaly(
                    dataset='sku_scenarios',
                    index=i,
                    record_id=record_id,
                    type='字段缺失',
                    severity='critical',
                    field=field,
                    value=None,
                    message=f"必需字段 '{field}' 缺失",
                    auto_fixable=False
                ))
            
            # 检查描述长度
            description = scenario.get('description', '')
            if description:
                is_short, actual_len = self.detect_title_too_short(description, rules['description_min_length'])
                if is_short:
                    anomalies.append(Anomaly(
                        dataset='sku_scenarios',
                        index=i,
                        record_id=record_id,
                        type='描述过短',
                        severity='info',
                        field='description',
                        value=description,
                        message=f"描述长度 {actual_len} 较短",
                        auto_fixable=False
                    ))
            
            # 检查关键词是否为空
            if 'keywords' in scenario and not scenario['keywords']:
                anomalies.append(Anomaly(
                    dataset='sku_scenarios',
                    index=i,
                    record_id=record_id,
                    type='关键词为空',
                    severity='info',
                    field='keywords',
                    value=[],
                    message="关键词列表为空",
                    auto_fixable=True,
                    fix_action="可从描述中提取关键词"
                ))
        
        return anomalies
    
    def auto_fix_keyword_extraction(self, text: str) -> List[str]:
        """从文本中自动提取关键词
        
        Args:
            text: 源文本
            
        Returns:
            提取的关键词列表
        """
        # 简单的关键词提取：提取中文词汇
        # 实际项目中可使用jieba等库
        keywords = []
        
        # 移除标点符号
        text = re.sub(r'[，。！？、；：""''（）【】\[\]]', ' ', text)
        
        # 提取2-4字的中文词
        pattern = r'[\u4e00-\u9fa5]{2,4}'
        matches = re.findall(pattern, text)
        
        # 去重并取前5个
        seen = set()
        for match in matches:
            if match not in seen and len(match) >= 2:
                keywords.append(match)
                seen.add(match)
                if len(keywords) >= 5:
                    break
        
        return keywords
    
    def apply_auto_fixes(self, data: Dict, anomalies: List[Anomaly]) -> Tuple[Dict, int]:
        """应用自动修复
        
        Args:
            data: 原始数据
            anomalies: 异常列表
            
        Returns:
            (修复后的数据, 修复数量)
        """
        fixed_count = 0
        
        for anomaly in anomalies:
            if not anomaly.auto_fixable:
                continue
            
            dataset = anomaly.dataset
            index = anomaly.index
            field = anomaly.field
            
            if dataset not in data:
                continue
            
            records = data[dataset]
            if not isinstance(records, list) or index >= len(records):
                continue
            
            record = records[index]
            
            # 应用修复
            if anomaly.type == '关键词为空':
                # 从标题或描述提取关键词
                source_text = record.get('title') or record.get('description', '')
                if source_text:
                    new_keywords = self.auto_fix_keyword_extraction(source_text)
                    if new_keywords:
                        record[field] = new_keywords
                        anomaly.fixed = True
                        fixed_count += 1
            
            elif anomaly.type == '状态值无效':
                if field == 'status':
                    record[field] = 'pending'
                    anomaly.fixed = True
                    fixed_count += 1
            
            elif anomaly.type == '标题过长':
                max_len = 100 if dataset == 'hot_topics' else 200
                if record.get('title') and len(record['title']) > max_len:
                    record['title'] = record['title'][:max_len] + '...'
                    anomaly.fixed = True
                    fixed_count += 1
        
        self.fixed_count = fixed_count
        return data, fixed_count
    
    def run_detection(self, data_paths: Dict[str, str] = None) -> Dict:
        """运行完整检测
        
        Args:
            data_paths: 数据文件路径字典
            
        Returns:
            检测报告
        """
        if data_paths is None:
            data_paths = {
                'hot_topics': 'hot_topics.json',
                'client_ideas': 'client_ideas.json',
                'sku_scenarios': 'sku_scenarios.json'
            }
        
        all_anomalies = []
        data = {}
        
        # 加载并分析每个数据集
        for dataset_name, filepath in data_paths.items():
            if not os.path.exists(filepath):
                all_anomalies.append(Anomaly(
                    dataset=dataset_name,
                    index=-1,
                    record_id='N/A',
                    type='文件缺失',
                    severity='critical',
                    field='file',
                    value=filepath,
                    message=f"数据文件不存在: {filepath}",
                    auto_fixable=False
                ))
                continue
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    dataset_data = json.load(f)
                
                # 处理嵌套数据结构
                if isinstance(dataset_data, dict):
                    if 'scenarios' in dataset_data:
                        records = dataset_data['scenarios']
                    elif 'topics' in dataset_data:
                        records = dataset_data['topics']
                    elif 'ideas' in dataset_data:
                        records = dataset_data['ideas']
                    else:
                        records = []
                else:
                    records = dataset_data
                
                data[dataset_name] = records
                
                # 分析数据
                if dataset_name == 'hot_topics':
                    anomalies = self.analyze_hot_topics(records)
                elif dataset_name == 'client_ideas':
                    anomalies = self.analyze_client_ideas(records)
                elif dataset_name == 'sku_scenarios':
                    anomalies = self.analyze_sku_scenarios(records)
                else:
                    anomalies = []
                
                all_anomalies.extend(anomalies)
                
            except json.JSONDecodeError as e:
                all_anomalies.append(Anomaly(
                    dataset=dataset_name,
                    index=-1,
                    record_id='N/A',
                    type='JSON解析错误',
                    severity='critical',
                    field='file',
                    value=str(e),
                    message=f"JSON文件解析失败: {filepath}",
                    auto_fixable=False
                ))
        
        # 应用自动修复
        if self.auto_fix:
            data, fixed_count = self.apply_auto_fixes(data, all_anomalies)
        
        # 生成报告
        severity_counts = {'critical': 0, 'warning': 0, 'info': 0}
        type_counts = {}
        
        for anomaly in all_anomalies:
            severity_counts[anomaly.severity] += 1
            type_counts[anomaly.type] = type_counts.get(anomaly.type, 0) + 1
        
        report = {
            'check_time': datetime.now().isoformat(),
            'total_issues': len(all_anomalies),
            'severity_counts': severity_counts,
            'type_counts': type_counts,
            'auto_fix_enabled': self.auto_fix,
            'fixed_count': self.fixed_count if self.auto_fix else 0,
            'anomalies': [
                {
                    'dataset': a.dataset,
                    'index': a.index,
                    'record_id': a.record_id,
                    'type': a.type,
                    'severity': a.severity,
                    'field': a.field,
                    'value': str(a.value)[:100] if a.value else None,
                    'message': a.message,
                    'auto_fixable': a.auto_fixable,
                    'fixed': a.fixed if self.auto_fix else False,
                    'fix_action': a.fix_action
                }
                for a in all_anomalies
            ],
            'summary': {
                'datasets_checked': len(data_paths),
                'datasets_with_issues': len(set(a.dataset for a in all_anomalies if a.dataset)),
                'recommendation': self._generate_recommendation(all_anomalies)
            }
        }
        
        return report, data
    
    def _generate_recommendation(self, anomalies: List[Anomaly]) -> str:
        """生成修复建议
        
        Args:
            anomalies: 异常列表
            
        Returns:
            建议文本
        """
        critical_count = sum(1 for a in anomalies if a.severity == 'critical')
        warning_count = sum(1 for a in anomalies if a.severity == 'warning')
        
        if critical_count > 0:
            return f"发现 {critical_count} 个严重问题，建议立即处理。"
        elif warning_count > 0:
            return f"发现 {warning_count} 个警告问题，建议尽快处理。"
        elif anomalies:
            return "数据质量良好，仅有少量信息提示。"
        else:
            return "数据质量优秀，未发现异常。"
    
    def save_fixed_data(self, data: Dict, data_paths: Dict[str, str]):
        """保存修复后的数据
        
        Args:
            data: 修复后的数据
            data_paths: 数据文件路径字典
        """
        for dataset_name, filepath in data_paths.items():
            if dataset_name not in data:
                continue
            
            try:
                # 读取原始文件结构
                with open(filepath, 'r', encoding='utf-8') as f:
                    original = json.load(f)
                
                # 保持原始结构
                if isinstance(original, dict):
                    if 'scenarios' in original:
                        original['scenarios'] = data[dataset_name]
                    elif 'topics' in original:
                        original['topics'] = data[dataset_name]
                    elif 'ideas' in original:
                        original['ideas'] = data[dataset_name]
                    
                    # 更新时间戳
                    original['updated_at'] = datetime.now().isoformat()
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        json.dump(original, f, ensure_ascii=False, indent=2)
                else:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        json.dump(data[dataset_name], f, ensure_ascii=False, indent=2)
                
                print(f"✅ 已保存修复后的数据: {filepath}")
            
            except Exception as e:
                print(f"❌ 保存失败 {filepath}: {e}")


def main():
    """主函数"""
    print("=" * 60)
    print("异常数据自动检测 - Phase 4.5")
    print("=" * 60)
    
    detector = AnomalyDetector(auto_fix=True)
    
    # 运行检测
    report, fixed_data = detector.run_detection()
    
    # 保存报告
    with open('anomaly_report.json', 'w', encoding='utf-8') as f:
        # 移除 fixed_data，只保存报告
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 检测报告已保存: anomaly_report.json")
    
    # 如果有自动修复，保存修复后的数据
    if detector.fixed_count > 0:
        print(f"\n🔧 自动修复了 {detector.fixed_count} 个问题")
        # 注释掉实际保存，避免意外修改数据
        # detector.save_fixed_data(fixed_data, data_paths)
    
    # 控制台输出摘要
    print("\n" + "=" * 60)
    print("检测摘要")
    print("=" * 60)
    print(f"检查时间: {report['check_time']}")
    print(f"总问题数: {report['total_issues']}")
    print(f"\n严重程度分布:")
    print(f"  - 严重: {report['severity_counts']['critical']}")
    print(f"  - 警告: {report['severity_counts']['warning']}")
    print(f"  - 信息: {report['severity_counts']['info']}")
    
    if report['type_counts']:
        print(f"\n问题类型分布:")
        for type_name, count in sorted(report['type_counts'].items(), key=lambda x: -x[1]):
            print(f"  - {type_name}: {count}")
    
    if report['anomalies']:
        print(f"\n问题详情 (前10条):")
        for a in report['anomalies'][:10]:
            severity_icon = {'critical': '🔴', 'warning': '🟡', 'info': '🔵'}.get(a['severity'], '⚪')
            print(f"  {severity_icon} [{a['dataset']}] {a['type']}: {a['message']}")
            if a['record_id'] != 'N/A':
                print(f"      记录ID: {a['record_id']}, 字段: {a['field']}")
    
    print(f"\n建议: {report['summary']['recommendation']}")
    print("\n" + "=" * 60)
    
    return report


if __name__ == '__main__':
    main()
