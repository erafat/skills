# Workflow 06: Apply Changes

## Overview

This workflow inserts approved citations into the manuscript, generates the bibliography, tracks all changes, and finalizes the session.

## Step 1: Pre-Application Verification

```
1. Verify backup exists:
   - Check backup file from initialization
   - If missing, create new backup now
   - Display: "✓ Backup verified: {backup_path}"

2. Load final approved references:
   - Count total references to insert
   - Verify all have complete metadata

3. Confirm with user:
"## Ready to Apply Changes

**Manuscript:** {filename}
**Backup:** {backup_path}

**Changes to apply:**
- Insert {n} new citations
- Add {n} entries to bibliography
- Format: {citation_format}
- Bibliography: {end_of_file / separate .bib}

Track changes will be enabled for your review.

Proceed? (yes/no)"
```

## Step 2: Determine Citation Numbers/Keys

```
Based on citation format:

### For Numbered Formats (Vancouver):

1. Find highest existing citation number
2. Assign new numbers sequentially:
   - If existing refs use [1]-[15], new refs start at [16]
   - Or renumber all if user prefers

3. Create number mapping:
{
  "citation_mapping": {
    "claim_7": "[16]",
    "claim_12": "[17]",
    "claim_15": "[16]"  // shares reference with claim_7
  }
}

### For Author-Date Formats (APA, Chicago, Harvard):

1. Generate citation keys:
   - (Smith, 2023)
   - (Smith & Jones, 2024)
   - (Smith et al., 2023)

2. Handle duplicates:
   - Same author, same year: (Smith, 2023a), (Smith, 2023b)

3. Create key mapping:
{
  "citation_mapping": {
    "claim_7": "(Smith, 2023)",
    "claim_12": "(Jones & Williams, 2024)",
    "claim_15": "(Smith, 2023)"  // reuses same reference
  }
}
```

## Step 3: Insert Inline Citations

```
For each claim with approved reference:

1. Locate claim in manuscript:
   - Use stored location (section, line/paragraph)
   - Verify claim text still matches

2. Determine insertion point:
   - End of sentence (after period)
   - Or per format conventions

3. Insert citation:

   Markdown (.md):
   Before: "Metformin reduces hepatic glucose production."
   After:  "Metformin reduces hepatic glucose production [16]."

   Or:     "Metformin reduces hepatic glucose production (Smith, 2023)."

   Word (.docx):
   - Insert citation with track changes enabled
   - Apply appropriate formatting

4. Track the change:
{
  "changes": [
    {
      "type": "citation_insert",
      "location": {"line": 89, "column": 45},
      "original": "production.",
      "modified": "production [16].",
      "reference": "Smith 2023"
    }
  ]
}

5. Update progress:
"[██████████████████████████████░] 96% - Inserting citation {n} of {total}"
```

## Step 4: Handle Shared References

```
When multiple claims share a reference:

1. Use same citation number/key
2. Track all insertion points:
{
  "reference_pmid_12345678": {
    "citation": "[16]",
    "inserted_at": [
      {"claim": 7, "location": "Line 89"},
      {"claim": 15, "location": "Line 134"}
    ]
  }
}

3. Note in change log:
"Reference [16] (Smith 2023) inserted at 2 locations"
```

## Step 5: Generate Bibliography

```
Based on bibliography_location setting:

### End of File (inline.md template):

1. Locate or create References section:
   - Find existing "References" or "Bibliography" heading
   - Or add new section at end of document

2. Format each reference per citation style:
   - Load template from templates/citation-formats/{format}.md
   - Apply formatting rules

3. Order references:
   - Numbered: In citation order [1], [2], [3]...
   - Author-date: Alphabetical by first author

4. Insert formatted bibliography:

```markdown
---

## References

1. Smith JA, Jones BC. Metformin inhibits hepatic gluconeogenesis through AMPK activation. Diabetes. 2023;72(5):678-689. doi:10.2337/db23-0123

2. Jones BC, Williams DE, Brown FG. Novel therapeutic approaches in type 2 diabetes. Nat Rev Drug Discov. 2024;23(2):112-128. doi:10.1038/nrd.2024.15

...
```

### Separate .bib File (bibtex.md template):

1. Generate .bib filename: {manuscript_name}.bib

2. Format each reference as BibTeX entry:
```bibtex
@article{smith2023metformin,
  author = {Smith, John A. and Jones, Brian C.},
  title = {Metformin inhibits hepatic gluconeogenesis through AMPK activation},
  journal = {Diabetes},
  year = {2023},
  volume = {72},
  number = {5},
  pages = {678--689},
  doi = {10.2337/db23-0123},
  pmid = {12345678}
}
```

3. Write .bib file to same directory as manuscript

4. Note in manuscript (if Markdown):
```markdown
<!-- Bibliography: paper.bib -->
```

5. Track file creation:
{
  "changes": [
    {
      "type": "file_created",
      "path": "{manuscript_dir}/paper.bib",
      "entries": 15
    }
  ]
}
```

## Step 6: Enable Track Changes (Word)

```
For .docx files:

1. Enable track changes mode before modifications
2. All insertions marked as additions
3. User can review in Word's Review pane

For .md files:

1. Generate diff summary
2. Optionally create .md.diff file showing changes
3. User can review with diff tool or in editor
```

## Step 7: Validate Changes

```
After all changes applied:

1. Parse modified document
2. Verify:
   - All citations inserted correctly
   - Citation numbers/keys match bibliography
   - No broken references
   - Document structure intact

3. Report any issues:
"⚠️ Validation warnings:
- Citation [17] may be misplaced (found mid-sentence)
- Reference entry for [20] appears truncated

Please review these locations manually."
```

## Step 8: Generate Change Summary

```
Display:

"## Changes Applied Successfully

[████████████████████████████████] 100% - Complete!

### Summary

**Citations inserted:** {n}
**Bibliography entries added:** {n}
**Shared references:** {n} references used for multiple claims

### Change Log

| Location | Change | Reference |
|----------|--------|-----------|
| Intro, L15 | Added [1] | Smith 2023 |
| Intro, L23 | Added [2] | Jones 2024 |
| Methods, L89 | Added [3] | Williams 2022 |
...

### Files Modified

1. **{manuscript_name}** - {n} citations added
2. **{manuscript_name}.bib** - Created with {n} entries (if applicable)

### Backup Location

Your original file is safely backed up at:
{backup_path}

To restore: Copy backup file over the modified manuscript.
"
```

## Step 9: Cleanup and Finalize

```
1. Mark session complete:
{
  "session_complete": true,
  "completed_at": timestamp,
  "final_stats": {
    "citations_added": n,
    "bibliography_entries": n,
    "claims_skipped": n,
    "duration_minutes": n
  }
}

2. Save final session state (for records)

3. Optionally clean up session file:
   - Keep session file for reference
   - Note: User chose no auto-cleanup

4. Display completion message:

"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## ✅ Citation Complete!

Your manuscript has been updated with {n} new references.

**Next steps:**
1. Review the changes in your document
2. Check track changes (Word) or diff (Markdown)
3. Verify citations appear correctly
4. Make any final adjustments

**Files:**
- Modified manuscript: {path}
- Backup: {backup_path}
{- Bibliography: {bib_path}}

Thank you for using cite-them-all!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

## Error Handling

### Write Permission Denied
```
Display: "Error: Cannot write to {path}. Permission denied."
Action:
- Check file permissions
- Offer to save to alternative location
- Do not lose prepared changes
```

### Document Structure Changed
```
Display: "Warning: Document structure has changed since analysis."
Action:
- Show differences detected
- Offer to re-analyze and re-locate claims
- Or proceed with best-effort placement
```

### Incomplete Bibliography Data
```
Display: "Warning: Reference #{n} has incomplete metadata."
Action:
- Show what's missing (DOI, pages, etc.)
- Insert with available data
- Note for user to complete manually
```

### Backup Creation Failed
```
Display: "Error: Could not create backup."
Action:
- STOP - do not proceed without backup
- Ask user to resolve (disk space, permissions)
- Only continue after backup confirmed
```

### Citation Collision
```
Display: "Warning: Citation number [X] already exists."
Action:
- Offer to renumber all citations
- Or start new citations after existing ones
- Get user confirmation before proceeding
```

## Rollback Procedure

```
If user needs to undo changes:

1. Locate backup file: {backup_path}
2. Instructions:

"## Rollback Instructions

To restore your original manuscript:

### Option 1: Manual
1. Delete or rename the modified file
2. Copy {backup_filename} to {original_filename}
3. Remove '_backup_{timestamp}' from the filename

### Option 2: Command Line
```bash
cp "{backup_path}" "{original_path}"
```

### Note
The .bib file (if created) can simply be deleted.
Your session data is preserved at:
~/.config/cite-them-all/sessions/{session_id}.json
"
```
