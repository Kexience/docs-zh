---
source_url: https://opencode.ai/docs/skills/
source_hash: sha256:6b9ac051468fe13624fc377b70e5f17bd959e957d82110fdcaeffc585e149439
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---
# 技能

创建一个技能，为 agent 提供针对某个特定任务的可复用指令。把一个 `SKILL.md` 文件放在 `.opencode/skills/<skill-id>` 中，并在 `description` 里描述何时使用它。

```markdown title=".opencode/skills/git-release/SKILL.md"
---
name: Git Release
description: Prepare release notes, version bumps, and GitHub releases
---

## Workflow

1. Read `references/release-policy.md`.
2. Summarize merged changes since the previous tag.
3. Propose the version bump before changing files.
4. Run `scripts/changelog.ts` only after the user approves the version.
```

OpenCode 会在该技能相关时对外声明它。此后 agent 可以用 `skill` 工具按需加载其指令，而不必把每个技能都塞进每次提示词中。

## 创建

把相关的脚本、参考资料和模板与 `SKILL.md` 放在一起：

```text
.opencode/skills/
└── git-release/
    ├── SKILL.md
    ├── scripts/
    │   └── changelog.ts
    └── references/
        └── release-policy.md
```

技能内部书写的路径相对于包含 `SKILL.md` 的目录。推荐使用目录形式，因为它为配套文件提供了一个私有的基础目录。

## 发现

OpenCode 会自动搜索以下位置：

| 范围 | 来源 |
| --------------------- | -------------------------------------- |
| 全局 | `~/.config/opencode/skills` |
| 全局兼容 | `~/.claude/skills`、`~/.agents/skills` |
| 项目 | `.opencode/skills` |
| 项目兼容 | `.claude/skills`、`.agents/skills` |

对于项目来源，OpenCode 会从当前目录向上搜索到项目根目录，并包含每一层中匹配的目录。

每个来源可以包含以下任一形式：

```text
skills/
├── review.md
└── git-release/
    └── SKILL.md
```

- Markdown 文件必须位于来源根目录，例如 `skills/review.md`。
- 文件名恰好为 `SKILL.md` 的文件可以嵌套在分组目录中，例如 `skills/git-release/SKILL.md` 或 `skills/teams/release/SKILL.md`。
- 包含 `SKILL.md` 的目录算作一个技能。OpenCode 不会在其中继续搜索更多技能。
- 隐藏文件、隐藏目录以及 `node_modules` 会被跳过。
- 搜索在来源根目录以下六层目录处停止。

## 来源

在任意 `opencode.json` 或 `opencode.jsonc` 中，用 `skills` 数组添加更多本地目录或 HTTP 目录（catalog）：

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "skills": [
    "./team-skills",
    "~/shared/opencode-skills",
    "/opt/company-skills",
    "https://example.com/opencode/skills/",
  ],
}
```

| 取值 | 解析方式 |
| ----- | ---------- |
| 相对路径 | 相对于当前 OpenCode 工作目录，而不是配置文件 |
| `~/` 路径 | 相对于当前用户的主目录 |
| 绝对路径 | 按原样使用 |
| `http://` 或 `https://` URL | 作为 HTTP 目录加载 |

每个被发现到的配置文件都会贡献自己的条目。`skills` 数组是合并而不是替换。

已连接的 [OpenCode Console](../console/index.md) 工作区也可以共享技能。

## 目录（Catalog）

HTTP 目录是一个带有 `index.json` 文件的 base URL：

```json title="index.json"
{
  "skills": [
    {
      "name": "git-release",
      "version": "3",
      "files": ["git-release.md", "references/release-policy.md"]
    }
  ]
}
```

对于该条目，OpenCode 会从 `<base-url>/git-release/<file>` 下载每个文件。

| 规则 | 要求 |
| ---- | ----------- |
| 路径 | 必须安全、相对且同源 |
| 条目文件 | 包含 `SKILL.md` 或 `<name>.md`，例如 `git-release.md` |
| 更新 | 文件变化时递增 `version`，以便 OpenCode 刷新缓存 |

每个下载下来的技能目录都会成为一个以条目名命名的来源根目录，因此 `git-release.md` 和 `SKILL.md` 的 ID 都是 `git-release`。

## Frontmatter

使用 frontmatter 来命名技能并控制它的出现方式：

```markdown title="SKILL.md"
---
name: Git Release
description: Prepare a repository release
metadata:
  opencode/autoinvoke: false
---

Prepare the changelog, version bump, tag, and release notes.
```

| 字段 | 行为 |
| ------------------------------ | ----------------------------------------------------------------- |
| `name` | 显示名称；默认为由路径推导出的 ID |
| `description` | 用于向模型展示该技能的摘要 |
| `metadata.opencode/autoinvoke` | 设为 `false` 可把该技能从模型的可用列表中隐藏 |
| `disable-model-invocation` | 设为 `true`，效果与 `opencode/autoinvoke: false` 相同 |

运行时所有 frontmatter 都是可选的。如果希望模型发现该技能，请写一个清晰的 `description`；没有 description 的技能不会被声明。

`opencode/autoinvoke: false` 只是把技能从模型的可用列表中隐藏。该技能仍然处于注册状态，并且仍可以通过 ID 显式加载。当 `disable-model-invocation` 和 `opencode/autoinvoke` 同时设置时，`opencode/autoinvoke` 优先。V2 接受 `license`、`compatibility` 等可移植性字段，但不会解释它们。

## ID

文件路径决定技能 ID。frontmatter 中的 `name` 只是一个显示标签。

| 文件 | ID |
| --------------------------------- | ------------- |
| `<source>/git-release.md` | `git-release` |
| `<source>/git-release/SKILL.md` | `git-release` |
| `<source>/teams/release/SKILL.md` | `release` |

ID 是精确且区分大小写的。对于需要跨环境移植的技能，请使用 1–64 个字符、唯一的小写 kebab-case ID，并与目录名保持一致：

```text
^[a-z0-9]+(-[a-z0-9]+)*$
```

V2 目前不强制执行该模式、1–64 字符的建议、`name` 与目录名的一致性，以及描述长度上限。

## 优先级

技能按 ID 选择。如果两个来源都定义了 `git-release`，则由后注册的来源提供 OpenCode 加载的技能：

```text
~/.config/opencode/skills/git-release/SKILL.md  ← 优先级较低
.opencode/skills/git-release/SKILL.md           ← 被加载
```

来源按从低到高的优先级注册：

1. 内置技能
2. `.claude/skills`，先全局，然后从最远的祖先目录向当前目录
3. `.agents/skills`，先全局，然后从最远的祖先目录向当前目录
4. `~/.config/opencode/skills`
5. 项目的 `.opencode/skills`，从项目根目录向当前目录
6. 显式的 `skills` 配置条目，按配置优先级和数组顺序

除非有意覆盖较早的技能，否则请避免使用重复的 ID。

## 加载

在每个模型步骤中，OpenCode 会列出已获允许、有 description 且未把 `opencode/autoinvoke` 设为 `false` 的技能。该列表只包含 ID、名称和 description，不包含完整的 Markdown 正文。

模型通过调用 `skill` 工具并传入精确的 ID 来加载技能：

```json title="skill tool input"
{
  "id": "git-release"
}
```

随后 OpenCode 会：

1. 选中该 ID 对应的当前定义。
2. 检查所选 agent 的 `skill` 权限。
3. 把 Markdown 正文（不含 frontmatter）加入对话。
4. 提供该技能的基础目录和最多十个配套文件路径的示例。

要自己加载一个技能，请在提示词中用 `@skill-id` 提及它。

配套文件的内容不会被自动加载。agent 会在技能指示它这样做时读取这些文件。文件示例只对基于目录的 `SKILL.md` 技能可用；扁平的 Markdown 技能不会获得邻近文件列表。

## 权限

使用 `skill` 动作，并以技能 ID 作为资源。规则按顺序执行，最后匹配的规则获胜：

```jsonc title="opencode.jsonc"
{
  "permissions": [
    { "action": "skill", "resource": "*", "effect": "allow" },
    { "action": "skill", "resource": "internal-*", "effect": "deny" },
    { "action": "skill", "resource": "experimental-*", "effect": "ask" },
  ],
}
```

| 效果 | 行为 |
| ------ | -------- |
| `allow` | 无需批准即可声明并加载匹配的技能 |
| `ask` | 声明匹配的技能，加载前询问 |
| `deny` | 对模型隐藏匹配的技能，并拒绝加载 |

把相同的规则放在 `agents.<id>.permissions` 下，可以只对某个 agent 生效。

## 故障排查

例如，下面这个技能的 ID 是 `release`，而不是其 frontmatter 中的名称 `Git Release`：

```text
.opencode/skills/release/SKILL.md
                      └─ ID: release
```

如果某个技能缺失或加载了错误的内容：

1. 确认该文件要么是根目录下的 `*.md`，要么是嵌套的且文件名恰好为 `SKILL.md` 的文件。
2. 检查由路径推导的、区分大小写的 ID，而不是 frontmatter 中的 `name`。
3. 如果希望模型发现该技能，请添加 `description`。
4. 检查 `opencode/autoinvoke` 以及所选 agent 的 `skill` 权限。
5. 查找是否有更靠后的来源定义了相同的 ID。
6. 对于 HTTP 目录，检查 `index.json`、同源的文件路径，以及是否更新了 `version`。
