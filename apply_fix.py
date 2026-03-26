import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 替换onclick
count = 0
def repl(m):
    global count
    count += 1
    return f'onclick="showHotspotDetail({count})"'
content = re.sub(r'onclick="toggleTopic\(this\)"', repl, content)
print(f"Replaced {count} onclick")

# 2. 在脚本弹窗前添加modal
modal = '''    <!-- 热点详情弹窗 -->
    <div id="hm" style="display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.6);z-index:10000;align-items:center;justify-content:center;">
<div style="background:white;border-radius:20px;max-width:650px;width:92%;max-height:85vh;overflow-y:auto;padding:28px;position:relative;">
<button onclick="document.getElementById('hm').style.display='none'" style="position:absolute;top:18px;right:18px;background:#f3f4f6;border:none;width:36px;height:36px;border-radius:50%;font-size:22px;cursor:pointer;">×</button>
<div id="hb"></div>
</div>
</div>
'''
content = content.replace('    <!-- 脚本弹窗 -->', modal + '    <!-- 脚本弹窗 -->')

# 3. 删除toggleTopic和showDetail函数
content = re.sub(r'\s*// 热点展开/收起功能[\s\S]*?showDetail\([^)]+\);\s*\}', '', content)

# 4. 在closeScript之前添加代码
code = '''var hd=[{id:1,title:"我的春日粉彩妆容公式",platform:"抖音",heat:"1210万",trend:"🔥🔥🔥 持续上升中",type:"妆容教程",aud:"18-35岁女性",time:"12:00-14:00",logic:"春季美妆旺季",link:"https://www.douyin.com/search/我的春日粉彩妆容公式",c:["快消-AHC"]},{id:2,title:"中国机器狼群",platform:"抖音",heat:"1166万",trend:"🔥🔥🔥 爆发增长",type:"科技",aud:"18-45岁男性",time:"全天",logic:"国防科技热点",link:"https://www.douyin.com/search/中国机器狼群",c:["3C数码-荣耀"]},{id:3,title:"一箭双星",platform:"抖音",heat:"1091万",trend:"🔥🔥 上升",type:"航天",aud:"25-50岁男性",time:"12:00-14:00",logic:"航天成就",link:"https://www.douyin.com/search/一箭双星",c:["3C数码-荣耀"]},{id:4,title:"AWE2025",platform:"微博",heat:"856万",trend:"🔥🔥 上升",type:"科技展会",aud:"25-45岁",time:"全天",logic:"家电展会",link:"https://s.weibo.com/weibo?q=AWE2025",c:["3C数码-荣耀"]},{id:5,title:"315晚会",platform:"微博",heat:"792万",trend:"🔥🔥🔥 爆发",type:"消费维权",aud:"全年龄段",time:"20:00-22:00",logic:"消费者权益日",link:"https://s.weibo.com/weibo?q=315晚会",c:["保健品-汤臣倍健"]},{id:6,title:"AI突破",platform:"微博",heat:"745万",trend:"🔥🔥 上升",type:"科技前沿",aud:"20-40岁",time:"10:00-12:00",logic:"AI持续火热",link:"https://s.weibo.com/weibo?q=人工智能突破",c:["3C数码-荣耀"]},{id:7,title:"春日穿搭OOTD",platform:"小红书",heat:"3.2亿",trend:"🔥🔥🔥 爆发",type:"穿搭",aud:"18-30岁女性",time:"10:00-12:00",logic:"春日换季",link:"https://www.xiaohongshu.com/search_result?keyword=春日穿搭OOTD",c:["快消-AHC"]},{id:8,title:"春季护肤",platform:"小红书",heat:"2.1亿",trend:"🔥🔥🔥 上升",type:"护肤",aud:"18-35岁女性",time:"10:00-12:00",logic:"换季护肤",link:"https://www.xiaohongshu.com/search_result?keyword=春季护肤攻略",c:["快消-AHC"]},{id:9,title:"露营装备",platform:"小红书",heat:"1.8亿",trend:"🔥🔥 上升",type:"户外",aud:"25-40岁",time:"周末",logic:"春暖花开",link:"https://www.xiaohongshu.com/search_result?keyword=露营装备推荐",c:["食品-OATLY"]},{id:10,title:"效率神器",platform:"微博",heat:"620万",trend:"🔥🔥 上升",type:"职场",aud:"22-35岁",time:"8:00-9:00",logic:"打工人共鸣",link:"https://s.weibo.com/weibo?q=打工人效率神器",c:["3C数码-荣耀"]}];
function showHotspotDetail(id){var d=null;for(var i=0;i<hd.length;i++)if(hd[i].id===id){d=hd[i];break}if(!d)return;var p=d.platform==="抖音"?"#1C1C1D":d.platform==="微博"?"#FF6600":"#FF2442";var ch="";for(var j=0;j<d.c.length;j++)ch+='<span style="background:#EEF2FF;color:#6366F1;padding:6px 14px;border-radius:20px;font-size:13px;margin:3px;">'+d.c[j]+"</span>";document.getElementById("hb").innerHTML='<div style="margin-bottom:16px"><span style="background:'+p+';color:white;padding:5px 14px;border-radius:8px;font-size:13px;font-weight:600">'+d.platform+'</span><span style="color:#EF4444;font-weight:700;margin-left:14px;font-size:18px">🔥 '+d.heat+"</span></div><h2 style='font-size:22px;margin-bottom:20px;color:#1F2937'>"+d.title+"</h2><div style='display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:20px'><div style='background:linear-gradient(135deg,#FEF3C7,#FDE68A);padding:14px;border-radius:12px'><div style='font-size:11px;color:#92400E'>热度趋势</div><div style='font-weight:700;color:#B45309;font-size:14px'>"+d.trend+"</div></div><div style='background:linear-gradient(135deg,#DBEAFE,#BFDBFE);padding:14px;border-radius:12px'><div style='font-size:11px;color:#1E40AF'>最佳发布时间</div><div style='font-weight:700;color:#1D4ED8;font-size:13px'>"+d.time+"</div></div></div><div style='margin-bottom:16px'><div style='font-size:12px;font-weight:700;color:#6B7280'>内容类型</div><div style='font-size:14px;color:#374151'>"+d.type+"</div></div><div style='margin-bottom:20px'><div style='font-size:12px;font-weight:700;color:#6B7280'>受众人群</div><div style='font-size:14px;color:#374151'>"+d.aud+"</div></div><div style='background:linear-gradient(135deg,#EEF2FF,#E0E7FF);padding:18px;border-radius:14px;border-left:5px solid #6366F1;margin-bottom:20px'><div style='font-size:15px;font-weight:700;color:#4F46E5;margin-bottom:12px'>🧠 热点背后逻辑</div><div style='font-size:14px;line-height:1.7;color:#4338CA'>"+d.logic+"</div></div><div style='margin-bottom:20px'><a href='"+d.link+"' target='_blank' style='display:inline-flex;align-items:center;gap:6px;padding:12px 22px;background:#6366F1;color:white;border-radius:10px;text-decoration:none;font-weight:600;font-size:14px'>🔗 浏览内容</a></div><div style='border-top:2px solid #F3F4F6;padding-top:18px'><div style='font-size:13px;font-weight:700;color:#6B7280;margin-bottom:10px'>💡 可借势客户</div><div style='display:flex;flex-wrap:wrap;gap:8px'>"+ch+"</div></div>";document.getElementById("hm").style.display="flex"}
document.getElementById("hm").addEventListener("click",function(e){if(e.target===this)this.style.display="none"});

'''
content = content.replace('        function closeScript()', code + '        function closeScript()')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Done!")
