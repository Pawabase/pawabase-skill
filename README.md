# Pawabase skill

An official Pawabase skill for coding agents. It routes Pawabase tasks to focused guidance on the system, TypeScript and Python clients, HTTP, auth and policies, data, storage, realtime, automation, AI, and operations. The skill distinguishes documented product capabilities from methods verified in a particular SDK release.

## Install in Codex

Clone this repository into your Codex skills directory:

```bash
git clone https://github.com/Pawabase/pawabase-skill.git ~/.codex/skills/pawabase
```

Then invoke `$pawabase` explicitly or let Codex discover it for Pawabase work. `SKILL.md` is the entrypoint; `references/` loads by topic.

## Source policy

The target environment's API Explorer and the installed SDK version take priority over general examples. The skill's [source map](references/source-map.md) records the baseline checked when it was written and points to the runtime, docs, and SDK repositories. Update that baseline as packages ship.

## Validate changes

```bash
python3 scripts/check_skill.py
python3 scripts/check_skill.py --docs ../pawabase-docs
```

The second command checks referenced docs paths against a local checkout. The skill-creator `quick_validate.py` checks the skill frontmatter and scaffold structure when available.
