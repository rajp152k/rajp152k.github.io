import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  pi.registerCommand("hart-improve", {
    description: "Reflect on this session and update H.A.R.T.'s collaboration habits",
    handler: async (args, ctx) => {
      const focus = args.trim();
      const prompt = [
        "Use the hart-coauthor skill in Improve H.A.R.T. mode.",
        "Review this session for Raj's explicit corrections, repeated preferences, rejected structures, and successful patterns.",
        "Update .pi/skills/hart-coauthor/references/learned-habits.md according to its improvement protocol.",
        "Update AGENTS.md only for durable repository-wide rules justified by the session.",
        "Report the evidence for every change and describe what behavior will differ next time.",
        focus ? `Focus especially on: ${focus}` : "",
      ].filter(Boolean).join("\n");

      if (ctx.isIdle()) {
        pi.sendUserMessage(prompt);
      } else {
        pi.sendUserMessage(prompt, { deliverAs: "followUp" });
        ctx.ui.notify("H.A.R.T. improvement review queued", "info");
      }
    },
  });

  pi.registerCommand("hart-review", {
    description: "Run the H.A.R.T. coherence review on a post or page",
    handler: async (args, ctx) => {
      const target = args.trim();
      if (!target) {
        ctx.ui.notify("Usage: /hart-review <post-or-page-path>", "warning");
        return;
      }
      const prompt = `Use the hart-coauthor skill in Review mode. Review ${target}, make coherence fixes that preserve Raj's intent, run the local blog build, and summarize the changes.`;
      if (ctx.isIdle()) {
        pi.sendUserMessage(prompt);
      } else {
        pi.sendUserMessage(prompt, { deliverAs: "followUp" });
        ctx.ui.notify("H.A.R.T. review queued", "info");
      }
    },
  });
}
