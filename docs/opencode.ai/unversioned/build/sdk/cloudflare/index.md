---
source_url: https://opencode.ai/docs/build/sdk/cloudflare/
source_hash: sha256:c95cc0cd0ae35b4e80af7800256f630a4d27ba602b8f46f1735319f26890ec37
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---
# Cloudflare

在 Cloudflare Durable Object 中使用 `@opencode/sdk/workerd`。该模式会使用 Durable Object 的 SQLite 存储，为驱逐恢复持久化事件，并替换不可用的本地文件系统和进程服务。

```sh
bun add @opencode/sdk
```

在整个 Durable Object 实例的生命周期内持有一个 host，而不是为每个请求都创建一个。

```ts
import { OpenCodeWorkerd } from "@opencode/sdk/workerd"
import myPlugin from "./my-plugin"

export class OpenCodeDO {
  private readonly opencode: Promise<OpenCodeWorkerd.Interface>

  constructor(state: DurableObjectState) {
    this.opencode = state.blockConcurrencyWhile(() =>
      OpenCodeWorkerd.create({
        storage: state.storage,
        config: { default_agent: "build" },
        plugins: [myPlugin],
      }),
    )
  }

  async fetch() {
    const opencode = await this.opencode
    return Response.json(await opencode.server.info())
  }
}
```

`blockConcurrencyWhile` 会在 host 就绪之前阻塞所有 Durable Object 事件，并在初始化失败时重置对象。保留的 Promise 让请求处理器在启动完成后可以直接访问同一个 host。

```ts
constructor(state: DurableObjectState) {
  this.opencode = state.blockConcurrencyWhile(() =>
    OpenCodeWorkerd.create({ storage: state.storage }),
  )
}
```

Wrangler 会通过 `workerd` 包条件选择 OpenCode 的 Workerd 安全实现。Cloudflare 可能会在不执行清理的情况下驱逐 Durable Object，因此正确性不应依赖于 `close()` 被调用。

```jsonc title="wrangler.jsonc"
{
  "compatibility_flags": ["nodejs_compat"]
}
```

## 路由出站请求

传入 `fetch` 可以把 OpenCode 的出站 HTTP 请求（OpenCode Console 配置、模型请求、web 抓取与搜索、well-known 配置以及远程 MCP 服务器）路由到自定义处理器，例如 Service Binding。Code Mode 中的 agent 代码继续使用 `globalThis.fetch`。

```ts
OpenCodeWorkerd.create({
  storage: state.storage,
  fetch: (input, init) => {
    const request = new Request(input, init)
    return new URL(request.url).hostname === "console.example.com" ? env.CONSOLE.fetch(request) : fetch(request)
  },
})
```

## 自定义

通过注册随 Worker 一起打包的插件来定制你的 OpenCode 实例。把插件传给 `OpenCodeWorkerd.create()`，即可定制 agent、模型、工具以及其他行为：

```ts
import { Plugin } from "@opencode/plugin"
import { OpenCodeWorkerd } from "@opencode/sdk/workerd"

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

await OpenCodeWorkerd.create({
  storage: state.storage,
  config: { default_agent: "build" },
  plugins: [plugin],
})
```

插件钩子、transform、工具以及完整的插件上下文请参阅[完整的插件文档](../../plugins/server/index.md)。
