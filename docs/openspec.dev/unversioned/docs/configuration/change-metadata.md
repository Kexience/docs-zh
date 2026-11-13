---
source_url: https://openspec.dev/docs/configuration/change-metadata
source_hash: sha256:4e6d3ae3981d5f9b151cd656be44137f15d0f2eb6f2901175602788e7b5f78cf
translated_at: 2026-11-13T09:48:42+08:00
translation_version: 1
---

# 变更元数据（.openspec.yaml）

## 位置 [#location]

每个变更把自己的元数据保存在 `openspec/changes/<change-name>/.openspec.yaml`，与它的产物放在一起。创建变更时会写入该文件，并填好 `schema` 和 `created`。

## 字段 [#fields]

| 键 | 类型 | 必填 | 作用 |
| --- | --- | --- | --- |
| `schema` | 字符串 | 是 | 此变更遵循的工作流模式 |
| `created` | 字符串，YYYY-MM-DD | 否 | 记录变更的创建日期 |
| `goal` | 字符串 | 否 | 记录此变更打算达成什么 |
| `affected_areas` | 字符串列表 | 否 | 记录此变更预计会涉及的领域 |
| `initiative` | 映射：`store` 和 `id` | 否 | 记录此变更所属的专项 |
| `skip_specs` | 布尔值 | 否 | 声明此变更不产生规格增量，因此零增量也能通过校验 |
| `retire_capabilities` | 布尔值 | 否 | 授权归档删除被此变更清空的能力 |

### schema [#schema]

此变更遵循的工作流模式。它在创建变更时设定，优先级高于项目配置，因此即使之后 `openspec/config.yaml` 发生变化，该变更仍保留自己的模式。运行 [`openspec schemas`](../cli.md#openspec-schemas) 可列出可用的模式名称。

### initiative [#initiative]

此变更所属的专项，由一个存储库 id 和一个专项 id 表示，两者都用 kebab-case：

```yaml
initiative:
  store: platform-specs
  id: unify-billing
```

除 `store` 和 `id` 之外的键会被拒绝。目前没有任何命令读取这个关联。

### skip_specs [#skip_specs]

声明此变更有意不产生任何规格增量：纯粹的重构、工具或文档变更。设置后，校验会接受零增量，那些本应生成规格文件的产物也算作完成。如果在 specs/ 下已存在规格文件却设置此项，会报校验错误。

### retire_capabilities [#retire_capabilities]

授权归档移除某个能力。当此变更的 REMOVED 增量拿走某个能力最后一条需求时，归档会删除该能力的主规格，而不是中止。之所以需要这个标志，是因为这种删除只能从 git 恢复，所以决定权留给作者。

### 扩展键 [#extension-keys]

以全小写 `x-` 开头的顶层键归你使用，用来存放其他工具或团队与变更并排放的数据，例如跟踪系统 id 或负责人：

```yaml
schema: spec-driven
x-tracker: SB-5497
x-jiraKey: ABC-1
x-owner:
  team: payments
```

- **名称**：小写 `x-` 前缀后至少跟一个字符，任何位置都不能有空白。前缀之后大小写和拼写随意，所以 `x-jiraKey` 和 `x-trackerID` 都合格。`X-Tracker`、单独的 `x-` 和 `x- tracker` 不合格，会被报为未知键。
- **值**：任意 YAML 值。OpenSpec 不读取也不校验它，它不改变任何行为。
- **作用域**：仅限顶层。`initiative` 内部的 `x-` 键仍会被拒绝，和那里其他任何键一样。
- **校验**：扩展键永远不会被报为未知，所以带有扩展键的变更能通过 `openspec validate --strict`。
- **归档**：文件随变更原样移动，扩展键一并保留。

## 示例 [#example]

一份填写完整的 .openspec.yaml：

```yaml
schema: spec-driven
created: 2026-08-14
goal: Add magic-link login to the API
affected_areas:
  - auth
  - api
```

## 校验 [#validation]

每当有命令写入或读取该文件时都会校验它。写入未通过校验会抛错，并且什么都不写。读取已有文件时，YAML 无效、字段违反其约定、或模式名称不可用，都会导致失败。文件不存在不算错误，此时该变更被视为没有元数据。

与 [config.yaml](./config-yaml.md) 不同，错误的值不会带着警告被丢弃。元数据出错会中止命令。

- **未知顶层键**：OpenSpec 会忽略它们。`status`、`instructions`、`validate` 和 `archive` 会报告它们没有效果。JSON 输出会在结构化结果中带上该警告。[扩展键](#extension-keys) 不属于未知键，永远不会被报告。
- **严格校验**：`openspec validate --strict` 把未知键警告视为失败。如果某个变更的额外键全是扩展键，则能通过。
