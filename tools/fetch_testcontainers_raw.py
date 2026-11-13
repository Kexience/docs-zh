#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Fetch the upstream Markdown sources of java.testcontainers.org.

The site is built by MkDocs from testcontainers/testcontainers-java/docs/*.md
(102 files, 1:1 with the sitemap). The rendered HTML loses the fence language
markers, so the raw Markdown is fetched to recover them, together with the
files referenced by `<!--codeinclude-->` directives.

Outputs:
  .cache/java.testcontainers.org/raw/<safe>.md      upstream Markdown per page
  .cache/java.testcontainers.org/ghfiles/<safe>      files referenced by codeinclude
  .cache/java.testcontainers.org/raw.json            url -> cache file / sha
"""
import hashlib
import json
import os
import re
import sys
import time

import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, ".cache", HOST := "java.testcontainers.org")
RAW = os.path.join(CACHE, "raw")
GHFILES = os.path.join(CACHE, "ghfiles")
RAWJSON = os.path.join(CACHE, "raw.json")
REPO = "testcontainers/testcontainers-java"
RAWURL = "https://raw.githubusercontent.com/%s/main/" % REPO

CODEINCLUDE = re.compile(
    r"<!--\s*codeinclude\s*-->\s*\n(?P<body>.*?)<!--\s*/codeinclude\s*-->", re.S)
DIRECTIVE = re.compile(r"\[(?P<title>[^\]]*)\]\((?P<path>[^)]+)\)(?P<opts>[^\n]*)")


def safe_name(slug):
    return slug.replace("/", "__") if slug else "__root__"


def include_candidates(rel, base):
    """A codeinclude path may be relative to the doc dir or to the repo root."""
    out = []
    a = os.path.normpath(os.path.join(base, rel))
    if a not in out:
        out.append(a)
    if not rel.startswith(".."):
        b = os.path.normpath(rel)
        if b not in out:
            out.append(b)
    return out


def fetch(session, url):
    for attempt in range(3):
        try:
            r = session.get(url, timeout=60)
            r.raise_for_status()
            return r.text
        except Exception as e:  # noqa: BLE001
            print("  retry %d %s: %s" % (attempt + 1, url, e))
            time.sleep(2)
    return None


def main():
    os.makedirs(RAW, exist_ok=True)
    os.makedirs(GHFILES, exist_ok=True)
    s = requests.Session()
    s.headers["User-Agent"] = "docs-translator/1.0"

    fetch_json = json.load(open(os.path.join(CACHE, "fetch.json"), encoding="utf-8"))
    slugs = sorted(fetch_json.keys())
    meta = {}
    if os.path.exists(RAWJSON):
        meta = json.load(open(RAWJSON, encoding="utf-8"))

    for slug in slugs:
        safe = safe_name(slug)
        dest = os.path.join(RAW, safe + ".md")
        repo_path = meta.get(slug, {}).get("repo_path")
        if slug in meta and os.path.exists(dest) and "--refresh" not in sys.argv:
            text = open(dest, encoding="utf-8").read()
            if not repo_path:
                # probe which upstream path this page came from
                for cand in ("docs/%s.md" % (slug or "index"), "docs/%s/index.md" % slug):
                    r = s.head(RAWURL + cand, timeout=30)
                    if r.status_code == 200:
                        repo_path = cand
                        break
                meta[slug]["repo_path"] = repo_path
        else:
            # site path may map to docs/<slug>.md or docs/<slug>/index.md
            text = fetch(s, RAWURL + "docs/%s.md" % (slug or "index"))
            repo_path = "docs/%s.md" % (slug or "index")
            if text is None and slug:
                text = fetch(s, RAWURL + "docs/%s/index.md" % slug)
                repo_path = "docs/%s/index.md" % slug
            if text is None:
                print("  FAILED raw:", slug)
                continue
            with open(dest, "w", encoding="utf-8", newline="") as f:
                f.write(text)
            meta[slug] = {
                "url": fetch_json[slug]["url"],
                "file": safe + ".md",
                "repo_path": repo_path,
                "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            }
        time.sleep(0.1)

    # files referenced by codeinclude directives
    # the plugin resolves them relative to the doc dir or to the repo root
    wanted = set()
    for slug in slugs:
        p = os.path.join(RAW, safe_name(slug) + ".md")
        if not os.path.exists(p):
            continue
        text = open(p, encoding="utf-8").read()
        base = os.path.dirname(meta.get(slug, {}).get("repo_path") or ("docs/%s.md" % (slug or "index")))
        for m in CODEINCLUDE.finditer(text):
            for d in DIRECTIVE.finditer(m.group("body")):
                rel = d.group("path").strip()
                if rel.startswith("http"):
                    continue
                for cand in include_candidates(rel, base):
                    wanted.add(cand)
    print("codeinclude targets: %d" % len(wanted))

    files_meta = {}
    if os.path.exists(os.path.join(CACHE, "ghfiles.json")):
        files_meta = json.load(open(os.path.join(CACHE, "ghfiles.json"), encoding="utf-8"))

    for full in sorted(wanted):
        safe = full.replace("/", "__")
        dest = os.path.join(GHFILES, safe)
        if full in files_meta and os.path.exists(dest) and "--refresh" not in sys.argv:
            continue
        text = fetch(s, RAWURL + full)
        if text is None:
            print("  FAILED file:", full)
            continue
        with open(dest, "w", encoding="utf-8", newline="") as f:
            f.write(text)
        files_meta[full] = {"file": safe, "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest()}
        time.sleep(0.1)

    with open(RAWJSON, "w", encoding="utf-8", newline="\n") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    with open(os.path.join(CACHE, "ghfiles.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(files_meta, f, ensure_ascii=False, indent=1)
    print("raw pages: %d, referenced files: %d" % (len(meta), len(files_meta)))


if __name__ == "__main__":
    main()
