# Awesome omp (oh-my-pi)

English | [中文](README.md)

> A source-checked research list for **omp** ([can1357/oh-my-pi](https://github.com/can1357/oh-my-pi)): understand how it works first, then browse a verified ecosystem and Pi compatibility notes. Written for humans and as context for AI agents. The Chinese README is the primary version; long-form docs are in Chinese.

**What omp is**: a terminal AI coding agent forked from [Pi](https://github.com/earendil-works/pi) that wires LSP, debuggers, structural editing and many tools into the agent.
**Not**: oh-my-posh (its themes are `*.omp.json`), the npm package `oh-my-pi`, or OpenMP.

<!-- BEGIN GENERATED: stats --><!-- END GENERATED: stats -->

## Contents

- [Start with these 3](#start-with-these-3)
- [omp in 30 seconds](#omp-in-30-seconds)
- [Featured](#featured)
- [Common misconceptions](#common-misconceptions)
- [Go deeper](#go-deeper)
- [Inclusion rules](#inclusion-rules)
- [How this differs from other lists](#how-this-differs-from-other-lists)
- [For AI agents](#for-ai-agents)
- [Disclaimer](#disclaimer)

## Start with these 3

<!-- BEGIN GENERATED: top3 -->
<!-- END GENERATED: top3 -->

## omp in 30 seconds

1. **Pi is a minimal core; omp is batteries included.** Both are extensible, but omp ships LSP, debuggers, a browser, subagents and a plugin marketplace.
2. **It bets on the harness, not the model.** The author argues that the same model succeeds far more often with better edit formats and tools ([why.md](docs/why.md)).
3. **Its ecosystem partly overlaps with Pi.** Pi packages often install, but directories and API versions differ; verify each one ([compat matrix](docs/pi-compat.md)).

## Featured

Full registry: [docs/ecosystem.md](docs/ecosystem.md).

<!-- BEGIN GENERATED: featured -->
<!-- END GENERATED: featured -->

## Common misconceptions

<!-- BEGIN GENERATED: misconceptions -->
<!-- END GENERATED: misconceptions -->

## Go deeper

- [docs/deep-dive.md](docs/deep-dive.md): architecture, hashline, TTSR, subagents, extension API, with source paths
- [docs/why.md](docs/why.md): why omp exists, community voices, outlook
- [docs/practice.md](docs/practice.md): install, extensions, marketplace, Pi packages, trust and safety
- [docs/pi-compat.md](docs/pi-compat.md) · [docs/ecosystem.md](docs/ecosystem.md) · [docs/timeline.md](docs/timeline.md)
- [examples/RUNLOG.md](examples/RUNLOG.md): offline load tests (no model calls)

## Inclusion rules

Included when all hold: public source or docs; positive evidence of omp support (stated in README/description, or tested here); activity within 180 days and not archived; auto-imported GitHub projects need 5+ stars and npm packages 300+ downloads last month. Every entry is labelled verified / self-claimed / tested / inferred. Registry categories are keyword-based and may be wrong.

## How this differs from other lists

[shaftoe/awesome-pi-coding-agent](https://github.com/shaftoe/awesome-pi-coding-agent) is a large daily auto-index of the Pi ecosystem; [thevibeworks/awesome-pi-agent](https://github.com/thevibeworks/awesome-pi-agent) is a hand-curated Pi list where omp is one section. This repo goes deep on omp only: mechanisms, per-entry omp evidence with dates, a Pi compatibility matrix and tested examples.

## For AI agents

Start at [llms.txt](llms.txt); full data in [data/awesome-omp.json](data/awesome-omp.json); fields in [AGENTS.md](AGENTS.md) and [data/schema.json](data/schema.json). Every entry has a stable anchor `docs/ecosystem.md#<id>`.

## License

[CC0-1.0](LICENSE).

## Disclaimer

This repository uses AI to help with research, analysis and diagrams. A human edits, corrects and organizes the content in depth. It is maintained mainly for my own technical research and practice, and is provided for reference only.

Data and status may lag behind the original sources. Please check the linked sources and use your own judgment before relying on them.

If any content infringes your rights, please open an [issue](https://github.com/hyeebeen/awesome-omp/issues) and I will review and remove it promptly.
