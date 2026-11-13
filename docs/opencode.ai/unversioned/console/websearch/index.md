---
source_url: https://opencode.ai/docs/console/websearch/
source_hash: sha256:a5b7b3e091d7b91e57b6c12a1a5d2e2778151a2a50edd6f2e8e781f8b804b338
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---

# 网页搜索

Console 为已连接的 OpenCode 用户提供托管的网页搜索。工作区所有者或管理员只需为工作区启用一次，无需给成员单独的搜索 provider 密钥。

每次成功的搜索花费 **$0.01**，计入工作区余额和成员消费限额。

## 启用

1. 以工作区所有者或管理员身份登录 [Console](https://opencode.ai/console)。
2. 打开 **Integrations**，在 **Hosted Web Search** 上点击 **Set up**。
3. 点击 **Enable**。

之后每个成员通过 `/connect` 把 OpenCode 连接到工作区。

```text
/connect
```

工作区配置会把 **OpenCode Web Search** 选为默认 provider。成员无需设置 `websearch.provider`，也无需添加 provider API key。自行设置了 `websearch.provider` 的成员会保留自己的选择。

## 搜索

在提示词中让 OpenCode 获取最新信息。搜索由 OpenCode 运行，而不是在 Console 的交互页面中。

```text
Find the latest Bun release and summarize the changes with source links.
```

托管 provider 会搜索公共网页并返回最多八个结果。OpenCode 使用这些结果回答提示词并引用来源。

关于配置权限或禁用该工具，参见[网页搜索指南](../../websearch/index.md)。

## 计费

Console 在一次搜索返回有效的结果集之后收取 **$0.01**。失败和被限流的搜索不收费。

网页搜索在 **Activity › Usage**、**Activity › Overview**、成员活动、发票和 CSV 导出中与模型用量分开显示。适用的全支出预算策略会把网页搜索费用包含在内。

## 隐私

托管的网页搜索没有任何数据留存。Console 及其托管搜索 provider 会处理每个查询及其结果，但不存储其内容。
