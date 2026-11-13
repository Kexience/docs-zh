---
source_url: https://opencode.ai/docs/cli/acp/
source_hash: sha256:698af6b5ba3dad2df3d6bd94478504450b69e3962558ee4c5a84ae95ecd49429
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# ACP

`opencode acp` 会把 OpenCode 作为 [Agent Client Protocol](https://agentclientprotocol.com) agent 运行，这样你就可以在 Zed 等 ACP 客户端中使用它。下面的示例把 OpenCode 添加到 Zed：

```json title="~/.config/zed/settings.json"
{
  "agent_servers": {
    "OpenCode": {
      "command": "opencode",
      "args": ["acp"]
    }
  }
}
```

其他 ACP 客户端使用相同的命令和 `acp` 参数，但配置文件和字段名可能不同。如果某个图形客户端找不到 `opencode`，请把 `command` 设置为 `which opencode` 输出的绝对路径。

## 身份验证

OpenCode 使用它已有的 provider 凭据。启动 ACP 客户端之前，先在终端中登录：

```bash
opencode auth login
```

OpenCode 提供一种身份验证方法 `opencode-login`。默认情况下它是一种 agent 身份验证方法。`authenticate` 请求只接受该方法，且不收集凭据。如果 provider 需要身份验证导致提示失败，OpenCode 会返回 ACP 的 `auth_required` 错误。

如果客户端把 `clientCapabilities.auth.terminal` 设为 `true`，则该身份验证方法会成为终端身份验证方法：

```json
{
  "id": "opencode-login",
  "name": "Login with opencode",
  "description": "Run `opencode auth login` in the terminal",
  "type": "terminal",
  "args": ["--login"]
}
```

客户端不得把该方法发送给 `authenticate`。相反，客户端应在启动 OpenCode 的命令上附加 `--login`（例如 `opencode acp --login`），并在终端中运行它。OpenCode 会执行 `opencode auth login` 流程然后退出。退出状态码 0 表示登录成功。客户端随后重新连接并再次发送 `initialize`。

如果客户端把 `clientCapabilities._meta["terminal-auth"]` 设为 `true`，则该身份验证方法会包含登录命令：

```json
{
  "id": "opencode-login",
  "name": "Login with opencode",
  "description": "Run `opencode auth login` in the terminal",
  "_meta": { "terminal-auth": { "command": "opencode", "args": ["auth", "login"], "label": "OpenCode Login" } }
}
```

## 故障排查

`opencode acp` 会在 stdin 上等待 ACP 消息，所以直接在终端里运行时看起来像卡住了。请改为从 ACP 客户端启动它。

如果客户端报告进程已退出或写入了无效的协议输出，请在客户端参数中的 `acp` 前面加上 `--print-logs`。这样 OpenCode 会把它的 ACP 日志和私有服务器日志写入 stderr，而 stdout 只承载 ACP 消息。

```bash
opencode --print-logs acp
```

## 协议参考

本节面向 ACP 客户端作者，列出 OpenCode 支持的 ACP 部分，以及 OpenCode 新增的 `_meta` 键。不认识这些键的客户端可以忽略它们。消息定义见 [ACP 文档](https://agentclientprotocol.com)。

### 传输

客户端把 `opencode acp` 作为子进程启动。两者通过 stdin 和 stdout 交换以换行分隔的 JSON-RPC 消息，使用 ACP 协议版本 1。

`opencode acp` 会为自己启动一个私有的 OpenCode 服务器。它不连接共享的后台服务，也不会为 ACP 打开网络端口。一个进程可以同时服务多个 ACP 会话。当客户端关闭 stdin 时它退出。

### 能力

OpenCode 的 `initialize` 响应包含以下 agent 能力：

```json
{
  "loadSession": true,
  "mcpCapabilities": { "http": true, "sse": false },
  "promptCapabilities": { "embeddedContext": true, "image": true },
  "sessionCapabilities": {
    "additionalDirectories": {},
    "close": {},
    "delete": {},
    "fork": {},
    "list": {},
    "resume": {}
  }
}
```

OpenCode 读取以下客户端能力：

| 能力                                   | 作用                                                            |
| -------------------------------------- | --------------------------------------------------------------- |
| `auth.terminal` 设为 `true`            | 身份验证方法是一种[终端身份验证方法](#身份验证)。               |
| `elicitation.form`                     | OpenCode 以表单形式提出[问题](#问题)。                          |
| `session.compaction`                   | OpenCode 通过 ACP 的更新上报[压缩](#压缩)。                     |
| `_meta["terminal-auth"]` 设为 `true`   | 身份验证方法包含[登录命令](#身份验证)。                         |

### 会话

客户端在创建会话时设置工作目录。OpenCode 使用该目录的配置，包括它的模型、agent、命令、技能、指令、插件和 MCP 服务器。

- `cwd` 必须是绝对路径。OpenCode 会以参数无效错误拒绝相对的 `cwd`。
- `session/load` 会重放已保存的消息。`session/resume` 和 `session/fork` 不会重放。
- 要加载、恢复或分叉会话，客户端必须把该会话所在目录作为 `cwd` 传入。OpenCode 会以参数无效错误拒绝不同的 `cwd`。
- `session/list` 每页最多返回 100 个会话。它接受 `cwd` 过滤器和 `cursor`。
- `session/close` 会中断进行中的工作，并将会话与 ACP 进程分离。OpenCode 保留已保存的会话。
- `session/delete` 会像 `session/cancel` 一样结束进行中的提示，然后移除会话。删除不存在的会话也会成功。
- 一个会话一次只运行一个提示。当第一个提示仍在进行时，OpenCode 会为第二个 `session/prompt` 返回错误。

### 取消

`session/cancel` 会以 `stopReason: "cancelled"` 结束进行中的提示。针对提示请求发送 `$/cancel_request` 效果相同。OpenCode 会拒绝挂起中的权限请求。取消后仍未完成的工具调用会被上报为 `failed`。

### 附加目录

客户端可以在 `session/new`、`session/load`、`session/resume` 和 `session/fork` 上传入 `additionalDirectories`：

```json
{ "cwd": "/work/app", "additionalDirectories": ["/work/shared"], "mcpServers": [] }
```

- 每一项都必须是不含 `*` 或 `?` 的绝对路径。
- OpenCode 允许在每个根目录内访问外部目录。读取、编辑和 shell 权限规则仍然适用。
- 每次请求中的列表会替换会话上一次的列表，正如[附加目录 RFD](https://agentclientprotocol.com/rfds/additional-directories) 所规定。
- OpenCode 把这些授权保存在会话上，因此其他 OpenCode 客户端使用该会话时它们同样生效。OpenCode 创建子会话时，子会话会复制这些授权。

`session/list` 在 `additionalDirectories` 中返回每个会话保存的列表。

### 配置选项

新会话使用该目录的默认模型和主 agent。`session/new`、`session/load`、`session/resume` 和 `session/fork` 的响应包含以下配置选项：

| ID       | 类别            | 值                                                            |
| -------- | --------------- | ------------------------------------------------------------- |
| `model`  | `model`         | 已启用的模型，形如 `provider/model`。`/variant` 后缀还会设置 effort。 |
| `effort` | `thought_level` | 模型的各变体以及 `default`。仅对有变体的模型存在。            |
| `mode`   | `mode`          | 可见的主 agent。                                              |

`session/set_config_option` 接受字符串值：

```json
{ "sessionId": "ses_123", "configId": "model", "value": "anthropic/claude-sonnet-5-5" }
```

`session/set_mode` 也会设置 agent。当可用模型或 agent 变化时，OpenCode 会发送 `config_option_update`。当另一个客户端更改了会话的模型或 agent 时，它也会发送一条。

### 提示内容

提示可以包含文本、图片、内嵌资源和资源链接。OpenCode 会忽略 audio 块，其他块的处理方式如下：

| 块                                                     | OpenCode 的处理方式                                                                    |
| ------------------------------------------------------ | -------------------------------------------------------------------------------------- |
| `text`                                                 | 发送给模型。                                                                           |
| `text`，audience 仅 `assistant`                        | 作为独立上下文发送给模型，不进入用户消息。                                             |
| `text`，audience 仅 `user`                             | 从模型输入中剔除。                                                                     |
| `image` 带 `data`                                      | 附加到提示。                                                                           |
| `image` 仅有 `uri`                                     | 作为资源链接处理。                                                                     |
| `resource` 带 `text`                                   | 在资源的路径或 URI 之后内联该文本。                                                    |
| `resource` 带 `blob`                                   | 如果有 `mimeType` 则附加，否则丢弃。                                                   |
| `resource_link` 指向 `file://` URI                     | 附加该文件。如果文件缺失或不可读，则改为发送 Markdown 链接。                           |
| `resource_link` 指向带 `path` 查询参数的 `zed://` URI  | 附加 `path` 处的文件。                                                                 |
| `resource_link` 指向其他 URI                           | 发送 Markdown 链接，例如 `[spec](https://example.com/spec.md)`。                       |

audience 来自块的 `annotations`。OpenCode 会拒绝既没有 `data` 也没有 `uri` 的 `image` 块。下面这个块仅作为模型的上下文：

```json
{ "type": "text", "text": "Open file: src/app.ts", "annotations": { "audience": ["assistant"] } }
```

### 命令

在 `session/new`、`session/load`、`session/resume` 或 `session/fork` 之后，OpenCode 会发送 `available_commands_update`，内容包括该目录的命令和内置的 `compact` 命令。当命令发生变化时，它会再发送一次更新。

```json
{
  "sessionUpdate": "available_commands_update",
  "availableCommands": [{ "name": "compact", "description": "Compact the session" }]
}
```

如果提示以 `/` 加某个可用命令的名称开头，OpenCode 会运行该命令，其余文本作为参数。以 `/` 开头的其他文本会作为普通提示发送。`/compact` 会运行[压缩](../../compaction/index.md)。

### MCP 服务器

客户端可以在 `session/new`、`session/load`、`session/resume` 和 `session/fork` 上传入 stdio 和 HTTP MCP 服务器。OpenCode 会把它们添加到会话所在目录，有效期是 `opencode acp` 进程的生命周期，因此该目录中的其他会话也能使用它们。OpenCode 会透传 HTTP 头，并且不对这些服务器使用 OAuth。它不宣传基于 SSE 的 MCP，也不支持基于 ACP 的 MCP。

| 情况                             | 行为                                                     |
| -------------------------------- | -------------------------------------------------------- |
| 与某个已配置服务器同名           | 客户端的服务器在该目录中替换已配置的那一个。             |
| [策略](../../policies/index.md)  | `integration.use` 规则仍然适用。                         |

```json
{ "type": "http", "name": "docs", "url": "https://mcp.example.com", "headers": [] }
```

### 权限

权限请求提供三个选项：

```json
[
  { "optionId": "once", "kind": "allow_once", "name": "Allow once" },
  { "optionId": "always", "kind": "allow_always", "name": "Always allow" },
  { "optionId": "reject", "kind": "reject_once", "name": "Reject" }
]
```

当请求会更改文件时，如果 OpenCode 能构建变更预览，它会附带 `diff` 内容。

### 问题

如果客户端声明了 `elicitation.form`，OpenCode 会以表单模式通过 `elicitation/create` 提出问题。当 OpenCode 曾把某个工具调用作为该会话的 `session/update` 发送时，请求会包含 `toolCallId`。

```json
{
  "mode": "form",
  "sessionId": "ses_123",
  "toolCallId": "call_1",
  "message": "Which package manager?",
  "requestedSchema": {
    "type": "object",
    "properties": { "pm": { "type": "string", "oneOf": [{ "const": "bun", "title": "Bun" }] } },
    "required": ["pm"]
  }
}
```

- OpenCode 绝不会发送可能收集机密信息的表单。
- 如果某个字段除了选项之外还接受手填答案，schema 会增加一个可选的 `<key>_custom` 字符串属性。对于单选，非空的自定义答案会替换所选选项；对于多选，OpenCode 会把它添加到已选项中。
- 如果用户拒绝或取消表单，OpenCode 会取消该问题。

如果 OpenCode 无法展示问题，它会取消该问题并告诉模型在没有答案的情况下继续。

### 压缩

如果客户端声明了 `session.compaction`，OpenCode 会使用 ACP [会话压缩](https://agentclientprotocol.com/rfds/session-compaction) RFD（目前处于 Preview 阶段）中的 `compaction_update` 和 `compaction_summary_chunk` 更新来上报压缩。当客户端加载会话时，OpenCode 会把每次已完成或失败的压缩作为一条更新重放。

```json
{
  "sessionUpdate": "compaction_update",
  "compactionId": "msg_123",
  "status": "completed",
  "summary": [{ "type": "text", "text": "..." }]
}
```

其他客户端收到的则是[压缩标记](#压缩标记)。子会话的压缩也是如此。

### 用量

提示响应包含来自 [end-turn usage](https://agentclientprotocol.com/rfds/end-turn-token-usage) RFD（草案）的 `usage`。`usage` 汇总本会话中该提示的各次模型调用，不包含子会话。

```json
{ "stopReason": "end_turn", "usage": { "inputTokens": 1200, "outputTokens": 340, "totalTokens": 1540 }, "_meta": {} }
```

在响应之前，OpenCode 会发送来自 [session usage](https://agentclientprotocol.com/rfds/session-usage) RFD 的 `usage_update`。只有当该提示消耗了 token 且 OpenCode 知道模型上下文大小时才会发送。`cost` 是会话的总花费，单位为美元。

```json
{ "sessionUpdate": "usage_update", "used": 1540, "size": 200000, "cost": { "amount": 0.012, "currency": "USD" } }
```

### 子会话

提示运行期间，OpenCode 会把来自其子会话的更新作为 `session/update` 通知发送到提示所在的会话上。每个更新都带有 `_meta["opencode/child-session"]`。OpenCode 会给工具调用 ID 加上 `<childSessionId>:` 前缀。如果子会话有标题，它还会给工具调用标题加上子会话标题前缀。

```json
{
  "sessionUpdate": "tool_call",
  "toolCallId": "ses_child:call_1",
  "title": "Explore the codebase: src/app.ts",
  "_meta": {
    "opencode/child-session": { "id": "ses_child", "parentID": "ses_123", "depth": 1, "title": "Explore the codebase" }
  }
}
```

| 字段       | 类型     | 说明                                                                        |
| ---------- | -------- | ---------------------------------------------------------------------------- |
| `id`       | `string` | 子会话的 ID。                                                               |
| `parentID` | `string` | 子会话的父会话 ID。                                                         |
| `depth`    | `number` | 提示会话的直接子会话为 1，其子会话的子会话为 2，依此类推。                  |
| `title`    | `string` | 子会话的标题。子会话没有标题时 OpenCode 会省略它。                          |

来自子会话的权限请求会在 `toolCall._meta` 上携带相同的键。提示结束后，OpenCode 停止发送子会话更新。来自子会话的权限请求和问题仍会送达客户端。

### 重试状态

当模型调用失败且 OpenCode 安排了重试时，它会发送带有 `_meta["opencode/retry"]` 的 `session_info_update`。重试开始时，OpenCode 会发送 `"opencode/retry": null`。收到提示响应时，请清除所有重试状态。

```json
{
  "sessionUpdate": "session_info_update",
  "_meta": {
    "opencode/retry": {
      "attempt": 1,
      "nextRetryAt": "2026-10-02T12:00:05.000Z",
      "error": { "type": "provider.rate-limit", "message": "Rate limit exceeded", "status": 429 }
    }
  }
}
```

| 字段          | 类型     | 说明                                                                                      |
| ------------- | -------- | ------------------------------------------------------------------------------------------ |
| `attempt`     | `number` | 重试的次数编号。                                                                          |
| `nextRetryAt` | `string` | 下一次尝试的时间，ISO 8601 格式。                                                         |
| `error`       | `object` | 包含 `type` 和 `message`。如果 provider 发送了 `status` 和 `response.body`，也会一并包含。 |

### 压缩标记

如果客户端没有声明 `session.compaction`，OpenCode 会通过带有 `_meta["opencode/compaction"]` 的 `session_info_update` 上报压缩进度。对于子会话压缩，OpenCode 始终使用标记。

```json
{
  "sessionUpdate": "session_info_update",
  "_meta": { "opencode/compaction": { "status": "started", "messageId": "msg_123", "reason": "auto" } }
}
```

| 字段        | 类型     | 说明                                                                                       |
| ----------- | -------- | ------------------------------------------------------------------------------------------ |
| `status`    | `string` | `started`、`completed` 或 `failed`。被取消的压缩为 `failed`。                              |
| `messageId` | `string` | 把一次压缩的开始与结束配对。请把它当作不透明的键。                                         |
| `reason`    | `string` | `auto` 或 `manual`。                                                                       |
| `error`     | `object` | 当 `status` 为 `failed` 时存在。形状与[重试](#重试状态)的 `error` 相同。                   |

标记不包含摘要。自动压缩可能在没有 `started` 标记的情况下失败。当客户端加载会话时，OpenCode 会把每次已完成或失败的压缩作为一个标记重放。
