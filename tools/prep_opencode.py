#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Prepare opencode.ai docs pages for translation.

Each cached page is split into:
  .work/prose/<safe>.md         prose with fenced code blocks -> @@CODE_n@@
  .work/blocks/<safe>.json      the fenced code blocks, in order
Large pages are chunked at heading boundaries into <safe>__pN.md.

.work/index.json is the manifest the assembler reads.
"""
import hashlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = "opencode.ai"
CACHE = os.path.join(ROOT, ".cache", HOST)
PROSE = os.path.join(ROOT, ".work", "prose")
BLOCKS = os.path.join(ROOT, ".work", "blocks")
LIMIT = 11000

FENCE = re.compile(r"^ {0,3}(?P<fence>`{3,}|~{3,})(?P<info>.*)$")
SEC = re.compile(r"^(?P<level>##|###) ")


def protect_blocks(body):
    """Replace fenced code blocks with @@CODE_n@@ placeholders (CommonMark fences)."""
    lines = body.split("\n")
    out, blocks = [], []
    fence = None
    buf, start_info = [], ""
    for ln in lines:
        m = FENCE.match(ln)
        if fence is None:
            if m and not (m.group("fence")[0] == "`" and "`" in m.group("info")):
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
            fence, buf = None, []
    if buf:  # unterminated fence: keep it verbatim rather than lose it
        idx = len(blocks) + 1
        blocks.append({"index": idx, "info": start_info.strip(), "text": "\n".join(buf)})
        out.append("@@CODE_%d@@" % idx)
    return "\n".join(out), blocks


def chunk(prose, safe):
    """Group heading-delimited sections into <=LIMIT-char parts."""
    if len(prose) <= LIMIT:
        return [(safe, prose)]
    lines = prose.split("\n")
    starts = [i for i, l in enumerate(lines) if SEC.match(l)]
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
    if cur:
        groups.append(cur)
    if len(groups) < 2:
        return [(safe, prose)]
    return [("%s__p%d" % (safe, gi),
             "\n".join(lines[g[0][0]:g[-1][1]])) for gi, g in enumerate(groups, 1)]


def main():
    for d in (PROSE, BLOCKS):
        os.makedirs(d, exist_ok=True)
    for f in os.listdir(PROSE):
        os.remove(os.path.join(PROSE, f))
    for f in os.listdir(BLOCKS):
        os.remove(os.path.join(BLOCKS, f))

    fetch = json.load(open(os.path.join(CACHE, "fetch.json"), encoding="utf-8"))
    index, seen = [], set()
    for e in fetch:
        if e["slug"] in seen:
            continue
        seen.add(e["slug"])
        if e.get("md_missing"):
            index.append(dict(e, prose_parts=[], blocks_file=None, code_blocks=0,
                              prose_chars=0, skip="no markdown twin"))
            continue
        raw = open(os.path.join(ROOT, e["source_file"]), encoding="utf-8").read()
        lines = raw.split("\n")
        assert lines[0].startswith("# "), e["slug"]
        title = lines[0][2:].strip()
        body = "\n".join(lines[1:]).strip("\n")
        prose, blocks = protect_blocks(body)
        safe = e["slug"].replace("/", "__") or "__root__"
        parts = chunk(prose, safe)
        for name, text in parts:
            with open(os.path.join(PROSE, name + ".md"), "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
        with open(os.path.join(BLOCKS, safe + ".json"), "w", encoding="utf-8", newline="\n") as f:
            json.dump(blocks, f, ensure_ascii=False, indent=1)
        index.append({
            "url": e["url"],
            "slug": e["slug"],
            "title": title,
            "source_file": e["source_file"],
            "local_path": e["local_path"],
            "source_hash": e["source_hash"],
            "prose_parts": [".work/prose/%s.md" % n for n, _ in parts],
            "blocks_file": ".work/blocks/%s.json" % safe,
            "chars": len(raw),
            "code_blocks": len(blocks),
            "prose_chars": sum(len(t) for _, t in parts),
        })

    with open(os.path.join(ROOT, ".work", "index.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(index, f, ensure_ascii=False, indent=1)

    pages = [e for e in index if not e.get("skip")]
    print("pages: %d (+%d skipped)" % (len(pages), len(index) - len(pages)))
    print("source chars: %d, prose chars: %d, code blocks: %d, prose parts: %d"
          % (sum(e["chars"] for e in pages), sum(e["prose_chars"] for e in pages),
             sum(e["code_blocks"] for e in pages),
             sum(len(e["prose_parts"]) for e in pages)))
    big = sorted(pages, key=lambda x: -x["prose_chars"])[:10]
    for e in big:
        print("  %-40s prose %6d  parts %d  blocks %d" % (e["slug"] or "(root)", e["prose_chars"],
                                                          len(e["prose_parts"]), e["code_blocks"]))


if __name__ == "__main__":
    sys.exit(main())
