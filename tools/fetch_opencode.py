#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Fetch every page of https://opencode.ai/docs in its native Markdown form.

The site serves a Markdown twin for each docs page (`/docs/config/` ->
`/docs/config.md`), so the source of truth is Markdown, not HTML.

Outputs:
  .cache/opencode.ai/llms.txt          the docs page list (llms.txt)
  .cache/opencode.ai/pages/<safe>.md    one raw Markdown page per URL
  .cache/opencode.ai/fetch.json        url -> cache file / title / bytes
"""
import hashlib
import json
import os
import re
import sys

import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = "opencode.ai"
CACHE = os.path.join(ROOT, ".cache", HOST)
PAGES = os.path.join(CACHE, "pages")
LLMS = os.path.join(CACHE, "llms.txt")

LINK = re.compile(r"\]\((https://%s/docs[^)]*)\)" % re.escape(HOST))


def safe_name(slug):
    return slug.replace("/", "__") if slug else "__root__"


def slug_of(url):
    path = url[len("https://" + HOST):]
    assert path.startswith("/docs"), url
    return path[len("/docs"):].strip("/")


def md_url(url):
    return url.rstrip("/") + ".md"


def local_path(slug):
    """URL slug -> path inside docs/<host>/<version>/ (trailing slash => index)."""
    if not slug:
        return "docs/index.md"
    return "docs/%s/index.md" % slug


def main():
    os.makedirs(PAGES, exist_ok=True)
    s = requests.Session()
    s.headers["User-Agent"] = "docs-translator/1.0"

    if os.path.exists(LLMS) and "--refresh-list" not in sys.argv:
        text = open(LLMS, encoding="utf-8").read()
    else:
        r = s.get("https://%s/docs/llms.txt" % HOST, timeout=60)
        r.raise_for_status()
        text = r.text
        with open(LLMS, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)

    urls = []
    for m in LINK.finditer(text):
        u = m.group(1)
        if u not in urls:
            urls.append(u)
    urls.insert(0, "https://%s/docs/" % HOST)

    index = []
    for url in urls:
        slug = slug_of(url)
        safe = safe_name(slug)
        dest = os.path.join(PAGES, safe + ".md")
        missing_md = False
        if os.path.exists(dest) and "--refresh" not in sys.argv:
            raw = open(dest, encoding="utf-8").read()
        else:
            r = s.get(md_url(url), timeout=90)
            if r.status_code == 404:
                # page has no Markdown twin (e.g. the generated API reference)
                missing_md = True
                r = None
            else:
                r.raise_for_status()
        if missing_md:
            print("%-46s MISSING .md  %s" % (slug, url))
            index.append({
                "url": url,
                "md_url": md_url(url),
                "slug": slug,
                "title": "",
                "source_file": None,
                "local_path": local_path(slug),
                "source_hash": None,
                "chars": 0,
                "md_missing": True,
            })
            continue
        if not (os.path.exists(dest) and "--refresh" not in sys.argv):
            raw = r.text.replace("\r\n", "\n").replace("\r", "\n")
            if not raw.endswith("\n"):
                raw += "\n"
            with open(dest, "w", encoding="utf-8", newline="\n") as f:
                f.write(raw)
        title = ""
        for ln in raw.split("\n"):
            if ln.startswith("# "):
                title = ln[2:].strip()
                break
        index.append({
            "url": url,
            "md_url": md_url(url),
            "slug": slug,
            "title": title,
            "source_file": ".cache/%s/pages/%s.md" % (HOST, safe),
            "local_path": local_path(slug),
            "source_hash": "sha256:" + hashlib.sha256(raw.encode("utf-8")).hexdigest(),
            "chars": len(raw),
        })
        print("%-46s %6d  %s" % (slug or "(root)", len(raw), title))

    with open(os.path.join(CACHE, "fetch.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(index, f, ensure_ascii=False, indent=1)
    total = sum(e["chars"] for e in index)
    print("pages: %d, total chars: %d" % (len(index), total))
    return 0


if __name__ == "__main__":
    sys.exit(main())
