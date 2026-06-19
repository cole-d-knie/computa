---
name: "context7"
description: "Use when the user asks for current, version-specific library/framework/API documentation, code examples, setup or configuration guidance, or explicitly says to use Context7; prefer the Context7 MCP server and fall back to the ctx7 CLI only if the MCP tools are unavailable."
---

# Context7

Use Context7 to fetch up-to-date documentation for third-party libraries,
frameworks, SDKs, and developer tools.

## When To Use

- The user explicitly says "use context7" or asks to use Context7.
- The user asks for current docs, version-specific behavior, setup steps,
  configuration, migrations, or code examples for a library or framework.
- The answer depends on APIs that may have changed since the model's training
  data.

## Primary Workflow

1. If the Context7 MCP tools are not already visible, use tool discovery for
   `context7 resolve library docs query-docs`.
2. Resolve the package or product name with
   `mcp__context7__.resolve_library_id`.
3. Query the selected library ID with `mcp__context7__.query_docs`.
4. If the user provides an exact Context7 library ID such as `/vercel/next.js`
   or `/vercel/next.js/v16.1.6`, skip resolution and query that ID directly.
5. Keep queries concise and do not include secrets, credentials, private source
   code, personal data, or proprietary implementation details.

## Fallback

If the MCP tools are unavailable after discovery, use the CLI:

```bash
npx -y ctx7 library "<library>" "<question>"
npx -y ctx7 docs "<libraryId>" "<question>"
```

If the CLI requires login or an API key, stop and explain that Context7 MCP is
configured but the CLI mode needs authentication.

## Response Rules

- Cite the Context7 library ID used.
- Mention the version when the user asked for one and Context7 returned a
  versioned ID.
- If Context7 returns weak or ambiguous matches, say what you selected and why.
- Do not pretend Context7 was used if the MCP/CLI lookup did not actually run.
