# Workflow 06: Apply Changes

## Overview

Insert approved citations into the manuscript, generate the bibliography, and present a summary.

## Step 1: Pre-Application Verification

```
1. Verify backup exists:
   - Check backup file from initialization
   - If missing, create new backup now
   - Report: "Backup verified: {backup_path}"

2. Confirm with user:
   "## Ready to Apply Changes

   Manuscript: {filename}
   Backup: {backup_path}

   Changes:
   - Insert {n} new citations
   - Add {n} entries to bibliography
   - Format: {citation_format}
   - Bibliography: {end_of_file / separate .bib}

   Proceed? (yes/no)"
```

## Step 2: Determine Citation Numbers/Keys

```
Based on citation format:

### For Numbered Formats (Vancouver):

1. Find highest existing citation number
2. Assign new numbers sequentially:
   - Existing refs use [1]-[15] -> new refs start at [16]
3. Shared references get the same number

### For Author-Date Formats (APA, Chicago, Harvard):

1. Generate citation keys:
   - (Smith, 2023)
   - (Smith & Jones, 2024)
   - (Smith et al., 2023)

2. Handle duplicates:
   - Same author, same year: (Smith, 2023a), (Smith, 2023b)
```

## Step 3: Insert Inline Citations

```
For each claim with an approved reference:

1. Locate the claim in the manuscript using stored line/paragraph info
2. Verify claim text still matches

3. Insert citation at end of sentence:

   Before: "Metformin reduces hepatic glucose production."
   After:  "Metformin reduces hepatic glucose production [16]."
   Or:     "Metformin reduces hepatic glucose production (Smith, 2023)."

4. Track the change:
   - Location, original text, modified text, reference
```

## Step 4: Handle Shared References

```
When multiple claims share a reference:
- Use the same citation number/key
- Note: "Reference [16] (Smith 2023) inserted at 2 locations"
```

## Step 5: Generate Bibliography

```
Based on bibliography_location setting:

### End of File:

1. Locate or create "## References" section
2. Format each reference using the template from templates/citation-formats/{format}.md
3. Order:
   - Numbered: in citation order [1], [2], [3]
   - Author-date: alphabetical by first author
4. Insert formatted bibliography

Example (Vancouver):

---

## References

1. Smith JA, Jones BC. Metformin inhibits hepatic gluconeogenesis
   through AMPK activation. Diabetes. 2023;72(5):678-689.
   doi:10.2337/db23-0123

2. Jones BC, Williams DE. Novel therapeutic approaches in type 2
   diabetes. Nat Rev Drug Discov. 2024;23(2):112-128.
   doi:10.1038/nrd.2024.15


### Separate .bib File:

1. Generate {manuscript_name}.bib
2. Format each reference as BibTeX (see templates/bibliography/bibtex.md)
3. Write .bib file to same directory
4. Add comment to manuscript: <!-- Bibliography: {filename}.bib -->
```

## Step 6: Validate Changes

```
After applying:

1. Re-read the modified document
2. Verify:
   - All citations inserted correctly
   - Citation numbers/keys match bibliography entries
   - No broken references
   - Document structure intact

3. Report any issues:
   "Warning: Citation [17] may be misplaced. Please check line {n}."
```

## Step 7: Change Summary

```
"## Changes Applied

Citations inserted: {n}
Bibliography entries added: {n}
Shared references: {n} references used for multiple claims

### Change Log

| Location | Change | Reference |
|----------|--------|-----------|
| Intro, L15 | Added [1] | Smith 2023 |
| Intro, L23 | Added [2] | Jones 2024 |
| Methods, L89 | Added [3] | Williams 2022 |

### Files Modified

1. {manuscript_name} - {n} citations added
{2. {manuscript_name}.bib - Created with {n} entries}

### Backup

Original file backed up at: {backup_path}
To restore: cp '{backup_path}' '{original_path}'"
```

## Step 8: Completion

```
"## Done

Your manuscript has been updated with {n} new references.

Next steps:
1. Review the changes in your editor
2. Verify citations appear correctly
3. Make any final adjustments

Files:
- Modified manuscript: {path}
- Backup: {backup_path}
{- Bibliography: {bib_path}}"
```

## Error Handling

### Write Permission Denied
```
"Cannot write to {path}."
Offer to save to alternative location.
```

### Document Structure Changed
```
"Document structure changed since analysis."
Offer to re-locate claims or proceed with best-effort placement.
```

### Incomplete Bibliography Data
```
"Reference #{n} has incomplete metadata (missing {fields})."
Insert with available data, note for user to complete manually.
```

### Backup Missing
```
STOP. Do not proceed without a backup.
"Could not verify backup. Creating new backup before proceeding."
```

### Citation Collision
```
"Citation number [X] already exists."
Offer to renumber or start after existing citations.
```

## Rollback

```
To restore the original manuscript:

cp "{backup_path}" "{original_path}"

Any .bib file created can simply be deleted.
```
