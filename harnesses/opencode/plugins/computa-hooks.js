import { spawnSync } from "node:child_process"

const COMPUTA_REPO = process.env.COMPUTA_REPO || "/Users/cole/Desktop/swarm-verify-skills"
const HOOK_RUNNER = `${COMPUTA_REPO}/scripts/computa_hooks.py`

function projectRoot(ctx, fallback) {
  return ctx?.worktree || ctx?.directory || ctx?.project?.directory || fallback || process.cwd()
}

function jsonPayload(payload) {
  const seen = new WeakSet()
  return JSON.stringify(payload, (_key, value) => {
    if (typeof value === "object" && value !== null) {
      if (seen.has(value)) return "[Circular]"
      seen.add(value)
    }
    if (typeof value === "string" && value.length > 10000) return `${value.slice(0, 10000)}...[truncated]`
    return value
  })
}

function runHook(eventName, cwd, options = {}, extraPayload = {}) {
  const args = [HOOK_RUNNER, "hook", "--format", "opencode", "--event", eventName, "--root", cwd]
  if (options.strict) args.push("--strict")
  if (options.closeout) args.push("--closeout")
  if (options.quietOk) args.push("--quiet-ok")
  if (options.expandQueue) args.push("--expand-queue")

  const payload = jsonPayload({
    hook_event_name: eventName,
    cwd,
    source: "opencode-plugin",
    ...extraPayload,
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
      if (type === "session.created") await log(runHook("SessionStart", cwd, { expandQueue: true }, { event }))
      if (type === "session.idle") runHook("Stop", cwd, { strict: true, closeout: true }, { event })
      if (type === "session.compacted") runHook("PostCompact", cwd, { quietOk: true }, { event })
      if (type === "session.error") runHook("StopFailure", cwd, { quietOk: true }, { event })
      if (type === "permission.asked") runHook("PermissionRequest", cwd, { strict: true, quietOk: true }, { event })
      if (type === "permission.replied") runHook("PermissionResult", cwd, { quietOk: true }, { event })
      if (type === "file.edited") runHook("AfterFileEdit", cwd, { quietOk: true }, { event })
      if (type === "command.executed") runHook("AfterShellExecution", cwd, { quietOk: true }, { event })
    },
    "tool.execute.before": async (input) => {
      runHook("PreToolUse", cwd, { strict: true, quietOk: true }, { input })
    },
    "tool.execute.after": async (input, output) => {
      runHook("PostToolUse", cwd, { quietOk: true }, { input, output })
    },
    "experimental.session.compacting": async (_input, output) => {
      const context = runHook("PreCompact", cwd, { expandQueue: true })
      if (context && Array.isArray(output.context)) output.context.push(context)
    },
  }
}
