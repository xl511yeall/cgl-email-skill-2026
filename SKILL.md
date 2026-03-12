---
name: email-summary
description: 邮件智能汇总 - 按对话合并、提取关键信息、输出简洁总结
metadata:
  openclaw:
    emoji: 📧
    requires:
      bins: [python3]
      env: [OUTLOOK_TOKEN]
    primaryEnv: OUTLOOK_TOKEN
---

# Email Summary Skill

邮件智能汇总技能，按对话合并邮件，提取关键信息，输出简洁总结。

## 功能

- 按 conversationId 自动合并邮件对话
- 识别重要关键词（offer、面试、入职等）
- 提取参与人、核心信息
- 判断最终结果（同意/拒绝/进行中）
- 输出简洁的整体总结

## 使用方式

```bash
python3 ~/.openclaw/workspace/skills/email-summary/summary.py [--top N]
```

## 输出格式

```
📧 邮件汇总

💼 对话1: [主题]
   结果: ✅ 同意
   原因: [关键原因]
   信息: 候选人XXX, Title, 薪资XXK

💼 对话2: [主题]
   结果: ⏳ 进行中
   ...
```

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
