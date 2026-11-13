---
source_url: https://openspec.dev/docs/project-config
source_hash: sha256:9cd2658877bf2e3454f71c70814ab4c3e72e0b4abe58be9563728de5a181577a
translated_at: 2026-11-13T09:48:42+08:00
translation_version: 1
---

# 项目配置

`openspec/config.yaml` 告诉工作流你希望如何规划变更。

例如，下面这份配置更新了 [tasks.md](./schemas/spec-driven.md) 产物的创建规则：

```yaml
rules:
  tasks:
    - End every task with a commit
```

智能体运行时，会从这些规则中取用，并确保每项任务都以一个提交步骤收尾。

规则要短。这里的一切都会进入智能体的上下文，冗长的规则反而会让输出变差。

## 工作方式 [#how-it-works]

config.yaml 存放的是智能体在创建产物或走工作流时收到的指令。

每次运行都会发生下面这些事：

1. 你运行一个工作流（例如 `/openspec-propose`）。
2. 智能体调用 [`openspec instructions`](./cli.md) 命令。
3. 该命令从 config.yaml 读取你的 context 和 rules。
4. OpenSpec 的内置指令与你的定制内容合并成一段提示词，交给智能体。
5. 智能体按这段提示词写出产物。

例如，配上 `context` 字段和本页开头的规则，[`openspec instructions`](./cli.md) 为 tasks.md 返回的内容如下（已裁剪并加注）：

```xml
<artifact id="tasks" change="add-dark-mode" schema="spec-driven">

  <!-- From your config.yaml: context -->
  <project_context>
    Designs and tasks must cover Windows, macOS, and Linux
    Write all artifacts in Spanish
  </project_context>

  <!-- From your config.yaml: rules for tasks -->
  <rules>
    - End every task with a commit
  </rules>

  <!-- From OpenSpec: the built-in guidance -->
  <instruction>
    ...how to write a good tasks.md...
  </instruction>

  <template>
    ...the tasks.md structure to fill in...
  </template>

</artifact>
```

你的配置先到达，然后是 OpenSpec 的内置指令和模板。规则是在内置内容之上追加，从不替换它们。对 config.yaml 的修改会在下一次运行时送达智能体。

## 字段 [#the-fields]

三个字段决定了智能体收到什么。每个字段的精确约定（类型、限制、校验）见[项目配置（config.yaml）](./configuration/config-yaml.md)。

| 字段 | 作用 | 注入到 |
|---|---|---|
| `context` | 智能体总会收到的指令 | 所有环节：每个产物、`apply`、`archive` |
| `rules` | 针对某一个产物的额外指令 | 仅该产物的创建过程 |
| `operations` | 关于工作流某一步如何执行的指导 | 仅 `apply` 和 `archive` |

config.yaml 的其他字段（`schema`、`store`、`references`）用于选择项目使用哪个模式、哪个 OpenSpec 根目录。约定页面有详细说明。

最后一列是精确的：字段只会到达那里列出的步骤。特别是 `verify` 永远收不到 `rules`，它按产物的字面内容核对实现是否一致。

### context [#context]

`context` 是智能体在创建产物、实施任务或归档变更时收到的背景信息。

```yaml
context: |
  We ship cross-platform. Designs and tasks must cover Windows, macOS, and Linux
  Write all artifacts in Spanish
```

用 `context` 承载那些应当影响工作流输出的事实和约束。长期的项目文档仍放在项目的文档文件里；凡是智能体能通过读代码了解到的东西，都不要放进来。

**换用其他语言**：由于 context 会到达每个产物，你可以加上 `Write all artifacts in Spanish.` 来让智能体用西班牙语写提案、规格、设计和任务产物。

### rules [#rules]

`rules` 挂到某一个产物上，以产物 id 为键。每一行都会追加到该产物的内置指引中：

```yaml
rules:
  proposal:
    - Keep proposals under 500 words
  tasks:
    - Every UI task includes a Playwright test
```

这样提案会保持简短，tasks.md 也总会规划浏览器测试。其他产物不受影响。

### operations [#operations]

`operations` 指导智能体如何执行 `apply` 和 `archive`，而不是产物里写什么：

```yaml
operations:
  apply:
    guidance:
      - Run the linter before marking a task complete
  archive:
    guidance:
      - Summarize what shipped before archiving
```

在 apply 期间，智能体每完成一项任务就跑一次 lint。在 archive 期间，它以一份总结收尾。

## 当 config.yaml 不够用时 [#when-configyaml-isnt-enough]

配置是在标准工作流之上追加指令，但它无法改变存在哪些产物，也无法改变产物的结构。当你需要这种层级的控制，或者规则没能稳定地引导行为时，请[派生一个模式](./customize-schemas.md)。
