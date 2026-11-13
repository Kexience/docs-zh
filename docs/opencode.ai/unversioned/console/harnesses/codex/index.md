---
source_url: https://opencode.ai/docs/console/harnesses/codex/
source_hash: sha256:18b6cca33556dbfd54c00d4d84ae294fa2d82f6571e2ba55f4eebc6b740eae7e
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# Codex

Codex 说的是 OpenAI Responses API。把它指向 Console，即可使用任意付费或 Go 模型，包括 Claude、Gemini 和开放模型。对于不接受 Responses 的模型，Console 会替你翻译请求。

## 配置

在 `~/.codex/config.toml` 中把 Console 添加为模型 provider，并将其设为默认。

```toml title="~/.codex/config.toml"
model = "gpt-6.1-sol"
model_provider = "opencode"

[model_providers.opencode]
name = "OpenCode Console"
base_url = "https://opencode.ai/inference/openai/v1"
env_key = "OPENCODE_API_KEY"
wire_api = "responses"
```

Codex 会在 base URL 后追加 `/responses`，并从 `env_key` 读取密钥。创建一个[个人 API key](../index.md#get-an-api-key)，然后导出它。

```bash
export OPENCODE_API_KEY="oc_sk_..."
codex
```

<Callout>
  Codex 只从 `~/.codex/config.toml` 读取模型 provider。项目的 `.codex/config.toml` 无法设置它们。
</Callout>

## Go

使用 Go base URL 和来自有 [Go](../../go/index.md) 订阅的工作区的 key。

```toml title="~/.codex/config.toml"
model = "kimi-k3"
model_provider = "opencode-go"

[model_providers.opencode-go]
name = "OpenCode Go"
base_url = "https://opencode.ai/inference/go/openai/v1"
env_key = "OPENCODE_API_KEY"
wire_api = "responses"
```

## 模型

把 `model` 设为 [Console](../../models/index.md#endpoints) 或 [Go](../../go/index.md#endpoints) 表中的任意模型 ID。单次运行可以用 `--model` 覆盖。

```bash
codex --model claude-sonnet-5-5
```

Codex 不了解其自身目录之外模型的上下文窗口或推理设置。它会对这些模型使用通用默认值并打印一条警告，你可以忽略它。

## Profiles

用 profile 让按量付费和 Go 并存。在 `~/.codex/config.toml` 中定义两个 provider，然后添加一个切换到 Go 的 profile 文件。

```toml title="~/.codex/go.config.toml"
model = "kimi-k3"
model_provider = "opencode-go"
```

```bash
codex --profile go
```

## Console MCP

添加 [Console MCP](../index.md#console-mcp) 服务器，并在浏览器中登录。

```bash
codex mcp add opencode-console --url https://opencode.ai/console/mcp
```

如果登录没有自动开始，可以手动运行。

```bash
codex mcp login opencode-console
```
