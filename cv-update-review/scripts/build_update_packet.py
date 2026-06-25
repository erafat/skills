#!/usr/bin/env python3
"""Build a Markdown CV update packet from evidence JSON files."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from collections import defaultdict
from pathlib import Path

from path_utils import find_basecamp_root, resolve_path


def load_json(path: str) -> dict:
    return json.loads(Path(path).expanduser().read_text(encoding="utf-8"))


def md_escape(value: str) -> str:
    return (value or "").replace("\n", " ").strip()


def record_label(record: dict) -> str:
    return record.get("title") or record.get("citation") or record.get("url") or "Untitled candidate"


def draft_entry(record: dict) -> str:
    if record.get("source") == "pubmed":
        return record.get("citation") or record_label(record)
    if record.get("source") == "rss":
        title = record_label(record)
        feed = record.get("feed_name") or "configured feed"
        published = record.get("published") or "date not parsed"
        return f"Public item on {feed}: {title}. ({published})"
    return record_label(record)


def evidence_text(record: dict) -> str:
    parts = []
    if record.get("url"):
        parts.append(record["url"])
    if record.get("pmid"):
        parts.append("PMID: " + record["pmid"])
    if record.get("query"):
        parts.append("query: " + record["query"])
    if record.get("feed_url"):
        parts.append("feed: " + record["feed_url"])
    return "; ".join(parts) or "Evidence source recorded in JSON."


def status_for(record: dict, recurring_policy: str) -> str:
    status = record.get("eligibility_status") or "hold_for_confirmation"
    title = record_label(record).lower()
    if recurring_policy == "major_milestones_only" and any(token in title for token in ["episode", "newsletter", "digest"]):
        return "hold_for_confirmation"
    return status


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    parser.add_argument("--start", required=True)
    parser.add_argument("--end", required=True)
    parser.add_argument("--evidence", action="append", default=[])
    parser.add_argument("--manual-note", action="append", default=[])
    parser.add_argument("--output", required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    config = load_json(args.config)
    basecamp_root = find_basecamp_root(args.config)
    records: list[dict] = []
    source_summaries: list[str] = []
    errors: list[dict] = []

    for path in args.evidence:
        payload = load_json(path)
        payload_records = payload.get("records", [])
        records.extend(payload_records)
        errors.extend(payload.get("errors", []))
        source_summaries.append(f"- `{path}`: {len(payload_records)} record(s)")

    for note in args.manual_note:
        records.append(
            {
                "source": "manual",
                "title": note,
                "eligibility_status": "hold_for_confirmation",
                "candidate_section": "Manual Recall / Needs Placement",
            }
        )

    recurring_policy = config.get("eligibility", {}).get("recurring_media_policy", "major_milestones_only")
    grouped: dict[str, list[dict]] = defaultdict(list)
    counts: dict[str, int] = defaultdict(int)
    for record in records:
        section = record.get("candidate_section") or "Needs Section Review"
        status = status_for(record, recurring_policy)
        record["_resolved_status"] = status
        counts[status] += 1
        grouped[section].append(record)

    today = dt.date.today().isoformat()
    owner = config.get("owner_display_name") or "CV owner"
    lines = [
        "---",
        "type: cv_update_packet",
        f"created: {today}",
        f"source_window_start: {args.start}",
        f"source_window_end: {args.end}",
        "generated_by: skill:cv-update-review",
        f"config_profile: {config.get('profile_name', args.config)}",
        "---",
        "",
        f"# CV Update Packet - {today}",
        "",
        f"Prepared for: **{owner}**",
        "",
        "## Source Window",
        "",
        f"- Window: **{args.start} -> {args.end}**",
        f"- Config: `{args.config}`",
        f"- CV document checked: `{resolve_path(config.get('cv_document', ''), basecamp_root)}`",
        "- Word edit performed: **No**",
        "",
        "## Evidence Sources",
        "",
    ]
    lines.extend(source_summaries or ["- No evidence files supplied."])
    if config.get("website_urls"):
        lines.append("- Manual website checks configured:")
        lines.extend([f"  - {url}" for url in config["website_urls"]])
    if config.get("manual_scholar_sources"):
        lines.append("- Manual Google Scholar/profile checks configured:")
        lines.extend([f"  - {url}" for url in config["manual_scholar_sources"]])
    if errors:
        lines.append("")
        lines.append("### Source Errors")
        lines.extend([f"- {error}" for error in errors])

    lines.extend(
        [
            "",
            "## Candidate Entries",
            "",
            "Confidence key:",
            "- **High** = date/title/role/venue verified by direct evidence",
            "- **Medium** = supported, but section/wording/evidence needs confirmation",
            "- **Low** = insufficient evidence; do not insert without explicit approval",
            "",
        ]
    )

    if not grouped:
        lines.append("No candidate entries found for this window.")
    for section, section_records in grouped.items():
        lines.append(f"### {section}")
        lines.append("")
        for index, record in enumerate(section_records, start=1):
            status = record["_resolved_status"]
            confidence = "High" if record.get("source") == "pubmed" and record.get("pmid") else "Medium"
            if status != "eligible":
                confidence = "Medium"
            lines.extend(
                [
                    f"{index}. **{md_escape(record_label(record))}**",
                    f"- Eligibility: `{status}`",
                    f"- Proposed CV entry: *{md_escape(draft_entry(record))}*",
                    f"- Evidence: {md_escape(evidence_text(record))}",
                    f"- Confidence: **{confidence}**",
                    "- Needs confirmation: section placement and final wording",
                    "",
                ]
            )

    lines.extend(
        [
            "## Recommended Exclusions / Holds",
            "",
        ]
    )
    held = [record for record in records if record.get("_resolved_status") != "eligible"]
    if held:
        for record in held:
            lines.append(f"- **{md_escape(record_label(record))}** - held for confirmation under current eligibility rules.")
    else:
        lines.append("- None identified.")

    lines.extend(
        [
            "",
            "## Approval Checklist",
            "",
            "| Include? | Candidate | Section | Final wording approved? | Evidence sufficient? |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for record in records:
        lines.append(
            f"| pending | {md_escape(record_label(record))} | {md_escape(record.get('candidate_section', ''))} | pending | pending |"
        )

    lines.extend(
        [
            "",
            "## Items Requiring Confirmation Before Word Edit",
            "",
            "- Confirm which candidates should be included.",
            "- Confirm final section placement.",
            "- Confirm final wording after comparing against the current CV style.",
            "- Confirm evidence is sufficient for every included item.",
            "",
            "## Summary Counts",
            "",
        ]
    )
    if counts:
        for status, count in sorted(counts.items()):
            lines.append(f"- `{status}`: {count}")
    else:
        lines.append("- No candidates.")

    output = resolve_path(args.output, basecamp_root)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote CV update packet: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
