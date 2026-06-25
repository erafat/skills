#!/usr/bin/env python3
"""Scan PubMed for configured author queries using NCBI E-utilities."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def load_config(path: str) -> dict:
    return json.loads(Path(path).expanduser().read_text(encoding="utf-8"))


def fetch_json(url: str, params: dict[str, str]) -> dict:
    full_url = url + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(full_url, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_xml(url: str, params: dict[str, str]) -> ET.Element:
    full_url = url + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(full_url, timeout=30) as response:
        return ET.fromstring(response.read())


def text_of(element: ET.Element | None) -> str:
    if element is None:
        return ""
    return " ".join("".join(element.itertext()).split())


def first_text(parent: ET.Element, path: str) -> str:
    return text_of(parent.find(path))


def article_date(article: ET.Element) -> str:
    pub_date = article.find(".//Journal/JournalIssue/PubDate")
    if pub_date is None:
        return ""
    year = first_text(pub_date, "Year")
    month = first_text(pub_date, "Month")
    day = first_text(pub_date, "Day")
    medline = first_text(pub_date, "MedlineDate")
    parts = [part for part in [year, month, day] if part]
    return " ".join(parts) or medline


def authors(article: ET.Element) -> list[str]:
    values: list[str] = []
    for author in article.findall(".//AuthorList/Author"):
        collective = first_text(author, "CollectiveName")
        if collective:
            values.append(collective)
            continue
        last = first_text(author, "LastName")
        initials = first_text(author, "Initials")
        fore = first_text(author, "ForeName")
        if last and initials:
            values.append(f"{last} {initials}")
        elif last and fore:
            values.append(f"{last} {fore}")
        elif last:
            values.append(last)
    return values


def doi(article: ET.Element) -> str:
    for article_id in article.findall(".//ArticleIdList/ArticleId"):
        if article_id.attrib.get("IdType") == "doi":
            return text_of(article_id)
    return ""


def citation(record: dict) -> str:
    authors_text = ", ".join(record["authors"])
    journal = record.get("journal_iso") or record.get("journal") or ""
    pieces = [
        authors_text + "." if authors_text else "",
        record["title"] + "." if record.get("title") else "",
        journal + "." if journal else "",
        record.get("publication_date", ""),
    ]
    if record.get("doi"):
        pieces.append("doi:" + record["doi"])
    pieces.append("PMID:" + record["pmid"])
    return " ".join(part for part in pieces if part).strip()


def parse_records(root: ET.Element, query: str) -> list[dict]:
    records: list[dict] = []
    for pubmed_article in root.findall(".//PubmedArticle"):
        article = pubmed_article.find(".//Article")
        if article is None:
            continue
        pmid = first_text(pubmed_article, ".//PMID")
        record = {
            "source": "pubmed",
            "query": query,
            "pmid": pmid,
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else "",
            "title": first_text(article, "ArticleTitle"),
            "authors": authors(article),
            "journal": first_text(article, "Journal/Title"),
            "journal_iso": first_text(article, "Journal/ISOAbbreviation"),
            "publication_date": article_date(article),
            "doi": doi(pubmed_article),
            "eligibility_status": "eligible",
            "candidate_section": "Published and Accepted Research Articles",
        }
        record["citation"] = citation(record)
        records.append(record)
    return records


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    parser.add_argument("--start", required=True, help="YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="YYYY-MM-DD")
    parser.add_argument("--query", action="append", default=[])
    parser.add_argument("--retmax", type=int, default=50)
    parser.add_argument("--output", default="")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    config = load_config(args.config)
    pubmed = config.get("pubmed", {})
    queries = args.query or pubmed.get("author_queries", [])
    if not queries:
        raise SystemExit("No PubMed queries configured.")

    api_key_env = pubmed.get("ncbi_api_key_env") or "NCBI_API_KEY"
    api_key = os.environ.get(api_key_env, "")
    common = {
        "db": "pubmed",
        "retmode": "json",
        "retmax": str(args.retmax),
        "datetype": "pdat",
        "mindate": args.start,
        "maxdate": args.end,
        "sort": "pub date",
        "tool": "cv-update-review",
    }
    if pubmed.get("email"):
        common["email"] = pubmed["email"]
    if api_key:
        common["api_key"] = api_key

    all_records: list[dict] = []
    errors: list[dict] = []
    delay = 0.12 if api_key else 0.35
    for query in queries:
        params = dict(common)
        params["term"] = query
        try:
            result = fetch_json(f"{EUTILS}/esearch.fcgi", params)
            ids = result.get("esearchresult", {}).get("idlist", [])
            if ids:
                time.sleep(delay)
                fetch_params = {
                    "db": "pubmed",
                    "id": ",".join(ids),
                    "retmode": "xml",
                    "tool": "cv-update-review",
                }
                if pubmed.get("email"):
                    fetch_params["email"] = pubmed["email"]
                if api_key:
                    fetch_params["api_key"] = api_key
                root = fetch_xml(f"{EUTILS}/efetch.fcgi", fetch_params)
                all_records.extend(parse_records(root, query))
        except Exception as exc:  # noqa: BLE001
            errors.append({"query": query, "error": str(exc)})
        time.sleep(delay)

    payload = {
        "source": "pubmed",
        "generated_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "window": {"start": args.start, "end": args.end},
        "records": all_records,
        "errors": errors,
    }

    text = json.dumps(payload, indent=2) + "\n"
    if args.output:
        output = Path(args.output).expanduser()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
        print(f"Wrote PubMed evidence: {output}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
