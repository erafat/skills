#!/usr/bin/env python3
"""Create a dated copy of a Word CV without modifying the original."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
from pathlib import Path

from path_utils import find_basecamp_root, resolve_path


def load_config(path: str) -> dict:
    return json.loads(Path(path).expanduser().read_text(encoding="utf-8"))


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    counter = 2
    while True:
        candidate = parent / f"{stem}_v{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="")
    parser.add_argument("--docx", default="")
    parser.add_argument("--output-dir", default="")
    parser.add_argument("--date", default=dt.date.today().isoformat())
    parser.add_argument("--force", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    config = load_config(args.config) if args.config else {}
    basecamp_root = find_basecamp_root(args.config or None)
    source = resolve_path(args.docx or config.get("cv_document", ""), basecamp_root)
    output_dir = resolve_path(args.output_dir or config.get("output_dir", ""), basecamp_root)
    if not source.exists():
        raise SystemExit(f"Missing source CV: {source}")
    if source.suffix.lower() != ".docx":
        raise SystemExit(f"Expected a .docx file: {source}")
    if not output_dir:
        raise SystemExit("Missing output directory.")
    output_dir.mkdir(parents=True, exist_ok=True)

    target = output_dir / f"{source.stem}_{args.date}.docx"
    if target.exists() and not args.force:
        target = unique_path(target)
    shutil.copy2(source, target)
    payload = {
        "source": str(source),
        "copy": str(target),
        "date": args.date,
        "original_preserved": True,
    }
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
