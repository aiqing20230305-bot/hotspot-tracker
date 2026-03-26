#!/usr/bin/env python3
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 替换所有onclick
count = 0
def replace_onclick(match):
    global count
    count += 1
    return f'onclick="showHotspotDetail({count})"'

content = re.sub(r'onclick="toggleTopic\(this\)"', replace_onclick, content)
print(f"Replaced {count} onclick handlers")

# 2. 在scriptModal之前添加modal HTML
modal_html = '''    <!-- 热点详情弹窗 -->
    <div id="hotspotModal" style="display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.6);z-index:10000;align-items:center;justify-content:center;">
        <div style="background:white;border-radius:20px;max-width:650px;width:92%;max-height:85vh;overflow-y:auto;padding:28px;position:relative;box-shadow:0 25px 50px rgba(0,0,0,0.25);">
            <button onclick="document.getElementById('hotspotModal').style.display='none'" style="position:absolute;top:18px;right:18px;background:#F3F4F6;border:none;width:36px;height:36px;border-radius:50%;font-size:22px;cursor:pointer;color:#666;">×</button>
            <div id="hotspotBody"></div>
        </div>
    </div>
    
    '''
content = content.replace('    <!-- 脚本弹窗 -->', modal_html + '<!-- 脚本弹窗 -->')

# 3. 在</script>之前添加函数和数据（只添加一次）
hotspot_code = '''
        // 热点详情数据
        var hotspotData = [
            {id:1,title:"我的春日粉彩妆容公式",platform:"抖音",heat:"1210万",trend:"🔥🔥🔥 持续上升中",contentType:"妆容教程、美妆测评",audience:"18-35岁女性，美妆爱好者",bestTime:"12:00-14:00, 18:00-22:00",logic:"春季是美妆旺季，粉彩契合春日氛围，妆容公式降低学习门槛。",link:"https://www.douyin.com/search/我的春日粉彩妆容公式",clients:["快消-AHC","快消-多芬","快消-力士"]},
            {id:2,title:"中国机器狼群巷战画面首次公开",platform:"抖音",heat:"1166万",trend:"🔥🔥🔥 爆发式增长",contentType:"军事科技、新闻热点",audience:"18-45岁男性，科技爱好者",bestTime:"全天可发，18:00-22:00最佳",logic:"国防科技话题引发民族自豪感，视频画面震撼。",link:"https://www.douyin.com/search/中国机器狼群",clients:["3C数码-荣耀","3C数码-罗技"]},
            {id:3,title:"我国又一次发射一箭双星",platform:"抖音",heat:"1091万",trend:"🔥🔥 持续上升",contentType:"航天科技、新闻",audience:"25-50岁男性，科迷",bestTime:"12:00-14:00, 20:00-22:00",logic:"航天成就振奋人心，增强民族自信。",link:"https://www.douyin.com/search/一箭双星",clients:["3C数码-荣耀"]},
            {id:4,title:"2025中国家电及消费电子博览会",platform:"微博",heat:"856万",trend:"🔥🔥 持续上升",contentType:"科技展会、新品发布",audience:"25-45岁消费电子用户",bestTime:"全天可发",logic:"AWE是行业顶级展会，新产品集中亮相。",link:"https://s.weibo.com/weibo?q=AWE2025",clients:["3C数码-荣耀","3C数码-罗技"]},
            {id:5,title:"315晚会曝光问题",platform:"微博",heat:"792万",trend:"🔥🔥🔥 爆发增长",contentType:"消费维权、新闻",audience:"全年龄段消费者",bestTime:"20:00-22:00",logic:"315是消费者权益日，曝光问题引发广泛关注。",link:"https://s.weibo.com/weibo?q=315晚会",clients:["保健品-汤臣倍健","家庭清洁-HC"]},
            {id:6,title:"人工智能新突破",platform:"微博",heat:"745万",trend:"🔥🔥 稳定上升",contentType:"科技前沿、深度分析",audience:"20-40岁科技爱好者",bestTime:"10:00-12:00, 14:00-18:00",logic:"AI持续火热，每次突破都引发热议。",link:"https://s.weibo.com/weibo?q=人工智能突破",clients:["3C数码-荣耀","3C数码-罗技"]},
            {id:7,title:"春日穿搭OOTD",platform:"小红书",heat:"3.2亿浏览",trend:"🔥🔥🔥 爆发式增长",contentType:"穿搭分享、好物推荐",audience:"18-30岁女性，时尚达人",bestTime:"10:00-12:00, 19:00-21:00",logic:"春日换季，穿搭需求旺盛，OOTD是永恒热点。",link:"https://www.xiaohongshu.com/search_result?keyword=春日穿搭OOTD",clients:["快消-AHC","快消-多芬","快消-力士"]},
            {id:8,title:"春季护肤攻略",platform:"小红书",heat:"2.1亿浏览",trend:"🔥🔥🔥 持续上升",contentType:"护肤教程、产品测评",audience:"18-35岁女性，护肤爱好者",bestTime:"10:00-12:00, 20:00-22:00",logic:"换季皮肤问题多，护肤需求激增。",link:"https://www.xiaohongshu.com/search_result?keyword=春季护肤攻略",clients:["快消-AHC","快消-多芬"]},
            {id:9,title:"露营装备推荐",platform:"小红书",heat:"1.8亿浏览",trend:"🔥🔥 稳定上升",contentType:"户外装备、好物推荐",audience:"25-40岁户外爱好者",bestTime:"周末全天，工作日19:00后",logic:"春季天气转暖，户外活动增多。",link:"https://www.xiaohongshu.com/search_result?keyword=露营装备推荐",clients:["食品-OATLY","食品-士力架"]},
            {id:10,title:"打工人效率神器",platform:"微博",heat:"620万",trend:"🔥🔥 稳定上升",contentType:"职场工具、好物分享",audience:"22-35岁职场人群",bestTime:"8:00-9:00, 12:00-13:00",logic:"打工人共鸣强，效率工具人人需要。",link:"https://s.weibo.com/weibo?q=打工人效率神器",clients:["3C数码-荣耀","3C数码-罗技"]}
        ];
        
        function showHotspotDetail(id) {
            var data = null;
            for(var i=0; i<hotspotData.length; i++) {
                if(hotspotData[i].id === id) { data = hotspotData[i]; break; }
            }
            if(!data) return;
            
            var pColor = data.platform==='抖音' ? '#1C1C1D' : (data.platform==='微博' ? '#FF6600' : '#FF2442');
            var clientsHTML = '';
            for(var j=0; j<data.clients.length; j++) {
                clientsHTML += '<span style="background:#EEF2FF;color:#6366F1;padding:6px 14px;border-radius:20px;font-size:13px;font-weight:500;margin:3px;">' + data.clients[j] + '</span>';
            }
            
            document.getElementById('hotspotBody').innerHTML = 
                '<div style="margin-bottom:16px;"><span style="background:' + pColor + ';color:white;padding:5px 14px;border-radius:8px;font-size:13px;font-weight:600;">' + data.platform + '</span><span style="color:#EF4444;font-weight:700;margin-left:14px;font-size:18px;">🔥 ' + data.heat + '</span></div>' +
                '<h2 style="font-size:22px;margin-bottom:20px;color:#1F2937;line-height:1.4;">' + data.title + '</h2>' +
                '<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:20px;"><div style="background:linear-gradient(135deg,#FEF3C7,#FDE68A);padding:14px;border-radius:12px;"><div style="font-size:11px;color:#92400E;margin-bottom:4px;">热度趋势</div><div style="font-weight:700;color:#B45309;font-size:14px;">' + data.trend + '</div></div><div style="background:linear-gradient(135deg,#DBEAFE,#BFDBFE);padding:14px;border-radius:12px;"><div style="font-size:11px;color:#1E40AF;margin-bottom:4px;">最佳发布时间</div><div style="font-weight:700;color:#1D4ED8;font-size:13px;">' + data.bestTime + '</div></div></div>' +
                '<div style="margin-bottom:16px;"><div style="font-size:12px;font-weight:700;color:#6B7280;margin-bottom:6px;">内容类型</div><div style="font-size:14px;color:#374151;">' + data.contentType + '</div></div>' +
                '<div style="margin-bottom:20px;"><div style="font-size:12px;font-weight:700;color:#6B7280;margin-bottom:6px;">受众人群</div><div style="font-size:14px;color:#374151;">' + data.audience + '</div></div>' +
                '<div style="background:linear-gradient(135deg,#EEF2FF,#E0E7FF);padding:18px;border-radius:14px;border-left:5px solid #6366F1;margin-bottom:20px;"><div style="font-size:15px;font-weight:700;color:#4F46E5;margin-bottom:12px;">🧠 热点背后逻辑</div><div style="font-size:14px;line-height:1.7;color:#4338CA;">' + data.logic + '</div></div>' +
                '<div style="margin-bottom:20px;"><a href="' + data.link + '" target="_blank" style="display:inline-flex;align-items:center;gap:6px;padding:12px 22px;background:#6366F1;color:white;border-radius:10px;text-decoration:none;font-weight:600;font-size:14px;box-shadow:0 4px 12px rgba(99,102,241,0.3);">🔗 浏览内容</a></div>' +
                '<div style="border-top:2px solid #F3F4F6;padding-top:18px;"><div style="font-size:13px;font-weight:700;color:#6B7280;margin-bottom:10px;">💡 可借势客户</div><div style="display:flex;flex-wrap:wrap;gap:8px;">' + clientsHTML + '</div></div>';
            
            document.getElementById('hotspotModal').style.display = 'flex';
        }
        
        document.getElementById('hotspotModal').addEventListener('click', function(e) { if(e.target === this) this.style.display = 'none'; });
        
'''

# 删除旧的toggleTopic函数
content = re.sub(r'\s*// 热点展开/收起功能\s*function toggleTopic\([^)]+\)\s*\{[\s\S]*?\n\s*\}', '', content)

# 删除旧的showDetail函数
content = re.sub(r'\s*function showDetail\([^)]+\)\s*\{[\s\S]*?\n\s*\}', '', content)

# 在closeScript之前插入代码
content = content.replace('        function closeScript()', hotspot_code + '        function closeScript()')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Done!")
