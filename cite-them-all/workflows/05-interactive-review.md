# Workflow 05: Interactive Review

## Overview

This workflow presents reference suggestions to the user for approval, processes feedback, and iterates until all references are confirmed.

## Step 1: Initialize Review Session

```
1. Load all claims and their candidates from session state

2. Calculate review statistics:
   - Total claims to review
   - Claims with strong candidates
   - Claims needing attention
   - Controversial claims

3. Display introduction:

"## Interactive Reference Review

I've found reference candidates for {total} claims in your manuscript.

For each claim, I'll show you:
- The claim text and location
- Suggested references with relevance explanations
- Quality metrics (citations, journal, type)

You can:
- Approve a suggested reference
- Request alternatives
- Skip (if no citation needed)
- Provide feedback for better searches

Let's begin!

[██████████████████████████░░░░] 80% - Starting interactive review
"
```

## Step 2: Present Claims for Review

```
For each claim (in order of priority):

1. Display claim card:

"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Claim {current} of {total}

**Location:** {section}, {line/paragraph reference}

**Claim:**
> {claim_text}

**Type:** {claim_type} | **Priority:** {priority}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

2. Display reference candidates:

"#### Suggested References

**#1** ⭐ RECOMMENDED

📄 **{title}**
👤 {authors} | 📅 {year} | 📰 *{journal}*

| Metric | Value |
|--------|-------|
| 📊 Citations | {count} ({percentile}) |
| 📚 Type | {review/primary} |
| 🏆 Journal | {reputation} |
| 🔓 Access | {open/closed} |

**Why recommended:**
> {relevance_explanation}

**Abstract excerpt:**
> {first_2_sentences_of_abstract}...

🔗 PMID: {pmid} | DOI: {doi}

---

**#2**

📄 **{title}**
...

---

**#3**
...
"
```

## Step 3: Collect User Decision

```
Display options:

"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Your decision:**

1. ✅ Approve #1 (recommended)
2. ✅ Approve #2
3. ✅ Approve #3
4. 🔄 Request alternatives
5. ⏭️ Skip (no citation needed)
6. 📝 Provide feedback for search

Commands: 'next', 'back', 'summary', 'save', 'done'

Enter choice:"

Process response:
- Numbers 1-N: Approve that reference
- 'alt' or 4: Request alternatives
- 'skip' or 5: Mark as skipped
- 'feedback' or 6: Prompt for feedback
- 'next': Go to next claim
- 'back': Return to previous claim
- 'summary': Show current summary
- 'save': Save and pause session
- 'done': Finalize if all reviewed
```

## Step 4: Handle Approve Action

```
When user approves a reference:

1. Update claim status:
{
  "claim_id": 7,
  "status": "approved",
  "selected_reference": {
    "pmid": "12345678",
    "citation_key": "smith2023metformin",
    "full_reference": "..."
  },
  "approved_at": timestamp
}

2. Display confirmation:
"✅ Reference approved for claim #{n}

Selected: Smith JA et al. (2023) Diabetes

[████████████████████████████░░] 87% - {approved}/{total} claims resolved"

3. Auto-advance to next claim
```

## Step 5: Handle Request Alternatives

```
When user requests alternatives:

1. Prompt for feedback:
"What's wrong with the current suggestions?

a) Not relevant enough
b) Too old - need more recent
c) Wrong article type (need review/primary)
d) Looking for specific aspect: [describe]
e) Just show me more options

Enter choice:"

2. Based on feedback, modify search:
   - a) Refine keywords, stricter relevance
   - b) Add date filter for last 3-5 years
   - c) Filter by article type
   - d) Add user's specific terms
   - e) Show next 5 candidates

3. Execute new search if needed

4. Display new candidates:
"### Alternative References

Based on your feedback, here are additional options:

**#4** 🆕 NEW
...

**#5** 🆕 NEW
..."

5. Return to decision collection
```

## Step 6: Handle Feedback

```
When user provides feedback:

1. Display prompt:
"Please describe what you're looking for:

Examples:
- 'Need a paper specifically about human trials'
- 'Looking for something from Nature or Science'
- 'Want a meta-analysis'
- 'Prefer papers by [author name]'

Your feedback:"

2. Parse and apply feedback:
   - Extract keywords
   - Identify filters (journal, author, type)
   - Build refined query

3. Run new search with feedback incorporated

4. Store feedback in session for learning:
{
  "user_feedback_history": [
    {
      "claim_id": 7,
      "original_query": "...",
      "feedback": "Need human trials",
      "refined_query": "... AND humans[MeSH]",
      "timestamp": "..."
    }
  ]
}

5. Present refined results
```

## Step 7: Handle Controversial Claims

```
For claims flagged as controversial:

Display:
"### ⚠️ Controversial Claim

This claim appears to have conflicting evidence in the literature.

**Claim:**
> {claim_text}

**Papers SUPPORTING this claim:**
#1: {title} - {brief_finding}
#2: {title} - {brief_finding}

**Papers with DIFFERENT conclusions:**
#3: {title} - {brief_finding}

**Options:**
a) Cite only supporting evidence
b) Cite both perspectives (recommended for balanced discussion)
c) Revise the claim to be more nuanced
d) Review papers in detail before deciding

Your choice:"

Handle based on response:
- a) Approve supporting reference only
- b) Approve multiple references, mark for special formatting
- c) Note for user to revise claim text
- d) Show full abstracts for review
```

## Step 8: Progress Tracking

```
After each decision, update and display progress:

"[████████████████████████████░░] {percentage}%

| Status | Count |
|--------|-------|
| ✅ Approved | {n} |
| ⏭️ Skipped | {n} |
| ⏳ Pending | {n} |
| 🔄 Needs alternatives | {n} |

{n} claims remaining to review."

Save session state after each decision for resume capability.
```

## Step 9: Review Summary

```
When user requests summary or all claims reviewed:

Display:
"## Review Summary

### Approved References ({count})

| # | Claim (truncated) | Reference |
|---|-------------------|-----------|
| 1 | "50% of patients..." | Smith 2023 |
| 2 | "Drug X inhibits..." | Jones 2024 |
...

### Skipped ({count})
- Claim #5: "DNA is genetic material" (common knowledge)
- Claim #12: User to add manually

### Needs Attention ({count})
- Claim #8: No suitable reference found
- Claim #15: Controversial - needs review

### Pending ({count})
- {list remaining claims}

---

**Options:**
a) Continue reviewing pending claims
b) Finalize and apply approved references
c) Save and continue later

Your choice:"
```

## Step 10: Finalization

```
When user chooses to finalize:

1. Verify all high-priority claims have references:
   - If not, warn user:
     "Warning: {n} high-priority claims still pending.
      Continue anyway? (yes/no)"

2. Confirm final selections:
"### Final Confirmation

You are about to add {count} references to your manuscript.

Citation format: {format}
Bibliography location: {location}

References to be added:
1. Smith JA et al. (2023) Diabetes...
2. Jones BC et al. (2024) Nature...
...

Proceed? (yes/no)"

3. If yes, proceed to Workflow 06
4. If no, return to review
```

## Completion

```
1. Update session state:
   - current_phase: "apply_changes"
   - review_completed_at: timestamp
   - approved_references: [final list]

2. Save session

3. Display:
"[██████████████████████████████] 95% - Review complete. Ready to apply changes."

4. Proceed to Workflow 06: Apply Changes
```

## Session Save (Pause)

```
When user chooses to save and continue later:

1. Ensure all state is persisted:
   - Current claim index
   - All decisions made
   - User feedback history

2. Display:
"Session saved!

To resume, run: /cite-them-all

Your progress:
- Claims reviewed: {reviewed}/{total}
- References approved: {approved}
- Session ID: {session_id}

See you next time!"

3. Exit workflow gracefully
```

## Error Handling

### Session Corruption
```
Display: "Warning: Session data appears corrupted."
Action:
- Attempt recovery from last known good state
- If unrecoverable, offer to restart review phase
- Preserve approved references if possible
```

### Reference No Longer Available
```
Display: "Reference #{pmid} no longer available in PubMed."
Action:
- Mark reference as unavailable
- Suggest alternatives
- Allow user to proceed with cached data or find replacement
```

### User Idle Timeout
```
After extended inactivity:
- Auto-save session state
- Display: "Session auto-saved due to inactivity."
- User can resume anytime with /cite-them-all
```
