#!/usr/bin/env python3
"""Read rpc_probe.py JSON on stdin; report whether a command name is present."""
import json, sys
want = sys.argv[1]
d = json.load(sys.stdin)
cmds = (d.get("get_available_commands") or {}).get("data") or {}
cmds = cmds.get("commands", cmds) if isinstance(cmds, dict) else cmds
names = sorted({c.get("name") for c in cmds if isinstance(c, dict)})
print("ready:", d.get("ready"), "| commands:", len(names), "|", want, "found:", want in names or any(want in (n or "") for n in names))
print("matches:", [n for n in names if want in (n or "")])
