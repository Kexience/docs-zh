---
source_url: https://openspec.dev/docs/glossary
source_hash: sha256:eab361043e82b59cc37e46b472ec01b1f447a6f65f7b084dbf11a8361bf8e34d
translated_at: 2026-11-13T09:48:42+08:00
translation_version: 1
---

# 术语表

OpenSpec 复用了一些在 git、CI 和智能体工具中含义不同的词。每一行给出 OpenSpec 的含义。最后一列在有更多细节时给出链接。

| 术语 | 释义 | 更多 |
|---|---|---|
| **实施** | 实施变更提案中的任务。技能：`openspec-apply-change`。 | [实施变更](./skills.md#openspec-apply-change) |
| **归档** | 完成变更提案：把它的增量合并进主规格，并把它的文件夹移到 `openspec/changes/archive/`。 | [快速开始](./quickstart.md) |
| **产物** | 变更提案中的规划文档：`proposal.md`、增量规格、`design.md`、`tasks.md`。不是构建产物。 | [产物](./schemas/spec-driven.md#artifacts) |
| **能力** | 你系统中的一个行为领域。每个能力在 `openspec/specs/<capability>/spec.md` 有一份规格。 | [能力](./schemas/spec-driven.md#proposalmd) |
| **变更提案** | 一个工作单元：`openspec/changes/<name>/` 下的一个文件夹，存放它的规划产物。常简称为“变更”。不是 git commit。 | [提案](./quickstart.md#step-2-propose) |
| **命令** | 在 OpenSpec 1.x 中，工作流的可输入入口（`/opsx:propose`、`/opsx-propose`）。OpenSpec 2.0 只安装技能。 | [支持的工具](./supported-tools.md) |
| **继续** | 为已有的变更提案创建下一个规划产物。技能：`openspec-continue-change`。 | [技能](./skills.md) |
| **交付方式** | 在 1.x 中，工作流的安装方式：作为技能、命令，或两者兼有。2.0 已弃用。 | [升级到 2.0](./upgrade-to-2.md) |
| **增量规格** | 变更提案中的规格，只在 `ADDED`、`MODIFIED`、`REMOVED` 和 `RENAMED` 标题下列出发生变化的内容。 | [增量规格](./schemas/spec-driven.md#delta-specs-specmd) |
| **探索** | 在提案之前与智能体一起把想法想透。不写代码。技能：`openspec-explore`。 | [探索一个想法](./skills.md#openspec-explore) |
| **快进** | 一次创建包含所有规划产物的变更提案，可直接实施。技能：`openspec-ff-change`。不是 git fast-forward。 | [技能](./skills.md) |
| **旧版工作流** | OPSX 之前的 `/openspec:*` 命令。 |  |
| **循环** | 变更提案经历的周期：探索、提案、评审、实施、归档。 | [快速开始](./quickstart.md) |
| **主规格** | `openspec/specs/` 这棵树：你系统当前已商定的行为。归档会把增量合并进它。尚无规格的能力会由其 `ADDED` 需求生成一份。 | [归档](./quickstart.md#step-5-archive) |
| **OpenSpec 根目录** | 命令解析并作用的 `openspec/` 树：你仓库的，或某个存储库的。 | [存储库](./stores.md#where-artifacts-get-created-when-using-stores) |
| **OPSX** | 当前的 OpenSpec 工作流系统。它的 1.x 命令使用 `/opsx:` 前缀。 |  |
| **配置档** | init 安装哪些工作流：`core` 或 `custom`。 | [配置档](./profiles.md) |
| **提案** | 创建变更提案并在一步内生成它的所有规划产物。技能：`openspec-propose`。 | [快速开始](./quickstart.md) |
| **注册表** | 机器级的已注册存储库列表，位于 `registry.yaml`。不是包注册表。 | [CLI](./cli.md#openspec-store) |
| **需求** | 系统必须具备的一项行为，用 SHALL 书写：规格中的 `### Requirement:`。 | [增量规格](./schemas/spec-driven.md#delta-specs-specmd) |
| **场景** | 需求下的一个可测试示例，采用 WHEN/THEN 形式。 | [增量规格](./schemas/spec-driven.md#delta-specs-specmd) |
| **模式** | 定义一个变更提案产出哪些产物、以什么顺序产出。不是 JSON Schema。 | [模式](./schemas.md) |
| **技能** | 工作流的指令，安装到你的 AI 工具读取的位置（`.agents/skills/` 等）。 | [技能](./skills.md) |
| **规格** | 描述某个能力当前行为的文件，位于 `openspec/specs/<capability>/spec.md`。 | [归档](./quickstart.md#step-5-archive) |
| **spec-driven** | 默认模式：提案，然后是增量规格，然后是设计，然后是任务。 | [spec-driven](./schemas/spec-driven.md) |
| **存储库** | 在你机器上注册的独立 OpenSpec 仓库，用于跨仓库的规划。不是数据存储。 | [存储库（beta）](./stores.md) |
| **同步** | 在不归档的情况下把已实施的增量合并进主规格。技能：`openspec-sync-specs`。 | [技能](./skills.md) |
| **模板** | 模式为每个产物提供的起始内容。 | [模式](./customize-schemas.md) |
| **更新** | 作为技能（`openspec-update-change`）：修订变更提案的规划产物。作为 CLI 命令（`openspec update`）：刷新 OpenSpec 已安装的文件。 | [更新变更](./skills.md#openspec-update-change)、[CLI](./cli.md) |
| **校验** | 归档前检查实现与变更提案的产物一致。技能：`openspec-verify-change`。 | [技能](./skills.md) |
| **工作流** | 一个具名的 OpenSpec 动作（提案、实施、归档……），作为技能安装进你的 AI 工具。 | [设置你的项目](./setup.md) |
| **工作集** | 在同一个工具中一起打开的个人本地文件夹组。不是存储库，也不共享任何内容。 | [工作集（beta）](./worksets.md) |
