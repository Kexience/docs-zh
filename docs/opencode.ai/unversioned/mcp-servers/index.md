---
source_url: https://opencode.ai/docs/mcp-servers/
source_hash: sha256:f2b5da3576afa5fd764a979bc8ce8bafbe39252775f0836af8906f315360d495
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# MCP 服务器

OpenCode 可以连接 [Model Context Protocol](https://modelcontextprotocol.io/)（MCP）服务器，并暴露工具、提示、资源和指令等能力。MCP 工具会占用模型上下文，因此只添加你需要的服务器。

## 设置

从要使用它的项目里添加一个远程服务器，然后检查其连接状态：

```sh
opencode mcp add context7 --url https://mcp.context7.com/mcp
opencode mcp list
```

该命令会把服务器写入项目[配置](../config/index.md)。加上 `--global` 可让它在所有项目中可用：

```sh
opencode mcp add context7 --global --url https://mcp.context7.com/mcp
```

远程服务器默认使用 OAuth。如果列表显示 `needs authentication`，打开 OpenCode，运行 `/mcps`，选中该服务器并登录。连接成功的服务器就可以供 agent 使用：

```text
✓ context7  connected
```

## 配置

要手动配置服务器，在 `mcp.servers` 下给它一个唯一名称。V2 不允许把服务器名称直接放在 `mcp` 下面。

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "servers": {
      "my-server": {
        "type": "local",
        "command": ["npx", "-y", "example-mcp-server"],
      },
    },
  },
}
```

服务器会自动连接。如果想保留配置但不连接，使用 `disabled`，而不是 `enabled` 字段：

```jsonc
{
  "mcp": {
    "servers": {
      "my-server": {
        "type": "local",
        "command": ["npx", "-y", "example-mcp-server"],
        "disabled": true,
      },
    },
  },
}
```

更高优先级的项目配置会整体替换同名服务器的对象。要区分不同的连接或账号，请使用不同的名称；否则就需要在覆盖中重复每一个必填字段：

```jsonc title="opencode.jsonc"
{
  "mcp": {
    "servers": {
      "my-server": {
        "type": "remote",
        "url": "https://mcp.example.com/mcp",
      },
    },
  },
}
```

## 本地

本地服务器是 OpenCode 通过 MCP stdio 传输启动的一个命令。用 `--` 之后的命令添加：

```sh
opencode mcp add everything -- npx -y @modelcontextprotocol/server-everything
```

通过重复的 `--env` 标志传递环境变量：

```sh
opencode mcp add everything --env LOG_LEVEL=info -- npx -y @modelcontextprotocol/server-everything
```

其他进程选项（如工作目录）请使用配置：

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "servers": {
      "everything": {
        "type": "local",
        "command": ["npx", "-y", "@modelcontextprotocol/server-everything"],
        "cwd": ".",
        "environment": {
          "LOG_LEVEL": "info",
          "MCP_API_KEY": "{env:MCP_API_KEY}",
        },
      },
    },
  },
}
```

| 字段 | 必填 | 描述 |
| --- | --- | --- |
| `type` | 是 | 必须为 `"local"`。 |
| `command` | 是 | 可执行文件及其参数。 |
| `cwd` | 否 | 进程目录。相对路径以工作区为基准解析，这也是默认值。 |
| `environment` | 否 | 添加到 OpenCode 继承的进程环境中的字符串变量。 |
| `disabled` | 否 | 为 `true` 时阻止连接。默认为 `false`。 |
| `codemode` | 否 | 设为 `false` 可直接暴露工具，而不是通过 Code Mode。默认为 `true`。 |
| `timeout` | 否 | 每个服务器的超时覆盖。 |
| `protocol` | 否 | `legacy`（默认）、`auto` 或 `2026-07-28`。参见[协议版本](#协议版本)。 |
| `pool` | 否 | 跨目录共享一条连接。默认为 `false`。参见[共享连接](#共享连接)。 |

用 `{env:NAME}` 做环境变量替换。`$NAME` 之类的 shell 表达式在 JSON 字符串中不会被展开：

```jsonc
{
  "environment": {
    "MCP_API_KEY": "{env:MCP_API_KEY}",
  },
}
```

## 远程

远程服务器使用 MCP Streamable HTTP 传输，需要绝对 URL：

```sh
opencode mcp add context7 --url https://mcp.context7.com/mcp
```

通过重复的 `--header` 标志传递请求头。给 `{env:NAME}` 引用加引号，让 shell 原样写入：

```sh
opencode mcp add context7 --url https://mcp.context7.com/mcp --header 'CONTEXT7_API_KEY={env:CONTEXT7_API_KEY}'
```

其他选项请使用配置。密钥应存放在环境变量中，而不是写进文件：

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "servers": {
      "context7": {
        "type": "remote",
        "url": "https://mcp.context7.com/mcp",
        "oauth": false,
        "headers": {
          "CONTEXT7_API_KEY": "{env:CONTEXT7_API_KEY}",
        },
      },
    },
  },
}
```

| 字段 | 必填 | 描述 |
| --- | --- | --- |
| `type` | 是 | 必须为 `"remote"`。 |
| `url` | 是 | 绝对的 Streamable HTTP endpoint。 |
| `headers` | 否 | 发送到该 endpoint 的字符串型 HTTP 头。 |
| `oauth` | 否 | OAuth 设置，或设为 `false` 以禁用 OAuth。 |
| `disabled` | 否 | 为 `true` 时阻止连接。默认为 `false`。 |
| `codemode` | 否 | 设为 `false` 可直接暴露工具，而不是通过 Code Mode。默认为 `true`。 |
| `timeout` | 否 | 每个服务器的超时覆盖。 |
| `protocol` | 否 | `legacy`（默认）、`auto` 或 `2026-07-28`。参见[协议版本](#协议版本)。 |
| `pool` | 否 | 跨目录共享一条连接。默认为 `false`。参见[共享连接](#共享连接)。 |

只有当服务器完全使用 API key 或其他头凭证时才使用 `oauth: false`：

```jsonc
{
  "type": "remote",
  "url": "https://mcp.example.com/mcp",
  "oauth": false,
  "headers": { "Authorization": "Bearer {env:MCP_API_KEY}" },
}
```

## OAuth

除非 `oauth` 为 `false`，否则远程服务器默认启用 OAuth。OpenCode 会发现授权服务器，用 PKCE 登录并刷新 token。凭证存放在项目配置之外。

大多数服务器只需要 URL：

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "servers": {
      "sentry": {
        "type": "remote",
        "url": "https://mcp.sentry.dev/mcp",
      },
    },
  },
}
```

如果服务器需要认证，运行 `/mcps`，选中它，然后在浏览器中完成授权。CLI 也可以发起同样的流程：

```sh
opencode mcp auth sentry
```

### 浏览器在另一台机器上

当 OpenCode 通过 SSH、容器或远程服务器运行时，登录后浏览器无法连回 OpenCode，会显示一个加载不出来的页面。从地址栏复制该页面的 URL，粘贴到登录提示中：

```text
http://127.0.0.1:52817/callback?code=...&state=...
```

在 OpenCode 等待浏览器的期间，这个提示会出现在 `/mcps`、`opencode mcp auth`，以及桌面端和 Web 应用的登录对话框中。

### 客户端注册

OpenCode 按以下顺序使用第一个适用的方式向授权服务器表明自己的身份：

| 方式 | 适用条件 |
| --- | --- |
| 预注册客户端 | 配置了 `oauth.client_id`。 |
| [Client ID Metadata Document](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization#client-id-metadata-documents)（CIMD） | 授权服务器支持 CIMD 和公共客户端，且未设置 `oauth.redirect_uri`。 |
| [动态客户端注册](https://datatracker.ietf.org/doc/html/rfc7591)（DCR） | 以上都不适用。OpenCode 注册一个客户端，并在之后的登录中复用。 |

授权服务器通过其元数据声明支持 CIMD：

```json
{
  "issuer": "https://auth.example.com",
  "client_id_metadata_document_supported": true,
  "token_endpoint_auth_methods_supported": ["none"]
}
```

使用 CIMD 时，OpenCode 把自己的元数据文档 URL 作为 `client_id` 发送，并跳过注册：

```text
https://opencode.ai/oauth/opencode/client.json
```

该文档允许这些不带端口的回环重定向：

- `http://127.0.0.1/callback`
- `http://localhost/callback`
- `http://127.0.0.1/mcp/oauth/callback`（供较旧的客户端使用）

授权服务器对这类重定向接受任意回环端口，[RFC 8252](https://datatracker.ietf.org/doc/html/rfc8252#section-7.3) 也是这样要求的，因此 `callback_port` 可以与 CIMD 搭配。自定义的 `redirect_uri` 则不行，此时 OpenCode 会回退到 DCR。

如果授权服务器既不支持 CIMD 也不支持 DCR，请配置预注册客户端。

### 预注册客户端

当 provider 提供客户端凭证时，使用 V2 的 snake_case OAuth 字段：

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "servers": {
      "company-tools": {
        "type": "remote",
        "url": "https://mcp.example.com/mcp",
        "oauth": {
          "client_id": "{env:MCP_CLIENT_ID}",
          "client_secret": "{env:MCP_CLIENT_SECRET}",
          "scope": "tools:read tools:execute",
          "callback_port": 19876,
          "redirect_uri": "http://127.0.0.1:19876/callback",
        },
      },
    },
  },
}
```

| 字段 | 描述 |
| --- | --- |
| `client_id` | 预注册的客户端 ID。优先于 CIMD 和 DCR。 |
| `client_secret` | 机密客户端（confidential client）的密钥，随 token 请求体发送。公共客户端可省略。 |
| `scope` | 以空格分隔的请求范围。默认为服务器拒绝未认证请求时给出的 scope。 |
| `callback_port` | 本地回调端口，取值 1 到 65535。默认取 `redirect_uri` 的端口，否则使用一个可用的临时端口。 |
| `redirect_uri` | 预注册的回环 URI，其路径和端口要能到达本地回调监听器。设置它会禁用 CIMD。 |
| `auth_server_metadata_url` | 授权服务器的 OAuth 或 OpenID Connect 元数据文档 URL。当 MCP 服务器没有发布指明其授权服务器的受保护资源元数据时设置它。 |

需要重新登录或切换账号时，移除已存储的 OAuth 凭证：

```sh
opencode mcp logout sentry
```

## 超时

超时值为正整数毫秒。在 `mcp.timeout` 下设置默认值；单个服务器的 `timeout` 对象会覆盖对应的默认值。

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "timeout": {
      "startup": 45000,
      "catalog": 30000,
      "execution": 600000,
    },
    "servers": {
      "slow-tools": {
        "type": "remote",
        "url": "https://mcp.example.com/mcp",
        "timeout": {
          "catalog": 60000,
        },
      },
    },
  },
}
```

| 超时项 | 默认值 | 适用于 |
| --- | --- | --- |
| `startup` | 30 秒 | 传输连接与服务器初始化。 |
| `catalog` | 30 秒 | 列出工具、提示、资源和资源模板。 |
| `execution` | 12 小时 | 工具调用、提示获取和资源读取。 |

## 协议版本

默认情况下，OpenCode 以经典的 MCP `initialize` 握手打开每个服务器。将某个服务器的 `protocol` 设置好，即可与基于 2026-07-28 修订版构建的服务器通信：

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "servers": {
      "modern": {
        "type": "remote",
        "url": "https://mcp.example.com/mcp",
        "protocol": "auto",
      },
    },
  },
}
```

| 取值 | 行为 |
| --- | --- |
| `legacy` | 默认。发送 `initialize`，支持到 2025-11-25 为止的协议修订版。 |
| `auto` | 用 `server/discover` 探测 2026-07-28 修订版，服务器不支持时回退到 `legacy`。 |
| `2026-07-28` | 要求 2026-07-28 修订版。对较旧的服务器连接会失败。 |

探测本地 `legacy` 服务器会额外产生一个短生命周期的进程，并且当服务器忽略未知请求时可能等待整个启动超时，因此请把 `auto` 限定在确实需要的服务器上。

## 共享连接

一个 OpenCode 服务器可以同时打开多个目录，每个目录都会独立连接每一个 MCP 服务器。把 `pool` 设为 `true`，可以让设置相同的目录共享一条连接和一个工具列表：

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "servers": {
      "cloudflare": {
        "type": "remote",
        "url": "https://mcp.cloudflare.com/mcp",
        "pool": true,
      },
    },
  },
}
```

- 只有 2026-07-28 修订版上的连接才会被共享。设置了 `pool` 后，未设置的 `protocol` 意味着 `auto`。以更旧修订版应答的服务器，或设置为 `legacy` 的服务器，会保持每个目录一条连接。
- 只有影响连接的一切因素都匹配时，目录之间才会共享连接：远程服务器的 URL、请求头、OAuth 设置和已登录账号，本地服务器的命令、工作目录和环境变量。超时和 `protocol` 也必须一致。服务器名称不必一致，但登录凭证按名称存储，因此 OAuth 服务器只有在同名下才会共享。
- 本地服务器只在本机的目录之间共享，不与工作区中的目录共享。跨项目共享需要固定的 `cwd`，例如 `"~"`。没有它就会在每个项目的文件夹中运行，于是每个项目各有一条，OpenCode 会记录警告。
- 共享连接没有 roots。当工具要求输入时，请求会出现在调用它的那个目录中。
- 一旦最后一个使用该连接的目录关闭或断开服务器，连接就会关闭。

## 名称

OpenCode 把工具命名为 `<server>_<tool>`。字母、数字、`_` 和 `-` 以外的字符都会替换为 `_`：

```text
server: context 7
tool:   resolve.library/id
name:   context_7_resolve_library_id
```

MCP 提示会变成名为 `<server>:<prompt>` 的命令，并采用同样的规范化。例如：

```text
/context_7:find_docs
```

命令文本按顺序填入提示的参数。用空格分隔它们，含空格的值要加引号：

```text
/context_7:find_docs react "server components"
```

选择短的服务器名称，并保证规范化之后仍然唯一。在默认的 Code Mode 下，工具按规范化后的服务器名称分组：

```text
tools.context_7.resolve_library_id(...)
```

## 权限

Code Mode 是默认方式。当某个服务器的工具必须保留在 provider 的原生工具列表中时，把 `codemode` 设为 `false`：

```jsonc
{
  "mcp": {
    "servers": {
      "context7": {
        "type": "remote",
        "url": "https://mcp.context7.com/mcp",
        "codemode": false,
      },
    },
  },
}
```

使用权限规则可以隐藏或拒绝工具，而无需断开其服务器。匹配规范化后的 `<server>_<tool>` 名称：

```jsonc
{
  "permissions": [
    {
      "action": "context7_*",
      "resource": "*",
      "effect": "deny",
    },
  ],
}
```

## 资源

agent 通过两个内置工具读取 MCP 资源：`list_mcp_resources` 和 `read_mcp_resource`。用以下权限规则控制它们：

| 规则 | 资源 |
| --- | --- |
| `opencode_list_mcp_resources` | 服务器名称。 |
| `opencode_read_mcp_resource` | `<server>:<uri>` |

例如，允许从 `docs` 服务器的所有读取：

```jsonc
{
  "permissions": [
    {
      "action": "opencode_read_mcp_resource",
      "resource": "docs:*",
      "effect": "allow",
    },
  ],
}
```

## 服务器指令

当服务器在初始化期间返回指令时，OpenCode 会把它们加入系统提示：

```text
<mcp_instructions>
  <server name="sentry">
    Search for an existing issue before creating a new one.
  </server>
</mcp_instructions>
```

对于使用 Code Mode 的服务器，OpenCode 会额外添加一行，说明 agent 可以在哪里找到该服务器的工具。

当 agent 的权限拒绝了某个服务器的全部工具时，该服务器的指令会被省略。当权限只拒绝 `execute` 时，服务器的工具会直接列出，其指令保留，但去掉 Code Mode 那一行。

## 输入请求

服务器可以在调用过程中通过 MCP elicitation 请求输入。OpenCode 会把请求显示为表单，URL 请求则显示为要打开的链接：

```text
sentry is requesting input
```

关闭表单即取消请求。

## 上下文

对于代表某个会话发起的调用，OpenCode 会在 `CallToolRequest.params._meta["ai.opencode/sessionID"]` 中发送会话 ID。这适用于 stdio 和 Streamable HTTP 上的直接工具与 Code Mode：

```json
{
  "method": "tools/call",
  "params": {
    "name": "lookup",
    "arguments": { "query": "example" },
    "_meta": { "ai.opencode/sessionID": "ses_..." }
  }
}
```

这个 ID 是请求元数据，不是工具参数，因此不会出现在模型可见的 schema 中。请把它当作不透明的关联值对待：

| 规则 | 行为 |
| --- | --- |
| 身份 | 它标识发起调用的 OpenCode 会话，而不是 MCP 传输会话。 |
| 存在性 | 没有会话上下文的调用中可能缺失。 |
| 安全性 | 不要仅凭它做认证或授权。 |
| 隐私 | 远程服务器会收到原始 ID，并可能记录或保留它。 |

## 管理

从任何项目列出服务器及其当前连接状态：

```sh
opencode mcp list
```

在 OpenCode 中使用 `/mcps` 查看、连接、断开或认证服务器。用 CLI 添加服务器并管理 OAuth 凭证：

```sh
opencode mcp add sentry --url https://mcp.sentry.dev/mcp
opencode mcp auth sentry
opencode mcp logout sentry
```

运行不带名称的 `opencode mcp auth`，可以从支持 OAuth 的服务器中选择：

```sh
opencode mcp auth
```

要移除服务器，把它当初添加进去的项目或全局配置里的条目删掉即可：

```jsonc
{
  "mcp": {
    "servers": {},
  },
}
```

在 `/mcps` 中断开服务器不会更改配置。要修改 OAuth 客户端设置、超时、工作目录，或想让某个服务器保持断开，请直接编辑配置：

```jsonc
{
  "mcp": {
    "servers": {
      "sentry": {
        "type": "remote",
        "url": "https://mcp.sentry.dev/mcp",
        "disabled": true,
      },
    },
  },
}
```
