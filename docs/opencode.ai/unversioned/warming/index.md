---
source_url: https://opencode.ai/docs/warming/
source_hash: sha256:03b06523b60ea899535d8b3fe324c31ec4d35f1a8f0ef2f22c90214f00dad38e
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# 预热

会话预热会周期性地向模型发送请求，以在你在两次提示之间暂停时，保住 provider 侧的提示缓存或其他短生命周期状态。该功能默认关闭。

可在任意 [OpenCode 配置文件](../config/index.md)中启用预热：

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "warming": true,
}
```

采用此配置时，OpenCode 会在最近活跃会话的提示缓存即将过期前对其进行预热：即模型 [`cache.ttl`](../models/index.md#cache-lifetime) 的 90% 时刻；模型没有该设置时，则每四分钟一次。它一直持续到距最近一次非预热请求已过去 30 分钟为止。

## 选项

使用对象形式可以更改预热提示、空闲间隔或活跃窗口：

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "warming": {
    "prompt": "Do not perform any work. Reply with exactly: OK",
    "interval": "5 minutes",
    "duration": "1 hour",
  },
}
```

| 字段 | 默认值 | 用途 |
| --- | --- | --- |
| `prompt` | 保活指令 | 作为一条临时用户消息附加到每次预热请求。默认提示要求模型不做任何工作、不使用工具，并回复 `OK`。 |
| `interval` | `"auto"` | 距下一次预热请求的空闲时间。`"auto"` 使用模型 `cache.ttl` 的 90%；模型没有该设置时为四分钟。 |
| `duration` | `"30 minutes"` | 预热窗口，从最近一次非预热模型请求起计。 |

省略的对象字段保持默认值。例如，下面只更改了间隔：

```jsonc title="opencode.jsonc"
{
  "warming": {
    "interval": "2 minutes",
  },
}
```

## 自动间隔

默认情况下 `interval` 为 `"auto"`，会在每个模型的提示缓存即将过期前进行预热。OpenCode 使用模型 [`cache.ttl`](../models/index.md#cache-lifetime) 设置的 90%，因此 `"5m"` 的缓存每 4.5 分钟预热一次。没有 `cache.ttl` 的模型每四分钟预热一次。

```jsonc title="opencode.jsonc"
{
  "warming": { "duration": "2 hours" },
  "providers": {
    "anthropic": { "settings": { "cache": { "ttl": "1h" } } },
  },
}
```

如果缓存的有效期比 `duration` 更长，比如使用默认 30 分钟窗口时的 `"1h"`，则不会预热，因为它本来就活得过预热窗口。OpenCode 会在每个会话中记录一次这种情况。想预热它就调大 `duration`。

## 按 provider 和模型设置

在 provider 或模型上设置 `settings.cache.warming`，可以只预热它们的会话，或给它们单独的时机。它取与顶层 `warming` 相同的值（`prompt` 除外），并覆盖顶层设置。模型设置优先于 provider 设置。

```jsonc title="opencode.jsonc"
{
  "providers": {
    "anthropic": {
      "settings": { "cache": { "ttl": "5m", "warming": true } },
      "models": {
        "claude-haiku-5-5": { "settings": { "cache": { "warming": false } } },
      },
    },
  },
}
```

这样 Anthropic 的会话每 4.5 分钟预热一次，但 Claude Haiku 5.5 除外，其他 provider 不预热。对象形式中未给出的字段依次取自顶层 `warming`，再取默认值。无效的设置会记录警告并回退到顶层 `warming`。

## 时长

`interval` 和 `duration` 接受时长字符串。两者都必须解析为大于零的有限值，且 `interval` 必须短于 `duration`；否则 OpenCode 会跳过预热并记录警告。

```jsonc title="opencode.jsonc"
{
  "warming": {
    "interval": "30 seconds",
    "duration": "1 hour",
  },
}
```

## 时机

预热在顶层会话中一次非预热模型请求之后开始。subagent 会话不会被预热。每个间隔都从最近一次请求或预热请求发出的时刻起计，而不是从其响应结束的时刻起计，因为 provider 的缓存有效期从请求到达它那一刻开始。预热请求不会延长活跃窗口。

```text
00:00  normal model request sent
00:01  response finishes
00:04  warming request
00:08  warming request
00:30  warming stops
```

任何新的非预热模型活动（包括压缩）都会重置这两个计时器。显式设置的间隔若大于或等于时长，会被拒绝并给出警告；如此之长的 `"auto"` 间隔会跳过预热，因为缓存本身就活得过窗口。

```text
00:00  normal model request
00:20  normal model request; window restarts
00:24  warming request
00:50  warming stops
```

OpenCode 绝不会在某个模型请求（包括压缩）正在运行时发送预热请求。如果间隔到期时仍有请求在运行，预热会等它结束再立即发送，前提是该请求建立的缓存尚未过期。若已过期，预热会停止，直到下一次正常请求。

```text
00:00  normal model request sent
00:04  interval due; request still running
00:04:30  response finishes; warming request
00:08:30  warming request
```

## 请求

预热请求使用会话当前的模型、agent、指令和对话上下文。OpenCode 会临时附加配置的提示，发起一次模型调用，然后丢弃响应。

```text
[current session context]
[transient user message: keep-alive prompt]
→ one model response, discarded
```

该请求不接受输入、不向历史添加消息，也不会改动持久的会话状态。OpenCode 不会分发本地工具调用，也不会继续工具循环；默认提示也要求模型不使用工具。

## 失败

预热失败只会被记录下来，不会导致失败，也不会改变会话。OpenCode 会等到下一个间隔再重试，同时原本的活跃窗口继续倒计时。

```text
00:04  warming request fails; session is unchanged
00:08  next warming attempt
```

如果一次预热请求未命中缓存——从缓存读取的内容少于写入的内容——该会话的预热会停止，直到它的下一次非预热请求。不报告缓存用量的 provider 永远不会被判为未命中。

```text
00:04  warming request misses the cache; warming stops
00:10  normal model request; warming resumes
00:14  warming request
```

## 成本

预热请求是真实的 provider 请求。它们会消耗 token、产生费用、计入速率限制，并可能像其他模型请求一样失败。

- 间隔越短，请求量越大。
- 时长越长，允许的预热请求越多。
- 只有当预热在 provider 侧带来的收益值得这些额外用量时，才启用它。

例如，在没有 `cache.ttl` 的模型上，默认设置允许在一个连续 30 分钟的窗口内最多进行七次预热尝试：分别在第 4、8、12、16、20、24 和 28 分钟。

## 禁用

将 `warming` 设为 `false` 可显式禁用。省略该字段同样保持禁用。

```jsonc title="opencode.jsonc"
{
  "warming": false,
}
```
