---
source_url: https://openspec.dev/docs/supported-tools
source_hash: sha256:0c28f7122f68087e3f04c0058249208966c69524094d4705538bfd1000e31a57
translated_at: 2026-11-13T09:48:42+08:00
translation_version: 1
---

# 支持的工具

矩阵中的每个工具都运行相同的 OpenSpec 工作流，这些工作流以技能形式安装。更早的版本还会写入命令文件。这些文件会怎样，见[升级到 2.0](./upgrade-to-2.md)。

## 技能写到哪里 [#where-skills-go]

每个工具的技能只写一次，写到 `.agents/skills/`。不读取该文件夹的工具，会在自己的 `skills/` 文件夹里为每个技能获得一个链接，指回共享副本。

一个为 Claude Code、Cursor 和 Codex 配置好的项目：

```
my-project/
├── .agents/skills/
│   ├── .openspec-target           the tools set up here, one per line
│   └── openspec-propose/SKILL.md  the one copy every tool reads
└── .claude/
    └── skills/openspec-propose    link to ../../.agents/skills/openspec-propose
```

Cursor 和 Codex 自己会读取 `.agents/skills/`，因此无需其他配置。

`.openspec-target` 是 `openspec update` 判断哪些内容属于 OpenSpec 的依据。每一行是以下之一：

| 行 | 含义 |
|---|---|
| `<tool>` | 此项目中已配置的工具，例如 `cursor`。 |
| `<tool> own-files` | OpenSpec 在该工具自己的文件夹里为它创建了链接，例如 `claude own-files`。删除该文件夹后，`update` 会移除该工具。 |
| `keep <skill>` | 你自己的技能，例如 `keep openspec-mine`。它在 OpenSpec 使用该文件夹之前就已存在，因此 OpenSpec 绝不触碰它。 |

- **创建链接**：Claude Code、Continue、ForgeCode、Kiro、CodeBuddy、EasyCode、iFlow、CodeArts、Lingma、GigaCode、Veai、Rovo Dev、Code Studio 和 Hermes Agent。
- **不创建链接**：其他所有工具直接读取 `.agents/skills/`，因此绝不会重复加载技能。
- **无法创建链接时**：OpenSpec 改为写入普通副本，并在 `openspec update` 时刷新它。

要添加未列出的工具，见[链接其他工具](#link-another-tool)。

## 支持矩阵 [#support-matrix]

调用方式以实施工作流为例展示。每个工作流的形态相同。把 id 传给 `openspec init --tools <id>` 可跳过选择器（[CLI](./cli.md)）。

| 工具 | `--tools` id | 技能 | 技能调用 |
|---|---|---|---|
| Amp | `amp` | `.agents/skills/` | `/openspec-apply-change` |
| Antigravity | `antigravity` | `.agents/skills/` | `/openspec-apply-change` |
| AtomCode | `atomcode` | `.agents/skills/` | `/openspec-apply-change` |
| Auggie (Augment CLI) | `auggie` | `.agents/skills/` | `/openspec-apply-change` |
| IBM Bob | `bob` | `.agents/skills/` | `/openspec-apply-change` |
| Claude Code | `claude` | `.agents/skills/`（链接位于 `.claude/skills/`） | `/openspec-apply-change` |
| Cline | `cline` | `.agents/skills/` | `/openspec-apply-change` |
| CodeArts | `codeartsagent` | `.agents/skills/`（链接位于 `.codeartsdoer/skills/`） | `/openspec-apply-change` |
| CodeBuddy Code (CLI) | `codebuddy` | `.agents/skills/`（链接位于 `.codebuddy/skills/`） | `/openspec-apply-change` |
| Code Studio | `codestudio` | `.agents/skills/`（链接位于 `.codestudio/skills/`） | `/openspec-apply-change` |
| Codex | `codex` | `.agents/skills/` | `$openspec-apply-change` |
| Continue | `continue` | `.agents/skills/`（链接位于 `.continue/skills/`） | `/openspec-apply-change` |
| CoStrict | `costrict` | `.agents/skills/` | `/openspec-apply-change` |
| Crush | `crush` | `.agents/skills/` | `/openspec-apply-change` |
| Cursor | `cursor` | `.agents/skills/` | `/openspec-apply-change` |
| DeepSeek Harness | `dsh` | `.agents/skills/` | `/openspec-apply-change` |
| Devin Desktop (formerly Windsurf) | `devin` | `.agents/skills/` | `/openspec-apply-change` |
| EasyCode | `easycode` | `.agents/skills/`（链接位于 `.easycode/skills/`） | `/openspec-apply-change` |
| Factory Droid | `factory` | `.agents/skills/` | `/openspec-apply-change` |
| ForgeCode | `forgecode` | `.agents/skills/`（链接位于 `.forge/skills/`） | `/openspec-apply-change` |
| Gemini CLI | `gemini` | `.agents/skills/` | `/openspec-apply-change` |
| GigaCode | `gigacode` | `.agents/skills/`（链接位于 `.gigacode/skills/`） | `/openspec-apply-change` |
| GitHub Copilot | `github-copilot` | `.agents/skills/` | `/openspec-apply-change` |
| Grok Build | `grok` | `.agents/skills/` | `/openspec-apply-change` |
| GSD | `gsd` | `.agents/skills/` | 请求 `openspec-apply-change` |
| Hermes Agent | `hermes` | `.agents/skills/`（链接位于 `.hermes/skills/`） | `/openspec-apply-change` |
| iFlow | `iflow` | `.agents/skills/`（链接位于 `.iflow/skills/`） | `/openspec-apply-change` |
| Junie | `junie` | `.agents/skills/` | `/openspec-apply-change` |
| Kilo Code | `kilocode` | `.agents/skills/` | `/openspec-apply-change` |
| Kimi Code | `kimi` | `.agents/skills/` | `/skill:openspec-apply-change` |
| Kiro | `kiro` | `.agents/skills/`（链接位于 `.kiro/skills/`） | `/openspec-apply-change` |
| Lingma | `lingma` | `.agents/skills/`（链接位于 `.lingma/skills/`） | `/openspec-apply-change` |
| MiniMax Code | `minimax-code` | `~/.minimax/skills/`（全局） | `/openspec-apply-change` |
| Mistral Vibe | `vibe` | `.agents/skills/` | `/openspec-apply-change` |
| Oh My Pi | `oh-my-pi` | `.agents/skills/` | `/openspec-apply-change` |
| OpenCode | `opencode` | `.agents/skills/` | `/openspec-apply-change` |
| Pi | `pi` | `.agents/skills/` | `/openspec-apply-change` |
| Qoder | `qoder` | `.agents/skills/` | `/openspec-apply-change` |
| Qwen Code | `qwen` | `.agents/skills/` | `/openspec-apply-change` |
| Rovo Dev CLI | `rovodev` | `.agents/skills/`（链接位于 `.rovodev/skills/`） | 请求 `openspec-apply-change` |
| Trae | `trae` | `.agents/skills/` | `/openspec-apply-change` |
| [Veai](https://veai.ru/docs/veai/download) | `veai` | `.agents/skills/`（链接位于 `.veai/skills/`） | `/openspec-apply-change` |
| Warp | `warp` | `.agents/skills/` | `/openspec-apply-change` |
| ZCode | `zcode` | `.agents/skills/` | `/openspec-apply-change` |
| Zoo Code | `roocode` | `.agents/skills/` | `/openspec-apply-change` |
| 其他 / 通用 | `agents` | `.agents/skills/` | `/openspec-apply-change` |

- **技能调用**：工具是否把技能注册为可输入条目，取决于该工具自身的行为。该列展示 OpenSpec 在生成文件以及 init 打印的提示中使用的拼写。如果输入后没有任何反应，请查阅你的工具的文档。

## 链接其他工具 [#link-another-tool]

读取 `.agents/skills/` 的工具无需任何操作：在 init 时选择 `agents`（[其他 / 通用](#other--universal-shared-agents-skills)）。只读取自己文件夹的工具，用一个链接就能指向共享副本。在终端中，从项目根目录执行：

```bash
mkdir -p .mytool
ln -s ../.agents/skills .mytool/skills
```

在 Windows 上，于命令提示符中：

```
mkdir .mytool
mklink /J .mytool\skills .agents\skills
```

把 `.mytool` 换成你的工具的文件夹。如果该工具已有自己的 `skills/` 文件夹，改为逐个链接技能：`ln -s ../../.agents/skills/openspec-propose .mytool/skills/openspec-propose`。

**提交链接**：Git 会把链接按链接存储。Windows 上的同事应运行 `git config --global core.symlinks true`（或用 `git clone -c core.symlinks=true <url>` 克隆）并开启开发者模式，才能创建链接。否则每个链接会被检出为一个小文本文件，`openspec update` 会用技能的普通副本替换它。用 `mklink /J` 创建的联接点不会按链接提交；需在每台机器上重新创建。

## 各工具说明 [#per-tool-notes]

此处未列出的工具，行为与其在矩阵中的那一行完全一致。

### Amazon Q Developer（已弃用） [#amazon-q-developer-retired]

OpenSpec 2.0 不再支持 Amazon Q Developer：它无法加载技能，且 AWS 正以 Kiro 取代它并将其弃用。`openspec init --tools amazon-q` 会以该消息终止。在为其配置过的项目中，`openspec update` 会移除 OpenSpec 写入 `.amazonq/` 的提示词和技能，并保留和列出你编辑过的内容。请改用 Kiro：`openspec init --tools kiro`。

### Antigravity [#antigravity]

- **当前文件夹**：Antigravity v1.20.5 及以后版本从 `.agents/` 读取工作区技能和工作流。
- **旧版文件夹**：OpenSpec 写入替代文件后，会从 `.agent/` 移除等效的生成文件。自定义文件以及改动过的生成文件会留在 `.agent/` 供你检查。
- **共享技能**：Antigravity 与其他所有工具读取同一份 `.agents/skills/` 副本。OpenSpec 在 2.0 之前写入 `.agents/workflows/` 的工作流会在更新时移除。

### Cline [#cline]

技能是 `.agents/skills/` 中的共享副本。OpenSpec 在 2.0 之前写入 `.clinerules/workflows/` 的工作流会在更新时移除；你自己在那里的规则保持不动。

### Codex [#codex]

- **CLI 和 IDE 扩展**：把 `$openspec-propose` 和你的想法一起说，或运行 `/skills` 选择技能。Codex 不识别 `/openspec-propose`（[上游 issue](https://github.com/openai/codex/issues/11817)）。
- **桌面应用**：在侧边栏打开 Skills 并选择 `openspec-propose`。[OpenAI 的技能文档](https://learn.chatgpt.com/docs/build-skills)介绍了这两个界面。
- **共享文件夹**：Codex 与其他所有工具读取同一份 `.agents/skills/` 副本。技能之间以技能名（`openspec-apply-change`）相互引用，Codex 以 `$openspec-apply-change` 调用它。
- **旧版路径**：更早版本安装到 `.codex/skills/` 下的技能会在下次 `openspec update` 时迁移。

### DeepSeek Harness [#deepseek-harness]

- **项目根目录**：DSH 使用最近的 `.git` 上级目录；不在 Git 中则使用当前目录。在那里运行 `openspec init --tools dsh`。对于嵌套的 OpenSpec 项目，把其 `.agents/skills/` 目录的绝对路径加入 DSH 的 `customSkillDirs`。名称冲突时仍以 Git 根目录下的技能优先（[上游发现规则](https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/skill/skill-filesystem)）。
- **旧副本**：2.0 之前遗留的 `.dsh/skills/` 副本（若未清理）会优先于 `.agents/skills/` 生效。`openspec update` 会移除未改动过的副本，并报告你修改过的副本。

### Devin Desktop（原 Windsurf） [#devin-desktop-formerly-windsurf]

- **两个智能体**：Devin Desktop 和 Devin Local 都运行共享技能。OpenSpec 在 2.0 之前写入 `.devin/workflows/` 的工作流会在更新时移除。
- **重命名**：`--tools windsurf` 仍解析为 `devin`。在旧版 `.windsurf/` 文件夹中存有 OpenSpec 文件的项目，会在下次 `openspec update` 时收到迁移提示。

### GitHub Copilot [#github-copilot]

- **技能**：Copilot 加载 `.agents/skills/openspec-*/SKILL.md`。以 `/openspec-<skill>` 调用技能。在 CLI 中，如果某个技能消失但其文件仍然存在，先运行 `/skills reload`，再运行 `/skills info openspec-propose` 确认已被发现。在 IDE 中，重启 IDE。
- **旧提示词文件**：OpenSpec 在 2.0 之前写入的 `.github/prompts/opsx-*.prompt.md` 文件会在更新时移除。

### GSD [#gsd]

- **项目技能**：GSD 从 [`.agents/skills/`](https://github.com/open-gsd/gsd-pi/blob/main/docs/user-docs/skills.md) 读取 OpenSpec 工作流。
- **调用**：让 GSD 使用 `openspec-<workflow>` 技能。GSD 也可以通过其技能发现设置选择匹配的技能。
- **不写子智能体文件**：[`.gsd/agents/`](https://github.com/open-gsd/gsd-pi/blob/main/docs/user-docs/subagents.md) 存放 GSD 的子智能体定义。OpenSpec 不会把工作流技能写到那里。

### Hermes Agent [#hermes-agent]

OpenSpec 把每个技能链接到项目的 `.hermes/skills/` 文件夹。Hermes v2026.6.5 及以后版本在你信任该仓库后会加载该文件夹：在项目内运行 `hermes skills trust`。在此之前，Hermes 会提示它发现了项目技能但未加载。在更早的版本中，改为把项目的 `.hermes/skills/` 文件夹加入 `~/.hermes/config.yaml` 中的 `skills.external_dirs`。init 会在安装后打印这条提醒。

### MiniMax Code [#minimax-code]

- **仅全局**：技能写入 `~/.minimax/skills/`。仓库内不写入任何内容。

### Warp [#warp]

- **OpenSpec 占用的内容**：`.warp/` 中没有任何内容。不创建也不编辑 Warp 设置和 `WARP.md`。

### 其他 / 通用（共享 `.agents` 技能） [#other--universal-shared-agents-skills]

- **适用场景**：任何读取共享 `.agents/skills/` 文件夹的工具，包括矩阵中没有对应行的工具。当你的助手未列出时，就选这一项。init 选择器的搜索框可以用 `universal`、`other`、`generic`、`custom`、`proprietary`、`unlisted`、`unsupported`、`vendor-neutral` 或 `agents.md` 找到它。
- **与其他工具并存**：所有工具读取同一个技能树。`.openspec-target` 列出项目中已配置的工具。要移除某个工具，删除它的文件夹（对没有自己文件夹的工具，则删除它在 `.openspec-target` 中的那一行）。
- **你自己的 `openspec-*` 技能**：在 OpenSpec 使用该文件夹之前就已存在于 `.agents/skills/` 的技能会被保留，绝不覆盖，并在 `.openspec-target` 中记为 `keep <skill>`。删除该技能，OpenSpec 才会写入自己的版本。
- **OpenSpec 占用的内容**：只有 `openspec-*` 文件夹和 `.openspec-target` 列表。`.agents/` 下的其他内容保持不动。
- **`AGENTS.md`**：不创建也不编辑。目标是 `.agents/` 文件夹，而不是该文件。
