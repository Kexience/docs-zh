---
source_url: https://opencode.ai/docs/build/sdk/effect/
source_hash: sha256:243dab2ea2277a8ea90d78aadb5ee94ae80fcba4e281fe49486c9b732e5963af
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# Effect

`@opencode/sdk/effect` 是 Effect 原生的嵌入式 SDK。操作返回带类型的 Effect 和 Stream，关闭所属的 Scope 时会释放 router、Location 服务、fiber 以及插件注册。

```sh
bun add @opencode/sdk effect@4.0.1
```

## 创建宿主

在 `Effect.scoped` 内创建宿主，然后使用它生成的 API 分组或 `sessions` 别名。

```ts
import { AbsolutePath, Location, OpenCode } from "@opencode/sdk/effect"
import { Effect } from "effect"

const program = Effect.scoped(
  Effect.gen(function* () {
    const opencode = yield* OpenCode.create()
    const session = yield* opencode.sessions.create({
      location: Location.Ref.make({ directory: AbsolutePath.make("/workspace") }),
    })
    yield* opencode.sessions.prompt({
      sessionID: session.id,
      text: "Review the current changes",
    })
    return session
  }),
)

const session = await Effect.runPromise(program)
```

嵌入式宿主使用的 schema 值、声明的错误、请求选项和 Stream 与 `@opencode/client/effect` 相同。

```ts
const info = yield* opencode.server.info()
const sessions = yield* opencode.sessions.list()
```

## 流式接收事件

流式端点返回 Effect `Stream` 值。当消费者需要在后台运行时，在宿主的 Scope 中 fork 它们。

```ts
import { Effect, Stream } from "effect"

yield* opencode.events.subscribe().pipe(
  Stream.runForEach((event) => Effect.logInfo("OpenCode event", { type: event.type })),
  Effect.forkScoped,
)
```

## 自定义

通过注册 Effect 插件来定制你的 OpenCode 实例。使用嵌入式宿主可以自定义 agent、模型、工具及其他行为：

```ts
import { Plugin } from "@opencode/plugin/effect"
import { Effect } from "effect"

const plugin = Plugin.define({
  id: "customize-agent",
  effect: (ctx) =>
    Effect.gen(function* () {
      const agent = ctx.agent
      yield* agent.transform((agents) => {
        agents.update("build", (agent) => {
          agent.description = "Builds features and fixes bugs for our team"
        })
      })
    }),
})

yield* opencode.plugin(plugin)
```

插件 hook、变换、工具以及完整的插件上下文请参阅[完整的 Effect 插件文档](../../plugins/effect/index.md)。

## Layer

当嵌入式宿主需要作为应用服务使用时，可以使用 `OpenCode.layer()`。

```ts
import { OpenCode } from "@opencode/sdk/effect"
import { Effect } from "effect"

const program = Effect.gen(function* () {
  const opencode = yield* OpenCode.Service
  return yield* opencode.server.info()
})

const health = await Effect.runPromise(program.pipe(Effect.provide(OpenCode.layer())))
```
