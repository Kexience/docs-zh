---
source_url: https://opencode.ai/docs/build/plugins/effect/rpc/
source_hash: sha256:cdd01d7ddc952f3e9391920c53458601ab33850001123f39ce7132c2b3d7974f
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# RPC

Effect 插件可以暴露返回类型化 Effect 和 Stream 的方法与事件。

## 定义

配合 Effect Schema 使用 `Rpc.define` 来定义 RPC。

```ts title="src/rpc.ts"
import { Rpc } from "@opencode/plugin/rpc"
import { Schema } from "effect"

export const Acme = Rpc.define({
  id: "acme",
  methods: {
    search: {
      input: Schema.Struct({ query: Schema.String }),
      output: Schema.Struct({ text: Schema.String }),
      errors: {
        not_found: Schema.Struct({ query: Schema.String }),
      },
    },
  },
  events: {
    updated: {
      schema: Schema.Struct({ itemID: Schema.String, text: Schema.String }),
    },
  },
})
```

### 校验

Effect Schema 会校验值并推断它们的 TypeScript 类型。

```ts
input: Schema.Struct({ query: Schema.String })
```

同时也支持 JSON Schema 和 Standard Schema。

### 输入与输出

`input` 用于方法参数，`output` 用于其返回值。没有值时，两者都可以省略。

```ts
search: {
  input: Schema.Struct({ query: Schema.String }),
  output: Schema.Struct({ text: Schema.String }),
}
```

### 错误

把预期的失败添加到 `errors` 中。每个键会成为该错误的 `type`。

```ts
errors: {
  not_found: Schema.Struct({ query: Schema.String }),
}
```

### 事件

把事件添加到顶层的 `events` 映射中。事件数据必须是一个对象。

```ts
events: {
  updated: {
    schema: Schema.Struct({ itemID: Schema.String, text: Schema.String }),
  },
}
```

## 实现

在插件的 Effect 中注册实现：

```ts title="src/index.ts"
import { Plugin } from "@opencode/plugin/effect"
import { Effect } from "effect"
import { Acme } from "./rpc.js"

export default Plugin.define({
  id: "acme-effect-plugin",
  effect: (ctx) =>
    Effect.gen(function* () {
      const registration = yield* ctx.rpc.register(Acme, {
        search: ({ query }, context) =>
          findText(query).pipe(
            Effect.flatMap((text) =>
              text
                ? Effect.succeed({ text })
                : Effect.fail(context.error("not_found", "Result not found", { query })),
            ),
          ),
      })

      const acme = ctx.rpc(Acme)
      const result = yield* acme.search({ query: "hello" })

      yield* registration.events.emit("updated", { itemID: "item-1", text: result.text })
    }).pipe(Effect.orDie),
})
```

错误映射会成为每个方法 Effect 的错误类型。使用 `context.error(...)` 创建已声明的错误。

## 调用

RPC 注册之后，就可以通过 HTTP 或从另一个插件调用它。

### HTTP

先创建 Effect 客户端，再创建 RPC 子客户端：

```ts
import { OpenCode } from "@opencode/client/effect"
import { Effect } from "effect"
import { FetchHttpClient } from "effect/http"
import { Acme } from "opencode-acme-plugin/rpc"

const program = Effect.gen(function* () {
  const client = yield* OpenCode.make({ baseUrl: "http://localhost:4096" })
  const acme = client.rpc(Acme)
  return yield* acme.search({ query: "hello" })
})

const result = await Effect.runPromise(program.pipe(Effect.provide(FetchHttpClient.layer)))
```

### 插件

另一个 Effect 插件可以从它的上下文创建本地子客户端：

```ts
import { Effect } from "effect"

effect: (ctx) =>
  Effect.gen(function* () {
    const acme = ctx.rpc(Acme)
    const result = yield* acme.search({ query: "hello" })
    yield* Effect.logInfo(result.text)
  }).pipe(Effect.orDie)
```

### 订阅

RPC 事件是 Stream。按事件名称订阅，并在一个带作用域的 fiber 中运行 Stream：

{/* prettier-ignore */}
```ts
import { Effect, Stream } from "effect"

const acme = ctx.rpc(Acme)

yield* acme.events.subscribe("updated").pipe(
  Stream.runForEach((event) => Effect.logInfo(event.data.text)),
  Effect.forkScoped,
)
```

订阅是实时的，当 Stream 消费停止时随之关闭。
