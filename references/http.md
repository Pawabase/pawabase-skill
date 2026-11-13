# HTTP API and wire contracts

Use the gateway URL for the target environment. Every app request carries `apikey: pb_pk_...` or `pb_sk_...`. Add `Authorization: Bearer <access token>` when acting as a signed-in user. Use `Content-Type: application/json` for JSON bodies. An environment's Studio API Explorer supplies its generated resource schema and OpenAPI. The public snapshot is useful for route discovery, but it is not a substitute for that environment's contract.

## Data REST

For resource `orders`, the live version is `/rest/v1/orders`:

| Method | Path | Result |
| --- | --- | --- |
| `GET` | `/rest/v1/orders` | `{data, page, per_page, total}` |
| `GET` | `/rest/v1/orders/{id}` | One record or `404` if absent/hidden |
| `POST` | `/rest/v1/orders` | `201` and created record |
| `PATCH`, `PUT` | `/rest/v1/orders/{id}` | Partial update; `PUT` does not clear omitted fields |
| `DELETE` | `/rest/v1/orders/{id}` | `204` without body |
| `POST` | `/rest/v1/orders/similar` | Vector search if configured |

```bash
curl "$PAWABASE_URL/rest/v1/orders?filter%5Bstatus%5D=eq.paid&sort=-created_at&per_page=50&page=2" \
  -H "apikey: $PAWABASE_KEY" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

Query parameters: `filter[field]=operator.value`, `sort`, `page` (from 1), `per_page` (1–200), `select`, `expand`, `q`, and `paginate=false` (at most 5,000 matches). Operators: `eq`, `neq`, `gt`, `gte`, `lt`, `lte`, `like`, `ilike`, `in`, `nin`, `is`, `isnot`. URL encode values. The server retains one filter per field; do not send two range bounds on the same field. `total` can be `null` with per-row rules. Expansion checks the related resource's rule.

## Public route families in the checked snapshot

| Family | Examples | Purpose |
| --- | --- | --- |
| `/auth/v1` | `/signup`, `/token`, `/user`, `/sessions`, `/orgs`, `/mfa`, `/passkeys` | Identity and user account |
| `/storage/v1` | `/object/{bucket}/{key}`, `/list/{bucket}`, `/sign/{bucket}/{key}` | Files, lists, signed access |
| `/realtime/v1` | `/publish`, `/sse`, `/channels/{channel}/history` | Live messages and history |
| `/functions/v1/{name}` | POST, only on compatible deployments | Legacy/function-kit invocation; verify it exists |
| `/flows/v1/{name}` | POST | Named HTTP-triggered flow |
| `/ai/v1` | `/chat/completions`, `/embeddings`, `/agents/{name}/runs` | Models and agents |
| `/hooks/v1/{env}/{slug}` | POST | Inbound webhook |
| `/health/v1` | GET | Health |

The checked public snapshot does not enumerate every resource's dynamic `/rest/v1` routes, legacy/deployed `/functions/v1/{name}` functions, or the `/platform/v1` management API. Current runtime guidance favors flows and custom routes for server logic. Custom routes are served under `/rest/v1` according to their definitions. Do not guess a body for these families; inspect the operation in target OpenAPI. `/studio` uses a Cloud-signed Studio token, not an app key. Management calls require scoped secret credentials and are restricted to the key's environment.

Common errors: `401` missing/bad key or needed identity; `403` rule/scope denial; `404` absent/hidden record or disabled operation; `409` uniqueness; `422` input/constraint; `429` rate/quota; `5xx` server. Preserve status, code, details, and request id. Read the docs' `database/rest-api.mdx` and `reference/errors.mdx` for the full wire model.
