#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Assemble the translated java.testcontainers.org pages into the docs tree.

Reads .work/index.json + .work/zh/*.md + .work/blocks/*.json, restores the
fenced code blocks byte-for-byte, rewrites in-site links to relative .md
links, adds frontmatter, writes docs/java.testcontainers.org/unversioned/...
and _manifest.json.

Usage:
  python tools/assemble_testcontainers.py --check   # validate only
  python tools/assemble_testcontainers.py            # validate then write
"""
import json
import os
import re
import sys
import posixpath
from datetime import datetime, timezone, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = "java.testcontainers.org"
DOC_VERSION = "unversioned"
UPSTREAM_VERSION = "2.0.5"
TZ = timezone(timedelta(hours=8))
NOW = datetime.now(TZ).replace(microsecond=0).isoformat()

PH = re.compile(r"@@CODE_(\d+)@@")
COMMENT = re.compile(r"<!--.*?-->", re.S)
LINK = re.compile(r"\]\((https?://%s[^)\s]*)\)" % re.escape(HOST))


def local_path(slug):
    """URL slug -> path inside the version dir (trailing slash => index.md)."""
    if not slug:
        return "index.md"
    return "%s/index.md" % slug


def rel_link(from_local, to_local, anchor):
    d = posixpath.dirname(from_local)
    r = posixpath.relpath(to_local, d if d else ".")
    if not r.startswith("."):
        r = "./" + r
    return r + ("#" + anchor if anchor else "")


def slug_of_url(url):
    """Absolute site URL -> slug (None when the URL is not on this site)."""
    path = url.split("?", 1)[0].split("#", 1)[0]
    path = path[len("https://" + HOST):]
    return path.strip("/")


def rewrite_links(text, from_local, known_slugs):
    """Rewrite links to this site into relative .md links."""

    def repl(m):
        url = m.group(1)
        slug = slug_of_url(url)
        if slug is None or slug not in known_slugs:
            return m.group(0)
        anchor = ""
        if "#" in url:
            anchor = url.split("#", 1)[1]
        return "](%s)" % rel_link(from_local, local_path(slug), anchor)

    return LINK.sub(repl, text)


def restore_blocks(text, blocks, slug):
    """Replace @@CODE_n@@ with the original fenced block text. Returns (text, errs)."""
    errs = []
    seen = []
    expected = {str(b["index"]): b for b in blocks}

    def repl(m):
        n = m.group(1)
        seen.append(n)
        b = expected.get(n)
        if b is None:
            errs.append("%s: unexpected placeholder @@CODE_%s@@" % (slug, n))
            return m.group(0)
        return b["text"]

    out = PH.sub(repl, text)
    missing = [k for k in expected if k not in seen]
    if missing:
        errs.append("%s: missing placeholders %s" % (slug, sorted(missing, key=int)))
    dups = [n for n in set(seen) if seen.count(n) > 1]
    if dups:
        errs.append("%s: duplicated placeholders %s" % (slug, sorted(dups, key=int)))
    if seen != sorted(seen, key=int):
        errs.append("%s: placeholder order changed" % slug)
    return out, errs


def existing_meta(path):
    """Read source_hash and translation_version from an already written page."""
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 3)
    if end < 0:
        return None
    fm = text[4:end]
    h = re.search(r"^source_hash:\s*(\S+)\s*$", fm, re.M)
    v = re.search(r"^translation_version:\s*(\d+)\s*$", fm, re.M)
    return {
        "source_hash": h.group(1) if h else None,
        "translation_version": int(v.group(1)) if v else 0,
    }


def strip_comments(text):
    """Drop HTML comments (authoring notes, never rendered on the site)."""
    out = COMMENT.sub("", text)
    out = re.sub(r"^\s*\n", "", out)
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out


def main():
    check_only = "--check" in sys.argv
    with open(os.path.join(ROOT, ".work", "index.json"), encoding="utf-8") as f:
        index = json.load(f)
    known = set(e["slug"] for e in index)
    outdir = os.path.join(ROOT, "docs", HOST, DOC_VERSION)

    errors = []
    results = []
    for e in index:
        slug = e["slug"]
        lp = e["local_path"]
        parts = []
        missing_file = False
        for p in e["prose_parts"]:
            zp = os.path.join(ROOT, ".work", "zh", os.path.basename(p))
            if not os.path.exists(zp):
                errors.append("%s: missing translation %s" % (slug, zp))
                missing_file = True
                break
            with open(zp, encoding="utf-8") as f:
                parts.append(f.read().strip("\n"))
        if missing_file:
            results.append({"slug": slug, "status": "missing", "local_path": lp,
                            "source_hash": e["source_hash"], "translation_version": 0})
            continue

        with open(os.path.join(ROOT, e["blocks_file"]), encoding="utf-8") as f:
            blocks = json.load(f)

        body = "\n\n".join(parts)
        # the first part starts with the Chinese page title
        title = ""
        lines = body.split("\n")
        if lines and lines[0].startswith("# "):
            title = lines[0][2:].strip()
            lines = lines[1:]
            body = "\n".join(lines)
        if not title:
            errors.append("%s: no Chinese title" % slug)
            title = e["title"]

        body = strip_comments(body)
        body, errs = restore_blocks(body, blocks, slug)
        errors.extend(errs)
        body = rewrite_links(body, lp, known)

        dest = os.path.join(outdir, lp.replace("/", os.sep))
        old = existing_meta(dest)
        if old and old["source_hash"] == e["source_hash"]:
            results.append({
                "slug": slug, "status": "unchanged", "local_path": lp,
                "source_hash": e["source_hash"],
                "translation_version": old["translation_version"], "dest": dest,
                "doc": None,
            })
            continue

        tv = old["translation_version"] + 1 if old else 1
        fm = (
            "---\n"
            "source_url: %s\n"
            "source_hash: %s\n"
            "translated_at: %s\n"
            "translation_version: %d\n"
            "---\n\n" % (e["url"], e["source_hash"], NOW, tv)
        )
        doc = fm + "# %s\n\n%s\n" % (title, body.strip("\n"))

        results.append({
            "slug": slug, "status": "failed" if errs else "translated",
            "local_path": lp, "source_hash": e["source_hash"],
            "translation_version": tv, "dest": dest, "doc": doc,
        })

    ok = [r for r in results if r["status"] == "translated"]
    kept = [r for r in results if r["status"] == "unchanged"]
    bad = [r for r in results if r["status"] not in ("translated", "unchanged")]
    print("translated: %d, unchanged: %d, failed: %d (total %d)"
          % (len(ok), len(kept), len(bad), len(results)))
    for r in bad:
        print("  NOT OK:", r["slug"], r["status"])
    if errors:
        print("--- errors (%d) ---" % len(errors))
        for x in errors:
            print("  ", x)

    if check_only:
        return 1 if (errors or bad) else 0
    if errors or bad:
        print("aborting write: fix errors first")
        return 1

    for r in ok:
        os.makedirs(os.path.dirname(r["dest"]), exist_ok=True)
        with open(r["dest"], "w", encoding="utf-8", newline="\n") as f:
            f.write(r["doc"])

    max_tv = max([r["translation_version"] for r in results] or [1])
    manifest = {
        "host": HOST,
        "doc_version": DOC_VERSION,
        "upstream_version": UPSTREAM_VERSION,
        "translation_version": max_tv,
        "updated_at": NOW,
        "source": "https://%s/sitemap.xml" % HOST,
        "counts": {
            "total": len(results),
            "translated": len(ok) + len(kept),
            "failed": len(bad),
        },
        "updated_this_run": len(ok),
        "pages": [
            {
                "url": e["url"],
                "local_path": r["local_path"],
                "status": "translated" if r["status"] in ("translated", "unchanged") else r["status"],
                "source_hash": r["source_hash"],
                "translation_version": r["translation_version"],
            }
            for r, e in zip(sorted(results, key=lambda x: x["slug"]),
                            sorted(index, key=lambda x: x["slug"]))
        ],
    }
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "_manifest.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("wrote %d, kept %d -> docs/%s/%s/" % (len(ok), len(kept), HOST, DOC_VERSION))
    return 0


if __name__ == "__main__":
    sys.exit(main())
