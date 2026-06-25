#!/usr/bin/env python3
"""Scan configured local text files for dated activity evidence."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path

from path_utils import find_basecamp_root, resolve_path

TEXT_SUFFIXES = {".md", ".txt", ".csv", ".tsv", ".json", ".yaml", ".yml"}
ISO_DATE = re.compile(r"\b(20\d{2}-\d{2}-\d{2})\b")


def load_config(path: str) -> dict:
    return json.loads(Path(path).expanduser().read_text(encoding="utf-8"))


def parse_date(value: str) -> dt.date | None:
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        return None


def dates_in_line(line: str) -> list[dt.date]:
    dates: list[dt.date] = []
    for match in ISO_DATE.findall(line):
        parsed = parse_date(match)
        if parsed:
            dates.append(parsed)
    return dates


def is_text_file(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in TEXT_SUFFIXES and path.stat().st_size <= 1_500_000


def configured_files(config: dict, max_files: int, basecamp_root: Path) -> list[Path]:
    seen: set[Path] = set()
    files: list[Path] = []
    for raw_path in config.get("local_activity_paths", []):
        path = resolve_path(raw_path, basecamp_root)
        if is_text_file(path) and path not in seen:
            files.append(path)
            seen.add(path)
    for raw_root in config.get("local_search_roots", []):
        root = resolve_path(raw_root, basecamp_root)
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if len(files) >= max_files:
                return files
            if any(part.startswith(".") for part in path.parts):
                continue
            if is_text_file(path) and path not in seen:
                files.append(path)
                seen.add(path)
    return files


def line_matches_keywords(line: str, keywords: list[str]) -> bool:
    if not keywords:
        return True
    lowered = line.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def scan_file(path: Path, start: dt.date, end: dt.date, keywords: list[str], include_undated_keyword: bool) -> list[dict]:
    records: list[dict] = []
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except Exception as exc:  # noqa: BLE001
        return [
            {
                "source": "local",
                "path": str(path),
                "error": str(exc),
                "eligibility_status": "hold_for_confirmation",
            }
        ]
    for line_number, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped:
            continue
        line_dates = dates_in_line(stripped)
        dated_in_window = any(start <= value <= end for value in line_dates)
        keyword_hit = line_matches_keywords(stripped, keywords)
        if not dated_in_window and not (include_undated_keyword and keyword_hit):
            continue
        if not keyword_hit:
            continue
        records.append(
            {
                "source": "local",
                "path": str(path),
                "line_number": line_number,
                "title": stripped[:180],
                "text": stripped,
                "dates": [value.isoformat() for value in line_dates],
                "eligibility_status": "hold_for_confirmation",
                "candidate_section": "Local Activity / Needs Review",
            }
        )
    return records


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    parser.add_argument("--start", required=True)
    parser.add_argument("--end", required=True)
    parser.add_argument("--keyword", action="append", default=[])
    parser.add_argument("--include-undated-keyword", action="store_true")
    parser.add_argument("--max-files", type=int, default=500)
    parser.add_argument("--output", default="")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    config = load_config(args.config)
    basecamp_root = find_basecamp_root(args.config)
    start = dt.date.fromisoformat(args.start)
    end = dt.date.fromisoformat(args.end)
    keywords = args.keyword or [
        "accepted",
        "published",
        "presented",
        "delivered",
        "invited",
        "lecture",
        "grand rounds",
        "abstract",
        "poster",
        "award",
        "committee",
        "service",
        "mentorship",
        "peer review",
    ]

    records: list[dict] = []
    files = configured_files(config, args.max_files, basecamp_root)
    for path in files:
        records.extend(scan_file(path, start, end, keywords, args.include_undated_keyword))

    payload = {
        "source": "local",
        "generated_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "window": {"start": args.start, "end": args.end},
        "files_scanned": len(files),
        "records": [record for record in records if "error" not in record],
        "errors": [record for record in records if "error" in record],
    }
    text = json.dumps(payload, indent=2) + "\n"
    if args.output:
        output = Path(args.output).expanduser()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
        print(f"Wrote local evidence: {output}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
