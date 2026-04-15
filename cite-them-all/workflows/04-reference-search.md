# Workflow 04: Reference Search

## Overview

Search PubMed (and optionally bioRxiv/medRxiv) for references to support each claim. Uses explicit MCP tool calls.

## Step 1: Confirm Search Settings

```
1. Confirm sources:
   "Searching: PubMed {+ bioRxiv/medRxiv if enabled}
    Candidates per claim: 5
    Change settings? (yes/no)"

2. If yes, allow toggling sources and candidate count
```

## Step 2: Build Search Queries

```
For each claim needing a new reference:

1. Extract search keywords:
   - Key scientific/medical terms from the claim
   - Remove common words (the, a, is, are)
   - Identify potential MeSH terms

2. Build primary PubMed query:
   "{term1} AND {term2} AND {term3}"

   Add date filter if prefer_recent:
   date_from: "{current_year - 10}"

3. Build fallback queries (if primary returns few results):
   - Broader: "{term1} AND {term2}"
   - With MeSH: "{term1}[MeSH Terms] AND {term2}"

Example:
  Claim: "Metformin inhibits hepatic gluconeogenesis"
  Primary: "metformin AND hepatic gluconeogenesis AND mechanism"
  Fallback: "metformin AND gluconeogenesis"
```

## Step 3: Execute PubMed Searches

```
For each claim:

1. Report: "Searching PubMed for claim {n} of {total}..."

2. Call search_articles:
   - query: primary query
   - max_results: 10
   - sort: "relevance"
   - date_from: (if prefer_recent)

3. If < 3 results, try fallback queries

4. For top results, call get_article_metadata with the PMIDs
   This returns for each paper:
   - Title
   - Authors
   - Journal
   - Year
   - Abstract
   - DOI
   - Publication type (review, clinical trial, etc.)
   - MeSH terms
```

## Step 3b: Expand with Related Articles (if needed)

```
If initial search returns fewer than 3 relevant results:

1. Take the PMID of the best result found
2. Call find_related_articles with that PMID
3. Call get_article_metadata for the top related articles
4. Add to candidate pool

This uses PubMed's word-weighted similarity analysis to find
papers that keyword search missed.
```

## Step 4: Search Preprint Servers (if enabled)

```
IMPORTANT: bioRxiv/medRxiv search_preprints has NO keyword search.
It can only browse by date range and subject category.

Strategy:
1. Determine the relevant bioRxiv category for this claim
   (use get_categories to see available categories)

2. Use search_preprints with:
   - recent_days: 90
   - category: relevant category
   - limit: 20

3. Manually assess titles for relevance to the claim

4. For any relevant preprints, use get_preprint for full metadata

5. Mark all preprint results clearly:
   "[PREPRINT - NOT PEER REVIEWED]"

Note: Most claims are better served by PubMed's peer-reviewed
literature. Preprints are supplementary.
```

## Step 5: Analyze and Rank Results

```
For each search result:

1. Relevance assessment (based on available data):
   - Does the title relate to the claim?
   - Does the abstract discuss the claim topic?
   - Is the paper recent (last 5 years)?
   - Is it the right article type? (review vs primary)
   - Is the journal recognized in this field?

2. Generate a relevance explanation:
   "This paper directly addresses metformin's mechanism of action
    on hepatic glucose production."

3. Note article type from get_article_metadata:
   - Review / Primary research / Clinical trial / Meta-analysis / Case report

4. Detect controversies:
   - If results show conflicting conclusions, flag the claim
   - Include papers from both perspectives

5. Select top 5 candidates per claim, with the best marked [RECOMMENDED]
```

## Step 5b: Deep Verification (optional, for top candidates)

```
For the top candidate per claim:

1. Use convert_article_ids to check for PMCID
2. If PMCID exists, use get_full_text_article to retrieve full text
3. Search the full text for content directly supporting the claim
4. Note findings in the relevance explanation

This helps distinguish papers that merely mention the topic
from papers that provide direct evidence for the claim.
```

## Step 6: Handle Poor Results

```
If no suitable results found for a claim:

"Claim #{n}: Limited results found

Claim: '{claim_text}'
Query: '{query}'

Options:
a) Suggest alternative search terms
b) Broaden the search
c) Try find_related_articles with a related paper
d) Skip (find reference manually)

What would you like to do?"
```

## Step 7: Search Summary

```
"## Search Complete

| Status | Claims |
|--------|--------|
| Good matches found | {n} |
| Limited options | {n} |
| No suitable results | {n} |
| Controversial (multiple views) | {n} |

Database usage:
- PubMed: {n} papers retrieved
{- bioRxiv/medRxiv: {n} preprints retrieved}

Ready for interactive review."
```

## Step 8: Proceed

```
Proceed to Workflow 05: Interactive Review
```

## Error Handling

### PubMed Unreachable
```
"Cannot connect to PubMed. Check internet connection."
Offer to retry or proceed with preprint servers only.
```

### Search Timeout
```
"Search timeout for claim #{n}."
Save partial results, offer to retry or skip.
```

### Preprint Server Issues
```
"Could not reach bioRxiv/medRxiv. Continuing with PubMed only."
```
