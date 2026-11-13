#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate the Chinese navigation index (index.md) from llms.txt.

The index is derived from the site's own llms.txt page list, so its structure
and link order mirror the live docs navigation.
"""
import hashlib
import os
import re
from datetime import datetime, timezone, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = "openspec.dev"
DOC_VERSION = "unversioned"
SRC = os.path.join(ROOT, ".cache", "openspec.dev", "llms.txt")
OUT = os.path.join(ROOT, "docs", HOST, DOC_VERSION, "index.md")
TZ = timezone(timedelta(hours=8))
NOW = datetime.now(TZ).replace(microsecond=0).isoformat()

GROUP_ZH = {
    "Start": "开始",
    "Customize": "定制",
    "Multi-repo (beta)": "多仓库（beta）",
    "Reference": "参考",
    "Schemas": "模式",
    "Configuration": "配置",
}

DESC_ZH = {
    "/docs/installation": "在你的机器上安装 openspec CLI、更新它、卸载它。",
    "/docs/setup": "把 OpenSpec 加入一个项目：运行 init，看看它写了什么，再做调整。",
    "/docs/quickstart": "你的第一个变更，从想法到归档，在新项目或已有项目里完成。",
    "/docs/upgrade-to-2": "OpenSpec 2.0 有哪些变化，以及如何把项目迁移过来。",
    "/docs/customize": "定制 OpenSpec 的各种选项。",
    "/docs/profiles": "选择安装哪些工作流。",
    "/docs/project-config": "用 config.yaml 里的几行配置，让工作流按你想要的方式规划变更。",
    "/docs/customize-schemas": "改变 OpenSpec 产出什么：产物、它们的顺序以及模板。",
    "/docs/stores": "规划跨仓库的变更：一个存储库，多个仓库。",
    "/docs/worksets": "在一个编辑器窗口里打开存储库和用它的仓库，让智能体同时看到两者。",
    "/docs/skills": "每个 OpenSpec 技能：参数、它创建什么、它如何回应。",
    "/docs/cli": "openspec 的终端命令。",
    "/docs/schemas": "所有可用的工作流模式及各自定义的产物。",
    "/docs/schemas/schema-yaml": "模式定义的每个字段，供阅读或编写模式时参考。",
    "/docs/schemas/spec-driven": "默认工作流的产物：它们的顺序、格式，以及它们生成的变更文件夹。",
    "/docs/configuration": "所有会改变 OpenSpec 行为的文件和设置，以及它们各自的位置。",
    "/docs/configuration/config-yaml": "openspec/config.yaml 的每个字段：这个项目用来规划的模式、context 和 rules。",
    "/docs/configuration/change-metadata": "随每个变更保存的元数据所支持的字段和校验规则。",
    "/docs/configuration/config-json": "config.json 的每个字段：openspec CLI 在你机器上的行为方式。",
    "/docs/supported-tools": "OpenSpec 支持哪些 AI 编码工具，以及如何调用各自的技能。",
    "/docs/glossary": "每个 OpenSpec 术语，一行一条。",
}

TITLE_ZH = {
    "/docs/installation": "安装",
    "/docs/setup": "配置你的项目",
    "/docs/quickstart": "快速入门",
    "/docs/upgrade-to-2": "升级到 2.0",
    "/docs/customize": "定制总览",
    "/docs/profiles": "配置档",
    "/docs/project-config": "项目配置",
    "/docs/customize-schemas": "模式",
    "/docs/stores": "存储库（beta）",
    "/docs/worksets": "工作集（beta）",
    "/docs/skills": "技能",
    "/docs/cli": "CLI",
    "/docs/schemas": "模式总览",
    "/docs/schemas/schema-yaml": "schema.yaml",
    "/docs/schemas/spec-driven": "spec-driven",
    "/docs/configuration": "配置总览",
    "/docs/configuration/config-yaml": "项目配置（config.yaml）",
    "/docs/configuration/change-metadata": "变更元数据（.openspec.yaml）",
    "/docs/configuration/config-json": "CLI 设置（config.json）",
    "/docs/supported-tools": "支持的工具",
    "/docs/glossary": "术语表",
}

LINK = re.compile(r"^(?P<indent>\s*)(?:-\s+)?\[(?P<title>[^\]]+)\]\((?P<url>/docs/[^)]*)\):?\s*(?P<desc>.*)$")
GROUP = re.compile(r"^-\s+\*\*(?P<name>.+?)\*\*\s*$")
BARE_GROUP = re.compile(r"^-\s+(?P<name>[A-Z][\w .()/-]+)$")


def local(url):
    slug = url[len("/docs/"):].strip("/")
    return "./docs/%s.md" % slug


def main():
    with open(SRC, "r", encoding="utf-8") as f:
        text = f.read()
    digest = "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()

    # Parse llms.txt into an ordered list of items:
    #   ("group", name)      top-level bold group -> "## name"
    #   ("subgroup", name)   bare "- Name" item that owns indented links
    #   ("link", url, indent)
    items = []
    for raw in text.split("\n"):
        if not raw.strip():
            continue
        g = GROUP.match(raw)
        if g:
            items.append(("group", g.group("name"), 0))
            continue
        m = LINK.match(raw)
        if m:
            indent = len(m.group("indent")) // 2
            items.append(("link", m.group("url"), indent))
            continue
        b = BARE_GROUP.match(raw)
        if b:
            name = b.group("name").strip()
            if name.lower() in ("documentation",):
                continue
            items.append(("subgroup", name, 0))

    out = []
    out.append("---")
    out.append("source_url: https://%s/llms.txt" % HOST)
    out.append("source_hash: %s" % digest)
    out.append("translated_at: %s" % NOW)
    out.append("translation_version: 1")
    out.append("---")
    out.append("")
    out.append("# OpenSpec 文档")
    out.append("")
    out.append("本目录是 openspec.dev 官方文档的中文译本，按站点的导航分组编排。")

    prev = None
    for kind, val, indent in items:
        if kind == "group":
            out.append("")
            out.append("## %s" % GROUP_ZH.get(val, val))
            out.append("")
        elif kind == "subgroup":
            out.append("- %s" % GROUP_ZH.get(val, val))
        else:
            url = val
            title = TITLE_ZH.get(url, url)
            desc = DESC_ZH.get(url, "")
            pad = "  " * indent
            entry = "%s- [%s](%s)" % (pad, title, local(url))
            if desc:
                entry += " —— %s" % desc
            out.append(entry)

    text_out = "\n".join(out).rstrip("\n") + "\n"
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(text_out)
    print("wrote", OUT)
    return text_out


if __name__ == "__main__":
    main()
