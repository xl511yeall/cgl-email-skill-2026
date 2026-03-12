# CGL-Email Skill 2026

邮件智能汇总 Skill for OpenClaw / QClaw

## 功能

- 按 conversationId 自动合并邮件对话
- 识别重要关键词（offer、面试，入职等）
- 提取参与人、核心信息
- 判断最终结果（同意/拒绝/进行中）
- 输出简洁的整体总结

## 文件结构

```
email-summary/
├── README.md      # 使用说明
├── SKILL.md       # Skill 定义
├── summary.py     # 汇总脚本
├── config.json    # 规则配置
└── upload.sh     # 一键上传脚本
```

## 快速开始

### 手动运行

```bash
python3 summary.py [--top N]
```

### 一键上传更新

```bash
./upload.sh
```

## 配置规则

编辑 `config.json` 自定义关键词和规则：

```json
{
  "keywords": {
    "offer": ["offer", "面试", "入职"],
    "salary": ["薪资", "奖金", "月薪"]
  }
}
```

## 定时任务

```bash
# 每天 1:00 自动执行
0 1 * * * /usr/bin/python3 /path/to/summary.py
```

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.1 | 2026-03-12 | 添加定时任务支持、可配置规则 |
| 1.0 | 2026-03-12 | 初始版本 |

## 作者

CGL Consulting - 大白 (Dabai)
