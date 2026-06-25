#!/usr/bin/env python3
"""Scan configured RSS/Atom feeds for items in a date window."""

from __future__ import annotations

import argparse
import datetime as dt
import email.utils
import json
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


def load_config(path: str) -> dict:
    return json.loads(Path(path).expanduser().read_text(encoding="utf-8"))


def clean(text: str | None) -> str:
    return " ".join((text or "").split())


def child_text(element: ET.Element, names: list[str]) -> str:
    for name in names:
        found = element.find(name)
        if found is not None and clean("".join(found.itertext())):
            return clean("".join(found.itertext()))
    for child in element:
        local = child.tag.split("}", 1)[-1].lower()
        if local in [name.lower() for name in names]:
            return clean("".join(child.itertext()))
    return ""


def parse_date(value: str) -> dt.datetime | None:
    if not value:
        return None
    try:
        parsed = email.utils.parsedate_to_datetime(value)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=dt.timezone.utc)
        return parsed
    except Exception:  # noqa: BLE001
        pass
    try:
        normalized = value.replace("Z", "+00:00")
        parsed = dt.datetime.fromisoformat(normalized)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=dt.timezone.utc)
        return parsed
    except Exception:  # noqa: BLE001
        return None


def fetch_feed(url: str) -> ET.Element:
    request = urllib.request.Request(url, headers={"User-Agent": "cv-update-review/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return ET.fromstring(response.read())


def feed_items(root: ET.Element) -> list[ET.Element]:
    rss_items = root.findall(".//item")
    if rss_items:
        return rss_items
    return [element for element in root.iter() if element.tag.split("}", 1)[-1] == "entry"]


def item_link(item: ET.Element) -> str:
    direct = child_text(item, ["link"])
    if direct:
        return direct
    for child in item:
        if child.tag.split("}", 1)[-1] == "link" and child.attrib.get("href"):
            return child.attrib["href"]
    return ""


def scan_one(feed: dict, start: dt.datetime, end: dt.datetime, include_undated: bool) -> tuple[list[dict], list[dict]]:
    records: list[dict] = []
    errors: list[dict] = []
    name = feed.get("name") or feed.get("url")
    url = feed.get("url")
    if not url:
        return records, [{"feed": name, "error": "missing url"}]
    try:
        root = fetch_feed(url)
        for item in feed_items(root):
            raw_date = child_text(item, ["pubDate", "published", "updated", "date"])
            parsed = parse_date(raw_date)
            if parsed is None and not include_undated:
                continue
            if parsed is not None and not (start <= parsed <= end):
                continue
            records.append(
                {
                    "source": "rss",
                    "feed_name": name,
                    "feed_url": url,
                    "title": child_text(item, ["title"]),
                    "url": item_link(item),
                    "published": raw_date,
                    "summary": child_text(item, ["description", "summary", "content"]),
                    "eligibility_status": "hold_for_confirmation",
                    "candidate_section": "Digital Scholarship / Public Media",
                }
            )
    except Exception as exc:  # noqa: BLE001
        errors.append({"feed": name, "url": url, "error": str(exc)})
    return records, errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    parser.add_argument("--start", required=True, help="YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="YYYY-MM-DD")
    parser.add_argument("--output", default="")
    parser.add_argument("--include-undated", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    config = load_config(args.config)
    start = dt.datetime.fromisoformat(args.start).replace(tzinfo=dt.timezone.utc)
    end = dt.datetime.fromisoformat(args.end).replace(hour=23, minute=59, second=59, tzinfo=dt.timezone.utc)
    records: list[dict] = []
    errors: list[dict] = []
    for feed in config.get("rss_feeds", []):
        feed_records, feed_errors = scan_one(feed, start, end, args.include_undated)
        records.extend(feed_records)
        errors.extend(feed_errors)

    payload = {
        "source": "rss",
        "generated_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "window": {"start": args.start, "end": args.end},
        "records": records,
        "errors": errors,
    }
    text = json.dumps(payload, indent=2) + "\n"
    if args.output:
        output = Path(args.output).expanduser()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
        print(f"Wrote RSS evidence: {output}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
