---
source_url: https://opencode.ai/docs/websearch/
source_hash: sha256:8dc1098d92e3c09942568d3899551f22674725ae3c98accab4d8328828773470
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# 网页搜索

向 OpenCode 询问最新信息时，它可以搜索网页、阅读结果，并在回答中附上来源链接。

```text
Find the latest Bun release and summarize the changes.
```

首次搜索时会提示你允许网页搜索并选择一个 provider。OpenCode 会记住你的选择，供之后的会话使用。

## Provider

OpenCode 内置五个搜索 provider：

| Provider  | ID          | 环境变量                       |
| ---       | ---         | ---                            |
| Exa       | `exa`       | `EXA_API_KEY`                  |
| Firecrawl | `firecrawl` | `FIRECRAWL_API_KEY`            |
| Parallel  | `parallel`  | `PARALLEL_API_KEY`             |
| Tavily    | `tavily`    | `TAVILY_API_KEY`               |
| TinyFish  | `tinyfish`  | `TINYFISH_API_KEY`（可选）     |

在 TUI 中用 `/connect` 关联一个账户，或在启动 OpenCode 之前设置 provider 的环境变量。

```bash
$ TAVILY_API_KEY=your-key opencode
```

## 选择

在 `opencode.jsonc` 中设置 provider 可以跳过选择提示。

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "websearch": {
    "provider": "tavily",
  },
}
```

使用 `"random"` 可以自动选择一个可用的 provider。每个会话会一直使用自己选中的 provider，直到该 provider 被限流。

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "websearch": {
    "provider": "random",
  },
}
```

## 限制

当某个 provider 返回 HTTP 429 时，随机选择会改用另一个可用的 provider 重试搜索。被限流的 provider 会等待其 `Retry-After` 时间，如果响应中没有包含有效时间则等待 60 秒。

```text
Exa returns HTTP 429
→ Exa enters cooldown
→ OpenCode retries with another provider
```

如果所有 provider 都在冷却中，搜索会立即失败。移动会话或重启其服务器会清除其记住的 provider；冷却状态由同一工作区中的会话共享。

## 权限

网页搜索使用 `websearch` 权限操作，资源为搜索查询。未被显式允许的搜索会先询问。

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "permissions": [
    {
      "action": "websearch",
      "resource": "*",
      "effect": "ask",
    },
  ],
}
```

关于规则顺序和匹配方式，请参阅[权限](../permissions/index.md)。

## 禁用

把 `websearch` 设为 `false`，即可从模型请求中移除网页搜索工具。

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "websearch": false,
}
```
