---
source_url: https://openspec.dev/docs/schemas/schema-yaml
source_hash: sha256:55334e14e1271e9f13de4e1b01078a00c73652c793770b371f79f70e91b3c44f
translated_at: 2026-11-13T09:48:42+08:00
translation_version: 1
---

# schema.yaml

`schema.yaml` 列出工作流创建的规划文件。它还定义这些文件的顺序以及到实现的交接。

## 位置 [#location]

项目模式位于 `openspec/schemas/<name>/` 下：

```text
openspec/schemas/review-first/
├── schema.yaml
└── templates/
    ├── proposal.md
    └── tasks.md
```

OpenSpec 会在这三处查找该目录，先匹配到的生效。

| 副本来源 | 目录 |
|---|---|
| **1. 项目** | `<project>/openspec/schemas/<name>/` |
| **2. 用户级，macOS 与 Linux** | `~/.local/share/openspec/schemas/<name>/` |
| **2. 用户级，Windows** | `%LOCALAPPDATA%\openspec\schemas\<name>\` |
| **3. 安装包** | 随 CLI 一起安装的模式 |

如果设置了 `XDG_DATA_HOME`，用户级目录在所有平台上都会移到 `$XDG_DATA_HOME/openspec/schemas/<name>/`。

目录名就是查找键，`--schema`、`config.yaml` 和 [`.openspec.yaml`](../configuration/change-metadata.md#schema) 都用它来查找。如果 `name` 字段与目录名不同，OpenSpec 仍按目录名查找。

[`openspec schema which <name>`](../cli.md#openspec-schema-which) 会打印当前生效的目录，以及它所遮蔽的低优先级副本。

## 顶层字段 [#top-level-fields]

| 字段 | 约定 |
|---|---|
| `name` | **必填。** 非空字符串，作为模式名存储。查找仍使用目录名。 |
| `version` | **必填。** 正整数，作为模式修订号存储。该值不改变 OpenSpec 的行为。 |
| `description` | 可选字符串，由 `openspec schemas` 打印。没有值时，该模式没有描述。 |
| `artifacts` | **必填。** 非空的[产物条目](#artifact-fields)列表。 |
| `apply` | 可选的 [apply 设置](#apply-fields)。没有该块时，OpenSpec 使用 [apply 默认值](#apply-defaults)。 |

## 产物字段 [#artifact-fields]

`artifacts` 下的每个条目定义一个规划文件或一组文件。

| 字段 | 约定 |
|---|---|
| `id` | **必填。** 唯一的非空字符串，用于依赖、项目规则、命令和 apply 设置。 |
| `generates` | **必填。** 相对路径或 glob，告诉智能体把产物写到变更文件夹内的什么位置。 |
| `description` | **必填。** 一个字符串，用于在发送给智能体的指令中标识该产物。 |
| `template` | **必填。** 相对路径，指向模式 `templates/` 文件夹中该产物的格式。 |
| `instruction` | 可选说明，告诉智能体应产出什么内容。 |
| `requires` | 必须先完成的产物 ID 列表。默认值：`[]`。 |

### `generates` [#generates]

路径从变更文件夹开始。对于名为 `add-auth` 的变更：

```yaml
generates: proposal.md
```

产物会写到这里：

```text
openspec/changes/add-auth/proposal.md
```

glob 可以匹配多个文件：

```yaml
generates: specs/**/*.md
```

这会匹配 `openspec/changes/add-auth/specs/` 下的 Markdown 文件。

OpenSpec 在 `generates` 中识别以下 glob 形式：

- **通配符与字符类**：包含 `*`、`?` 或 `[` 的值，例如 `specs/**/*.md` 和 `review-[ab].md`。
- **花括号展开**：如 `review-{api,ui}.md` 这样的备选，以及 `file-{1..3}.md` 这样的范围。
- **扩展 glob（Extglob）**：如 `@(proposal|design).md`、`+(proposal|design).md` 和 `!(proposal|design).md` 这样的模式。

**字面文件名**：只有开头一个 `!` 并不构成 glob。要指定该文件名，请使用 `generates: '!review.md'`。像 `(proposal|design).md` 这样的普通圆括号，以及 `review-{api}.md` 这样的单元素花括号，也仍然按字面处理。

OpenSpec 会拒绝绝对路径、包含 `..` 段的路径，以及花括号或圆括号嵌套超过 16 层的 glob，例如 `{a,{b,{c,...}}}`。实际模式只需一到两层。它还会拒绝展开后模式数超过 1,024 的 glob，例如重复十一次的 `{a,b}`，或像 `file-{1..5000}.md` 这样的范围。错误信息为 `Artifact output pattern expands to more than 1024 patterns`。实际模式只会展开出少数几个。

#### 完成判定 [#completion]

OpenSpec 检查输出是否存在。它不读取文件内容来判断产物是否完成。

| `generates` 值 | 视为完成的条件 |
|---|---|
| `proposal.md` | 该文件存在。 |
| `specs/**/*.md` | glob 至少匹配一个文件。 |

### `template` [#template]

路径从模式的 `templates/` 文件夹开始。在 `review-first` 模式中：

```yaml
template: proposal.md
```

OpenSpec 读取该文件：

```text
openspec/schemas/review-first/templates/proposal.md
```

OpenSpec 把模板内容作为输出格式交给智能体。它不会把模板复制到变更文件夹中。

OpenSpec 会拒绝绝对路径和包含 `..` 段的路径。

### `requires` [#requires]

- **依赖**：`requires` 中的每个 ID 都必须指向同一模式中的另一个产物。
- **就绪状态**：产物的所有依赖都完成后，它才变为就绪。
- **无效依赖图**：缺失的 ID、重复的 ID 和依赖环都会导致校验失败。
- **并列**：当多个产物都就绪时，它们在 `artifacts` 中的顺序决定 OpenSpec 先返回哪一个。

## `apply` 字段 [#apply-fields]

`apply` 定义实现开始前必须存在什么。

| 字段 | 约定 |
|---|---|
| `requires` | **必填。** 非空的产物列表，这些产物必须在 `apply` 指令就绪前存在。 |
| `tracks` | 可选的相对路径或 glob，指向变更文件夹中的 Markdown 任务文件。默认值：`null`。 |
| `instruction` | 可选说明，在 `apply` 就绪时发送给智能体。默认使用 OpenSpec 内置说明。 |

产物的 `requires` 控制规划顺序。`apply.requires` 控制 `apply` 指令何时就绪。

### `tracks` [#tracks]

路径从变更文件夹开始。对于名为 `add-auth` 的变更，`tracks: tasks.md` 读取：

```text
openspec/changes/add-auth/tasks.md
```

像 `tracks: "**/tasks.md"` 这样的 glob 会读取所有匹配文件，例如 `backend/tasks.md` 和 `frontend/tasks.md`。OpenSpec 会合并它们的任务与进度。产物的 `generates` 字段应使用同一个值，这样状态和列表跟踪的是同一批文件。`generates` 的花括号限制（嵌套 16 层、展开 1,024 个模式）在这里同样适用。

如果没有文件匹配，或匹配的文件中没有任何带任务文本的复选框，实施会一直处于阻塞状态。OpenSpec 会把这些复选框形式计入：

```markdown
- [ ] Pending task
- [x] Completed task
* [X] Completed task
+ [ ] Pending task
1. [ ] Pending task
2) [x] Completed task
```

任何 Markdown 列表标记都可以：`-`、`*`、`+`，或最多九位数字后跟 `.` 或 `)`。允许前导空格。任务文本可以折行到下面的行。OpenSpec 会把折行内容当作任务的一部分读取，直到空行、标题、代码围栏或另一个列表项为止。spec-driven 页面的 [tasks.md 小节](./spec-driven.md#tasksmd)定义了默认模式产出的更严格格式。

被跟踪的文件决定实施状态：

- **`blocked`**：没有文件匹配，或没有任何可读文件包含带任务文本的复选框。
- **`ready`**：至少有一个任务待完成，或某个匹配文件无法读取而另一个文件提供了任务。
- **`all_done`**：所有被跟踪的任务都已勾选，且所有匹配文件都已读取。

如果某个匹配文件无法读取，实施会保留可读文件中的任务与进度，但不会把该变更标记为 `all_done`。[`apply` JSON 输出](../cli.md#openspec-instructions)会指出每个不可用的文件及原因。

OpenSpec 会拒绝绝对路径和包含 `..` 段的路径。

### `apply` 默认值 [#apply-defaults]

| 行为 | 默认值 |
|---|---|
| 必需产物 | 模式中的每个产物 |
| 进度跟踪 | 不跟踪文件 |
| 智能体说明 | 内置 apply 说明 |

## 完整示例 [#complete-example]

```yaml
name: review-first
version: 1
description: Proposal and implementation checklist

artifacts:
  - id: proposal
    generates: proposal.md
    description: Why the change is needed and what it affects
    template: proposal.md
    instruction: |
      Explain the problem, the proposed change, and its impact.
    requires: []

  - id: tasks
    generates: tasks.md
    description: Trackable implementation checklist
    template: tasks.md
    instruction: |
      Break the approved proposal into ordered implementation tasks.
    requires:
      - proposal

apply:
  requires:
    - tasks
  tracks: tasks.md
  instruction: |
    Work through the pending tasks and mark each one complete.
```

## 校验 [#validation]

[`openspec schema validate <name>`](../cli.md#openspec-schema-validate) 会检查：

- 字段类型与必填字段
- 相对路径
- 产物 ID、依赖与依赖环
- `apply.requires` 中的 ID：每一个都必须是该模式中的产物
- 模板文件

如果某个模式的 `apply.requires` 含未知 ID，该模式不会加载，因此每个用到它的命令都会报出这个错误。

当 `apply.tracks` 与某个产物的 `generates` 值不完全相等时，校验会给出警告但不会失败。OpenSpec 通过比较这两个字符串来找到被跟踪的产物，因此其他任何值都会让它无法判断该文件属于哪个产物的进度。这包括像 `task.md` 这样的笔误，也包括 `tracks: tasks/main.md` 与 `generates: tasks/*.md` 不匹配的情况——尽管 glob 确实会产出该文件，但两个字符串仍然不同。无论哪种情况，apply 都会继续读取该文件，但 `openspec list` 和 `openspec status` 统计的是 `tasks.md`。

校验不会发现以下错误：

| 错误 | 结果 |
|---|---|
| 字段拼错，例如 `instrution` | OpenSpec 会忽略它。校验不会报告该笔误。 |
| `name` 与模式目录名不同 | 校验通过。OpenSpec 仍按目录名查找。 |
