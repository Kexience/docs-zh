---
source_url: https://opencode.ai/docs/console/billing/
source_hash: sha256:83a12e82756da7591adc21de84f79b05451f09b2db1215f366ead5eded14a74c
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---
# 计费

Console 对任何规模的团队都免费，没有按席位收费。你只需为用量付费，费用从覆盖整个工作区的预付额度（credits）中扣除。Owner 和 admin 在 **Settings › Billing** 中管理计费。

通过[你自己的 provider](../providers/index.md) 产生的用量由该 provider 计费，而不是由 Console 计费。

## 添加支付方式

1. 打开 **Settings › Billing**。
2. 在 **Payment methods** 下，点击 **Add**。
3. 选择一种支付方式并完成 Stripe 设置。

支持的支付方式：

- 银行卡
- Link
- 支付宝
- UPI
- 微信支付

使用 **⋯ › Make default** 来选择用于自动扣款的支付方式。移除某个支付方式可能会中断依赖它的自动充值和 Go 续订。

## 添加额度

1. 在 **Credits** 下，点击 **Add credits**。
2. 选择 $10、$50 或 $100，或选择 **Other** 并输入金额。
3. 选择支付方式并点击 **Confirm and pay**。

系统会在其上加收 4.6% + $0.31 的处理费，因此购买 $50 实际支付 $52.61，而完整的 $50 会计入余额。

## 自动充值

自动充值会在余额不足时自动购买额度。

1. 在 **Auto-recharge** 下，点击 **Add rule**。
2. 设置触发扣款的余额阈值和每次充值的金额。
3. 点击 **Save**。

自动充值会从默认支付方式扣款，并包含处理费。如果扣款失败，自动充值会关闭，直到你重新设置。

## 查看余额

**Activity** 中的 **Billing** 卡片会向 owner 和 admin 显示余额，并可打开 **Settings › Billing**。

工作区顶栏中的 **Billing** 按钮，或按 `B` 键，会打开一个抽屉，实时显示 Go 限额、额度和用量。Owner 和 admin 可以看到工作区的余额、用量和自动充值；成员只能看到自己的用量和限额。

## 额度用尽时

一旦余额归零，付费请求会返回 HTTP `402` 失败。余额永远不会变为负数。

```text
Upstream request failed: Insufficient account funds
```

## 发票

每笔支付都会出现在 **Invoices** 下，带有状态和 **Download invoice** 或 **View receipt** 链接。

| 条目 | 产生方式 |
| ---------------- | ---------------------------------------- |
| 余额充值 | 手动添加额度 |
| 自动充值 | 自动充值 |
| Go 订阅 | 订阅 Go、Go Plus 或 Go Teams |
| Go 续订 | Go 的每月续订 |
| Go Plus 升级 | 从 Go 升级到 Go Plus |
| Go Teams 升级 | 从 Go 或 Go Plus 升级到 Go Teams |
| Go Teams 成员 | 有成员加入 Go Teams 工作区 |
| Monthly Usage | 账单式计费 |

## 税务表单

美国客户可以下载 [Anomaly Innovations Inc. 的 W-9 表格](https://opencode.ai/docs/assets/anomaly-w9.pdf)。

## 账单式计费

有信用协议的工作区可以按月开具发票，而不是购买预付额度。请联系支持团队进行设置。

- 用量从信用额度中扣除，而不是从预付余额中扣除。
- 每个月的发票在每月 1 日（UTC）开具，14 天后到期。
- 未支付的发票上有 **Pay now** 按钮。
- 当达到信用额度上限或发票逾期时，请求会返回 HTTP `402` 失败。

## Go

[OpenCode Go](../go/index.md) 订阅使用相同的支付方式，并出现在同一张发票列表中。你也可以[用额度支付 Go](../go/index.md#pay-with-credit)。在 **Go** 页面开启 **Extra Usage**，即可在达到 Go 限额后用额度继续付费。
