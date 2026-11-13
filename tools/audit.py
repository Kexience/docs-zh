#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Terminology consistency audit: report outlier terms with context lines."""
import json
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "openspec.dev", "unversioned", "docs")

# term -> group; each group lists the variants that must not mix
GROUPS = {
    "spec": ["规格", "规范"],
    "schema": ["模式", "架构"],
    "agent": ["智能体", "代理"],
    "apply": ["实施", "应用"],
    "artifact": ["产物", "构件", "制品"],
    "archive": ["归档", "存档"],
    "profile": ["配置档"],
    "skill": ["技能"],
}

# outliers worth showing in context
WATCH = ["规范", "架构", "代理", "应用", "构件", "制品", "存档"]


def main():
    files = []
    for dirpath, _, names in os.walk(OUT):
        for n in sorted(names):
            if n.endswith(".md"):
                files.append(os.path.join(dirpath, n))

    texts = {}
    for p in files:
        with open(p, encoding="utf-8") as f:
            texts[p] = f.read()

    lines = []
    lines.append("# 术语一致性审计\n")
    lines.append("共 %d 个文件\n" % len(files))

    lines.append("\n## 各组变体出现次数\n")
    lines.append("| 组 | 变体计数 |")
    lines.append("|---|---|")
    for g, terms in GROUPS.items():
        counts = []
        for t in terms:
            c = sum(v.count(t) for v in texts.values())
            counts.append("%s=%d" % (t, c))
        lines.append("| %s | %s |" % (g, "  ".join(counts)))

    lines.append("\n## 需人工判断的变体（附上下文）\n")
    for term in WATCH:
        hits = []
        for p, v in texts.items():
            for m in re.finditer(re.escape(term), v):
                a = max(0, m.start() - 45)
                b = min(len(v), m.end() + 45)
                ctx = v[a:b].replace("\n", " ")
                hits.append((os.path.relpath(p, OUT), ctx))
        if not hits:
            continue
        lines.append("\n### `%s`（%d 处）\n" % (term, len(hits)))
        for f, c in hits[:40]:
            lines.append("- `%s` … %s …" % (f, c))

    dest = os.path.join(ROOT, ".work", "audit.md")
    with open(dest, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    print("wrote", dest)


if __name__ == "__main__":
    main()
