---
source_url: https://openspec.dev/docs/schemas
source_hash: sha256:639b398b6a0a2d5435a462f3e0e7b44a890e5bcbdb49c208273971ee86b09689
translated_at: 2026-11-13T09:48:42+08:00
translation_version: 1
---

# 模式总览

模式定义一份变更提案会产出哪些产物，以及按什么顺序产出。在磁盘上，它是一个内含 schema.yaml 的文件夹。该文件的每个字段都在 [schema.yaml](./schemas/schema-yaml.md) 页面上。

## 可用的模式 [#available-schemas]

CLI 自带一个模式：

| 模式 | 产物 |
|---|---|
| [spec-driven](./schemas/spec-driven.md)（默认） | `proposal`、`specs`、`design`、`tasks` |

项目可以添加自己的模式，一台机器也可以全局覆盖。这些文件夹位于何处、哪一份副本生效，见 schema.yaml 的[位置](./schemas/schema-yaml.md#location)一节。

在终端中，[`openspec schemas`](./cli.md#openspec-schemas) 会打印你的项目能看到的每一个模式。
