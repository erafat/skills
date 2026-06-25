#!/usr/bin/env python3
"""Extract nearby text/style examples from a Word CV."""

from __future__ import annotations

import argparse
import json
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

from path_utils import resolve_path

NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def paragraph_text(paragraph: ET.Element) -> str:
    return "".join(node.text or "" for node in paragraph.findall(".//w:t", NS)).strip()


def paragraph_style(paragraph: ET.Element) -> str:
    style = paragraph.find("./w:pPr/w:pStyle", NS)
    return style.attrib.get(f"{{{NS['w']}}}val", "") if style is not None else ""


def has_numbering(paragraph: ET.Element) -> bool:
    return paragraph.find("./w:pPr/w:numPr", NS) is not None


def extract_paragraphs(docx: Path) -> list[dict]:
    with zipfile.ZipFile(docx) as archive:
        xml = archive.read("word/document.xml")
    root = ET.fromstring(xml)
    paragraphs: list[dict] = []
    for idx, paragraph in enumerate(root.findall(".//w:p", NS)):
        text = paragraph_text(paragraph)
        if not text:
            continue
        paragraphs.append(
            {
                "index": idx,
                "text": text,
                "style": paragraph_style(paragraph),
                "numbered_or_bulleted": has_numbering(paragraph),
            }
        )
    return paragraphs


def section_windows(paragraphs: list[dict], sections: list[str], max_examples: int) -> dict[str, list[dict]]:
    windows: dict[str, list[dict]] = {}
    for section in sections:
        lowered = section.lower()
        match_at = None
        for pos, paragraph in enumerate(paragraphs):
            if lowered in paragraph["text"].lower():
                match_at = pos
                break
        if match_at is None:
            windows[section] = []
            continue
        windows[section] = paragraphs[match_at : match_at + max_examples + 1]
    return windows


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--docx", required=True)
    parser.add_argument("--section", action="append", default=[])
    parser.add_argument("--max-examples", type=int, default=8)
    parser.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    docx = resolve_path(args.docx)
    if not docx.exists():
        raise SystemExit(f"Missing DOCX: {docx}")
    paragraphs = extract_paragraphs(docx)
    sections = args.section or []
    if args.json:
        payload = {
            "docx": str(docx),
            "paragraph_count": len(paragraphs),
            "sections": section_windows(paragraphs, sections, args.max_examples) if sections else {},
        }
        print(json.dumps(payload, indent=2))
        return 0

    print(f"# CV Style Extract\n\nDocument: `{docx}`\n")
    if not sections:
        print("## First Paragraphs\n")
        for paragraph in paragraphs[: args.max_examples]:
            print(f"- [{paragraph['index']}] style={paragraph['style'] or 'none'} bullet={paragraph['numbered_or_bulleted']} :: {paragraph['text']}")
        return 0

    for section, window in section_windows(paragraphs, sections, args.max_examples).items():
        print(f"## Section Match: {section}\n")
        if not window:
            print("- No matching section text found.\n")
            continue
        for paragraph in window:
            print(f"- [{paragraph['index']}] style={paragraph['style'] or 'none'} bullet={paragraph['numbered_or_bulleted']} :: {paragraph['text']}")
        print("")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
