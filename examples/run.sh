#!/bin/sh
# Reproduce examples/RUNLOG.md in an isolated sandbox: temp HOME, empty env, no API keys.
# Usage: sh examples/run.sh [omp-version]   (needs bun, python3)
set -eu
VER=${1:-18.12.5}
EX=$(cd "$(dirname "$0")" && pwd)
LAB=$(mktemp -d /tmp/omp-lab.XXXXXX)
mkdir -p "$LAB/home" "$LAB/pkg" "$LAB/proj"
cd "$LAB/pkg" && echo '{"name":"lab","private":true}' > package.json
env -i PATH="$PATH" HOME="$LAB/home" bun add "@oh-my-pi/pi-coding-agent@$VER" >/dev/null
OMP="$LAB/pkg/node_modules/.bin/omp"
mkdir -p "$LAB/home/.omp/agent" && cp "$EX/models.offline.yml" "$LAB/home/.omp/agent/models.yml"
M="--model offline-dummy/dummy"
run() { (cd "$LAB/proj" && env -i PATH="$PATH" HOME="$LAB/home" OMP="$OMP" "$@"); }
echo "## version"; run "$OMP" --version
echo "## 1. extension via -e"
run python3 "$EX/rpc_probe.py" $M -e "$EX/minimal-extension/hello.ts" | python3 "$EX/summarize_probe.py" hello-omp
echo "## 2. marketplace add + install"
run "$OMP" plugin marketplace add "$EX/minimal-marketplace"
run "$OMP" plugin discover awesome-omp-demo
run "$OMP" plugin install hello-skill@awesome-omp-demo
run "$OMP" plugin list
echo "## 3. skill visible after install"
run python3 "$EX/rpc_probe.py" $M | python3 "$EX/summarize_probe.py" hello
echo "## 4. Pi package on omp: ${PI_PKG:-pi-web-access}"
run "$OMP" install "npm:${PI_PKG:-pi-web-access}" || echo "install failed"
run "$OMP" plugin list
run python3 "$EX/rpc_probe.py" $M > "$LAB/probe4.json" || true
echo "tool ${PI_TOOL:-web_search} in dumpTools: $(grep -c "\"${PI_TOOL:-web_search}\"" "$LAB/probe4.json")"
grep -o '"error"[^}]*' "$LAB/probe4.json" | head -3 || true
echo "LAB=$LAB (delete when done)"
