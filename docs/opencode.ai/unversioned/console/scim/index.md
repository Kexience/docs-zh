---
source_url: https://opencode.ai/docs/console/scim/
source_hash: sha256:7896e3ab6ea9c3e08efea510866bf631660a234612b1c7c395e76c9a26321cd6
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# 目录同步

目录同步（SCIM 2.0）会在你于身份提供商中给某人分配工作区时把他加入工作区，并在你取消分配时移除其访问权。角色始终在 Console 中管理。

```text
https://opencode.ai/console/scim/v2
```

## 开始之前

- 为工作区设置 [SSO](../sso/index.md)。
- [验证](../sso/index.md#verify-email-domains)你的成员用来登录的每一个邮箱域名。目录同步只添加已验证域名下的人；其他人请从 [Members](../members/index.md) 邀请。

## 创建 token

只有工作区所有者可以设置目录同步，或创建和吊销其 token。

1. 打开 **Settings › Security**，在 **Directory sync** 下点击 **Set up**。
2. 复制 **SCIM base URL** 和 token。token 只显示一次，请存放在密钥管理器中。

你的身份提供商会在每次请求时携带这个 token。

```text
Authorization: Bearer <token>
```

## 连接你的身份提供商

### Okta

1. 添加 **SCIM 2.0 Test App (Header Auth)** 应用。
2. 设置 base URL，并在 **API Token** 中输入 `Bearer ` 加 token。
3. 启用 **Create Users**、**Update User Attributes** 和 **Deactivate Users**。保持 **Import Groups** 和密码同步关闭。

### Microsoft Entra ID

1. 在你的企业应用中打开 **Provisioning**，把模式设为 **Automatic**。
2. 把 base URL 填入 **Tenant URL**，把 token 填入 **Secret Token**。
3. 分配用户和组，然后启动 provisioning。

### 其他提供商

使用带请求头 token 认证的 SCIM 2.0 应用，指向该 base URL。Console 支持 `/Users` 和 `/Groups` 端点。

先分配一个测试账号。在第一次请求之后，**Directory sync** 会显示 **Connected to your identity provider**。

## 同步内容

| 在你的身份提供商中 | 在 Console 中                                                              |
| ------------------ | -------------------------------------------------------------------------- |
| 分配一个人         | 以 **Member** 身份加入。已有成员保持其角色。                               |
| 更新姓名           | 更新个人资料。                                                             |
| 取消分配或停用     | 暂停访问并显示为 **Deactivated**。其创建的 API key 会被吊销。              |
| 重新分配           | 恢复访问。已吊销的 key 保持吊销。                                          |
| 删除               | 从工作区移除。其账号和其他工作区不受影响。                                 |

- 角色和邮箱地址不会因目录同步而改变。
- 最后一位所有者不能被停用或删除。
- 有 [Go](../go/index.md) 订阅的工作区无法通过目录同步添加成员。

## 组

推送组以便为其成员打标签，例如使用 Okta 的 **Push Groups** 或 Entra 的组分配。先分配人员，再推送他们的组。

```text
Platform Admins  →  platform-admins
```

每个组都会用一个以该组命名的标签来标记其成员。在 **Settings › Security › Group tags** 下，你可以重命名标签、让多个组指向同一个标签，或停止给某个组打标签。退出一个组会移除它的标签。

## 轮换 token

1. 点击 **New token**，把它安装到你的身份提供商。
2. 等到新 token 显示出最后使用时间。
3. 吊销旧 token。

吊销 token 会停止后续更新，但不会改变现有成员。删除 SSO 连接会吊销所有 token。

## SSO 与目录同步

一旦工作区签发过 token，SSO 就不再[自动添加成员](../sso/index.md#automatic-membership)。由目录决定谁属于工作区，即使 token 后来被吊销也是如此。
