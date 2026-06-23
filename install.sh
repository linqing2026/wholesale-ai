#!/bin/bash
# 批发AI助手 · 一键部署脚本
# 使用方法: bash install.sh
set -e

echo "🍷 批发AI助手 · 安装中..."
echo ""

# ── 1. 检查 Python ──
if ! command -v python3 &>/dev/null; then
    echo "❌ 未找到 python3，请先安装 Python 3.9+"
    echo "   Ubuntu/Debian: sudo apt install python3"
    echo "   CentOS/RHEL:   sudo yum install python3"
    exit 1
fi
echo "✅ Python $(python3 --version)"

# ── 2. 检查 sqlite3 ──
if ! python3 -c "import sqlite3" 2>/dev/null; then
    echo "❌ sqlite3 模块不可用"
    exit 1
fi
echo "✅ SQLite3"

# ── 3. 检查/安装 OpenClaw ──
if ! command -v openclaw &>/dev/null; then
    echo "⚠️  OpenClaw 未安装，正在安装..."
    if command -v npm &>/dev/null; then
        npm install -g openclaw
    else
        echo "❌ 请先安装 Node.js: https://nodejs.org"
        exit 1
    fi
fi
echo "✅ OpenClaw $(openclaw --version 2>/dev/null || echo 'installed')"

# ── 4. 初始化数据库 ──
DB_PATH="${HOME}/.openclaw/wholesale.db"
if [ -f "$DB_PATH" ]; then
    echo "⚠️  数据库已存在: $DB_PATH (跳过创建)"
else
    mkdir -p "$(dirname "$DB_PATH")"
    SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
    python3 -c "
import sqlite3, os
db = '$DB_PATH'
schema = os.path.join('$SCRIPT_DIR', 'data', 'schema.sql')
if os.path.exists(schema):
    with open(schema) as f:
        sql = f.read()
    conn = sqlite3.connect(db)
    conn.executescript(sql)
    conn.commit()
    conn.close()
    print(f'✅ 数据库已创建: {db}')
else:
    print('❌ 未找到 schema.sql')
    exit(1)
"
fi

# ── 5. 安装查询引擎 ──
cp -f "$(dirname "$0")/scripts/wholesale_query.py" "${HOME}/.openclaw/scripts/wholesale_query.py"
echo "✅ 查询引擎已安装"

# ── 6. 飞书配置提示 ──
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🍷 安装完成！"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "下一步："
echo "  1. 飞书开放平台创建应用: https://open.feishu.cn"
echo "  2. 获取 App ID + App Secret"
echo "  3. 编辑 ~/.openclaw/openclaw.json 添加 Agent 配置"
echo "     (参考 deploy/openclaw_agent.yaml)"
echo "  4. 重启 OpenClaw: openclaw gateway restart"
echo "  5. 在飞书群 @批发助手 试试: 补货"
echo ""
echo "📖 详细部署指南: DEPLOY.md"
