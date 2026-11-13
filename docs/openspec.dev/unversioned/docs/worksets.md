---
source_url: https://openspec.dev/docs/worksets
source_hash: sha256:12a13d53479153ce89e204f1b5cd7848ac1c9ec3f0319e8f68c29087c85facca
translated_at: 2026-11-13T09:48:42+08:00
translation_version: 1
---

# 工作集（beta）

用了存储库之后，智能体所需的上下文被拆散在多个文件夹里。规格和变更住在存储库里，代码住在各个仓库里。在一个仓库里启动的智能体只能读取和检索那个仓库，别的都碰不到，所以它只掌握了半幅图景。

工作集就是 OpenSpec 为此提供的工具。工作集是一份保存下来的、有名字的文件夹列表，你把它们一起打开。本页假定存储库已经建好并注册到你的机器上。[存储库（beta）](./stores.md) 讲了这部分。

## 工作方式 [#how-it-works]

- **它是什么**：一份有名字的文件夹列表，只保存在你的机器上。不会往成员文件夹里写任何东西，也不会提交任何内容。
- **打开时做什么**：OpenSpec 按列表生成一个 `.code-workspace` 文件，并在它上面启动你的编辑器。所有成员文件夹都在同一个窗口里。
- **你会得到什么**：编辑器的搜索，以及你在该窗口里运行的任何智能体，都能读取每个成员文件夹。智能体可以在一个会话里检索存储库的规格和仓库的代码。
- **它不改变什么**：命令使用哪个 `openspec/` 文件夹。这一点仍然遵循[产物在哪里创建](./stores.md#where-artifacts-get-created-when-using-stores)。

## 设置 [#set-it-up]

1. **保存工作集**（每台机器一次）。把仓库和存储库列为成员，并指定用来打开它们的工具：

   ```bash
   # save a named list of folders you open together
   openspec workset create platform \
     --member ~/src/web-app \
     --member ~/openspec/team-plans \
     --tool code
   ```

   ```yaml
   Saved workset 'platform' (2 members) to your machine.
   Open it any time with: openspec workset open platform
   ```

2. 每次开始工作时**打开它**：

   ```bash
   # open every member in one VS Code window
   openspec workset open platform
   ```

`openspec workset list` 显示你保存了什么，`openspec workset remove <name>` 删除工作集而不碰成员文件夹：

```yaml
platform  (opens in VS Code)
  web-app     /Users/you/src/web-app
  team-plans  /Users/you/openspec/team-plans
```

## 用它：一个变更，两个文件夹 [#use-it-one-change-two-folders]

假设 `add-login` 变更位于 `team-plans` 存储库，它的代码位于 `web-app`。打开 `platform` 工作集，让智能体实施这个变更。在那一个会话里，它可以：

- 读取 `team-plans/openspec/changes/add-login/` 以及旁边的规格
- 编辑 `web-app/` 里的代码
- 从 `web-app` 内部运行 `openspec` 命令

没有工作集的话，智能体只能看到它启动时所在的那个文件夹。

## 开箱可用的工具 [#tools-out-of-the-box]

- **VS Code**（`--tool code`）和 **Cursor**（`--tool cursor`）：内置。各自打开一个包含所有成员文件夹的窗口。
- **终端里的 Claude Code 和 Codex**：在相关工作流改造期间，暂时禁用作为工作集启动器。`--tool claude` 或 `--tool codex` 会报错中止，说明这一点并指向 VS Code 或 Cursor。
- **其他编辑器**：在 [CLI 设置（config.json）](./configuration/config-json.md) 的 `openers` 键下添加它们。
