---
source_url: https://opencode.ai/docs/console/providers/
source_hash: sha256:8b2c090128878fcb4ec086e20801d7382dfdfb700716a25490c24c1ad31ebf7a
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# Providers

连接你已经在付费的 provider 账号，例如 Anthropic、OpenAI 或 AWS Bedrock，并与工作区中的所有成员共享它们的模型。Console 会存储凭据并通过其网关提供每个 provider，因此成员可以直接使用这些模型，而永远看不到 provider 密钥。你自己的工具也可以通过 [Providers API](../api/providers/index.md) 使用同一个网关。

所有者和管理员可以在 **Providers** 标签页中管理 provider。成员在运行 `/connect` 之后即可在 OpenCode 中使用已启用的模型。

## 连接 provider

1. 打开 **Providers**，点击 **Connect Provider**。
2. 从目录中选择一个 provider，并输入其 API key。
3. 可以选择点击 **Test connection**，然后点击 **Save**。

目录中包括 Anthropic、OpenAI、Google、xAI、DeepSeek、Mistral、Groq、OpenRouter 等众多 provider。目录 provider 已预先配置好各自的模型。

### 云端 provider

云端 provider 需要一些额外的细节。

| Provider | 详细信息 |
| --------------------- | ------------------------------------- |
| Azure | 资源名称和 API key |
| AWS Bedrock | 区域和 API key |
| Google Vertex AI | 区域和服务账号 JSON |
| Cloudflare AI Gateway | 账号 ID、Gateway ID 和 API token |
| Databricks | 工作区 URL 和 token |

### 自定义 provider

点击 **Add Custom Provider** 可以连接任何其他端点，然后通过 **Add Model** 添加其模型。

| 字段 | 说明 |
| ---------- | ------------------------------------------------------------------------------- |
| Base URL | Console 转发请求的位置，例如 `https://api.deepseek.com/v1`。 |
| Format | Chat Completions、Responses API、Anthropic Compatible 或 Google Generative AI。 |
| Auth mode | Bearer、API key 请求头或自定义请求头。 |
| Credential | Console 发送给该 provider 的密钥。 |

## 选择模型

打开一个 provider 可以查看它的模型。只有已启用的模型才对成员可用。

- 使用 **Enabled** 开关来打开或关闭某个模型。
- 打开 **New models** 可以启用该 provider 未来新增的模型。

## 编辑模型

点击某个模型即可编辑它。关闭面板时更改会被保存。

| 部分 | 可以修改的内容 |
| ------------- | --------------------------------------------------------------- |
| General | 显示名称、API ID、工具支持、输入和输出类型 |
| Variants | 拥有各自请求头或主体的变体 |
| Configuration | 默认变体、请求头和请求体、token 限制 |
| Cost Tiers | 每 1M token 的输入、输出、缓存读取和缓存写入价格 |

### 自定义定价

目录模型初始使用 provider 的标价。如果你有协商的价格（例如 OpenAI 合同上的折扣），可以在 **Cost Tiers** 下覆盖价格，让用量报告和[预算](../budgets/index.md)与你的实际支出一致。

| 字段 | 标价 | 你的价格 |
| ---------------- | ---------- | ---------- |
| Input price | $2.50 | $2.00 |
| Output price | $15.00 | $12.00 |
| Cache read price | $0.25 | $0.20 |

你修改过的价格会在 provider 页面上高亮显示。使用字段上的 **Restore default value**，或模型上的 **⋯ › Restore...**，即可恢复为标价。

当某个模型在超过某个上下文大小时收费更高（例如超过 200K token 的提示词），可以添加一个 **Context** 档位。

### 自定义模型

点击 **Add Model** 可以添加目录中没有的模型，包括其 **Display name** 和 **Model ID**。在现有模型上使用 **⋯ › Duplicate...** 可以从它的设置开始。

## OpenCode 模型

**Models** 标签页管理 Console 提供的[模型](../models/index.md)，这些模型从工作区额度中扣费。它的工作方式与 provider 页面类似：

- 打开或关闭单个模型。
- 关闭 **Free models** 可以为工作区屏蔽免费模型。
- 打开 **New models** 可以自动启用新的 Console 模型。

通过 **⋯ › Disable** 禁用整个 provider，即可只使用你自己的 provider。

## 在 OpenCode 中使用

成员运行 `/connect` 并选择工作区。每个已启用的 provider 会显示为工作区名称后跟 provider 名称，`/models` 会列出其已启用的模型。

```text
Acme Inc. / Anthropic
```

在 **Settings › General** 中打开 **Managed providers only**，可以为所有人把 OpenCode 限制在工作区的 provider 之内。

## 发送身份

当 provider 是你自己运行的网关时，可以在其页面打开 **Send identity**。此后，Console 会在发送到那里的每个模型请求中添加一个 `x-opencode-actor` 请求头。该请求头指明请求背后的成员或服务账号，这样你的网关就可以按发送者记录或限制请求。

```text
x-opencode-actor: eyJhbGciOiJFUzI1NiIsInR5cCI6Im9wZW5jb2RlLWFjdG9yK2p3dCIsImtpZCI6Ii4uLiJ9...
```

- 它默认关闭，更改 base URL 会将其关闭。
- 仍处于供应商自身 API 的 provider（例如 `https://api.openai.com/v1`）不会显示该设置，因为供应商会忽略这个请求头。
- Console 会移除客户端发送的任何 `x-opencode-*` 请求头，因此你的网关收到的唯一 `x-opencode-actor` 就是 Console 签署的那一个。
- **Test connection** 和模型列表调用使用凭据单独请求 `GET <base URL>/models`，因此不要在该路由上要求这个请求头。

### Token

该请求头是一个由 Console 为每个请求签署的 JWT。

| 字段 | 值 |
| ------------ | ------------------------------------------------ |
| `alg` | `ES256` |
| `typ` | `opencode-actor+jwt` |
| `iss` | `https://opencode.ai/inference` |
| `aud` | provider 的 base URL，不含末尾斜杠 |
| `iat`, `exp` | `exp` 是 `iat` 之后 120 秒 |

| 声明 | 值 |
| -------------------- | ---------------------------------------------------------------------- |
| `sub` | 成员为 `user_id`，否则为 `service_account_id` |
| `workspace_id` | 请求所在的工作区 |
| `user_id`, `email` | 该成员（当请求由成员发送时） |
| `service_account_id` | 该服务账号（当请求由服务账号发送时，包括 agent） |
| `session_id` | 客户端的会话 ID（当它发送了会话 ID 时） |
| `request_id` | 客户端在 `x-opencode-log-id` 响应头中收到的 ID |

成员的请求携带如下负载：

```json
{
  "iss": "https://opencode.ai/inference",
  "aud": "https://llm.example.com/v1",
  "sub": "user_...",
  "workspace_id": "org_...",
  "user_id": "user_...",
  "email": "ada@example.com",
  "session_id": "ses_...",
  "request_id": "019a6e8f-24a0-7b12-9c3d-4e5f6a7b8c9d",
  "iat": 1794500000,
  "exp": 1794500120
}
```

### 校验 token

Console 在 `https://opencode.ai/inference/.well-known/jwks.json` 发布其公钥，并附带 `Cache-Control: public, max-age=300`。请依次检查签名、签发者、受众、类型和时效，然后检查工作区。下面的示例使用 [jose](https://github.com/panva/jose)。

```ts
import { createRemoteJWKSet, jwtVerify } from "jose"

const keys = createRemoteJWKSet(new URL("https://opencode.ai/inference/.well-known/jwks.json"))

export async function sender(request: Request) {
  const token = request.headers.get("x-opencode-actor")
  if (!token) throw new Error("Missing x-opencode-actor")
  const { payload } = await jwtVerify(token, keys, {
    issuer: "https://opencode.ai/inference",
    audience: "https://llm.example.com/v1",
    algorithms: ["ES256"],
    typ: "opencode-actor+jwt",
    maxTokenAge: "120s",
    clockTolerance: "5s",
  })
  if (payload.workspace_id !== "org_...") throw new Error("Another workspace")
  return payload
}
```

把 `audience` 设置为 Console 中保存的 provider base URL（不含末尾斜杠），并把 `org_...` 替换为你的 Console URL 中的工作区 ID。Console 会在使用新的签名密钥之前先发布它，因此按 `kid` 查找密钥的校验器（正如 `createRemoteJWKSet` 所做的那样）可以在密钥轮换期间持续工作。

## 禁用或移除

打开 provider 的 **⋯** 菜单：

- **Disable** 会向成员隐藏该 provider 及其模型，但保留其设置。
- **Remove...** 会删除该 provider 及其模型。对话框会显示最近有谁使用过它，并提供 **Disable instead** 选项。

要轮换密钥，请点击 provider 页面上的凭据并输入新的密钥。

## 计费

token 由 provider 向你收费；Console 不会为它们收取额度。Console 仍然会使用模型的定价记录每个请求及其成本，因此用量报告和[预算](../budgets/index.md)会包含这部分。

如果你想在 OpenCode 之外从自己的工具调用 provider，请使用 [Providers API](../api/providers/index.md)。
