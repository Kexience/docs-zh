---
source_url: https://opencode.ai/docs/console/harnesses/raycast/
source_hash: sha256:eec370ff4482f7e2dd8d7a734a918d8caa1c567d535c79ca8d7fc115acc24025
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# Raycast

通过 [OpenCode 扩展](https://www.raycast.com/vimtor/opencode)，你可以在 Raycast AI Chat、Quick AI 和 AI Commands 中使用 Console 和 Go 模型。由扩展提供的模型需要 [Raycast Pro](https://www.raycast.com/pro)。

## 配置

该扩展会加载你的工作区中已启用的模型，并把用量计入该工作区。选择付费或 Go 模型；免费层级的 chat 模型需要 OpenCode，从 Raycast 会返回 HTTP `403`。

1. 从 Raycast Store 安装该扩展。
2. 创建一个[个人 API key](../index.md#get-an-api-key)，并粘贴到扩展的 **API Key** 偏好设置中。
3. 在 Raycast 模型选择器中允许该扩展提供模型。

在 Console 中启用或停用模型后，运行 **Refresh Models**。

```text
Refresh Models
```

## Go

使用来自有 [Go](../../go/index.md) 订阅的工作区的 key。之后扩展就会在模型选择器中列出 Go 模型。

## Console MCP

使用 **Install MCP Server** 命令添加 [Console MCP](../index.md#console-mcp) 服务器。

| 字段       | 值                                |
| ---------- | --------------------------------- |
| Transport  | HTTP                              |
| URL        | `https://opencode.ai/console/mcp` |
| OAuth Type | Dynamic                           |

Raycast 第一次使用该服务器时会要求你登录。
