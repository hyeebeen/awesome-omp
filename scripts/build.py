#!/usr/bin/env python3
"""Deterministic generator. data/*.yml (+ data/metrics.json) is the only source.

Outputs (no wall-clock timestamps -> idempotent):
  data/awesome-omp.json   full export for agents
  llms.txt                LLM entry point (whole file)
  docs/ecosystem.md       registry tables, one stable anchor per entry id
  docs/pi-compat.md       Pi vs omp compatibility matrix
  docs/timeline.md        milestones
  README.md / README.en.md  blocks between <!-- BEGIN GENERATED: X --> ... <!-- END GENERATED: X -->
     X in: top3, featured (grouped by task), misconceptions, lore, stats

Usage: build.py [--check]   (--check: exit 1 if any output would change)
"""
from __future__ import annotations
import json, re, sys
from collections import Counter
from common import REPO, load_all, load_metrics
import validate

CATS = [  # reader-task order: understand -> start -> extend -> integrate -> work -> learn
    ("core", "omp 本体", "omp itself"),
    ("doc", "官方文档导读", "Official docs"),
    ("provider", "模型与 provider", "Models & providers"),
    ("extension", "扩展", "Extensions"),
    ("plugin", "插件 / 扩展合集", "Plugins & bundles"),
    ("marketplace", "插件市场源", "Marketplaces"),
    ("skill", "Skills 与规则", "Skills & rules"),
    ("theme", "主题与界面", "Themes & UI"),
    ("mcp-lsp-dap", "MCP / LSP / DAP", "MCP / LSP / DAP"),
    ("memory", "记忆与上下文", "Memory & context"),
    ("frontend", "桌面 / Web / 移动前端", "Desktop, web & mobile frontends"),
    ("editor", "编辑器与终端集成", "Editor & terminal integration"),
    ("workflow", "工作流与多 agent", "Workflows & multi-agent"),
    ("learning", "文章 / 教程 / 讨论", "Articles, tutorials & discussions"),
    ("zh", "中文社区", "Chinese community"),
    ("adjacent", "相邻清单与项目", "Adjacent lists & projects"),
]
TASKS = [  # README picks grouped by what the reader wants to do (entries.yml `task`)
    ("understand", "想弄懂原理", "Understand how it works"),
    ("extend", "想写扩展或接插件", "Write extensions or add plugins"),
    ("models", "想配模型和工作流", "Set up models and workflows"),
    ("embed", "想换界面或嵌进自己的工具", "Use another UI or embed omp"),
    ("compare", "想看社区评价和选型", "Community views and comparisons"),
    ("zh", "中文读者", "Chinese readers"),
]
CAT_ZH = {c: z for c, z, _ in CATS}
CAT_EN = {c: e for c, _, e in CATS}
SUPPORT = {
    "native": ("omp 官方", "official omp"),
    "declared": ("项目声明支持 omp", "declares omp support"),
    "pi-compat-tested": ("Pi 包，已在 omp 实测加载", "Pi package, load-tested on omp"),
    "pi-compat-unverified": ("Pi 包，omp 上未验证", "Pi package, untested on omp"),
    "about": ("内容关于 omp", "about omp"),
    "unsupported": ("不支持", "unsupported"),
    "unknown": ("未确认", "unknown"),
}
EVID = {"verified": "已验证", "self-claimed": "自述", "tested": "实测", "inferred": "推断"}


def clip(s, n):
    """Cut to n chars without leaving a half URL behind."""
    s = s or ""
    if len(s) <= n:
        return s
    return re.sub(r"\S*https?://\S*$", "", s[:n]).rstrip() + "…"


def esc(s):
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)|</?(?:img|a|p|br|div|h[1-6]|picture|source|span|b|strong|em|sub|sup|details|summary|code|kbd|table|tr|td|th|center)\b[^>]*>", " ", s or "")
    s = re.sub(r"\s+", " ", s.replace("|", "\\|")).strip()
    return re.sub(r"(?<![(<])(https?://[^\s)）]+)", r"<\1>", s)


def metric(e, m):
    it = m["items"].get(e["id"]) or {}
    parts = []
    if it.get("stars") is not None:
        parts.append(f"★{it['stars']:,}")
    if it.get("npm_monthly") is not None:
        parts.append(f"⬇{it['npm_monthly']:,}/月")
    if it.get("archived"):
        parts.append("已归档")
    return " ".join(parts) or "—"


def sort_key(e, m):
    it = m["items"].get(e["id"]) or {}
    return (not e.get("featured"), -(it.get("stars") or 0) - (it.get("npm_monthly") or 0) / 100, e["name"].lower())


def ecosystem(d, m):
    out = ["# 生态登记（全量） / Ecosystem registry", "",
           "> 由 `scripts/build.py` 从 `data/entries.yml` 生成，请勿手改。每行开头的锚点 `#<id>` 永久有效。",
           f"> 指标（★、npm 月下载）由 `scripts/metrics.py` 抓取，抓取时间：{m.get('fetched_at') or '未抓取'}（Asia/Shanghai）。", "",
           "「omp 支持」列的含义见文末。精选在 [README](../README.md#精选)。", ""]
    by = {}
    for e in d["entries"]:
        by.setdefault(e["category"], []).append(e)
    out.append("| 分类 | 条目 |\n|---|---|")
    for c, z, en in CATS:
        if c in by:
            out.append(f"| [{z}](#cat-{c}) | {len(by[c])} |")
    out.append("")
    for c, z, en in CATS:
        if c not in by:
            continue
        out += [f'<a id="cat-{c}"></a>', "", f"## {z} / {en}", "",
                "| 名称 | 说明 | omp 支持 | 证据 | 指标 | 核实 |", "|---|---|---|---|---|---|"]
        for e in sorted(by[c], key=lambda e: sort_key(e, m)):
            star = " ⭐" if e.get("featured") else ""
            desc = e.get("why") or e.get("summary") or ""
            ev = f"{EVID[e['evidence_type']]}：{e['evidence']}"
            src = " ".join(f"[{i + 1}]({s['url']})" for i, s in enumerate(e["sources"]))
            out.append(f'| <a id="{e["id"]}"></a>[{esc(e["name"])}]({e["url"]}){star} | {esc(clip(desc, 200))} | '
                       f'{SUPPORT[e["omp_support"]][0]} | {esc(clip(ev, 220))} {src} | {metric(e, m)} | {e["verified_at"]} |')
        out.append("")
    out += ["## omp 支持的含义", ""]
    out += [f"- **{z}**（`{k}`）：{en}" for k, (z, en) in SUPPORT.items()]
    out += ["", "证据类型：已验证＝官方文档/源码/API 可见；自述＝项目自己的说法（README 或描述里提到 omp）；"
            "实测＝本仓库 [examples/RUNLOG.md](../examples/RUNLOG.md) 跑过；推断＝我们的判断。", ""]
    return "\n".join(out)


def compat(d):
    out = ["# Pi 与 omp 兼容矩阵 / Pi vs omp compatibility", "",
           "> 由 `scripts/build.py` 从 `data/compat.yml` 生成，请勿手改。", "",
           "| 项目 | Pi | omp | 结论 | 证据 |", "|---|---|---|---|---|"]
    lab = {"same": "相同", "compatible": "兼容", "partial": "部分兼容", "different": "不同", "omp-only": "omp 独有", "unknown": "未确认"}
    for r in d["compat"]:
        src = "；".join(f"[{esc(s.get('label') or 'source')}]({s['url']})" for s in r["sources"])
        out.append(f'| <a id="{r["id"]}"></a>{esc(r["item"])} | {esc(r["pi"])} | {esc(r["omp"])} | {lab[r["status"]]} | {EVID[r["evidence_type"]]}：{src} |')
    c = Counter(r["status"] for r in d["compat"])
    out += ["", "汇总：" + "，".join(f"{lab[k]} {v}" for k, v in sorted(c.items())) + "。", "",
            "结论：Pi 包**可能**在 omp 上能用，但要逐个验证；发现目录和配置根目录不同，Claude Code 插件市场是 omp 独有。", ""]
    return "\n".join(out)


def timeline(d):
    out = ["# 时间线 / Timeline", "", "> 由 `scripts/build.py` 从 `data/milestones.yml` 生成。日期为 Asia/Shanghai。", "",
           "| 日期 | 版本 | 事件 | 证据 |", "|---|---|---|---|"]
    for x in sorted(d["milestones"], key=lambda x: x["date"]):
        src = " ".join(f"[{i + 1}]({s['url']})" for i, s in enumerate(x["sources"]))
        out.append(f"| {x['date']} | {x.get('version') or '—'} | {esc(x['what'])} | {EVID[x['evidence_type']]} {src} |")
    return "\n".join(out) + "\n"


def blocks(d, m, en=False):
    feat = sorted([e for e in d["entries"] if e.get("featured")], key=lambda e: e["rank"])
    w = "why_en" if en else "why"
    top3 = "\n".join(f"{e['rank']}. **[{e['name']}]({e['url']})**{': ' if en else '：'}{e[w]}" for e in feat[:3])
    groups = []
    for key, zh, eng in TASKS:
        items = [e for e in feat if e.get("task") == key]
        if not items:
            continue
        groups += [f"### {eng if en else zh}", ""]
        for e in items:
            cat = CAT_EN[e["category"]] if en else CAT_ZH[e["category"]]
            if en:
                groups.append(f"- **[{e['name']}]({e['url']})** ({cat}) — {e[w]} [details](docs/ecosystem.md#{e['id']})")
            else:
                groups.append(f"- **[{e['name']}]({e['url']})**（{cat}）：{e[w]} [详情](docs/ecosystem.md#{e['id']})")
        groups.append("")
    featured = "\n".join(groups).rstrip()
    mis = []
    for i, x in enumerate(d["misconceptions"], 1):
        src = " ".join(f"[{s.get('label') or 'source'}]({s['url']})" for s in x["sources"])
        if en:
            mis.append(f"{i}. **Myth:** {x['myth_en']}\n   **Fact:** {x['fact_en']} ({src})")
        else:
            mis.append(f"{i}. **误解：**{x['myth']}\n   **事实：**{x['fact']}（{src}）")
    misc = "\n".join(mis)
    by = Counter(e["category"] for e in d["entries"])
    sup = Counter(e["omp_support"] for e in d["entries"])
    if en:
        stats = (f"{len(d['entries'])} entries in {len(by)} categories · {len(feat)} featured · "
                 f"{len(d['misconceptions'])} misconceptions · {len(d['compat'])} compat rows · "
                 f"{sup.get('native', 0)} official, {sup.get('declared', 0)} declare omp support, "
                 f"{sup.get('pi-compat-tested', 0)} Pi packages load-tested on omp. Metrics fetched {m.get('fetched_at') or 'n/a'} (UTC+8).")
    else:
        stats = (f"共 {len(d['entries'])} 条，{len(by)} 个分类；精选 {len(feat)} 条；常见误解 {len(d['misconceptions'])} 条；"
                 f"兼容矩阵 {len(d['compat'])} 行。其中 omp 官方 {sup.get('native', 0)} 条，项目声明支持 omp {sup.get('declared', 0)} 条，"
                 f"Pi 包在 omp 实测加载 {sup.get('pi-compat-tested', 0)} 条。指标抓取于 {m.get('fetched_at') or '未抓取'}（Asia/Shanghai）。")
    lore = []
    for x in sorted([x for x in d["milestones"] if x.get("lore")], key=lambda x: x["date"]):
        src = x["sources"][0]["url"]
        what = x["what_en"] if en else x["what"]
        if en:
            lore.append(f"- **{x['date']}** · {what} ([{x['evidence_type']}]({src}))")
        else:
            lore.append(f"- **{x['date']}** · {what}（[{EVID[x['evidence_type']]}]({src})）")
    return {"top3": top3, "featured": featured, "misconceptions": misc, "lore": "\n".join(lore), "stats": stats}


def replace_blocks(text, bl, path):
    for k, v in bl.items():
        pat = re.compile(rf"(<!-- BEGIN GENERATED: {k} -->)(.*?)(<!-- END GENERATED: {k} -->)", re.S)
        if not pat.search(text):
            raise SystemExit(f"{path}: missing marker {k}")
        inline = k == "stats"
        text = pat.sub(lambda mm: mm.group(1) + (v if inline else "\n" + v + "\n") + mm.group(3), text)
    return text


def llms(d, m):
    feat = sorted([e for e in d["entries"] if e.get("featured")], key=lambda e: e["rank"])
    out = ["# awesome-omp", "",
           "> Curated, source-checked research list for omp (can1357/oh-my-pi), a coding agent forked from Pi. "
           "Not oh-my-posh, not the npm package `oh-my-pi`, not OpenMP.", "",
           f"Counts: {len(d['entries'])} entries, {len(feat)} featured, {len(d['misconceptions'])} misconceptions, {len(d['compat'])} Pi-vs-omp compat rows. "
           f"Metrics fetched {m.get('fetched_at') or 'n/a'} (UTC+8). Data rule: every entry has sources, evidence_type (verified|self-claimed|tested|inferred) and verified_at.", "",
           "## Data", "",
           "- [data/awesome-omp.json](data/awesome-omp.json): full export (entries, misconceptions, milestones, compat, metrics)",
           "- [data/schema.json](data/schema.json): JSON Schema; field meanings in [AGENTS.md](AGENTS.md)", "",
           "## Core docs", "",
           "- [docs/deep-dive.md](docs/deep-dive.md): what omp is, architecture, key mechanisms with source paths",
           "- [docs/why.md](docs/why.md): why omp exists, community voices, outlook",
           "- [docs/practice.md](docs/practice.md): install, config, extensions, marketplace, safety",
           "- [docs/pi-compat.md](docs/pi-compat.md): Pi vs omp compatibility matrix",
           "- [docs/ecosystem.md](docs/ecosystem.md): full registry with anchors",
           "- [docs/timeline.md](docs/timeline.md): milestones",
           "- [examples/RUNLOG.md](examples/RUNLOG.md): offline load tests of a minimal extension, marketplace and a Pi package", "",
           "## Featured", ""]
    out += [f"- [{e['name']}]({e['url']}): {e['why_en']}" for e in feat]
    out += ["", "## Misconceptions", ""]
    out += [f"- {x['myth_en']} -> {x['fact_en']}" for x in d["misconceptions"]]
    return "\n".join(out) + "\n"


def main():
    check = "--check" in sys.argv
    errs = validate.errors()
    if errs:
        print("\n".join(errs)); sys.exit(1)
    d, m = load_all(), load_metrics()
    outs = {
        "data/awesome-omp.json": json.dumps({**d, "metrics": m}, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
        "llms.txt": llms(d, m),
        "docs/ecosystem.md": ecosystem(d, m),
        "docs/pi-compat.md": compat(d),
        "docs/timeline.md": timeline(d),
    }
    for f, en in (("README.md", False), ("README.en.md", True)):
        p = REPO / f
        if p.exists():
            outs[f] = replace_blocks(p.read_text(encoding="utf-8"), blocks(d, m, en), f)
    changed = []
    for f, txt in outs.items():
        p = REPO / f
        if not p.exists() or p.read_text(encoding="utf-8") != txt:
            changed.append(f)
            if not check:
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(txt, encoding="utf-8")
    if check and changed:
        print("out of date:", ", ".join(changed)); sys.exit(1)
    print(("check ok" if check else "built") + f": {len(outs)} files, changed {len(changed)}")


if __name__ == "__main__":
    main()
