# AGENTS.md

任务：**给域名 → 找线上开发文档 → 翻译成本地文档。** 本文只管四件事：清洗、保存、版本号、维护列表。

**不审校**：译文写完直接落盘，不做二次审校、回读校对、润色轮次，也不留审校环节给别人。只要格式符合 §1、§2 就直接写文件——文字质量靠一次译到位，不再回头改。

---

## 1. 清洗数据

抓下来是整页 HTML，先剔壳再翻译。

**去掉**：导航栏、侧栏、页脚、面包屑、页内 TOC、评论区、cookie 提示、推广位、"上一页/下一页"、"编辑此页"、"本页是否有帮助"。

**保留**（顺序不变）：`h1–h4`、段落、列表、表格、代码块（含语言标记）、行内代码、引用块、提示块（`:::note`、`> **Note**`、`<Callout>`）、图片（含 alt）、链接。

主内容选择器按序试，取第一个非空的：`main article` → `.theme-doc-markdown` → `.md-content` → `.markdown-body` → `#content` → `article` → `main`。

**代码块原样保留，一个字符都不改**（含缩进、注释、空行）——这是译文正确性的底线。

原文本身就是 Markdown 的（`llms.txt`、ReadTheDocs 的 `_sources/*.rst.txt`、MkDocs 的 `search_index.json`），直接用，不做 HTML 反向转换。

清洗结果缓存到 `.cache/<host>/<slug>.html`，重跑命中缓存，不重复抓。

---

## 2. 如何保存

```
INDEX.md                  ← 维护列表，见 §4
docs/<host>/<version>/
  index.md              ← /
  guide/install.md      ← /guide/install
  api/index.md          ← /api/
  _manifest.json
```

**目录与文件名**

- `<host>`：小写域名，去 `www.`；带端口把 `:` 换成 `_` → `localhost_3000`。
- 路径镜像线上 path，丢掉 `query`、`fragment`；有 `<link rel="canonical">` 以它为准（去重 `?lang=`）。
- **尾斜杠 → `<段名>/index.md`；没有尾斜杠 → `<段名>.md`**。根路径 → `index.md`。
- 统一小写（Windows 大小写不敏感，避免撞名）；空格转 `-`，`<>:"|?*` 转 `_`；段名超 80 字符截断 + 8 位 hash。

**每页 frontmatter（必填）**

```yaml
---
source_url: https://docs.example.com/guide/install
source_hash: sha256:9f2c...
translated_at: 2026-11-13T09:35:00+08:00
---
```

正文第一行是 `# 译后标题`。

**链接**

- 指向已抓取的页面 → 相对 `.md`（`./install.md`、`../api/index.md`）
- 指向未抓取的站内页 → 保留原绝对 URL
- 站外链接、图片 URL → 原样不动

**清单**：`_manifest.json` 一页一条，记 `url` / `local_path` / `status` / `source_hash`。没有清单就无法判断哪些页变了，别只靠目录树。

---

## 3. 版本号

两个版本都要落进路径或字段，否则增量更新没法判断。

**文档版本（线上）**：路径含 `/v1.2/`、`/v2/`、`/latest/` 时，它作为 `<version>` 一级目录：

```
docs/docs.example.com/v1.2/guide/install.md
docs/docs.example.com/unversioned/guide/install.md   ← 站点无版本时
```

只翻**一个**版本（默认 `latest` 或最新稳定版），在 `_manifest.json` 的 `doc_version` 写明，避免同一内容存多份。

**译文版本（本地）**：frontmatter 里 `translation_version: 1`，单调递增不跳号。原文 `source_hash` 变了才 +1 重新翻译；没变绝不覆盖已有译文。

`_manifest.json` 顶层记：

```json
{
  "host": "docs.example.com",
  "doc_version": "v1.2",
  "translation_version": 3,
  "updated_at": "2026-11-13T09:35:00+08:00",
  "counts": { "total": 42, "translated": 40, "failed": 2 }
}
```

同一路径只保留最新译文，历史版本交给 git，不在目录里堆 `v1/ v2/ v3/` 副本。

---

## 4. 维护列表 `INDEX.md`

根目录 `INDEX.md` 的表格是"这份文档什么时候翻的、哪个版本、要不要更新"的唯一入口。**每次任务开始先读它挑活，结束必须回填。** 一行 = 一个 `<host>/<version>`。

```markdown
| 站点 | 文档版本 | 译文版本 | 生成时间 | 最近检查 | 页数 | 状态 | 入口 |
|---|---|---|---|---|---|---|---|
| docs.example.com | v1.2 | 3 | 2026-11-13T09:35+08:00 | 2026-11-20T10:00+08:00 | 42 | 已同步 | docs/docs.example.com/v1.2/index.md |
| api.example.com | unversioned | 1 | 2026-11-01T14:20+08:00 | 2026-11-01T14:20+08:00 | 18 | 待更新 | docs/api.example.com/unversioned/index.md |
```

- **生成时间**：本轮译文落盘时间，只在真正写入译文时改。
- **最近检查**：最后一次回访原站的时间，没重新抓就沿用旧值。
- **译文版本**：与 frontmatter / `_manifest.json` 的 `translation_version` 必须一致，对不上以 `INDEX.md` 为准并修正另两处。
- **状态**：`已同步` / `待更新` / `部分失败`。

规则：

- 时间一律 ISO 8601 带时区（`2026-11-13T09:35+08:00`），不写"11月13日"，否则排不了序。
- 只增改，不删行；某站点下线时把状态改成 `已下线`。历史差异看 git。
- 判定 `待更新`：距 `最近检查` 超过 30 天，或 sitemap `lastmod` 晚于 `生成时间`，或重抓后 `source_hash` 有变化。
- 同一站点多版本各占一行，不要合并。

**更新一个站点的流程**

1. 读 `INDEX.md`，挑状态为 `待更新` 的行。
2. 重取清单（`llms.txt` / `sitemap.xml`），比对页数与 URL 增减。
3. 逐页抓取比对 `source_hash`：变了才重译，没变的跳过（不覆盖已有译文）。
4. 更新该站 `_manifest.json`（页数、`translation_version`、`updated_at`）。
5. 回填 `INDEX.md` 对应行：`译文版本 +1`、`生成时间`、`最近检查`、`页数`、`状态`。
