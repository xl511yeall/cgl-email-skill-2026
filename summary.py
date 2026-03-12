#!/usr/bin/env python3
"""
CGL-Email Skill 2026 - 邮件智能汇总
按对话合并，输出简洁总结

使用方式：
  手动运行: python3 summary.py [--top N]
  定时任务: 建议配置 cronjob 每天 1:00 执行
"""
import requests
import os
import json
import re
from datetime import datetime

# 配置
GRAPH_API = "https://microsoftgraph.chinacloudapi.cn"
TOKEN_FILE = os.path.expanduser("~/.openclaw/workspace/.outlook_token.txt")
OUTPUT_DIR = os.path.expanduser("~/.openclaw/workspace/邮件汇总")

# 关键词
IMPORTANT_KEYWORDS = ['offer', '面试', '入职', '签约', '薪资', '奖金', '合同', '审批', 'cgl', '候选人', '推荐', 'bd']

def get_token():
    """获取 Outlook Token"""
    if not os.path.exists(TOKEN_FILE):
        print("❌ Token 文件不存在")
        return None
    with open(TOKEN_FILE) as f:
        return f.read().strip()

def fetch_emails(token, top=30):
    """获取邮件列表"""
    headers = {'Authorization': f'Bearer {token}'}
    url = f"{GRAPH_API}/v1.0/me/messages?$top={top}&$orderby=receivedDateTime desc"
    resp = requests.get(url, headers=headers, timeout=30)
    return resp.json().get('value', [])

def group_conversations(messages):
    """按 conversationId 分组"""
    conversations = {}
    for msg in messages:
        conv_id = msg.get('conversationId', 'unknown')
        if conv_id not in conversations:
            conversations[conv_id] = []
        
        sender = msg.get('from', {}).get('emailAddress', {})
        conversations[conv_id].append({
            'time': msg.get('receivedDateTime', '')[11:16],
            'sender': sender.get('name', '未知'),
            'email': sender.get('address', ''),
            'subject': msg.get('subject', ''),
            'preview': msg.get('bodyPreview', '')[:150]
        })
    return conversations

def analyze_conversation(msgs):
    """分析单个对话"""
    all_text = ' '.join([m['subject'] + m['preview'] for m in msgs])
    
    # 检查是否重要
    if not any(kw in all_text.lower() for kw in IMPORTANT_KEYWORDS):
        return None
    
    # 提取参与人
    participants = list(set([m['sender'] for m in msgs]))
    
    # 判断结果
    last_preview = msgs[-1]['preview'].lower()
    if '同意' in last_preview or '批准' in last_preview:
        result = '✅ 同意'
    elif '拒绝' in last_preview or '不同意' in last_preview:
        result = '❌ 拒绝'
    else:
        result = '⏳ 进行中'
    
    # 提取关键信息
    info = extract_info(msgs)
    
    return {
        'subject': msgs[0]['subject'][:50],
        'participants': participants,
        'result': result,
        'info': info,
        'count': len(msgs),
        'preview': msgs[-1]['preview'][:100]
    }

def extract_info(msgs):
    """提取关键信息"""
    info = []
    all_text = ' '.join([m['preview'] for m in msgs])
    
    # 候选人
    if '候选人' in all_text:
        match = re.search(r'候选人[：:]([^\s，,]+)', all_text)
        if match:
            info.append(f"候选人: {match.group(1)}")
    
    # Title
    match = re.search(r'Title[:\s]+([^\n，,]+)', all_text, re.I)
    if match:
        info.append(f"Title: {match.group(1).strip()}")
    
    # 薪资
    match = re.search(r'(\d+K)', all_text)
    if match:
        info.append(f"薪资: {match.group(1)}")
    
    # 入职日期
    match = re.search(r'入职日期[：:]?\s*(\d+月\d+日)', all_text)
    if match:
        info.append(f"入职: {match.group(1)}")
    
    return info

def generate_summary(conversations):
    """生成汇总"""
    lines = []
    lines.append(f"📧 邮件汇总 ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n")
    
    count = 0
    for conv_id, msgs in conversations.items():
        result = analyze_conversation(msgs)
        if result:
            count += 1
            lines.append(f"💼 对话{count}: {result['subject']}")
            lines.append(f"   结果: {result['result']}")
            lines.append(f"   参与人: {', '.join(result['participants'][:3])}")
            if result['info']:
                lines.append(f"   信息: {', '.join(result['info'])}")
            lines.append("")
    
    if count == 0:
        lines.append("今日无重要邮件")
    
    return "\n".join(lines)

def save_summary(content, output_dir=None):
    """保存汇总到文件"""
    if output_dir is None:
        output_dir = OUTPUT_DIR
    
    os.makedirs(output_dir, exist_ok=True)
    
    today = datetime.now().strftime('%Y-%m-%d')
    filename = os.path.join(output_dir, f"邮件汇总_{today}.txt")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 已保存到: {filename}")
    return filename

def main(top=30, save=True):
    """主函数"""
    print("🔄 正在获取邮件...")
    
    token = get_token()
    if not token:
        return
    
    messages = fetch_emails(token, top)
    conversations = group_conversations(messages)
    
    summary = generate_summary(conversations)
    print(summary)
    
    if save:
        save_summary(summary)
    
    return summary

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='CGL邮件智能汇总')
    parser.add_argument('--top', type=int, default=30, help='获取邮件数量')
    parser.add_argument('--no-save', action='store_true', help='不保存到文件')
    
    args = parser.parse_args()
    
    main(top=args.top, save=not args.no_save)
