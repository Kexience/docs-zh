#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Assemble translated prose back into the docs tree.

Reads .work/index.json + .work/zh/*.md + .work/blocks/*.json, restores fenced
code blocks byte-for-byte, rewrites /docs links to relative .md links, adds
frontmatter, writes docs/<host>/<version>/... and _manifest.json.

Usage:
  python tools/assemble.py --check   # validate only, write nothing
  python tools/assemble.py           # validate then write
"""
import json
import os
import re
import sys
import posixpath
from datetime import datetime, timezone, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = "openspec.dev"
DOC_VERSION = "unversioned"
UPSTREAM_VERSION = "2.0"
TZ = timezone(timedelta(hours=8))
NOW = datetime.now(TZ).replace(microsecond=0).isoformat()

PH = re.compile(r"@@CODE_(\d+)@@")
COMMENT = re.compile(r"<!--.*?-->", re.S)


def strip_comments(text):
    """Drop HTML comments: authoring notes, never rendered on the site."""
    out = COMMENT.sub("", text)
    # collapse blank lines left behind at the start
    out = re.sub(r"^\s*\n", "", out)
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out

# slug -> Chinese h1
TITLES = {
    "installation": "安装",
    "setup": "配置你的项目",
    "quickstart": "快速入门",
    "upgrade-to-2": "升级到 2.0",
    "customize": "定制总览",
    "profiles": "配置档",
    "project-config": "项目配置",
    "customize-schemas": "模式",
    "stores": "存储库（beta）",
    "worksets": "工作集（beta）",
    "skills": "技能",
    "cli": "CLI",
    "schemas": "模式总览",
    "schemas/schema-yaml": "schema.yaml",
    "schemas/spec-driven": "spec-driven",
    "configuration": "配置总览",
    "configuration/config-yaml": "项目配置（config.yaml）",
    "configuration/change-metadata": "变更元数据（.openspec.yaml）",
    "configuration/config-json": "CLI 设置（config.json）",
    "supported-tools": "支持的工具",
    "glossary": "术语表",
}


def local_path(slug):
    """URL path segment -> local path inside the version dir."""
    return "docs/%s.md" % slug


def rel_link(from_local, to_local, anchor):
    d = posixpath.dirname(from_local)
    r = posixpath.relpath(to_local, d if d else ".")
    if not r.startswith("."):
        r = "./" + r
    return r + ("#" + anchor if anchor else "")


def rewrite_links(text, from_local, known_slugs):
    """Rewrite (/docs/x) and (/docs/x#a) to relative .md links."""

    def repl(m):
        target = m.group(1)
        if not target.startswith("/docs"):
            return m.group(0)
        path, _, anchor = target.partition("#")
        slug = path[len("/docs"):].strip("/")
        if slug == "":
            return m.group(0)
        if slug in known_slugs:
            return "(%s)" % rel_link(from_local, local_path(slug), anchor)
        # not captured: keep absolute
        return "(https://%s%s)" % (HOST, target)

    return re.sub(r"\((/(?:docs)[^)\s]*)\)", repl, text)


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
        lp = local_path(slug)
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
            results.append({"slug": slug, "status": "missing"})
            continue

        with open(os.path.join(ROOT, e["blocks_file"]), encoding="utf-8") as f:
            blocks = json.load(f)

        body = "\n\n".join(parts)
        body = strip_comments(body)
        body, errs = restore_blocks(body, blocks, slug)
        errors.extend(errs)
        body = rewrite_links(body, lp, known)

        title = TITLES.get(slug)
        if not title:
            errors.append("%s: no Chinese title" % slug)
            title = e["title"]

        dest = os.path.join(outdir, lp.replace("/", os.sep))
        old = existing_meta(dest)
        if old and old["source_hash"] == e["source_hash"]:
            # Source unchanged: never overwrite an existing translation.
            results.append({
                "slug": slug,
                "status": "unchanged",
                "local_path": lp,
                "source_hash": e["source_hash"],
                "translation_version": old["translation_version"],
                "dest": dest,
                "doc": None,
            })
            continue

        # New page -> 1; source changed -> monotonically +1.
        tv = old["translation_version"] + 1 if old else 1
        fm = (
            "---\n"
            "source_url: https://%s/docs/%s\n"
            "source_hash: %s\n"
            "translated_at: %s\n"
            "translation_version: %d\n"
            "---\n\n" % (HOST, slug, e["source_hash"], NOW, tv)
        )
        doc = fm + "# %s\n\n%s\n" % (title, body.strip("\n"))

        results.append({
            "slug": slug,
            "status": "failed" if errs else "translated",
            "local_path": lp,
            "source_hash": e["source_hash"],
            "translation_version": tv,
            "dest": dest,
            "doc": doc,
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
        "source": "https://%s/llms-full.txt" % HOST,
        "counts": {
            "total": len(results),
            "translated": len(ok) + len(kept),
            "failed": len(bad),
        },
        "updated_this_run": len(ok),
        "pages": [
            {
                "url": "https://%s/docs/%s" % (HOST, r["slug"]),
                "local_path": r["local_path"],
                # a page kept from a previous run still has a translation
                "status": "translated" if r["status"] == "unchanged" else r["status"],
                "source_hash": r["source_hash"],
                "translation_version": r["translation_version"],
            }
            for r in sorted(results, key=lambda x: x["slug"])
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
