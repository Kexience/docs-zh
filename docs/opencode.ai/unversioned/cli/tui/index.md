---
source_url: https://opencode.ai/docs/cli/tui/
source_hash: sha256:a1fa60f217f4077a9cb7820d3feb0e40350160790c6027039c1a4c6039155207
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# TUI

在你的项目目录中运行 OpenCode，输入请求，然后按 **Enter**。

```bash
cd ~/code/my-project
opencode
```

```text
Explain how authentication works in this project
```

按 **Shift+Enter**、**Ctrl+Enter**、**Alt+Enter** 或 **Ctrl+J** 可以换行。当 OpenCode 正在工作时，**Enter** 用于干预当前会话；按 **Ctrl+X** 再按 **Enter** 可以把提示词排入队列稍后执行。

## 上下文

输入 `@` 搜索文件，选中后即可把该文件附加到提示词中。在 `@` 之后继续输入可以缩小结果范围。

```text
Review @src/auth.ts for error handling problems
```

可以在路径后面附加行号或行范围。

```text
Explain @src/auth.ts#20-45
```

## Shell

在空提示词的开头输入 `!` 进入 shell 模式。输入命令后按 **Enter**；按 **Esc** 可以在未执行命令的情况下退出 shell 模式。

```text
!git status
```

Shell 命令在会话的工作目录中运行，其输出会保留在会话中。

## 命令

输入 `/` 列出斜杠命令。继续输入可以过滤列表，然后按 **Enter** 运行选中的命令。

```text
/models
```

常用命令包括 `/new`、`/sessions`、`/models`、`/agents`、`/undo`、`/redo` 和 `/editor`。按 **Ctrl+P** 打开命令面板，可以查看当前视图下所有可用的操作。

更新之后，OpenCode 会在主屏幕上一次性展示本次版本的更新内容。运行 `/highlights` 可以再次查看，或在 [`cli.json`](../config/index.md#alerts) 中设置 `"highlights": false` 来禁止它自动打开。

## 题外话提问

运行 `/btw <question>` 可以就目前的对话快速提问。回答会使用会话的上下文和当前模型，但不会被加入对话，因此不影响后续的提示词。`/btw` 运行期间会在提示词页脚显示一个指示器，回答完成后在一个对话框中打开；按 **C** 可以复制。

```text
/btw why did the test in step 2 fail?
```

## 模型

按 **Ctrl+X** 再按 **M** 选择模型，或运行 `/models`。按 **F2** 可以在最近使用的模型之间循环切换。

按 **Ctrl+X** 再按 **A** 选择 agent，或运行 `/agents`。按 **Shift+Tab** 可以循环切换 agent。

## 会话

按 **Ctrl+X** 再按 **N** 新建会话。按 **Ctrl+X** 再按 **L**，或运行 `/sessions`，可以回到已有的会话；**Ctrl+O** 同时打开最近的会话和项目。

标签页默认启用。使用 **Ctrl+Tab** 和 **Ctrl+Shift+Tab** 在标签页之间切换，按 **Ctrl+X** 再按 **W** 关闭一个标签页，按 **Ctrl+Shift+T** 重新打开最近关闭的标签页。

## 历史

按 **Ctrl+X** 再按 **U**，或运行 `/undo`，可以回退最近一条用户消息及其后续工作。被回退的提示词会回到输入框，方便你编辑。

按 **Ctrl+X** 再按 **R**，或运行 `/redo`，可以恢复被回退的工作。改为发送一条新提示词则意味着接受这次回退，并从该时间点继续。

## 编辑器

设置 `VISUAL` 或 `EDITOR`，然后按 **Ctrl+X** 再按 **E**，或运行 `/editor`，即可在对应编辑器中编辑当前提示词。保存并退出后，文本会返回输入框，按 **Enter** 发送。

```bash
export EDITOR="nvim"
opencode
```

前导键默认为 **Ctrl+X**。要修改这些快捷键，请参阅[按键绑定](../keybinds/index.md)。
