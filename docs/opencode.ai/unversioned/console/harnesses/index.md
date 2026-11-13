---
source_url: https://opencode.ai/docs/console/harnesses/
source_hash: sha256:11e10188ae973e804c40dfe98e8a4b0e2c8ef89ee6546ce8d2ab82d06948725d
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# Harnesses

Console 可以与 OpenCode 之外的编码 agent 配合使用。把一个 harness 通过 API key 指向 Console 网关，即可使用任何付费模型或 Go 模型，用量会像其他请求一样计入你的工作区。

| Harness | 按量付费 | Go | MCP |
| --------------------------------------------- | ------------- | --------- | --- |
| [Claude Code](claude-code/index.md) | 是 | 是 | 是 |
| [Codex](codex/index.md) | 是 | 是 | 是 |
| [Hermes](hermes/index.md) | 内置 | 内置 | 是 |
| [Pi](pi/index.md) | 内置 | 内置 | 是 |
| [Raycast](raycast/index.md) | 扩展 | 扩展 | 是 |

免费档的聊天模型只能在 OpenCode 内部使用。其他 harness 对这些模型会收到 HTTP `403`，即使持有 Console API key 也一样。请使用付费模型或 Go 订阅。

## 获取 API key

harness 使用 Console API key 进行认证。最快的选择是[个人 API key](../api/index.md#personal-api-keys)，它会以你的身份调用模型。

1. 在 [Console](https://opencode.ai/console) 的账号菜单中打开 **Account**。
2. 在 **Personal API keys** 下，点击 **Add API key**。
3. 选择工作区，为密钥命名，然后点击 **Create**。
4. 复制该密钥。它只显示一次。

```text
oc_sk_1a2b3c4d5e6f_...
```

用量会计入你的[成员预算](../budgets/index.md#member-budgets)。按量付费请使用有额度的工作区的密钥；使用 Go 请使用订阅了 [Go](../go/index.md) 的工作区的密钥。

对于共享机器或 CI，所有者和管理员可以改为创建[服务账号](../api/index.md#service-accounts)密钥，这样用量就不会绑定到某个人。

## Base URL

按量付费和 Go 由不同的 base URL 提供。请使用与你的方案匹配的那一个。

| 方案 | Base URL |
| ------------- | ---------------------------------- |
| 按量付费 | `https://opencode.ai/inference` |
| Go | `https://opencode.ai/inference/go` |

在其后追加你的 harness 所讲 API 的路径。每个 API 都提供所有付费模型和 Go 文本模型：当模型本身讲某个 API 时，Console 会把请求发送到该模型自己的端点，否则进行翻译。

| API | 路径 |
| ----------------------- | ----------------------------------------------- |
| OpenAI Responses | `/openai/v1/responses` |
| OpenAI Chat Completions | `/openai/v1/chat/completions` |
| Anthropic Messages | `/anthropic/v1/messages` |
| Gemini | `/google/v1beta/models/<model>:generateContent` |

```text
https://opencode.ai/inference/go/openai/v1/chat/completions
```

## 会话

在每次请求中发送一个稳定的会话 ID，这样 Console 可以一致地路由一段对话并复用其提示缓存。Go [要求](../go/index.md#where-can-i-use-it)这样做。

```text
x-opencode-session: ses_...
```

Console 也识别 Claude Code、Codex、Hermes 和 Pi 发送的原生会话请求头，因此它们无需额外配置。

## Console MCP

支持 MCP 的 harness 可以通过 Console MCP 服务器管理工作区。它使用带动态客户端注册的 OAuth，因此你从浏览器登录，而不是粘贴密钥。

```text
https://opencode.ai/console/mcp
```

每个 harness 页面都说明了如何添加它。当你的工作区启用该服务器时，OpenCode 会自动把它添加为 `opencode_console`，并在首次使用时要求你从浏览器登录。
