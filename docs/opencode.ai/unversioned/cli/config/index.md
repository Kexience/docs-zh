---
source_url: https://opencode.ai/docs/cli/config/
source_hash: sha256:ee88e96eeb554c139efcf6aa3af589e6fa6706046d409dbe694e62c8370486ef
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# 设置

CLI 设置只控制终端客户端。它与 `opencode.json(c)` 中的服务器设置和项目设置是相互独立的。

在 TUI 中按 `Ctrl+P`，然后选择 **Open settings** 即可修改常用设置。

<img src={`${import.meta.env.BASE_URL}assets/cli/settings.png`} alt="OpenCode TUI settings dialog" />

## 配置文件

OpenCode 将 CLI 设置保存在一个全局文件中：

```text
~/.config/opencode/cli.json
```

当设置了 `$XDG_CONFIG_HOME` 时，OpenCode 使用：

```text
$XDG_CONFIG_HOME/opencode/cli.json
```

CLI 设置没有项目级配置文件。添加官方发布的 JSON Schema 以获得校验和自动补全：

```json title="cli.json"
{
  "$schema": "https://opencode.ai/v2/cli.json"
}
```

OpenCode 在创建或迁移该文件时会自动加上 `$schema`。TUI 运行期间，合法的编辑会即时生效并重新加载。

未知的设置会被忽略。请保留 `$schema`，这样编辑器才能标出无效的值。

## 内联配置

设置 `OPENCODE_CLI_CONFIG_CONTENT` 可以通过内联 JSON 应用 CLI 设置：

```sh
OPENCODE_CLI_CONFIG_CONTENT='{"tabs":{"mode":"off"}}' opencode
```

OpenCode 会将内联设置合并到全局 `cli.json` 之上。嵌套对象会进行合并，而来自环境变量的数组和标量值会直接覆盖全局值。只要该变量存在，内联设置就始终保持最高优先级。

## 外观

选择主题、控制界面动效，并覆盖终端光标：

```json title="cli.json"
{
  "theme": {
    "name": "tokyonight",
    "mode": "system"
  },
  "animations": true,
  "cursor": {
    "style": "block",
    "blinking": true
  }
}
```

<div class="docs-table-scroll" role="region" aria-label="Appearance settings" tabIndex={0}>

| 设置              | 取值                                    | 说明                                                                     |
| ----------------- | --------------------------------------- | ------------------------------------------------------------------------ |
| `theme.name`      | 字符串                                  | 选择内置主题、自定义主题或由终端派生的主题。                             |
| `theme.mode`      | `system`、`dark` 或 `light`             | 跟随终端外观，或将主题锁定为单一配色模式。                               |
| `animations`      | 布尔值                                  | 启用界面动画。                                                           |
| `cursor.style`    | `block`、`underline`、`line`、`default` | 设置光标形状。`default` 会保留终端原本的光标形状。                       |
| `cursor.blinking` | 布尔值                                  | 控制光标闪烁。当样式为 `default` 时无效。                                |

</div>

关于主题的选择与创建，请参阅[主题](../theme/index.md)。

## 输入

配置鼠标捕获、滚动、编辑器上下文、粘贴以及提示词图片预览：

```json title="cli.json"
{
  "mouse": true,
  "scroll": {
    "speed": 3,
    "acceleration": false
  },
  "prompt": {
    "editor": true,
    "paste": "compact",
    "image_preview": false
  }
}
```

<div class="docs-table-scroll" role="region" aria-label="Input settings" tabIndex={0}>

| 设置                       | 取值                            | 说明                                                                        |
| -------------------------- | ------------------------------- | --------------------------------------------------------------------------- |
| `mouse`                    | 布尔值                          | 启用终端鼠标捕获。                                                          |
| `scroll.speed`             | 数字，至少为 `0.001`            | 设置每次滚动输入的固定滚动距离。                                            |
| `scroll.acceleration`      | 布尔值                          | 加速连续滚动。启用后优先于速度设置。                                        |
| `prompt.editor`            | 布尔值                          | 将当前编辑器中的文件或选区作为提示词上下文。                                |
| `prompt.paste`             | `compact` 或 `full`             | 大段粘贴内容显示为紧凑占位符或完整文本。                                    |
| `prompt.image_preview`     | 布尔值                          | 在提示词输入框上方显示图片附件预览。                                        |

</div>

## 会话

配置全屏 TUI 会话的呈现方式以及新会话的起始位置：

```json title="cli.json"
{
  "session": {
    "sidebar": "auto",
    "scrollbar": false,
    "submit_scroll": "bottom",
    "thinking": "hide",
    "grouping": "auto",
    "image_preview": false,
    "tps": true,
    "markdown": "rendered",
    "new_location": "launch",
    "permissions": "prompt"
  }
}
```

<div class="docs-table-scroll" role="region" aria-label="Session settings" tabIndex={0}>

| 设置                    | 取值                        | 说明                                                                         |
| ----------------------- | --------------------------- | ---------------------------------------------------------------------------- |
| `session.sidebar`       | `auto` 或 `hide`            | 空间允许时显示侧栏，或始终隐藏。                                             |
| `session.scrollbar`     | 布尔值                      | 显示会话记录滚动条。                                                         |
| `session.submit_scroll` | `bottom` 或 `keep`          | 发送提示词时跳转到最新消息，或保持当前位置。                                 |
| `session.thinking`      | `show` 或 `hide`            | 默认显示或隐藏模型推理过程。                                                 |
| `session.grouping`      | `auto` 或 `none`            | 将相关的会话记录条目分组显示，或逐条独立渲染。                               |
| `session.image_preview` | 布尔值                      | 在会话记录中显示用户附件和工具结果图片。                                     |
| `session.tps`           | 布尔值                      | 在助手消息页脚显示每秒输出 token 数。                                        |
| `session.markdown`      | `source` 或 `rendered`      | 显示 Markdown 语法标记，或在渲染后的内容中隐藏它们。                         |
| `session.new_location`  | `launch` 或 `inherit`       | 从 TUI 启动目录开始，或继承当前活动会话的位置。                              |
| `session.permissions`   | `prompt` 或 `autoaccept`    | 权限请求时进行提示，或自动接受所有请求。                                     |

</div>

## 标签页

配置持久化的会话标签条：

```json title="cli.json"
{
  "tabs": {
    "mode": "auto",
    "scope": "cwd",
    "layout": "horizontal",
    "indicators": "status"
  }
}
```

旧版的布尔值设置 `tabs.enabled` 仍然受支持：`true` 等价于 `on`，`false` 等价于 `off`。OpenCode 读取它时不会重写配置文件。

<div class="docs-table-scroll" role="region" aria-label="Tab settings" tabIndex={0}>

| 设置              | 取值                        | 说明                                                                          |
| ----------------- | --------------------------- | ----------------------------------------------------------------------------- |
| `tabs.mode`       | `auto`、`on` 或 `off`       | 自动、始终或从不使用标签页。Auto 模式在 Herdr 内会自动隐藏标签页。            |
| `tabs.scope`      | `cwd` 或 `global`           | 按工作目录维护独立的标签页，或全局共享。                                      |
| `tabs.layout`     | `horizontal` 或 `vertical`  | 将标签页排列为水平标签条，或垂直侧栏。                                        |
| `tabs.indicators` | `status` 或 `numbers`       | 显示状态图标，或始终显示标签页编号。                                          |

</div>

数字编号模式下仍会保留状态颜色和背景动画。无论哪种指示模式，都可以使用 Ctrl+数字 快捷键切换标签页。

## 差异对比

配置 diff 的初始范围和呈现方式：

```json title="cli.json"
{
  "diffs": {
    "source": "branch",
    "wrap": "word",
    "tree": true,
    "single": false,
    "view": "auto"
  }
}
```

<div class="docs-table-scroll" role="region" aria-label="Diff settings" tabIndex={0}>

| 设置           | 取值                                        | 说明                                                      |
| -------------- | ------------------------------------------- | --------------------------------------------------------- |
| `diffs.source` | `branch`、`committed`、`working` 或 `turn`  | 设置初始审查范围。                                        |
| `diffs.wrap`   | `word` 或 `none`                            | 按单词折行显示长行，或不折行。                            |
| `diffs.tree`   | 布尔值                                      | 显示 diff 文件树。                                        |
| `diffs.single` | 布尔值                                      | 仅显示当前选中文件的补丁。                                |
| `diffs.view`   | `auto`、`split` 或 `unified`                | 设置布局。`auto` 会根据可用宽度自动选择。                 |

</div>

`branch` 显示**全部（All）**分支和本地更改，`committed` 仅显示分支提交，`working` 显示已暂存、未暂存和未跟踪的更改。`turn` 显示**最近一轮（Last turn）**，即会话在最近一轮工作中修改的文件；它会在会话完成一轮工作时刷新，并且当 `/diff` 不是从某个会话中打开时回退到 `branch`。

在 `/diff` 中，按 `d` 可以更改范围，或在 **Base** 中选择用于比较的分支。这些视图内的选择只在本次 TUI 退出前有效，不会修改 `cli.json`。

## 提醒

独立启用系统通知和提示音：

```json title="cli.json"
{
  "attention": {
    "notifications": true,
    "sound": true,
    "volume": 0.4,
    "sound_pack": "opencode.default",
    "sounds": {
      "permission": "/home/me/sounds/permission.wav"
    }
  }
}
```

<div class="docs-table-scroll" role="region" aria-label="Alert settings" tabIndex={0}>

| 设置                      | 取值                   | 说明                                                                                                     |
| ------------------------- | ---------------------- | -------------------------------------------------------------------------------------------------------- |
| `attention.notifications` | 布尔值                 | 显示系统通知，通常在终端未获得焦点时触发。                                                               |
| `attention.sound`         | 布尔值                 | 播放提示音。                                                                                             |
| `attention.volume`        | `0` 到 `1` 之间的数字  | 设置音量。                                                                                               |
| `attention.sound_pack`    | 字符串                 | 选择要启用的音效包 ID。                                                                                  |
| `attention.sounds`        | 对象                   | 覆盖 `default`、`question`、`permission`、`error`、`done` 或 `subagent_done` 的音效文件。                 |

</div>

无效或无法读取的覆盖文件会回退到该事件的内置音效。

更新之后，TUI 会在主屏幕上一次性展示新版本的更新亮点。运行 `/highlights` 可以再次查看，或关闭该对话框：

```json title="cli.json"
{
  "highlights": false
}
```

## 终端

配置终端集成：

```json title="cli.json"
{
  "terminal": {
    "title": true,
    "copy": "select"
  }
}
```

<div class="docs-table-scroll" role="region" aria-label="Terminal settings" tabIndex={0}>

| 设置             | 取值                 | 说明                                                                                                     |
| ---------------- | -------------------- | -------------------------------------------------------------------------------------------------------- |
| `terminal.title` | 布尔值               | 更新终端窗口标题。                                                                                       |
| `terminal.copy`  | `manual` 或 `select` | 手动复制，或选中后立即复制。平台默认值在 Windows 上为 `manual`，其他平台为 `select`。                    |

</div>

## Mini

`mini` 配置组控制 [`opencode mini`](../index.md#mini)——一个极简的交互界面：

```json title="cli.json"
{
  "mini": {
    "thinking": "show",
    "tools": "hide",
    "shell_output": "hide",
    "turn_summary": "show",
    "footer": "show",
    "splash": "show",
    "work_spinner": "block-soft-slide",
    "mono": false,
    "replay": true,
    "replay_limit": 200
  }
}
```

<div class="docs-table-scroll" role="region" aria-label="Mini settings" tabIndex={0}>

| 设置                | 取值                           | 说明                                                                               |
| ------------------- | ------------------------------ | ---------------------------------------------------------------------------------- |
| `mini.thinking`     | `show` 或 `hide`               | 显示或隐藏模型推理过程。                                                           |
| `mini.tools`        | `show` 或 `hide`               | 显示或隐藏工具调用及其之前的助手文本。                                             |
| `mini.shell_output` | `show` 或 `hide`               | 显示或隐藏 shell 工具的原始输出。                                                  |
| `mini.turn_summary` | `show` 或 `hide`               | 在回滚缓冲区中显示或隐藏 agent、模型和耗时的摘要。                                 |
| `mini.footer`       | `show` 或 `hide`               | 显示或隐藏持久化的活动状态、模型、用量和上下文信息。                               |
| `mini.splash`       | `show` 或 `hide`               | 显示或隐藏进入和退出的启动横幅。                                                   |
| `mini.work_spinner` | spinner ID                     | 选择页脚中的工作动画。                                                             |
| `mini.mono`         | 布尔值                         | 使用单色 ASCII 输出。                                                              |
| `mini.replay`       | 布尔值                         | 在恢复会话和终端尺寸变化时还原会话历史。                                           |
| `mini.replay_limit` | 正整数                         | 限制重放只显示最新的消息。默认上限为 `200`。                                       |

</div>

可用的 spinner ID 有：

```text
block-soft-slide  block-soft-sweep  block-low-comet  block-low-duet
block-shuttle     block-bridge      block-squeeze    small-toggle
square-toggle     grow-shrink       quadrant-orbit   crosshatch
density-wave      seed
```

命令行中 `mini` 的重放参数仅在该次调用中优先于这些设置。

## 按键绑定

覆盖某个命令的绑定以及前导键超时时间：

```json title="cli.json"
{
  "keybinds": {
    "leader": "ctrl+x",
    "app.exit": ["ctrl+c", "ctrl+d", "<leader>q"],
    "prompt.paste": {
      "key": "ctrl+v",
      "event": "press",
      "preventDefault": false,
      "fallthrough": false
    },
    "help.show": false
  },
  "leader": {
    "timeout": 2000
  }
}
```

<div class="docs-table-scroll" role="region" aria-label="Keybind settings" tabIndex={0}>

| 设置                        | 取值                                             | 说明                                                                 |
| --------------------------- | ------------------------------------------------ | -------------------------------------------------------------------- |
| `keybinds.leader`           | 绑定值                                           | 设置其他绑定中 `<leader>` 所引用的按键。                             |
| `keybinds.<command>`        | 绑定值                                           | 覆盖某个命令 ID 的绑定。                                             |
| `keybinds.*.key`            | 按键字符串或描述符                               | 为对象形式的绑定选择按键。                                           |
| `keybinds.*.event`          | `press` 或 `release`                             | 将对象形式的绑定限制为单一按键事件。                                 |
| `keybinds.*.preventDefault` | 布尔值                                           | 控制是否阻止终端对该按键的默认行为。                                 |
| `keybinds.*.fallthrough`    | 布尔值                                           | 允许优先级更低的事件处理器接收同一事件。                             |
| `leader.timeout`            | 正整数                                           | 设置按下前导键后等待的毫秒数。                                       |

</div>

绑定值可以是字符串、备选项数组或对象。使用 `"none"` 或 `false` 可以禁用某个绑定。
关于按键语法、所有命令 ID 以及每个默认绑定，请参阅[按键绑定](../keybinds/index.md)。

## 插件

按顺序加载仅限终端使用的插件：

```json title="cli.json"
{
  "plugins": [
    "-opencode.notifications",
    {
      "package": "./plugins/status",
      "options": {
        "compact": true
      }
    }
  ]
}
```

<div class="docs-table-scroll" role="region" aria-label="Plugin settings" tabIndex={0}>

| 设置                 | 取值            | 说明                                                            |
| -------------------- | --------------- | --------------------------------------------------------------- |
| `plugins`            | 数组            | 声明按顺序排列的启用指令和外部插件。                            |
| `plugins[].package`  | 字符串          | 设置包名、本地路径或 file URL。                                 |
| `plugins[].options`  | 对象            | 将插件专属的选项传递给该插件。                                  |

</div>

关于包的写法、本地发现、通配符和禁用指令，请参阅[插件](../plugins/index.md)。

## 调试与实验性功能

启用诊断，或加入当前可用的实验特性：

```json title="cli.json"
{
  "debug": {
    "devtools": false,
    "timing": false,
    "turn_tokens": "verbose"
  },
  "experimental": {}
}
```

<div class="docs-table-scroll" role="region" aria-label="Debug and experimental settings" tabIndex={0}>

| 设置                | 取值                            | 说明                                                                                |
| ------------------- | ------------------------------- | ----------------------------------------------------------------------------------- |
| `debug.devtools`    | 布尔值                          | 显示 DevTools 调试栏。                                                              |
| `debug.timing`      | 布尔值                          | 在调试栏中显示首次绘制耗时诊断。                                                    |
| `debug.turn_tokens` | 布尔值或 `verbose`              | 显示每轮的 token 用量；`verbose` 还会包含工具调用的输入。                            |
| `experimental`      | 特性 ID 到布尔值的对象          | 启用或禁用可能随时变更或被移除的实验特性，恕不另行通知。                             |

</div>

请只使用 TUI 的 **Experiments** 对话框中当前列出的特性 ID。未知 ID 不会产生任何效果。
