# Workflow 05: Interactive Review

## Overview

Present reference suggestions for user approval. Process feedback and iterate until all references are confirmed.

## Step 1: Introduction

```
"## Interactive Reference Review

I've found reference candidates for {total} claims.

For each claim, I'll show:
- The claim text and location
- Suggested references with relevance explanations
- Article type and availability info

You can: Approve, Reject, Request alternatives, or Skip each claim.

Let's begin."
```

## Step 2: Present Each Claim

Present claims in priority order (HIGH first).

### Claim Display Format

```
### Claim {current} of {total}

**Location:** {section}, paragraph {n}

> {claim_text}

Type: {claim_type} | Priority: {priority}

#### Suggested References

1. [RECOMMENDED] {authors} ({year})
   "{title}"
   {journal}
   - Type: {publication_type}
   - Access: {open_access_status}
   - Relevance: {explanation of why this paper supports the claim}
   - PMID: {pmid} | DOI: {doi}

2. {authors} ({year})
   "{title}"
   {journal}
   - Type: {publication_type}
   - Relevance: {explanation}
   - PMID: {pmid}

3. {authors} ({year})
   ...
```

### User Decision

```
Your decision:
1. Approve #1 (recommended)
2. Approve #2
3. Approve #3
4. Request alternatives
5. Skip (no citation needed)
6. Provide feedback for better search

Enter choice:
```

## Step 3: Handle Approve

```
When user approves:

1. Record the selected reference for this claim
2. Confirm: "Reference approved: {short_citation}"
3. Advance to next claim
```

## Step 4: Handle Request Alternatives

```
"What's wrong with the current suggestions?

a) Not relevant enough
b) Too old - need more recent
c) Wrong article type (need review/primary)
d) Looking for specific aspect: [describe]
e) Just show more options

Enter choice:"

Based on feedback:
- a) Refine keywords, search again
- b) Add date_from filter for last 3-5 years
- c) Add publication type filter
- d) Incorporate user's terms into query
- e) Show next batch of candidates

Run new search and present results.
```

## Step 5: Handle Feedback

```
"Describe what you're looking for:

Examples:
- 'Need a paper specifically about human trials'
- 'Looking for something from Nature or Science'
- 'Want a meta-analysis'
- 'Prefer papers by [author name]'

Your feedback:"

Parse feedback, build refined query, run search, present results.
```

## Step 6: Handle Controversial Claims

```
When a claim has conflicting evidence:

"### Controversial Claim

> {claim_text}

Papers SUPPORTING this claim:
1. {title} - {brief finding}

Papers with DIFFERENT conclusions:
2. {title} - {brief finding}

Options:
a) Cite only supporting evidence
b) Cite both perspectives (recommended for balanced discussion)
c) Revise the claim to be more nuanced
d) Review paper abstracts before deciding

Your choice:"
```

## Step 7: Progress Tracking

```
After each decision, show:

"{approved}/{total} claims resolved | {pending} remaining"
```

## Step 8: Review Summary

```
When all claims reviewed or user requests summary:

"## Review Summary

| Status | Count |
|--------|-------|
| Approved | {n} |
| Using existing ref | {n} |
| Skipped | {n} |
| Needs alternatives | {n} |
| Pending | {n} |

### Approved References

| # | Claim (truncated) | Reference | Type |
|---|-------------------|-----------|------|
| 1 | '50% of patients...' | Smith 2023 | Primary |
| 2 | 'Drug X inhibits...' | Jones 2024 | Review |

Options:
a) Continue reviewing pending claims
b) Finalize and apply approved references
c) Go back and change a decision"
```

## Step 9: Finalization

```
When user chooses to finalize:

1. Check for unresolved high-priority claims:
   If any remain: "Warning: {n} high-priority claims still pending. Continue anyway?"

2. Confirm:
   "You are about to add {count} references.
    Citation format: {format}
    Bibliography location: {location}

    Proceed? (yes/no)"

3. If yes: proceed to Workflow 06
4. If no: return to review
```

## Error Handling

### Reference No Longer Available
```
"Reference PMID:{pmid} could not be re-fetched."
Suggest alternatives.
```
