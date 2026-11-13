#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Split openspec.dev llms-full.txt into per-page Markdown, protect fenced code blocks.

Outputs:
  .cache/openspec.dev/pages/<slug>.md      raw page source (fence-safe split)
  .work/prose/<slug>.md                    prose-only text, code blocks -> @@CODE_n@@
  .work/blocks/<slug>.json                 ordered fenced code blocks
  .work/index.json                         manifest of pages
"""
import json
import re
import hashlib
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, ".cache", "openspec.dev", "llms-full.txt")

PAGES = os.path.join(ROOT, ".cache", "openspec.dev", "pages")
PROSE = os.path.join(ROOT, ".work", "prose")
BLOCKS = os.path.join(ROOT, ".work", "blocks")

HEADER = re.compile(r"^# (?P<title>.+?) \(/docs/(?P<slug>[^)]+)\)\s*$")
FENCE = re.compile(r"^(?P<indent>\s*)(?P<fence>`{3,}|~{3,})(?P<info>.*)$")


def split_pages(text):
    """Split on '# Title (/docs/slug)' lines that are outside fenced code."""
    lines = text.split("\n")
    pages = []
    cur = None
    fence = None
    for ln in lines:
        m = FENCE.match(ln)
        if m:
            tok = m.group("fence")
            if fence is None:
                fence = tok
            elif tok[0] == fence[0] and len(tok) >= len(fence) and m.group("info").strip() == "":
                fence = None
            if cur is not None:
                cur["lines"].append(ln)
            continue
        if fence is None:
            h = HEADER.match(ln)
            if h:
                if cur is not None:
                    pages.append(cur)
                cur = {"title": h.group("title").strip(), "slug": h.group("slug").strip(), "lines": []}
                continue
        if cur is not None:
            cur["lines"].append(ln)
    if cur is not None:
        pages.append(cur)
    return pages


def protect_blocks(body):
    """Replace fenced code blocks with @@CODE_n@@ placeholders."""
    lines = body.split("\n")
    out = []
    blocks = []
    i = 0
    fence = None
    buf = []
    start_info = None
    while i < len(lines):
        ln = lines[i]
        m = FENCE.match(ln)
        if fence is None:
            if m:
                fence = m.group("fence")
                start_info = m.group("info")
                buf = [ln]
                i += 1
                continue
            out.append(ln)
            i += 1
            continue
        else:
            buf.append(ln)
            tok = m.group("fence") if m else None
            if tok and tok[0] == fence[0] and len(tok) >= len(fence) and m.group("info").strip() == "":
                fence = None
                idx = len(blocks) + 1
                blocks.append({
                    "index": idx,
                    "info": start_info.strip(),
                    "text": "\n".join(buf),
                })
                out.append("@@CODE_%d@@" % idx)
                buf = []
            i += 1
    if buf:
        # unterminated fence: keep raw so nothing is lost
        idx = len(blocks) + 1
        blocks.append({"index": idx, "info": (start_info or "").strip(), "text": "\n".join(buf)})
        out.append("@@CODE_%d@@" % idx)
    return "\n".join(out), blocks


CHUNK_LIMIT = 15000
H2 = re.compile(r"^## ")


def chunk(prose, safe):
    """Split prose at '## ' boundaries into <=CHUNK_LIMIT-char parts.

    Returns list of (filename, text). Joining the texts with a blank line
    reconstructs the original exactly (parts only break at top-level headings).
    """
    if len(prose) <= CHUNK_LIMIT:
        return [(safe + ".md", prose)]
    lines = prose.split("\n")
    starts = [i for i, l in enumerate(lines) if H2.match(l)]
    if not starts:
        return [(safe + ".md", prose)]
    # include any preamble before the first '## ' in the first section
    starts = [0] + starts
    # greedy grouping of sections
    groups = []
    cur = []
    cur_len = 0
    for idx, s in enumerate(starts):
        e = starts[idx + 1] if idx + 1 < len(starts) else len(lines)
        size = len("\n".join(lines[s:e]))
        if cur and cur_len + size > CHUNK_LIMIT:
            groups.append(cur)
            cur, cur_len = [], 0
        cur.append((s, e))
        cur_len += size
    if cur:
        groups.append(cur)
    if len(groups) < 2:
        return [(safe + ".md", prose)]
    out = []
    for gi, g in enumerate(groups, 1):
        text = "\n".join(lines[g[0][0]:g[-1][1]])
        out.append(("%s__p%d.md" % (safe, gi), text))
    return out


def main():
    for d in (PAGES, PROSE, BLOCKS):
        os.makedirs(d, exist_ok=True)
    with open(SRC, "r", encoding="utf-8") as f:
        text = f.read()
    pages = split_pages(text)
    index = []
    for p in pages:
        slug = p["slug"]
        body = "\n".join(p["lines"]).strip("\n")
        raw = "# %s\n\n%s\n" % (p["title"], body) if body else "# %s\n" % p["title"]
        safe = slug.replace("/", "__")
        with open(os.path.join(PAGES, safe + ".md"), "w", encoding="utf-8", newline="\n") as f:
            f.write(raw)
        prose, blocks = protect_blocks(body)
        parts = chunk(prose, safe)
        for name, text in parts:
            with open(os.path.join(PROSE, name), "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
        with open(os.path.join(BLOCKS, safe + ".json"), "w", encoding="utf-8", newline="\n") as f:
            json.dump(blocks, f, ensure_ascii=False, indent=1)
        index.append({
            "slug": slug,
            "title": p["title"],
            "source_file": ".cache/openspec.dev/pages/%s.md" % safe,
            "prose_parts": [".work/prose/%s" % n for n, _ in parts],
            "blocks_file": ".work/blocks/%s.json" % safe,
            "source_hash": "sha256:" + hashlib.sha256(raw.encode("utf-8")).hexdigest(),
            "chars": len(raw),
            "code_blocks": len(blocks),
            "prose_chars": len(prose),
        })
    with open(os.path.join(ROOT, ".work", "index.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(index, f, ensure_ascii=False, indent=1)
    print("pages: %d" % len(index))
    for e in index:
        print("  %-28s %6d chars  %2d blocks  %s" % (e["slug"], e["chars"], e["code_blocks"], e["title"]))


if __name__ == "__main__":
    main()
