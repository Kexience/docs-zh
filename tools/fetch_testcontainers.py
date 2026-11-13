#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Fetch every page of https://java.testcontainers.org into a local cache.

The site is a MkDocs Material build of testcontainers/testcontainers-java.
There is no llms.txt, so the page list comes from sitemap.xml.

Outputs:
  .cache/java.testcontainers.org/sitemap.xml     the raw sitemap
  .cache/java.testcontainers.org/<safe>.html     one HTML page per URL
  .cache/java.testcontainers.org/fetch.json      url -> cache file / bytes

Re-running reuses the cache; pass --refresh to re-download.
"""
import json
import os
import re
import sys
import time

import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = "java.testcontainers.org"
CACHE = os.path.join(ROOT, ".cache", HOST)
SITEMAP = os.path.join(CACHE, "sitemap.xml")

UA = "docs-translator/1.0 (+https://github.com/)"


def safe_name(slug):
    """URL slug -> cache file stem (slashes become __)."""
    return slug.replace("/", "__") if slug else "__root__"


def main():
    os.makedirs(CACHE, exist_ok=True)
    s = requests.Session()
    s.headers["User-Agent"] = UA

    if os.path.exists(SITEMAP) and "--refresh-list" not in sys.argv:
        xml = open(SITEMAP, encoding="utf-8").read()
    else:
        r = s.get("https://%s/sitemap.xml" % HOST, timeout=60)
        r.raise_for_status()
        xml = r.text
        with open(SITEMAP, "w", encoding="utf-8", newline="\n") as f:
            f.write(xml)

    urls = re.findall(r"<loc>\s*(https?://[^<\s]+)\s*</loc>", xml)
    urls = [u for u in urls if u.startswith("https://%s/" % HOST)]
    # root first, then sitemap order
    urls = sorted(set(urls), key=lambda u: (u != "https://%s/" % HOST,))

    fetch = {}
    fpath = os.path.join(CACHE, "fetch.json")
    if os.path.exists(fpath) and "--refresh" not in sys.argv:
        fetch = json.load(open(fpath, encoding="utf-8"))

    for i, url in enumerate(urls, 1):
        slug = url.split("/", 3)[3] if len(url.split("/", 3)) > 3 else ""
        slug = slug.strip("/")
        safe = safe_name(slug)
        dest = os.path.join(CACHE, safe + ".html")
        if slug in fetch and os.path.exists(dest) and "--refresh" not in sys.argv:
            continue
        if os.path.exists(dest) and "--refresh" not in sys.argv:
            fetch[slug] = {"url": url, "file": safe + ".html", "bytes": os.path.getsize(dest)}
            continue
        for attempt in range(3):
            try:
                r = s.get(url, timeout=60)
                r.raise_for_status()
                with open(dest, "w", encoding="utf-8", newline="") as f:
                    f.write(r.text)
                fetch[slug] = {"url": url, "file": safe + ".html", "bytes": len(r.text)}
                break
            except Exception as e:  # noqa: BLE001
                print("  retry %d %s: %s" % (attempt + 1, url, e))
                time.sleep(2)
        else:
            print("  FAILED:", url)
        time.sleep(0.25)

    with open(fpath, "w", encoding="utf-8", newline="\n") as f:
        json.dump(fetch, f, ensure_ascii=False, indent=1)
    print("cached %d pages" % len(fetch))
    total = sum(v.get("bytes", 0) for v in fetch.values())
    print("total bytes: %d" % total)


if __name__ == "__main__":
    main()
