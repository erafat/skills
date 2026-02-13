# Interactive Review Report Template

This template defines the format for presenting reference suggestions to the user for review.

## Report Header

```markdown
# Citation Review Report

**Manuscript:** {manuscript_name}
**Claims identified:** {total_claims}
**References suggested:** {total_suggestions}

---
```

## Claim Entry Format

```markdown
### Claim {number} of {total}

**Location:** {section_name}, {paragraph/line_reference}

**Claim text:**
> {claim_text}

**Claim type:** {claim_type}
<!-- Types: Statistical | Factual assertion | Background statement | Methodological | Common knowledge -->

**Status:** {status}
<!-- Status: Pending review | Approved | Needs alternatives | Using existing reference -->

---

#### Suggested References

{reference_suggestions}

---

**Your decision:**
- [ ] Approve reference #{recommended}
- [ ] Request alternatives
- [ ] Skip (no citation needed)
- [ ] Use existing reference: ________

**Feedback (optional):**
> {user_feedback_area}

---
```

## Reference Suggestion Format

```markdown
**#{suggestion_number}** {recommendation_label}

**Title:** {title}
**Authors:** {authors}
**Journal:** {journal} ({year})

| Detail | Value |
|--------|-------|
| Type | {article_type} |
| Open Access | {oa_status} |

**Why recommended:**
> {relevance_explanation}

**Abstract excerpt:**
> {abstract_snippet}...

**PMID:** {pmid} | **DOI:** [{doi}]({doi_url})

---
```

## Recommendation Labels

Use plain text labels (no emoji):

```
[RECOMMENDED] - Best match for this claim
[REVIEW ARTICLE] - Comprehensive overview
[PRIMARY RESEARCH] - Original study
[RECENT] - Published within last 2 years
[OPEN ACCESS] - Freely available
```

## Controversial Claim Alert

```markdown
### Controversial Claim Detected

**Claim text:**
> {claim_text}

**Note:** This claim appears controversial. Found papers with conflicting conclusions:

**Supporting:**
- {paper_1_title} ({year}) - {brief_conclusion}

**Contradicting:**
- {paper_2_title} ({year}) - {brief_conclusion}

**Recommendation:** Consider citing both perspectives or revising the claim.

**Your decision:**
- [ ] Cite supporting evidence only
- [ ] Cite both perspectives
- [ ] Revise claim
- [ ] Skip citation

---
```

## Existing Reference Reuse

```markdown
### Existing Reference Available

**Claim text:**
> {claim_text}

**This claim may be supported by a reference already in your manuscript:**

**Existing reference #{ref_number}:**
> {existing_reference_text}

**Relevance assessment:**
> {why_it_supports_claim}

**Your decision:**
- [ ] Use existing reference
- [ ] Search for new references instead
- [ ] Use both existing and new reference

---
```

## Summary Section

```markdown
---

## Review Summary

| Status | Count |
|--------|-------|
| Approved | {approved_count} |
| Using existing | {existing_count} |
| Pending | {pending_count} |
| Skipped | {skipped_count} |
| Needs alternatives | {alternatives_count} |

### Approved References

| # | Claim | Reference | Type |
|---|-------|-----------|------|
| 1 | {claim_snippet} | {ref_short} | {type} |
| 2 | {claim_snippet} | {ref_short} | {type} |
...

---

## Next Steps

{next_steps_message}

- [ ] **Confirm all selections** - Proceed to insert citations
- [ ] **Review flagged items** - {flagged_count} items need attention
- [ ] **Request more alternatives** - Search again for specific claims

---
```

## Interactive Commands

Users can respond with:

```
approve 1        - Approve suggestion #1
reject 2         - Reject suggestion #2, request alternatives
skip             - Skip this claim (no citation needed)
use existing 3   - Use existing reference #3
feedback: [text] - Provide specific feedback for search refinement
next             - Move to next claim
back             - Return to previous claim
summary          - Show current summary
done             - Finalize all approved and proceed
```
