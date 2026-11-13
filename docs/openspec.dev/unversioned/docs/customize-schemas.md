---
source_url: https://openspec.dev/docs/customize-schemas
source_hash: sha256:59ff4a3dd54ed8bde7ea5ada4bdf21768f07762b768cc970867f5fbd0ce89574
translated_at: 2026-11-13T09:48:42+08:00
translation_version: 1
---

# 模式

一个模式定义变更提案会产出什么：哪些产物、按什么顺序、来自哪些模板。例如，默认内置的模式 [spec-driven](./schemas/spec-driven.md) 大致按以下顺序产出这四个产物，每一个都建立在前一个之上：

```
proposal → specs → design → tasks
```

如果你希望这些是不同的文档——更少、名称不同或结构不同——就分叉（fork）一个模式。

## 模式存放在哪里 [#where-schemas-live]

OpenSpec 按顺序在三处查找模式，并使用最先找到的那一个：

1. **你的项目**：`openspec/schemas/`，随仓库提交，这样整个团队都能拿到。
2. **本机**：macOS 和 Linux 上是 `~/.local/share/openspec/schemas`（若设置了 `$XDG_DATA_HOME` 则在其下），Windows 上是 `%LOCALAPPDATA%\openspec\schemas`。这里的模式在你参与的每个项目中都可用。
3. **安装包**：像 `spec-driven` 这样的内置模式随 openspec 本身一起发布。

同一个名称可以存在于多处，更具体的位置优先。`openspec schema which` 会显示正在使用的是哪一份副本：

```
$ openspec schema which spec-driven
Schema: spec-driven
Source: project
Path: /your-project/openspec/schemas/spec-driven

Shadows:
  package: .../openspec/schemas/spec-driven
```

## 模式里有什么 [#whats-in-a-schema]

一个模式由一个文件夹中的纯文本文件定义：一个声明各产物的 schema.yaml，以及每个产物对应的一份模板。下面是内置的 `spec-driven`：

```
spec-driven/
├── schema.yaml
└── templates/
    ├── proposal.md
    ├── spec.md
    ├── design.md
    └── tasks.md
```

- **schema.yaml**：声明每个产物、它生成的文件、它起始所用的模板、它首先需要什么，以及智能体创建它时收到的指令。每个字段的约定见 [schema.yaml](./schemas/schema-yaml.md)。
- **templates/**：每个产物一个 Markdown 骨架，由智能体填写。

下面是 schema.yaml 中 tasks 产物的条目（已删减）：

```yaml
artifacts:
  - id: tasks
    generates: tasks.md
    description: Implementation checklist with trackable tasks
    template: tasks.md
    instruction: |
      ...what the agent is told when creating tasks.md...
    requires:
      - specs
      - design
```

内置模式随 openspec 包发布，所以永远不要就地编辑它们。要得到自己的副本，请分叉。

## 创建自己的自定义模式 [#creating-your-own-custom-schema]

有两种方式获得自己的模式：

1. **分叉现有模式**并编辑自己的副本。如果现有模式接近你想要的效果，从这里开始，因为它里面的一切已经可用。
2. 如果都不合适，就**从零开始**，用 `openspec schema init` 搭建一个空模式的骨架。

### 分叉现有模式 [#fork-an-existing-schema]

1. 从项目根目录运行命令，分叉你想作为起点的模式：

   ```console
   $ openspec schema fork spec-driven

   Note: Schema commands are experimental and may change.
   ✔ Forked 'spec-driven' to 'spec-driven-custom'

   Source: .../openspec/schemas/spec-driven (package)
   Destination: /your-project/openspec/schemas/spec-driven-custom
   ```

   传入第二个参数来指定名称（`openspec schema fork spec-driven team-flow`）。名称采用 kebab-case。

2. 编辑副本：schema.yaml 和模板。[编辑你的分叉](#editing-your-fork)说明了要改什么。

3. 校验它：

   ```bash
   openspec schema validate spec-driven-custom
   ```

   这是唯一能在你做到一半之前发现坏模式（缺模板、YAML 有误、依赖环）的命令。

4. 在 openspec/config.yaml 中让项目指向它。这一步需要你来做，因为分叉不会改动 config.yaml：

   ```yaml
   schema: spec-driven-custom
   ```

5. 新的变更提案现在会遵循你的模式。之前创建的变更仍保留其创建时所用的模式。

要在不改动 config.yaml 的情况下处处替换默认模式，就以相同名称分叉：`openspec schema fork spec-driven spec-driven`。这样你的项目副本会遮蔽内置模式，如[模式存放在哪里](#where-schemas-live)所述。

### 从零开始 [#start-from-scratch]

`openspec schema init` 会搭建一个新模式的骨架，而不是复制现有模式：

```console
$ openspec schema init lite --description "Lite flow" --artifacts proposal,tasks

✔ Created schema 'lite'
Schema created at: /your-project/openspec/schemas/lite
Artifacts: proposal, tasks
```

骨架是空白的。产物只取自内置的四个 ID，生成的模板不带任何说明，所以在你自己写之前，智能体得到的指引更少。之后，分叉的步骤同样适用：先校验，再让 config.yaml 指向它。

## 编辑你的分叉 [#editing-your-fork]

分叉有两类文件要编辑：

- **templates/** 改变每个文档的骨架。给 tasks 模板加一节，每个新的 tasks.md 就会以它开头。保留第一行的 `#` 标题：产物会继承它，因此每个生成的文件打开时都是带标题的文档。
- **schema.yaml** 改变工作流本身：存在哪些产物、每个产物首先需要什么，以及智能体创建它时收到的指令。

例如，要去掉设计文档以获得更精简的流程：

1. 从 schema.yaml 删除 `design` 条目。
2. 从 `tasks` 的 `requires` 列表中移除 `design`。
3. 校验：

   ```console
   $ openspec schema validate spec-driven-custom

   ✓ Schema 'spec-driven-custom' is valid
   ```

跳过第 2 步，校验就会发现它：

```console
✗ Schema 'spec-driven-custom' has errors:
  error: Invalid dependency reference in artifact 'tasks': 'design' does not exist
```

每次手动编辑后都要校验。否则坏模式会在变更进行到一半、工作流请求一个并不存在的文件时才暴露出来。与 config.yaml 一样，模式的修改会在下一次运行时到达智能体。

## 分叉是一个快照 [#a-fork-is-a-snapshot]

`openspec update` 会刷新已安装的技能，但从不触碰 `openspec/schemas/`。你的分叉完全按你离开时的样子继续工作，这也意味着当内置模式演进时，它不再获得这些改进。若日后想采纳，请以新名称再次分叉内置模式，再把差异移植过来。

## 共享模式 [#sharing-schemas]

共享一个模式就是复制它的文件夹。

- **与团队共享**：提交 `openspec/schemas/`，仓库上的每个人都会用到它。
- **跨项目共享**：把文件夹放到[模式存放在哪里](#where-schemas-live)所述的用户级目录中。
- **来自社区**：[社区目录](https://github.com/Fission-AI/OpenSpec/blob/main/docs/customization.md#community-schemas)列出了共享的模式。复制一个到 `openspec/schemas/<name>`，它就会像你自己的模式一样工作。

模式注册表（公开与私有）正在开发中，届时模式可按名称安装，无需手动复制。

### 配合 Superpowers 使用 OpenSpec [#use-openspec-with-superpowers]

社区维护的 [`superpowers-bridge`](https://github.com/JiangWay/openspec-schemas/tree/main/superpowers-bridge) 模式把 OpenSpec 产物连接到 [Superpowers](https://github.com/obra/superpowers) 的执行技能。把它复制进项目前，请先阅读该桥接的安装与兼容性说明。

该桥接在 OpenSpec 之外单独发布。OpenSpec 不测试其 Superpowers 集成，也不为其管理版本。
