---
source_url: https://opencode.ai/docs/console/api/inference/
source_hash: sha256:3e4f439887e0433c5178ef86563a788948b885119638b05260c003618358165d
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# 推理 API

Console 推理服务在 `https://opencode.ai/inference` 提供 OpenAI、Anthropic 和 Gemini 兼容的 API。向与模型 API 家族匹配的端点发送 JSON `POST` 请求。

```bash
curl -X POST "https://opencode.ai/inference/openai/v1/chat/completions" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "kimi-k3",
    "messages": [{ "role": "user", "content": "Say hi" }]
  }'
```

## 身份验证

把 `<token>` 替换为在 [Console](https://opencode.ai/console) 中创建的[个人 API 密钥](../index.md#个人-api-密钥)或[服务账户密钥](../index.md#服务账户)。付费模型需要该请求头。免费层级的对话模型只能在 OpenCode 内部使用；其他客户端会收到 HTTP `403`，即使带有 API 密钥也一样。其他客户端请使用付费模型或 [Go](../../go/index.md) 订阅。

```text
Authorization: Bearer <token>
```

## 端点

| API                     | 路径                                                      |
| ----------------------- | --------------------------------------------------------- |
| OpenAI Chat Completions | `/inference/openai/v1/chat/completions`                   |
| OpenAI Responses        | `/inference/openai/v1/responses`                          |
| Anthropic Messages      | `/inference/anthropic/v1/messages`                        |
| Gemini                  | `/inference/google/v1beta/models/<model>:generateContent` |

每个模型只由一个 API 家族提供服务。参见[模型端点](../../models/index.md#endpoints)表，或获取实时列表：

```bash
curl https://opencode.ai/inference/v1/models
```

### OpenAI Chat Completions

`kimi-k3`、`glm-5.3`、`minimax-m3` 等开放模型以及免费模型使用 Chat Completions API。

```bash
curl -X POST "https://opencode.ai/inference/openai/v1/chat/completions" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "glm-5.3",
    "messages": [{ "role": "user", "content": "Say hi" }]
  }'
```

### OpenAI Responses

GPT 模型使用 Responses API。

```bash
curl -X POST "https://opencode.ai/inference/openai/v1/responses" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-6.1-sol",
    "input": "Say hi"
  }'
```

### Anthropic Messages

Claude 和 Qwen 模型使用 Messages API。必须提供 `max_tokens`。

```bash
curl -X POST "https://opencode.ai/inference/anthropic/v1/messages" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-sonnet-5-5",
    "max_tokens": 1024,
    "messages": [{ "role": "user", "content": "Say hi" }]
  }'
```

### Gemini

Gemini 模型把模型和方法放在路径中。把 `:generateContent` 替换为 `:streamGenerateContent` 即可流式获取响应。

```bash
curl -X POST "https://opencode.ai/inference/google/v1beta/models/gemini-4-argon:generateContent" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{ "parts": [{ "text": "Say hi" }] }]
  }'
```

## 费用

每个响应都会在相应 API 本就返回的用量旁边报告这次请求花费了多少钱：OpenAI 和 Anthropic 在 `usage` 中，Gemini 在 `usageMetadata` 中。流式响应在携带最终用量的事件上报告它：带 `stream_options.include_usage` 的 Chat Completions 的最终用量块、Responses 的 `response.completed`、Messages 的 `message_delta`，以及 Gemini 的最后一个块。

```json
"usage": {
  "prompt_tokens": 1200,
  "completion_tokens": 300,
  "cost": 0.00412,
  "opencode": {
    "billing_source": "balance",
    "list_cost": 0.00412,
    "tokens": { "input": 1200, "output": 300, "reasoning": 120, "cache_read": 8000, "cache_write_5m": 0, "cache_write_1h": 0 }
  }
}
```

| 字段                      | 含义                                                                                                                         |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `cost`                    | 从你的余额中扣除的美元金额。免费模型以及 [Go](../../go/index.md) 限额内的用量为 `0`。使用你自己的 provider 密钥时，是按你的 provider 收费估算的金额（除非它自己报告）；模型没有定价时则没有该字段。 |
| `opencode.billing_source` | `free`、`balance`、`go`、`go-plus` 或 `byok`（你自己的 provider 密钥）。                                                      |
| `opencode.list_cost`      | 按模型定价计算的美元金额，包含高峰时段和长上下文定价。                                                                        |
| `opencode.estimated`      | 当 `cost` 是按模型定价估算的金额，而不是 OpenCode 实际扣收的金额时为 `true`。仅在使用你自己的 provider 密钥时设置。            |
| `opencode.allowance`      | 仅限 Go：这次请求计入你的[用量限制](../../go/index.md#usage-limits)的份额，以套餐月度限额的美元数计。                         |
| `opencode.tokens`         | 向你计费的 token。`input` 不含缓存读写；`output` 包含 `reasoning`。                                                           |

图片生成会在响应上报告同样的字段；对于流式响应，也会在每张完成的图片上报告累计费用。费用在响应结束时即已确定，先于你的余额或 Go 用量更新。如果你的余额或 Go 限额在请求中途耗尽，实际扣收金额可能低于报告值，但绝不会更高。
