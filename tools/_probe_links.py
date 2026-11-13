# -*- coding: utf-8 -*-
import collections
import glob
import re

links = collections.Counter()
for p in glob.glob(".cache/opencode.ai/pages/*.md"):
    c = open(p, encoding="utf-8").read()
    for m in re.finditer(r"\]\(([^)\s]+)\)", c):
        t = m.group(1)
        links[t.split("#")[0]] += 1
print("distinct link targets:", len(links))
kinds = collections.Counter()
for t, n in links.items():
    if t.startswith("https://opencode.ai"):
        kinds["abs-opencode"] += n
    elif t.startswith("/docs"):
        kinds["root-docs"] += n
    elif t.startswith("/"):
        kinds["root-other"] += n
    elif t.startswith("#"):
        kinds["anchor"] += n
    elif t.startswith("http"):
        kinds["external"] += n
    elif t.startswith("mailto"):
        kinds["mailto"] += n
    else:
        kinds["relative"] += n
print(kinds)
print("--- root-other samples ---")
for t, n in sorted(links.items(), key=lambda x: -x[1]):
    if t.startswith("/") and not t.startswith("/docs"):
        print(n, t)
print("--- relative samples ---")
for t, n in sorted(links.items(), key=lambda x: -x[1]):
    if not t.startswith(("/", "#", "http", "mailto")):
        print(n, t)
