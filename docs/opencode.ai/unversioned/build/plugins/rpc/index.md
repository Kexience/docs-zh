---
source_url: https://opencode.ai/docs/build/plugins/rpc/
source_hash: sha256:dab4e31acc16ea76081ba5c1ad3a6356e861062b5952c6f4f13d2244ac4ba5a5
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---
# RPC

插件可以暴露自定义方法和事件，它们在服务器上运行，并可以被其他插件或客户端调用。

## 定义

使用 `Rpc.define` 列出 RPC 的方法、错误和事件。

```ts title="src/rpc.ts"
import { Rpc } from "@opencode/plugin/rpc"

export const Acme = Rpc.define({
  id: "acme",
  methods: {
    search: {
      input: {
        type: "object",
        properties: { query: { type: "string" } },
        required: ["query"],
        additionalProperties: false,
      },
      output: {
        type: "object",
        properties: { text: { type: "string" } },
        required: ["text"],
        additionalProperties: false,
      },
      errors: {
        not_found: {
          type: "object",
          properties: { query: { type: "string" } },
          required: ["query"],
          additionalProperties: false,
        },
      },
    },
  },
  events: {
    updated: {
      schema: {
        type: "object",
        properties: {
          itemID: { type: "string" },
          text: { type: "string" },
        },
        required: ["itemID", "text"],
        additionalProperties: false,
      },
    },
  },
})
```

### 校验

RPC 定义描述了方法、事件和错误的输入与输出形状。它支持两种 schema 格式：

- JSON Schema，简单且无需额外依赖。
- 任何符合 Standard Schema 的校验器
  - Zod
  - Valibot
  - ArkType

### 输入与输出

每个方法都可以为其参数定义一个 `input` schema，为其返回值定义一个 `output` schema。如果方法不接受或不返回值，则可以省略其中之一。

```ts
search: {
  input: {
    type: "object",
    properties: { query: { type: "string" } },
    required: ["query"],
  },
  output: {
    type: "object",
    properties: { text: { type: "string" } },
    required: ["text"],
  },
}
```

JSON Schema 的值在 TypeScript 中是 `unknown`，因此使用前需要先收窄类型。Standard Schema 则可以推断输入和输出类型。

### 错误

在方法上添加 `errors` 映射来声明预期的失败。每个键都会成为错误的 `type`，其 schema 定义该错误的 `data`。

```ts
errors: {
  not_found: {
    type: "object",
    properties: { query: { type: "string" } },
    required: ["query"],
    additionalProperties: false,
  },
}
```

以 `rpc.` 开头的错误名被 OpenCode 保留。

### 事件

把事件添加到顶层的 `events` 映射中。每个事件都有一个 schema，用于描述发送给订阅者的数据。

事件数据必须是一个对象。没有数据时，请使用空对象 schema：

```ts
events: {
  refreshed: {
    schema: { type: "object", additionalProperties: false },
  },
}
```

标量、数组、`null` 和 `undefined` 都不是有效的事件数据。

## 实现

在 `setup` 中注册实现：

```ts title="src/index.ts"
import { Plugin } from "@opencode/plugin"
import { Acme } from "./rpc.js"

export default Plugin.define({
  id: "acme-plugin",
  async setup(ctx) {
    const registration = await ctx.rpc.register(Acme, {
      search: async (input, context) => {
        const { query } = input as { query: string }
        const text = await findText(query, { signal: context.signal })
        if (!text) return context.error("not_found", "Result not found", { query })
        return { text }
      },
    })

    const acme = ctx.rpc(Acme)
    const result = await acme.search({ query: "hello" })

    await registration.events.emit("updated", { itemID: "item-1", text: "ready" })
  },
})
```

注册 RPC 之后，同一个插件可以通过 `ctx.rpc(Acme)` 调用它。

第二个参数包含用于取消的 `signal`，以及用于声明错误的 `context.error(...)`。你可以返回错误，也可以抛出错误。

一个插件可以注册多个 RPC。释放（dispose）注册即可将其移除。

## 调用

RPC 注册之后，可以通过 HTTP 调用，也可以从其他插件调用。

### HTTP

创建一个 OpenCode 客户端，然后用 `client.rpc` 为该 RPC 创建一个子客户端：

```ts
import { OpenCode } from "@opencode/client"
import { Acme } from "opencode-acme-plugin/rpc"

const client = OpenCode.make({
  baseUrl: "http://localhost:4096",
})

const acme = client.rpc(Acme)
const result = await acme.search({ query: "hello" })
```

### 插件

插件本身已经有 OpenCode 客户端。例如，TUI 插件可以从 `context.client` 创建同样的 RPC 子客户端：

```ts title="src/tui.ts"
import { Plugin } from "@opencode/plugin/tui"
import { Acme } from "opencode-acme-plugin/rpc"

export default Plugin.define({
  id: "acme-tui",
  async setup(context) {
    const acme = context.client.rpc(Acme)
    const result = await acme.search({ query: "hello" })
    console.log(result)
  },
})
```

[GUI 插件](../gui/index.md)从 `ctx.client` 读取桌面应用自身服务器的客户端：

```tsx title="src/gui.tsx"
import { Command, Plugin } from "@opencode/plugin/gui"
import { Acme } from "opencode-acme-plugin/rpc"

export default Plugin.define({
  setup(ctx) {
    ctx.add(Command, {
      id: "search",
      title: "Search Acme",
      run: async () => {
        const result = await ctx.client.rpc(Acme).search({ query: "hello" })
        console.log(result)
      },
    })
  },
})
```

在调用处读取 `ctx.client`：服务器重启后它会变化。服务器不可达时，每次调用都会拒绝。

### 订阅

用 `events.on` 注册回调，并在不再需要监听时取消订阅：

```ts
const unsubscribe = acme.events.on("updated", (event) => {
  console.log(event.type, event.location.directory, event.data.text)
})

unsubscribe()
```

要使用异步可迭代对象，请使用 `events.subscribe("updated")`：

```ts
for await (const event of acme.events.subscribe("updated")) {
  console.log(event.data.text)
}
```

事件订阅只在线时有效，断开连接的订阅者会错过事件。

- 订阅时使用本地名称，例如 `updated`。
- 接收到的事件类型带有前缀，例如 `rpc.acme.updated`。
- 每个事件都包含 `data` 和 `location`。
- 插件卸载会关闭其订阅。

外部客户端会接收到来自所有位置的事件，因此必要时请检查 `event.location`。服务器插件仍然需要被配置并处于运行状态。
