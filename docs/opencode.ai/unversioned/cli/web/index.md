---
source_url: https://opencode.ai/docs/cli/web/
source_hash: sha256:1a9489fc02d9c4df30dfabfa6e4c652917422d7db916b407aeb33de2a5b124e5
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# Web

OpenCode 自带一个 Web UI，由驱动 TUI 的同一台服务器提供服务。它默认可用，并受密码保护。

## 访问

```bash
$ opencode pair

  Open a link to connect. Links work once and expire in 5 minutes.

  http://127.0.0.1:49374/auth/connect/...

  █▀▀▀▀▀█ ...
```

在浏览器中打开链接即会以会话 cookie 登录并加载 Web UI。用 OpenCode 应用扫描二维码，或把链接粘贴到应用的服务器地址输入框，都会以同样的方式连接应用。会话有效期为 30 天；修改服务器密码会让所有会话登出。

### 通过 SSH

当服务器只监听 localhost 时，可以在本机转发它的端口，然后在本地打开打印出的链接：

```bash
$ ssh -L 49374:127.0.0.1:49374 my-server
```

默认情况下服务器只监听 localhost。它的端口取决于平台：

| 平台                  | 默认端口 |
| --------------------- | ------------ |
| macOS、Linux 和 WSL   | 49374        |
| Windows               | 28894        |

Windows 保留 49152 及以上的端口，WSL 镜像网络还会保留其下方的另一段端口。用 `opencode service status` 打印当前地址：

```bash
$ opencode service status
http://127.0.0.1:49374
```

你可以用 `opencode service` 命令修改这项配置。

### 远程访问

要从任意位置连接，可通过 [OpenTunnel](https://github.com/anomalyco/opentunnel)远程地址进行配对：

```bash
$ opencode pair --remote
```

第一次开启远程访问时，它会先征求确认：

```text
▲  This will expose your OpenCode server to the internet.
│  Traffic is end-to-end encrypted, and access requires your server password.
│  To pair locally instead, run `opencode pair` without the --remote flag.
│
◆  Expose your server to the internet?
│  ● Yes / ○ No
```

在没有交互式终端的情况下，除非传入 `--yes` 表示接受，否则命令会失败。接受之后，后续运行会跳过该提示，即使已经用 `opencode service set remote false` 关闭了远程访问也是如此。

## 配置

用 `opencode service set` 设置任意选项：

```bash
# Listen on every network interface
$ opencode service set hostname 0.0.0.0

# Use a fixed port instead of the channel default
$ opencode service set port 49374

# Replace the generated password
$ opencode service set password "a-long-secret"

# Allow a web client served from another origin
$ opencode service set cors https://app.example.com,https://other.example.com

# Pass an environment variable to the server process
$ opencode service set env OPENCODE_LOG_LEVEL DEBUG
```

修改设置会停止后台服务器。重新启动它以应用新配置：

```bash
$ opencode service start
```

## 独立运行

`opencode serve` 以前台方式运行同一台服务器，而不是通过共享的后台服务。

```bash
$ opencode serve --hostname 0.0.0.0 --port 4096
server listening on http://0.0.0.0:4096
server password <password>
```

在以下情况下可以使用它：

- 在共享的、常驻的或远程主机上运行 OpenCode，然后用 `opencode --server <url>` 连接客户端。
- 为单个进程控制主机名、端口和 CORS 来源。
- 在 systemd、Docker 等要求前台进程的监管器或其他环境下运行。
- 使用专用服务器，而不是共享的后台服务。

用 `--server` 将客户端连接到它：

```bash
$ opencode --server http://127.0.0.1:4096
```

### 身份验证

设置 `OPENCODE_PASSWORD` 可以使用固定密码而不是自动生成的密码。`opencode --server` 也使用同一变量获取密码。

```bash
$ OPENCODE_PASSWORD="a-long-secret" opencode serve --port 4096
$ OPENCODE_PASSWORD="a-long-secret" opencode --server http://127.0.0.1:4096
```

其他 HTTP 客户端使用 Basic 认证。用户名始终是 `opencode`，只有密码可以更改。

```bash
$ curl -u opencode:a-long-secret http://127.0.0.1:4096/api/info
```
