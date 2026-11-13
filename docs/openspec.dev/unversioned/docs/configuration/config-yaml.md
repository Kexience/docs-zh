---
source_url: https://openspec.dev/docs/configuration/config-yaml
source_hash: sha256:6c8ae1caa6e56e609be968f60cc7cb6b653c11bcaa92f8e2b4e277d1c2f63e23
translated_at: 2026-11-13T09:48:42+08:00
translation_version: 1
---

# 项目配置（config.yaml）

## 位置 [#location]

每个 OpenSpec 项目把配置文件放在项目根目录的 `openspec/config.yaml`。

## 字段 [#fields]

| 键 | 类型 | 必填 | 作用 |
| --- | --- | --- | --- |
| `schema` | 字符串 | 是 | 本项目变更遵循的工作流模式 |
| `context` | 字符串 | 否 | 注入到每个产物、apply 和 archive |
| `rules` | 映射：产物 ID → 字符串列表 | 否 | 追加到某个产物内置指引中的额外规则 |
| `operations` | 映射：操作 → 指引列表 | 否 | 针对 apply 和 archive 工作的建议性指引 |
| `store` | 字符串 | 否 | 当此 openspec/ 只有配置时使用的兜底 OpenSpec 根目录 |
| `references` | 列表 | 否 | 其规格会被索引进指令输出的存储库 |

无效字段从不会让命令失败。每个字段单独校验，坏值会被丢弃并给出警告。无法读取或不是合法 YAML 的文件会被忽略并给出警告，但 `openspec validate` 除外——它的退出码为 1，好让 CI 抓到问题。

这些字段里该写什么，见[项目配置](../project-config.md)。

### schema [#schema]

本项目每个变更都遵循的工作流模式。合法值是 `spec-driven`，或项目自定义的模式名。运行 [`openspec schemas`](../cli.md#openspec-schemas) 可列出可用的模式名称。

### context [#context]

自由文本，会注入每个产物的指令，并提供给 apply 和 archive。上限为 50KB，超出会被忽略并给出警告。

### rules [#rules]

针对某一个产物的额外规则，追加到该模式的内置指引中：

```yaml
rules:
  proposal:
    - Keep proposals under 500 words
```

产物 ID 不限于内置名称，因此自定义模式里的产物也可以作为键。

### operations [#operations]

关于 apply 和 archive 工作如何开展的建议性指引，与产物规则分开：

```yaml
operations:
  apply:
    guidance:
      - Keep test summaries concise
```

只读取 `apply` 和 `archive`。

### store [#store]

用作 OpenSpec 根目录的存储库 id，只有当此 openspec/ 目录只有配置（没有 specs/ 或 changes/）时才会用到。它是兜底，绝不是覆盖。完整的解析顺序见[根目录解析](../stores.md#where-artifacts-get-created-when-using-stores)。

### references [#references]

本项目工作会引用的存储库 id。每个存储库的规格索引（id、摘要、获取命令）会被加入指令输出。规格内容从不内联，根目录解析也从不受影响。每一项可以是一个存储库 id，或一个带 `id` 和可选 `remote` 克隆源的映射：

```yaml
references:
  - platform-specs
  - id: billing-specs
    remote: git@github.com:acme/billing-specs.git
```

## 示例 [#example]

一份填写完整的 config.yaml：

```yaml
schema: spec-driven

context: |
  Designs and tasks must cover Windows, macOS, and Linux
  Write all artifacts in Spanish

rules:
  proposal:
    - Keep proposals under 500 words
    - Always state what is out of scope
  tasks:
    - Break tasks into chunks of max 2 hours

operations:
  apply:
    guidance:
      - Keep test summaries concise
  archive:
    guidance:
      - Summarize the archive outcome before finishing
```

## 旧版文件名 [#legacy-names]

当 `config.yaml` 不存在时，`openspec/config.yml` 会作为别名被读取。两个文件都存在时，`config.yaml` 优先，`config.yml` 被忽略。`openspec init` 创建的是 `config.yaml`。
