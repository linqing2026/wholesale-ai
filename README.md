# 🍷 批发AI助手 — Wholesale AI Assistant

**进口酒水批发商的飞书智能管家 · Powered by OpenClaw + DeepSeek**

> 一句话查利润 · 自动补货预警 · 供应商比价 · 库存健康扫描  
> 飞书群直接用，不用打开电脑

---

## 🎯 这是什么？

一个运行在 [OpenClaw](https://github.com/openclaw/openclaw) 环境中的飞书智能体，专为进口酒水批发商设计。接入飞书群后，你@它问什么它回什么——

```
你：利润 82拉菲 6800
它：🟢 拉菲 1982 · 进价¥4200 · 综合成本¥4830 · 售¥6800 → 毛利29.0%
```

## ⚡ 四大能力

| 模块 | 怎么用 | 做什么 |
|------|--------|--------|
| 📦 **采购参谋** | `补货` | 扫描库存，低于安全水位自动建议补货 |
| 💰 **利润精算师** | `利润 酒款名 售价` | 综合成本 ×1.15，秒算毛利 |
| 📊 **供应商比价** | `比价 酒款名` | 按进价排序，一眼看谁最便宜 |
| 🏥 **库存健康** | `库存健康` | 找呆滞品、算资金占用TOP5 |

## 🚀 3 分钟部署

### 前置条件
- 一台 Linux 服务器（1C2G 即可）
- 已安装 [OpenClaw](https://docs.openclaw.ai)
- 飞书开放平台创建的应用（获取 App ID + App Secret）

### 安装步骤

```bash
# 1. 复制本项目
git clone https://github.com/linqing2026/wholesale-ai.git
cd wholesale-ai

# 2. 初始化数据库
sqlite3 ~/.openclaw/wholesale.db < data/schema.sql

# 3. 复制查询引擎
cp scripts/wholesale_query.py /path/to/openclaw/scripts/

# 4. 配置 OpenClaw Agent（见 deploy/）
# 5. 绑定飞书应用
# 6. 重启 OpenClaw Gateway

# 7. 在飞书群 @批发助手 试一下：
#    补货
#    利润 82拉菲 6800
```

## 📁 项目结构

```
wholesale-ai/
├── README.md
├── AGENTS.md                  ← Agent 定义
├── SOUL.md                    ← Agent 人设
├── scripts/
│   └── wholesale_query.py     ← 四大模块查询引擎
├── data/
│   └── schema.sql            ← 数据库建表
└── deploy/
    └── openclaw_agent.yaml   ← OpenClaw 部署配置
```

## 💰 商业模式

| 层级 | 面向用户 | 价格 |
|------|---------|------|
| 🆓 免费版 | 自己部署，接自己飞书 | ¥0 |
| ⭐ 托管版 | 帮你部署 + 维护 | ¥99-299/月 |
| 🏆 定制版 | 加品类/对接现有系统 | ¥3000-8000/次 |

## 👤 作者

**林清** — 7 年快消 B2B 经验，曾为区域龙头。现在用 AI 赋能进口酒水批发。

- GitHub: [@linqing2026](https://github.com/linqing2026)
- 合作咨询：飞书搜索「批发助手」

---

*Built with OpenClaw + DeepSeek V4 Pro*
