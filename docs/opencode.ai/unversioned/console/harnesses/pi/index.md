---
source_url: https://opencode.ai/docs/console/harnesses/pi/
source_hash: sha256:d1161504d2470e6a39b4b33af31498db5b98319cbe9e1f26823d17c3396500ae
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# Pi

[Pi](https://pi.dev) 内置了面向按量付费和 Go 的 OpenCode provider。它会为每个付费或 Go 模型选择正确的 API。免费层级的对话模型需要 OpenCode，从 Pi 访问会返回 HTTP `403`。

| Provider      | 套餐          |
| ------------- | ------------- |
| `opencode`    | 按量付费      |
| `opencode-go` | Go            |

## 配置

两个 provider 都从 `OPENCODE_API_KEY` 读取密钥。请创建一个[个人 API 密钥](../index.md#get-an-api-key)。

```bash
export OPENCODE_API_KEY="oc_sk_..."
pi --model opencode/claude-sonnet-5-5
```

你也可以在 Pi 中运行 `/login` 并选择 provider。Pi 会把密钥保存在 `~/.pi/agent/auth.json` 中。

```text
/login opencode
```

## Go

使用来自拥有 [Go](../../go/index.md) 订阅的工作区的密钥，并配合 `opencode-go` provider。

```bash
pi --model opencode-go/kimi-k3
```

## 模型

以 `<provider>/<model-id>` 的形式选择模型，ID 来自 [Console](../../models/index.md#endpoints) 或 [Go](../../go/index.md#endpoints) 表格。使用 `--list-models` 可列出 Pi 已知的模型。

```bash
pi --list-models opencode-go
```

在 `~/.pi/agent/settings.json` 中设置默认值，或在 `/model` 选择器中按 `Ctrl+S`。

```json title="~/.pi/agent/settings.json"
{
  "defaultProvider": "opencode-go",
  "defaultModel": "kimi-k3"
}
```

当新的 Console 模型尚未出现时，运行 `pi update --models`。

## Console MCP

Pi v0.99.0 及更高版本支持 MCP。添加 [Console MCP](../index.md#console-mcp) 服务器，然后在浏览器中完成登录。

```bash
pi mcp add opencode-console --url https://opencode.ai/console/mcp
pi mcp login opencode-console
```
