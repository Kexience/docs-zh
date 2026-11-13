---
source_url: https://opencode.ai/docs/console/api/
source_hash: sha256:9e5fde6bf5966124d6f5ab358d58d291376f94630b39ee22dfc134fa13e0feb2
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# API 概览

Console API 让你的脚本和集成能够调用模型。每个请求都使用 API 密钥进行身份验证。

```bash
curl --fail-with-body "https://opencode.ai/inference/v1/models" \
  --header "Authorization: Bearer oc_sk_..."
```

| API                                      | 端点                                       |
| ---------------------------------------- | ------------------------------------------ |
| [推理](inference/index.md)               | `https://opencode.ai/inference/...`        |
| [Providers](providers/index.md)          | `https://opencode.ai/inference/custom/...` |

## API 密钥

工作区成员和服务账户都可以持有 API 密钥。发送密钥时将其作为 bearer token。

```text
Authorization: Bearer oc_sk_...
```

|                  | 个人 API 密钥                                        | 服务账户密钥                                                             |
| ---------------- | ---------------------------------------------------- | ------------------------------------------------------------------------ |
| 创建者           | 任意成员，为自己创建                                 | 所有者和管理员                                                           |
| 创建位置         | **Account › Personal API keys**                      | **Settings › Service accounts**                                          |
| 代表谁           | 创建该密钥的成员                                     | 该服务账户                                                               |
| 用量计入         | 该成员的[预算](../budgets/index.md#member-budgets)   | 服务账户的[预算](../budgets/index.md#service-account-budgets)            |
| 最适合           | 你自己的脚本和[harness](../harnesses/index.md)       | CI、共享机器和集成                                                       |

- 每个密钥只在一个工作区中有效，创建时即选定。无需工作区请求头。
- 完整密钥只在创建后立即显示一次。之后 Console 只显示它的前缀。
- **有效期**为可选项：**Never**、**1 day**、**7 days**、**30 days** 或 **Custom**（1 到 365 天）。过期的密钥无法续期，只能新建。

## 个人 API 密钥

个人密钥以你的身份行事。你的角色、[预算](../budgets/index.md#member-budgets)和模型规则都适用于它。

1. 从账户菜单打开 **Account**，找到 **Personal API keys**。
2. 点击 **Add API key**。
3. 选择 **Workspace**、**Key name**，以及可选的 **Expiration**。所有者和管理员还可以选择 **Permissions**。
4. 点击 **Create** 并复制密钥。

```text
oc_sk_1a2b3c4d5e6f_...
```

密钥遵循你当前对该工作区的访问权限。如果你的角色变了，密钥能做的事也随之变化。如果工作区强制启用 [SSO](../sso/index.md#sso-enforcement)，则只有在你拥有活跃的 SSO 会话时密钥才可用，除非你是所有者。

## 服务账户

服务账户是工作区中的非人类成员，拥有自己的 API 密钥、用量和[预算](../budgets/index.md#service-account-budgets)。自动化场景请使用服务账户，这样用量不会挂在某个人头上。它们由所有者和管理员管理。

1. 打开 **Settings › Service accounts**，点击 **Add Service Account**，然后命名，例如 `CI Pipeline`。
2. 打开该服务账户，点击 **Add API Key**。
3. 选择 **Key name**、可选的 **Expiration** 和 **Permissions**，然后点击 **Create**。
4. 复制密钥。

```bash
export SERVICE_API_KEY="oc_sk_..."
```

所有者和管理员之后可以通过密钥操作菜单中的 **Edit…** 重命名服务账户密钥或更改其权限。

## 权限

每个密钥都有一个权限级别，创建密钥时在 **Permissions** 下选择。

| 权限           | 允许的内容                                                                       |
| -------------- | -------------------------------------------------------------------------------- |
| **All**        | 成员或服务账户能做的一切，**This account's API keys** 除外。                     |
| **Restricted** | 仅限你选择的资源。                                                               |
| **Read only**  | 对所有资源的只读访问。该密钥可以列出模型但不能调用它们。                         |

密统能做的永远不会超过它所代表的对象。个人密钥受成员当前角色限制，服务账户密钥受[服务账户能做的事](#限制)限制。

### 受限密钥

把每个资源设置为 **None**、**Read** 或 **Write**。**Write** 包含 **Read**。

| 资源                        | 级别                  |
| --------------------------- | --------------------- |
| **Models**                  | **Read**、**Request** |
| **Usage**                   | **Read**              |
| **Budgets**                 | **Read**、**Write**   |
| **Members**                 | **Read**、**Write**   |
| **Providers**               | **Read**、**Write**   |
| **Billing**                 | **Read**、**Write**   |
| **Workspace settings**      | **Read**、**Write**   |
| **SSO**                     | **Read**              |
| **Service accounts**        | **Read**              |
| **This account's API keys** | **Write**             |

**Models › Read** 可列出模型，**Models › Request** 还能通过[推理](inference/index.md)和 [Providers](providers/index.md) API 调用模型。例如，一个只调用模型的密钥需要：

```text
Permissions: Restricted
Models:      Request
```

在分级权限推出之前以 **Inference only** 创建的密钥会显示为 **Restricted**，且 **Models** 设为 **Request**。

### 谁能授予什么

- **成员**只能创建可以列出和调用模型的个人密钥。Console 会显示 "This key can list and call models as you."，而不给出权限选项。
- **所有者和管理员**可以为他们的个人密钥授予 **All**、**Restricted** 或 **Read only**，上限是他们自己的角色。默认是 **Restricted** 且 **Models** 设为 **Request**。如果他们之后被降级，其密钥的权限也会相应缩减。
- **服务账户密钥**默认为 **All**。权限由所有者和管理员选择。

### 限制

有些操作始终需要有人在 Console 中登录，而用密钥创建密钥受到严格限制。

- 任何 API 密钥都不能更改 SSO 设置或删除工作区。
- 服务账户密钥不能邀请成员、更改角色、移除成员、管理计费、更改工作区设置、管理模型，也不能创建或移除服务账户，即使拥有 **All** 也不行。
- **This account's API keys** 仅对服务账户密钥可用，且 **All** 不包含它。拥有它的密钥只能为其所属的服务账户创建和吊销密钥。新建的密钥必须是 **Restricted**，不得超过创建密钥的权限范围，且不能包含 **This account's API keys**。
- 个人密钥永远无法获得 **This account's API keys**，任何 API 密钥都不能创建或吊销个人 API 密钥。

超出密钥权限的请求返回 HTTP `403`。

## 吊销

| 密钥                | 谁可以吊销         | 位置                                                                              |
| ------------------- | ------------------ | --------------------------------------------------------------------------------- |
| 个人 API 密钥       | 拥有它的成员       | **Account › Personal API keys**，然后 **Revoke**                                  |
| 个人 API 密钥       | 所有者和管理员     | **Settings › Members** 中该成员页面下的 **API Keys**                              |
| 服务账户密钥        | 所有者和管理员     | **Settings › Service accounts** 中该服务账户页面下的 **API Keys**                 |

以下情况也会自动吊销密钥：

- 离开工作区、被移出工作区，或通过 [SCIM](../scim/index.md) 被取消配置时，该人在其中创建的每个密钥（包括服务账户密钥）都会被吊销。同一服务账户上的其他密钥继续有效。
- 移除服务账户会吊销其所有密钥。

被吊销和过期的密钥立即失效，并返回 HTTP `401`。
