#!/usr/bin/env python3
"""Estimate manuscript word counts from a plain text extraction."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

SECTION_RE = re.compile(
    r"^(abstract|introduction|methods?|results?|discussion|conclusion|references?|bibliography|figure legends?)\b",
    re.IGNORECASE,
)
WORD_RE = re.compile(r"\b[\w'-]+\b")


def count_words(text: str) -> int:
    return len(WORD_RE.findall(text))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("text_file", type=Path)
    args = parser.parse_args()

    text = args.text_file.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    sections: list[tuple[str, list[str]]] = [("front_matter", [])]

    for line in lines:
        stripped = line.strip()
        match = SECTION_RE.match(stripped)
        if match and len(stripped.split()) <= 6:
            sections.append((match.group(1).lower(), []))
        sections[-1][1].append(line)

    total = count_words(text)
    print(f"total_words,{total}")
    for name, section_lines in sections:
        section_text = "\n".join(section_lines)
        print(f"{name},{count_words(section_text)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
