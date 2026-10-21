# Pi 与 omp 兼容矩阵 / Pi vs omp compatibility

> 由 `scripts/build.py` 从 `data/compat.yml` 生成，请勿手改。

| 项目 | Pi | omp | 结论 | 证据 |
|---|---|---|---|---|
| <a id="extension-api"></a>扩展模块形态 / Extension module shape | TS 模块默认导出工厂，`import type { ExtensionAPI } from "@earendil-works/pi-coding-agent"` | 同样是默认导出工厂，类型来自 `@oh-my-pi/pi-coding-agent`；`@mariozechner/*`、`@earendil-works/*` 作用域被别名到 omp 自己的包（PI_SCOPE_ALIASES） | 兼容 | 已验证：[Pi extensions.md](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/extensions.md)；[omp extensions.md](https://github.com/can1357/oh-my-pi/blob/main/docs/extensions.md)；[legacy-pi-compat.ts（PI_SCOPE_ALIASES）](https://github.com/can1357/oh-my-pi/blob/main/packages/coding-agent/src/extensibility/plugins/legacy-pi-compat.ts) |
| <a id="extension-dir"></a>扩展自动发现目录 / Auto-discovery directory | `~/.pi/agent/extensions/`、项目 `.pi/extensions/` | `~/.omp/agent/extensions/`、项目 `.omp/extensions/`；`.pi/extensions` 不是原生发现目录 | 不同 | 已验证：[Pi extensions.md](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/extensions.md)；[omp extension-loading.md](https://github.com/can1357/oh-my-pi/blob/main/docs/extension-loading.md) |
| <a id="npm-package-install"></a>安装 Pi 社区包 / Installing a Pi package from npm | `pi install npm:<pkg>` | `omp install npm:<pkg>`；实测 pi-web-access 0.43.0 装上后 `web_search` 工具出现（未实际执行搜索） | 部分兼容 | 实测：[Pi packages.md](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/packages.md)；[RUNLOG 第 4 项](https://github.com/hyeebeen/awesome-omp/blob/main/examples/RUNLOG.md) |
| <a id="package-manifest"></a>包清单字段 / Package manifest | package.json `pi` 字段 + keyword `pi-package` | 原生读 `omp.extensions`；仍接受旧的 `pi.extensions` | 兼容 | 已验证：[Pi packages.md](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/packages.md)；[omp extension-loading.md](https://github.com/can1357/oh-my-pi/blob/main/docs/extension-loading.md) |
| <a id="newer-pi-api"></a>Pi 新版专有 API / APIs added in newer Pi | 随 Pi 版本演进（例如 pi-web-access 提示的 Dynamic tool activation 需要 Pi 0.86.0+） | 不保证有；实测 pi-web-access 自动降级为常驻工具 | 部分兼容 | 实测：[RUNLOG 第 4 项](https://github.com/hyeebeen/awesome-omp/blob/main/examples/RUNLOG.md) |
| <a id="claude-plugins"></a>Claude Code 插件市场 / Claude Code plugin marketplaces | 无内置插件市场（用 npm/git 包分发） | `/marketplace`、`omp plugin`；读 `.omp-plugin/marketplace.json`，兜底 `.claude-plugin/marketplace.json` | omp 独有 | 实测：[omp marketplace.md](https://github.com/can1357/oh-my-pi/blob/main/docs/marketplace.md)；[RUNLOG 第 2–3 项](https://github.com/hyeebeen/awesome-omp/blob/main/examples/RUNLOG.md) |
| <a id="skills"></a>Skills（SKILL.md） | 支持（skills.md） | 支持，另外自动读取 .claude/.cursor/.codex 等目录中已有的 skills 与规则 | 兼容 | 已验证：[Pi skills.md](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/skills.md)；[omp skills.md](https://github.com/can1357/oh-my-pi/blob/main/docs/skills.md)；[omp README「Discovery」](https://github.com/can1357/oh-my-pi/blob/main/README.md) |
| <a id="themes"></a>主题 / Themes | 有主题机制（themes.md） | 有自己的主题文档（theme.md）；格式是否互通未实测 | 未确认 | 推断：[Pi themes.md](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/themes.md)；[omp theme.md](https://github.com/can1357/oh-my-pi/blob/main/docs/theme.md) |
| <a id="config-dir"></a>配置根目录 / Config root | `~/.pi/agent` | `~/.omp/agent`（可用 `--profile`、XDG 改位置） | 不同 | 已验证：[omp config-usage.md](https://github.com/can1357/oh-my-pi/blob/main/docs/config-usage.md)；[Pi settings.md](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/settings.md) |
| <a id="upstream-sync"></a>代码同步 / Upstream sync | 上游 | 手工移植；文档记录的上次同步点为 2026-03-22（上游 commit b21b42d） | 不同 | 已验证：[porting-from-pi-mono.md](https://github.com/can1357/oh-my-pi/blob/main/docs/porting-from-pi-mono.md) |

汇总：兼容 3，不同 3，omp 独有 1，部分兼容 2，未确认 1。

结论：Pi 包**可能**在 omp 上能用，但要逐个验证；发现目录和配置根目录不同，Claude Code 插件市场是 omp 独有。
