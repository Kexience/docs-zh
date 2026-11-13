---
source_url: https://opencode.ai/docs/troubleshooting/
source_hash: sha256:754f9485e251b2ebb3b54e60c274a668dd9e03d53fc27dbab7ae13845586dd65
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# 故障排查

<Callout type="tip">
  你可以让 OpenCode 调试它自己。描述问题并让它使用这个故障排查页面；它可以阅读下面的步骤、检查其服务和日志，并帮助定位问题。
</Callout>

OpenCode 采用客户端-服务器架构。一个后台服务器拥有会话、插件、权限和其他应用状态。首先确定问题出在客户端、共享服务器还是某个特定项目。

## 检查后台服务

显示当前的服务器信息：

```bash
opencode service status
```

验证其 API 是否健康：

```bash
opencode api get /api/info
```

如果服务卡住或状态不健康，重启它：

```bash
opencode service restart
```

你也可以显式地停止和启动它：

```bash
opencode service stop
opencode service start
```

<Callout type="note">
  OpenCode 通常会自动发现或启动共享的后台服务。只有在诊断其生命周期时才需要这些服务命令。
</Callout>

## 允许浏览器来源

如果另一个来源的浏览器客户端因为 CORS 无法连接，请把该客户端的来源添加到服务配置中：

```bash
opencode service set cors http://192.168.1.10:3001
opencode service get cors
```

使用精确的 HTTP 或 HTTPS 来源，必要时包括端口，不要带路径或末尾斜杠。要允许多个来源，请以一个参数传入逗号分隔的列表；每个来源前后的空白会被去除：

```bash
opencode service set cors "http://192.168.1.10:3001, https://app.example.com"
```

`service get cors` 会打印一个 JSON 数组。使用以下命令移除已配置的列表：

```bash
opencode service unset cors
```

设置或取消服务配置会停止后台服务。它下次启动时会加载新配置；使用 `opencode service start` 可以显式启动它。

对于前台服务器，为每个额外允许的来源重复 `--cors`：

```bash
opencode serve --cors http://192.168.1.10:3001 --cors https://app.example.com
```

使用 `serve --service` 时，提供的 `--cors` 标志会为该进程覆盖持久化的列表。没有这些标志时，服务模式使用持久化的列表。CORS 不会更改监听地址，也不会绕过服务器认证。

## 检查 API

`api` 命令使用本地服务发现和认证流程。它接受 HTTP 方法和路径，或 OpenAPI 操作 ID。

所有端点和操作 ID 参见 [API 参考](../api/index.md)。

使用 `--data` 或 `-d` 传入 JSON 请求体，使用 `--header` 或 `-H` 添加请求头。

<Callout type="warning">
  当没有可用的健康兼容服务时，运行 `opencode api` 可能会启动后台服务。
</Callout>

## 读取日志

已安装的构建把日志写入：

```text
~/.local/share/opencode/log/opencode.log
```

在重现问题的同时跟踪日志：

```bash
tail -f ~/.local/share/opencode/log/opencode.log
```

每一行都包含一个进程 `run` ID 和一个 `role` 字段。使用 `role=server` 查看会话、provider、插件、权限和工具活动。

```bash
grep 'role=server' ~/.local/share/opencode/log/opencode.log
grep 'run=8fc3b1d5' ~/.local/share/opencode/log/opencode.log
```

## 捕获堆快照

在任何平台上为正在运行的后台服务器写入内存（堆）快照：

```bash
opencode debug heap-dump
```

该命令会等待快照完成后打印其路径：

```text
/home/me/.local/share/opencode/log/heap-48213-2026-10-23T013012345Z.heapsnapshot
```

使用 `--directory` 可以把它写到别处。目录缺失时服务器会创建它：

```bash
opencode debug heap-dump --directory ./snapshots
```

- 它只使用已经在运行的服务器，从不启动、替换或重启服务器。
- 使用 `--server <url>` 可以捕获你用 `opencode serve` 启动的服务器。如果它设置了密码，请设置 `OPENCODE_PASSWORD`。此时 `--directory` 是服务器所在机器上的路径。
- 在 Chrome DevTools 的 Memory 面板中打开该文件。

<Callout type="warning">
  服务器在写入快照期间会暂停，其内存占用可能会在短时间内升高。快照可能包含提示词、文件内容和凭据。请不要公开分享它。
</Callout>

### 在桌面应用中

从命令面板运行 **Capture heap snapshots**。它会在你的 Downloads 文件夹中写入一个文件夹，包含应用每个部分的快照，以及一份快照无法显示的内存的细分：

```text
opencode-heap-2026-10-23T013012345Z/
  memory.json                  where the memory is, per process, in MiB: start here
  memory-infra.json            Chromium's memory dump trace; open it in https://ui.perfetto.dev
  heap-48213-….heapsnapshot    the desktop's own server
  window-1-48390.heapsnapshot  one per app window
  main-48102.heapsnapshot      the desktop main process
  gpu.json                     the GPU and driver
  manifest.json                processes, PIDs, and memory before and after; written last
```

- 堆快照只包含 JavaScript 对象和页面。图片、布局、合成器层和 GPU 内存在 `memory.json` 和 `memory-infra.json` 中。
- 不会被捕获。请改在那台机器上使用 `opencode debug heap-dump`。
- 服务器把快照直接写入该文件夹，因此不会有大量数据被移动或复制。
- 不包括浏览器标签页，因为它们的快照包含你访问过的页面的内容。

## 捕获 CPU 和内存分析

在 macOS 和 Linux 上，你可以向正在运行的 OpenCode 进程发送信号来捕获诊断数据。从健康端点获取后台服务器的 PID：

```bash
opencode api get /api/info
```

使用响应中的 `pid` 配合以下信号之一：

- `SIGPROF` 捕获一个十秒的 CPU 分析：

  ```bash
  kill -SIGPROF <pid>
  ```

  结果以 `cpu-<pid>-<timestamp>.cpuprofile` 写入日志目录。

- `SIGUSR1` 捕获一个内存（堆）快照：

  ```bash
  kill -SIGUSR1 <pid>
  ```

  结果以 `heap-<pid>-<timestamp>.heapsnapshot` 写入日志目录。

在打开文件之前，请等待 `opencode.log` 中出现 `CPU profile written` 或 `heap snapshot written`。相应的日志条目包含其完整路径。你可以在 Chrome DevTools 中查看这两种文件类型。

<Callout type="note">
  信号触发的分析在 Windows 上不可用。请改用 `opencode debug heap-dump` 获取堆快照。写入堆快照可能会暂停进程并暂时增加其内存占用。
</Callout>

## 服务文件

共享服务器把自己注册在：

```text
~/.local/state/opencode/service.json
```

它的私有服务配置单独存储在：

```text
~/.config/opencode/service.json
```

数据库通常位于：

```text
~/.local/share/opencode/opencode.db
```

`OPENCODE_DB` 可以覆盖数据库位置。

<Callout type="warning">
  故障排查时不要删除或编辑服务文件或数据库。使用服务命令来管理守护进程，并在使用外部工具检查持久化数据之前先做好备份。
</Callout>

## 报告问题

报告一个可重现的问题时，请包含以下内容：

- `opencode --version` 的输出
- `opencode service status` 的输出
- 重现该问题的最短步骤序列
- 该问题影响的是共享服务、某个特定客户端还是某个项目
- 相关的日志行，包括它们的 `run` 和 `role` 字段

在分享日志之前，请移除 API key、授权请求头、提示词、文件内容和其他敏感数据。

可重现的问题请提交到 [GitHub Issues](https://github.com/anomalyco/opencode/issues)。
