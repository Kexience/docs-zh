#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Upstream watcher：每周检查三个文档站有没有更新，只报告，不改译文。

每个站点用各自可行的探测方式：
  opencode.ai             → 逐页取 `<canonical-url>.md`（上游对每页都提供 Markdown 镜像），比 sha256
  java.testcontainers.org → 解析 sitemap.xml，比每个 URL 的 <lastmod>
  openspec.dev            → 抓 llms-full.txt，用 prep.split_pages 逐页比 source_hash

基线存在 `.cache/upstream_state.json`（.cache 已 gitignore）。首次运行只建基线，不报变更。

用法：
  python tools/watch_upstream.py            # 人话输出
  python tools/watch_upstream.py --json     # 机器可读，给 cron 用
  python tools/watch_upstream.py --reset    # 丢掉基线重建

退出码：0 = 无变化；1 = 有变化或抓取失败。
"""
import hashlib
import json
import os
import re
import sys
import urllib.request
import urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
STATE = os.path.join(ROOT, ".cache", "upstream_state.json")
UA = {"User-Agent": "Mozilla/5.0 (docs-zh maintenance bot)"}

sys.path.insert(0, os.path.join(ROOT, "tools"))
import prep  # noqa: E402

LLMSFULL_HOSTS = {"openspec.dev": "https://openspec.dev/llms-full.txt"}
SITEMAP_HOSTS = {"java.testcontainers.org": "https://java.testcontainers.org/sitemap.xml"}
MD_MIRROR_HOSTS = {"opencode.ai"}


def get(url, timeout=60):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def sha(data):
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def manifest(host):
    hdir = os.path.join(DOCS, host)
    if not os.path.isdir(hdir):
        return None, None
    vers = sorted(d for d in os.listdir(hdir) if os.path.isdir(os.path.join(hdir, d)))
    if not vers:
        return None, None
    ver = vers[-1]
    p = os.path.join(hdir, ver, "_manifest.json")
    if not os.path.exists(p):
        return ver, None
    return ver, json.load(open(p, encoding="utf-8"))


def md_mirror_pages(host, errs):
    """每页取 <url>.md，返回 {url: hash}。"""
    ver, m = manifest(host)
    if not m:
        errs.append("%s: 无 _manifest.json" % host)
        return {}
    out, skipped = {}, []
    for p in m.get("pages", []):
        url = p["url"].rstrip("/")
        target = url + ".md"
        try:
            data = get(target, timeout=45)
        except urllib.error.HTTPError as e:
            if e.code in (404, 410, 403):
                skipped.append((url, e.code))
                continue
            errs.append("%s: %s → HTTP %s" % (host, target, e.code))
            continue
        except Exception as e:
            errs.append("%s: %s → %s: %s" % (host, target, type(e).__name__, e))
            continue
        out[url] = sha(data)
    if skipped:
        print_ = "  (跳过 %d 页无 Markdown 镜像: %s)" % (len(skipped), ", ".join(u for u, _ in skipped[:3]))
        out.setdefault("__note__", print_)
    return out


def sitemap_pages(host, errs):
    """解析 sitemap，返回 {url: lastmod}。"""
    url = SITEMAP_HOSTS[host]
    try:
        xml = get(url).decode("utf-8", "replace")
    except Exception as e:
        errs.append("%s: sitemap 抓取失败 %s: %s" % (host, type(e).__name__, e))
        return {}
    out = {}
    for blk in re.findall(r"<url>(.*?)</url>", xml, re.S):
        loc = re.search(r"<loc>(.*?)</loc>", blk, re.S)
        lm = re.search(r"<lastmod>(.*?)</lastmod>", blk, re.S)
        if loc:
            out[loc.group(1).strip().rstrip("/")] = (lm.group(1).strip() if lm else "")
    return out


def llmsfull_pages(host, errs):
    """llms-full.txt 逐页 hash，键名与 check_updates.py 一致（含 /docs/ 前缀）。"""
    url = LLMSFULL_HOSTS[host]
    try:
        text = get(url).decode("utf-8", "replace")
    except Exception as e:
        errs.append("%s: llms-full 抓取失败 %s: %s" % (host, type(e).__name__, e))
        return {}
    out = {}
    for p in prep.split_pages(text):
        body = "\n".join(p["lines"]).strip("\n")
        raw = "# %s\n\n%s\n" % (p["title"], body) if body else "# %s\n" % p["title"]
        out["https://%s/%s" % (host, p["slug"].lstrip("/"))] = sha(raw)
    return out


def collect():
    errs, snap = [], {}
    for host in MD_MIRROR_HOSTS:
        d = md_mirror_pages(host, errs)
        d.pop("__note__", None)
        snap[host] = d
    for host in SITEMAP_HOSTS:
        snap[host] = sitemap_pages(host, errs)
    for host in LLMSFULL_HOSTS:
        snap[host] = llmsfull_pages(host, errs)
    return snap, errs


def main():
    as_json = "--json" in sys.argv
    if "--reset" in sys.argv and os.path.exists(STATE):
        os.remove(STATE)
    first_run = not os.path.exists(STATE)
    prev = {} if first_run else json.load(open(STATE, encoding="utf-8"))

    snap, errs = collect()
    report = {"checked_at": None, "first_run": first_run, "hosts": {}, "errors": errs}
    import datetime
    report["checked_at"] = datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()

    changed_any = bool(errs)
    for host, cur in sorted(snap.items()):
        old = (prev or {}).get(host, {})
        if first_run or not old:
            report["hosts"][host] = {"baseline": len(cur), "changed": [], "added": [], "removed": []}
            continue
        changed = sorted(u for u in cur if u in old and old[u] != cur[u])
        added = sorted(u for u in cur if u not in old)
        removed = sorted(u for u in old if u not in cur)
        report["hosts"][host] = {"baseline": len(cur), "changed": changed,
                                 "added": added, "removed": removed}
        if changed or added or removed:
            changed_any = True

    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    json.dump(snap, open(STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=0)

    if as_json:
        print(json.dumps(report, ensure_ascii=False, indent=1))
    else:
        print("上游文档检查 %s%s" % (report["checked_at"], "（首次运行，仅建基线）" if first_run else ""))
        for host, r in sorted(report["hosts"].items()):
            if first_run:
                print("- %-26s 基线 %d 页" % (host, r["baseline"]))
                continue
            n = len(r["changed"]) + len(r["added"]) + len(r["removed"])
            print("- %-26s %s（追踪 %d 页）" % (
                host, "✓ 无变化" if not n else
                "变更 %d / 新增 %d / 已删 %d" % (len(r["changed"]), len(r["added"]), len(r["removed"])),
                r["baseline"]))
            for u in r["changed"]:
                print("    ~ %s" % u)
            for u in r["added"]:
                print("    + %s" % u)
            for u in r["removed"]:
                print("    - %s" % u)
        for e in errs:
            print("! %s" % e)
    return 1 if changed_any else 0


if __name__ == "__main__":
    sys.exit(main())
