#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Quality gate for the assembled translation.

Checks, per page:
  1. file exists, frontmatter has the 4 required keys
  2. h1 present and is Chinese
  3. fenced code blocks in the final doc are byte-identical to the source blocks
  4. heading structure (# counts by level) matches the source page
  5. every table keeps the same row count and column count as the source
  6. every relative link resolves to a file that exists
  7. prose lines that are still pure English (possible untranslated text)

Fence handling follows CommonMark: a fence closes only on the same character,
at least as long as the opener, with no info string. This matters because the
spec-driven page nests ``` inside ````md blocks.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = "openspec.dev"
VER = "unversioned"
OUTDIR = os.path.join(ROOT, "docs", HOST, VER)
CJK = re.compile(r"[\u4e00-\u9fff]")
COMMENT = re.compile(r"<!--.*?-->", re.S)
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")


def split_fm(text):
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 3)
    if end < 0:
        return None, text
    return text[4:end], text[end + 5:]


def scan(text):
    """Return list of (line, is_code). Fence lines count as code."""
    rows = []
    fence = None  # (char, length)
    for ln in text.split("\n"):
        m = FENCE.match(ln)
        if fence is None:
            if m and not (m.group(1)[0] == "`" and "`" in m.group(2)):
                fence = (m.group(1)[0], len(m.group(1)))
                rows.append((ln, True))
            else:
                rows.append((ln, False))
        else:
            if (m and m.group(1)[0] == fence[0]
                    and len(m.group(1)) >= fence[1]
                    and m.group(2).strip() == ""):
                fence = None
            rows.append((ln, True))
    return rows


def fenced(text):
    """Extract fenced blocks, opener line through closer line inclusive."""
    blocks = []
    cur = None
    fence = None
    for ln, is_code in scan(text):
        m = FENCE.match(ln)
        if cur is None:
            if is_code and m:
                cur = [ln]
                fence = (m.group(1)[0], len(m.group(1)))
            continue
        cur.append(ln)
        if (m and m.group(1)[0] == fence[0]
                and len(m.group(1)) >= fence[1]
                and m.group(2).strip() == ""):
            blocks.append("\n".join(cur))
            cur = None
            fence = None
    if cur:
        blocks.append("\n".join(cur))
    return blocks


def headings(text):
    d = {}
    for ln, is_code in scan(text):
        if is_code:
            continue
        h = re.match(r"^(#{2,4}) ", ln)
        if h:
            d[len(h.group(1))] = d.get(len(h.group(1)), 0) + 1
    return d


def tables(text):
    """Return list of (rows, col-counts) per contiguous table."""
    res = []
    cur = []
    for ln, is_code in scan(text):
        if not is_code and ln.strip().startswith("|"):
            cur.append(ln)
        else:
            if cur:
                cols = tuple(len(r.strip().strip("|").split("|")) for r in cur)
                res.append((len(cur), cols))
                cur = []
    if cur:
        cols = tuple(len(r.strip().strip("|").split("|")) for r in cur)
        res.append((len(cur), cols))
    return res


def main():
    with open(os.path.join(ROOT, ".work", "index.json"), encoding="utf-8") as f:
        index = json.load(f)
    problems = []
    total_blocks = 0

    for e in index:
        slug = e["slug"]
        lp = "docs/%s.md" % slug
        path = os.path.join(OUTDIR, lp.replace("/", os.sep))
        if not os.path.exists(path):
            problems.append("%s: MISSING output file" % slug)
            continue
        with open(path, encoding="utf-8") as f:
            doc = f.read()
        fm, body = split_fm(doc)
        if fm is None:
            problems.append("%s: no frontmatter" % slug)
        else:
            for k in ("source_url", "source_hash", "translated_at", "translation_version"):
                if not re.search(r"^%s:" % k, fm, re.M):
                    problems.append("%s: frontmatter missing %s" % (slug, k))

        # h1
        m = re.search(r"^# (.+)$", body, re.M)
        if not m:
            problems.append("%s: no h1" % slug)
        elif not CJK.search(m.group(1)) and slug not in (
            "cli", "schemas/schema-yaml", "schemas/spec-driven",
        ):
            problems.append("%s: h1 not Chinese: %r" % (slug, m.group(1)))

        # code blocks byte-identical to source
        with open(os.path.join(ROOT, e["blocks_file"]), encoding="utf-8") as f:
            blocks = json.load(f)
        got = fenced(body)
        want = [b["text"] for b in blocks]
        total_blocks += len(want)
        if got != want:
            if len(got) != len(want):
                problems.append("%s: code block count %d != %d" % (slug, len(got), len(want)))
            else:
                for i, (a, b) in enumerate(zip(got, want), 1):
                    if a != b:
                        problems.append("%s: code block #%d differs from source" % (slug, i))

        # heading structure
        with open(os.path.join(ROOT, e["source_file"]), encoding="utf-8") as f:
            src = f.read()
        src = COMMENT.sub("", src)
        hs, hd = headings(src), headings(body)
        if hs != hd:
            problems.append("%s: heading counts differ src=%s dst=%s" % (slug, hs, hd))

        # tables
        ts, td = tables(src), tables(body)
        if len(ts) != len(td):
            problems.append("%s: table count %d != %d" % (slug, len(td), len(ts)))
        else:
            for i, (a, b) in enumerate(zip(ts, td), 1):
                if a != b:
                    problems.append("%s: table #%d shape %s != %s" % (slug, i, b, a))

        # links
        for lm in re.finditer(r"\]\(([^)\s]+)\)", body):
            t = lm.group(1)
            if t.startswith("./") or t.startswith("../"):
                tgt = t.split("#")[0]
                p = os.path.normpath(os.path.join(os.path.dirname(path), tgt.replace("/", os.sep)))
                if not os.path.exists(p):
                    problems.append("%s: broken relative link %s" % (slug, t))
            elif t.startswith("#"):
                if "[#%s]" % t[1:] not in body:
                    problems.append("%s: dangling in-page anchor %s" % (slug, t))
            elif t.startswith("/"):
                problems.append("%s: absolute site link left unrewritten %s" % (slug, t))

        # untranslated prose
        for ln, is_code in scan(body):
            if is_code:
                continue
            s = ln.strip()
            if not s or s.startswith("|") or s.startswith("#"):
                continue
            if CJK.search(s):
                continue
            words = re.findall(r"[A-Za-z][A-Za-z'-]{1,}", re.sub(r"`[^`]*`", " ", s))
            if len(words) >= 6:
                problems.append("%s: possible untranslated line: %r" % (slug, s[:90]))

    print("pages checked: %d" % len(index))
    print("code blocks compared: %d" % total_blocks)
    if problems:
        print("PROBLEMS: %d" % len(problems))
        for p in problems:
            print("  -", p)
        return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
