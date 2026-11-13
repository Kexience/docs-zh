---
source_url: https://opencode.ai/docs/console/members/
source_hash: sha256:7164c0ea97654b7cce566d589166c0ed90a48d4e38c7dce491fb5ad1f6a99153
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# 成员

所有者和管理员在 **Settings › Members** 中管理人员。打开一个成员可以查看其用量和预算策略。

## 邀请成员

1. 打开 **Settings › Members**，点击 **Invite Members**。
2. 添加一个或多个电子邮箱地址。用空格、逗号或分号分隔，或直接粘贴一个列表。
3. 点击 **Send invitations**。

每个人都会收到一封标题为 **Join Acme Inc. on OpenCode** 的邮件，内含 **Join workspace** 按钮。

邀请在 7 天后过期。所有人都会以 **Member** 身份加入；在他们加入后可以[更改其角色](#更改角色)。

<Callout>
  [OpenCode Go](../go/index.md) 和 Go Plus 面向单个成员。要邀请队友，请升级到 Go Teams（每成员每月 $20）。在 Go Teams 中，你邀请或预配的每个成员都拥有自己的 Go 限额，从他们加入当月起按每月 $20 计费。
</Callout>

成员也可以自动加入：

- [SSO](../sso/index.md#automatic-membership) 在已验证邮箱域名下的人首次登录时把他们加入。
- [目录同步](../scim/index.md)随着你在身份提供方中的分配自动添加和移除人员。

## 接受邀请

受邀者必须使用发送邀请时所用的电子邮箱登录。接受邀请有两种方式：

- 点击邀请邮件中的 **Join workspace**，然后登录或创建账号。
- 登录 Console，打开工作区菜单，并在 **Pending invitations** 下点击 **Join**。

如果他们使用不同的账号登录，Console 会要求他们以受邀邮箱 **Sign out and continue**。

## 管理待处理的邀请

待处理的邀请会出现在 Members 表格中，显示为 **Pending · Expires** 加日期，或 **Expired**。

| 操作 | 方式 |
| ------ | ----------------------------------------------------------------------------------------- |
| 重新发送 | **⋯ › Resend invitation**。发送一个有效期 7 天的新链接；旧链接随即失效。 |
| 撤销 | **⋯ › Remove...**。链接立即失效。 |

## 更改角色

打开成员所在行中的角色菜单，选择 **Member**、**Admin** 或 **Owner**。

你只能授予不高于自己角色的权限，并且工作区始终保留至少一名所有者。参见[角色](../workspaces/index.md#roles)。

## 移除成员

1. 点击成员所在行中的 **⋯ › Remove...**。
2. 通过 **Remove member** 确认。

其访问权限会立即被撤销，之后你可以再次邀请他们。他们的历史用量会保留在工作区的报告中。

移除成员还会撤销他们在工作区中创建的 API key，包括服务账号密钥。服务账号本身会保留，其他人创建的密钥继续有效。参见[撤销](../api/index.md#revocation)。

## 成员详情

点击一个成员可以查看其月度预算、使用的模型和客户端、用量图表以及请求日志。在这里可以设置其[预算](../budgets/index.md#member-budgets)，并将其用量导出为 CSV。
