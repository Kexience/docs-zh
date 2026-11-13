---
source_url: https://opencode.ai/docs/agents/
source_hash: sha256:51dd27e610b4155b9c6a5bdca11e6e7e481e36e87dccfa05f0714f5d598ae3fe
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# Agent

创建一个 Markdown 文件即可添加可复用的 agent。下面的示例添加了一个只读的 reviewer，供主 agent 发起代码评审：

```md title=".opencode/agents/reviewer.md"
---
description: Reviews changes for correctness and regressions
mode: subagent
model: anthropic/claude-sonnet-5-5#high
permissions:
  - action: edit
    resource: "*"
    effect: deny
  - action: shell
    resource: "*"
    effect: deny
---

Review the current changes. List findings in severity order with file and line references.
```

让你的主 agent 使用它：

```text
Use the reviewer subagent to review my current changes.
```

一个 agent 会将系统提示词、模型偏好、权限和显示细节组合成一个命名的助手配置。

## 位置

把 Markdown agent 保存到全局（对所有项目生效）或项目内部：

```text
~/.config/opencode/agents/<name>.md
.opencode/agents/<name>.md
```

OpenCode 会从当前目录向上直到项目根目录发现项目中的 `.opencode` 目录。嵌套路径会成为 agent ID 的一部分：

```text
.opencode/agents/team/reviewer.md  →  team/reviewer
```

## 格式

### Markdown

frontmatter 接受与 `agents` 配置条目相同的字段。Markdown 正文会成为 agent 的 `system` 提示词：

```md title=".opencode/agents/explainer.md"
---
description: Explains code without changing it
mode: subagent
---

Explain the relevant code with short examples. Do not edit files.
```

V1 frontmatter 字段已弃用。仍使用这些字段的文件如何被读取，参见 [Agent 文件](../migrate-v1/index.md#agent-files)。

### JSONC

在任意 [OpenCode 配置文件](../config/index.md)的 `agents` 下定义 agent：

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "agents": {
    "reviewer": {
      "description": "Reviews current changes",
      "mode": "subagent",
      "system": "Report findings in severity order.",
      "permissions": [
        { "action": "edit", "resource": "*", "effect": "deny" },
      ],
    },
  },
}
```

## 选择

设置会话未选择 agent 时使用的主 agent：

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "default_agent": "writer",
  "agents": {
    "writer": { "mode": "primary" },
  },
}
```

所选的默认 agent 必须存在、可见并支持作为主 agent 使用。否则 OpenCode 会使用 `build`，然后是第一个可见且具备主 agent 能力的 agent。更改此设置不会替换已存在会话上存储的 agent。

## 模式

根据 agent 应该在哪里运行来设置 `mode`：

```jsonc
{
  "agents": {
    "reviewer": { "mode": "subagent" },
  },
}
```

| 模式 | 行为 |
| --- | --- |
| `primary` | 作为会话的主 agent 运行。这是新自定义 agent 的默认值。 |
| `subagent` | 只通过 `subagent` 工具在子会话中运行。 |
| `all` | 既可作为主 agent，也可作为 subagent 运行。 |

Subagent 在自己的子会话中以全新上下文运行。它们总是在后台运行：当子会话进入空闲时父会话会收到一份报告，之后每完成一轮工作都会再收到一次。父 agent 的 `subagent` 权限控制它可以启动哪些 agent；子会话则使用自己配置的权限。

```jsonc
{
  "agents": {
    "orchestrator": {
      "permissions": [
        { "action": "subagent", "resource": "*", "effect": "deny" },
        { "action": "subagent", "resource": "reviewer", "effect": "allow" },
      ],
    },
  },
}
```

## 内置 agent

OpenCode 包含以下可见 agent：

| Agent | 模式 | 用途 |
| --- | --- | --- |
| **Build** (`build`) | `primary` | 默认编码 agent。默认允许使用工具和访问工作区之外的内容；读取敏感的环境变量文件时会请求批准。 |
| **Plan** (`plan`) | `primary` | 只探索和规划，不修改常规项目文件。被要求时它可以写 OpenCode 计划文件，shell 命令仍受权限控制。 |
| **General** (`general`) | `subagent` | 以广泛的工具访问权限处理研究和多步骤工作，但不能启动更多 subagent。 |
| **Explore** (`explore`) | `subagent` | 搜索和阅读代码或网络资源，不修改文件。 |

使用相同的 ID 即可覆盖内置 agent：

```jsonc
{
  "agents": {
    "build": {
      "permissions": [
        { "action": "shell", "resource": "git push *", "effect": "ask" },
      ],
    },
  },
}
```

隐藏的 `compaction`、`title` 和 `summary` agent 负责维护任务，不能被直接选中。V2 没有内置的 `scout` agent。

## 合并

agent 定义按配置顺序合并。靠后的标量值替换靠前的值，request 映射按键合并，权限规则则是追加：

```jsonc
{
  "permissions": [
    { "action": "shell", "resource": "*", "effect": "ask" },
  ],
  "agents": {
    "build": {
      "permissions": [
        { "action": "shell", "resource": "git status", "effect": "allow" },
      ],
    },
  },
}
```

全局 `permissions` 先于 agent 专属规则应用，因此靠后的 agent 规则可以对它们进行细化。

## 选项

### Description

`description` 说明 agent 的用途。请为 subagent 添加它，因为 OpenCode 会把它展示给负责选择要启动哪个 agent 的模型：

```yaml
description: Reviews database migrations for safety
```

### Mode

`mode` 接受 `primary`、`subagent` 或 `all`。新的自定义 agent 省略该字段时默认为 `primary`：

```yaml
mode: all
```

### Model

`model` 使用 `provider/model` 格式，并可选 `#variant`：

```yaml
model: anthropic/claude-sonnet-5-5#high
```

JSON 配置也接受展开形式：

```jsonc
{
  "agents": {
    "reviewer": {
      "model": {
        "providerID": "anthropic",
        "model": "claude-sonnet-5-5",
        "variant": "high",
      },
    },
  },
}
```

- Subagent 使用自己配置的模型，未配置时继承父会话的模型。
- 会话单独存储自己选定的模型。按 ID 选择主 agent 不会改变该模型。

### System

`system` 设置 agent 的系统提示词。非空值会替换该 agent 的 provider 基础提示词：

```jsonc
{
  "agents": {
    "reviewer": { "system": "Review only. Do not modify files." },
  },
}
```

项目指令、技能、引用及其他指令来源仍会被添加。在 Markdown agent 中，请把这段文字放在文档正文里，而不是 `system` frontmatter 字段中。

### Permissions

`permissions` 是一组按顺序匹配的规则：

```jsonc
{
  "agents": {
    "reviewer": {
      "permissions": [
        { "action": "*", "resource": "*", "effect": "deny" },
        { "action": "read", "resource": "src/**", "effect": "allow" },
      ],
    },
  },
}
```

| 字段 | 含义 |
| --- | --- |
| `action` | 工具或权限操作。支持通配符。 |
| `resource` | 被该操作匹配的路径、命令、agent ID 或其他值。支持通配符。 |
| `effect` | `allow`、`ask` 或 `deny`。 |

最后一条匹配的规则生效，因此要把宽泛的规则放在例外之前。常见操作包括：

| 操作 | 覆盖范围 |
| --- | --- |
| `shell` | Shell 命令 |
| `edit` | 编辑、写入和补丁工具 |
| `subagent` | 子 agent |
| `read`, `glob`, `grep` | 本地发现工具 |
| `webfetch`, `websearch` | 网络工具 |
| `skill` | 技能加载 |

对于 `read`、`edit` 和 `external_directory` 资源，OpenCode 会展开 `~` 和 `$HOME`：

```jsonc
{ "action": "read", "resource": "~/notes/**", "effect": "allow" }
```

Shell 资源保持为原始命令文本，不会展开这些值。

### Steps

`steps` 设置模型步数的正数上限：

```yaml
steps: 8
```

在最后一步，OpenCode 会移除工具并要求模型用文字总结。新的用户输入会重置该额度。

### Hidden

`hidden` 会把一个 agent 从常规列表、交互式发现和 subagent 目录中移除：

```yaml
hidden: true
```

这控制的是可见性，而不是安全性。要限制行为，请使用权限。

### Color

`color` 使用六位十六进制值设置 agent 的 UI 颜色：

```yaml
color: "#ff6b6b"
```

### Disabled

`disabled` 会在配置加载到该处时移除一个内置或自定义 agent：

```jsonc
{
  "agents": {
    "plan": { "disabled": true },
  },
}
```

### Request

`request` 接受按 agent 定制的请求头和 JSON 请求体覆盖：

```jsonc
{
  "agents": {
    "reviewer": {
      "request": {
        "headers": { "x-agent": "reviewer" },
        "body": { "temperature": 0.1 },
      },
    },
  },
}
```

<Callout type="warning">
  V2 会话运行器会保留这些值，但尚未随模型请求一起发送。请改为在 provider、模型或模型变体上配置生效的请求设置。
</Callout>

在新的 V2 agent 配置中，不要使用 `temperature`、`top_p`、`prompt`、`permission`、`tools`、`disable` 或 `maxSteps` 等旧版顶层字段。
