---
source_url: https://opencode.ai/docs/build/plugins/migrate-v1/
source_hash: sha256:4f91d15e16a0372843c1ea0d814081546ddee9e1f02611c97517e8d82a279756
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---
# 从 V1 迁移插件

插件配置可以自动规范化，但插件实现代码必须手动移植。V1 插件函数返回一个同时包含工具和钩子（hook）的对象。V2 插件默认导出一个带有 `id` 和 `setup(ctx)` 的定义；`setup` 通过上下文注册钩子、transform、工具和订阅。

<Callout type="warning">
  V1 插件实现无法在 V2 中运行。移动文件或重命名配置条目是不够的。
</Callout>

## 迁移插件配置

把 `plugin` 重命名为 `plugins`。把"包 + 选项"的元组形式替换为对象形式：

```jsonc
// V1
{
  "plugin": [
    "opencode-example-plugin",
    ["./plugin/local.ts", { "enabled": true }]
  ]
}

// V2
{
  "plugins": [
    "opencode-example-plugin",
    {
      "package": "./plugin/local",
      "options": { "enabled": true }
    }
  ]
}
```

V2 会从 `.opencode/plugin/` 和 `.opencode/plugins/` 两处发现本地插件；V2 文件请使用 `.opencode/plugins/`。配置中的本地路径必须指向目录。对于上面的示例，请把移植后的实现移到 `./plugin/local/index.ts`；配置为 `./plugin/local.ts` 的文件会被跳过并在日志中记录一条警告。移动插件时，请把它的支撑模块一并保留在旁边。本地插件和包插件使用相同的实现 API。

## 替换入口

更改包导入，把导出的插件函数替换为 `Plugin.define`，并把初始化逻辑移入 `setup`。

```ts title="V1"
import type { Plugin } from "@opencode-ai/plugin"

export const ExamplePlugin: Plugin = async ({ directory, project, client }) => {
  await client.app.log({
    body: { service: "example", level: "info", message: `Loaded for ${project.id}` },
  })

  return {
    // V1 tools and hooks
  }
}
```

```ts title="V2"
import { Plugin } from "@opencode/plugin"

export default Plugin.define({
  id: "example",
  async setup(ctx) {
    await ctx.storage.set("last-project", ctx.location.project.id)
    console.log(`Loaded for ${ctx.location.directory}`)
  },
})
```

每个 V2 插件都需要一个稳定的 `id`。插件存储按这个 ID 划分作用域，状态和诊断信息中也用该 ID 标识插件。已发布的插件应当依赖与目标 OpenCode 版本兼容的 `@opencode/plugin` 版本。

## 迁移上下文

V2 上下文既是 OpenCode 客户端，也是插件 API。大多数操作按领域（domain）分组，而不是挂在一个单独的 `client` 属性上。

| V1 | V2 |
| --------------------------------------- | ------------------------------------------------------------------- |
| `directory` | `ctx.location.directory` |
| `project` | `ctx.location.project` |
| `client` | 领域方法，例如 `ctx.session`、`ctx.permission`、`ctx.agent` |
| 插件选项参数 | `ctx.options` |
| 返回的 `dispose()` 钩子 | `setup` 返回的清理函数 |
| 返回的 `event` 钩子 | `ctx.event.subscribe()` |
| 返回的配置、模型或工具更改 | 对应领域的 `transform(...)` |
| `$` Bun shell 助手 | 导入并管理你的插件所使用的进程 API |

`ctx.location` 描述的是该插件实例加载时所在的位置，而不是该插件可能观察到的每个会话或事件的位置。当这个区别很重要时，请直接读取会话或事件数据。

上下文暴露的领域远多于表中列出的这些，还包括目录（catalogs）、命令、集成、MCP 服务器、references、技能、存储、VCS、worktree 和 web 搜索。请参阅[完整的插件上下文](../server/index.md#api)。

## 在 `setup` 中注册钩子

V1 通过字符串键返回钩子。V2 在拥有该操作的领域上注册每个钩子。回调接收一个可变的事件对象，而不是分开的 `input` 和 `output` 对象。

```ts title="V1"
import type { Plugin } from "@opencode-ai/plugin"

export const GuardPlugin: Plugin = async () => ({
  "tool.execute.before": async (input, output) => {
    if (input.tool === "read" && output.args.filePath.includes(".env")) {
      throw new Error("Do not read .env files")
    }
  },
  "shell.env": async (_input, output) => {
    output.env.COMPANY_ENV = "development"
  },
})
```

```ts title="V2"
import { Plugin } from "@opencode/plugin"

export default Plugin.define({
  id: "company.guard",
  async setup(ctx) {
    await ctx.tool.hook("execute.before", (event) => {
      const input = event.input as { filePath?: string }
      if (event.tool === "read" && input.filePath?.includes(".env")) {
        throw new Error("Do not read .env files")
      }
    })

    await ctx.shell.hook("create.before", (event) => {
      event.env.COMPANY_ENV = "development"
    })
  },
})
```

注册在插件生命周期内保持有效，并在插件卸载时被释放。只有当插件需要通过 `registration.dispose()` 提前移除某个特定的钩子或 transform 时，才需要保留返回的注册对象。

使用下表为每个 V1 钩子找到最接近的 V2 API：

| V1 钩子 | V2 API |
| -------------------------------------- | ------------------------------------------------------------ |
| `event` | `ctx.event.subscribe()` |
| `dispose` | `setup` 返回的清理函数 |
| `config` | 受影响领域上的 transform |
| `tool` 映射 | `ctx.tool.transform(...)` |
| `auth` | `ctx.integration.transform(...)` 和集成 API |
| `provider` | `ctx.provider.transform(...)` 和 `ctx.model.transform(...)` |
| `chat.message` | `ctx.session.hook("prompt", ...)` |
| `chat.params` | `ctx.session.hook("context", ...)` |
| `chat.headers` | `ctx.session.hook("model.request", ...)` 或 `"http.request"` |
| `permission.ask` | `ctx.permission.hook("evaluate", ...)` |
| `command.execute.before` | 命令 transform 或提示词钩子，取决于意图 |
| `tool.execute.before` | `ctx.tool.hook("execute.before", ...)` |
| `tool.execute.after` | `ctx.tool.hook("execute.after", ...)` |
| `shell.env` | `ctx.shell.hook("create.before", ...)` |
| `tool.definition` | `ctx.tool.transform(...)` |
| `experimental.chat.system.transform` | `ctx.session.hook("context", ...)` 并编辑 `event.system` |
| `experimental.chat.messages.transform` | `ctx.session.hook("context", ...)` 并编辑 `event.messages` |
| `experimental.session.compacting` | `ctx.session.hook("compaction", ...)` |

这些是迁移目的地，并不总是简单的重命名。特别要注意，V2 的 `prompt` 钩子在提示词被持久接纳之前运行，而 `context` 在 agent 模型请求发出前一刻运行。如果某个转换必须作用于每一种模型请求，请分别注册 `context`、`compaction`、`generate` 和 `title`。

并非每个实验性 V1 钩子都有直接对应的 V2 钩子。对于使用 `experimental.compaction.autocontinue`、`experimental.provider.small_model` 或 `experimental.text.complete` 的插件，请基于 V2 的会话、provider、模型和事件 API 重新评估，而不是保留对内部生命周期的假设。

`command.execute.before` 也没有一对一的全局钩子。当插件拥有某个命令时，用 `ctx.command.transform` 注册该命令。如果真实意图是修改由命令和其他提示词来源提交的提示词，请使用提示词钩子。

## 迁移请求钩子

V2 把提示词接纳、模型可见上下文、语义模型选项和原生 HTTP 分成不同层。请为你的插件选择所需的最窄一层。

```ts title="V1"
import type { Plugin } from "@opencode-ai/plugin"

export const RequestPlugin: Plugin = async () => ({
  "chat.params": async (_input, output) => {
    output.temperature = 0.2
    output.maxOutputTokens = 8_000
  },
  "chat.headers": async (_input, output) => {
    output.headers["x-plugin"] = "review"
  },
  "experimental.chat.system.transform": async (_input, output) => {
    output.system.push("Focus on correctness.")
  },
})
```

```ts title="V2"
import { Plugin } from "@opencode/plugin"

export default Plugin.define({
  id: "review-request",
  async setup(ctx) {
    await ctx.session.hook("context", (event) => {
      event.system.push({ type: "text", text: "Focus on correctness." })
      event.options.temperature = 0.2
      event.options.maxTokens = 8_000
    })

    await ctx.session.hook("model.request", (event) => {
      event.headers["x-plugin"] = "review"
    })
  },
})
```

语义化的 provider 选项请放在 `event.options` 中。模型请求头和原始请求设置请使用 `model.request`；只有当插件需要原生 provider HTTP 交互时才使用 `http.request` 或 `http.response`。provider 特定的钩子可以把 `{ providerID: "..." }` 作为第三个参数传给 `ctx.session.hook`。

## 迁移自定义工具

V1 返回一个用旧的 `tool()` 助手构建的 `tool` 映射。V2 通过同步的 `ctx.tool.transform` 编辑器注册工具定义。工具 schema 使用 JSON Schema，执行结果返回结构化内容。

```ts title="V1"
import { tool } from "@opencode-ai/plugin"

export const ToolsPlugin = async () => ({
  tool: {
    greeting: tool({
      description: "Create a greeting",
      args: { name: tool.schema.string() },
      async execute(args) {
        return `Hello ${args.name}!`
      },
    }),
  },
})
```

```ts title="V2"
import { Plugin } from "@opencode/plugin"

export default Plugin.define({
  id: "greeting",
  async setup(ctx) {
    await ctx.tool.transform((editor) => {
      editor.add({
        name: "greeting",
        description: "Create a greeting",
        input: {
          type: "object",
          properties: { name: { type: "string" } },
          required: ["name"],
          additionalProperties: false,
        },
        async execute(input) {
          return { content: `Hello ${(input as { name: string }).name}!` }
        },
      })
    })
  },
})
```

transform 是可重放的状态编辑。请保持其回调同步、轻量，且不包含一次性的副作用。在注册之前加载外部数据，在回调中捕获它，并在数据变化时调用该领域的 `reload()` 方法。之后执行的插件 transform 能看到之前的更改，并可以更新、替换或移除它们。

同样的 transform 模式可以替代 V1 的 `config` 和 `provider` 钩子，但 V2 不暴露一个可变的全局配置对象。请向拥有该配置的领域注册更改：`ctx.agent`、`ctx.provider`、`ctx.model`、`ctx.command`、`ctx.integration`、`ctx.mcp`、`ctx.reference`、`ctx.skill`、`ctx.tool`、`ctx.vcs`、`ctx.websearch` 或 `ctx.worktree`。认证方式属于集成（integration）；provider transform 贡献来源定义和 provider 设置，而模型 transform 对完整的活跃 provider 模型集合应用限制和覆盖。

```ts
await ctx.provider.transform((editor) => {
  editor.update("anthropic", (provider) => {
    provider.headers = { ...provider.headers, "x-company": "engineering" }
  })
})

await ctx.model.transform((editor) => {
  editor.list("anthropic").forEach((model) => {
    if (!model.capabilities.tools) editor.remove(model.providerID, model.id)
  })
})
```

## 迁移事件与清理

V1 的 `event` 回调变为对公共服务器事件流的异步订阅。通过 `setup` 返回的清理函数中止它。

```ts title="V2"
import { Plugin } from "@opencode/plugin"

export default Plugin.define({
  id: "notifications",
  setup(ctx) {
    const controller = new AbortController()

    void (async () => {
      for await (const event of ctx.event.subscribe({ signal: controller.signal })) {
        if (event.type === "session.idle") console.log("Session completed")
      }
    })()

    return () => controller.abort()
  },
})
```

清理函数用于定时器、子进程、套接字以及插件拥有的其他资源。钩子和 transform 的注册按插件划分作用域，会被自动清理。

## 迁移选项与持久状态

从 `ctx.options` 读取选项。当状态属于某个插件时，使用 `ctx.storage` 而不是自己发明一个全局文件；它的 JSON 值是持久的，并且按插件划分作用域。

```ts
const strict = ctx.options.strict === true
await ctx.storage.set("settings", { strict })
const settings = await ctx.storage.get("settings")
```

## 用一个包同时支持 V1 和 V2

一个包可以在一个默认导出中临时暴露两种实现。V1 调用 `server()`，V2 调用 `setup()`。这两套 API 仍然是分开的，这种形式不会自动转换钩子。

```ts title="src/index.ts"
import { Plugin } from "@opencode/plugin"

export default {
  ...Plugin.define({
    id: "example",
    async setup(ctx) {
      await ctx.tool.hook("execute.before", () => {
        console.log("A tool is about to run")
      })
    },
  }),
  async server() {
    return {
      "tool.execute.before": async () => {
        console.log("A tool is about to run")
      },
    }
  },
}
```

OpenCode `1.18.29` 及更高版本支持 V1 对象入口。如果你还要支持更老的 V1 版本，请使用单独的包版本或入口，并测试你声称支持的最老版本。在你的支持窗口结束后移除 V1 实现。

## 验证移植后的插件

对每个插件：

1. 确认其 ID 和来源出现在活跃插件列表中。
2. 实际触发每一个已注册的钩子、transform、工具、命令和事件订阅。
3. 通过重新加载或移除插件来验证清理逻辑。
4. 用一个干净的项目测试插件选项和持久化状态。
5. 对于已发布的包，请测试已安装的包，而不是仅测试通过 workspace 链接的副本。

完整的 Promise API 请参阅 [Server](../server/index.md)，Effect 入口请参阅 [Effect 插件](../effect/index.md)，自定义方法和事件请参阅[插件 RPC](../rpc/index.md)，终端 UI 请参阅 [TUI 插件](../cli/index.md)。
