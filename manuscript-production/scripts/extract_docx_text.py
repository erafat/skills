#!/usr/bin/env python3
"""Extract visible text from a DOCX into a plain text file."""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def para_text(paragraph: ET.Element) -> str:
    parts: list[str] = []
    for node in paragraph.iter():
        if node.tag == f"{{{NS['w']}}}t":
            parts.append(node.text or "")
        elif node.tag == f"{{{NS['w']}}}tab":
            parts.append("\t")
        elif node.tag == f"{{{NS['w']}}}br":
            parts.append("\n")
    return "".join(parts).strip()


def extract_docx(path: Path) -> str:
    with zipfile.ZipFile(path) as zf:
        xml = zf.read("word/document.xml")
    root = ET.fromstring(xml)
    paragraphs = [para_text(p) for p in root.findall(".//w:p", NS)]
    paragraphs = [p for p in paragraphs if p]
    text = "\n\n".join(paragraphs)
    return re.sub(r"\n{3,}", "\n\n", text)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("docx", type=Path)
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args()

    if not args.docx.exists():
        print(f"Missing DOCX: {args.docx}", file=sys.stderr)
        return 2

    output = args.output or args.docx.with_suffix(".extracted.txt")
    text = extract_docx(args.docx)
    word_count = len(re.findall(r"\b\w+\b", text))
    output.write_text(text + "\n", encoding="utf-8")
    print(f"Wrote {output}")
    print(f"Words: {word_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
