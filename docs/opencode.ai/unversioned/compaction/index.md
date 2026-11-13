---
source_url: https://opencode.ai/docs/compaction/
source_hash: sha256:128af13661a2ccbb9019925f7f21858320ba2a58bebe9d33fd6776ea298432e2
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# 压缩（Compaction）

压缩通过用一份摘要替换较早的对话，为长会话腾出空间，使会话能够突破模型上下文上限继续进行。

## 工作原理

当会话接近模型的上下文上限时，OpenCode 会总结当前的整个对话。同时，它会在摘要旁保留最近的对话（默认约 15,000 token），使近期的确切细节依然可用。

```text
before   [ system prompt ][ older conversation ............ ][ recent 15k ][ pending work ]
request  [ system prompt ][ older conversation ............ ][ recent 15k ][ summary instructions ]
after    [ system prompt ][ summary of older + recent ][ recent 15k ][ pending work ]
```

发送完整对话可以让摘要请求在 provider 支持时复用正常请求的提示词缓存。之后的压缩会基于该检查点之后的对话来更新已有的摘要。

## 启动

自动压缩默认开启：

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "compaction": {
    "auto": true,
    "keep": { "tokens": 15000 },
  },
}
```

压缩是有损的。如果近期的确切细节很重要，可以调大 `keep.tokens`，或者在自动压缩发生之前主动请求压缩。

## 手动

可以随时请求压缩，即使历史很短也可以：

```sh
opencode api post /api/session/ses_example/compact --data '{}'
```

`api` 命令会发现后台服务并完成认证。它的响应只确认请求已被接受，不会等待摘要生成完成。请关注 `session.compaction.*` 事件来了解它何时结束。完整操作请参阅 [API 参考](../api/index.md)。

| 规则 | 行为 |
| --- | --- |
| 时机 | 在下一个安全点运行，先于仍在等待中的提示词。 |
| 重复 | 在一次压缩待处理期间发起的请求会合并进其中。 |
| 自动化 | 即使 `compaction.auto` 为 `false` 也能工作。 |

传入 `id` 可以让一次确切的重试具备幂等性。将同一个 ID 用于不同的请求会返回冲突。

```sh
opencode api post /api/session/ses_example/compact --data '{"id":"msg_compact_once"}'
```

## 设置

在任意 [OpenCode 配置文件](../config/index.md)中添加 `compaction`：

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "compaction": {
    "auto": false,
    "keep": { "tokens": 24000 },
    "buffer": "20%",
  },
}
```

| 字段 | 默认值 | 行为 |
| --- | ---: | --- |
| `auto` | `true` | 接近上下文上限时自动压缩；当 provider 以"请求过长"拒绝请求时，自动恢复一次。手动压缩始终可用。 |
| `keep.tokens` | `15000` | 保留在摘要旁边的近期对话的大致规模。数值越大保留的细节越多，但留给新工作的空间越少。 |
| `buffer` | `"15%"`，至少 16k | 模型上下文窗口中保持空闲的比例。对话达到剩余部分时，自动压缩随之启动。数值越大，压缩发生得越早。 |

`keep.tokens` 接受非负整数。

### Buffer

`buffer` 是每个模型窗口的百分比，因此一个设置就能适配所有模型：

| 模型窗口 | `"buffer": "20%"` 时的压缩点 |
| ---: | ---: |
| 128k | ~102k |
| 1M | 800k |

- 它是保持空闲的空间，而不是压缩的触发点：`"20%"` 表示在窗口填满 80% 时压缩。
- 接受 `"1%"` 到 `"99%"`，包括 `"12.5%"` 这样的小数。
- 也可以使用 token 数量，例如 `20000`。同一个数量在小窗口中占比很大，在大窗口中占比很小。
- 不小于模型窗口的 token 数会被忽略，并采用默认值。

## 模型

默认情况下，OpenCode 使用会话的模型自己编写摘要。设置 `agents.compaction.model` 可以让摘要改用其他模型：

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "agents": {
    "compaction": { "model": "anthropic/claude-sonnet-5-5" },
  },
}
```

如果该模型无法解析，OpenCode 会回退到会话的模型。

## 后台压缩

<Callout type="warning">
  实验性功能。可能在任何版本中变更、损坏或被移除，恕不另行通知。
</Callout>

自动压缩通常会在摘要写入期间暂停会话。启用后台压缩后，OpenCode 会提前写好摘要，并在压缩时机到来时换入：

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "experimental": {
    "background_compaction": true,
  },
}
```

```text
60k tokens before the threshold   summary of the conversation so far starts in the background
                                  the session keeps going; the summary is held, not applied
threshold                         the held summary is swapped in; everything since it is kept as is
```

在较小的上下文窗口上，摘要最晚会在上一次压缩后的首个响应与阈值之间的中点启动。

| 规则 | 行为 |
| --- | --- |
| 成本 | 摘要请求会复用提示词缓存。即使摘要最终未被使用（例如会话在阈值之前就结束了），也仍会消耗 token。 |
| 等待 | 如果压缩时机到来时摘要仍在写入，会话会等待其完成。 |
| 回退 | 如果暂存摘要之后的对话增长超过了阈值的约 40%，或者模型、指令、对话起点发生了变化，则按常规方式进行压缩。 |
| 跳过 | 原生压缩、模型切换后立即发生的情况，以及 provider 以"请求过长"拒绝请求的情况不使用它。在超过提示词缓存生命周期的中断之后，它会从下一个响应重新开始。 |
| 存储 | 暂存的摘要保存在内存中，重启后会丢失。 |

## Provider

一些 provider 可以在它们那一侧压缩对话。可以通过 `settings.compaction` 按 provider 或按模型启用：

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "providers": {
    "openai": {
      "settings": { "compaction": { "type": "native" } },
      "models": {
        "gpt-6.1-sol": { "settings": { "compaction": { "type": "summary" } } },
      },
    },
  },
}
```

模型设置会覆盖 provider 设置。`native` 使用 provider 自身的压缩；`summary` 使用 OpenCode 自己的压缩。

使用原生压缩时，OpenCode 将对话发送到 provider 的压缩端点。provider 返回一个不透明的加密项，用来替代较早的对话。你的近期消息和附件（最多 `keep.tokens`）会保留在它旁边：

```text
before   [ older conversation ........................ ][ recent user messages ]
after    [ encrypted checkpoint + recent user messages ]
```

| 主题 | 行为 |
| --- | --- |
| 支持 | OpenAI Responses 模型。支持情况因部署和模型而异。 |
| 阈值 | 与摘要压缩使用相同的 `auto` 和 `buffer` 设置。手动请求同样可用。 |
| 可移植性 | 加密检查点只能与同一个 provider 和模型配合使用。如果切换模型，会话会改从原始对话继续。 |
| 过长 | 如果 provider 以"压缩后过长"拒绝，OpenCode 会用更小的请求重试。它不会切换为摘要方式。 |

## 摘要

摘要的结构经过设计，让另一个 agent 能够据此接手工作：

```md
## Objective
Finish the authentication migration.

## Next Move
- Update the callback handler.
- Verify the login flow.
```

摘要涵盖目标与需求、已做的决策、已完成和进行中的工作、阻碍与下一步行动，以及相关文件。在保留在旁边的近期对话中，较长的工具输出会被缩短，附件数据会被替换为简短描述。

压缩之后，指令文件的当前版本会成为会话的基线；参见[指令](../instructions/index.md)。

## 限制

| 限制 | 结果 |
| --- | --- |
| 模型 | 摘要压缩遵循 `agents.compaction.model`；否则使用会话的模型。原生压缩始终使用会话的模型。 |
| 历史 | 压缩需要有较早的对话可供替换。当请求几乎全部由固定指令和工具 schema 组成时，它无法腾出空间。 |
| 大小 | 如果待压缩的对话本身过长，OpenCode 会发送一个精简的文本版本，并可能省略最早的几轮交流。 |
| 恢复 | 被"过长"拒绝的请求会被压缩并重试一次。第二次被拒绝则作为错误返回。 |
| 存储 | 即使较早的消息不再发送给模型，它们仍会保留在存储中。 |

例如，压缩在这种情况下无能为力：

```text
128k context = 120k fixed instructions and tools + 8k conversation
```

## 迁移

V1 使用尾部轮次与剪裁行为。V2 使用摘要和 `compaction.keep.tokens`：

```jsonc
{
  "compaction": {
    "keep": { "tokens": 15000 }
  }
}
```

本页介绍的设置和行为均适用于 V2。
