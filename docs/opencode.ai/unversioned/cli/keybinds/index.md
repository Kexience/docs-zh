---
source_url: https://opencode.ai/docs/cli/keybinds/
source_hash: sha256:42fc2caa8b88bbae905e6d222c75dcfa67db1ffc0d5af6e7467f3612437f728e
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# 按键绑定

在 `cli.json` 中自定义按键绑定：

```json title="cli.json"
{
  "keybinds": {
    "leader": "ctrl+space",
    "command.palette.show": "ctrl+k",
    "app.exit": ["ctrl+c", "ctrl+d"],
    "app.debug": false
  },
  "leader": {
    "timeout": 1500
  }
}
```

单个按键用字符串表示：

```json
{
  "keybinds": {
    "command.palette.show": "ctrl+k"
  }
}
```

多个备选按键之间用逗号分隔：

```json
{
  "keybinds": {
    "app.exit": "ctrl+c,ctrl+d"
  }
}
```

使用 `"none"` 或 `false` 可禁用某个绑定：

```json
{
  "keybinds": {
    "app.debug": "none",
    "help.show": false
  }
}
```

使用对象可指定事件行为：

```json
{
  "keybinds": {
    "prompt.paste": {
      "key": "ctrl+v",
      "preventDefault": false
    }
  }
}
```

`leader` 默认为 `ctrl+x`。其他绑定中的 `<leader>` 引用的是这个前导键。

```json
{
  "keybinds": {
    "leader": "ctrl+space",
    "model.list": "<leader>m"
  },
  "leader": {
    "timeout": 2000
  }
}
```

未知的命令 ID 会被忽略。

## 应用程序

| ID                         | 默认值                    | 说明                       |
| -------------------------- | ------------------------- | -------------------------- |
| `leader`                   | `ctrl+x`                  | 按键组合的前导键           |
| `app.exit`                 | `ctrl+c,ctrl+d,<leader>q` | 退出应用程序               |
| `app.debug`                | `none`                    | 切换调试面板               |
| `app.console`              | `none`                    | 切换控制台                 |
| `app.scrap`                | `none`                    | 打开便签界面               |
| `app.toggle.animations`    | `none`                    | 切换动画                   |
| `app.toggle.file_context`  | `none`                    | 切换文件上下文             |
| `app.toggle.diffwrap`      | `none`                    | 切换 diff 自动换行         |
| `app.toggle.paste_summary` | `none`                    | 切换粘贴摘要               |
| `command.palette.show`     | `ctrl+p`                  | 列出可用命令               |
| `help.show`                | `none`                    | 打开帮助对话框             |
| `docs.open`                | `none`                    | 打开文档                   |
| `opencode.settings`        | `none`                    | 打开设置                   |
| `server.pair`              | `none`                    | 配对设备                   |
| `service.restart`          | `none`                    | 重启服务                   |
| `location.reload`          | `none`                    | 重新加载配置               |

## Mini

`app.clear` 命令仅在 [`opencode mini`](../index.md) 中可用。按 `ctrl+l` 可清除可见屏幕并重新绘制提示符，终端会保留回滚缓冲区。

```json title="cli.json"
{
  "keybinds": {
    "app.clear": "ctrl+l"
  }
}
```

| ID          | 默认值   | 说明     |
| ----------- | -------- | -------- |
| `app.clear` | `ctrl+l` | 清除屏幕 |

## Diff 查看器

按 `d`（`diff.switch_source`）选择 **All**、**Committed**、**Uncommitted** 或 **Last turn**（会话内），或选择 **Base** 更改对比分支。所选范围会一直保留，直到 TUI 退出。可通过 [`cli.json` 中的 `diffs.source`](../config/index.md#diffs) 设置初始范围。

滚动、翻页以及跳转到开头/结尾的快捷键始终作用于 diff。键盘焦点无法切换：点击文件可打开文件，点击文件夹可展开或折叠，滚动文件树则使用鼠标滚轮。

使用 `n` / `p` 或 `alt+down` / `alt+up`（macOS 上为 Option 键）在文件之间移动。在 diff 查看器内，Alt 快捷键用于切换文件，而不是切换会话标签页。

按 `m` 可将文件标记为已审阅并折叠其补丁正文。在全文件视图中，再次按 `m` 可取消标记并重新展开补丁。单文件视图在标记已审阅后会自动前进到下一个文件，但在最后一个文件处会停留而不循环。取消标记时永远不会前进。

在侧栏或文件的 diff 标题上右键，可选择 **Mark complete**（或 **Mark incomplete**）。这与 `m` 修改的是同一个已审阅状态。通过菜单完成其他文件的操作时，不会选中该文件，也不会改变当前正在查看的文件位置。

带 Shift 的 `diff.help` 备选按键是为了支持那些在按下 `?` 时会上报 Shift 修饰键的终端。

| ID                       | 默认值              | 说明                            |
| ------------------------ | ------------------- | ------------------------------- |
| `diff.open`              | `none`              | 打开 diff 查看器                |
| `diff.close`             | `escape,q`          | 关闭 diff 查看器                |
| `diff.down`              | `j,down`            | diff 查看器向下移动             |
| `diff.up`                | `k,up`              | diff 查看器向上移动             |
| `diff.page.down`         | `pagedown,ctrl+f`   | diff 查看器向下翻页             |
| `diff.page.up`           | `pageup,ctrl+b`     | diff 查看器向上翻页             |
| `diff.half_page.down`    | `ctrl+d`            | diff 查看器向下滚动半页         |
| `diff.half_page.up`      | `ctrl+u`            | diff 查看器向上滚动半页         |
| `diff.first`             | `gg,home`           | 跳转到 diff 开头                |
| `diff.last`              | `shift+g,end`       | 跳转到 diff 末尾                |
| `diff.next_hunk`         | `]`                 | 跳转到下一个 diff hunk          |
| `diff.previous_hunk`     | `[`                 | 跳转到上一个 diff hunk          |
| `diff.next_file`         | `n,alt+down`        | 跳转到下一个 diff 文件          |
| `diff.previous_file`     | `p,alt+up`          | 跳转到上一个 diff 文件          |
| `diff.toggle_file_tree`  | `b`                 | 切换 diff 查看器文件树          |
| `diff.single_patch`      | `s`                 | 切换单个补丁视图                |
| `diff.switch_source`     | `d`                 | 选择 diff 审阅范围              |
| `diff.toggle_view`       | `v`                 | 切换 diff 查看器分屏或统一视图  |
| `diff.toggle_fullscreen` | `f`                 | 切换 diff 查看器全屏            |
| `diff.mark_reviewed`     | `m`                 | 切换所选 diff 文件的已审阅状态  |
| `diff.help`              | `?,shift+?,shift+/` | 显示更多 diff 查看器快捷键      |

已废弃的 `diff.toggle`、`diff.expand`、`diff.expand_all`、`diff.collapse` 和 `diff.switch_focus` 配置项仍然被接受，但不再注册快捷键。

## 外观与导航

| ID                         | 默认值          | 说明                     |
| -------------------------- | --------------- | ------------------------ |
| `prompt.editor`            | `<leader>e`     | 打开外部编辑器           |
| `theme.switch`             | `none`          | 列出可用主题             |
| `theme.switch_mode`        | `none`          | 在浅色与深色主题模式间切换 |
| `theme.mode.lock`          | `none`          | 锁定或解锁主题模式       |
| `session.sidebar.toggle`   | `<leader>b`     | 切换侧栏                 |
| `pane.focus.left`          | `<leader>left`  | 聚焦会话面板             |
| `pane.focus.right`         | `<leader>right` | 聚焦右侧面板             |
| `terminal.select`          | `<leader>down`  | 选择终端                 |
| `terminal.toggle`          | `<leader>t`     | 切换终端面板             |
| `terminal.close`           | `<leader>up`    | 关闭终端面板             |
| `session.toggle.scrollbar` | `none`          | 切换会话滚动条           |
| `opencode.status`          | `<leader>s`     | 查看状态                 |
| `opencode.debug`           | `none`          | 查看调试信息             |

## 会话

| ID                                    | 默认值                  | 说明                               |
| ------------------------------------- | ----------------------- | ---------------------------------- |
| `session.export`                      | `<leader>x`             | 将会话导出到编辑器                 |
| `session.copy`                        | `none`                  | 复制会话记录                       |
| `session.copy.id`                     | `none`                  | 复制会话 ID                        |
| `session.move`                        | `none`                  | 移动会话                           |
| `session.new`                         | `<leader>n`             | 新建会话                           |
| `session.list`                        | `<leader>l`             | 列出所有会话                       |
| `open.menu`                           | `ctrl+o`                | 打开最近的会话和项目               |
| `session.tab.next`                    | `ctrl+tab,alt+down`     | 切换到下一个打开的会话标签页       |
| `session.tab.previous`                | `ctrl+shift+tab,alt+up` | 切换到上一个打开的会话标签页       |
| `session.tab.history.back`            | `none`                  | 在会话标签页历史中后退             |
| `session.tab.history.forward`         | `ctrl+i`                | 在会话标签页历史中前进             |
| `session.tab.next_unread`             | `alt+shift+down`        | 切换到下一个未读会话标签页         |
| `session.tab.previous_unread`         | `alt+shift+up`          | 切换到上一个未读会话标签页         |
| `session.tab.close`                   | `<leader>w`             | 关闭当前会话标签页                 |
| `session.tab.reopen`                  | `ctrl+shift+t`          | 重新打开最近关闭的会话标签页       |
| `session.timeline`                    | `<leader>g`             | 显示会话时间线                     |
| `session.fork`                        | `none`                  | 从消息分叉会话                     |
| `session.rename`                      | `ctrl+r`                | 重命名会话                         |
| `session.delete`                      | `ctrl+d`                | 删除会话                           |
| `session.interrupt`                   | `escape`                | 中断当前会话                       |
| `session.background`                  | `ctrl+b`                | 将阻塞会话的工具转入后台           |
| `session.compact`                     | `<leader>c`             | 压缩会话                           |
| `session.aside`                       | `none`                  | 提出附带问题                       |
| `session.cd`                          | `none`                  | 更改工作目录                       |
| `session.queued_prompts`              | `<leader>q`             | 管理排队中的提示                   |
| `queued_prompt.undo`                  | `ctrl+u`                | 撤销排队的提示                     |
| `queued_prompt.delete`                | `ctrl+d`                | 删除排队的提示                     |
| `session.toggle.exploration_grouping` | `none`                  | 切换相关工具调用的分组显示         |
| `session.verbosity.cycle`             | `none`                  | 循环切换记录的详细程度             |
| `session.child.first`                 | `down`                  | 切换 subagent 选择器               |
| `session.child.next`                  | `right`                 | 转到下一个子会话                   |
| `session.child.previous`              | `left`                  | 转到上一个子会话                   |
| `session.parent`                      | `up`                    | 转到父会话                         |
| `session.pin.toggle`                  | `ctrl+f`                | 在会话列表中固定或取消固定会话     |
| `session.quick_switch.1`              | `<leader>1`             | 切换到快速槽位 1 中的会话          |
| `session.quick_switch.2`              | `<leader>2`             | 切换到快速槽位 2 中的会话          |
| `session.quick_switch.3`              | `<leader>3`             | 切换到快速槽位 3 中的会话          |
| `session.quick_switch.4`              | `<leader>4`             | 切换到快速槽位 4 中的会话          |
| `session.quick_switch.5`              | `<leader>5`             | 切换到快速槽位 5 中的会话          |
| `session.quick_switch.6`              | `<leader>6`             | 切换到快速槽位 6 中的会话          |
| `session.quick_switch.7`              | `<leader>7`             | 切换到快速槽位 7 中的会话          |
| `session.quick_switch.8`              | `<leader>8`             | 切换到快速槽位 8 中的会话          |
| `session.quick_switch.9`              | `<leader>9`             | 切换到快速槽位 9 中的会话          |
| `session.tab.select.1`                | `<leader>1,ctrl+1`      | 切换到会话标签页 1                 |
| `session.tab.select.2`                | `<leader>2,ctrl+2`      | 切换到会话标签页 2                 |
| `session.tab.select.3`                | `<leader>3,ctrl+3`      | 切换到会话标签页 3                 |
| `session.tab.select.4`                | `<leader>4,ctrl+4`      | 切换到会话标签页 4                 |
| `session.tab.select.5`                | `<leader>5,ctrl+5`      | 切换到会话标签页 5                 |
| `session.tab.select.6`                | `<leader>6,ctrl+6`      | 切换到会话标签页 6                 |
| `session.tab.select.7`                | `<leader>7,ctrl+7`      | 切换到会话标签页 7                 |
| `session.tab.select.8`                | `<leader>8,ctrl+8`      | 切换到会话标签页 8                 |
| `session.tab.select.9`                | `<leader>9,ctrl+9`      | 切换到会话标签页 9                 |
| `session.tab.select.10`               | `<leader>0,ctrl+0`      | 切换到会话标签页 10                |

## 模型与 agent

| ID                             | 默认值      | 说明                        |
| ------------------------------ | ----------- | --------------------------- |
| `stash.delete`                 | `ctrl+d`    | 删除暂存条目                |
| `model.dialog.provider`        | `ctrl+a`    | 从模型对话框打开 provider 列表 |
| `model.dialog.favorite`        | `ctrl+f`    | 切换模型收藏状态            |
| `model.dialog.usage`           | `ctrl+u`    | 从模型对话框打开用量限制    |
| `model.list`                   | `<leader>m` | 列出可用模型                |
| `model.cycle_recent`           | `f2`        | 下一个最近使用的模型        |
| `model.cycle_recent_reverse`   | `shift+f2`  | 上一个最近使用的模型        |
| `model.cycle_favorite`         | `none`      | 下一个收藏的模型            |
| `model.cycle_favorite_reverse` | `none`      | 上一个收藏的模型            |
| `mcp.list`                     | `none`      | 列出 MCP 服务器             |
| `usage.show`                   | `none`      | 查看用量限制                |
| `provider.connect`             | `none`      | 连接集成                    |
| `agent.list`                   | `<leader>a` | 列出 agent                  |
| `agent.cycle`                  | `shift+tab` | 下一个 agent                |
| `agent.cycle.reverse`          | `none`      | 上一个 agent                |
| `variant.cycle`                | `ctrl+t`    | 循环切换模型变体            |
| `variant.list`                 | `none`      | 列出模型变体                |

## 会话导航

| ID                              | 默认值                 | 说明                   |
| ------------------------------- | ---------------------- | ---------------------- |
| `session.page.up`               | `pageup,ctrl+alt+b`    | 消息向上滚动一页       |
| `session.page.down`             | `pagedown,ctrl+alt+f`  | 消息向下滚动一页       |
| `session.line.up`               | `ctrl+alt+y`           | 消息向上滚动一行       |
| `session.line.down`             | `ctrl+alt+e`           | 消息向下滚动一行       |
| `session.half.page.up`          | `ctrl+alt+u`           | 消息向上滚动半页       |
| `session.half.page.down`        | `ctrl+alt+d`           | 消息向下滚动半页       |
| `session.first`                 | `ctrl+g,home,alt+home` | 跳转到第一条消息       |
| `session.last`                  | `ctrl+alt+g,end`       | 跳转到最后一条消息     |
| `session.message.next`          | `none`                 | 跳转到下一条消息       |
| `session.message.previous`      | `none`                 | 跳转到上一条消息       |
| `session.message.user.next`     | `none`                 | 跳转到下一条用户消息   |
| `session.message.user.previous` | `none`                 | 跳转到上一条用户消息   |
| `session.messages_last_user`    | `alt+end`              | 跳转到最后的用户消息   |
| `messages.copy`                 | `<leader>y`            | 复制消息               |
| `session.undo`                  | `<leader>u`            | 撤销消息               |
| `session.redo`                  | `<leader>r`            | 重做消息               |
| `session.toggle.thinking`       | `none`                 | 切换思考块的可见性     |

## 提示命令

| ID                            | 默认值           | 说明           |
| ----------------------------- | ---------------- | -------------- |
| `prompt.submit`               | `none`           | 提交提示       |
| `prompt.queue`                | `<leader>return` | 将提示加入队列 |
| `prompt.editor_context.clear` | `none`           | 清除编辑器上下文 |
| `prompt.images.view`          | `<leader>i`      | 查看图片附件   |
| `prompt.skills`               | `none`           | 打开技能选择器 |
| `prompt.stash`                | `none`           | 暂存提示       |
| `prompt.stash.pop`            | `none`           | 取出已暂存的提示 |
| `prompt.stash.list`           | `none`           | 列出已暂存的提示 |

## 输入编辑

| ID                              | 默认值                                                                        | 说明                 |
| ------------------------------- | ----------------------------------------------------------------------------- | -------------------- |
| `prompt.clear`                  | `ctrl+c`                                                                      | 清空输入框           |
| `prompt.paste`                  | `{"key":"ctrl+v","preventDefault":false}`（`ctrl+v`；`preventDefault: false`） | 从剪贴板粘贴         |
| `input.submit`                  | `return`                                                                      | 提交输入             |
| `input.newline`                 | `shift+return,ctrl+return,alt+return,ctrl+j`                                  | 在输入中插入换行     |
| `input.move.left`               | `left,ctrl+b`                                                                 | 输入中光标左移       |
| `input.move.right`              | `right,ctrl+f`                                                                | 输入中光标右移       |
| `input.move.up`                 | `up`                                                                          | 输入中光标上移       |
| `input.move.down`               | `down`                                                                        | 输入中光标下移       |
| `input.select.left`             | `shift+left`                                                                  | 输入中向左选择       |
| `input.select.right`            | `shift+right`                                                                 | 输入中向右选择       |
| `input.select.up`               | `shift+up`                                                                    | 输入中向上选择       |
| `input.select.down`             | `shift+down`                                                                  | 输入中向下选择       |
| `input.line.home`               | `ctrl+a`                                                                      | 输入中移动到行首     |
| `input.line.end`                | `ctrl+e`                                                                      | 输入中移动到行尾     |
| `input.select.line.home`        | `ctrl+shift+a`                                                                | 输入中选择到行首     |
| `input.select.line.end`         | `ctrl+shift+e`                                                                | 输入中选择到行尾     |
| `input.visual.line.home`        | `alt+a`                                                                       | 输入中移动到可视行首 |
| `input.visual.line.end`         | `alt+e`                                                                       | 输入中移动到可视行尾 |
| `input.select.visual.line.home` | `alt+shift+a`                                                                 | 输入中选择到可视行首 |
| `input.select.visual.line.end`  | `alt+shift+e`                                                                 | 输入中选择到可视行尾 |
| `input.buffer.home`             | `none`                                                                        | 输入中移动到缓冲区开头 |
| `input.buffer.end`              | `none`                                                                        | 输入中移动到缓冲区末尾 |
| `input.select.buffer.home`      | `shift+home`                                                                  | 输入中选择到缓冲区开头 |
| `input.select.buffer.end`       | `shift+end`                                                                   | 输入中选择到缓冲区末尾 |
| `input.delete.line`             | `ctrl+shift+d`                                                                | 删除输入中的整行     |
| `input.delete.to.line.end`      | `ctrl+k`                                                                      | 删除输入中光标到行尾的内容 |
| `input.delete.to.line.start`    | `ctrl+u`                                                                      | 删除输入中光标到行首的内容 |
| `input.backspace`               | `backspace,shift+backspace`                                                   | 输入中退格           |
| `input.delete`                  | `ctrl+d,delete,shift+delete`                                                  | 删除输入中的字符     |
| `input.undo`                    | `ctrl+-,super+z`                                                              | 输入中撤销           |
| `input.redo`                    | `ctrl+.,super+shift+z`                                                        | 输入中重做           |
| `input.word.forward`            | `alt+f,alt+right,ctrl+right`                                                  | 输入中光标向前移动一个词 |
| `input.word.backward`           | `alt+b,alt+left,ctrl+left`                                                    | 输入中光标向后移动一个词 |
| `input.select.word.forward`     | `alt+shift+f,alt+shift+right`                                                 | 输入中向前选择一个词 |
| `input.select.word.backward`    | `alt+shift+b,alt+shift+left`                                                  | 输入中向后选择一个词 |
| `input.delete.word.forward`     | `alt+d,alt+delete,ctrl+delete`                                                | 输入中向前删除一个词 |
| `input.delete.word.backward`    | `ctrl+w,ctrl+backspace,alt+backspace`                                         | 输入中向后删除一个词 |
| `input.select.all`              | `super+a`                                                                     | 输入中全选           |
| `prompt.history.previous`       | `up`                                                                          | 上一条历史记录       |
| `prompt.history.next`           | `down`                                                                        | 下一条历史记录       |

## 编辑器

| ID                            | 默认值   | 说明         |
| ----------------------------- | -------- | ------------ |
| `composer.subagent.up`        | `up`     | 上一个 subagent |
| `composer.subagent.down`      | `down`   | 下一个 subagent |
| `composer.subagent.select`    | `return` | 转到 subagent |
| `composer.subagent.interrupt` | `ctrl+d` | 中断 subagent |
| `composer.shell.up`           | `up`     | 上一个 shell |
| `composer.shell.down`         | `down`   | 下一个 shell |
| `composer.shell.select`       | `return` | 查看 shell 输出 |
| `composer.shell.kill`         | `ctrl+d` | 终止 shell 命令 |
| `composer.terminal.up`        | `up,k`   | 上一个终端   |
| `composer.terminal.down`      | `down,j` | 下一个终端   |
| `composer.terminal.select`    | `return` | 选择终端     |

在 **Shell** 标签页中选中正在运行的命令并按 **Enter**，或直接点击它，即可查看捕获的 stdout 和 stderr。
使用 **↑/↓**、**Page Up/Down** 或 **Home** 滚动，按 **End** 跟随新输出，按 **Esc** 返回且不停止命令。
查看器显示最近的输出，命令退出后仍保持打开；重定向到文件的输出不会包含在内。

## 对话框与自动补全

| ID                             | 默认值        | 说明                     |
| ------------------------------ | ------------- | ------------------------ |
| `dialog.select.prev`           | `up,ctrl+p`   | 移动到上一个对话框条目   |
| `dialog.select.next`           | `down,ctrl+n` | 移动到下一个对话框条目   |
| `dialog.select.page_up`        | `pageup`      | 对话框中向上翻页         |
| `dialog.select.page_down`      | `pagedown`    | 对话框中向下翻页         |
| `dialog.select.home`           | `home`        | 移动到第一个对话框条目   |
| `dialog.select.end`            | `end`         | 移动到最后一个对话框条目 |
| `dialog.select.submit`         | `return`      | 确认所选对话框条目       |
| `dialog.prompt.submit`         | `return`      | 提交对话框提示           |
| `dialog.integration.rename`    | `ctrl+r`      | 重命名集成账户           |
| `dialog.integration.delete`    | `ctrl+d`      | 删除集成账户             |
| `dialog.integration.copy`      | `tab`         | 复制授权链接             |
| `dialog.worktree.generate`     | `tab`         | 生成 worktree 名称       |
| `dialog.move_session.new`      | `ctrl+a`      | 新建 worktree            |
| `dialog.move_session.move`     | `ctrl+m`      | 将会话移动到 worktree    |
| `dialog.move_session.delete`   | `ctrl+d`      | 删除 worktree            |
| `dialog.move_session.refresh`  | `ctrl+r`      | 刷新 worktree            |
| `prompt.autocomplete.prev`     | `up,ctrl+p`   | 移动到上一个自动补全条目 |
| `prompt.autocomplete.next`     | `down,ctrl+n` | 移动到下一个自动补全条目 |
| `prompt.autocomplete.hide`     | `escape`      | 隐藏自动补全             |
| `prompt.autocomplete.select`   | `return`      | 选择自动补全条目         |
| `prompt.autocomplete.complete` | `tab`         | 补全自动补全条目         |
| `permission.prompt.fullscreen` | `ctrl+f`      | 切换权限提示全屏         |
| `plugins.toggle`               | `return`      | 切换插件                 |
| `dialog.mcp.toggle`            | `space`       | 切换 MCP 服务器          |
| `dialog.plugins.error`         | `space`       | 查看插件错误             |
| `dialog.plugins.update`        | `ctrl+u`      | 从插件对话框更新插件     |
| `dialog.plugins.check`         | `ctrl+r`      | 检查插件更新             |

## 终端与插件

| ID                      | 默认值   | 说明               |
| ----------------------- | -------- | ------------------ |
| `terminal.suspend`      | `ctrl+z` | 挂起终端           |
| `terminal.title.toggle` | `none`   | 切换终端标题       |
| `plugins.list`          | `none`   | 打开插件管理对话框 |

## Which-Key

| ID                         | 默认值                      | 说明                     |
| -------------------------- | --------------------------- | ------------------------ |
| `which-key.toggle`         | `ctrl+alt+k`                | 切换 which-key 面板      |
| `which-key.layout.toggle`  | `ctrl+alt+shift+k`          | 切换 which-key 布局      |
| `which-key.pending.toggle` | `ctrl+alt+shift+p`          | 切换 which-key 待定预览  |
| `which-key.group.previous` | `ctrl+alt+left,ctrl+alt+[`  | 上一个 which-key 组      |
| `which-key.group.next`     | `ctrl+alt+right,ctrl+alt+]` | 下一个 which-key 组      |
| `which-key.scroll.up`      | `ctrl+alt+up,ctrl+alt+p`    | which-key 向上滚动       |
| `which-key.scroll.down`    | `ctrl+alt+down,ctrl+alt+n`  | which-key 向下滚动       |
| `which-key.page.up`        | `ctrl+alt+pageup`           | which-key 向上翻页       |
| `which-key.page.down`      | `ctrl+alt+pagedown`         | which-key 向下翻页       |
| `which-key.home`           | `ctrl+alt+home`             | 跳转到第一个 which-key 绑定 |
| `which-key.end`            | `ctrl+alt+end`              | 跳转到最后一个 which-key 绑定 |
