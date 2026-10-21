// Minimal omp extension: one LLM-callable tool + one slash command.
// Load with: omp -e examples/minimal-extension/hello.ts
// API reference: https://github.com/can1357/oh-my-pi/blob/main/docs/extensions.md
import type { ExtensionAPI } from "@oh-my-pi/pi-coding-agent";

export default function hello(pi: ExtensionAPI) {
  pi.registerTool({
    name: "hello_awesome_omp",
    label: "Hello",
    description: "Return a greeting. Used to prove the extension loaded.",
    parameters: pi.zod.object({ name: pi.zod.string().describe("Name to greet") }),
    async execute(_toolCallId, params, _onUpdate, _ctx, _signal) {
      return { content: [{ type: "text", text: `hello, ${params.name}` }] };
    },
  });
  pi.registerCommand("hello-omp", {
    description: "Print a greeting (awesome-omp minimal extension)",
    handler: async (_args, ctx) => {
      ctx.ui.notify("hello from awesome-omp", "info");
    },
  });
}
