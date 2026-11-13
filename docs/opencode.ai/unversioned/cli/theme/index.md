---
source_url: https://opencode.ai/docs/cli/theme/
source_hash: sha256:8c5b1b0b057d0e72af2b7b823bd5571d895f26ec1ef0e4171f3f2d979572c540
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# 主题

OpenCode 自带许多适用于亮色和暗色模式的内置主题。你可以在设置中选择一个，也可以混搭出属于自己的颜色。

## 选择主题

按 `Ctrl+P`，选择 **Open settings**，然后打开 **Theme**。默认主题是 `opencode`。

你也可以在全局 [CLI 设置](../config/index.md)中设置主题和模式：

```json title="~/.config/opencode/cli.json"
{
  "$schema": "https://opencode.ai/v2/cli.json",
  "theme": {
    "name": "tokyonight",
    "mode": "dark"
  }
}
```

运行 `/themes` 可以在不打开设置的情况下切换主题。

## 系统颜色

当 OpenCode 能够读取你的终端调色板时，主题选择器会包含 `system` 主题。它从终端的前景色、背景色和 ANSI 调色板推导颜色。

主题名 `system` 表示使用从终端推导的颜色。模式 `system` 表示跟随终端的亮色或暗色外观。

## 模式

使用 `system` 跟随终端外观，或把主题锁定为亮色或暗色模式：

| 模式 | 行为 |
| --- | --- |
| `system` | 跟随终端检测到的亮色或暗色外观。 |
| `dark` | 始终使用主题的暗色配色。 |
| `light` | 始终使用主题的亮色配色。 |

它对应 CLI 配置中 `theme` 里的 `mode` 字段。如果自定义主题只提供一种模式，那么在请求另一种模式时 OpenCode 会使用它仅有的那种模式。

## 添加主题

要添加你下载或从他人那里得到的主题，把它的 JSON 文件复制到全局主题目录：

```bash
cp theme.json ~/.config/opencode/themes/
```

也可以把主题放进某个项目的 `.opencode/themes` 目录，让它只在该项目中可用。

文件名会成为主题名。例如 `my-theme.json` 会显示为 `my-theme`。添加文件后重启 OpenCode，然后运行 `/themes` 选中它。

OpenCode 只读取 `.json` 文件。更靠近当前目录的主题会替换全局或父级目录中的同名主题。

## 在插件中使用主题

[TUI 插件](../../build/plugins/cli/index.md)通过 `context.theme` 读取解析后的颜色，通过 `context.themeMode` 读取活动模式。使用语义 token，你的插件就能跟随所选主题：

```tsx title="Inside a TUI plugin component"
import { usePlugin } from "@opencode/plugin/tui"

function Status() {
  const context = usePlugin()
  return <text fg={context.theme.text.base}>Ready</text>
}
```

公开的 TUI 插件 API 不能注册主题。自定义主题请用 JSON 文件放在上述目录中。

## 创建主题

使用我们的[主题工具](https://opencode.ai/theme/)来创建或编辑主题。这个工具让你更容易理解结构、修改它并定义自定义颜色。下面的说明仅供参考。

主题把共享的语义 token 与按模式区分的调色板分开：

| 部分 | 用途 |
| --- | --- |
| `base` | 所有模式共享的完整 token 树。 |
| `light`、`dark` | 该模式的完整色相调色板，以及可选的 token 覆盖。 |

每个主题都要提供完整的 `base`，并且至少定义 `light` 或 `dark` 之一。各模式从文件的 `base` 继承；它们不从内置的 OpenCode 主题继承，也不互相继承。

下面的示例只展示与每个概念相关的部分。在自定义之前，先用主题编辑器生成一个完整的文件。

### 结构

把两种模式都用到的颜色放进 `base`，需要时再在 `light` 或 `dark` 中覆盖：

```json title="theme.json (excerpt)"
{
  "$schema": "https://opencode.ai/theme.json",
  "base": {
    "text": {
      "base": "$hue.neutral.200",
      "muted": "$hue.neutral.400"
    }
  },
  "light": {
    "hue": {}
  },
  "dark": {
    "hue": {},
    "text": {
      "muted": "$hue.neutral.300"
    }
  }
}
```

完整的 `base` 提供每一个语义 token。每种模式提供全部必需的色相，并可以覆盖 base token 树的任意部分。

### 颜色与引用

颜色可以是十六进制值、`"transparent"`，或对另一个主题颜色的引用：

```json title="Inside base or a mode"
{
  "text": {
    "base": "#eeeeee",
    "muted": "$hue.neutral.400"
  },
  "border": {
    "base": "$text.muted"
  }
}
```

### 色相

色相是九级色阶。每种模式都要定义八个基础色相和三个别名：

| 类别 | 取值 |
| --- | --- |
| 基础 | `gray`、`red`、`orange`、`yellow`、`green`、`cyan`、`blue`、`purple` |
| 别名 | `accent`、`interactive`、`neutral` |
| 层级 | `100`、`200`、`300`、`400`、`500`、`600`、`700`、`800`、`900` |

为基础色相定义全部九个层级，或者把一个色相别名到另一个色相：

```json title="Inside light or dark"
{
  "hue": {
    "purple": {
      "100": "#b38ff4",
      "200": "#9d7cd8",
      "300": "#8869bd",
      "400": "#7357a2",
      "500": "#5f4688",
      "600": "#4b356f",
      "700": "#392557",
      "800": "#271640",
      "900": "#17072b"
    },
    "accent": "$hue.purple"
  }
}
```

色相层级遵循该模式的对比方向。亮色主题从 `100` 的深色到 `900` 的浅色；暗色主题从 `100` 的浅色到 `900` 的深色。

`base` 中的 `categorical` 数组设置用于区分 agent 及其他重复条目的有序色相：

```json title="Inside base"
{
  "categorical": ["accent", "purple", "green", "blue"]
}
```

### 语义 token

语义 token 为 UI 角色分配颜色。组件使用这些角色，而不是直接挑选颜色。

| 分组 | 用途 |
| --- | --- |
| `text` | 基础、弱化、极弱、操作、表单字段和反馈文本。`faint` 默认为 `muted`。 |
| `background` | 基础、抬升表面、操作、表单字段和反馈填充。 |
| `border`、`scrollbar` | 边框和滚动条颜色。 |
| `diff` | 新增、删除、上下文、高亮和行号颜色。 |
| `syntax` | 源代码高亮。 |
| `markdown` | Markdown 元素。 |

例如，`text.muted` 控制次要文本，而 `background.raised` 定义逐级抬升的表面：

```json title="Inside base"
{
  "text": {
    "base": "$hue.neutral.200",
    "muted": "$hue.neutral.400"
  },
  "background": {
    "base": "$hue.neutral.800",
    "raised": {
      "base": "$hue.neutral.700",
      "high": "$hue.neutral.600",
      "max": "$hue.neutral.500"
    }
  }
}
```

语法键为 `comment`、`keyword`、`function`、`variable`、`string`、`number`、`type`、`operator` 和 `punctuation`。

Markdown 键为 `text`、`heading`、`link`、`linkText`、`code`、`blockQuote`、`emphasis`、`strong`、`horizontalRule`、`listItem`、`listEnumeration`、`image`、`imageText` 和 `codeBlock`。

### 操作与状态

操作有 `primary`、`secondary` 和 `destructive` 三种变体。操作和表单字段使用 `base` 加上可选的交互状态：

```json title="Inside base or a mode"
{
  "text": {
    "action": {
      "primary": {
        "base": "$hue.interactive.400",
        "$hovered": "$hue.interactive.300",
        "$disabled": "$hue.neutral.600"
      }
    }
  }
}
```

状态键为 `$hovered`、`$focused`、`$pressed`、`$selected` 和 `$disabled`。未指定的状态使用该操作或表单字段的 `base` 颜色。

### 对话框表面

面板、对话框、菜单和 toast 从 `background.raised` 中选择自己的深度。对话框还可以用 `@dialog` 额外覆盖语义 token：

```json title="Inside base or a mode"
{
  "@dialog": {
    "background": {
      "base": "$background.raised.base",
      "action": {
        "primary": {
          "$hovered": "$background.raised.high"
        }
      }
    }
  }
}
```

TUI 在应用 `@dialog` 之后会再次解析引用，因此引用 `$background.base` 的 token 会跟随对话框背景。上下文操作的 `base` 会成为其未指定状态的回退值；显式的状态覆盖仍然优先。
