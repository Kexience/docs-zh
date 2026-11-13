---
source_url: https://opencode.ai/docs/formatters/
source_hash: sha256:8082294d239a399e55616951a0518d349a714ba34041c47eb3aa13eb42c1fc25
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# 格式化工具

OpenCode 可以在 `write`、`edit` 或 `patch` 工具修改文件之后对其进行格式化。格式化工具默认关闭，因此需要在配置中启用它们：

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "formatter": true,
}
```

## 启用

把 `formatter` 设为 `true` 可启用所有内置格式化工具。OpenCode 只在某个内置工具的可执行文件及其项目专属要求都可用时才运行它。

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "formatter": true,
}
```

对象形式同样会启用内置工具，并允许你覆盖它们或添加自定义格式化工具。空对象会保留继承来的格式化工具设置，而 `true` 会把它们重置为内置工具。

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "formatter": {},
}
```

## 内置工具

OpenCode 内置了以下格式化工具定义。大多数要求对应的命令可用；带额外检测规则的定义在下方列出。

| 格式化工具 | 扩展名 | 要求 |
| --- | --- | --- |
| `gofmt` | `.go` | `gofmt` 命令 |
| `mix` | `.ex`, `.exs`, `.eex`, `.heex`, `.leex`, `.neex`, `.sface` | `mix` 命令 |
| `oxfmt` | `.js`, `.jsx`, `.mjs`, `.cjs`, `.ts`, `.tsx`, `.mts`, `.cts` | `package.json` 中的 `oxfmt` 依赖 |
| `prettier` | `.js`, `.jsx`, `.mjs`, `.cjs`, `.ts`, `.tsx`, `.mts`, `.cts`, `.html`, `.htm`, `.css`, `.scss`, `.sass`, `.less`, `.vue`, `.svelte`, `.json`, `.jsonc`, `.yaml`, `.yml`, `.toml`, `.xml`, `.md`, `.mdx`, `.graphql`, `.gql` | `package.json` 中的 `prettier` 依赖 |
| `biome` | 与上方 `prettier` 相同的扩展名 | `biome.json` 或 `biome.jsonc`，以及已安装的 `@biomejs/biome` 二进制 |
| `zig` | `.zig`, `.zon` | `zig` 命令 |
| `clang-format` | `.c`, `.cc`, `.cpp`, `.cxx`, `.c++`, `.h`, `.hh`, `.hpp`, `.hxx`, `.h++`, `.ino`, `.C`, `.H` | `clang-format` 命令和 `.clang-format` |
| `ktlint` | `.kt`, `.kts` | `ktlint` 命令 |
| `ruff` | `.py`, `.pyi` | `ruff` 命令以及 Ruff 配置或依赖声明 |
| `air` | `.R` | 自我标识为 R 格式化工具的 `air` 命令 |
| `uv` | `.py`, `.pyi` | 支持 `uv format` 的 `uv` 命令 |
| `rubocop` | `.rb`, `.rake`, `.gemspec`, `.ru` | `rubocop` 命令 |
| `standardrb` | `.rb`, `.rake`, `.gemspec`, `.ru` | `standardrb` 命令 |
| `htmlbeautifier` | `.erb` | `htmlbeautifier` 命令 |
| `dart` | `.dart` | `dart` 命令 |
| `ocamlformat` | `.ml`, `.mli` | `ocamlformat` 命令和 `.ocamlformat` |
| `terraform` | `.tf`, `.tfvars` | `terraform` 命令 |
| `latexindent` | `.tex` | `latexindent` 命令 |
| `gleam` | `.gleam` | `gleam` 命令 |
| `shfmt` | `.sh`, `.bash` | `shfmt` 命令 |
| `nixfmt` | `.nix` | `nixfmt` 命令 |
| `rustfmt` | `.rs` | `rustfmt` 命令 |
| `pint` | `.php` | `composer.json` 中的 `laravel/pint` |
| `ormolu` | `.hs` | `ormolu` 命令 |
| `cljfmt` | `.clj`, `.cljs`, `.cljc`, `.edn` | `cljfmt` 命令 |
| `dfmt` | `.d` | `dfmt` 命令 |

例如，启用内置工具后，OpenCode 会发现并为匹配的文件运行项目本地的 Prettier 依赖：

```jsonc title="opencode.jsonc"
{
  "formatter": true,
}
```

## 自定义

添加一个具名条目可以修改内置工具或定义自定义格式化工具。自定义格式化工具需要同时具备 `command` 和 `extensions` 才能运行。

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "formatter": {
    "prettier": {
      "environment": {
        "NODE_ENV": "development",
      },
      "extensions": [".js", ".ts"],
    },
    "deno-markdown": {
      "command": ["deno", "fmt", "$FILE"],
      "extensions": [".md"],
    },
  },
}
```

| 字段 | 类型 | 行为 |
| --- | --- | --- |
| `disabled` | `boolean` | 为 `true` 时移除该具名格式化工具。 |
| `command` | `string[]` | 替换内置命令，或定义自定义命令。 |
| `environment` | `Record<string, string>` | 在保留父环境的同时添加环境变量。 |
| `extensions` | `string[]` | 替换内置扩展名列表，或定义自定义列表。需包含开头的点号。 |

所有字段都是可选的。内置条目会继承省略的值，而缺少 command 或 extensions 的新条目无法运行。

```jsonc title="opencode.jsonc"
{
  "formatter": {
    "prettier": {
      "extensions": [".md", ".mdx"],
    },
  },
}
```

## 命令

`command` 是参数数组，而不是 shell 命令字符串。OpenCode 会把 `$FILE` 替换为文件的绝对路径，并在当前项目目录下运行该命令。

```jsonc title="opencode.jsonc"
{
  "formatter": {
    "custom": {
      "command": ["custom-fmt", "--write", "$FILE"],
      "extensions": [".custom"],
    },
  },
}
```

## 匹配

OpenCode 将文件的最终扩展名与 `extensions` 进行比较。匹配区分大小写，并且像 `.part.md` 这样的复合条目不会匹配 `notes.part.md`，因为它的最终扩展名是 `.md`。

```jsonc title="opencode.jsonc"
{
  "formatter": {
    "markdown": {
      "command": ["deno", "fmt", "$FILE"],
      "extensions": [".md"],
    },
  },
}
```

当多个格式化工具匹配时，OpenCode 按注册顺序逐一尝试，并在第一个成功的命令后停止。内置工具保持其内置顺序；自定义条目按对象顺序排列在其后。如果某个命令退出失败，OpenCode 会记录该失败并尝试下一个匹配项。

```jsonc title="opencode.jsonc"
{
  "formatter": {
    "preferred": {
      "command": ["preferred-fmt", "$FILE"],
      "extensions": [".foo"],
    },
    "fallback": {
      "command": ["fallback-fmt", "$FILE"],
      "extensions": [".foo"],
    },
  },
}
```

## 禁用

当没有任何配置文件设置 `formatter` 时，格式化处于关闭状态。要禁用某个较低优先级文件启用的格式化，可将其设为 `false`。

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "formatter": false,
}
```

要在保留其他内置工具的同时禁用某一个，可将它的具名条目标记为 disabled。

```jsonc title="opencode.jsonc"
{
  "formatter": {
    "prettier": {
      "disabled": true,
    },
  },
}
```
