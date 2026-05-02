#!/usr/bin/env python3
"""Flag sentences with potentially overstrong manuscript language."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

RISK_TERMS = [
    "cause",
    "causes",
    "causal",
    "prove",
    "proves",
    "prevent",
    "prevents",
    "prevention",
    "eliminate",
    "guarantee",
    "mortality",
    "sudep",
    "life expectancy",
    "independent risk factor",
    "definitive",
    "conclusive",
    "must",
    "will",
]

SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("text_file", type=Path)
    args = parser.parse_args()

    text = args.text_file.read_text(encoding="utf-8", errors="replace")
    sentences = SENTENCE_RE.split(re.sub(r"\s+", " ", text))
    lowered_terms = [(term, re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE)) for term in RISK_TERMS]

    for idx, sentence in enumerate(sentences, start=1):
        hits = [term for term, pattern in lowered_terms if pattern.search(sentence)]
        if hits:
            print(f"{idx}\t{','.join(hits)}\t{sentence.strip()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
