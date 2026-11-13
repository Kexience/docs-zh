---
source_url: https://opencode.ai/docs/build/client/
source_hash: sha256:54a0f18adfb9bb74843e69126da2a13baca7babe8fe8fd700b9c2c273ef10226
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# JavaScript

`@opencode/client` 是 OpenCode HTTP API 的 TypeScript 客户端。当你的应用需要通过网络连接 OpenCode 服务器时使用它。它的原生类型和方法与 [API 参考](../../api/index.md)基于同一份契约生成。插件 RPC 类型来自导入的 RPC 定义。

## 安装

```sh
bun add @opencode/client
```

## 创建客户端

用服务器 URL 创建客户端，然后调用按 API 资源分组的方法：

```ts
import { OpenCode } from "@opencode/client"

const client = OpenCode.make({
  baseUrl: "http://localhost:4096",
})

const session = await client.session.create({
  location: { directory: "/workspace" },
})

await client.session.prompt({
  sessionID: session.id,
  text: "Review the current changes",
})
```

## 请求头与请求

通过 `headers` 向 `OpenCode.make` 传入默认的认证或应用请求头。也可以提供自定义的 `fetch` 实现。每个操作的最后一个参数都是请求选项，可用于 `AbortSignal` 或单次请求的请求头。事件订阅是例外：它们只接受订阅者本地的取消方式，并使用基础客户端的请求头。

```ts
const client = OpenCode.make({
  baseUrl: "https://opencode.example.com",
  headers: {
    authorization: `Bearer ${process.env.OPENCODE_TOKEN}`,
  },
})

await client.session.list(undefined, {
  signal: AbortSignal.timeout(10_000),
})
```

## 流式事件

流式端点返回异步可迭代对象：

```ts
for await (const event of client.event.subscribe()) {
  console.log(event.type)
}
```

原生与 RPC 事件订阅者共享每个客户端的一条惰性连接。创建客户端、句柄和可迭代对象都不会打开事件连接；开始消费才会。中断迭代或中止某个订阅者只会结束那一个迭代器。最后一个订阅者离开时连接关闭。共享数据源会等待活跃订阅者接收每个事件；消费者在执行慢速工作前应当先做缓冲。

订阅只面向实时数据，没有回放，也没有自动重连。数据源故障会结束当前订阅；恢复后请重新订阅。较晚加入的原生订阅者会收到当前的 `server.connected` 标记，而不是过去的业务事件。

传入 `types` 可以只接收部分事件类型。事件类型会相应收窄，并且 `server.connected` 始终会送达，以便被过滤的订阅者知道何时重新同步。过滤发生在客户端内部的共享连接上。

```ts
for await (const event of client.event.subscribe({ types: ["config.updated"] })) {
  // event.type is "config.updated" | "server.connected"
}
```

## 插件 RPC

导入插件的共享契约，并传给 `client.rpc`：

```ts
import { OpenCode } from "@opencode/client"
import { Acme } from "opencode-acme-plugin/rpc"

const acme = client.rpc(Acme)
const result = await acme.search(
  { query: "hello" },
  { location: { directory: "/workspace" }, signal: AbortSignal.timeout(10_000) },
)

const unsubscribe = acme.events.on("updated", (event) => {
  console.log(event.type, event.location.directory, event.data.text)
})
```

方法的第二个可选参数承载 `location`、`signal` 和 `headers`，与插件定义的输入分开。省略 location 时遵循原生请求默认值：先取基础 location 请求头，再取服务器的工作目录。构造子客户端时不会选定任何 location。

方法的参数和结果从定义中推断。Schema 解析属于契约边界：调用方发送可接受的输入表示，处理器收到的是解析后的值。Promise 客户端接受 Standard Schema 或普通 JSON Schema 定义，并且不在本地运行 schema 解析器：服务器返回的已是解析并转换后的输出。Effect Schema 定义需要使用 Effect 客户端。

声明的方法错误会像其他 Promise 客户端端点的错误一样 reject，且捕获到的错误不带类型。通用的 HTTP RPC 错误包装会被类型化子客户端移除。保留的 `rpc.*` 框架失败仍然是普通的 RPC 失败，而无关的认证、传输和协议错误保持其常规的客户端表示。

RPC 订阅使用本地名称，并接收该 RPC 在所有 location 上的事件。检查必需的 `event.location` 来筛选它们。`events.subscribe` 与原生的异步可迭代 API 一致：

```ts
for await (const event of acme.events.subscribe("updated")) {
  console.log(event.data.text)
}
```

`events.on` 是同一数据源之上的便捷封装。它返回取消订阅函数；异步回调会按顺序 await。回调或数据源失败会被记录并结束该监听器。原生订阅和类型化订阅都会收到同样的常规 `rpc.<rpcID>.<event>` 信封，事件数据为直接的对象。实时订阅不回放错过的事件。

服务器插件必须被配置并实现该 RPC；导入定义并不会注册它。定义与注册 API 参见[插件 RPC](../plugins/rpc/index.md)。任何 HTTP 客户端也可以调用通用的 `POST /api/rpc/{rpcID}/{method}` 路由，发送 `{ "input": ... }` 并接收 `{ "output": ... }`。省略的输入/输出字段表示没有值。

## 本地后台服务

客户端的主要入口是浏览器兼容的，不包含本地进程管理。在 Node 应用中，请从 `@opencode/client/service` 导入原生的 Promise 服务 API。

- `Service.discover()` 返回一个健康的已注册 endpoint，不启动进程。
- `Service.ensure()` 返回一个兼容的服务，必要时启动一个。
- `Service.stop()` 停止确切的那个已注册服务实例。
- `Service.headers(endpoint)` 为客户端创建认证请求头。

```ts
import { OpenCode } from "@opencode/client"
import { Service } from "@opencode/client/service"

const endpoint = await Service.ensure()
const client = OpenCode.make({
  baseUrl: endpoint.url,
  headers: Service.headers(endpoint),
})

const info = await client.server.info()
```

`Service.ensure()` 接受可选的注册文件、版本、服务命令和 `onStart` 回调。`version` 接受精确值或兼容性谓词：

```ts
const endpoint = await Service.ensure({
  file: "/var/run/opencode/service.json",
  version: (version) => version.startsWith("2."),
  command: ["opencode", "serve", "--service"],
  onStart(reason, previousVersion) {
    console.log(reason, previousVersion)
  },
})
```

省略这些选项时使用标准注册路径和 `opencode serve --service` 命令。
