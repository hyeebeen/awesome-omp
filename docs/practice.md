# 实践：安装、配置、扩展、安全

> 命令均来自官方 README / docs，核实于 2026-10-21。实测部分见 [examples/RUNLOG.md](../examples/RUNLOG.md)。

## 安装

| 方式 | 命令 |
|---|---|
| 脚本（macOS / Linux） | `curl -fsSL https://omp.sh/install \| sh` |
| Homebrew | `brew install can1357/tap/omp` |
| Bun（官方推荐） | `bun install -g @oh-my-pi/pi-coding-agent` |
| Nix | `nix run github:can1357/oh-my-pi` |
| Windows | `irm https://omp.sh/install.ps1 \| iex` |
| mise | `mise use -g github:can1357/oh-my-pi` |

要求 bun ≥ 1.3.14（README）。Alpine 需先 `apk add libstdc++ libgcc`。

## 第一次运行

1. 选模型：`omp login` 登录 provider，或设置 `ANTHROPIC_API_KEY` 等环境变量，或写 `~/.omp/agent/models.yml`（[models.md](https://github.com/can1357/oh-my-pi/blob/main/docs/models.md)）。
2. 没有默认模型时 omp 直接退出，这是正常行为。
3. 补全：`eval "$(omp completions zsh)"`。

## 写一个扩展

最小例子：[examples/minimal-extension/hello.ts](../examples/minimal-extension/hello.ts)。

```sh
omp -e examples/minimal-extension/hello.ts          # 临时加载
mkdir -p .omp/extensions && cp examples/minimal-extension/hello.ts .omp/extensions/   # 项目内自动发现
```

## 做一个插件市场

最小例子：[examples/minimal-marketplace/](../examples/minimal-marketplace/)。

```sh
omp plugin marketplace add ./examples/minimal-marketplace
omp plugin install hello-skill@awesome-omp-demo
omp plugin list
```

安装后会话里会出现 `skill:hello`。TUI 中改动插件后用 `/reload-plugins` 刷新；新工具、hooks、扩展模块要重启会话（[marketplace.md](https://github.com/can1357/oh-my-pi/blob/main/docs/marketplace.md)）。

## 装 Pi 社区包

```sh
omp install npm:pi-web-access
```

先看 [兼容矩阵](pi-compat.md)。建议用 `omp --profile test` 在隔离 profile 里试。

## 离线验证（不调用任何模型）

```sh
sh examples/run.sh 18.12.5
```

它会在临时 HOME 里安装指定版本，用一个指向关闭端口的假 provider 启动 `omp --mode rpc`，读取命令和工具列表。

## 信任与安全

- **打开仓库即加载项目输入**：settings、extensions、hooks、tools、commands、skills、rules、项目 MCP 配置都会按设计加载（[README「Project inputs and trust」](https://github.com/can1357/oh-my-pi/blob/main/README.md#project-inputs-and-trust)）。
- 收窄输入：
  - `--no-extensions`：不做扩展自动发现（显式 `-e` 仍生效）。
  - `--trusted-extension /abs/path.ts`：只允许指定扩展。
  - `--config <file>`：用 YAML overlay 关掉项目 `.mcp.json`（要写嵌套键，平铺的 `mcp.enableProjectConfig: false` 会被忽略）。
  - `--no-tools` 只关内置工具，项目工具模块是另一条发现路径。
- **扩展是任意代码**：Pi 包、marketplace 插件都在本机执行。只装看过源码或可信来源的。
- **凭据自动发现**：omp 会读环境变量里的模型 key。我们第一次试跑时，它在未配置的情况下就从环境中选出了默认模型。做实验请用 `env -i` 或单独 profile。
- **订阅账号**：有用户反馈部分 provider 的 OAuth 只接受官方客户端（[HN](https://news.ycombinator.com/item?id=49007232)），使用前看清服务条款。
- 秘密管理见 [secrets.md](https://github.com/can1357/oh-my-pi/blob/main/docs/secrets.md)，审批模式见 [approval-mode.md](https://github.com/can1357/oh-my-pi/blob/main/docs/approval-mode.md)。
