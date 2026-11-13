---
source_url: https://opencode.ai/docs/migrate-v1/
source_hash: sha256:5c4f19aa7b16d25ef328097173e19bee5032c0a890e6625717c3bc32cebf44d3
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# 从 V1 迁移

OpenCode 1 和 OpenCode 2 都使用 `opencode` 命令，默认不再并排安装。安装 V2 之前请先移除由包管理器安装的 V1；V2 的 curl 安装器会替换 V1 的二进制。

## 破坏性变更

V2 有三处有意的破坏性变更：

- [插件](../build/plugins/migrate-v1/index.md)使用新的插件 API。
- [服务器 API 和客户端](服务器-api-和客户端)有了新契约。
- [终端客户端配置](../cli/config/index.md)从分层的 `tui.json(c)` 文件迁移到一个全局 `cli.json` 文件（自动迁移）。

这些区域之外的受支持 V1 功能旨在保持与 V1 兼容。V1 schema 接受的部分字段从未有过 V2 对应物，会被有意忽略；这些字段列在[接受但不支持的字段](接受但不支持的字段)下。

`.opencode/` 中现有的受支持服务器配置字段、agent 定义、命令定义、技能及其他文件应当无需改动即可继续工作。如果本指南描述的受支持行为在 V2 中失效，应将其视为兼容性 bug，而不是预期的迁移要求。

<Callout type="tip">
  如果受支持的 V1 功能在 V2 中无法工作，请按照[故障排除](../troubleshooting/index.md)中的问题报告指引提交一个兼容性问题。
</Callout>

## 安装 V2

按照[安装说明](../index.md#cli)安装 V2 终端客户端。

开始使用 V2 之前不需要重写所有内容。一次务实的迁移是：

1. 保留现有的配置和基于文件的定义。
2. 启动 V2，验证模型、凭据、agent、权限和 MCP 服务器。
3. 迁移插件，因为 V1 插件实现无法在 V2 中运行。
4. 迁移调用服务器 API 的集成。
5. 准备就绪时再把配置转换为原生 V2 形态。这一步是可选的。

验证迁移期间请保留一份 V1 设置的副本。V1 和 V2 使用相同的配置位置，因此不要在把文件转换为原生 V2 专属形态后仍让 V1 指向它们。

## 配置

本节同时覆盖 JSON/JSONC 配置和 `.opencode/` 下基于文件的定义。

### 直接使用现有配置

V2 从与 V1 相同的位置读取现有的系统、全局和项目配置：

```text
/Library/Application Support/opencode/opencode.json(c)
/etc/opencode/opencode.json(c)
%ProgramData%\opencode\opencode.json(c)
/Library/Managed Preferences/<user>/ai.opencode.managed.plist
/Library/Managed Preferences/ai.opencode.managed.plist
~/.config/opencode/opencode.json(c)
<project>/opencode.json(c)
<project>/.opencode/opencode.json(c)
```

V2 会在内存中规范化受支持的 V1 字段和原生 V2 字段，而不改写源文件。现有的受支持 V1 配置应能继续工作，因此你不需要为了试用或采用 V2 而转换它。

与 V1 一样，系统配置和 macOS 托管偏好拥有最高优先级，它们的设置会覆盖全局和项目文件。它们的[策略](../policies/index.md#precedence)（包括迁移过来的 `enabled_providers` 和 `disabled_providers`）同样高于全局和项目策略。覆盖某个设置无法阻止用户添加 provider、MCP 服务器、agent 或插件，因此请把管理员强制要求的限制表达为 `policies`，而不是 `permissions` 之类的普通设置。

### 让 OpenCode 帮你迁移

V1 配置格式仍受支持。原生 V2 格式是可选的，它让若干设置更加显式、更符合人体工学。

推荐的迁移路径是让 OpenCode 替你更新配置：

```text
Migrate my OpenCode configuration, including file-based definitions, from the V1 format to the native V2 format.
Preserve its behavior and all unrelated settings.
```

OpenCode 可以检查完整文件、应用下文中的相关改动，并避免重写不需要更改的设置。转换不必一次完成：受支持的 V1 字段和原生 V2 字段可以在顶层共存。当两种形式设置同一个规范值时，只要原生 V2 值有效，无论 JSON 键顺序如何它都会优先。

嵌套混合被有意限制在边界内。OpenCode 能识别 `mcp`、`compaction` 和 `experimental` 内部的 V1/V2 混合成员，但不会在单个 agent、provider、命令或模型内部递归推断格式。请让这些嵌套条目各自完整地使用一种格式。受支持的 V1 语法本身会安静地被接受；格式错误的值、不受支持的旧字段以及相互冲突的 V1/V2 值会产生警告，而无关的有效设置继续加载。

### 权限和工具

V1 按工具对权限效果分组。V2 使用一个有序的 `permissions` 数组，让优先级和例外变得显式：

```jsonc
// V1
{
  "permission": {
    "bash": {
      "git push *": "ask"
    },
    "edit": "allow"
  },
  "tools": {
    "websearch": false
  }
}

// V2
{
  "permissions": [
    { "action": "shell", "resource": "git push *", "effect": "ask" },
    { "action": "edit", "resource": "*", "effect": "allow" },
    { "action": "websearch", "resource": "*", "effect": "deny" }
  ]
}
```

权限操作也变了：`bash` 变为 `shell`，`task` 变为 `subagent`，`write` 和 `patch` 变为 `edit`。有序的 V2 规则格式参见[权限](../permissions/index.md)。

Todos 在 V2 中默认关闭。要开启它们，请使用实验性开关。它可能在未来的版本中更改或被移除；参见[实验性功能](../config/index.md#experimental)。

```jsonc
{
  "experimental": {
    "todo": true,
  },
}
```

<Callout type="warning">
  V1 在访问项目外路径前会先询问。V2 不会：`external_directory` 默认是允许的。要保留 V1 的行为，请在 `permissions` 中添加 `{ "action": "external_directory", "resource": "*", "effect": "ask" }`。
</Callout>

### Agent 和模式

单数的 `agent` 和已弃用的 `mode` 映射变为 `agents`。agent 字段变得与 V2 配置的其余部分更加一致：

```jsonc
// V1
{
  "agent": {
    "reviewer": {
      "prompt": "Review for correctness and missing tests.",
      "model": "anthropic/claude-sonnet-5-5",
      "variant": "high",
      "disable": false,
      "permission": {
        "edit": "deny"
      }
    }
  }
}

// V2
{
  "agents": {
    "reviewer": {
      "system": "Review for correctness and missing tests.",
      "model": "anthropic/claude-sonnet-5-5#high",
      "disabled": false,
      "permissions": [
        { "action": "edit", "resource": "*", "effect": "deny" }
      ]
    }
  }
}
```

`prompt` 变为 `system`，`disable` 变为 `disabled`，单独的 `variant` 以 `#` 连接到模型引用之后。`maxSteps` 变为 `steps`。旧 `mode` 映射中的条目变为主 agent。

Agent 的 [`request.body`](../agents/index.md#request)会被保留但不会发送给模型，因此 V1 的 `temperature`、`top_p` 和 `options` 在那里不起作用。请改为在模型变体上设置它们。DeepSeek 只在关闭思考时应用 `temperature`，所以下面这个变体同时关闭了思考：

```jsonc title="opencode.jsonc"
{
  "providers": {
    "opencode": {
      "models": {
        "deepseek-v4.1-flash": {
          "variants": [{ "id": "review", "body": { "thinking": { "type": "disabled" }, "temperature": 0.2 } }],
        },
      },
    },
  },
  "agents": {
    "reviewer": { "model": "opencode/deepseek-v4.1-flash#review" },
  },
}
```

provider 的 JSON 字段用 `body`，provider 包选项用 `settings`。参见[模型选项](../models/index.md#options)。

### Snapshots

把单数的 `snapshot` 字段重命名为 `snapshots`。它的布尔值不变：

```jsonc
// V1
{ "snapshot": false }

// V2
{ "snapshots": false }
```

### Media

把单数的 `attachment` 对象重命名为 `media`。嵌套的图片设置名称不变：

```jsonc
// V1
{ "attachment": { "image": { "auto_resize": true } } }

// V2
{ "media": { "image": { "auto_resize": true } } }
```

### MCP 服务器

V2 把服务器归到 `mcp.servers` 下，用取反的 `disabled` 取代 `enabled`，并拆分超时的用途：

```jsonc
// V1
{
  "mcp": {
    "playwright": {
      "type": "local",
      "command": ["npx", "@playwright/mcp"],
      "enabled": true,
      "timeout": 30000
    }
  }
}

// V2
{
  "mcp": {
    "servers": {
      "playwright": {
        "type": "local",
        "command": ["npx", "@playwright/mcp"],
        "disabled": false,
        "timeout": {
          "catalog": 30000,
          "execution": 30000
        }
      }
    }
  }
}
```

远程 OAuth 字段改为蛇形命名：`clientId` 变为 `client_id`，`clientSecret` 变为 `client_secret`，`callbackPort` 变为 `callback_port`，`redirectUri` 变为 `redirect_uri`。V1 的 `experimental.mcp_timeout` 值也变为默认的 `mcp.timeout.catalog` 和 `mcp.timeout.execution` 值。参见 [MCP 服务器](../mcp-servers/index.md)。

### 压缩

V2 把保留上下文的 token 预算归到 `keep` 下，并给预留部分起了更清晰的名字：

```jsonc
// V1
{
  "compaction": {
    "preserve_recent_tokens": 8000,
    "reserved": 20000
  }
}

// V2
{
  "compaction": {
    "keep": {
      "tokens": 8000
    },
    "buffer": 20000
  }
}
```

V1 的 token 数按原样沿用。V2 还接受模型窗口的百分比，例如 `"buffer": "15%"`，这适合窗口大小不同的模型。

`auto` 名称不变。V2 没有原生的 `tail_turns` 或 `prune` 字段；这两个旧字段会被忽略并给出警告。最近的上下文改为按 token 预算保留。参见[压缩](../compaction/index.md)。

### 技能

V1 将额外的技能路径和 URL 分开。V2 把两者合并为一个有序数组：

```jsonc
// V1
{
  "skills": {
    "paths": ["./team-skills"],
    "urls": ["https://example.com/skills/"]
  }
}

// V2
{
  "skills": ["./team-skills", "https://example.com/skills/"]
}
```

现有的技能文件和自动的 `.opencode/skills/` 发现机制不变。参见[技能](../skills/index.md)。

### 命令

把单数的 `command` 映射重命名为 `commands`，`subtask` 重命名为 `subagent`。把单独的模型 `variant` 以 `#` 连接到模型引用：

```jsonc
// V1
{
  "command": {
    "review": {
      "template": "Review the current changes.",
      "model": "anthropic/claude-sonnet-5-5",
      "variant": "high",
      "subtask": true
    }
  }
}

// V2
{
  "commands": {
    "review": {
      "template": "Review the current changes.",
      "model": "anthropic/claude-sonnet-5-5#high",
      "subagent": true
    }
  }
}
```

`template`、`description` 和 `agent` 名称不变。旧版 `subtask` 仍然被接受；被委派的命令现在会在后台自动运行，并把结果报告给父会话。现有的 Markdown 命令定义继续受支持。参见[命令](../commands/index.md)。

### 引用

把已弃用的单数 `reference` 映射重命名为 `references`：

```jsonc
// V1
{ "reference": { "docs": "../docs" } }

// V2
{ "references": { "docs": "../docs" } }
```

V1 本来就接受 `references`，所以文件如果已经用它就无需改动。引用条目的结构不变。参见[引用](../references/index.md)。

### Providers

把单数的 `provider` 映射重命名为 `providers`。V2 把运行时包、端点和请求设置分开：

```jsonc
// V1
{
  "provider": {
    "acme": {
      "npm": "@ai-sdk/openai-compatible",
      "api": "https://llm.example.com/v1",
      "options": {
        "apiKey": "{env:ACME_API_KEY}"
      }
    }
  }
}

// V2
{
  "providers": {
    "acme": {
      "package": "aisdk:@ai-sdk/openai-compatible",
      "settings": {
        "baseURL": "https://llm.example.com/v1",
        "apiKey": "{env:ACME_API_KEY}"
      }
    }
  }
}
```

V1 的 `npm` 变为 `package`，AI SDK 包会加上 `aisdk:` 前缀。`api` 变为 `settings.baseURL`。provider 的 `options` 会按照其请求角色拆分为 `settings`、`headers` 和 `body`。`options.setCacheKey` 变为 provider 上的 `compatibility.supportsPromptCacheKey`。参见 [Providers](../providers/index.md)。

V2 合并了两个旧版 provider 命名空间：

| V1 provider ID             | 规范的 V2 provider ID |
| -------------------------- | ------------------------ |
| `azure-cognitive-services` | `azure`                  |
| `google-vertex-anthropic`  | `google-vertex`          |

对无歧义的 V1 provider、agent、命令和 provider 过滤字段的迁移都使用这些规范 ID。共享的顶层 `model` 字段保留其确切的 provider ID，因为同样的语法在原生 V2 配置中也是有效的；迁移旧版内置 provider 时请把该字段更新为规范 ID。

### 模型和变体

模型仍嵌套在 provider 之下，但若干模型字段变得更加显式：

- `id` 变为 `modelID`。
- `tool_call` 和 `modalities` 变为 `capabilities.tools`、`capabilities.input` 和 `capabilities.output`。
- `"deprecated"` 的 `status` 变为 `disabled: true`。
- 缓存费用从 `cache_read` 和 `cache_write` 移到 `cache.read` 和 `cache.write`。
- provider 专属的 `options` 变为 `settings`。
- V1 的 variants 对象变为 V2 数组，每个条目带一个 `id`。

```jsonc
// V1
{
  "variants": {
    "high": {
      "reasoningEffort": "high"
    }
  }
}

// V2
{
  "variants": [
    {
      "id": "high",
      "settings": {
        "reasoningEffort": "high"
      }
    }
  ]
}
```

完整的原生模型结构参见[模型](../models/index.md)。

### 没有直接原生对应物的受支持字段

大多数结构不变的字段——包括 `shell`、`model`、`default_agent`、`watcher`、`formatter`、`instructions`、`enterprise` 和 `tool_output`——无需迁移。

V2 接受并保留 `lsp` 配置，但不会运行语言服务器、不提供 LSP 工具，也不产生 LSP 诊断。请把依赖这些能力的工作流替换为项目的 lint、typecheck 或编译器命令。

V1 的 provider 过滤器没有一对一的原生 V2 配置字段，但其行为仍通过[策略](../policies/index.md)受支持：

- `enabled_providers` 变为一条内部的默认拒绝 provider 策略，后跟对所列 provider 的 allow。
- `disabled_providers` 变为针对所列 provider 的内部 deny 策略。
- `autoupdate` 变为 `update`：`false` 映射为 `"disable"`，`"notify"` 映射为 `"notify"`，`true` 映射为 `"auto"`。
- `small_model` 变为内置 `title` agent 的 `model` 选择。原生 V2 配置应改用 `agents.title.model`。

你可以继续用 V1 语法保留这些字段。OpenCode 会不带警告地规范化它们。

### 接受但不支持的字段

V1 schema 还接受过一些没有任何受支持 V2 行为的字段。V2 会忽略这些值并发出警告，以免被误认为生效的配置：

- `logLevel`：启动 OpenCode 时使用 `OPENCODE_LOG_LEVEL`。
- `server`：使用 V2 服务和显式服务器选项；服务器 API 是有意的破坏性变更。
- 顶层 `subagent_depth`：改用 `experimental.subagent_depth`。
- `compaction.tail_turns` 和 `compaction.prune`：V2 改用 `compaction.keep.tokens` 和基于检查点的压缩。
- V1 JSON 配置中 agent 的 `name`。
- 没有 `type` 的仅 enabled V1 MCP 条目。
- V1 实验性字段 `batch_tool`、`openTelemetry`、`primary_tools` 和 `continue_loop_on_deny`。
- V1 provider 字段 `id`、`whitelist` 和 `blacklist`。
- V1 provider-model 字段 `release_date`、`attachment`、`reasoning`、`temperature`、`experimental`、非 `deprecated` 的 `status`，以及布尔值 `interleaved`。

忽略这些字段是有意的，不属于兼容性退化。如果 V2 未保留本指南在其他地方认定为受支持的行为，请按照[故障排除](../troubleshooting/index.md)中的问题报告指引操作。

### Agent 文件

V1 agent 文件可能使用 `agent/`、`agents/`、`mode/` 或 `modes/`。V2 仍然会发现全部四个目录。推荐的 V2 位置是：

```text
.opencode/agents/<name>.md
```

V1 `mode/` 或 `modes/` 目录下的文件表示主 agent。把它们移动到 `agents/` 时，请在 frontmatter 中加上 `mode: primary`。`agent/` 下的文件可以移动到 `agents/` 而不改变其路径派生的 ID。

把 frontmatter 转换为原生 V2 字段时：

- 保留 Markdown 正文作为 agent 的系统指令。
- 在 JSON 配置中出现时把 `prompt` 重命名为 `system`；文件正文不需要 `system` 字段。
- 把 `disable` 重命名为 `disabled`，`permission` 重命名为 `permissions`。
- 把 `model` 和 `variant` 组合为 `provider/model#variant`。
- 按上文[所示](agent-和模式)在模型变体上设置采样和 provider 选项。

V1 agent frontmatter 已弃用，但仍会自动转换。每个文件都按一种格式读取。使用了 `permissions`、`request`、`system` 或 `disabled` 中任意一项的文件按 V2 读取，其中的 V1 字段（如 `name`、`tools`、`permission` 或 `temperature`）会被忽略并在日志中警告。其他使用 V1 字段的文件按 V1 读取。请一次性转换文件的 frontmatter，不要混用两种格式。参见 [Agent](../agents/index.md)。

### 命令文件

V1 命令文件可能使用 `command/` 或 `commands/`。V2 会发现两者。推荐的位置是：

```text
.opencode/commands/<name>.md
```

把文件从 `command/` 移动到 `commands/` 下相同的相对路径，以保留命令名。Markdown 正文仍是命令模板，`description` 和 `agent` frontmatter 名称不变。把 `subtask` 重命名为 `subagent` 以使用后台委派的原生名称。如果 frontmatter 中有分开的 `model` 和 `variant` 字段，请把变体附加到模型并移除 `variant`：

```yaml
# V1
model: anthropic/claude-sonnet-5-5
variant: high
subtask: true

# V2
model: anthropic/claude-sonnet-5-5#high
subagent: true
```

参见[命令](../commands/index.md)。

### 技能文件

V2 会同时从 `.opencode/skill/` 和 `.opencode/skills/` 发现技能。推荐的布局是：

```text
.opencode/skills/<skill-id>/SKILL.md
```

请移动完整的技能目录而不只是 `SKILL.md`，以便相对路径的脚本、引用和其他支持文件仍然可用。保持目录名稳定以保留技能 ID。现有的技能 frontmatter 和 Markdown 正文不需要为 V2 重写。参见[技能](../skills/index.md)。

### 指令文件

现有的 `AGENTS.md` 文件原地保留。V2 会发现全局的 `~/.config/opencode/AGENTS.md`，以及从当前目录向上直到用户主目录的环境 `AGENTS.md` 文件。主目录之外的项目，发现到项目根目录为止。

如果 V1 的设置依赖 `CLAUDE.md` 兜底，请把这些指引移到适用的 `AGENTS.md` 中。V2 目前只发现 `AGENTS.md`；由于非 API 的 V1 行为旨在保持兼容，请连同受影响项目的详情一并提交兼容性问题。参见[指令](../instructions/index.md)。

## 终端客户端配置

V2 用一个全局终端客户端配置文件取代分层的 V1 `tui.json(c)` 文件：

```text
~/.config/opencode/cli.json
```

终端客户端拥有这个文件；后台服务不加载它。当 `cli.json` 不存在时，首次 V2 终端客户端启动会迁移受支持的全局 `tui.json` 设置和持久化偏好，同时保持 V1 文件不变。项目本地的客户端配置不会被迁移，因为 V2 客户端配置是全局的。当前客户端设置的参考请见 [CLI 设置](../cli/config/index.md)。

## 插件

把 `plugin` 重命名为 `plugins`。把包加选项的元组替换为对象：

```jsonc
// V1
{
  "plugin": ["opencode-example-plugin", ["./plugin/local.ts", { "enabled": true }]]
}

// V2
{
  "plugins": [
    "opencode-example-plugin",
    {
      "package": "./plugin/local",
      "options": { "enabled": true }
    }
  ]
}
```

V2 会同时从 `.opencode/plugin/` 和 `.opencode/plugins/` 发现本地插件；V2 文件请使用 `.opencode/plugins/`。配置的本地路径必须是目录，因此请把迁移的插件移到 `./plugin/local/index.ts`。

<Callout type="warning">
  V1 插件实现无法在 V2 中运行。移动文件或重命名其配置条目是不够的。
</Callout>

请按照专门的[插件迁移指南](../build/plugins/migrate-v1/index.md)迁移入口点、hook、工具、事件和包导出。

## 服务器 API 和客户端

OpenCode 2 有一套经过修订、更符合人体工学的服务器 API 和一组新的客户端。调用 V1 服务器 API 的集成必须迁移到 V2 API。

使用 `@opencode/client` 包访问已发布的 V2 API。它的端点、请求类型和响应请参见生成的 [API 参考](../api/index.md)。

### 服务器身份验证

V2 服务器仍使用 HTTP Basic 认证，但有这些变化：

- `OPENCODE_PASSWORD` 设置密码。`OPENCODE_SERVER_PASSWORD` 仍然可用。
- `OPENCODE_SERVER_USERNAME` 不再受支持。用户名始终是 `opencode`。

```bash
# V1
OPENCODE_SERVER_USERNAME=alice OPENCODE_SERVER_PASSWORD=secret opencode serve

# V2
OPENCODE_PASSWORD=secret opencode serve
```

参见 [Web](../cli/web/index.md#authentication)。

## 验证你的设置

在把 V2 用于日常工作之前，请先在一个项目中验证你的模型、provider 凭据、agent、权限、MCP 服务器和插件。在确认所需的 V2 行为之前保留你的 V1 设置，并且不要让 V1 指向你已转换为原生 V2 形态的配置。
