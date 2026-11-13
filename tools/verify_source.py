#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Independent integrity check against the original llms-full.txt.

Does not trust .work/blocks/*.json: re-splits the cached source from scratch
and compares each page's fenced code blocks with the assembled translation.
Also recomputes source_hash and checks it against _manifest.json.
"""
import hashlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import prep  # noqa: E402
import qa    # noqa: E402

SRC = os.path.join(ROOT, ".cache", "openspec.dev", "llms-full.txt")
OUTDIR = os.path.join(ROOT, "docs", "openspec.dev", "unversioned")


def main():
    with open(SRC, encoding="utf-8") as f:
        text = f.read()
    pages = prep.split_pages(text)
    with open(os.path.join(OUTDIR, "_manifest.json"), encoding="utf-8") as f:
        manifest = json.load(f)
    by_url = {p["url"]: p for p in manifest["pages"]}

    problems = []
    checked = 0
    total = 0
    for p in pages:
        slug = p["slug"]
        body = "\n".join(p["lines"]).strip("\n")
        raw = "# %s\n\n%s\n" % (p["title"], body) if body else "# %s\n" % p["title"]
        want = qa.fenced(body)

        url = "https://openspec.dev/docs/%s" % slug
        entry = by_url.get(url)
        if not entry:
            problems.append("%s: not in manifest" % slug)
            continue
        path = os.path.join(OUTDIR, entry["local_path"].replace("/", os.sep))
        if not os.path.exists(path):
            problems.append("%s: missing %s" % (slug, path))
            continue
        with open(path, encoding="utf-8") as f:
            doc = f.read()
        fm, out_body = qa.split_fm(doc)
        got = qa.fenced(out_body)

        if got != want:
            if len(got) != len(want):
                problems.append("%s: %d blocks vs %d in source" % (slug, len(got), len(want)))
            else:
                for i, (a, b) in enumerate(zip(got, want), 1):
                    if a != b:
                        problems.append("%s: block #%d differs from source" % (slug, i))

        h = "sha256:" + hashlib.sha256(raw.encode("utf-8")).hexdigest()
        if h != entry["source_hash"]:
            problems.append("%s: source_hash mismatch" % slug)
        if fm and ("source_hash: %s" % h) not in fm:
            problems.append("%s: frontmatter source_hash mismatch" % slug)
        if fm and ("source_url: %s" % url) not in fm:
            problems.append("%s: frontmatter source_url mismatch" % slug)

        checked += 1
        total += len(want)

    print("pages: %d, code blocks verified against raw source: %d" % (checked, total))
    if problems:
        print("PROBLEMS: %d" % len(problems))
        for x in problems:
            print("  -", x)
        return 1
    print("SOURCE INTEGRITY OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
