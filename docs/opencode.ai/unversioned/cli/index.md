---
source_url: https://opencode.ai/docs/cli/
source_hash: sha256:21eb6f9805f5f3c4e9f6b1a21e848c6dc134cc1de1b5826275a11248903aa58b
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# 简介

在项目中运行 CLI 即可打开全屏终端界面：

```bash
opencode
```

传入一个目录即可在另一个项目中工作：

```bash
opencode ~/code/my-project
```

推荐的终端：

- [Ghostty](https://ghostty.org)
- [WezTerm](https://wezterm.org)
- [Alacritty](https://alacritty.org)
- [Kitty](https://sw.kovidgoyal.net/kitty/)

支持真彩色（truecolor）的终端能让主题呈现最准确的颜色；不支持的终端会使用现有色板的近似配色。

## 自动化

使用 `opencode run` 可以在不打开交互界面的情况下提交提示。它面向脚本、CI 任务以及其他需要在终端直接获得模型输出的工作流。

```bash
opencode run "Explain this repository"
```

## Mini

使用 `opencode mini` 可以启动 OpenCode 的精简交互界面，而不是全屏 TUI。

```bash
opencode mini
```

运行 `opencode mini --help` 可查看它的会话、模型、agent、提示和回放选项。

## 后台服务

默认情况下，OpenCode 会为你的用户账户发现或启动一个共享的后台服务器。每个本地 OpenCode 客户端都连接到该服务器，它负责会话、配置、集成、权限和工具执行。

使用 `--standalone` 以私有服务器运行，或使用 `--server` 连接到指定的服务器 URL：

```bash
opencode --standalone
opencode --server http://localhost:4096
```

要让私有服务器成为 CLI 命令的默认选择而不是启动共享服务，可以禁用它：

```bash
opencode service set disabled true
opencode
```

这会停止正在运行的后台服务。`--server` 仍然可以连接到显式选择的服务器；`opencode service start` 仍然可以显式启动共享服务。要恢复自动使用服务，运行 `opencode service unset disabled`。配对功能依赖共享服务，禁用期间不可用。

共享服务的诊断见[故障排查](../troubleshooting/index.md)，服务器端点见 [API 参考](../api/index.md)。

## 路径

打印某个特定的本地路径，供其他工具使用：

```bash
opencode debug paths db
sqlite3 "$(opencode debug paths db)"
```

可选的选择器接受 `db`、`home`、`data`、`config`、`cache`、`state`、`tmp`、`bin`、`log` 或 `repos`，并且只输出路径和一个换行符。数据库路径遵循发布渠道和 `OPENCODE_DB`；相对的数据库覆盖值会相对于数据目录解析，`:memory:` 则原样输出。该命令不会启动服务器，也不会打开数据库。

省略选择器则显示所有路径及其标签：

```bash
opencode debug paths
```

## 卸载

先预览将被移除的文件和安装内容：

```bash
opencode uninstall --dry-run
```

运行 `opencode uninstall` 确认移除。OpenCode 会在移除全局缓存目录之前停止已注册的后台服务和持久终端；该目录由多个 OpenCode 版本和渠道共享。会话数据、配置和状态永远不会被移除。

- `--force`（`-f`）跳过确认，用于非交互式移除。
- 包管理器安装会使用检测到的包管理器。Curl 安装会打印最终需要手动删除可执行文件的命令。
