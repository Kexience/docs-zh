# -*- coding: utf-8 -*-
import glob
import os
import re

import requests

r = requests.get("https://opencode.ai/docs/api/", timeout=60)
t = r.text
found = set()
for m in re.findall(r"[\"'(]([^\"'()\s]*openapi[^\"'()\s]*)", t, re.I):
    found.add(m)
for f in sorted(found):
    print("SPEC?", f)
print("--- inbound /docs/api links ---")
for p in glob.glob(".cache/opencode.ai/pages/*.md"):
    c = open(p, encoding="utf-8").read()
    n = len(re.findall(r"/docs/api", c))
    if n:
        print(os.path.basename(p), n)
