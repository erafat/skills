# Workflow 04: Reference Search

## Overview

This workflow searches PubMed (and optionally bioRxiv/medRxiv) to find appropriate references for each claim needing citations.

## Step 1: Confirm Search Sources

```
1. Load search source preferences from config

2. Confirm with user:
"I will search the following databases for references:

✅ PubMed (peer-reviewed literature)
{❌/✅} bioRxiv (biology preprints)
{❌/✅} medRxiv (medical preprints)

Change search sources? (yes/no):"

3. If yes, allow user to toggle sources

4. Confirm search depth:
"Search depth:
- Standard: 5 candidates per claim (faster)
- In-depth: 10 candidates per claim (more thorough)

Current setting: {setting}. Change? (yes/no):"
```

## Step 2: Prepare Search Queries

```
For each claim needing new references:

1. Extract search keywords from claim:
   - Key nouns and medical/scientific terms
   - Remove common words (the, a, is, are)
   - Identify MeSH terms where applicable

2. Build PubMed query:
   Primary query: "{term1} AND {term2} AND {term3}"

   Add filters based on preferences:
   - Date range: AND ("2015"[Date - Publication] : "3000"[Date - Publication])
   - Article type: AND (Review[Publication Type]) -- if prefer_reviews

3. Build fallback queries (if primary returns few results):
   - Broader: "{term1} AND {term2}"
   - Related terms: Use MeSH synonyms

4. Store queries:
{
  "claim_id": 7,
  "primary_query": "metformin AND hepatic gluconeogenesis AND mechanism",
  "fallback_queries": [
    "metformin AND glucose production",
    "metformin AND liver AND diabetes"
  ]
}
```

## Step 3: Execute Searches

```
For each claim:

1. Display progress:
   "[████████████████████░░░░░░░░░░] 65% - Searching for claim {n} of {total}"
   "Query: {query}"

2. Search PubMed:
   - Execute primary query
   - Retrieve top {search_depth} results
   - If < 3 results, try fallback queries

3. Search preprint servers (if enabled):
   - bioRxiv: Search recent preprints
   - medRxiv: Search recent preprints
   - Mark results as [PREPRINT]

4. For each result, fetch:
   - PMID
   - Title
   - Authors
   - Journal
   - Year
   - Abstract
   - DOI
   - Citation count (if available)
   - Article type (review/primary research)

5. Handle rate limiting:
   - If rate limited, display: "Rate limit reached. Waiting..."
   - Implement exponential backoff
   - Continue after delay

6. Store results:
{
  "claim_id": 7,
  "search_results": [
    {
      "pmid": "12345678",
      "title": "Metformin inhibits hepatic gluconeogenesis...",
      "authors": ["Smith JA", "Jones BC"],
      "journal": "Diabetes",
      "year": 2023,
      "abstract": "...",
      "doi": "10.2337/db23-0123",
      "citation_count": 45,
      "article_type": "primary_research",
      "is_preprint": false,
      "source": "pubmed"
    }
  ]
}
```

## Step 4: Analyze and Rank Results

```
For each search result:

1. Relevance scoring (0-100):
   - Title match with claim keywords: +30 max
   - Abstract discusses claim topic: +40 max
   - Recent publication (last 5 years): +10
   - High citation count: +10
   - From preferred journal: +10

2. Quality indicators:
   - Citation count relative to field
   - Journal reputation (impact factor proxy)
   - Article type (review vs primary)
   - Open access status

3. Generate relevance explanation:
   "This paper directly addresses metformin's mechanism of action
    on hepatic glucose production, reporting a 30% reduction in
    gluconeogenesis through AMPK activation."

4. Detect controversies:
   - If results show conflicting conclusions
   - Flag claim as "controversial"
   - Include papers from both perspectives

5. Store analysis:
{
  "result_id": "pmid_12345678",
  "relevance_score": 85,
  "quality_metrics": {
    "citation_count": 45,
    "citation_percentile": "top 20%",
    "journal_reputation": "high",
    "article_type": "primary_research",
    "open_access": true
  },
  "relevance_explanation": "Directly addresses claim...",
  "recommended": true
}
```

## Step 5: Select Top Candidates

```
For each claim:

1. Rank results by combined score:
   combined_score = relevance_score * 0.7 + quality_score * 0.3

2. Select top candidates:
   - Standard depth: Top 5
   - In-depth: Top 10

3. Mark recommended choice:
   - Highest combined score gets "RECOMMENDED" badge
   - Flag any close alternatives

4. Handle special cases:
   - Controversial claims: Include opposing views
   - No good matches: Flag for user, suggest query refinement
   - All preprints: Warn user about peer review status

5. Update session state:
{
  "claim_id": 7,
  "candidates": [
    {
      "rank": 1,
      "pmid": "12345678",
      "recommended": true,
      "reason": "Best match: directly addresses mechanism, highly cited"
    },
    {
      "rank": 2,
      "pmid": "23456789",
      "recommended": false,
      "reason": "Good alternative: recent review article"
    }
  ],
  "controversial": false,
  "search_complete": true
}
```

## Step 6: Handle No Results / Poor Results

```
If no suitable results found:

1. Display:
   "⚠️ Claim #{n}: Limited results found

   Claim: '{claim_text}'
   Query: '{query}'
   Results: {count} papers, none highly relevant

   Options:
   a) Suggest alternative search terms
   b) Broaden the search
   c) Try different databases
   d) Skip this claim (user will find reference manually)

   What would you like to do?"

2. If user suggests terms:
   - Re-run search with new terms
   - Add to session for learning

3. If user skips:
   - Mark claim as "manual_reference_needed"
   - Continue with other claims
```

## Step 7: Progress Summary

```
After all searches complete:

Display:
"## Search Complete

[██████████████████████████░░░░] 80% - Reference search complete

### Results Summary

| Status | Claims |
|--------|--------|
| ✅ Good matches found | {n} |
| ⚠️ Limited options | {n} |
| ❌ No suitable results | {n} |
| ⚡ Controversial (multiple views) | {n} |

### Database Usage
- PubMed: {n} papers retrieved
- bioRxiv: {n} preprints retrieved
- medRxiv: {n} preprints retrieved

Total unique references found: {total}

Ready for interactive review."
```

## Completion

```
1. Update session state:
   - current_phase: "interactive_review"
   - search_completed_at: timestamp
   - last_updated: timestamp

2. Save session

3. Display:
   "[██████████████████████████░░░░] 80% - Search phase complete"

4. Proceed to Workflow 05: Interactive Review
```

## Error Handling

### PubMed Unreachable
```
Display: "Error: Cannot connect to PubMed. Check internet connection."
Action:
- Retry with exponential backoff (3 attempts)
- Offer to continue with preprint servers only
- Save progress and offer to resume later
```

### Rate Limiting
```
Display: "PubMed rate limit reached."
Action:
- Show countdown: "Resuming in {seconds}..."
- Implement 1s base delay, doubling each retry
- Max delay: 60 seconds
- Continue automatically after delay
```

### Search Timeout
```
Display: "Search timeout for claim #{n}."
Action:
- Save partial results
- Offer to retry or skip
- Continue with other claims
```

### API Errors
```
Display: "API error: {error_message}"
Action:
- Log error details
- Retry once
- If persistent, mark claim for manual handling
```

### Preprint Server Issues
```
Display: "Warning: Could not reach {server}. Continuing with PubMed only."
Action:
- Continue search with available sources
- Note limitation in results
```
