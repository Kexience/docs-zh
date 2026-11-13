---
source_url: https://openspec.dev/docs/profiles
source_hash: sha256:9f3b7d9addca40a0077f9ff107b2599ff3ae833b1ea1a73e9026e3ef2d53a1bc
translated_at: 2026-11-13T09:48:42+08:00
translation_version: 1
---

# 配置档

配置档表达的是你的偏好：在你的机器上安装哪些 OpenSpec 工作流（也就是 AI 工具里的[技能](./setup.md#the-workflow-files-skills)）。默认配置档是 `core`。增删工作流后，你的选择会保存为 `custom` 配置档。

## 核心集合 [#the-core-set]

`core` 配置档安装六个工作流，覆盖从想法到归档的整个循环：

| 工作流 | 用途 |
|---|---|
| [`explore`](./skills.md#openspec-explore) | 在想法变成变更提案之前把它想透 |
| [`propose`](./skills.md#openspec-propose) | 创建变更提案，并一步生成它的全部规划产物 |
| [`apply`](./skills.md#openspec-apply-change) | 实施变更提案中的任务 |
| [`update`](./skills.md#openspec-update-change) | 修订变更提案已有的规划产物 |
| [`sync`](./skills.md#openspec-sync-specs) | 把变更提案的规格更新合并进 `specs/`，但不归档 |
| [`archive`](./skills.md#openspec-archive-change) | 把已完成的变更提案移入归档 |

每一项都链接到它的完整约定：参数、它创建什么、它如何回应。

## 扩展集合：可选工作流 [#expanding-the-set-optional-workflows]

核心集合之外还有六个工作流。其中三个（`new`、`continue`、`ff`）逐个产物地创建变更提案，而不是像 `propose` 那样一次全建。

| 工作流 | 用途 |
|---|---|
| [`new`](./skills.md#openspec-new-change) | 以一个空脚手架开始一个变更提案 |
| [`continue`](./skills.md#openspec-continue-change) | 在变更提案中一次创建一个规划产物 |
| [`ff`](./skills.md#openspec-ff-change) | 一次创建变更提案以及实现所需的全部规划产物 |
| [`verify`](./skills.md#openspec-verify-change) | 检查实现是否与变更提案的产物一致 |
| [`bulk-archive`](./skills.md#openspec-bulk-archive-change) | 一次归档多个变更提案 |
| [`onboard`](./skills.md#openspec-onboard) | 通过完整做一个真实的变更提案来学习这套工作流 |

要改变这个集合，运行交互式选择器：

```bash
openspec config profile
```

选择器把全部十二个工作流列为复选框，已安装的会被勾选。只要选择结果不恰好是核心六个，就会保存为 `custom` 配置档，因此你也可以取消勾选你用不到的核心工作流。

## 交付方式（2.0 中已废弃） [#delivery-retired-in-20]

OpenSpec 2.0 只安装技能，因此 `delivery` 设置不再改变任何东西。已有的值会保留。`openspec config set delivery <value>` 仍会保存该值，并打印一条提示说明它没有效果。

在 1.x 中，delivery 用于选择安装技能、命令，还是两者都装。命令文件会怎样，见[升级到 2.0](./upgrade-to-2.md)。

## 切换配置档 [#switching-profiles]

切换分两步：先在机器上改变配置档，然后更新每个项目以应用它。

1. 改变配置档：

   ```bash
   openspec config profile        # interactive
   openspec config profile core   # reset to the core six
   ```

2. 在你工作的每个项目里运行更新：

   ```bash
   openspec update
   ```

如果你当前所在的目录已经是一个 OpenSpec 项目，交互流程会主动提出在那里替你执行第 2 步。
