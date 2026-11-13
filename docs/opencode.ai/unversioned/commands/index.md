---
source_url: https://opencode.ai/docs/commands/
source_hash: sha256:c9dac1dda111fdba38895780e7c5014ca58965122a247adc31c6acceee90e8a3
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# 命令

创建 `.opencode/commands/review.md`，即可把一段提示词变成 `/review`：

```md title=".opencode/commands/review.md"
Review $ARGUMENTS for bugs and missing tests.
```

在 TUI 中带目标运行它：

```text
/review src/auth.ts
```

OpenCode 会以用户提示词的形式提交 `Review src/auth.ts for bugs and missing tests.`

## Markdown

全局命令放在 `~/.config/opencode/commands/`，项目命令放在 `.opencode/commands/`。

```text
~/.config/opencode/commands/review.md
.opencode/commands/review.md
```

只会发现 `.md` 文件。嵌套路径会成为以 `/` 分隔的命令名：

```md title=".opencode/commands/team/review.md"
Review $ARGUMENTS using the team's checklist.
```

以 `/team/review src/auth.ts` 运行嵌套命令。旧版的单数目录 `command/` 同样会被发现，但新文件请使用 `commands/`。

当命令需要元数据时，可以添加 YAML frontmatter。裁剪后的 Markdown 正文始终是提示词模板。

```md title=".opencode/commands/review.md"
---
description: Review code for correctness
agent: plan
model: anthropic/claude-sonnet-5-5#high
---

Review $ARGUMENTS. Report bugs first.
```

## JSON

在任意 OpenCode JSON 或 JSONC [配置文件](../config/index.md)的 `commands` 下定义命令。每个命令都需要一个 `template`。

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "commands": {
    "review": {
      "description": "Review code for correctness",
      "template": "Review $ARGUMENTS. Report bugs first.",
    },
  },
}
```

## 字段

Markdown frontmatter 和 JSON 条目接受相同的字段，区别在于 Markdown 的 `template` 来自文件正文。

| 字段 | 是否必需 | 行为 |
| --- | --- | --- |
| `template` | 仅 JSON | 提示词模板。 |
| `description` | 否 | 在命令列表和发现界面中显示的文字。 |
| `agent` | 否 | 命令运行时选用的 agent。 |
| `model` | 否 | 模型覆盖，格式为 `provider/model` 或 `provider/model#variant`。 |
| `subagent` | 否 | `true` 在后台子会话中运行；`false` 强制使用当前会话。 |
| `subtask` | 否 | `subagent` 的已弃用别名。 |

例如，下面这个 JSON 命令设置了所有当前可选字段：

```jsonc title="opencode.jsonc"
{
  "commands": {
    "audit": {
      "template": "Audit $ARGUMENTS.",
      "description": "Audit a package",
      "agent": "general",
      "model": "anthropic/claude-sonnet-5-5#high",
      "subagent": true,
    },
  },
}
```

不要把 `template` 放进 Markdown frontmatter；正文就是它的来源。

## 参数

使用 `$ARGUMENTS` 表示与输入完全一致的完整参数字符串。

```md title=".opencode/commands/component.md"
Create a typed React component named $ARGUMENTS.
```

对于 `/component Account Settings`，占位符会变成 `Account Settings`。

## 位置参数

使用 `$1`、`$2` 及更大的数字表示解析出的位置参数。单引号或双引号可以分组单词，并且引号本身会被去掉。

```md title=".opencode/commands/check.md"
Check $1. Focus on $2.
```

对于 `/check src/auth.ts "error handling"`，`$1` 变成 `src/auth.ts`，`$2` 变成 `error handling`。

编号最高的占位符会吞掉它的参数及其后的所有内容。缺失的位置会变成空字符串。

```md title=".opencode/commands/compare.md"
Compare $1 with $2.
```

对于 `/compare api stable branch`，OpenCode 会提交 `Compare api with stable branch.`

## 兜底

当模板中既没有 `$ARGUMENTS` 也没有位置占位符时，OpenCode 会在一个空行之后附加非空参数。

```md title=".opencode/commands/explain.md"
Explain this code clearly.
```

对于 `/explain src/cache.ts`，提示词会变成：

```text
Explain this code clearly.

src/cache.ts
```

## Shell

用 `!` 加反引号包裹一条 shell 命令，可以在提示词提交前插入其输出。

```md title=".opencode/commands/review-diff.md"
Review this diff:

!`git diff --stat && git diff`
```

OpenCode 使用配置的 shell 在当前项目位置运行每个代码块，并插入其合并后的输出。参数占位符会先被展开：

```md title=".opencode/commands/history.md"
Summarize these commits:

!`git log --oneline -$1`
```

对于 `/history 5`，shell 收到的是 `git log --oneline -5`。不要把不受信任的参数放进 shell 代码块。

<Callout type="warning">
  Shell 代码块在 OpenCode 解析命令时运行，不经过 agent 的工具权限流程。只使用来自可信来源的命令。
</Callout>

## 附件

存储的模板不会展开 `@path`；它会保留为普通的提示词文本。

```md title=".opencode/commands/readme.md"
Review @README.md.
```

要附加文件，请在调用命令时通过输入框添加。OpenCode 在提交展开后的提示词时会保留这些输入框附件。

## 执行

命令会在提交持久化用户提示词之前展开参数和 shell 代码块。它们默认在当前会话中运行。

```md title=".opencode/commands/plan.md"
---
agent: plan
---

Plan $ARGUMENTS.
```

运行 `/plan migration` 会在提交提示词前把当前会话切换到 `plan`。

模型选择遵循以下规则：

1. 命令的 `model` 覆盖所有其他模型。
2. 否则，所选命令 agent 配置的模型覆盖调用时激活的模型。
3. 否则，当前会话的模型保持激活。

例如，下面这个命令同时选择了它的 agent 和一个显式模型：

```md title=".opencode/commands/design.md"
---
agent: plan
model: openai/gpt-6.1-sol#high
---

Design $ARGUMENTS.
```

## 后台运行

设置 `subagent: true` 可以让命令在后台子会话中运行。

```md title=".opencode/commands/audit.md"
---
description: Audit changes
agent: general
subagent: true
---

Audit $ARGUMENTS for bugs and missing tests.
```

父会话保持可用，并保留自己的 agent 和模型。子会话结束时，OpenCode 会把它的结果或失败发回父会话。

| 值 | 行为 |
| --- | --- |
| `true` | 始终使用子会话，即使所选 agent 是 `mode: primary`。 |
| `false` | 始终使用当前会话，即使所选 agent 是 `mode: subagent`。 |
| 省略 | 仅当所选 agent 是 `mode: subagent` 时才使用子会话。 |

子会话依次使用命令的模型、所选 agent 的模型、父会话的模型。旧版 `subtask` 仍然被接受；如果两个字段同时存在，`subagent` 优先。

```yaml
subagent: false
subtask: true
```

这个示例会在当前会话中运行，因为 `subagent` 优先。

## 加载

Markdown 命令和 JSON 命令共用一个注册表。后加载的来源会替换与先加载来源同名的命令。

```text
~/.config/opencode/commands/review.md   # Lower priority
.opencode/commands/review.md           # Replaces the global command
```

项目来源优先于全局来源，更近的项目来源优先于祖先目录来源。自定义定义也可以替换先前的内置命令。OpenCode 会自动重载命令文件和配置变更。

```md title=".opencode/commands/review.md"
Review only the staged changes: !`git diff --cached`
```

保存这个文件后，`/review` 无需重启 OpenCode 即可更新。
