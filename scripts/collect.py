#!/usr/bin/env python3
"""Ecosystem collector (research tool, report-only).

Searches GitHub repos and npm for omp / oh-my-pi candidates, fetches each
README / package description, and records the positive evidence line that
mentions omp. Output: research/raw/candidates-<date>.json. Never edits data/.
Needs `gh` (logged in). GitHub search is throttled to ~20 req/min.
"""
import json, re, subprocess, sys, time, urllib.request, urllib.parse, datetime, base64

TZ = datetime.timezone(datetime.timedelta(hours=8))
NOW = datetime.datetime.now(TZ)
GH_QUERIES = [
    "oh-my-pi", "\"oh my pi\"", "topic:oh-my-pi", "topic:omp", "omp coding agent",
    "omp extension", "omp plugin", "omp in:name pi", "omp-plugin", "omp marketplace",
    "can1357", "omp.sh", "omp agent in:name", "omp 插件", "omp 汉化", "oh-my-pi 中文",
]
NPM_QUERIES = ["oh-my-pi", "omp extension", "keywords:omp", "keywords:oh-my-pi", "omp plugin", "omp coding agent", "@oh-my-pi"]
# Positive evidence: explicit mention of the can1357 project, not oh-my-posh.
EVID = re.compile(r"(oh[- ]?my[- ]?pi|can1357|omp\.sh|\bomp\b(?![.-]?json)|@oh-my-pi/)", re.I)
NOISE = re.compile(r"oh-my-posh|openmp|open-mpi|\.omp\.json", re.I)

def gh(path, raw=False):
    args = ["gh", "api", path]
    if raw:
        args += ["-H", "Accept: application/vnd.github.raw"]
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode:
        return None
    return r.stdout if raw else json.loads(r.stdout)

def search_repos(q):
    out = []
    for page in (1, 2, 3):
        res = gh(f"search/repositories?q={urllib.parse.quote(q)}&per_page=100&page={page}")
        time.sleep(3)
        if not res:
            break
        out += res["items"]
        if len(res["items"]) < 100:
            break
    return out

def evidence(text):
    for line in text.splitlines():
        if EVID.search(line) and not NOISE.search(line):
            return line.strip()[:240]
    return None

def main():
    cands = {}
    for q in GH_QUERIES:
        for it in search_repos(q):
            fn = it["full_name"]
            if fn.lower() in ("can1357/oh-my-pi",):
                continue
            c = cands.setdefault("gh:" + fn, {"source": "github", "id": fn, "url": it["html_url"],
                "description": it["description"], "stars": it["stargazers_count"], "pushed_at": it["pushed_at"],
                "archived": it["archived"], "fork": it["fork"], "topics": it.get("topics", []), "queries": []})
            c["queries"].append(q)
        print(f"gh {q!r}: total {len(cands)}", file=sys.stderr)
    for q in NPM_QUERIES:
        for frm in (0, 250):
            u = "https://registry.npmjs.org/-/v1/search?" + urllib.parse.urlencode({"text": q, "size": 250, "from": frm})
            try:
                res = json.load(urllib.request.urlopen(u, timeout=30))
            except Exception as e:
                print("npm fail", q, e, file=sys.stderr); break
            for o in res["objects"]:
                p = o["package"]
                c = cands.setdefault("npm:" + p["name"], {"source": "npm", "id": p["name"],
                    "url": f"https://www.npmjs.com/package/{p['name']}", "description": p.get("description"),
                    "version": p.get("version"), "date": p.get("date"), "repo": (p.get("links") or {}).get("repository"),
                    "keywords": p.get("keywords", []), "queries": []})
                c["queries"].append(q)
            if len(res["objects"]) < 250:
                break
            time.sleep(1)
        print(f"npm {q!r}: total {len(cands)}", file=sys.stderr)
    # evidence pass
    for k, c in cands.items():
        text = " ".join([c.get("description") or "", " ".join(c.get("topics") or c.get("keywords") or [])])
        ev = evidence(text) if not NOISE.search(text) else None
        where = "description" if ev else None
        if not ev and c["source"] == "github" and not c["archived"]:
            readme = gh(f"repos/{c['id']}/readme", raw=True) or ""
            ev = evidence(readme); where = "README" if ev else None
            time.sleep(0.3)
        c["evidence"] = ev; c["evidence_where"] = where
    out = f"research/raw/candidates-{NOW:%Y-%m-%d}.json"
    json.dump({"collected_at": NOW.isoformat(timespec="minutes"), "gh_queries": GH_QUERIES, "npm_queries": NPM_QUERIES,
               "candidates": cands}, open(out, "w"), ensure_ascii=False, indent=1)
    print(out, len(cands), sum(1 for c in cands.values() if c["evidence"]), file=sys.stderr)

if __name__ == "__main__":
    main()
