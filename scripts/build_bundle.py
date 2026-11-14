#!/usr/bin/env python3
"""Build the single-file skill: SKILL.md plus every reference, as one Markdown document an AI can read from a URL.

    python3 scripts/build_bundle.py --out ../pawabase-website/public/SKILL.md
    python3 scripts/build_bundle.py --out ../pawabase-website/public/SKILL.md --check

Links between references become links to sections of the same file, and docs paths become links to the docs site.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS_SITE = "https://docs.pawabase.com"
REPOSITORY = "https://github.com/Pawabase/pawabase-skill"

# Reading order: how it fits, how to do the common jobs, the clients, then each area, then lookups.
ORDER = [
    "system", "recipes", "typescript", "python", "http", "auth-policies", "data", "storage", "realtime", "automation", "ai",
    "mcp", "operations", "platform-lifecycle", "capability-boundaries", "troubleshooting", "scenario-map", "source-map",
    "docs-catalog",
]

FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
HEADING = re.compile(r"^(#{1,5}) ", re.M)
FENCE = re.compile(r"^```.*?^```", re.M | re.S)
LINK = re.compile(r"\]\((?:references/)?([a-z-]+)\.md\)")
DOC_PATH = re.compile(r"`([a-z][a-z0-9-]+(?:/[a-z0-9-]+)+)\.mdx`")


def slug(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def outside_code(text: str, change) -> str:
    """Apply *change* to the prose only, leaving fenced code alone."""
    out, last = [], 0
    for block in FENCE.finditer(text):
        out.append(change(text[last:block.start()]))
        out.append(block.group(0))
        last = block.end()
    out.append(change(text[last:]))
    return "".join(out)


def build() -> str:
    skill = (ROOT / "SKILL.md").read_text()
    frontmatter = FRONTMATTER.match(skill)
    assert frontmatter, "SKILL.md needs frontmatter"
    body = skill[frontmatter.end():]

    sections: dict[str, tuple[str, str]] = {}
    for name in ORDER:
        text = (ROOT / "references" / f"{name}.md").read_text()
        title = text.splitlines()[0].lstrip("# ").strip()
        sections[name] = (title, text)
    missing = sorted({p.stem for p in (ROOT / "references").glob("*.md")} - set(ORDER))
    assert not missing, f"add these references to ORDER: {missing}"

    def links(prose: str) -> str:
        prose = LINK.sub(lambda m: f"](#{slug(sections[m.group(1)][0])})", prose)
        return DOC_PATH.sub(lambda m: f"[`{m.group(1)}`]({DOCS_SITE}/{m.group(1)})", prose)

    parts = [
        f"---\n{frontmatter.group(1)}\n---\n",
        "<!-- Built from " + REPOSITORY + " by scripts/build_bundle.py. Edit the skill there, not this file. -->\n\n",
        outside_code(body, links).rstrip() + "\n\n",
        "## How to use this file\n\n"
        "This is the whole Pawabase skill in one document: the rules above, then every reference below. Read the rules and the\n"
        "sections the task needs. Docs links go to the live docs at " + DOCS_SITE + "; the target environment's own OpenAPI\n"
        "(Studio → API Explorer) and the installed client remain the contract. To install the skill as a folder instead, clone\n"
        f"{REPOSITORY}.\n\n"
        "Contents:\n\n" + "\n".join(f"- [{title}](#{slug(title)})" for title, _ in sections.values()) + "\n",
    ]
    for title, text in sections.values():
        demoted = outside_code(text, lambda prose: HEADING.sub(lambda m: "#" + m.group(1) + " ", prose))
        parts.append("\n---\n\n" + outside_code(demoted, links).rstrip() + "\n")
    return "".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--check", action="store_true", help="fail when the file is out of date")
    args = parser.parse_args()
    bundle = build()
    if args.check:
        current = args.out.read_text() if args.out.exists() else ""
        if current != bundle:
            print(f"{args.out} is out of date: run scripts/build_bundle.py --out {args.out}")
            return 1
        print(f"{args.out} is up to date.")
        return 0
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(bundle)
    print(f"Wrote {args.out} ({len(bundle.splitlines())} lines, {len(bundle) // 1024} KB).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
