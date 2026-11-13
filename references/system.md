# System model

## How the parts connect

A project contains isolated environments such as `development`, `staging`, and `production`. Each environment owns its database, users, keys, secrets, resources, rules, files, flows, and settings. The client points at an API URL and presents an environment's key. The public edge checks the key, origins, scopes, limits, rate limits, and quotas, then passes authenticated caller context to the server. The server checks the resource's access rule before reading or changing data. Write operations can emit events, invalidate caches, and broadcast realtime changes. Automation subscriptions can start flows or send webhooks in the background.

In the checked-in runtime, `pawabase_server` is one Sillo application and process with a public listener behind the edge plus an internal listener. Studio is a separate browser interface that calls its `/studio` API. Do not infer a microservice boundary between auth, data, flows, and realtime in this runtime.

## Data and policy

A **resource** exposes a database table through five independently configurable operations: list, get, create, update, and delete. Each operation can be disabled and has its own rule. Relations have their own target-resource read checks. A table's database schema and resource definition are related but distinct; after creating or changing a resource definition, migration may be required to change the physical table.

Rules can inspect `$auth`, `$record`, `$input`, `$request`, `$credential`, `$object`, `$event`, and `$now`. A rule may mean anyone, signed-in users, owner, role, permission, scope, or a custom condition. Secret keys and Studio pass rules. Ordinary list requests may return only allowed rows; `total` can be `null` when a per-row rule makes a correct count unavailable. One-record reads may return `404` for either absent or hidden records. Write-only fields are omitted from responses.

## Identity and keys

Every request needs `apikey`. A user request also carries `Authorization: Bearer <access token>`. A publishable key is meant for client apps and remains subject to policies. A secret key bypasses policies and can carry management scopes. A key belongs to one environment. Scopes restrict route families such as `data`, `storage`, `auth`, `flows`, `ai`, and `realtime`; management families require secret keys. User metadata is editable by the user and must not be used as authority for permissions.

Authentication includes sessions, email/password, links and codes, social and company sign-in, MFA, passkeys, roles, organizations, machine identities, and token profiles. Availability and setup vary by deployment. For a specific flow, read `pawabase-docs/auth/` and inspect the installed SDK's auth methods.

## Reliability and deployment

Events and reactions are at least once and can run independently or out of order. Make event handlers and webhook receivers idempotent. Realtime messages are for live delivery; store durable business state in records. Definitions can be copied or promoted between environments, while rows, users, keys, and secrets remain separate. Use backups and Activity/Observability when validating production changes.

Read `pawabase-docs/concepts/how-pawabase-fits-together.mdx`, `database/how-data-works.mdx`, `policies/how-rules-work.mdx`, `reference/keys-and-security.mdx`, and `environments/overview.mdx` for the detailed model.
