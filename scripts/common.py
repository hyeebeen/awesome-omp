"""Shared loaders for awesome-omp scripts."""
from __future__ import annotations
import json
from pathlib import Path
import yaml

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"
FILES = ("entries", "misconceptions", "milestones", "compat")


def load_all() -> dict:
    out = {}
    for name in FILES:
        p = DATA / f"{name}.yml"
        doc = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        out[name] = doc.get(name, [])
    return out


def load_metrics() -> dict:
    p = DATA / "metrics.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"fetched_at": None, "items": {}}
