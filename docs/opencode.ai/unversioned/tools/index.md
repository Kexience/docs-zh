---
source_url: https://opencode.ai/docs/tools/
source_hash: sha256:fe2de4daf2cc53529c2117b7bb5377f1730cc5a92119f43305e8f2049e6ada4a
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# 工具

直接说出你想要的结果。OpenCode 会自行选择可用的工具，在需要时请求批准，并返回结果。

```text
Find where request timeouts are configured, change the default to 30 seconds,
and run the relevant existing tests.
```

这类任务通常会用到 `grep` 或 `glob`、`read`、某个编辑工具以及 `shell`。你也可以点名某个工具来指定具体的做法。

```text
Use grep to find every reference to DEFAULT_TIMEOUT, then read the matching files.
```

## 文件

### Read

`read` 返回文件内容或非递归的目录列表。传入 `path`；用 `offset` 和 `limit` 对较大的结果分页读取。

```text
Read src/server.ts starting at line 120 and return at most 80 lines.
```

文本读取的每页结果带行号，最多 2,000 行、50 KiB。单行超过 2,000 个字符会被截短。该工具还能把 PNG、JPEG、GIF、WebP 和 PDF 文件传给模型，源数据最多 20 MiB。其他二进制文件会失败。支持的媒体类型和图片处理见[附件](../attachments/index.md)。

权限：`read`，资源为规范化后的路径。

### Glob

`glob` 根据诸如 `**/*.ts` 的模式查找文件路径。除非 `path` 指定了其他相对目录，否则搜索当前目录；`hidden` 包含隐藏条目，`limit` 限制结果数量。

```text
Use glob with **/*.test.ts under packages/core and return at most 50 files.
```

默认上限为 100 个文件，搜索超时为 30 秒。
权限：`glob`，资源为请求的模式。

### Grep

`grep` 搜索文件内容，返回路径、行号和预览。除非 `literal` 为 true，`pattern` 使用正则表达式语法。可以用 `path`、`include`、`caseSensitive` 或 `limit` 收窄搜索范围。

```text
Use grep for the literal text "request timed out" in src, including only *.ts files.
```

默认上限为 100 条匹配行，搜索超时为 30 秒。
权限：`grep`，资源为请求的模式，而不是搜索路径。

### Edit

`edit` 替换现有文件中的文本。提供 `path`、`oldString` 和一个不同的 `newString`；旧文本必须恰好匹配一次，除非 `replaceAll` 为 true。

```text
In src/config.ts, replace the unique text "timeout: 60" with "timeout: 30".
```

`edit` 适合范围明确的小改动。OpenCode 可能会在写入后对文件进行格式化。
权限：`edit`，资源为目标路径。

### Write

`write` 依据 `path` 和 `content` 创建或完全替换一个文本文件。它会自动创建缺失的父目录，并可能运行已配置的格式化工具。

```text
Create docs/example.md with a heading and one setup command.
```

如果只需要修改现有文件的一部分，请改用 `edit`。
权限：`edit`，资源为目标路径。

### Patch

`patch` 应用一个补丁，可同时添加、更新、移动或删除多个文件。它的 `patchText` 使用 `*** Add File`、`*** Update File` 和 `*** Delete File` 分段。

```text
Use patch to rename src/old.ts to src/new.ts and update its exported name.
```

OpenCode 针对受支持的 GPT 模型提供 `patch`；其他模型会得到 `edit` 和 `write`。权限：`edit`，资源为每个受影响的路径。

活动 Location 及其项目 worktree 之外的路径还会对照 `external_directory` 进行检查，该规则默认允许。路径规范化、规则顺序和已保存的批准见[权限](../permissions/index.md)。要让外部材料以名称形式可用，请配置[引用](../references/index.md)。

## 命令

### Shell

`shell` 在宿主用户的 shell 中执行命令。请设置 `workdir` 而不是在命令里写 `cd`；当默认的两分钟前台超时不适用时，以毫秒为单位设置 `timeout`。

```text
Run bun test from packages/core with a five-minute timeout.
```

对于开发服务器或其他长期运行的进程，可将 `background` 设为 true。后台调用会立即返回，并在完成时通知会话；除非显式提供，否则没有超时。较大的输出会被截短，完整输出保留在一个受管理的文件中。

权限：`shell`，资源为扫描器生成的每条命令。扫描器还会检查外部工作目录以及能从命令推断出的目录。shell 拥有宿主用户的文件系统、进程和网络权限，因此请在[权限](../permissions/index.md)中使用窄范围的规则。

## 网络

### Webfetch

`webfetch` 以 `markdown`、`text` 或 `html` 格式获取一个 HTTP 或 HTTPS URL。默认为 Markdown；`timeout` 最多接受 120 秒。

```text
Fetch https://example.com/docs as markdown.
```

它接受文本类响应，如 HTML、纯文本、JSON 和 XML，但不接受图片或其他二进制下载。较大的输出可能被截短，完整文本保留在受管理的存储中。权限：`webfetch`，资源为请求的 URL。

### Websearch

`websearch` 在所选的集成中搜索最新信息。输入是一个搜索 `query`。

```text
Search the web for the latest Bun release notes.
```

权限：`websearch`，资源为查询内容。provider、选择方式、速率限制和禁用该工具的方法见[网络搜索](../websearch/index.md)。

## 图片

### 图片生成

`experimental_image_generate` 根据提示创建新图片，或编辑已有图片。它是实验性功能，仅在已连接的 provider 具有图像模型时出现。要选择它的默认模型，请参见 [`experimental.image_generate`](../config/index.md#image-generation)。

```text
Generate a flat app icon of a paper plane on a blue background and save it to assets/icon.png.
```

传入 `prompt`，可选地传入 `images` 用于编辑或作为参考、指定的 `model`，或保存到的 `path`。它在后台运行，图片就绪后会以保存路径通知会话。

权限：`experimental_image_generate`，资源为所选模型。

## 交互

### Question

`question` 会暂停执行，并向用户展示一个或多个问题。每个问题有简短的标题、提示和选项；`multiple` 允许选择多个答案。自由填写答案始终可用。

```text
Before changing the API, ask me to choose between a breaking change and a compatibility layer.
```

权限：`question`，资源为 `*`。客户端必须支持交互式表单，关闭表单即取消问题。

### Skill

`skill` 将某个可用技能 ID 的说明和随附资源加载到对话中。

```text
Load the effect skill before changing this Effect code.
```

ID 必须出现在已声明的技能列表中，或由用户明确指定。
权限：`skill`，资源为技能 ID。技能的创建、发现和加载规则见[技能](../skills/index.md)。

## 自动化

### Subagent

`subagent` 用已配置的 subagent 启动一个子会话。提供 agent ID、简短的 `description` 和完整的 `prompt`。

```text
Ask the explore subagent to map the authentication flow and return the key files.
```

subagent 始终在后台运行。调用会立即返回 `sessionID`，父会话在子会话空闲时收到一条 `<subagent>` 消息，之后每轮工作完成后也会再次收到，因此父会话可以继续工作或结束回合而无需等待。传入返回的 `sessionID` 可以继续同一个子对话；对正在运行的子会话的后续输入会加入其当前运行。只能使用 subagent 模式的 agent，默认嵌套深度为一层。

权限：`subagent`，资源为所选的 agent ID。

### Execute

`execute` 在 Code Mode 中运行 JavaScript，使 agent 能够调用并组合目录中的工具。它适合并行执行相互独立的调用，以及在不把每个中间值都塞进模型上下文的情况下处理结果。

```text
Read package.json and README.md in parallel, then return their relevant setup details.
```

运行时没有直接的文件系统访问、导入或定时器。它提供 `fetch` 用于 HTTP 请求；其他一切都通过其目录中的工具完成。以资源 `*` 拒绝 `execute` 会移除 Code Mode，此时它原本要访问的工具（包括未设置 `codemode: false` 的服务器提供的 MCP 工具）会作为直接工具列出，每个请求都会附带其完整定义。如果不希望 agent 拥有这些工具，也一并拒绝它们。嵌套的内置工具和 MCP 工具仍会执行各自的权限检查，插件工具也会执行它们声明的权限。

### Sessions

`opencode` Code Mode 命名空间包含会话工具：

- `session_rename` 更改当前会话（或由 `sessionID` 指定的其他会话）的标题。
- `session_move` 将当前会话或另一个选定的会话移动到相对或绝对的 `directory`。移动在安全边界处生效，因此依赖目标位置的工作应放在后续调用中进行。

```text
Rename this session to "Timeout cleanup", then move it to the new worktree.
```

### Worktrees

同一命名空间还管理会话所属项目的 worktree：

- `worktree_create` 根据 `name` 创建 worktree 并返回其 `directory`。项目的 worktree 配置决定目的地和策略。
- `worktree_list` 列出项目的 worktree。
- `worktree_remove` 移除 OpenCode 为项目记录的某个 worktree。设置 `force` 可丢弃未提交的更改。

```text
Create a worktree named "login" and move this session into it.
```

`worktree_remove` 使用 `edit` 权限，资源为该 worktree 目录。其他 worktree 工具不会请求内置的权限操作。

## 浏览器

`browser` Code Mode 命名空间控制 OpenCode 桌面应用附带的浏览器。先打开一个标签页并保存返回的 `tabID`，然后把该明确的 ID 传给每一次页面操作。

```text
Open https://example.com, take a snapshot of that tab, and report the main heading.
```

该命名空间包括标签页和导航命令、页面快照与搜索、点击和表单输入、截图、文件传输、控制台与网络检查、性能追踪、堆内存检查以及 Lighthouse 审计。截图要求有一个获得焦点且可见的标签页。上传路径为服务器本地路径；截图返回服务器本地路径，每次文件传输上限为 5 MiB。

页面内容、日志、请求头和响应体都是不可信数据，而不是 agent 指令。以资源 `*` 设置 `browser` 拒绝规则会移除整个浏览器目录；浏览器操作不会逐项弹出权限提示。

## 扩展

[MCP 服务器](../mcp-servers/index.md)提供的工具，其名称和输入来自每个已连接的服务器。它们的权限动作为 `<server>_<tool>`，资源为 `*`。它们不是内置目录的固定组成部分。默认情况下，agent 通过 `execute` 在服务器的命名空间下访问它们；在服务器上设置 `codemode: false` 可将其工具直接列出。

[技能](../skills/index.md)提供的是任务说明，而不是新的可执行工具。[附件](../attachments/index.md)把用户选择的内容放入提示，而[引用](../references/index.md)提供命名的目录。这些功能与工具互为补充，但不会绕过它们的权限检查。
