---
source_url: https://opencode.ai/docs/instructions/
source_hash: sha256:48f7b9812fc57a166b305d5a9c64febd78f2446b403cc1d6b9cd6da1d63ef46a
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# 指令（Instructions）

添加一个 `AGENTS.md` 文件，为 OpenCode 提供持续生效的项目指引。可以用它记录构建命令、架构说明、代码规范和验证要求。

```md title="AGENTS.md"
# Project instructions

- Run `bun typecheck` after changing TypeScript.
- Keep database queries in `src/database`.
- Do not edit generated files directly.
```

将项目指令文件提交到仓库，这样在该仓库中工作的每个人都能得到相同的指引。

## 作用范围

把 `AGENTS.md` 放在希望其指引生效的目录中。OpenCode 会加载全局文件，以及从当前工作区目录向上至家目录之间的每一个 `AGENTS.md`。对于位于家目录之外的工作区，它会停在项目根目录。

```text
~/.config/opencode/AGENTS.md
~/code/my-project/AGENTS.md
~/code/my-project/packages/AGENTS.md
~/code/my-project/packages/web/AGENTS.md  ← current workspace
```

在这个示例中，四个文件都会被加载，并按以下顺序组合：

```text
~/.config/opencode/AGENTS.md
packages/web/AGENTS.md
packages/AGENTS.md
AGENTS.md
```

适用于所有地方的指引放在全局文件中。仓库级的指引放在项目根目录，更具体的指引放在更靠近它所覆盖代码的位置。OpenCode 只组合这些文件，不会解决它们之间的冲突。

如果工作区在项目根目录之外，则只加载全局文件。设置 `OPENCODE_DISABLE_PROJECT_CONFIG=1` 可以跳过项目 `AGENTS.md` 的发现，同时不禁用全局文件。

<Callout type="note">
  OpenCode V2 只识别 `AGENTS.md`。它不会使用 `CLAUDE.md` 作为回退。
</Callout>

## 发现

工作区以下的指令文件会随着 agent 探索项目而被发现。读取某个文件或列出某个目录时，会加载该目标与工作区之间的所有 `AGENTS.md` 文件。

```text
my-project/                         ← current workspace
├── AGENTS.md                       loaded initially
└── packages/
    └── web/
        ├── AGENTS.md               loaded when this area is read
        └── src/
            └── app.ts              read target
```

嵌套文件按由近到远的顺序加载，并在其指令条目仍保留在模型可见历史中时进行去重。再次读取同一区域通常不会重复注入。如果压缩或回退移除了该条目，之后的读取可能会再次加载该文件。

嵌套文件加载后，对其的编辑不会被自动检测。当更新后的文本需要立即生效时，请新建一个会话。

## 顺序

选中的 agent 或 provider 的系统提示词最先发送。随后 OpenCode 按以下顺序组装初始指令：

```text
1. Agent or provider system prompt
2. Code Mode tool guidance, when enabled
3. MCP server, reference, and skill guidance
4. Global and project AGENTS.md files, then configured instructions
5. Built-in date and environment context
6. Session-specific instruction entries supplied through the API
```

这些来源是组合关系，而不是相互覆盖。之后发现的嵌套 `AGENTS.md` 文件会按发现顺序加入会话历史。

## 更新

在会话运行期间编辑全局或向上发现的 `AGENTS.md`，即可更新其指引。

```bash
$ printf '\n- Run the integration suite before committing.\n' >> AGENTS.md
```

在下一个模型请求之前，OpenCode 会检测到变化，并在送达待处理的输入之前加入一条指令更新：

```text
AGENTS.md changes
→ instruction update
→ next prompt
```

- 移除所有环境 `AGENTS.md` 会告诉会话，先前的环境指令不再适用。
- 临时的读取失败会保留最后已知的指令，而不是将其视为已删除。
- 移动会话会保留其指令状态，因此目标位置的指引会以更新的形式引入。
- 提交一次会话回退会清除其指令状态，并在下一个提示词之前重新加载指令。

指令内容保持特权状态。客户端可以看到哪些来源发生了变化，但看不到其内容。

## 配置

使用 `instructions` 数组，可以在发现的 `AGENTS.md` 文件之外添加文件、glob 模式或 HTTP(S) URL：

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": [
    "CONTRIBUTING.md",
    "docs/guidelines/*.md",
    "~/rules/opencode.md",
    "https://example.com/instructions.md",
  ],
}
```

配置的指令在 `AGENTS.md` 文件之后按列出顺序加载。所有配置文档中的条目都会被合并。

| 条目                    | 解析方式                                                               |
| ----------------------- | ---------------------------------------------------------------------- |
| 相对路径或 glob         | 在从工作区到项目根目录之间的每个目录中搜索                             |
| `~/` 路径               | 从你的家目录解析                                                       |
| 绝对路径                | 按原样使用；文件名可以是 glob                                          |
| `http://` 或 `https://` | 配置加载时获取，超时时间为五秒                                         |

- 本地文件在发生变化时与 `AGENTS.md` 一样更新。匹配某个 glob 的新文件会在下一次配置变更时加载。
- 缺失的文件会被跳过。无法获取的 URL 也会被跳过，或者保留其上次获取的内容。
- 在 `OPENCODE_DISABLE_PROJECT_CONFIG=1` 下，或当工作区位于项目之外时，相对条目会相对于全局配置目录解析。

已连接的 [OpenCode Console](../console/index.md) 工作区也可以共享指令。

关于配置位置和优先级，请参阅[配置](../config/index.md)。
