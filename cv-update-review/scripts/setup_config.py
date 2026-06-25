#!/usr/bin/env python3
"""Create a public CV update review config file."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path

from path_utils import resolve_path


def prompt(label: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{label}{suffix}: ").strip()
    return value or default


def prompt_list(label: str) -> list[str]:
    print(f"{label} Enter one per line. Leave blank when done.")
    values: list[str] = []
    while True:
        value = input("> ").strip()
        if not value:
            return values
        values.append(value)


def parse_feed(value: str) -> dict[str, str]:
    if "=" in value:
        name, url = value.split("=", 1)
        return {"name": name.strip(), "url": url.strip()}
    return {"name": value.strip(), "url": value.strip()}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default=".cv-update-review/config.json")
    parser.add_argument("--profile-name", default="")
    parser.add_argument("--owner", default="")
    parser.add_argument("--cv-document", default="")
    parser.add_argument("--output-dir", default="")
    parser.add_argument("--author-query", action="append", default=[])
    parser.add_argument("--pubmed-email", default="")
    parser.add_argument("--ncbi-api-key-env", default="NCBI_API_KEY")
    parser.add_argument("--rss-feed", action="append", default=[], help="name=url or url")
    parser.add_argument("--website-url", action="append", default=[])
    parser.add_argument("--scholar-url", action="append", default=[])
    parser.add_argument("--local-activity-path", action="append", default=[])
    parser.add_argument("--local-search-root", action="append", default=[])
    parser.add_argument(
        "--cadence",
        choices=["monthly", "quarterly", "ad-hoc", "custom"],
        default="",
        help="How often to run the CV review.",
    )
    parser.add_argument("--custom-cadence", default="", help="Free-text cadence when --cadence=custom.")
    parser.add_argument(
        "--offer-automation",
        choices=["yes", "no"],
        default="",
        help="Whether setup should record that the user wants an automation offered/configured.",
    )
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--non-interactive", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    output = Path(args.output).expanduser()

    if output.exists() and not args.force:
        raise SystemExit(f"Config already exists: {output}. Use --force to overwrite.")

    if args.non_interactive:
        missing = [
            name
            for name, value in {
                "--profile-name": args.profile_name,
                "--owner": args.owner,
                "--cv-document": args.cv_document,
                "--output-dir": args.output_dir,
            }.items()
            if not value
        ]
        if missing:
            raise SystemExit("Missing required non-interactive values: " + ", ".join(missing))
    else:
        if not args.profile_name:
            args.profile_name = prompt("Profile name", "cv-profile")
        if not args.owner:
            args.owner = prompt("Name as it should appear in packets")
        if not args.cv_document:
            args.cv_document = prompt("Path to current Word CV (.docx); ${BASECAMP_ROOT} is supported")
        if not args.output_dir:
            args.output_dir = prompt("Output folder for packets and dated CV copies")
        if not args.author_query:
            args.author_query = prompt_list("PubMed author queries, e.g. Clinician JQ[Author].")
        if not args.rss_feed:
            args.rss_feed = prompt_list("RSS/Atom feeds, e.g. Personal site=https://example.org/feed.xml.")
        if not args.website_url:
            args.website_url = prompt_list("Public website URLs for manual verification.")
        if not args.scholar_url:
            args.scholar_url = prompt_list("Google Scholar/profile URLs for manual verification.")
        if not args.local_activity_path:
            args.local_activity_path = prompt_list("Local activity log/status files.")
        if not args.local_search_root:
            args.local_search_root = prompt_list("Local folders to search for activity evidence.")
        if not args.cadence:
            args.cadence = prompt("Review cadence: monthly, quarterly, ad-hoc, or custom", "monthly")
        if args.cadence == "custom" and not args.custom_cadence:
            args.custom_cadence = prompt("Custom review cadence")
        if not args.offer_automation:
            args.offer_automation = prompt("Offer to configure a scheduled automation? yes/no", "no")

    config = {
        "schema_version": 1,
        "profile_name": args.profile_name,
        "owner_display_name": args.owner,
        "cv_document": args.cv_document,
        "output_dir": args.output_dir,
        "pubmed": {
            "author_queries": args.author_query,
            "email": args.pubmed_email,
            "ncbi_api_key_env": args.ncbi_api_key_env,
        },
        "rss_feeds": [parse_feed(value) for value in args.rss_feed],
        "website_urls": args.website_url,
        "manual_scholar_sources": args.scholar_url,
        "local_activity_paths": args.local_activity_path,
        "local_search_roots": args.local_search_root,
        "eligibility": {
            "mode": "completed_public_accepted_only",
            "recurring_media_policy": "major_milestones_only",
            "require_user_confirmation_before_docx_edit": True,
        },
        "review_schedule": {
            "cadence": args.cadence or "monthly",
            "custom_cadence": args.custom_cadence,
            "offer_automation": (args.offer_automation or "no").lower() == "yes",
            "automation_mode": "packet_only_until_user_approval",
        },
        "cv_sections": [],
        "created_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
    }

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    out_dir = resolve_path(args.output_dir) if args.output_dir else None
    if out_dir:
        out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Wrote config: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
