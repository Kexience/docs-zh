---
source_url: https://opencode.ai/docs/console/go/
source_hash: sha256:ae4b8acf1df7d9f0dd6c86f99a9e5d7ea865fcca4877793087b0326a920e31a8
translated_at: 2026-11-13T21:30:00+08:00
translation_version: 1
---
# Go

OpenCode Go 让你能稳定地使用热门的开放编码模型，提供三个按月计费的方案：

| 方案 | 价格 | 包含的用量 |
| ------------ | -------------------- | -------------------------------------------------------------------------- |
| **Go** | **$10/月** | 以更低成本使用下述模型 |
| **Go Plus** | **$40/月** | 下述模型的用量上限更高 |
| **Go Teams** | **$20/成员/月** | 每位成员拥有自己的限额，每个模型都比 Go 高 $5/月 |

Go 在 OpenCode 中的工作方式与其他 provider 一样。你订阅 OpenCode Go 并获取 API key。它**完全可选**，使用 OpenCode 并不需要它。

该服务主要面向国际用户设计，提供稳定的全球访问。

## 使用方式

1. 登录 [OpenCode Console](https://opencode.ai/console)，订阅 Go、Go Plus 或 Go Teams，填写计费信息，并复制你的 API key。
2. 在 TUI 中运行 `/connect`，选择 **OpenCode Go**，粘贴你的 API key。

   ```text
   /connect
   ```

3. 运行 `/models` 选择一个通过 Go 提供的模型。

   ```text
   /models
   ```

<Callout>
  Go 和 Go Plus 面向只有一个成员的工作区，例如你注册时创建的 **Personal** 工作区。
  两者都可以随时升级到 Go Teams，当月未用完的额度会以余额返还。Go Teams 覆盖
  多成员工作区中的每一位成员，价格为每成员每月 $20。月中加入的成员
  收取 $20 并获得完整的一个月额度。Go Teams 不覆盖服务账号。
</Callout>

当前的模型列表包括：

- **Grok 4.7**
- **GLM-5.3-Flash**
- **GLM-5.3**
- **GLM-5.2**
- **GPT 6 Luna**
- **GPT 5.6 Luna**
- **Claude Haiku 5.5**
- **Gemini 4 Argon**
- **Kimi K3.1 Pro**
- **Kimi K3**
- **Kimi K2.7 Code**
- **LongCat-2.0**
- **Step 5 Preview**
- **Beam Free**（限时，限地区）
- **Iceman Contributor Free**（限时）
- **LongCat 2.5 Free**（限时）
- **MiMo-V2.6-Flash**
- **MiMo-V2.6-Pro**
- **MiMo-V2.5**
- **MiMo-V2.5-Pro**
- **MiniMax M3.1 Flash**
- **MiniMax M3**
- **Muse Spark 1.3 Contributor**（[限地区](https://ai.developer.meta.com/legal/geographic-use-policy)）
- **Muse Spark 1.2 Contributor**（[限地区](https://ai.developer.meta.com/legal/geographic-use-policy)）
- **Qwen3.8 Max**
- **Qwen3.8 Flash**
- **Qwen3.7 Plus**
- **DeepSeek V4.1 Flash**
- **DeepSeek V4 Pro**
- **Hy4**
- **Hy4 preview**
- **Hy3**

模型列表可能会随着我们测试和新增模型而变化。

### 启用受限模型

工作区的隐私设置会作用于 Go。默认情况下，会使用请求数据进行训练的付费端点被屏蔽，允许的地区为**欧洲与美国**。未保存隐私设置的工作区，对来自中国的请求也允许**全球**。

在 **Settings › Privacy** 中，owner 或 admin 可以启用：

- **DeepSeek V4.1 Flash 与 V4 Pro：** 在 **Regions** 下选择 **Global**。
- **LongCat 2.5 Free：** 在 **Regions** 下选择 **Global**。
- **Muse Spark 1.3 Contributor 与 Muse Spark 1.2 Contributor：** 开启 **Allow paid endpoints that train on request data**。

每个模型的训练与保留条款请参阅[隐私](隐私)。

## 用额度支付

Owner 和 admin 可以用工作区的额度支付 Go 的费用，包括续订和升级。在订阅时选择 **Credit** 作为支付方式，或稍后在 **Manage subscription** 中选择。它与 [Extra Usage](超出限额后的用量) 是分开的，后者用于支付超出限额的用量。

- 全部价格从你的额度余额中扣除。如果余额不足，可以先充值。
- 续订会在计费周期结束时从额度中扣除价格。如果额度不够，Go 会保持活跃，续订会在周期结束后第 1、3、7 天重试，并在充入足够额度后立即重试。如果最后一次重试失败，Go 会终止。
- 使用[账单式计费](../billing/index.md#invoiced-billing)的工作区不能用额度支付 Go。
- 用额度支付的 Go 费用退款会退回你的额度，并终止该 Go 周期。

## 可以在哪里使用？

OpenCode Go 为 [OpenCode](https://opencode.ai) 以及产生类似请求类型的其他编码 agent 而设计。我们会监控流量，防止影响其他用户体验的滥用行为。

你的客户端应当：

1. 发送典型的编码 agent 流量
2. 用它自己的 user agent 标识自己，例如 `my-coding-agent/1.0`，而不是通用的 SDK 或 HTTP 库名称。
3. 为每个会话在 `x-opencode-session` 中发送稳定的会话 ID，以便我们优化路由和提示词缓存。

要在 Claude Code、Codex、Hermes、Pi 和 Raycast 中接入 Go，请参阅 [Harnesses](../harnesses/index.md)。

### 已验证的客户端

除 OpenCode 外，以下客户端已验证可以正常使用 OpenCode Go，但我们不保证它们未来持续可用。

| 客户端 | 会话支持 |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Hermes** | 升级到 **v0.21.6 或更高版本**，它会在主请求和辅助 OpenCode 请求上发送该请求头（[PR #101864](https://github.com/NousResearch/hermes-agent/pull/101864)）。 |
| **Claude Code** | Go 能识别其原生会话请求头，无需自定义请求头包装。 |
| **Codex** | Go 能识别其原生会话请求头。部分版本和代理配置仍会丢失它；转发请求时请保留会话请求头。 |
| **ZCode** | Go 能识别其原生会话请求头。我们[关于 `x-opencode-session` 的请求](https://github.com/zai-org/feedback/issues/492)仍然未关闭，但现在已经不再必须发送该特定请求头。 |
| **Pi** | 当前构建版本会为 OpenCode 发送会话信息。请更新较旧的安装。 |
| **jcode** | 升级到 **v0.81.6 或更高版本**，它包含[会话请求头修复](https://github.com/1jehuang/jcode/issues/1167)。 |
| **Kilo Code CLI** | 包含 [PR #13752](https://github.com/Kilo-Org/kilocode/pull/13752) 的构建版本恢复了 OpenCode 会话请求头。该修复只覆盖 CLI，不包括 VS Code 扩展。请参阅 [issue #13723](https://github.com/Kilo-Org/kilocode/issues/13723)。 |

### 已知有问题的客户端

在我们调查过的版本中，这些客户端的会话支持缺失或不完整。链接的报告用于跟踪修复和变通方案。

| 客户端 | 状态与跟踪 |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **DeepSeek Harness** | 会话信息在部分模型路径上会到达，但在其他路径上缺失。我们能识别其原生请求头；剩余工作是在所有适配器上都发送它。[Discussion #5495](https://github.com/deepseek-ai/deepseek-harness/discussions/5495)。 |
| **GitHub Copilot Chat** | 自动会话请求头支持已在 [VS Code issue #334186](https://github.com/microsoft/vscode/issues/334186) 中提出请求。 |
| **Kimi Code** | [issue #3506](https://github.com/MoonshotAI/kimi-code/issues/3506) 中的会话请求头请求已以"不计划实现"关闭。 |
| **MiMo Code** | [Issue #2317](https://github.com/XiaomiMiMo/MiMo-Code/issues/2317) 已关闭，[PR #2327](https://github.com/XiaomiMiMo/MiMo-Code/pull/2327) 未合并即被关闭。 |

## 用量限额

用量限额以每月美元金额定义。下表展示了每个方案的每月限额以及每个模型的 token 价格。Go、Go Plus 和 Go Teams 的 token 价格相同。

每个模型有如下用量限额：5 小时 — 每月限额的 20%；每周 — 50%；每月 — 100%。

下面每个模型的每月限额决定了它的用量如何计入这些配额。每次响应都会报告该请求计入了多少，见 [`opencode.allowance`](../api/inference/index.md#cost)。

token 价格按每 1M token 计。

<PlanTabs id="go-pricing" label="Go plan" syncKey="go-plan">
  <div slot="go">

    | 模型 | 输入 | 输出 | 缓存读取 | 缓存写入 | 每月上限 |
    | -------------------------------- | --------------- | ----------------- | --------------- | ------------ | ---------------------------------------------- |
    | GLM-5.3-Flash | $0.15 | $0.50 | $0.03 | - | **$60** |
    | GLM-5.3 | $1.40 | $4.40 | $0.26 | - | **$15** |
    | GLM-5.2 | $1.40 | $4.40 | $0.26 | - | **$60** |
    | Kimi K3.1 Pro | $2.00 | $10.00 | $0.20 | $2.00 | **$15** |
    | Kimi K3 | $3.00 | $15.00 | $0.30 | $3.00 | **$15** |
    | Kimi K2.7 Code | $0.95 | $4.00 | $0.19 | - | **$60** |
    | LongCat-2.0 | $0.30 | $1.20 | $0.006 | - | **$60** |
    | Step 5 Preview | $1.00 | $2.70 | $0.10 | - | **$15** |
    | Beam Free | 免费 | 免费 | 免费 | - | **无限**<br /><small>限时</small> |
    | Iceman Contributor Free | 免费 | 免费 | 免费 | - | **无限**<br /><small>限时</small> |
    | LongCat 2.5 Free | 免费 | 免费 | 免费 | - | **无限**<br /><small>限时</small> |
    | MiMo-V2.6-Flash | $0.14 | $0.28 | $0.0028 | - | **$60** |
    | MiMo-V2.6-Pro | $0.435 | $0.87 | $0.003625 | - | **$15** |
    | MiMo-V2.5 | $0.14 | $0.28 | $0.0028 | - | **$60** |
    | MiMo-V2.5-Pro | $0.435 | $0.87 | $0.003625 | - | **$15** |
    | MiniMax M3.1 Flash | $0.15 | $0.60 | $0.015 | - | **$20** |
    | MiniMax M3（≤ 512K tokens） | $0.30 | $1.20 | $0.06 | - | **$60** |
    | MiniMax M3（> 512K tokens） | $0.60 | $2.40 | $0.12 | - | **$60** |
    | Muse Spark 1.3 Contributor | $0.10 | $0.20 | $0.002 | - | **$60** |
    | Muse Spark 1.2 Contributor | $0.10 | $0.20 | $0.002 | - | **$60** |
    | Qwen3.8 Max | $2.00 | $6.00 | $0.25 | $2.50 | **$15** |
    | Qwen3.8 Flash | $0.15 | $0.47 | $0.016 | $0.20 | **$30** |
    | Qwen3.7 Plus（≤ 256K tokens） | $0.40 | $1.60 | $0.04 | $0.50 | **$60** |
    | Qwen3.7 Plus（> 256K tokens） | $1.20 | $4.80 | $0.12 | $1.50 | **$60** |
    | DeepSeek V4.1 Flash（闲时） | $0.15 | $0.60 | $0.003 | - | **$100** |
    | DeepSeek V4.1 Flash（忙时） | $0.30 | $1.20 | $0.006 | - | **$100** |
    | DeepSeek V4 Pro（闲时） | $0.66 | $1.98 | $0.022 | - | **$15** |
    | DeepSeek V4 Pro（忙时） | $1.32 | $3.96 | $0.044 | - | **$15** |
    | Hy4 | $0.834 | $2.501 | $0.042 | - | **$60** |
    | Hy4 preview | $0.834 | $2.501 | $0.042 | - | **$30** |
    | Hy3 | $0.14 | $0.58 | $0.035 | - | **$60** |
    | Grok 4.7（≤ 200K tokens） | $2.00 | $6.00 | $0.50 | - | **$15** |
    | Grok 4.7（> 200K tokens） | $4.00 | $12.00 | $1.00 | - | **$15** |
    | GPT 6 Luna（≤ 272K tokens） | $0.10 | $0.50 | $0.01 | $0.125 | **$15** |
    | GPT 6 Luna（> 272K tokens） | $0.20 | $0.75 | $0.02 | $0.25 | **$15** |
    | GPT 5.6 Luna（≤ 272K tokens） | $0.20 | $1.20 | $0.02 | $0.25 | **$15** |
    | GPT 5.6 Luna（> 272K tokens） | $0.40 | $1.80 | $0.04 | $0.50 | **$15** |
    | Claude Haiku 5.5（≤ 100K tokens） | $0.10 | $0.50 | $0.01 | $0.125 | **$15** |
    | Claude Haiku 5.5（> 100K tokens） | $0.50 | $2.50 | $0.05 | $0.625 | **$15** |
    | Gemini 4 Argon（五折） | ~~$4.00~~ $2.00 | ~~$20.00~~ $10.00 | ~~$0.20~~ $0.10 | - | **$30** |

  </div>
  <div slot="go-plus">

    | 模型 | 输入 | 输出 | 缓存读取 | 缓存写入 | 每月上限 |
    | -------------------------------- | --------------- | ----------------- | --------------- | ------------ | ---------------------------------------------- |
    | GLM-5.3-Flash | $0.15 | $0.50 | $0.03 | - | **$180** |
    | GLM-5.3 | $1.40 | $4.40 | $0.26 | - | **$120** |
    | GLM-5.2 | $1.40 | $4.40 | $0.26 | - | **$180** |
    | Kimi K3.1 Pro | $2.00 | $10.00 | $0.20 | $2.00 | **$60** |
    | Kimi K3 | $3.00 | $15.00 | $0.30 | $3.00 | **$60** |
    | Kimi K2.7 Code | $0.95 | $4.00 | $0.19 | - | **$180** |
    | LongCat-2.0 | $0.30 | $1.20 | $0.006 | - | **$240** |
    | Step 5 Preview | $1.00 | $2.70 | $0.10 | - | **$60** |
    | Beam Free | 免费 | 免费 | 免费 | - | **无限**<br /><small>限时</small> |
    | Iceman Contributor Free | 免费 | 免费 | 免费 | - | **无限**<br /><small>限时</small> |
    | LongCat 2.5 Free | 免费 | 免费 | 免费 | - | **无限**<br /><small>限时</small> |
    | MiMo-V2.6-Flash | $0.14 | $0.28 | $0.0028 | - | **$120** |
    | MiMo-V2.6-Pro | $0.435 | $0.87 | $0.003625 | - | **$60** |
    | MiMo-V2.5 | $0.14 | $0.28 | $0.0028 | - | **$120** |
    | MiMo-V2.5-Pro | $0.435 | $0.87 | $0.003625 | - | **$60** |
    | MiniMax M3.1 Flash | $0.15 | $0.60 | $0.015 | - | **$80** |
    | MiniMax M3（≤ 512K tokens） | $0.30 | $1.20 | $0.06 | - | **$180** |
    | MiniMax M3（> 512K tokens） | $0.60 | $2.40 | $0.12 | - | **$180** |
    | Muse Spark 1.3 Contributor | $0.10 | $0.20 | $0.002 | - | **$120** |
    | Muse Spark 1.2 Contributor | $0.10 | $0.20 | $0.002 | - | **$120** |
    | Qwen3.8 Max | $2.00 | $6.00 | $0.25 | $2.50 | **$60** |
    | Qwen3.8 Flash | $0.15 | $0.47 | $0.016 | $0.20 | **$90** |
    | Qwen3.7 Plus（≤ 256K tokens） | $0.40 | $1.60 | $0.04 | $0.50 | **$180** |
    | Qwen3.7 Plus（> 256K tokens） | $1.20 | $4.80 | $0.12 | $1.50 | **$180** |
    | DeepSeek V4.1 Flash（闲时） | $0.15 | $0.60 | $0.003 | - | **$200** |
    | DeepSeek V4.1 Flash（忙时） | $0.30 | $1.20 | $0.006 | - | **$200** |
    | DeepSeek V4 Pro（闲时） | $0.66 | $1.98 | $0.022 | - | **$60** |
    | DeepSeek V4 Pro（忙时） | $1.32 | $3.96 | $0.044 | - | **$60** |
    | Hy4 | $0.834 | $2.501 | $0.042 | - | **$240** |
    | Hy4 preview | $0.834 | $2.501 | $0.042 | - | **$120** |
    | Hy3 | $0.14 | $0.58 | $0.035 | - | **$240** |
    | Grok 4.7（≤ 200K tokens） | $2.00 | $6.00 | $0.50 | - | **$60** |
    | Grok 4.7（> 200K tokens） | $4.00 | $12.00 | $1.00 | - | **$60** |
    | GPT 6 Luna（≤ 272K tokens） | $0.10 | $0.50 | $0.01 | $0.125 | **$60** |
    | GPT 6 Luna（> 272K tokens） | $0.20 | $0.75 | $0.02 | $0.25 | **$60** |
    | GPT 5.6 Luna（≤ 272K tokens） | $0.20 | $1.20 | $0.02 | $0.25 | **$60** |
    | GPT 5.6 Luna（> 272K tokens） | $0.40 | $1.80 | $0.04 | $0.50 | **$60** |
    | Claude Haiku 5.5（≤ 100K tokens） | $0.10 | $0.50 | $0.01 | $0.125 | **$60** |
    | Claude Haiku 5.5（> 100K tokens） | $0.50 | $2.50 | $0.05 | $0.625 | **$60** |
    | Gemini 4 Argon（五折） | ~~$4.00~~ $2.00 | ~~$20.00~~ $10.00 | ~~$0.20~~ $0.10 | - | **$120** |

  </div>
  <div slot="go-teams">

    | 模型 | 输入 | 输出 | 缓存读取 | 缓存写入 | 每月上限 |
    | -------------------------------- | --------------- | ----------------- | --------------- | ------------ | ---------------------------------------------- |
    | GLM-5.3-Flash | $0.15 | $0.50 | $0.03 | - | **$65** |
    | GLM-5.3 | $1.40 | $4.40 | $0.26 | - | **$20** |
    | GLM-5.2 | $1.40 | $4.40 | $0.26 | - | **$65** |
    | Kimi K3.1 Pro | $2.00 | $10.00 | $0.20 | $2.00 | **$20** |
    | Kimi K3 | $3.00 | $15.00 | $0.30 | $3.00 | **$20** |
    | Kimi K2.7 Code | $0.95 | $4.00 | $0.19 | - | **$65** |
    | LongCat-2.0 | $0.30 | $1.20 | $0.006 | - | **$65** |
    | Step 5 Preview | $1.00 | $2.70 | $0.10 | - | **$20** |
    | Beam Free | 免费 | 免费 | 免费 | - | **无限**<br /><small>限时</small> |
    | Iceman Contributor Free | 免费 | 免费 | 免费 | - | **无限**<br /><small>限时</small> |
    | LongCat 2.5 Free | 免费 | 免费 | 免费 | - | **无限**<br /><small>限时</small> |
    | MiMo-V2.6-Flash | $0.14 | $0.28 | $0.0028 | - | **$65** |
    | MiMo-V2.6-Pro | $0.435 | $0.87 | $0.003625 | - | **$20** |
    | MiMo-V2.5 | $0.14 | $0.28 | $0.0028 | - | **$65** |
    | MiMo-V2.5-Pro | $0.435 | $0.87 | $0.003625 | - | **$20** |
    | MiniMax M3.1 Flash | $0.15 | $0.60 | $0.015 | - | **$25** |
    | MiniMax M3（≤ 512K tokens） | $0.30 | $1.20 | $0.06 | - | **$65** |
    | MiniMax M3（> 512K tokens） | $0.60 | $2.40 | $0.12 | - | **$65** |
    | Muse Spark 1.3 Contributor | $0.10 | $0.20 | $0.002 | - | **$65** |
    | Muse Spark 1.2 Contributor | $0.10 | $0.20 | $0.002 | - | **$65** |
    | Qwen3.8 Max | $2.00 | $6.00 | $0.25 | $2.50 | **$20** |
    | Qwen3.8 Flash | $0.15 | $0.47 | $0.016 | $0.20 | **$35** |
    | Qwen3.7 Plus（≤ 256K tokens） | $0.40 | $1.60 | $0.04 | $0.50 | **$65** |
    | Qwen3.7 Plus（> 256K tokens） | $1.20 | $4.80 | $0.12 | $1.50 | **$65** |
    | DeepSeek V4.1 Flash（闲时） | $0.15 | $0.60 | $0.003 | - | **$105** |
    | DeepSeek V4.1 Flash（忙时） | $0.30 | $1.20 | $0.006 | - | **$105** |
    | DeepSeek V4 Pro（闲时） | $0.66 | $1.98 | $0.022 | - | **$20** |
    | DeepSeek V4 Pro（忙时） | $1.32 | $3.96 | $0.044 | - | **$20** |
    | Hy4 | $0.834 | $2.501 | $0.042 | - | **$65** |
    | Hy4 preview | $0.834 | $2.501 | $0.042 | - | **$35** |
    | Hy3 | $0.14 | $0.58 | $0.035 | - | **$65** |
    | Grok 4.7（≤ 200K tokens） | $2.00 | $6.00 | $0.50 | - | **$20** |
    | Grok 4.7（> 200K tokens） | $4.00 | $12.00 | $1.00 | - | **$20** |
    | GPT 6 Luna（≤ 272K tokens） | $0.10 | $0.50 | $0.01 | $0.125 | **$20** |
    | GPT 6 Luna（> 272K tokens） | $0.20 | $0.75 | $0.02 | $0.25 | **$20** |
    | GPT 5.6 Luna（≤ 272K tokens） | $0.20 | $1.20 | $0.02 | $0.25 | **$20** |
    | GPT 5.6 Luna（> 272K tokens） | $0.40 | $1.80 | $0.04 | $0.50 | **$20** |
    | Claude Haiku 5.5（≤ 100K tokens） | $0.10 | $0.50 | $0.01 | $0.125 | **$20** |
    | Claude Haiku 5.5（> 100K tokens） | $0.50 | $2.50 | $0.05 | $0.625 | **$20** |
    | Gemini 4 Argon（五折） | ~~$4.00~~ $2.00 | ~~$20.00~~ $10.00 | ~~$0.20~~ $0.10 | - | **$35** |

  </div>
</PlanTabs>

**Beam Free：** 限时免费。不适用于安哥拉、白俄罗斯、柬埔寨、中国（包括香港和澳门）、古巴、刚果民主共和国、赤道几内亚、伊朗、伊拉克、老挝、利比亚、尼日利亚、朝鲜、俄罗斯、叙利亚、土库曼斯坦、乌兹别克斯坦、委内瑞拉，以及乌克兰的克里米亚、顿涅茨克和卢甘斯克地区。

**Iceman Contributor Free：** 限时免费。

**LongCat 2.5 Free：** 限时免费。

**Gemini 4 Argon：** 五折优惠持续到 2026 年 11 月 30 日。

**DeepSeek V4.1 Flash / V4 Pro：** 忙时为 UTC 时间周一至周五的 01:00-04:00 和 06:00-10:00；其余时间（包括周末）为闲时。[了解更多](https://api-docs.deepseek.com/quick_start/pricing/)。

### 预估请求数

下表基于典型的 Go 使用模式估算请求数。Go Plus 和 Go Teams 的估算值会随每个模型更高的用量上限等比放大。

<PlanTabs id="go-requests" label="Go plan" syncKey="go-plan">
  <div slot="go">

    | 模型 | 每 5 小时请求数 | 每周请求数 | 每月请求数 |
    | -------------------------- | -------------------- | ----------------- | ------------------ |
    | GLM-5.3-Flash | 6,320 | 15,790 | 31,580 |
    | GLM-5.3 | 220 | 540 | 1,080 |
    | GLM-5.2 | 880 | 2,150 | 4,300 |
    | Kimi K3.1 Pro | 147 | 368 | 735 |
    | Kimi K3 | 110 | 250 | 490 |
    | Kimi K2.7 Code | 1,350 | 3,380 | 6,750 |
    | LongCat-2.0 | 11,400 | 28,600 | 57,200 |
    | Step 5 Preview | 430 | 1,070 | 2,130 |
    | Beam Free | 无限 | 无限 | 无限 |
    | Iceman Contributor Free | 无限 | 无限 | 无限 |
    | LongCat 2.5 Free | 无限 | 无限 | 无限 |
    | MiMo-V2.6-Flash | 30,100 | 75,200 | 150,400 |
    | MiMo-V2.6-Pro | 3,250 | 8,150 | 16,300 |
    | MiMo-V2.5 | 30,100 | 75,200 | 150,400 |
    | MiMo-V2.5-Pro | 3,250 | 8,150 | 16,300 |
    | MiniMax M3.1 Flash | 3,880 | 9,690 | 19,380 |
    | MiniMax M3 | 3,200 | 8,000 | 16,000 |
    | Muse Spark 1.3 Contributor | 45,300 | 113,300 | 226,600 |
    | Muse Spark 1.2 Contributor | 45,300 | 113,300 | 226,600 |
    | Qwen3.8 Max | 160 | 400 | 810 |
    | Qwen3.8 Flash | 5,400 | 13,500 | 27,000 |
    | Qwen3.7 Plus | 4,300 | 10,800 | 21,600 |
    | DeepSeek V4.1 Flash | 43,330 | 108,330 | 216,670 |
    | DeepSeek V4 Pro | 1,050 | 2,600 | 5,200 |
    | Hy4 | 2,710 | 6,770 | 13,500 |
    | Hy4 preview | 1,350 | 3,380 | 6,770 |
    | Hy3 | 4,300 | 10,750 | 21,500 |
    | Grok 4.7 | 169 | 423 | 845 |
    | GPT 6 Luna | 4,230 | 10,560 | 21,130 |
    | GPT 5.6 Luna | 2,050 | 5,100 | 10,250 |
    | Claude Haiku 5.5 | 3,850 | 9,620 | 19,230 |
    | Gemini 4 Argon | 440 | 1,080 | 2,120 |

  </div>
  <div slot="go-plus">

    | 模型 | 每 5 小时请求数 | 每周请求数 | 每月请求数 |
    | -------------------------- | -------------------- | ----------------- | ------------------ |
    | GLM-5.3-Flash | 18,960 | 47,370 | 94,740 |
    | GLM-5.3 | 1,760 | 4,320 | 8,640 |
    | GLM-5.2 | 2,640 | 6,450 | 12,900 |
    | Kimi K3.1 Pro | 588 | 1,471 | 2,941 |
    | Kimi K3 | 440 | 1,000 | 1,960 |
    | Kimi K2.7 Code | 4,050 | 10,140 | 20,250 |
    | LongCat-2.0 | 45,600 | 114,400 | 228,800 |
    | Step 5 Preview | 1,720 | 4,280 | 8,520 |
    | Beam Free | 无限 | 无限 | 无限 |
    | Iceman Contributor Free | 无限 | 无限 | 无限 |
    | LongCat 2.5 Free | 无限 | 无限 | 无限 |
    | MiMo-V2.6-Flash | 60,200 | 150,400 | 300,800 |
    | MiMo-V2.6-Pro | 13,000 | 32,600 | 65,200 |
    | MiMo-V2.5 | 60,200 | 150,400 | 300,800 |
    | MiMo-V2.5-Pro | 13,000 | 32,600 | 65,200 |
    | MiniMax M3.1 Flash | 15,500 | 38,760 | 77,520 |
    | MiniMax M3 | 9,600 | 24,000 | 48,000 |
    | Muse Spark 1.3 Contributor | 90,600 | 226,600 | 453,200 |
    | Muse Spark 1.2 Contributor | 90,600 | 226,600 | 453,200 |
    | Qwen3.8 Max | 640 | 1,600 | 3,240 |
    | Qwen3.8 Flash | 16,200 | 40,500 | 81,000 |
    | Qwen3.7 Plus | 12,900 | 32,400 | 64,800 |
    | DeepSeek V4.1 Flash | 86,670 | 216,670 | 433,330 |
    | DeepSeek V4 Pro | 4,200 | 10,400 | 20,800 |
    | Hy4 | 10,840 | 27,080 | 54,000 |
    | Hy4 preview | 5,400 | 13,520 | 27,080 |
    | Hy3 | 17,200 | 43,000 | 86,000 |
    | Grok 4.7 | 676 | 1,692 | 3,380 |
    | GPT 6 Luna | 16,920 | 42,240 | 84,520 |
    | GPT 5.6 Luna | 8,200 | 20,400 | 41,000 |
    | Claude Haiku 5.5 | 15,380 | 38,460 | 76,920 |
    | Gemini 4 Argon | 1,760 | 4,320 | 8,480 |

  </div>
  <div slot="go-teams">

    | 模型 | 每 5 小时请求数 | 每周请求数 | 每月请求数 |
    | -------------------------- | -------------------- | ----------------- | ------------------ |
    | GLM-5.3-Flash | 6,847 | 17,110 | 34,210 |
    | GLM-5.3 | 293 | 720 | 1,440 |
    | GLM-5.2 | 953 | 2,330 | 4,660 |
    | Kimi K3.1 Pro | 196 | 491 | 980 |
    | Kimi K3 | 147 | 333 | 653 |
    | Kimi K2.7 Code | 1,462 | 3,660 | 7,310 |
    | LongCat-2.0 | 12,350 | 30,980 | 61,970 |
    | Step 5 Preview | 573 | 1,430 | 2,840 |
    | Beam Free | 无限 | 无限 | 无限 |
    | Iceman Contributor Free | 无限 | 无限 | 无限 |
    | LongCat 2.5 Free | 无限 | 无限 | 无限 |
    | MiMo-V2.6-Flash | 32,608 | 81,470 | 162,930 |
    | MiMo-V2.6-Pro | 4,333 | 10,870 | 21,730 |
    | MiMo-V2.5 | 32,608 | 81,470 | 162,930 |
    | MiMo-V2.5-Pro | 4,333 | 10,870 | 21,730 |
    | MiniMax M3.1 Flash | 4,850 | 12,110 | 24,230 |
    | MiniMax M3 | 3,467 | 8,670 | 17,330 |
    | Muse Spark 1.3 Contributor | 49,075 | 122,740 | 245,480 |
    | Muse Spark 1.2 Contributor | 49,075 | 122,740 | 245,480 |
    | Qwen3.8 Max | 213 | 530 | 1,080 |
    | Qwen3.8 Flash | 6,300 | 15,750 | 31,500 |
    | Qwen3.7 Plus | 4,658 | 11,700 | 23,400 |
    | DeepSeek V4.1 Flash | 45,500 | 113,750 | 227,500 |
    | DeepSeek V4 Pro | 1,400 | 3,470 | 6,930 |
    | Hy4 | 2,936 | 7,330 | 14,630 |
    | Hy4 preview | 1,575 | 3,940 | 7,900 |
    | Hy3 | 4,658 | 11,650 | 23,290 |
    | Grok 4.7 | 225 | 564 | 1,130 |
    | GPT 6 Luna | 5,640 | 14,080 | 28,170 |
    | GPT 5.6 Luna | 2,733 | 6,800 | 13,670 |
    | Claude Haiku 5.5 | 5,133 | 12,830 | 25,640 |
    | Gemini 4 Argon | 513 | 1,260 | 2,470 |

  </div>
</PlanTabs>

估算使用以下每次请求的 token 数；实际用量会有差异。

- Grok 4.7 — 每次请求 390 输入、32,500 缓存、120 输出 token
- GLM-5.3-Flash — 每次请求 1,000 输入、55,000 缓存、200 输出 token
- GLM-5.3/5.2 — 每次请求 700 输入、52,000 缓存、150 输出 token
- GPT 6 Luna — 每次请求 1,000 输入、50,000 缓存、220 输出 token
- GPT 5.6 Luna — 每次请求 1,000 输入、50,000 缓存、220 输出 token
- Claude Haiku 5.5 — 每次请求 1,100 输入、55,000 缓存、240 输出 token
- Kimi K3.1 Pro — 每次请求 1,050 输入、76,500 缓存、300 输出 token
- Kimi K3 — 每次请求 1,050 输入、76,500 缓存、300 输出 token
- Kimi K2.7 Code — 每次请求 870 输入、55,000 缓存、200 输出 token
- LongCat-2.0 — 每次请求 920 输入、88,900 缓存、200 输出 token
- Step 5 Preview — 每次请求 1,000 输入、55,000 缓存、200 输出 token
- DeepSeek V4.1 Flash — 每次请求 410 输入、71,300 缓存、310 输出 token
- DeepSeek V4 Pro — 每次请求 750 输入、82,000 缓存、290 输出 token
- MiniMax M3.1 Flash — 每次请求 500 输入、49,400 缓存、360 输出 token
- MiniMax M3 — 每次请求 510 输入、56,000 缓存、190 输出 token
- Muse Spark 1.3 Contributor — 每次请求 620 输入、71,400 缓存、300 输出 token
- Muse Spark 1.2 Contributor — 每次请求 620 输入、71,400 缓存、300 输出 token
- MiMo-V2.6-Flash — 每次请求 830 输入、71,500 缓存、295 输出 token
- MiMo-V2.6-Pro — 每次请求 790 输入、86,000 缓存、305 输出 token
- MiMo-V2.5 — 每次请求 830 输入、71,500 缓存、295 输出 token
- MiMo-V2.5-Pro — 每次请求 790 输入、86,000 缓存、305 输出 token
- Qwen3.8 Max — 每次请求 420 输入、66,000 缓存、200 输出 token
- Qwen3.8 Flash — 每次请求 600 输入、58,000 缓存、200 输出 token
- Qwen3.7 Plus — 每次请求 500 输入、57,000 缓存、190 输出 token
- Hy4 — 每次请求 830 输入、71,500 缓存、295 输出 token
- Hy4 preview — 每次请求 830 输入、71,500 缓存、295 输出 token
- Hy3 — 每次请求 830 输入、71,500 缓存、295 输出 token

你可以在[控制台](https://opencode.ai/console)中查看当前用量。

<Callout type="tip">如果达到用量限额，你可以继续使用免费模型。</Callout>

用量限额可能会随着我们从早期使用和反馈中学习而调整。

---

### 超出限额后的用量

如果你的 Console 余额中还有额度，可以在 **Go** 页面开启 **Extra Usage**。开启后，当你达到用量限额时，Go 会回退到你的[按量付费余额](../models/index.md#pricing)，而不是拦截请求。

Go Teams 默认开启 **Extra Usage**，你可以在 **Go** 页面将其关闭或重新开启。

### 为什么部分模型的用量较低

在 Go 中，不同模型包含的每月用量不同。

对大多数模型，我们通过批量折扣和预留 GPU 算力来实现这一点，然后把这些节省以更高的每月用量让利给你。

对部分模型，我们还没有机会谈到折扣或以更低成本托管，可能因为模型太新，也可能因为其公开定价本身已经是折扣价。

对于这些模型，你得到的用量仍然比直接向模型 provider 付费略多一些；这就是它们包含的每月用量较低的原因。

## 端点

你也可以通过以下 API 端点访问 Go 模型。每个模型都列出了其原生 API，但每个文本模型也可以通过其他 API 使用，由 Console 进行转换。完整列表请参阅 [Base URLs](../harnesses/index.md#base-urls)。

<div class="docs-table-scroll" role="region" aria-label="Go model endpoints" tabIndex={0}>

| 模型 | 模型 ID | 端点 | AI SDK 包 |
| -------------------------- | -------------------------- | ---------------------------------------------------------------------- | --------------------------- |
| Grok 4.7 | grok-4.7 | `https://opencode.ai/inference/go/openai/v1/responses` | `@ai-sdk/openai` |
| GPT 6 Luna | gpt-6-luna | `https://opencode.ai/inference/go/openai/v1/responses` | `@ai-sdk/openai` |
| GPT 5.6 Luna | gpt-5.6-luna | `https://opencode.ai/inference/go/openai/v1/responses` | `@ai-sdk/openai` |
| Claude Haiku 5.5 | claude-haiku-5-5 | `https://opencode.ai/inference/go/anthropic/v1/messages` | `@ai-sdk/anthropic` |
| Gemini 4 Argon | gemini-4-argon | `https://opencode.ai/inference/go/google/v1beta/models/gemini-4-argon` | `@ai-sdk/google` |
| GLM-5.3-Flash | glm-5.3-flash | `https://opencode.ai/inference/go/openai/v1/chat/completions` | `@ai-sdk/openai-compatible` |
| GLM-5.3 | glm-5.3 | `https://opencode.ai/inference/go/openai/v1/chat/completions` | `@ai-sdk/openai-compatible` |
| GLM-5.2 | glm-5.2 | `https://opencode.ai/inference/go/openai/v1/chat/completions` | `@ai-sdk/openai-compatible` |
| Kimi K3.1 Pro | kimi-k3.1-pro | `https://opencode.ai/inference/go/openai/v1/chat/completions` | `@ai-sdk/openai-compatible` |
| Kimi K3 | kimi-k3 | `https://opencode.ai/inference/go/openai/v1/chat/completions` | `@ai-sdk/openai-compatible` |
| Kimi K2.7 Code | kimi-k2.7-code | `https://opencode.ai/inference/go/openai/v1/chat/completions` | `@ai-sdk/openai-compatible` |
| LongCat-2.0 | longcat-2.0 | `https://opencode.ai/inference/go/openai/v1/chat/completions` | `@ai-sdk/openai-compatible` |
| DeepSeek V4.1 Flash | deepseek-v4.1-flash | `https://opencode.ai/inference/go/openai/v1/chat/completions` | `@ai-sdk/openai-compatible` |
| DeepSeek V4 Pro | deepseek-v4-pro | `https://opencode.ai/inference/go/openai/v1/chat/completions` | `@ai-sdk/openai-compatible` |
| MiMo-V2.6-Flash | mimo-v2.6-flash | `https://opencode.ai/inference/go/openai/v1/chat/completions` | `@ai-sdk/openai-compatible` |
| MiMo-V2.6-Pro | mimo-v2.6-pro | `https://opencode.ai/inference/go/openai/v1/chat/completions` | `@ai-sdk/openai-compatible` |
| MiMo-V2.5 | mimo-v2.5 | `https://opencode.ai/inference/go/openai/v1/chat/completions` | `@ai-sdk/openai-compatible` |
| MiMo-V2.5-Pro | mimo-v2.5-pro | `https://opencode.ai/inference/go/openai/v1/chat/completions` | `@ai-sdk/openai-compatible` |
| MiniMax M3.1 Flash | minimax-m3.1-flash | `https://opencode.ai/inference/go/openai/v1/chat/completions` | `@ai-sdk/openai-compatible` |
| MiniMax M3 | minimax-m3 | `https://opencode.ai/inference/go/anthropic/v1/messages` | `@ai-sdk/anthropic` |
| Muse Spark 1.3 Contributor | muse-spark-1.3-contributor | `https://opencode.ai/inference/go/openai/v1/responses` | `@ai-sdk/openai` |
| Muse Spark 1.2 Contributor | muse-spark-1.2-contributor | `https://opencode.ai/inference/go/openai/v1/responses` | `@ai-sdk/openai` |
| Qwen3.8 Max | qwen3.8-max | `https://opencode.ai/inference/go/anthropic/v1/messages` | `@ai-sdk/anthropic` |
| Qwen3.8 Flash | qwen3.8-flash | `https://opencode.ai/inference/go/anthropic/v1/messages` | `@ai-sdk/anthropic` |
| Qwen3.7 Plus | qwen3.7-plus | `https://opencode.ai/inference/go/anthropic/v1/messages` | `@ai-sdk/anthropic` |
| Hy4 | hy4 | `https://opencode.ai/inference/go/openai/v1/chat/completions` | `@ai-sdk/openai-compatible` |
| Hy4 preview | hy4-preview | `https://opencode.ai/inference/go/openai/v1/chat/completions` | `@ai-sdk/openai-compatible` |
| Hy3 | hy3 | `https://opencode.ai/inference/go/openai/v1/chat/completions` | `@ai-sdk/openai-compatible` |
| Step 5 Preview | step-5-preview | `https://opencode.ai/inference/go/openai/v1/chat/completions` | `@ai-sdk/openai-compatible` |
| Beam Free | beam-free | `https://opencode.ai/inference/go/openai/v1/chat/completions` | `@ai-sdk/openai-compatible` |
| Iceman Contributor Free | iceman-contributor-free | `https://opencode.ai/inference/go/openai/v1/chat/completions` | `@ai-sdk/openai-compatible` |
| LongCat 2.5 Free | longcat-2.5-free | `https://opencode.ai/inference/go/openai/v1/chat/completions` | `@ai-sdk/openai-compatible` |

</div>

这些 AI SDK 包适用于直接调用 Go 的应用程序。要在 OpenCode 中使用 Go，请用 `/connect` 连接，并使用 `opencode-go/<model-id>` 格式设置[模型](../../models/index.md)：

```jsonc title="opencode.jsonc"
{
  "$schema": "https://opencode.ai/config.json",
  "model": "opencode-go/kimi-k3",
}
```

### 模型列表

从模型端点获取可用模型及其元数据的完整列表：

```bash
curl https://opencode.ai/inference/go/v1/models
```

## 隐私

| 模型 | 模型训练 | 数据保留 |
| -------------------------- | -------------- | -------------- |
| Grok 4.7 | 不使用 | 30 天 |
| GPT 6 Luna | 不使用 | 30 天 |
| GPT 5.6 Luna | 不使用 | 30 天 |
| Claude Haiku 5.5 | 不使用 | 30 天 |
| Gemini 4 Argon | 不使用 | 0 天 |
| GLM-5.3-Flash | 不使用 | 0 天 |
| GLM-5.3 | 不使用 | 0 天 |
| GLM-5.2 | 不使用 | 0 天 |
| Kimi K3.1 Pro | 不使用 | 0 天 |
| Kimi K3 | 不使用 | 0 天 |
| Kimi K2.7 Code | 不使用 | 0 天 |
| LongCat-2.0 | 不使用 | 0 天 |
| MiMo-V2.6-Pro | 不使用 | 0 天 |
| MiMo-V2.6-Flash | 不使用 | 0 天 |
| MiMo-V2.5-Pro | 不使用 | 0 天 |
| MiMo-V2.5 | 不使用 | 0 天 |
| Qwen3.8 Max | 不使用 | 0 天 |
| Qwen3.8 Flash | 不使用 | 0 天 |
| Qwen3.7 Plus | 不使用 | 0 天 |
| MiniMax M3.1 Flash | 不使用 | 0 天 |
| MiniMax M3 | 不使用 | 0 天 |
| Muse Spark 1.3 Contributor | 是 | 非 ZDR |
| Muse Spark 1.2 Contributor | 是 | 非 ZDR |
| DeepSeek V4.1 Flash | 不使用 | 0 天\* |
| DeepSeek V4 Pro | 不使用 | 0 天\* |
| Hy4 | 不使用 | 0 天 |
| Hy4 preview | 不使用 | 0 天 |
| Hy3 | 不使用 | 0 天 |
| Step 5 Preview | 不使用 | 0 天 |
| Beam Free | 不使用 | 30 天 |
| Iceman Contributor Free | 是 | 非 ZDR |
| LongCat 2.5 Free | 不使用 | 0 天 |

- **Grok 4.7：** ZDR 会禁用依赖已存储数据的重要 API 功能，包括有状态的 Responses API、Files 与 Collections，以及 Batch API。[了解更多](https://docs.x.ai/developers/faq/security#what-is-zero-data-retention-zdr)。
- **GPT 6 Luna / GPT 5.6 Luna：** 所有 API 功能使用都会生成滥用监测日志，最长保留 30 天。[了解更多](https://developers.openai.com/api/docs/guides/your-data#data-retention-controls-for-abuse-monitoring)。
- **Claude Haiku 5.5：** 依据 [Anthropic 的数据政策](https://docs.anthropic.com/en/docs/claude-code/data-usage)，请求会保留 30 天。
- **Muse Spark 1.3 Contributor：** 以大幅折扣的 token 价格换取使用你的提示词和补全来训练未来 Meta 模型的许可。可用范围仅限于 Meta 的[地理使用政策](https://ai.developer.meta.com/legal/geographic-use-policy)允许的地区。[了解更多](https://dev.meta.ai/docs/pricing-rate-limits#contributor-tier)。
- **Muse Spark 1.2 Contributor：** 以大幅折扣的 token 价格换取使用你的提示词和补全来训练未来 Meta 模型的许可。可用范围仅限于 Meta 的[地理使用政策](https://ai.developer.meta.com/legal/geographic-use-policy)允许的地区。[了解更多](https://dev.meta.ai/docs/pricing-rate-limits#contributor-tier)。
- **Iceman Contributor Free：** 限时免费，以换取使用你的提示词和补全来改进模型的许可。
- **LongCat 2.5 Free：** 托管在中国。需要你的工作区隐私设置中允许**全球**地区。
- **DeepSeek：** ZDR 协议每月续签。当前协议有效期至 2026 年 11 月 30 日。

## 背景

开放模型已经变得非常强。在编码任务上，它们的性能已接近专有模型。由于许多 provider 都能以有竞争力的方式提供它们，它们通常便宜得多。

然而，获得对它们的可靠、低延迟访问可能很难。不同 provider 的质量和可用性参差不齐。

<Callout type="tip">我们测试了一小组与 OpenCode 配合良好的模型和 provider。</Callout>

为了解决这个问题，我们做了几件事：

1. 我们测试了一批精选的开放模型，并与它们的团队讨论如何以最佳方式运行它们。
2. 我们与几家 provider 合作，确保这些模型被正确地提供。
3. 我们对"模型 + provider"的组合进行了基准测试，得出了我们愿意推荐的列表。

Go、Go Plus 和 Go Teams 都提供对这些模型的访问；请根据使用量选择合适的方案，或选择 Go Teams 覆盖整个团队。

## 目标

我们创建 OpenCode Go 是为了：

1. 以低成本的订阅让更多人**用得起** AI 编码。
2. 为最好的开放编码模型提供**可靠**的访问。
3. 精选经过**测试和基准验证**、适合编码 agent 使用的模型。
4. **不锁定**，允许你在 OpenCode 中继续使用任何其他 provider。
