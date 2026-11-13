---
source_url: https://opencode.ai/docs/plugins/
source_hash: sha256:7083383f1a149f4887a8cbaa806ae849910391f634368822344315279cd557af
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# 插件

在 `opencode.json(c)` 中添加已发布的包、带版本号的包、带作用域的包或本地插件目录。

## 配置

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": [
    "opencode-acme-plugin",
    "opencode-acme-plugin@1.2.0",
    "@acme/opencode-plugin",
    "./plugins/local",
    "../shared/plugin",
    "/absolute/path/plugin",
    "file:///home/me/plugins/local",
    {
      "package": "@acme/opencode-plugin",
      "options": {
        "agent": "reviewer",
        "strict": true,
      },
    },
  ],
}
```

相对路径会相对于包含该条目的配置文件进行解析。

配置的本地路径必须是目录。指向单个文件的路径会被跳过。关于 OpenCode 如何在目录中定位各个部分，参见[加载](../build/plugins/index.md#load)。

来自各个适用配置文件的插件数组会按优先级从低到高依次合并生效，而不是互相替换。

```text
~/.config/opencode/opencode.jsonc
./opencode.jsonc
./.opencode/opencode.jsonc
```

## 发现

OpenCode 还会从每一个已发现的 `.opencode/plugins/` 目录中加载直接的 `.ts` 和 `.js` 文件，以及紧邻的插件包目录。

```text
.opencode/
└── plugins/
    ├── concise.ts
    ├── reviewer.js
    └── acme-package/
```

全局插件在 OpenCode 配置目录下使用相同的发现布局。

```text
~/.config/opencode/plugins/
```

位于项目根目录 `opencode.json(c)` 旁边的 `plugins/` 目录不会被自动发现；需要显式配置其插件目录，或将其移动到 `.opencode/` 之下。

```jsonc title="opencode.jsonc"
{
  "plugins": ["./plugins/local"]
}
```

## 控制

插件条目按顺序处理。在 ID 或通配符前加 `-` 前缀可将其禁用，使用 `*` 表示所有插件，使用 `.*` 匹配 ID 前缀。后面的 ID 可以重新启用某个插件。

```jsonc title="opencode.jsonc"
{
  "plugins": ["*", "-opencode.provider.*", "opencode.provider.openai", "-acme.reviewer"]
}
```

要禁用添加到新 fork 的提示，请在 `plugins` 中添加 `"-opencode.fork-notice"`。

有两个内置插件会忽略移除操作，以防止仓库关闭[策略](../policies/index.md)的强制执行：`opencode.config.policy` 和 `opencode.provider.opencode`，后者是用于下发组织策略的 Console 连接。

## 管理

使用 CLI 安装、列出、检查、更新或移除全局包插件。

```sh
opencode plugin add opencode-acme-plugin@1.2.0
opencode plugin list
opencode plugin list --builtin
opencode plugin check
opencode plugin update
opencode plugin update opencode-acme-plugin
opencode plugin remove opencode-acme-plugin@1.2.0
```

`plugin check` 会检查服务器端、仅 GUI 和仅 TUI 的包插件是否有更新。`plugin update` 会更新所有过期的包；传入一个已配置的包目标则只检查或更新该包。本地插件和锁定到精确版本的包会被跳过。

包安装接受带版本、标签或范围的 npm 名称，以及兼容 npm 的 Git 包规范。Git 仓库可以使用托管快捷方式、HTTPS 或 SSH，包括通过你现有的 Git 凭据可访问的私有仓库。

```sh
opencode plugin add @acme/opencode-plugin@latest
opencode plugin add github:acme/opencode-plugin
opencode plugin add git+ssh://git@github.com/acme/opencode-plugin.git#main
opencode plugin add 'github:acme/plugins#main::path:packages/opencode-plugin'
```

支持分支、标签、完整的提交哈希以及 npm 的 `::path:` 仓库子目录选择器。本地路径可以直接配置；`plugin add` 不接受 tarball 和 npm 别名目标。

## 重载

被监视的配置目录下的更改会自动重载。服务器启动时会立即加载已缓存的包插件，在后台安装缺失的包，并检查未锁定版本的 npm 和 Git 插件是否有更新，且不改动已安装的包。精确的 npm 版本和完整的 Git 提交哈希会保持锁定。对未受监视的本地依赖所做的更改可能仍需要重启 OpenCode。

```sh
touch .opencode/plugins/concise/index.ts
opencode service restart
```

## 桌面端

导出 `./gui-experimental` 的插件还会为 OpenCode Desktop 添加面板、命令或设置。应用从它运行的服务器加载插件，因此要在每个窗口中使用该插件，请在你的全局 `opencode.json(c)` 中进行配置。

```jsonc title="~/.config/opencode/opencode.jsonc"
{
  "plugins": ["opencode-acme-plugin"],
}
```

当选择应用自身的服务器时，它们会显示在**设置 > 扩展 > 插件**中。插件的开关只关闭其桌面 UI，**重新加载**会在失败后重新加载它。要关闭整个插件，请在 `plugins` 中添加 `-` 及其 ID，例如 `"-acme"`。

## 终端

仅 TUI 的插件需要单独配置，并且在连接到远程服务器时保持启用。

```json title="cli.json"
{
  "plugins": ["opencode-acme-cli"]
}
```

<Card title="构建插件" href="/build/plugins">
  创建插件来添加工具、钩子、集成、命令、agent 以及其他行为。
</Card>
