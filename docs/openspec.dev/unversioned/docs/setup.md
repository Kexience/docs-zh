---
source_url: https://openspec.dev/docs/setup
source_hash: sha256:c86caf9e4413e9b107b24d44242f7544e7f3727917f5688f3fcfb6c0745300ea
translated_at: 2026-11-13T09:48:42+08:00
translation_version: 1
---

# 配置你的项目

## 选择 OpenSpec 存放的位置 [#pick-where-openspec-lives]

- **在你的仓库中（默认）**：规格和变更就放在它们所描述的代码旁边，并随代码一起做版本管理。本页其余部分都按这种方式展开。
- **在存储库中**：一个独立的规划仓库，由使用它的各个仓库共享，适用于多仓库场景，或希望把规划完全放在仓库之外。什么情况下值得这样做、以及如何建立一个存储库，见[存储库（beta）](./stores.md)。

## 初始化你的项目 [#initialize-your-project]

装好 CLI（[安装](./installation.md)）后，在项目根目录运行 init。在你的终端中：

```bash
cd <your-project>
openspec init
```

init 会问你在用哪些 AI 工具，为你选中的工具写入工作流文件，并报告结果：

```
OpenSpec Setup Complete

Created: Claude Code
6 skills in .agents/skills/ (linked from .claude/skills/)
Config: openspec/config.yaml (schema: spec-driven)
```

如果你的工具运行在 IDE 中，请重启它，以便加载新的技能。

重复运行 init 是安全的：

- 你已设置好的工具会打印 `Refreshed` 而不是 `Created`。
- 再次运行 init 并选中新工具，就会添加该工具。
- `--tools` 参数会跳过选择器（[CLI 参考](./cli.md)）。

### 迁移已有的 `project.md` [#migrate-an-existing-projectmd]

init 不会把旧版的 `openspec/project.md` 复制到 `config.yaml`。它会保留该文件，并打印一条由 AI 协助迁移的请求。

在你的 AI 对话中：

```
Review openspec/project.md and migrate its useful content to openspec/config.yaml.
Keep context concise: include only project-wide facts needed during artifact creation, apply, and archive.
Move artifact-specific guidance into rules for the matching artifacts.
Move guidance for apply or archive into the matching operations entry.
Leave out generic, outdated, or verbose material. Do not delete project.md.
```

检查 `config.yaml`，准备好后删除 `project.md`。

## init 会安装什么 [#what-init-installs]

运行 init 会在你的项目中创建两样东西：

- 仓库根目录下的 `openspec/` 文件夹
- 工作流文件：技能放在共享的 `.agents/skills/` 文件夹中，需要时从工具自己的文件夹建立链接（例如 `.claude/skills/`）

像提交其他源码一样把它们全部提交。

init 还会删除旧版本生成的命令文件，并保留你编辑过的那些。1.0 之前设置的项目还有更早的遗留物：像 `.claude/commands/openspec/` 这样的文件夹，以及 `CLAUDE.md`、`AGENTS.md` 这类文件中的 OpenSpec 标记块。交互式 init 会在删除前询问。使用 `--force`、`--tools` 或非交互运行时，init 会不经询问直接删除，包括这些块中的任何修改，所以请先备份。

### `openspec/` 文件夹 [#the-openspec-folder]

每个 OpenSpec 产物都放在这里，即项目根目录下。大致结构如下：

```
openspec/
├── config.yaml     project settings and context for the AI
├── specs/          your specs (empty for now)
└── changes/        in-motion changes (empty for now)
    └── archive/    completed changes move here
```

[项目配置](./project-config.md)介绍了 `config.yaml`。

### 工作流文件（技能） [#the-workflow-files-skills]

这些就是 OpenSpec 的工作流，也就是你工作中会用到的一系列动作。以下是安装在共享 `.agents/skills/` 文件夹中的技能：

```
.agents/skills/
├── openspec-explore/              think through an idea first
├── openspec-propose/              propose a change
├── openspec-apply-change/         implement a change's tasks
├── openspec-update-change/        revise a change's plan
├── openspec-sync-specs/           sync a change's spec updates into specs/
├── openspec-archive-change/       move a finished change to the archive
├── openspec-verify-change/        check the implementation matches the plan (not included by default)
└── openspec-bulk-archive-change/  archive several changes at once (not included by default)
```

这是默认集合加上两个可选工作流。[配置档](./profiles.md)列出了全部十二个。

无论你设置了多少工具，每个技能只在这里写一次。不读取 `.agents/skills/` 的工具（Claude Code、Kiro 等）会在自己的文件夹中得到指向每个技能的链接，例如 `.claude/skills/openspec-propose`。MiniMax Code 是唯一的例外：它的技能放到主文件夹下的 `~/.minimax/skills/`。[支持的工具](./supported-tools.md#where-skills-go)展示了目录布局以及哪些工具会获得链接。

每个工作流都是一个**技能**：你要求做这件事时智能体会读取的指令，或者你按名称调用的指令（Claude Code 中是 `/openspec-apply-change`，Codex 中是 `$openspec-apply-change`）。[支持的工具](./supported-tools.md#support-matrix)列出了各工具的写法。

OpenSpec 1.x 还会为每个工作流写一个命令文件（`/opsx:apply`）。OpenSpec 2.0 只安装技能。[升级到 2.0](./upgrade-to-2.md)介绍了有哪些变化。

#### 更改安装内容 [#change-what-gets-installed]

交互式选择器会改变工作流集合（[配置档](./profiles.md)）。在你的终端中：

```bash
openspec config profile
```

对“Apply changes to this project now?”回答 yes 会在当场应用。其他项目会在下次 `openspec update` 时采用。该设置是全局的，按机器生效。

#### Claude Code 不显示工作流 [#claude-code-doesnt-show-the-workflows]

Claude Code 从 `.claude/skills/openspec-*` 加载 OpenSpec 技能，这些链接指向 `.agents/skills/openspec-*`。如果它们缺失，刷新项目。在你的终端中：

```bash
openspec update
```

重启 Claude Code，然后在其对话中运行 `/openspec-propose`。如果只缺少部分工作流，[更改你的配置档](./profiles.md#expanding-the-set-optional-workflows)。

设置完成。[快速上手](./quickstart.md)会从这里带你完成第一个变更。
