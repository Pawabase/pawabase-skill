---
name: pawabase
description: Build, integrate, troubleshoot, and operate Pawabase projects using its verified SDKs and HTTP API. Use for Pawabase-specific data, auth, policies, storage, realtime, flows, automation, AI, environments, and deployment work.
---

# Pawabase

Pawabase provides environment-scoped app backends: resources over database tables, identity, access rules, files, live channels, flows, events, AI, and operations. Use this skill to make correct Pawabase decisions and code against the version actually available to the user.

## Establish the contract

Identify the target project, environment, gateway URL, caller identity, key type, and installed SDK version when they matter. Inspect the target environment's generated OpenAPI in Studio for exact endpoints and schemas. Use [source and compatibility](references/source-map.md) to resolve disagreements between documentation and packages. Never assume a client method exists because Studio supports the feature.

For a broad or unfamiliar request, find the closest case in the [scenario map](references/scenario-map.md). If it is not listed, search the [docs catalog](references/docs-catalog.md) for the feature, check its current product status, then verify the deployed contract. Treat these maps as locators, not promises that every deployment supports every feature.

## Read by task

| Task | Reference |
| --- | --- |
| Architecture, environments, request flow | [System](references/system.md) |
| TypeScript, JavaScript, Node, React | [TypeScript client](references/typescript.md) |
| Python scripts, client, functions, CLI | [Python kit](references/python.md) |
| Raw requests or another language | [HTTP API](references/http.md) |
| Sign-in, sessions, keys, access rules | [Auth and policies](references/auth-policies.md) |
| Tables, queries, migrations, relations | [Data](references/data.md) |
| Buckets, uploads, URLs, files | [Storage](references/storage.md) |
| WebSocket, SSE, channels, presence, live records | [Realtime](references/realtime.md) |
| Flows, routes, jobs, events, webhooks, mail | [Automation](references/automation.md) |
| Models, vector search, agents, knowledge | [AI](references/ai.md) |
| Studio, management, IaC, releases, debugging | [Operations](references/operations.md) |
| Cloud setup, self-hosting, backups, API versions, incident recovery | [Platform lifecycle](references/platform-lifecycle.md) |
| Feature gaps, legacy paths, and unsupported behavior | [Capability boundaries](references/capability-boundaries.md) |
| Failing requests, missing data, live updates, jobs, or mail | [Troubleshooting](references/troubleshooting.md) |

Read only the relevant references. For a feature crossing areas, read both and verify the boundary with an actual request or test.

## Invariants

- Browser and mobile apps use `pb_pk_` publishable keys. User calls carry the user's access token. `pb_sk_` secret keys belong only on trusted servers and bypass access rules.
- Keys, data, identities, policies, secrets, and storage are environment-specific. A configured environment must match the key's environment.
- Access is checked by the server per operation. A one-record `404` can conceal a row the caller may not read. Test policies with real and unrelated users, not only a secret key.
- A resource definition and its physical database table are separate; changing the definition can require a migration.
- Background events can be delivered more than once. Make side effects idempotent. Realtime is a notification path; records hold durable state.
- Do not claim an SDK method, endpoint, or retry guarantee until verified in the installed version or target OpenAPI. Prefer a verified raw HTTP call when the SDK lacks a feature.
- Distinguish the Python function kit (`pawabase`) from Pawabase IaC (`pawabase-iac`). Both document a `pawabase` CLI; inspect the installed command and package before using it.
- Before destructive restore, schema, key, or bulk replay work, inspect the target environment and the concrete plan/backup. Pawabase backups exclude stored file bytes, secrets, and raw API keys.
