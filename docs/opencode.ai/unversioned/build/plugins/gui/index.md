---
source_url: https://opencode.ai/docs/build/plugins/gui/
source_hash: sha256:3446119f57563a03759ca16f6aa8c48dce1a17adfc7babf415f965cb6e7e98ea
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# GUI

GUI 插件通过 GUI 插件 SDK `@opencode/plugin/gui` 为 OpenCode Desktop 添加面板、命令、设置页面和原生集成。它是[插件包](../index.md)中的 `./gui-experimental` 部分，可以单独存在，也可以与[服务器部分](../server/index.md)和 [TUI 部分](../cli/index.md)并列。

<Callout type="note">
  GUI 插件 API 是实验性的，可能在版本之间变化。`-experimental` 导出名在你的包中就说明了这一点。
</Callout>

`./gui-experimental` 文件默认导出 `Plugin.define`，与服务器部分和 TUI 部分一样：

```tsx title="src/gui.tsx"
import { Command, Plugin } from "@opencode/plugin/gui"
import { Acme } from "./rpc"

export default Plugin.define({
  i18n: { en: { "command.open": "Open Acme" } },
  setup(ctx) {
    ctx.add(Command, () => ({
      id: "open",
      title: ctx.t("command.open"),
      run: () => void ctx.client.rpc(Acme).open({}),
    }))
  },
  main(ctx) {
    ctx.log.write("info", "acme started")
  },
})
```

GUI 插件可以在两个进程中运行：

- **`setup`** 在每个桌面应用窗口中运行。它贡献面板、命令、设置页面、槽位、服务器来源、链接处理器和样式。参见[窗口](#窗口)。
- **`main`** 在 Electron 主进程中运行一次。它提供类型化的 `Ipc` 契约、原生菜单项、`WebContentsView` 嵌入以及 Node 与 Electron 集成。参见[主进程](#主进程)。

## 包

一个插件包可以用同一个 npm 包同时提供服务器、TUI 和 GUI 代码。在 `./tui` 旁边加一个 `./gui-experimental` 导出，OpenCode Desktop 就会在自己的后台服务器上为每个插件加载它。

```json title="package.json"
{
  "name": "opencode-acme-plugin",
  "type": "module",
  "exports": {
    ".": "./src/index.ts",
    "./tui": "./src/tui.tsx",
    "./gui-experimental": "./dist/gui-experimental.cjs"
  },
  "dependencies": {
    "@opencode/plugin": "latest"
  },
  "devDependencies": {
    "solid-js": "^1.9.0",
    "vite": "^7.0.0",
    "vite-plugin-solid": "^2.11.0"
  }
}
```

用户像安装其他插件一样安装它；没有单独的 GUI 安装步骤。

```jsonc title="opencode.jsonc"
{
  "plugins": ["opencode-acme-plugin"],
}
```

GUI 不声明 id：它取插件的 id，即服务器部分的 `id`；对于没有服务器部分的包，则取包名（没有 `name` 的本地目录使用目录名）。通过 `ctx.id` 读取它。

### 一个文件，两个进程

每个进程都会求值整个 `./gui-experimental` 文件并读取其默认导出。窗口运行 `setup`，桌面应用的主进程运行 `main`。

```tsx title="src/gui.tsx"
import { shell } from "electron"
import { Plugin } from "@opencode/plugin/gui"

export default Plugin.define({
  setup(ctx) {
    // Window code: Solid components, ctx.layout, ctx.add(Command, …).
  },
  main(ctx) {
    // Main code: electron, Node built-ins, ctx.windows.
    ctx.windows.on("open", () => shell.beep())
  },
})
```

因为两个进程求值同一个文件，每一方都会为另一方的模块准备惰性占位符：

- **在窗口中**，`electron` 和 Node 内置模块是惰性占位符。
- **在主进程中**，Solid 和仅窗口可用的模块是惰性占位符。

占位符接受模块作用域上的任何属性读取、调用或构造，例如 Solid 的提升模板或打包器提升的 `require` 调用。把每个进程的代码放在各自的 setup 内：跑错进程的代码只会拿到占位符，而不是可用的值。

`Plugin.define` 和契约助手在两个进程中来自同一个 SDK。在主进程中，`@opencode/plugin/gui` 解析为主 SDK，它导出同样的 `Plugin`、`Store`、`Ipc`、`Contract` 和 `Registry`。一份定义同时服务两个进程。它仅窗口可用的导出，如 `Command`、`bindPlugin` 和 `createKeyed`，在主进程中是 `undefined`，因此只在 `setup` 内使用它们。

## 构建产物

`./gui-experimental` 必须是一个预构建好的 CommonJS 文件。用 `@opencode/plugin/gui/vite` 提供的 Vite 预设来构建：

```ts title="vite.config.ts"
import { defineConfig } from "vite"
import { gui } from "@opencode/plugin/gui/vite"

export default defineConfig({ plugins: [gui()] })
```

```bash
vite build
```

该预设做以下事情：

- 用 `vite-plugin-solid` 编译 Solid JSX。
- 产出一个 CommonJS 文件，并内联所有动态 `import()`，因为应用无法加载第二个 chunk。
- 把应用的[共享模块](#共享模块)、Electron 和 Node 内置模块保持为外部依赖，其余依赖全部打包。
- 遇到任何其他 `effect/*`、`solid-js/*` 或 `@opencode/*` 模块时构建失败。应用不提供它，打包出来的副本也不会共享应用的实例。

```text
effect/Schema is not a module the OpenCode app provides to plugin GUIs: effect, @opencode/plugin/gui, …
```

改为从共享入口导入，例如 `import { Schema } from "effect"`。

### 预设选项

给 `gui()` 传选项可以更改入口或输出文件。

```ts title="vite.config.ts"
export default defineConfig({ plugins: [gui({ entry: "src/desktop.tsx", outFile: "dist/desktop.cjs" })] })
```

- `entry` 是默认导出 `Plugin.define` 的文件。默认为 `src/gui.tsx`。
- `outFile` 是 `./gui-experimental` 导出指向的产物。默认为 `dist/gui-experimental.cjs`。

#### 参考

```ts
function gui(options?: GuiOptions): Plugin[]

interface GuiOptions {
  entry?: string
  outFile?: string
}
```

### 依赖

把构建工具加入 devDependencies。应用在运行时提供 `@opencode/plugin/gui`，因此产物只需要 `@opencode/plugin` 依赖中的类型。

```bash
bun add -d vite vite-plugin-solid solid-js
```

`main` 中的 Electron 和 Node 类型，还需要加上 `electron` 和 `@types/node`：

```bash
bun add -d electron @types/node
```

### 共享模块

每个进程都会向产物提供这些模块。请求一个任何进程都不提供的模块，会导致插件的 GUI 失败。

```ts
import { Schema } from "effect" // Both processes
import { createSignal } from "solid-js" // Windows; an inert placeholder in the main process
import { readFile } from "node:fs/promises" // The main process; an inert placeholder in windows
```

- **两个进程都有**：`effect`、`@opencode/plugin/gui`、`@opencode/plugin/gui/main`、`@opencode/plugin/rpc`、`@opencode/schema/rpc`、`@opencode/client` 和 `@opencode/client/effect`。
- **仅窗口有**：`solid-js`、`solid-js/web`、`solid-js/store`、`@opencode/client/solid` 和 `@opencode/plugin/gui/{file,review,browser}`。主进程拿到的是惰性占位符。
- **仅主进程有**：`electron` 和 Node 内置模块（如 `node:fs`）。窗口拿到的是惰性占位符。

## GUI 入口在哪里加载

OpenCode Desktop 从它自己的后台服务器加载 GUI 入口，而该服务器已经在加载你配置中的插件，因此它们不会引入新的代码来源。在全局 `opencode.json(c)` 中配置插件，即可让它的 GUI 在每个窗口可用。

<Callout type="note">
  TUI 从 `cli.json` 读取它的插件，但桌面应用只读 `opencode.json(c)`。一个只提供 TUI 部分、且用户列在 `cli.json` 中的包，一旦加上 `./gui-experimental`，也必须列进 `opencode.json(c)`。
</Callout>

桌面应用的主进程从它自己的服务器列出插件并读取其产物，使用的凭证只有它自己持有，并把同样的集合发给窗口。窗口无法提供主进程代码。

服务器部分加载失败的插件没有 GUI。

## 重新加载与更新

从本地目录加载插件，并在每次变更时重新构建：

```bash
vite build --watch
```

- `package.json` 带 `name` 和 `exports` 的本地目录会通过它们解析 `./gui-experimental`。没有它们时，加载其根目录下的 `gui-experimental.cjs`（或 `.js`）。入口必须是 `.cjs` 或 `.js`；其他文件会被忽略。
- 每次重新构建都会在每个窗口和主进程中重新加载插件的 GUI。服务器入口不会重启。
- 已安装包的 GUI 只随其版本变化。
- 在 `opencode.json(c)` 中更改插件的 `options` 会重新加载插件。
- `opencode plugin update` 会在更新完成后替换包的 GUI。
- [**Settings > Extensions > Plugins**](../../../plugins/index.md#desktop) 会列出该插件，并带一个可以关闭其 GUI 的开关。要移除它，把它从 `opencode.json(c)` 中删掉，或运行 `opencode plugin remove <package>`。

<Callout type="note">
  应用自带的插件保留了它们的 id。如果你的插件 id 是其中之一、以 `.` 嵌套在某个之下、有别的 id 嵌套在它之下，或位于 `opencode` 命名空间中，它的 GUI 不会加载，并且 **Settings > Extensions > Plugins** 会把它列为未加载。
</Callout>

## 定义 GUI 插件

`Plugin.define` 声明插件运行的系统、其存储的窗口状态，以及它的文案。宿主会在任一 setup 运行之前读取这些声明。

```ts title="src/gui/definition.ts"
import { Schema } from "effect"
import { Plugin, Store } from "@opencode/plugin/gui"

export const definition = Plugin.define({
  os: ["macos", "linux"],
  stores: {
    prefs: Store.global(Schema.Struct({ enabled: Schema.Boolean }), { enabled: true }),
  },
  i18n: {
    en: { title: "Acme", "command.open": "Open Acme" },
    de: { title: "Acme", "command.open": "Acme öffnen" },
  },
})
```

- 宿主给插件 id，即 `ctx.id`：服务器部分的 `id`；对于没有服务器部分的包则是包名（没有 `name` 的本地目录用目录名）。它会作为插件创建的所有 id 的前缀：命令（`<id>.<command>`）、面板键（`<id>:<tab>`）、存储键（`plugin.<id>.<key>`），以及它提供的[契约与 Ipc](#契约与-token) 的 id。
- `os` 把插件限定在某些操作系统上。省略它则在每个 OS 上运行。`os` 不包含当前系统的插件不会运行，并且 **Settings > Extensions > Plugins** 会保留它的行并显示 "Not available on this system."
- `stores` 为窗口声明[存储状态](#存储状态)。通过 `ctx.stores.<key>` 读取。
- `i18n` 按语言存放文案。每种语言都内联写全；英文会填补任何语言缺少的键。用 `ctx.t(key, params)` 和 `ctx.plural(key, count)` 读取。在窗口中，`ctx.t` 还会读取应用的共享键，例如 `common.*`。在 `main` 中，缺失的键返回键名本身。
- 定义 `setup`、`main` 或两者。两者都没有的 GUI 无法加载。
- 没有 setup 时，`Plugin.define` 会把声明作为 `Plugin.Declarations` 返回，因此其他文件中的 setup 可以根据它们获得类型。`Plugin.Definition` 是完整定义的类型。
- 插件不声明它提供或使用的契约。它在运行时提供和读取它们；参见[契约与 token](#契约与-token)。

#### 参考

```ts
interface Declarations {
  os?: ("macos" | "windows" | "linux")[]
  stores?: Record<string, StoreDeclaration>
  i18n?: { en: Messages; [locale: string]: Messages }
}

interface Definition extends Declarations {
  setup?(ctx: SetupContext<this>): Cleanup | void
  main?(ctx: MainContext): Cleanup | void | Promise<Cleanup | void>
}

type Messages = Record<string, string>

type Cleanup = () => void | Promise<void>
```

### 拆分到多个文件

小的 GUI 插件可以放在 `src/gui.tsx` 里。更大的插件应在 `definition.ts` 中声明插件，把共享 token 放进 `contract.ts`，每个 setup 写在各自的文件里，然后在 `src/gui.tsx` 中组合。

```text
src/
├── index.ts            Server part: Plugin.define from @opencode/plugin
├── rpc.ts              RPC contract between the server part and its clients
├── gui.tsx             ./gui-experimental entry: export default Plugin.define({ ...definition, setup, main })
└── gui/
    ├── definition.ts   Plugin.define: os, stores, i18n
    ├── contract.ts     Tokens other code may import: Ipc, Contract, Registry
    ├── window.tsx      Window setup: Plugin.Setup<typeof definition>
    ├── main.ts         Main setup: Plugin.MainSetup (desktop only)
    ├── page.tsx        Components that panels and pages render
    └── i18n/en.ts      English copy
```

窗口启动时会求值整个 `./gui-experimental` 文件，因此保持模块作用域和 `setup` 轻量。在这里注册贡献，把昂贵的工作放进组件、`createKeyed` 或 `createLatest` 中。

对于更大的插件，先声明插件，再从声明为每个 setup 提供类型，然后用它们定义插件。

```ts title="src/gui/definition.ts"
import { Schema } from "effect"
import { Plugin, Store } from "@opencode/plugin/gui"

export const definition = Plugin.define({
  stores: { notes: Store.global(Schema.Struct({ count: Schema.Number }), { count: 0 }) },
})
```

```tsx title="src/gui/window.tsx"
import type { Plugin } from "@opencode/plugin/gui"
import { Notes } from "./contract"
import type { definition } from "./definition"

export const setup: Plugin.Setup<typeof definition> = (ctx) => {
  ctx.provide(Notes, { count: () => ctx.stores.notes.value.count })
}
```

```ts title="src/gui/main.ts"
import type { Plugin } from "@opencode/plugin/gui"

export const main: Plugin.MainSetup = (ctx) => {
  ctx.log.write("info", "acme started")
}
```

```tsx title="src/gui.tsx"
import { Plugin } from "@opencode/plugin/gui"
import { definition } from "./gui/definition"
import { main } from "./gui/main"
import { setup } from "./gui/window"

export default Plugin.define({ ...definition, setup, main })
```

- `Plugin.Setup<typeof definition>` 是窗口 setup 的类型。它根据声明的 store 为 `ctx.stores` 提供类型。
- `Plugin.MainSetup` 是 main setup 的类型，`Plugin.Cleanup` 是任一 setup 可以返回的清理函数的类型。
- 从 `@opencode/plugin/gui` 导入注册表、token 和助手，例如 `Command`、`SettingsPage`、`Panel`、`Slot`、`Contract`、`Ipc`、`Registry`、`Store`、`createKeyed`、`usePlugin` 和 `bindPlugin`。
- 仅主进程可用的注册表（如 `MenubarItem`）从 `@opencode/plugin/gui/main` 导入。

## 共享上下文

两个 setup 都会收到插件选项、OpenCode 服务器的客户端和应用元数据，与服务器部分和 TUI 部分一样。

### 选项

`ctx.options` 存放插件在 `opencode.json(c)` 条目中的 `options`：与服务器部分拿到的值相同。

```jsonc title="opencode.jsonc"
{
  "plugins": [{ "package": "opencode-acme-plugin", "options": { "team": "core" } }],
}
```

```ts
setup(ctx) {
  const team = ctx.options.team
}
```

- 更改选项会重新加载插件。

### 服务器客户端

`ctx.client` 是运行该插件的服务器的 OpenCode 客户端：桌面应用自己的服务器。用它通过 [RPC](../rpc/index.md) 调用你的服务器部分。

```ts
import { Command } from "@opencode/plugin/gui"
import { Acme } from "./rpc"

ctx.add(Command, () => ({
  id: "search",
  title: ctx.t("command.search"),
  run: async () => {
    const result = await ctx.client.rpc(Acme).search({ query: "todo" })
    console.log(result)
  },
}))
```

- 在调用处读取 `ctx.client`。该服务器重启之后它会变化。
- 服务器不可达时，每次调用都会 reject。

### 应用元数据

`ctx.app` 描述正在运行的应用。

```ts
if (!ctx.app.packaged) console.log(`Acme on ${ctx.app.name} ${ctx.app.version} (${ctx.app.channel})`)
```

- `name` 是 `"opencode"`，与服务器插件的 `ctx.app.name` 一样。
- 在 Electron 应用和 `main` 中，`platform` 是 `"desktop"`；在浏览器标签页中是 `"web"`。
- 当桌面应用以打包方式运行时，`packaged` 为 `true`。在 web 上始终为 `false`。
- 服务器插件拿到 `name`、`version` 和 `channel`；TUI 插件拿到 `version` 和 `channel`。

#### 参考

```ts
interface App {
  name: string
  version: string
  channel: "local" | "dev" | "beta" | "prod"
  platform: "web" | "desktop"
  packaged: boolean
}
```

## 契约与 token

token 让 GUI 插件能够跨进程以及彼此之间通信，而无需导入对方的运行时代码。把每个 token 放进 `contract.ts`。token 只持有它的种类和 id，外加一个 `Ipc` 的 schema，因此其他插件可以在不导入你的运行时代码的情况下导入它。

- `ctx.provide(token, impl)` 提供你自己的某个 token：来自窗口 setup 的 `Contract`，或来自 `main` 的 `Ipc`。
- `ctx.use(token)` 跟随另一个插件提供的契约或 `Ipc`。它返回一个 [`Live`](#live-依赖与失败处理) 访问器。
- `ctx.main(ipc)` 返回你自己的 `main` 提供的某个 `Ipc` 的客户端。

插件只能提供 id 等于自身 id 或以其为前缀的 token，形如 `<id>.<name>`。对其他 id，`ctx.provide` 会抛错，`ctx.main` 对不在你的 id 之下的 `Ipc` 会抛错。本页示例使用插件 id `acme`，因此它们的 token id 以 `acme.` 开头。

```ts
Contract.define<AcmeBadge, "acme.badge">("acme.badge") // Plugin acme can provide it.
Contract.define<AcmeBadge, "badge">("badge") // ctx.provide throws in plugin acme.
```

### 契约

当某个插件的窗口 setup 要把一个 API 或 Solid 组件暴露给其他插件的窗口 setup 时，使用 `Contract.define`。

```ts title="src/gui/contract.ts"
import type { JSX } from "solid-js"
import { Contract } from "@opencode/plugin/gui"

export interface AcmeBadge {
  Badge(props: { readonly label: string }): JSX.Element
  count(): number
}

export const AcmeBadge = Contract.define<AcmeBadge, "acme.badge">("acme.badge")
```

在窗口 setup 中用 `ctx.provide` 提供它。当契约包含组件时，在 setup 期间用 `bindPlugin` 包裹它。这样组件内部的 `usePlugin()` 读到的是提供者的上下文，而不是消费者的。

```tsx title="src/gui.tsx"
import { bindPlugin, Plugin } from "@opencode/plugin/gui"
import { AcmeBadge } from "./gui/contract"

export default Plugin.define({
  i18n: { en: { title: "Acme" } },
  setup(ctx) {
    ctx.provide(AcmeBadge, {
      Badge: bindPlugin((props: { readonly label: string }) => (
        <span>
          {ctx.t("title")}: {props.label}
        </span>
      )),
      count: () => 42,
    })
  },
})
```

- 用 `bindPlugin` 包裹的组件，其 props 需要显式标注类型，如 `bindPlugin((props: FileTreeProps) => ...)`。TypeScript 在 `ctx.provide` 内无法推断它们。
- 数据方法（如 `count`）不用包裹。
- `ctx.provide` 返回一个可以提前撤回契约的函数。宿主也会随当前所有者一起撤回它，否则在插件停止时撤回。

### 使用其他插件的契约

从你的包中导出 `contract.ts`，例如作为 `./contract`，让其他插件可以导入它的 token。另一个插件用 `ctx.use(token)` 跟随该契约。访问器的值会随提供者启动、停止和重启而变化，因此在使用处读取它。

```tsx title="src/gui.tsx"
import { Plugin, Slot } from "@opencode/plugin/gui"
import { AcmeBadge } from "opencode-acme-plugin/contract"

export default Plugin.define({
  setup(ctx) {
    const badge = ctx.use(AcmeBadge)

    const count = () => {
      const live = badge()

      return live.status === "active" ? live.value.count() : 0
    }

    ctx.add(Slot, { at: "window.bottom", render: () => <span>{count()}</span> })
  },
})
```

- 对同一个 token 的每次调用，`ctx.use` 返回同一个访问器。
- 提供者离线时，消费者仍然继续工作。参见 [Live 依赖与失败处理](#live-依赖与失败处理)。

### main 与窗口之间的 IPC

用 `Ipc.define` 配合 Effect `Schema` 编解码器定义 `main` 与 `setup` 之间的类型化桥接。`main` 用 `ctx.provide` 实现它，窗口通过 `ctx.main` 调用它。

```ts title="src/gui/contract.ts"
import { Schema } from "effect"
import { Ipc } from "@opencode/plugin/gui"

export const KeepAwake = Ipc.define({
  id: "acme.awake",
  methods: {
    screenActive: { output: Schema.Boolean },
    setScreenActive: { input: Schema.Boolean },
  },
})
```

```ts
const awake = ctx.main(KeepAwake)

await awake.setScreenActive(true)
```

- 其他插件像契约一样用 `ctx.use(KeepAwake)` 跟随你的 `Ipc`。
- 状态、事件和提供者参见[定义并提供 Ipc](#定义并提供-ipc)。

### 你的插件拥有的注册表

用 `Registry.define` 定义你的插件拥有的列表。其他插件用 `ctx.add` 贡献条目，你的插件用 `ctx.list` 读取它们。

```ts title="src/gui/contract.ts"
import { Registry } from "@opencode/plugin/gui"

export interface Exporter {
  readonly id: string
  readonly title: string
  run(text: string): void
}

export const Exporter = Registry.define<Exporter>("acme.exporter")
```

```tsx
// Another plugin contributes an item.
ctx.add(Exporter, () => ({ id: "gist", title: ctx.t("exporter.gist"), run: (text) => upload(text) }))

// The owner lists every contribution. Reactive: read it in render or in a memo.
const exporters = () => ctx.list(Exporter)
```

## 窗口

插件的 `setup` 在每个桌面应用窗口中运行。把它传给插件 [`./gui-experimental` 文件](#定义-gui-插件)中来自 `@opencode/plugin/gui` 的 `Plugin.define`。`setup` 是同步的，可以返回清理函数；参见[生命周期与清理](#生命周期与清理)。

```tsx title="src/gui.tsx"
import { Command, Plugin } from "@opencode/plugin/gui"

export default Plugin.define({
  i18n: { en: { open: "Open Acme" } },
  setup(ctx) {
    ctx.add(Command, () => ({
      id: "open",
      title: ctx.t("open"),
      run: () => ctx.system.openExternal("https://acme.example"),
    }))
  },
})
```

## 组件

在 Solid 组件内部，调用 `usePlugin<typeof definition>()` 即可得到 `setup` 收到的同一个上下文对象。从声明所在的独立文件中获取它的类型（[拆分到多个文件](#拆分到多个文件)），这样组件与定义互不导入。

```tsx title="src/gui/window.tsx"
import { Slot, usePlugin, type Plugin } from "@opencode/plugin/gui"
import type { definition } from "./definition"

function StatusLabel() {
  const ctx = usePlugin<typeof definition>()

  return <span>{ctx.t("title")}</span>
}

export const setup: Plugin.Setup<typeof definition> = (ctx) => {
  ctx.add(Slot, { at: "window.bottom", render: () => <StatusLabel /> })
}
```

`usePlugin` 在插件贡献之外会抛错。在被另一个插件渲染的组件中，它返回那个插件的上下文，因此你提供在契约上的组件要用 `bindPlugin` 包裹；参见[契约](#契约)。

## 注册表

把注册表 token 和条目传给 `ctx.add` 即可为窗口外壳做出贡献。当条目跟随响应式状态（如语言）时，把条目作为函数传入，形如 `() => item | undefined`。宿主会在其读取的内容变化时再次运行该函数。返回 `undefined` 即撤回该条目，直到函数再次返回一个条目为止。

```ts
ctx.add(Command, () => ({ id: "open", title: ctx.t("command.open"), run: () => open() }))
```

- 在函数内部用 `ctx.t` 读取标签。在固定条目中一次性读出的标签会保留读取时的语言。
- 当条目有字面量类型的字段时，例如 `hidden: true`、`section`、`icon` 或菜单名称，要标注函数的返回类型：`(): Command => ({ ... })`。否则 TypeScript 会把该字段拓宽为 `string` 或 `boolean`，导致没有重载匹配。
- 永不变化的条目直接传固定值，例如[样式](#样式)。
- 宿主会让某些对象保持稳定：面板从 `list` 返回的标签页，以及带 `render` 的条目（如面板和设置页面）。从 getter 读取它们的标签，例如 `get title() { return ctx.t("title") }`。
- `ctx.add` 返回一个可以提前撤回该条目的函数。

### 命令

`Command` 把一个操作加入命令面板、**Settings > Shortcuts**，以及可选的输入框 `/` 菜单。宿主把命令发布为 `<plugin id>.<command id>`。

```ts
import { Command } from "@opencode/plugin/gui"

ctx.add(
  Command,
  (): Command => ({
    id: "toggle",
    title: ctx.t("command.toggle"),
    keywords: "notes scratch",
    group: ctx.t("command.category.view"),
    section: "terminal",
    bind: "ctrl+`",
    slash: { name: "notes", after: "open" },
    featured: true,
    enabled: !!ctx.sessions.current(),
    run: () => {
      const session = ctx.sessions.current()

      if (session) ctx.layout.toggle(`${ctx.id}:main`, session)
    },
  }),
)
```

- `title` 是面板中的标签，`description` 是其第二行，`group` 是其分类，均为翻译后的文本。
- `keywords` 存放面板额外匹配的词，用空格分隔。
- `section` 是 **Settings > Shortcuts** 的分区。默认为 `general`。
- `bind` 是默认按键绑定，例如 `mod+shift+t`。用户可以更改它。
- `slash` 还把命令放入 `/` 菜单。带上 `arguments: true` 时，名称之后的文本会传给 `run(input)`。
- `hidden` 让命令不出现在面板中，但其按键绑定仍然生效。
- `suggested` 还会在命令启用时把它列在 **Suggested** 下面。`featured` 则在面板不带查询打开时列出它。
- `enabled: false` 会把命令从面板中移除并关闭其按键绑定。它是响应式的。
- `scope` 是一个 CSS 选择器，键盘焦点必须位于其内部，绑定才会生效。带上 `editable` 时，文本字段持有焦点时绑定也会触发。
- 要从自己的代码运行命令，使用 `ctx.commands.run`；参见[运行命令](#运行命令)。

从按键绑定触发时，`run` 可以返回 `false` 来拒绝该按键。事件随后会继续传递给其目标，就像该命令没有按键绑定一样。下面这个命令会在用户在空提示中按下 Enter 时继续会话，而把其他所有 Enter 留给提示框：

```ts
ctx.add(Command, () => ({
  id: "continue",
  title: ctx.t("command.continue"),
  bind: "enter",
  editable: true,
  hidden: true,
  run: () => {
    const composer = ctx.screen.current()?.composer
    const session = ctx.sessions.current()

    if (!composer?.focused() || composer.text().trim() || !session) return false
    void session.server.client.session.prompt({ sessionID: session.id, text: ctx.t("continue") })
  },
}))
```

- 同步返回 `false`；返回 promise 表示接管该按键。
- 从命令面板或 slash 命令返回的 `false` 没有额外效果。

#### 参考

```ts
interface Command {
  id: string
  title: string
  description?: string
  keywords?: string
  group?: string
  section?: "general" | "session" | "navigation" | "model" | "terminal" | "prompt"
  bind?: string
  slash?: { name: string; arguments?: true; after?: string }
  hidden?: true
  suggested?: boolean
  featured?: true
  enabled?: boolean
  scope?: string
  editable?: true
  run(input?: string): void | false | Promise<void>
}
```

### 面板

`Panel` 向会话的侧边区域（`region: "side"`）贡献标签页。用户可以把标签页拖到时间线下方的底部面板。

```tsx
import { Panel, type PanelTab } from "@opencode/plugin/gui"

const mainTab: PanelTab = {
  id: "main",
  get title() {
    return ctx.t("panel.title")
  },
  closable: "compact",
  fallback: true,
}

ctx.add(Panel, {
  id: "main",
  region: "side",
  mobile: {
    get title() {
      return ctx.t("panel.title")
    },
    order: 45,
    kind: "menu",
    icon: "file-tree",
  },
  list: (input) => (input.open.includes("main") ? [mainTab] : []),
  render: (props) => <NotesView session={props.session} screen={props.screen} tab={props.tab} />,
})
```

所有面板回调（`list`、`render`、`focus`、`enter`、`close`、`closed`、`restore`、`normalize`）都接收单个输入对象：

- 在使用处把 `props.session` 和 `props.tab` 当作响应式 getter 读取。不要在 `render` 顶部解构它们：当用户从会话 A 切到会话 B 时，面板保持挂载，`props.session` 会原地更新。
- `props.screen` 是拥有 `SessionScreen`（`file`、`comment`、`composer`）的常量。它的操作始终指向被路由的会话。
- 标签页未变化时，`list` 要返回同一个 `PanelTab` 对象，这样宿主不会重新挂载它的触发器。标签从 getter 读取，这样无需新对象也能跟随语言。

面板的回调：

- `list` 返回要显示的标签页。`input.open` 存放本插件保存在会话中的标签页 id。它是响应式的。
- `render` 渲染一个标签页的内容，仅一次。
- `focus` 在标签页被选中时运行。`restored` 对区域挂载时的那个选中项为 `true`。
- `enter` 在用户用开关打开侧边区域并切到该标签页时运行，此时标签页已在屏幕上。把键盘焦点移到该标签页自己的目标上，例如文本字段。当焦点仍在区域之外时，宿主会聚焦该区域。
- `close` 在宿主移除标签页之后运行。
- `closed` 和 `restore` 让用户可以重新打开已关闭的标签页；参见[重新打开已关闭的标签页](#重新打开已关闭的标签页)。
- `normalize` 返回某个存储形态不止一种的标签页 id 的规范形式。

面板的选项：

- `mobile` 为面板添加窄屏视图。带上 `cached: true` 时，用户切换到其他视图期间该视图保持挂载。默认情况下，视图每次显示时都会挂载。
- `wide` 在侧边区域打开时请求更宽的会话最小宽度。
- `width` 给面板一个自己的侧边区域宽度；参见[面板宽度](#面板宽度)。
- `transient` 面板的标签页不会被恢复。

#### 面板宽度

默认情况下，侧边区域中的每个标签页都与对话共用宽度。当你的面板比审查或浏览器需要更少或更多空间时，设置 `width`。传入 CSS 像素，或用 `"narrow"` 表示区域允许的最窄宽度。

```ts
ctx.add(Panel, {
  id: "quota",
  region: "side",
  width: "narrow",
  list: (input) => (input.open.includes("quota") ? [tab] : []),
  render: () => <Quota />,
})
```

- 该宽度在侧边面板显示该面板某个标签页期间生效。其他标签页保持对话的宽度。
- 当用户在该面板某个标签页上拖动分隔条时，宿主会为该面板在整个应用范围内保留那个宽度，取代 `width`。
- 宿主让对话保持其最小宽度，并让区域至少保持 `"narrow"`。
- `ctx.layout.side.width(panel)` 读取已存储的宽度，`ctx.layout.side.resize(panel, width)` 存储一个宽度，效果与拖动相同。已存储的宽度甚至对没有 `width` 的面板也生效。

标签页的选项：

- `id` 是标签页 id；它的宿主键是 `<plugin id>:<id>`。`title` 是其可访问名称，`label` 渲染自定义触发器内容。
- `pinned` 标签页无需打开即会列出，排在最前，永远不会被关闭或拖动。
- `draggable` 允许用户重新排序标签页。默认为 `true`。
- `closable` 设置关闭按钮的外观：`"compact"`、`"hover"`，或 `false` 表示没有。
- `transient` 标记一个启动器标签页（如 **Open file**），它会被下一次预览替换。
- `fallback` 在已存储的选中项缺失时启用回退选择。
- 同一 `group` 中的标签页共享一个保持挂载的渲染。
- `missing` 给标签页加删除线，例如文件已不存在的情况。
- `hidden` 让已恢复的标签页保持列出且可选，但不绘制，用于其内容尚不可知的情形。
- `file` 是标签页显示的工作区路径，会作为会话的打开文件之一列出。
- `tabbable` 把标签面板加入 tab 顺序，用于没有可聚焦元素的内容。

#### 参考

```ts
interface Panel {
  id: string
  region: "side"
  mobile?: MobileView
  wide?: boolean
  width?: number | "narrow"
  transient?: boolean
  list(input: { session: MountedSession; screen: SessionScreen; open: string[] }): PanelTab[]
  render(props: PanelProps): JSX.Element
  focus?(input: PanelProps & { restored: boolean }): void
  enter?(input: PanelProps): void
  close?(input: PanelProps): void
  closed?(input: PanelProps): ClosedPanelTab | false | undefined
  restore?(input: { session: MountedSession; screen: SessionScreen; id: string; data?: string }): void
  normalize?(input: { id: string; session: MountedSession; screen: SessionScreen }): string
}

interface PanelProps {
  tab: PanelTab
  session: MountedSession
  screen: SessionScreen
}

interface PanelTab {
  id: string
  title: string
  label?(state: { active: boolean; preview: boolean; session: MountedSession }): JSX.Element
  pinned?: boolean
  draggable?: boolean
  closable?: "compact" | "hover" | false
  transient?: boolean
  fallback?: boolean
  group?: string
  missing?: boolean
  hidden?: boolean
  file?: string
  tabbable?: boolean
}

interface MobileView {
  title: string
  order: number
  kind: "tab" | "menu" | "drawer"
  icon?: IconName
  cached?: boolean
}
```

### 重新打开已关闭的标签页

宿主为用户关闭的每个侧边标签页保留一条记录。焦点位于侧边区域内时，⌘⇧T 会重新打开最近的一个。侧边区域的 **New tab** 视图会把带 `file` 的已关闭标签页列在 **Recently closed** 下。添加 `closed` 和 `restore` 来控制标签页在那里如何显示以及如何恢复。

```tsx
ctx.add(Panel, {
  id: "page",
  region: "side",
  list: (input) => input.open.map(pageTab),
  render: (props) => <PageView tab={props.tab} />,
  closed: (input) => {
    const url = pages.get(input.tab.id)

    return url ? { icon: "globe", detail: new URL(url).host, data: url } : false
  },
  restore: (input) => {
    if (input.data) openPage(input.session, input.data)
  },
})
```

- `closed` 在用户关闭标签页时运行。现在就捕获重新打开所需的一切：返回该行如何显示以及 `restore` 所需的 `data`，当标签页无法恢复时返回 `false`。
- `title` 默认为标签页的标题，`icon` 默认为面板的移动端图标。带 `file` 的标签页显示其文件图标，其所在文件夹作为 `detail`。
- 宿主会存储该记录，因此 `data` 要保持小巧，例如一个 URL。
- `restore` 收到已关闭标签页的 `id` 和 `closed` 返回的 `data`。没有 `restore` 时，宿主会以同样的键再次打开。
- 没有 `closed` 时，非 `transient` 的标签页会以其标题列出，并以同样的键重新打开。

#### 参考

```ts
interface ClosedPanelTab {
  title?: string
  icon?: IconName
  detail?: string
  data?: string
}
```

### 设置页面

`SettingsPage` 向 **Settings** 贡献一个页面，或向宿主页面的某个分区贡献一个分区（`page: "general"` 或 `page: "servers"`），或向宿主的 General 分区贡献若干行（`page: "general", section: "general"`）。

```tsx
import { SettingsPage } from "@opencode/plugin/gui"
import { AcmeSettings } from "./settings"

ctx.add(SettingsPage, {
  id: "acme",
  icon: "server",
  get title() {
    return ctx.t("title")
  },
  get entries() {
    return [{ id: "sync", title: ctx.t("settings.sync"), keywords: "sync remote" }]
  },
  render: (input) => <AcmeSettings highlight={input.target} />,
})
```

- `id` 是页面的设置标签值（`/settings?tab=<id>`），也是 `ctx.layout.settings` 的参数。
- `page` 表示在宿主页面上添加一个分区而不是一个页面。带上 `section: "general"` 时，它会向该页面的 General 分区添加若干行。
- `title` 和 `icon` 是页面的导航标签和图标。
- `entries` 是搜索元数据，在不挂载页面的情况下建立索引。当搜索展示某个条目时，`render` 会收到其 id 作为 `target`。
- 设置页面带 `render`，因此宿主会让它保持稳定。从 getter 读取它的标签和条目。

用应用的设置组件渲染页面，让它看起来和应用自己的页面一样，并且搜索可以展示它的行：

```tsx
const ui = ctx.ui

const AcmeSettings = () => (
  <ui.SettingsLayout title={ctx.t("title")} description={ctx.t("description")}>
    <ui.SettingsSection title={ctx.t("settings.section")}>
      <ui.SettingsRow id="sync" title={ctx.t("settings.sync")} description={ctx.t("settings.sync.description")}>
        <ui.Switch label={ctx.t("settings.sync")} hideLabel checked={sync()} onChange={setSync} />
      </ui.SettingsRow>
    </ui.SettingsSection>
  </ui.SettingsLayout>
)
```

- 你自己的页面渲染 `SettingsLayout`；宿主页面上的分区（`page`）渲染 `SettingsSection`；宿主分区中的行（`section`）渲染 `SettingsRow`。
- 行的 `id` 就是展示它的 `SettingEntry.id`：搜索会滚动到该行并高亮它。
- 它们的 props 参见[设置组件](#设置组件)。

#### 参考

```ts
interface SettingsPage {
  id: string
  page?: "general" | "servers"
  section?: "general"
  title: string
  icon?: IconName
  entries?: SettingEntry[]
  render(input: { target?: string }): JSX.Element
}

interface SettingEntry {
  id: string
  title: string
  description?: string
  keywords?: string
}
```

### 槽位

`Slot` 把 UI 渲染到四个窗口槽位之一。

```tsx
import { Slot } from "@opencode/plugin/gui"

ctx.add(Slot, {
  at: "session.header",
  order: 10,
  render: (input) => <UsageRing session={input.session} active={input.active} />,
})
```

- `window.bottom` 是窗口底部的一条全宽横条，位于 toast 之上。
- `session.header` 是会话时间线的标题行。缓存的时间线在隐藏期间保持挂载，`active` 为 `false`。
- `session.location.menu` 向项目菜单添加条目，位于其位置详情之后。
- `session.panel.end` 在侧边区域标签条的末端放置操作。
- `order` 对同一个槽位中的条目排序。

`session.location.menu` 会收到 `shown`，在项目菜单打开期间为 `true`。只在它为 `true` 时订阅位置数据：

```tsx
ctx.add(Slot, {
  at: "session.location.menu",
  render: (input) => <BranchStatus session={input.session} screen={input.screen} shown={input.shown} />,
})
```

项目菜单是宿主菜单：用 `ctx.ui.MenuItem`、`MenuSub`、`MenuGroup` 和 `MenuSeparator` 渲染它的行，这样它们可以像宿主的行一样用键盘导航并在选择后关闭菜单。参见[菜单行](#菜单行)。

```tsx
ctx.add(Slot, {
  at: "session.location.menu",
  render: (input) => <ctx.ui.MenuItem label={ctx.t("usage")} icon="status" onSelect={() => openUsage(input.session)} />,
})
```

#### 参考

```ts
type Slot = {
  [At in keyof SlotMap]: { at: At; order?: number; render(input: SlotMap[At]): JSX.Element }
}[keyof SlotMap]

interface SlotMap {
  "window.bottom": Record<string, never>
  "session.header": { screen: SessionScreen; session: MountedSession; active: boolean }
  "session.location.menu": { screen: SessionScreen; session: MountedSession; shown: boolean }
  "session.panel.end": { screen: SessionScreen; session: MountedSession }
}
```

### 菜单项

`MenuItem` 向侧面板的 **+** 菜单（`"session.panel"`）、**Add server** 菜单（`"server.add"`）或 Settings 中每个服务器的行菜单（`"server.row"`）添加条目。

```ts
import { MenuItem } from "@opencode/plugin/gui"

ctx.add(MenuItem, (): MenuItem => {
  const session = ctx.sessions.current()

  return {
    menu: "session.panel",
    id: "open",
    title: ctx.t("menu.open"),
    icon: "folder",
    keybind: `${ctx.id}.open`,
    opened: !!session && ctx.layout.state(`${ctx.id}:main`, session) !== "closed",
    run: () => {
      if (session) ctx.layout.open(`${ctx.id}:main`, session)
    },
  }
})
```

- `order` 按升序排列条目。默认为 `0`。
- `server.row` 条目的 `run` 会收到该行的服务器键。`when` 只在部分行上列出该条目，`enabled` 让它在其他行上以禁用状态显示。

`session.panel` 条目同时也是启动器。当用户在没有标签页的情况下打开侧边区域，或在没有条目是 `primary` 的情况下点击 **+** 时，宿主会显示一个列出启动器的 **New tab** 视图。

- `icon` 是条目的图标，`keybind` 是一个已发布的命令 id，条目会显示它的快捷键。
- `description` 是启动器行中标题后面的简短弱化说明，例如一个计数。
- `opened: true` 表示该条目打开的标签页已经打开。启动器列表会把它排除，而 **+** 菜单仍会列出它。
- `primary: true` 让 **+** 直接运行该条目，而不是显示启动器。`order` 中的第一个 primary 条目获胜。在没有标签页时打开侧边区域仍会显示 **New tab** 视图，其中列出既不是 primary 也没有打开的条目。
- `ctx.layout.side.menu()` 列出每个插件的 `session.panel` 条目，用于实现你自己的启动器；参见[布局](#布局)。

#### 参考

```ts
type MenuItem = SessionPanelMenuItem | ServerAddMenuItem | ServerRowMenuItem

interface SessionPanelMenuItem {
  menu: "session.panel"
  id: string
  title: string
  order?: number
  icon?: IconName
  keybind?: string
  description?: string
  opened?: boolean
  primary?: true
  run(): void
}

interface ServerAddMenuItem {
  menu: "server.add"
  id: string
  title: string
  order?: number
  run(): void
}

interface ServerRowMenuItem {
  menu: "server.row"
  id: string
  title: string
  order?: number
  when?(server: string): boolean
  enabled?(server: string): boolean
  run(server: string): void
}
```

### 标题栏项

`TitlebarItem` 在窗口标题栏或标签页页脚渲染一个胶囊按钮。它的标签在悬停时显示。

```ts
import { TitlebarItem } from "@opencode/plugin/gui"

ctx.add(TitlebarItem, (): TitlebarItem | undefined =>
  syncing() ? { id: "sync", label: ctx.t("syncing"), icon: "server", busy: true, run: () => sync() } : undefined,
)
```

- `title` 是它与 `label` 不同时的可访问名称。
- `busy` 显示加载指示器并禁用该胶囊。`pressed` 显示按下状态。
- `run` 在点击时运行。只用于展示的条目可以省略它。

#### 参考

```ts
interface TitlebarItem {
  id: string
  label: string
  title?: string
  icon?: IconName
  busy?: boolean
  pressed?: boolean
  run?(): void
}
```

### 输入框胶囊

`ComposerPill` 在会话输入框上方的行中添加一个胶囊，与应用的后台工作和 todo 胶囊并列。用于属于用户当前所在会话的状态，例如其分支的拉取请求。胶囊浮在时间线之上，因此胶囊的出现或消失不会改变输入框的尺寸。该行跟随用户的后台活动对齐方式，并且不会显示在子 agent 的会话中。

`show` 为一个会话返回胶囊，或返回 `undefined` 表示在那里不显示。宿主会为每个已挂载的输入框运行它，并在其读取的内容变化时再次运行。下面这个插件通过其服务器部分的 [RPC](../rpc/index.md) 列出每个会话目录的打开拉取请求，并把它们显示为一个胶囊：

```tsx
import { createStore } from "solid-js/store"
import { ComposerPill, createKeyed } from "@opencode/plugin/gui"
import { GitHub, type Pull } from "./rpc"

const [pulls, setPulls] = createStore<Record<string, readonly Pull[]>>({})

createKeyed(
  () => ctx.sessions.current()?.directory,
  (directory) =>
    void ctx.client
      .rpc(GitHub)
      .pulls({ directory })
      .then((list) => setPulls(directory, list)),
)

ctx.add(ComposerPill, {
  id: "pulls",
  show: (input) => {
    const list = pulls[input.session.directory] ?? []

    if (list.length === 0) return undefined

    return {
      icon: "github",
      label: ctx.plural("pulls", list.length),
      tone: list.some((pull) => pull.checks === "failure") ? "danger" : undefined,
      title: ctx.t("pulls.title"),
      rows: list.map((pull) => ({
        id: String(pull.number),
        label: `#${pull.number} ${pull.title}`,
        icon: pull.checks === "failure" ? "circle-x" : "circle-check",
        tone: pull.checks === "failure" ? "danger" : "success",
        detail: pull.branch,
        run: () => ctx.system.openExternal(pull.url),
      })),
    }
  },
})
```

- `label` 是胶囊的文本，过长时截断。`icon` 是可选的。
- `tone` 为图标着色：`"success"`、`"warning"` 或 `"danger"`。
- `rows` 让胶囊打开一个菜单，标题为 `title`，没有标题时为 `label`。每行有自己的 `icon`、`tone` 和弱化的 `detail`，选中时运行 `run`；没有 `run` 的行只做展示。
- 没有 `rows` 时，胶囊在点击时运行 `run`。
- `title` 也是它与 `label` 不同时胶囊的可访问名称。
- `order` 把你的胶囊排到其他插件的胶囊之间，值小的在前。应用自带的胶囊排在最前。
- 抛错的 `show` 只会让你的插件的贡献失败。

#### 参考

```ts
interface ComposerPill {
  id: string
  order?: number
  show(input: ComposerPillProps): ComposerPillView | undefined
}

interface ComposerPillProps {
  session: MountedSession
  screen: SessionScreen
}

interface ComposerPillView {
  label: string
  icon?: IconName
  tone?: ComposerPillTone
  title?: string
  rows?: ComposerPillRow[]
  run?(): void
}

interface ComposerPillRow {
  id: string
  label: string
  icon?: IconName
  tone?: ComposerPillTone
  detail?: string
  run?(): void
}

type ComposerPillTone = "success" | "warning" | "danger"
```

### 代码块

`CodeBlock` 把你列出的语言的围栏代码块渲染为你自己的 UI，取代高亮显示的代码。适用于画出来比源码更好读的内容，例如 ` ```csv ` 表格或 ` ```latex ` 公式：

```tsx
import { For } from "solid-js"
import { CodeBlock } from "@opencode/plugin/gui"

ctx.add(CodeBlock, {
  languages: ["csv"],
  render: (props) => {
    const rows = props.code.split("\n").map((line) => line.split(","))

    if (rows.length < 2) return undefined

    return (
      <table>
        <tbody>
          <For each={rows}>
            {(row) => (
              <tr>
                <For each={row}>{(cell) => <td>{cell}</td>}</For>
              </tr>
            )}
          </For>
        </tbody>
      </table>
    )
  },
})
```

- `languages` 与围栏信息字符串的第一个词比较，转为小写：` ```CSV title="Q3" ` 匹配 `csv`。宿主不解析别名，因此把你接受的每个名称都列出来。
- `render` 收到代码块的 `code`、`language`，以及展示它的 `session`。返回 `undefined` 或 `null` 可以保留高亮代码，例如源码无法解析时。
- 抛错的 render 会把错误记录在你的插件名下，代码块则显示其源码。你的其他贡献继续工作。
- 当多个插件列出同一种语言时，第一个贡献的来渲染它。当你列出 `mermaid` 时，你的渲染器也会取代应用自带的 Mermaid 图。

#### 流式传输

宿主只在收到结束围栏后才渲染代码块。在代码块流式输出的过程中，以及消息在块中间停止时，用户看到的是高亮代码；随后你的 UI 原地替换它。你的 render 永远不会看到半个代码块。

#### 适用范围

| 界面区域                                                     | 代码块内容 |
| ------------------------------------------------------------ | ------------------ |
| 时间线：助手文本和工具输出                                   | 是                 |
| 会话屏幕上的侧面板，例如 Markdown 预览                       | 是                 |
| 在会话屏幕上渲染的 `ctx.ui.Markdown`                         | 是                 |
| `ctx.ui.Code`，以及你自己的 `CodeBlock` render 内的 Markdown | 否                 |
| 设置页面、对话框以及其他屏幕之外的界面                       | 否                 |

#### 布局与性能

- 没有任何插件列出的语言的代码块没有开销；只有被列出语言的代码块才会渲染你的 UI，且只在其时间线行出现在屏幕上时。
- 代码块随你的 UI 增长和收缩。给异步内容一个最小高度，这样内容到达时时间线的移动更少。
- 代码块保留其 Copy 按钮（复制的是源码），你的 `CodeBlockAction` 按钮会出现在其右上角。

### 代码块操作

`CodeBlockAction` 在你列出的语言的代码块的 Copy 按钮旁添加一个按钮。`run` 收到的代码块与 `CodeBlock` render 收到的相同：

```ts
import { CodeBlockAction } from "@opencode/plugin/gui"

ctx.add(CodeBlockAction, {
  id: "run",
  languages: ["sh", "bash", "shell", "zsh"],
  icon: "terminal",
  get title() {
    return ctx.t("run")
  },
  run: (input) => runInTerminal(input.code, input.session),
})
```

- 按钮在代码块的结束围栏到达后显示，因此它永远不会对半个命令执行操作。
- 按钮在悬停或键盘聚焦时与 Copy 一起出现，位于其之前，按 `order` 升序排列。
- 从 getter 读取 `title`，这样它能跟随语言。
- 抛错或 reject 的 `run` 会记录在你的插件名下，其他一切不变。

#### 参考

```ts
interface CodeBlock {
  languages: string[]
  render(props: CodeBlockProps): JSX.Element | undefined
}

interface CodeBlockAction {
  id: string
  languages: string[]
  icon: IconName
  title: string
  order?: number
  run(input: CodeBlockProps): void | Promise<void>
}

interface CodeBlockProps {
  code: string
  language: string
  session?: MountedSession
}
```

### 链接处理器

`LinkHandler` 打开用户在消息或输入框 chip 中点击的本地文件或自定义链接。`match` 返回 true 且 `priority` 最高的处理器会打开该链接。

```ts
import { LinkHandler } from "@opencode/plugin/gui"

ctx.add(LinkHandler, {
  priority: 10,
  match: (link) => link.href.endsWith(".acme"),
  open: (link) => openAcmeFile(link.href, link.session),
  exists: (link) => acmeFileExists(link.href),
})
```

- `href` 是目标：路径、URL 或 `file://` 链接。
- `origin` 是产生该链接条目的插件。
- `exact` 表示路径是已知的工作区文件，不是从文本猜测的。
- `background` 链接不得切换窄屏视图。
- `base` 是链接书写时所在的工作区相对目录。
- 没有 `exists` 时，`ctx.links.exists` 会回答 `false`，这样文本永远不会看起来像一个处理器无法打开的链接。

#### 参考

```ts
interface LinkHandler {
  priority?: number
  match(link: Link): boolean
  open(link: Link): void
  exists?(link: Link): boolean | Promise<boolean>
}

interface Link {
  href: string
  origin?: string
  exact?: boolean
  background?: boolean
  base?: string
  session?: SessionRef
}
```

### 服务器

`Server` 贡献一组服务器连接，例如你的插件在其他机器上启动的服务器。

```ts
import { Server } from "@opencode/plugin/gui"

ctx.add(
  Server,
  (): Server => ({
    ready: loaded(),
    entries: machines().map((machine) => ({
      id: machine.id,
      name: machine.name,
      label: "Acme",
      state: machine.url ? "ready" : "starting",
      http: machine.url ? { url: machine.url } : undefined,
    })),
  }),
)
```

- 启动会等待每个来源变为 `ready`。就绪来源的条目就是它的完整清单。
- `order` 按升序排列各来源。
- 每个条目的键是 `<plugin id>:<id>`。`label` 是其 `name` 旁边的短徽章。
- `auth` 表示服务器在等待用户登录，`incompatible` 表示它运行的版本本应用不支持。
- `listed: false` 让条目不出现在应用的服务器列表中。Settings 仍会显示它。
- `http` 是 endpoint，在服务器 `ready` 之后。
- `reconnect` 重新解析一个掉线的 endpoint，`connect` 准备一个尚未就绪的服务器，`remove` 在条目被移除之前运行。
- `row` 渲染该服务器的设置行，`cover` 在服务器未就绪时覆盖被路由的会话。
- `row` 会收到宿主的状态 `Indicator`、最新的 `health()` 检查，以及该行 `server.row` 菜单的 `Items`。它的 `remove()` 先运行条目的 `remove`，然后关闭该服务器的标签页。

#### 参考

```ts
interface Server {
  ready: boolean
  order?: number
  entries: ServerEntry[]
}

interface ServerEntry {
  id: string
  name: string
  label?: string
  state: "stopped" | "starting" | "auth" | "ready" | "failed" | "incompatible"
  listed?: boolean
  http?: { url: string; password?: string }
  reconnect?(signal: AbortSignal): Promise<{ url: string; password?: string }>
  connect?(): Promise<boolean>
  remove?(): Promise<void>
  row?(row: ServerRow): JSX.Element
  cover?(input: { tab: string }): JSX.Element
}

interface ServerRow {
  key: string
  health(): ServerHealth | undefined
  Indicator(props: { health?: ServerHealth; connecting?: boolean; auth?: boolean }): JSX.Element
  remove(): Promise<void>
  Items(): JSX.Element
}

interface ServerHealth {
  healthy: boolean
  version?: string
  incompatible?: boolean
  checking?: boolean
}
```

### 样式

`Style` 在贡献处于活动状态期间向文档注入一段 CSS 字符串。

```ts
import { Style } from "@opencode/plugin/gui"
import css from "./panel.css?inline"

ctx.add(Style, css)
```

### 主题

`Theme` 向 Settings › Appearance › Theme 添加一个配色主题。它采用与应用自带主题文件相同的格式，因此主题文件可以直接导入。

```ts
import { Theme } from "@opencode/plugin/gui"
import midnight from "./midnight.json"

ctx.add(Theme, midnight)
```

主题文件自己命名，并给出一个亮色和一个暗色变体。每个变体从 `palette` 或 `seeds` 出发，绝不同时使用两者，并可用 `overrides` 固定单个 token。

```json
{
  "$schema": "https://opencode.ai/desktop-theme.json",
  "name": "Midnight",
  "id": "midnight",
  "light": {
    "palette": {
      "neutral": "#eceff4",
      "ink": "#2e3440",
      "primary": "#5e81ac",
      "success": "#8fbcbb",
      "warning": "#d08770",
      "error": "#bf616a",
      "info": "#81a1c1"
    }
  },
  "dark": {
    "palette": {
      "neutral": "#1b1f27",
      "ink": "#e5e9f0",
      "primary": "#88c0d0",
      "success": "#a3be8c",
      "warning": "#d08770",
      "error": "#bf616a",
      "info": "#81a1c1"
    },
    "overrides": { "syntax-keyword": "#88c0d0" }
  }
}
```

- 选择器按 `name` 的字母顺序把插件主题列在应用主题之间。
- 宿主把每个主题的键设为 `<plugin id>:<theme id>`，因此它永远不会替换应用主题或其他插件的主题。
- 撤回主题，或禁用插件，会把它从选择器中移除。选中过它的用户会保留这个选择：窗口显示默认主题，直到该主题回归。
- 启动时，窗口显示上次运行缓存的配色，直到插件再次贡献该主题。

## 宿主 API

宿主 API 是 `ctx` 的属性。在应用界面挂载之前它们都不会抛错：读取返回其文档中的默认值，早期的写入（如 `ctx.layout.open`、`ctx.dialogs.open` 和 store 更新）会等待并在第一个路由渲染后按调用顺序应用。

```ts
ctx.add(Command, () => ({
  id: "copy-directory",
  title: ctx.t("command.copyDirectory"),
  run: () => {
    const session = ctx.sessions.current()

    if (session) void ctx.system.copy(session.directory)
  },
}))
```

下面各节逐一介绍每个 API。`ctx.options`、`ctx.client` 和 `ctx.app` 是[共享上下文](#共享上下文)，`ctx.provide`、`ctx.use` 和 `ctx.main` 配合[契约与 token](#契约与-token) 工作，`ctx.stores` 存放插件[声明](#定义-gui-插件)的 store。

#### 参考

```ts
interface SetupContext<D> extends Context {
  stores: Record<string, Persisted<unknown> | ((session: SessionRef) => Persisted<unknown>)>
}

interface Context {
  id: string
  options: PluginOptions
  client: OpenCodeClient
  app: App
  signal: AbortSignal
  add<T>(registry: Registry<T>, item: () => T | undefined): Cleanup
  add<T>(registry: Registry<T>, item: T): Cleanup
  list<T>(registry: Registry<T>): T[]
  provide<T>(token: Contract<T>, impl: T): Cleanup
  use<T>(token: Contract<T>): () => Live<T>
  use<S extends IpcSpec>(token: Ipc<S>): () => Live<IpcClient<S>>
  main<S extends IpcSpec>(token: Ipc<S>): IpcClient<S>
  t(key: string, params?: Record<string, string | number | boolean>): string
  plural(key: string, count: number, params?: Record<string, string | number | boolean>): string
  layout: Layout
  sessions: Sessions
  screen: Screen
  servers: Servers
  storage: Storage
  dialogs: Dialogs
  toast: Toasts
  attention: Attention
  tabs: Tabs
  keybinds: Keybinds
  commands: Commands
  links: Links
  embeds: Embeds
  ui: Ui
  system: System
  desktop: Desktop | undefined
  locale: Locale
  appearance: Appearance
  router: Router
  workspaces: Workspaces
}
```

### 布局

`ctx.layout.open(key, session, options?)` 通过键打开一个面板标签页，键形如 `<plugin id>:<tab id>`。它对尚未挂载的会话也有效。

```ts
const session = ctx.sessions.current()

if (session) ctx.layout.open(`${ctx.id}:main`, session, { tab: "select", background: true })
```

- `tab: "open"` 是默认值，在预览槽位中选中该标签页。`"preview"` 让它成为新的预览，`"append"` 添加但不选中它，`"select"` 添加并选中它，同时保留预览。
- `background: true` 在窄屏上保持当前视图并打开侧边区域，适用于用户不是从面板发起的操作。
- `close(key, session)` 移除标签页并调用其面板的 `close`。`toggle(key, session)` 关闭可见的标签页，否则打开它。
- `hide(key, session)` 隐藏显示某个可见标签页的面板，但不关闭标签页：侧边区域，或用户移过去的那个底部面板。再次打开标签页会显示其面板。
- `state(key, session)`：标签页不在标签条中时为 `"closed"`；在条中但其面板显示其他标签页时为 `"open"`；面板显示它但面板被隐藏（侧边区域关闭，或底部面板隐藏）时为 `"active"`；在屏幕上时为 `"visible"`。
- `stored(session)` 是本插件保存在会话侧边标签条中的标签页 id。
- `ready()` 在已存储的布局加载完成后为 `true`；`narrow()` 在视口小于 768px 时为 `true`。
- `side.opened(session)` 在侧边区域打开时为 `true`，`side.toggle(session)` 打开或关闭它。
- `side.menu()` 按 `order` 列出每个插件的 `session.panel` [菜单项](#菜单项)，用于实现你自己的启动器。
- `side.width(panel)` 和 `side.resize(panel, width)` 读取并存储你某个面板的侧边区域宽度；参见[面板宽度](#面板宽度)。
- `sidebar.opened()` 是每个侧面板共享的内部侧边栏偏好。
- `scroll` 按会话和键存储滚动偏移。
- `settings(page?)` 打开 Settings。`project(server, title)` 打开某个项目的目录选择器和一个新草稿。
- `draft({ server, directory, prompt })` 在自己的标签页中打开一个新的草稿会话，填好提示供用户检查和发送。

```ts
const session = ctx.sessions.current()
const launchers = () => ctx.layout.side.menu().filter((item) => !item.primary && !item.opened)

if (session) {
  ctx.layout.draft({ server: session.server.id, directory: session.directory, prompt: ctx.t("setup.prompt") })
}
```

#### 参考

```ts
interface Layout {
  open(key: string, session: SessionRef, options?: OpenOptions): void
  close(key: string, session: SessionRef): void
  toggle(key: string, session: SessionRef): void
  hide(key: string, session: SessionRef): void
  state(key: string, session: SessionRef): PanelState
  stored(session: SessionRef): string[]
  ready(): boolean
  narrow(): boolean
  side: {
    opened(session: SessionRef): boolean
    toggle(session: SessionRef): void
    menu(): SessionPanelMenuItem[]
    width(panel: string): number | undefined
    resize(panel: string, width: number): void
  }
  sidebar: {
    opened(): boolean
  }
  scroll: {
    get(session: SessionRef, key: string): { x: number; y: number } | undefined
    set(session: SessionRef, key: string, value: { x: number; y: number }): void
  }
  settings(page?: string): void
  project(server: string, title: string): void
  draft(input: { server: string; directory: string; prompt: string }): void
}

type PanelState = "closed" | "open" | "active" | "visible"

interface OpenOptions {
  tab?: "open" | "preview" | "append" | "select"
  background?: boolean
}
```

### 会话与会话屏幕

`ctx.sessions.current()` 是被路由的会话，`ctx.screen.current()` 是它的屏幕。两者在首页和草稿上都是 `undefined`。在执行操作处读取它们，绝不要在 `setup` 中只读一次。

```ts
const session = ctx.sessions.current()
const file = ctx.screen.current()?.file

if (session && file) void file.sync("README.md")
```

- `key` 是 `<server id>\n<session id>`，跨服务器唯一。用它可以作为会话级状态的键。
- `tab` 是拥有该会话的外壳标签页的键。服务器还在创建它时 `pending` 为 `true`。
- `directory` 是会话的工作区目录，当它就是项目根目录时 `local` 为 `true`。
- `listedProject` 是该会话所属的侧边栏项目。
- `visit` 在会话每次被路由时都是一个新对象。
- `background` 列出该会话正在运行的子 agent 和 shell 命令。
- `ctx.sessions.list()` 返回打开的外壳标签页中的会话。
- 屏幕的 `file` 读取工作区的文件，`comment` 存放下一条提示的行内评论。`composer` 是下一条提示：它的文本、附加部分和模型；参见[附加到输入框](#附加到输入框)。
- `file.sync(path)` 加载一个文件并让服务器监视其变化。文件的标签页关闭时调用 `file.unwatch(path)`。

#### 参考

```ts
interface Sessions {
  list(): SessionRef[]
  current(): MountedSession | undefined
}

interface SessionRef {
  key: string
  id: string
  tab: string
  server: ServerRef
  pending: boolean
  location: LocationRef | undefined
}

interface MountedSession extends SessionRef {
  visit: object
  project: Project | undefined
  listedProject: { worktree: string; name?: string; icon?: Project["icon"] } | undefined
  directory: string
  local: boolean
  background: BackgroundTask[]
}

interface Screen {
  current(): SessionScreen | undefined
}

interface SessionScreen {
  file: Files
  comment: Comments
  composer: Composer
}

interface Files {
  root: string
  ready(): boolean
  resolve(path: string): string
  absolute(path: string): boolean
  get(path: string): FileState | undefined
  missing(path: string): boolean
  sync(path: string, options?: { force?: boolean; silent?: boolean }): Promise<void>
  unwatch(path: string): void
  exists(path: string): Promise<boolean>
  search(query: string, options?: { kind?: "file" | "any"; limit?: number; signal?: AbortSignal }): Promise<string[]>
  selection: {
    get(path: string): LineRange | null | undefined
    set(path: string, range: LineRange | null): void
  }
  scroll: {
    get(path: string): { top?: number; left?: number }
    set(path: string, value: { top?: number; left?: number }): void
  }
  tree: {
    list(path: string): FileNode[]
    state(path: string): { expanded: boolean; loaded?: boolean; loading?: boolean; error?: string } | undefined
    sync(path: string, options?: { force?: boolean }): Promise<void>
    expand(path: string, options?: { list?: boolean }): void
    collapse(path: string): void
  }
}

interface Comments {
  list(file?: string): Comment[]
  add(input: Omit<Comment, "id" | "time">): Comment
  update(id: string, comment: string): void
  remove(id: string): void
  focus: {
    current(): { file: string; id: string } | null
    set(value: { file: string; id: string } | null): void
  }
  active: {
    current(): { file: string; id: string } | null
    set(value: { file: string; id: string } | null): void
  }
}
```

### 附加到输入框

在事件处理函数或命令中用 `ctx.screen.current()?.composer`，把文件、备注或引用附加到用户的下一条提示。

```ts
const composer = ctx.screen.current()?.composer

composer?.attach({
  type: "note",
  origin: ctx.id,
  commentID: crypto.randomUUID(),
  label: "button#submit",
  icon: "globe",
  subject: 'element <button id="submit">Save</button>',
  comment: "Make this button primary and disable it while saving.",
  href: "http://localhost:3000/settings",
})
```

- `attach` 不会移动键盘焦点。调用 `focus()` 可把焦点移到提示框。
- `update(commentID, { comment?, preview? })` 修改一个已附加的部分；备注或引用只接受新的 `comment`。
- `detach(commentID)` 移除一个已附加的部分。
- 备注的 `live` 会在该备注仍留在本应用进程内期间替换其 `subject` 和 `href`，用于只有本进程能解析的引用，例如页面元素。存储的草稿会丢弃它，被回滚或分叉恢复的已发送消息也会丢弃它。

引用（quote）是用户从你的插件展示的内容（例如日志输出）中引用的文本，可带一条评论。它以会话时间线中引用的样式渲染，使用来源的图标和标签。先检查 `quotable()`：在子 agent 的会话中（没有输入框）以及输入框正在运行 shell 命令时，它为 `false`。

```ts
const composer = ctx.screen.current()?.composer

if (composer?.quotable()) {
  const commentID = crypto.randomUUID()

  composer.attach({
    type: "quote",
    commentID,
    text: selection,
    source: { label: ctx.t("source.label"), icon: "console", subject: "the Acme log" },
  })
  composer.focus(commentID)
}
```

- `source.subject` 告诉模型来源的名称，例如 `the terminal`。它不做本地化。
- 省略 `comment` 让用户从 chip 自己添加。
- `focus(commentID)` 打开一个已附加引用的评论编辑器。当输入框未显示时（例如窄屏上显示的是面板），编辑器会在输入框显示后打开。
- 模型读到 `The user quoted the following from <subject>:`，然后是每行以 `> ` 为前缀的文本，然后是评论（若有）。

#### 参考

```ts
interface ComposerFile {
  type: "file"
  path: string
  selection?: { startLine: number; endLine: number; startChar: number; endChar: number }
  preview?: string
  comment?: string
  commentID?: string
  commentOrigin?: "review" | "file"
}

interface ComposerNote {
  type: "note"
  origin: string
  commentID: string
  label: string
  icon: IconName
  subject: string
  comment: string
  href?: string
  live?: { subject: string; href?: string }
}

interface ComposerQuote {
  type: "quote"
  commentID: string
  text: string
  comment?: string
  source: { label: string; icon: IconName; subject: string }
}
```

### 读取和写入提示

用 `text()` 读取用户输入的内容，用 `focused()` 判断是否正在输入：

```ts
const composer = ctx.screen.current()?.composer
const empty = !composer?.text().trim()
```

- `text()` 是纯文本形式的提示：mention 以其 `@` 文本读取，附件和已附加部分不包含在内。shell 模式下它是 shell 命令。在会话的草稿加载之前它为 `""`，在子 agent 的会话（没有输入框）中也是 `""`。它是响应式的。
- `focused()` 在键盘焦点位于提示框内时为 `true`。它不是响应式的，因此在执行操作处读取它，例如命令的 `run` 中。

`insert(text)` 把文本输入提示框，供用户检查和发送。输入框上的任何东西都不会替用户发送提示。

```ts
const composer = ctx.screen.current()?.composer

composer?.insert(`Explain ${path}`)
composer?.focus()
```

- `insert` 把文本加到用户上次留在提示框中的光标处，否则加到末尾，并把光标移到其后。它不替换选中的文本。
- 文本不会被解析：`@path` 保持为文本，不变成 mention。
- `setText(text)` 替换提示文本，包括 mention。附件和已附加部分保持不变。`setText("")` 清空文本。
- 两者都不移动键盘焦点。调用 `focus()` 可把焦点移到提示框。
- 在会话存储的草稿加载之前发起的写入（`insert`、`setText`、`attach`、`update` 或 `detach`）会等待它。然后按调用顺序应用到调用时被路由的那个会话。它绝不会替换存储的草稿。
- 在没有输入框的子 agent 会话中，这些写入不起作用。

### 选择模型

`model()` 是下一条提示将使用的模型，`setModel` 像模型选择器一样选中一个：

```ts
const composer = ctx.screen.current()?.composer

if (composer && !composer.setModel({ providerID: "anthropic", modelID: "claude-sonnet-4-5", variant: "high" })) {
  ctx.toast.show({ variant: "error", title: ctx.t("model.unavailable") })
}
```

- `model()` 是用户为被路由会话做的选择，否则是 agent 的默认值，否则是应用的默认值。在模型目录加载期间、没有已连接的 provider 提供该模型时，以及子 agent 会话中，它为 `undefined`。它是响应式的。
- `setModel` 把该模型设为会话的选择及其第一个最近使用的模型。不传 `variant` 时，模型保留选择器会为它显示的变体。
- `setVariant(variant)` 选中当前模型的一个变体。`undefined` 选中模型的默认变体。
- 当目录在加载、没有已连接的 provider 提供该模型，或模型没有该变体时，`setModel` 返回 `false` 且不改变任何东西。
- 当没有当前模型或模型没有该变体时，`setVariant` 返回 `false` 且不改变任何东西。
- 在子 agent 会话中，两者都返回 `false`。

#### 参考

```ts
interface Composer {
  text(): string
  insert(text: string): void
  setText(text: string): void
  model(): ComposerModel | undefined
  setModel(model: ComposerModel): boolean
  setVariant(variant: string | undefined): boolean
  attach(part: ComposerFile | ComposerNote | ComposerQuote): void
  quotable(): boolean
  focus(commentID?: string): void
  update(id: string, patch: { comment?: string; preview?: string }): void
  detach(id: string): void
  focused(): boolean
}

interface ComposerModel {
  providerID: string
  modelID: string
  variant?: string
}
```

### 服务器与服务器事件

`ctx.servers.get(id)` 返回一个实时的 `ServerRef`。运行你插件的桌面应用自有服务器的 id 是 `"sidecar"`。用 `data.on` 响应其事件：

```ts
import { onCleanup } from "solid-js"
import { createKeyed } from "@opencode/plugin/gui"

createKeyed(
  () => ctx.servers.get("sidecar")?.data,
  (data) => onCleanup(data.on("session.created", (event) => console.log(event))),
)
```

- `id` 是宿主键：`"sidecar"`、一个 http URL，或[贡献的服务器](#服务器)的 `<plugin id>:<id>`。
- `data` 是该服务器同步的数据，例如会话和项目，`on(type, handler)` 用于其事件。它是响应式的。
- `builtin` 对应用自有服务器为 `true`。
- 当服务器版本与本应用兼容时 `compatible` 为 `true`；其事件连接建立期间 `connected` 为 `true`。
- `password` 是用户配置的 HTTP basic 密码（若有）。
- 每次都从实时的 `ServerRef` 读取 `client`、`data` 和 `url`：重启的服务器在同一个 id 下会拿到新的客户端。
- `ctx.servers.list()` 返回应用列出的服务器的 id。

#### 参考

```ts
interface Servers {
  list(): string[]
  get(id: string): ServerRef | undefined
}

interface ServerRef {
  id: string
  name: string
  url: string
  password?: string
  client: OpenCodeClient
  data: Data
  local: boolean
  builtin: boolean
  compatible: boolean
  connected: boolean
}
```

### 对话框

`ctx.dialogs.open(render, { replace? })` 在已有对话框之上打开一个对话框，并返回一个句柄，其 `close()` 可关闭它。对话框在其所属作用域结束时也会关闭。

```tsx
const handle = ctx.dialogs.open((dialog) => <ConfirmDialog onDone={dialog.close} />)
```

- `replace: true` 会先关闭所有已打开的对话框，包括宿主的和其他插件的。
- `ctx.dialogs.active()` 在任一对话框打开时为 `true`。
- 用 `ctx.ui.Dialog` 渲染内容以获得应用的对话框框架；参见[应用组件](#应用组件)。

### 询问用户

`confirm`、`alert`、`prompt` 和 `select` 在应用自己的对话框中询问，因此你的插件不需要自己的对话框 UI。每个都返回答案的 promise。

```ts
const ok = await ctx.dialogs.confirm({ title: ctx.t("end.title"), confirm: ctx.t("end"), danger: true })
```

- `confirm` 只在用户确认时解析为 `true`。`danger` 把确认按钮渲染为危险样式，且初始焦点在取消按钮上。
- 每个对话框的打开方式与 `open` 相同，并随发起询问的所属者一起关闭，否则随你的插件关闭。
- 取消、按 Escape、点击外部、被替换的对话框，或所属者结束，会让 `confirm` 解析为 `false`，`prompt` 和 `select` 解析为 `undefined`。

`alert` 告知用户一件必须确认的事，只有一个按钮。无论以何种方式关闭，它都在对话框关闭后解析：

```ts
await ctx.dialogs.alert({ title: ctx.t("export.done"), description: path })
```

`prompt` 请求一行文本。其初始 `value` 处于选中状态，输入即替换。它永远不会解析出空字符串：字段为空时提交不起作用。`secret: true` 隐藏用户输入，用于密码或 token：

```ts
const token = await ctx.dialogs.prompt({ title: ctx.t("token.title"), placeholder: "ghp_…", secret: true })
```

`select` 在可搜索列表中列出选项，类似命令面板，并解析所选选项的 `value`：

```ts
const url = await ctx.dialogs.select({
  title: ctx.t("links.title"),
  options: links.map((link) => ({ title: link.title, description: link.url, value: link.url, group: link.host })),
})

if (url) ctx.system.openExternal(url)
```

- 搜索匹配每个选项的 `title` 和 `description`。
- `group` 相同的选项列在同一标题下。
- `current` 是最初高亮的选项的值。

#### 参考

```ts
interface Dialogs {
  open(render: (dialog: DialogHandle) => JSX.Element, options?: { replace?: boolean }): DialogHandle
  confirm(options: ConfirmOptions): Promise<boolean>
  alert(options: AlertOptions): Promise<void>
  prompt(options: PromptOptions): Promise<string | undefined>
  select<T>(options: SelectOptions<T>): Promise<T | undefined>
  active(): boolean
}

interface DialogHandle {
  close(): void
}

interface ConfirmOptions {
  title: string
  description?: string
  confirm?: string
  cancel?: string
  danger?: boolean
}

interface AlertOptions {
  title: string
  description?: string
  ok?: string
}

interface PromptOptions {
  title: string
  description?: string
  placeholder?: string
  value?: string
  secret?: boolean
  submit?: string
}

interface SelectOptions<T> {
  title: string
  placeholder?: string
  options: { title: string; value: T; description?: string; group?: string }[]
  current?: T
}
```

### 应用组件

插件产物无法导入 `@opencode/ui`，因此 `ctx.ui` 把应用自带的组件交给它。它们以用户的主题、字体和语言渲染，所以你的插件 UI 的外观和行为与应用一致。

```tsx
import { Show } from "solid-js"
import { createLatest, Panel } from "@opencode/plugin/gui"

const ui = ctx.ui
const summary = createLatest(
  () => ctx.sessions.current()?.directory,
  (directory, signal) => fetchSummary(directory, signal),
)

ctx.add(Panel, {
  id: "summary",
  region: "side",
  list: () => [summaryTab],
  render: () => (
    <div>
      <ui.Tooltip value={ctx.t("copy")}>
        <ui.IconButton icon="copy" label={ctx.t("copy")} onClick={() => void ctx.system.copy(summary.latest ?? "")} />
      </ui.Tooltip>
      <Show when={summary.latest} fallback={<ui.Loader size="large" />}>
        {(text) => <ui.Markdown text={text()} />}
      </Show>
    </div>
  ),
})
```

- `Icon`、`Button` 和 `IconButton` 接受任意 `IconName`，与 SDK 的每个 `icon` 字段一样。`IconButton` 的 `label` 是其可访问名称；把它包在 `Tooltip` 里可在悬停时显示。
- 按钮上的 `busy` 会把图标替换为加载指示器并禁用按钮，直到它重新变回 `false`。
- 所有与 AI 工作无关的加载状态都使用 `Loader`，例如面板、搜索或连接的加载。
- `Menu` 打开一个 `items` 列表：操作、`{ type: "separator" }` 和 `{ type: "group", label, items }`。
- `Switch` 和 `TextInput` 不保存状态：把 `onChange` 或 `onInput` 的值传回 `checked` 或 `value`。
- `Keybind` 把按键显示为 chip，例如 `ctx.keybinds.keybind(command)`。
- `Markdown` 按时间线渲染消息的方式渲染，`Code` 显示一个高亮的只读代码块。两者在挂载后不久填充内容。

`Dialog` 是应用的对话框框架：标题、内容和按钮。从 `ctx.dialogs.open` 渲染它；在其他地方它渲染不出有用的东西。

```tsx
const ui = ctx.ui

ctx.dialogs.open((dialog) => (
  <ui.Dialog
    title={ctx.t("rename.title")}
    footer={
      <ui.Button variant="contrast" onClick={dialog.close}>
        {ctx.t("done")}
      </ui.Button>
    }
  >
    <ui.TextInput label={ctx.t("rename.label")} value={name()} onInput={setName} onSubmit={dialog.close} autofocus />
  </ui.Dialog>
))
```

- `size` 默认为 `"fit"`：宽 480px，高度随内容。`"normal"`、`"large"` 和 `"x-large"` 是固定尺寸。
- Escape 和点击外部会关闭对话框。`closable: false` 隐藏头部的关闭按钮。

#### 菜单行

`MenuItem`、`MenuSub`、`MenuGroup` 和 `MenuSeparator` 是宿主渲染的菜单（例如 `session.location.menu` 槽位）所用的行。它们可以用键盘导航、显示宿主的弱化图标和快捷键 chip，并在选择后关闭菜单。

```tsx
import { For } from "solid-js"

const ui = ctx.ui

ctx.add(Slot, {
  at: "session.location.menu",
  render: (input) => (
    <>
      <ui.MenuItem
        label={ctx.t("usage")}
        icon="status"
        keys={["Ctrl", "U"]}
        onSelect={() => openUsage(input.session)}
      />
      <ui.MenuSub label={ctx.t("openIn")} icon="outline-share">
        <For each={apps()}>{(app) => <ui.MenuItem label={app.name} onSelect={() => launch(app, input.session)} />}</For>
      </ui.MenuSub>
    </>
  ),
})
```

- `MenuItem` 接受的字段与 `Menu` 的 `items` 条目相同。
- `MenuSub` 在行旁的子菜单中打开其子项。`onOpenChange` 告诉你它何时打开，以便只在打开时加载其行。
- `MenuGroup` 把行放在一个标题下，`MenuSeparator` 在行之间画一条线。
- `MenuItem`、`MenuSub` 和 `MenuGroup` 在菜单之外会抛错：宿主会记录错误，并且不渲染该贡献的任何内容。

#### 选择器

`Select` 从一组选项中挑一个，就像应用的设置行选择语言一样。它的值是字符串；`options` 的类型把它收窄。

```tsx
const [period, setPeriod] = createSignal<"day" | "month">("day")

<ui.Select
  label={ctx.t("period")}
  options={[
    { value: "day", label: ctx.t("period.day") },
    { value: "month", label: ctx.t("period.month") },
  ]}
  value={period()}
  onChange={setPeriod}
/>
```

- `label` 是选择器的可访问名称；所选选项的 `label` 是它显示的内容。
- 没有任何选项具有的 `value` 会显示 `placeholder`。再次选择已选中的选项不会调用 `onChange`。

#### 设置组件

`SettingsLayout`、`SettingsSection` 和 `SettingsRow` 按应用渲染自己设置页面的方式渲染一个[设置页面](#设置页面)：页面头部、带标题的边框列表分区，以及带标题、描述和末端控件的行。

```tsx
<ui.SettingsLayout title={ctx.t("title")} description={ctx.t("description")} actions={<HelpButton />}>
  <ui.SettingsSection title={ctx.t("section.display")} footer={<Show when={error()}>{ctx.t("error")}</Show>}>
    <ui.SettingsRow id="acme-period" title={ctx.t("period")} description={ctx.t("period.description")}>
      <ui.Select label={ctx.t("period")} options={periods()} value={period()} onChange={setPeriod} />
    </ui.SettingsRow>
  </ui.SettingsSection>
</ui.SettingsLayout>
```

- 你自己的页面用 `SettingsLayout`，宿主页面上的分区用 `SettingsSection`，宿主分区中的行单独用 `SettingsRow`。无论哪种情况，行都会与宿主的行对齐。
- 行上的 `id` 是展示它的 `SettingEntry.id`。展示页面自身 id 的搜索会高亮头部。
- `actions` 位于标题行的末端。分区的 `footer` 位于其列表之下、边框之外。
- 它们的外观取自 Settings 屏幕的样式，因此要从 `SettingsPage` 中渲染它们。

#### 参考

```ts
interface Ui {
  Icon(props: UiIconProps): JSX.Element
  Button(props: UiButtonProps): JSX.Element
  IconButton(props: UiIconButtonProps): JSX.Element
  Tooltip(props: UiTooltipProps): JSX.Element
  Menu(props: UiMenuProps): JSX.Element
  MenuItem(props: UiMenuItem): JSX.Element
  MenuSeparator(): JSX.Element
  MenuGroup(props: UiMenuGroupProps): JSX.Element
  MenuSub(props: UiMenuSubProps): JSX.Element
  Loader(props: UiLoaderProps): JSX.Element
  Dialog(props: UiDialogProps): JSX.Element
  Switch(props: UiSwitchProps): JSX.Element
  TextInput(props: UiTextInputProps): JSX.Element
  Select<T extends string>(props: UiSelectProps<T>): JSX.Element
  Keybind(props: UiKeybindProps): JSX.Element
  Markdown(props: UiMarkdownProps): JSX.Element
  Code(props: UiCodeProps): JSX.Element
  SettingsLayout(props: UiSettingsLayoutProps): JSX.Element
  SettingsSection(props: UiSettingsSectionProps): JSX.Element
  SettingsRow(props: UiSettingsRowProps): JSX.Element
}

interface UiIconProps {
  name: IconName
  size?: "small" | "normal" | "large"
  class?: string
}

interface UiButtonProps {
  children: JSX.Element
  onClick?: (event: MouseEvent) => void
  variant?: "neutral" | "contrast" | "ghost" | "ghost-muted" | "danger"
  size?: "small" | "normal" | "large"
  icon?: IconName
  disabled?: boolean
  busy?: boolean
  type?: "button" | "submit"
  autofocus?: boolean
  class?: string
}

interface UiIconButtonProps {
  icon: IconName
  label: string
  onClick?: (event: MouseEvent) => void
  variant?: "neutral" | "ghost" | "ghost-muted"
  size?: "small" | "normal" | "large"
  disabled?: boolean
  pressed?: boolean
  busy?: boolean
  class?: string
}

interface UiTooltipProps {
  value: JSX.Element
  keys?: string[]
  placement?: "top" | "bottom" | "left" | "right"
  children: JSX.Element
}

interface UiMenuProps {
  label: string
  items: UiMenuEntry[]
  trigger?: "icon" | "button"
  icon?: IconName
  placement?: "bottom-start" | "bottom-end" | "top-start" | "top-end"
  disabled?: boolean
}

type UiMenuEntry = UiMenuItem | UiMenuSeparator | UiMenuGroup

interface UiMenuItem {
  type?: "item"
  label: string
  icon?: IconName
  keys?: string[]
  disabled?: boolean
  onSelect(): void
}

interface UiMenuSeparator {
  type: "separator"
}

interface UiMenuGroup {
  type: "group"
  label: string
  items: UiMenuItem[]
}

interface UiMenuGroupProps {
  label: string
  children: JSX.Element
}

interface UiMenuSubProps {
  label: string
  icon?: IconName
  disabled?: boolean
  onOpenChange?: (open: boolean) => void
  children: JSX.Element
}

interface UiLoaderProps {
  size?: "small" | "normal" | "large"
  class?: string
}

interface UiDialogProps {
  title: string
  description?: string
  children?: JSX.Element
  footer?: JSX.Element
  size?: "fit" | "normal" | "large" | "x-large"
  closable?: boolean
}

interface UiSwitchProps {
  checked: boolean
  onChange: (checked: boolean) => void
  label: string
  hideLabel?: boolean
  description?: string
  disabled?: boolean
}

interface UiTextInputProps {
  value: string
  onInput: (value: string) => void
  label: string
  placeholder?: string
  onSubmit?: (value: string) => void
  type?: "text" | "password" | "search" | "url"
  size?: "normal" | "large"
  disabled?: boolean
  invalid?: boolean
  autofocus?: boolean
  class?: string
}

interface UiKeybindProps {
  keys: string[]
  class?: string
}

interface UiMarkdownProps {
  text: string
  class?: string
}

interface UiCodeProps {
  content: string
  language?: string
  class?: string
}

interface UiSelectProps<T extends string> {
  options: UiSelectOption<T>[]
  value: T | undefined
  onChange: (value: T) => void
  label: string
  placeholder?: string
  disabled?: boolean
  invalid?: boolean
  placement?: "bottom-start" | "bottom-end" | "top-start" | "top-end"
  class?: string
}

interface UiSelectOption<T extends string> {
  value: T
  label: string
}

interface UiSettingsLayoutProps {
  title: string
  description?: string
  actions?: JSX.Element
  children: JSX.Element
}

interface UiSettingsSectionProps {
  title?: string
  children: JSX.Element
  footer?: JSX.Element
}

interface UiSettingsRowProps {
  title: JSX.Element
  description?: JSX.Element
  id?: string
  children?: JSX.Element
}
```

### Toast

`ctx.toast.show` 在窗口角落显示一条短消息，并返回一个句柄，其 `dismiss()` 可关闭它。

```ts
ctx.toast.show({ variant: "success", title: ctx.t("invite.copied") })
```

- `variant` 是 `"default"`、`"success"`、`"error"` 或 `"loading"`。`success` toast 会显示对勾图标，除非你设置了 `icon`。
- `duration` 是 toast 显示的时长，以毫秒计。默认 5 秒。
- `persistent: true` 让 toast 保持显示，直到用户或 `dismiss()` 关闭它，并忽略 `duration`。
- 与一个仍在显示的 toast 相同时，会替换它而不是再叠一份。
- 你的插件的 toast 会在它停止时关闭，因此不会有按钮比运行它的代码活得更久。toast 不会随显示它的组件或 `createKeyed` 运行而关闭。

工作运行期间显示一个 `loading` toast，工作结束时关闭它：

```ts
const saving = ctx.toast.show({ variant: "loading", title: ctx.t("saving"), persistent: true })
await save()
saving.dismiss()
```

`actions` 添加按钮。点击会运行该操作并关闭 toast：

```ts
ctx.toast.show({
  variant: "error",
  title: ctx.t("sync.failed"),
  actions: [{ label: ctx.t("retry"), run: () => void sync() }],
})
```

#### 参考

```ts
interface Toasts {
  show(options: ToastOptions): ToastHandle
}

interface ToastHandle {
  dismiss(): void
}

interface ToastOptions {
  title: string
  description?: string
  variant?: "default" | "success" | "error" | "loading"
  icon?: IconName
  duration?: number
  persistent?: boolean
  actions?: ToastAction[]
}

interface ToastAction {
  label: string
  run(): void
}
```

### 通知

`ctx.attention.notify` 在用户看向别处时引起其注意：一条系统通知和一个声音，规则与应用自带的通知相同。

```ts
const session = ctx.sessions.current()

if (session) {
  void ctx.attention.notify({
    title: ctx.t("tests.done"),
    message: ctx.t("tests.summary", { failed: 0 }),
    session: { server: session.server.id, id: session.id },
    id: run.id,
  })
}
```

- 系统通知只在没有任何应用窗口持有焦点时显示。声音则无论如何都会播放。
- 两者都遵循 **Settings > Notifications**。`variant: "default"` 遵循 **Agent** 行，`variant: "error"` 遵循 **Errors** 行。两者的桌面通知默认关闭；声音是开启的。
- `sound: false` 永远不播放声音。
- 点击通知会把应用带到前台，并打开你提供的 `session`。
- 每个应用窗口都运行你的插件自己的副本。传入事件的 `id`（例如一次运行的 id），这样只有第一个发送它的窗口会通知并播放声音。没有 `id` 时，每次调用都会通知。
- 在应用界面挂载之前，`notify` 会等待它。

`notify` 从不 reject。它解析自己做了什么：应用请求系统显示通知时 `notification` 为 `true`，声音已开始时 `sound` 为 `true`。

```ts
const result = await ctx.attention.notify({ title: ctx.t("deploy.failed"), variant: "error" })

if (!result.notification) ctx.toast.show({ variant: "error", title: ctx.t("deploy.failed") })
```

- 用户关闭了通知、某个应用窗口持有焦点，或另一个窗口已经发送了同一个 `id` 时，`notification` 为 `false`。系统仍可能隐藏应用请求显示的通知，例如用户拒绝了浏览器的权限时。

#### 参考

```ts
interface Attention {
  notify(options: NotifyOptions): Promise<NotifyResult>
}

interface NotifyOptions {
  title: string
  message?: string
  variant?: "default" | "error"
  session?: { server: string; id: string }
  sound?: boolean
  id?: string
}

interface NotifyResult {
  notification: boolean
  sound: boolean
}
```

### 用量数据

会话的 token、费用和计划数据在其服务器的数据中，与应用为头部 "28k · $0.28" 读取的是同一个响应式 store。请从那里读取，而不是从 opencode 的数据库。

```ts
import { lastAssistantWithUsage } from "@opencode/client/solid"

const data = session.server.data
const info = () => data.session.get(session.id)

const tokens = () => info()?.tokens // this session's tokens by kind
const cost = () => data.session.cost(session.id) // USD, with subagent sessions
const step = () => lastAssistantWithUsage(data.session.message.list(session.id), info()?.revert?.messageID)
const limits = () => (session.location ? data.location.usage.limits(session.location) : undefined)
```

- `step()` 是当前填充上下文窗口的那个助手步骤，与应用的上下文环使用的是同一个。把它与 `data.location.model.list` 中模型的 `limit.context` 比较。
- 一旦 `data.location.usage.sync(location)` 加载完成，`limits()` 持有 OpenCode Console 的预算和 Go 计划额度。服务器报告没有时它为 `null`。

### 标签页

`ctx.tabs` 读取并更改外壳的标签条：即作为标签页打开的会话和草稿。下面代码在某次运行结束时把会话的标签页移到最前：

```ts
import { onCleanup } from "solid-js"
import { createKeyed } from "@opencode/plugin/gui"

createKeyed(
  () => ctx.servers.get("sidecar")?.data,
  (data) =>
    onCleanup(
      data.on("session.execution.succeeded", (event) => {
        const tab = ctx.tabs.list().find((item) => item.session?.id === event.data.sessionID)

        if (tab) ctx.tabs.move(tab.key, 0)
      }),
    ),
)
```

- `list()` 按标签条顺序返回打开的标签页。它是响应式的。草稿的 `session` 为 `undefined`；屏幕上的标签页 `active` 为 `true`。
- `open({ server, id }, { focus? })` 把一个会话作为标签页打开在标签条末尾，除非 `focus` 为 `true`，否则在后台打开。已经打开的会话保留其标签页，由父会话标签页展示的子 agent 也是如此。
- `focus(key)` 显示一个标签页，`move(key, index)` 移动它，`close(key)` 像用户那样关闭它。
- 不属于任何打开标签页的键不起作用。在应用界面挂载之前发起的写入会等待它。

#### 参考

```ts
interface Tabs {
  list(): ShellTab[]
  open(session: { server: string; id: string }, options?: { focus?: boolean }): void
  focus(key: string): void
  move(key: string, index: number): void
  close(key: string): void
}

interface ShellTab {
  key: string
  session: SessionRef | undefined
  active: boolean
}
```

### 按键绑定

`ctx.keybinds` 读取用户为某个已发布命令 id 设置的快捷键。

```ts
const label = ctx.keybinds.keybind(`${ctx.id}.open`)
const chord = ctx.keybinds.keys("mod+k")
const pressed = (event: KeyboardEvent) => ctx.keybinds.matches(`${ctx.id}.open`, event)
```

- `keybind(command)` 返回命令实际生效的按键绑定的展示部分，例如 `["Ctrl", "K"]`。命令未绑定时为空。
- `keys(bind)` 返回一个应用不拥有的组合键的展示部分，例如某个页面自行处理的键。
- `matches(command, event)` 在事件匹配命令实际生效的按键绑定时为 `true`。

#### 参考

```ts
interface Keybinds {
  keybind(command: string): string[]
  keys(bind: string): string[]
  matches(command: string, event: KeyboardEvent): boolean
}
```

### 运行命令

`ctx.commands.run(id)` 以在命令面板中选择该命令的方式运行它。当命令无法运行时返回 `false`：

```ts
if (!ctx.commands.run("terminal.toggle")) ctx.toast.show({ title: ctx.t("terminal.unavailable") })
```

- `id` 是任意插件的已发布插件命令 `<plugin id>.<command id>`，或应用自带的命令之一，例如 `command.palette`。
- 应用的命令 id 不是稳定 API，可能在版本之间变化。
- 没有启用的命令拥有该 id 时，`run` 返回 `false`。已列出但被禁用的命令不会运行。
- 在应用界面挂载之前，没有任何命令注册，因此 `run` 返回 `false`。
- `run` 不等待命令的异步工作。

#### 参考

```ts
interface Commands {
  run(id: string): boolean
}
```

### 系统与环境

`ctx.system` 在每个平台上都可用。`ctx.desktop` 增加仅桌面端可用的能力，在 web 上是 `undefined`。

```ts
const show = async (path: string) => {
  if (ctx.desktop && (await ctx.desktop.reveal(path))) return
  await ctx.system.copy(path)
}
```

- `system.save` 在桌面端显示保存对话框，在 web 上下载。用户取消对话框时返回 `false`。
- `system.openExternal` 在系统浏览器中打开 URL。应用内的链接请使用 `ctx.links.open`，它会把 `Link` 路由到其[链接处理器](#链接处理器)。
- `desktop.launch(path, app?)` 用某个应用（或默认应用）打开路径。`desktop.reveal(path)` 在文件管理器中显示它。
- `ctx.embeds` 在窗口中渲染主进程的 Web 视图；参见[内嵌 Web 视图](#内嵌-web-视图)。
- `ctx.locale` 读取界面语言及其书写方向。`ctx.appearance.font("mono")` 是用户终端字体的 CSS font family。
- `ctx.router` 读取当前路由路径以及路由切换是否正在进行。
- `ctx.workspaces.on("remove", handler)` 在用户从服务器移除一个工作区目录时运行，以便你清理以它为作用域的 store。

`desktop.pick(options)` 用系统的打开对话框向用户请求文件或文件夹，并解析其绝对路径：

```ts
const [folder] = (await ctx.desktop?.pick({ directory: true, title: ctx.t("pick.folder") })) ?? []

if (folder) await ctx.client.rpc(Acme).index({ directory: folder })
```

- `directory: true` 选择文件夹而不是文件，`multiple: true` 允许用户选择多个。
- `extensions` 限定可选择的文件，不带点，例如 `["json"]`。文件夹忽略它。
- `title` 是对话框标题。并非所有系统都会显示它。
- 用户取消时路径为空。对话框无法打开时 `pick` 会 reject。
- `pick` 仅限桌面端：浏览器永远不会告诉页面所选文件的位置。

`ctx.appearance.mode()` 是界面显示的配色方案，`"light"` 或 `"dark"`。它是响应式的：

```ts
const background = () => (ctx.appearance.mode() === "dark" ? "#000" : "#fff")
```

- 它跟随用户在 **Settings > Appearance** 中的选择，**System** 会解析为系统当前的方案。
- 在应用界面挂载之前，它是系统的方案。

#### 参考

```ts
interface System {
  copy(text: string): Promise<void>
  save(file: { name: string; content: string }): Promise<boolean>
  openExternal(url: string): void
}

interface Desktop {
  os: "macos" | "windows" | "linux"
  zoom(): number
  launch(path: string, app?: string): Promise<void>
  reveal(path: string): Promise<boolean>
  installed(app: string): Promise<boolean>
  pick(options?: PickOptions): Promise<string[]>
}

interface PickOptions {
  directory?: boolean
  multiple?: boolean
  title?: string
  extensions?: string[]
}

interface Links {
  open(link: Link): boolean
  exists(link: Link): boolean | Promise<boolean>
}

interface Locale {
  locale(): string
  direction(): "ltr" | "rtl"
}

interface Appearance {
  font(kind: "mono"): string
  mode(): "light" | "dark"
}

interface Router {
  path(): string
  routing(): boolean
}

interface Workspaces {
  on(event: "remove", handler: (value: { server: string; directory: string }) => void): Cleanup
}
```

## 存储状态

桌面窗口通过 IPC 加载存储状态，而 web 端立即读取 `localStorage`。在 `Plugin.define({ stores })` 中声明 store，宿主会替你加载它们。

- **`Store.global`** 为整个应用保存一个值。它在 `setup` 运行之前加载，因此 `ctx.stores.name.value` 永远不是 `undefined`。
- **`Store.session`** 为每个会话保存一个值。它在会话挂载时加载；在此之前 `ctx.stores.name(session).value` 为 `undefined`。

声明的 store 是给窗口用的。`main` 用 `ctx.storage.store` 打开其状态，它是同步读取的；参见[主上下文](#主上下文)。

用 `update(draft => …)` 原地修改值，它必须不返回任何东西，或用 `set(next)` 替换它：

```ts
const enabled = ctx.stores.prefs.value.enabled

ctx.stores.prefs.update((draft) => {
  draft.enabled = !draft.enabled
})
```

- `ready()` 在值加载完成后为 `true`。在此之前发起的写入会等待，并按调用顺序应用。
- `from` 指定其他存储键，在 store 还没有值时从中一次性导入值，例如你重命名过的 store 的键：`"plugin.acme.settings"`。传入一个列表可以依次尝试多个键，最新的在前。在 store 被移除之前，另一个键会保留它的副本。

```ts
stores: {
  prefs: Store.global(Prefs, { enabled: true }, ["plugin.acme.settings.v2", "plugin.acme.settings"]),
}
```

#### 参考

```ts
const Store: {
  global(schema: Schema, initial: T, from?: string | string[]): StoreDeclaration
  session(schema: Schema, initial: T, from?: string | string[]): StoreDeclaration
}

interface Persisted<T, V = T | undefined> {
  value: V
  ready(): boolean
  update(mutate: (draft: T) => undefined): void
  set(next: T): void
}
```

### 运行时 store

`ctx.storage.store(key, options)` 为只在运行时才知道的键打开一个 store。`scope` 按服务器、目录或会话各保存一个值。

```tsx
import { Schema } from "effect"
import { usePlugin, type MountedSession } from "@opencode/plugin/gui"
import type { definition } from "./definition"

function DraftView(props: { readonly session: MountedSession }) {
  const ctx = usePlugin<typeof definition>()

  const draft = ctx.storage.store("draft", {
    schema: Schema.Struct({ text: Schema.String }),
    initial: { text: "" },
    scope: { server: props.session.server.id, directory: props.session.directory },
  })

  return <p>{draft.value?.text}</p>
}
```

- `scope: "global"` 是默认值，为整个应用保存一个值。
- `scope: { server, directory? }` 为每个服务器保存一个值，或为其上的每个工作区目录保存一个值。
- `scope: { session }` 为每个会话保存一个值，会话移动到新目录时会重新打开。
- 运行时 store 的 `value` 在加载之前是 `undefined`。
- `ctx.storage.memory(key, { initial })` 保存窗口本地的状态，它能在插件重载后存续，但不能在窗口重载后存续。
- `ctx.storage.remove(key, { scope, from })` 删除值，键会重新读出 `initial`。

#### 参考

```ts
interface Storage {
  store(key: string, options: StoreOptions): Persisted<T>
  memory(key: string, options: { initial: T }): [Store<T>, (mutation: (draft: T) => void) => void]
  remove(key: string, options?: { scope?: StorageScope; from?: string | string[] }): void
}

interface StoreOptions {
  schema: Schema
  initial: T
  scope?: StorageScope
  from?: string | string[]
}

type StorageScope = "global" | { server: string; directory?: string } | { session: SessionRef }
```

## 响应式原语

优先使用这些助手，而不是原始的 `createEffect`、`createRenderEffect` 和 `createComputed`。它们遵循插件的生命周期及其依赖的重启，而手写的 effect 往往在这两方面出错。

### createKeyed

`createKeyed(source, fn, { otherwise?, equals? })` 为每个键在一个全新的 owner 中运行 `fn`：`ctx.use` 访问器的每个活跃代（generation），或普通访问器的每个值。在 `fn` 内注册的任何东西都随该次运行结束。

```tsx
import { onCleanup } from "solid-js"
import { createKeyed, usePlugin, type SessionScreen } from "@opencode/plugin/gui"
import { Changes } from "@opencode/plugin/gui/review"

function ChangedFiles(props: { readonly screen: SessionScreen }) {
  const ctx = usePlugin()

  // Each active generation of Changes keeps this view's changes loaded; the watch ends with it.
  createKeyed(ctx.use(Changes), (changes) => onCleanup(changes.watch(props.screen, "files")))

  return <FileMarkers screen={props.screen} />
}
```

- `otherwise` 在源没有键时运行：一个未活跃的 `Live` 访问器，或值为 `undefined`、`null` 或 `false` 的普通访问器。
- `equals` 决定普通访问器的新值是否为同一个键，从而不再次运行 `fn`。当源每次都构建新对象时使用它。`Live` 访问器始终按代（generation）作为键。

#### 参考

```ts
function createKeyed<T>(
  source: () => Live<T> | T,
  fn: (value: T) => void,
  options?: { otherwise?(): void; equals?(previous: T, next: T): boolean },
): void
```

### createLatest

`createLatest(source, (value, signal) => promise)` 在 `source` 变化时获取数据，中止过期的请求，并且从不挂起。

```ts
const summary = createLatest(
  () => ctx.sessions.current()?.directory,
  (directory, signal) => fetchSummary(directory, signal),
)
const text = () => summary.latest ?? ""
```

- `latest` 是最近一次结果，在更新的请求运行期间保留。第一次之前为 `undefined`。
- `loading` 在针对当前值的请求进行中时为 `true`。
- `error` 是当前请求的 rejection（若有）。

#### 参考

```ts
function createLatest<S, T>(
  source: () => Live<S> | S,
  fetch: (value: S, signal: AbortSignal) => Promise<T>,
): { latest: T | undefined; loading: boolean; error: unknown }
```

### createVisitState

`createVisitState(initial)` 创建一个 `[value, setValue]` signal，每当用户离开会话再返回时都会重置。

```ts
const [expanded, setExpanded] = createVisitState(false)
```

#### 参考

```ts
function createVisitState<T>(initial: T): [value: () => T, set: (next: T) => void]
```

### usePanel 和 useDrawer

`usePanel()` 读取外围的面板框架，在面板渲染之外会抛错。`useDrawer()` 返回贡献外围的移动端抽屉，在其之外为 `undefined`。

```ts
const panel = usePanel()
const drawer = useDrawer()
const compact = () => panel.placement() === "mobile"
const close = () => drawer?.close()
```

- `placement()` 在侧边区域中为 `"side"`，在窄屏视图中为 `"mobile"`。
- `visible()` 在区域打开且该标签页被选中时为 `true`。区域播放关闭动画期间 `present()` 保持 `true`。
- `reserve()` 要求你在头部末端留出宿主区域开关的空间。
- `sidebar` 是每个侧面板共享的内部侧边栏偏好。带侧边栏的面板自己渲染它的开关。
- `drawer.open(view)` 用某个视图替换抽屉的视图，并带一个返回控件。

#### 参考

```ts
function usePanel(): PanelFrame
function useDrawer(): { close(): void; open(view: DrawerView): void } | undefined

interface PanelFrame {
  visible(): boolean
  present(): boolean
  placement(): "side" | "mobile"
  reserve(): boolean
  animate(): boolean
  open(): string[]
  sidebar: {
    opened(): boolean
    width(): number
    transition(): boolean
    resize(width: number): void
    toggle(): void
  }
}

interface DrawerView {
  title: string
  content: JSX.Element
  trigger: HTMLElement
}
```

## 应用契约

应用向每个插件提供这些契约。用 `ctx.use(token)` 跟随其中一个，并在它不是 `active` 时处理好，就像对待其他插件的契约一样。例如 `Browser` 在 web 上是 `inactive` 的。

### 文件

`@opencode/plugin/gui/file` 导出应用的文件树和 **Open in** 按钮，以及 `FileViewer` 注册表。

```tsx
import { bindPlugin } from "@opencode/plugin/gui"
import { FileViewer, type FileViewerProps } from "@opencode/plugin/gui/file"

// A viewer for a kind of file the file view does not render itself.
ctx.add(FileViewer, {
  kinds: ["document"],
  View: bindPlugin((props: FileViewerProps) => <AcmeDoc bytes={props.bytes} onError={props.onError} />),
})
```

- **`FileTree`** 是一个契约。`Tree` 和 `List` 渲染带变更标记的工作区文件的虚拟化树或列表。用 `ctx.use(FileTree)` 读取。树的 `labels` 在文件夹名称后追加文本，例如它有多少条目。
- **`OpenInApp`** 是一个契约。`Button` 是桌面端会话工作区的 **Open in** 按钮。
- **`FileViewer`** 是一个注册表。查看器列出它渲染的 `kinds`，可以用 `problem` 拒绝字节，并渲染一个报告 `onDetails` 和 `onError` 的 `View`。

#### 参考

```ts
interface FileTree {
  Tree(props: FileTreeProps): JSX.Element
  List(props: FileListProps): JSX.Element
}

interface FileTreeProps {
  screen: SessionScreen
  session: MountedSession
  allowed: string[]
  kinds?: Map<string, ChangeKind>
  labels?: Map<string, string>
  active?: string
  onFileClick(path: string): void
}

interface FileListProps {
  screen: SessionScreen
  session: MountedSession
  files: string[]
  kinds?: Map<string, ChangeKind>
  active?: string
  highlighted?: string
  onFileClick(path: string): void
}

interface OpenInApp {
  Button(props: { screen: SessionScreen; session: MountedSession }): JSX.Element
}

interface FileViewer {
  kinds: ArtifactKind[]
  problem?(bytes: Uint8Array): string | undefined
  View: Component<FileViewerProps>
}

interface FileViewerProps {
  bytes: Uint8Array
  onDetails(details: string[]): void
  onError(reason?: string): void
}
```

### 审查变更

`@opencode/plugin/gui/review` 导出 `Changes`（应用对会话变更的视图）和 `ChangeKind`（`"add"`、`"del"` 或 `"mix"`）。

```ts
import { Changes } from "@opencode/plugin/gui/review"

const changes = ctx.use(Changes)

const count = () => {
  const live = changes()
  const session = ctx.sessions.current()

  return live.status === "active" && session ? live.value.diffs(session).length : 0
}
```

- `diffs(session)` 是当前审查模式下的 diff，一旦加载完成 `ready(session)` 为 `true`。两者都是响应式的。只有被路由的会话有变更；其他会话读取为空。
- `kinds(session)` 把每个变更的文件和目录映射到其 `ChangeKind`。
- `active(session)` 是审查面板显示的文件。
- `details(session)` 是会话目录的未提交变更，无论审查模式是什么。
- `focus(session, path)` 在审查面板中显示一个文件，`open(session)` 显示全部变更。
- `watch(screen, source)` 在某个视图展示变更期间保持其变更处于加载状态，并跨该视图的会话切换。传入来自面板或槽位输入的所属 screen。它返回一个停止监视的函数；参见 [createKeyed](#createkeyed)。
- `tree` 监视是一份持久的变更列表：打开侧边区域会刷新它。`details` 监视会加载 `details(session)`。

#### 参考

```ts
interface Changes {
  diffs(session: SessionRef): FileDiffInfo[]
  ready(session: SessionRef): boolean
  kinds(session: SessionRef): Map<string, ChangeKind>
  active(session: SessionRef): string | undefined
  details(session: SessionRef): FileDiffInfo[] | undefined
  focus(session: SessionRef, path: string): void
  open(session: SessionRef): void
  watch(screen: SessionScreen, source: "tree" | "files" | "details"): () => void
}

type ChangeKind = "add" | "del" | "mix"
```

### Browser

`@opencode/plugin/gui/browser` 导出 `Browser`，即会话的桌面浏览器面板。

```ts
import { Browser } from "@opencode/plugin/gui/browser"

const session = ctx.sessions.current()
const live = ctx.use(Browser)()
const url = "http://localhost:3000"

if (session && live.status === "active" && live.value.canOpen(session, url)) live.value.open(session, url)
```

- `attached(session)` 在该会话拥有浏览器面板时为 `true`。
- `canOpen(session, path?)` 在工作区文件或 http(s) URL 可以在面板中打开时为 `true`。
- `open(session, url)` 在会话的侧面板中把 URL 作为浏览器标签页打开。
- `openFile(session, path)` 把工作区文件作为 `file://` 标签页打开。

#### 参考

```ts
interface Browser {
  attached(session: SessionRef): boolean
  canOpen(session: SessionRef, path?: string): boolean
  open(session: SessionRef, url: string): void
  openFile(session: SessionRef, path: string): void
}
```

## 主进程

在 OpenCode Desktop 上，插件的 `main` setup 在 Electron 主进程中运行一次，是应用级单例。它可以完全访问 Node.js 内置模块、`electron` 和主进程宿主 API。把它传给插件 [`./gui-experimental` 文件](#定义-gui-插件)中的 `Plugin.define`，与窗口的 `setup` 并列或单独使用。

```tsx title="src/gui.tsx"
import { Schema } from "effect"
import { powerSaveBlocker } from "electron"
import { Plugin } from "@opencode/plugin/gui"
import { KeepAwake } from "./gui/contract"

export default Plugin.define({
  main(ctx) {
    const stored = ctx.storage.store("keepScreenActive", { schema: Schema.Boolean, initial: false })
    let blockerId: number | undefined

    const release = () => {
      if (blockerId === undefined) return
      powerSaveBlocker.stop(blockerId)
      blockerId = undefined
    }

    const setActive = (enabled: boolean) => {
      if (enabled && blockerId === undefined) blockerId = powerSaveBlocker.start("prevent-display-sleep")
      if (!enabled) release()
      stored.set(enabled)
    }

    if (stored.value) setActive(true)

    ctx.provide(KeepAwake, {
      screenActive: () => blockerId !== undefined && powerSaveBlocker.isStarted(blockerId),
      setScreenActive: (enabled) => setActive(enabled),
    })

    return release
  },
})
```

在窗口中，`electron` 是惰性占位符，因此在共享的 `./gui-experimental` 文件中这个导入是安全的。参见[一个文件，两个进程](#一个文件两个进程)。

## 主上下文

`main` 收到的是 `MainContext`。与窗口的 `setup` 不同，`main` 可以是 `async` 的，并且可以返回（或解析为）一个清理函数。

```ts
main(ctx) {
  ctx.log.write("info", "acme started", { version: ctx.app.version })
}
```

- `ctx.options`、`ctx.client` 和 `ctx.app` 是[共享上下文](#共享上下文)。在 `main` 中，`ctx.app.platform` 始终是 `"desktop"`。
- `ctx.storage.store(key, { schema, initial })` 在插件的命名空间中同步打开一个 store。它的 `value` 始终有定义，每次 `set` 或 `update` 都在返回之前写入数据库。`ctx.storage.remove(key)` 删除值。
- `ctx.signal` 在插件被禁用、重新加载或移除，或应用退出时中止。`ctx.onCleanup(fn)` 会在那时运行 `fn`；参见[生命周期与清理](#生命周期与清理)。
- `ctx.provide` 在插件 id 之下实现一个 `Ipc`；参见[定义并提供 Ipc](#定义并提供-ipc)。
- `ctx.add` 向主进程注册表（如 [`MenubarItem`](#原生应用菜单)）做出贡献。
- `ctx.windows` 列出应用的窗口，并报告某个窗口何时打开或关闭。
- `ctx.embeds` 把 `WebContentsView` 放进窗口的布局；参见[内嵌 Web 视图](#内嵌-web-视图)。
- `ctx.serverEndpoints.get(id)` 返回某个服务器的 URL 和凭证。桌面应用自有服务器是 `"sidecar"`。
- `ctx.cli` 描述桌面应用运行的 OpenCode CLI。
- `ctx.log.write` 写入桌面日志文件。

#### 参考

`@opencode/plugin/gui/main` 把下面的 `MainStorage` 和 `MainEmbeds` 作为 `Storage` 和 `Embeds` 导出。

```ts
interface MainContext {
  id: string
  options: PluginOptions
  client: OpenCodeClient
  app: App
  signal: AbortSignal
  onCleanup(fn: Cleanup): void
  storage: MainStorage
  provide<S extends IpcSpec>(token: Ipc<S>, impl: IpcImpl<S>): IpcProvider<S>
  add<T>(registry: Registry<T>, item: () => T | undefined): Cleanup
  add<T>(registry: Registry<T>, item: T): Cleanup
  list<T>(registry: Registry<T>): T[]
  t(key: string, params?: Record<string, string | number | boolean>): string
  plural(key: string, count: number, params?: Record<string, string | number | boolean>): string
  windows: Windows
  embeds: MainEmbeds
  serverEndpoints: { get(id: string): ServerEndpoint | undefined }
  cli: { version: string; command: string[]; binary?: string; development: boolean }
  log: { write(level: "debug" | "info" | "warn" | "error", message: string, data?: Record<string, unknown>): void }
}

interface MainStorage {
  store(key: string, options: { schema: Schema; initial: T }): Persisted<T, T>
  remove(key: string): void
}

interface Windows {
  get(id: number): BrowserWindow | undefined
  list(): BrowserWindow[]
  focused(): BrowserWindow | undefined
  on(event: "open" | "close", handler: (window: BrowserWindow) => void): Cleanup
}

interface ServerEndpoint {
  id: string
  url: string
  headers: Record<string, string>
  sameMachine: boolean
  password?: string
}
```

## 定义并提供 Ipc

`Ipc` spec 可以声明每个窗口的 `state`、可调用的 `methods`，以及推送的 `events`。Effect `Schema` 校验并编码每一个跨越该桥接的值。

```ts title="src/gui/contract.ts"
import { Schema } from "effect"
import { Ipc } from "@opencode/plugin/gui"

export const Counter = Ipc.define({
  id: "acme.counter",
  state: Schema.Struct({ count: Schema.Number }),
  methods: {
    increment: {
      input: Schema.Number,
      output: Schema.Number,
    },
    reset: {},
  },
  events: {
    overflow: Schema.Struct({ limit: Schema.Number }),
  },
})
```

- id 是你的插件 id 或以其为前缀，例如 `acme.counter`。对其他 id，`main` 中的 `ctx.provide` 和窗口中的 `ctx.main` 都会抛错。
- 不接收参数的方法省略 `input`，不返回值的方法省略 `output`。

#### 参考

```ts
interface IpcSpec {
  id: string
  state?: Schema
  methods: Record<string, { input?: Schema; output?: Schema }>
  events?: Record<string, Schema>
}
```

### 在 main 中实现 provider

每个方法收到解码后的输入和一个 `Caller`（`{ window, signal }`）。当 `state` 变化时调用 `provider.changed(window?)`，把新快照推送给已订阅的窗口，或调用 `provider.emit(name, payload, window?)` 发送事件。

```ts title="src/gui/main.ts"
import type { Plugin } from "@opencode/plugin/gui"
import { Counter } from "./contract"

export const main: Plugin.MainSetup = (ctx) => {
  const counts = new Map<number, number>()

  const provider = ctx.provide(Counter, {
    state: (window: number) => ({ count: counts.get(window) ?? 0 }),
    increment: (step, caller) => {
      const next = (counts.get(caller.window) ?? 0) + step
      counts.set(caller.window, next)
      provider.changed(caller.window)

      if (next > 100) provider.emit("overflow", { limit: 100 }, caller.window)

      return next
    },
    reset: (_input, caller) => {
      counts.set(caller.window, 0)
      provider.changed(caller.window)
    },
  })
}
```

- 带 `state` 的 spec 在实现中还需要 `state(window)`。主进程会在窗口订阅时以及每次 `changed` 时读取它。
- 抛错的方法会让窗口的调用 reject。
- 省略 `window` 时，`changed` 和 `emit` 会到达每个窗口。
- `dispose()` 提前撤回该 `Ipc`。在插件再次提供它或停止之前，窗口看到它处于 `pending`，`ctx.main` 调用会等待。宿主也会在插件停止时撤回它。

#### 参考

```ts
type IpcImpl<S extends IpcSpec> = {
  [Name in keyof S["methods"]]: (input: Input<Name>, caller: Caller) => Output<Name> | Promise<Output<Name>>
} & { state(window: number): State }

interface Caller {
  window: number
  signal: AbortSignal
}

interface IpcProvider<S extends IpcSpec> {
  changed(window?: number): void
  emit(name: keyof S["events"], data: EventData, window?: number): void
  dispose(): void
}
```

### 在窗口中使用 Ipc

在窗口中，`ctx.main(Counter)` 返回你的 `main` 提供的那个 `Ipc` 的客户端。没有 `input` schema 的方法只接受可选的 `{ signal }` 调用选项。不要把 `undefined` 作为它的第一个参数传入。

```tsx title="src/gui/window.tsx"
import { Command, type Plugin } from "@opencode/plugin/gui"
import { Counter } from "./contract"
import type { definition } from "./definition"

export const setup: Plugin.Setup<typeof definition> = (ctx) => {
  const counter = ctx.main(Counter)

  // Follows main across restarts; removed when the plugin stops.
  counter.on("overflow", (data) => console.log(`Counter exceeded ${data.limit}`))

  ctx.add(Command, () => ({
    id: "increment",
    title: ctx.t("command.increment"),
    enabled: ctx.app.platform === "desktop",
    run: async () => {
      await counter.increment(1, { signal: ctx.signal })
      await counter.reset({ signal: ctx.signal })
    },
  }))
}
```

- 调用在 `main` 启动期间会等待。当 `main` 无法应答时它会 reject：在 web 上，当插件的 `main` 未运行或已失败时，以及方法抛错时。在用户需要反馈的地方捕获该 rejection。
- `state()` 和 `on()` 会跟随 `main` 跨越重启。监听器随当前所有者结束，否则随插件结束。
- 对同一个 token 的每次调用，`ctx.main` 都返回同一个客户端。

用 `client.state()` 读取本窗口的 `state`。在第一个快照到达之前它为 `undefined`，并在 `main` 每次调用 `changed` 时更新。

```tsx
const count = () => ctx.main(Counter).state()?.count ?? 0
```

#### 参考

```ts
type IpcClient<S extends IpcSpec> = {
  [Name in keyof S["methods"]]: S["methods"][Name] extends { input: Schema }
    ? (input: Input<Name>, options?: { signal?: AbortSignal }) => Promise<Output<Name>>
    : (options?: { signal?: AbortSignal }) => Promise<Output<Name>>
} & {
  state(): State | undefined
  on(name: keyof S["events"], listener: (data: EventData) => void): Cleanup
}
```

在 `src/gui.tsx` 中用两个 setup 定义插件：`Plugin.define({ ...definition, setup, main })`。

### 其他插件

另一个插件用 `ctx.use(Counter)` 跟随你的 `Ipc`，就像跟随一个契约。当它是 `active` 时，其值就是同一个 `IpcClient`。

```ts
const counter = ctx.use(Counter)

const count = () => {
  const live = counter()

  return live.status === "active" ? (live.value.state()?.count ?? 0) : 0
}
```

- 每个 `Ipc` 在 web 上都是 `inactive` 的，因为那里没有主进程。

## 原生应用菜单

`main` 用来自 `@opencode/plugin/gui/main` 的 `MenubarItem` 向原生菜单（macOS 的应用菜单、File、Edit、View、Go、Window 和 Help）以及 Windows 和 Linux 上的应用内菜单添加条目：

```ts
import { MenubarItem } from "@opencode/plugin/gui/main"

ctx.add(
  MenubarItem,
  (): MenubarItem => ({
    menu: "help",
    id: "diagnostics",
    after: "logs.export",
    label: ctx.t("menu.diagnostics"),
    enabled: () => true,
    run: (focusedWindow) => {
      focusedWindow?.webContents.focus()
    },
  }),
)
```

- `after` 指定它跟随的条目：本插件的某个条目（按其 id），或内置条目（按其命令，否则按其操作，否则按其角色），例如 `logs.export`、`edit.copy` 或 `about`。没有匹配时，该条目放在菜单末尾。
- `app` 条目只出现在 macOS 上。
- `run` 收到聚焦的窗口（若有）。
- 主进程在每次构建菜单时读取该函数，因此标签跟随语言。

#### 参考

```ts
interface MenubarItem {
  menu: "app" | "file" | "edit" | "view" | "go" | "window" | "help"
  id: string
  label: string
  after?: string
  enabled?(): boolean
  run(window: BrowserWindow | undefined): void
}
```

## 内嵌 Web 视图

要把一个隔离的 `WebContentsView` 嵌入面板，在 `main` 中创建它，并从窗口渲染它的盒子。

```ts title="src/gui/main.ts"
import { type BrowserWindow, WebContentsView } from "electron"
import type { Plugin } from "@opencode/plugin/gui"

export const main: Plugin.MainSetup = (ctx) => {
  const attach = (window: BrowserWindow) => {
    const view = new WebContentsView()
    const embed = ctx.embeds.create(view, window)
    void view.webContents.loadURL("https://acme.example")
    embed.show(true)
    // Send embed.id to the window over your Ipc.
  }
  ctx.windows.list().forEach(attach)
  ctx.windows.on("open", attach)
}
```

```tsx title="src/gui/pane.tsx"
<ctx.embeds.View id={embedId} visible radius={8} />
```

- `"open"` 只对之后才打开的窗口触发，因此先附加到 `ctx.windows.list()`。
- 窗口把嵌入的 `id` 传给 `ctx.embeds.View` 和 `ctx.embeds.capture`。
- `show(visible)` 是页面一侧的可见性：只有当窗口为它排布布局且 `show(true)` 保持时，视图才显示。
- `on("visible", handler)` 在视图进入或离开屏幕时运行，包括窗口在其位置绘制静止图像时。
- `capture()` 返回页面的静止图像，隐藏期间为 `undefined`。
- `dispose()` 把视图从窗口移除，但不关闭它的页面；用完时调用 `view.webContents.close()`。宿主也会在插件消失时释放嵌入。
- 在窗口中，`View` 用嵌入填满它的盒子。宿主让视图的边界、缩放、圆角和对话框遮挡保持同步，并在窗口隐藏或对话框打开时隐藏它。
- `frozen` 在活动视图的位置绘制一张静止图像，这样 DOM 内容可以浮在其上。`radius` 让底部圆角化，`background` 是圆角显示的颜色。
- `page` 是嵌入显示的内容，例如其 URL。面板移动期间，宿主会在其位置绘制嵌入的静止图像，并丢弃 `page` 值不同期间拍摄的静止图像。
- 窗口的 `capture(id)` 返回一张 JPEG 静止图像；嵌入隐藏时为 `undefined`，且在 web 上始终如此。

#### 参考

```ts
interface MainEmbeds {
  create(view: WebContentsView, window: BrowserWindow): Embed
}

interface Embed {
  id: string
  show(visible: boolean): void
  on(event: "visible", handler: (visible: boolean) => void): Cleanup
  capture(): Promise<NativeImage | undefined>
  dispose(): void
}

interface Embeds {
  View(props: EmbedProps): JSX.Element
  capture(id: string): Promise<Uint8Array | undefined>
}

interface EmbedProps {
  id: string | undefined
  visible: boolean
  frozen?: boolean
  page?: string
  radius?: number
  background?: string
  class?: string
  children?: JSX.Element
}
```

## Live 依赖与失败处理

`ctx.use(token)` 返回一个响应式 `Live<T>` 的访问器：即提供该 token 的插件的状态。你的插件会在那个提供者离线期间继续运行，因此要处理好非 `active` 的状态。任何控件都不应失效，任何加载指示都不应永远转下去。

```ts
import { Browser } from "@opencode/plugin/gui/browser"

const browser = ctx.use(Browser)

ctx.add(Command, () => {
  const live = browser()
  const session = ctx.sessions.current()

  return {
    id: "preview",
    title: ctx.t("command.preview"),
    enabled: live.status === "active" && !!session,
    run: () => {
      if (live.status === "active" && session) live.value.open(session, "http://localhost:3000")
    },
  }
})
```

- **`pending`：** 提供者尚未启动，例如其插件正在加载或重启。显示加载状态，或隐藏可选控件。
- **`active`：** 提供者在运行，`value` 是它的契约或 `Ipc` 客户端。`generation` 计数激活次数，重启的提供者会带着新的一代回来。
- **`inactive`, `disabled`：** 提供者被关闭、缺失，或在该平台不可用，就像每个 `Ipc` 在 web 上那样。显示不可用状态，或省略该控件。
- **`inactive`, `failed`：** 提供者的 setup 抛错了。显示不可用状态。
- 你自己的 `main` 没有 `Live` 状态。通过 [`ctx.main`](#在窗口中使用-ipc) 发起的调用会在它启动期间等待，在它无法应答时 reject。

#### 参考

```ts
type Live<T> =
  | { status: "pending" }
  | { status: "active"; value: T; generation: number }
  | { status: "inactive"; reason: "disabled" | "failed" }
```

## 生命周期与清理

通过 `ctx` 注册的一切（`ctx.add`、`ctx.provide`、`ctx.dialogs.open`、`ctx.embeds.create` 和 `Ipc` 事件监听器）在其所属作用域结束时被撤回：

- 在组件或 `createKeyed` 回调内部，注册在该组件或 `createKeyed` 运行被释放时结束。
- 在 `setup` 的顶层，注册在插件被禁用、重新加载或移除，或其窗口关闭时结束。
- 在 `main` 中，注册在插件被禁用、重新加载或移除，或应用退出时结束。嵌入还会在其窗口关闭时结束。

对于其他资源（如定时器或 socket），从 setup 返回一个清理函数。它会在同一时刻运行。

- **窗口 `setup`** 不能是 `async` 的，因为它运行在 Solid owner 之下。返回一个清理函数，或使用 `onCleanup` 或 `ctx.signal`。
- **`main`** 可以是 `async` 的。返回（或解析为）一个清理函数，或用 `ctx.onCleanup(fn)` 注册。

### 窗口 setup

窗口 `setup` 必须是同步的。把异步工作放进 `createKeyed` 或 `createLatest` 中启动。

```tsx title="src/gui.tsx"
import { Command, createKeyed, Plugin } from "@opencode/plugin/gui"
import { Changes } from "@opencode/plugin/gui/review"

export default Plugin.define({
  i18n: { en: { changes: "Show changes" } },
  setup(ctx) {
    // Runs once per active generation of Changes; the command is withdrawn with it.
    createKeyed(ctx.use(Changes), (changes) => {
      ctx.add(Command, () => ({
        id: "changes",
        title: ctx.t("changes"),
        run: () => {
          const session = ctx.sessions.current()

          if (session) changes.open(session)
        },
      }))
    })

    const timer = setInterval(() => console.log("still here"), 60_000)

    return () => clearInterval(timer)
  },
})
```

### main setup

`main` 可以是 `async` 的。为它打开的资源返回（或解析为）一个清理函数，或用 `ctx.onCleanup(fn)` 注册它。

```ts
async main(ctx) {
  const socket = await connect(ctx.options)

  ctx.onCleanup(() => socket.close())
}
```

- `ctx.onCleanup` 在插件被禁用、重新加载或移除，或应用退出时运行它的函数，后注册的先运行。插件已经消失时，它会立即运行该函数。
- `await` 之后，如果 `ctx.signal` 已中止，在注册或更改任何东西之前先 return。
- `async` 的清理会把退出延迟到它结束为止，最多 3 秒。
