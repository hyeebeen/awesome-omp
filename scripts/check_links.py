#!/usr/bin/env python3
"""Check local Markdown links and #anchors (relative paths only).
Anchors: GitHub-style heading slugs plus explicit <a id="..."></a>. Exit 1 on any broken link."""
from __future__ import annotations
import re, sys
from pathlib import Path
from common import REPO

LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
SKIP = ("http://", "https://", "mailto:")


def slug(h: str) -> str:
    h = re.sub(r"<[^>]+>", "", h).strip().lower()
    h = re.sub(r"[^\w\u4e00-\u9fff\- ]", "", h)
    return h.replace(" ", "-")


def anchors(p: Path) -> set[str]:
    t = p.read_text(encoding="utf-8")
    t_nocode = re.sub(r"(?s)```.*?```", "", t)
    out = set(re.findall(r'<a id="([^"]+)"', t))
    for line in t_nocode.splitlines():
        m = re.match(r"^#{1,6}\s+(.*)$", line)
        if m:
            out.add(slug(m.group(1)))
    return out


def main() -> int:
    bad, n = [], 0
    files = [p for p in REPO.rglob("*.md") if "node_modules" not in p.parts and "raw" not in p.parts]
    cache = {}
    for f in files:
        text = re.sub(r"(?s)```.*?```", "", f.read_text(encoding="utf-8"))
        for target in LINK.findall(text):
            if target.startswith(SKIP):
                continue
            n += 1
            path, _, frag = target.partition("#")
            dest = (f.parent / path).resolve() if path else f
            if not dest.exists():
                bad.append(f"{f.relative_to(REPO)}: missing {target}"); continue
            if frag and dest.suffix == ".md":
                a = cache.setdefault(dest, anchors(dest))
                if frag not in a:
                    bad.append(f"{f.relative_to(REPO)}: missing anchor {target}")
    for b in bad:
        print("BROKEN", b)
    print(f"check_links: {n} local links in {len(files)} files, {len(bad)} broken")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
