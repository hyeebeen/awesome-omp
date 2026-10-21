#!/bin/sh
# One command for every local check (CI runs the same steps):
# validate -> build --check -> unit tests -> markdownlint -> local links/anchors -> mermaid render
set -eu
cd "$(dirname "$0")/.."
echo "== validate (jsonschema + hygiene) =="; python3 scripts/validate.py
echo "== build --check (idempotent generation) =="; python3 scripts/build.py --check
echo "== unit tests (python unittest) =="; python3 -m unittest discover -s tests -q
echo "== markdownlint-cli2 =="; markdownlint-cli2 "**/*.md" "#node_modules" "#research/raw"
echo "== local links + anchors (scripts/check_links.py) =="; python3 scripts/check_links.py
if [ "${SKIP_MERMAID:-0}" = "1" ]; then echo "== mermaid: skipped (SKIP_MERMAID=1) =="; else
echo "== mermaid render (scripts/check_mermaid.sh) =="; sh scripts/check_mermaid.sh; fi
echo "ALL CHECKS PASSED"
