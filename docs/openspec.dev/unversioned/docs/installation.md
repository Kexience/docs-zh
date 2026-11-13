---
source_url: https://openspec.dev/docs/installation
source_hash: sha256:f792fd750d39ee14054ffa045f1b847da81f4abed9f72a989e94a9c4a4eabe46
translated_at: 2026-11-13T09:48:42+08:00
translation_version: 1
---

# 安装

## 安装 [#install]

在 macOS 或 Linux 上，于终端中：

```bash
curl -fsSL https://openspec.dev/cli/install.sh | sh
```

在 Windows 上，于 PowerShell 中：

```powershell
irm https://openspec.dev/cli/install.ps1 | iex
```

如果安装程序打印出 `export PATH=...` 一行，请运行它。然后[检查是否成功](#check-it-worked)。

## 用 AI 助手安装 [#install-with-your-ai-assistant]

把以下内容粘贴到你的 AI 对话中：

```text
Fetch https://raw.githubusercontent.com/Fission-AI/OpenSpec/main/install.md and follow it.
```

或者，在终端中把它管道传给一个 CLI 智能体（以 Claude Code 为例）：

```bash
curl -fsSL https://raw.githubusercontent.com/Fission-AI/OpenSpec/main/install.md | claude
```

这会获取[仓库根目录的 install.md](https://github.com/Fission-AI/OpenSpec/blob/main/install.md)，它是一份为任何能运行 shell 命令的智能体编写的提示词（少数 IDE 集成不行）。你的助手应当：

1. 如果机器上已有该 CLI，就跳过安装，并按它原先安装的方式提议更新。如果原先是 npm 或 Homebrew，只提一次 `openspec install` 会切换到独立安装，但不催促你。否则，向你展示上面的安装命令，并在运行前等待你确认。
2. 仅在你要求或安装程序失败时才改用 npm；如果你的 Node 低于 22.12.0，则停止。
3. 确认 `openspec` 在你的 PATH 上。
4. 说出它认为你要用的文件夹，建议使用你当前正在对话的 AI 工具，并询问你还用哪些工具，然后在那里运行 `openspec init`（[项目设置](./setup.md)步骤）。
5. 报告 init 创建了什么，以及在你的工具中调用 OpenSpec 的确切拼写。

它在任何需要特权的操作之前停下，且从不编辑你的 shell 启动文件。上面的[安装命令](#install)和下面的[包管理器](#package-managers)才是权威依据，提示词只是替你执行它们。

这种安装方式是新的，结果会因所用模型而异。只有在你能够接受纠正 AI 的错误时才使用。否则建议按下面的标准方法操作。

## 包管理器 [#package-managers]

这些方式把 OpenSpec 作为 Node.js 包安装，因此需要 Node.js 22.12.0 或更新版本（Homebrew 和 Nix 自带）。在终端中：

```bash
node --version
```

如果输出 `v22.12.0` 或更高版本，用 npm 安装：

```npm
npm install -g @fission-ai/openspec@latest
```

否则，从 [nodejs.org](https://nodejs.org) 安装更新的 Node，或通过你的版本管理器（nvm、fnm、asdf、volta）安装，或改用[独立安装](#install)。

### Homebrew [#homebrew]

Homebrew 在 macOS 或 Linux 上安装 OpenSpec 及其 Node.js 依赖。在终端中：

```bash
brew install openspec
```

该 formula 已发布在 [homebrew-core](https://formulae.brew.sh/formula/openspec)，因此无需添加 tap。

### Yarn [#yarn]

`yarn global add` 仅适用于 Yarn Classic（1.x）。新版 Yarn 移除了全局安装，因此请改用 npm、pnpm 或 bun。全局 CLI 不必与你的项目使用同一个包管理器。

### Bun [#bun]

Bun 只安装 OpenSpec，不负责运行它，因此机器上仍需要 Node（见[包管理器](#package-managers)）。没有 Node 时，每个命令都会以 `env: node: No such file or directory` 失败。Bun 对待[所有 Node CLI](https://bun.com/docs/pm/bunx#shebangs)都是如此。

### Deno [#deno]

Deno 从 npm 安装该 CLI，并且需要显式的权限标志。在终端中：

```bash
deno install --global \
  --allow-read --allow-write --allow-env --allow-sys=cpus,homedir --allow-net=edge.openspec.dev \
  npm:@fission-ai/openspec@latest
```

有些命令会启动其他程序：[`openspec config edit`](./cli.md) 会打开你的编辑器。Deno 每次运行都会用权限提示打断这类命令。要让它不再询问，在安装命令中加入带作用域的 `--allow-run=<program>`。

> [!NOTE]
> 如果 Deno 无法解析 `@latest`，改为固定一个版本范围：`npm:@fission-ai/openspec@^1.7.0`。

### Nix [#nix]

OpenSpec 仓库附带一个 Nix flake。把它安装到你的配置档中。在终端中：

```bash
nix profile install github:Fission-AI/OpenSpec
```

或者先运行一次性命令，不进行安装：

```bash
nix run github:Fission-AI/OpenSpec -- --version
```

这样不会在你的 PATH 上留下任何东西，因此事后无需检查安装。

改为把 OpenSpec 放进项目开发 shell 的话，把该 flake 作为输入加入，并使用它的默认包；[flake.nix](https://github.com/Fission-AI/OpenSpec/blob/main/flake.nix) 列出了各项输出。

Nix 包在标准位置（`share/bash-completion/completions`、`share/fish/vendor_completions.d`、`share/zsh/site-functions`）附带 Bash、Fish 和 Zsh 补全脚本，因此会随包加载，无需运行 `openspec completion install`。

## 检查是否成功 [#check-it-worked]

无论使用哪种方法，在终端中：

```bash
openspec --version
```

如果输出版本号，说明该 CLI 在你的 PATH 上。它每台机器只需安装一次。

接下来，[设置你的项目](./setup.md)。如果你的助手已经运行过 init，该页会说明它写入了什么以及如何调整。

## 安装选项 [#install-options]

要指定版本或文件夹，在 `sh` 之前设置变量：

```bash
curl -fsSL https://openspec.dev/cli/install.sh | OPENSPEC_VERSION=v1.15.0 sh
```

- **`OPENSPEC_VERSION`**：要安装的版本，例如 `v1.15.0`。默认为最新版本。
- **`OPENSPEC_INSTALL_DIR`**：安装到的文件夹。默认为 `~/.local/bin`（Windows：`%LOCALAPPDATA%\Programs\openspec`）。

在 Windows 上，先设置变量：

```powershell
$env:OPENSPEC_VERSION = 'v1.15.0'
irm https://openspec.dev/cli/install.ps1 | iex
```

在 Alpine Linux 上，安装前运行 `apk add libstdc++ libgcc`。

### 手动下载 [#download-by-hand]

每个版本为每种计算机提供一个文件：

| 计算机 | 文件 |
|---|---|
| Mac，Apple 芯片 | `openspec-darwin-arm64.tar.gz` |
| Mac，Intel | `openspec-darwin-x64.tar.gz` |
| Linux，arm64 | `openspec-linux-arm64.tar.gz` |
| Linux，x64 | `openspec-linux-x64.tar.gz` |
| Alpine，arm64 | `openspec-linux-arm64-musl.tar.gz` |
| Alpine，x64 | `openspec-linux-x64-musl.tar.gz` |
| Windows，arm64 | `openspec-windows-arm64.zip` |
| Windows，x64 | `openspec-windows-x64.zip` |

1. **下载**你的文件，来自[最新版本](https://github.com/Fission-AI/OpenSpec/releases/latest)。文件会在版本发布几分钟后上传到该发布页。如果你的文件还没有列出，稍等并重新加载，或取上一个版本的文件。
2. **解包**它。在终端中：`tar -xzf openspec-darwin-arm64.tar.gz`。在 Windows 上，右键点击 `.zip` 并选择“全部解压缩”。
3. **在 macOS 上**，在你解包到的文件夹中运行 `xattr -d com.apple.quarantine openspec`。在此之前，macOS 会阻止在浏览器中下载的文件。
4. **移动** `openspec` 到 PATH 上的某个文件夹，例如 `~/.local/bin`。在 Windows 上，把 `openspec.exe` 移到用户 PATH 上的某个文件夹，例如 `%LOCALAPPDATA%\Programs\openspec`。

### 校验下载 [#verify-a-download]

要确认文件是由 OpenSpec 发布工作流构建的，用 [GitHub CLI](https://cli.github.com) 运行：

```bash
gh attestation verify openspec-darwin-arm64.tar.gz --repo Fission-AI/OpenSpec
```

如果该文件并非由该工作流构建，它就会失败。安装命令已用该版本的 `SHA256SUMS` 校验每次下载，因此这一步是可选的。

## 从 npm 切换到独立安装 [#switch-from-npm-to-the-standalone-install]

切换是可选的；npm 方式仍然可用。你的设置和项目会沿用，只有程序本身改变。

**1. 安装独立副本。** 在终端中：

```bash
openspec install
```

它会安装独立的 `openspec`，并打印移除你的 npm 或 Homebrew 副本的命令。

**2. 移除旧副本。** 它通常在你的 PATH 中排在最前，因此在它消失之前会继续被运行。运行第 1 步打印的命令，例如：

```npm
npm uninstall -g @fission-ai/openspec
```

**3. 检查运行的是哪个副本。** 打开一个新终端：

```bash
openspec version
```

它应当打印 `OpenSpec <version> (standalone)`。如果它显示的是某个包管理器，说明 PATH 上还有另一个副本：`which -a openspec`（Windows：`where.exe openspec`）会列出所有副本，请移除其他副本。

任何项目都不需要重新初始化。要切回去，删除该文件并再次运行 npm 安装。

## 更新 [#updating]

在终端中，在你运行过 init 的每个项目里：

```bash
openspec update
```

当有更新的 CLI 时，[`openspec update`](./cli.md#openspec-update) 会提示，并可以为你安装；该升级每台机器一次。每次运行都会刷新项目生成的技能，这些技能从不自行更新。已是最新的项目会打印 `✓ All 2 tool(s) up to date (v1.7.0)`。

> [!WARNING]
> 使用独立安装时，运行 `openspec install` 就地替换你的副本；`openspec update` 会在有更新版本时告诉你。使用 Homebrew 时，运行 `brew upgrade openspec`。使用 Deno 时，带 `-f` 重新运行 [Deno 安装](#deno)；不带它则不会覆盖已安装的命令。使用 Nix 时，用 `nix profile upgrade openspec`。

> [!NOTE]
> 全局 npm 安装属于某一个 Node 安装。用 nvm 切换 Node 版本后，`openspec` 命令不会跟着过去，因此需要在新版本下重新安装。

## 卸载 [#uninstalling]

要卸载 OpenSpec，请按下面的步骤执行；这些步骤都不会触碰你的源代码。你也可以让智能体看这一节，由它处理卸载。

**1. 移除 [shell 补全](./cli.md#openspec-completion)**（如果你设置过），趁该 CLI 仍能执行此操作时。在终端中：

```bash
openspec completion uninstall
```

**2. 移除 CLI。** 对于独立安装，删除 `~/.local/bin/openspec`（Windows：`%LOCALAPPDATA%\Programs\openspec`，并从用户 PATH 中移除该文件夹）。对于 npm，在终端中：

```npm
npm uninstall -g @fission-ai/openspec
```

使用 Homebrew：`brew uninstall openspec`。使用 Deno：`deno uninstall --global openspec`。使用 Nix：`nix profile remove openspec`。你的 shell 应该再也找不到 `openspec`。

**3. 删除剩余内容，或保留它们。**

- 每个项目生成的智能体文件：`.agents/skills/` 中的 `openspec-*` 技能和 `.openspec-target`，以及 `.claude/skills/` 这类工具文件夹中的 `openspec-*` 链接。[支持的工具](./supported-tools.md)列出了哪些工具会获得链接；MiniMax Code 把技能放在 `~/.minimax/skills`。
- 更早版本的残留：`CLAUDE.md` 或 `AGENTS.md` 中的标记块（删除该块，保留文件），以及 `~/.codex/prompts` 中的 `opsx-*.md` 提示词。
- `openspec/` 文件夹：先停一下。`specs/` 和 `changes/archive/` 是你对系统的记录，是纯 Markdown，没有 OpenSpec 也能正常阅读。
- 每台机器的状态：`~/.config/openspec/` 中的设置和遥测 id；`~/.local/share/openspec/` 中的模式覆盖、存储库注册，以及独立安装的内置模式（`binary-schemas/`）（Windows：`%APPDATA%\openspec`、`%LOCALAPPDATA%\openspec`）。注册项只是指针；它们所指向的存储库仓库不受影响。
