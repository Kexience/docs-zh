#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Convert the cached java.testcontainers.org HTML into per-page Markdown.

The site is a MkDocs Material build. Each page's article is converted to
Markdown, then the fenced code blocks are protected the same way as the other
pipelines:

  .cache/java.testcontainers.org/pages/<safe>.md   the cleaned English page
  .work/prose/<safe>.md                            prose, code -> @@CODE_n@@
  .work/blocks/<safe>.json                         the fenced code blocks
  .work/index.json                                 manifest of pages

Code block language markers are recovered from the upstream Markdown
(testcontainers/testcontainers-java/docs/*.md), because the rendered HTML
drops them.
"""
import hashlib
import json
import os
import re
import sys
from urllib.parse import urljoin

from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = "java.testcontainers.org"
CACHE = os.path.join(ROOT, ".cache", HOST)
PAGES = os.path.join(CACHE, "pages")
RAW = os.path.join(CACHE, "raw")
GHFILES = os.path.join(CACHE, "ghfiles")
PROSE = os.path.join(ROOT, ".work", "prose")
BLOCKS = os.path.join(ROOT, ".work", "blocks")
LIMIT = 11000

CODEINCLUDE_BLOCK = re.compile(
    r"<!--\s*codeinclude\s*-->\s*\n(?P<body>.*?)<!--\s*/codeinclude\s*-->", re.S)
DIRECTIVE = re.compile(r"\[(?P<title>[^\]]*)\]\((?P<path>[^)]+)\)(?P<opts>[^\n]*)")
FENCE_RE = re.compile(r"^[ \t]*```(?P<lang>[^\n`]*)\n(?P<text>.*?)^[ \t]*```", re.M | re.S)

EXT_LANG = {
    ".java": "java", ".kt": "kotlin", ".kts": "kotlin", ".groovy": "groovy",
    ".xml": "xml", ".yaml": "yaml", ".yml": "yaml", ".json": "json",
    ".sh": "bash", ".bash": "bash", ".properties": "properties", ".sql": "sql",
    ".py": "python", ".js": "javascript", ".ts": "typescript", ".go": "go",
    ".rs": "rust", ".cs": "csharp", ".conf": "conf", ".toml": "toml",
    ".gradle": "groovy", ".txt": "text", ".dockerfile": "dockerfile",
    ".html": "html", ".css": "css", ".rb": "ruby", ".php": "php",
}

BLOCK_TAGS = {"p", "div", "pre", "table", "blockquote", "ul", "ol", "h1", "h2",
              "h3", "h4", "h5", "h6", "hr", "figure", "dl", "section", "article"}


def safe_name(slug):
    return slug.replace("/", "__") if slug else "__root__"


def norm_ws(text):
    return re.sub(r"\s+", " ", text).strip()


def dedent(text):
    """Remove the common leading indentation of a block of text."""
    lines = text.split("\n")
    indents = [len(l) - len(l.lstrip()) for l in lines if l.strip()]
    if not indents:
        return text
    n = min(indents)
    return "\n".join(l[n:] if l.strip() else "" for l in lines)


def norm_code(text):
    """Normalise code text for comparison only (not for output)."""
    lines = [l.rstrip() for l in dedent(text.replace("\r\n", "\n")).split("\n")]
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines)


def fence(text, lang=""):
    body = text.replace("\r\n", "\n").rstrip("\n")
    mark = "````" if "```" in body else "```"
    return "%s%s\n%s\n%s" % (mark, lang or "", body, mark)


class Page:
    """Renders one MkDocs article as Markdown."""

    def __init__(self, slug, url, html, langs=None):
        self.slug = slug
        self.url = url
        self.path = urlparse_path(url)
        self.langs = list(langs or [])
        self.lang_i = 0
        self.soup = BeautifulSoup(html, "html.parser")

    # -- helpers ---------------------------------------------------------
    def abs(self, href):
        if not href:
            return ""
        href = href.strip()
        if href.startswith(("http://", "https://", "mailto:", "#", "data:")):
            return href
        return urljoin("https://%s%s" % (HOST, self.path), href)

    def next_lang(self):
        if self.lang_i < len(self.langs):
            lang = self.langs[self.lang_i]
            self.lang_i += 1
            return lang or ""
        self.lang_i += 1
        return ""

    # -- inline ----------------------------------------------------------
    def inline(self, node):
        if isinstance(node, NavigableString):
            return re.sub(r"\s+", " ", str(node))
        if not isinstance(node, Tag):
            return ""
        name = node.name
        cls = node.get("class") or []
        if name in ("svg", "path", "g", "input", "button"):
            return ""
        if name == "code":
            t = node.get_text()
            if "`" in t:
                return "``%s``" % t
            return "`%s`" % t
        if name in ("strong", "b"):
            return "**%s**" % self.inline_children(node)
        if name in ("em", "i"):
            return "*%s*" % self.inline_children(node)
        if name == "a":
            if "headerlink" in cls:
                return ""
            href = self.abs(node.get("href"))
            text = self.inline_children(node)
            if not text.strip():
                return ""
            if not href:
                return text
            return "[%s](%s)" % (text, href)
        if name == "img":
            return "![%s](%s)" % (node.get("alt") or "", self.abs(node.get("src") or ""))
        if name == "br":
            return "\n"
        if name in ("del", "s"):
            return "~~%s~~" % self.inline_children(node)
        return self.inline_children(node)

    def inline_children(self, node):
        out = []
        for child in node.children:
            out.append(self.inline(child))
        return "".join(out)

    # -- blocks ----------------------------------------------------------
    def blocks(self, parent):
        out = []
        for child in parent.children:
            if isinstance(child, NavigableString):
                t = norm_ws(str(child))
                if t:
                    out.append(t)
                continue
            if not isinstance(child, Tag):
                continue
            md = self.block(child)
            if md and md.strip():
                out.append(md.strip("\n"))
        return "\n\n".join(out)

    def block(self, tag):
        name = tag.name
        cls = tag.get("class") or []

        if name in ("h1", "h2", "h3", "h4", "h5", "h6"):
            level = int(name[1])
            text = self.inline_children(tag).strip()
            if not text:
                return ""
            return "%s %s" % ("#" * level, text)
        if name == "p":
            return self.mixed(tag)
        if name == "hr":
            return "---"
        if name == "pre":
            return self.code_of(tag)
        if name == "table":
            return self.table(tag)
        if name == "blockquote":
            body = self.blocks(tag)
            return quote(body)
        if name in ("ul", "ol"):
            return self.list(tag, name == "ol")
        if name in ("dl",):
            return self.blocks(tag)
        if name == "div":
            if "highlight" in cls or "codehilite" in cls:
                return self.code_of(tag)
            if "admonition" in cls:
                return self.admonition(tag)
            if "tabbed-set" in cls:
                return self.tabbed(tag)
            if "highlight" in cls:
                return self.code_of(tag)
            return self.blocks(tag)
        if name in ("figure", "section", "article", "details", "summary", "dl", "fieldset"):
            return self.blocks(tag)
        if name in ("span", "code", "a", "em", "strong", "b", "i", "sup", "sub",
                    "small", "abbr", "label", "kbd", "q", "cite", "u", "var",
                    "time", "dd", "dt", "figcaption", "font", "mark", "del", "s"):
            return self.inline(tag)
        return self.blocks(tag)

    def mixed(self, tag):
        """A <p> may hold block-level children (Python-Markdown leaves the
        codehilite <div> inside the paragraph)."""
        parts, buf = [], []
        for child in tag.children:
            if isinstance(child, NavigableString):
                buf.append(self.inline(child))
                continue
            if isinstance(child, Tag) and child.name in BLOCK_TAGS:
                text = "".join(buf).strip()
                buf = []
                if text:
                    parts.append(text)
                md = self.block(child)
                if md.strip():
                    parts.append(md.strip("\n"))
                continue
            buf.append(self.inline(child))
        text = "".join(buf).strip()
        if text:
            parts.append(text)
        return "\n\n".join(parts)

    def code_of(self, tag):
        code = tag.find("code")
        pre = tag.find("pre")
        node = code if code is not None else pre
        text = node.get_text() if node is not None else ""
        return fence(text, self.next_lang())

    def admonition(self, tag):
        title = ""
        t = tag.select_one(".admonition-title")
        if t is not None:
            title = norm_ws(t.get_text())
            t.extract()
        body = self.blocks(tag)
        quoted, loose = [], []
        for chunk in body.split("\n\n"):
            if chunk.startswith("```"):
                loose.append(chunk)
            else:
                quoted.append(chunk)
        parts = []
        if title:
            parts.append("> **%s**\n>" % title)
        if quoted:
            parts.append(quote("\n\n".join(quoted)))
        if loose:
            parts.append("\n\n".join(loose))
        return "\n\n".join(parts)

    def tabbed(self, tag):
        labels = [norm_ws(l.get_text()) for l in tag.select(".tabbed-labels > label")]
        blocks = tag.select(".tabbed-content > .tabbed-block")
        out = []
        if blocks:
            for i, b in enumerate(blocks):
                label = labels[i] if i < len(labels) else ""
                content = self.blocks(b)
                if label:
                    out.append("**%s**\n\n%s" % (label, content) if content else "**%s**" % label)
                elif content:
                    out.append(content)
        else:
            if labels:
                out.append("**%s**" % labels[0])
            out.append(self.blocks(tag))
        return "\n\n".join(x for x in out if x.strip())

    def list(self, tag, ordered):
        items = []
        number = 0
        for li in tag.find_all("li", recursive=False):
            number += 1
            items.append(self.li(li, ordered, number))
        return "\n".join(items)

    def li(self, li, ordered, number):
        parts, nested = [], []
        blocks = li.find_all(["p", "pre", "div", "table", "blockquote"], recursive=False)
        for child in li.children:
            if isinstance(child, NavigableString):
                t = re.sub(r"\s+", " ", str(child))
                if t.strip():
                    parts.append(t)
            elif isinstance(child, Tag):
                if child.name in ("ul", "ol"):
                    nested.append(child)
                elif child in blocks:
                    md = self.block(child)
                    if md.strip():
                        parts.append("\n\n" + md.strip("\n"))
                else:
                    parts.append(self.inline(child))
        text = "".join(parts).strip()
        prefix = ("%d. " % number) if ordered else "- "
        lines = text.split("\n")
        out = prefix + lines[0]
        for line in lines[1:]:
            out += "\n" + (" " * len(prefix) + line if line.strip() else "")
        for n in nested:
            out += "\n" + indent(self.list(n, n.name == "ol"), " " * len(prefix))
        return out

    def table(self, tag):
        rows = []
        for tr in tag.find_all("tr"):
            cells = []
            for cell in tr.find_all(["th", "td"], recursive=False):
                txt = self.inline_children(cell).strip()
                txt = txt.replace("\n", "<br>")
                cells.append(txt.replace("|", "\\|"))
            if cells:
                rows.append(cells)
        if not rows:
            return ""
        width = max(len(r) for r in rows)
        rows = [r + [""] * (width - len(r)) for r in rows]
        out = ["| " + " | ".join(rows[0]) + " |",
               "| " + " | ".join(["---"] * width) + " |"]
        for r in rows[1:]:
            out.append("| " + " | ".join(r) + " |")
        return "\n".join(out)


def urlparse_path(url):
    p = url.split("/", 3)
    return "/" + (p[3] if len(p) > 3 else "")


def quote(text):
    lines = []
    for block in text.split("\n"):
        lines.append("> " + block if block.strip() else ">")
    return "\n".join(lines)


def indent(text, prefix):
    return "\n".join((prefix + l) if l.strip() else l for l in text.split("\n"))


# -- upstream alignment ---------------------------------------------------
def raw_items(raw_text, base):
    """Ordered list of code items in the upstream Markdown.

    A `<!--codeinclude-->` block may hold several directives, each of which
    becomes one code block on the rendered page.
    """
    items = []
    for m in CODEINCLUDE_BLOCK.finditer(raw_text):
        for d in DIRECTIVE.finditer(m.group("body")):
            rel = d.group("path").strip()
            full = os.path.normpath(os.path.join(base, rel)) if not rel.startswith("http") else rel
            items.append({"pos": m.start() + d.start(), "kind": "include", "path": full,
                          "title": d.group("title").strip()})
    for m in FENCE_RE.finditer(raw_text):
        items.append({"pos": m.start(), "kind": "fence",
                      "lang": m.group("lang").strip(), "text": m.group("text")})
    items.sort(key=lambda x: x["pos"])
    return items


def lang_for(path):
    ext = os.path.splitext(path)[1].lower()
    return EXT_LANG.get(ext, "")


def loose_in_file(file_text, code_text):
    """True if the longest distinctive line of code_text occurs in file_text."""
    lines = [l.strip() for l in code_text.split("\n") if l.strip()]
    if not lines:
        return False
    probe = max(lines, key=len)
    if len(probe) < 8:
        return False
    return probe in file_text


def fence_matches(raw_text, rendered_text):
    """Compare an upstream fence with a rendered block.

    The upstream Markdown may contain placeholders such as `{{latest_version}}`
    that MkDocs substitutes at build time, so those become wildcards, and
    Jinja `{% raw %}` markers that are not rendered.
    """
    raw_text = "\n".join(l for l in raw_text.split("\n")
                         if l.strip() not in ("{% raw %}", "{% endraw %}"))
    r = norm_code(raw_text)
    d = norm_code(rendered_text)
    if r == d:
        return True
    if "{{" not in r:
        return False
    pattern = re.escape(r)
    pattern = re.sub(r"\\\{\\\{.*?\\\}\\\}", ".*?", pattern)
    return re.match("(?s)" + pattern + r"\Z", d) is not None


def align_langs(items, blocks_text, ghfiles):
    """Match rendered code blocks with upstream items to recover languages."""
    langs = []
    ri = 0
    for text in blocks_text:
        found = ""
        j = ri
        while j < len(items):
            it = items[j]
            if it["kind"] == "fence":
                if fence_matches(it["text"], text):
                    found = it["lang"]
                    ri = j + 1
                    break
            else:
                src = ghfiles.get(it["path"])
                if src and loose_in_file(src, text):
                    found = lang_for(it["path"])
                    ri = j + 1
                    break
            j += 1
        langs.append(found)
    return langs


def collect_code_texts(html):
    """Code blocks of a page, in document order."""
    soup = BeautifulSoup(html, "html.parser")
    art = soup.select_one("main article") or soup.select_one("article") or soup
    out = []
    for pre in art.find_all("pre"):
        code = pre.find("code")
        node = code if code is not None else pre
        out.append(node.get_text())
    return out


# -- pipeline -------------------------------------------------------------
def protect_blocks(body):
    lines = body.split("\n")
    out, blocks = [], []
    fence_re = re.compile(r"^ {0,3}(?P<fence>`{3,}|~{3,})(?P<info>.*)$")
    fence, buf, start_info = None, [], ""
    for ln in lines:
        m = fence_re.match(ln)
        if fence is None:
            if m:
                fence = (m.group("fence")[0], len(m.group("fence")))
                start_info = m.group("info")
                buf = [ln]
                continue
            out.append(ln)
            continue
        buf.append(ln)
        if (m and m.group("fence")[0] == fence[0]
                and len(m.group("fence")) >= fence[1]
                and m.group("info").strip() == ""):
            idx = len(blocks) + 1
            blocks.append({"index": idx, "info": start_info.strip(), "text": "\n".join(buf)})
            out.append("@@CODE_%d@@" % idx)
            buf, fence = [], None
    if buf:
        idx = len(blocks) + 1
        blocks.append({"index": idx, "info": start_info.strip(), "text": "\n".join(buf)})
        out.append("@@CODE_%d@@" % idx)
    return "\n".join(out), blocks


def chunk(prose, safe):
    if len(prose) <= LIMIT:
        return [(safe, prose)]
    lines = prose.split("\n")
    sec = re.compile(r"^(##|###) ")
    starts = [i for i, l in enumerate(lines) if sec.match(l)]
    if not starts:
        return [(safe, prose)]
    starts = [0] + starts
    groups, cur, cur_len = [], [], 0
    for i, s in enumerate(starts):
        e = starts[i + 1] if i + 1 < len(starts) else len(lines)
        text = "\n".join(lines[s:e])
        if cur and cur_len + len(text) > LIMIT:
            groups.append(cur)
            cur, cur_len = [], 0
        cur.append((s, e))
        cur_len += len(text) + 1
    texts = ["\n".join(lines[g[0][0]:g[-1][1]]) for g in groups]
    if len(texts) < 2:
        texts = [prose]
    out = []
    for t in texts:
        out.extend(split_paras(t))
    if len(out) < 2:
        return [(safe, prose)]
    return [("%s__p%d" % (safe, i), t) for i, t in enumerate(out, 1)]


def split_paras(text):
    if len(text) <= LIMIT:
        return [text]
    paras, cur = [], []
    for para in text.split("\n\n"):
        if cur and sum(len(p) + 2 for p in cur) + len(para) > LIMIT:
            paras.append("\n\n".join(cur))
            cur = []
        cur.append(para)
    if cur:
        paras.append("\n\n".join(cur))
    return paras


def main():
    for d in (PAGES, PROSE, BLOCKS):
        os.makedirs(d, exist_ok=True)
        for f in os.listdir(d):
            os.remove(os.path.join(d, f))

    fetch = json.load(open(os.path.join(CACHE, "fetch.json"), encoding="utf-8"))
    raw_meta = json.load(open(os.path.join(CACHE, "raw.json"), encoding="utf-8"))
    gh_meta = json.load(open(os.path.join(CACHE, "ghfiles.json"), encoding="utf-8"))
    ghfiles = {}
    for path, info in gh_meta.items():
        p = os.path.join(GHFILES, info["file"])
        if os.path.exists(p):
            ghfiles[path] = open(p, encoding="utf-8").read()

    index = []
    for slug in sorted(fetch.keys()):
        url = fetch[slug]["url"]
        html = open(os.path.join(CACHE, fetch[slug]["file"]), encoding="utf-8").read()
        raw_path = os.path.join(RAW, safe_name(slug) + ".md")
        raw_text = open(raw_path, encoding="utf-8").read() if os.path.exists(raw_path) else ""
        base = os.path.dirname(raw_meta.get(slug, {}).get("repo_path") or "docs/%s.md" % (slug or "index"))

        code_texts = collect_code_texts(html)
        langs = align_langs(raw_items(raw_text, base), code_texts, ghfiles)

        page = Page(slug, url, html, langs)
        soup = BeautifulSoup(html, "html.parser")
        art = soup.select_one("main article")
        if art is None:
            art = soup.select_one("article") or soup.select_one("main") or soup
        # drop chrome: "edit this page" link, heading anchors
        for a in art.select('a[href*="/edit/"]'):
            a.decompose()
        for a in art.select("a.headerlink"):
            a.decompose()
        h1 = art.find("h1")
        title = norm_ws(h1.get_text()) if h1 else (slug or HOST)
        if h1 is not None:
            h1.decompose()
        page.lang_i = 0
        body = page.blocks(art)

        raw = "# %s\n\n%s\n" % (title, body.strip("\n"))
        safe = safe_name(slug)
        with open(os.path.join(PAGES, safe + ".md"), "w", encoding="utf-8", newline="\n") as f:
            f.write(raw)

        prose, blocks = protect_blocks(body.strip("\n"))
        parts = chunk(prose, safe)
        for name, text in parts:
            with open(os.path.join(PROSE, name + ".md"), "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
        with open(os.path.join(BLOCKS, safe + ".json"), "w", encoding="utf-8", newline="\n") as f:
            json.dump(blocks, f, ensure_ascii=False, indent=1)

        index.append({
            "url": url,
            "slug": slug,
            "title": title,
            "source_file": ".cache/%s/pages/%s.md" % (HOST, safe),
            "local_path": local_path(slug),
            "source_hash": "sha256:" + hashlib.sha256(raw.encode("utf-8")).hexdigest(),
            "prose_parts": [".work/prose/%s.md" % n for n, _ in parts],
            "blocks_file": ".work/blocks/%s.json" % safe,
            "chars": len(raw),
            "code_blocks": len(blocks),
            "prose_chars": sum(len(t) for _, t in parts),
            "langs": langs,
        })

    with open(os.path.join(ROOT, ".work", "index.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(index, f, ensure_ascii=False, indent=1)

    print("pages: %d, source chars: %d, prose chars: %d, code blocks: %d, parts: %d"
          % (len(index), sum(e["chars"] for e in index), sum(e["prose_chars"] for e in index),
             sum(e["code_blocks"] for e in index), sum(len(e["prose_parts"]) for e in index)))
    nolang = sum(1 for e in index for l in e["langs"] if not l)
    total = sum(len(e["langs"]) for e in index)
    print("code blocks with language: %d/%d" % (total - nolang, total))
    for e in sorted(index, key=lambda x: -x["prose_chars"])[:10]:
        print("  %-45s prose %6d parts %d blocks %d" % (e["slug"] or "(root)", e["prose_chars"],
                                                         len(e["prose_parts"]), e["code_blocks"]))


def local_path(slug):
    """URL slug -> path inside docs/<host>/<version>/."""
    if not slug:
        return "index.md"
    return "%s/index.md" % slug


if __name__ == "__main__":
    sys.exit(main())
