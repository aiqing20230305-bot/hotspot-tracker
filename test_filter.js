#!/usr/bin/env node
/**
 * 测试脚本：验证平台筛选功能
 */

const fs = require('fs');
const path = require('path');

const inputFile = path.join(__dirname, 'hot_topics.json');
const topics = JSON.parse(fs.readFileSync(inputFile, 'utf8'));

console.log('🧪 平台筛选功能测试\n');
console.log(`总数据量: ${topics.length} 条\n`);

// 测试各种筛选场景
const testCases = [
    { platform: '抖音', description: '筛选抖音平台' },
    { platform: '微博', description: '筛选微博平台' },
    { platform: '小红书', description: '筛选小红书平台' },
    { platform: 'B站', description: '筛选B站平台' },
];

testCases.forEach(({ platform, description }) => {
    console.log(`\n📌 测试: ${description}`);
    console.log(`   筛选条件: platform = "${platform}"`);
    
    const filtered = topics.filter(t => {
        // 支持 platforms 数组格式
        if (t.platforms && Array.isArray(t.platforms)) {
            return t.platforms.includes(platform);
        }
        // 兼容字符串格式（可能是组合格式如 "微博/抖音"）
        const platformStr = t.platform || '';
        if (platformStr.includes('/')) {
            return platformStr.split('/').includes(platform);
        }
        return platformStr.includes(platform);
    });
    
    console.log(`   ✅ 匹配结果: ${filtered.length} 条`);
    
    // 显示前3条匹配的标题
    if (filtered.length > 0) {
        console.log(`   📋 示例:`);
        filtered.slice(0, 3).forEach(t => {
            console.log(`      - ${t.title.substring(0, 40)}...`);
            console.log(`        平台: ${t.platform} | platforms: [${t.platforms?.join(', ')}]`);
        });
    }
});

// 测试模糊匹配功能
console.log('\n\n🔍 测试模糊匹配（确保包含搜索正常工作）');
const partialMatch = topics.filter(t => {
    const platform = t.platform || '';
    return platform.includes('抖');
});
console.log(`   使用 "抖" 进行 includes 匹配: ${partialMatch.length} 条`);

// 验证数据结构
console.log('\n\n✅ 数据结构验证:');
const sample = topics[0];
console.log(`   platform 字段: ${sample.platform}`);
console.log(`   platforms 数组: [${sample.platforms?.join(', ')}]`);
console.log(`   platforms 类型: ${Array.isArray(sample.platforms) ? 'Array ✅' : 'Not Array ❌'}`);

console.log('\n\n🎉 所有测试完成！');
