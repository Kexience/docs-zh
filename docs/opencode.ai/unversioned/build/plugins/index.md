---
source_url: https://opencode.ai/docs/build/plugins/
source_hash: sha256:681ef8c90bae67c43b00d13d840588fbb7e9226128e3e85fb098838342893f28
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# 概览

插件可以修改 OpenCode 的行为并添加新功能。一个插件就是一个包，可以包含 server 部分、TUI 部分、GUI 部分，或任意组合。

```ts title=".opencode/plugins/example/index.ts"
import { Plugin } from "@opencode/plugin"

export default Plugin.define({
  id: "example",
  async setup(ctx) {
    await ctx.storage.set("loaded", true)
  },
})
```

要迁移现有的 OpenCode 1 插件？请遵循 [V1 插件迁移指南](migrate-v1/index.md)。

## 组成部分

每个部分都是包的一个导出。所有部分的 SDK 都来自唯一的 `@opencode/plugin` 依赖。

```json title="package.json"
{
  "name": "opencode-acme-plugin",
  "version": "1.0.0",
  "type": "module",
  "exports": {
    ".": "./src/index.ts",
    "./tui": "./src/tui.tsx",
    "./gui-experimental": "./dist/gui-experimental.cjs",
    "./rpc": "./src/rpc.ts"
  },
  "files": ["src", "dist"],
  "dependencies": {
    "@opencode/plugin": "latest"
  }
}
```

- **Server**（`.` 或 `./server`）借助 `@opencode/plugin` 运行在 OpenCode 服务器中。它添加工具、钩子、集成、命令和 agent。参见 [Server](server/index.md)；Effect API 见 [Effect 插件](effect/index.md)。
- **TUI**（`./tui`）借助 `@opencode/plugin/tui` 运行在终端 UI 中。参见 [TUI](cli/index.md)。
- **GUI**（`./gui-experimental`）借助 `@opencode/plugin/gui`，在每个 OpenCode Desktop 窗口中运行其 `setup`，并在桌面应用的主进程中运行其 `main`。参见 [GUI](gui/index.md)。
- **RPC**（`./rpc`）是一个类型化契约，由 server 部分实现，供其他部分和客户端调用。参见 [RPC](rpc/index.md)。

插件的 `id` 来自其 server 部分的 `Plugin.define`。只有 GUI 部分而没有 server 部分的包，以包名（或本地目录名）作为 `id`。TUI 部分声明自己的 `id`；GUI 部分不声明，直接沿用插件的。

## 加载

`.opencode/plugins/` 下的插件会自动加载，就像上面的本地示例一样。要加载已发布的包或其他位置的插件目录，请把它们添加到 `opencode.json(c)` 的 `plugins` 中：

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": [
    "opencode-acme-plugin",
    "opencode-acme-plugin@1.2.0",
    "@acme/opencode-plugin",
    "./plugins/local",
    "../shared/plugin",
    "/absolute/path/plugin",
    "file:///home/me/plugins/local",
    {
      "package": "@acme/opencode-plugin",
      "options": {
        "agent": "reviewer",
        "strict": true,
      },
    },
  ],
}
```

- 一个条目会加载所有部分。TUI 加载其 server 所加载插件的 TUI 部分，OpenCode Desktop 则加载全局 `opencode.json(c)` 中插件的 GUI 部分。
- 只含 TUI 部分的包应放入 [`cli.json`](../../cli/plugins/index.md)。
- 带有 `package.json` 的 `name` 和 `exports` 的本地插件目录，会像已发布的包一样通过它们加载各部分。如果没有这些字段，则按根目录下的文件名加载：`server`（否则用 `index`）、`tui` 和 `rpc`，扩展名为 `.ts`、`.tsx` 或 `.js`；GUI 部分为 `gui-experimental.cjs`（或 `.js`）。
- 更多加载和配置选项见[配置插件](../../plugins/index.md)。

## 发布

已发布的插件就是一个 npm 包，带有上面的 `package.json`。它的各部分使用与本地插件相同的默认导出。

```bash
npm publish
```

- 当其他插件和客户端需要导入你的 [RPC 契约](rpc/index.md)而不加载你的实现时，请导出 `./rpc`。
- 发布前先构建 GUI bundle，并通过 `files` 把它包含进来。参见[构建 bundle](gui/index.md#build-the-bundle)。
- 使用与你目标 OpenCode 版本兼容的版本号，并测试已安装的包，而不只是 workspace 链接的副本。当你采用更新的 API 契约时，发布一次兼容的插件更新。

<CardGroup cols={2}>
  <Card title="Server" href="/build/plugins/server">
    在 OpenCode 服务器中添加工具、钩子、集成、命令和 agent。
  </Card>
  <Card title="TUI" href="/build/plugins/cli">
    向终端 UI 添加命令、路由、插槽和 Markdown 渲染器。
  </Card>
  <Card title="GUI" href="/build/plugins/gui">
    向 OpenCode Desktop 添加面板、命令、设置页面和原生集成。
  </Card>
  <Card title="RPC" href="/build/plugins/rpc">
    从 server 部分向其他部分和客户端暴露类型化的方法和事件。
  </Card>
</CardGroup>
