#!/bin/bash
# CGL-Email-Skill 上传脚本

echo "📦 准备上传到 GitHub..."

cd ~/.openclaw/workspace/skills/email-summary

# 检查 git 状态
if [ ! -d .git ]; then
    echo "❌ 未初始化 git"
    exit 1
fi

# 添加所有更改
git add -A

# 检查是否有更改
if git diff --staged --quiet; then
    echo "没有需要提交的更改"
else
    # 让用户输入提交信息
    echo "📝 请输入提交信息:"
    read msg
    if [ -z "$msg" ]; then
        msg="Update: $(date '+%Y-%m-%d %H:%M')"
    fi
    
    git commit -m "$msg"
    echo "✅ 已提交"
fi

# 推送到 GitHub
echo "🚀 正在推送到 GitHub..."
git push origin main

if [ $? -eq 0 ]; then
    echo "✅ 推送成功!"
    echo "🔗 https://github.com/xl511yeall/cgl-email-skill-2026"
else
    echo "❌ 推送失败，请检查网络或认证"
fi
