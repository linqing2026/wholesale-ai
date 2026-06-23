# 部署指南

## 你需要什么

| 项目 | 说明 |
|------|------|
| 一台 Linux 服务器 | 1 核 2G 即可，约 ¥50/月（阿里云/腾讯云轻量） |
| 飞书开放平台账号 | 免费注册 [open.feishu.cn](https://open.feishu.cn) |
| 20 分钟时间 | 跟着走就行 |

## 第一步：服务器环境

SSH 登录你的服务器，安装 Node.js（如果还没有）：

```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs python3

# CentOS/RHEL
curl -fsSL https://rpm.nodesource.com/setup_20.x | sudo bash -
sudo yum install -y nodejs python3
```

## 第二步：安装批发助手

```bash
# 克隆项目
git clone https://github.com/linqing2026/wholesale-ai.git
cd wholesale-ai

# 一键安装
bash install.sh
```

安装过程自动完成：
- ✅ 检查 Python 和 sqlite3 环境
- ✅ 安装 OpenClaw（如果未安装）
- ✅ 创建数据库（含 8 款示例数据）
- ✅ 安装四大模块查询引擎

## 第三步：创建飞书应用

1. 打开 [飞书开放平台](https://open.feishu.cn)
2. 创建「企业自建应用」
3. 应用名称：**批发助手**
4. 获取 **App ID** 和 **App Secret**（在「凭证与基础信息」页）

### 添加应用权限

在「权限管理」页面，添加以下权限：
- `im:message` - 获取与发送消息
- `im:message:group` - 获取群消息
- `im:chat` - 获取群信息
- `im:resource` - 获取消息中的资源

### 事件订阅（可选）

如果希望 @批发助手 自动响应，在「事件订阅」页面：
- 请求网址：`https://你的服务器IP:18789/feishu/event`
- 添加事件：`im.message.receive_v1`

### 发布应用

在「版本管理与发布」页面创建新版本并发布。

## 第四步：配置 OpenClaw Agent

编辑 `~/.openclaw/openclaw.json`，找到 `agents.list`，添加：

```json
{
  "id": "wholesale",
  "name": "批发助手",
  "workspace": "/home/openclaw/workspace-wholesale",
  "model": "deepseek/deepseek-v4-pro"
}
```

在 `channels.feishu.accounts` 中添加：

```json
"你的飞书App ID": {
  "appId": "你的飞书App ID",
  "appSecret": "你的飞书App Secret",
  "enabled": true,
  "name": "批发助手"
}
```

在 `bindings` 中添加：

```json
{
  "type": "route",
  "agentId": "wholesale",
  "match": {
    "channel": "feishu",
    "accountId": "你的飞书App ID"
  }
}
```

## 第五步：启动

```bash
openclaw gateway restart
```

## 第六步：测试

把飞书应用机器人加入一个飞书群，@它试试：

```
补货
利润 82拉菲 6800
比价 茅台
库存健康
```

## 问题排查

| 问题 | 检查 |
|------|------|
| 机器人不回消息 | `openclaw gateway status` 确认网关运行中 |
| 数据库无数据 | `sqlite3 ~/.openclaw/wholesale.db "SELECT COUNT(*) FROM wines"` |
| 飞书推送失败 | 检查 App Secret 是否正确，应用是否已发布 |
| 端口被墙 | 确认服务器防火墙开放 18789 端口 |

## 成本估计

| 项目 | 月费 |
|------|------|
| 云服务器（1C2G） | ¥50 |
| DeepSeek API | ¥10-30（按用量） |
| OpenAI 兼容模型（可选） | 免费（用本地 ollama） |
| **合计** | **¥60-80/月** |

---

有问题？飞书搜索「批发助手」或提 [GitHub Issue](https://github.com/linqing2026/wholesale-ai/issues)。
