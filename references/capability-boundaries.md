# Capability boundaries and compatibility

Use this when an example seems to contradict the installed package or the user asks whether a feature is available. These boundaries come from the checked runtime feature inventory and SDK exports; verify against the target deployment before treating them as timeless product limits.

| Area | Checked boundary | Practical response |
| --- | --- | --- |
| Python functions | Python `pawabase` 0.2.0 has a function kit, while the current runtime inventory says functions are not a current product area. | Prefer flows, routes, jobs, or mounted code for a new current project. Use the kit only when its route/CLI is confirmed on the target deployment. |
| Python client | The checked 0.2.0 wheel has flat methods, not the docs' `pb.auth`, `pb.from_`, `pb.realtime`, `pb.storage`, `pb.ai`, or `pb.manage`. | Inspect the installed package; use newer compatible package or verified HTTP. |
| TypeScript client | Checked 0.1.0 has no `pb.ai`, `pb.manage`, `realtime.stream`, or `liveQuery` export. | Inspect installed declarations; use supported HTTP/protocol calls where needed. |
| IaC | `pawabase-iac` is a separate distribution; both it and the function kit document a `pawabase` command. | Inspect package/entrypoint and help before running `init`, `emulate`, `plan`, or `deploy`. |
| Realtime | SSE is subscribe-only; MQTT, MQTT over WebSocket, HTTP streaming, and long polling are not live in checked docs. Only durable channel kind changes persistence behavior. | Use WebSocket for interactive presence/publish and HTTP for publishing. |
| Pawabase MCP | `/mcp/v1` is stateless JSON-RPC over Streamable HTTP POST; no MCP SSE stream or session endpoints. Remote access needs a scoped secret key; local stdio has installation authority. | Configure an MCP client's HTTP transport, or explicitly launch `pawabase-server mcp` on a trusted host. |
| Search | PostgreSQL uses ranked full-text search; SQLite/MySQL use case-insensitive substring matching. No typo tolerance, highlights, or external search engine in the checked runtime. | Choose query and UI behavior for the actual database dialect. |
| Backups | Environment backups exclude stored object bytes, secret values, raw API keys, sessions, logs, and jobs. | Back up object storage separately and re-provision secrets/keys after restore. |
| Data cache | API writes invalidate a table's response cache; external SQL writes do not. | Invalidate or disable cache when another writer changes the table. |
| SQL | Studio write SQL needs explicit opt-in; the flow SQL query block is read-only. | Use resource blocks or a transaction block for flow writes. |
| Domains | Pawabase verifies/routes custom domains but does not act as a general certificate authority. | Provide TLS/proxy support in the deployment. |
| Dashboards | Public dashboards still observe resource policies. | Test with anonymous and real users. |
| Cloud vs server | Cloud accounts, organization billing, and plan administration are outside the core self-hosted runtime. | Route Cloud questions to Cloud docs and account controls, not server management endpoints. |

## Decide whether a path is safe to recommend

1. Verify the feature exists in the target environment or its generated OpenAPI, not only in a documentation page.
2. Verify the installed SDK exports the method. If it does not, use a raw HTTP request only after the target endpoint and auth scheme are confirmed.
3. Check whether the feature is deployment-specific, legacy, preview, or Cloud-only. State the distinction in the answer.
4. For migrations, bulk replay, restore, and other state-changing operations, inspect the preview/plan and actual target before executing.

The source for this boundary list is `PAWABASE_FEATURE_INVENTORY.md`, section **Explicit boundaries and non-features**, in the runtime repository. Recheck that section when the runtime changes.
