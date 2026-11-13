---
source_url: https://opencode.ai/docs/console/harnesses/hermes/
source_hash: sha256:d139ca7c89e884090d79930bb82a56abf4f8bf94ce977c9f2503e9714527ad88
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# Hermes

[Hermes Agent](https://hermes-agent.nousresearch.com) 内置了适用于按量付费（pay-as-you-go）和 Go 的 OpenCode provider。它会为每个付费或 Go 模型选择合适的 API。免费层的聊天模型需要 OpenCode，Hermes 会对其返回 HTTP `403`。

| Provider       | 套餐           | 密钥变量               |
| -------------- | ------------- | ---------------------- |
| `opencode-zen` | 按量付费       | `OPENCODE_ZEN_API_KEY` |
| `opencode-go`  | Go            | `OPENCODE_GO_API_KEY`  |

## 配置

运行模型设置流程，按量付费选择 **OpenCode Zen**，Go 选择 **OpenCode Go**。

```bash
hermes model
```

粘贴一个[个人 API key](../index.md#get-an-api-key)，然后选择一个模型。Hermes 会把密钥保存到 `~/.hermes/.env`，把选择结果保存到 `~/.hermes/config.yaml`。

```yaml title="~/.hermes/config.yaml"
model:
  provider: opencode-go
  default: kimi-k3
```

<Callout>Go 要求每次请求都携带会话 ID。Hermes v0.21.6 及更高版本会自动发送。</Callout>

## 模型

直接使用[Console](../../models/index.md#endpoints)或 [Go](../../go/index.md#endpoints)表格中的模型 ID，无需加前缀。在会话中用 `/model` 切换模型，也可以为单次运行指定一个模型。

```bash
hermes chat --provider opencode-zen --model claude-sonnet-5-5
```

## Console MCP

用 OAuth 添加 [Console MCP](../index.md#console-mcp)服务器，然后在浏览器中登录。

```bash
hermes mcp add opencode-console --url https://opencode.ai/console/mcp --auth oauth
hermes mcp login opencode-console
```

也可以把它加到 `~/.hermes/config.yaml` 中，并在会话里运行 `/reload-mcp`。

```yaml title="~/.hermes/config.yaml"
mcp_servers:
  opencode-console:
    url: https://opencode.ai/console/mcp
    auth: oauth
```
