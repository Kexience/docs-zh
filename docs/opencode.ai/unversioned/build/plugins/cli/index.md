---
source_url: https://opencode.ai/docs/build/plugins/cli/
source_hash: sha256:6f09bda16d3a528b24a3cb67ea9b67044739b8d6b136a2f54852226d87bd5150
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# TUI

TUI 插件通过命令、路由、插槽、Markdown 渲染器、通知和本地状态扩展终端 UI。TUI 插件是[插件包](../index.md)的 `./tui` 部分，通常与[服务器端部分](../server/index.md)放在一起。

```ts title="src/tui.tsx"
import { Plugin } from "@opencode/plugin/tui"

export default Plugin.define({
  id: "acme.cli",
  setup(context) {
    context.ui.toast.show({ message: "TUI plugin loaded", variant: "success" })
  },
})
```

直接导入 `@opencode/plugin/tui`。OpenCode 在运行时解析这个导入，因此本地 TUI 插件不需要指向 OpenCode 源码检出目录的绝对路径。

## 上下文

`setup` 接收配置、应用元数据、当前位置、OpenCode 客户端、缓存数据、主题 token、OpenTUI 渲染器，以及下文记录的 UI API。

```ts
setup(context) {
  const compact = context.options.compact === true
  const location = context.location ?? context.data.location.default()
  const version = context.app.version
  const channel = context.app.channel
  const client = context.client
  const renderer = context.renderer
  const theme = context.theme
}
```

返回一个清理函数，用于插件所拥有的资源。

```ts
setup(context) {
  const stop = context.data.on("session.execution.succeeded", () => {})
  return () => stop()
}
```

## 客户端

`context.client` 是生成的 OpenCode 客户端，可以调用所连接的服务器，包括远程服务器。

```ts
const response = await context.client.plugin.list({
  location: context.location ?? context.data.location.default(),
})
const plugins = response.data
```

## 事件

使用 `data.on` 监听单个类型化事件，或使用 `data.listen` 监听所有服务器事件；两者都返回一个取消订阅函数。

```ts
const stopPermission = context.data.on("permission.asked", (event) => {
  context.ui.toast.show({ message: `Permission ${event.data.id}` })
})
const stopAll = context.data.listen(({ details }) => console.log(details.type))

return () => {
  stopPermission()
  stopAll()
}
```

## 会话

会话数据暴露列表、查找、层级、成本、状态、同步和失效等接口。

```ts
const sessions = context.data.session.list()
const session = context.data.session.get(sessionID)
const rootID = context.data.session.root(sessionID)
const familyIDs = context.data.session.family(sessionID)
const cost = context.data.session.cost(sessionID)
const status = context.data.session.status(sessionID)
await context.data.session.sync(sessionID)
context.data.session.invalidate(sessionID)
```

待处理的收件箱条目和消息具有列表、查找、同步和失效 API。

```ts
await context.data.session.pending.sync(sessionID)
const pending = context.data.session.pending.list(sessionID)
context.data.session.pending.invalidate(sessionID)

await context.data.session.message.sync(sessionID)
const messages = context.data.session.message.list(sessionID)
const message = context.data.session.message.get(sessionID, messageID)
context.data.session.message.invalidate(sessionID)
```

权限请求可以按会话读取和刷新。

```ts
await context.data.session.permission.sync(sessionID)
const requests = context.data.session.permission.list(sessionID) ?? []
context.data.session.permission.invalidate(sessionID)
```

表单可以在某个位置被列出、刷新、回复或取消。

```ts
import type { SessionFormCancelInput, SessionFormReplyInput } from "@opencode/client"

async function handleForm(reply: SessionFormReplyInput, cancel: SessionFormCancelInput) {
  const location = context.location
  await context.data.session.form.sync(sessionID, location)
  const forms = context.data.session.form.list(sessionID, location) ?? []
  await context.data.session.form.reply(reply, location)
  await context.data.session.form.cancel(cancel, location)
  context.data.session.form.invalidate(sessionID, location)
}
```

## 项目与 shell

项目和已保存的权限支持列表、查找、同步和失效操作。

```ts
await context.data.project.sync()
const projects = context.data.project.list()
const project = context.data.project.get(projectID)
context.data.project.invalidate()

await context.data.project.permission.sync(projectID)
const saved = context.data.project.permission.list(projectID) ?? []
context.data.project.permission.invalidate(projectID)
```

shell 数据支持位置作用域的列表、查找、同步和失效操作。

```ts
await context.data.shell.sync(context.location)
const shells = context.data.shell.list(context.location)
const shell = context.data.shell.get(shellID)
context.data.shell.invalidate(context.location)
```

## 位置数据

位置状态暴露默认位置和刷新控制。

```ts
const location = context.data.location.default()
await context.data.location.sync(location)
context.data.location.invalidate(location)
```

版本控制状态在某个位置暴露仓库信息。

```ts
await context.data.location.vcs.sync(context.location)
const vcs = context.data.location.vcs.info(context.location)
const branch = vcs?.branch.current
context.data.location.vcs.invalidate(context.location)
```

agent、命令、集成、模型、provider、引用、技能和 MCP 数据共享 `list`、`sync` 和 `invalidate` 方法。

```ts
const location = context.location
await Promise.all([
  context.data.location.agent.sync(location),
  context.data.location.command.sync(location),
  context.data.location.integration.sync(location),
  context.data.location.model.sync(location),
  context.data.location.provider.sync(location),
  context.data.location.reference.sync(location),
  context.data.location.skill.sync(location),
  context.data.location.mcp.server.sync(location),
  context.data.location.mcp.resource.sync(location),
])

const agents = context.data.location.agent.list(location) ?? []
const commands = context.data.location.command.list(location) ?? []
const integrations = context.data.location.integration.list(location) ?? []
const models = context.data.location.model.list(location) ?? []
const providers = context.data.location.provider.list(location) ?? []
const references = context.data.location.reference.list(location) ?? []
const skills = context.data.location.skill.list(location) ?? []
const servers = context.data.location.mcp.server.list(location) ?? []
const resources = context.data.location.mcp.resource.list(location) ?? []

context.data.location.model.invalidate(location)
```

## 注意提醒（Attention）

注意提醒请求可以显示系统通知、播放配置的声音，或根据终端焦点状态两者都做。

```ts
const result = await context.attention.notify({
  title: "OpenCode",
  message: "Session done",
  notification: { when: "blurred" },
  sound: { name: "done", volume: 0.5, when: "always" },
})
console.log(result.ok, result.notification, result.sound, result.skipped)
```

## 主题与渲染器

在 OpenTUI 元素中使用语义化的主题 token，并将 `context.renderer` 传递给特定渲染器的辅助函数。

```tsx
const Status = () => <text fg={context.theme.text.base}>Ready</text>
const renderer = context.renderer
```

渲染器绘制的 OpenTUI 资源需要 `context.renderer.nativeScene` 作为其所有者。例如，`<markdown>` 和 `<code>` 需要一个 `SyntaxStyle`。在渲染器空闲时、即绘制它的最后一帧之后，销毁该资源。

```tsx
import { SyntaxStyle } from "@opentui/core"

const style = SyntaxStyle.fromStyles({ default: { fg: context.theme.text.base } }, context.renderer.nativeScene)
context.ui.slot({ append: "home.footer", render: () => <markdown content="Ready" syntaxStyle={style} /> })
return () => context.renderer.idle().then(() => style.destroy())
```

要读取一个可渲染元素的布局样式，请以 Yoga Node getter 的名称调用相应方法，例如 `box.getPadding(Yoga.Edge.Bottom)` 或 `box.getMaxWidth()`。宿主的可渲染元素不属于插件 API 的一部分，其结构和样式可能在任何版本中变化。

### 为 OpenTUI 0.5 构建的插件

OpenCode 使用它自带的 OpenTUI 运行插件。自 OpenTUI 0.6 起：

- `SyntaxStyle.create()`、`SyntaxStyle.fromStyles()`、`SyntaxStyle.fromTheme()`、`TextBuffer.create()` 和 `EditBuffer.create()` 把所有者作为最后一个参数；`OptimizedBuffer.create()` 则在 `owner` 选项中接收它。请传入 `context.renderer.nativeScene`。OpenTUI 0.5 会忽略这个额外参数，因此插件在较旧的 OpenCode 版本上仍能运行。
- 来自 `@opencode/theme/tui` 的 `generateSyntax()` 把所有者作为第二个参数：`generateSyntax(context.theme, context.renderer.nativeScene)`。较旧的 `@opencode/theme` 版本构建样式时不带所有者，因此也要更新该包。
- `getLayoutNode()` 已被移除。在 OpenTUI 0.6.5 及更高版本上，把 `getLayoutNode().getMaxWidth()` 和其他样式 getter 替换为同名的可渲染元素方法。把 `getComputedLayout()` 和其他计算出的位置与大小 getter 替换为 `getLayout()`，把 `markDirty()` 替换为 `invalidateIntrinsicSize()`。计算出的 padding、margin 和 border 没有替代品，`getPadding(edge)` 只读取为该边设置的 padding。要恢复某个 getter 报告为未设置（`Unit.Undefined`）的样式，请给该属性赋值 `undefined`，适用于 OpenTUI 0.6.6 及更高版本。

[OpenTUI 0.6.0 发布说明](https://opentui.com/docs/releases/0.6.0)列出了每一项变化。

## Solid 组件

在路由、对话框或插槽渲染的 JSX 中，使用 `usePlugin` 访问当前上下文。

```tsx
import { usePlugin } from "@opencode/plugin/tui"

function Status() {
  const context = usePlugin()
  return <text fg={context.theme.text.base}>{context.app.version}</text>
}
```

## Markdown

按语言注册围栏代码渲染器；返回的函数用于注销它。

```ts
const unregister = context.markdown.registerCodeBlockRenderer("acme", (_token, render) => render.defaultRender())
return unregister
```

## 命令与按键映射

在响应式的按键映射层中注册面板命令、斜杠命令和键盘命令。

```ts
context.keymap.layer(() => ({
  mode: "global",
  priority: 10,
  commands: [
    {
      id: "acme.status",
      title: "Show Acme status",
      group: "Acme",
      bind: "ctrl+g",
      palette: true,
      slash: { name: "acme", aliases: ["status"], arguments: true },
      enabled: () => true,
      suggested: true,
      run: async (input) => context.ui.toast.show({ message: input ?? "Ready" }),
    },
  ],
  bindings: ["acme.status"],
}))
```

可以从 `setup` 调用 `layer`，包括在 `await` 之后调用，也可以从组件中调用。每个层在以下情况中最早发生的一种时被移除：

- 插件被禁用、重载或 setup 失败。
- 创建它的组件或响应式计算（例如插槽、路由或对话框）被销毁。

层工厂必须是纯函数。OpenCode 会先不带依赖跟踪地求值一次，以验证初始命令形态，然后再以响应式方式求值。初始命令形态错误（例如面板命令缺少 ID）会从 `layer()` 抛出。绑定解析错误由 OpenTUI 处理。后续响应式更新产生的错误遵循 Solid 的错误处理机制。

```ts
async setup(context) {
  const settings = await loadSettings()
  context.keymap.layer(() => ({
    mode: "global",
    commands: [{ id: "acme.sync", title: "Sync Acme", palette: true, run: () => sync(settings) }],
  }))
}
```

一个层可以指定一个 OpenTUI 可渲染元素作为目标，并且命令可以返回 `false` 以继续键盘分发。

```ts
context.keymap.layer(() => ({
  target: () => panel,
  commands: [{ bind: "escape", run: (_input, event) => (event ? false : undefined) }],
}))
```

分发命令、检查快捷键和命令状态，或推入一个临时输入模式。

```ts
context.keymap.dispatch("acme.status", "verbose")
const shortcuts = context.keymap.shortcuts("acme.status")
const commands = context.keymap.commands()
const pending = context.keymap.pending()
const active = context.keymap.active()
const currentMode = context.keymap.mode.current()
const popMode = context.keymap.mode.push("acme-search")
popMode()
```

## 存储

持久化存储在重启后保留 JSON，并在多个 TUI 实例之间同步。

```ts
const [settings, updateSettings] = context.storage.store("settings", {
  initial: { compact: false },
})
await updateSettings((draft) => {
  draft.compact = true
})
```

内存存储在插件重载后保留，但在 TUI 退出时被丢弃。

```ts
const [state, updateState] = context.storage.memory("state", {
  initial: { count: 0 },
})
updateState((draft) => {
  draft.count++
})
```

## 对话框与提示条

使用基于 Promise 的对话框实现警告、确认、文本输入和选择。

```ts
await context.ui.dialog.alert({ title: "Acme", message: "Ready" })
const confirmed = await context.ui.dialog.confirm({
  title: "Continue?",
  message: "Run the Acme action?",
  label: { confirm: "Run", cancel: "Cancel" },
})
const name = await context.ui.dialog.prompt({ title: "Name", placeholder: "release" })
const mode = await context.ui.dialog.select({
  title: "Mode",
  current: "safe",
  options: [
    { title: "Safe", value: "safe", description: "Ask before changes" },
    { title: "Fast", value: "fast", disabled: false, category: "Advanced" },
  ],
})
```

### 选择搜索

传入 `search` 可以自定义匹配逻辑和结果顺序。它会对每个查询运行，包括空查询，并且只接收已启用的选项。结果按返回顺序列出，每个类别内联显示。

```ts
const project = await context.ui.dialog.select({
  title: "Projects",
  options: [
    { title: "Alpha", value: "alpha", category: "Recent" },
    { title: "Beta", value: "beta", category: "Pinned" },
  ],
  search: (query, options) =>
    options
      .filter((option) => option.title.toLowerCase().includes(query.toLowerCase()))
      .toSorted((left, right) => right.title.localeCompare(left.title)),
})
```

### 选择操作

操作显示在页脚，可以通过其键盘绑定、点击、或 Tab 聚焦后按 Enter 来运行。默认情况下，它们接收选中的值，并且在没有选择时不可用。对于不需要选择的操作，使用 `selection: "none"`。

```ts
await context.ui.dialog.select({
  title: "Projects",
  options: [{ title: "Alpha", value: "alpha" }],
  actions: [
    { bind: "ctrl+o", title: "Inspect", onTrigger: (value) => context.ui.toast.show({ message: value }) },
    { bind: "ctrl+a", title: "Close", side: "right", selection: "none", onTrigger: () => context.ui.dialog.clear() },
  ],
})
```

- 操作不会关闭对话框，也不会敲定 promise。
- Enter 或点击某个选项会以选中的值完成解析。
- Escape、`clear()` 或显示另一个对话框会以 `undefined` 完成解析。
- 不要绑定 `ctrl+n` 或 `ctrl+p`。对话框为导航保留了它们，并且其自身的绑定优先。

自定义 JSX 对话框可以设置自身大小并自行关闭。

```tsx
context.ui.dialog.set({ size: "large", centered: true })
context.ui.dialog.show(
  () => (
    <box>
      <text>Acme</text>
    </box>
  ),
  () => console.log("closed"),
)
context.ui.dialog.clear()
```

提示条支持标题、消息、变体和时长。

```ts
context.ui.toast.show({
  title: "Acme",
  message: "Saved",
  variant: "success",
  duration: 3000,
})
```

## 路由与标签页

注册一个 JSX 路由，检查当前路由，并导航到主页、某个会话或插件页面。

```tsx
const unregister = context.ui.router.register({
  name: "dashboard",
  render: ({ data }) => <text>{String(data?.title ?? "Acme")}</text>,
})
const current = context.ui.router.current()
context.ui.router.navigate({ type: "plugin", name: "dashboard", data: { title: "Status" } })
context.ui.router.navigate({ type: "session", sessionID })
context.ui.router.navigate({ type: "home" })
return unregister
```

当会话标签页功能启用时，标签页可以被列出、打开、聚焦、移动和关闭。`open` 不改变焦点；`focus` 会在需要时打开标签页。

```ts
if (context.ui.tabs.enabled()) {
  context.ui.tabs.open(backgroundSessionID)
  context.ui.tabs.focus(sessionID)
  const tabs = context.ui.tabs.list()
  context.ui.tabs.move(backgroundSessionID, tabs.length - 1)
  context.ui.tabs.close(sessionID)
  context.ui.tabs.close()
}
```

## 模型

读取提示词选定的模型并更改其变体。在 Solid 计算中读取时，`current()` 和 `variant.list()` 是响应式的。`variant` 为 `undefined` 表示模型默认值。

```ts
const selected = context.ui.model.current()
const variants = context.ui.model.variant.list()
context.ui.model.variant.set("high")
context.ui.model.variant.set(undefined)
```

当没有选中模型或模型没有该变体时，`variant.set` 返回 `false`。把它绑定到一个命令，可以替换内置的变体循环，例如跳过模型默认值：

```ts
context.keymap.layer(() => ({
  commands: [
    {
      id: "acme.variant.cycle",
      title: "Cycle variants",
      bind: "tab",
      run() {
        const variants = context.ui.model.variant.list()
        if (variants.length === 0) return
        const index = variants.indexOf(context.ui.model.current()?.variant ?? "")
        context.ui.model.variant.set(variants[(index + 1) % variants.length])
      },
    },
  ],
}))
```

## 插槽（Slots）

插槽在 `app`、`home.footer`、`home.footer.status`、`prompt.footer`、`prompt.footer.status`、`prompt.footer.file`、`session.composer.top`、`sidebar.content` 或 `sidebar.footer` 处插入或替换 JSX。

```tsx
return context.ui.slot({
  append: "sidebar.content",
  render: ({ sessionID }) => <text>{context.data.session.get(sessionID)?.title}</text>,
})
```

使用 `prepend`、`append`、`before`、`after` 或 `replace` 指定放置方式。

```tsx
context.ui.slot({ prepend: "home.footer", render: () => <text>Before footer content</text> })
context.ui.slot({ append: "home.footer", render: () => <text>After footer content</text> })
context.ui.slot({ before: "home.footer", render: () => <text>Before footer slot</text> })
context.ui.slot({ after: "home.footer", render: () => <text>After footer slot</text> })
context.ui.slot({ replace: "home.footer", render: () => <text>New footer</text> })
```

使用 `home.footer.status` 可以向内置的页脚行添加内容而不替换它。状态贡献显示在 OpenCode 的健康指示器之后、版本号之前。

```tsx
context.ui.slot({ append: "home.footer.status", render: () => <text>SYNCED</text> })
```

### 会话面板

向 `session.panel` 注册一个贡献，然后通过命令打开面板。宿主负责大小、焦点和全屏呈现；插件负责其内容。选中的名称会作为 `panel.name` 传递给每个贡献，由每个贡献自行决定是否渲染。

```tsx
import { Show } from "solid-js"

context.ui.slot({
  append: "session.panel",
  render: (panel) => (
    <Show when={panel.name === "acme.review"}>
      <ReviewPanel panel={panel} />
    </Show>
  ),
})

context.ui.slot({
  append: "app",
  render: () => {
    context.keymap.layer(() => ({
      mode: "global",
      commands: [
        {
          id: "acme.review",
          title: "Open review",
          slash: { name: "review" },
          run: () => {
            context.ui.panel.open("acme.review")
          },
        },
      ],
    }))
    return null
  },
})
```

- 在会话之外打开会返回 `false`。
- 这是一个普通的插槽：全部五种放置方式和现有的替换顺序规则都适用。
- 对可以独立选择的贡献使用 `append`，使它们能够共存。`replace` 仍然会接管整个插槽。
- 名称是共享的选择值，而不是已注册的所有权声明。使用带插件前缀的名称（例如 `acme.review`）以避免冲突。打开一个没有匹配渲染器的名称会让插槽保持为空。
- 更改呈现方式会保留已挂载的贡献。关闭面板会销毁它们；禁用插件会通过正常的插槽清理机制移除其贡献。
- 它的键盘层和输入模式只在面板拥有输入时生效。

插槽接收响应式的 `name`、`sessionID`、`width`、`presentation` 和 `focused` 属性，外加 `focus`、`close` 和 `toggleFullscreen` 动作。宿主让窄终端保持全屏；在空间足以容纳侧面板之前，`toggleFullscreen` 不起作用。

```tsx
import type { PanelInput } from "@opencode/plugin/tui/context"
import { usePlugin } from "@opencode/plugin/tui"

function ReviewPanel(props: { panel: PanelInput }) {
  const context = usePlugin()
  context.keymap.layer(() => ({
    commands: [
      {
        id: "acme.review.fullscreen",
        bind: "f",
        run: props.panel.toggleFullscreen,
      },
    ],
  }))
  return <text>Reviewing {props.panel.sessionID}</text>
}
```

你可以请求初始的全屏呈现，检查自己当前活跃的面板，或关闭它而不影响其他插件的面板。

```ts
context.ui.panel.open("acme.review", { presentation: "fullscreen" })
const current = context.ui.panel.current()
context.ui.panel.close()
```

## 格式化

格式化文件系统路径以便显示，包括主目录缩写。

```ts
const displayPath = context.ui.format.path(context.location?.directory ?? "/home/me/project")
```

## 发布与加载

通过 `./tui` 暴露 TUI 插件；当插件渲染 JSX 时，添加 OpenTUI 对等依赖。

```json title="package.json"
{
  "name": "opencode-acme-plugin",
  "type": "module",
  "exports": {
    ".": "./src/index.ts",
    "./tui": "./src/tui.tsx"
  },
  "dependencies": {
    "@opencode/plugin": "latest"
  },
  "peerDependencies": {
    "@opentui/core": ">=0.6.6",
    "@opentui/solid": ">=0.6.6",
    "solid-js": ">=1.9.0"
  }
}
```

在[服务器端部分](../server/index.md)或 [GUI 部分](../gui/index.md)旁边导出 `./tui`，即可被自动加载。

```ts title="src/index.ts"
import { Plugin } from "@opencode/plugin"

export default Plugin.define({
  id: "acme.server",
  setup() {},
})
```

在 [`cli.json`](../../../cli/plugins/index.md) 中配置仅 TUI 的包，使其在连接远程服务器时保持启用。

```json title="cli.json"
{
  "plugins": ["opencode-acme-plugin"]
}
```
