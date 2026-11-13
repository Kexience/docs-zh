---
source_url: https://opencode.ai/docs/cli/plugins/
source_hash: sha256:5a79f8dc7591f0862e1c1e6b6956f7e70a29577d008e4d02e88c3af88cd6df9f
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---
# 插件

在 `opencode.json(c)` 中配置且暴露了 TUI 组件的插件会被 CLI 自动加载。要了解如何构建插件，请参阅[构建插件](../../build/plugins/index.md)。你不需要把同一个包再加到 `cli.json` 中。CLI 会从已连接的 OpenCode 服务器获取活跃插件列表，因此即使服务器是远程的也能生效。

`cli.json` 用于仅面向 CLI 的插件。这些插件在终端本地运行，并且在 CLI 连接到远程服务器时仍然保持活跃：

```json title="cli.json"
{
  "plugins": [
    "opencode.example",
    "opencode.example@1.0.0",
    "@example/opencode-tui",
    "@example/opencode-tui@1.0.0",
    "./plugins/status",
    "../plugins/status",
    "/home/user/plugins/status",
    "file:///home/user/plugins/status"
  ]
}
```

条目按顺序处理。在 ID 或通配符前加 `-` 前缀可禁用匹配的插件：

```json title="cli.json"
{
  "plugins": ["*", "-opencode.notifications", "-team.*"]
}
```

使用对象形式传递插件选项：

```json title="cli.json"
{
  "plugins": [
    {
      "package": "@example/opencode-tui",
      "options": {
        "compact": true
      }
    }
  ]
}
```

OpenCode 还会在全局配置目录和项目的 `.opencode` 目录下发现插件。每个插件使用与已发布包相同的布局，server 和 TUI 入口放在一起。

```text title="Plugin discovery paths"
<global-config>/plugins/status/index.ts
<global-config>/plugins/status/tui.ts
<project>/.opencode/plugins/status/index.ts
<project>/.opencode/plugins/status/tui.ts
```

被发现的插件可以直接导入 `@opencode/plugin/tui`，OpenCode 会在运行时解析这个包。示例请参阅[构建 TUI 插件](../../build/plugins/cli/index.md)。
