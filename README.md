# CGL-Email Skill 2026

邮件智能汇总 Skill for OpenClaw / QClaw

## 功能

- 按 conversationId 自动合并邮件对话
- 识别重要关键词（offer、面试，入职等）
- 提取参与人、核心信息
- 判断最终结果（同意/拒绝/进行中）
- 输出简洁的整体总结

## 使用方式

### 手动运行

```bash
python3 summary.py [--top N]
```

### 定时任务（推荐）

配置 cronjob 每天自动执行：

```bash
# 每天 1:00 自动执行
0 1 * * * /usr/bin/python3 /Users/mac/.openclaw/workspace/skills/email-summary/summary.py >> /Users/mac/.openclaw/workspace/logs/邮件汇总.log 2>&1
```

## 输出格式

```
📧 今日邮件汇总

💼 对话1: [主题]
   结果: ✅ 同意
   参与人: 张三, 李四
   信息: 候选人: 王五, Title: VP, 薪资: 20K

💼 对话2: [主题]
   结果: ⏳ 进行中
   ...
```

## 配置

需要提前配置 Outlook 世纪互联 Token：
- Token 文件：`~/.openclaw/workspace/.outlook_token.txt`
- API 端点：`microsoftgraph.chinacloudapi.cn`

## 关键词库

| 类别 | 关键词 |
|------|--------|
| Offer | offer, 面试, 入职, 签约 |
| 薪资 | 薪资, 奖金, 月薪, 年薪 |
| 合同 | 合同, 审批, 协议 |
| 业务 | CGL, 候选人, 推荐, BD, 客户 |

## 规则

1. 按对话合并，不逐封列出
2. 只给简洁整体总结
3. 包含：结果 + 原因 + 核心信息
4. 避免大段引用原文

## 版本

- V1.1 (2026-03-12): 添加定时任务支持

## 作者

CGL Consulting - 大白 (Dabai)
