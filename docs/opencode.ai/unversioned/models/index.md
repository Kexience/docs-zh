---
source_url: https://opencode.ai/docs/models/
source_hash: sha256:533ec23167b445fec082f5e24d7621d9977d01f0eabc35dc37868797c642bd17
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---
# 模型

使用 `/models` 为当前会话选择模型：

```text
/models
```

OpenCode 会列出来自 [models.dev](https://models.dev)、provider 集成以及你的配置中的模型。选择器只显示已启用且其 provider 在当前项目中可用的模型。在 [Providers](../providers/index.md) 中连接 provider。

## 选择

从 `/models` 中挑选一个条目，而不必猜测它的 provider 或模型 ID。该选择只作用于当前会话，不会更改你的配置。

```text
anthropic/claude-sonnet-5-5
```

可用性是按项目划分的：

- 模型必须已启用。
- 它的 provider 必须在当前项目中可用。
- 来自其他项目的凭据和配置不会自动带入。

## 单次运行

使用 `--model` 为一次命令行运行选择模型，而不更改已配置的默认值：

```bash
opencode run --model anthropic/claude-sonnet-5-5 "Refactor parseToken"
```

agent 和命令也可以选择自己的模型。请参阅 [Agents](../agents/index.md) 和 [Commands](../commands/index.md)。

## 默认值

在 `opencode.json` 或 `opencode.jsonc` 中设置 `model`，为新任务选择默认模型：

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-sonnet-5-5",
}
```

当配置的模型已启用且其 provider 可用时，它会成为目录中的默认值。否则，OpenCode 会回退到最新的可用受支持模型。

- 会话已经选择的模型优先于配置的默认值。
- 切换会话的模型不会重写配置文件。
- 根级 `model` 目前只保留默认的 provider 和模型，不保留 variant。

配置文件的位置和优先级请参阅 [Config](../config/index.md)。

## 免费模型

在服务器进程上设置 `OPENCODE_DISABLE_FREE_MODELS=1`（或 `true`），可以隐藏 [OpenCode 免费模型](../console/models/index.md#free-models)：

```bash
OPENCODE_DISABLE_FREE_MODELS=1 opencode serve
```

对于共享的后台服务器：

```bash
opencode service set env OPENCODE_DISABLE_FREE_MODELS 1
```

免费指的是没有输入价格的 `opencode` 或 `opencode-go` 模型。这些模型会从目录和默认值中消失；显式选择它们会失败并报 `Model unavailable`。在未登录状态下，`opencode` provider 不存在，直到你连接 OpenCode Console 账户或设置 `OPENCODE_API_KEY`，之后它的付费模型会恢复。

## 变体（Variants）

变体是同一个模型的命名选项，常用于推理力度或 token 预算。在为一次运行、会话、agent 或命令选择时附加 `#variant`：

```bash
opencode run --model openai/gpt-6.1-sol#high "Review this migration plan"
```

变体名称来自所选模型当前的目录元数据。诸如 `low`、`high`、`max` 之类的名称并非每个模型都有，未知变体会导致模型解析错误。

在模型的 `variants` 数组中定义新变体，或以相同 ID 替换目录中的变体：

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "providers": {
    "openai": {
      "models": {
        "gpt-6.1-sol": {
          "settings": {
            "reasoningEffort": "medium",
          },
          "variants": [
            {
              "id": "fast",
              "settings": {
                "reasoningEffort": "low",
              },
            },
            {
              "id": "deep",
              "settings": {
                "reasoningEffort": "high",
                "reasoningSummary": "auto",
              },
            },
          ],
        },
      },
    },
  },
}
```

每个变体可以包含 `settings`、`headers` 和 `body`。它们的值在 provider 和模型的值之后生效。

要替换模型的推理变体，请在 `capabilities.reasoning` 中描述其推理控制项，采用 [models.dev](https://models.dev) 的 v2 形状。OpenCode 会据此为该模型的包构建变体：

```jsonc title="opencode.jsonc"
{
  "providers": {
    "openai": {
      "models": {
        "gpt-6.1-sol": {
          "capabilities": {
            "reasoning": {
              "supported": true,
              "effort": ["low", "medium", "high"],
            },
          },
        },
      },
    },
  },
}
```

| 字段 | 用途 |
| ----------- | -------------------------------------------------------------------------- |
| `supported` | 模型是否进行推理。`false`，或仅有 `true` 而没有控制项时，不会生成任何变体。 |
| `toggle` | 添加一个关闭推理的 `none` 变体。 |
| `effort` | 要提供的力度等级。`default` 保留 provider 默认值，不添加变体。 |
| `budget` | 可选的思维 token `min` 和 `max`。设置了 `effort` 时被忽略。 |

`variants` 中列出的变体会应用在根据 `capabilities.reasoning` 构建出的变体之上。

## 选项

provider 和模型条目可以用 `settings`、`headers` 和 `body` 定制请求：

```jsonc title="opencode.jsonc"
{
  "providers": {
    "openai": {
      "settings": {
        "baseURL": "https://api.example.com/v1",
      },
      "headers": {
        "X-Team": "platform",
      },
      "models": {
        "gpt-6.1-sol": {
          "settings": {
            "reasoningEffort": "high",
          },
          "body": {
            "store": false,
          },
        },
      },
    },
  },
}
```

| 字段 | 用途 |
| ---------- | ------------------------------------------------------------------ |
| `settings` | provider 包选项，例如 `baseURL` 或 `reasoningEffort`。 |
| `headers` | 额外的 HTTP 请求头。 |
| `body` | provider 特定的请求体字段。 |

OpenCode 先应用 provider 的值，其次是模型的值，最后是所选变体的值。

- 嵌套的 `settings` 和 `body` 对象会被合并。
- 后出现的数组和标量值会替换之前的值。
- 请求头名称的匹配不区分大小写。
- 这些选项是 provider 特定的，可能被其他 provider 包忽略或拒绝。

## 别名

使用 `modelID` 为一个 API 模型提供一个更友好的目录 ID：

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "model": "openai/coding-default",
  "providers": {
    "openai": {
      "models": {
        "coding-default": {
          "modelID": "gpt-6.1-sol",
          "name": "Coding default",
          "capabilities": {
            "tools": true,
            "freeform": ["text", "lark"],
            "input": ["text", "image"],
            "output": ["text"],
          },
          "limit": {
            "context": 200000,
            "output": 32000,
          },
        },
      },
    },
  },
}
```

在这里，`openai/coding-default` 是可供选择的引用，而实际发送给 provider 的是 `gpt-6.1-sol`。对于目录中尚不存在的模型，OpenCode 假定：

- 支持 JSON 工具，输入为文本和图像，输出为文本。除非 `capabilities.freeform` 列出了格式，否则不支持自由格式（freeform）的工具输入。
- 上下文上限 200,000 token，输出上限 32,000 token。
- 输入上限未指定。

OpenCode 识别 `text`、`regex` 和 `lark`。models.dev 中其他格式名称会被忽略，但不会因此丢弃该模型或其工具。如果某个目录模型前面的代理拒绝 freeform 工具，请在该模型上把 `capabilities.freeform` 设为 `[]`。

这些是回退假设，并非检测到的能力。已知时请设置准确的 `capabilities` 和 `limit` 值；显式值会覆盖这些回退。添加 `disabled: true` 可以把某个模型从可用目录中隐藏：

```jsonc title="opencode.jsonc"
{
  "providers": {
    "openai": {
      "models": {
        "legacy-model": {
          "disabled": true,
        },
      },
    },
  },
}
```

## 推理

对于在自定义 assistant 消息字段中流式传输推理内容的 OpenAI 兼容模型，请设置 `compatibility.reasoningField`：

```jsonc title="opencode.jsonc"
{
  "providers": {
    "local": {
      "models": {
        "reasoner": {
          "compatibility": {
            "reasoningField": "reasoning_content",
          },
        },
      },
    },
  },
}
```

OpenCode 识别 `reasoning`、`reasoning_content` 和 `reasoning_text`，也接受其他 provider 特定的字符串。它会从该字段读取流式推理，并在把先前的 assistant 消息发回模型时还原该字段。相关的 `requireReasoning` 字段请参阅[兼容性](#兼容性)。

## 提示词缓存

OpenCode 会在已知需要的位置（例如 Anthropic）自动放置提示词缓存断点。当 Claude 模型通过 LiteLLM 这类 OpenAI 兼容代理提供服务时，OpenCode 无法得知它们需要 Anthropic 风格的 `cache_control` 断点。请在这些 Claude 模型上设置 `compatibility.cacheFormat`：

```jsonc title="opencode.jsonc"
{
  "providers": {
    "litellm": {
      "package": "@opencode/ai/providers/openai-compatible",
      "settings": { "baseURL": "https://litellm.example.com/v1" },
      "models": {
        "claude-sonnet-5-5": {
          "compatibility": { "cacheFormat": "anthropic" },
        },
        "claude-opus-5-5": {
          "compatibility": { "cacheFormat": "anthropic" },
        },
        // 同一代理上的其他模型会自动缓存，无需设置。
        "gpt-6.1-sol": {},
      },
    },
  },
}
```

OpenCode 随后会用 `cache_control: { "type": "ephemeral" }` 标记最后一个工具定义、系统提示词以及最新的消息，这使用端点默认的五分钟缓存时长。对于阿里云 Model Studio 模型，请使用 `"alibaba"`，它们接受相同的标记但会忽略工具定义上的标记。当某个 provider 服务下的每个模型都接受相同格式时，请在 provider 上设置 `compatibility.cacheFormat`。其他字段请参阅[兼容性](#兼容性)。

### 缓存时长

OpenCode 默认不发送缓存时长，因此每个 provider 使用自己的默认值，例如 Anthropic 为五分钟。可以在 provider 或模型上设置 `settings.cache.ttl` 来请求不同的时长。模型上的设置会覆盖 provider 上的设置。

```jsonc title="opencode.jsonc"
{
  "providers": {
    "anthropic": {
      "settings": { "cache": { "ttl": "1h" } },
      "models": {
        "claude-haiku-5-5": { "settings": { "cache": { "ttl": "5m" } } },
      },
    },
  },
}
```

`ttl` 接受一个数字加一个单位：`ms`、`s`、`m`、`h` 或 `d`，例如 `"5m"`、`"1h"` 或 `"24h"`。OpenCode 会按给定值原样发送，因此请使用 provider 接受的值：

| API | 时长放在哪里 |
| --- | --- |
| Anthropic Messages | 每个缓存标记上的 `cache_control.ttl`。Anthropic 接受 `"5m"` 和 `"1h"`。 |
| Bedrock Converse | 每个 `cachePoint` 上的 `ttl`。只支持五分钟缓存的旧 Claude 模型会忽略 `"1h"`。 |
| OpenAI Chat 与 Responses | `"24h"` 会发送到 `prompt_cache_retention`；其他值发送到 `prompt_cache_options.ttl`。 |

无需标记即自动缓存的 provider（例如 Gemini）会忽略它。更长的缓存时长通常写入成本更高：Anthropic 对一小时缓存写入收取输入价格的 2 倍，五分钟的收取 1.25 倍。

[Warming](../warming/index.md) 可以利用该时长，用 `interval: "auto"` 来安排其请求的时机。

## 兼容性

`compatibility` 描述模型所使用的 API 在请求和响应上的特殊行为，例如哪个字段承载推理内容，或端点是否接受 `prompt_cache_key`。每个模型都通过某一个 API 提供服务，一个字段只有在该 API 读取它时才生效，其他字段会被忽略。

```jsonc title="opencode.jsonc"
{
  "providers": {
    "local": {
      "compatibility": { "streamUsage": false },
      "models": {
        "reasoner": {
          "compatibility": { "reasoningField": "reasoning_content", "maxTokensField": "max_tokens" },
        },
      },
    },
  },
}
```

provider 级的 `compatibility` 作用于该 provider 的每个模型。模型自身的 `compatibility` 会逐字段覆盖它：OpenCode 从 [models.dev](https://models.dev) 为该模型的 API 发布的值（`reasoningField`、`maxTokensField` 和 `mediaInput`）出发，然后应用模型的配置。未设置的字段保持 provider 包的内置默认值或检测结果。`supportsThinkingBlockBinding` 和 `supportsEffortUpdates` 是仅模型级的字段。

| 字段 | 作用 | 读取方 | 取值与默认值 |
| --- | --- | --- | --- |
| `reasoningField` | 承载推理内容的 assistant 消息字段。读取流式推理时首先检查该字段，回传先前推理时也使用它。 | OpenAI Chat | 除 `role`、`content`、`refusal`、`tool_calls` 之外的任何字段名。未设置时使用流中观察到的字段，否则为 `reasoning_content`。 |
| `requireReasoning` | 在每条先前的 assistant 消息上都发送推理字段，没有推理时发送空字符串。 | OpenAI Chat | `true` 或 `false`。当设置了 `reasoningField` 或模型是 DeepSeek 时默认为 `true`，否则为 `false`。 |
| `maxTokensField` | 承载输出 token 上限的请求体字段。 | OpenAI Chat | `max_completion_tokens` 或 `max_tokens`。未设置时，对于需要 `max_tokens` 的 provider（如 DeepSeek、Moonshot、Together AI、Z.AI、Cerebras）检测为 `max_tokens`，否则为 `max_completion_tokens`。 |
| `requireFinishReason` | 把没有 `finish_reason` 就结束的流视为未完成的响应错误。`false` 则接受其为已结束。 | OpenAI Chat | `true` 或 `false`。默认为 `true`。 |
| `requireAssistantAfterTool` | 在工具结果与下一条用户消息之间插入一条 assistant 消息，适用于拒绝该顺序的端点。 | OpenAI Chat | `true` 或 `false`。Mistral 系列的模型 ID 默认为 `true`，否则为 `false`。 |
| `supportsPromptCacheKey` | 端点是否接受 `prompt_cache_key` 请求体字段。 | OpenAI Chat、OpenAI Responses、Mistral | `true` 或 `false`。OpenAI Chat 只有在 `true` 时才发送该键，部分 provider 包默认设为 `true`。其他 API 在非 `false` 时都会发送。 |
| `streamUsage` | 通过 `stream_options.include_usage` 在流中请求 token 用量。 | OpenAI Chat | `true` 或 `false`。默认为 `true`。 |
| `cacheFormat` | 端点接受的提示词缓存标记语法。覆盖 provider 的自动断点放置。`alibaba` 会跳过工具定义。 | 所有带提示词缓存标记的 API，包括 OpenAI Chat、Anthropic Messages 和 Bedrock Converse | `anthropic` 或 `alibaba`。未设置时使用 provider 默认值。请参阅[提示词缓存](#提示词缓存)。 |
| `supportsThinkingBlockBinding` | 请求 API 丢弃其先前上下文已变化的思维块，而不是拒绝整个请求。 | Anthropic Messages、Bedrock Converse | `true` 或 `false`。未设置时检测 Claude 5.1 及更高版本。 |
| `supportsEffortUpdates` | 把推理力度的变化作为逐消息更新发送，从而保持提示词缓存。否则该变化作用于整个请求。 | Anthropic Messages、OpenAI Responses | `true` 或 `false`。未设置时检测 Claude Opus 5、Claude 5.1 及更高版本，以及 GPT-6 及更高版本。 |
| `mediaInput` | 决策请求中图像及其他媒体所在的位置。 | System One | `assets`（从状态中引用的图像）、`state`（内联在状态中）或 `root`（顶层的 `images`、`audio`、`videos` 列表）。未设置时使用 provider 默认值。 |

## 本地模型

OpenCode 会在默认本地地址上自动发现 Ollama、LM Studio 和 vLLM 的模型。你也可以手动配置任何 OpenAI 兼容的服务器。

```text
ollama/gemma3:4b
lmstudio/google/gemma-4-26b-a4b
vllm/Qwen/Qwen3-Coder-30B-A3B-Instruct
```

### Ollama

当 Ollama 监听在 `http://127.0.0.1:11434` 时，使用 `ollama` provider ID 选择一个被发现的模型：

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "model": "ollama/gemma3:4b",
}
```

OpenCode 会在后台刷新模型清单，并从 Ollama 读取上下文、视觉和工具使用能力。仅用于嵌入（embedding）的模型会被排除。

对于其他主机或端口，请设置 Ollama 的 OpenAI 兼容 URL。发现仍然使用相同路径前缀下的原生 Ollama API：

```jsonc title="opencode.jsonc"
{
  "providers": {
    "ollama": {
      "settings": {
        "baseURL": "http://127.0.0.1:5678/v1",
        "apiKey": "{env:OLLAMA_API_KEY}",
      },
    },
  },
}
```

- 端点不需要 bearer 认证时，请省略 `apiKey`。
- 使用 `"plugins": ["-opencode.provider.ollama"]` 禁用发现。

### LM Studio

当 LM Studio 服务器在 `http://127.0.0.1:1234` 无认证运行时，使用 `lmstudio` provider ID 选择一个被发现的模型：

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "model": "lmstudio/google/gemma-4-26b-a4b",
}
```

OpenCode 会在后台刷新模型清单，并从 LM Studio 读取上下文、视觉和工具使用能力。嵌入模型会被排除。

对于其他主机或端口，请设置 OpenAI 兼容 URL。模型仍会被自动发现：

```jsonc title="opencode.jsonc"
{
  "providers": {
    "lmstudio": {
      "settings": {
        "baseURL": "http://127.0.0.1:5678/v1",
        "apiKey": "{env:LMSTUDIO_API_KEY}",
      },
    },
  },
}
```

- LM Studio 认证被禁用时，请省略 `apiKey`。
- 使用 `"plugins": ["-opencode.provider.lmstudio"]` 禁用发现。

### vLLM

当 vLLM 监听在 `http://127.0.0.1:8000` 时，使用 `vllm` provider ID 选择一个被发现的模型：

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "model": "vllm/Qwen/Qwen3-Coder-30B-A3B-Instruct",
}
```

OpenCode 会检查 `/health`，在后台刷新 `/v1/models`，把上报的 `max_model_len` 用作上下文上限，并且只包含归属为 `vllm` 的模型卡。

被发现的模型会声明文本输入和输出，但不支持视觉和工具。vLLM 通过 `--enable-auto-tool-choice` 和 `--tool-call-parser` 之类的服务器参数启用工具调用，发现机制不会上报这些参数。

对于其他端点或需要认证的服务器，请设置其 OpenAI 兼容 URL：

```jsonc title="opencode.jsonc"
{
  "providers": {
    "vllm": {
      "settings": {
        "baseURL": "http://127.0.0.1:9000/v1",
        "apiKey": "{env:VLLM_API_KEY}",
      },
    },
  },
}
```

- 认证被禁用时，请省略 `apiKey`。
- 使用 `"plugins": ["-opencode.provider.vllm"]` 禁用发现。
- 支持带路径前缀的代理。例如，`https://example.com/vllm/v1` 会检查 `/vllm/health` 并发现 `/vllm/v1/models`。

### 兼容服务器

对于其他 OpenAI 兼容服务器，请定义它的 provider 包、端点和至少一个模型：

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "model": "local/coder",
  "providers": {
    "local": {
      "name": "Local server",
      "package": "@opencode/ai/providers/openai-compatible",
      "settings": {
        "baseURL": "http://127.0.0.1:1234/v1",
      },
      "models": {
        "coder": {
          "modelID": "model-name-on-server",
          "capabilities": {
            "tools": true,
            "input": ["text"],
            "output": ["text"],
          },
          "limit": {
            "context": 32768,
            "output": 8192,
          },
        },
      },
    },
  },
}
```

请使用服务器真实的模型名称、上限、输入输出类型和工具支持情况。OpenCode 无法检测自定义模型回退值是否准确。如果端点需要密钥，请在 `settings` 中添加 `apiKey`，并使用环境变量替换，例如 `"apiKey": "{env:LOCAL_API_KEY}"`；不要提交密钥。

## 引用

模型选择器使用 `provider/model` 格式，可附加 `#variant`：

```text
openai/gpt-6.1-sol
openai/gpt-6.1-sol#high
openrouter/anthropic/claude-sonnet-5.5#high
```

| 部分 | 规则 |
| ---------- | ---------------------------------------------------------- |
| provider | 在第一个 `/` 处结束；不能包含 `/` 或 `#`。 |
| 模型 | 可以包含更多 `/` 字符；不能包含 `#`。 |
| 变体 | 存在时跟随在 `#` 之后。 |
| 大小写 | provider 和模型 ID 区分大小写。 |

请使用目录 ID 而不是 provider 的显示名称。根级、agent 和命令的 `model` 字段接受上述字符串形式，或展开的对象形式：

```jsonc
{
  "model": {
    "providerID": "openrouter",
    "model": "anthropic/claude-sonnet-5.5",
  },
}
```

展开形式适用于生成式或程序化配置。

## 注意事项

配置模型时请记住以下规则：

```jsonc
{
  "model": "openai/gpt-6.1-sol"
}
```

- 选择器对象使用 `model`；provider 目录条目使用 `modelID` 表示实际发送给 provider 的 ID。
- 尽管根级选择形状接受 variant，但 V2 目录默认值不会保留它。请改为为会话、单次运行、agent 或命令选择 variant。
- 模型选项是 provider 特定的，其他 provider 包可能会忽略或拒绝它们。
- 目录数据、凭据和配置都按位置隔离。某个项目中可用的模型在另一个项目中可能不可用。
- 配置文件通常会自动重新加载。已经在进行中的模型请求会保留它启动时所用的设置。
