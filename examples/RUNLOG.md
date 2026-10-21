# RUNLOG：在 box 上实测 omp

- 运行时间：2026-10-21 11:39 (Asia/Shanghai)
- 环境：Linux x86_64，bun 1.4.2，python 3.13.5
- 隔离：`mktemp -d` 临时 HOME，`env -i` 空环境（不继承任何 API key），模型指向关闭的本地端口 `127.0.0.1:9`（examples/models.offline.yml），全程不调用任何模型。
- 复现：`sh examples/run.sh 18.12.5`

## 结论

| # | 测什么 | 结果 |
|---|---|---|
| 1 | `omp -e examples/minimal-extension/hello.ts` 加载最小扩展 | 通过：RPC `get_available_commands` 出现 `hello-omp`（source=extension），`get_state.dumpTools` 含工具 `hello_awesome_omp` |
| 2 | 本地目录作为 marketplace：add → discover → install → list | 通过：`hello-skill@awesome-omp-demo (0.1.0) (user)` |
| 3 | 安装后的 skill 是否进入会话 | 通过：命令列表出现 `skill:hello` |
| 4 | Pi 社区包 `npm:pi-web-access` 用 `omp install` 装进 omp | 通过（加载层面）：0.43.0 安装成功，`web_search` 工具出现在 dumpTools；包自己提示「Dynamic tool activation requires Pi 0.86.0 or newer」并降级为常驻工具。未实际执行搜索。 |

## 发现

- 没有可用模型时 omp 拒绝启动（「No default model selected」），RPC 也不会发 ready 帧。离线测试必须先配一个假 provider。
- models.yml 的自定义模型 `cost` 必须同时给 `cacheRead`、`cacheWrite`，否则整份配置被拒（schema error）。
- 首次在默认 shell 里试跑时，omp 自动读取了环境中已有的模型 key 选择默认模型（未发起请求）。之后全部改用 `env -i`。这正是「信任与安全」一节要提醒的：omp 会自动发现环境变量里的凭据。

## 原始输出

```text
Resolving dependencies
Resolved, downloaded and extracted [507]
warn: incorrect peer dependency "@opentelemetry/api@1.10.0"

warn: incorrect peer dependency "@opentelemetry/api@1.10.0"

warn: incorrect peer dependency "@opentelemetry/api@1.10.0"

warn: incorrect peer dependency "@opentelemetry/api@1.10.0"

warn: incorrect peer dependency "@opentelemetry/api@1.10.0"

warn: incorrect peer dependency "@opentelemetry/api@1.10.0"

warn: incorrect peer dependency "@opentelemetry/api@1.10.0"

warn: incorrect peer dependency "@opentelemetry/api@1.10.0"

warn: incorrect peer dependency "@opentelemetry/api@1.10.0"

warn: incorrect peer dependency "@opentelemetry/api@1.10.0"

warn: incorrect peer dependency "@opentelemetry/api@1.10.0"

warn: incorrect peer dependency "@opentelemetry/api@1.10.0"
Saved lockfile
## version
omp/18.12.5
## 1. extension via -e
ready: True | commands: 52 | hello-omp found: True
matches: ['hello-omp']
## 2. marketplace add + install
✔ Added marketplace: <repo>/examples/minimal-marketplace
Available Plugins (awesome-omp-demo):

  hello-skill
    Minimal plugin with one skill
✔ Installed hello-skill from awesome-omp-demo (0.1.0)
Marketplace Plugins:

  hello-skill@awesome-omp-demo (0.1.0) (user)
## 3. skill visible after install
ready: True | commands: 52 | hello found: True
matches: ['skill:hello']
## 4. Pi package on omp: pi-web-access
[pi-web-access] Dynamic tool activation requires Pi 0.86.0 or newer; web tools remain eagerly available.
✔ Installed pi-web-access@0.43.0
npm Plugins:

● pi-web-access@0.43.0

Marketplace Plugins:

  hello-skill@awesome-omp-demo (0.1.0) (user)
tool web_search in dumpTools: 1
LAB=$LAB (delete when done)
EXIT 0
```
