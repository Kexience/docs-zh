# docs-zh

第三方开发文档的中文译文仓库。抓取线上文档 → 清洗 → 翻译 → 归档，每个站点按 `host/version` 独立存放，页面的原文地址与内容哈希写在 frontmatter 里，便于判断哪些页需要重新翻译。

## 目录结构

```
INDEX.md                     维护列表：每个站点/版本一行（译文版本、生成时间、页数、状态）
docs/<host>/<version>/
  index.md                   站点入口（对应 / 或 llms.txt）
  <path>.md                  镜像线上路径，如 docs/guide/install.md ← /guide/install
  _manifest.json             页面清单：url / local_path / status / source_hash
tools/                       抓取、切分、拼装、校验脚本
```

每页 frontmatter：

```yaml
---
source_url: https://docs.example.com/guide/install
source_hash: sha256:9f2c...
translated_at: 2026-11-13T09:35:00+08:00
translation_version: 1
---
```

## 当前收录

| 站点 | 文档版本 | 页数 | 状态 |
|---|---|---|---|
| [java.testcontainers.org](docs/java.testcontainers.org/unversioned/README.md) | unversioned（上游 2.0.5） | 102 | 已同步 |
| [openspec.dev](docs/openspec.dev/unversioned/index.md) | unversioned（上游 2.0） | 21 | 已同步 |

完整列表见 [INDEX.md](INDEX.md)。

## 约定

- 只翻译一个版本（默认 `latest` 或最新稳定版），同一内容不重复存多份。
- `source_hash` 变化才重新翻译并递增 `translation_version`；未变化不覆盖已有译文。
- 代码块与原文逐字节一致；站内链接改写为相对 `.md`，站外链接原样保留。
- 抓取缓存与流水线中间产物（`.cache/`、`.work/`）不入库。
