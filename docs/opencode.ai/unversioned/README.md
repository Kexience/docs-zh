---
source_url: https://opencode.ai/docs/
source_hash: sha256:6cdeb5ff3b59930bf426f4c563e8e5bcb4135c56b8a63ce47b787c533f3c7606
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---
# 简介

OpenCode 是一个开源 coding agent，提供终端界面、桌面应用和网页应用三种形态。

## CLI

<CodeTabs
  id="install"
  label="Install method"
  tabs={[
    { label: "curl", code: "curl -fsSL https://opencode.ai/v2/install | bash" },
    { label: "homebrew", code: "brew install anomalyco/tap/opencode-v2" },
    { label: "npm", code: "npm install -g @opencode/cli" },
    { label: "bun", code: "bun install -g --trust @opencode/cli" },
    { label: "pnpm", code: "pnpm add -g --allow-build=@opencode/cli @opencode/cli" },
    { label: "yarn", code: "yarn global add @opencode/cli" },
    { label: "vite+", code: "vp install -g @opencode/cli" },
    { label: "aur", code: "paru -S opencode-beta" },
    { label: "mise", code: "mise use -g opencode" },
  ]}
/>

npm 包会通过 postinstall 脚本为你的平台选择原生 `opencode` 二进制文件。Bun 和 pnpm 命令显式允许了这个必需的脚本；Vite+ 无需额外参数。mise 命令需要 mise 2026.10.9 或更高版本；更旧的版本会安装 OpenCode 1。

不支持 Windows 上的包管理器。

下载适用于你平台的独立 CLI 二进制文件。

- **macOS：** [Apple silicon](https://opencode.ai/update/api/latest/cli/opencode/opencode-darwin-arm64.zip) · [Intel](https://opencode.ai/update/api/latest/cli/opencode/opencode-darwin-x64.zip) · [Intel（基线版）](https://opencode.ai/update/api/latest/cli/opencode/opencode-darwin-x64-baseline.zip)
- **Windows：** [ARM64](https://opencode.ai/update/api/latest/cli/opencode/opencode-windows-arm64.zip) · [x64](https://opencode.ai/update/api/latest/cli/opencode/opencode-windows-x64.zip) · [x64（基线版）](https://opencode.ai/update/api/latest/cli/opencode/opencode-windows-x64-baseline.zip)
- **Linux（glibc）：** [ARM64](https://opencode.ai/update/api/latest/cli/opencode/opencode-linux-arm64.tar.gz) · [x64](https://opencode.ai/update/api/latest/cli/opencode/opencode-linux-x64.tar.gz) · [x64（基线版）](https://opencode.ai/update/api/latest/cli/opencode/opencode-linux-x64-baseline.tar.gz)
- **Linux（musl）：** [ARM64](https://opencode.ai/update/api/latest/cli/opencode/opencode-linux-arm64-musl.tar.gz) · [x64](https://opencode.ai/update/api/latest/cli/opencode/opencode-linux-x64-musl.tar.gz) · [x64（基线版）](https://opencode.ai/update/api/latest/cli/opencode/opencode-linux-x64-baseline-musl.tar.gz)

## 桌面应用

下载适用于你平台的最新 OpenCode Desktop 构建版本。

- **macOS：** [Apple silicon](https://opencode.ai/update/api/latest/desktop/opencode/opencode-desktop-mac-arm64.dmg) · [Intel](https://opencode.ai/update/api/latest/desktop/opencode/opencode-desktop-mac-x64.dmg)
- **Windows：** [x64](https://opencode.ai/update/api/latest/desktop/opencode/opencode-desktop-win-x64.exe) · [ARM64](https://opencode.ai/update/api/latest/desktop/opencode/opencode-desktop-win-arm64.exe)
- **Linux（.deb）：** [x64](https://opencode.ai/update/api/latest/desktop/opencode/opencode-desktop-linux-amd64.deb) · [ARM64](https://opencode.ai/update/api/latest/desktop/opencode/opencode-desktop-linux-arm64.deb)
- **Linux（.rpm）：** [x64](https://opencode.ai/update/api/latest/desktop/opencode/opencode-desktop-linux-x86_64.rpm) · [ARM64](https://opencode.ai/update/api/latest/desktop/opencode/opencode-desktop-linux-aarch64.rpm)
- **Linux（AppImage）：** [x64](https://opencode.ai/update/api/latest/desktop/opencode/opencode-desktop-linux-x86_64.AppImage) · [ARM64](https://opencode.ai/update/api/latest/desktop/opencode/opencode-desktop-linux-arm64.AppImage)

## Web

使用 `opencode pair` 命令访问 OpenCode 网页界面。

```bash
$ opencode pair

  Open a link to connect. Links work once and expire in 5 minutes.

  http://127.0.0.1:49374/auth/connect/...
```

## Docker

Docker 镜像使用带版本号的标签，例如 `ghcr.io/anomalyco/opencode:2.0.0`。

---

## 连接

OpenCode 内置了对众多 LLM provider 的支持。你可以在 [TUI 中](cli/providers/index.md)用 `/connect` 直接连接它们。

要配置自定义 provider，请参阅 [Providers](providers/index.md)。

如果你想方便地使用最好的 coding 模型，可以试试 [OpenCode Console](console/index.md)。

你也可以尝试 [OpenCode Go](console/go/index.md)，这是一个每月 10 美元的订阅计划，让你可以使用最好的 coding 模型。

---

## 自定义

通过编辑 [OpenCode 配置](config/index.md)、[加载插件](plugins/index.md)、[连接 MCP 服务器](mcp-servers/index.md)或[创建命令](commands/index.md)，把 OpenCode 变成你自己的工具。终端界面的主题和按键绑定请参阅 [CLI 设置](cli/config/index.md)。

---

## 学习

如果你有兴趣深入学习 OpenCode，Boot.dev 在我们团队的参与下打造了一门出色的 [AI Coding with OpenCode](https://www.boot.dev/courses/learn-ai-coding) 课程。课程中的所有内容都可以免费阅读和观看，不过部分交互功能可能需要付费。

---

## 全站目录

以下目录按官方站点的导航分组编排，共 68 页；未收录的页面已注明。

## 文档
- [简介](README.md)
- [配置](./config/index.md)
- [从 V1 迁移](./migrate-v1/index.md)
- [故障排查](./troubleshooting/index.md)
### 配置
- [Agent](./agents/index.md)
- [模型](./models/index.md)
- [技能](./skills/index.md)
- [主题](./themes/index.md)
- [命令](./commands/index.md)
- [插件](./plugins/index.md)
- [Provider](./providers/index.md)
- [网页搜索](./websearch/index.md)
- [网络](./network/index.md)
- [快照（Snapshots）](./snapshots/index.md)
- [压缩（Compaction）](./compaction/index.md)
- [格式化工具](./formatters/index.md)
- [引用（References）](./references/index.md)
- [附件](./attachments/index.md)
- [工具](./tools/index.md)
- [MCP 服务器](./mcp-servers/index.md)
- [权限](./permissions/index.md)
- [策略](./policies/index.md)
- [指令（Instructions）](./instructions/index.md)
- [预热](./warming/index.md)
## CLI
- [简介](./cli/index.md)
- [TUI](./cli/tui/index.md)
- [设置](./cli/config/index.md)
- [Web](./cli/web/index.md)
- [Providers](./cli/providers/index.md)
- [命令](./cli/commands/index.md)
- [ACP](./cli/acp/index.md)
- [主题](./cli/theme/index.md)
- [插件](./cli/plugins/index.md)
- [按键绑定](./cli/keybinds/index.md)
## 构建
- [简介](./build/index.md)
### 插件
- [概览](./build/plugins/index.md)
- [服务器端](./build/plugins/server/index.md)
- [TUI](./build/plugins/cli/index.md)
- [GUI](./build/plugins/gui/index.md)
- [RPC](./build/plugins/rpc/index.md)
- [从 V1 迁移插件](./build/plugins/migrate-v1/index.md)
### 客户端
- [JavaScript](./build/client/index.md)
### SDK
- [概览](./build/sdk/index.md)
- [Cloudflare](./build/sdk/cloudflare/index.md)
### Effect
- [Effect](./build/plugins/effect/index.md)
- [RPC](./build/plugins/effect/rpc/index.md)
- [Effect](./build/client/effect/index.md)
- [Effect](./build/sdk/effect/index.md)
## API
- [Overview](https://opencode.ai/docs/api)（线上为自动生成的 OpenAPI 参考，未收录）
## 控制台
- [简介](./console/index.md)
- [模型](./console/models/index.md)
- [Providers](./console/providers/index.md)
- [网页搜索](./console/websearch/index.md)
- [Go](./console/go/index.md)
### 工作区
- [基础](./console/workspaces/index.md)
- [成员](./console/members/index.md)
- [SSO](./console/sso/index.md)
- [目录同步](./console/scim/index.md)
- [预算](./console/budgets/index.md)
- [计费](./console/billing/index.md)
### API
- [API 概览](./console/api/index.md)
- [推理 API](./console/api/inference/index.md)
- [Providers API](./console/api/providers/index.md)
### Harnesses
- [Harnesses](./console/harnesses/index.md)
- [Claude Code](./console/harnesses/claude-code/index.md)
- [Codex](./console/harnesses/codex/index.md)
- [Hermes](./console/harnesses/hermes/index.md)
- [Pi](./console/harnesses/pi/index.md)
- [Raycast](./console/harnesses/raycast/index.md)
