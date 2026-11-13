---
source_url: https://opencode.ai/docs/config/
source_hash: sha256:6d4d8e0ecc7466b15c434737883545527fbce7041aec0fee75bf22ffe2b00eed
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# 配置

在项目中创建 `opencode.jsonc` 来配置 OpenCode。添加 schema 以便编辑器校验，然后只设置你需要的选项。

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-sonnet-5-5",
}
```

你也可以让 OpenCode 替你更新这个文件。

## 格式

OpenCode 支持 JSON 和 JSONC。当你需要注释或尾随逗号时，请使用 JSONC。

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  // Use this model by default.
  "model": "anthropic/claude-sonnet-5-5",
}
```

## 位置

把受管的、机器级范围的设置放在系统配置目录中：

| 平台 | 目录 |
| -------- | --------------------------------------- |
| macOS | `/Library/Application Support/opencode` |
| Linux | `/etc/opencode` |
| Windows | `%ProgramData%\opencode` |

系统目录的工作方式与全局目录相同。除了 `opencode.json(c)`，它还会为机器上的每个用户加载 `agents/`、`commands/`、`skills/` 和 `plugins/`：

```text
/etc/opencode/
├── opencode.json
├── agents/review.md
├── commands/release.md
└── skills/deploy/SKILL.md
```

在 macOS 上，OpenCode 还会读取由 MDM 工具为 `ai.opencode.managed` 域部署的受管偏好设置。用户专属的描述文件会取代机器级范围的描述文件：

```text
/Library/Managed Preferences/<user>/ai.opencode.managed.plist
/Library/Managed Preferences/ai.opencode.managed.plist
```

受管设置拥有最高优先级，因此用户和项目无法覆盖其中设定的值，且受管偏好设置的优先级高于系统目录。仅靠设置本身无法阻止用户添加 provider、MCP 服务器、agent 或插件；要在受管配置中使用[策略](../policies/index.md#precedence)来强制执行限制。

把适用于每个项目的用户设置放在全局配置中：

```text
~/.config/opencode/opencode.json(c)
```

把项目设置放在以下任一文件中：

```text
/home/user/projects/my-app/opencode.json(c)
/home/user/projects/my-app/.opencode/opencode.json(c)
```

OpenCode 从当前目录一直搜索到文件系统根目录。它先把最远目录到最近目录中的直接 `opencode.json(c)` 文件合并起来，然后按同样的顺序合并 `.opencode` 目录中的文件。这意味着每个被发现的 `.opencode` 配置都会覆盖所有直接配置。除非你需要这种行为，否则请在整个目录树中统一使用一种形式。

例如，从 `/home/user/projects/acme/packages/web` 启动 OpenCode：

```text
/etc/opencode/opencode.json
~/.config/opencode/opencode.json

/home/user/projects/acme/
├── opencode.json
└── packages/
    └── web/
        ├── opencode.json
        └── src/
```

OpenCode 按优先级从低到高应用这些文件：

1. `~/.config/opencode/opencode.json`
2. `/home/user/projects/acme/opencode.json`
3. `/home/user/projects/acme/packages/web/opencode.json`
4. `/etc/opencode/opencode.json`

包配置会覆盖仓库配置中匹配的设置，仓库配置又覆盖全局配置。系统配置覆盖以上全部。不冲突的设置会被保留。来自全局文件和项目文件的[策略](../policies/index.md#precedence)以相反的顺序评估，而系统策略的优先级高于所有其他策略。

## Schema

完整的 OpenCode 配置 schema 可在 [opencode.ai/config.json](https://opencode.ai/config.json) 获取。

在配置文件中添加 `$schema` 字段，即可在支持 JSON Schema 的编辑器中启用校验和自动补全：

```json title="opencode.json"
{
  "$schema": "https://opencode.ai/config.json"
}
```

请把该 schema 当作可用字段、可接受的值以及嵌套配置结构的权威来源。

### Shell

设置终端和 shell 工具使用的 shell。

```jsonc
{
  "shell": "/bin/zsh",
}
```

### 模型

以 `provider/model` 格式设置默认模型。根级默认值目前不保留 `#variant`；agent 和命令的模型引用可以选择变体。

```jsonc
{
  "model": "anthropic/claude-sonnet-5-5",
}
```

关于模型选择和本地模型，参见[模型指南](../models/index.md)。

### Agent

选择当会话未显式选择 agent 时使用的主 agent。

```jsonc
{
  "default_agent": "build",
}
```

关于内置和自定义 agent，参见 [agent 指南](../agents/index.md)。

### 更新

在全局配置中控制更新检查。把 `update` 设为 `"disable"` 可以跳过检查，设为 `"notify"` 表示在安装前提示可用更新，设为 `"auto"` 表示自动安装更新。省略时，`update` 默认为 `"notify"`。

自动安装不会重启正在运行的服务器。请手动重启以激活已安装的更新。项目级设置会被忽略。

```jsonc
{
  "update": "notify",
}
```

### 用户名

设置一个用户名。OpenCode 接受这个字段，但不会在对话中显示它。

```jsonc
{
  "username": "alice",
}
```

### 权限

定义有序规则，在 agent 对匹配的资源使用某个工具之前进行允许、拒绝或询问。

```jsonc
{
  "permissions": [
    {
      "action": "shell",
      "resource": "git push *",
      "effect": "ask",
    },
  ],
}
```

关于规则匹配和可用的操作，参见[权限指南](../permissions/index.md)。

### 策略

允许或拒绝某个 provider 的使用、硬性拒绝某项权限检查，或封锁某个 MCP 服务器、技能或插件，使用有序的语句，并且更宽泛的配置可以覆盖它们。

```jsonc
{
  "policies": [
    { "action": "provider.use", "resource": "*", "effect": "deny" },
    { "action": "provider.use", "resource": "anthropic", "effect": "allow" },
    { "action": "tool.use", "resource": "shell:git push *", "effect": "deny" },
  ],
}
```

关于匹配、跨配置文件的优先级以及由 Console 管理的策略，参见[策略指南](../policies/index.md)。

### Agents

覆盖内置 agent，或定义拥有各自模型、指令、模式和权限的专用 agent。

```jsonc
{
  "agents": {
    "reviewer": {
      "description": "Review changes without editing files",
      "mode": "subagent",
      "system": "Focus on correctness, security, and missing tests.",
      "permissions": [{ "action": "edit", "resource": "*", "effect": "deny" }],
    },
  },
}
```

关于全部 agent 选项和基于文件的 agent，参见 [agent 指南](../agents/index.md)。

### 快照

启用或禁用撤销和回退行为所使用的文件系统快照。

```jsonc
{
  "snapshots": false,
}
```

关于撤销和重做行为，参见[快照指南](../snapshots/index.md)。

### 监视器

忽略不应触发文件系统更新的文件和目录。

```jsonc
{
  "watcher": {
    "ignore": ["dist/**", "coverage/**"],
  },
}
```

### 格式化器

在 `write`、`edit` 或 `patch` 工具修改文件之后对文件进行格式化。把 `formatter` 设为 `true` 可启用可用的内置格式化器。

```jsonc
{
  "formatter": true,
}
```

关于内置和自定义格式化器，参见[格式化器指南](../formatters/index.md)。

### 媒体

控制 `read` 工具加载的超大图片在发送给模型之前如何被缩放或拒绝。

```jsonc
{
  "media": {
    "image": {
      "auto_resize": true,
      "max_width": 2000,
      "max_height": 2000,
      "max_base64_bytes": 5242880,
    },
  },
}
```

关于图片处理和限制，参见[附件指南](../attachments/index.md)。

### 输出

设置工具结果保留的最大行数和字节数。

```jsonc
{
  "tool_output": {
    "max_lines": 2000,
    "max_bytes": 51200,
  },
}
```

### 搜索

选择 OpenCode 进行网页搜索的方式。使用 `"random"` 可自动选择一个可用的 provider。

```jsonc
{
  "websearch": {
    "provider": "random",
  },
}
```

关于 provider、凭据、选择方式、速率限制和禁用搜索，参见[网页搜索指南](../websearch/index.md)。

### MCP

配置本地和远程 Model Context Protocol 服务器。全局 `mcp.timeout` 值适用于配置文件中定义的服务器；每个服务器自身的 `timeout` 会覆盖它们。

```jsonc
{
  "mcp": {
    "servers": {
      "playwright": {
        "type": "local",
        "command": ["bunx", "@playwright/mcp"],
      },
    },
  },
}
```

关于远程服务器、OAuth、环境变量和超时，参见 [MCP 指南](../mcp-servers/index.md)。

### 压缩（Compaction）

控制自动上下文压缩以及它保留多少近期上下文。

```jsonc
{
  "compaction": {
    "auto": true,
    "keep": {
      "tokens": 15000,
    },
    "buffer": "15%",
  },
}
```

`buffer` 是在自动压缩开始之前模型上下文窗口中保持空闲的比例。

本地摘要仍然是默认方式。要通过 provider 或模型策略为自动和手动请求启用原生 provider 压缩：

```jsonc
{
  "providers": {
    "openai": {
      "settings": { "compaction": { "type": "native" } },
      "models": {
        "gpt-6.1-sol": { "settings": { "compaction": { "type": "summary" } } },
      },
    },
  },
}
```

模型设置会覆盖 provider 设置。自动压缩使用所选模型的可用输入预算。provider 检查点在相同的 `compaction.keep.tokens` 预算内保留近期的用户消息，该预算也是本地摘要用于其保留尾部的预算。顶层的 `compaction.auto: false` 会禁用新的自动压缩，但不丢弃已安装的检查点。关于预算和溢出恢复，参见[压缩指南](../compaction/index.md)。

### 预热（Warming）

通过周期性的临时请求让最近活跃的模型会话保持温热。预热默认关闭；把它设为 `true` 可以在每个模型的缓存即将过期时进行预热，最长持续 30 分钟。

```jsonc
{
  "warming": {
    "prompt": "Do not perform any work. Reply with exactly: OK",
    "interval": "auto",
    "duration": "30 minutes",
  },
}
```

provider 或模型的 `settings.cache.warming` 会覆盖它，而 `settings.cache.ttl` 设置 provider 保留缓存的时长。关于请求行为、自定义和成本考量，参见[预热指南](../warming/index.md)；关于 `cache.ttl`，参见[缓存生命周期](../models/index.md#cache-lifetime)。

### 技能（Skills）

添加 OpenCode 应当在其中搜索 agent 技能的目录或 URL。

```jsonc
{
  "skills": ["./team-skills", "https://example.com/.well-known/skills/"],
}
```

关于技能结构和 `.opencode/skills/` 下的自动发现，参见[技能指南](../skills/index.md)。

### 命令

把可复用的斜杠命令定义为具名的提示词模板。

```jsonc
{
  "commands": {
    "review": {
      "description": "Review the current changes",
      "template": "Review the current diff for correctness and missing tests.",
    },
  },
}
```

关于参数、模型、agent 和基于文件的命令，参见[命令指南](../commands/index.md)。

### 指令（Instructions）

声明额外的指令文件、glob 模式或 HTTP(S) URL。OpenCode 会把它们与发现的 `AGENTS.md` 文件一起加载。

```jsonc
{
  "instructions": ["CONTRIBUTING.md", "docs/guidelines/*.md"],
}
```

关于项目指令和 `AGENTS.md`，参见[指令指南](../instructions/index.md)。

### 引用（References）

把本地目录或 Git 仓库作为具名的辅助上下文提供。

```jsonc
{
  "references": {
    "docs": {
      "path": "../product-docs",
      "description": "Product behavior and terminology",
    },
    "effect": {
      "repository": "Effect-TS/effect",
      "branch": "main",
    },
  },
}
```

关于简写形式、可见性和路径解析，参见[引用指南](../references/index.md)。

### Worktree

设置新本地 worktree 的父目录。OpenCode 会在其后附加请求的或生成的 worktree 名称。

```jsonc
{
  "worktree": {
    "directory": "../worktrees",
  },
}
```

相对路径相对于项目已保存的规范检出进行解析。全局配置和项目配置都适用此规则；绝对路径按原样使用，`~/` 相对于用户的主目录解析。

例如，下面的全局配置会把新的 worktree 放在每个项目自己的 `.lane/trees/` 目录下：

```jsonc
{
  "worktree": {
    "directory": ".lane/trees",
  },
}
```

没有这个设置时，创建会使用服务器数据目录下的 `worktree/<first-six-project-ID-characters>`。worktree 的创建和刷新会从项目已保存的规范检出加载配置，即使其他克隆共享其项目 ID 也是如此。更改它不会移动现有的 worktree。

Git 是内置的默认策略。注册了策略的[插件](../build/plugins/server/index.md#worktrees)在该插件运行时中会自动成为默认策略。项目操作使用规范检出的运行时。特定于策略的选项属于该插件，而不属于 `worktree` 配置对象。

### 插件

从包或本地插件目录加载插件。当插件接受选项时，使用对象形式。

```jsonc
{
  "plugins": [
    "opencode-example-plugin",
    {
      "package": "./plugins/local",
      "options": {
        "enabled": true,
      },
    },
  ],
}
```

关于插件加载和配置，参见[插件指南](../plugins/index.md)。

### Providers

配置 provider，并添加或覆盖它们的模型、请求设置、请求头和模型变体。

```jsonc
{
  "providers": {
    "openai": {
      "models": {
        "gpt-6.1-sol-custom": {
          "modelID": "gpt-6.1-sol",
          "name": "GPT-6.1 Sol Custom",
          "limit": {
            "context": 200000,
            "output": 32000,
          },
        },
      },
    },
  },
}
```

provider 的 `settings.transport: "websocket"` 会选择其会话 WebSocket。

关于凭据、自定义端点、provider 包、WebSocket 传输和模型配置，参见 [provider 指南](../providers/index.md)。

## 变量

你可以在配置文件中使用变量替换来引用环境变量和文件内容。请把引用放在 JSON 字符串内。

### 环境变量

使用 `{env:VARIABLE_NAME}` 替换环境变量：

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "model": "{env:OPENCODE_MODEL}",
  "providers": {
    "anthropic": {
      "settings": {
        "apiKey": "{env:ANTHROPIC_API_KEY}",
      },
    },
  },
}
```

如果环境变量未设置，它会被替换为空字符串。

### 文件

使用 `{file:path/to/file}` 替换文件的内容：

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "providers": {
    "openai": {
      "settings": {
        "apiKey": "{file:~/.secrets/openai-key}",
      },
    },
  },
}
```

文件路径可以是：

- 相对于配置文件所在目录
- 绝对路径，或以 `~/` 开头指向你的主目录

如果文件不存在，它会被替换为空字符串。

这些功能适用于：

- 把 API key 等敏感数据保存在单独的文件中。
- 在多个配置文件之间共享公共的配置片段。

## 实验性

<Callout type="warning">
  实验性设置可能在任何版本中变化、损坏或被移除，恕不另行通知。不要在稳定的工作流中依赖它们。
</Callout>

所有实验性设置都位于 `experimental` 键之下：

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "experimental": {
    "todo": true,
    "subagent_depth": 2,
    "background_compaction": true,
    "image_generate": { "model": "openai/gpt-image-2" },
    "location_idle_timeout": "4 hours",
  },
}
```

### 待办事项（Todos）

把 `todo` 设为 `true` 可以给 agent 提供一个 `todowrite` 工具来跟踪多步骤工作。默认为 `false`。

### Subagent 深度

`subagent_depth` 设置 subagent 可以启动自己的 subagent 的深度。默认为 `1`，因此 subagent 不能再启动另一个 subagent。

### 后台压缩

把 `background_compaction` 设为 `true` 可以在需要之前在后台写入压缩摘要，这样自动压缩就不会暂停会话。默认为 `false`。关于它的工作原理，参见[压缩](../compaction/index.md#background-compaction)。

```jsonc
{
  "experimental": {
    "background_compaction": true,
  },
}
```

### 图片生成

`image_generate` 为 [`experimental_image_generate`](../tools/index.md#image-generate) 工具设置默认模型，格式为 `providerID/modelID`，可选地附带 `#variant`。当该模型不可用或无法处理某个请求时，OpenCode 会自动选择另一个图片模型。

```jsonc
{
  "experimental": {
    "image_generate": {
      "model": "openai/gpt-image-2",
    },
  },
}
```

### 位置空闲超时

`location_idle_timeout` 控制一个项目位置可以在没有会话活动的情况下保持多久，之后 OpenCode 会卸载其服务。它接受诸如 `"2 hours"` 的时长，默认为 `"60 minutes"`。正在运行的会话和后台任务会让位置保持加载。把它设为 `false` 可以永不卸载空闲的位置。项目配置可以覆盖全局值。

```jsonc
{
  "experimental": {
    "location_idle_timeout": false,
  },
}
```

### 已弃用的策略

`experimental.policies` 已被弃用。请改用顶层的 [`policies`](../policies/index.md)。旧键仍然有效，并会合并到 `policies` 中。
