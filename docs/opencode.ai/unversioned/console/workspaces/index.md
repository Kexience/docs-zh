---
source_url: https://opencode.ai/docs/console/workspaces/
source_hash: sha256:e3b82b3416b1e64e2a33cdc630b9a3a140bb4202f0ab6560ead106fa23e41921
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# 基础

工作区承载了 [Console](https://opencode.ai/console) 中的所有内容：成员、额度、预算、provider、策略和服务账户。用量和计费都按工作区单独追踪。

一个工作区可以只有一个成员。你可以独自使用额度、[自己的 provider](../providers/index.md)、预算和 [Go](../go/index.md)，只在需要时再[邀请成员](../members/index.md)。

## 你的第一个工作区

注册时，Console 会为你创建一个名为 **Personal** 的工作区，你是它的所有者兼唯一成员。如果你通过邀请注册，则会加入发出邀请的工作区，而不会创建 Personal 工作区。

## 创建工作区

1. 在顶栏打开工作区菜单。
2. 点击 **Create Workspace**。
3. 输入 **Workspace name**，然后点击 **Create**。

你会成为新工作区的所有者。

## 切换工作区

从工作区菜单中选择另一个工作区。Console 会让你停留在同一个页面，例如从 `/acme/settings/members` 切换过去时，会打开另一个工作区的 Members 页面。

待处理的邀请会显示在同一菜单的顶部。参见[成员](../members/index.md#accept-an-invitation)。

## 连接 OpenCode

在 OpenCode 中运行 `/connect`，然后在浏览器中选择工作区。此后 OpenCode 就会使用该工作区的模型、策略和预算。

```text
/connect
```

再次运行 `/connect` 可以把 OpenCode 切换到另一个工作区。工作区[策略](../../policies/index.md#console)会被替换为新工作区的策略，断开连接时则被清除。

## 角色

每个成员拥有一个角色。新成员始终以 **Member** 身份加入。

| 角色   | 可以做的事                                                                                                           |
| ------ | -------------------------------------------------------------------------------------------------------------------- |
| Member | 使用 OpenCode，查看自己的用量、日志和预算。                                                                          |
| Admin  | 拥有 Member 的全部能力，另外可以管理成员、计费、预算、provider、策略、服务账户和设置。                               |
| Owner  | 拥有 Admin 的全部能力，另外可以管理 SSO 和目录同步、授予 Owner 角色，以及删除工作区。                                |

成员可以在 **Activity** 上查看自己的用量和日志，并且当排行榜对成员可见时还能看到排行榜。当工作区拥有 [Go Teams](../go/index.md) 订阅时，他们还能看到 **Go** 以及自己的配额限制。
他们从账户菜单打开 **Account**。

### 角色规则

- 一个工作区可以有多位所有者，并且始终保留至少一位。
- 你不能授予比自己更高的角色，因此只有所有者才能让其他人成为所有者。
- 你不能更改自己的角色。

### 转移所有权

1. 以所有者身份打开 **Settings › Members**，将新所有者的角色设为 **Owner**。
2. 让新所有者把你的角色改为 **Admin** 或 **Member**。

## 删除工作区

只有所有者才能删除工作区，且前提是他们至少还属于另一个工作区。

1. 打开 **Settings › General**，点击 **Delete workspace**。
2. 勾选所有确认项。
3. 点击 **Delete workspace** 进行确认。

删除立即生效且无法撤销：

- 成员立即失去访问权限。
- 所有服务账户的 API key 和待处理的邀请被吊销。
- 自动充值停止。
- 正在生效的 Go 订阅终止。
- 剩余的额度余额作废。

<Callout type="warning">有支付正在处理时无法删除。请在几分钟后重试。</Callout>

## 退出工作区

1. 从账户菜单打开 **Account**。
2. 在 **Connected workspaces** 下，点击该工作区旁边的 **Leave**。
3. 通过 **Leave workspace** 确认。

最后一位所有者不能退出；请先将另一位成员设为所有者。在启用了 SSO 或目录同步的工作区中，成员资格由你的身份提供方管理，因此无法从 Console 退出。退出后想重新加入，请申请新的邀请。
