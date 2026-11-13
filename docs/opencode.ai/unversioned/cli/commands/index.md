---
source_url: https://opencode.ai/docs/cli/commands/
source_hash: sha256:cdc54954aa6cd48a86fabce48209c6836dbf8f242111bd012348df26a236a6c8
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# 命令

每个命令都支持 `--help` 查看完整的标志列表，例如 `opencode run --help`。一些依赖服务器的命令支持 `--standalone` 来运行私有服务器，或 `--server <url>` 来指定目标服务器；具体支持的标志请查看命令的帮助。

## run

发送一条消息并打印回复，不打开交互界面。

```bash
$ opencode run "Explain this repository"
```

### CI

在 CI 中，把 provider 的 API key 作为 secret 传入，并使用 standalone 模式，让私有服务器收到它。例如，下面这个 GitHub Actions job 会审查检出的仓库：

```yaml
name: OpenCode review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm install --global @opencode/cli
      - run: opencode run --standalone --model anthropic/claude-sonnet-5-5 "Review this repository for correctness and summarize any issues."
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

选择一个模型。

```bash
$ opencode run --model anthropic/claude-sonnet-5-5 "Refactor parseToken"
```

继续上一次会话。

```bash
$ opencode run --continue "Now handle the expired case"
```

为脚本输出以换行分隔的 JSON。

```bash
$ opencode run --format json "List the TODO comments"
```

把文件附加到消息上。

```bash
$ opencode run --file src/server.ts --file src/client.ts "Review these for bugs"
```

用指定的 agent 运行。

```bash
$ opencode run --agent build "Fix the failing test"
```

继续指定的会话。

```bash
$ opencode run --session ses_4f2a1c "Check edge cases"
```

自动批准未被显式拒绝的权限。

```bash
$ opencode run --auto "Fix the failing test"
```

创建会话时直接设为归档，让脚本或 CI 运行不出现在会话列表和收件箱中。会话仍然存在：`opencode session list` 会包含它，你也可以按 ID 打开。

```bash
$ opencode run --archived "Review this diff"
```

查看所有子命令和标志。

```bash
$ opencode run --help
```

## mini

启动精简的交互界面，而不是全屏 TUI。

```bash
$ opencode mini
```

继续上一次会话。

```bash
$ opencode mini --continue
```

以指定的模型和初始提示启动。

```bash
$ opencode mini --model anthropic/claude-sonnet-5-5 --prompt "Summarize this repository"
```

继续指定的会话。

```bash
$ opencode mini --session ses_4f2a1c
```

查看所有子命令和标志。

```bash
$ opencode mini --help
```

## session

管理会话。

```bash
$ opencode session list
```

限制列表条数并以 JSON 输出。

```bash
$ opencode session list --max-count 20 --format json
```

删除一个会话及其子会话。

```bash
$ opencode session delete ses_9c1b08
```

将会话数据导出为 JSON。

```bash
$ opencode session export ses_4f2a1c
```

导出时对敏感的对话记录和文件数据做脱敏。

```bash
$ opencode session export ses_4f2a1c --sanitize
```

从 JSON 文件或 URL 导入会话数据。

```bash
$ opencode session import session.json
```

导入到指定目录。

```bash
$ opencode session import session.json --directory ~/code/project
```

查看所有子命令和标志。

```bash
$ opencode session --help
```

## auth

管理 AI provider 和凭证。

```bash
$ opencode auth list
```

以 JSON 形式列出。

```bash
$ opencode auth list --format json
```

登录一个 provider。

```bash
$ opencode auth login anthropic
```

用指定的认证方式登录。

```bash
$ opencode auth login anthropic --method key
```

登出一个已保存的账号。

```bash
$ opencode auth logout anthropic work
```

切换某个集成的活动账号。

```bash
$ opencode auth switch anthropic work
```

导出已保存的凭证，并在另一台机器上导入。该文件包含密钥。

```bash
$ opencode auth export anthropic > credentials.json
$ opencode auth import credentials.json
```

查看所有子命令和标志。

```bash
$ opencode auth --help
```

## models

列出所有可用模型。

```bash
$ opencode models
```

查看所有子命令和标志。

```bash
$ opencode models --help
```

## mcp

管理 MCP（Model Context Protocol）服务器。

```bash
$ opencode mcp list
```

添加一个远程服务器。

```bash
$ opencode mcp add context7 --url https://mcp.context7.com/mcp
```

向全局配置添加一个本地服务器。

```bash
$ opencode mcp add everything --global -- npx -y @modelcontextprotocol/server-everything
```

添加一个带环境变量的本地服务器。

```bash
$ opencode mcp add everything --env LOG_LEVEL=debug -- npx -y @modelcontextprotocol/server-everything
```

添加一个带请求头的远程服务器。

```bash
$ opencode mcp add context7 --url https://mcp.context7.com/mcp --header CONTEXT7_API_KEY=secret
```

对支持 OAuth 的远程服务器进行认证。

```bash
$ opencode mcp auth sentry
```

移除某个服务器已存储的 OAuth 凭证。

```bash
$ opencode mcp logout sentry
```

查看所有子命令和标志。

```bash
$ opencode mcp --help
```

## plugin

管理插件。

```bash
$ opencode plugin list
```

包含内置的服务器插件。

```bash
$ opencode plugin list --builtin
```

安装一个插件并添加到全局配置。

```bash
$ opencode plugin add @example/opencode-tui
```

检查包插件的更新。

```bash
$ opencode plugin check
```

更新包插件。

```bash
$ opencode plugin update
```

从全局配置移除一个插件。

```bash
$ opencode plugin remove @example/opencode-tui
```

查看所有子命令和标志。

```bash
$ opencode plugin --help
```

## stats

显示可分享的使用统计。

```bash
$ opencode stats
```

显示最近 7 天。

```bash
$ opencode stats --days 7
```

显示模型使用情况。

```bash
$ opencode stats --models
```

显示费用和 token 明细。

```bash
$ opencode stats --cost
```

输出 JSON 而不是报告。

```bash
$ opencode stats --json
```

只显示当前项目。

```bash
$ opencode stats --project .
```

查看所有子命令和标志。

```bash
$ opencode stats --help
```

## serve

启动 API 和 web 服务器。参见 [Web](../web/index.md)。

```bash
$ opencode serve
```

绑定到所有网络接口上的固定端口。

```bash
$ opencode serve --hostname 0.0.0.0 --port 4096
```

允许来自其他源（origin）的浏览器客户端。

```bash
$ opencode serve --cors https://app.example.com
```

查看所有子命令和标志。

```bash
$ opencode serve --help
```

## pair

输出一次性链接（以及第一个链接的二维码），用于把浏览器或应用登录到服务器。链接 5 分钟后过期，且只能使用一次。

```bash
$ opencode pair
```

在链接中使用外部 URL。

```bash
$ opencode pair --url https://dev.example.com
```

通过 OpenTunnel 远程地址从任何地方配对。这会把服务器暴露到互联网上，因此第一次启用远程访问时它会说明这一点并请你确认。参见[远程访问](../web/index.md#remote-access)。

```bash
$ opencode pair --remote
```

不经提示直接接受，例如在没有终端的脚本中。

```bash
$ opencode pair --remote --yes
```

查看所有子命令和标志。

```bash
$ opencode pair --help
```

## service

管理后台服务器。参见 [Web](../web/index.md)。

```bash
$ opencode service start
```

重启它。

```bash
$ opencode service restart
```

查看它的状态。

```bash
$ opencode service status
```

停止它。

```bash
$ opencode service stop
```

读取一个设置。

```bash
$ opencode service get hostname
```

设置一个设置项。

```bash
$ opencode service set hostname 0.0.0.0
```

允许额外的 CORS 源。

```bash
$ opencode service set cors https://app.example.com
```

给服务器进程传入一个环境变量。

```bash
$ opencode service set env OPENCODE_LOG_LEVEL DEBUG
```

把设置重置为默认值。

```bash
$ opencode service unset hostname
```

查看所有子命令和标志。

```bash
$ opencode service --help
```

## reload

在不重启服务器的情况下重新加载配置。正在运行的会话会在下一个步骤边界用新的服务继续。

```bash
$ opencode reload
```

## api

向运行中的服务器发起请求。

```bash
$ opencode api GET /api/session
```

用查询参数调用一个操作 ID。

```bash
$ opencode api session.list --param limit=10
```

发送 JSON 请求体。

```bash
$ opencode api session.create --data '{"title": "New session"}'
```

添加一个请求头。

```bash
$ opencode api GET /api/session -H "accept: application/json"
```

查看所有子命令和标志。

```bash
$ opencode api --help
```

## acp

通过 stdin 和 stdout 启动一个 Agent Client Protocol 服务器，供编辑器集成使用。它会一直运行，直到客户端关闭连接。

```bash
$ opencode acp
```

查看所有子命令和标志。

```bash
$ opencode acp --help
```

## debug

提供调试和排障工具。

```bash
$ opencode debug agents
```

列出配置来源。

```bash
$ opencode debug config
```

为运行中的后台服务器写一份堆快照并打印其路径。

```bash
$ opencode debug heap-dump
```

把快照写入你指定的目录。

```bash
$ opencode debug heap-dump --directory ./snapshots
```

显示全局路径。

```bash
$ opencode debug paths
```

打印单个路径。

```bash
$ opencode debug paths db
```

查看所有子命令和标志。

```bash
$ opencode debug --help
```

## upgrade

把 OpenCode 升级到最新版本或指定版本。别名：`update`。

```bash
$ opencode upgrade
```

用指定的包管理器升级到指定版本。

```bash
$ opencode upgrade 2.0.21 --method bun
```

查看所有子命令和标志。

```bash
$ opencode upgrade --help
```

## uninstall

停止后台服务、移除全局缓存并卸载 OpenCode。会话数据、配置和状态不会被移除。

```bash
$ opencode uninstall
```

预览将被移除的内容。

```bash
$ opencode uninstall --dry-run
```

查看所有子命令和标志。

```bash
$ opencode uninstall --help
```
