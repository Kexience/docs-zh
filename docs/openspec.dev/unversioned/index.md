---
source_url: https://openspec.dev/llms.txt
source_hash: sha256:1aa4733db6a696fadd6e841eab6b3c943e280419d6ddb88022ad9dde08d3ad02
translated_at: 2026-11-13T09:45:00+08:00
translation_version: 1
---

# OpenSpec 文档

本目录是 openspec.dev 官方文档的中文译本，按站点的导航分组编排。

## 开始

- [安装](./docs/installation.md) —— 在你的机器上安装 openspec CLI、更新它、卸载它。
- [配置你的项目](./docs/setup.md) —— 把 OpenSpec 加入一个项目：运行 init，看看它写了什么，再做调整。
- [快速入门](./docs/quickstart.md) —— 你的第一个变更，从想法到归档，在新项目或已有项目里完成。
- [升级到 2.0](./docs/upgrade-to-2.md) —— OpenSpec 2.0 有哪些变化，以及如何把项目迁移过来。

## 定制

- [定制总览](./docs/customize.md) —— 定制 OpenSpec 的各种选项。
- [配置档](./docs/profiles.md) —— 选择安装哪些工作流。
- [项目配置](./docs/project-config.md) —— 用 config.yaml 里的几行配置，让工作流按你想要的方式规划变更。
- [模式](./docs/customize-schemas.md) —— 改变 OpenSpec 产出什么：产物、它们的顺序以及模板。

## 多仓库（beta）

- [存储库（beta）](./docs/stores.md) —— 规划跨仓库的变更：一个存储库，多个仓库。
- [工作集（beta）](./docs/worksets.md) —— 在一个编辑器窗口里打开存储库和用它的仓库，让智能体同时看到两者。

## 参考

- [技能](./docs/skills.md) —— 每个 OpenSpec 技能：参数、它创建什么、它如何回应。
- [CLI](./docs/cli.md) —— openspec 的终端命令。
- 模式
  - [模式总览](./docs/schemas.md) —— 所有可用的工作流模式及各自定义的产物。
  - [schema.yaml](./docs/schemas/schema-yaml.md) —— 模式定义的每个字段，供阅读或编写模式时参考。
  - [spec-driven](./docs/schemas/spec-driven.md) —— 默认工作流的产物：它们的顺序、格式，以及它们生成的变更文件夹。
- 配置
  - [配置总览](./docs/configuration.md) —— 所有会改变 OpenSpec 行为的文件和设置，以及它们各自的位置。
  - [项目配置（config.yaml）](./docs/configuration/config-yaml.md) —— openspec/config.yaml 的每个字段：这个项目用来规划的模式、context 和 rules。
  - [变更元数据（.openspec.yaml）](./docs/configuration/change-metadata.md) —— 随每个变更保存的元数据所支持的字段和校验规则。
  - [CLI 设置（config.json）](./docs/configuration/config-json.md) —— config.json 的每个字段：openspec CLI 在你机器上的行为方式。
- [支持的工具](./docs/supported-tools.md) —— OpenSpec 支持哪些 AI 编码工具，以及如何调用各自的技能。
- [术语表](./docs/glossary.md) —— 每个 OpenSpec 术语，一行一条。
