# AGENTS.md — how AI agents should read and edit this repo

## What this repo is

A research list about **omp = can1357/oh-my-pi** (npm `@oh-my-pi/pi-coding-agent`, binary `omp`). Never confuse it with oh-my-posh (`*.omp.json`), the npm package `oh-my-pi` (acidsugarx), or OpenMP.

## Read

1. `llms.txt` — short entry point.
2. `data/awesome-omp.json` — full export: `entries`, `misconceptions`, `milestones`, `compat`, `metrics`.
3. Long-form (Chinese): `docs/deep-dive.md`, `docs/why.md`, `docs/practice.md`.

## Data flow

```text
scripts/collect.py ──> research/raw/candidates-*.json ──> scripts/import_candidates.py ──┐
humans / agents edit ────────────────────────────────────────────────────────────────────┤
                                                                                         v
               data/entries.yml  data/misconceptions.yml  data/milestones.yml  data/compat.yml
scripts/metrics.py ──> data/metrics.json (stars, npm downloads; the ONLY place numbers live)
                                                                                         v
                         scripts/build.py ──> README blocks, llms.txt, docs/ecosystem.md,
                                              docs/pi-compat.md, docs/timeline.md, data/awesome-omp.json
```

## Entry fields (`data/entries.yml`, schema `data/schema.json`)

| Field | Meaning |
|---|---|
| `id` | Stable anchor (`docs/ecosystem.md#<id>`). Never change; add old names to `aliases`. |
| `category` | core, doc, provider, extension, plugin, marketplace, skill, theme, mcp-lsp-dap, memory, frontend, editor, workflow, learning, zh, adjacent. Auto-imported rows are keyword-classified. |
| `kind` | repo, npm, doc, article, video, site, discussion |
| `omp_support` | `native` official omp · `declared` project says it supports omp · `pi-compat-tested` Pi package we load-tested on omp · `pi-compat-unverified` · `about` content about omp · `unsupported` · `unknown` |
| `evidence_type` | `verified` docs/source/API · `self-claimed` the project's own words · `tested` reproduced in examples/RUNLOG.md · `inferred` our judgement |
| `evidence` | The quoted line or a short description of the proof |
| `sources[]` | First-hand links |
| `verified_at` | YYYY-MM-DD (Asia/Shanghai) |
| `featured`, `rank`, `why`, `why_en` | README picks (15–20, ranks 1..N; 1–3 = 「只看 3 条」) |

## Rules for edits

- Edit only `data/*.yml`, docs prose, examples, scripts. Never hand-edit generated files (see `scripts/build.py` docstring) or any number (stars, downloads, counts).
- Every new claim needs a first-hand source and an `evidence_type`. Self-claims (benchmarks, provider counts) stay labelled self-claimed.
- "Unsupported" needs positive evidence (maintainer statement or code search); otherwise use `unknown`.
- Versions and dates belong in `data/milestones.yml` and research notes only.
- Run `sh scripts/check.sh` before proposing a change.

## AI contribution policy

AI-assisted PRs are welcome if a human checked every claim against the linked source. Do not submit auto-generated lists, marketing copy, or entries without omp evidence. Disclose authorship of your own projects.
