#!/usr/bin/env python3
"""Check portable skill links and optional Pawabase docs references."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\]\(([^)#]+)(?:#[^)]*)?\)")
DOC_PATH = re.compile(r"`([a-z][a-z0-9-]+/[a-z0-9-]+\.mdx)`")


def check(docs: Path | None) -> list[str]:
    errors: list[str] = []
    skill = ROOT / "SKILL.md"
    body = skill.read_text()
    if not re.match(r"\A---\nname: pawabase\ndescription: .+\n---\n", body):
        errors.append("SKILL.md: expected Pawabase YAML frontmatter")

    for file in sorted(ROOT.rglob("*.md")):
        content = file.read_text()
        for target in LINK.findall(content):
            if "://" not in target and not (file.parent / target).exists():
                errors.append(f"{file.relative_to(ROOT)}: broken link {target}")
        if docs is not None and file.parent == ROOT / "references":
            for target in DOC_PATH.findall(content):
                if not (docs / target).exists():
                    errors.append(f"{file.relative_to(ROOT)}: missing docs page {target}")
        for number, line in enumerate(content.splitlines(), 1):
            if line != line.rstrip():
                errors.append(f"{file.relative_to(ROOT)}:{number}: trailing whitespace")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--docs", type=Path, help="local pawabase-docs checkout")
    args = parser.parse_args()
    errors = check(args.docs)
    if errors:
        print("\n".join(errors))
        return 1
    print("Pawabase skill links and references are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
