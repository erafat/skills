# Workflow 03: Existing References Check

## Overview

Detect existing citations, verify they support their claims using PubMed tools, and identify reuse opportunities for new claims.

## Step 1: Detect Existing Citation Format

```
1. Scan manuscript for citation patterns:

   Numbered:
   - [1], [2], [1,2], [1-3]
   - (1), (2), (1,2), (1-3)

   Author-date:
   - (Author, Year)
   - (Author and Author, Year)
   - (Author et al., Year)

   Other indicators:
   - "References" or "Bibliography" section
   - DOI patterns: 10.xxxx/xxxxx
   - PMID mentions

2. Report: "Detected citation format: {format}. Found {count} existing citations."
```

## Step 2: Parse Existing References

```
1. Locate the reference list section (end of document)

2. For each reference, extract what's available:
   - Authors
   - Title
   - Journal
   - Year
   - Volume/Issue/Pages
   - DOI (if present)
   - PMID (if present)

3. Map inline citations to reference list entries

4. Report: "Parsed {count} existing references"
```

## Step 3: Ask About Verification

```
"I found {count} existing references. Would you like me to verify
that each reference actually supports the claim it's cited for?

This involves fetching each paper from PubMed and checking the abstract
against the claim. It takes additional time but helps ensure accuracy.

Verify existing references? (yes/no)"
```

## Step 4: Verify References (if requested)

Use PubMed tools to look up each existing reference. The tool sequence depends on what metadata is available:

### Resolution Strategy

```
For each existing reference:

1. If PMID is present:
   -> Use get_article_metadata with the PMID

2. If DOI is present but no PMID:
   -> Use convert_article_ids with id_type='doi' to get the PMID
   -> Then use get_article_metadata

3. If neither PMID nor DOI is present:
   -> Use lookup_article_by_citation with available fields:
      - journal (journal name or abbreviation)
      - year (publication year)
      - author (first author last name)
      - first_page (first page number)
      - volume (volume number)
   -> This returns the matched PMID
   -> Then use get_article_metadata

4. If lookup_article_by_citation fails:
   -> Fall back to search_articles with:
      query: "title keywords[Title] AND author[Author]"
   -> Pick the best match from results
```

### Claim-Support Analysis

```
For each verified reference:

1. Get the paper's abstract from get_article_metadata
2. Find where the reference is cited in the manuscript
3. Extract the claim/sentence it supports

4. Assess support level:
   - STRONG: Abstract directly addresses and supports the claim
   - MODERATE: Abstract partially relates to the claim
   - WEAK: Abstract doesn't clearly support the claim
   - MISMATCH: Abstract contradicts or is unrelated to the claim

5. Optionally deepen analysis:
   -> Use convert_article_ids to check for PMCID
   -> If PMCID exists, use get_full_text_article for full text
   -> Search full text for content that directly supports the claim
   -> This is more reliable than abstract-only assessment
```

## Step 5: Report Verification Results

```
"## Reference Verification Results

### Strong Support ({count})
These references clearly support their claims:

| # | Claim | Reference | Assessment |
|---|-------|-----------|------------|
| 1 | "50% develop neuropathy" | Smith 2024 | Reports 48% incidence |

### Moderate Support ({count})
These references partially support their claims:

| # | Claim | Reference | Note |
|---|-------|-----------|------|
| 3 | "Drug X is effective" | Jones 2023 | Study in mice, not humans |

### Weak/Mismatch ({count})
These references may not adequately support their claims:

| # | Claim | Reference | Issue |
|---|-------|-----------|-------|
| 5 | "Causes cancer" | Brown 2022 | Discusses correlation, not causation |

Recommendation: Review flagged references and consider replacements."

Allow user to:
- Keep reference as-is
- Find replacement reference
- Revise the claim to match the reference
```

## Step 6: Match Existing References to New Claims

```
1. For each new claim (from Workflow 02) without a citation:

2. Check if any existing reference could support it:
   - Compare claim keywords with reference topics/abstracts
   - Score: GOOD MATCH / POSSIBLE / NO MATCH

3. Present matches:

"## Reference Reuse Opportunities

Claim #7: 'Metformin reduces hepatic glucose production'
Location: Methods, paragraph 3

Potential existing reference:
  [3] Johnson AB et al. (2023) 'Metformin mechanisms in type 2 diabetes'
  Why: This paper discusses metformin's effects on glucose metabolism.

Your decision:
- Use existing reference [3]
- Search for a more specific reference
- Skip"
```

## Step 7: Summary

```
"## Summary

- Existing references verified: {count}
- References flagged for review: {count}
- New claims resolved with existing refs: {count}
- Claims still needing new references: {count}

Ready to search for new references?"
```

## Step 8: Proceed

```
Proceed to Workflow 04: Reference Search
```

## Error Handling

### Reference Not Found in PubMed
```
"Could not find reference: '{title}'"
Action: Mark as unverifiable, continue with others
```

### Malformed Reference List
```
"Warning: Could not parse some references."
Action: List unparseable entries, ask user to clarify or skip
```

### No Existing References
```
"No existing references found."
Action: Skip verification, proceed to reference search
```
