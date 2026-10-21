#!/bin/sh
# Render every ```mermaid block with mermaid-cli (mmdc); fail on any parse/render error.
# Uses $MMDC if set, else `npx -y @mermaid-js/mermaid-cli`.
set -eu
cd "$(dirname "$0")/.."
TMP=$(mktemp -d)
python3 - "$TMP" <<'PY'
import re, sys, pathlib
out = pathlib.Path(sys.argv[1]); n = 0
for p in sorted(pathlib.Path('.').rglob('*.md')):
    if 'node_modules' in p.parts or 'raw' in p.parts: continue
    for i, m in enumerate(re.findall(r"```mermaid\n(.*?)```", p.read_text(encoding='utf-8'), re.S)):
        n += 1; (out / f"{str(p).replace('/', '_')}_{i}.mmd").write_text(m, encoding='utf-8')
print(f"mermaid blocks: {n}")
PY
MMDC=${MMDC:-"npx -y @mermaid-js/mermaid-cli"}
CFG="$TMP/puppeteer.json"; echo '{"args":["--no-sandbox"]}' > "$CFG"
fail=0
for f in "$TMP"/*.mmd; do
  if $MMDC -q -p "$CFG" -i "$f" -o "${f%.mmd}.svg" >/dev/null 2>"$f.err"; then :; else echo "FAIL $(basename "$f")"; cat "$f.err" | head -5; fail=1; fi
done
rm -rf "$TMP"
[ $fail -eq 0 ] && echo "mermaid: all blocks rendered" || exit 1
