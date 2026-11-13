---
source_url: https://opencode.ai/docs/providers/
source_hash: sha256:b3b18400a1f4f320785fac00adc41dfb03469ac1ab92ac361f08945f17c3ab29
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# Provider

OpenCode 内置来自 [models.dev](https://models.dev) 的 provider 与模型目录。对大多数 provider 而言，先连接账号，再选择模型。

## 设置

运行 `/connect`，选择一个 provider 并输入其凭证。然后运行 `/models` 选择它的一个模型。

```text
/connect
/models
```

## Go

[OpenCode Go](../console/go/index.md) 是一项可选订阅，涵盖经 OpenCode 团队测试的编程模型。在[控制台](https://opencode.ai/console)中订阅，复制你的 API key，然后以 **OpenCode Go** 的身份连接。

```text
/connect
# Select OpenCode Go, then paste your API key.
/models
```

用量限制、endpoint 和隐私细节请参阅 [Go 指南](../console/go/index.md)。

## ChatGPT

可以使用 ChatGPT Plus 或 Pro 计划来代替 OpenAI API key。连接 **OpenAI**，然后选择 **Sign in with ChatGPT** 或某一种旧版 **Codex** 登录方式。用量会计入你的计划，因此这些模型不显示费用。

```text
/connect
/models
```

### 上下文限制

默认情况下，OpenCode 会把这些登录方式的上下文窗口限制在每个模型真实上限以下。这些上限与 Codex 的默认值一致，因此你的计划用量的消耗速率与其他 OpenAI 产品相近。

| 模型                  | 输入上限   |
| --------------------- | ----------- |
| GPT-6.1 Sol 及更新    | 500,000     |
| 更早的模型            | 272,000     |

如果不想启用，可在配置中禁用这个上限插件。`-` 前缀会关闭一个内置插件；其他所有插件保持启用。

```jsonc title="opencode.jsonc"
{
  "plugins": ["-opencode.provider.openai-context-caps"],
}
```

## 自定义

当某个 provider 的 API 不在目录中时，可以自行添加。下面这个兼容 OpenAI 的示例一次性定义了凭证、运行时包、endpoint 和第一个模型。

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "providers": {
    "acme": {
      "name": "Acme",
      "env": ["ACME_API_KEY"],
      "package": "@opencode/ai/providers/openai-compatible",
      "settings": {
        "baseURL": "https://llm.acme.example/v1",
      },
      "models": {
        "qwen3-coder": {
          "name": "Qwen 3 Coder",
        },
      },
    },
  },
}
```

`providers` 对象以模型引用中使用的 provider ID 为键，例如 `acme/qwen3-coder`。

| 字段 | 用途 |
| --- | --- |
| `name` | 显示名称。 |
| `env` | 可提供凭证的环境变量名的有序列表。 |
| `package` | 运行时 provider 包。 |
| `canonical` | 该 provider 继承其目录默认值的内置 provider ID。 |
| `compatibility` | 该 provider 下所有模型共享的 API 兼容性问题。参见[兼容性](../models/index.md#compatibility)。 |
| `settings` | 类型化的 OpenCode 控制项，以及传给运行时包的 JSON 选项。 |
| `headers` | 添加到请求中的字符串型 HTTP header。 |
| `body` | 合并进请求体的 JSON 字段。 |
| `models` | 要添加或覆盖的模型，以 OpenCode 模型 ID 为键。 |

## Endpoint

覆盖 `settings.baseURL` 可以让目录中的 provider 走代理或兼容 endpoint。它原有的包、模型和连接方式仍然生效。

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "providers": {
    "anthropic": {
      "settings": {
        "baseURL": "https://llm-proxy.example.com/anthropic",
      },
    },
  },
}
```

`settings` 取决于所用的包。只有所选包支持时，字段才会生效。

## 请求

用 `headers` 设置额外的 HTTP header，用 `body` 设置需要合并进每个请求体的 JSON 字段。

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "providers": {
    "openai": {
      "headers": {
        "X-Gateway-Tenant": "engineering",
      },
      "body": {
        "metadata": {
          "application": "opencode",
        },
      },
    },
  },
}
```

当只有 provider 的部分流量需要这种覆盖时，也可以在模型或变体上设置这两个字段。

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "providers": {
    "openai": {
      "models": {
        "gpt-6.1-sol": {
          "headers": { "X-Model-Tier": "coding" },
          "variants": [
            {
              "id": "batch",
              "body": { "service_tier": "flex" },
            },
          ],
        },
      },
    },
  },
}
```

## 超时

HTTP 请求最多等待 5 分钟来获取响应 header，流式响应块之间最多等待 15 分钟。把 provider 的 `settings.headerTimeout` 或 `settings.chunkTimeout` 设为毫秒数可修改限制，设为 `false` 可禁用。`settings.timeout` 还会限制整个请求从发出到响应完成的时长；它没有默认值。这些配置作用于整个 provider，而不是按模型或变体生效。在 WebSocket 传输上，`chunkTimeout` 限制的是帧间隔，默认为 30 分钟。

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "providers": {
    "anthropic": {
      "settings": {
        "headerTimeout": 600000,
        "chunkTimeout": false,
      },
    },
  },
}
```

超出任一限制的请求会以传输错误失败。请求超时后，OpenCode 最多重试三次才放弃。

## 请求编码

`settings.encoding` 会用 `"zstd"` 或 `"gzip"` 压缩 HTTP 请求体，或用 `"none"` 发送纯 JSON。可以在 provider、模型或变体上设置；最具体的值优先。只启用 endpoint 能解码的压缩方式：大多数 provider 和网关会拒绝压缩的请求体。使用 ChatGPT 登录且未配置自定义 `baseURL` 时，OpenAI 默认使用 `"zstd"`；使用 API key 则发送纯 JSON。WebSocket 消息不受影响。

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "providers": {
    "openai": {
      "settings": { "encoding": "none" },
    },
  },
}
```

## 包

`package` 字段选择与 provider 通信的运行时。对于实现了 OpenAI 请求格式的 API，使用兼容运行时。

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "providers": {
    "acme": {
      "package": "@opencode/ai/providers/openai-compatible",
      "settings": {
        "baseURL": "https://llm.acme.example/v1",
      },
      "models": {
        "qwen3-coder": {},
      },
    },
  },
}
```

原生包选项包括：

- `@opencode/ai/providers/openai`
- `@opencode/ai/providers/openai/chat`
- `@opencode/ai/providers/openai/responses`
- `@opencode/ai/providers/openai-compatible`
- `@opencode/ai/providers/openai-compatible/responses`
- `@opencode/ai/providers/anthropic`
- `@opencode/ai/providers/anthropic-compatible`
- `@opencode/ai/providers/google`
- `@opencode/ai/providers/google-vertex`
- `@opencode/ai/providers/google-vertex/gemini`
- `@opencode/ai/providers/google-vertex/chat`
- `@opencode/ai/providers/google-vertex/responses`
- `@opencode/ai/providers/google-vertex/messages`
- `@opencode/ai/providers/azure`
- `@opencode/ai/providers/azure/chat`
- `@opencode/ai/providers/azure/responses`
- `@opencode/ai/providers/amazon-bedrock`
- `@opencode/ai/providers/amazon-bedrock/mantle`
- `@opencode/ai/providers/amazon-bedrock/mantle/chat`
- `@opencode/ai/providers/amazon-bedrock/mantle/messages`
- `@opencode/ai/providers/amazon-bedrock/mantle/responses`
- `@opencode/ai/providers/openrouter`
- `@opencode/ai/providers/xai`

也可以使用 npm 包（例如 `@acme/opencode-provider`），或者用绝对 `file://` URL 指向本地包。

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "providers": {
    "acme": {
      "package": "@acme/opencode-provider",
      "models": { "acme-coder": {} },
    },
  },
}
```

## 模型

在 provider 的 `models` 映射中添加或覆盖模型。映射的键是 OpenCode 使用的模型 ID；`modelID` 更改发送给 provider 的 ID。

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "model": "openai/coding",
  "providers": {
    "openai": {
      "models": {
        "coding": {
          "modelID": "gpt-6.1-sol",
          "name": "GPT-6.1 Sol Coding",
        },
      },
    },
  },
}
```

| 字段 | 用途 |
| --- | --- |
| `modelID` | 发送给 provider 的模型或部署 ID。 |
| `name` | 显示名称。 |
| `family` | 用于对相关模型分组的模型族。 |
| `type` | 模型产出物的类型，如 `chat`、`image` 或 `decision`。默认为 `chat`；只有 chat 模型可用于会话。 |
| `releaseDate` | 发布日期，格式为 `YYYY-MM-DD` 或 `YYYY-MM`。 |
| `package` | 该模型的运行时覆盖。 |
| `settings` | 模型级的 OpenCode 控制项和包特定的 JSON 设置。 |
| `headers` | 额外的字符串型请求 header。 |
| `body` | 额外的 JSON 请求体字段。 |
| `capabilities` | 工具支持、可接受的输入与输出媒体类型、temperature 支持以及推理控制。 |
| `compatibility` | 该模型的 API 兼容性问题，会覆盖 provider 级设置。参见[兼容性](../models/index.md#compatibility)。 |
| `variants` | 具有各自 `settings`、`headers` 和 `body` 的命名变体。 |
| `cost` | 每百万 token 的输入、输出及可选缓存定价。 |
| `limit` | 上下文、输入和输出 token 上限。 |
| `disabled` | 为 `true` 时将该模型从可选项中移除。 |

模型的选择、默认值、能力、上限、费用和变体请参见[模型](../models/index.md)。

## Azure

Azure 的标准目录 endpoint 除了凭证之外还需要资源名称。先设置一次 `settings.resourceName`，然后按 [Provider 账号](../cli/providers/index.md)所述，连接 API key 或使用 Azure CLI 的 Microsoft Entra ID 会话。

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "providers": {
    "azure": {
      "settings": {
        "resourceName": "my-models",
      },
    },
  },
}
```

可以在 [Azure 门户](https://portal.azure.com/)或 [Microsoft Foundry](https://ai.azure.com/)中找到 **Resource name**。它也是 `https://my-models.openai.azure.com/` 和 `https://my-models.services.ai.azure.com/` 这类 endpoint 的第一部分。

```bash
az cognitiveservices account list \
  --query "[].{name:name,resourceGroup:resourceGroup}" \
  --output table
```

要使用 Entra ID，先安装 [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) 并登录，然后在连接 Azure 时选择 **Microsoft Entra ID (Azure CLI)**。

```bash
az login
```

如果配置或环境变量中没有提供资源名称，连接时需要输入。随连接保存的资源名称优先于配置；如需更改，请重新连接。

Azure CLI 连接使用 Azure CLI 中选定的账号。如果资源位于其他租户或订阅，需要显式选择两者。

```bash
az login --tenant TENANT_ID
az account set --subscription NAME_OR_ID
```

也可以不用配置，改由 `AZURE_RESOURCE_NAME` 向 OpenCode 服务器提供资源名称。旧变量 `AZURE_COGNITIVE_SERVICES_RESOURCE_NAME` 同样有效。

### 部署

Azure 只通过部署来提供模型，因此 OpenCode 会列出你资源下的部署，并以此取代完整的 Azure 目录。该列表会在启动后、连接后以及切换账号后在后台加载。要使用之后新添加的部署，请重启 OpenCode 或重新连接。

- 在某个连接的列表加载完成之前，或加载失败时，完整目录仍然可用。
- 同一连接重新加载失败时，会保留其上一次完整的清单。
- 切换账号时绝不会显示上一个账号的清单；新账号从完整目录开始。
- 部署继承其目录模型的限制、费用和能力。

部署名称就是其模型 ID，由于 Azure 忽略名称的大小写，统一为小写，例如 `azure/gpt-production`。以模型命名的部署（如 `gpt-6-luna`）保留目录 ID。在其他部署被添加或移除时，这些 ID 保持稳定。

OpenCode 根据部署所发布的模型将其与目录匹配；当 Azure 对模型的拼写不同（如以 `gpt-4` 表示 GPT-4 Turbo）时，则按名称匹配。以另一个模型命名的部署（例如部署 `gpt-6-luna` 的 `gpt-6.1-sol`）会显示那个模型的名称、限制和费用。

使用 Azure CLI 时，OpenCode 通过 Azure 管理 API 列出部署，这需要对资源的读取权限。如果失败（使用 API key 时则始终如此），会改用资源的旧版部署清单。发现过程会读完所有分页后才发布列表。自定义 `settings.baseURL` 会保留完整目录。

当部署的模型不在目录中（例如微调模型），或者想自行把模型 ID 映射到部署时，可以显式配置该部署。OpenCode 会记录一条警告，指出这些部署。显式配置的模型始终保留。

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "providers": {
    "azure": {
      "models": {
        "gpt-6-luna": {
          "modelID": "gpt-production",
        },
      },
    },
  },
}
```

你的身份需要具备以下角色之一：

- Azure OpenAI 模型需要 **Cognitive Services OpenAI User**。
- 其他 Foundry 模型需要 **Cognitive Services User**。

如果请求使用了错误租户的 token，请以所需的租户重新登录。

```bash
az login --tenant TENANT_ID
```

## Bedrock

Amazon Bedrock 使用 AWS 默认凭证链。具名 AWS profile 是最简单的持久配置；OpenCode 也识别访问密钥环境变量、web 身份和容器凭证。

```bash
aws configure sso --profile work
aws sso login --profile work
```

在 provider 设置中选择 profile 和区域。配置了 `profile`、`AWS_PROFILE`、`AWS_ACCESS_KEY_ID`、web 身份 token 文件或容器凭证 URI 之一即可激活该 provider；仅有区域则不会。

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "providers": {
    "amazon-bedrock": {
      "settings": {
        "profile": "work",
        "region": "us-west-2",
      },
    },
  },
}
```

未显式指定区域时，OpenCode 依次使用 `AWS_REGION`、`AWS_DEFAULT_REGION`，最后是 `us-east-1`。对于私有或 VPC endpoint，设置 `baseURL` 即可，profile 和区域保持不变。

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "providers": {
    "amazon-bedrock": {
      "settings": {
        "profile": "work",
        "region": "us-west-2",
        "baseURL": "https://bedrock-runtime.vpce.example.com",
      },
    },
  },
}
```

Bedrock API key 使用 `AWS_BEARER_TOKEN_BEDROCK`。其他 AWS 变量用于 SigV4，不会作为 OpenCode 的 API key 账号存储。

## Vertex

Google Vertex 使用应用默认凭证（ADC），并且需要先指定项目，模型才可用。先创建本地 ADC，再在 provider 设置中设置项目和位置。

```bash
gcloud auth application-default login
```

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "providers": {
    "google-vertex": {
      "settings": {
        "project": "my-project",
        "location": "us-central1",
      },
    },
  },
}
```

OpenCode 还会按此顺序从 `GOOGLE_VERTEX_PROJECT`、`GOOGLE_CLOUD_PROJECT`、`GCP_PROJECT` 或 `GCLOUD_PROJECT` 解析项目。位置则从 `GOOGLE_VERTEX_LOCATION`、`GOOGLE_CLOUD_LOCATION` 或 `VERTEX_LOCATION` 解析，默认为 `us-central1`。

```bash
GOOGLE_CLOUD_PROJECT=my-project GOOGLE_VERTEX_LOCATION=europe-west4 opencode --standalone
```

服务账号走同样的 ADC 路径。将 `GOOGLE_APPLICATION_CREDENTIALS` 指向服务账号 JSON 文件，同时仍需通过设置或上述项目变量之一提供项目。

```bash
GOOGLE_APPLICATION_CREDENTIALS=/secure/vertex.json \
GOOGLE_CLOUD_PROJECT=my-project \
opencode --standalone
```

Gemini、Anthropic 以及兼容 OpenAI 的 Vertex 目录模型统一使用 `google-vertex` 这一个 provider ID。旧的 `google-vertex-anthropic` provider ID 在 V2 中已不可用。

## Copilot

GitHub Copilot 支持设备 OAuth，而不是手动输入 API key。连接 **GitHub Copilot**，选择 GitHub.com 或 GitHub Enterprise，完成设备流程，然后打开 `/models`。

```text
/connect
# Select GitHub Copilot, then Login with GitHub Copilot.
/models
```

对于 GitHub Enterprise，在提示时输入部署 URL 或域名。当 GitHub 返回 Copilot API endpoint 时，OpenCode 会使用它；否则从企业域名推导 endpoint。

```text
company.ghe.com
```

连接的账号需要拥有 Copilot Chat 权限。如果 GitHub 显示没有授权，请注册 Copilot Free 或让组织分配 Copilot 席位，然后重新连接。OpenCode 会在登录后以及活动的 Copilot 账号变化时获取该账号当前的模型列表。

## Ollama

启动 Ollama 并拉取一个模型。OpenCode 会探测 `http://127.0.0.1:11434`，发现补全类模型，并在无需连接账号的情况下把它们加入 `/models`。

```bash
ollama serve
ollama pull qwen3:8b
```

通过 `settings.baseURL` 将 OpenCode 指向远程或代理的 Ollama 服务器。路径中要包含 `/v1`；OpenCode 会据此推导原生的 `/api/tags` 和 `/api/show` 发现路径。`apiKey` 是可选的，会以 bearer token 的形式随发现和模型请求发送。

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "providers": {
    "ollama": {
      "settings": {
        "baseURL": "https://ollama.example.com/v1",
        "apiKey": "{env:OLLAMA_API_KEY}",
      },
    },
  },
}
```

发现过程会定期刷新，并在临时故障期间保留上一次成功的清单。纯嵌入模型不会出现，因为 OpenCode 只添加 Ollama 元数据中包含 `completion` 能力的模型。

## 运行时

LM Studio 和 vLLM 也有内置的本地发现。它们的默认 endpoint 是 `http://127.0.0.1:1234/v1` 和 `http://127.0.0.1:8000/v1`。

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "providers": {
    "lmstudio": {
      "settings": { "baseURL": "http://gpu-host:1234/v1" },
    },
    "vllm": {
      "settings": { "baseURL": "http://gpu-host:8000/v1" },
    },
  },
}
```

LM Studio 从 `/api/v1/models` 发现语言模型。vLLM 在读取 `/v1/models` 之前会先检查 `/health`；它的发现机制无法推断工具支持，因此发现的 vLLM 模型初始为禁用工具。对于其他兼容 OpenAI 的运行时，使用[自定义 provider](#自定义)方案并显式列出其模型。

## 网关

OpenRouter 使用其原生运行时和目录。向 OpenCode 服务器提供 `OPENROUTER_API_KEY` 或连接 OpenRouter 账号，然后在 provider 前缀之后使用完整的 OpenRouter 模型 ID 引用模型。

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "model": "openrouter/anthropic/claude-sonnet-5.5",
}
```

在覆盖其 endpoint 或经由兼容 OpenRouter 的网关路由时，保留原生 OpenRouter 包。这样可保持 OpenRouter 的请求与推理行为不变。

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "providers": {
    "openrouter": {
      "settings": {
        "baseURL": "https://openrouter-gateway.example.com/api/v1",
      },
      "headers": {
        "X-Gateway-Tenant": "engineering",
      },
    },
  },
}
```

对于暴露兼容 OpenAI 的 API 但拥有自己模型清单的网关，应改用自定义 provider。配置键会成为 provider 前缀，每个 `models` 键会成为可选的模型 ID。

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "model": "company/coder",
  "providers": {
    "company": {
      "env": ["COMPANY_GATEWAY_KEY"],
      "package": "@opencode/ai/providers/openai-compatible",
      "settings": {
        "baseURL": "https://gateway.example.com/v1",
      },
      "models": {
        "coder": { "modelID": "upstream/coder-v2" },
      },
    },
  },
}
```

## 错误

Provider 和模型错误通常能指明失败阶段。在更换包之前，先检查服务器进程的环境变量和确切的模型 ID。

| 错误或现象 | 排查 |
| --- | --- |
| `No model is available for session ...` | 当前没有可选择的已启用模型。完成该 provider 特定的设置，然后在 `/models` 中选择模型。 |
| `Model unavailable: provider/model` | provider 未启用、模型 ID 不存在或已禁用，或动态发现不再返回该模型。对于自定义别名，检查 `models` 映射的键而不是 `modelID`。 |
| `Cannot initialize provider/model: NAME is required to resolve the provider endpoint` | `baseURL` 中仍留有 `${NAME}` 占位符。在 OpenCode 服务器上设置该变量，或把模板替换为完整的 endpoint。 |
| `Azure resource name is missing` | 设置 `providers.azure.settings.resourceName`、`AZURE_RESOURCE_NAME`，或提供完整的 `settings.baseURL`。 |
| Vertex 未出现 | 在 provider 设置中设置可解析的项目，或使用受支持的项目变量。仅有 ADC 不会激活该 provider。 |
| Bedrock 未出现 | 提供 profile 或其他受支持的 AWS 凭证链输入。仅 `AWS_REGION` 只选择区域。 |
| Ollama 没有模型 | 确认服务器在从 `baseURL` 推导出的路径上暴露 `/api/tags` 和 `/api/show`，且 `/api/show` 报告了 `completion` 能力。 |
| Copilot 没有模型 | 确认活动的 OAuth 账号拥有 Copilot Chat 权限。模型同步失败会记录为 `failed to sync GitHub Copilot models`。 |

V2 会拒绝已弃用的 provider ID 并给出直接替代项。用 `azure/<model>` 替代 `azure-cognitive-services/<model>`，用 `google-vertex/<model>` 替代 `google-vertex-anthropic/<model>`。

## WebSockets

OpenAI、xAI 以及受支持的 Azure Responses 模型可以在每个会话中保持一条 WebSocket 连接。连续的步骤会复用未变化的请求前缀，只发送自上次响应以来新增的内容，从而减少长会话中的上传量。

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "providers": {
    "openai": {
      "settings": { "transport": "http" },
    },
  },
}
```

WebSocket 行为遵循以下规则：

- 内置 provider 会按各自的策略为受支持的路由启用。
- provider 的 `settings.transport: "websocket"` 会启用它；`"http"` 则禁用。
- 在没有 WebSocket 通道的路由上设置 `"websocket"` 会记录警告并回退到 HTTP。
- OpenAI provider 的压缩（compaction）也使用同一条连接。
- xAI 仅从已存储的响应继续。在其默认的 `store: false` 下，每个步骤都会通过复用的连接完整发送。
- 关闭的 socket 会在下一步重连。如果连接无法建立，会话会改用 HTTP 继续。
- 带 `http.request` 或 `http.response` 钩子的 provider 插件保持使用 HTTP，以便每个请求都可被观察。
