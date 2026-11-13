---
source_url: https://opencode.ai/docs/console/harnesses/claude-code/
source_hash: sha256:e66bbe590a66ab488b11be81d752e617bcd9d6c5960dc058d4b8fe224c057ea1
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# Claude Code

Claude Code 说的是 Anthropic Messages API。通过两个环境变量把它指向 Console，即可使用任何付费或 Go 模型，包括 GPT、Gemini 和开放模型。对于不接受 Anthropic Messages 的模型，Console 会自动翻译请求。

```bash
export ANTHROPIC_BASE_URL="https://opencode.ai/inference/anthropic"
export ANTHROPIC_AUTH_TOKEN="oc_sk_..."
claude --model claude-sonnet-5-5
```

把 `oc_sk_...` 替换为[个人 API 密钥](../index.md#get-an-api-key)。

## 配置

在 `~/.claude/settings.json` 中设置这些变量，即可在每个会话中使用 Console。把 `opus`、`sonnet` 和 `haiku` 别名映射到 Console 模型，这样 `/model` 和后台任务就会使用它们。

```json title="~/.claude/settings.json"
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://opencode.ai/inference/anthropic",
    "ANTHROPIC_AUTH_TOKEN": "oc_sk_...",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "claude-opus-5-5",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-sonnet-5-5",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "claude-haiku-5-5"
  }
}
```

Claude Code 会在基础 URL 后追加 `/v1/messages`，因此不要在基础 URL 中包含该路径。运行 `/status` 确认基础 URL 和 token 已生效。

<Callout>
  请使用 `ANTHROPIC_AUTH_TOKEN`，而不是 `ANTHROPIC_API_KEY`。如果你已登录 Claude 账户，请先运行 `/logout`，以免 Claude Code 把该登录信息发送给 Console。
</Callout>

## Go

使用 Go 基础 URL 和来自拥有 [Go](../../go/index.md) 订阅的工作区的密钥。

```json title="~/.claude/settings.json"
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://opencode.ai/inference/go/anthropic",
    "ANTHROPIC_AUTH_TOKEN": "oc_sk_...",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "minimax-m3",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "claude-haiku-5-5"
  }
}
```

## 模型

可以使用 [Console](../../models/index.md#endpoints) 或 [Go](../../go/index.md#endpoints) 表格中的任何模型 ID。在会话中用 `/model` 切换模型，或为单次运行指定一个模型。

```bash
claude --model gpt-6.1-sol
```

## Console MCP

为你的所有项目添加 [Console MCP](../index.md#console-mcp) 服务器。

```bash
claude mcp add --transport http --scope user opencode-console https://opencode.ai/console/mcp
```

在 Claude Code 中运行 `/mcp`，选择 `opencode-console`，然后在浏览器中完成登录。
