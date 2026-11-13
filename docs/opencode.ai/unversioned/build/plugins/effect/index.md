---
source_url: https://opencode.ai/docs/build/plugins/effect/
source_hash: sha256:64ac60a31af3c6441760f641ee9e49dfaf0d3b517c11da1224538b89428a89d1
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# Effect

`@opencode/plugin/effect` 是 OpenCode 插件 API 的 Effect 原生版本。它的上下文操作返回 Effect 或 Stream，回调返回 Effect，插件生命周期由 `Scope` 表示。

OpenCode 在加载插件及其 `node_modules` 依赖时，会在运行时提供 `effect`（包括导出的 `effect/*` 子路径）和 `@opencode/plugin`。请将它们安装为 peer/dev 依赖以便本地类型检查和测试，而不要把它们的代码打包进你的插件。

```sh
bun add --peer @opencode/plugin effect@4.0.1
```

从 `.opencode/plugins/` 导出一个 Effect 插件即可自动加载。

```ts title=".opencode/plugins/concise/index.ts"
import { Plugin } from "@opencode/plugin/effect"
import { Effect } from "effect"

export default Plugin.define({
  id: "example",
  effect: (ctx) =>
    Effect.gen(function* () {
      const storage = ctx.storage
      yield* storage.set("loaded", true)
    }),
})
```

`.opencode/plugins/` 之外的已发布包和插件目录，使用与其他服务器插件相同的 `plugins` 配置。

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": [
    "opencode-acme-effect-plugin",
    "opencode-acme-effect-plugin@1.2.0",
    "@acme/opencode-effect-plugin",
    "./plugins/local-effect",
    {
      "package": "@acme/opencode-effect-plugin",
      "options": { "agent": "reviewer", "strict": true },
    },
  ],
}
```

关于启用方式、包解析和配置优先级，参见[配置插件](../../../plugins/index.md)。

```ts title="plugins/local-effect/index.ts"
import { Plugin } from "@opencode/plugin/effect"
import { Effect } from "effect"

export default Plugin.define({
  id: "local-effect",
  effect: (ctx) =>
    Effect.gen(function* () {
      yield* Effect.logInfo("Effect plugin loaded", { version: ctx.app.version })
    }),
})
```

## 生命周期

`effect` 在插件加载时运行。当插件重载或卸载时它的 scope 会关闭，因此注册项、受 scope 管理的 fiber 和 finalizer 会一起被释放。

```ts
import { Plugin } from "@opencode/plugin/effect"
import { Effect } from "effect"

export default Plugin.define({
  id: "lifecycle",
  effect: (ctx) =>
    Effect.gen(function* () {
      yield* Effect.logInfo("loaded", { version: ctx.app.version })
      yield* Effect.addFinalizer(() => Effect.logInfo("unloaded"))
    }),
})
```

后台任务请使用受 scope 管理的 fiber。插件 scope 会在清理时中断该 fiber。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const storage = ctx.storage
    yield* Effect.repeat(
      storage.set("heartbeat", { time: Date.now() }),
      { schedule: Schedule.spaced("1 minute") },
    ).pipe(Effect.forkScoped)
  }),
```

### 上下文

上下文暴露了已连接 OpenCode 服务器的 Effect 客户端，以及插件专属的 transform、hook、storage、reload 和 options。它不暴露 OpenCode 的私有 Core 服务。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const plugins = ctx.plugin
    const active = yield* plugins.list().pipe(Effect.orDie)
    yield* Effect.logInfo("active plugins", { count: active.data.length })
  }),
```

插件定义和完整上下文的声明如下。

```ts
interface Context {
  readonly app: App
  readonly location: Location.Info
  readonly options: PluginOptions
  readonly agent: AgentDomain
  readonly aisdk: AISDKDomain
  readonly command: CommandDomain
  readonly event: EventDomain
  readonly experimental: {
    readonly terminal: Pick<ExperimentalApi<unknown>["persistentPty"], "read">
    readonly generate: GenerateApi<unknown>
  }
  readonly integration: IntegrationDomain
  readonly mcp: MCPDomain
  readonly model: ModelDomain
  /** @deprecated Use `experimental.generate.text`. */
  readonly generate: Pick<ExperimentalGenerateApi<unknown>, "text">
  readonly permission: PermissionDomain
  readonly plugin: Pick<PluginApi<unknown>, "list">
  readonly provider: ProviderDomain
  readonly reference: ReferenceDomain
  readonly rpc: RpcDomain
  readonly session: SessionDomain
  readonly shell: ShellDomain
  readonly skill: SkillDomain
  readonly storage: StorageDomain
  readonly tool: ToolDomain
  readonly vcs: VcsDomain
  readonly websearch: WebSearchDomain
  readonly worktree: WorktreeDomain
}

interface Plugin<R = Scope.Scope> {
  readonly id: string
  readonly effect: (context: Context) => Effect.Effect<void, never, R>
}
```

### Options

通过 `opencode.json(c)` 中的对象形式传递选项。

```jsonc title="opencode.jsonc"
{
  "plugins": [
    {
      "package": "./plugins/company-effect",
      "options": { "strict": true },
    },
  ],
}
```

从 `ctx.options` 读取选项。使用前先对 unknown 值做收窄。

```ts title="plugins/company-effect/index.ts"
import { Plugin } from "@opencode/plugin/effect"
import { Effect } from "effect"

export default Plugin.define({
  id: "company",
  effect: (ctx) =>
    Effect.gen(function* () {
      const strict = ctx.options.strict === true
      yield* Effect.logInfo("company plugin configured", { strict })
    }),
})
```

## Transform

Transform 通过编辑器同步地编辑状态。OpenCode 在每个域内按注册顺序应用 transform。来源会先贡献 provider 和不可变的模型定义；模型 transform 再去编辑活跃 provider 的候选集合。对注册执行 `yield*` 会把注册保留在插件 scope 中。

```ts title="plugins/models-effect/index.ts"
import { Model, Plugin, Provider } from "@opencode/plugin/effect"
import { Effect } from "effect"

export default Plugin.define({
  id: "company.models",
  effect: (ctx) =>
    Effect.gen(function* () {
      const providerID = Provider.ID.make("acme")
      const models = [{ ...Model.Info.default(providerID, Model.ID.make("reasoner")), name: "Acme Reasoner" }]
      yield* ctx.provider.transform((editor) => {
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
    }),
})
```

模型 transform 可以在整个活跃 provider 候选集合上强制执行策略。

```ts title="plugins/model-budget-effect/index.ts"
effect: (ctx) =>
  Effect.gen(function* () {
    yield* ctx.model.transform((editor) => {
      editor
        .list()
        .filter((model) => model.cost.some((tier) => tier.output > 20))
        .forEach((model) => {
          editor.remove(model.providerID, model.id)
        })
    })
  }),
```

当 transform 所使用的外部状态发生变化时调用 `reload`。这里，`loadFromSource()` 返回 `{ info: Provider.Info, models: readonly Model.Info[] }` 条目；provider reload 还会使整个模型结果失效。

```ts title="plugins/models-effect/index.ts"
effect: (ctx) =>
  Effect.gen(function* () {
    const provider = ctx.provider
    const source = { providers: yield* loadFromSource() }

    yield* provider.transform((editor) => {
      source.providers.forEach((provider) => editor.add(provider))
    })

    yield* Effect.repeat(
      Effect.gen(function* () {
        source.providers = yield* loadFromSource()
        yield* provider.reload()
      }),
      { schedule: Schedule.spaced("1 minute") },
    ).pipe(Effect.forkScoped)
  }),
```

## API

### Agent

读取所有 agent，或按 ID 获取单个 agent。客户端响应包含解析后的 location 和 schema 数据。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const agent = ctx.agent
    const agents = yield* agent.list().pipe(Effect.orDie)
    const build = yield* agent.get({ agentID: Agent.ID.make("build") }).pipe(Effect.orDie)
    yield* Effect.logInfo("agents", { count: agents.data.length, build: build.data.name })
  }),
```

Transform 或 reload agent。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const agent = ctx.agent
    yield* agent.transform((editor) => {
      editor.default("build")
      editor.update("build", (item) => (item.description = "Builds features and fixes bugs"))
      editor.remove("legacy")
    })
    yield* agent.reload()
  }),
```

Schema：[`Agent.Info`](../../../api/index.md#schema-Agent.Info)。

```ts
interface AgentEditor {
  list(): readonly Types.DeepMutable<Agent.Info>[]
  get(id: string): Types.DeepMutable<Agent.Info> | undefined
  default(id: string | undefined): void
  update(id: string, update: (agent: Types.DeepMutable<Agent.Info>) => void): void
  remove(id: string): void
}

interface AgentDomain extends AgentApi<unknown> {
  readonly transform: Transform<AgentEditor>
  readonly reload: () => Effect.Effect<void>
}
```

### Providers

读取可用的 provider，或按 ID 检查某个 provider 的元数据。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const provider = ctx.provider
    const providers = yield* provider.list().pipe(Effect.orDie)
    const anthropic = yield* provider.get({ providerID: Provider.ID.make("anthropic") }).pipe(Effect.orDie)
    yield* Effect.logInfo("providers", {
      providers: providers.data.length,
      anthropic: anthropic.data.name,
    })
  }),
```

Provider transform 编辑 provider 设置和来源定义。编辑器读取包括非活跃 provider，并暴露不可变定义；`models.update` 编辑的是某个来源模型的私有副本。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    yield* ctx.provider.transform((editor) => {
      editor.update("anthropic", (provider) => {
        provider.headers = { ...provider.headers, "x-company": "engineering" }
      })
      editor.models.update("anthropic", "claude-sonnet-5-5", (model) => (model.name = "Team Sonnet"))
      editor.models.remove("anthropic", "legacy-model")
      editor.remove("legacy-provider")
    })
  }),
```

用 `models.set` 替换一个来源清单，然后在它捕获的定义发生变化后 reload。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const provider = ctx.provider
    const source = { models: yield* loadModels() }
    yield* provider.transform((editor) => editor.models.set("acme", source.models))
    source.models = yield* loadModels()
    yield* provider.reload()
  }),
```

对于按账号区分的发现，请把用于加载清单的连接作为 `sourceConnection` 传入。在选择其他连接时，OpenCode 会排除该 provider，直到你的插件发布了刷新后的清单。

{/* prettier-ignore */}
```ts
const connection = yield* ctx.integration.connection.active("acme")
if (!connection) return
const inventory = yield* loadInventory(connection)
yield* ctx.provider.transform((editor) => {
  editor.add({ info: inventory.provider, models: inventory.models, sourceConnection: connection })
})
```

Schema：[`Provider.Info`](../../../api/index.md#schema-Provider.Info)、[`Model.Info`](../../../api/index.md#schema-Model.Info)。

```ts
interface ProviderRecord {
  readonly provider: Provider.Info
  readonly models: ReadonlyMap<string, Model.Info>
  readonly sourceConnection?: ConnectionInfo
}

interface ProviderEditor {
  list(): readonly ProviderRecord[]
  get(providerID: string): ProviderRecord | undefined
  add(input: { info: Provider.Info; models: readonly Model.Info[]; sourceConnection?: ConnectionInfo }): void
  update(providerID: string, update: (provider: Types.DeepMutable<Provider.Info>) => void): void
  remove(providerID: string): void
  readonly models: {
    set(providerID: string, models: readonly Model.Info[]): void
    update(providerID: string, modelID: string, update: (model: Types.DeepMutable<Model.Info>) => void): void
    remove(providerID: string, modelID: string): void
  }
}

interface ProviderDomain extends ProviderApi<unknown> {
  readonly transform: Transform<ProviderEditor>
  readonly reload: () => Effect.Effect<void>
}
```

### Models

读取可用的模型和默认选择。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const model = ctx.model
    const models = yield* model.list().pipe(Effect.orDie)
    const selected = yield* model.default().pipe(Effect.orDie)
    yield* Effect.logInfo("models", { count: models.data.length, selected: selected.data?.name })
  }),
```

模型 transform 编辑整个活跃 provider 候选集合。在所有 transform 结束前，禁用的候选仍然可编辑；`update` 只能在可用 provider 下添加模型。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    yield* ctx.model.transform((editor) => {
      editor.list("anthropic").forEach((model) => {
        editor.update(model.providerID, model.id, (draft) => {
          draft.enabled = draft.capabilities.tools
        })
      })
      editor.default.set("anthropic", "claude-sonnet-5-5")
      editor.remove("anthropic", "legacy-model")
    })
  }),
```

回调编辑原始的模型覆盖。provider 默认值会在 OpenCode 提交结果时合并一次；未变化的读取会复用该结果。`editor.provider` 读取的是不可变的来源定义，包括非活跃模板，而不是模型 transform 的输出。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const model = ctx.model
    yield* model.transform((editor) => {
      const source = editor.provider.get("anthropic")?.models.get("claude-sonnet-5-5")
      if (!source) return
      editor.update("anthropic", source.id, (draft) => {
        draft.limit.context = Math.min(draft.limit.context, source.limit.context)
      })
    })
    yield* model.reload()
  }),
```

Schema：[`Model.Info`](../../../api/index.md#schema-Model.Info)。

```ts
interface ModelEditor {
  list(providerID?: string): readonly Types.DeepMutable<Model.Info>[]
  get(providerID: string, modelID: string): Types.DeepMutable<Model.Info> | undefined
  update(providerID: string, modelID: string, update: (model: Types.DeepMutable<Model.Info>) => void): void
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

interface ModelDomain extends ModelApi<unknown> {
  readonly transform: Transform<ModelEditor>
  readonly reload: () => Effect.Effect<void>
}
```

### Commands

读取当前位置可用的命令。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const command = ctx.command
    const commands = yield* command.list().pipe(Effect.orDie)
    yield* Effect.logInfo("commands", { names: commands.data.map((item) => item.name) })
  }),
```

当前的命令 transform 仅支持添加。executor 会接收会话、提示词附件和投递模式。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const command = ctx.command
    const session = ctx.session
    yield* command.transform((editor) => {
      editor.add({
        name: "security-review",
        description: "Review changes for security issues",
        execute: (input) =>
          session.prompt({
            ...input.prompt,
            sessionID: input.sessionID,
            text: `Review these changes for security issues.\n\n${input.prompt.text}`,
            delivery: input.delivery,
          }).pipe(Effect.asVoid),
      })
    })
    yield* command.reload()
  }),
```

Schema：[`Command.Info`](../../../api/index.md#schema-Command.Info)、[`Session.Inbox.Delivery`](../../../api/index.md#schema-Session.Inbox.Delivery)。

```ts
interface CommandInvocation {
  readonly sessionID: Session.ID
  readonly prompt: PromptInput.Prompt
  readonly delivery: SessionInbox.Delivery
}

interface CommandDefinition {
  readonly name: string
  readonly description?: string
  readonly execute: (input: CommandInvocation) => Effect.Effect<void, unknown>
}

interface CommandEditor {
  add(definition: CommandDefinition): void
}

interface CommandDomain extends Pick<CommandApi<unknown>, "list"> {
  readonly transform: Transform<CommandEditor>
  readonly reload: () => Effect.Effect<void>
}
```

### 集成

读取集成，并在存在凭据时解析活跃凭据。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const integration = ctx.integration
    const integrations = yield* integration.list().pipe(Effect.orDie)
    const github = yield* integration.get({ integrationID: Integration.ID.make("github") }).pipe(Effect.orDie)
    const connection = yield* integration.connection.active("github")
    const credential = connection ? yield* integration.connection.resolve(connection).pipe(Effect.orDie) : undefined
    yield* Effect.logInfo("integration", {
      count: integrations.data.length,
      github: github.data.name,
      credential: credential?.type,
    })
  }),
```

用密钥连接，或通过已连接的 API 驱动一次 OAuth 尝试。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const integration = ctx.integration
    const token = yield* Config.Redacted("GITHUB_TOKEN").pipe(Effect.orDie)
    yield* integration.connect
      .key({ integrationID: Integration.ID.make("github"), key: Redacted.value(token) })
      .pipe(Effect.orDie)

    const attempt = yield* integration.oauth
      .connect({
        integrationID: Integration.ID.make("acme"),
        methodID: Integration.MethodID.make("oauth"),
      })
      .pipe(Effect.orDie)
    const status = yield* integration.oauth
      .status({
        integrationID: Integration.ID.make("acme"),
        attemptID: attempt.data.attemptID,
      })
      .pipe(Effect.orDie)
    yield* Effect.logInfo("OAuth status", { status: status.data })
  }),
```

Transform 集成和认证方式。OAuth 方式回调是 Effect，并且可以获取受 scope 管理的资源。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const integration = ctx.integration
    yield* integration.transform((editor) => {
      editor.update("acme", (item) => (item.name = "Acme"))
      editor.method.update({
        integrationID: "acme",
        method: { id: "device", type: "oauth", label: "Sign in with Acme" },
        authorize: () =>
          Effect.succeed({
            mode: "code",
            url: "https://acme.example/device",
            instructions: "Enter the displayed code",
            callback: (code) => exchangeCode(code),
          }),
      })
    })
    yield* integration.reload()
  }),
```

Schema：[`Integration.Info`](../../../api/index.md#schema-Integration.Info)、[`Integration.Method`](../../../api/index.md#schema-Integration.Method)、[`Connection.Info`](../../../api/index.md#schema-Connection.Info)、[`Form.Answer`](../../../api/index.md#schema-Form.Answer)。

```ts
type IntegrationOAuthAuthorization = {
  readonly url: string
  readonly instructions: string
  readonly expiresAt?: number
} & (
  | { readonly mode: "auto"; readonly callback: Effect.Effect<Credential.OAuth, unknown> }
  | { readonly mode: "code"; readonly callback: (code: string) => Effect.Effect<Credential.OAuth, unknown> }
)

type IntegrationOAuthMethodRegistration = {
  readonly integrationID: string
  readonly method: IntegrationOAuthMethod
  readonly authorize: (answer: Form.Answer) => Effect.Effect<IntegrationOAuthAuthorization, unknown, Scope.Scope>
  readonly refresh?: (credential: Credential.OAuth) => Effect.Effect<Credential.OAuth, unknown>
  readonly label?: (credential: Credential.OAuth) => string | undefined
}

interface IntegrationEditor {
  list(): readonly IntegrationRef[]
  get(id: string): IntegrationRef | undefined
  update(id: string, update: (integration: IntegrationRef) => void): void
  remove(id: string): void
  readonly method: {
    list(integrationID: string): readonly IntegrationMethod[]
    update(input: IntegrationMethodRegistration): void
    remove(integrationID: string, method: IntegrationMethod): void
  }
}

interface IntegrationDomain extends Omit<IntegrationApi<unknown>, "wellknown"> {
  readonly transform: Transform<IntegrationEditor>
  readonly reload: () => Effect.Effect<void>
  readonly connection: {
    readonly active: (integrationID: string) => Effect.Effect<ConnectionInfo | undefined>
    readonly resolve: (connection: ConnectionInfo) => Effect.Effect<Credential.Value | undefined, unknown>
  }
}
```

### MCP

列出 MCP 服务器及其当前连接状态。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const mcp = ctx.mcp
    const servers = yield* mcp.list().pipe(Effect.orDie)
    yield* Effect.logInfo("MCP servers", { count: servers.data.length })
  }),
```

插件只能通过 transform 管理 MCP 服务器。用 `editor.set` 添加或替换服务器，用 `editor.update` 修改其配置，用 `editor.remove` 移除它。用 `editor.list` 和 `editor.get` 检查配置。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const mcp = ctx.mcp
    yield* mcp.transform((editor) => {
      const servers = editor.list()
      const docs = editor.get("docs")
      editor.set("docs", { type: "remote", url: "https://mcp.example.com" })
      editor.update("docs", (server) => (server.disabled = false))
      editor.remove("legacy")
    })
  }),
```

在 transform 中设置 `disabled: true` 可禁用服务器并断开连接，设置 `disabled: false` 可启用它并允许 OpenCode 连接。OpenCode 会依据转换后的配置来调和服务器生命周期。

当 transform 所使用的外部状态发生变化后调用 `reload()`，以重新应用 transform 并调和服务器。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const mcp = ctx.mcp
    yield* mcp.reload()
  }),
```

Schema：[`Mcp.Server`](../../../api/index.md#schema-Mcp.Server)、[`Mcp.LocalConfigEncoded`](../../../api/index.md#schema-Mcp.LocalConfigEncoded)、[`Mcp.RemoteConfigEncoded`](../../../api/index.md#schema-Mcp.RemoteConfigEncoded)。

```ts
interface MCPEditor {
  list(): readonly [string, Types.DeepMutable<Mcp.ServerConfig>][]
  get(name: string): Types.DeepMutable<Mcp.ServerConfig> | undefined
  set(name: string, config: Mcp.ServerConfig): void
  update(name: string, update: (config: Types.DeepMutable<Mcp.ServerConfig>) => void): void
  remove(name: string): void
}

interface MCPDomain extends Pick<McpApi<unknown>, "list"> {
  readonly transform: Transform<MCPEditor>
  readonly reload: () => Effect.Effect<void>
}
```

### 插件

列出当前位置的活跃、失败和已解析插件。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const plugin = ctx.plugin
    const plugins = yield* plugin.list().pipe(Effect.orDie)
    yield* Effect.forEach(plugins.data, (item) => Effect.logInfo("plugin", item), { discard: true })
  }),
```

当只关心活跃插件时，在 Effect 管道中过滤 schema 值。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const plugin = ctx.plugin
    const active = yield* plugin.list().pipe(
      Effect.orDie,
      Effect.map((result) => result.data.filter((item) => item.state.status === "active")),
    )
    yield* Effect.logInfo("active plugin count", { count: active.length })
  }),
```

Schema：[`Plugin.Info`](../../../api/index.md#schema-Plugin.Info)、[`Plugin.Source`](../../../api/index.md#schema-Plugin.Source)。

```ts
interface PluginApi<E = never> {
  readonly list: PluginListOperation<E>
}

interface Context {
  readonly plugin: PluginApi<unknown>
}
```

### 引用

读取当前位置可用的引用。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const reference = ctx.reference
    const references = yield* reference.list().pipe(Effect.orDie)
    yield* Effect.logInfo("references", { count: references.data.length })
  }),
```

添加或移除本地与 Git 引用，然后在外部状态变化后 reload。`get(name)` 返回当前配置的来源，名称不存在时返回 `undefined`。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const reference = ctx.reference
    yield* reference.transform((editor) => {
      editor.add("handbook", { type: "local", path: "/workspace/docs/handbook" })
      editor.add("standards", { type: "git", repository: "https://github.com/acme/standards", branch: "main" })
      const handbook = editor.get("handbook")
      editor.remove("legacy")
    })
    yield* reference.reload()
  }),
```

Schema：[`Reference.Info`](../../../api/index.md#schema-Reference.Info)、[`Reference.LocalSource`](../../../api/index.md#schema-Reference.LocalSource)、[`Reference.GitSource`](../../../api/index.md#schema-Reference.GitSource)。

```ts
interface ReferenceEditor {
  add(name: string, source: ReferenceLocalSource | ReferenceGitSource): void
  remove(name: string): void
  list(): readonly (readonly [string, ReferenceLocalSource | ReferenceGitSource])[]
  get(name: string): ReferenceLocalSource | ReferenceGitSource | undefined
}

interface ReferenceDomain extends ReferenceApi<unknown> {
  readonly transform: Transform<ReferenceEditor>
  readonly reload: () => Effect.Effect<void>
}
```

### 会话

创建或读取会话，然后选择后续工作使用的 agent 和模型。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const session = ctx.session
    const created = yield* session.create({ title: "Review" }).pipe(Effect.orDie)
    const current = yield* session.get({ sessionID: created.id }).pipe(Effect.orDie)
    yield* session.switchAgent({ sessionID: current.id, agent: Agent.ID.make("build") }).pipe(Effect.orDie)
    yield* session
      .switchModel({
        sessionID: current.id,
        model: { providerID: Provider.ID.make("anthropic"), id: Model.ID.make("claude-sonnet-5-5") },
      })
      .pipe(Effect.orDie)
  }),
```

发送提示词、临时生成请求、命令或合成消息。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const session = ctx.session
    const created = yield* session.create({ title: "Automation" }).pipe(Effect.orDie)
    yield* session.prompt({ sessionID: created.id, text: "Review the current changes" }).pipe(Effect.orDie)
    const summary = yield* session
      .generate({ sessionID: created.id, prompt: "Summarize this project" })
      .pipe(Effect.orDie)
    yield* session.command({ sessionID: created.id, name: "review", text: "--staged" }).pipe(Effect.orDie)
    yield* session
      .synthetic({ sessionID: created.id, text: `Summary generated: ${summary.text}`, resume: false })
      .pipe(Effect.orDie)
  }),
```

逐页列出会话。要获取下一页，把 `cursor.next` 作为 `cursor` 传回即可。游标会记住你的过滤条件，因此无需重复它们。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const page = yield* ctx.session.list({ directory: ctx.location.directory, limit: 20 }).pipe(Effect.orDie)
    const next = page.cursor.next
      ? yield* ctx.session.list({ cursor: page.cursor.next, limit: 20 }).pipe(Effect.orDie)
      : undefined
  }),
```

用 `remove` 移除临时会话。移除会停止正在进行的执行，并递归删除子会话。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const created = yield* ctx.session.create({ title: "Temporary worker" }).pipe(Effect.orDie)
    yield* ctx.session.remove({ sessionID: created.id }).pipe(Effect.orDie)
  }),
```

用 `compact` 请求压缩。它返回的是被接纳的收件箱条目，而不是已完成的摘要；默认情况下压缩在下一个步骤边界运行。传 `delivery: "queue"` 则改为保留队列顺序。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const created = yield* ctx.session.create({ title: "Review" }).pipe(Effect.orDie)
    const compaction = yield* ctx.session.compact({ sessionID: created.id }).pipe(Effect.orDie)
  }),
```

用 `instructions.entry` 附加、列出或移除带键的会话指令条目。条目会以 `<context key="...">` 块的形式呈现在会话的指令中，更新或移除会在下一个步骤边界被宣布，而不会排队一条消息回合。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const created = yield* ctx.session.create({ title: "Review" }).pipe(Effect.orDie)
    yield* ctx.session.instructions.entry
      .put({ sessionID: created.id, key: "deploy-target", value: "production" })
      .pipe(Effect.orDie)
    const entries = yield* ctx.session.instructions.entry.list({ sessionID: created.id }).pipe(Effect.orDie)
    yield* ctx.session.instructions.entry.remove({ sessionID: created.id, key: "deploy-target" }).pipe(Effect.orDie)
  }),
```

Schema：[`Session.Info`](../../../api/index.md#schema-Session.Info)、[`Model.Ref`](../../../api/index.md#schema-Model.Ref)、[`Session.Inbox.User`](../../../api/index.md#schema-Session.Inbox.User)、[`Session.Inbox.Synthetic`](../../../api/index.md#schema-Session.Inbox.Synthetic)、[`InstructionEntry.Info`](../../../api/index.md#schema-InstructionEntry.Info)。

```ts
type SessionDomain = Pick<
  SessionApi<unknown>,
  | "list"
  | "create"
  | "get"
  | "remove"
  | "switchAgent"
  | "switchModel"
  | "prompt"
  | "generate"
  | "command"
  | "compact"
  | "synthetic"
  | "interrupt"
  | "update"
  | "move"
  | "wait"
  | "context"
  | "instructions"
>
```

### 技能

读取当前位置的技能。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const skill = ctx.skill
    const skills = yield* skill.list().pipe(Effect.orDie)
    yield* Effect.logInfo("skills", { ids: skills.data.map((item) => item.id) })
  }),
```

Transform 并 reload 技能。使用重新导出的 Effect schema 构造器来创建品牌化（branded）的值。`get(id)` 返回当前编辑器条目，技能不存在时返回 `undefined`。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const skill = ctx.skill
    yield* skill.transform((editor) => {
      editor.add(Skill.Info.make({
        id: Skill.ID.make("review"),
        name: Skill.Name.make("Review"),
        description: "Review the current changes",
        path: Skill.Info.fields.path.make("/workspace/.opencode/skills/review/SKILL.md"),
        content: "Review the current changes for correctness and missing tests.",
      }))
      const review = editor.get("review")
      editor.update("review", (item) => (item.autoinvoke = true))
      editor.remove("legacy")
    })
    yield* skill.reload()
  }),
```

Schema：[`Skill.Info`](../../../api/index.md#schema-Skill.Info)。

```ts
interface SkillEditor {
  list(): readonly Types.DeepMutable<Skill.Info>[]
  get(id: string): Types.DeepMutable<Skill.Info> | undefined
  add(skill: Skill.Info): void
  update(id: string, update: (skill: Types.DeepMutable<Skill.Info>) => void): void
  remove(id: string): void
}

interface SkillDomain extends SkillApi<unknown> {
  readonly transform: Transform<SkillEditor>
  readonly reload: () => Effect.Effect<void>
}
```

### Storage

存储、读取和移除以插件 ID 为作用域的持久化 JSON 值。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const storage = ctx.storage
    yield* storage.set("settings", { strict: true })
    const settings = yield* storage.get("settings")
    yield* Effect.logInfo("settings", { settings })
    yield* storage.remove("settings")
  }),
```

按前缀扫描键，并使用游标分页。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const storage = ctx.storage
    const first = yield* storage.scan({ prefix: "cache/", limit: 100 })
    const second = first.next
      ? yield* storage.scan({ prefix: "cache/", after: first.next, limit: 100 })
      : { entries: [] }
    yield* Effect.logInfo("cache entries", { count: first.entries.length + second.entries.length })
  }),
```

Storage 接受 Effect 的 JSON 类型，并直接返回 Effect。

```ts
interface StorageDomain {
  readonly get: (key: string) => Effect.Effect<Schema.Json | undefined>
  readonly set: (key: string, value: Schema.Json) => Effect.Effect<void>
  readonly remove: (key: string) => Effect.Effect<void>
  readonly scan: (options: StorageScanOptions) => Effect.Effect<StorageScanResult>
}
```

### 工具

使用 Effect `Schema` 注册带类型的工具。executor 接收解码后的输入，并返回一个包含带类型输出、展示内容或元数据的 Effect。

编辑器支持 `add`、`update` 和 `remove`。transform 回调是同步的：它不得返回 Effect 或 Promise。请在注册或 reload 之前加载外部数据。OpenCode 会在一个全新编辑器上按注册顺序重放活跃的 transform；对于相同的有效工具名，后一次有效注册会覆盖前一次。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const tool = ctx.tool
    yield* tool.transform((editor) => {
      editor.namespace({
        name: "acme",
        description: "Customer account tools",
      })
      editor.add({
        name: "greeting",
        description: "Create a greeting",
        input: Schema.Struct({ name: Schema.String }),
        output: Schema.Struct({ greeting: Schema.String }),
        options: { namespace: "acme", codemode: true },
        execute: ({ name }, context) =>
          Effect.gen(function* () {
            yield* context.progress({ status: "greeting" })
            return { output: { greeting: `Hello ${name}!` } }
          }),
      })
    })
  }),
```

在回调捕获的来源数据发生变化后调用 `yield* ctx.tool.reload()`。Reload 会以原有顺序重放活跃的 transform；它不会重新运行插件 effect。

Effect 工具接受与 Promise 工具相同的[自由格式输入声明](../server/index.md#freeform-tool-input)。如果模型未声明支持该格式，工具将保持其常规的对象输入。

工具的 `id` 包含其有效名称，当该 ID 不存在时 `get()` 返回 `undefined`。使用 `update` 和 `remove` 时传入有效工具名，包括其命名空间（即上文的 `acme_greeting`）。命名空间中的点和工具名中不受支持的字符会变成 `_`。缺失的名称会被忽略；创建工具需要带完整定义的 `add`。更新会保留名称和命名空间。请通过赋值新的 schema 或选项来替换它们，而不是修改嵌套值。无效的更新会被记录日志，并保持先前的定义不变。

{/* prettier-ignore */}
```ts
yield* ctx.tool.transform((editor) => {
  editor.update("acme_greeting", (tool) => {
    tool.description = "Greet the user by name"
  })
  editor.remove("acme_obsolete")
})
```

更新和移除会与添加一起按顺序重放，包括在 MCP 目录刷新之后。

`transform` 返回一个受 scope 管理的注册。运行 `yield* registration.dispose` 可移除它的 transform 并基于剩余 transform 重建，从而露出它先前覆盖的任何定义。释放是幂等的，关闭插件 scope 也会释放它的注册。

每次模型请求都会捕获一份工具快照。Reload 和释放只影响未来的快照，不影响已被现有请求捕获的定义或 executor。闭包引用了可变插件数据的 executor 仍然能观察到那些数据；如果某个值必须始终与该定义绑定，请在 transform 内部捕获它。

Schema：[`Tool.Content`](../../../api/index.md#schema-Tool.Content)、[`Tool.TextContent`](../../../api/index.md#schema-Tool.TextContent)、[`Tool.FileContent`](../../../api/index.md#schema-Tool.FileContent)。

```ts
interface ToolEditor {
  list(): readonly (Tool.Info & { readonly id: string })[]
  get(id: string): (Tool.Info & { readonly id: string }) | undefined
  namespace(namespace: { name: string; description: string }): void
  add<Input extends Tool.ValueSchema<any>, Output extends Tool.ValueSchema<any> | undefined>(
    tool: Tool.Info<Input, Output>,
  ): void
  update(id: string, update: (tool: Types.Mutable<Tool.Info>) => void): void
  remove(id: string): void
}

interface ToolDomain {
  readonly list: () => Effect.Effect<readonly (Tool.Info & { readonly id: string })[]>
  readonly transform: Transform<ToolEditor>
  readonly reload: () => Effect.Effect<void>
}
```

### VCS

读取仓库信息、工作副本状态或文件差异。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const vcs = ctx.vcs
    const info = yield* vcs.get().pipe(Effect.orDie)
    const branches = yield* vcs.branch.list({ search: "feature", limit: 10 }).pipe(Effect.orDie)
    const changes = yield* vcs.status().pipe(Effect.orDie)
    const diff = yield* vcs.diff({ mode: "working", context: 3 }).pipe(Effect.orDie)
    yield* Effect.logInfo("vcs", { branch: info.data.branch.current, files: changes.data.length })
  }),
```

通过受 scope 管理的 transform 注册一个按 location 限定作用域的 provider。与检测到的仓库类型匹配的 provider 会被自动选中；用 `editor.default.set` 可以选择其他 provider。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const vcs = ctx.vcs
    yield* vcs.transform((editor) => {
      editor.add({
        id: "custom",
        name: "Custom VCS",
        info: () => Effect.succeed({ branch: { current: "feature", default: "main" } }),
        branches: (input) => readBranches(input),
        status: (scope) => readStatus(scope.worktree),
        diff: (input) => readDiff(input),
      })
      editor.default.set("custom")
    })
  }),
```

Provider 回调会接收当前 location、工作副本根目录、规范化的项目根目录，以及可选的仓库存储。diff 回调还会接收所选模式、请求的上下文行数和输出字节预算。仓库发现仍然使用 OpenCode 内置的 Git 和 Mercurial 检测器。

Provider 可以选择性地实现 `init(scope)` 来在 `scope.worktree` 中创建仓库。初始化按 ID 选择 provider（默认是 Git），而不是按检测到的仓库类型。即使 location 尚无仓库也可以注册带 `init` 的 provider；OpenCode 会在调用它之前检查该目录存在且没有仓库，然后重新发现项目。新的仓库格式仍需要在此回调之外的发现支持。

Schema：[`Vcs.Info`](../../../api/index.md#schema-Vcs.Info)、[`Vcs.FileStatus`](../../../api/index.md#schema-Vcs.FileStatus)、[`FileDiff.Info`](../../../api/index.md#schema-FileDiff.Info)。

```ts
interface VcsEditor {
  add(definition: VcsDefinition): void
  readonly default: {
    get(): string | undefined
    set(selection: string): void
  }
}

interface VcsDomain extends Omit<VcsApi<unknown>, "init"> {
  readonly transform: Transform<VcsEditor>
  readonly reload: () => Effect.Effect<void>
}

interface VcsDefinition {
  readonly init?: (scope: VcsScope) => Effect.Effect<void, unknown>
  // Existing info, branches, status, and diff callbacks are required.
}
```

### 网络搜索

列出 provider，或通过选定的 provider 执行查询。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const websearch = ctx.websearch
    const providers = yield* websearch.providers().pipe(Effect.orDie)
    const results = yield* websearch
      .query({ query: "OpenCode plugins", providerID: WebSearch.ID.make("internal") })
      .pipe(Effect.orDie)
    yield* Effect.logInfo("websearch", { providers: providers.data.length, results: results.data.results.length })
  }),
```

注册一个 Effect executor 并选择默认 provider。将默认值设为 `false` 可禁用网络搜索。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const websearch = ctx.websearch
    yield* websearch.transform((editor) => {
      editor.add({
        id: "internal",
        name: "Internal search",
        execute: ({ query }) => searchInternal(query),
      })
      editor.default.set("internal")
    })
    yield* websearch.reload()
  }),
```

Schema：[`WebSearch.Provider`](../../../api/index.md#schema-WebSearch.Provider)、[`WebSearch.Result`](../../../api/index.md#schema-WebSearch.Result)。

```ts
interface WebSearchDefinition {
  readonly id: string
  readonly name: string
  readonly execute: (input: WebSearch.ProviderInput) => Effect.Effect<readonly WebSearch.Result[], unknown>
}

interface WebSearchEditor {
  add(definition: WebSearchDefinition): void
  readonly default: {
    get(): string | false | undefined
    set(selection: string | false): void
  }
}

interface WebSearchDomain extends WebsearchApi<unknown> {
  readonly transform: Transform<WebSearchEditor>
  readonly reload: () => Effect.Effect<void>
}
```

### 事件

公开的服务器事件订阅是一个 Effect `Stream`。在插件 scope 中 fork 它的消费者，以便自动中断。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const event = ctx.event
    yield* event.subscribe().pipe(
      Stream.tap((item) => Effect.logDebug("OpenCode event", { type: item.type })),
      Stream.runDrain,
      Effect.forkScoped,
    )
  }),
```

传入 `types` 可只接收你需要的事件类型。Stream 的类型会相应收窄，因此不需要类型守卫。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const event = ctx.event
    yield* event.subscribe({ types: ["config.updated"] }).pipe(
      Stream.runForEach(() => Effect.logInfo("configuration changed")),
      Effect.forkScoped,
    )
  }),
```

Schema：[`V2EventEncoded`](../../../api/index.md#schema-V2EventEncoded)。

```ts
type EventType = Exclude<OpenCodeEvent["type"], "server.connected">

interface EventDomain {
  readonly subscribe: <Type extends EventType = EventType>(input?: {
    readonly types?: ReadonlyArray<Type>
  }) => Stream.Stream<Extract<OpenCodeEvent, { type: Type }>, unknown>
}
```

## Hook

Hook 会拦截正在进行的操作。多个插件可以注册同一个 hook；OpenCode 按插件顺序运行它们，因此靠后的 hook 能看到靠前 hook 做出的更改。注册在插件 scope 内保持活跃。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const session = ctx.session
    yield* session.hook("context", () => Effect.void)
  }),
```

### 会话

在模型分发前一刻修改组装好的系统指令、消息或工具。`context` 针对 agent 循环运行；`compaction`、`generate` 和 `title` 针对那些辅助请求运行。`compaction` 和 `title` 接受一个 `result`，用于跳过模型调用。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const session = ctx.session
    yield* session.hook("context", (event) =>
      Effect.sync(() => {
        event.system.push({ type: "text", text: "Keep the review focused on correctness." })
        delete event.tools.write
      }),
    )
    yield* session.hook("compaction", (event) =>
      Effect.map(summarize(event.messages), (summary) => {
        event.result = { summary }
      }),
    )
  }),
```

`context`、`compaction` 和 `generate` hook 中的消息携带其已存储消息的 `metadata`，只读（例如某个 `prompt` hook 设置的内容）。它不会发送给模型。

承载 OpenCode 指令的 `system` 部分还会在 `metadata.experimental.instructions` 中把每个来源以 `{ key, text }` 的形式列出，例如 `core/date` 或 `core/environment`，这样 hook 就能区分各来源。该列表是一份副本：编辑该部分的 `text` 不会更新它。这是实验性功能，可能会变化。

修改模型请求设置，并且可以选择把 hook 限定到某个 provider。事件携带的 `kind` 与下文 HTTP hook 相同。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const session = ctx.session
    yield* session.hook(
      "model.request",
      (event) => Effect.sync(() => (event.headers["x-plugin"] = "review")),
      { providerID: "anthropic" },
    )
  }),
```

修改原生的 provider 请求或响应。它们的 body 是一次性流；读取前请克隆或替换 body。两个 hook 都会对会话发出的每个请求运行；`event.kind` 是 `"primary"`、`"compaction"`、`"title"` 或 `"generate"`，取决于发起该请求的流程。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const session = ctx.session
    yield* session.hook("http.request", (event) =>
      Effect.sync(() => {
        event.request.headers.set("x-session-id", event.sessionID)
        if (event.kind === "title") event.request.headers.set("x-priority", "background")
      }),
    )
    yield* session.hook("http.response", (event) =>
      Effect.sync(() => {
        event.response = new Response(event.response.body, {
          status: event.response.status,
          headers: { ...Object.fromEntries(event.response.headers), "x-plugin": "review" },
        })
      }),
    )
  }),
```

通过 WebSocket 流式传输的 provider 会为每个会话复用一条连接，因此 HTTP hook 看不到那部分流量。实验性的 `experimental.ws.handshake` hook 在每次模型调用时、在选定连接之前运行一次，并暴露连接的 `url` 和 `headers`；修改其中任何一个都会重新打开 socket。当 WebSocket 路由回退到 HTTP 时，HTTP hook 仍然会针对这些请求运行。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    yield* ctx.session.hook(
      "experimental.ws.handshake",
      (event) =>
        Effect.gen(function* () {
          event.headers.authorization = `Bearer ${yield* mintToken(event.url)}`
          delete event.headers["api-key"]
        }),
      { providerID: "azure" },
    )
  }),
```

`experimental.ws.send` 和 `experimental.ws.receive` 暴露的是帧本身：`send` 在 provider 驱动构建出站帧之后运行，`receive` 在每个入站帧被驱动观察到之前运行。hook 返回时 `frame` 中存放的内容就是实际跨网络传输或到达驱动的内容；OpenCode 不对它做校验。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    yield* ctx.session.hook(
      "experimental.ws.send",
      (event) =>
        Effect.sync(() => {
          const body = JSON.parse(event.frame)
          if (body.type === "response.create") body.metadata = { ...body.metadata, session: event.sessionID }
          event.frame = JSON.stringify(body)
        }),
      { providerID: "openai" },
    )
  }),
```

覆盖对某次 provider 失败的重试决定，或替换其以毫秒计的延迟。该 hook 在 OpenCode 完成失败分类并提出其策略之后、任何重试被调度之前运行。它不暴露 OpenCode 内部如何执行下一次尝试。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    yield* ctx.session.hook("retry", (event) =>
      Effect.sync(() => {
        if (event.error.status === 429) {
          event.decision = { retry: true, delay: 10_000 }
          return
        }
        if (event.error.type === "provider.invalid-request" && event.attempt === 2) {
          event.decision = { retry: true, delay: 0 }
          return
        }
        if (event.attempt >= 3) event.decision = { retry: false }
      }),
    )
  }),
```

初始的 `decision` 是 OpenCode 的策略，因此 hook 既可以把通常终止性的 provider 失败改为可重试，也可以否决一个提议的重试。多个 hook 按注册顺序运行，靠后的 hook 能看到当前的决定。内置的最大尝试次数仍是硬性上限。`attempt` 是正在提议的物理尝试次数；初始请求是第 `1` 次，因此第一次重试是第 `2` 次。无效的延迟（`NaN`、无穷大或负值）会回退到计算出的延迟。上下文溢出恢复仍然与此分开，因为它压缩对话而不是重试同一请求。

#### 参考

```ts
interface SessionHooks {
  readonly context: SessionContext
  readonly compaction: SessionCompaction
  readonly generate: SessionGenerate
  readonly title: SessionTitle
  readonly "model.request": SessionModelRequest
  readonly "http.request": SessionHttpRequest
  readonly "http.response": SessionHttpResponse
  readonly "experimental.ws.handshake": SessionWebSocketHandshake
  readonly "experimental.ws.send": SessionWebSocketSend
  readonly "experimental.ws.receive": SessionWebSocketReceive
  readonly retry: SessionRetry
}

type RetryDecision = { retry: false } | { retry: true; delay: number }

interface SessionRetry {
  readonly sessionID: string
  readonly agent: string
  readonly model: { providerID: string; id: string; variant?: string }
  readonly error: { type: string; message: string; status?: number }
  readonly attempt: number
  decision: RetryDecision
}

interface SessionHookDomain {
  readonly hook: ModelHooks<SessionHooks>
}
```

### Shell

在执行前修改 shell 命令、工作目录、超时、可执行文件或环境变量。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const shell = ctx.shell
    yield* shell.hook("create.before", (event) =>
      Effect.sync(() => {
        if (event.command === "npm") event.command = "bun"
        event.timeout = Math.min(event.timeout, 60_000)
        event.env.COMPANY_ENV = "development"
      }),
    )
  }),
```

#### 参考

```ts
interface ShellCreateBefore {
  command: string
  cwd: string
  timeout: number
  shell: string
  env: Record<string, string | undefined>
}

interface ShellHooks {
  readonly "create.before": ShellCreateBefore
}

interface ShellHookDomain {
  readonly hook: Hooks<ShellHooks>
}
```

### 工具

前置 hook 可以替换输入，或用 `Tool.Error` 失败。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const tool = ctx.tool
    yield* tool.hook("execute.before", (event) =>
      event.tool === "write"
        ? Effect.fail(new Tool.Error({ message: "Writes are disabled" }))
        : Effect.logDebug("tool input", { tool: event.tool, input: event.input }),
    )
  }),
```

后置 hook 可以检查或替换成功的结果与失败。

```ts
effect: (ctx) =>
  Effect.gen(function* () {
    const tool = ctx.tool
    yield* tool.hook("execute.after", (event) => {
      if (event.status === "error") return Effect.logWarning("tool failed", { message: event.error.message })
      return Effect.sync(() => {
        event.result = { ...event.result, metadata: { observed: true } }
      })
    })
  }),
```

#### 参考

```ts
interface ToolHooks {
  readonly "execute.before": ToolExecuteBefore
  readonly "execute.after": ToolExecuteAfter
}

interface ToolFailures extends Record<keyof ToolHooks, unknown> {
  readonly "execute.before": Tool.Error
  readonly "execute.after": never
}

interface ToolHookDomain {
  readonly hook: Hooks<ToolHooks, ToolFailures>
}
```

共享的注册类型显示了哪些操作需要插件 scope。

```ts
interface Registration {
  readonly dispose: Effect.Effect<void>
}

type Hooks<Spec, Failures extends Record<keyof Spec, unknown> = Record<keyof Spec, never>> = <Name extends keyof Spec>(
  name: Name,
  callback: (input: Spec[Name]) => Effect.Effect<void, Failures[Name]>,
) => Effect.Effect<Registration, never, Scope.Scope>

type Transform<Input> = (callback: (input: Input) => void) => Effect.Effect<Registration, never, Scope.Scope>
```

## 发布

包插件使用与本地 Effect 插件相同的默认导出。从主入口导出 Effect 实现，并把 `effect` 声明为 `peerDependency`。在 `devDependencies` 下固定 `@opencode/plugin` 所使用的版本，这样开发安装只会有一份副本。

```json title="package.json"
{
  "name": "opencode-acme-effect-plugin",
  "version": "1.0.0",
  "type": "module",
  "exports": {
    ".": "./src/index.ts"
  },
  "dependencies": {
    "@opencode/plugin": "latest"
  },
  "peerDependencies": {
    "effect": "^4.0.1"
  },
  "devDependencies": {
    "effect": "4.0.1"
  }
}
```

OpenCode 会把对 `effect`、导出的 `effect/*` 子路径以及 `@opencode/plugin` 的导入（包括插件 `node_modules` 中依赖的导入）重定向到宿主的运行时实例，这样 fiber、logger 和 `Schema` 解析器就能共享同一份运行时副本。

- 不要把 `effect` 打包进发布的插件产物。如果用打包器构建，请把 `effect` 和 `effect/*` 标记为 external。
- 插件及其 `node_modules` 依赖始终针对宿主 OpenCode 发布版的 `effect` 实例执行。请使用与目标 OpenCode 发布版兼容的 `effect` API 和模块路径；基于其他 `effect` 主版本（如 Effect 3）构建的依赖同样会收到宿主的 `effect`，不受支持。
- 只提供公开的 `effect` 子路径。导入 Effect 私有 `internal` 模块之一的插件会加载失败，并报出指明该路径的错误。
- 编译后的 OpenCode 二进制不包含 Effect HTTP API 文档页面所需的 Scalar 和 Swagger UI 资源；从插件提供这些页面时只会显示一条提示。

包入口导出带 `effect` 函数的 `Plugin.define`。

```ts title="src/index.ts"
import { Plugin } from "@opencode/plugin/effect"
import { Effect } from "effect"

export default Plugin.define({
  id: "acme.published",
  effect: (ctx) =>
    Effect.gen(function* () {
      const storage = ctx.storage
      yield* storage.set("installed", true)
    }),
})
```

请使用与目标 OpenCode 发布版兼容的版本，并测试已安装的包本身，而不是只测试通过 workspace 链接的副本。

```sh
bun pm pack
bun add ./opencode-acme-effect-plugin-1.0.0.tgz
```
