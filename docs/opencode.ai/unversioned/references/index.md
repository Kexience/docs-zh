---
source_url: https://opencode.ai/docs/references/
source_hash: sha256:a62fa3f4495bc9fad58cb5a92a09adeac8de67bbb1e7a83dba522b3569b0c501
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# 引用（References）

引用（References）让 OpenCode 能够以命名方式访问当前项目之外的目录。在 `opencode.json` 或 `opencode.jsonc` 中添加一个引用，然后在需要时在客户端中附加它的别名。

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "references": {
    "docs": {
      "path": "../product-docs",
      "description": "Use for product behavior and terminology",
    },
  },
}
```

附加 `docs` 之后，让 agent 检查相关路径：

```text
Read the attached docs reference and summarize api/authentication.md.
```

引用适合用于文档、共享库、示例，或来自其他仓库的源代码。

## 本地

使用 `path` 指向一个本地目录：

```jsonc
{
  "references": {
    "design-system": {
      "path": "../design-system",
      "description": "Use when working with components or design tokens",
    },
  },
}
```

路径的行为如下：

- 相对路径从包含配置文件的目录开始解析。
- 支持绝对路径。
- 支持相对于家目录的路径，例如 `~/docs`。

当不需要其他字段时，可以使用字符串简写形式：

```jsonc
{
  "references": {
    "docs": "../docs",
    "shared": "~/work/shared",
  },
}
```

<Callout type="note">
  简写字符串只有在以 `.`、`/` 或 `~` 开头时才被视为本地路径。请使用 `./docs` 而不是 `docs`；裸的 `docs` 值会被解释为一个 Git 仓库。
</Callout>

## Git

使用 `repository` 指向一个远程 Git 仓库：

```jsonc
{
  "references": {
    "effect": {
      "repository": "Effect-TS/effect",
      "branch": "main",
    },
    "internal-sdk": {
      "repository": "git@gitlab.example.com:platform/sdk.git",
      "branch": "release/v2",
    },
  },
}
```

支持的远程形式包括：

- GitHub 的 `owner/repo` 简写
- Git URL
- host/path 形式
- SCP 风格的远程地址

不支持本地的 `file:` 仓库。

使用字符串简写可以跟随远程的默认分支：

```jsonc
{
  "references": {
    "effect": "Effect-TS/effect",
    "sdk": "gitlab.com/platform/sdk",
  },
}
```

未指定 `branch` 时，OpenCode 会检出并刷新远程的默认分支。分支名可以包含字母、数字、`/`、`_`、`.` 和 `-`，但不能以 `-` 开头，也不能包含 `..`。

```jsonc
{
  "references": {
    "sdk": {
      "repository": "example/sdk",
      "branch": "release/v2.1",
    },
  },
}
```

## 存储

OpenCode 会规范化每个远程地址，并在其全局数据目录下为每个远程和分支保存一份检出。未显式指定分支时，路径采用如下形式：

```text
opencode/repos/<host>/<repository-path>
```

在典型的 Linux 安装中，`Effect-TS/effect` 存储在：

```text
~/.local/share/opencode/repos/github.com/Effect-TS/effect
```

显式指定分支时，会追加一个编码后的 `@<branch>` 后缀：

```text
~/.local/share/opencode/repos/github.com/Effect-TS/effect@main
```

## 刷新

缺失的仓库会被异步克隆。当引用加载或重新加载时，以及当该 Location 中有新的用户提示词被受理之后，已有的检出会在后台进行检查。

```text
Prompt admitted → refresh check starts in background → agent continues
```

如果某个检出的上次刷新尝试距今至少 24 小时，或者从未记录过尝试，则它符合刷新条件。刷新会拉取并重置到配置的分支或远程的默认分支。

```text
Last attempt: 25 hours ago → eligible
Last attempt: 2 hours ago  → skipped
```

刷新行为遵循以下规则：

- 时间戳在服务重启后仍然保留。
- 使用同一检出的 Location 共享其时间戳。
- 失败的尝试会被记录，并同样受 24 小时限制约束。
- Location 未被使用时，不会有周期性轮询。
- 克隆或刷新失败不会阻止其他引用加载。

提示词不会等待克隆或刷新完成。附件中可能包含较旧的内容，即使之后一次工具读取已经看到更新后的检出；一个新引用也可能在其检出尚未就绪时就出现。

```text
Attachment created → cached content
Background refresh completes → later tool read sees newer content
```

<Callout type="warning">
  缓存的检出是共享的，并且可能在 agent 使用期间被更新。请避免编辑缓存的检出，因为刷新会将其重置。
</Callout>

## 引导说明

`description` 用于告诉 agent 何时引用是相关的。带描述的引用会连同其别名和解析后的路径一起出现在 agent 指令中。

```jsonc
{
  "references": {
    "docs": {
      "path": "../docs",
      "description": "Use for product behavior and terminology",
    },
  },
}
```

没有描述的引用仍然对客户端可用，但不会被自动推荐。

```jsonc
{
  "references": {
    "archive": {
      "path": "../archive",
    },
  },
}
```

## 可见性

将 `hidden` 设为 `true` 可以把引用从交互式客户端的选择器中移除：

```jsonc
{
  "references": {
    "internal": {
      "path": "../internal",
      "description": "Use for internal service behavior",
      "hidden": true,
    },
  },
}
```

`hidden` 只影响交互式可见性。该引用仍然存在于引用 API 中，并且如果它带有描述，也会出现在 agent 指令中。

## 用法

客户端通过引用的根别名来附加它。附件包含根目录下直接文件和目录的非递归列表。

```text
Attached alias: docs
Ask: Inspect docs/guides/deployment.md and explain the deployment steps.
```

需要根目录以下的内容时，可以让 agent 检查具体路径。

## 权限

引用不会授予额外的工具权限。活动 Location 之外的访问仍遵循常规的工具规则和 `external_directory` 权限；编辑还需要相应的编辑权限。

```text
Read ../product-docs/api.md
```

只有当当前的权限允许该外部读取时，这个请求才会成功。

## 字段

| 字段          | 本地     | Git      | 说明                                          |
| ------------- | -------- | -------- | --------------------------------------------- |
| `path`        | 必填     | 否       | 本地目录路径                                  |
| `repository`  | 否       | 必填     | 远程 Git 仓库                                 |
| `branch`      | 否       | 可选     | 要拉取并检出的分支                            |
| `description` | 可选     | 可选     | 说明 agent 应在何时使用它的引导文字           |
| `hidden`      | 可选     | 可选     | 从交互式客户端选择器中隐藏                    |

一个完整的 Git 条目可以使用所有与 Git 兼容的字段：

```jsonc
{
  "references": {
    "sdk": {
      "repository": "example/sdk",
      "branch": "main",
      "description": "Use for SDK implementation details",
      "hidden": false,
    },
  },
}
```

## 别名

别名不能为空，也不能包含 `/`、`\`、空白字符、反引号或逗号。

```text
Valid:   docs
Invalid: product docs
Invalid: docs/api
```
