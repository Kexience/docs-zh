---
source_url: https://opencode.ai/docs/console/
source_hash: sha256:5b8d74775c5091440fcd6beb510ab2f9ebbdbb3d9c654a1aef293d18239c8fba
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# 简介

[OpenCode Console](https://opencode.ai/console) 是一项可选服务，无论你独自使用还是团队协作，都能为 OpenCode 带来额外的便利。

- [工作区](workspaces/index.md)：与你的[团队](members/index.md)共享访问权限
- [推理服务](models/index.md)：涵盖专有模型和开源模型
- [Provider](providers/index.md)：通过 Console 网关接入你自己的 provider 账户
- 用量追踪和[预算](budgets/index.md)控制
- 部署团队级策略以约束 OpenCode 的行为
- [网页搜索](websearch/index.md)
- [Harnesses](harnesses/index.md)：在 Claude Code、Codex 及其他 agent 中使用 Console 模型
- [OpenCode Go、Go Plus 与 Go Teams](go/index.md)：每月 $10、$40 和 $20/成员的订阅，用于访问开源模型

## 快速开始

使用 Console 并不需要一个团队。每个账户都以一个 **Personal** 工作区起步，你是其中的唯一成员。

1. 登录 [Console](https://opencode.ai/console)。
2. 订阅 [Go](go/index.md)、添加[额度](billing/index.md#add-credits)，或接入一个 [provider](providers/index.md)。
3. 在 OpenCode 中运行 `/connect` 并选择工作区。
4. 可选：[邀请](members/index.md#invite-members)你的团队。

```text
/connect
```

## 策略

Policies 页面中的 Providers 和 Tools 规则适用于连接到该工作区的每一个 OpenCode 客户端。它们以[策略](../policies/index.md#console)语句的形式下发，优先级高于成员的用户级和项目级配置，并在约一分钟内生效。托管偏好设置和系统配置文件仍然高于工作区配置；参见[优先级](../policies/index.md#precedence)。
