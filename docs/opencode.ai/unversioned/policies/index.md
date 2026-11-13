---
source_url: https://opencode.ai/docs/policies/
source_hash: sha256:ebbfd395f209c6d457ca0cb359386fb5f0972eaeb1b2813b5e0fa4102a83f4c2
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# 策略

策略决定 OpenCode 是否可以对某个具名资源执行操作。它们在 `policies` 下编写，也可以由连接的 [OpenCode Console](../console/index.md)工作区下发。

策略与[权限](../permissions/index.md)是分开的。权限是按 agent 生效的工具规则，可以 `allow`、`deny` 或 `ask`。策略是二元的、从不弹窗，只会收紧权限和 provider 原本允许的范围。

## 配置

在 `opencode.jsonc` 中添加一条语句即可在所有位置拒绝一个 provider：

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "policies": [{ "action": "provider.use", "resource": "openai", "effect": "deny" }],
}
```

被拒绝的 provider 会从目录和模型选择中消失，即使它有有效凭据也一样。

早期版本从 `experimental.policies` 读取策略。该键仍然有效，并会合并到 `policies`：

```jsonc
{
  "experimental": {
    "policies": [{ "action": "provider.use", "resource": "openai", "effect": "deny" }],
  },
}
```

## 语句

每条语句有三个字段：

| 字段       | 取值                                                                                                                        | 含义                                   |
| ---------- | --------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| `action`   | `provider.use`, `tool.use`, `integration.connect`, `integration.use`, `mcp.use`, `skill.use`, `plugin.use`, `websearch.use` | 被控制的操作                           |
| `resource` | 字符串或通配符模式                                                                                                          | 语句作用于什么；取决于操作             |
| `effect`   | `allow`, `deny`                                                                                                             | 语句匹配时的决定                       |

未通过校验的语句会被丢弃并在服务器日志中给出警告，列表的其余部分仍然生效。编辑一条 `deny` 后请检查日志。

## 匹配

资源使用与权限相同的整值通配符：`*` 匹配零个或多个字符，`?` 匹配一个字符。

```jsonc
{
  "policies": [{ "action": "provider.use", "resource": "company-*", "effect": "deny" }],
}
```

这会拒绝 `company-us` 和 `company-eu`。以 ` *` 结尾的模式也会匹配不带参数的值本身，因此 `shell:git push *` 同时覆盖单独的 `git push`。

## 顺序

当多条语句匹配时，最后一条生效。没有特异性规则，因此把宽泛的语句放在前面，例外放在后面。如果没有任何语句匹配，该操作就是允许的。

```jsonc
{
  "policies": [
    { "action": "provider.use", "resource": "*", "effect": "deny" },
    { "action": "provider.use", "resource": "anthropic", "effect": "allow" },
  ],
}
```

这样只剩 Anthropic 可用。

## Providers

`provider.use` 控制 provider 是否完全可用。资源是 provider ID：`anthropic`、`openai`、`opencode`，或来自 [`providers`](../providers/index.md)的自定义 ID。

```jsonc
{
  "providers": {
    "company-ai": {
      "package": "@opencode/ai/providers/openai-compatible",
      "settings": { "baseURL": "https://ai.company.example/v1" },
    },
  },
  "policies": [
    { "action": "provider.use", "resource": "*", "effect": "deny" },
    { "action": "provider.use", "resource": "company-ai", "effect": "allow" },
  ],
}
```

`providers` 条目配置端点；这些语句让它成为 OpenCode 唯一会使用的 provider。无论 provider 是通过何种途径被知晓的——目录数据、环境变量、已保存账号、内置插件还是配置——策略都会生效。

请用 `provider.use` 取代 V1 的 `enabled_providers` 和 `disabled_providers` 列表。V1 文件仍可加载；参见[从 V1 迁移](../migrate-v1/index.md#supported-fields-without-direct-native-equivalents)。

## 工具

`tool.use` 语句会硬性拒绝一次[权限](../permissions/index.md)检查。资源是 `<action>:<value>`，会与该工具检查的每个资源进行匹配。

```jsonc
{
  "policies": [
    { "action": "tool.use", "resource": "shell:git push *", "effect": "deny" },
    { "action": "tool.use", "resource": "edit:*.env", "effect": "deny" },
    { "action": "tool.use", "resource": "webfetch:*", "effect": "deny" },
  ],
}
```

被拒绝的检查会以 `Blocked by configuration policy` 失败，而不是弹窗。它在 agent 规则和已保存的批准之后应用，因此会同时覆盖 `ask` 和"总是允许"式的批准。

| 模式                         | 阻止的内容                                |
| ---------------------------- | ----------------------------------------- |
| `shell:*`                    | 所有 shell 命令                           |
| `read:*/.ssh/*`              | 读取 SSH 凭据材料                         |
| `external_directory:*`       | 对 Location 或 worktree 之外的任何访问    |
| `subagent:general`           | 启动某一个 subagent                       |
| `github_delete_repository:*` | 某一个 MCP 工具                           |
| `*`                          | 其他未被拒绝的一切                        |

带 `allow` 的 `tool.use` 语句永远不会授予访问权。它只会解除先前更宽泛的 `deny`，之后由 agent 自身的规则决定。

```jsonc
{
  "policies": [
    { "action": "tool.use", "resource": "shell:*", "effect": "deny" },
    { "action": "tool.use", "resource": "shell:git status *", "effect": "allow" },
  ],
}
```

`git status` 会回退到 agent 的 `shell` 规则；其他所有命令都被阻止。

## 集成

集成是你在 `/connect` 中连接的任何东西：OpenCode Console（`opencode`）、诸如 `anthropic` 的 provider、诸如 `exa` 的网络搜索服务，或诸如 `https://ai.acme.com` 的知名配置来源。登录 MCP 服务器不受集成策略影响；控制 MCP 服务器请使用 `mcp.use`。

`integration.connect` 控制 `/connect` 列出哪些集成以及哪些可以连接。资源是集成 ID。

`integration.use` 控制集成提供的一切：它的 provider 和模型、它的网络搜索，以及 Console 工作区或知名来源下发的 MCP 服务器和配置。资源是 `<integration>#<account>`，其中 account 是已连接的组织或账号 ID，例如 `opencode#org_01M3CAP8H43Z49CER6NT0Y3ZF1`。没有连接账号时就是裸的集成 ID：未登录的免费层是 `opencode`，`ANTHROPIC_API_KEY` 环境变量是 `anthropic`，来自 `opencode.json` 的 provider 则是其 provider ID。

下面这条 MDM 策略只要求一个 Console 工作区，其他一律禁止：

```jsonc
{
  "policies": [
    { "action": "integration.connect", "resource": "*", "effect": "deny" },
    { "action": "integration.connect", "resource": "opencode", "effect": "allow" },
    { "action": "integration.use", "resource": "*", "effect": "deny" },
    { "action": "integration.use", "resource": "opencode#org_01M3CAP8H43Z49CER6NT0Y3ZF1", "effect": "allow" },
  ],
}
```

`/connect` 只提供 Console 供成员登录。免费层、个人 Console 账号、其他组织、环境变量 API key 以及来自 `opencode.json` 的 provider 全都不可用。工作区的 provider、MCP 服务器和网络搜索正常工作，并且在 Console 中修改它们不需要新的 MDM 配置文件。

只有托管策略可以扣留集成下发的 MCP 服务器和配置；无论哪种情况，集成自身的策略都会继续适用。

## MCP 服务器、技能和插件

| 操作         | 资源                                                            |
| ------------ | --------------------------------------------------------------- |
| `mcp.use`    | [MCP 服务器](../mcp-servers/index.md)，按其配置名               |
| `skill.use`  | [技能](../skills/index.md)，按其 ID                             |
| `plugin.use` | [插件](../plugins/index.md)，按不带版本号的包名或绝对路径       |

```jsonc
{
  "policies": [
    { "action": "mcp.use", "resource": "*", "effect": "deny" },
    { "action": "mcp.use", "resource": "github", "effect": "allow" },
    { "action": "plugin.use", "resource": "opencode-acme-cli", "effect": "deny" },
  ],
}
```

被拒绝的 MCP 服务器或技能会被移除，被拒绝的插件不会被加载，无论它是如何配置的。

### 从 `integration.use` 升级

在 OpenCode 2.2.3 之前，`integration.use` 通过 `mcp:`、`skill:` 或 `plugin:` 前缀覆盖 MCP 服务器、技能和插件。带前缀的语句仍然会加载，并被转换为 `mcp.use`、`skill.use` 或 `plugin.use`。

不带这些前缀之一的语句（包括裸的 `*`）现在改为作用于集成。像下面这样宽泛的 deny：

```jsonc
{ "action": "integration.use", "resource": "*", "effect": "deny" }
```

不再阻止 MCP 服务器、技能或插件。相反，它会阻止所有 provider（包括免费层），除非后面的语句允许某个集成。要保留旧含义，请替换为：

```jsonc
{
  "policies": [
    { "action": "mcp.use", "resource": "*", "effect": "deny" },
    { "action": "skill.use", "resource": "*", "effect": "deny" },
    { "action": "plugin.use", "resource": "*", "effect": "deny" },
  ],
}
```

例外也按同样方式迁移：`integration.use` 的 `mcp:github` 变成 `mcp.use` 的 `github`，`skill:team:review` 变成 `skill.use` 的 `team:review`。

早于 2.2.3 的客户端会忽略 `integration.connect`、`integration.use`（新含义）、`mcp.use`、`skill.use` 和 `plugin.use`，因此凡依赖这些语句之处都要求 2.2.3 或更新版本。

## 网络搜索

`websearch.use` 控制 `websearch` 工具可以使用哪些网络搜索 provider。资源是 provider ID：`opencode` 表示来自 Console 的 OpenCode Web Search，内置 provider 如 `exa`、`firecrawl`、`parallel`、`tavily` 或 `tinyfish`，或某个插件添加的 provider 的 ID。

```jsonc
{
  "policies": [
    { "action": "websearch.use", "resource": "*", "effect": "deny" },
    { "action": "websearch.use", "resource": "opencode", "effect": "allow" },
  ],
}
```

被拒绝的 provider 即使无需 API key 也能工作（如 Exa 和 TinyFish）也会被移除。当所有 provider 都被拒绝时，`websearch` 工具不再被提供。早于 2.2.6 的客户端会忽略 `websearch.use`。

## 优先级

普通设置让最近的配置获胜。策略正好相反：来自更宽泛配置的语句会更晚求值，因此会覆盖更窄的语句。托管配置和连接的 Console 始终高于用户和项目文件。

| 权威        | 来源                                                                                                           |
| ----------- | -------------------------------------------------------------------------------------------------------------- |
| 1（最高）   | macOS 托管偏好设置（`/Library/Managed Preferences/ai.opencode.managed.plist`）                                 |
| 2           | 系统 `opencode.json(c)`（`/Library/Application Support/opencode`、`/etc/opencode`、`%ProgramData%\opencode`）  |
| 3           | 已连接的 OpenCode Console 工作区                                                                               |
| 4           | 全局 `~/.config/opencode/opencode.json(c)`                                                                     |
| 5           | 直接的 `opencode.json(c)`；外层目录胜过内层目录                                                                |
| 6（最低）   | `.opencode/opencode.json(c)`；外层目录胜过内层目录                                                             |

仓库无法重新启用你在全局拒绝的 provider：

```jsonc title="~/.config/opencode/opencode.jsonc"
{
  "policies": [{ "action": "provider.use", "resource": "openai", "effect": "deny" }],
}
```

```jsonc title="project/opencode.jsonc"
{
  "policies": [{ "action": "provider.use", "resource": "openai", "effect": "allow" }],
}
```

`openai` 保持被拒绝。在同一个文件内，语句保持书写顺序。

## Console

[OpenCode Console](../console/index.md)上的工作区会把它针对 Providers 和 Tools 的策略编译成工作区配置中普通的 `policies` 语句。OpenCode 合并该配置时，把它视作一个排在托管偏好和系统文件之下、但高于其他一切配置文件的配置文件，因此组织级的 `deny` 无法被仓库或用户的 `allow` 解除，而组织级的 `allow` 可以解除更低权威的 `deny`。托管偏好和系统文件仍然覆盖工作区。

来自这些语句的拒绝会指明工作区：

```text
Blocked by Acme's policy
```

语句跟随已连接的账号。

| 事件               | 结果                                      |
| ------------------ | ----------------------------------------- |
| Console 策略变更   | 在下一次拉取时应用，大约每分钟一次        |
| 切换到其他工作区   | 语句被替换为该工作区的语句                |
| 断开连接           | 语句被清空                                |
| Console 不可达     | 该连接的最后一条语句继续生效              |

Console 插件和策略插件无法通过 `plugins` 禁用；参见[插件控制](../plugins/index.md#control)。

<Callout type="note">
  策略不配置端点或凭据，也不能让一个不可用的 provider 变得可用。它们同样不会沙箱化插件代码：被拒绝的 provider 是在正常的 provider 和模型路径上被阻止的。
</Callout>
