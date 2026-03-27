#!/bin/bash
# 每日自动更新脚本
# 运行目录
cd /Users/zhangjingwei/.qclaw/workspace/hotspot-tracker

# 运行Python更新脚本
python3 auto_update.py

# 提交更新到Git
git add -A
git commit -m "Auto update: $(date '+%Y-%m-%d %H:%M:%S') - $(cat client_ideas.json | python3 -c 'import json,sys;print(len(json.load(sys.stdin)))') topics"
git push origin main

echo "✅ 每日更新完成: $(date)"
