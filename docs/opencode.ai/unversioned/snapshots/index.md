---
source_url: https://opencode.ai/docs/snapshots/
source_hash: sha256:9a730a042390c312a04979e1a54adead85045f14202d6da4d4a1fdac4252289f
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# 快照（Snapshots）

快照让你能够将最近的对话和文件更改一起撤销。可以用它来修订最近的工作，但重要的内容仍请使用 Git 提交或备份来保存。

## 工作流程

在想要修订的响应之后运行 `/undo`。OpenCode 会暂存这次回滚，恢复受影响的文件，并把被撤回的提示词放回输入框，方便你编辑。

```text
/undo

# Edit the restored prompt, then submit it again.
Add validation without changing the public API.
```

提交编辑后的提示词会正式执行已暂存的回滚。在提交之前，运行 `/redo` 可以取消它，恢复到 `/undo` 之前的对话和文件。

```text
/redo
```

终端还提供默认快捷键：

| 操作                     | 命令    | 快捷键        |
| ---                      | ---     | ---           |
| 暂存上一条消息的回滚     | `/undo` | `<leader>u`   |
| 取消已暂存的回滚         | `/redo` | `<leader>r`   |

你也可以选中较早的一条消息，选择 **Revert** 来暂存一个回到该时间点的回滚。

## 捕获

对每一个模型步骤，OpenCode 会在模型调用之前立即尝试一次快照，并在该步骤到达记录的成功或失败状态时再拍一次。助手消息会记录这两次快照之间发生了哪些路径变更。

```text
before model step ── snapshot A
model edits src/api.ts
step finishes ────── snapshot B ── changed: src/api.ts
```

捕获是尽力而为的。如果任一快照不可用，对话会继续进行，但该步骤可能没有可用于恢复的文件更改。

## 范围

快照覆盖会话在 Git worktree 内的活动目录。例如，一个在 `packages/app` 中打开的会话会捕获 `packages/app` 下符合条件（eligible）的文件，而不是仓库中其他地方的更改。

| 内容                                       | 是否捕获 | 示例                                    |
| ---                                        | ---      | ---                                     |
| 活动目录中的已跟踪文件                     | 是       | `packages/app/src/app.tsx`              |
| 未忽略的未跟踪文件，单个不超过 2 MiB       | 是       | `packages/app/notes.txt`                |
| 被 Git 忽略的文件                          | 否       | `packages/app/dist/app.js`              |
| 超过 2 MiB 的单个未跟踪文件                | 否       | `packages/app/debug.log`                |
| 活动目录之外的文件                         | 否       | `packages/server/src/index.ts`          |
| Git 元数据和其他副作用                     | 否       | 提交、分支、数据库或进程                |

文件系统快照需要 Git 仓库。在仓库之外，`/undo` 仍可回滚对话历史，但无法恢复文件。

## 恢复

一次回滚只恢复归因于所选对话边界之后的助手步骤的那些路径。每个路径都会回到第一次被回退步骤之前的状态；由这些步骤创建的文件，如果在当时并不存在，则会被移除。

| 时间线               | `src/api.ts` | `src/new.ts` |
| ---                  | ---          | ---          |
| 所选边界             | 版本 A       | 不存在       |
| 之后的助手步骤       | 版本 B       | 已创建       |
| 回滚之后             | 版本 A       | 已移除       |

未归因于这些步骤的路径不会被动。对受影响路径的当前编辑可能被覆盖，因此在继续之前请查看恢复摘要和 `git diff`。

```sh
git diff --stat
git diff
```

## 存储

OpenCode 将快照存储在本地，位于其数据目录下一个独立的内部 Git 对象数据库中。快照捕获不会创建提交、移动分支，也不会有意更改你仓库的索引。

```sh
# Your repository remains an ordinary dirty worktree after capture.
git status --short
```

快照对象可能包含已跟踪文件和符合条件的未跟踪文件的完整内容。请将 OpenCode 数据目录视为敏感的本地数据。

## 设置

快照默认启用。在[配置](../config/index.md#snapshots)中把 `snapshots` 设为 `false` 可以停止之后的文件系统捕获。

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "snapshots": false,
}
```

禁用快照不会删除已经存储的快照。对话回滚仍然可用，但由于缺少捕获的文件系统状态，它无法恢复相关的文件更改。

## 安全性

快照是一种便利功能，而不是事务或备份：

- Shell 命令可能更改服务、进程、网络资源、数据库、Git 状态、被忽略的输出或活动目录之外的文件。恢复快照不会撤销这些影响。
- 中断或失败的工作可能在捕获失败或不存在可用的快照对时留下更改。
- 恢复受影响的路径会覆盖它们的当前内容。取消一次已暂存的回滚也可能覆盖其后的编辑。
- OpenCode 在会话运行期间会拒绝回滚操作，但外部编辑器和命令仍可能在捕获与恢复之间更改 worktree。
- 提交一次回滚只是从当前会话的对话视图中移除消息，而不会从持久化的会话历史或已有的快照存储中移除。它不是安全擦除。

在脏（dirty）worktree 上使用 `/undo` 之前，请先提交或备份重要工作。
