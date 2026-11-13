---
source_url: https://openspec.dev/docs/skills
source_hash: sha256:ff2d31affad698cd6196725328fb001f7679f5138527c0f7b5864f4bd80fc898
translated_at: 2026-11-13T09:48:42+08:00
translation_version: 1
---

# 技能

技能分为两组：

- **Core**：默认安装，是主要的规划循环。
- **Optional**：只有你通过[配置档](./profiles.md)主动添加时才安装。

每个技能都要求项目已经在使用 OpenSpec。在它第一个会写入任何内容的步骤之前，技能会检查是否存在已解析的根目录。不存在时的行为取决于技能是如何被触达的：

- **自动选中**：你的智能体自行选择了该技能，你并未提到 OpenSpec。它会放下 OpenSpec，按平常方式回答你的请求，就像 OpenSpec 未安装时一样。
- **显式 OpenSpec 请求**：你提到了 OpenSpec，或按名称调用了该技能。它会在写入前停下并询问如何继续：在这里运行 `openspec init`、用 `--store <id>` 指向某个存储库，或不使用 OpenSpec 继续。它会等待你的回答。

按名称调用技能始终属于第二种情况。若某个项目的 `openspec/config.yaml` 指定了一个本机无法解析的存储库（未注册，或 `store:` 行格式错误），该项目不会被当作未初始化：技能会停下并显示该存储库的错误及其修复方式。这两种情况下都没有技能会自行创建 `openspec/` 目录。下面各条目描述在根目录就位后每个技能做什么。

| 技能 | 职责 | 类型 |
|---|---|---|
| [openspec-explore](#openspec-explore) | 在想法变成变更提案之前把它想清楚 | Core |
| [openspec-propose](#openspec-propose) | 一步创建变更提案及其全部规划产物 | Core |
| [openspec-apply-change](#openspec-apply-change) | 实施变更提案里的任务 | Core |
| [openspec-update-change](#openspec-update-change) | 修订变更提案的计划 | Core |
| [openspec-sync-specs](#openspec-sync-specs) | 把变更提案的规格更新合并进 `specs/` | Core |
| [openspec-archive-change](#openspec-archive-change) | 把已完成的变更提案移入归档 | Core |
| [openspec-new-change](#openspec-new-change) | 以空脚手架启动一份变更提案 | Optional |
| [openspec-continue-change](#openspec-continue-change) | 一次创建一个后续规划产物 | Optional |
| [openspec-ff-change](#openspec-ff-change) | 一趟创建变更提案以及实施所需的每一个产物 | Optional |
| [openspec-verify-change](#openspec-verify-change) | 检查实现是否与计划一致 | Optional |
| [openspec-bulk-archive-change](#openspec-bulk-archive-change) | 一次归档多个变更提案 | Optional |
| [openspec-onboard](#openspec-onboard) | 通过端到端做一份真实变更提案来学习工作流 | Optional |

下面每个条目都会点名负责下一步的技能。当你的配置档未包含该技能时，安装的文件绝不会提到它：交接会变成等效的 `openspec` 命令，或对你的一句普通请求，而仅为指向缺失技能而存在的那一行根本不会写入。因此你拥有的技能始终交接到你拥有的技能。你得到哪一组由[配置档](./profiles.md)决定。

## openspec-explore [#openspec-explore]

在想法变成变更提案之前把它想清楚。

| 契约 | 说明 |
|---|---|
| **参数** | 一个主题：一个想法、一个问题、一次比较，或一份已有变更提案的名称（在该提案的上下文中探索）。什么都不给时进入探索模式。 |
| **创建** | 默认不创建任何内容。它只阅读和调查。应你要求时它会记录洞见：在 `openspec/changes/<name>/` 下新建一份变更提案，或更新已有提案的 proposal、design、specs 或 tasks。绝不写代码。 |
| **响应** | 一段开放对话，没有必需输出。思路成型时，它会总结问题、做法、未决问题和后续步骤，并提议把这些记录下来。由你决定。实现绝不从这里开始。 |

## openspec-propose [#openspec-propose]

创建一份变更提案，并一步生成它的全部规划产物。

| 契约 | 说明 |
|---|---|
| **参数** | 一个 kebab-case 名称（`add-dark-mode`）或一段普通描述。两者都不给时会询问。 |
| **创建** | `openspec/changes/<name>/`，包含模式定义的每一个产物，按依赖顺序（spec-driven：proposal、增量规格、design、tasks）。绝不写代码。 |
| **响应** | 已创建的产物、可供审阅的状态，以及下一步。到此为止；实现要等 `openspec-apply-change`。 |

## openspec-apply-change [#openspec-apply-change]

实施变更提案里的任务，逐项推进列表，直到完成或受阻。

| 契约 | 说明 |
|---|---|
| **参数** | 变更提案名称（`add-auth`），可选。目标不明确时，它会列出活跃的变更提案并请你选择。 |
| **创建** | 代码：每个任务所需的最小改动，落在你的项目文件中。在变更提案中，它会勾选每个已完成任务（`- [ ]` 变为 `- [x]`），位置由 `sourcePath` 和从 1 开始的 `line` 指定的被跟踪文件决定。模式可能跨多个文件跟踪任务。 |
| **响应** | 每个任务的进展，然后是总体计数（N/M 个任务完成）。全部完成：建议 `openspec-archive-change`。因缺少产物而受阻：指向 `openspec-continue-change`；若未安装该技能（core 配置档不含它），则指向 `openspec status` 和 `openspec instructions`。任务不清或出错：暂停并询问。 |

## openspec-update-change [#openspec-update-change]

修订变更提案已有的规划产物，并保持它们彼此一致。

| 契约 | 说明 |
|---|---|
| **参数** | 变更提案名称，可选，加上你想要的修订。未说明修订时，它会做一次一致性审查：交叉检查各产物之间的矛盾、缺口和重复。 |
| **创建** | 编辑已存在的产物文件。一个例外：对于以 glob 形式书写、例如 `specs/**/*.md` 且已有至少一个文件的产物，在你确认路径后它可以添加缺失的配套文件。尚无任何文件的产物属于 `openspec-continue-change` 的职责。缺少该技能时（core 配置档不含它），改为指向 `openspec status` 和 `openspec instructions`。绝不写代码。 |
| **响应** | 逐次展示每处拟议修订，仅在你确认后才写入，一次一个产物。结束时说明修订了什么以及下一步；实现要等 `openspec-apply-change`。 |

## openspec-sync-specs [#openspec-sync-specs]

把变更提案的规格更新合并进 `specs/`，而不归档它。

| 契约 | 说明 |
|---|---|
| **参数** | 变更提案名称，可选。你也可以只指定其增量规格中的一部分，那就只同步那些。 |
| **创建** | 为每个增量规格编辑或创建 `openspec/specs/<capability-path>/spec.md`，把新增、修改、移除和重命名的需求合并进主规格。绝不写代码。 |
| **响应** | 在更新后的规格通过校验后，按能力汇总新增、修改、移除或重命名的需求。变更提案保持活跃；归档要等 `openspec-archive-change`。 |

## openspec-archive-change [#openspec-archive-change]

把已完成的变更提案移入归档。

| 契约 | 说明 |
|---|---|
| **参数** | 变更提案名称，可选。 |
| **创建** | 把变更提案文件夹移到 `openspec/changes/archive/YYYY-MM-DD-<name>/`（若名称已以日期开头则不再加日期）。经你批准，它会先同步尚未处理的增量规格。安装了 `openspec-sync-specs` 时，它运行该工作流；否则由它自己把增量规格合并进主规格。绝不写代码。 |
| **响应** | 产物或任务不完整时，归档前会警告并询问；存在增量规格时还会问是否同步。结束时给出摘要：名称、模式、归档位置、规格同步状态以及任何警告。 |

## openspec-new-change [#openspec-new-change]

以空脚手架启动一份变更提案。

| 契约 | 说明 |
|---|---|
| **参数** | 一个 kebab-case 名称（`add-user-auth`）或一段普通描述；仅在非默认工作流时再给一个模式名。两者都不给时会问你想要构建什么。 |
| **创建** | `openspec/changes/<name>/` 作为空脚手架：还没有任何产物，绝不写代码。 |
| **响应** | 脚手架的名称和位置、该工作流的产物顺序、状态（0/N 完成），以及第一个产物的模板。起草产物要等 `openspec-continue-change`。 |

## openspec-continue-change [#openspec-continue-change]

在变更提案中一次创建一个后续规划产物。

| 契约 | 说明 |
|---|---|
| **参数** | 变更提案名称，可选。若仍不明确，它会请你从最近修改过的提案中挑选。 |
| **创建** | 模式序列中下一个就绪的单个产物，写入变更提案文件夹。每次运行一个产物，绝不写代码。 |
| **响应** | 已创建的产物、进度（共 M 个，完成 N 个），以及由此解锁了哪些产物。规划完成时它会说明；实现转到 `openspec-apply-change`。 |

## openspec-ff-change [#openspec-ff-change]

一趟创建一份变更提案以及实施所需的每一个规划产物。

| 契约 | 说明 |
|---|---|
| **参数** | 一个 kebab-case 名称或一段普通描述。两者都不给时会询问。若同名变更提案已存在，它会建议改为继续该提案。 |
| **创建** | `openspec/changes/<name>/` 以及实施所需的每一个规划产物，按依赖顺序（spec-driven：proposal、specs、design、tasks），只略去标记为跳过或条件性的产物。绝不写代码。 |
| **响应** | 变更提案的名称和位置、创建的每一个产物，以及被跳过的条件性产物及原因。到此为止；实现要等 `openspec-apply-change`。 |

## openspec-verify-change [#openspec-verify-change]

检查实现是否与变更提案的产物一致。

| 契约 | 说明 |
|---|---|
| **参数** | 变更提案名称，可选。不明确时它会询问，并列出带有 tasks 产物的变更提案。 |
| **创建** | 无。它阅读变更提案的产物和代码库。校验只输出报告。 |
| **响应** | 一份报告：完整性（Completeness）、正确性（Correctness）和一致性（Coherence）的评分卡，然后是 CRITICAL、WARNING 和 SUGGESTION 级问题及建议，最后是归档就绪性评估。它不改变任何东西，也不归档。 |

## openspec-bulk-archive-change [#openspec-bulk-archive-change]

一次归档多个变更提案。

| 契约 | 说明 |
|---|---|
| **参数** | 无。它列出活跃的变更提案并请你任意多选，另有全选选项。若没有活跃的提案，它会说明并停止。 |
| **创建** | 为每个被归档的变更提案创建 `openspec/changes/archive/YYYY-MM-DD-<name>/`（已带日期的名称保留其前缀）。每份提案的增量规格会先通过 `openspec-sync-specs` 同步。绝不写代码。 |
| **响应** | 每份变更提案一张状态表，整批只需一次确认，然后给出已归档、已跳过和失败的摘要，以及规格同步结果。当两份变更提案触及同一份规格时，它会检查代码库，并按最旧的优先同步已实施的增量。 |

## openspec-onboard [#openspec-onboard]

通过端到端做一份真实变更提案来学习工作流。

| 契约 | 说明 |
|---|---|
| **参数** | 无。它会扫描你的代码库寻找小型入门任务，请你挑一个或描述你自己的任务。 |
| **创建** | 为所选任务创建一份真实的变更提案，一次一个产物，然后在你确认实施后写真实代码。最后归档该变更提案。 |
| **响应** | 对完整循环的讲解式走查，并在需要你输入时暂停：探索、创建、逐个构建产物、实施、归档。结束时给出回顾以及指向 `openspec-propose` 的提示。大约需要 15 到 20 分钟。 |
