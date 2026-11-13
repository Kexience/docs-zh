---
source_url: https://openspec.dev/docs/configuration/config-json
source_hash: sha256:8ac3f6a76640019e10263ebb63d2feba045fb5157f9994ea45eb8406cd739695
translated_at: 2026-11-13T09:48:42+08:00
translation_version: 1
---

# CLI 设置（config.json）

## 位置 [#location]

CLI 在 macOS 和 Linux 上把机器级设置保存在 `~/.config/openspec/config.json`，在 Windows 上保存在 `%APPDATA%\openspec\config.json`。只要设置了 `$XDG_CONFIG_HOME`，它在所有平台上都优先。`openspec config` 命令负责读取和编辑这个文件。

## 字段 [#fields]

| 键 | 类型 | 必填 | 作用 |
| --- | --- | --- | --- |
| `profile` | 字符串：`core` 或 `custom` | 否 | 决定 `openspec init` 安装哪套工作流 |
| `delivery` | 字符串：`both`、`skills` 或 `commands` | 否 | 2.0 中已废弃：仍会被读取，但不再改变任何行为 |
| `workflows` | 字符串列表 | 否 | `custom` 配置档安装的工作流列表 |
| `featureFlags` | 映射：标志 → 布尔值 | 否 | 布尔型功能开关 |
| `defaultStore` | 字符串 | 否 | 根目录解析时使用的机器级兜底存储库 |
| `openers` | 映射：工具 id → 设置 | 否 | 工作集可在其中打开的工具，以及各工具的启动方式 |
| `telemetry` | 映射 | 否 | 遥测退出状态、匿名 id，以及首次提示是否已显示 |

### profile [#profile]

决定 `openspec init` 安装哪套工作流。默认为 `core`：propose、explore、apply、update、sync 和 archive。设为 `custom` 时，改为严格按 `workflows` 列表安装。

### delivery [#delivery]

在 OpenSpec 2.0 中已废弃，2.0 只安装技能。该值仍会被接受和读取，因此旧配置依然有效，但它不再影响 `init` 和 `update` 安装什么。默认值为 `skills`。在 1.x 中，它用于选择安装技能、斜杠命令，还是两者都装（[升级到 2.0](../upgrade-to-2.md)）。

### workflows [#workflows]

`custom` 配置档安装的工作流；配置档为 `core` 时忽略。有效 id：`propose`、`explore`、`new`、`continue`、`apply`、`update`、`ff`、`sync`、`archive`、`bulk-archive`、`verify`、`onboard`。

### featureFlags [#featureflags]

以标志名为键的布尔开关，用 `openspec config set featureFlags.<flag> true` 设置。目前 CLI 尚未读取任何标志。

### defaultStore [#defaultstore]

根目录解析时使用的机器级兜底存储库 id，只有当 `--store` 参数、本地 `openspec/` 目录和项目的 `store:` 指针都无法确定时才会用到。完整的解析顺序见[根目录解析](../stores.md#where-artifacts-get-created-when-using-stores)。

### openers [#openers]

工作集可以在其中打开的工具，以工具 id 为键。在终端里用 `openspec config edit` 编辑全局 `config.json` 中的 `openers`。

| 字段 | 约定 |
| --- | --- |
| `style` | `workspace-file` 或 `attach-dirs`。新工具必填；内置工具可省略。 |
| `label` | 显示在工具选择器中的非空字符串。新工具默认为其 id。 |
| `command` | 非空的可执行文件名或路径。新工具默认为其 id。参数要放进 `args`，不要写在这个字符串里。 |
| `args` | 字符串数组，在 workspace 文件或 attach 标志之前传入。新工具默认为 `[]`。 |
| `attach_flag` | 非空字符串，`attach-dirs` 时与每个成员路径配对。新工具默认为 `--add-dir`。`workspace-file` 时忽略。 |

**内置工具覆盖：** `code`、`cursor`、`claude` 和 `codex` 会保留你省略的任何字段。设置 `args` 会替换整个参数列表；设为 `[]` 会清空它。

**启动方式：** `workspace-file` 把生成的 `.code-workspace` 路径传给可执行文件。`attach-dirs` 为每个成员（包括主成员）传入一对"标志/路径"。

**可用性：** `attach-dirs` 类型的 opener（包括 Claude Code 和 Codex）默认禁用。你无法用 `--tool` 选择或保存它们，OpenSpec 也会拒绝打开已经指定了这类 opener 的工作集。配置覆盖不会启用 `attach-dirs` 启动方式。

**校验：** 未知字段、类型无效，以及新工具缺少 `style`，都会在工作集命令读取 opener 表时报错。

下面这个例子添加 VS Code Insiders，并在内置 VS Code opener 每次启动时传入 `--new-window`：

```json
{
  "openers": {
    "code-insiders": {
      "style": "workspace-file",
      "label": "VS Code Insiders"
    },
    "code": {
      "args": ["--new-window"]
    }
  }
}
```

对应的 `code-insiders` 或 `code` 可执行文件必须已安装，并且在 `PATH` 中可用。

### telemetry [#telemetry]

CLI 会保存你的匿名 id，以及首次运行提示是否已显示。把 `telemetry.enabled` 设为 `false` 即可关闭遥测。你也可以在环境中设置 `OPENSPEC_TELEMETRY=0` 或 `DO_NOT_TRACK=1` 来退出。

## 示例 [#example]

一份填写完整的 config.json：

```json
{
  "profile": "core",
  "featureFlags": {},
  "telemetry": {
    "anonymousId": "5f8a2c1e-4b6d-4f9a-9c3d-7e1b2a8d4c6f",
    "noticeSeen": true
  }
}
```
