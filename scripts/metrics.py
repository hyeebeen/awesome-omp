#!/usr/bin/env python3
"""Fetch live metrics for entries -> data/metrics.json (the ONLY writer of numbers).

GitHub: stars, pushed_at, archived (via `gh api` or GITHUB_TOKEN). npm: last-month
downloads. Timestamp in Asia/Shanghai. Run before build.py; commit both.
"""
from __future__ import annotations
import datetime, json, os, subprocess, sys, time, urllib.request
from common import DATA, load_all

TZ = datetime.timezone(datetime.timedelta(hours=8))


def gh(path):
    r = subprocess.run(["gh", "api", path], capture_output=True, text=True)
    return json.loads(r.stdout) if r.returncode == 0 else None


def npm_monthly(name):
    try:
        u = "https://api.npmjs.org/downloads/point/last-month/" + name
        return json.load(urllib.request.urlopen(u, timeout=20)).get("downloads")
    except Exception:
        return None


def main():
    items = {}
    for e in load_all()["entries"]:
        it = {}
        if e.get("repo"):
            r = gh(f"repos/{e['repo']}")
            if r:
                it.update(stars=r["stargazers_count"], archived=r["archived"], pushed_at=r["pushed_at"][:10])
            else:
                it.update(error="repo not reachable")
            time.sleep(0.2)
        if e.get("npm"):
            it["npm_monthly"] = npm_monthly(e["npm"])
        if it:
            items[e["id"]] = it
    out = {"fetched_at": datetime.datetime.now(TZ).strftime("%Y-%m-%d %H:%M"), "items": dict(sorted(items.items()))}
    (DATA / "metrics.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"metrics: {len(items)} items, fetched_at {out['fetched_at']}")


if __name__ == "__main__":
    sys.exit(main())
