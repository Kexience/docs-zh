---
source_url: https://opencode.ai/docs/build/plugins/server/
source_hash: sha256:0750ebdab9ad876774096c1d637366b6cf7c90cfebdc2b7df0a10021d42577a4
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# 服务器端

插件的服务器端部分运行在 OpenCode 服务器中。它修改 OpenCode 的行为并添加功能：工具、钩子、集成、命令和 agent。关于插件包如何组织、加载和发布，参见[概览](../index.md)。

```ts title=".opencode/plugins/example/index.ts"
import { Plugin } from "@opencode/plugin"

export default Plugin.define({
  id: "example",
  async setup(ctx) {
    await ctx.storage.set("loaded", true)
  },
})
```

## 生命周期

`setup` 在插件加载时运行。它可以返回一个清理函数，该函数在插件卸载时运行。

```ts
import { Plugin } from "@opencode/plugin"

export default Plugin.define({
  id: "example",
  setup(ctx) {
    console.log(`loaded in OpenCode ${ctx.app.version}`)
    return () => console.log("unloaded")
  },
})
```

### 上下文

插件上下文本质上是一个 [OpenCode 服务器客户端](../../client/index.md)。它的读取和操作方法与客户端使用相同的输入和响应。此外，它还提供插件专属的方法，用于变换（transforms）、运行时钩子、重载、注册和插件选项。

```ts
setup(ctx) {
  console.log(ctx.app.version)
}
```

`ctx.location` 描述该插件实例的加载位置。它包含 `directory`、可选的 `workspaceID`，以及 `project` 元数据（`id`、`directory` 和 `canonical`）。它在 Promise 插件和 Effect 插件中都可用。这是该插件实例自身的位置，而不是它能访问的每个会话或收到的事件的位置。

```ts
setup(ctx) {
  console.log(ctx.location.directory)
  console.log(ctx.location.project.canonical)
}
```

### 选项

在 `opencode.json(c)` 中使用对象形式传入插件选项。

```jsonc title="opencode.jsonc"
{
  "plugins": [
    {
      "package": "./plugins/company",
      "options": {
        "strict": true,
      },
    },
  ],
}
```

在 `setup` 期间从 `ctx.options` 读取这些值。

```ts title="plugins/company/index.ts"
import { Plugin } from "@opencode/plugin"

export default Plugin.define({
  id: "company",
  setup(ctx) {
    const strict = ctx.options.strict === true
  },
})
```

## 变换（Transforms）

变换是对 OpenCode 领域状态的同步编辑，且每一个变换都建立在其所在领域中较早的注册之上。诸如 `ctx.model.list()` 之类的注册表读取会反映迄今为止的每一次注册，包括插件 setup 期间的注册；启动时的批量处理只会合并更新通知，绝不会延迟读取所返回的内容。资源状态 API 仍然报告正在运行的资源的状态：一个定义被注册并不意味着它的连接或其他资源工作已经完成。

数据源通过 `ctx.provider.transform` 贡献 provider 和不可变的模型定义。

```ts title="plugins/models/index.ts"
import { Model, Plugin, Provider } from "@opencode/plugin"

export default Plugin.define({
  id: "company.models",
  async setup(ctx) {
    const providerID = Provider.ID.make("acme")
    const models = [{ ...Model.Info.default(providerID, Model.ID.make("reasoner")), name: "Acme Reasoner" }]
    await ctx.provider.transform((editor) => {
      editor.add({
        info: {
          ...Provider.Info.empty(providerID),
          name: "Acme",
          activation: "enabled",
          package: "@opencode/ai/providers/openai-compatible",
          settings: { baseURL: "http://127.0.0.1:8000/v1" },
        },
        models,
      })
    })

    const available = await ctx.model.list()
  },
})
```

任何注册、移除或 `reload()` 都会将注册表标记为已更改；下一次读取会按注册顺序把所有活跃的变换重放到一个全新的值上来重建它。请保持变换的轻量和可重复性。你已读取过的值永远不会被后续的重建修改。

在 provider 变换和可用性解析完成之后，OpenCode 会实体化活跃 provider 的模型，并按顺序重放每一次模型变换。模型策略可以检查整个候选集合，包括刚刷新的新数据源。

```ts title="plugins/model-budget/index.ts"
import { Plugin } from "@opencode/plugin"

export default Plugin.define({
  id: "company.model-budget",
  async setup(ctx) {
    await ctx.model.transform((editor) => {
      editor
        .list()
        .filter((model) => model.cost.some((tier) => tier.output > 20))
        .forEach((model) => {
          editor.remove(model.providerID, model.id)
        })
    })
  },
})
```

被捕获的输入不会被自动监视。请在同步回调之前加载外部数据，然后在这些输入变化后调用 `reload()`。这里，`loadFromSource()` 返回 `{ info: Provider.Info, models: readonly Model.Info[] }` 形式的条目。

```ts title="plugins/models/index.ts"
import { Plugin } from "@opencode/plugin"

export default Plugin.define({
  id: "company.models",
  async setup(ctx) {
    const source = { providers: await loadFromSource() }

    await ctx.provider.transform((editor) => {
      source.providers.forEach((provider) => editor.add(provider))
    })

    const refresh = async () => {
      source.providers = await loadFromSource()
      await ctx.provider.reload()
    }

    const timer = setInterval(() => void refresh().catch(console.error), 60_000)
    return () => clearInterval(timer)
  },
})
```

provider 的更改会使整个活跃模型结果失效，因此输出价格策略仍会过滤刷新后的模型。当只有被模型变换捕获的输入发生变化时，请使用 `ctx.model.reload()`。

## API

### Agent

读取所有 agent 或按 ID 获取单个 agent。

```ts
const agents = await ctx.agent.list()
const build = await ctx.agent.get({ agentID: "build" })
```

注册一个变换来检查、更新、移除或选择默认 agent。

```ts
await ctx.agent.transform((editor) => {
  const agents = editor.list()
  const build = editor.get("build")

  editor.default("build")
  editor.update("build", (agent) => {
    agent.description = "Builds features and fixes bugs"
  })
  editor.remove("legacy")
})
```

当变换所使用的外部状态发生变化后，重新加载 agent。

```ts
await ctx.agent.reload()
```

#### 参考

Schema：[`Agent.Info`](../../../api/index.md#schema-Agent.Info)

```ts
interface AgentContext {
  list(input?: AgentListInput, requestOptions?: RequestOptions): Promise<AgentListOutput>
  get(input: AgentGetInput, requestOptions?: RequestOptions): Promise<AgentGetOutput>
  transform(callback: (editor: AgentEditor) => void): Promise<Registration>
  reload(): Promise<void>
}

interface AgentEditor {
  list(): readonly AgentInfo[]
  get(id: string): AgentInfo | undefined
  default(id: string | undefined): void
  update(id: string, update: (agent: AgentInfo) => void): void
  remove(id: string): void
}

interface Registration {
  dispose(): Promise<void>
}
```

### Providers

读取可用的 provider 或按 ID 检查某个 provider 的元数据。

```ts
const providers = await ctx.provider.list()
const provider = await ctx.provider.get({ providerID: "anthropic" })
```

provider 变换编辑 provider 的设置和数据源定义。编辑器的读取包括不活跃的 provider，并暴露不可变的定义；`models.update` 编辑的是数据源模型的一个自有副本。

```ts
await ctx.provider.transform((editor) => {
  editor.update("anthropic", (provider) => {
    provider.headers = { ...provider.headers, "x-company": "engineering" }
  })
  editor.models.update("anthropic", "claude-sonnet-5-5", (model) => {
    model.name = "Team Sonnet"
  })
  editor.models.remove("anthropic", "legacy-model")
  editor.remove("legacy-provider")
})
```

使用 `models.set` 替换 provider 的数据源清单，然后在被捕获的定义变化后重载。

```ts
const source = { models: await loadModels() }
await ctx.provider.transform((editor) => {
  editor.models.set("acme", source.models)
})

source.models = await loadModels()
await ctx.provider.reload()
```

对于特定账号的发现，请把用于加载清单的连接作为 `sourceConnection` 传入。当选择了另一个连接时，OpenCode 会排除该 provider，直到你的插件发布其刷新后的清单。

```ts
const connection = await ctx.integration.connection.active("acme")
if (!connection) return
const inventory = await loadInventory(connection)
await ctx.provider.transform((editor) => {
  editor.add({ info: inventory.provider, models: inventory.models, sourceConnection: connection })
})
```

#### 参考

Schema：[`Provider.Info`](../../../api/index.md#schema-Provider.Info)、[`Model.Info`](../../../api/index.md#schema-Model.Info)

```ts
interface ProviderDomain extends ProviderApi {
  transform(callback: (editor: ProviderEditor) => void): Promise<Registration>
  reload(): Promise<void>
}

interface ProviderRecord {
  readonly provider: Provider.Info
  readonly models: ReadonlyMap<string, Model.Info>
  readonly sourceConnection?: ConnectionInfo
}

interface ProviderEditor {
  list(): readonly ProviderRecord[]
  get(providerID: string): ProviderRecord | undefined
  add(input: { info: Provider.Info; models: readonly Model.Info[]; sourceConnection?: ConnectionInfo }): void
  update(providerID: string, update: (provider: DeepMutable<Provider.Info>) => void): void
  remove(providerID: string): void
  readonly models: {
    set(providerID: string, models: readonly Model.Info[]): void
    update(providerID: string, modelID: string, update: (model: DeepMutable<Model.Info>) => void): void
    remove(providerID: string, modelID: string): void
  }
}
```

### 模型

读取可用的模型和默认选择。

```ts
const models = await ctx.model.list()
const selected = await ctx.model.default()
```

模型变换编辑整个活跃 provider 的候选集合。在所有变换完成之前，被禁用的候选仍然可以编辑；`update` 只能在可用的 provider 之下添加模型。

```ts
await ctx.model.transform((editor) => {
  editor.list("anthropic").forEach((model) => {
    editor.update(model.providerID, model.id, (draft) => {
      draft.enabled = draft.capabilities.tools
    })
  })
  editor.default.set("anthropic", "claude-sonnet-5-5")
  editor.remove("anthropic", "legacy-model")
})
```

回调编辑的是原始的模型覆盖值。当 OpenCode 提交结果时，provider 默认值会被合并一次；未发生变化的读取会复用该结果。`editor.provider` 暴露的是不可变的数据源定义（包括不活跃的模板），而不是模型变换的输出。

```ts
await ctx.model.transform((editor) => {
  const source = editor.provider.get("anthropic")?.models.get("claude-sonnet-5-5")
  if (!source) return
  editor.update("anthropic", source.id, (model) => {
    model.limit.context = Math.min(model.limit.context, source.limit.context)
  })
})

await ctx.model.reload()
```

#### 参考

Schema：[`Model.Info`](../../../api/index.md#schema-Model.Info)

```ts
interface ModelDomain extends ModelApi {
  transform(callback: (editor: ModelEditor) => void): Promise<Registration>
  reload(): Promise<void>
}

interface ModelEditor {
  list(providerID?: string): readonly DeepMutable<Model.Info>[]
  get(providerID: string, modelID: string): DeepMutable<Model.Info> | undefined
  update(providerID: string, modelID: string, update: (model: DeepMutable<Model.Info>) => void): void
  remove(providerID: string, modelID: string): void
  readonly default: {
    get(): { providerID: string; modelID: string } | undefined
    set(providerID: string, modelID: string): void
  }
  readonly provider: {
    list(): readonly ProviderRecord[]
    get(providerID: string): ProviderRecord | undefined
  }
}
```

### 命令

读取某个位置可用的命令。

```ts
const commands = await ctx.command.list()
```

通过变换注册命令。执行器会收到会话、提示词附件以及请求的投递模式。

```ts
await ctx.command.transform((editor) => {
  editor.add({
    name: "security-review",
    description: "Review changes for security issues",
    execute: async ({ sessionID, prompt, delivery }) => {
      await ctx.session.prompt({
        ...prompt,
        sessionID,
        text: `Review these changes for security issues.\n\n${prompt.text}`,
        delivery,
      })
    },
  })
})
```

当变换所使用的外部状态发生变化后，重新加载命令。

```ts
await ctx.command.reload()
```

#### 参考

Schema：[`Command.Info`](../../../api/index.md#schema-Command.Info)、[`Session.Inbox.Delivery`](../../../api/index.md#schema-Session.Inbox.Delivery)

```ts
interface CommandContext {
  list(input?: CommandListInput, requestOptions?: RequestOptions): Promise<CommandListOutput>
  transform(callback: (editor: CommandEditor) => void): Promise<Registration>
  reload(): Promise<void>
}

interface CommandEditor {
  add(definition: CommandDefinition): void
}

interface CommandDefinition {
  name: string
  description?: string
  execute(input: CommandInvocation): Promise<void>
}

interface CommandInvocation {
  sessionID: string
  prompt: PromptInput
  delivery: "steer" | "queue"
}
```

### 集成（Integrations）

读取集成并检查活跃的凭据。

```ts
const integrations = await ctx.integration.list()
const github = await ctx.integration.get({ integrationID: "github" })
const connection = await ctx.integration.connection.active("github")
const credential = connection ? await ctx.integration.connection.resolve(connection) : undefined
```

使用 API key 连接集成。

```ts
await ctx.integration.connect.key({
  integrationID: "github",
  key: process.env.GITHUB_TOKEN!,
})
```

启动、检查、完成或取消一次 OAuth 连接尝试。

```ts
const attempt = await ctx.integration.oauth.connect({ integrationID: "github", methodID: "oauth" })
const status = await ctx.integration.oauth.status({ integrationID: "github", attemptID: attempt.data.attemptID })
await ctx.integration.oauth.complete({ integrationID: "github", attemptID: attempt.data.attemptID, code })
await ctx.integration.oauth.cancel({ integrationID: "github", attemptID: attempt.data.attemptID })
```

基于命令的连接暴露相同的启动、状态和取消流程。

```ts
const attempt = await ctx.integration.command.connect({ integrationID: "acme", methodID: "cli" })
const status = await ctx.integration.command.status({ integrationID: "acme", attemptID: attempt.data.attemptID })
await ctx.integration.command.cancel({ integrationID: "acme", attemptID: attempt.data.attemptID })
```

注册一个变换来检查集成并管理它们的认证方法。

```ts
await ctx.integration.transform((editor) => {
  const integrations = editor.list()
  const acme = editor.get("acme")

  editor.update("acme", (integration) => {
    integration.name = "Acme"
  })
  editor.method.update({
    integrationID: "acme",
    method: { id: "cli", type: "command", label: "Sign in with Acme CLI", command: ["acme", "login"] },
  })

  const methods = editor.method.list("acme")
  const legacy = methods.find((method) => method.type === "command" && method.id === "legacy")
  if (legacy) editor.method.remove("acme", legacy)
  editor.remove("legacy")
})
```

当变换所使用的外部状态发生变化后，重新加载集成。

```ts
await ctx.integration.reload()
```

#### 参考

Schema：[`Integration.Info`](../../../api/index.md#schema-Integration.Info)、[`Integration.Method`](../../../api/index.md#schema-Integration.Method)、[`Connection.Info`](../../../api/index.md#schema-Connection.Info)、[`Form.Answer`](../../../api/index.md#schema-Form.Answer)

```ts
interface IntegrationContext {
  list(input?: IntegrationListInput, requestOptions?: RequestOptions): Promise<IntegrationListOutput>
  get(input: IntegrationGetInput, requestOptions?: RequestOptions): Promise<IntegrationGetOutput>
  connect: {
    key(input: IntegrationConnectKeyInput, requestOptions?: RequestOptions): Promise<void>
  }
  oauth: {
    connect(
      input: IntegrationOauthConnectInput,
      requestOptions?: RequestOptions,
    ): Promise<IntegrationOauthConnectOutput>
    status(input: IntegrationOauthStatusInput, requestOptions?: RequestOptions): Promise<IntegrationOauthStatusOutput>
    complete(input: IntegrationOauthCompleteInput, requestOptions?: RequestOptions): Promise<void>
    cancel(input: IntegrationOauthCancelInput, requestOptions?: RequestOptions): Promise<void>
  }
  command: {
    connect(
      input: IntegrationCommandConnectInput,
      requestOptions?: RequestOptions,
    ): Promise<IntegrationCommandConnectOutput>
    status(
      input: IntegrationCommandStatusInput,
      requestOptions?: RequestOptions,
    ): Promise<IntegrationCommandStatusOutput>
    cancel(input: IntegrationCommandCancelInput, requestOptions?: RequestOptions): Promise<void>
  }
  transform(callback: (editor: IntegrationEditor) => void): Promise<Registration>
  reload(): Promise<void>
  connection: {
    active(integrationID: string): Promise<ConnectionInfo | undefined>
    resolve(connection: ConnectionInfo): Promise<CredentialValue | undefined>
  }
}

interface IntegrationEditor {
  list(): readonly IntegrationRef[]
  get(id: string): IntegrationRef | undefined
  update(id: string, update: (integration: IntegrationRef) => void): void
  remove(id: string): void
  method: {
    list(integrationID: string): readonly IntegrationMethod[]
    update(input: IntegrationMethodRegistration): void
    remove(integrationID: string, method: IntegrationMethod): void
  }
}
```

### 凭据

将一个已保存的凭据设为其所属集成的活跃凭据。

```ts
await ctx.credential.activate({ credentialID })
```

#### 参考

```ts
interface CredentialContext {
  activate(input: CredentialActivateInput, requestOptions?: RequestOptions): Promise<void>
}
```

### MCP

列出 MCP 服务器及其当前的连接状态。

```ts
const servers = await ctx.mcp.list()
```

插件只能通过变换来管理 MCP 服务器。使用 `editor.set` 添加或替换服务器，使用 `editor.update` 修改其配置，使用 `editor.remove` 移除它。使用 `editor.list` 和 `editor.get` 检查配置。

```ts
await ctx.mcp.transform((editor) => {
  const servers = editor.list()
  const docs = editor.get("docs")
  editor.set("docs", { type: "remote", url: "https://mcp.example.com" })
  editor.update("docs", (server) => {
    server.disabled = false
  })
  editor.remove("legacy")
})
```

在变换中设置 `disabled: true` 可以禁用服务器并断开其连接，设置 `disabled: false` 则启用它并允许 OpenCode 进行连接。OpenCode 会根据变换后的配置来协调服务器的生命周期。

当变换所使用的外部状态发生变化后，调用 `reload()` 以重新应用变换并协调服务器。

```ts
await ctx.mcp.reload()
```

#### 参考

Schema：[`Mcp.Server`](../../../api/index.md#schema-Mcp.Server)、[`Mcp.LocalConfigEncoded`](../../../api/index.md#schema-Mcp.LocalConfigEncoded)、[`Mcp.RemoteConfigEncoded`](../../../api/index.md#schema-Mcp.RemoteConfigEncoded)

```ts
interface MCPContext {
  list(input?: McpListInput, requestOptions?: RequestOptions): Promise<McpListOutput>
  transform(callback: (editor: MCPEditor) => void): Promise<Registration>
  reload(): Promise<void>
}

interface MCPEditor {
  list(): readonly (readonly [string, McpServerConfig])[]
  get(name: string): McpServerConfig | undefined
  set(name: string, config: McpServerConfig): void
  update(name: string, update: (config: McpServerConfig) => void): void
  remove(name: string): void
}
```

### 插件

列出某个位置当前处于活跃状态的插件。

```ts
const plugins = await ctx.plugin.list()
```

#### 参考

Schema：[`Plugin.Info`](../../../api/index.md#schema-Plugin.Info)、[`Plugin.Source`](../../../api/index.md#schema-Plugin.Source)

```ts
interface PluginContext {
  list(input?: PluginListInput, requestOptions?: RequestOptions): Promise<PluginListOutput>
}
```

### 引用（References）

读取某个位置可用的引用。

```ts
const references = await ctx.reference.list()
```

注册一个变换来检查、添加或移除本地和 Git 引用。`get(name)` 返回当前已配置的数据源，如果该名称不存在则返回 `undefined`。

```ts
await ctx.reference.transform((editor) => {
  const references = editor.list()
  editor.add("handbook", { type: "local", path: "/workspace/docs/handbook" })
  editor.add("standards", { type: "git", repository: "https://github.com/acme/standards", branch: "main" })
  const handbook = editor.get("handbook")
  editor.remove("legacy")
})
```

当变换所使用的外部状态发生变化后，重新加载引用。

```ts
await ctx.reference.reload()
```

#### 参考

Schema：[`Reference.Info`](../../../api/index.md#schema-Reference.Info)、[`Reference.LocalSource`](../../../api/index.md#schema-Reference.LocalSource)、[`Reference.GitSource`](../../../api/index.md#schema-Reference.GitSource)

```ts
interface ReferenceContext {
  list(input?: ReferenceListInput, requestOptions?: RequestOptions): Promise<ReferenceListOutput>
  transform(callback: (editor: ReferenceEditor) => void): Promise<Registration>
  reload(): Promise<void>
}

interface ReferenceEditor {
  list(): readonly (readonly [string, ReferenceLocalSource | ReferenceGitSource])[]
  get(name: string): ReferenceLocalSource | ReferenceGitSource | undefined
  add(name: string, source: ReferenceLocalSource | ReferenceGitSource): void
  remove(name: string): void
}
```

### 生成（实验性）

使用选定的模型进行生成，而不创建会话、调用工具或写入会话历史。这些 API 可能会变化。`ctx.generate.text` 仍然可用，但已被弃用，推荐使用 `ctx.experimental.generate.text`。

```ts
const review = await ctx.experimental.generate.text({
  model: { providerID: "anthropic", id: "claude-sonnet-5-5" },
  prompt: "Review this proposed action.",
})

const { images } = await ctx.experimental.generate.image({
  model: { providerID: "openai", id: "gpt-image-1-mini" },
  prompt: "A watercolor fox in the snow",
  aspect: "16:9",
})

const { answers } = await ctx.experimental.generate.decisions({
  model: { providerID: "opencode", id: "jev-1.13" },
  input: [{ type: "text", text: "I was charged twice, please refund one." }],
  questions: [{ type: "predicate", name: "refund", instructions: "Is this a refund request?" }],
})
```

### 权限

在执行操作之前请求权限。`assert` 会评估会话的[权限规则](../../../permissions/index.md)（包括已保存的批准记录），并在某条规则的结果为 `ask` 时向用户发出提示。一旦操作被允许，它就会完成解析。

```ts
execute: async (input, context) => {
  await ctx.permission.assert({
    sessionID: context.sessionID,
    agent: context.agent,
    source: { type: "tool", messageID: context.messageID, id: context.id },
    action: "deploy",
    resources: [input.environment],
    save: [input.environment],
  })
  return { content: await deploy(input.environment) }
}
```

- `action` 和 `resources` 会与规则进行匹配。任何 `deny` 都会阻止该操作；否则任何 `ask` 都会发出提示。
- `save` 列出当用户选择始终允许时要存储的模式。
- `agent` 选择适用谁的规则，默认为会话的 agent。`source` 将提示关联到一次工具调用。
- `metadata` 向权限提示和 `evaluate` 钩子传递额外的细节。

deny 规则或带有反馈的拒绝会以携带原因的 `Tool.Error` 进行拒绝，以便模型看到原因并继续执行。单纯的拒绝会结束当前步骤。让这些错误向上传播，而不是把它们作为工具输出返回。

检查或解决待处理的权限请求。

```ts
const pending = await ctx.permission.list({ sessionID })
const request = await ctx.permission.get({ sessionID, requestID })
await ctx.permission.reply({ sessionID, requestID, decision: "once" })
```

替换会话级别的权限规则。它们会在 agent 的规则之后被评估，最后匹配的规则胜出。子会话在创建时会继承当时生效的规则。

```ts
await ctx.session.update({
  sessionID,
  permissions: [{ action: "edit", resource: "/path/to/original/checkout/**", effect: "deny" }],
})
```

### 会话

创建或读取会话。

```ts
const created = await ctx.session.create({ title: "Review" })
const session = await ctx.session.get({ sessionID })
const messages = await ctx.session.context({ sessionID })
```

分页列出会话。要获取下一页，请把 `cursor.next` 作为 `cursor` 传回。游标会记住你的筛选条件，因此无需重复传入。

```ts
const page = await ctx.session.list({ directory: ctx.location.directory, limit: 20 })
const next = page.cursor.next ? await ctx.session.list({ cursor: page.cursor.next, limit: 20 }) : undefined
```

更改后续请求使用的 agent 或模型。

```ts
await ctx.session.switchAgent({ sessionID, agent: "build" })
await ctx.session.switchModel({ sessionID, model: { providerID: "anthropic", id: "claude-sonnet-5-5" } })
```

发送用户提示、临时生成请求、命令或合成消息。

```ts
const prompt = await ctx.session.prompt({ sessionID, text: "Review the current changes" })
const generated = await ctx.session.generate({ sessionID, prompt: "Summarize this project" })
await ctx.session.command({ sessionID, name: "review", text: "--staged" })
const synthetic = await ctx.session.synthetic({ sessionID, text: "Deployment completed" })
```

`generate` 返回 `text` 以及该次调用的 `tokens` 和 `cost`，其格式与助手消息上报它们时使用的形状相同。

重命名、中断或等待会话。

```ts
await ctx.session.update({ sessionID, title: "Review" })
await ctx.session.interrupt({ sessionID, resume: false })
await ctx.session.wait({ sessionID })
```

使用 `remove` 移除临时会话。移除会停止正在进行的执行，并递归删除其子会话。

```ts
await ctx.session.remove({ sessionID })
```

使用 `compact` 请求压缩。它返回的是被接收的收件箱条目，而不是已完成的摘要；压缩默认在下一个步骤边界运行。若要保持队列顺序，请传入 `delivery: "queue"`。

```ts
const compaction = await ctx.session.compact({ sessionID })
```

使用 `instructions.entry` 附加、列出或移除带键的会话指令条目。条目以 `<context key="...">` 块的形式呈现在会话的指令中，更新或移除会在下一个步骤边界宣布，而不会排队一条消息回合。

```ts
await ctx.session.instructions.entry.put({ sessionID, key: "deploy-target", value: "production" })
const entries = await ctx.session.instructions.entry.list({ sessionID })
await ctx.session.instructions.entry.remove({ sessionID, key: "deploy-target" })
```

#### 参考

Schema：[`Session.Info`](../../../api/index.md#schema-Session.Info)、[`Model.Ref`](../../../api/index.md#schema-Model.Ref)、[`Session.Inbox.User`](../../../api/index.md#schema-Session.Inbox.User)、[`Session.Inbox.Synthetic`](../../../api/index.md#schema-Session.Inbox.Synthetic)、[`InstructionEntry.Info`](../../../api/index.md#schema-InstructionEntry.Info)

```ts
interface SessionContext {
  create(input?: SessionCreateInput, requestOptions?: RequestOptions): Promise<SessionInfo>
  get(input: SessionGetInput, requestOptions?: RequestOptions): Promise<SessionInfo>
  remove(input: SessionRemoveInput, requestOptions?: RequestOptions): Promise<void>
  context(input: SessionContextInput, requestOptions?: RequestOptions): Promise<readonly SessionMessageInfo[]>
  instructions: {
    entry: {
      list(
        input: ExperimentalSessionInstructionsEntryListInput,
        requestOptions?: RequestOptions,
      ): Promise<readonly InstructionEntryInfo[]>
      put(input: ExperimentalSessionInstructionsEntryPutInput, requestOptions?: RequestOptions): Promise<void>
      remove(input: ExperimentalSessionInstructionsEntryRemoveInput, requestOptions?: RequestOptions): Promise<void>
    }
  }
  switchAgent(input: SessionSwitchAgentInput, requestOptions?: RequestOptions): Promise<void>
  switchModel(input: SessionSwitchModelInput, requestOptions?: RequestOptions): Promise<void>
  update(input: SessionUpdateInput, requestOptions?: RequestOptions): Promise<void>
  move(input: SessionMoveInput, requestOptions?: RequestOptions): Promise<void>
  prompt(input: SessionPromptInput, requestOptions?: RequestOptions): Promise<SessionInboxUser>
  generate(input: SessionGenerateInput, requestOptions?: RequestOptions): Promise<{ text: string }>
  command(input: SessionCommandInput, requestOptions?: RequestOptions): Promise<void>
  compact(input: SessionCompactInput, requestOptions?: RequestOptions): Promise<SessionInboxCompaction>
  synthetic(input: SessionSyntheticInput, requestOptions?: RequestOptions): Promise<SessionInboxSynthetic>
  interrupt(input: SessionInterruptInput, requestOptions?: RequestOptions): Promise<{ interrupted: boolean }>
  wait(input: ExperimentalSessionWaitInput, requestOptions?: RequestOptions): Promise<void>
}
```

### 技能（Skills）

读取某个位置可用的技能。

```ts
const skills = await ctx.skill.list()
```

注册一个变换来检查、添加、更新或移除技能。`get(id)` 返回当前编辑器中的条目，如果该技能不存在则返回 `undefined`。

```ts
import { Skill } from "@opencode/plugin"

await ctx.skill.transform((editor) => {
  const skills = editor.list()
  editor.add({
    id: Skill.ID.make("review"),
    name: Skill.Name.make("Review"),
    description: "Review the current changes",
    path: Skill.Info.fields.path.make("/workspace/.opencode/skills/review/SKILL.md"),
    content: "Review the current changes for correctness and missing tests.",
  })
  const review = editor.get("review")
  editor.update("review", (skill) => {
    skill.autoinvoke = true
  })
  editor.remove("legacy")
})
```

当变换所使用的外部状态发生变化后，重新加载技能。

```ts
await ctx.skill.reload()
```

#### 参考

Schema：[`Skill.Info`](../../../api/index.md#schema-Skill.Info)

```ts
interface SkillContext {
  list(input?: SkillListInput, requestOptions?: RequestOptions): Promise<SkillListOutput>
  transform(callback: (editor: SkillEditor) => void): Promise<Registration>
  reload(): Promise<void>
}

interface SkillEditor {
  list(): readonly SkillInfo[]
  get(id: string): SkillInfo | undefined
  add(skill: SkillInfo): void
  update(id: string, update: (skill: SkillInfo) => void): void
  remove(id: string): void
}
```

### 存储

存储、读取或移除以插件为作用域的持久化 JSON 值。

```ts
await ctx.storage.set("settings", { strict: true })
const settings = await ctx.storage.get("settings")
await ctx.storage.remove("settings")
```

按前缀扫描键，支持可选的游标分页。

```ts
const page = await ctx.storage.scan({ prefix: "cache/", limit: 100 })
const next = page.next
```

#### 参考

```ts
interface StorageContext {
  get(key: string): Promise<Json | undefined>
  set(key: string, value: Json): Promise<void>
  remove(key: string): Promise<void>
  scan(options: StorageScanOptions): Promise<StorageScanResult>
}

interface StorageScanOptions {
  prefix: string
  after?: string
  limit?: number
}

interface StorageScanResult {
  entries: readonly { key: string; value: Json }[]
  next?: string
}
```

### 工具

在所有变换完成之后、在变换回调之外，读取当前已注册的工具。每个工具都有一个包含其生效名称的 `id`。

```ts
const tools = await ctx.tool.list()
const read = tools.find((tool) => tool.id === "read")
```

使用同步变换注册、更新和移除工具，Promise 插件中也同样适用。请在注册或重载之前加载外部数据。后面一个有效的注册会覆盖相同的生效工具名称。

```ts
const registration = await ctx.tool.transform((editor) => {
  editor.namespace({
    name: "acme",
    description: "Customer account tools",
  })
  editor.add({
    name: "greeting",
    description: "Create a greeting",
    input: {
      type: "object",
      properties: { name: { type: "string" } },
      required: ["name"],
      additionalProperties: false,
    },
    options: { namespace: "acme", codemode: true },
    execute: async (input, context) => {
      await context.progress({ status: "greeting" })
      return { content: `Hello ${(input as { name: string }).name}!` }
    },
  })
})
```

Promise 工具执行器会收到 `context.signal`。请把它传递给可取消的工作，例如 `fetch`，这样停止会话时也会停止底层操作。

```ts
execute: async ({ url }, context) => {
  const response = await fetch(url, { signal: context.signal })
  return { content: await response.text() }
}
```

#### 自由格式工具输入

当一个直接工具恰好只有一个必填的字符串字段时，可以让模型在没有 JSON 包装的情况下直接写入该字符串。将 `freeform` 设置为 `{ type: "text" }`、`{ type: "regex", pattern }` 或 `{ type: "lark", grammar }`。

```ts
editor.add({
  name: "ticket",
  description: "Look up a ticket by ID",
  options: { codemode: false },
  input: Schema.Struct({ id: Schema.String }),
  freeform: { type: "regex", pattern: "OPS-[0-9]+" },
  execute: async ({ id }) => ({ content: await lookup(id) }),
})
```

如果所选模型的 API 在 models.dev 上列出了 `regex`，模型就可以直接写入 `OPS-42`。否则 Core 只会省略 `freeform`：模型仍然拥有 `ticket` 工具，并以 `{"id":"OPS-42"}` 的形式调用它。缺失或为空的格式列表表示不支持自由格式。无论哪种情况，执行器都会收到 `{ id }`。

在 Code Mode（`codemode: true`）中，自由格式工具直接接收其字符串，例如 `await tools.ticket("OPS-42")`。`await tools.ticket({ id: "OPS-42" })` 同样有效。

在回调所捕获的数据源发生变化后，调用 `reload()`。重载会以原有顺序重放活跃的变换；它不会重新运行插件的 setup。

```ts
await ctx.tool.reload()
```

使用 `list()` 和 `get()` 检查编辑器中当前的工具。工具有一个包含其生效名称的 `id`，当该 ID 不存在时 `get()` 返回 `undefined`。使用 `update` 和 `remove` 时要传入生效的工具名称，包括其命名空间（即上面的 `acme_greeting`）。命名空间中的点号和工具名称中不受支持的字符会变成 `_`。缺失的名称会被忽略；创建工具需要通过 `add` 传入完整的定义。更新会保留名称和命名空间。要替换 schema 或选项，请直接赋新的值，而不是修改嵌套值。无效的更新会被记录日志，并保持原有定义不变。

```ts
await ctx.tool.transform((editor) => {
  editor.update("acme_greeting", (tool) => {
    tool.description = "Greet the user by name"
  })
  editor.remove("acme_obsolete")
})
```

更新和移除会与添加一起按顺序重放，包括在 MCP 目录刷新之后。销毁它们的注册会移除这些更改，并从剩余的变换中重建。

销毁一个注册可以移除其变换并从剩余的变换中重建，从而显露它先前覆盖的任何更早的定义。销毁是幂等的，卸载插件同样会销毁其注册。

```ts
await registration.dispose()
```

每次模型请求都会捕获一个稳定、可执行的工具快照。后续的变换、重载和销毁影响的是未来的快照，而不是已被捕获的定义、Code Mode 命名空间描述或执行器。闭包引用了可变插件数据的执行器仍然会观察到该数据的变化；如果某个值必须始终与该定义绑定，请在变换内部捕获它。

#### 参考

Schema：[`Tool.Content`](../../../api/index.md#schema-Tool.Content)、[`Tool.TextContent`](../../../api/index.md#schema-Tool.TextContent)、[`Tool.FileContent`](../../../api/index.md#schema-Tool.FileContent)

```ts
interface ToolContext {
  list(): Promise<readonly (ToolInfo & { readonly id: string })[]>
  transform(callback: (editor: ToolEditor) => void): Promise<Registration>
  reload(): Promise<void>
}

interface ToolEditor {
  list(): readonly (ToolInfo & { readonly id: string })[]
  get(id: string): (ToolInfo & { readonly id: string }) | undefined
  namespace(namespace: { name: string; description: string }): void
  add(tool: ToolInfo): void
  update(id: string, update: (tool: Types.Mutable<ToolInfo>) => void): void
  remove(id: string): void
}
```

### VCS

读取仓库信息、工作副本状态或文件差异。

```ts
const info = await ctx.vcs.get()
const branches = await ctx.vcs.branch.list({ search: "feature", limit: 10 })
const changes = await ctx.vcs.status()
const diff = await ctx.vcs.diff({ mode: "working", context: 3 })
```

通过变换注册一个位置作用域的 VCS provider。与检测到的仓库类型匹配的 provider 会被自动选中；使用 `editor.default.set` 可以选择其他 provider。

```ts
await ctx.vcs.transform((editor) => {
  editor.add({
    id: "custom",
    name: "Custom VCS",
    info: async () => ({ branch: { current: "feature", default: "main" } }),
    branches: async (input, { signal }) => readBranches(input, signal),
    status: async (scope, { signal }) => readStatus(scope.worktree, signal),
    diff: async (input, { signal }) => readDiff(input, signal),
  })
  editor.default.set("custom")
})
```

provider 的回调会收到当前的位置、工作副本根目录、规范的项目根目录以及可选的仓库存储。差异回调还会收到选定的模式、请求的上下文以及输出字节预算。仓库发现仍然使用 OpenCode 内置的 Git 和 Mercurial 检测器。

provider 可以选择性地实现 `init(scope, { signal })`，在 `scope.worktree` 中创建仓库。初始化是按 ID 选择 provider（默认为 Git），而不是按检测到的仓库类型。即使位置中还没有仓库，也要注册带有 `init` 的 provider；OpenCode 会在调用它之前检查该目录存在且没有仓库，然后重新发现项目。新的仓库格式仍然需要此回调之外的发现支持。

#### 参考

Schema：[`Vcs.Info`](../../../api/index.md#schema-Vcs.Info)、[`Vcs.FileStatus`](../../../api/index.md#schema-Vcs.FileStatus)、[`FileDiff.Info`](../../../api/index.md#schema-FileDiff.Info)

```ts
interface VcsContext {
  get(input?: VcsGetInput, requestOptions?: RequestOptions): Promise<VcsGetOutput>
  branch: {
    list(input?: VcsBranchListInput, requestOptions?: RequestOptions): Promise<VcsBranchListOutput>
  }
  status(input?: VcsStatusInput, requestOptions?: RequestOptions): Promise<VcsStatusOutput>
  diff(input: VcsDiffInput, requestOptions?: RequestOptions): Promise<VcsDiffOutput>
  transform(callback: (editor: VcsEditor) => void): Promise<Registration>
  reload(): Promise<void>
}

interface VcsEditor {
  add(definition: VcsDefinition): void
  default: {
    get(): string | undefined
    set(providerID: string): void
  }
}

interface VcsDefinition {
  init?(scope: VcsScope, context: { signal: AbortSignal }): Promise<void>
  // Existing info, branches, status, and diff callbacks are required.
}
```

### Worktree

使用正常的插件生命周期注册本地 worktree 策略。本例中的实现模块负责选项验证以及后端的 `create`、`remove` 和 `list` 操作。

```ts title="plugins/worktrees/index.ts"
import { Plugin } from "@opencode/plugin"
import { makeStrategy } from "./strategy"

export default Plugin.define({
  id: "company.worktrees",
  async setup(ctx) {
    const strategy = makeStrategy(ctx.options)
    await ctx.worktree.transform((editor) => {
      editor.add(strategy)
    })
  },
})
```

通过 `plugins` 加载插件，并单独配置公共目标目录：

```jsonc title="opencode.jsonc"
{
  "worktree": { "directory": "../worktrees" },
  "plugins": [{ "package": "./plugins/worktrees", "options": {} }],
}
```

- 添加一个策略会自动选中它。最后活跃的注册胜出；无需任何策略选择配置。
- 销毁其注册或卸载插件会恢复之前的实现，最终恢复为内置的 Git 策略。
- `reload()` 会在被捕获的输入变化后重放变换；它不会重新运行插件的 setup。
- 创建失败不会通过 Git 重试。即使默认策略发生变化，现有的 worktree 也会保留其记录的所有者。
- 策略管理的是本地目录。远程工作区的供给不属于这个接口的一部分。

#### 操作

插件上下文暴露与客户端相同的基于项目的 worktree 操作。每个操作都需要一个 `projectID`。`list` 只读取已保存的清单，包括同一项目已知的检出；它不会加载配置、启动插件或发现文件系统变化。

```ts
const projectID = ctx.location.project.id
const created = await ctx.worktree.create({ projectID, name: "task" })
const inventory = await ctx.worktree.list({ projectID })
await ctx.worktree.refresh({ projectID })
await ctx.worktree.remove({ projectID, directory: created.directory, force: false })
```

create 会从项目已保存的 `canonical` 目录加载配置和插件，并使用它们选中的策略。它接受可选的父 `directory`、来源 `from`、起始 `branch` 和 `name`。来源默认为规范检出，`from` 覆盖必须属于该项目。选择来源不会改变配置根目录。所提供的起始 ref 必须被选中的策略支持；例如，Rift 的原生快照操作没有 ref 选择选项。

create 和 refresh 会等待规范检出的插件激活。在该检出的插件 setup 期间发起的调用能看到迄今为止的注册，并且不会等待它们自身的激活。

remove 会加载规范配置并激活其插件，然后使用 worktree 记录的策略，而不是当前选中的默认策略。记录的所有者不可用会产生错误。worktree 的目标位置可以位于其他地方：

```ts
await ctx.worktree.remove({
  directory: "/worktrees/task",
  projectID,
  force: false,
})
```

缺少所有者会导致移除失败，而不是回退到 Git。策略可以抛出 `new Worktree.OperationError({ message: "Uncommitted changes", forceRequired: true })`（从 `@opencode/plugin` 导入 `Worktree`），以便在不依赖 Core 或 Git 错误的情况下请求强制确认。

refresh 会加载规范配置，并要求所有可用的策略在已知的检出根目录下查找 worktree。它会合并结果、保留已记录的所有权，并清除缺失的目录。某个发现源失败会被记录日志，而其他源继续运行。即使没有可用的策略报告某个目录，已存在的目录也会保持已保存状态。监听 `worktree.updated` 并再次调用 `list` 以读取变化后的清单。

```ts
await ctx.worktree.refresh({ projectID })
```

#### 参考

实现方会在命名和冲突处理之后收到一个建议的目标目录。请从 `create` 返回实际的目录；当后端需要自己的布局时，它可能有所不同。OpenCode 会解析返回的路径，并将其用于清单、启动命令和 API 结果。返回的目录必须存在。

选择其他目标位置的策略需自行处理那里的命名冲突。OpenCode 在调用策略之前仍然会创建建议的父目录。`list` 必须只报告该策略拥有的目录，以及任何仓库根目录。

```ts
interface WorktreeDefinition {
  readonly id: string
  create(
    input: { sourceDirectory: string; directory: string; branch?: string },
    context: { signal: AbortSignal },
  ): Promise<{ directory: string }>
  remove(input: { directory: string; force: boolean }, context: { signal: AbortSignal }): Promise<void>
  list(
    sourceDirectory: string,
    context: { signal: AbortSignal },
  ): Promise<readonly { directory: string; type: "root" | "worktree" }[]>
}

interface WorktreeEditor {
  add(definition: WorktreeDefinition): void
}

interface WorktreeDomain extends WorktreeApi {
  transform(callback: (editor: WorktreeEditor) => void): Promise<Registration>
  reload(): Promise<void>
}
```

Promise 回调必须配合 `signal` 的取消。Effect 回调返回 Effects，并改用 Effect 中断。注册保持限定在插件运行时之内；项目操作使用规范检出的注册表。Core 配置适配器将目录设置输入到该注册表。

### 网页搜索（Websearch）

列出网页搜索 provider 或通过选定的 provider 运行查询。

```ts
const providers = await ctx.websearch.providers()
const results = await ctx.websearch.query({ query: "OpenCode plugins", providerID: "internal" })
```

通过变换注册一个 provider 并选择默认 provider。

```ts
await ctx.websearch.transform((editor) => {
  editor.add({
    id: "internal",
    name: "Internal search",
    execute: async ({ query }, { signal }) => {
      const response = await fetch(`https://search.example.com?q=${encodeURIComponent(query)}`, { signal })
      const result = (await response.json()) as { url: string; title: string; content: string }
      return [{ url: result.url, title: result.title, content: result.content, time: {} }]
    },
  })
  editor.default.set("internal")
})
```

选择 `false` 可以禁用网页搜索；在外部状态变化后重新加载 provider。

```ts
await ctx.websearch.transform((editor) => editor.default.set(false))
await ctx.websearch.reload()
```

#### 参考

Schema：[`WebSearch.Provider`](../../../api/index.md#schema-WebSearch.Provider)、[`WebSearch.Result`](../../../api/index.md#schema-WebSearch.Result)

```ts
interface WebSearchContext {
  providers(input?: WebsearchProvidersInput, requestOptions?: RequestOptions): Promise<WebsearchProvidersOutput>
  query(input: WebsearchQueryInput, requestOptions?: RequestOptions): Promise<WebsearchQueryOutput>
  transform(callback: (editor: WebSearchEditor) => void): Promise<Registration>
  reload(): Promise<void>
}

interface WebSearchEditor {
  add(provider: WebSearchDefinition): void
  default: {
    get(): string | false | undefined
    set(providerID: string | false): void
  }
}
```

### 事件

订阅所连接服务器的公共事件流。在插件清理时中止该流。传入 `types`，例如 `ctx.event.subscribe({ types: ["config.updated"] })`，可以只接收那些事件类型；事件会按此进行类型化。插件运行在服务器内部，因此与 SDK 客户端不同，它们永远不会收到 `server.connected`。未知类型名称会被忽略，并在服务器日志中记录一条警告。

```ts
const controller = new AbortController()
void (async () => {
  for await (const event of ctx.event.subscribe({ signal: controller.signal })) {
    console.log(event.type)
  }
})()
return () => controller.abort()
```

#### 参考

Schema：[`V2EventEncoded`](../../../api/index.md#schema-V2EventEncoded)

```ts
type EventType = Exclude<OpenCodeEvent["type"], "server.connected">

interface EventContext {
  subscribe<Type extends EventType = EventType>(options?: {
    types?: Type[]
    signal?: AbortSignal
  }): AsyncIterable<Extract<OpenCodeEvent, { type: Type }>>
}
```

## 钩子（Hooks）

钩子拦截运行中的操作。在其所属领域上注册钩子，并在不再需要时销毁返回的注册。

```ts
const registration = await ctx.session.hook("context", () => {})
await registration.dispose()
```

多个插件可以注册同一个钩子。OpenCode 按插件顺序运行它们，因此后面的钩子可以看到前面的钩子所做的更改。

### 会话

会话钩子拦截提示接收、模型调用、原生 HTTP 和重试。

#### Forks

`fork` 钩子在 OpenCode 复制历史之后、fork 调用返回之前运行。`sessionID` 标识新会话。

```ts
await ctx.session.hook("fork", ({ sessionID }) => console.log(sessionID))
```

#### 提示接收

在附件和技能解析以及持久化收件箱接收之前，拦截传入的用户提示：

```ts
await ctx.session.hook("prompt", (event) => {
  event.prompt.text = event.prompt.text.replaceAll("company-secret", "[redacted]")
  event.prompt.files ??= []
  event.prompt.files.push({ uri: "file:///project/policy.md" })
  event.metadata = { ...event.metadata, source: "company-policy" }
  event.delivery = "queue"
})
```

钩子收到的是一个自有、可变的草稿：

- `prompt` 包含 `text`、`files`、`agents` 中的 agent 提及，以及选定的 `skills`。
- `metadata` 包含应用定义的接收元数据。
- `delivery` 默认为 `"steer"`，可以改为 `"queue"`。
- 会话和消息 ID 是只读的；钩子无法重定向接收。

钩子添加的文件和技能遵循正常的解析和验证路径。在重写文本时，请更新或移除不再匹配的附件 `mention` 偏移量。agent 提及不会切换会话的活跃 agent。

提示钩子在以下条件下运行：

- 钩子在会话的位置插件就绪后按注册顺序运行。
- 通过 `session.prompt` 提交的命令会运行该钩子。
- 合成消息、shell 消息、压缩控制和移动控制不会。
- 该钩子在接收期间运行一次，而不是在每次模型调用之前。
- provider 作用域不可用，因为模型解析发生在接收之后。

编辑结果会成为持久化的规范用户输入。如果准备失败或被中断，OpenCode 不会接收该提示。

请保持提示钩子可安全重试。它们不是一个精确一次（exactly-once）的副作用边界：

- 重试一个已处于待处理或已投递状态的 ID 会返回原始的接收结果，而不会重新运行钩子。
- 并发提交可能多次运行钩子，但只有第一次成功的接收生效。
- 提示钩子转换输入，不提供类型化的拒绝 API。

#### 模型请求

在模型分发之前立即修改组装好的系统指令、消息、工具或请求选项。会话发出的每种请求都有各自的钩子，因此插件可以对 agent 循环和辅助请求采取不同的处理：

- `context` 针对 agent 循环运行，包括由工具驱动的续接。
- `compaction` 针对检查点摘要运行。`messages` 是正在被摘要的对话记录；OpenCode 在钩子运行之后附加其摘要提示。设置 `result` 可以自己记录压缩并跳过模型调用；它接受与已完成的压缩消息相同的字段。
- `generate` 针对临时的 `ctx.session.generate` 调用运行。
- `title` 针对标题生成运行。它没有 `agent` 或 `tools`。设置 `result` 可以自己提供标题。

```ts
await ctx.session.hook("context", (event) => {
  event.system.push({ type: "text", text: "Keep the review focused on correctness." })
  delete event.tools.write
  event.options.temperature = 0.2
  event.options.maxTokens = 8_000
})

await ctx.session.hook("compaction", async (event) => {
  event.result = { summary: await summarize(event.messages) }
})
```

这些更改只影响即将发出的模型调用，不影响持久化的历史或配置。一个应当适用于每种请求的钩子必须为每种类型分别注册。

`context`、`compaction` 和 `generate` 钩子中的消息带有其存储消息的 `metadata`，为只读（例如，某个 `prompt` 钩子设置的内容）。它不会发送给模型。

承载 OpenCode 指令的 `system` 部分还会在 `metadata.experimental.instructions` 中将每个来源列为 `{ key, text }`，例如 `core/date` 或 `core/environment`，这样钩子就能区分这些来源。该列表是一个副本：编辑该部分的 `text` 不会更新它。这是实验性功能，可能会变化。

请求覆盖遵循以下规则：

- `options` 在每次模型调用时初始为空；它不包含已解析的模型设置。
- 有类型的键是生成设置；任何其他键都会作为 provider 选项传递给选定的协议。
- 钩子按注册顺序运行，后面的钩子可以看到前面钩子所做的覆盖。
- 请求覆盖的优先级高于模型默认值，模型默认值又高于路由默认值。
- provider 选项对象递归合并；数组和标量值会替换较早的值。
- 删除一个覆盖或将其设为 `undefined` 会回退到已配置的默认值，而不是移除它们。
- 原始 HTTP 主体覆盖在协议降级之后应用，可以覆盖由此产生的字段。

#### Provider 选项

provider 选项使用所选协议的语义化选项名称，而不是原始的 HTTP 主体字段。请将特定于 provider 的设置限定到匹配的 provider。例如，OpenAI Responses 使用 `reasoningEffort`：

```ts
await ctx.session.hook(
  "context",
  (event) => {
    event.options.reasoningEffort = "high"
  },
  { providerID: "openai" },
)
```

生成选项取决于所选的协议和模型：

- `maxTokens` 是语义化的输出 token 上限。
- Gemini 支持 `topK`；OpenAI Responses 不暴露它。

#### 模型解析

实验性。每当会话为某个请求解析模型时运行，在此之前不会为该请求构建任何内容。`model` 初始为选定的模型；可以更改它，让该请求由同一 provider 的另一个模型（包括从模型选择器中隐藏的模型）来服务。会话保留其选定的模型；请求和助手消息使用新的模型。`kind` 说明当前正在解析哪种请求，因此路由器可以跳过标题请求，或在压缩之后重新路由。来自其他 provider 的模型会因不可用而失败。

```ts
await ctx.session.hook(
  "experimental.model.resolve",
  (event) => {
    if (event.model.id === "auto" && event.kind !== "title")
      event.model = { providerID: event.model.providerID, id: pick(event.sessionID) }
  },
  { providerID: "acme" },
)
```

#### 模型请求（HTTP 层）

修改模型请求设置，并可选择将钩子限定到某一个 provider。该事件携带与下文 HTTP 钩子相同的 `kind`。

```ts
await ctx.session.hook(
  "model.request",
  (event) => {
    event.headers["x-plugin"] = "review"
  },
  { providerID: "anthropic" },
)
```

#### 原生 HTTP

修改原生的 provider 请求或响应。它们的主体是一次性流；在读取之前请克隆或替换主体。

两个钩子对会话发出的每个请求都会运行。`event.kind` 说明是哪个流程发出的：`"primary"` 表示 agent 循环，`"compaction"` 表示检查点摘要，`"title"` 表示标题生成，`"generate"` 表示临时的 `ctx.session.generate` 调用。请使用它而不是 agent ID 来区分辅助请求。

```ts
await ctx.session.hook("http.request", (event) => {
  event.request.headers.set("x-session-id", event.sessionID)
  if (event.kind === "title") event.request.headers.set("x-priority", "background")
})

await ctx.session.hook("http.response", (event) => {
  event.response = new Response(event.response.body, {
    status: event.response.status,
    headers: { ...Object.fromEntries(event.response.headers), "x-plugin": "review" },
  })
})
```

#### 原生 WebSocket（实验性）

通过 WebSocket 流式传输的 provider 会为每个会话打开一个连接并在多个请求之间复用，因此 `http.request` 和 `http.response` 永远看不到那些流量。`experimental.ws.handshake` 钩子在每个模型调用时、在连接被选定之前运行一次。它携带与 HTTP 钩子相同的 `sessionID`、`agent`、`model` 和 `kind`，外加连接的 `url` 和 `headers`。更改 `url` 或 `headers` 会更改请求使用的套接字，因此轮换的 bearer token 会重新打开连接。

HTTP 钩子仍然会对每个 HTTP 请求运行，包括 WebSocket 路由回退到的请求。

```ts
await ctx.session.hook(
  "experimental.ws.handshake",
  async (event) => {
    event.headers.authorization = `Bearer ${await mintToken(event.url)}`
    delete event.headers["api-key"]
  },
  { providerID: "azure" },
)
```

`experimental.ws.send` 和 `experimental.ws.receive` 暴露帧本身，相当于编辑 HTTP 请求或响应主体的 WebSocket 对应物。`send` 在 provider 驱动构建出站帧之后、写入之前运行；`receive` 在每个入站帧被驱动观察到之前运行。两者都把帧作为字符串携带，并在钩子返回时发送 `frame` 所持有的内容。

OpenCode 不会验证重写后的帧。驱动会根据 provider 的回复跟踪状态，因此改变协议含义的重写由插件负责，与重写 HTTP 主体一样。

```ts
await ctx.session.hook(
  "experimental.ws.send",
  (event) => {
    const body = JSON.parse(event.frame)
    if (body.type === "response.create") body.metadata = { ...body.metadata, session: event.sessionID }
    event.frame = JSON.stringify(body)
  },
  { providerID: "openai" },
)

await ctx.session.hook("experimental.ws.receive", (event) => {
  if (event.frame.includes('"type":"error"')) console.error(event.frame)
})
```

这些钩子是实验性的，其名称或形态可能变化。

#### 重试策略

覆盖 provider 失败的重试决定，或替换其以毫秒为单位的延迟。该钩子在 OpenCode 对失败进行分类并提出其策略之后、在任何重试被调度之前运行。它不暴露 OpenCode 内部如何执行下一次尝试。

```ts
await ctx.session.hook("retry", (event) => {
  if (event.error.status === 429) {
    event.decision = { retry: true, delay: 10_000 }
    return
  }
  if (event.error.type === "provider.invalid-request" && event.attempt === 2) {
    event.decision = { retry: true, delay: 0 }
    return
  }
  if (event.attempt >= 3) event.decision = { retry: false }
})
```

重试钩子可以通过让一个终态失败变得可重试，或者否决一个提议的重试，来修改 OpenCode 的初始 `decision`。

重试决定遵循以下规则：

- 多个钩子按注册顺序运行，后面的钩子能看到当前的决定。
- 内置的最大尝试次数仍然是硬性限制。
- `attempt` 是当前考虑的物理尝试次数。初始请求为 `1`，因此第一次重试是 `2`。
- 无效的延迟（例如 `NaN`、无穷大或负值）会回退到计算出的延迟。
- 上下文溢出的恢复是独立的，因为它压缩对话而不是重试同一请求。

#### 会话参考

```ts
import type { SessionPrompt } from "@opencode/plugin/promise/session"

interface SessionHooks {
  prompt: SessionPrompt
  context: SessionContextHook
  compaction: SessionContextHook & { result?: SessionCompactionResult }
  generate: SessionContextHook
  title: SessionRequestHook & { result?: string }
  "experimental.model.resolve": SessionModelResolveHook
  "model.request": SessionModelRequestHook
  "http.request": SessionHttpRequestHook
  "http.response": SessionHttpResponseHook
  "experimental.ws.handshake": SessionWebSocketHandshakeHook
  "experimental.ws.send": SessionWebSocketSendHook
  "experimental.ws.receive": SessionWebSocketReceiveHook
  retry: SessionRetryHook
}

interface SessionModelResolveHook {
  readonly sessionID: string
  readonly agent: string
  readonly kind: "primary" | "compaction" | "title" | "generate"
  model: { providerID: string; id: string; variant?: string }
}

interface SessionWebSocketHandshakeHook {
  readonly sessionID: string
  readonly agent: string
  readonly model: { providerID: string; id: string; variant?: string }
  readonly kind: "primary" | "compaction" | "title" | "generate"
  url: string
  headers: Record<string, string>
}

interface SessionWebSocketSendHook {
  readonly sessionID: string
  readonly agent: string
  readonly model: { providerID: string; id: string; variant?: string }
  readonly kind: "primary" | "compaction" | "title" | "generate"
  frame: string
}

interface SessionWebSocketReceiveHook {
  readonly sessionID: string
  readonly agent: string
  readonly model: { providerID: string; id: string; variant?: string }
  readonly kind: "primary" | "compaction" | "title" | "generate"
  frame: string
}

type RetryDecision = { retry: false } | { retry: true; delay: number }

interface SessionRetryHook {
  readonly sessionID: string
  readonly agent: string
  readonly model: { providerID: string; id: string; variant?: string }
  readonly error: { type: string; message: string; status?: number }
  readonly attempt: number
  decision: RetryDecision
}

interface SessionRequestHook {
  readonly sessionID: string
  readonly model: { providerID: string; id: string; variant?: string }
  system: SystemPart[]
  messages: Message[]
  options: {
    maxTokens?: number
    temperature?: number
    topP?: number
    topK?: number
    frequencyPenalty?: number
    presencePenalty?: number
    seed?: number
    stop?: string[]
  } & Record<string, unknown>
}

interface SessionContextHook extends SessionRequestHook {
  readonly agent: string
  tools: Record<string, { description: string; input: JsonSchema }>
}

interface SessionCompactionResult {
  summary: string
  native?: Record<string, unknown>
  metadata?: Record<string, unknown>
  tokens?: TokenUsage
}

interface SessionHookContext {
  hook<Name extends keyof SessionHooks>(
    name: Name,
    callback: (event: SessionHooks[Name]) => Promise<void> | void,
    options?: Name extends "prompt" ? never : { providerID?: string },
  ): Promise<Registration>
}
```

### 权限

在配置的规则被评估之后、操作运行之前或权限提示发布之前，审查权限决定。

```ts
await ctx.permission.hook("evaluate", async (event) => {
  if (event.action === "read") return

  const messages = await ctx.session.context({ sessionID: event.sessionID })
  const review = await ctx.generate.text({
    model: { providerID: "anthropic", id: "claude-sonnet-5-5" },
    prompt: buildSafetyPrompt({ messages, action: event.action, resources: event.resources }),
  })
  const decision = parseDecision(review.text)

  event.effect = decision.effect
  event.message = decision.reason
})
```

权限钩子遵循以下规则：

- 钩子针对 `allow` 和 `ask` 决定运行。
- 显式配置的 `deny` 是终态，不会调用钩子。
- 钩子可以把 `effect` 改为 `allow`、`ask` 或 `deny`。
- `message` 出现在升级后的权限请求中，或成为拒绝原因。

#### 参考

```ts
interface PermissionEvaluation {
  readonly sessionID: string
  readonly agent?: string
  readonly action: string
  readonly resources: readonly string[]
  readonly metadata?: Record<string, unknown>
  readonly source?: { type: "tool"; messageID: string; id: string }
  effect: "allow" | "ask" | "deny"
  message?: string
}
```

### Shell

在执行之前修改 shell 命令、工作目录、超时、可执行文件或环境变量。

```ts
await ctx.shell.hook("create.before", (event) => {
  event.timeout = Math.min(event.timeout, 60_000)
  event.env.COMPANY_ENV = "development"
})
```

#### 参考

```ts
interface ShellHookContext {
  hook(name: "create.before", callback: (event: ShellCreateBefore) => Promise<void> | void): Promise<Registration>
}

interface ShellCreateBefore {
  command: string
  cwd: string
  timeout: number
  shell: string
  env: Record<string, string | undefined>
}
```

### 工具

在执行之前检查或替换工具输入。

```ts
await ctx.tool.hook("execute.before", (event) => {
  if (event.tool === "read") console.log(event.input)
})
```

在执行之后检查成功的结果或失败。

```ts
await ctx.tool.hook("execute.after", (event) => {
  if (event.status === "completed") event.result = { ...event.result, metadata: { observed: true } }
  if (event.status === "error") console.error(event.error.message)
})
```

#### 参考

```ts
interface ToolHooks {
  "execute.before": ToolExecuteBefore
  "execute.after": ToolExecuteCompleted | ToolExecuteFailed
}

interface ToolHookContext {
  hook<Name extends keyof ToolHooks>(
    name: Name,
    callback: (event: ToolHooks[Name]) => Promise<void> | void,
  ): Promise<Registration>
}
```

## 支持 V1

插件可以从同一个包入口同时支持 V1 和 V2。默认导出一个对象，同时包含 V1 的 `server()` 函数和 V2 的 `setup()` 函数：

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

- V1 调用 `server()` 并使用返回的钩子。
- V2 读取默认导出的 `id` 和 `setup()`（Effect 插件则是 `effect()`），忽略 `server()`。
- 让每个实现各自使用自己的 API；共享一个导出并不会把 V1 钩子转换为 V2 钩子。
- 将 `Plugin.define(...)` 展开到导出的对象中，这样它会对 V2 定义独立于 `server()` 进行类型检查。

对象形式的 V1 在 OpenCode `1.18.29` 中受支持。更早的 V1 版本可能期望函数导出；请用你打算支持的最老 V1 版本以及 V2 测试已安装的包。
