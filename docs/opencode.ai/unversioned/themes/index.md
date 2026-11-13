---
source_url: https://opencode.ai/docs/themes/
source_hash: sha256:ef25937b992c7483b0c412aff76ad8654bd6a3521e0ed2c44f59106f414b92e7
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---
# 主题

在终端界面按 `Ctrl+P`，选择 **Open settings**，再打开 **Theme**，即可选择主题。你也可以直接在全局 CLI 配置中设置：

```json title="~/.config/opencode/cli.json"
{
  "theme": {
    "name": "tokyonight",
    "mode": "system"
  }
}
```

主题属于终端客户端。请把主题选择写在 `cli.json` 中，而不是 `opencode.json`。配置文件位置和其他终端设置请参阅 [CLI 设置](../cli/config/index.md)。

## 模式

使用 `system` 跟随终端的外观，或将主题锁定为某一种模式：

```json title="~/.config/opencode/cli.json"
{
  "theme": {
    "name": "opencode",
    "mode": "dark"
  }
}
```

| 值 | 行为 |
| -------- | --------------------------------------------- |
| `system` | 跟随终端的浅色或深色模式。 |
| `dark` | 始终使用深色主题。 |
| `light` | 始终使用浅色主题。 |

如果自定义主题只提供了一种模式，当请求的是另一种模式时，OpenCode 会使用它提供的那种模式。

## 内置主题

按名称选择内置主题：

```json title="~/.config/opencode/cli.json"
{
  "theme": {
    "name": "catppuccin"
  }
}
```

可用主题包括：

- `aura`、`ayu`、`carbonfox`、`cobalt2`、`cursor`、`dracula`、`everforest`、`flexoki`
- `catppuccin`、`catppuccin-frappe`、`catppuccin-macchiato`
- `github`、`gruvbox`、`kanagawa`、`material`、`matrix`、`mercury`、`monokai`、`nightowl`、`nord`
- `one-dark`、`opencode`、`orng`、`lucent-orng`、`osaka-jade`、`palenight`、`rosepine`
- `solarized`、`synthwave84`、`tokyonight`、`vercel`、`vesper`、`zenburn`

当 OpenCode 能够读取你的终端调色板时，可以使用 `system` 主题。

## 文件

要创建一个名为 `ocean` 的全局主题，可以用主题工具在全局主题目录中生成一个完整的文件。它的关键结构如下所示：

```json title="~/.config/opencode/themes/ocean.json (excerpt)"
{
  "base": {
    "text": {
      "base": "#d8f3ff"
    }
  },
  "dark": {
    "hue": {
      "accent": "$hue.cyan"
    }
  }
}
```

然后在设置中选择 `ocean`，或在 `cli.json` 中把 `theme.name` 设为 `ocean`。文件名（不含 `.json` 后缀）就是主题名。

| 范围 | 目录 |
| ------- | ------------------------------------------ |
| 全局 | `~/.config/opencode/themes/` |
| 项目 | 项目目录树中的 `.opencode/themes/` |

OpenCode 只读取 `.json` 文件。离当前目录更近的主题会替换同名的全局主题或父级主题。

## 格式

每个 V2 主题都要声明一棵完整的 `base` 令牌树，以及至少一个 `light` 或 `dark` 色调（hue）调色板。各模式只从该文件的 base 继承，不会从内置的 OpenCode 主题或其他模式继承。在自定义之前，先用主题工具生成一个完整的 base。

下例只展示了与各概念相关的部分，并不是完整的主题文件。

```json title="themes/ocean.json"
{
  "base": {
    "text": {
      "base": "#16324f"
    }
  },
  "light": {
    "hue": {}
  },
  "dark": {
    "hue": {},
    "text": { "base": "#d8f3ff" }
  }
}
```

## 颜色

可以使用十六进制颜色、`transparent`，或对其他主题颜色的引用：

```json title="themes/ocean.json"
{
  "base": {
    "text": {
      "base": "#d8f3ff",
      "muted": "$hue.neutral.400"
    },
    "background": {
      "base": "transparent"
    }
  }
}
```

十六进制值可以使用 3、4、6 或 8 位。引用以 `$` 开头；色调引用的形式为 `$hue.<name>.<step>`。

## 色调

覆盖一个色调别名即可一次性更改一组相关的颜色：

```json title="themes/ocean.json"
{
  "base": {
    "categorical": ["accent", "purple", "green"]
  },
  "dark": {
    "hue": {
      "accent": "$hue.cyan",
      "interactive": "$hue.blue"
    }
  }
}
```

| 类型 | 取值 |
| ------- | -------------------------------------------------------------------- |
| 基础色 | `gray`、`red`、`orange`、`yellow`、`green`、`cyan`、`blue`、`purple` |
| 别名 | `accent`、`interactive`、`neutral` |
| 阶梯 | `100`、`200`、`300`、`400`、`500`、`600`、`700`、`800`、`900` |

色调阶梯遵循该模式的对比方向：浅色主题从 `100` 的深色到 `900` 的浅色，深色主题则从 `100` 的浅色到 `900` 的深色。

`categorical` 设置用于区分 agent 和其他重复出现项目的有序色调。它必须至少包含一个基础色调或别名。

## 状态

使用状态键来更改交互式颜色。未指定的状态会使用最近的基础值：

```json title="themes/ocean.json"
{
  "base": {
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
}
```

| 分组 | 取值 |
| --------- | --------------------------------------------------------- |
| 动作 | `primary`、`secondary`、`destructive` |
| 状态 | `$hovered`、`$focused`、`$pressed`、`$selected`、`$disabled` |

表单字段在 `text.formfield` 或 `background.formfield` 下直接使用同样的状态键。

## 令牌

完整的 `base` 包含所有令牌组。某个模式在提供完整的色调调色板之后，可以覆盖其中任意部分：

```json title="themes/ocean.json"
{
  "base": {
    "border": {
      "base": "$hue.neutral.700"
    },
    "syntax": {
      "comment": "$hue.neutral.500",
      "keyword": "$hue.accent.400"
    },
    "diff": {
      "text": {
        "added": "$hue.green.400",
        "removed": "$hue.red.400"
      }
    }
  }
}
```

| 令牌组 | 用途 |
| ------------ | ------------------------------------------------------------- |
| `text` | 基础、弱化、淡化、动作、表单字段和反馈文字 |
| `background` | 基础、表面、动作、表单字段和反馈填充 |
| `border` | 边框 |
| `scrollbar` | 滚动条 |
| `diff` | 新增、删除、上下文、高亮和行号颜色 |
| `syntax` | 源代码高亮 |
| `markdown` | Markdown 元素 |

语法键包括 `comment`、`keyword`、`function`、`variable`、`string`、`number`、`type`、`operator` 和 `punctuation`。Markdown 键包括 `text`、`heading`、`link`、`linkText`、`code`、`blockQuote`、`emphasis`、`strong`、`horizontalRule`、`listItem`、`listEnumeration`、`image`、`imageText` 和 `codeBlock`。

## 凸起表面

面板、对话框、菜单和提示条从 `background.raised` 中选择自己的层次。对话框还支持上下文相关的 `@dialog` 表面。TUI 会在应用 `@dialog` 后重新解析调色板，因此引用 `$background.base` 的令牌会跟随对话框的背景：

```json title="themes/ocean.json"
{
  "base": {
    "background": {
      "base": "#071521",
      "raised": {
        "base": "#0c1f2e",
        "high": "#102a3c",
        "max": "#16364b"
      }
    },
    "@dialog": {
      "background": {
        "base": "$background.raised.base"
      }
    }
  }
}
```

`@dialog` 接受与基础模式相同的令牌组。动作的上下文相关 `base` 也会成为其未指定状态的回退值；显式的状态覆盖仍然优先。
