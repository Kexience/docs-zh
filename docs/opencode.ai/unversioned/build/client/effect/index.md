---
source_url: https://opencode.ai/docs/build/client/effect/
source_hash: sha256:f3b4b1acfe4fbd2bc010dadbfb06843ba9b5998ebf02ef7f60393757c52858e2
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# Effect

`@opencode/client/effect` 是 OpenCode HTTP API 的 Effect 原生客户端。它返回类型化的 Effect 和 Stream，并把响应解码为 OpenCode schema 值。

```sh
bun add @opencode/client effect@4.0.1
```

## 创建客户端

用服务器 URL 创建客户端，然后调用按 API 资源分组的方法。

```ts
import { AbsolutePath, Location, OpenCode } from "@opencode/client/effect"
import { Effect } from "effect"
import { FetchHttpClient } from "effect/http"

const program = Effect.gen(function* () {
  const client = yield* OpenCode.make({ baseUrl: "http://localhost:4096" })
  const session = yield* client.session.create({
    location: Location.Ref.make({ directory: AbsolutePath.make("/workspace") }),
  })
  yield* client.session.prompt({
    sessionID: session.id,
    text: "Review the current changes",
  })
  return session
})

const session = await Effect.runPromise(program.pipe(Effect.provide(FetchHttpClient.layer)))
```

## 请求头与请求

在提供的 `HttpClient` 上配置默认请求头。原生操作使用常规的 Effect 中断来取消。RPC 方法还接受每次调用的 location、请求头和 signal 选项。

{/* prettier-ignore */}
```ts
import { HttpClient, HttpClientRequest } from "effect/http"

const httpClient = yield* HttpClient.HttpClient
const client = yield* OpenCode.make({ baseUrl: "https://opencode.example.com" }).pipe(
  Effect.provideService(
    HttpClient.HttpClient,
    HttpClient.mapRequest(httpClient, (request) =>
      HttpClientRequest.setHeaders(request, { authorization: `Bearer ${process.env.OPENCODE_TOKEN}` }),
    ),
  ),
)

const sessions = yield* client.session.list()
```

## 流式事件

`event.subscribe()` 和 `experimental.session.log()` 这类流式操作返回 Effect Stream。

{/* prettier-ignore */}
```ts
import { Effect, Stream } from "effect"

yield* client.event
  .subscribe()
  .pipe(Stream.runForEach((event) => Effect.logInfo("OpenCode event", { type: event.type })))
```

原生与 RPC 事件 Stream 在每个客户端之间共享一条惰性连接。构造 Stream 不会连接；消费它才会。停止一个消费者不影响其他消费者继续运行，最后一个消费者离开时数据源关闭。数据源 EOF 或失败会结束当前订阅，不会自动重试或回放。较晚加入的原生消费者会在实时事件之前收到当前连接标记。

## 插件 RPC

使用与 Promise 客户端和服务器插件相同的共享契约：

{/* prettier-ignore */}
```ts
import { Acme } from "opencode-acme-plugin/rpc"

const acme = client.rpc(Acme)
const result = yield* acme.search({ query: "hello" }, { location: { directory: "/workspace" } })

yield* acme.events
  .subscribe("updated")
  .pipe(
    Stream.runForEach((event) =>
      Effect.logInfo("Plugin event", { type: event.type, location: event.location, text: event.data.text }),
    ),
  )
```

方法的参数和结果从契约推断。第二个可选参数承载 `location`、`signal` 和 `headers`；省略 location 时使用常规的请求默认值。调用会随消费它的 Effect 一起被中断。方法错误映射在 Effect 错误通道中推断。声明的错误通过各自的数据 schema 解码。类型化子客户端会移除通用的 HTTP RPC 错误包装；保留的 `rpc.*` 类型用于标识框架失败。

RPC 事件是类型化的 Stream，而不是回调式的 `on` 监听器。它们接收该 RPC 在所有 location 上的事件，每个事件都带必需的 `location` 和常规的前缀类型（如 `rpc.acme.updated`）。这一点与服务器插件句柄不同，后者固定在各自的 location 上。定义、schema、注册和实时订阅语义参见 [Effect 插件 RPC](../../plugins/effect/rpc/index.md)。

## 本地后台服务

仅限 Node 的 `@opencode/client/effect/service` 入口以 Effect 的形式发现、启动、认证并停止本地后台服务。

```sh
bun add @effect/platform-node@4.0.1
```

为已确保运行的服务创建一个经过认证的客户端。

```ts
import { NodeFileSystem } from "@effect/platform-node"
import { OpenCode } from "@opencode/client/effect"
import { Service } from "@opencode/client/effect/service"
import { Effect } from "effect"
import { FetchHttpClient, HttpClient, HttpClientRequest } from "effect/http"

const program = Effect.gen(function* () {
  const endpoint = yield* Service.ensure()
  const httpClient = yield* HttpClient.HttpClient
  const client = yield* OpenCode.make({ baseUrl: endpoint.url }).pipe(
    Effect.provideService(
      HttpClient.HttpClient,
      HttpClient.mapRequest(httpClient, (request) =>
        HttpClientRequest.setHeaders(request, Service.headers(endpoint) ?? {}),
      ),
    ),
  )
  return yield* client.server.info()
})

const health = await Effect.runPromise(
  program.pipe(Effect.provide(FetchHttpClient.layer), Effect.provide(NodeFileSystem.layer)),
)
```

只发现而不启动，或停止确切的那个已注册服务。

{/* prettier-ignore */}
```ts
const endpoint = yield* Service.discover()
yield* Service.stop()
```
