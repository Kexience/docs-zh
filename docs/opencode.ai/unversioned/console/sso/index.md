---
source_url: https://opencode.ai/docs/console/sso/
source_hash: sha256:f004b67d1ef24114cb63efd3a37e094dc734f17d7b9380403f5ad0779548720f
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# SSO

单点登录（SSO）让工作区成员在登录时经由你公司的身份提供方完成认证。所有者可以在 **Settings › Security** 中进行设置，每个工作区都包含该功能。

| 协议 | Provider |
| -------------- | -------------------------------------------------------------------------------------- |
| OpenID Connect | Google Workspace、Microsoft Entra ID、Okta、Auth0、Ping Identity 或任何 OIDC provider |
| SAML 2.0 | Google Workspace、Microsoft Entra ID、Okta 或任何 SAML provider |

每个工作区有一个 SSO 连接。

## 设置 OIDC

1. 打开 **Settings › Security**，点击 **Configure SSO**，选择 **OpenID Connect** 和你的 provider。
2. 按照显示的步骤在 provider 中创建一个应用，附带 `openid`、`email` 和 `profile` 作用域。
3. 输入 **Issuer URL** 或你的租户/域名，加上 **Client ID**、**Client Secret** 和一个 **Display Name**，然后点击 **Save**。
4. 把连接中的 **Callback URL** 复制到 provider 允许的重定向 URI 中。

```text
https://opencode.ai/console/auth/sso/ssoconn_.../callback
```

保存时 Console 会检查该 issuer 是否可访问。连接保存后 SSO 立即生效。

## 设置 SAML

1. 打开 **Settings › Security**，点击 **Configure SSO**，选择 **SAML 2.0** 和你的 provider。
2. 把 **ACS URL** 和 **SP Entity ID** 复制到你的 provider。自定义 provider 可以使用 **SP Metadata URL**，或改为下载 XML。
3. 通过 URL、XML 上传或粘贴添加 provider 的元数据。你也可以手动输入 **IdP Entity ID**、**IdP SSO URL** 和 **IdP Certificate**。
4. 检查详细信息并点击 **Activate SSO**。

```text
ACS URL:       https://opencode.ai/console/auth/sso/ssoconn_.../callback
SP Entity ID:  https://opencode.ai/console/auth/sso/ssoconn_.../metadata
```

你的 provider 必须对响应或断言进行签名，并以 `email` 属性或 NameID 的形式发送用户的邮箱。

## 验证邮箱域名

使用已验证域名邮箱登录 [Console](https://opencode.ai/console) 的人会被送到你的身份提供方。SSO 激活后，在 **Email domains** 下点击 **Add domain**，输入你的域名，并发布显示的 TXT 记录。

```text
Name:   _opencode-console-challenge.example.com
Type:   TXT
Value:  oc-verify=...
```

记录发布后点击 **Verify Domain**。DNS 变更可能需要一段时间才能传播。每个域名只能属于一个工作区。

## SSO 强制

工作区启用 SSO 后，管理员和成员必须通过它登录才能打开该工作区，Console 会自动将他们重定向。通过 `/connect` 连接 OpenCode 遵循同样的规则。

所有者也可以不通过 SSO 登录，因此配置错误的 provider 不会把工作区锁在它的设置之外。

## 自动加入成员

已验证域名下的人在首次通过 SSO 登录时会以 **Member** 身份加入工作区。在以下情况下他们不会被自动加入：

- 他们有待处理的邀请。此时会改用该邀请。
- 工作区使用[目录同步](../scim/index.md)，由它决定成员资格。
- 工作区有 [Go](../go/index.md) 订阅。

发送到 SSO 工作区的邀请会在受邀者打开链接时将其送往你的身份提供方。

## 已有账号

如果有人已经拥有使用同一邮箱的 Console 账号，他们会在 SSO 流程中再次登录，并通过 **Link account** 确认。邀请不会跳过这一确认。已验证工作区域名下由 SCIM 预配的账号仍然可以自动关联。

## 编辑或删除

点击连接上的 **Edit** 可以修改其详情。将密钥或证书留空即可保留当前值。要在 OIDC 和 SAML 之间切换，请删除该连接并新建一个。

通过 **⋯ › Delete...** 删除连接。成员会回到他们的其他登录方式，目录同步会停止并撤销其 token。邮箱域名会被保留。
