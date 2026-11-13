---
source_url: https://openspec.dev/docs/cli
source_hash: sha256:9852474beab52bac9b6afbd29fca866b718fa415b85d7b5e80afcdd39653ac13
translated_at: 2026-11-13T09:48:42+08:00
translation_version: 1
---

# CLI

## 命令 [#commands]

**初始设置**

| 命令 | 作用 |
|---|---|
| [`openspec init`](#openspec-init) | 在项目中初始化 OpenSpec。 |
| [`openspec update`](#openspec-update) | 更新 OpenSpec 已安装的指令文件。 |
| [`openspec config`](#openspec-config) | 查看和修改全局配置。 |

**变更与规格**

| 命令 | 作用 |
|---|---|
| [`openspec list`](#openspec-list) | 列出变更；加上 `--specs` 则列出规格。 |
| [`openspec show`](#openspec-show) | 以 markdown 或 JSON 形式输出变更或规格。 |
| [`openspec view`](#openspec-view) | 单屏展示规格与变更的仪表盘。 |
| [`openspec validate`](#openspec-validate) | 检查变更与规格的结构问题。 |
| [`openspec archive`](#openspec-archive) | 把已完成的变更移到归档并更新主规格。 |

**工作流与模式**

其中大部分由你的智能体在工作流中运行。

| 命令 | 作用 |
|---|---|
| [`openspec new`](#openspec-new) | 创建新的变更目录。 |
| [`openspec status`](#openspec-status) | 单个变更或所有活跃变更的产物完成状态。 |
| [`openspec instructions`](#openspec-instructions) | 创建产物、实施或归档的指令。 |
| [`openspec templates`](#openspec-templates) | 模式各产物解析后的模板路径。 |
| [`openspec schemas`](#openspec-schemas) | 列出可用的工作流模式。 |
| [`openspec schema`](#openspec-schema) | 检查、派生或创建模式（实验性）。 |

**多仓库（beta）**

| 命令 | 作用 |
|---|---|
| [`openspec store`](#openspec-store) | 创建和管理存储库：注册在本机上的独立 OpenSpec 仓库。 |
| [`openspec doctor`](#openspec-doctor) | 报告解析出的 OpenSpec 根目录的关系健康状况。 |
| [`openspec context`](#openspec-context) | 输出解析出的 OpenSpec 根目录的工作上下文。 |
| [`openspec workset`](#openspec-workset) | 组合、保存并打开个人工作视图。 |

**实用工具**

| 命令 | 作用 |
|---|---|
| [`openspec version`](#openspec-version) | 报告已安装的版本，并可选地检查更新。 |
| [`openspec install`](#openspec-install) | 安装独立的 `openspec`，它无需 Node.js 即可运行。 |
| [`openspec feedback`](#openspec-feedback) | 提交关于 OpenSpec 的反馈。 |
| [`openspec completion`](#openspec-completion) | 安装或生成 shell 补全。 |

**已弃用**

| 命令 | 作用 |
|---|---|
| [`openspec change`](#openspec-change) | 变更的 show、list 和 validate 的名词形式。CLI 会给出警告并指向动词优先的命令。 |
| [`openspec spec`](#openspec-spec) | 规格的 show、list 和 validate 的名词形式，警告相同。 |

每个命令都接受 `-h, --help`。裸 `openspec` 命令还接受：

- `-V, --version`：打印 CLI 版本。
- `--no-color`：禁用彩色输出。

## openspec init [#openspec-init]

在项目中初始化 OpenSpec。

```bash
openspec init                        # current directory, interactive tool picker
openspec init --tools claude,cursor  # set up specific tools, no prompts
openspec init --tools none           # openspec/ structure only, no tool files
```

不带 `--tools` 时，init 会在交互式终端中提示你挑选工具。在非交互式终端中，它会配置在项目里检测到的工具。若一个都没检测到，则以退出码 1 结束并列出有效的 id。

**仅作为存储库的仓库**

当 `openspec/config.yaml` 中包含 `store:` 行，且仓库没有本地规格或变更时，从仓库根目录运行 init：

```bash
# install Claude Code integration files in the code repo
openspec init --tools claude
```

- **集成文件**：写在代码仓库中。
- **`openspec/config.yaml`**：逐字节保留。
- **`openspec/specs/` 和 `openspec/changes/`**：不在代码仓库中创建。

从子目录运行 init 会以退出码 1 结束，并提示你从仓库根目录运行。`--language` 同样以退出码 1 结束，因为语言属于外部存储库的配置。请在存储库根目录运行 init，或直接编辑该配置。

**参数**

| 参数 | 说明 |
|---|---|
| `path` | 要初始化的项目目录。默认：当前目录。不存在时会创建。 |

**选项**

| 选项 | 作用 |
|---|---|
| `--tools <tools>` | 逗号分隔的工具 id、`all` 或 `none`。跳过选择器。id 列在[支持的工具](./supported-tools.md)中。 |
| `--language <language>` | 向新建的项目配置添加语言指令。当仓库的 `store:` 行指向外部存储库时被拒绝。 |
| `--force` | 不经询问即删除旧版 OpenSpec 布局中的文件。否则交互式运行会先确认清理。 |
| `--profile <profile>` | 为本次运行覆盖全局配置中的配置档：`core`（标准工作流集合）或 `custom`（保存在全局配置中的工作流）。 |
| `--no-animation` | 显示静态欢迎界面，而非动画界面。 |

**输出**

OpenSpec 只写一次技能，写到 `.agents/skills/`。需要这些技能的工具会在自己的文件夹中获得链接。MiniMax Code 则得到自己的副本，位于 `~/.minimax/skills/`：

```
▌ OpenSpec structure created
✔ Setup complete for Claude Code

OpenSpec Setup Complete

Created: Claude Code
6 skills in .agents/skills/ (linked from .claude/skills/)
Config: openspec/config.yaml (schema: spec-driven)

Getting started:
  Start your first change: /openspec-propose "your idea"
```

`--tools none` 只创建 `openspec/config.yaml`。在已初始化的项目上，init 会就地重写已安装的文件，摘要显示 `Refreshed: Claude Code` 和 `Config: openspec/config.yaml (exists)`。

**退出码**

- `0`：设置完成。
- `1`：`--tools` 或 `--profile` 值无效、非交互式运行未检测到工具且没有 `--tools`，或仅存储库的调用无效。

## openspec update [#openspec-update]

更新 OpenSpec 已安装的指令文件。

```bash
openspec update             # refresh tools whose files are older than the CLI
openspec update --force     # rewrite files even when they're current
openspec update --dry-run   # list what an update would change, and change nothing
```

update 会找出 init 配置过的工具，并将其生成的文件与 CLI 的版本比对。若存在更新的 OpenSpec 版本，它会先提出升级 CLI，然后用升级后的版本重新运行。设置 `OPENSPEC_NO_UPDATE_CHECK=1` 可跳过该检查。

**参数**

| 参数 | 说明 |
|---|---|
| `path` | 要更新的项目目录。默认：当前目录。 |

**选项**

| 选项 | 作用 |
|---|---|
| `--force` | 即使已是最新，也重写每个已配置工具的文件。 |
| `--dry-run` | 报告本次更新将新增、修改或删除的每个文件，但不写入任何内容。不做 CLI 升级检查，也没有提示。与 `--force` 组合可预览强制更新。 |
| `--json` | 配合 `--dry-run` 时，以 JSON 打印计划。不带 `--dry-run` 时以退出码 1 结束。 |

**预览更新**

`--dry-run` 按非交互式运行会做出的更新来规划：走同一代码路径，但记录而非执行每一次写入和删除。真实更新会触及的每个文件都会被列出，包括：

- 把 OpenSpec 文件从工具的旧目录移出（`.kimi/` 移到 `.kimi-code/`，`.windsurf/` 移到 `.devin/`，`.codex/` 和 `.agent/` 移到 `.agents/`）；
- 在早于配置档的安装首次获得全局配置时保存该配置；
- 同步 GitHub Copilot 云端智能体文件；
- 配合 `--force` 时，配置仅出现在旧版产物中的工具并清理这些产物，包括已停用的全局 Codex 提示词。

```bash
openspec update --dry-run
```

```
2 file(s) would change:
  update  .agents/skills/openspec-propose/SKILL.md  (openspec)
  add     ~/.config/openspec/config.json  (openspec)
```

`--dry-run --json` 以单个 JSON 文档打印同样的计划：

```json
{
  "changes": [
    { "path": ".agents/skills/openspec-propose/SKILL.md", "action": "update", "tool": "openspec" },
    { "path": "~/.config/openspec/config.json", "action": "add", "tool": "openspec" }
  ],
  "notes": [],
  "failures": []
}
```

| 字段 | 内容 |
|---|---|
| `changes[].path` | 相对于项目的路径。项目之外的文件（例如全局技能或全局配置）从主目录起显示为 `~/...`；若也在主目录之外，则显示为绝对路径。 |
| `changes[].action` | `add`、`update` 或 `delete`。新字节与旧字节相同的文件不列出。 |
| `changes[].tool` | 文件所属的已配置工具，例如 `claude`。不属于单一工具的文件为 `openspec`：`.agents/skills/` 中的共享技能、全局配置，以及旧版产物清理。 |
| `notes[]` | `{ code, message }`，对应终端用户会被询问或被警告的某个步骤。`legacy-tool-directories`：交互式运行会先询问的移动；`changes` 会把它记为已执行。`legacy-artifacts`：发现了来自 OpenSpec 旧版布局的文件，例如 `openspec-proposal.md` 斜杠命令或 `AGENTS.md` 中的 OpenSpec 标记块。不带 `--force` 时，非交互式更新不会动它们，`changes` 也不记录；`--dry-run --force` 会列出它们的清理。`edited-skills`：update 将替换你在它安装的某个技能内所做的修改，消息会指明这些文件。普通刷新时为空。 |
| `failures[]` | `{ tool, error }`，对应真实更新会失败的每个工具，包括它无法完成的写入：本该是文件的位置是目录、本该是目录的位置是文件，或文件或文件夹没有写权限。对该工具，`changes` 在真实更新停止的地方停止；其他工具仍会被规划。只有在写入时磁盘才会报告的错误（例如空间不足）无法预见。 |

规划之前就失败（例如没有 OpenSpec 目录）时，仍会只打印一个 JSON 文档：空计划加上一个 `status` 数组，其中包含 `severity`、`code`（`update_error`）和 `message`。退出码为 1。

**输出**

当每个工具的文件都与 CLI 版本一致时：

```
✓ All 1 tool(s) up to date (v1.7.0)
  Tools: claude

Use --force to refresh files anyway.
```

当某工具的文件来自较旧的 CLI 时（或使用 `--force` 时，此时改为打印 `Force updating 1 tool(s): claude`）：

```
Updating 1 tool(s): claude (1.6.0 → 1.7.0)

✔ Updated Claude Code

✓ Updated: Claude Code (v1.7.0)
Tools: Claude Code
```

涉及基于 IDE 的工具（例如 Cursor 或 Kiro）的更新以 `Restart your IDE to refresh skills.` 结尾。

在没有 OpenSpec 的目录中，update 会拒绝执行：

```
✖ Error: No OpenSpec directory found. Run 'openspec init' first.
```

**退出码**

- `0`：文件已更新，或一切已是最新。
- `1`：该路径下没有 OpenSpec 目录，或更新失败。

## openspec config [#openspec-config]

查看和修改全局配置。

```bash
openspec config list                  # see current settings
openspec config set profile core      # change one value
openspec config profile               # interactive workflow picker
```

| 子命令 | 作用 |
|---|---|
| `path` | 打印配置文件位置。 |
| `list` | 显示所有当前设置。 |
| `get <key>` | 打印单个值，原始形式，便于脚本使用。 |
| `set <key> <value>` | 设置一个值，并强制转换其类型。 |
| `unset <key>` | 删除某个键，使其默认值生效。 |
| `reset` | 把所有配置重置为默认值。 |
| `edit` | 在 `$EDITOR` 中打开配置文件。 |
| `profile [preset]` | 配置安装哪些工作流。 |

配置是整机全局的，以 JSON 存储在 `config path` 指向的位置：若该环境变量已设置，则为 `$XDG_CONFIG_HOME/openspec/config.json`，否则为 `~/.config/openspec/config.json`（macOS、Linux）或 `%APPDATA%\openspec\config.json`（Windows）。每个子命令都接受 `--scope <scope>`，但目前只有 `global` 有效。其他任何范围都会以退出码 1 结束，并提示 `Error: Project-local config is not yet implemented`。

### openspec config path [#openspec-config-path]

```bash
openspec config path
```

```
/Users/you/.config/openspec/config.json
```

### openspec config list [#openspec-config-list]

```bash
openspec config list          # readable settings plus profile summary
openspec config list --json   # raw config as JSON
```

**选项**

| 选项 | 作用 |
|---|---|
| `--json` | 以 JSON 打印配置对象。 |

**输出**

先是各项设置，然后是配置档摘要。它会标明配置档是显式设置还是默认值，并把 `delivery` 标记为已停用：

```
featureFlags: {}
profile: core
delivery: skills

Profile settings:
  profile: core (default)
  delivery: skills (retired in 2.0, ignored)
  workflows: propose, explore, apply, update, sync, archive (from core profile)
```

### openspec config get [#openspec-config-get]

```bash
openspec config get profile
```

**参数**

| 参数 | 说明 |
|---|---|
| `key` | 要读取的键。用点号可访问嵌套值（`featureFlags.workspaces`）。 |

**输出**

裸值，可直接用于脚本。对象以紧凑 JSON 打印：

```
core
```

**退出码**

- `0`：已打印值。
- `1`：该键没有值，且不打印任何内容。

### openspec config set [#openspec-config-set]

```bash
openspec config set profile core
openspec config set featureFlags.workspaces true
```

**参数**

| 参数 | 说明 |
|---|---|
| `key` | 要写入的键，嵌套值用点号。 |
| `value` | 新值。`true`/`false` 会转为布尔值，数字字符串会转为数字。 |

**选项**

| 选项 | 作用 |
|---|---|
| `--string` | 把值存为字符串，跳过类型转换。 |
| `--allow-unknown` | 允许模式不认识的键。 |

**输出**

```
Set featureFlags.workspaces = true
```

`delivery` 仍被接受，因此旧脚本还能用，但它不再改变任何东西（[升级到 2.0](./upgrade-to-2.md)）：

```
Set delivery = "skills"
Note: delivery no longer changes anything; OpenSpec 2.0 installs skills only.
```

未知的键和无效的值会在保存任何内容之前以退出码 1 失败：

```
Error: Invalid configuration key "bogus.key". Unknown top-level key "bogus".
Use "openspec config list" to see available keys.
Pass --allow-unknown to bypass this check.
```

```
Error: Invalid configuration - profile: Invalid option: expected one of "core"|"custom"
```

如果配置文件存在但不包含 JSON 对象——无论是完全不是有效 JSON，还是其根是 `null` 或数组之类的东西——`config set`、`config unset` 和 `config profile` 都会以退出码 1 结束并保持文件不变。用 `openspec config edit` 修复它，或用 `openspec config reset --all` 替换它：

```
Error: /home/you/.config/openspec/config.json could not be parsed, so it was left unchanged.
Fix it with "openspec config edit", or reset it with "openspec config reset --all".
```

在修复之前，遥测和 `openspec update` 中的后台更新检查会保持关闭。显式的 `openspec version --check` 仍会运行。

### openspec config unset [#openspec-config-unset]

```bash
openspec config unset profile
```

删除该键，使默认值重新生效。带内置默认值的键始终算作已设置，所以即使你从未设置过，这里也会报告成功：

```
Unset profile (reverted to default)
```

完全没有值的键会打印 `Key "featureFlags.nothere" was not set`。两种情况退出码都是 0。无法解析的配置文件则以退出码 1 结束，与 `config set` 相同。

### openspec config reset [#openspec-config-reset]

```bash
openspec config reset --all      # asks for confirmation
openspec config reset --all -y   # no prompt
```

**选项**

| 选项 | 作用 |
|---|---|
| `--all` | 必需。重置所有内容。 |
| `-y, --yes` | 跳过确认提示。 |

**输出**

```
Configuration reset to defaults
```

不带 `--all` 时以退出码 1 结束，并打印用法行。

**退出码**

- `0`：重置完成，或你在提示处回答了否。
- `1`：缺少 `--all`。
- `130`：提示被 Ctrl-C 取消。

### openspec config edit [#openspec-config-edit]

```bash
openspec config edit
```

在 `$EDITOR` 中打开配置文件（回退到 `$VISUAL`），若文件不存在则先用默认值创建。编辑器关闭后会校验该文件。无效的 JSON 或无效配置会以退出码 1 结束。

编辑器值可以带参数和引号路径，例如 `code --wait` 或 `"/Applications/Sublime Text.app/Contents/SharedSupport/bin/subl" -w`。它不经 shell 而按词切分，因此 `$VAR`、`~` 和 `;` 都按字面传递。无法启动或退出码非零的编辑器会打印一行错误并以退出码 1 结束。

未配置编辑器时以退出码 1 结束：

```
Error: No editor configured
Set the EDITOR or VISUAL environment variable to your preferred editor
Example: export EDITOR=vim
```

### openspec config profile [#openspec-config-profile]

```bash
openspec config profile        # interactive picker (needs a terminal)
openspec config profile core   # apply the core preset directly
```

**参数**

| 参数 | 说明 |
|---|---|
| `preset` | 可选的预设名称。只存在 `core`。它会选中核心工作流。 |

不带预设时，交互式选择器会显示你当前的工作流，允许你修改它们（复选列表），打印差异，并在 OpenSpec 项目内主动提出为你运行 `openspec update`。在非终端环境中以退出码 1 结束：

```
Interactive mode required. Use `openspec config profile core` or set config via environment/flags.
```

**输出**

修改后的配置要等项目更新后才会生效：

```
Config updated. Run `openspec update` in your projects to apply.
```

**退出码**

- `0`：配置档已保存，或你保留了当前设置。
- `1`：未知预设、无终端，或提出运行的 `openspec update` 失败。
- `130`：选择器被 Ctrl-C 取消。

## openspec list [#openspec-list]

列出变更；加上 `--specs` 则列出规格。

```bash
openspec list                    # active changes, most recently modified first
openspec list --archived         # archived changes
openspec list --all              # active and archived changes
openspec list --specs            # specs with requirement counts
openspec list --json             # machine-readable, includes the resolved root
```

各行来自解析出的根目录下的 `openspec/changes/` 和 `openspec/specs/`。默认的变更列表会跳过 `openspec/changes/archive/`。

**选项**

| 选项 | 作用 |
|---|---|
| `--specs` | 列出规格而非变更。 |
| `--changes` | 列出变更。这是默认行为。 |
| `--archived` | 只列出已归档的变更。不能与 `--specs` 组合。 |
| `--all` | 列出活跃和已归档的变更。不能与 `--specs` 组合。优先于 `--archived`。 |
| `--sort <order>` | `recent`（最近修改优先）或 `name`。默认：`recent`。规格始终按名称排序。 |
| `--json` | 打印 JSON 而非表格。 |
| `--store <id>` | 使用已注册的存储库作为 OpenSpec 根目录，而非当前项目。 |

**输出**

每个变更一行：名称、任务状态、最后修改时间。状态列会显示 `No tasks`、`2/5 tasks` 或 `✓ Complete`。

```
Changes:
  add-rate-limit     No tasks      just now
```

`--all` 把活跃和已归档的变更分组到不同标题下。每组使用选定的排序方式：

```
Changes:
  add-rate-limit     No tasks      just now

Archived Changes:
  2026-08-10-add-login     ✓ Complete    2d ago
```

```
Specs:
  api     requirements 1
```

`--json` 会添加任务计数，以及取值为 `no-tasks`、`in-progress` 或 `complete` 的 `status`：

```json
{
  "changes": [
    {
      "name": "add-rate-limit",
      "completedTasks": 0,
      "totalTasks": 0,
      "lastModified": "2026-08-11T13:44:40.171Z",
      "status": "no-tasks"
    }
  ],
  "root": {
    "path": "/Users/you/projects/my-app",
    "source": "nearest"
  }
}
```

使用 `--archived` 或 `--all` 时，每个变更对象都包含 `archived` 布尔值。合并后的数组使用选定的排序方式。当已归档变更受跟踪的任务文件中有未勾选的任务时，它仍可能具有 `in-progress` 状态。不带这两个选项时，JSON 形状保持不变。

空列表会打印 `No active changes found.`、`No archived changes found.`、`No changes found.` 或 `No specs found.`，退出码仍为 0。

变更是 `openspec/changes/` 下直接一层的目录。与规格不同，变更不能嵌套在命名空间文件夹中。像 `changes/mobile/` 这样只包着一个变更（`changes/mobile/refresh-token/`）的文件夹，会以状态 `not a change` 列出，随后是一条警告，指明其中的嵌套目录。`--json` 会用 `nested` 数组标记该条目，并添加一个顶层 `warnings` 数组。`show`、`status`、`validate` 和 `archive` 会以同样的消息拒绝该文件夹。要修复它，把变更上移，并把命名空间并入其名称：

```bash
mv openspec/changes/mobile/refresh-token openspec/changes/mobile-refresh-token
rmdir openspec/changes/mobile
```

**退出码**

- `0`：已打印列表，即使为空。
- `1`：未找到 OpenSpec 根目录（在项目之外且没有 `--store`）。

## openspec show [#openspec-show]

以 markdown 或 JSON 形式输出变更或规格。

```bash
openspec show add-rate-limit              # change: prints proposal.md
openspec show add-rate-limit --diff       # change: append requirement diffs
openspec show api                         # spec: prints spec.md
openspec show api --json --no-scenarios   # spec JSON without scenario text
```

不带名称时，show 会询问要变更还是规格，然后列出可挑选的条目。在非交互式终端中，它以退出码 1 结束，改为打印直接形式。

**参数**

| 参数 | 说明 |
|---|---|
| `item-name` | 要显示的变更或规格，用文件夹名（`add-rate-limit`、`api`）。 |

**选项**

| 选项 | 作用 |
|---|---|
| `--json` | 打印结构化 JSON 而非原始 markdown。 |
| `--type <change\|spec>` | 当变更和规格同名时指定类型。 |
| `--no-interactive` | 绝不提示：缺少名称即报错。 |
| `--deltas-only` | JSON、变更：把输出限制为增量。变更 JSON 本就只含增量，因此输出与单纯的 `--json` 相同。 |
| `--requirements-only` | `--deltas-only` 的已弃用别名。在 stderr 上给出警告。 |
| `--diff` | 变更：追加每个需求的增量差异。对规格则忽略并给出警告。 |
| `--requirements` | JSON、规格：保留需求文本，清空 `scenarios` 数组。 |
| `--no-scenarios` | JSON、规格：输出与 `--requirements` 相同。 |
| `-r, --requirement <id>` | JSON、规格：按从 1 开始的位置输出单个需求。不能与 `--requirements` 组合。 |
| `--store <id>` | 使用已注册的存储库作为 OpenSpec 根目录，而非当前项目。 |

不适用于所解析类型的选项会被忽略，并在 stderr 上给出警告。

**输出**

文本模式是原始直通：变更打印其 `proposal.md`，规格打印其 `spec.md`。

```
# Add rate limiting

## Why
Unauthenticated clients can exhaust the API.

## What Changes
- Add per-client rate limiting to the public API.
```

对变更而言，`--diff` 先打印提案，然后是一个 `Specifications Changed (diffs)` 小节。ADDED 需求包含其全文。REMOVED 需求保留作者填写的 Reason 和 Migration。RENAMED 需求显示 FROM 和 TO。MODIFIED 需求显示与对应主需求的统一差异。

如果 MODIFIED 标题只有在折叠大小写或空白后才匹配，输出会同时包含差异和一条警告，说明归档匹配是精确匹配。如果主规格或需求缺失，输出会给出警告并打印完整的增量块。没有文本差异的 MODIFIED 块会打印 `(no textual changes)`。

带 `--json` 的变更是增量形状：

```json
{
  "id": "add-rate-limit",
  "title": "Add rate limiting",
  "deltaCount": 1,
  "deltas": [
    {
      "spec": "api",
      "operation": "ADDED",
      "description": "Add requirement: The API SHALL limit each client to 100 requests per minute.",
      "requirement": {
        "name": "Rate limit",
        "text": "The API SHALL limit each client to 100 requests per minute.",
        "scenarios": [
          {
            "name": "Client exceeds the limit",
            "rawText": "- **WHEN** a client sends its 101st request within a minute\n- **THEN** the API responds 429"
          }
        ]
      },
      ...
    }
  ],
  "root": {
    "path": "/Users/you/projects/my-app",
    "source": "nearest"
  }
}
```

每个需求带有其 `name`，即 `Requirement:` 之后的标题文本。归档就是用这个名称匹配 MODIFIED、REMOVED 和 RENAMED 条目。每个场景带有其 `name`，即 `Scenario:` 之后的标题文本。两个标题末尾连续的 `#` 不属于名称。

`--json --diff` 保持这个顶层形状。MODIFIED 增量会增加一个 `diff` 字符串、一个 `warning` 字符串，或两者都有。其他操作不变。`diff` 字符串为空表示主块与增量块文本完全相同。

带 `--json` 的规格会列出其需求及场景。需求和场景带有与变更 JSON 相同的 `name` 字段：

```json
{
  "id": "api",
  "title": "api",
  "overview": "Public HTTP API behavior.",
  "requirementCount": 1,
  "requirements": [
    {
      "name": "Health endpoint",
      "text": "The API SHALL expose a health endpoint.",
      "scenarios": [
        {
          "name": "Health check succeeds",
          "rawText": "- **WHEN** a client requests GET /health\n- **THEN** the API responds 200"
        }
      ]
    }
  ],
  "metadata": {
    "version": "1.0.0",
    "format": "openspec"
  },
  "root": {
    "path": "/Users/you/projects/my-app",
    "source": "nearest"
  }
}
```

未知名称会给出近似匹配建议：`Unknown item 'does-not-exist'. Did you mean: add-rate-limit, api?`。同时匹配变更和规格的名称会报错并要求指定 `--type`。

**退出码**

- `0`：已打印条目。
- `1`：名称未知或有歧义、在终端之外没有给出名称、`-r` 索引越界、`--requirements` 与 `-r` 组合，或 `--diff` 时无法读取增量或主规格。

## openspec view [#openspec-view]

打印一屏规格与变更仪表盘。

```bash
openspec view   # project summary in one screen
```

view 打印一次仪表盘后退出，不读取任何按键。变更按任务进度分组：Draft（还没有任务）、Active（任务进行中，带进度条和百分比）、Completed（所有任务已勾选）。规格列出时带需求数，最多的在前。

**选项**

| 选项 | 作用 |
|---|---|
| `--store <id>` | 使用已注册的存储库作为 OpenSpec 根目录，而非当前项目。 |

**输出**

```
OpenSpec Dashboard

════════════════════════════════════════════════════════════
Summary:
  ● Specifications: 1 specs, 1 requirements
  ● Draft Changes: 1
  ● Active Changes: 0 in progress
  ● Completed Changes: 0

Draft Changes
────────────────────────────────────────────────────────────
  ○ add-rate-limit

Specifications
────────────────────────────────────────────────────────────
  ▪ api                            1 requirement

════════════════════════════════════════════════════════════

Use openspec list --changes or openspec list --specs for detailed views
```

当任何变更存在进行中的任务时，会出现一行 `Task Progress` 摘要。

每个活跃变更还会在其任务进度条下方显示其模式和产物状态：

```text
    └─ [spec-driven] proposal✓ specs→ design→ tasks✓
```

| 标记 | 产物状态 |
|---|---|
| `✓` | 其输出已存在。已存在的 tasks 产物即算完成，即使其清单尚未完成。 |
| `→` | 已就绪，可以创建。 |
| 无标记 | 因缺少依赖而受阻。 |
| `(skipped)` | 该变更跳过它。 |

如果工作流无法加载，view 会打印警告，并保持该变更的任务进度可见。运行 `openspec status --change <name>` 可单独检查该工作流。使用 `openspec view --store <id>` 之后，请给 status 传入相同的 `--store <id>`。

**退出码**

- `0`：已打印仪表盘。
- `1`：未找到 OpenSpec 根目录（在项目之外且没有 `--store`）。

## openspec validate [#openspec-validate]

检查变更与规格的结构问题。

```bash
openspec validate add-rate-limit   # one change or spec, by name
openspec validate --all            # every change and spec
```

不带名称也不带批量选项时，validate 会提示你挑选条目。在非交互式终端中，它以退出码 1 结束，改为打印批量选项。

**参数**

| 参数 | 说明 |
|---|---|
| `item-name` | 要校验的变更或规格，用文件夹名（`add-rate-limit`、`api`）。 |

**选项**

| 选项 | 作用 |
|---|---|
| `--all` | 校验所有变更和规格。 |
| `--changes` | 校验所有变更。 |
| `--specs` | 校验所有规格。 |
| `--archived` | 检查已归档变更的任务完成情况，但不校验其已应用的规格增量。 |
| `--strict` | 把警告视为失败。 |
| `--type <change\|spec>` | 当变更和规格同名时指定类型。 |
| `--json` | 打印结构化报告而非文本。 |
| `--report <mode>` | 批量输出：`full`（默认）或 `findings`。需要显式的批量范围。 |
| `--concurrency <n>` | 批量运行时的最大并行校验数。默认：`OPENSPEC_CONCURRENCY`，否则为 6。 |
| `--no-interactive` | 绝不提示：名称缺失或有歧义即报错。 |
| `--store <id>` | 使用已注册的存储库作为 OpenSpec 根目录，而非当前项目。 |

**输出**

批量运行会为每个条目打印一行状态，随后是任何发现项，最后是总计：

```
✓ change/add-rate-limit
✓ spec/api
Totals: 2 passed, 0 failed (2 items)
```

**任务复选框发现项**

进度只统计复选框，别的都不算，因此写成普通项目符号的任务文件会被读作零个任务：`openspec list` 和 `openspec status` 报告没有工作，`openspec archive` 也没有可标记为未完成的内容。validate 会对每个列出工作却没有复选框的受跟踪任务文件报告 `WARNING`：

```text
⚠ [WARNING] tasks.md: This change counts as 0 tasks: no line in its tracked task files is a checkbox, so "openspec list" and "openspec status" report no work and "openspec archive" has nothing to flag as incomplete. Write each task as "- [ ] 1.1 Description".
```

只有在变更的整个受跟踪集合中一个复选框都没有时，该警告才会触发。真实清单旁边有一个纯文字文件不会被报告；只要存在一个复选框，撰写中的变更就会保留其进度。`--strict` 会把该警告变成失败。行号在 `--json` 报告中。

围栏代码块、HTML 注释、YAML front matter 和缩进代码不会被扫描，因此粘贴的终端示例绝不会被误认为任务列表。

**归档合并发现项**

对变更而言，validate 会针对当前主规格运行归档的合并构建器，但不写入文件。它把合并冲突（例如缺少 `MODIFIED` 目标，或 `ADDED` 需求冲突）作为 `INFO` 报告：

```text
ℹ [INFO] api/spec.md: Archive would refuse this delta: api MODIFIED failed for header "### Requirement: Rate limiting" - not found
```

即使校验通过，这些发现项也会同时出现在文本和 JSON 输出中。`INFO` 从不改变退出码，在 `--strict` 下亦然：缺失的目标可能属于尚未归档的兄弟变更。已同步进主规格的增量遵循归档现有的合并规则。

该检查不会运行归档后续的合并规格校验或退役检查。报告干净并不保证归档一定成功。

如果合并预检无法启动，会有 `INFO` 发现项说明原因。已有的校验发现项和退出码保持不变。

失败的条目会列出每个问题和修复方式：

```
Change 'add-rate-limit' has issues
✗ [ERROR] api/spec.md: ADDED "Rate limiting" must include at least one scenario
Next steps:
  - Ensure change has deltas in specs/: use headers ## ADDED/MODIFIED/REMOVED/RENAMED Requirements
  - Each requirement MUST include at least one #### Scenario: block
  - Debug parsed deltas: openspec show add-rate-limit --json --deltas-only
```

`--json` 为整次运行打印一份报告：

```json
{
  "items": [
    {
      "id": "add-rate-limit",
      "type": "change",
      "valid": true,
      "issues": [],
      "durationMs": 2
    }
  ],
  "summary": {
    "totals": {
      "items": 1,
      "passed": 1,
      "failed": 0
    },
    "byType": {
      "change": {
        "items": 1,
        "passed": 1,
        "failed": 0
      }
    }
  },
  "version": "1.0",
  "root": {
    "path": "/Users/you/projects/my-app",
    "source": "nearest"
  }
}
```

`issues` 条目带有 `level`，取值为 `ERROR`、`WARNING` 或 `INFO`。

**退出码**

- `0`：所有校验的条目都通过，包括空的批量范围。
- `1`：某个条目失败、报告请求无效、`openspec/config.yaml` 无法读取或不是有效的 YAML，或本次运行失败（例如名称未知或没有 OpenSpec 根目录）。无法读取或解析的配置会在检查任何条目之前终止运行；带 `--json` 时，它会作为单个 `status` 条目报告，代码为 `unreadable_config` 或 `unparseable_config`。

### --report full|findings [#--report-fullfindings]

为显式的批量校验范围选择输出方式：

- **`full`**：所有条目。这是默认值。显式 `--report full` 保持既有输出形状，不添加报告元数据。
- **`findings`**：只含有问题的条目，包括带有警告或信息的通过条目。每个条目仍会被校验。总计、严格模式行为和退出码不变。

```bash
openspec validate --all --report findings
openspec validate --archived --report findings --json
```

**范围**

| 选项 | findings 报告中的 `report.scope` |
|---|---|
| `--all` | `all` |
| `--changes` | `changes` |
| `--specs` | `specs` |
| `--changes --specs`，或 `--all` 加其中任一选项 | `all` |
| `--archived` | `archived` |

两种显式报告模式都会拒绝位置参数式条目名称、缺少批量范围，以及归档范围与活跃范围组合。

#### 发现项文本输出 [#findings-text-output]

**人类可读输出**：stdout 打印 `Scope: <scope> (<count> items)`，然后是总计。当没有带问题的条目时：

```text
Scope: all (2 items)
No item findings.
Totals: 2 passed, 0 failed (2 items)
```

带问题的条目名称、严重级别标签、路径和消息会打印到 stderr。活跃范围的失败会在总计之后保留 `Details:` 重运行提示。既有的根横幅和进度输出可能出现在报告之前。

#### 发现项 JSON 输出 [#findings-json-output]

`--report findings --json` 打印一个文档。本例有两个干净条目：

```json
{
  "report": {
    "kind": "validation-findings",
    "version": "1.0",
    "scope": "all",
    "returnedItems": 0,
    "totalItems": 2
  },
  "itemFindings": [],
  "summary": {
    "totals": { "items": 2, "passed": 2, "failed": 0 },
    "byType": {
      "change": { "items": 1, "passed": 1, "failed": 0 },
      "spec": { "items": 1, "passed": 1, "failed": 0 }
    }
  },
  "root": { "path": "/Users/you/projects/my-app", "source": "nearest" }
}
```

- **`report.kind` 和 `report.version`**：标识 `validation-findings` 形状，版本为 `1.0`。没有顶层 `version` 或 `items`。
- **`report.returnedItems` 和 `report.totalItems`**：分别统计返回的记录数和所有被校验的条目数。
- **`itemFindings`**：`issues` 数组非空的完整条目记录。包含 `ERROR`、`WARNING` 和 `INFO` 问题。每条记录保留 `id`、`type`、`valid`、`issues` 和 `durationMs`。已归档条目使用 `type: "change"`。
- **`summary`**：整次运行的总计和按类型的计数，而非返回子集的计数。空范围的各项总计为零，退出码为 0。
- **`root`**：与完整报告相同的已选根目录元数据。

**记录保真**：返回的条目保持完整报告中的顺序，以及条目或问题上的任何附加字段。过滤不会重写消息或位置，包括可选的 `line` 和 `column` 字段。

**命令失败**：根目录选择或条目发现失败会保留既有的 `status` 诊断并以退出码 1 结束。它们不会返回已完成的发现项报告，也不会返回成功的空报告。

#### 无效的报告请求 [#invalid-report-requests]

两种显式报告模式都会在根目录选择或条目发现之前拒绝这些请求：

- 不支持的 report 值，包括空字符串。
- 位置参数式条目名称，即使同时给出了批量选项。
- 没有显式批量范围。
- `--archived` 与 `--all`、`--changes` 或 `--specs` 组合。

在 JSON 模式下，被拒绝的请求以退出码 1 结束，只带一个单元素 `status` 数组。它没有 `root` 或报告载荷：

```bash
openspec validate --all --report bogus --json
```

```json
{
  "status": [
    {
      "severity": "error",
      "code": "invalid_validation_report_request",
      "message": "Unknown validation report 'bogus'.",
      "fix": "Use --report full|findings with --all, --changes, --specs, or --archived, without an item name. Do not combine archived and active scopes."
    }
  ]
}
```

人类可读模式把错误打印到 stderr。不带值的裸 `--report` 会在 stderr 上产生 Commander 语法错误，带 `--json` 时也一样；它不使用这个诊断外壳。

#### 在外部过滤完整报告 [#filter-a-full-report-externally]

要得到自定义 JSON 视图，可用 `jq` 或 PowerShell 过滤完整报告。这些脚本示例会保留校验的退出码，并让命令错误文档保持原样。

在 Bash 中用 `jq`：

```bash
if validation_json=$(openspec validate --all --json); then
  validation_exit=0
else
  validation_exit=$?
fi
printf '%s\n' "$validation_json" |
  jq 'if has("items") then .items |= map(select(.issues | length > 0)) else . end'
exit "$validation_exit"
```

在 PowerShell 中：

```powershell
$validationJson = openspec validate --all --json
$validationExit = $LASTEXITCODE
$validationReport = $validationJson | ConvertFrom-Json
if ($validationReport.PSObject.Properties.Name -contains 'items') {
  $validationReport.items = @($validationReport.items | Where-Object { $_.issues.Count -gt 0 })
}
$validationReport | ConvertTo-Json -Depth 100
exit $validationExit
```

这些自定义视图保留完整报告的键，但省略干净条目。它们既不是完整的 full-v1 报告，也不是带版本的 `--report findings` 形状。

## openspec archive [#openspec-archive]

把已完成的变更移到归档并更新主规格。

```bash
openspec archive add-rate-limit -y                # archive one change, merge its deltas
openspec archive add-rate-limit -y --skip-specs   # archive without touching the specs
```

不带名称时，archive 会提示你挑选一个变更。在非交互式终端中，它以退出码 1 结束，改为打印重运行命令。

**参数**

| 参数 | 说明 |
|---|---|
| `change-name` | 要归档的变更，用文件夹名（`add-rate-limit`）。 |

**选项**

| 选项 | 作用 |
|---|---|
| `-y, --yes` | 对每个确认都回答是：规格更新、未完成任务、跳过校验。 |
| `--skip-specs` | 归档时不改动主规格（基础设施、工具或纯文档类变更）。 |
| `--no-validate` | 跳过校验。archive 会先要求你确认，`-y` 可代为确认。 |
| `--json` | 打印结构化结果而非文本。确认规格更新需要 `--yes`。 |
| `--store <id>` | 使用已注册的存储库作为 OpenSpec 根目录，而非当前项目。 |

**输出**

成功运行会报告任务状态，预览规格更新，应用它们，并给出归档文件夹：

```
Task status: ✓ Complete

Specs to update:
  api: update
Applying changes to openspec/specs/api/spec.md:
  + 1 added
Totals: + 1, ~ 0, - 0, → 0
Specs updated successfully.
Change 'add-rate-limit' archived as '2026-08-11-add-rate-limit'.
```

变更文件夹整体移到 `openspec/changes/archive/2026-08-11-add-rate-limit/`，名称前加上今天的日期。每个增量合并进其主规格：上面的 ADDED 需求被追加到 `openspec/specs/api/spec.md`。不带 `-y` 时，archive 会显示预览并在更新前询问。拒绝的话仍会归档该变更，但不动规格。

使用 `--json --yes` 时：

```json
{
  "archive": {
    "change": "add-rate-limit",
    "archivedAs": "2026-08-11-add-rate-limit",
    "path": "/Users/you/projects/my-app/openspec/changes/archive/2026-08-11-add-rate-limit",
    "specsUpdated": true,
    "totals": {
      "added": 1,
      "modified": 0,
      "removed": 0,
      "renamed": 0
    }
  },
  "root": {
    "path": "/Users/you/projects/my-app",
    "source": "nearest"
  }
}
```

archive 会先校验该变更，并拒绝未通过的变更：

```
Validation errors in change delta specs:
  ✗ ADDED "Rate limiting" must include at least one scenario

Validation failed. Please fix the errors before archiving.
To skip validation (not recommended), use --no-validate flag.
```

未完成的任务会给出警告但不阻止。交互式下 archive 会询问是否继续，`-y` 则自行继续：

```
Task status: 1/2 tasks
Warning: 1 incomplete task(s) found. Continuing due to --yes flag.
```

**退出码**

- `0`：变更已归档，无论是否有规格更新。
- `1`：校验失败、变更名称未知，或需要确认却读不到回答。

## openspec new [#openspec-new]

创建新的变更目录。

```bash
openspec new change add-caching                                # metadata only
openspec new change add-search --goal "Users can search docs"  # record a goal
```

`new` 有一个子命令 `new change <name>`。它创建 `openspec/changes/<name>/`，其中只有一个 [`.openspec.yaml` 元数据文件](./configuration/change-metadata.md)：

```yaml
schema: spec-driven
created: 2026-08-11
```

产物（proposal、specs、design、tasks）不在这里搭建。稍后由你编写，`openspec status` 会告诉你下一个是哪个。

**参数**

| 参数 | 说明 |
|---|---|
| `name` | 变更的文件夹名（`add-caching`）。 |

**选项**

| 选项 | 作用 |
|---|---|
| `--description <text>` | 同时在变更目录中创建一个包含该文本的 `README.md`。 |
| `--goal <text>` | 在 `.openspec.yaml` 中保存一行 `goal:`。 |
| `--schema <name>` | 该变更的工作流模式。默认：`spec-driven`，也是唯一随附的模式。 |
| `--json` | 以 JSON 打印创建的变更而非文本。 |
| `--store <id>` | 使用已注册的存储库作为 OpenSpec 根目录，而非当前项目。 |

**输出**

```
Created change 'add-caching' at openspec/changes/add-caching/
Schema: spec-driven
Next: openspec status --change add-caching
```

当未找到 `openspec/` 目录时，`new change` 会在你所在的位置创建一个，并说明这一点：

```
Created change 'add-caching' at openspec/changes/add-caching/
Schema: spec-driven
Next: openspec status --change add-caching

Note: no OpenSpec root was found here, so one was created at openspec/.
Run `openspec init` to finish setting this project up, or delete that directory if you meant a different project.
```

该提示与其余人类可读输出一起发到 stdout，带 `--json` 时绝不出现。

在已有 `openspec/` 的项目中使用 `--json` 时：

```json
{
  "change": {
    "id": "add-caching",
    "path": "/Users/you/projects/my-app/openspec/changes/add-caching",
    "metadataPath": "/Users/you/projects/my-app/openspec/changes/add-caching/.openspec.yaml",
    "schema": "spec-driven"
  },
  "root": {
    "path": "/Users/you/projects/my-app",
    "source": "nearest"
  }
}
```

当未找到 `openspec/` 目录且 `new change` 创建了一个时，JSON 形状相同。`root.path` 是你运行命令时所在的目录，`root.source` 为 `implicit`：

```json
"root": {
  "path": "/Users/you/projects/my-app",
  "source": "implicit"
}
```

**退出码**

- `0`：变更已创建。
- `1`：变更已存在，或模式未知。

## openspec status [#openspec-status]

报告单个变更或所有活跃变更的产物完成状态。

```bash
openspec status --change add-rate-limit          # checklist view
openspec status --change add-rate-limit --json   # structured report
openspec status --all                            # every active change
openspec status --all --json                     # one batch report
```

存在活跃变更时，必须且只能使用 `--change` 或 `--all` 之一。两者都不给时，status 会以退出码 1 结束并列出可用的变更，即使只有一个：

```text
✖ Error: Missing required option --change (or --all for every active change). Available changes:
  add-rate-limit
```

当项目没有活跃变更时，status 会打印 `No active changes. Create one with: openspec new change <name>`，即使两个选项都不给也以退出码 0 结束。使用 `--all --json` 时，同样的空状态为 `{ "changes": [], "message": "No active changes.", "root": ... }`。

**选项**

| 选项 | 作用 |
|---|---|
| `--change <id>` | 要报告的变更，用文件夹名。 |
| `--all` | 报告所有活跃变更，按名称排序。不能与 `--change` 组合。 |
| `--schema <name>` | 覆盖从 `openspec/config.yaml` 自动检测到的模式。未知名称会报错。 |
| `--json` | 打印结构化报告而非文本。 |
| `--store <id>` | 使用已注册的存储库作为 OpenSpec 根目录，而非当前项目。 |

**输出**

模式各产物的清单：`[x]` 已完成，`[ ]` 可以编写，`[-]` 在其依赖的产物存在之前受阻。

```
Change: add-rate-limit
Schema: spec-driven
Change root: /Users/you/projects/my-app/openspec/changes/add-rate-limit
Progress: 2/4 artifacts complete

[x] proposal
[x] specs
[ ] design
[-] tasks (blocked by: design)

Next: openspec instructions design --change "add-rate-limit" --json
```

`Next:` 行会给出推进该变更的那一条命令，因此在全新会话中仅凭 `openspec status` 就能重新接手一个变更。规划尚未完成时它给出下一个就绪的产物，当所有规划产物都存在时则给出 `openspec instructions apply`：

```
[x] proposal
[x] specs
[x] design
[x] tasks

All planning artifacts complete!
Next: openspec instructions apply --change "add-rate-limit" --json
```

解析出的根目录是存储库时，它会带上 `--store <id>`，并给出与 JSON 中 `nextSteps` 句子相同的命令。

`--json` 会添加每个产物的依赖、解析后的文件路径，以及建议的下一步。已截断：

```json
{
  "changeName": "add-rate-limit",
  "schemaName": "spec-driven",
  "isComplete": false,
  "nextSteps": [
    "Run openspec instructions design --change \"add-rate-limit\" --json before writing that artifact."
  ],
  "artifacts": [
    {
      "id": "proposal",
      "outputPath": "proposal.md",
      "status": "done",
      "requires": []
    },
    {
      "id": "design",
      "outputPath": "design.md",
      "status": "ready",
      "requires": [
        "proposal"
      ]
    },
    {
      "id": "tasks",
      "outputPath": "tasks.md",
      "status": "blocked",
      "requires": [
        "specs",
        "design"
      ],
      "missingDeps": [
        "design"
      ]
    }
  ]
}
```

使用 `--all --json` 时，`changes` 为每个变更包含相同的状态对象，但不含每个变更各自的 `root`。所选根目录在外层出现一次。本例截断了上面展示的每个变更的状态字段：

```json
{
  "changes": [
    {
      "changeName": "add-rate-limit",
      "schemaName": "spec-driven",
      "artifacts": []
    }
  ],
  "root": {
    "path": "/Users/you/projects/my-app",
    "source": "nearest"
  }
}
```

如果某个变更无法加载，批次会继续。它的条目包含 `changeName` 和一个 `status` 诊断，而其他条目仍然可用。命令以退出码 1 结束，JSON 模式下亦然，因此 CI 不会把不完整的报告当作成功。JSON 输出仍是一个可解析的文档。

**退出码**

- `0`：所有请求的状态都已打印；空的 `--all` 报告也以退出码 0 结束。
- `1`：请求的变更加载失败、缺少 `--change` 或 `--all`、两个选项同时给出、变更不存在，或模式覆盖未知。

## openspec instructions [#openspec-instructions]

打印创建产物、实施或归档的指令。你的智能体在工作流中运行它，以获取下一步的指令文本。

```bash
openspec instructions proposal --change add-rate-limit   # how to write one artifact
openspec instructions apply --change add-rate-limit      # how to implement the change
openspec instructions archive --change add-rate-limit    # inputs for archiving
```

**参数**

| 参数 | 说明 |
|---|---|
| `artifact` | 模式中的产物 id（`spec-driven` 中为 `proposal`、`specs`、`design`、`tasks`），或保留字 `apply` 和 `archive`。 |

**选项**

| 选项 | 作用 |
|---|---|
| `--change <id>` | 要为其生成指令的变更。必需。 |
| `--schema <name>` | 覆盖模式。否则从 `config.yaml` 自动检测。 |
| `--json` | 打印结构化对象而非文本。 |
| `--store <id>` | 使用已注册的存储库作为 OpenSpec 根目录，而非当前项目。 |

**输出**

产物形式会打印一个指令块：任务、要写入的文件、如何写入、该产物的模板，以及完成它会解锁什么。

```
<artifact id="proposal" change="add-rate-limit" schema="spec-driven">

<task>
Create the proposal artifact for change "add-rate-limit".
Initial proposal document outlining the change
</task>

<output>
Write to: /Users/you/projects/my-app/openspec/changes/add-rate-limit/proposal.md
</output>

<instruction>
Create the proposal document that establishes WHY this change is needed.
...
```

`apply` 打印上下文文件、任务进度和工作指令：

```
## Apply: add-rate-limit
Schema: spec-driven

### Context Files
- proposal: /Users/you/projects/my-app/openspec/changes/add-rate-limit/proposal.md
- specs: /Users/you/projects/my-app/openspec/changes/add-rate-limit/specs/api/spec.md
- tasks: /Users/you/projects/my-app/openspec/changes/add-rate-limit/tasks.md

### Progress
1/3 complete

### Tasks
- [x] 1.1 Add rate limit middleware
- [ ] 1.2 Return 429 with Retry-After header
- [ ] 1.3 Add tests for burst traffic

### Instruction
Read context files, work through pending tasks, mark complete as you go.
Pause if you hit blockers or need clarification.

No project context or operation guidance configured.
```

所需产物缺失时，`apply` 会改为报告 `### ⚠️ Blocked` 并列出它们。`archive` 打印变更名称，以及配置中的任何项目上下文和操作指引。没有配置时，它只说明这一点，不再多说。

使用 `--json` 时，每种形式返回一个对象。产物形式开头为：

```json
{
  "changeName": "add-rate-limit",
  "artifactId": "proposal",
  "schemaName": "spec-driven",
  "changeDir": "/Users/you/projects/my-app/openspec/changes/add-rate-limit",
  ...
```

随后是 `outputPath`、`existingOutputPaths`、完整的 `instruction` 和 `template` 字符串、`dependencies`、`unlocks` 和 `root`。`apply` 形式带有 `contextFiles`、`progress`、`tasks`、`taskTrackingConfigured`、`state`（`blocked`、`ready`、`all_done`）和 `instruction`。

每个 `tasks` 条目带有 `id`、`description`、`done`、`sourcePath` 和 `line`。`sourcePath` 是提供该任务的受跟踪文件的绝对路径。`line` 是该文件中任务复选框的行号（从 1 开始）。`description` 是任务的完整文本：跨多行折行的任务会以一行返回，末尾的 `\` 换行会被去掉。

`taskTrackingConfigured` 始终是布尔值：当模式设置了非空的 [`apply.tracks`](./schemas/schema-yaml.md#tracks) 时为 `true`，即使没有文件匹配；否则为 `false`。如果匹配到的跟踪文件无法读取，`unavailableTrackingFiles` 会包含其绝对 `path` 和错误 `reason`。所有匹配文件都可读时该字段被省略。可读文件仍会贡献 `tasks` 和 `progress`，但在所有匹配文件都被读取之前，`state` 不能是 `all_done`。

**退出码**

- `0`：已打印指令。
- `1`：产物未知、变更未知、模式未知，或缺少 `--change`。每个错误都会列出有效值。

## openspec templates [#openspec-templates]

打印模式各产物解析后的模板路径。

```bash
openspec templates          # default schema: spec-driven
openspec templates --json   # map of artifact ids to paths
```

**选项**

| 选项 | 作用 |
|---|---|
| `--schema <name>` | 要解析的模式。默认：`spec-driven`。 |
| `--json` | 打印产物 id 到模板路径的 JSON 映射。 |

**输出**

```
Schema: spec-driven
Source: package

proposal:
  /usr/local/lib/node_modules/@fission-ai/openspec/schemas/spec-driven/templates/proposal.md
specs:
  /usr/local/lib/node_modules/@fission-ai/openspec/schemas/spec-driven/templates/spec.md
design:
  /usr/local/lib/node_modules/@fission-ai/openspec/schemas/spec-driven/templates/design.md
tasks:
  /usr/local/lib/node_modules/@fission-ai/openspec/schemas/spec-driven/templates/tasks.md
```

`Source` 指明模式解析自哪里：`project`（你项目中的 `openspec/schemas/`）、`user`（全局覆盖），或 `package`（内置于 CLI）。project 优先于 user，user 优先于 package。

```json
{
  "proposal": {
    "path": "/usr/local/lib/node_modules/@fission-ai/openspec/schemas/spec-driven/templates/proposal.md",
    "source": "package"
  },
  "specs": {
    "path": "/usr/local/lib/node_modules/@fission-ai/openspec/schemas/spec-driven/templates/spec.md",
    "source": "package"
  },
  "design": {
    "path": "/usr/local/lib/node_modules/@fission-ai/openspec/schemas/spec-driven/templates/design.md",
    "source": "package"
  },
  "tasks": {
    "path": "/usr/local/lib/node_modules/@fission-ai/openspec/schemas/spec-driven/templates/tasks.md",
    "source": "package"
  }
}
```

**退出码**

- `0`：已打印路径。
- `1`：模式未知。错误会列出可用的模式。

## openspec schemas [#openspec-schemas]

列出可用的工作流模式。

```bash
openspec schemas          # names, descriptions, artifact order
openspec schemas --json   # machine-readable, for agent use
```

**选项**

| 选项 | 作用 |
|---|---|
| `--json` | 以 JSON 输出（供智能体使用）。 |

**输出**

```
Available schemas:

  spec-driven
    Default OpenSpec workflow - proposal → specs → design → tasks
    Artifacts: proposal → specs → design → tasks
```

来自你项目的模式标记为 `(project)`，全局覆盖标记为 `(user override)`。

```json
[
  {
    "name": "spec-driven",
    "description": "Default OpenSpec workflow - proposal → specs → design → tasks",
    "artifacts": [
      "proposal",
      "specs",
      "design",
      "tasks"
    ],
    "source": "package"
  }
]
```

**退出码**

- `0`：已列出模式。
- `1`：无法读取模式列表。

## openspec schema [#openspec-schema]

检查、派生或创建模式（实验性）。每个子命令都会先在 stderr 上打印 `Note: Schema commands are experimental and may change.`。

```bash
openspec schema which spec-driven          # where a schema resolves from
openspec schema fork spec-driven my-flow   # copy a schema into the project
openspec schema init my-schema             # create a schema from scratch
```

| 子命令 | 作用 |
|---|---|
| `which` | 显示模式解析自哪里。 |
| `validate` | 检查模式的结构和模板。 |
| `fork` | 把现有模式复制到项目中以便自定义。 |
| `init` | 创建新的项目内模式。 |

模式从三个位置解析，先匹配到的生效：

| 来源 | 位置 |
|---|---|
| `project` | 当前项目中的 `openspec/schemas/`。 |
| `user` | `~/.local/share/openspec/schemas/`（会遵循 `XDG_DATA_HOME` 和 Windows 的 `%LOCALAPPDATA%`）。 |
| `package` | CLI 随附的模式。`spec-driven` 就在这里。 |

### openspec schema which [#openspec-schema-which]

显示 CLI 将使用模式的哪个副本。

```bash
openspec schema which spec-driven
openspec schema which --all        # every schema, grouped by source
```

**参数**

| 参数 | 说明 |
|---|---|
| `name` | 要查找的模式。除非设置了 `--all`，否则必需。两者都不给时，which 以退出码 1 结束。 |

**选项**

| 选项 | 作用 |
|---|---|
| `--all` | 列出每个模式及其解析来源。 |
| `--json` | 以 JSON 打印解析结果。 |

**输出**

```
Schema: spec-driven
Source: package
Path: /usr/local/lib/node_modules/@fission-ai/openspec/schemas/spec-driven
```

当更高优先级的副本遮蔽了另一个时，`Shadows:` 小节会列出被遮蔽的副本。使用 `--json` 时：

```json
{
  "name": "my-flow",
  "source": "project",
  "path": "/Users/you/projects/my-app/openspec/schemas/my-flow",
  "shadows": []
}
```

未知名称以退出码 1 结束，并列出可用的模式。

### openspec schema validate [#openspec-schema-validate]

检查模式的结构和模板。

```bash
openspec schema validate spec-driven   # one schema, from any source
openspec schema validate               # every project-local schema
```

它会验证 `schema.yaml` 存在且可解析、结构符合模式格式、每个产物的模板文件都存在于该模式的 `templates/` 目录中，以及依赖图没有环或未知引用（包括 `apply.requires` 中的）。若某个 `apply.tracks` 值与任何产物的 `generates` 值不完全相等，会打印一行 `warning:` 但不导致校验失败，因为此时 OpenSpec 无法判断该文件属于哪个产物的进度。

**选项**

| 选项 | 作用 |
|---|---|
| `--json` | 打印结构化报告而非文本。 |
| `--verbose` | 打印每个校验步骤。 |

**输出**

```
✓ Schema 'spec-driven' is valid
```

不带名称时，每个项目模式在 `Validation Results:` 标题下各占一行。失败的模式会列出其问题，运行以退出码 1 结束：

```
✗ Schema 'my-schema' has errors:
  error: Template file 'tasks.md' not found for artifact 'tasks'
```

### openspec schema fork [#openspec-schema-fork]

把现有模式复制到项目中，以便自定义。

```bash
openspec schema fork spec-driven my-flow
```

**参数**

| 参数 | 说明 |
|---|---|
| `source` | 要复制的模式，可来自任何来源位置。 |
| `name` | 副本的名称。kebab-case（`my-workflow`）。默认：`<source>-custom`。 |

**选项**

| 选项 | 作用 |
|---|---|
| `--force` | 覆盖已存在的目标模式。 |
| `--json` | 以 JSON 打印结果。 |

**输出**

```
✔ Forked 'spec-driven' to 'my-flow'

Source: /usr/local/lib/node_modules/@fission-ai/openspec/schemas/spec-driven (package)
Destination: /Users/you/projects/my-app/openspec/schemas/my-flow
```

派生结果落在 `openspec/schemas/` 中，其 `schema.yaml` 里的 `name:` 字段会被改写为新名称：

```
openspec/schemas/my-flow/
├── schema.yaml
└── templates/
    ├── design.md
    ├── proposal.md
    ├── spec.md
    └── tasks.md
```

目标已存在即为错误，除非传入 `--force`。保留源名称的派生会遮蔽原始模式。

### openspec schema init [#openspec-schema-init]

创建带有起始模板的新项目内模式。

```bash
openspec schema init my-schema --description "Lightweight flow" --artifacts proposal,tasks
```

在交互式终端中不带 `--description` 也不带 `--artifacts` 时，init 会提示输入描述、选择产物清单，并询问是否把该模式设为项目默认。在非终端环境中，它使用下面的默认值。

**参数**

| 参数 | 说明 |
|---|---|
| `name` | 新模式名称。kebab-case（`my-workflow`）。 |

**选项**

| 选项 | 作用 |
|---|---|
| `--description <text>` | 模式描述。默认：`Custom workflow schema for <name>`。 |
| `--artifacts <list>` | 逗号分隔的产物 ID，取自 `proposal`、`specs`、`design`、`tasks`。默认：全部四个。 |
| `--default` | 把 `schema: <name>` 写入现有的 `openspec/config.yaml` 或 `openspec/config.yml`。两者都不存在时创建 `openspec/config.yaml`。新变更使用该模式。 |
| `--no-default` | 跳过关于默认值的提示。 |
| `--force` | 覆盖同名的现有模式。 |
| `--json` | 以 JSON 打印结果。 |

创建模式和更新 `--default` 配置是一次操作。如果 OpenSpec 无法校验或写入配置，配置和任何现有模式都会保持不变。

**输出**

```
✔ Created schema 'my-schema'

Schema created at: /Users/you/projects/my-app/openspec/schemas/my-schema

Artifacts: proposal, tasks
```

磁盘上的布局：

```
openspec/schemas/my-schema/
├── schema.yaml
└── templates/
    ├── proposal.md
    └── tasks.md
```

`schema.yaml` 把选中的产物与其依赖接好。包含 `tasks` 时，它还会得到一个跟踪 `tasks.md` 的 `apply` 阶段。用 `openspec new --schema my-schema` 使用该模式。

## openspec store [#openspec-store]

创建并管理存储库：注册到你机器上的独立 OpenSpec 仓库。

```bash
openspec store setup team-context --path ~/openspec/team-context   # create and register
openspec store register ~/stores/design-system                     # register an existing checkout
openspec store list                                                # see what's registered
```

注册信息保存在按机器划分的注册表中：`~/.local/share/openspec/stores/registry.yaml`，设置了 `XDG_DATA_HOME` 时为 `$XDG_DATA_HOME/openspec/stores/registry.yaml`。每个子命令都接受 `--json`，用于打印结构化报告而非文本。子命令缺失或未知时运行 `openspec store` 会以退出码 1 退出，并列出所有子命令。

| 子命令 | 作用 |
|---|---|
| `setup [id]` | 创建存储库文件夹并注册它。 |
| `register [path]` | 注册一个已存在的存储库文件夹。 |
| `unregister <id>` | 忘掉该注册信息。文件夹仍留在磁盘上。 |
| `remove <id>` | 忘掉该注册信息并删除文件夹。 |
| `list`（别名 `ls`） | 列出已注册的存储库。 |
| `doctor [id]` | 检查已注册存储库的注册信息、元数据和 Git 状态。 |

### openspec store setup [#openspec-store-setup]

创建存储库文件夹并注册它。

```bash
openspec store setup team-context --path ~/openspec/team-context
```

在交互式终端中，setup 会提示补全缺失的名称和位置，并在创建任何内容前确认。在交互式终端之外，缺少名称或缺 `--path` 会以退出码 1 退出，并说明需要传入哪个标志。对已注册的存储库重复运行 setup 会报告 `Registry: already registered`。

当 `--path` 位于另一个 Git 仓库内部时，setup 会以 `store_setup_inside_git_repo` 错误退出 1，因为在那里初始化存储库会让一个仓库嵌套进另一个仓库。`--no-init-git` 不创建仓库，因此跳过该检查。如果你的主目录本身就是一个 Git 仓库（例如 dotfiles 仓库），可以用它在 `~/openspec/<id>` 保留一个存储库。

**参数**

| 参数 | 说明 |
|---|---|
| `id` | 存储库名称。它将成为传给 `--store` 的 id。 |

**选项**

| 选项 | 作用 |
|---|---|
| `--path <path>` | 存储库应位于的文件夹（`~` 会展开）。 |
| `--init-git` | 初始化 Git 仓库并创建初始提交。默认。 |
| `--no-init-git` | 跳过所有 Git 操作：不初始化，也不创建初始提交。 |
| `--remote <url>` | 记录在 `store.yaml` 中的标准克隆源。 |

**输出**

```
Store ready: team-context
Location: /Users/you/stores/team-context
OpenSpec root: ready
Registry: registered

Next: run normal OpenSpec commands against this store, for example:
  openspec new change <change-id> --store team-context
Share this store by committing and pushing it like any Git repo.
```

`--json` 报告创建了什么，以及注册在何处：

```json
{
  "store": {
    "id": "design-system",
    "root": "/Users/you/stores/design-system",
    "metadata_path": "/Users/you/stores/design-system/.openspec-store/store.yaml"
  },
  "registry": {
    "path": "/Users/you/.local/share/openspec/stores/registry.yaml",
    "registered": true,
    "already_registered": false
  },
  "git": {
    "is_repository": true,
    "initialized": true,
    "committed": true
  },
  "created_files": [
    "openspec/",
    "openspec/specs/",
    "openspec/changes/",
    "openspec/changes/archive/",
    "openspec/config.yaml",
    "openspec/specs/.gitkeep",
    "openspec/changes/archive/.gitkeep",
    ".openspec-store/store.yaml"
  ],
  "status": []
}
```

### openspec store register [#openspec-store-register]

注册一个已存在的存储库文件夹，例如你克隆的同事的存储库。

```bash
openspec store register ~/stores/design-system
```

该文件夹必须包含一个健康的 `openspec/` 根目录。存在 `.openspec-store/store.yaml` 时，register 会复用其中记录的 id。不存在时，register 会在创建该元数据之前询问。在交互式终端之外，改为传入 `--yes`。一台机器上，每个存储库 id 只能注册一个检出。同一 id 下的第二个路径，或同一路径下的第二个 id，都会以退出码 1 退出。

**参数**

| 参数 | 说明 |
|---|---|
| `path` | 要注册的存储库文件夹（`~` 会展开）。必需。 |

**选项**

| 选项 | 作用 |
|---|---|
| `--id <id>` | 存储库 id。默认为元数据或文件夹名。 |
| `--yes` | 确认为健康的 OpenSpec 根目录创建存储库身份元数据。 |

**输出**

```
Store registered: design-system
Location: /Users/you/stores/design-system
OpenSpec root: ready
Registry: registered
```

`--json` 打印与 `store setup --json` 相同结构的文档。

### openspec store unregister [#openspec-store-unregister]

忘掉该注册信息。文件夹仍留在磁盘上。

```bash
openspec store unregister design-system
```

```
Unregistered store: design-system
Files kept at: /Users/you/stores/design-system
```

### openspec store remove [#openspec-store-remove]

忘掉该注册信息并删除文件夹。

```bash
openspec store remove design-system --yes
```

在交互模式下，remove 会在删除前询问。使用 `--json` 时，或在交互式终端之外时，删除需要 `--yes`：

```
Error: Pass --yes to delete store files non-interactively.
Fix: openspec store remove design-system --yes
```

当文件夹缺少匹配的存储库元数据，或其中包含另一个已注册的存储库（例如作为 Git 子模块引入的存储库）时，remove 会以退出码 1 退出，且不删除任何内容。此时错误为 `store_remove_contains_registered_store`：先运行 `openspec store unregister <nested-id>`，或运行 `openspec store unregister <id>` 只忘掉该存储库而不删除文件。

**选项**

| 选项 | 作用 |
|---|---|
| `--yes` | 确认删除本地存储库文件夹。 |

**输出**

```
Removed store: design-system
Deleted: /Users/you/stores/design-system
```

### openspec store list [#openspec-store-list]

列出已注册的存储库。`ls` 是别名。

```bash
openspec store list
```

```
OpenSpec stores (2)

ID              Location
design-system   /Users/you/stores/design-system
team-context    /Users/you/stores/team-context
```

没有任何已注册的存储库时，list 会打印 `No stores registered.`，以及接下来可以运行的 setup 与 register 命令。

### openspec store doctor [#openspec-store-doctor]

检查已注册存储库的注册信息、元数据和 Git 状态。

```bash
openspec store doctor                # every registered store
openspec store doctor team-context  # one store
```

**输出**

```
Store doctor

team-context
  Location: /Users/you/stores/team-context
  OpenSpec root: ok
  Metadata: ok
  Git: repository detected (commits: yes, uncommitted changes: no, remote: none)
  Issues: none
```

**退出码**

- `0`：报告已打印，即使有存储库报告了问题。
- `1`：报告无法运行（例如未知的存储库 id）。

## openspec doctor [#openspec-doctor]

报告解析出的 OpenSpec 根目录的关系健康状况。

```bash
openspec doctor                       # nearest openspec/ root above your cwd
openspec doctor --store team-context  # a registered store as the root
```

doctor 是只读的：它绝不克隆、同步或修复。它报告根目录是否健康，以及 `openspec/config.yaml` 中声明的每个引用能否在这台机器上解析。当你的 cwd 之上没有根目录且未传入 `--store` 时，它会以退出码 1 退出，并列出你已注册的存储库。

**选项**

| 选项 | 作用 |
|---|---|
| `--store <id>` | 改用已注册的存储库作为 OpenSpec 根目录，而不是当前项目。 |
| `--json` | 以 JSON 打印健康报告。 |

**输出**

```
Doctor

Root
  Location: /Users/you/projects/my-app
  OpenSpec root: ok

References
  - team-context: ok (/Users/you/stores/team-context)
```

使用 `--store` 时，根目录即该存储库，报告中会多出一行存储库信息：

```
Using OpenSpec root: team-context (/Users/you/stores/team-context)
Doctor

Root
  Location: /Users/you/stores/team-context
  OpenSpec root: ok
  Store: team-context (metadata ok)

References
  (none declared)
```

```json
{
  "root": {
    "path": "/Users/you/projects/my-app",
    "source": "nearest",
    "healthy": true,
    "status": []
  },
  "store": null,
  "references": [
    {
      "store_id": "team-context",
      "root": "/Users/you/stores/team-context",
      "status": []
    }
  ],
  "status": []
}
```

**退出码**

- `0`：报告已打印，包括列出问题的情况。
- `1`：无法解析出根目录（cwd 之上没有 `openspec/` 且未传入 `--store`），或 `--store` 的 id 未知。

## openspec context [#openspec-context]

打印解析出的 OpenSpec 根目录的工作上下文：该根目录，加上 `openspec/config.yaml` 中声明的每个被引用存储库，各自附有一条获取命令。

```bash
openspec context                       # nearest openspec/ root above your cwd
openspec context --store team-context  # a registered store as the root
openspec context --json                # agent brief
```

无法在这台机器上解析的引用会进入 `Not available on this machine` 一节，每条都附带修复方式。

**选项**

| 选项 | 作用 |
|---|---|
| `--store <id>` | 改用已注册的存储库作为 OpenSpec 根目录，而不是当前项目。 |
| `--json` | 以 JSON 打印智能体简报。 |
| `--code-workspace <path>` | 同时为该集合写一个 VS Code workspace 文件。 |
| `--force` | 覆盖已存在的 `--code-workspace` 文件。 |

**输出**

```
Working context for my-app (/Users/you/projects/my-app)

OpenSpec root
  my-app  /Users/you/projects/my-app

Referenced stores
  team-context  /Users/you/stores/team-context
    Fetch: openspec show <spec-id> --type spec --store team-context
```

使用 `--store` 时，该存储库就是整个集合：

```
Using OpenSpec root: team-context (/Users/you/stores/team-context)
Working context for team-context (/Users/you/stores/team-context)

OpenSpec root
  team-context  /Users/you/stores/team-context

No references declared; the working set is this root alone.
```

```json
{
  "root": {
    "path": "/Users/you/projects/my-app",
    "source": "nearest",
    "role": "openspec_root"
  },
  "members": [
    {
      "role": "referenced_store",
      "id": "team-context",
      "path": "/Users/you/stores/team-context",
      "fetch": "openspec show <spec-id> --type spec --store team-context",
      "status": []
    }
  ],
  "status": []
}
```

**写入 workspace 文件**

`--code-workspace` 会在你给出的路径写一个 VS Code workspace 文件：根目录一个文件夹，每个可用的被引用存储库一个 `ref:<id>` 文件夹。不可用的引用会被跳过，并在摘要行中列出名称：`Wrote /Users/you/projects/my-app/openspec.code-workspace (2 folders)`。摘要输出到 stderr，因此 `--json` 的 stdout 仍是一个 JSON 文档。文件已存在时会以退出码 1 退出，除非传入 `--force`。

```json
{
  "folders": [
    {
      "name": "my-app",
      "path": "/Users/you/projects/my-app"
    },
    {
      "name": "ref:team-context",
      "path": "/Users/you/stores/team-context"
    }
  ]
}
```

**退出码**

- `0`：报告已打印。
- `1`：无法解析出根目录（cwd 之上没有 `openspec/` 且未传入 `--store`），或 `--code-workspace` 写入被拒绝。

## openspec workset [#openspec-workset]

组合、保存并打开个人工作视图。工作集是一份已保存的、带名称的文件夹列表，这些文件夹由你一起使用。

```bash
openspec workset create checkout --member ~/projects/checkout-api --member web=~/projects/checkout-web
openspec workset list
openspec workset remove checkout --yes
```

| 子命令 | 作用 |
|---|---|
| `create [name]` | 组合并保存一份由你选择的文件夹组成的命名工作视图。 |
| `list`、`ls` | 显示已保存的工作集及其成员。 |
| `open <name>` | 在你的工具中打开已保存的工作集（编辑器窗口或智能体会话）。 |
| `remove <name>` | 删除已保存的工作集（成员文件夹绝不会被改动）。 |

工作集完全本地：

- 它的状态只保存在一个文件夹中：`~/.local/share/openspec/worksets/`（设置时用 `$XDG_DATA_HOME/openspec/worksets/`；Windows 上为 `%LOCALAPPDATA%\openspec\worksets\`）。
- 不会向成员文件夹写入任何内容，也不会有任何提交或共享。
- 删除那一个文件夹即可清除全部痕迹。

### openspec workset create [#openspec-workset-create]

保存一份带名称的文件夹工作视图。

```bash
openspec workset create checkout \
  --member ~/projects/checkout-api \
  --member web=~/projects/checkout-web
```

在交互式终端中，create 会询问标志未提供的内容：名称、逐个文件夹、一个工具，然后询问是否现在就打开该工作集。在交互式终端之外，缺少名称或成员即为错误。名称已保存过始终是错误。请先删除它。

**参数**

| 参数 | 说明 |
|---|---|
| `name` | 工作集名称。Kebab-case：小写字母、数字、单个连字符。在交互式终端之外必需。 |

**选项**

| 选项 | 作用 |
|---|---|
| `--member <member>` | 成员文件夹，形式为 `<path>` 或 `<name>=<path>`，可重复。第一个是主成员。路径必须是已存在的文件夹，标签默认为文件夹自身的名称。 |
| `--tool <id>` | 打开该工作集时优先使用的工具。内置 id：`code`（VS Code）、`cursor`（Cursor）。`claude` 和 `codex` 暂时停用。 |
| `--json` | 以 JSON 打印已保存的工作集。 |

**输出**

```
Saved workset 'checkout' (2 members) to your machine.
Open it any time with: openspec workset open checkout
```

### openspec workset list [#openspec-workset-list]

显示已保存的工作集及其成员，按名称排序。

```bash
openspec workset list   # alias: ls
```

**选项**

| 选项 | 作用 |
|---|---|
| `--json` | 以 JSON 打印工作集。 |

**输出**

每个工作集一块：名称、它的工具（如果有），然后每个成员一行 `name  path`。没有任何已保存的工作集时，list 会打印 `No worksets saved. Create one with: openspec workset create`。

```
checkout
  checkout-api  /Users/you/projects/checkout-api
  web           /Users/you/projects/checkout-web
checkout-tool  (opens in VS Code)
  checkout-api  /Users/you/projects/checkout-api
```

使用 `--json` 时：

```json
{
  "worksets": [
    {
      "name": "checkout",
      "members": [
        {
          "name": "checkout-api",
          "path": "/Users/you/projects/checkout-api"
        },
        {
          "name": "web",
          "path": "/Users/you/projects/checkout-web"
        }
      ]
    }
  ],
  "status": []
}
```

### openspec workset open [#openspec-workset-open]

在你的工具中打开已保存的工作集。编辑器类工具（`code`、`cursor`）会得到一个生成的 `.code-workspace` 文件。窗口打开后命令即返回。CLI 智能体工具（`claude`、`codex`）本会接管当前终端并带上所有成员。由于该流程正在重做，它们暂时停用，因此工作集目前只能在 IDE 中打开。

```bash
openspec workset open checkout                # saved tool, or a prompt
openspec workset open checkout --tool cursor  # this tool just this once
```

**参数**

| 参数 | 说明 |
|---|---|
| `name` | 要打开的工作集。 |

**选项**

| 选项 | 作用 |
|---|---|
| `--tool <id>` | 仅这一次用该工具打开。 |

既没有 `--tool` 也没有已保存的工具时，open 会提示你选择一个已安装的工具。在交互式终端之外则以退出码 1 退出。

- 已不存在的成员文件夹会被跳过并给出警告。主成员缺失时，下一个仍然存在的成员会成为本次打开的主成员。没有任何成员文件夹存在时，打开失败。
- `--json` 会被拒绝：open 会把终端交给工具，没有 JSON 模式。
- 启动失败时，错误信息末尾给出手动方式：workspace 文件的路径和成员列表。

**退出码**

- 与工具保持一致：命令以工具自身的退出码退出，信号会变成 `128+n`（Ctrl-C 之后为 `130`）。
- `1`：工作集未知、没有可用的成员文件夹，或没有可用的工具。

### openspec workset remove [#openspec-workset-remove]

删除已保存的工作集及其生成的 `.code-workspace` 文件。成员文件夹绝不会被改动。

```bash
openspec workset remove checkout --yes
```

在交互式终端中，remove 会显示该工作集并要求你确认。使用 `--json` 时，或在终端之外时，需要 `--yes`，否则以退出码 1 退出。

**选项**

| 选项 | 作用 |
|---|---|
| `--yes` | 非交互地确认删除。 |
| `--json` | 以 JSON 打印删除结果。 |

**输出**

```
Removed workset 'checkout'. Member folders were not touched.
```

## openspec version [#openspec-version]

报告正在运行的 OpenSpec 版本，以及这份副本是如何安装的。

```bash
openspec version                 # local version and install details
openspec version --json          # structured local report
openspec version --check         # also check for an update
openspec version --check --json  # structured local and update report
```

不带 `--check` 时，该命令是本地操作，不发起任何网络请求。它可以在 OpenSpec 项目之外工作。现有的 `openspec --version` 标志仍是最短形式，只打印纯粹的版本号。

**选项**

| 选项 | 作用 |
|---|---|
| `--json` | 打印单个带版本号的 JSON 文档，而非文本。 |
| `--check` | 检查是否有更新的发布版本。npm、项目安装和源码安装会询问配置的 npm 注册表。独立安装改为询问 GitHub releases（见下文）。 |

**输出**

对于全局 npm 安装：

```text
OpenSpec 1.13.2 (npm, global)
```

安装范围是 `global`、`project`、`temporary`（用于 npx 这类临时运行器）、`source`（用于检出）或 `standalone`（用于[独立安装](./installation.md#install)）。OpenSpec 会省略它无法识别的细节，而不是猜测。

`--json` 会把未知细节保留为显式的 `null` 值：

```json
{
  "schemaVersion": 1,
  "version": "1.13.2",
  "install": {
    "location": "/opt/homebrew/lib/node_modules/@fission-ai/openspec",
    "packageManager": "npm",
    "scope": "global"
  }
}
```

使用 `--check` 时，若有可用更新，会加上最新版本号；当 OpenSpec 能为该安装识别出安全命令时，还会加上该命令：

```text
OpenSpec 1.13.2 (npm, global)
Update available: 1.14.0
  npm install -g @fission-ai/openspec@latest
```

```json
{
  "schemaVersion": 1,
  "version": "1.13.2",
  "install": {
    "location": "/opt/homebrew/lib/node_modules/@fission-ai/openspec",
    "packageManager": "npm",
    "scope": "global"
  },
  "update": {
    "status": "available",
    "latest": "1.14.0",
    "command": "npm install -g @fission-ai/openspec@latest",
    "canSelfUpgrade": true
  }
}
```

更新状态取值：

| 状态 | 含义 |
|---|---|
| `available` | 可以安装一个比当前运行版本更新的安全版本。 |
| `current` | 检查已完成，未发现更新的版本。 |
| `disabled` | 设置了 `OPENSPEC_NO_UPDATE_CHECK`，或（仅 npm 安装）某个注册表覆盖被拒绝。`latest` 为 `null`。 |
| `offline` | 注册表或 GitHub 不可用、拒绝了请求（例如限流），或返回了不可用的响应。`latest` 为 `null`。 |

对于独立安装，更新命令是 `openspec install`，检查范围与该命令能获取的内容一致：GitHub 上附有 `SHA256SUMS` 的最新稳定版本。几分钟前刚发布、文件尚未附上的版本不会被提供。npm 注册表设置不适用于这项检查。

因为 `--check` 是显式请求，即使遥测已关闭（`DO_NOT_TRACK`、`OPENSPEC_TELEMETRY=0`、`telemetry.enabled: false`），或在 CI 中，它仍会运行。只有 `OPENSPEC_NO_UPDATE_CHECK` 能关闭它；对 npm 安装而言，还可由被拒绝的非 HTTPS 注册表覆盖关闭。`openspec update` 中的后台检查在上述所有情况下仍然保持关闭。被禁用和离线的检查仍以退出码 0 退出，因为更新可用性只是建议性的。该命令绝不会升级 OpenSpec；`canSelfUpgrade` 只报告现有的 `openspec update` 路径能否安全升级这份副本。

**退出码**

- `0`：本地报告已打印，包括被禁用或离线的更新检查。
- `1`：命令语法无效，例如不受支持的 `--upgrade` 选项。

## openspec install [#openspec-install]

安装独立的 `openspec`。从 npm 或 Homebrew 安装运行它可切换过去；从独立安装运行它可就地升级。

```bash
openspec install          # newest release
openspec install 1.15.0   # a specific release
```

它运行[安装脚本](./installation.md#install)，该脚本挑选所有文件都已附上的最新版本以及适合你机器的文件，并用该版本的 `SHA256SUMS` 校验：

- **从包管理器安装**：安装到 `~/.local/bin`（Windows：`%LOCALAPPDATA%\Programs\openspec`），并打印移除旧副本的命令，例如 `npm uninstall -g @fission-ai/openspec`。它绝不自行移除该副本。
- **从独立安装**：在原地以其自身名称替换正在运行的文件。

之后它会说明 `openspec` 现在运行的是哪一份副本，因为 PATH 中更靠前的包管理器副本在你移除它之前仍会继续运行。

**参数**

| 参数 | 说明 |
|---|---|
| `version` | 要安装的发布版本，例如 `1.15.0`。可选；默认为最新版。 |

`OPENSPEC_INSTALL_DIR` 和 `OPENSPEC_INSTALL_NAME` 可以指定别的文件夹或文件名。

**退出码**

- `0`：已安装。
- `1`：该版本不是发布版本，或下载、安装失败。你当前的副本保持原样。

## openspec feedback [#openspec-feedback]

提交关于 OpenSpec 的反馈。

```bash
openspec feedback "Validate output is hard to scan"
openspec feedback "Archive fails on Windows" --body "Steps: init, propose, archive. Error: EPERM."
```

CLI 通过你的 `gh` CLI 把你的消息作为 GitHub issue 提交到 `Fission-AI/OpenSpec` 仓库。标题会变成 `Feedback: <message>`。正文使用 bug 表单的标题结构：你的消息位于 `What happened` 之下，`--body` 文本位于 `Details` 之下，还有一个 `Minimal steps to reproduce` 一节请你补充复现步骤，因为 CLI 无法填写这些内容。页脚会加上 CLI 版本、平台和时间戳。该 issue 会带上 `feedback` 标签。如果仓库没有定义该标签，CLI 会去掉它重试并说明。

**参数**

| 参数 | 说明 |
|---|---|
| `message` | 一行摘要。会成为 issue 标题。必需。 |

**选项**

| 选项 | 作用 |
|---|---|
| `--body <text>` | 加进 issue 正文的更详细描述。 |

**输出**

成功时：

```
✓ Feedback submitted successfully!
Issue URL: https://github.com/Fission-AI/OpenSpec/issues/1234
```

未安装 `gh`，或 `gh` 未登录时，不会提交任何内容。CLI 会在 `--- FORMATTED FEEDBACK ---` 标记之间打印格式化后的反馈，然后给出一个链接：该链接打开 bug 报告表单，并预填标题、发生了什么（你的消息和 `--body` 文本）、CLI 版本和环境（平台和 Node 版本）。你在浏览器中完成表单的其余部分。未登录的路径还会加上 `To auto-submit in the future: gh auth login`。

**退出码**

- `0`：issue 已创建，或执行了手动提交的回退路径（没有 `gh`，或 `gh` 未登录）。
- `1`：未提供消息。
- `gh` 自身的退出码：认证之后 `gh` 失败（网络、限流、issues 被禁用）。CLI 会先重新打印你的反馈和手动提交 URL。

## openspec completion [#openspec-completion]

安装或生成 shell 补全。

```bash
openspec completion install        # detect your shell, install, wire up config
openspec completion generate zsh   # print the script to stdout
```

支持的 shell：`zsh`、`bash`、`fish`、`powershell`。每个子命令都接受一个可选的 shell 参数。省略时，CLI 会从环境中检测你的 shell。

| 子命令 | 作用 |
|---|---|
| `generate [shell]` | 把补全脚本打印到 stdout。 |
| `install [shell]` | 写入脚本并配置你的 shell 启动文件。 |
| `uninstall [shell]` | 移除脚本和配置块。 |

通过 Nix 安装时，补全已在相应位置：flake 包在标准位置提供了 Bash、Fish 和 Zsh 脚本，因此无需 `install`（[安装](./installation.md#nix)）。

### openspec completion generate [#openspec-completion-generate]

打印脚本，不写入任何内容。

```
#compdef openspec

# Zsh completion script for OpenSpec CLI
# Auto-generated - do not edit manually

_openspec() {
  local context state line
  typeset -A opt_args
...
```

### openspec completion install [#openspec-completion-install]

写入脚本并修改你的 shell 配置。配置修改位于 `# OPENSPEC:START` 和 `# OPENSPEC:END` 标记之间。已存在的脚本会先备份（`.backup-<timestamp>` 副本）。

| Shell | 脚本位置 | 修改的配置 |
|---|---|---|
| zsh | `~/.zsh/completions/_openspec` | 当 `ZDOTDIR` 是绝对路径时为 `$ZDOTDIR/.zshrc`，否则为 `~/.zshrc` |
| bash | `~/.local/share/bash-completion/completions/openspec` | `~/.bashrc` |
| fish | `~/.config/fish/completions/openspec.fish` | 无：fish 会自动加载它。 |
| powershell | 你的配置文件旁的 `OpenSpecCompletion.ps1` | `$PROFILE` |

安装了 Oh My Zsh 时，脚本会改放于 `$ZSH_CUSTOM/completions/_openspec`（默认 `~/.oh-my-zsh/custom/completions/_openspec`）。

相对路径或以 `~` 开头的 `ZDOTDIR` 会被忽略，改为编辑 `~/.zshrc`。脚本已是最新时再次运行 install，仍会把配置块加到 zsh 实际读取的 `.zshrc`。

**选项**

| 选项 | 作用 |
|---|---|
| `--verbose` | 同时打印安装路径、任何备份路径，以及被编辑的配置文件。 |

**输出**

```
✓ Completion script installed and .zshrc configured successfully

Restart your shell or run: exec zsh
```

### openspec completion uninstall [#openspec-completion-uninstall]

移除脚本和带标记的配置块。它在改动你的配置前会询问（默认：否）。

对 zsh，它会清理 install 编辑的 `.zshrc`；若旧版安装在 `ZDOTDIR` 下的 `~/.zshrc` 中留下过配置块，也会一并清理该文件。如果某个配置块无法移除，uninstall 会指出文件名并以退出码 1 退出。

**选项**

| 选项 | 作用 |
|---|---|
| `-y, --yes` | 跳过确认提示。 |

**输出**

```
✓ Completion script removed from /Users/you/.zsh/completions/_openspec. Removed OpenSpec configuration from ~/.zshrc
```

**退出码**

- `0`：脚本已生成、安装或移除。取消的卸载也以退出码 0 退出。
- `1`：shell 不受支持或未被检测到，或安装、卸载步骤失败。

## openspec change [#openspec-change]

`show`、`list` 和 `validate` 的已弃用名词形式。每次运行都会给出警告并指向动词在前的命令，然后仍然照常运行：

```
Warning: The "openspec change ..." commands are deprecated. Prefer verb-first commands (e.g., "openspec list", "openspec validate --changes").
Warning: "openspec change list" is deprecated. Use "openspec list".
add-rate-limit
```

| 已弃用 | 改用 |
|---|---|
| `openspec change show <name>` | `openspec show <name>` |
| `openspec change list` | `openspec list` |
| `openspec change validate <name>` | `openspec validate <name>`（所有变更：`openspec validate --changes`） |

动词在前的章节记录了这些标志。

## openspec spec [#openspec-spec]

`show`、`list` 和 `validate` 的已弃用名词形式。每次运行都会给出警告并指向动词在前的命令，然后仍然照常运行：

```
Warning: The "openspec spec ..." commands are deprecated. Prefer verb-first commands (e.g., "openspec show", "openspec validate --specs").
api
```

| 已弃用 | 改用 |
|---|---|
| `openspec spec show <id>` | `openspec show <id>` |
| `openspec spec list` | `openspec list --specs` |
| `openspec spec validate <id>` | `openspec validate <id>`（所有规格：`openspec validate --specs`） |

动词在前的章节记录了这些标志。
