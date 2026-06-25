# CV Update Packet Template

Use this structure for monthly or ad hoc review packets.

```markdown
---
type: cv_update_packet
created: YYYY-MM-DD
source_window_start: YYYY-MM-DD
source_window_end: YYYY-MM-DD
generated_by: skill:cv-update-review
config_profile: <profile name or config path>
---

# CV Update Packet - YYYY-MM-DD

Prepared for: **<name>**

## Source Window

- Window: **YYYY-MM-DD -> YYYY-MM-DD**
- Config: `<config path>`
- CV document checked: `<path>`
- Word edit performed: **No**

## Evidence Sources

### PubMed
- <query/source summary>

### Website/RSS
- <feed/source summary>

### Local Evidence
- <configured local paths searched>

### Manual Recall
- <user-supplied items or "not yet provided">

## Candidate Entries

Confidence key:
- **High** = date/title/role/venue verified by direct evidence
- **Medium** = supported, but section/wording/evidence needs confirmation
- **Low** = insufficient evidence; do not insert without explicit approval

### <Proposed CV Section>

1. **<Short candidate label>**
- Eligibility: `eligible | hold_for_confirmation | not_now | exclude`
- Proposed CV entry: *<draft wording matched to current CV style as much as possible>*
- Evidence: `<path or URL>`
- Confidence: **High | Medium | Low**
- Needs confirmation: <specific question or "none">

## Recommended Exclusions / Holds

- **<candidate>** - <why excluded or held>

## Approval Checklist

| Include? | Candidate | Section | Final wording approved? | Evidence sufficient? |
| --- | --- | --- | --- | --- |
| pending | <candidate> | <section> | pending | pending |

## Items Requiring Confirmation Before Word Edit

- <specific decisions needed>
```

Do not skip the approval checklist. The checklist is the handoff between the
discovery packet and the Word edit.
