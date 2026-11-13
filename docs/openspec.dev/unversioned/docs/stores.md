---
source_url: https://openspec.dev/docs/stores
source_hash: sha256:372b7ce0044778e483449a353260aba0a916b834e07e36e1724ae0cc5079e12a
translated_at: 2026-11-13T09:48:42+08:00
translation_version: 1
---

# 存储库（beta）

OpenSpec 通常位于一个仓库内：一个 `openspec/` 文件夹，紧邻它所规划的代码。存储库把该文件夹移入它自己的仓库，多个代码仓库可以共享它。

在每台机器上完成一次性设置后，`status`、`new change` 和 `archive` 等命令可以在任何目录下作用于该存储库。

```
         team-plans  (a store: OpenSpec in its own repo)
         ├── .openspec-store/store.yaml   the store's name
         └── openspec/
             ├── specs/
             └── changes/
                   ▲
                   │ set up once on each machine,
                   │ shared by pushing and cloning like any repo
     ┌─────────────┼─────────────┐
     │             │             │
 web-app       api-server     mobile-app
(code repo)   (code repo)    (code repo)
```

你通过 git 共享存储库，方式与共享代码相同：自己提交、推送、拉取和评审。规格和变更与代码一样拥有分支和拉取请求。

## 何时需要存储库 [#when-you-need-one]

使用存储库的两个常见原因：

- **前端和后端在不同仓库**：一个功能同时涉及两者，而规划需要一个统一的归属处，而不是分成两半。

  ```
        shop-plans  (store)
        └── openspec/changes/add-discounts/    one plan for the feature
                  ▲
        ┌─────────┴─────────┐
        │                   │
    storefront             api
  (frontend repo)     (backend repo)
  ```

- **一个产品，多个客户端仓库**：Android、iOS 和 web 各自从自己的仓库发布，但共享同一套预期行为。规格描述行为而非实现，因此一份规格即可服务这三者。

  ```
          product-specs  (store)
          └── openspec/specs/checkout/spec.md    the expected behavior
                    ▲
      ┌─────────────┼─────────────┐
      │             │             │
  android-app    ios-app       web-app
  (code repo)   (code repo)   (code repo)
  ```

你可以有不止一个存储库，但建议保持数量少一些。

## 设置存储库 [#set-up-a-store]

一个人创建存储库，然后其他人加入。

1. **创建存储库**（一人操作，每个团队一次）。运行 `openspec store setup` 并回答提示：

   ```bash
   # run from anywhere; it asks what to create and where
   openspec store setup
   ```
   
   它会问三个问题：
   
   - **存储库名称**：`team-plans`
   - **该存储库应放在哪里？** 预填 `~/openspec/<name>`，按 Enter 接受，或输入其他路径
   - **创建该存储库吗？** 会显示即将创建的内容，回答 `Yes`
   
   然后它会报告创建了什么：
   
   ```yaml
   Store ready: team-plans
   Location: ~/openspec/team-plans
   OpenSpec root: ready
   Registry: registered
   
   Next: run normal OpenSpec commands against this store, for example:
     openspec new change <change-id> --store team-plans
   Share this store by committing and pushing it like any Git repo.
   ```

2. **推送到你的 git 托管平台。**先在平台上创建一个空的 `team-plans` 仓库。setup 不会添加 git 远程，因此先把存储库连接到该仓库，再推送：

   ```bash
   # connect the store to the empty repo on your git host
   cd ~/openspec/team-plans
   git remote add origin git@github.com:acme/team-plans.git

   # publish it
   git push -u origin main
   ```
   
3. **加入存储库**（每位同事，每台机器一次）：
   
   ```bash
   # get the store onto your machine
   git clone git@github.com:acme/team-plans.git ~/openspec/team-plans
   
   # tell OpenSpec where it lives
   openspec store register ~/openspec/team-plans
   ```

   ```yaml
   Store registered: team-plans
   Location: /Users/you/openspec/team-plans
   OpenSpec root: ready
   Registry: registered
   ```
   
   注册会告诉你的机器该存储库在哪里。存储库的名称已经提交在它内部，位于 `.openspec-store/store.yaml`。setup 已注册创建者的副本，因此只有克隆得到的副本需要这一步。
   
4. **确认是否成功**，在任意目录下：
   
   ```bash
   # any OpenSpec command reaches the store by name
   openspec status --store team-plans
   ```

   ```yaml
   Using OpenSpec root: team-plans (/Users/you/openspec/team-plans)
   No active changes. Create one with: openspec new change <name> --store team-plans
   ```
   
## 设置类型 [#types-of-setups]

OpenSpec 有三种设置。本页余下内容使用这些名称：

- **repo-local**：OpenSpec 位于你的仓库内，不使用存储库。这是默认方式。
- **store-only**：你的仓库不保留自己的规格或变更。所有内容都在存储库中。
- **store-optional**：你的项目有自己的 `openspec/` 文件夹，并在你要求时访问存储库。

### 默认方式：OpenSpec 位于你的仓库内（`repo-local`） [#the-default-openspec-inside-your-repo-repo-local]

`openspec init` 会在你的代码旁放置一个 `openspec/` 文件夹，该仓库的规格和变更就放在那里。不涉及存储库。这是[设置你的项目](./setup.md)所教的设置，大多数项目永远不需要另一种。

```
web-app  (code repo)
└── openspec/
    ├── specs/
    └── changes/
```

### OpenSpec 在你的仓库之外，位于存储库中（`store-only`） [#openspec-outside-your-repo-in-a-store-store-only]

仓库不保留自己的规格或变更。它规划的一切都在存储库中，仓库配置中的一行把两者连接起来。

当一个团队构建所有仓库并在一处规划时，这很常见。[上文的示例](#when-you-need-one)都属于这种形态。

```
team-plans  (store)
└── openspec/
    ├── specs/       the repo's specs live here
    └── changes/     its changes too
          ▲
          │ store: team-plans   (the connecting line)
web-app  (code repo)
└── openspec/
    └── config.yaml    nothing else
```

### OpenSpec 既在你的仓库中，也在存储库中（`store-optional`） [#openspec-in-your-repo-and-in-a-store-store-optional]

仓库对自己的工作保持 repo-local，存储库则存放共享的规格和变更。在仓库内，OpenSpec 使用你项目的 `openspec/` 文件夹，只有传入 `--store` 时才访问存储库。

当一个仓库在存储库出现之前就在使用 OpenSpec，或一个基本独立的仓库只是偶尔涉及共享工作时，这很常见。

```
team-plans  (store)
└── openspec/          the shared specs and changes
          ▲
          │ only when you pass --store team-plans
web-app  (code repo)
└── openspec/          this repo's own
    ├── config.yaml
    ├── specs/
    └── changes/
```

仓库可以先以 repo-local 开始，之后再把它自己的规格和变更迁移到存储库。[把仓库的规格和变更迁移到存储库](#move-a-repos-specs-and-changes-into-the-store)说明了做法。

## 使用存储库时产物创建在哪里 [#where-artifacts-get-created-when-using-stores]

使用存储库时，OpenSpec 还必须决定产物创建在哪里。这取决于你的设置：

- **store-only**（你的项目只写入存储库）：每个产物都创建在存储库中。下面的 `store:` 行记录了这一点。
- **store-optional**（你的项目有自己的 `openspec/` 文件夹，同时也使用存储库）：产物创建在你的项目中，除非你在请求中指明存储库，或为该变更传入 `--store`。之后由你的智能体在整个工作流剩余部分携带该标志。

OpenSpec 把产物写入两个位置之一：你项目的 `openspec/` 文件夹，或存储库的对应文件夹。它按以下顺序选择，第一个适用的选项胜出：

1. **命令上的 `--store <id>`。** 永远胜出，任意目录下都适用。
2. **你项目的 `openspec/` 文件夹。** 如果你的项目有自己的 `specs/` 或 `changes/` 文件夹，OpenSpec 就用它们。
3. **你项目中的 `store:` 行。** 这是 store-only 项目记录其存储库的方式。
4. **你机器上的 `defaultStore`。** 以上都不适用时的回退。

如果这些都不适用，而你又注册过存储库，命令会失败并列出它们。当某个存储库的 id 与你的仓库在其 `origin` 远程中的名称匹配时，错误会指明该存储库以及选择它的 `store:` 行。OpenSpec 从不自行按名称挑选存储库，因为不同组织中的仓库可能重名。

当 OpenSpec 选定一个存储库时，它会在命令输出之前打印 `Using OpenSpec root: ...`。

### `store:` 行（store-only 项目） [#the-store-line-store-only-projects]

在你项目的 `openspec/config.yaml` 中添加一行：

```yaml
# web-app/openspec/config.yaml
store: team-plans
```

你或你的智能体在项目内运行的一切现在都使用该存储库，无需输入任何标志：

```bash
# inside web-app, connected
openspec status
```

```yaml
Using OpenSpec root: team-plans (/Users/you/openspec/team-plans)
No active changes. Create one with: openspec new change <name> --store team-plans
```

- **没有这一行**：在 store-only 项目中运行普通命令，OpenSpec 会报错并列出你注册的存储库。
- **提交它**：克隆你项目的同事也会得到这一行。他们仍需在自己的机器上注册该存储库（[设置存储库的第 3 步](#set-up-a-store)），否则 OpenSpec 会报错并提示他们注册。
- **与真实文件夹并存**：如果你的项目同时有 `specs/` 或 `changes/` 文件夹，OpenSpec 会使用它们并忽略该行，同时给出警告。

### 在 store-only 仓库中安装集成 [#install-integrations-in-a-store-only-repo]

在代码仓库根目录运行 init，即可安装 AI 工具集成文件，而无需把规划移回该仓库：

```bash
# inside web-app, at the repository root
openspec init --tools claude
```

- **集成文件**：写入代码仓库。
- **`openspec/config.yaml`**：逐字节保留，包括 `store:` 行。
- **`openspec/specs/` 和 `openspec/changes/`**：不在代码仓库中创建。

OpenSpec 拒绝在代码仓库的子目录中执行该命令。请在仓库根目录运行。

OpenSpec 在这里也会拒绝 `--language`，因为语言属于外部存储库的配置。请在存储库根目录运行 init，或直接编辑该配置。

### 你机器上的 `defaultStore` [#defaultstore-on-your-machine]

如果你参与的每个项目都使用同一个存储库，设置一次即可。当 OpenSpec 找不到标志、没有本地 `openspec/` 文件夹、也没有 `store:` 行时，会回退到它：

```bash
# use team-plans whenever nothing else names a store
openspec config set defaultStore team-plans

# undo it
openspec config unset defaultStore
```

**始终作用于本地的命令。** `init`、`update`、`templates`、`schemas` 以及 `openspec schema` 的子命令只作用于当前目录，不接受 `--store`。

## 把仓库的规格和变更迁移到存储库 [#move-a-repos-specs-and-changes-into-the-store]

要把仓库从 repo-local 变为 store-only：

1. 把仓库 `openspec/specs/` 和 `openspec/changes/` 中的所有内容迁移到存储库中的同名文件夹。
2. 删除已空的文件夹，使仓库的 `openspec/` 文件夹只保留 `config.yaml`。
3. 在该 `config.yaml` 中添加 `store:` 行。

此时在仓库内运行 `openspec status`，输出会以 `Using OpenSpec root: team-plans` 开头。

## 在存储库中工作 [#work-in-the-store]

无论对你还是对你的智能体，工作流都不变。提案、实施和归档照常运行。唯一的区别是产物创建在哪里，[上一节](#where-artifacts-get-created-when-using-stores)对此作了说明。

在 store-only 仓库内创建变更，它会落到存储库中：

```bash
# inside web-app; the store: line routes this to team-plans
openspec new change add-login
```

```yaml
Using OpenSpec root: team-plans (/Users/you/openspec/team-plans)
Created change 'add-login' at /Users/you/openspec/team-plans/openspec/changes/add-login/
Schema: spec-driven
Next: openspec status --change add-login --store team-plans
```

- **它去了哪里**：进入存储库本身的仓库，而不是你的代码旁边。
- **共享它**：在你提交并推送存储库本身的仓库之前，该变更只存在于你的检出中。同事拉取后才能看到。工作流写入的每个产物都是如此。
- **文档中的路径**：文档中凡出现 `openspec/` 路径的地方，在存储库设置中，该文件夹就是存储库的那个。

当产物创建在你没预料到的位置时，`openspec doctor` 会检查你的设置而不做任何改动，并为每个发现打印修复方法：

```bash
# check the current root and its stores
openspec doctor
```

```yaml
Doctor

Root
  Location: /Users/you/openspec/team-plans
  OpenSpec root: ok
  Store: team-plans (metadata ok)

References
  (none declared)
```

当你想要同样的整体情况但不想做检查时，`openspec context` 会列出当前目录所使用的根目录和存储库。

要在一个编辑器窗口中打开存储库和某个仓库，让你的智能体同时读取两者，见[工作集（beta）](./worksets.md)。

## 从另一个存储库读取规格 [#read-specs-from-another-store]

你的仓库可以保留自己的 `openspec/` 文件夹，同时让智能体读取另一个存储库的规格。在仓库的 `openspec/config.yaml` 中通过 `references:` 声明该存储库：

```yaml
# api-server/openspec/config.yaml
references:
  - team-plans
```

引用是只读的。你的工作仍留在你的仓库中，引用只改变告知智能体的内容。

当工作流创建产物时，其指令中会加入一份被引用存储库的规格索引，每条都有一行摘要和获取它的确切命令：

```xml
<referenced_stores>
<!-- Read-only upstream context. Fetch what you need; cite what you use. -->
Store team-plans (/Users/you/openspec/team-plans):
  - payments: Rules for charging and refunding customers.
  Fetch: openspec show <spec-id> --type spec --store team-plans
</referenced_stores>
```

引用也可以携带存储库的克隆 URL，供尚未拥有该存储库的机器使用：

```yaml
references:
  - team-plans
  - { id: design-system, remote: "git@github.com:acme/design-system.git" }
```

声明 URL 后，`openspec doctor` 会把缺失的存储库变成可直接粘贴的修复方法：

```yaml
# output wrapped to fit
References
  - team-plans: ok (/Users/you/openspec/team-plans)
  - design-system: Referenced store 'design-system' is not registered on this machine.
    Fix: git clone -- git@github.com:acme/design-system.git '/Users/you/openspec/design-system' &&
         openspec store register '/Users/you/openspec/design-system' --id design-system
```

## beta 限制 [#beta-limits]

- **形态可能变化**：命令名、标志和文件格式可能在不同版本之间变化。升级后请重读本页。
- **刻意不做同步**：OpenSpec 从不克隆、拉取或推送。过期检出会显示过期的规格，直到你拉取；引用也照磁盘上现有的内容读取。
- **每个存储库名称只能有一个检出**：在已注册的名称下注册第二个文件夹会失败，并提示先运行 `openspec store unregister`。
