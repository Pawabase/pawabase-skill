# Pawabase skill

[![Check skill](https://github.com/Pawabase/pawabase-skill/actions/workflows/check.yml/badge.svg)](https://github.com/Pawabase/pawabase-skill/actions/workflows/check.yml)

The official Pawabase skill for AI coding agents. It teaches an agent how Pawabase fits together, which client or endpoint to
reach for, how to keep keys and access rules right, and how to prove a change works on the actual environment before calling it
done. It works with any agent that reads skills: Claude Code, Codex, Cursor and others.

It covers the TypeScript client (`@pawabase/client` 0.7), the Python client (`pawabase` 0.9), raw HTTP, auth and organizations,
access policies, data, storage, realtime and live queries, flows and routes, mail, AI models, agents and knowledge, environments,
releases, backups, and connecting AI tools over MCP.

## Use it without installing

The whole skill is also published as one file at **https://pawabase.com/SKILL.md**. Give your agent this prompt:

> Read https://pawabase.com/SKILL.md and follow it to add Pawabase as the backend for this project.

## Install

The skill is a folder: [`SKILL.md`](SKILL.md) is the entry point, and it loads the short [references](references) it needs.

**Claude Code**

```bash
git clone https://github.com/Pawabase/pawabase-skill.git ~/.claude/skills/pawabase
```

For one repository only, clone it into `.claude/skills/pawabase` in that repository.

**Codex**

```bash
git clone https://github.com/Pawabase/pawabase-skill.git ~/.agents/skills/pawabase
```

For one repository only, use `.agents/skills/pawabase` in that repository.

**Other agents**

Clone the folder wherever your agent loads skills or instructions from, and point it at `SKILL.md`. Nothing in the skill depends
on a particular agent.

Then start a new session and ask for something real, for example: *"Use the Pawabase skill to add sign-in and a tasks list to
this app."* Agents also pick the skill up on their own for Pawabase work. Keep one copy installed; to update, `git pull` in the
folder.

## Connect an environment (optional)

The skill on its own gives guidance. To let your agent look at and work on a real environment, connect it to Pawabase's MCP
server as well. The two work together: the skill decides what should happen, MCP lets the agent check and do it.

1. In Studio, open the environment you want, then **AI → AI tools**, and create a secret key with the scope you need:
   **Look only** (`ai-read`) to inspect, **Build with me** (`ai-build`) to make development changes. It is shown once.
2. Keep it in your shell or secret manager as `PAWABASE_MCP_KEY`. Never commit it, and never use a publishable `pb_pk_` key here.
3. Add the server to your agent, using your project's API address:

**Claude Code**

```bash
claude mcp add --transport http pawabase https://YOUR-API/mcp/v1 --header "apikey: $PAWABASE_MCP_KEY"
```

**Codex** (`~/.codex/config.toml`)

```toml
[mcp_servers.pawabase]
url = "https://YOUR-API/mcp/v1"
env_http_headers = { apikey = "PAWABASE_MCP_KEY" }
```

**Cursor and other clients** (`mcp.json`)

```json
{ "mcpServers": { "pawabase": { "url": "https://YOUR-API/mcp/v1", "headers": { "apikey": "${env:PAWABASE_MCP_KEY}" } } } }
```

4. Ask: *"Using Pawabase MCP, list the tables in this environment."*

A key belongs to one environment. Use a separate, read-only key for production. Pawabase serves stateless Streamable HTTP at
`POST /mcp/v1` and accepts the key as an `apikey` header or a Bearer token; `GET /mcp/v1` answering `405` is expected. The
[MCP reference](references/mcp.md) covers scopes, confirmations, local stdio, and troubleshooting.

Letting a **Pawabase agent** call outside tools (GitHub, Linear, any MCP server) is the other direction, set up in Studio under
**AI → Connections**. It is covered in the same reference.

## What the skill does

| Area | What the agent learns |
| --- | --- |
| Build | Clients for TypeScript and Python, raw HTTP, generated types, sessions and SSR, records and relations, files and image sizes, live queries and channels |
| Secure | Publishable, secret and machine keys; per-action policies; organizations, roles and company sign-in; bot protection; user API keys |
| Automate | Flows, custom routes, events, schedules, webhooks in and out, background jobs, mail |
| AI | The model gateway, embeddings and vector search, agents with approvals, knowledge bases, MCP in both directions |
| Ship and operate | Environments, reviewed promotion, API versions, previews, backups and restores, activity, traces, alarms, quotas |

It works from the installed package and the target environment's own OpenAPI, not from memory: before it uses a method it checks
that the installed version has it, and it says so when a feature needs a newer package or a raw request. See the
[source map](references/source-map.md) and [capability boundaries](references/capability-boundaries.md).

## Maintain

With [`Pawabase/pawabase-docs`](https://github.com/Pawabase/pawabase-docs) checked out beside this repository:

```bash
python3 scripts/check_skill.py --docs ../pawabase-docs        # links, docs pages, formatting
python3 scripts/build_catalog.py --docs ../pawabase-docs --check
python3 scripts/build_catalog.py --docs ../pawabase-docs      # refresh the docs catalog after docs change
python3 scripts/build_bundle.py --out ../pawabase-website/public/SKILL.md   # rebuild pawabase.com/SKILL.md
```

CI runs both checks against the docs revision pinned in [`.github/workflows/check.yml`](.github/workflows/check.yml). When an
SDK or the server changes, update the [source map](references/source-map.md) and the client references with what was verified,
and move the pin.
