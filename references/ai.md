# AI gateway, vector search, and agents

Pawabase can keep provider credentials on the server, expose named models, generate embeddings, search vector fields, and run agents against project resources. A model name such as `chat` is an environment alias, not necessarily a provider model id. Each model/agent has access rules and usage controls. Provider keys must not enter app code.

The checked public OpenAPI snapshot includes `GET /ai/v1/models`, `POST /ai/v1/chat/completions`, `POST /ai/v1/embeddings`, `POST /ai/v1/agents/{name}/runs`, run inspection/decision routes, and knowledge document/search routes. Use that operation's schema in target OpenAPI before sending payloads. The verified TypeScript 0.1.0 client has no `pb.ai`; the verified Python 0.2.0 wheel has no `pb.ai`. Newer docs' `pb.ai.chat` examples require a version that actually exports it, otherwise use authenticated HTTP.

For semantic search, configure a vector field and embedding pipeline on a resource, then use its documented `/rest/v1/<table>/similar` route. The list policy governs search results; vector data can be omitted from ordinary reads. For knowledge bases, ingest documents and search them using the configured model and access rules. Agents use named tools/resources and should act under the requesting user's authority unless explicitly configured otherwise. Inspect approvals, step/time/cost limits, and run state before building automated mutations.

Debug AI failures by separating the provider connection, model alias, access rule, quota/cost limit, embedding pipeline, and agent tool permissions. Read `ai/gateway.mdx`, `ai/use-it.mdx`, `ai/vector-search.mdx`, `ai/agents/overview.mdx`, `ai/agents/approvals-and-limits.mdx`, and `ai/knowledge/overview.mdx` in the docs repo.

Pawabase's MCP endpoint is a management connection for external AI tools, distinct from an app-facing agent. Give each tool an environment-specific scoped key; a read-only production key and a build-capable development key have different consequences. Check the tool's granted scopes and the target environment before allowing it to change resources. Read `ai/mcp.mdx` for current connection and audit behavior.
