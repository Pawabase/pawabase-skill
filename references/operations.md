# Environments, deployment, management, and diagnosis

An environment is a separate backend: database rows, users, resources, policies, keys, secrets, buckets/files, auth and mail settings, flows, agents, and activity. Development, staging, and production should use distinct credentials. Copy/promote moves definitions, not data, users, keys, or secrets. The key used by an SDK must belong to its configured environment.

## Build changes

Studio is the browser control plane for resources, policies, auth, storage, realtime, logic, AI, mail, and Activity. For repeatable definitions, the docs' IaC workflow supports project configuration, tables, fields, relations, policies, buckets, flows, routes, webhooks, and deployment plans. A resource definition change may require a database migration. Inspect the plan and target environment, validate in development/staging, and confirm the physical schema before relying on the new API shape.

The product docs also describe management clients: `@pawabase/client/manage` and `pb.manage`. These are **not** present in the checked TypeScript 0.1.0 package exports or Python 0.2.0 wheel. Use them only after confirming a newer package exposes them; otherwise use verified management HTTP with an appropriately scoped secret key. A secret key can manage only its own environment. `/studio` needs a Cloud-signed Studio token and is not the ordinary app management endpoint.

Backups and restores affect durable state. Before a production schema change or restore, inspect the current backup/restore workflow and the target environment. Preview replay/redelivery/bulk actions when the endpoint supports dry run, and decide how duplicate side effects are handled. Avoid replaying successful events just to test an integration.

## Diagnose by layer

| Symptom | Check |
| --- | --- |
| `401` | Key presence/validity, environment, allowed origin/IP, bearer token or session expiry |
| `403` | Key scope, enabled operation, caller roles/org/assurance, specific policy |
| `404` on one row | Resource/path/id, operation enablement, read rule hiding the row |
| `409` or `422` | Unique/foreign-key constraint, field validation, schema migration |
| `429` | Key rate limit, environment quota, `Retry-After` |
| Realtime refusal | Channel rule, subscribe/publish difference, token, presence/history settings |
| Automation missing | Source event, subscription filter, flow run, job status, webhook delivery |

Preserve request id from SDK/API errors and trace it through Studio → Activity/Observability. Check the exact failed operation as the intended user, then use a secret key only as a controlled comparison. For runtime contributors, use the server's `ARCHITECTURE.md`, feature inventory, route decorators, and tests rather than inferring internal service boundaries. Read `environments/overview.mdx`, `environments/promote.mdx`, `tools/iac/overview.mdx`, `activity/overview.mdx`, `backups/overview.mdx`, and `tools/management-client.mdx` in the docs repo.
