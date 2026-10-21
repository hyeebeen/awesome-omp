#!/usr/bin/env python3
"""One-shot research tool: turn research/raw/candidates-<date>.json into
registry rows appended to data/entries.yml. Never overwrites existing rows
(matched by repo, npm name or url). Gate (README「收录门槛」):
  - positive omp evidence line (strong name match, or bare "omp" next to
    agent words), not oh-my-posh / OpenMP noise
  - GitHub: not archived, pushed within 180 days, >= MIN_STARS stars, not
    can1357/* itself; npm: >= MIN_NPM downloads last month, not @oh-my-pi/*
Every imported row is evidence_type self-claimed with the matched line as
evidence, category from keywords (heuristic, reviewed by a human later).
Usage: import_candidates.py research/raw/candidates-2026-10-21.json [--dry]
"""
from __future__ import annotations
import json, re, sys, time, urllib.request, urllib.parse
import yaml
from common import DATA

MIN_STARS, MIN_NPM, SINCE = 5, 300, "2026-04-24"
STRONG = re.compile(r"oh[- ]?my[- ]?pi|ohmypi|can1357|omp\.sh|@oh-my-pi/", re.I)
BARE = re.compile(r"\bomp\b", re.I)
AGENTY = re.compile(r"\bpi\b|agent|coding|harness|claude|codex|opencode|llm", re.I)
NOISE = re.compile(r"posh|openmp|open-mpi|\.omp\.json|prompt theme", re.I)
RULES = [
    ("zh", re.compile(r"[\u4e00-\u9fff]|\bzh\b|-zh\b|chinese|i18n", re.I)),
    ("frontend", re.compile(r"desktop|\bgui\b|web ?ui|webui|android|\bios\b|mobile|electron|tauri|\bapp\b|phone|telegram|discord|slack|weixin|wechat|feishu", re.I)),
    ("editor", re.compile(r"vs ?code|neovim|nvim|\bzed\b|emacs|jetbrains|intellij|tmux|zellij|wezterm|ghostty|kitty|terminal", re.I)),
    ("marketplace", re.compile(r"marketplace", re.I)),
    ("mcp-lsp-dap", re.compile(r"\bmcp\b|\blsp\b|\bdap\b|language server|debugger", re.I)),
    ("memory", re.compile(r"memory|context|compaction|\brag\b|knowledge|recall", re.I)),
    ("provider", re.compile(r"provider|\bproxy\b|gateway|router|routing|ollama|vllm|llama\.cpp|openai-compatible|\bmodels?\b|subscription|oauth", re.I)),
    ("theme", re.compile(r"theme|statusline|status line|\bui\b|tui|render", re.I)),
    ("workflow", re.compile(r"subagent|sub-agent|orchestr|multi-agent|swarm|workflow|kanban|parallel|autonomous|loop|plan mode", re.I)),
    ("skill", re.compile(r"skill|rules?\b|prompt", re.I)),
    ("learning", re.compile(r"tutorial|course|guide|\bdocs?\b|handbook|lesson", re.I)),
    ("plugin", re.compile(r"plugin|\bpack\b|bundle|collection|toolkit|suite", re.I)),
]


def classify(text):
    for cat, rx in RULES:
        if rx.search(text):
            return cat
    return "extension"


def ok_evidence(ev, name, desc):
    if not ev or NOISE.search(ev) or NOISE.search(name) or NOISE.search(desc or ""):
        return False
    return bool(STRONG.search(ev) or (BARE.search(ev) and AGENTY.search(ev)))


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60]


def npm_monthly(name):
    try:
        return json.load(urllib.request.urlopen("https://api.npmjs.org/downloads/point/last-month/" + urllib.parse.quote(name, safe="@/"), timeout=20)).get("downloads") or 0
    except Exception:
        return 0


def main():
    src, dry = sys.argv[1], "--dry" in sys.argv
    date = re.search(r"(\d{4}-\d{2}-\d{2})", src).group(1)
    cands = json.load(open(src))["candidates"]
    doc = yaml.safe_load((DATA / "entries.yml").read_text(encoding="utf-8")) or {"entries": []}
    have_repo = {(e.get("repo") or "").lower() for e in doc["entries"]}
    have_npm = {(e.get("npm") or "").lower() for e in doc["entries"]}
    have_url = {e["url"].rstrip("/").lower() for e in doc["entries"]}
    ids = {e["id"] for e in doc["entries"]}
    new, by_repo = [], {}
    for c in cands.values():
        if c["source"] != "github" or not ok_evidence(c["evidence"], c["id"], c["description"]):
            continue
        if c["id"].lower().startswith("can1357/") or c["archived"] or c["pushed_at"] < SINCE or c["stars"] < MIN_STARS:
            continue
        if c["id"].lower() in have_repo or c["url"].lower() in have_url:
            continue
        text = " ".join([c["id"], c["description"] or "", " ".join(c.get("topics") or [])])
        e = {"id": slug(c["id"].split("/")[1]), "name": c["id"].split("/")[1], "url": c["url"], "category": classify(text),
             "kind": "repo", "repo": c["id"], "npm": None, "omp_support": "declared", "evidence_type": "self-claimed",
             "evidence": f"{c['evidence_where']}: {c['evidence']}", "summary": c["description"],
             "sources": [{"url": c["url"], "label": c["evidence_where"]}], "verified_at": date, "featured": False}
        if e["id"] in ids:
            e["id"] = slug(c["id"])
        ids.add(e["id"]); new.append(e); by_repo[c["id"].lower()] = e
    for c in cands.values():
        if c["source"] != "npm" or not ok_evidence(c["evidence"], c["id"], c["description"]):
            continue
        if c["id"].startswith("@oh-my-pi/") or c["id"] == "oh-my-pi" or c["id"].lower() in have_npm:
            continue
        m = re.search(r"github\.com/([^/]+/[^/#.]+)", c.get("repo") or "")
        repo = m.group(1) if m else None
        if repo and repo.lower() in by_repo:
            by_repo[repo.lower()]["npm"] = c["id"]
            continue
        if repo and repo.lower() in have_repo:
            continue
        if (c.get("date") or "") < SINCE:
            continue
        dl = npm_monthly(c["id"]); time.sleep(0.15)
        if dl < MIN_NPM:
            continue
        text = " ".join([c["id"], c["description"] or "", " ".join(c.get("keywords") or [])])
        e = {"id": slug(c["id"].lstrip("@")), "name": c["id"], "url": c["url"], "category": classify(text), "kind": "npm",
             "repo": repo, "npm": c["id"], "omp_support": "declared", "evidence_type": "self-claimed",
             "evidence": f"npm {c['evidence_where']}: {c['evidence']}", "summary": c["description"],
             "sources": [{"url": c["url"], "label": "npm"}] + ([{"url": f"https://github.com/{repo}", "label": "source"}] if repo else []),
             "verified_at": date, "featured": False}
        if e["id"] in ids or e["url"].lower() in have_url:
            continue
        ids.add(e["id"]); new.append(e)
    from collections import Counter
    print(f"import: {len(new)} new rows", Counter(e["category"] for e in new), Counter(e["kind"] for e in new))
    if not dry:
        doc["entries"] += new
        (DATA / "entries.yml").write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=1000), encoding="utf-8")


if __name__ == "__main__":
    main()
