# Workflow 03: Existing References Check

## Overview

This workflow detects existing citations in the manuscript, verifies they support their claims, and identifies opportunities to reuse them for new claims.

## Step 1: Detect Existing Citation Format

```
1. Scan manuscript for citation patterns:

   Numbered patterns:
   - [1], [2], [1,2], [1-3]
   - (1), (2), (1,2), (1-3)
   - Superscript: ¹, ², ¹⁻³

   Author-date patterns:
   - (Author, Year)
   - (Author and Author, Year)
   - (Author et al., Year)
   - Author (Year)

   Other indicators:
   - "References" or "Bibliography" section
   - DOI patterns: 10.xxxx/xxxxx
   - PMID mentions

2. Determine primary format:
   - If multiple formats detected, ask user which is primary
   - Store detected format in session state

3. Display:
   "Detected citation format: {format_name}
   Found {count} existing citations in the manuscript."
```

## Step 2: Parse Existing References

```
1. Locate reference list section:
   - Search for "References", "Bibliography", "Works Cited"
   - May be at end of document

2. Parse each reference entry:
   For each reference, extract:
   - Authors
   - Title
   - Journal
   - Year
   - Volume/Issue/Pages
   - DOI (if present)
   - PMID (if present)

3. Map inline citations to reference list:
   - [1] → First reference entry
   - (Smith, 2024) → Entry by Smith in 2024

4. Store in session state:
{
  "existing_references": [
    {
      "ref_number": 1,
      "raw_text": "Smith JA, Jones BC. Title of paper...",
      "parsed": {
        "authors": ["Smith JA", "Jones BC"],
        "title": "Title of paper",
        "journal": "Nature",
        "year": 2024,
        "doi": "10.1038/xxxxx",
        "pmid": "12345678"
      },
      "cited_at": [
        {"claim_id": null, "location": "Introduction, Line 15"}
      ],
      "verified": false
    }
  ]
}

5. Display progress:
   "[██████████████░░░░░░░░░░░░░░░░] 40% - Parsed {count} existing references"
```

## Step 3: Ask User About Verification

```
Display:
"I found {count} existing references in your manuscript.

Would you like me to verify that each reference actually supports the claim it's cited for?

This involves:
1. Fetching each paper's abstract from PubMed
2. Analyzing if the paper supports the claim
3. Flagging any mismatches

This helps ensure citation accuracy but takes additional time.

Verify existing references? (yes/no):"

Store response in session state.
```

## Step 4: Verify References (If Requested)

```
For each existing reference:

1. Fetch paper details:
   - If DOI present: Look up via DOI
   - If PMID present: Fetch from PubMed
   - If neither: Search PubMed by title/authors

2. Get abstract and key findings

3. Find where reference is cited in manuscript:
   - Identify the claim/sentence it's attached to
   - Extract context (surrounding sentences)

4. Analyze support:
   Does the paper actually support the claim?

   Scoring:
   - STRONG: Paper directly addresses and supports the claim
   - MODERATE: Paper partially supports or is tangentially related
   - WEAK: Paper doesn't clearly support the claim
   - MISMATCH: Paper contradicts or doesn't relate to the claim

5. Store verification results:
{
  "verification": {
    "ref_number": 1,
    "claim_text": "50% of patients develop neuropathy",
    "paper_abstract": "...",
    "support_level": "strong|moderate|weak|mismatch",
    "analysis": "Paper reports 48% neuropathy incidence, directly supporting the claim",
    "flagged": false
  }
}

6. Update progress:
   "[████████████████░░░░░░░░░░░░░░] 50% - Verifying reference {n} of {total}"
```

## Step 5: Report Verification Results

```
Display:

"## Reference Verification Results

### ✅ Strong Support ({count})
These references clearly support their claims:
| # | Claim | Reference | Assessment |
|---|-------|-----------|------------|
| 1 | "50% develop neuropathy" | Smith 2024 | Reports 48% incidence |

### ⚠️ Moderate Support ({count})
These references partially support their claims:
| # | Claim | Reference | Note |
|---|-------|-----------|------|
| 3 | "Drug X is effective" | Jones 2023 | Study in mice, not humans |

### ❌ Weak/Mismatch ({count})
These references may not adequately support their claims:
| # | Claim | Reference | Issue |
|---|-------|-----------|-------|
| 5 | "Causes cancer" | Brown 2022 | Paper discusses correlation, not causation |

**Recommendation:** Review flagged references and consider finding alternatives."

Allow user to:
- Keep reference as-is
- Find replacement reference
- Revise the claim to match the reference
```

## Step 6: Match Existing References to New Claims

```
1. For each new claim (from Workflow 02) without a citation:

2. Check if any existing reference could support it:
   - Compare claim keywords with reference topics
   - Analyze if reference's abstract relates to claim

3. Score potential matches:
   - GOOD MATCH: Reference directly relevant
   - POSSIBLE: Reference tangentially related
   - NO MATCH: Reference unrelated

4. Store matches:
{
  "reuse_opportunities": [
    {
      "claim_id": 7,
      "claim_text": "Metformin reduces glucose levels",
      "existing_ref": 3,
      "match_quality": "good",
      "reason": "Reference 3 is a Metformin efficacy study"
    }
  ]
}

5. Display progress:
   "[██████████████████░░░░░░░░░░░░] 55% - Checking reference reuse opportunities"
```

## Step 7: Present Reuse Opportunities

```
Display:

"## Reference Reuse Opportunities

The following new claims could potentially use existing references:

### Claim #7: "Metformin reduces hepatic glucose production"
**Location:** Methods, Line 89

**Potential existing reference:**
> [3] Johnson AB et al. (2023) "Metformin mechanisms in type 2 diabetes"

**Why it might work:**
This paper discusses Metformin's effects on glucose metabolism, including hepatic pathways.

**Your decision:**
- [ ] Use existing reference [3]
- [ ] Search for a more specific reference
- [ ] Review the existing paper first

---

### Claim #12: "Insulin resistance precedes diabetes onset"
...

"

For each opportunity, get user decision:
- Use existing reference
- Search for new reference
- Skip (mark as needing new reference)
```

## Step 8: Update Session State

```
1. Update claims with reuse decisions:
   - Mark claims using existing references as "resolved"
   - Mark remaining claims as "needs_new_reference"

2. Summary:
{
  "existing_refs_summary": {
    "total_existing": 15,
    "verified": true,
    "strong_support": 10,
    "moderate_support": 3,
    "flagged": 2,
    "reused_for_new_claims": 4
  }
}

3. Display:
"## Summary

- Existing references verified: {count}
- References flagged for review: {count}
- New claims resolved with existing refs: {count}
- Claims still needing new references: {count}

Ready to search for new references?"
```

## Completion

```
1. Update session state:
   - current_phase: "reference_search"
   - last_updated: timestamp

2. Save session

3. Display:
   "[████████████████████░░░░░░░░░░] 60% - Existing reference check complete"

4. Proceed to Workflow 04: Reference Search
```

## Error Handling

### Reference Not Found in PubMed
```
Display: "Could not find reference #{n} in PubMed: '{title}'"
Action:
- Try alternative search (by DOI, authors)
- Mark as "unverifiable" and note for user
- Continue with other references
```

### Malformed Reference List
```
Display: "Warning: Could not parse some references in the bibliography."
Action:
- List unparseable entries
- Ask user to clarify or skip
```

### No Existing References
```
Display: "No existing references found in the manuscript."
Action:
- Skip verification step
- Proceed directly to reference search for all claims
```

### Rate Limiting
```
Display: "PubMed rate limit reached. Waiting {seconds} seconds..."
Action:
- Implement exponential backoff
- Continue after delay
- Show progress to user
```
