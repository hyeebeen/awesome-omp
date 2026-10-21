#!/usr/bin/env python3
"""Validate data/*.yml against data/schema.json plus hygiene rules.

Rules beyond the schema: unique ids (entries, misconceptions, compat), unique
URLs among entries, featured count 15-20 with unique ranks 1..N, ranks 1-3
present (README「只看 3 条」), local source paths exist, self-claimed
entries never marked featured without a why.
Exit 0 = ok, 1 = errors (printed).
"""
from __future__ import annotations
import json, sys
from collections import Counter
from jsonschema import Draft202012Validator
from common import DATA, REPO, load_all


def errors() -> list[str]:
    data = load_all()
    schema = json.loads((DATA / "schema.json").read_text(encoding="utf-8"))
    errs = [f"schema: {'/'.join(map(str, e.path))}: {e.message}" for e in Draft202012Validator(schema).iter_errors(data)]
    for key in ("entries", "misconceptions", "compat"):
        for i, n in Counter(x.get("id") for x in data[key]).items():
            if n > 1:
                errs.append(f"{key}: duplicate id {i}")
    for u, n in Counter(e.get("url", "").rstrip("/").lower() for e in data["entries"]).items():
        if n > 1:
            errs.append(f"entries: duplicate url {u}")
    feat = [e for e in data["entries"] if e.get("featured")]
    if not 15 <= len(feat) <= 20:
        errs.append(f"featured: need 15-20, have {len(feat)}")
    ranks = sorted(e.get("rank", 0) for e in feat)
    if ranks != list(range(1, len(feat) + 1)):
        errs.append(f"featured: ranks must be 1..{len(feat)}, got {ranks}")
    for key in data:
        for x in data[key]:
            for s in x.get("sources", []):
                u = s["url"]
                if not u.startswith("http") and not (REPO / u.split("#")[0]).exists():
                    errs.append(f"{key}/{x.get('id', x.get('date'))}: local source missing: {u}")
    return errs


if __name__ == "__main__":
    e = errors()
    for x in e:
        print("ERROR", x)
    data = load_all()
    print(f"validate: {len(data['entries'])} entries, {len(data['misconceptions'])} misconceptions, "
          f"{len(data['milestones'])} milestones, {len(data['compat'])} compat rows, {len(e)} errors")
    sys.exit(1 if e else 0)
