# Awesome omp (oh-my-pi)

English | [中文](README.md)

> A source-checked research list for **omp** ([can1357/oh-my-pi](https://github.com/can1357/oh-my-pi)): understand how it works first, then browse a verified ecosystem and Pi compatibility notes. Written for humans and as context for AI agents. The Chinese README is the primary version; long-form docs are in Chinese.

**What omp is**: a terminal AI coding agent forked from [Pi](https://github.com/earendil-works/pi) that wires LSP, debuggers, structural editing and many tools into the agent.
**Not**: oh-my-posh (its themes are `*.omp.json`), the npm package `oh-my-pi`, or OpenMP.

<!-- BEGIN GENERATED: stats -->380 entries in 16 categories · 20 featured · 9 misconceptions · 10 compat rows · 9 official, 351 declare omp support, 1 Pi packages load-tested on omp. Metrics fetched 2026-10-21 11:59 (UTC+8).<!-- END GENERATED: stats -->

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
1. **[omp (can1357/oh-my-pi)](https://github.com/can1357/oh-my-pi)**：The source. The README walks through 21 features and docs/ holds about 85 mechanism docs, more accurate than any second-hand intro.
2. **[The harness problem（作者博客）](https://blog.can.ac/2026/02/12/the-harness-problem/)**：Why omp exists: the author argues the harness, not the model, is often the bottleneck; changing only the edit format (hashline) lifted most models. Self-reported benchmark.
3. **[The Harness Playbook（Stencil 博客）](https://stencil.so/blog/harness-playbook)**：The author's own postmortem of omp and the plan for omp² (Python extensions). Read before investing in omp extensions.
<!-- END GENERATED: top3 -->

## omp in 30 seconds

1. **Pi is a minimal core; omp is batteries included.** Both are extensible, but omp ships LSP, debuggers, a browser, subagents and a plugin marketplace.
2. **It bets on the harness, not the model.** The author argues that the same model succeeds far more often with better edit formats and tools ([why.md](docs/why.md)).
3. **Its ecosystem partly overlaps with Pi.** Pi packages often install, but directories and API versions differ; verify each one ([compat matrix](docs/pi-compat.md)).

## Featured

Full registry: [docs/ecosystem.md](docs/ecosystem.md).

<!-- BEGIN GENERATED: featured -->
| # | Pick | Category | Why it is worth your time | Data |
|---|---|---|---|---|
| 1 | [omp (can1357/oh-my-pi)](https://github.com/can1357/oh-my-pi) | omp itself | The source. The README walks through 21 features and docs/ holds about 85 mechanism docs, more accurate than any second-hand intro. | [details](docs/ecosystem.md#oh-my-pi) |
| 2 | [The harness problem（作者博客）](https://blog.can.ac/2026/02/12/the-harness-problem/) | Articles, tutorials & discussions | Why omp exists: the author argues the harness, not the model, is often the bottleneck; changing only the edit format (hashline) lifted most models. Self-reported benchmark. | [details](docs/ecosystem.md#the-harness-problem) |
| 3 | [The Harness Playbook（Stencil 博客）](https://stencil.so/blog/harness-playbook) | Articles, tutorials & discussions | The author's own postmortem of omp and the plan for omp² (Python extensions). Read before investing in omp extensions. | [details](docs/ecosystem.md#harness-playbook) |
| 4 | [omp 文档：Extensions + Extension loading](https://github.com/can1357/oh-my-pi/blob/main/docs/extensions.md) | Official docs | The authority on writing extensions: factory, events, tools, slash commands, UI, and discovery paths. Our minimal extension follows it and loads in tests. | [details](docs/ecosystem.md#docs-extensions) |
| 5 | [omp 文档：Marketplace 插件系统](https://github.com/can1357/oh-my-pi/blob/main/docs/marketplace.md) | Official docs | omp reads the Claude Code plugin marketplace format, its biggest ecosystem difference from Pi. Covers scopes, lockfile and reload rules. | [details](docs/ecosystem.md#docs-marketplace) |
| 6 | [Pi（earendil-works/pi，原 badlogic/pi-mono）](https://github.com/earendil-works/pi) | Adjacent lists & projects | omp's upstream. Explains the minimal-Pi vs batteries-included-omp split and which Pi packages carry over (see the compat matrix). | [details](docs/ecosystem.md#earendil-pi) |
| 7 | [omp 文档：TTSR 注入生命周期](https://github.com/can1357/oh-my-pi/blob/main/docs/ttsr-injection-lifecycle.md) | Official docs | omp's most distinctive mechanism: rules cost no context until the output matches a regex, then the stream is aborted, the rule injected and the turn retried. Traced to source. | [details](docs/ecosystem.md#docs-ttsr) |
| 8 | [Hacker News：Oh-my-pi – A coding agent with the IDE wired in](https://news.ycombinator.com/item?id=48994611) | Articles, tutorials & discussions | Real user voices: easy start and good search integration, but also worries about subscription OAuth bans and doubts about benchmarks. | [details](docs/ecosystem.md#hn-launch) |
| 9 | [Custom Models in Oh My Pi（doug.sh）](https://doug.sh/posts/oh-my-pi-custom-models/) | Models & providers | Most practical guide to local models: working models.yml for each inference server, model roles and allowlists, plus two changes needed since omp 18.2.7. | [details](docs/ecosystem.md#doug-custom-models) |
| 10 | [pi-web-access](https://github.com/nicobailon/pi-web-access) | Extensions | Evidence that Pi packages can work on omp: installs and exposes web_search, but a feature needing Pi 0.86+ is disabled. A reference for porting Pi packages. | [details](docs/ecosystem.md#pi-web-access) |
| 11 | [Magic Context（cortexkit）](https://github.com/cortexkit/magic-context) | Memory & context | Cross-session memory and context management that detects omp and replaces its built-in compaction. Good for long sessions. | [details](docs/ecosystem.md#magic-context) |
| 12 | [gooey-pi](https://github.com/am-will/gooey-pi) | Desktop, web & mobile frontends | One of the most-starred desktop frontends (Electron, cross-platform) for people who prefer a GUI; supports both Pi and omp. | [details](docs/ecosystem.md#gooey-pi) |
| 13 | [pi-automode](https://github.com/czottmann/pi-automode) | Workflows & multi-agent | Adds a Claude-Code-style auto mode: a chosen model decides which actions can proceed. Compare with omp's own approval-mode. | [details](docs/ecosystem.md#pi-automode) |
| 14 | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | Marketplaces | The marketplace used in omp's own quick start. One command brings Claude Code plugins into omp; verify each plugin yourself. | [details](docs/ecosystem.md#claude-plugins-official) |
| 15 | [Pi vs OMP (Oh My Pi Agent)：Everything You Need to Know（Composio）](https://composio.dev/content/pi-vs-omp) | Articles, tutorials & discussions | A rare side-by-side of Pi and omp for quick orientation. Vendor content; check claims against our compat matrix. | [details](docs/ecosystem.md#composio-pi-vs-omp) |
| 16 | [Current Agentic Development Environment：Orca + Oh My Pi](https://james-carr.org/posts/2026-09-30-current-agentic-development-setup-orca-oh-my-pi/) | Articles, tutorials & discussions | A concrete example of omp model roles (default, smol, slow, plan...) and which model fills each. | [details](docs/ecosystem.md#james-carr-orca-omp) |
| 17 | [omp-docs-cn（非官方中文文档站）](https://github.com/Aieguu/omp-docs-cn) | Chinese community | Entry point for Chinese readers. Unofficial and may lag upstream; English docs/ win on conflicts. | [details](docs/ecosystem.md#omp-docs-cn) |
| 18 | [thevibeworks/awesome-pi-agent](https://github.com/thevibeworks/awesome-pi-agent) | Adjacent lists & projects | Hand-curated Pi ecosystem list where omp is one section. Go there for Pi-wide extensions, forks and frontends. | [details](docs/ecosystem.md#thevibeworks-awesome-pi-agent) |
| 19 | [omp 文档：RPC 与 SDK](https://github.com/can1357/oh-my-pi/blob/main/docs/rpc.md) | Official docs | Two ways to embed omp: the Node SDK and stdio NDJSON RPC. Our offline tests use RPC to list commands and tools without calling a model. | [details](docs/ecosystem.md#docs-rpc-sdk) |
| 20 | [omp 文档：子 agent 发现与选择](https://github.com/can1357/oh-my-pi/blob/main/docs/task-agent-discovery.md) | Official docs | Subagents are omp's main way of working. Covers agent definition fields, source precedence and spawn-depth limits. | [details](docs/ecosystem.md#docs-task-agents) |
<!-- END GENERATED: featured -->

## Common misconceptions

<!-- BEGIN GENERATED: misconceptions -->
1. **Myth:** `*.omp.json` theme files are omp themes.
   **Fact:** `*.omp.json` is the theme suffix of oh-my-posh, a shell prompt renderer. omp themes are documented in docs/theme.md. ([oh-my-posh themes/](https://github.com/JanDeDobbeleer/oh-my-posh/tree/main/themes) [omp theme.md](https://github.com/can1357/oh-my-pi/blob/main/docs/theme.md))
2. **Myth:** The npm package `oh-my-pi` is omp.
   **Fact:** That package is an unrelated Pi add-on by acidsugarx. omp ships as `@oh-my-pi/pi-coding-agent` with the `omp` binary. ([npm oh-my-pi](https://www.npmjs.com/package/oh-my-pi) [npm @oh-my-pi/pi-coding-agent](https://www.npmjs.com/package/@oh-my-pi/pi-coding-agent))
3. **Myth:** omp is a GitHub fork of Pi and follows Pi features automatically.
   **Fact:** The repo is not a GitHub fork and versions independently. Upstream changes are ported by hand; the documented last sync point is 2026-03-22. ([repos API (fork: false)](https://api.github.com/repos/can1357/oh-my-pi) [porting-from-pi-mono.md](https://github.com/can1357/oh-my-pi/blob/main/docs/porting-from-pi-mono.md))
4. **Myth:** Every Pi extension works on omp unchanged.
   **Fact:** omp aliases `@mariozechner/*` and `@earendil-works/*` imports and `omp install npm:<pkg>` installs Pi packages, but discovery dirs differ and newer Pi APIs may be missing. Our test: pi-web-access loads but disables a feature that needs Pi 0.86+. Verify per package. ([legacy-pi-compat.ts](https://github.com/can1357/oh-my-pi/blob/main/packages/coding-agent/src/extensibility/plugins/legacy-pi-compat.ts) [RUNLOG](https://github.com/hyeebeen/awesome-omp/blob/main/examples/RUNLOG.md))
5. **Myth:** Hashline edits beat other formats for every model.
   **Fact:** In the author's own benchmark hashline beat patch in 14 of 16 models; DeepSeek V3.2 and GPT-5.2 Codex got worse. An HN user reports models spending many turns repairing broken anchored edits. No third-party replication found. ([The harness problem](https://blog.can.ac/2026/02/12/the-harness-problem/) [HN 评论（localroast）](https://news.ycombinator.com/item?id=49545358))
6. **Myth:** Opening an untrusted repo in omp only reads code.
   **Fact:** By design omp loads the project's settings, extensions, hooks, tools, commands, skills, rules and project MCP config. Narrow inputs with `--no-extensions`, `--trusted-extension` or a `--config` overlay. ([README「Project inputs and trust」](https://github.com/can1357/oh-my-pi/blob/main/README.md#project-inputs-and-trust))
7. **Myth:** The README's provider/tool counts and benchmark numbers are independent facts.
   **Fact:** They are the project's own claims and change between releases; benchmarks are the author's own. Cite them as self-claimed. ([omp README](https://github.com/can1357/oh-my-pi/blob/main/README.md))
8. **Myth:** omp's TypeScript extension API is a stable long-term platform.
   **Fact:** In The Harness Playbook the author says the current design pushes complexity onto extensions and announces omp², whose extensions use Python. No release date is given; this is a stated plan. ([The Harness Playbook](https://stencil.so/blog/harness-playbook))
9. **Myth:** omp starts without any model configured.
   **Fact:** Without a default model omp exits ("No default model selected") and RPC never sends ready. For offline tests configure a dummy provider (examples/models.offline.yml). ([RUNLOG](https://github.com/hyeebeen/awesome-omp/blob/main/examples/RUNLOG.md))
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
