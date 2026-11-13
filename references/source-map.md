# Source, compatibility, and verification

This repository is a portable skill, not a copy of all Pawabase documentation. Product docs, SDK releases, and a deployed server can differ. Resolve an implementation question in this order:

1. **Target deployment:** Studio's environment-specific API Explorer/OpenAPI, capabilities, and settings.
2. **Installed client:** package version, exported types or Python module members, and source if available.
3. **Product docs:** [Pawabase docs repository](https://github.com/Pawabase/pawabase-docs), especially the topic path below.
4. **Server implementation:** [Pawabase runtime repository](https://github.com/Pawabase/pawabase), for behavior not covered by the contract.

Do not elevate an example in newer docs to an SDK guarantee. If sources disagree, identify the exact version or environment and say what was verified.

## Verified local baseline when authored

| Artifact | Checked state | Consequence |
| --- | --- | --- |
| `@pawabase/client` | `0.1.0` checked-in package | Exports data, auth, storage, functions, flows, routes, realtime and raw `request`. No `ai` or `manage` export in `client.ts`. |
| Python `pawabase` | `0.2.0` wheel inspected | Flat data, function, event, flow, and deployment methods plus function kit/CLI. No `pb.auth`, `pb.from_`, `pb.realtime`, `pb.ai`, or `pb.manage`. The runtime inventory says functions are not a current product area; verify deployment support. |
| `pawabase-iac` | Separate package described in current docs | Python declarations plus `validate`, `emulate`, `plan`, `deploy`; do not confuse its CLI with the Python function kit's CLI. |
| Public OpenAPI | `pawabase-docs/openapi/public.json` snapshot | 77 public paths; excludes an environment's dynamic resource schema and management internals. |
| Product docs | Checked-out docs repository | Some pages describe a broader, newer client interface. Check installed versions before copying. |

Inspect Python with `python3 -c 'import pawabase; print(pawabase.__version__, pawabase.__all__)'`. Inspect TypeScript with `node_modules/@pawabase/client/package.json` and exported declarations. For raw HTTP, use the environment's OpenAPI; table fields, policies, and enabled operations vary.

For a command named `pawabase`, inspect `command -v pawabase`, `pawabase --help`, and the installed distribution. Do not infer that the function kit's `deploy` and IaC's `deploy` are interchangeable. For runtime feature status, read `PAWABASE_FEATURE_INVENTORY.md` section **Explicit boundaries and non-features** and check the deployed capability before proposing a legacy path.
The `/mcp/v1` management transport is excluded from generated OpenAPI; use the runtime's `docs/mcp.md` and `pawabase_server/mcp/` for its contract. The client tool catalog is filtered by the connected key's scopes.

## Topic locator

Paths below are relative to the [docs repository](https://github.com/Pawabase/pawabase-docs):

| Topic | Start with |
| --- | --- |
| Product model | `concepts/how-pawabase-fits-together.mdx` |
| TypeScript and Python | `quickstarts/javascript.mdx`, `quickstarts/node.mdx`, `quickstarts/react.mdx`, `quickstarts/python.mdx` |
| Data API | `database/how-data-works.mdx`, `database/rest-api.mdx`, `database/relations.mdx` |
| Access and auth | `reference/keys-and-security.mdx`, `policies/how-rules-work.mdx`, `auth/how-auth-works.mdx` |
| Realtime | `realtime/channels.mdx`, `realtime/record-changes.mdx`, `realtime/connection.mdx` |
| Storage | `storage/upload.mdx`, `storage/urls-and-links.mdx`, `storage/access.mdx` |
| Logic/automation | `logic/flows.mdx`, `automation/overview.mdx`, `automation/reliability.mdx` |
| AI | `ai/overview.mdx`, `ai/gateway.mdx`, `ai/agents/overview.mdx` |
| MCP and agent connections | `ai/mcp.mdx`, `ai/apps/overview.mdx`, plus runtime `docs/mcp.md` |
| Operations | `environments/overview.mdx`, `tools/iac/overview.mdx`, `activity/overview.mdx` |
| Cloud, release, recovery | `cloud/overview.mdx`, `environments/api-versions.mdx`, `backups/overview.mdx`, `guides/production-checklist.mdx` |

For contributor work, the runtime's `ARCHITECTURE.md` and `PAWABASE_FEATURE_INVENTORY.md` give the service map; actual behavior lives in `pawabase_server/`. The [TypeScript SDK](https://github.com/Pawabase/pawabase-js) and [Python SDK](https://github.com/Pawabase/pawabase-python) repositories provide package sources, subject to installed-version checks.
