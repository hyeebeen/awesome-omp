# Contributing

1. Check [docs/ecosystem.md](docs/ecosystem.md); the entry may exist.
2. Open an issue with the **New entry** or **Status change** template, or a PR editing `data/*.yml`.
3. Provide first-hand evidence of omp support (README line, docs, code, or a test with the omp version).
4. Run `sh scripts/check.sh` (needs python3 + pyyaml + jsonschema, markdownlint-cli2, Node for mermaid-cli). Set `SKIP_MERMAID=1` if you cannot run Chrome.
5. Do not edit generated files or numbers; run `python3 scripts/build.py`.

Inclusion rules: see README「收录规则」. Field definitions and AI policy: [AGENTS.md](AGENTS.md).
