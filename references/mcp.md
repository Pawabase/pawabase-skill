# MCP: connect AI tools and Pawabase

Pawabase participates in MCP in two directions. Keep them separate:

| Direction | What it does | Where to configure |
| --- | --- | --- |
| **AI client → Pawabase** | Codex, Claude, Cursor, or another MCP client inspects and manages a Pawabase environment. | Pawabase's `/mcp/v1` endpoint or local `pawabase-server mcp`. |
| **Pawabase agent → external MCP server** | A Pawabase agent uses an outside app's tools, such as GitHub, Linear, or a custom server. | Studio → AI → Connections → Any MCP server, then the agent's tool list. |

The skill itself is instructions. Installing `$pawabase` does not create an MCP connection. MCP is optional for the skill's advice; use it when live project inspection or management is useful.

## When MCP is already connected

Discover the Pawabase tool/resource catalog supplied by the client. Start with a read such as `get_overview`, `list_environments`, or `pawabase://{env}/overview` to identify the environment and visible scope. Use a purpose-built tool (`list_resources`, `get_resource`, `list_flow_runs`, and so on) before the broader `request_platform` escape hatch. For a definition change, inspect the current definition and plan/schema drift, apply the authorized change, then verify the result with a read. Do not ask the user to paste an API key when the connected tool already has the needed access. If a tool is absent, determine whether the key lacks its scope or the runtime lacks that tool; do not invent a tool call.

## AI client → Pawabase: choose authority first

For a hosted/remote client, use the public **HTTPS** gateway address `https://YOUR-API/mcp/v1`, not the internal server port. Pawabase's HTTP MCP endpoint is stateless Streamable HTTP: JSON-RPC over `POST`, ordinary JSON response, no session or SSE stream. `GET` and `DELETE` return `405`. The endpoint can be disabled with `PAWABASE_MCP_ENABLED=false`; the local stdio command remains a separate explicit option.
The route is intentionally excluded from the environment's generated OpenAPI. Verify it against the runtime MCP guide and the target deployment rather than expecting it in the API Explorer.

Create a **secret** environment key in Studio → AI → AI tools (or the environment's API keys page) and select **Look only** (`ai-read`) or **Build with me** (`ai-build`). A publishable key is refused. A scoped secret key needs at least one management scope to reach MCP; each listed tool and each call is then checked against its scopes. A key is pinned to its own environment and cannot escape into another environment through `request_platform`. An unscoped secret key exposes every available tool for that environment, so use a scoped key for ordinary AI clients. The key is shown once. Keep it in the client/secret store, not in git, chat, or a committed TOML file.

`ai-read` can inspect project definitions and activity without changing them. `ai-build` adds data and definition building but excludes users, keys, secrets, snapshots, and promotion. Exact tool visibility depends on key scopes and runtime version. The tool list can include resources/schema, records, policies, flows/jobs, storage, mail, webhooks, logs, AI models, and release/backup operations. Do not assume a static tool count.

### Codex remote example

Put the key in `PAWABASE_MCP_KEY` in the environment that **launches Codex**. Add to `~/.codex/config.toml` or a trusted project `.codex/config.toml`:

```toml
[mcp_servers.pawabase]
url = "https://YOUR-API/mcp/v1"
env_http_headers = { apikey = "PAWABASE_MCP_KEY" }
default_tools_approval_mode = "writes"
startup_timeout_sec = 20
tool_timeout_sec = 60
```

Pawabase also accepts `Authorization: Bearer pb_sk_...` on this endpoint, so Codex's `bearer_token_env_var = "PAWABASE_MCP_KEY"` is an alternative to `env_http_headers`. Do not set both for the same key. Run `codex mcp list`, inspect `/mcp` in the Codex TUI, then ask for a harmless read such as “List the tables in development.” If you launch Codex as a desktop app, ensure its process can read the environment variable. Codex's `writes` mode prompts for tools not annotated read-only; keep it enabled for production. See the [official Codex MCP configuration](https://learn.chatgpt.com/docs/extend/mcp?surface=cli).

### Other clients

Claude Code's documented remote form is:

```bash
claude mcp add --transport http pawabase \
  'https://YOUR-API/mcp/v1' \
  --header 'apikey: YOUR_SCOPED_SECRET_KEY'
```

This literal command may persist the key in local client configuration or shell history. Prefer the client's secure credential storage when available. Other clients need Streamable HTTP, the endpoint URL, and either `apikey` or Bearer authentication. If a hosted ChatGPT connector only offers OAuth, Pawabase's API-key endpoint cannot complete that OAuth flow by itself; use a supported API-key/custom-header connection or an approved credential proxy. Do not disable Pawabase authentication to make a connector work.

### Local stdio

For a client on the same trusted host as the runtime, launch `pawabase-server mcp` over stdio. It reads normal `PAWABASE_*` runtime settings and needs database/secrets access. This path has installation authority, not an environment-scoped remote key. Use an absolute executable path, a trusted working directory, and no terminal allocation. The runtime's `docs/mcp.md` includes Codex, Claude Desktop, and Docker examples.

## How tool calls behave

MCP tools call Pawabase's existing management API and retain its validation, scopes, migrations, quotas, and audit logging. Read tools/resources/prompts are also filtered by scope. Useful built-in prompts include `design_data_model`, `secure_resource`, `build_flow`, `investigate_errors`, `review_environment`, and `ship_changes`; available names can vary with runtime version.

Some high-impact tools require a `confirm` value, including deletes, write SQL, setting a secret, sending email, and non-dry-run promotion. That confirmation is a workflow pause, **not a hard permission boundary**: a client could supply it itself. Key scopes and the client's approval settings are the hard controls. `promote_environment` defaults to a dry run. For table work, define → inspect schema changes/migrate → use records. `create_resource` alone does not silently apply destructive schema changes. Prefer record tools for writes because direct SQL may miss normal events and realtime side effects.

Each tool call is audited as `mcp.tool` with tool name, environment, outcome, and argument names, not secret values. The underlying management change is audited too. A newly created API key is returned in plaintext once; secret values otherwise remain write-only.

## Verify the connection

If the key is already in a secure environment variable, a read-only handshake can confirm transport and auth:

```bash
curl --fail-with-body "$PAWABASE_URL/mcp/v1" \
  -H "apikey: $PAWABASE_MCP_KEY" \
  -H 'content-type: application/json' \
  -H 'accept: application/json, text/event-stream' \
  --data '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"curl","version":"1"}}}'
```

Then `tools/list` with another JSON-RPC `POST`. Do not send a real key to example endpoints or paste it into an issue. A `GET` probe returning `405` is expected and does not mean MCP is down.

| Symptom | Check |
| --- | --- |
| `401` / `403` | Secret key, expiry, management scopes, key route/IP restrictions, environment ownership. |
| `403 Origin` | Browser Origin must match the request host or configured public URLs; server-to-server clients usually omit Origin. |
| `404` | URL is `/mcp/v1`, deployment includes the server, and `PAWABASE_MCP_ENABLED` is on. |
| `405` on `GET` | Expected; configure Streamable HTTP `POST`, not legacy SSE. |
| Protocol-version error | Use a supported version/current client; runtime docs list `2024-11-05`, `2025-03-26`, `2025-06-18`. |
| Tool missing | Key lacks its management scope; inspect the scoped tool catalog. |
| `isError: true` | MCP connected, but the underlying management call failed; inspect the tool response. |
| Change not visible | Confirm client and Studio environment match; inspect pending resource migration. |

For runtime-specific details, read [Pawabase's MCP guide](https://github.com/Pawabase/pawabase/blob/main/docs/mcp.md) and the docs site's `ai/mcp.mdx`.

## Pawabase agent → external MCP server

In Studio, open **AI → Connections → Add a connection → Any MCP server**. Supply the external server's HTTPS URL and, if needed, a least-privilege credential. Choose **Check** to test the connection. Add it to the agent under **Add → An app**; for generic MCP servers, choose all tools or an explicit allowlist. Agent approval settings still govern actions that change external state. The connection secret is stored in that Pawabase environment and is excluded from exports/backups.

The runtime accepts bearer, custom-header, or basic authentication for outbound MCP connections. It checks the destination against outbound URL/private-host rules before connecting. A failed Check may mean bad URL, network policy, expired key, insufficient external scopes, or incompatible transport. Diagnose those separately from Pawabase agent permissions. See the docs site's `ai/apps/overview.mdx` and `ai/agents/tools.mdx`.
