# TypeScript and JavaScript client

Install `@pawabase/client`. The verified local 0.1.0 client exports `createClient`, `PawabaseClient`, typed errors, auth, data, storage, functions, flows, routes, realtime, `request`, and `status`. It supports ESM/CommonJS and standard `fetch`/`WebSocket`. Browser code must use a publishable key.

```ts
import { createClient } from "@pawabase/client";

const pb = createClient({ url, apiKey: publishableKey, environment: "production" });
await pb.auth.signInWithPassword({ email, password });
const page = await pb.from("tasks").eq("done", false).order("created_at", "desc").perPage(20);
const task = await pb.from("tasks").create({ title: "Review", done: false });
await pb.from("tasks").update(task.id, { done: true });
```

The user session is shared across client modules and refreshed by the auth client. Browser storage defaults to localStorage; supply an adapter where unavailable. Use `pb.asUser(accessToken)` on a server request to apply that person's policies. Use a separate server-only secret-key client for administration. Call `pb.dispose()` when discarding the client.

## Verified 0.1.0 surface

| Area | Methods and behavior |
| --- | --- |
| Records | `from(name)` / `resource(name)`; immutable query builders with `eq`, `where`, `select`, `expand`, `order`, `page`, `perPage`, `first`, `count`, `all`; records with `get`, `maybeGet`, `create`, `createMany`, `update`, `delete`. |
| Auth | `signUp`, `signInWithPassword`, magic link, OAuth URL/redirect, `getUser`, `updateUser`, `signOut`, `getSession`, MFA, sessions, organizations, token profiles. MFA sign-in can return `mfa_required`. |
| Storage | `storage.from(bucket)` for upload, download, list, remove, public and signed URLs. |
| Server logic | `functions.invoke`, `flows.run`, `routes` methods; `request(method, path)` for a verified endpoint without a wrapper. |
| Realtime | `realtime.channel`, `publish`, socket connect/status; channel subscribe/send/track/history. See [realtime](realtime.md). |

The verified 0.1.0 client does **not** expose the newer docs' `pb.ai`, `pb.manage`, or SSE `pb.realtime.stream` methods. Use the target version's exports or an authenticated raw request. Do not import `@pawabase/client/manage` unless the installed package exports that subpath.

## Query and failure details

One server filter is retained per field; the client rejects repeated bounds on the same field. `eq(field, false)` is sent as `is.false`. Commas inside `in` values are refused. `createMany` is not atomic. Under per-row policies, `total` can be `null` and pages can be short. A `404` can mean a read rule hid a row.

Errors derive from `PawabaseError`. HTTP subclasses include `AuthenticationError`, `PermissionError`, `NotFoundError`, `ValidationError`, `ConflictError`, `RateLimitError`, and `ServerError`; retain `status`, `code`, and `requestId` for diagnosis. `NetworkError`, `TimeoutError`, `AbortError`, `ConfigError`, `InvalidQueryError`, and `RealtimeError` cover other failures. The client follows `Retry-After` on 429; it retries transient failures for safe/idempotent calls, but ordinary POST/PATCH are not repeated after uncertain network failure unless explicitly marked idempotent. Make server side effects safe for duplicate attempts before opting in.

Generate a `Database` type from the environment's OpenAPI with `pawabase-types`, then `createClient<Database>(...)`. Run its `--check` option in CI if schema drift matters. Expanded relation types may need manual augmentation.

Check installed declarations for signatures. The verified source areas are `src/client.ts`, `data.ts`, `auth.ts`, `files.ts`, `functions.ts`, `realtime.ts`, `http.ts`, and `errors.ts` in the TypeScript SDK repository.
