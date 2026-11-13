---
source_url: https://opencode.ai/docs/permissions/
source_hash: sha256:ceb578f112d84ce0d8f9d25775cbb5893db5cfc9ceb3ca9620bf20abb1f0e79b
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# 权限

权限用于控制 agent 是否可以对某个资源执行某个操作。

## 配置

一种常见的配置方式是：运行 shell 命令前先询问，放行常规的 Git 查看操作，并始终禁止 push。在 `opencode.jsonc` 中添加以下按顺序排列的规则：

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "permissions": [
    { "action": "shell", "resource": "*", "effect": "ask" },
    { "action": "shell", "resource": "git status *", "effect": "allow" },
    { "action": "shell", "resource": "git diff *", "effect": "allow" },
    { "action": "shell", "resource": "git push *", "effect": "deny" },
  ],
}
```

最后匹配到的规则生效，因此具体的例外规则要放在宽泛规则之后。

<Callout type="warning">
  V1 使用不同的字段和 action 名称。在 V2 中，请使用 `permissions`、`shell` 和 `subagent`，而不是 `permission`、`bash` 和 `task`。
</Callout>

## 规则

每条规则需要三个字符串字段：

| 字段       | 含义                                                                         |
| ---------- | ---------------------------------------------------------------------------- |
| `action`   | 工具权限操作                                                                 |
| `resource` | 被使用的值，例如路径、命令、URL、查询、skill ID 或 agent ID                  |
| `effect`   | `allow`、`deny` 或 `ask`                                                     |

```jsonc
{
  "permissions": [
    { "action": "read", "resource": "*", "effect": "allow" },
    { "action": "read", "resource": "*.env", "effect": "deny" },
  ],
}
```

| 效果    | 结果                                 |
| ------- | ------------------------------------ |
| `allow` | 直接继续，不提示                     |
| `deny`  | 阻止该操作                           |
| `ask`   | 等待客户端做出决定                   |

如果没有规则匹配，OpenCode 默认使用 `ask`。

## 匹配

action 和 resource 使用简单的整值通配符：

| 模式    | 匹配                                       |
| ------- | ------------------------------------------ |
| `*`     | 零个或多个字符，包括 `/`                   |
| `?`     | 恰好一个字符                               |
| 其他    | 该字面字符本身                             |

```jsonc
{
  "permissions": [
    { "action": "edit", "resource": "packages/docs/*.mdx", "effect": "allow" },
  ],
}
```

该模式会匹配整个规范化后的路径。反斜杠会被规范化为正斜杠，并且在 Windows 上匹配不区分大小写。

以 ` *` 结尾的 shell 模式还会匹配不带参数的命令：

```jsonc
{ "action": "shell", "resource": "git status *", "effect": "allow" }
```

这会同时匹配 `git status` 和 `git status --short`。

OpenCode 按顺序组合规则并采用最后一个匹配项。优先级更低的配置先加载，随后追加全局规则，最后追加 agent 规则。

```jsonc
{
  "permissions": [
    { "action": "read", "resource": "*", "effect": "allow" },
    { "action": "read", "resource": "secrets/*", "effect": "deny" },
  ],
}
```

一次操作可能检查多个资源，例如一个补丁涉及多个文件。任何一个 `deny` 都会否决整个操作；否则只要有一个 `ask` 就会询问；否则该操作被放行。

## 操作（Actions）

V2 的 action 名称是字符串，因此插件可以定义更多 action。内置工具目前使用以下 action 和 resource：

| 操作                          | 资源                                                                           |
| --------------------          | ------------------------------------------------------------------------------- |
| `read`                        | 相对于 Location 的内部路径，或规范化的外部绝对路径                              |
| `edit`                        | `edit`、`write` 和 `patch` 的目标路径                                           |
| `glob`                        | 请求的 glob 模式                                                                |
| `grep`                        | 请求的正则表达式，而非搜索路径                                                  |
| `shell`                       | 由扫描器产出的命令字符串；复合命令可能产出多条                                  |
| `subagent`                    | 目标 agent ID                                                                   |
| `skill`                       | Skill ID                                                                        |
| `question`                    | `*`                                                                             |
| `webfetch`                    | 请求的 URL                                                                      |
| `websearch`                   | 搜索查询                                                                        |
| `experimental_image_generate` | 所选图像模型，形如 `providerID/modelID`，若设置了变体则追加 `#variant`          |
| `external_directory`          | 规范化的外部目录边界，通常以 `/*` 结尾                                          |
| `<server>_<tool>`             | 对于 MCP 工具为 `*`；两个名称中不受支持的字符会被替换为 `_`                     |
| `opencode_list_mcp_resources` | MCP 服务器名称                                                                  |
| `opencode_read_mcp_resource`  | `<server>:<uri>`                                                                |
| `execute`                     | `*`；一条 deny 规则会移除 Code Mode 并直接列出其工具，同时嵌套工具会执行各自的规则 |

例如，允许一个 skill 而拒绝其他所有 skill：

```jsonc
{
  "permissions": [
    { "action": "skill", "resource": "*", "effect": "deny" },
    { "action": "skill", "resource": "effect", "effect": "allow" },
  ],
}
```

`doom_loop` 和 `lsp` 不是当前 V2 Core 的权限操作。

## 目录

既不在当前 Location 内、也不在其非根项目 worktree 内的路径，会先按 `external_directory` 规则检查，然后才检查其 `read` 或 `edit` 规则。默认策略允许 `external_directory`，因此除非你添加规则，否则外部路径不会触发提示。如果希望在访问项目之外的任何路径前先询问：

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "permissions": [
    { "action": "external_directory", "resource": "*", "effect": "ask" },
  ],
}
```

在其后添加更具体的规则，可以放行或拒绝特定目录：

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "permissions": [
    { "action": "external_directory", "resource": "~/projects/reference/*", "effect": "allow" },
    { "action": "read", "resource": "~/projects/reference/*", "effect": "allow" },
    { "action": "edit", "resource": "~/projects/reference/*", "effect": "deny" },
  ],
}
```

这适用于 `read`、`edit`、`write` 和 `patch` 使用的外部路径。`shell` 在检查 `shell` 资源之前，也会检查其外部工作目录以及由扫描器推断出的目录。

对于 `external_directory`、`read` 和 `edit`，开头的 `~`、`~/`、`$HOME` 或 `$HOME/` 会在配置加载时被展开：

```jsonc
{ "action": "read", "resource": "$HOME/reference/*", "effect": "allow" }
```

`shell` 资源保持原始命令文本，不会进行家目录展开。

<Callout type="warning">
  `shell` 以宿主用户的文件系统、进程和网络权限运行。从命令文本推断目录只是尽力而为，因此更推荐收紧 shell 白名单，而不是试图用模式识别每一个危险命令。
</Callout>

相对的修改路径可能离开当前 Location，但仍在项目 worktree 内。显式的外部路径在匹配前会被规范化，因此只应授权可信的目录边界。

## 扫描器

Shell 权限检查使用 OpenCode 内置的 shell 扫描器，覆盖 Bash、Zsh、POSIX `sh` 和 PowerShell。当命令存在畸形语法，或包含扫描器无法安全分析的动态求值时，会返回扫描器错误，而不是执行未经校验的子命令。

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "policies": [
    {
      "permissions": [
        { "action": "shell", "resource": "git status *", "effect": "allow" },
        { "action": "shell", "resource": "rm *", "effect": "deny" },
      ],
    },
  ],
}
```

权限规则、已保存的批准模式，以及尽力而为的目录推断，都会应用于每一个提取出的子命令和 `cd` 目标。对于未知目录，没有额外的批准模式，也没有一刀切的限制。

## 默认值

每个 agent（包括自定义 agent）都以以下按顺序排列的基础策略开始：

```jsonc
[
  { "action": "*", "resource": "*", "effect": "allow" },
  { "action": "read", "resource": "*.env", "effect": "ask" },
  { "action": "read", "resource": "*.env.*", "effect": "ask" },
  { "action": "read", "resource": "*.env.example", "effect": "allow" },
]
```

内置 agent 会追加以下策略：

| Agent        | 附加策略                                                                       |
| ------------ | ------------------------------------------------------------------------------ |
| `build`      | 允许提问                                                                       |
| `plan`       | 允许提问；除 `~/.opencode/plan` 下的文件外，拒绝一切编辑                        |
| `general`    | 拒绝提问和启动子 agent                                                          |
| `explore`    | 除 shell、读取、glob、grep、网页抓取、网页搜索和外部目录外，拒绝一切操作；读取 `.env` 时会询问 |
| `title`      | 拒绝所有操作                                                                    |
| `summary`    | 拒绝所有操作                                                                    |
| `compaction` | 保留基础策略                                                                    |

由于默认规则不会对 `external_directory` 触发询问，Location 和 worktree 之外的读取和编辑会直接进行、不弹出提示。如[目录](目录)所示，添加一条 `external_directory` 的 `ask` 或 `deny` 规则，可以恢复提示或阻止外部访问。
后续追加的全局规则和 agent 规则会覆盖这些默认值。

## Agent

将共享规则放在顶层，将更具体的规则放在 `agents.<id>.permissions` 下：

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "permissions": [
    { "action": "shell", "resource": "*", "effect": "ask" },
    { "action": "shell", "resource": "git status *", "effect": "allow" },
  ],
  "agents": {
    "reviewer": {
      "description": "Review code without changing it",
      "mode": "subagent",
      "permissions": [
        { "action": "edit", "resource": "*", "effect": "deny" },
      ],
    },
  },
}
```

Agent 规则会追加在全局规则之后，而不是替换全局数组。自定义子 agent 使用自己的权限，而不是其父 agent 权限的子集。

## 批准

当某条规则解析为 `ask` 时，客户端可以回复：

| 选择           | 回复       | 结果                                                                 |
| -------------- | ---------- | -------------------------------------------------------------------- |
| 仅本次允许     | `once`     | 只批准当前待处理的请求                                               |
| 始终允许       | `always`   | 批准该请求，并将该工具提议的模式保存到项目中                         |
| 拒绝           | `reject`   | 拒绝该请求，以及该会话中所有其他待处理的权限请求                     |

例如，对 `git status --short` 选择**始终允许**，可能会保存一条覆盖后续 `git status` 命令的 shell 前缀：

```text
shell: git status * → allow
```

已保存的批准是持久的、项目范围的 `allow` 规则。它们永远不会覆盖已配置的 `deny`。保存模式由工具自行提议：有的工具提议 `*`，shell 提议命令前缀，skill 和子 agent 提议各自的 ID。请定期审查宽泛的批准项，并移除不再需要的条目。

客户端在拒绝时可以附带反馈。非交互式客户端必须自行决定如何处理批准请求；已配置的 `deny` 规则始终强制生效。

## 策略（Policies）

在这些规则和已保存的批准执行完毕之后，[策略](../policies/index.md)可以对权限检查进行硬性否决。它会把 `allow` 或 `ask` 变成 `deny`，绝不会授予访问权限。

```jsonc
{
  "policies": [{ "action": "tool.use", "resource": "shell:sudo *", "effect": "deny" }],
}
```

全局策略和 Console 托管的策略会覆盖项目配置——组织正是通过这种方式阻止某个仓库本想放行的命令。
