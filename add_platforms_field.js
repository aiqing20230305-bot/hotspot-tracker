#!/usr/bin/env node
/**
 * 修复脚本：为 hot_topics.json 添加 platforms 数组字段
 * 用途：将组合平台字段（如 "微博/抖音"）拆分为数组格式，便于未来扩展
 * 
 * 执行方式：node add_platforms_field.js
 */

const fs = require('fs');
const path = require('path');

const inputFile = path.join(__dirname, 'hot_topics.json');
const backupFile = path.join(__dirname, 'hot_topics.json.backup');

async function main() {
    console.log('🔧 开始修复 platforms 字段...\n');
    
    // 读取原文件
    if (!fs.existsSync(inputFile)) {
        console.error('❌ 错误：找不到 hot_topics.json 文件');
        process.exit(1);
    }
    
    const rawData = fs.readFileSync(inputFile, 'utf8');
    const topics = JSON.parse(rawData);
    
    console.log(`📊 读取到 ${topics.length} 条热点数据\n`);
    
    // 统计处理情况
    let addedCount = 0;
    let alreadyHasArray = 0;
    let needsSplit = 0;
    
    // 处理每条数据
    const updatedTopics = topics.map((topic, index) => {
        const platform = topic.platform || '';
        
        // 如果已有 platforms 数组，跳过
        if (topic.platforms && Array.isArray(topic.platforms)) {
            alreadyHasArray++;
            return topic;
        }
        
        // 拆分组合平台字段
        let platforms;
        if (platform.includes('/')) {
            platforms = platform.split('/').map(p => p.trim()).filter(p => p);
            needsSplit++;
        } else if (platform) {
            platforms = [platform.trim()];
        } else {
            platforms = ['其他'];
        }
        
        addedCount++;
        
        return {
            ...topic,
            platforms: platforms
        };
    });
    
    // 创建备份
    console.log('💾 创建备份文件...');
    fs.copyFileSync(inputFile, backupFile);
    console.log(`✅ 备份已保存至: ${backupFile}\n`);
    
    // 写入新文件
    const outputData = JSON.stringify(updatedTopics, null, 2);
    fs.writeFileSync(inputFile, outputData, 'utf8');
    
    console.log('📈 处理统计:');
    console.log(`  - 新增 platforms 字段: ${addedCount} 条`);
    console.log(`  - 已有 platforms 数组: ${alreadyHasArray} 条`);
    console.log(`  - 拆分组合平台字段: ${needsSplit} 条\n`);
    
    console.log('✅ 修复完成！\n');
    
    // 显示示例
    console.log('📋 示例数据对比:');
    const exampleBefore = topics[0];
    const exampleAfter = updatedTopics[0];
    console.log('修复前:', JSON.stringify({
        platform: exampleBefore.platform,
        platforms: exampleBefore.platforms
    }, null, 2));
    console.log('\n修复后:', JSON.stringify({
        platform: exampleAfter.platform,
        platforms: exampleAfter.platforms
    }, null, 2));
}

main().catch(err => {
    console.error('❌ 执行出错:', err);
    process.exit(1);
});
