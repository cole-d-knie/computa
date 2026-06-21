import { spawnSync } from "node:child_process"

const COMPUTA_REPO = process.env.COMPUTA_REPO || "/Users/cole/Desktop/swarm-verify-skills"
const HOOK_RUNNER = `${COMPUTA_REPO}/scripts/computa_hooks.py`

function projectRoot(ctx, fallback) {
  return ctx?.worktree || ctx?.directory || ctx?.project?.directory || fallback || process.cwd()
}

function runHook(eventName, cwd, options = {}) {
  const args = [HOOK_RUNNER, "hook", "--format", "opencode", "--event", eventName, "--root", cwd]
  if (options.strict) args.push("--strict")
  if (options.closeout) args.push("--closeout")
  if (options.quietOk) args.push("--quiet-ok")

  const payload = JSON.stringify({
    hook_event_name: eventName,
    cwd,
    source: "opencode-plugin",
  })
  const result = spawnSync("python3", args, {
    input: payload,
    encoding: "utf8",
  })
  const stdout = (result.stdout || "").trim()
  const stderr = (result.stderr || "").trim()
  if (result.error || result.status === null || result.status !== 0) {
    throw new Error(stderr || stdout || result.error?.message || `Computa hook failed: ${eventName}`)
  }
  return stdout
}

export const ComputaHooksPlugin = async (ctx) => {
  const cwd = projectRoot(ctx)
  const log = async (message) => {
    if (!message || !ctx.client?.app?.log) return
    await ctx.client.app.log({
      body: {
        service: "computa-hooks",
        level: "info",
        message,
      },
    })
  }

  return {
    event: async ({ event }) => {
      const type = event?.type || ""
      if (type === "session.created") await log(runHook("SessionStart", cwd))
      if (type === "session.idle") runHook("Stop", cwd, { strict: true, closeout: true })
      if (type === "session.compacted") runHook("PostCompact", cwd, { quietOk: true })
      if (type === "session.error") runHook("StopFailure", cwd, { quietOk: true })
      if (type === "permission.asked") runHook("PermissionRequest", cwd, { strict: true, quietOk: true })
      if (type === "permission.replied") runHook("PermissionResult", cwd, { quietOk: true })
      if (type === "file.edited") runHook("AfterFileEdit", cwd, { quietOk: true })
      if (type === "command.executed") runHook("AfterShellExecution", cwd, { quietOk: true })
    },
    "tool.execute.before": async () => {
      runHook("PreToolUse", cwd, { strict: true, quietOk: true })
    },
    "tool.execute.after": async () => {
      runHook("PostToolUse", cwd, { quietOk: true })
    },
    "experimental.session.compacting": async (_input, output) => {
      const context = runHook("PreCompact", cwd)
      if (context && Array.isArray(output.context)) output.context.push(context)
    },
  }
}
