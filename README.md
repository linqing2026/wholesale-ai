# 🍷 批发AI助手 — Wholesale AI Assistant

<p align="center">
  <b>进口酒水批发商的飞书智能管家</b><br>
  <sub>一句话查利润 · 自动补货预警 · 供应商比价 · 库存健康扫描</sub>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/OpenClaw-2026.4+-orange.svg" alt="OpenClaw">
  <img src="https://img.shields.io/badge/Framework-OpenClaw-purple.svg" alt="Framework">
</p>

---

## 🎯 这是什么？

飞书群里的 AI 批发管家。**你 @它，它回你。**

```
你：利润 82拉菲 6800
它：🟢 拉菲 1982 · 进价¥4200 · 综合成本¥4830 · 售¥6800 → 毛利29.0% (¥1970/箱)
```

不需要打开电脑，不需要登录系统。**手机飞书群聊就是你的经营控制台。**

---

## ⚡ 四大能力

| 模块 | 用法 | 做什么 |
|------|------|--------|
| 📦 **采购参谋** | `补货` | 扫描库存，低于安全水位自动建议补货 |
| 💰 **利润精算** | `利润 酒款名 售价` | 综合成本(进价×1.15)，秒算毛利率 |
| 📊 **供应商比价** | `比价 酒款名` | 所有供应商报价排序，标注最低价 |
| 🏥 **库存健康** | `库存健康` | 查呆滞品 + 资金占用 TOP5 |

---

## 🚀 5 分钟部署

```bash
# 1. 克隆
git clone https://github.com/linqing2026/wholesale-ai.git
cd wholesale-ai

# 2. 安装
bash install.sh

# 3. 配置飞书应用（见 DEPLOY.md）
# 4. 重启网关 → 飞书群 @批发助手
```

📖 完整部署指南：[DEPLOY.md](./DEPLOY.md)

## 📊 使用演示

### 采购参谋
```
你：补货
它：📦 补货建议
    茅台 2015 · 库存3箱 · 安全水位5箱 · 建议补7箱
```

### 利润精算
```
你：利润 82拉菲 6800
它：🟢 拉菲 1982 · 进价¥4200 · 综合成本¥4830 · 售¥6800 → 毛利29.0%
```

> 支持模糊匹配：「82拉菲」自动识别为「拉菲 1982」

### 供应商比价
```
你：比价 茅台
它：📊 茅台 供应商比价
    国酒商贸 · ¥2600/箱 ← 最低
    国酒商贸 · ¥3800/箱 (+¥1200)
```

### 库存健康
```
你：库存健康
它：⚠️ 呆滞品（库存超安全水位2倍）
    拉菲 2015 · 库存15箱(安全5) · 占用¥42,000
    ...
    💰 资金占用 TOP5
    1. 拉菲 2015 · ¥42,000
    ...
```

---

## 📁 项目结构

```
wholesale-ai/
├── README.md              ← 本文件
├── DEPLOY.md              ← 详细部署指南
├── AGENTS.md              ← Agent 定义
├── SOUL.md                ← Agent 人设
├── install.sh             ← 一键安装脚本
├── scripts/
│   └── wholesale_query.py ← 四大模块查询引擎
├── data/
│   └── schema.sql         ← 数据库建表 + 示例数据
└── deploy/
    └── openclaw_agent.yaml ← OpenClaw 配置参考
```

---

## 🔧 技术栈

- **Agent 框架**：[OpenClaw](https://github.com/openclaw/openclaw)
- **推理模型**：DeepSeek V4 Pro（也支持本地 Ollama 模型）
- **数据存储**：SQLite（单文件，零配置）
- **消息通道**：飞书群机器人
- **语言**：Python 3.9+，仅依赖标准库

---

## 💰 商业模式

| 层级 | 对象 | 价格 |
|------|------|------|
| 🆓 **开源版** | 自己部署，接自己飞书 | ¥0 |
| ⭐ **托管版** | 帮你部署 + 维护 + 数据备份 | ¥199/月 |
| 🏆 **定制版** | 加品类 / 对接现有系统 / 独立品牌 | ¥5000 起 |

📩 飞书搜索「批发助手」咨询托管和定制。

---

## 👤 作者

**林清** — 7 年快消 B2B 经验，从区域代理商到 AI 创业者。

- GitHub：[@linqing2026](https://github.com/linqing2026)
- 项目主页：[github.com/linqing2026/wholesale-ai](https://github.com/linqing2026/wholesale-ai)

---

*Built with OpenClaw · DeepSeek V4 Pro · ❤️*
