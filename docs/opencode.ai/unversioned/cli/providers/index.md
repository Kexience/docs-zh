---
source_url: https://opencode.ai/docs/cli/providers/
source_hash: sha256:e8dd9e28796d78f03381c89c4dbf28a6a12863064781b77dbd93c32163a8b8f6
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# Providers

在 TUI 中连接一个 provider，然后选择它的一个模型：

```text
/connect
/models
```

`/connect` 会列出当前服务器和项目可用的集成。选择一个 provider，当它提供多种认证方式时选择其中一种，然后按提示操作。

## TUI

TUI 支持 API key、OAuth 以及 provider 认证命令。OAuth 会打开一个授权 URL 或显示一个待输入的代码；按 `o` 打开 URL，按 `c` 复制授权信息。

```text
/connect
# Select OpenAI, then Codex device code (legacy).
```

再次运行 `/connect` 可以添加另一个账号。选择一个已连接的 provider 会打开它的账号列表，你可以在其中激活、重命名或删除已保存的账号。

## CLI

使用 `auth login` 可以在不打开 TUI 的情况下使用相同的 provider 认证方式。不带 provider 参数时，该命令会打开一个交互式 provider 选择器。

```bash
opencode auth login
```

传入集成 ID 或名称可以跳过第一个选择器。使用 `--method key` 可以显式选择 API key 输入方式。

```bash
opencode auth login anthropic --method key
```

方式 ID 因 provider 而异。当某个 provider 提供多种方式时，不带 `--method` 运行该命令即可查看可用方式。

```bash
opencode auth login openai
```

API key 输入和 provider 表单需要交互式终端。需要你粘贴授权码的 OAuth 方式同样需要交互式终端。

## 方式

OpenCode 通过四种集成方式接收 provider 凭据：

| 方式     | 行为                                                                                   |
| ---      | ---                                                                                    |
| API key  | 提示输入密钥并将其保存为 provider 账号。                                               |
| OAuth    | 提供浏览器 URL、设备码或授权码提示，然后保存 token，并在支持的情况下自动刷新。         |
| 命令     | 运行 provider 提供的认证命令，并将其标准输出保存为密钥。                               |
| 环境变量 | 从服务器进程读取受支持的变量，但不保存它。                                             |

provider 可以为 API key 和 OAuth 方式添加表单，用于收集 Azure 资源名或 GitHub Enterprise 域名等必填信息。CLI 和 TUI 会在开始认证前渲染这些表单。

## 环境变量

在处理模型请求的服务器进程上设置 provider 支持的环境变量。对于一次性的私有服务器，可以在启动独立模式时传入它。

```bash
ANTHROPIC_API_KEY=sk-ant-... opencode --standalone
```

对于共享的后台服务器，请将该变量加入其托管环境。此操作会停止正在运行的服务；下一个 OpenCode 命令会以新值重新启动它。

```bash
opencode service set env ANTHROPIC_API_KEY sk-ant-...
opencode auth list
```

环境变量连接会以 `environment` 类型出现在 `auth list` 中。它们不是账号：`auth logout` 无法移除它们，取消设置该变量即可断开连接。对于同一个集成，已保存的账号优先于环境变量连接。

```bash
opencode auth list
opencode service unset env ANTHROPIC_API_KEY
```

一些 provider 还会使用它们原生的环境凭据链而不是 API key 变量：

- Amazon Bedrock 支持 AWS 默认凭据链，包括 profile、访问密钥环境变量、web 身份以及容器凭据。它还支持 `AWS_BEARER_TOKEN_BEDROCK`。
- Google Vertex 使用 Application Default Credentials 和一个可解析的项目。例如，先用 `gcloud auth application-default login` 认证，再设置 `GOOGLE_CLOUD_PROJECT`。
- 当安装了 `az` 时，Azure 会将 **Microsoft Entra ID (Azure CLI)** 作为一种连接方式提供。先运行 `az login`，然后在 `/connect` 或 `auth login azure` 中选择该方式。

```bash
gcloud auth application-default login
GOOGLE_CLOUD_PROJECT=my-project opencode
```

provider 专属和服务器端的配置请参阅 [Providers](../../providers/index.md)。

## 账号

每次成功的 API key、OAuth 或命令登录都会创建一个已保存的账号。最新的账号会成为活跃账号；可以按标签或凭据 ID 切换活跃账号。

```bash
opencode auth list
opencode auth switch anthropic work
```

使用 `auth logout` 移除已保存的账号。这两个命令在省略参数时都会打开选择器。

```bash
opencode auth logout anthropic work
```

在 TUI 中，`/connect` 为已保存的账号提供同样的添加、激活、重命名和删除操作。

## 存储

已保存的 API key 和 OAuth token 存放在服务器的 SQLite 数据库中。对于本地服务器，用以下命令打印其数据库路径：

```bash
opencode debug paths db
```

常见的发布路径是 `~/.local/share/opencode/opencode.db`；`XDG_DATA_HOME`、发布渠道和 `OPENCODE_DB` 都可能改变它。不要通过编辑数据库来管理凭据；请使用 `/connect` 或 `auth` 命令。

V2 在数据库迁移期间会从 OpenCode 数据目录中旧版的 `auth.json` 导入受支持的凭据。新增和更新的凭据存放在 SQLite 中，而不会写回该文件。
