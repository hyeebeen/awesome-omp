#!/usr/bin/env python3
"""Start `omp --mode rpc` with no API key, send get_commands / get_state, print frames.
Proves extensions/plugins load without calling any model. Usage:
  OMP=/path/to/omp python3 examples/rpc_probe.py [extra omp args...]
Run with an isolated HOME (see examples/run.sh)."""
import json, os, subprocess, sys, time, select
omp = os.environ.get("OMP", "omp")
p = subprocess.Popen([omp, "--mode", "rpc", "--no-session", *sys.argv[1:]], stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
def frames(timeout):
    end = time.time() + timeout
    while time.time() < end:
        r, _, _ = select.select([p.stdout], [], [], 0.5)
        if r:
            line = p.stdout.readline()
            if not line: return
            try: yield json.loads(line)
            except Exception: pass
out = {}
for f in frames(40):
    if f.get("type") == "ready":
        out["ready"] = True
        for i, cmd in enumerate(["get_available_commands", "get_state"]):
            p.stdin.write(json.dumps({"id": f"q{i}", "type": cmd}) + "\n"); p.stdin.flush()
    if f.get("type") == "response":
        out[f.get("command") or f.get("id")] = f
        if len(out) >= 3: break
p.kill()
print(json.dumps(out, ensure_ascii=False))
