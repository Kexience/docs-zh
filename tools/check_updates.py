#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Check upstream for changes against a host's _manifest.json.

维护用：只判断哪几页变了，不写译文、不改 _manifest.json（除非 --stamp）。

用法：
  python tools/check_updates.py                 # 检查所有站点
  python tools/check_updates.py openspec.dev    # 只查一个
  python tools/check_updates.py --stamp         # 顺带更新 INDEX.md 的「最近检查」

判定依据：重新抓 llms-full.txt → 用 prep.split_pages 切分 → 每页 source_hash
与 _manifest.json 里的比对。hash 算法与 prep.py 完全一致（sha256 of
"# Title\\n\\nbody\\n"），所以能直接对上。

退出码：0 = 全部未变；1 = 有变更（新页/改页/删页）。
"""
import hashlib
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
CACHE = os.path.join(ROOT, ".cache")
TZ = timezone(timedelta(hours=8))
NOW = datetime.now(TZ).replace(microsecond=0)
STAMP = NOW.isoformat()

sys.path.insert(0, os.path.join(ROOT, "tools"))
import prep  # noqa: E402

UA = {"User-Agent": "Mozilla/5.0 (docs-zh maintenance bot)"}


def fetch(url, dest):
    """下载到 dest；返回 (内容, 是否网络有变化之外的问题)。"""
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "wb") as f:
        f.write(data)
    return data.decode("utf-8", "replace")


def cached_or_fetch(url, dest, use_cache=False):
    if use_cache and os.path.exists(dest):
        return open(dest, "r", encoding="utf-8").read()
    return fetch(url, dest)


def url_for(host, slug):
    return "https://%s/docs/%s" % (host, slug)


def check_host(host, use_cache=False):
    hdir = os.path.join(DOCS, host)
    versions = [d for d in os.listdir(hdir) if os.path.isdir(os.path.join(hdir, d))]
    rc = 0
    for ver in sorted(versions):
        mpath = os.path.join(hdir, ver, "_manifest.json")
        if not os.path.exists(mpath):
            print("  [%s/%s] 无 _manifest.json，跳过" % (host, ver))
            continue
        m = json.load(open(mpath, encoding="utf-8"))
        src = m.get("source") or ""
        print("\n== %s / %s ==" % (host, ver))
        print("   源: %s" % (src or "(未记录)"))
        if "llms-full.txt" not in src:
            print("   ! 源不是 llms-full.txt，本脚本无法逐页比对，需人工处理")
            rc = 1
            continue
        dest = os.path.join(CACHE, host, "llms-full.txt")
        try:
            text = cached_or_fetch(src, dest, use_cache)
        except Exception as e:
            print("   ! 抓取失败: %s" % e)
            rc = 1
            continue
        pages = prep.split_pages(text)
        live = {}
        for p in pages:
            slug = p["slug"]
            body = "\n".join(p["lines"]).strip("\n")
            raw = "# %s\n\n%s\n" % (p["title"], body) if body else "# %s\n" % p["title"]
            live[url_for(host, slug)] = {
                "hash": "sha256:" + hashlib.sha256(raw.encode("utf-8")).hexdigest(),
                "chars": len(raw),
            }
        known = {p["url"]: p for p in m.get("pages", [])}
        changed = [u for u in live if u in known and known[u].get("source_hash") != live[u]["hash"]]
        added = [u for u in live if u not in known]
        removed = [u for u in known if u not in live]
        same = len([u for u in live if u in known and u not in changed])

        print("   上游 %d 页 / 清单 %d 页 → 未变 %d · 变更 %d · 新增 %d · 上游已删 %d"
              % (len(live), len(known), same, len(changed), len(added), len(removed)))
        for u in changed:
            print("     ~ 变更: %s (%d → %d 字符)" % (u, len(known[u].get("local_path", "")), live[u]["chars"]))
        for u in added:
            print("     + 新增: %s (%d 字符)" % (u, live[u]["chars"]))
        for u in removed:
            print("     - 删除: %s -> %s" % (u, known[u].get("local_path")))
        if not (changed or added or removed):
            print("   ✓ 与上游一致，无需重译")
        else:
            rc = 1
    return rc


def stamp_index(found):
    """把 INDEX.md 里对应行的「最近检查」更新为当前时间。"""
    path = os.path.join(ROOT, "INDEX.md")
    if not os.path.exists(path):
        return
    lines = open(path, encoding="utf-8").read().splitlines()
    out = []
    for ln in lines:
        cells = ln.split("|")
        if len(cells) >= 9 and cells[1].strip() in found:
            cells[6] = " %s " % STAMP
            ln = "|".join(cells)
        out.append(ln)
    open(path, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
    print("\n已回填 INDEX.md 最近检查: %s" % STAMP)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    use_cache = "--offline" in sys.argv
    hosts = args or sorted(d for d in os.listdir(DOCS) if os.path.isdir(os.path.join(DOCS, d)))
    rc = 0
    for h in hosts:
        rc |= check_host(h, use_cache)
    if "--stamp" in sys.argv:
        stamp_index(set(hosts))
    print("\n时间: %s" % STAMP)
    return rc


if __name__ == "__main__":
    sys.exit(main())
