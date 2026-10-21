#!/usr/bin/env python3
"""Weekly REPORT-ONLY recheck. Never edits data/.

Checks: latest omp release vs the newest version in data/milestones.yml;
each repo entry: reachable, archived, pushed within 180 days, omp evidence
still present in README/description (declared entries only).
Output: Markdown report (stdout or --out). Exit 0 = nothing to report,
2 = suggestions found (with --fail-on-change), 1 = script error.
Human must confirm every suggestion (renamed repos, monorepos and
README rewrites cause false positives).
"""
from __future__ import annotations
import argparse, datetime, re, subprocess, json, sys, time
from common import load_all

STRONG = re.compile(r"oh[- ]?my[- ]?pi|ohmypi|can1357|omp\.sh|@oh-my-pi/|\bomp\b", re.I)
TZ = datetime.timezone(datetime.timedelta(hours=8))


def gh(path, raw=False):
    a = ["gh", "api", path] + (["-H", "Accept: application/vnd.github.raw"] if raw else [])
    r = subprocess.run(a, capture_output=True, text=True)
    if r.returncode:
        return None
    return r.stdout if raw else json.loads(r.stdout)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out"); ap.add_argument("--fail-on-change", action="store_true"); ap.add_argument("--limit", type=int)
    a = ap.parse_args()
    d = load_all()
    now = datetime.datetime.now(TZ)
    since = (now - datetime.timedelta(days=180)).strftime("%Y-%m-%d")
    lines, sugg = [f"# Recheck report {now:%Y-%m-%d %H:%M} (UTC+8)", ""], 0
    rel = gh("repos/can1357/oh-my-pi/releases/latest")
    known = sorted((m for m in d["milestones"] if m.get("version")), key=lambda m: m["date"])[-1]["version"]
    if rel and rel["tag_name"] != known:
        sugg += 1
        lines.append(f"- omp latest release is **{rel['tag_name']}** ({rel['published_at']}), data says {known}. Update milestones/facts if notable.")
    rows = [e for e in d["entries"] if e.get("repo")][: a.limit]
    for e in rows:
        r = gh(f"repos/{e['repo']}")
        time.sleep(0.2)
        if not r:
            sugg += 1; lines.append(f"- `{e['id']}`: repo {e['repo']} not reachable (deleted/renamed/private?)"); continue
        if r["full_name"].lower() != e["repo"].lower():
            sugg += 1; lines.append(f"- `{e['id']}`: renamed to {r['full_name']}")
        if r["archived"]:
            sugg += 1; lines.append(f"- `{e['id']}`: archived")
        if r["pushed_at"][:10] < since and e["category"] not in ("adjacent",):
            sugg += 1; lines.append(f"- `{e['id']}`: no push since {r['pushed_at'][:10]} (gate: 180 days)")
        if e["omp_support"] == "declared":
            text = (r.get("description") or "") + " " + " ".join(r.get("topics") or [])
            if not STRONG.search(text):
                readme = gh(f"repos/{e['repo']}/readme", raw=True) or ""
                if not STRONG.search(readme):
                    sugg += 1; lines.append(f"- `{e['id']}`: omp evidence no longer found in description/README")
    lines += ["", f"Checked {len(rows)} repo entries; {sugg} suggestion(s). Report only — confirm by hand before editing data/."]
    out = "\n".join(lines) + "\n"
    if a.out:
        open(a.out, "w").write(out)
    print(out)
    return 2 if (sugg and a.fail_on_change) else 0


if __name__ == "__main__":
    sys.exit(main())
