---
source_url: https://opencode.ai/docs/build/sdk/
source_hash: sha256:f07ef149e9fbe8571544d6761aa15581e208e44c8c082b2596cb51d9043194fc
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# 概览

`@opencode/sdk` 把 OpenCode 直接托管在你的应用内。与[网络客户端](../client/index.md)不同，它会组装 OpenCode 服务器，并通过内存中的 HTTP 路由器转发 API 调用。它不打开任何 HTTP 监听器，也不在客户端与服务器之间增加网络跳数。

关于 Cloudflare Durable Objects，请参阅 [Cloudflare 指南](cloudflare/index.md)。

安装 SDK：

```sh
bun add @opencode/sdk
```

## 创建宿主

`OpenCode.create()` 返回一个显式持有的宿主。使用 `await using` 来释放它的路由器、Location 服务、fiber 和作用域化的插件注册：

```ts
import { OpenCode } from "@opencode/sdk"

await using opencode = await OpenCode.create()
const session = await opencode.sessions.create({
  location: { directory: "/workspace" },
})

await opencode.sessions.prompt({
  sessionID: session.id,
  text: "Review the current changes",
})
```

当显式资源管理不可用时，可以显式调用 `await opencode.close()`。

内嵌宿主使用与 `@opencode/client` 相同的 Promise 值、声明的错误、请求选项和 `AsyncIterable` 流。它暴露完整的生成客户端，并为会话组和事件组额外提供 `sessions` 和 `events` 便捷别名。

## Worktree

Worktree 操作需要 `projectID`。create 和 refresh 会从项目保存的规范检出（canonical checkout）中加载配置和插件。list 只读取保存的清单；remove 会激活规范插件并使用记录的策略，若该策略不可用则失败。

```ts
const projectID = session.projectID
const worktree = await opencode.worktree.create({ projectID, name: "task" })
await opencode.worktree.refresh({ projectID })
await opencode.worktree.remove({ projectID, directory: worktree.directory, force: false })
```

refresh 会使用所有可用的策略在已知的检出根目录中发现 worktree。通过[插件的 worktree transform](../plugins/server/index.md#worktrees) 注册自定义策略。

## 流式事件

```ts
for await (const event of opencode.events.subscribe()) {
  console.log(event.type)
}
```

通过生成的请求选项传入 `AbortSignal`，或者结束迭代即可取消其响应体。

## 自定义

通过注册插件来定制你的 OpenCode 实例。把插件传给 `OpenCode.create()`，在内嵌宿主启动时定制 agent、模型、工具和其他行为：

```ts
import { Plugin } from "@opencode/plugin"
import { OpenCode } from "@opencode/sdk"

const plugin = Plugin.define({
  id: "customize-agent",
  async setup(ctx) {
    await ctx.agent.transform((agents) => {
      agents.update("build", (agent) => {
        agent.description = "Builds features and fixes bugs for our team"
      })
    })
  },
})

await using opencode = await OpenCode.create({ plugins: [plugin] })
```

启动后调用 `await opencode.plugin(plugin)` 可以再注册一个插件。

插件钩子、transform、工具和完整的插件上下文，参见[完整的插件文档](../plugins/server/index.md)。
