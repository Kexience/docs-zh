---
source_url: https://opencode.ai/docs/console/api/providers/
source_hash: sha256:4d8eea8e003542e250db42e6b57df6b9eea9477e72ec92376db2dbd144e6a86b
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# Providers API

连接到你工作区的每个 [provider](../../providers/index.md)都会通过 Console 网关在自己的 URL 上提供服务。`/connect` 之后 OpenCode 会自动使用它；你也可以直接调用它，以便在自己的工具中使用同样的 provider。Console 会在转发前附加 provider 凭据，因此 provider 密钥永远不会离开工作区。

```bash
curl -X POST "https://opencode.ai/inference/custom/conn_.../chat/completions" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-v4.1-flash",
    "messages": [{ "role": "user", "content": "Say hi" }]
  }'
```

## Provider URL

从 **Providers** 下该 provider 的页面复制 **Console API URL**。

```text
https://opencode.ai/inference/custom/<connection_id>
```

## 身份验证

把 `<token>` 替换为在 Console 中创建的[服务账号密钥](../index.md#service-accounts)。Console 会在转发前把它换成该连接的凭据。

```text
Authorization: Bearer <token>
```

Console 也会从 `x-api-key`、`api-key` 或 `x-goog-api-key` 中读取密钥，因此将 provider SDK 指向 Console API URL 时也能正常工作。

## 端点

把 provider 的 API 路径附加到 Console API URL 之后。Console 会将请求转发到该连接的 base URL，并原样返回 provider 的响应。

| 格式                 | 路径                              |
| -------------------- | --------------------------------- |
| Chat Completions     | `/chat/completions`               |
| Responses API        | `/responses`                      |
| Anthropic 兼容       | `/messages`                       |
| Google Generative AI | `/models/<model>:generateContent` |

按 provider 页面上显示的样子发送模型 ID。当模型在上游有不同的 API ID 时，Console 会自动改写。未在该连接上启用的模型请求会被拒绝。

### Chat Completions

```bash
curl -X POST "https://opencode.ai/inference/custom/conn_.../chat/completions" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-v4.1-flash",
    "messages": [{ "role": "user", "content": "Say hi" }]
  }'
```

### Responses API

```bash
curl -X POST "https://opencode.ai/inference/custom/conn_.../responses" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-6.1-sol",
    "input": "Say hi"
  }'
```

### Anthropic 兼容

`max_tokens` 为必填项。

```bash
curl -X POST "https://opencode.ai/inference/custom/conn_.../messages" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-sonnet-5-5",
    "max_tokens": 1024,
    "messages": [{ "role": "user", "content": "Say hi" }]
  }'
```

### Google Generative AI

模型和方法都是路径的一部分。把 `:generateContent` 替换为 `:streamGenerateContent` 即可流式接收响应。

```bash
curl -X POST "https://opencode.ai/inference/custom/conn_.../models/gemini-4-argon:generateContent" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{ "parts": [{ "text": "Say hi" }] }]
  }'
```

## 用量

请求会按照每个模型上设置的价格计入[预算](../../budgets/index.md)。token 费用由 provider 直接向你收取。
