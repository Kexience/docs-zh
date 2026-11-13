---
source_url: https://opencode.ai/docs/console/models/
source_hash: sha256:7eb1c281bc39a27650ba39d47ee7af8bc7ad7df236924d1324320bd5c66c87dd
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# 模型

OpenCode Console 提供一份由 OpenCode 团队测试并验证过的模型列表。登录、充值，然后获取 API key，即可在 OpenCode 或其他编程 agent 中使用这些模型。

Console 在 OpenCode 中就像任何一个普通的 provider。它**完全是可选的**，你完全可以改用其他 provider。如果你想使用包含额度的订阅方案，请参阅 [OpenCode Go](../go/index.md)。

## 工作原理

1. 登录 [console](https://opencode.ai/console)，填写计费信息并充值，然后复制你的 API key。
2. 在 TUI 中运行 `/connect`，选择 OpenCode 按量付费 provider，并粘贴你的 API key。

   ```text
   /connect
   ```

3. 运行 `/models` 查看可用模型并进行选择。

   ```text
   /models
   ```

系统按请求计费，你可以随时为账户充值。

## 端点

你也可以通过以下 API 端点直接访问这些模型。免费档位的聊天模型需要 OpenCode；在其他客户端中请使用付费模型或 [Go](../go/index.md)。

每个模型都列出了它的原生 API，但所有文本模型也可以通过其他 API 访问，由 Console 负责转译。完整列表见[基础 URL](../harnesses/index.md#base-urls)。

<div class="docs-table-scroll" role="region" aria-label="Console model endpoints" tabIndex={0}>

| 模型                            | 模型 ID                         | 端点                                                                       | AI SDK 包                   |
| ------------------------------- | ------------------------------- | -------------------------------------------------------------------------- | --------------------------- |
| GPT 6 Astra                     | gpt-6-astra                     | `https://opencode.ai/inference/openai/v1/responses`                        | `@ai-sdk/openai`            |
| GPT 6 Sol                       | gpt-6-sol                       | `https://opencode.ai/inference/openai/v1/responses`                        | `@ai-sdk/openai`            |
| GPT 6.1 Sol                     | gpt-6.1-sol                     | `https://opencode.ai/inference/openai/v1/responses`                        | `@ai-sdk/openai`            |
| GPT 6 Luna                      | gpt-6-luna                      | `https://opencode.ai/inference/openai/v1/responses`                        | `@ai-sdk/openai`            |
| GPT 5.6 Sol                     | gpt-5.6-sol                     | `https://opencode.ai/inference/openai/v1/responses`                        | `@ai-sdk/openai`            |
| GPT 5.6 Terra                   | gpt-5.6-terra                   | `https://opencode.ai/inference/openai/v1/responses`                        | `@ai-sdk/openai`            |
| GPT 5.6 Luna                    | gpt-5.6-luna                    | `https://opencode.ai/inference/openai/v1/responses`                        | `@ai-sdk/openai`            |
| GPT 5.5                         | gpt-5.5                         | `https://opencode.ai/inference/openai/v1/responses`                        | `@ai-sdk/openai`            |
| GPT 5.5 Pro                     | gpt-5.5-pro                     | `https://opencode.ai/inference/openai/v1/responses`                        | `@ai-sdk/openai`            |
| GPT 5.4                         | gpt-5.4                         | `https://opencode.ai/inference/openai/v1/responses`                        | `@ai-sdk/openai`            |
| GPT 5.4 Pro                     | gpt-5.4-pro                     | `https://opencode.ai/inference/openai/v1/responses`                        | `@ai-sdk/openai`            |
| GPT 5.4 Mini                    | gpt-5.4-mini                    | `https://opencode.ai/inference/openai/v1/responses`                        | `@ai-sdk/openai`            |
| GPT 5.4 Nano                    | gpt-5.4-nano                    | `https://opencode.ai/inference/openai/v1/responses`                        | `@ai-sdk/openai`            |
| GPT 5.3 Codex                   | gpt-5.3-codex                   | `https://opencode.ai/inference/openai/v1/responses`                        | `@ai-sdk/openai`            |
| GPT 5.3 Codex Spark             | gpt-5.3-codex-spark             | `https://opencode.ai/inference/openai/v1/responses`                        | `@ai-sdk/openai`            |
| GPT 5.2                         | gpt-5.2                         | `https://opencode.ai/inference/openai/v1/responses`                        | `@ai-sdk/openai`            |
| GPT 5.2 Codex                   | gpt-5.2-codex                   | `https://opencode.ai/inference/openai/v1/responses`                        | `@ai-sdk/openai`            |
| GPT 5.1                         | gpt-5.1                         | `https://opencode.ai/inference/openai/v1/responses`                        | `@ai-sdk/openai`            |
| GPT 5.1 Codex                   | gpt-5.1-codex                   | `https://opencode.ai/inference/openai/v1/responses`                        | `@ai-sdk/openai`            |
| GPT 5.1 Codex Max               | gpt-5.1-codex-max               | `https://opencode.ai/inference/openai/v1/responses`                        | `@ai-sdk/openai`            |
| GPT 5.1 Codex Mini              | gpt-5.1-codex-mini              | `https://opencode.ai/inference/openai/v1/responses`                        | `@ai-sdk/openai`            |
| GPT 5                           | gpt-5                           | `https://opencode.ai/inference/openai/v1/responses`                        | `@ai-sdk/openai`            |
| GPT 5 Codex                     | gpt-5-codex                     | `https://opencode.ai/inference/openai/v1/responses`                        | `@ai-sdk/openai`            |
| GPT 5 Nano                      | gpt-5-nano                      | `https://opencode.ai/inference/openai/v1/responses`                        | `@ai-sdk/openai`            |
| Claude Fable 5.2                | claude-fable-5-2                | `https://opencode.ai/inference/anthropic/v1/messages`                      | `@ai-sdk/anthropic`         |
| Claude Fable 5.1                | claude-fable-5-1                | `https://opencode.ai/inference/anthropic/v1/messages`                      | `@ai-sdk/anthropic`         |
| Claude Fable 5                  | claude-fable-5                  | `https://opencode.ai/inference/anthropic/v1/messages`                      | `@ai-sdk/anthropic`         |
| Claude Opus 5.5                 | claude-opus-5-5                 | `https://opencode.ai/inference/anthropic/v1/messages`                      | `@ai-sdk/anthropic`         |
| Claude Opus 5                   | claude-opus-5                   | `https://opencode.ai/inference/anthropic/v1/messages`                      | `@ai-sdk/anthropic`         |
| Claude Opus 4.8                 | claude-opus-4-8                 | `https://opencode.ai/inference/anthropic/v1/messages`                      | `@ai-sdk/anthropic`         |
| Claude Opus 4.7                 | claude-opus-4-7                 | `https://opencode.ai/inference/anthropic/v1/messages`                      | `@ai-sdk/anthropic`         |
| Claude Opus 4.6                 | claude-opus-4-6                 | `https://opencode.ai/inference/anthropic/v1/messages`                      | `@ai-sdk/anthropic`         |
| Claude Opus 4.5                 | claude-opus-4-5                 | `https://opencode.ai/inference/anthropic/v1/messages`                      | `@ai-sdk/anthropic`         |
| Claude Sonnet 5.5               | claude-sonnet-5-5               | `https://opencode.ai/inference/anthropic/v1/messages`                      | `@ai-sdk/anthropic`         |
| Claude Sonnet 5                 | claude-sonnet-5                 | `https://opencode.ai/inference/anthropic/v1/messages`                      | `@ai-sdk/anthropic`         |
| Claude Sonnet 4.6               | claude-sonnet-4-6               | `https://opencode.ai/inference/anthropic/v1/messages`                      | `@ai-sdk/anthropic`         |
| Claude Sonnet 4.5               | claude-sonnet-4-5               | `https://opencode.ai/inference/anthropic/v1/messages`                      | `@ai-sdk/anthropic`         |
| Claude Haiku 5.5                | claude-haiku-5-5                | `https://opencode.ai/inference/anthropic/v1/messages`                      | `@ai-sdk/anthropic`         |
| Claude Haiku 4.5                | claude-haiku-4-5                | `https://opencode.ai/inference/anthropic/v1/messages`                      | `@ai-sdk/anthropic`         |
| Gemini 4 Carbon                 | gemini-4-carbon                 | `https://opencode.ai/inference/google/v1beta/models/gemini-4-carbon`       | `@ai-sdk/google`            |
| Gemini 4 Argon                  | gemini-4-argon                  | `https://opencode.ai/inference/google/v1beta/models/gemini-4-argon`        | `@ai-sdk/google`            |
| Gemini 4 Hydrogen               | gemini-4-hydrogen               | `https://opencode.ai/inference/google/v1beta/models/gemini-4-hydrogen`     | `@ai-sdk/google`            |
| Gemini 3.8 Flash                | gemini-3.8-flash                | `https://opencode.ai/inference/google/v1beta/models/gemini-3.8-flash`      | `@ai-sdk/google`            |
| Gemini 3.7 Flash                | gemini-3.7-flash                | `https://opencode.ai/inference/google/v1beta/models/gemini-3.7-flash`      | `@ai-sdk/google`            |
| Gemini 3.6 Flash                | gemini-3.6-flash                | `https://opencode.ai/inference/google/v1beta/models/gemini-3.6-flash`      | `@ai-sdk/google`            |
| Gemini 3.5 Flash                | gemini-3.5-flash                | `https://opencode.ai/inference/google/v1beta/models/gemini-3.5-flash`      | `@ai-sdk/google`            |
| Gemini 3.5 Flash Lite           | gemini-3.5-flash-lite           | `https://opencode.ai/inference/google/v1beta/models/gemini-3.5-flash-lite` | `@ai-sdk/google`            |
| Gemini 3.1 Pro                  | gemini-3.1-pro                  | `https://opencode.ai/inference/google/v1beta/models/gemini-3.1-pro`        | `@ai-sdk/google`            |
| Gemini 3 Flash                  | gemini-3-flash                  | `https://opencode.ai/inference/google/v1beta/models/gemini-3-flash`        | `@ai-sdk/google`            |
| Grok 4.7                        | grok-4.7                        | `https://opencode.ai/inference/openai/v1/responses`                        | `@ai-sdk/openai`            |
| Grok 4.6                        | grok-4.6                        | `https://opencode.ai/inference/openai/v1/responses`                        | `@ai-sdk/openai`            |
| Grok 4.5                        | grok-4.5                        | `https://opencode.ai/inference/openai/v1/responses`                        | `@ai-sdk/openai`            |
| Grok Build 0.1                  | grok-build-0.1                  | `https://opencode.ai/inference/openai/v1/responses`                        | `@ai-sdk/openai`            |
| Muse Ember 1.0                  | muse-ember-1.0                  | `https://opencode.ai/inference/openai/v1/responses`                        | `@ai-sdk/openai`            |
| Muse Wonder 1.0                 | muse-wonder-1.0                 | `https://opencode.ai/inference/openai/v1/responses`                        | `@ai-sdk/openai`            |
| Muse Spark 1.3                  | muse-spark-1.3                  | `https://opencode.ai/inference/openai/v1/responses`                        | `@ai-sdk/openai`            |
| Muse Spark 1.2                  | muse-spark-1.2                  | `https://opencode.ai/inference/openai/v1/responses`                        | `@ai-sdk/openai`            |
| Qwen3.8 Max                     | qwen3.8-max                     | `https://opencode.ai/inference/openai/v1/chat/completions`                 | `@ai-sdk/openai-compatible` |
| Qwen3.8 Flash                   | qwen3.8-flash                   | `https://opencode.ai/inference/anthropic/v1/messages`                      | `@ai-sdk/anthropic`         |
| Qwen3.6 Plus                    | qwen3.6-plus                    | `https://opencode.ai/inference/anthropic/v1/messages`                      | `@ai-sdk/anthropic`         |
| Qwen3.5 Plus                    | qwen3.5-plus                    | `https://opencode.ai/inference/anthropic/v1/messages`                      | `@ai-sdk/anthropic`         |
| DeepSeek V4.1 Flash             | deepseek-v4.1-flash             | `https://opencode.ai/inference/openai/v1/chat/completions`                 | `@ai-sdk/openai-compatible` |
| DeepSeek V4 Pro                 | deepseek-v4-pro                 | `https://opencode.ai/inference/openai/v1/chat/completions`                 | `@ai-sdk/openai-compatible` |
| MiniMax M3                      | minimax-m3                      | `https://opencode.ai/inference/openai/v1/chat/completions`                 | `@ai-sdk/openai-compatible` |
| MiniMax M2.7                    | minimax-m2.7                    | `https://opencode.ai/inference/openai/v1/chat/completions`                 | `@ai-sdk/openai-compatible` |
| MiniMax M2.5                    | minimax-m2.5                    | `https://opencode.ai/inference/openai/v1/chat/completions`                 | `@ai-sdk/openai-compatible` |
| GLM 5.3 Flash                   | glm-5.3-flash                   | `https://opencode.ai/inference/openai/v1/chat/completions`                 | `@ai-sdk/openai-compatible` |
| GLM 5.3                         | glm-5.3                         | `https://opencode.ai/inference/openai/v1/chat/completions`                 | `@ai-sdk/openai-compatible` |
| GLM 5.2                         | glm-5.2                         | `https://opencode.ai/inference/openai/v1/chat/completions`                 | `@ai-sdk/openai-compatible` |
| GLM 5.1                         | glm-5.1                         | `https://opencode.ai/inference/openai/v1/chat/completions`                 | `@ai-sdk/openai-compatible` |
| GLM 5                           | glm-5                           | `https://opencode.ai/inference/openai/v1/chat/completions`                 | `@ai-sdk/openai-compatible` |
| Kimi K2.5                       | kimi-k2.5                       | `https://opencode.ai/inference/openai/v1/chat/completions`                 | `@ai-sdk/openai-compatible` |
| Kimi K2.6                       | kimi-k2.6                       | `https://opencode.ai/inference/openai/v1/chat/completions`                 | `@ai-sdk/openai-compatible` |
| Kimi K2.7 Code                  | kimi-k2.7-code                  | `https://opencode.ai/inference/openai/v1/chat/completions`                 | `@ai-sdk/openai-compatible` |
| Kimi K3                         | kimi-k3                         | `https://opencode.ai/inference/openai/v1/chat/completions`                 | `@ai-sdk/openai-compatible` |
| Mistral Large 4                 | mistral-large-4                 | `https://opencode.ai/inference/openai/v1/chat/completions`                 | `@ai-sdk/openai-compatible` |
| GPT 6 Luna Decision             | gpt-6-luna-decision             | `https://opencode.ai/inference/systemone/v1/systemone`                     | -                           |
| Gemini Decision 1               | gemini-decision-1               | `https://opencode.ai/inference/systemone/v1/systemone`                     | -                           |
| Jev 1.13                        | jev-1.13                        | `https://opencode.ai/inference/systemone/v1/systemone`                     | -                           |
| Jev 1.13 Free                   | jev-1.13-free                   | `https://opencode.ai/inference/systemone/v1/systemone`                     | -                           |
| Big Pickle                      | big-pickle                      | `https://opencode.ai/inference/openai/v1/chat/completions`                 | `@ai-sdk/openai-compatible` |
| Iceman Free                     | iceman-free                     | `https://opencode.ai/inference/openai/v1/chat/completions`                 | `@ai-sdk/openai-compatible` |
| Inkling 2 Small Free            | inkling-2-small-free            | `https://opencode.ai/inference/openai/v1/chat/completions`                 | `@ai-sdk/openai-compatible` |
| GLM-5.3-Flash Free              | glm-5.3-flash-free              | `https://opencode.ai/inference/openai/v1/chat/completions`                 | `@ai-sdk/openai-compatible` |
| DeepSeek V4.1 Flash Free        | deepseek-v4.1-flash-free        | `https://opencode.ai/inference/openai/v1/chat/completions`                 | `@ai-sdk/openai-compatible` |
| MiniMax M3.1 Flash Free         | minimax-m3.1-flash-free         | `https://opencode.ai/inference/openai/v1/chat/completions`                 | `@ai-sdk/openai-compatible` |
| Beam Free                       | beam-free                       | `https://opencode.ai/inference/openai/v1/chat/completions`                 | `@ai-sdk/openai-compatible` |
| Flint 40B Free                  | flint-40b-free                  | `https://opencode.ai/inference/openai/v1/chat/completions`                 | `@ai-sdk/openai-compatible` |
| LongCat 2.5 Free                | longcat-2.5-free                | `https://opencode.ai/inference/openai/v1/chat/completions`                 | `@ai-sdk/openai-compatible` |
| MiMo-V2.6-Flash Free            | mimo-v2.6-flash-free            | `https://opencode.ai/inference/openai/v1/chat/completions`                 | `@ai-sdk/openai-compatible` |
| Nemotron 3 Ultra Free           | nemotron-3-ultra-free           | `https://opencode.ai/inference/openai/v1/chat/completions`                 | `@ai-sdk/openai-compatible` |
| Nemotron 3.5 Lightning Free     | nemotron-3.5-lightning-free     | `https://opencode.ai/inference/openai/v1/chat/completions`                 | `@ai-sdk/openai-compatible` |
| Nemotron 3.5 Super VL Free      | nemotron-3.5-super-vl-free      | `https://opencode.ai/inference/openai/v1/chat/completions`                 | `@ai-sdk/openai-compatible` |

</div>

这些 AI SDK 包用于直接调用端点的应用程序。要在 OpenCode 中选择一个[模型](../../models/index.md)，请使用 `opencode/<model-id>` 格式：

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "model": "opencode/gpt-6.1-sol",
}
```

### 模型列表

从 models 端点获取完整的可用模型列表及其元数据：

```bash
curl https://opencode.ai/inference/v1/models
```

### Jev

Jev 是 TypeSafe AI 推出的 System One 模型，用于快速、结构化的决策。它不生成文本，而是根据带类型的问题对一个 `state` 进行评估，并返回你的代码可以直接使用的取值和概率。它支持是非题（`noul`）、选择题（`choice`）和基于评分标准的打分题（`score`）。

将你的 OpenCode Console API key 用于 `https://opencode.ai/inference/systemone/v1/systemone` 端点。以下示例检查一条支持请求是否紧急：

```bash
curl https://opencode.ai/inference/systemone/v1/systemone \
  -H "Authorization: Bearer $OPENCODE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "jev-1.13",
    "state": "My payments have failed for three days and I am losing sales. Please help now.",
    "questions": {
      "is_urgent": {
        "type": "noul",
        "instructions": "Does this request require urgent attention?"
      }
    }
  }'
```

你可以在一次请求中提出多个问题。Jev 会并行评估这些问题，并在对应的问题 ID 下返回每个答案：

```bash
curl https://opencode.ai/inference/systemone/v1/systemone \
  -H "Authorization: Bearer $OPENCODE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "jev-1.13",
    "state": "My order arrived late and the item is damaged. I want a refund.",
    "questions": {
      "department": {
        "type": "choice",
        "instructions": "Which team should handle this request?",
        "criteria": {
          "returns": "Refunds, exchanges, or damaged items",
          "shipping": "Delivery delays or lost packages",
          "billing": "Charges, invoices, or payment problems"
        }
      },
      "frustration": {
        "type": "score",
        "instructions": "How frustrated is the customer?",
        "criteria": ["Calm", "Frustrated", "Very angry"]
      }
    }
  }'
```

使用 `jev-1.13-free` 替代 `jev-1.13` 即可使用限时免费模型。关于问题类型和响应字段的详细信息，请参阅 [TypeSafe AI 文档](https://docs.typesafe.ai/)。

### GPT 6 Luna Decision 与 Gemini Decision 1

`gpt-6-luna-decision` 和 `gemini-decision-1` 在同一端点接受与 Jev 相同的 System One 请求。可以在 `state` 中以聊天式部件（`image_url`、`input_audio`、`video_url`、`file`）传入图片、音频、视频和 PDF。GPT 6 Luna Decision 接受文本和图片；Gemini Decision 1 还接受音频、视频和 PDF。

```bash
curl https://opencode.ai/inference/systemone/v1/systemone \
  -H "Authorization: Bearer $OPENCODE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-decision-1",
    "state": "I was charged twice for my order.",
    "questions": {
      "refund": {
        "type": "noul",
        "instructions": "Is this a refund request?"
      }
    }
  }'
```

## 定价

Console 采用按量付费定价。以下是**每 100 万 token**的价格。

<div class="docs-table-scroll" role="region" aria-label="Console model pricing" tabIndex={0}>

| 模型                               | 输入            | 输出            | 缓存读取        | 缓存写入     |
| --------------------------------- | --------------- | --------------- | --------------- | ------------ |
| Big Pickle                        | 免费            | 免费            | 免费            | -            |
| Iceman Free                       | 免费            | 免费            | 免费            | -            |
| Inkling 2 Small Free              | 免费            | 免费            | 免费            | -            |
| GLM-5.3-Flash Free                | 免费            | 免费            | 免费            | -            |
| DeepSeek V4.1 Flash Free          | 免费            | 免费            | 免费            | -            |
| MiniMax M3.1 Flash Free           | 免费            | 免费            | 免费            | -            |
| Beam Free                         | 免费            | 免费            | 免费            | -            |
| Flint 40B Free                    | 免费            | 免费            | 免费            | -            |
| LongCat 2.5 Free                  | 免费            | 免费            | 免费            | -            |
| MiMo-V2.6-Flash Free              | 免费            | 免费            | 免费            | -            |
| Nemotron 3 Ultra Free             | 免费            | 免费            | 免费            | -            |
| Nemotron 3.5 Lightning Free       | 免费            | 免费            | 免费            | -            |
| Nemotron 3.5 Super VL Free        | 免费            | 免费            | 免费            | -            |
| Jev 1.13 Free                     | 免费            | 免费            | -               | -            |
| Jev 1.13                          | $0.042          | 免费            | -               | -            |
| Gemini Decision 1                 | $0.10           | 免费            | -               | -            |
| GPT 6 Luna Decision (≤ 272K tokens) | $0.10           | 免费            | $0.01           | $0.125       |
| GPT 6 Luna Decision (> 272K tokens) | $0.20           | 免费            | $0.02           | $0.25        |
| MiniMax M3                        | $0.30           | $1.20           | $0.06           | -            |
| MiniMax M2.7                      | $0.30           | $1.20           | $0.06           | -            |
| MiniMax M2.5                      | $0.30           | $1.20           | $0.06           | -            |
| GLM 5.3 Flash                     | $0.15           | $0.50           | $0.03           | -            |
| GLM 5.3                           | $1.40           | $4.40           | $0.26           | -            |
| GLM 5.2                           | $1.40           | $4.40           | $0.26           | -            |
| GLM 5.1                           | $1.40           | $4.40           | $0.26           | -            |
| GLM 5                             | $1.00           | $3.20           | $0.20           | -            |
| Kimi K2.7 Code                    | $0.95           | $4.00           | $0.19           | -            |
| Kimi K3                           | $3.00           | $15.00          | $0.30           | $3.00        |
| Kimi K2.6                         | $0.95           | $4.00           | $0.16           | -            |
| Kimi K2.5                         | $0.60           | $3.00           | $0.10           | -            |
| Mistral Large 4（5 折）           | ~~$1.36~~ $0.68 | ~~$4.18~~ $2.09 | ~~$0.14~~ $0.07 | -            |
| Qwen3.8 Max                       | $2.00           | $6.00           | $0.25           | $2.50        |
| Qwen3.8 Flash                     | $0.15           | $0.47           | $0.016          | $0.20        |
| Qwen3.6 Plus                      | $0.50           | $3.00           | $0.05           | $0.625       |
| Qwen3.5 Plus                      | $0.20           | $1.20           | $0.02           | $0.25        |
| DeepSeek V4.1 Flash               | $0.30           | $1.20           | $0.006          | -            |
| DeepSeek V4 Pro                   | $1.74           | $3.48           | $0.145          | -            |
| Claude Fable 5.2                  | $8.00           | $40.00          | $0.20           | $10.00       |
| Claude Fable 5.1                  | $10.00          | $50.00          | $0.25           | $12.50       |
| Claude Fable 5                    | $10.00          | $50.00          | $1.00           | $12.50       |
| Claude Opus 5.5                   | $4.00           | $20.00          | $0.20           | $5.00        |
| Claude Opus 5                     | $5.00           | $25.00          | $0.50           | $6.25        |
| Claude Opus 4.8                   | $5.00           | $25.00          | $0.50           | $6.25        |
| Claude Opus 4.7                   | $5.00           | $25.00          | $0.50           | $6.25        |
| Claude Opus 4.6                   | $5.00           | $25.00          | $0.50           | $6.25        |
| Claude Opus 4.5                   | $5.00           | $25.00          | $0.50           | $6.25        |
| Claude Sonnet 5.5                 | $2.00           | $10.00          | $0.10           | $2.50        |
| Claude Sonnet 5                   | $2.00           | $10.00          | $0.20           | $2.50        |
| Claude Sonnet 4.6                 | $3.00           | $15.00          | $0.30           | $3.75        |
| Claude Sonnet 4.5 (≤ 200K tokens) | $3.00           | $15.00          | $0.30           | $3.75        |
| Claude Sonnet 4.5 (> 200K tokens) | $6.00           | $22.50          | $0.60           | $7.50        |
| Claude Haiku 5.5 (≤ 100K tokens)  | $0.10           | $0.50           | $0.01           | $0.125       |
| Claude Haiku 5.5 (> 100K tokens)  | $0.50           | $2.50           | $0.05           | $0.625       |
| Claude Haiku 4.5                  | $1.00           | $5.00           | $0.10           | $1.25        |
| Gemini 4 Carbon（5 折）           | ~~$4.00~~ $2.00 | ~~$20.00~~ $10.00 | ~~$0.20~~ $0.10 | -          |
| Gemini 4 Argon（5 折）            | ~~$4.00~~ $2.00 | ~~$20.00~~ $10.00 | ~~$0.20~~ $0.10 | -          |
| Gemini 4 Hydrogen                 | $1.50           | $7.50           | $0.075          | -            |
| Gemini 3.8 Flash（5 折）          | ~~$1.50~~ $0.75 | ~~$7.50~~ $3.75 | ~~$0.15~~ $0.075 | -           |
| Gemini 3.7 Flash（5 折）          | ~~$1.50~~ $0.75 | ~~$7.50~~ $3.75 | ~~$0.15~~ $0.075 | -           |
| Gemini 3.6 Flash（5 折）          | ~~$1.50~~ $0.75 | ~~$7.50~~ $3.75 | ~~$0.15~~ $0.075 | -           |
| Gemini 3.5 Flash                  | $1.50           | $9.00           | $0.15           | -            |
| Gemini 3.5 Flash Lite             | $0.30           | $2.50           | $0.03           | -            |
| Gemini 3.1 Pro (≤ 200K tokens)    | $2.00           | $12.00          | $0.20           | -            |
| Gemini 3.1 Pro (> 200K tokens)    | $4.00           | $18.00          | $0.40           | -            |
| Gemini 3 Flash                    | $0.50           | $3.00           | $0.05           | -            |
| Grok 4.7 (≤ 200K tokens)          | $2.00           | $6.00           | $0.50           | -            |
| Grok 4.7 (> 200K tokens)          | $4.00           | $12.00          | $1.00           | -            |
| Grok 4.6 (≤ 200K tokens)          | $2.00           | $6.00           | $0.50           | -            |
| Grok 4.6 (> 200K tokens)          | $4.00           | $12.00          | $1.00           | -            |
| Grok 4.5 (≤ 200K tokens)          | $2.00           | $6.00           | $0.30           | -            |
| Grok 4.5 (> 200K tokens)          | $4.00           | $12.00          | $0.60           | -            |
| Grok Build 0.1                    | $1.00           | $2.00           | $0.20           | -            |
| Muse Ember 1.0 (≤ 200K tokens)    | $0.10           | $0.50           | $0.004          | -            |
| Muse Ember 1.0 (> 200K tokens)    | $0.30           | $1.50           | $0.012          | -            |
| Muse Wonder 1.0                   | $4.00           | $20.00          | $0.20           | -            |
| Muse Spark 1.3                    | $1.25           | $4.25           | $0.15           | -            |
| Muse Spark 1.2                    | $1.25           | $4.25           | $0.15           | -            |
| GPT 6 Astra (≤ 272K tokens)       | $10.00          | $50.00          | $1.00           | $12.50       |
| GPT 6 Astra (> 272K tokens)       | $20.00          | $75.00          | $2.00           | $25.00       |
| GPT 6 Sol (≤ 272K tokens)         | $2.00           | $10.00          | $0.20           | $2.50        |
| GPT 6 Sol (> 272K tokens)         | $4.00           | $15.00          | $0.40           | $5.00        |
| GPT 6.1 Sol (≤ 272K tokens)       | $2.00           | $10.00          | $0.10           | $2.50        |
| GPT 6.1 Sol (> 272K tokens)       | $4.00           | $15.00          | $0.20           | $5.00        |
| GPT 6 Luna (≤ 272K tokens)        | $0.10           | $0.50           | $0.01           | $0.125       |
| GPT 6 Luna (> 272K tokens)        | $0.20           | $0.75           | $0.02           | $0.25        |
| GPT 5.6 Sol (≤ 272K tokens)       | $4.00           | $20.00          | $0.40           | $5.00        |
| GPT 5.6 Sol (> 272K tokens)       | $8.00           | $30.00          | $0.80           | $10.00       |
| GPT 5.6 Terra (≤ 272K tokens)     | $2.00           | $12.00          | $0.20           | $2.50        |
| GPT 5.6 Terra (> 272K tokens)     | $4.00           | $18.00          | $0.40           | $5.00        |
| GPT 5.6 Luna (≤ 272K tokens)      | $0.20           | $1.20           | $0.02           | $0.25        |
| GPT 5.6 Luna (> 272K tokens)      | $0.40           | $1.80           | $0.04           | $0.50        |
| GPT 5.5 (≤ 272K tokens)           | $5.00           | $30.00          | $0.50           | -            |
| GPT 5.5 (> 272K tokens)           | $10.00          | $45.00          | $1.00           | -            |
| GPT 5.5 Pro                       | $30.00          | $180.00         | $30.00          | -            |
| GPT 5.4 (≤ 272K tokens)           | $2.50           | $15.00          | $0.25           | -            |
| GPT 5.4 (> 272K tokens)           | $5.00           | $22.50          | $0.50           | -            |
| GPT 5.4 Pro                       | $30.00          | $180.00         | $30.00          | -            |
| GPT 5.4 Mini                      | $0.75           | $4.50           | $0.075          | -            |
| GPT 5.4 Nano                      | $0.20           | $1.25           | $0.02           | -            |
| GPT 5.3 Codex Spark               | $1.75           | $14.00          | $0.175          | -            |
| GPT 5.3 Codex                     | $1.75           | $14.00          | $0.175          | -            |
| GPT 5.2                           | $1.75           | $14.00          | $0.175          | -            |
| GPT 5.2 Codex                     | $1.75           | $14.00          | $0.175          | -            |
| GPT 5.1                           | $1.07           | $8.50           | $0.107          | -            |
| GPT 5.1 Codex                     | $1.07           | $8.50           | $0.107          | -            |
| GPT 5.1 Codex Max                 | $1.25           | $10.00          | $0.125          | -            |
| GPT 5.1 Codex Mini                | $0.25           | $2.00           | $0.025          | -            |
| GPT 5                             | $1.07           | $8.50           | $0.107          | -            |
| GPT 5 Codex                       | $1.07           | $8.50           | $0.107          | -            |
| GPT 5 Nano                        | $0.05           | $0.40           | $0.005          | -            |

</div>

**Gemini 4 Carbon 和 Gemini 4 Argon：** 5 折优惠有效期至 2026 年 11 月 30 日。

**Gemini 3.8 Flash、Gemini 3.7 Flash 和 Gemini 3.6 Flash：** 5 折优惠有效期至 2026 年 12 月 31 日。

你可能会在自己的用量历史中看到[低成本模型](../../models/index.md)，例如 Haiku、Nano 或 Flash。OpenCode 使用这些模型来生成会话标题。

<Callout>
  每次充值都会加收 4.6% + $0.31 的处理费，用于覆盖支付成本；除此之外我们不再收取任何费用。
</Callout>

### 免费模型

- GLM-5.3-Flash Free 在 OpenCode 上限时免费。其 provider 遵循零留存政策，不会将你的数据用于模型训练。
- DeepSeek V4.1 Flash Free 在 OpenCode 上限时免费。其 provider 遵循零留存政策，不会将你的数据用于模型训练。
- MiniMax M3.1 Flash Free 在 OpenCode 上限时免费。其 provider 遵循零留存政策，不会将你的数据用于模型训练。
- MiMo-V2.6-Flash Free 在 OpenCode 上限时提供。团队正利用这段时间收集反馈并改进模型。
- Nemotron 3 Ultra Free 在 OpenCode 上限时提供。团队正利用这段时间收集反馈并改进模型。
- Nemotron 3.5 Lightning Free 在 OpenCode 上限时提供。团队正利用这段时间收集反馈并改进模型。
- Nemotron 3.5 Super VL Free 在 OpenCode 上限时提供。团队正利用这段时间收集反馈并改进模型。
- Big Pickle 是一款隐身（stealth）模型，在 OpenCode 上限时免费。团队正利用这段时间收集反馈并改进模型。
- Iceman Free 是一款隐身（stealth）模型，在 OpenCode 上限时免费。团队正利用这段时间收集反馈并改进模型。
- Inkling 2 Small Free 在 OpenCode 上限时免费。其 provider 会留存你的数据，并可能将其用于模型训练；请参阅[隐私](#隐私)。该模型在欧洲经济区（欧盟、冰岛、列支敦士登、挪威）以及古巴、伊朗、朝鲜、俄罗斯、乌克兰和委内瑞拉不可用。
- Beam Free 在 OpenCode 上限时免费。其 provider 不会将你的数据用于模型训练，但出于安全考虑会将其保留 30 天。该模型在安哥拉、白俄罗斯、柬埔寨、中国（含香港和澳门）、古巴、刚果民主共和国、赤道几内亚、伊朗、伊拉克、老挝、利比亚、尼日利亚、朝鲜、俄罗斯、叙利亚、土库曼斯坦、乌兹别克斯坦、委内瑞拉，以及乌克兰的克里米亚、顿涅茨克和卢甘斯克地区不可用。
- Flint 40B Free 在 OpenCode 上限时免费。团队正利用这段时间收集反馈并改进模型。
- LongCat 2.5 Free 在 OpenCode 上限时免费，每天限 100 次请求。其 provider 遵循零留存政策，不会将你的数据用于模型训练。该模型托管在中国。
- Jev 1.13 Free 在 OpenCode 上限时提供。

要在 OpenCode 中隐藏免费模型，请设置 `OPENCODE_DISABLE_FREE_MODELS=1`。参见[免费模型](../../models/index.md#free-models)。

如有任何疑问，请[联系我们](mailto:help@anoma.ly)。

### 自动充值与预算

[自动充值](../billing/index.md#auto-recharge)会在余额不足时自动购买额度，而[预算](../budgets/index.md)则为工作区和每个成员设定月度支出上限。

### 已弃用的模型

| 模型               | 弃用日期          |
| ------------------ | ----------------- |
| Crouton Alpha Free | 2026 年 11 月 9 日 |
| Pulse Alpha Free   | 2026 年 11 月 6 日 |
| DeepSeek V4 Flash  | 2026 年 10 月 26 日 |
| GPT 5.2 Codex      | 2026 年 7 月 23 日 |
| GPT 5.1 Codex      | 2026 年 7 月 23 日 |
| GPT 5.1 Codex Max  | 2026 年 7 月 23 日 |
| GPT 5.1 Codex Mini | 2026 年 7 月 23 日 |
| GPT 5 Codex        | 2026 年 7 月 23 日 |
| Claude Opus 4.1    | 2026 年 8 月 5 日 |
| Claude Sonnet 4    | 2026 年 6 月 15 日 |
| Claude Haiku 3.5   | 2026 年 2 月 16 日 |
| Gemini 3 Pro       | 2026 年 3 月 9 日 |
| MiniMax M2.5       | 2026 年 8 月 5 日 |
| MiniMax M2.1       | 2026 年 3 月 15 日 |
| GLM 5              | 2026 年 5 月 14 日 |
| GLM 4.7            | 2026 年 3 月 15 日 |
| GLM 4.6            | 2026 年 3 月 15 日 |
| Kimi K2.5          | 2026 年 8 月 5 日 |
| Kimi K2 Thinking   | 2026 年 3 月 6 日 |
| Kimi K2            | 2026 年 3 月 6 日 |
| Qwen3 Coder 480B   | 2026 年 2 月 6 日 |

## 隐私

我们所有的模型都托管在美国和欧盟。我们的 provider 遵循零留存政策，不会将你的数据用于模型训练，但以下例外情况除外：

- Big Pickle：免费期内，收集的数据可能用于改进模型。
- Iceman Free：免费期内，收集的数据会被留存并用于改进模型。
- Inkling 2 Small Free：免费期内，收集的数据会被留存，可能用于监控模型在真实场景中的表现以及模型训练。请参阅 Thinking Machines 的[服务条款](https://thinkingmachines.ai/legal/tml-free-research-api-tier-terms-of-service.pdf)和[隐私声明](https://thinkingmachines.ai/legal/tml-free-research-api-tier-privacy-notice.pdf)。
- Flint 40B Free：免费期内，收集的数据可能用于改进模型。数据会保留 30 天。
- MiMo-V2.6-Flash Free：免费期内，收集的数据可能用于改进模型。
- Nemotron 3 Ultra Free（NVIDIA 免费端点）：仅供试用——请勿提交个人或机密数据。出于安全目的以及改进 NVIDIA 产品和服务的目的，你的使用情况会被记录。用于改进目的的会话记录数据不会关联到你的身份或任何持久标识符。关于我们数据处理实践的更多信息，请参阅我们的[隐私政策](https://assets.ngc.nvidia.com/products/api-catalog/legal/NVIDIA%20API%20Trial%20Terms%20of%20Service.pdf)。与该端点交互即表示你同意我们收集、记录和使用此类信息，并同意[NVIDIA API 试用服务条款](https://assets.ngc.nvidia.com/products/api-catalog/legal/NVIDIA%20API%20Trial%20Terms%20of%20Service.pdf)。
- Nemotron 3.5 Lightning Free（NVIDIA 免费端点）：仅供试用——请勿提交个人或机密数据。出于安全目的以及改进 NVIDIA 产品和服务的目的，你的使用情况会被记录。用于改进目的的会话记录数据不会关联到你的身份或任何持久标识符。关于我们数据处理实践的更多信息，请参阅我们的[隐私政策](https://assets.ngc.nvidia.com/products/api-catalog/legal/NVIDIA%20API%20Trial%20Terms%20of%20Service.pdf)。与该端点交互即表示你同意我们收集、记录和使用此类信息，并同意[NVIDIA API 试用服务条款](https://assets.ngc.nvidia.com/products/api-catalog/legal/NVIDIA%20API%20Trial%20Terms%20of%20Service.pdf)。
- Nemotron 3.5 Super VL Free（NVIDIA 免费端点）：仅供试用——请勿提交个人或机密数据。出于安全目的以及改进 NVIDIA 产品和服务的目的，你的使用情况会被记录。用于改进目的的会话记录数据不会关联到你的身份或任何持久标识符。关于我们数据处理实践的更多信息，请参阅我们的[隐私政策](https://assets.ngc.nvidia.com/products/api-catalog/legal/NVIDIA%20API%20Trial%20Terms%20of%20Service.pdf)。与该端点交互即表示你同意我们收集、记录和使用此类信息，并同意[NVIDIA API 试用服务条款](https://assets.ngc.nvidia.com/products/api-catalog/legal/NVIDIA%20API%20Trial%20Terms%20of%20Service.pdf)。
- OpenAI API：请求会按照 [OpenAI 数据政策](https://platform.openai.com/docs/guides/your-data)保留 30 天。
- Anthropic API：请求会按照 [Anthropic 数据政策](https://docs.anthropic.com/en/docs/claude-code/data-usage)保留 30 天。
- Mistral API：提示词和其他输入不会被用于训练。数据按照 [Mistral 数据保留政策](https://docs.mistral.ai/admin/monitor-comply/zero-data-retention)进行保留。
- Beam Free：提示词和其他输入不会被用于训练。出于安全考虑，数据会保留 30 天。
- LongCat 2.5 Free：托管在中国。提示词和其他输入不会被用于训练，也不会被留存。

关于订阅制模型，请参阅 [Go 隐私说明](../go/index.md#privacy)。

## 面向团队

你可以通过[工作区](../workspaces/index.md)与团队共享 Console 模型。所有者和管理员可以[邀请成员](../members/index.md)、在 **Models** 标签页中选择启用的模型、设置[预算](../budgets/index.md)，并接入[他们自己的 provider](../providers/index.md)。

## 背景

市面上的模型很多，但只有少数能胜任编程 agent 的工作。provider 之间的配置、性能和质量也各不相同，因此同一个模型经过 OpenRouter 之类的网关访问时，表现可能有所不同。

<Callout type="tip">我们测试了一组精选的、与 OpenCode 配合良好的模型和 provider。</Callout>

为了构建这份目录，我们：

1. 测试了一组精选的模型，并与他们的团队探讨如何以最佳方式运行这些模型。
2. 与 provider 合作，确保模型被正确地提供服务。
3. 对每个模型/provider 组合进行基准测试，最终得出我们放心推荐的列表。

Console 是一个 AI 网关，让你能够访问这些模型。

## 目标

我们构建 Console 是为了：

1. 为编程 agent **基准测试**最好的模型和 provider。
2. 提供**最高质量**的选项，不降级性能，也不路由到更廉价的 provider。
3. 按**成本价**出售，把降价让利传递给用户，仅在覆盖处理费的范围内加价。
4. **不锁定**：你可以将 Console 与任何编程 agent 搭配使用，也可以在 OpenCode 中改用其他 provider。
