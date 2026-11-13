# Pawabase for coding agents

[![Check skill](https://github.com/Pawabase/pawabase-skill/actions/workflows/check.yml/badge.svg)](https://github.com/Pawabase/pawabase-skill/actions/workflows/check.yml)

The official, open Pawabase skill. It teaches an AI coding agent how Pawabase fits together, when to use each SDK or HTTP endpoint, and how to verify the target environment before changing it. It includes TypeScript, Python, auth, data, policies, storage, realtime, flows, automation, AI, Cloud, and operations.

**The skill and MCP are complementary.** The skill provides instructions and version-aware guidance. Pawabase's optional MCP server gives an AI client live, scoped access to one environment. Installing the skill alone does not connect to a project.

## 1. Install the skill

For Codex, clone into the user skills directory documented by [OpenAI](https://learn.chatgpt.com/docs/build-skills):

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/Pawabase/pawabase-skill.git ~/.agents/skills/pawabase
```

Start a new Codex session and ask: **“Use `$pawabase` to help me build a signed-in Pawabase app.”** Codex can also select it automatically for Pawabase tasks. For a repository-only installation, place the same folder under `.agents/skills/pawabase` in your project. If an existing skill with the same name is already installed, update that copy instead of keeping two copies.

The entrypoint is [SKILL.md](SKILL.md). It routes to short, focused references; the [scenario map](references/scenario-map.md) handles common tasks, and the [docs catalog](references/docs-catalog.md) locates all 244 pages in the checked Pawabase docs revision.

## 2. Optionally connect Pawabase MCP

Use MCP when you want your AI client to inspect a real project, read logs, review definitions, or build resources. This connects **your AI client to Pawabase**. A Pawabase agent calling an outside MCP server is a different setup, covered in the [MCP guide](references/mcp.md).

1. In Pawabase Studio, choose the intended environment and open **AI → AI tools**. Create a secret key with **Look only** (`ai-read`) for inspection, or **Build with me** (`ai-build`) for development changes. Copy it once into your local secret store. A publishable `pb_pk_` key will not work for management MCP.
2. Put the secret key in `PAWABASE_MCP_KEY` in the environment that launches Codex. Do not commit it or paste it into this repository.
3. Add this to `~/.codex/config.toml`, replacing the URL with your project gateway URL:

   ```toml
   [mcp_servers.pawabase]
   url = "https://YOUR-API/mcp/v1"
   env_http_headers = { apikey = "PAWABASE_MCP_KEY" }
   default_tools_approval_mode = "writes"
   startup_timeout_sec = 20
   tool_timeout_sec = 60
   ```

4. Run `codex mcp list`, inspect `/mcp` in the Codex terminal UI, then ask: **“Using Pawabase MCP, list the tables in development.”** The key is tied to its environment. Use a separate read-only key for production.

Pawabase serves stateless Streamable HTTP at **`POST /mcp/v1`**. It accepts the `apikey` header or a Bearer secret key. It does not offer the older HTTP+SSE MCP transport; `GET /mcp/v1` returning `405` is expected. Remote clients need an HTTPS gateway. See [Pawabase MCP setup and troubleshooting](references/mcp.md), [Pawabase's runtime MCP guide](https://github.com/Pawabase/pawabase/blob/main/docs/mcp.md), and the [official Codex MCP configuration](https://learn.chatgpt.com/docs/extend/mcp?surface=cli).

### Other AI clients

Claude Code, Cursor, and other Streamable HTTP clients use the same `/mcp/v1` URL with a scoped secret key in an `apikey` header or Bearer authentication. The [MCP guide](references/mcp.md) includes a Claude Code example, local `pawabase-server mcp` stdio setup, protocol checks, and common failures. A hosted ChatGPT connection depends on the workspace's supported authentication method; an OAuth-only connector cannot authenticate directly to Pawabase's API-key MCP endpoint.

### Pawabase agents using outside tools

To let a **Pawabase agent** call GitHub, Linear, or another service, open **AI → Connections → Add a connection → Any MCP server**, enter the external server's HTTPS URL and credential, choose **Check**, then add that connection to the agent and limit its tools. This is outbound from Pawabase and does not use your `/mcp/v1` management key. See [outbound MCP](references/mcp.md).

## What the skill covers

| Area | Guidance |
| --- | --- |
| Build an app | JS/TS and Python clients, raw HTTP, generated types, auth sessions, SSR, records, files, live updates |
| Secure it | Publishable versus secret keys, per-operation policies, organizations, machine identities, channel and bucket rules |
| Add behavior | Flows, custom routes, events, schedules, webhooks, jobs, mail, agents and vector search |
| Ship and operate | Environments, IaC, migrations, API versions, previews, backups, logs, incidents and quotas |
| Connect AI | Inbound Pawabase MCP, outbound agent MCP, tool scopes, approvals, audit, transport troubleshooting |

The skill checks versions because the checked `@pawabase/client` 0.1.0 and Python `pawabase` 0.2.0 packages expose less than some newer product documentation. It does not invent SDK methods to fill that gap. See the [source and compatibility map](references/source-map.md) and [capability boundaries](references/capability-boundaries.md).

## Maintain the skill

From this repository, with a sibling checkout of `Pawabase/pawabase-docs`:

```bash
python3 scripts/check_skill.py --docs ../pawabase-docs
python3 scripts/build_catalog.py --docs ../pawabase-docs --check
```

To refresh the docs catalog after docs changes, run `python3 scripts/build_catalog.py --docs ../pawabase-docs` and review the diff. CI checks links and the catalog against the pinned docs revision. The skill-creator validator can check the `SKILL.md` manifest separately. Keep the [source map](references/source-map.md) current when SDKs or runtime behavior change.
