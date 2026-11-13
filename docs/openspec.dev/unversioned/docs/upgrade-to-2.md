---
source_url: https://openspec.dev/docs/upgrade-to-2
source_hash: sha256:9a7c9ae016673344279ac09d44a69729fe01001be3bc2dd392723df73694cd58
translated_at: 2026-11-13T09:48:42+08:00
translation_version: 1
---

# 升级到 2.0

要升级，先更新 CLI，然后在每个项目中运行 `openspec update`。你的技能会移入一个共享文件夹，旧的命令文件会被移除。你编辑过的旧命令文件和旧技能副本会保留。

> [!WARNING]
> `update` 会替换你在 OpenSpec 安装到 `.agents/skills/` 的技能内部所做的修改，且不保留副本。请先保存这些修改：[你定制过的技能](#skills-you-customized)。

## 有哪些变化 [#what-changes]

| | 1.x | 2.0 |
|---|---|---|
| 技能存放位置 | 每个工具自己的文件夹里各一份副本 | `.agents/skills/` 中一份副本，为需要的工具建立链接 |
| 命令文件（`/opsx:propose`） | 安装在技能旁边 | 已移除。改用技能，它们做同样的工作 |
| `delivery` 设置 | 技能、命令或两者 | 已废弃：一切都是技能 |
| Amazon Q Developer | 提示词文件和技能 | 已弃用：它无法加载技能。`update` 会移除它的 OpenSpec 文件；请改用 Kiro |

[支持的工具](./supported-tools.md#where-skills-go)展示了新的布局以及哪些工具会获得链接。

## 升级一个项目 [#upgrade-a-project]

先提交你的工作，以便能回到那个状态。这个提交也是你在 `.agents/skills/` 中某个技能内部所做修改的唯一副本。`git stash` 无法保存升级本身，因为 git 无法暂存一个变成链接的文件夹。

**1. 更新 CLI**，按你当初安装的方式（[更新](./installation.md#updating)）。

**2. 在每个项目中运行 update。** 在你的终端中：

```bash
openspec update
```

**3. 提交结果。** 链接会像其他文件一样被提交。

再次运行 `update` 不会有任何变化。

## update 做了什么 [#what-update-does]

- **技能**：只写入 `.agents/skills/` 一次，在工具需要时从其自己的文件夹建立链接（例如 `.claude/skills/`）。
- **旧技能副本**：旧版本写入各工具文件夹的副本会被移除。
- **命令文件**：旧版本生成的命令文件会被移除。
- **你编辑过的旧文件**：编辑过的命令文件，或工具自己文件夹中被编辑过的技能副本，会保留并列出。后面几节说明如何处理它们。
- **OpenSpec 安装的技能**：就地刷新，与每次 1.x 更新一样。其中的修改会被替换。`update` 会点名每个发生这种情况的技能。
- **链接**：绝不会被跟踪到项目之外。
- **项目之外**：`update` 只改动你的全局配置、MiniMax Code 的 `~/.minimax/skills/`，以及 `~/.codex/prompts/` 中的旧 OpenSpec 提示词。只有在使用 `--force` 或你确认之后，它才会移除这些提示词。

## 旧命令与对应的技能 [#old-commands-and-their-skills]

每个 1.x 命令都有一个指令相同的技能：

| 1.x 命令 | 2.0 技能 |
|---|---|
| `/opsx:propose` | `openspec-propose` |
| `/opsx:explore` | `openspec-explore` |
| `/opsx:apply` | `openspec-apply-change` |
| `/opsx:update` | `openspec-update-change` |
| `/opsx:sync` | `openspec-sync-specs` |
| `/opsx:archive` | `openspec-archive-change` |
| `/opsx:new` | `openspec-new-change` |
| `/opsx:continue` | `openspec-continue-change` |
| `/opsx:ff` | `openspec-ff-change` |
| `/opsx:verify` | `openspec-verify-change` |
| `/opsx:bulk-archive` | `openspec-bulk-archive-change` |
| `/opsx:onboard` | `openspec-onboard` |

你也可以直接说出要做的事（"为添加深色模式做提案"）。要按名称调用技能，在 Claude Code 和大多数其他工具中输入 `/openspec-propose`，在 Codex 中输入 `$openspec-propose`。[支持的工具](./supported-tools.md#support-matrix)列出了各工具的写法。

## 你编辑过的命令文件 [#command-files-you-edited]

`update` 只删除与 OpenSpec 生成内容一致的命令文件。你改动过的会被保留并列出：

```
Kept 1 command file that does not match what OpenSpec generated (likely edited):
  .claude/commands/opsx/apply.md
Move anything worth keeping into the skill, then delete by hand.
```

你的工具可能仍会把保留下来的文件显示为命令。把需要的内容移走后，就删除它。

1.0 之前设置的项目有更旧的文件，例如 `.claude/commands/openspec/`。当它们与早期版本一致时，`update` 会不经询问直接删除。否则会先询问，非交互运行则不动它们。使用 `--force` 时，无论是否编辑过都会直接删除，所以请先备份。

## 你编辑过的技能文件夹 [#skill-folders-you-edited]

`update` 还会保留你在工具自己文件夹中编辑过的旧技能副本。同时读取自己文件夹和 `.agents/skills/` 的工具可能会把该技能加载两次。把需要的内容移走后，就删除保留下来的文件夹。

MiniMax Code 把技能放在 `~/.minimax/skills/`。当 `update` 刷新你在那里编辑过的技能时，它会先把你的副本另存为旁边的 `SKILL.md.bak`。

## 你定制过的技能 [#skills-you-customized]

`update` 会重写 OpenSpec 安装在 `.agents/skills/` 中的每个技能，例如 `.agents/skills/openspec-propose/SKILL.md`。1.x 中也是如此。如果你编辑过其中某个，你的修改会被替换且不会备份。`update` 会告诉你是哪些技能：

```
Replaced your edits in 1 skill OpenSpec installs: .agents/skills/openspec-propose/SKILL.md. OpenSpec refreshes this skill on every update and keeps no copy. Recover your text from git, and keep lasting changes in a skill of your own under another name.
```

要在任何改动发生前查看受影响的技能，运行 `openspec update --dry-run`。它会打印一条注明这些技能的提示。

要让定制内容跨更新保留，就把它放在 `update` 不会写入的地方：

- **项目指令**：`openspec/config.yaml` 中的 `context` 和 `rules` 能把你的指令交给智能体，而无需编辑技能（[项目配置](./project-config.md)）。
- **你自己的技能**：名称不以 `openspec-` 开头的技能，例如 `.agents/skills/team-propose/`。`update` 从不触碰它。

## 为提交的链接配置 Windows [#set-up-windows-for-committed-links]

链接会像其他文件一样被提交。Windows 上的团队成员需要两项设置才能把它们检出为链接：

**1. 在 git 中开启链接。** 在你的终端中：

```bash
git config --global core.symlinks true
```

或者用 `git clone -c core.symlinks=true <url>` 克隆。

**2. 开启开发者模式**（在 Windows 设置中），以便能创建链接。

没有这两项设置，每个链接会被检出成一个小的文本文件。`openspec update` 会用技能的普通副本替换它。

## 链接 OpenSpec 未支持的工具 [#link-a-tool-that-openspec-doesnt]

大多数工具直接读取 `.agents/skills/`。如果你的工具只读取自己的文件夹，[链接另一个工具](./supported-tools.md#link-another-tool)展示了让它指向共享副本的那一条命令。

## 继续使用 1.x [#stay-on-1x]

你不必马上升级。1.x 会照原样继续工作。按你当初安装的方式锁定版本。

用 npm 时，在你的终端中：

```npm
npm install -g @fission-ai/openspec@1
```

使用独立安装时，指定发行版本（[安装选项](./installation.md#install-options)）：

```bash
curl -fsSL https://openspec.dev/cli/install.sh | OPENSPEC_VERSION=v1.17.0 sh
```

在 Windows 上（PowerShell）：

```powershell
$env:OPENSPEC_VERSION = 'v1.17.0'
irm https://openspec.dev/cli/install.ps1 | iex
```

当 `openspec update` 提议升级 CLI 时，拒绝它。要停止该提议，设置 `OPENSPEC_NO_UPDATE_CHECK=1`。
