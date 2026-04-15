# Workflow 02: Claim Detection

## Overview

Identify statements in the manuscript that require citations, categorize them, and find opportunities for reference sharing.

## Step 1: Analyze Document Structure

```
1. Identify document sections:
   - Abstract
   - Introduction
   - Methods
   - Results
   - Discussion
   - Conclusion
   - (Any custom sections)

2. Note section context:
   - Introduction/Discussion: typically need most citations
   - Methods: focus on methodological claims
   - Results: usually cite own data, fewer external refs needed
```

## Step 2: Identify Claim Types

Scan the manuscript for statements requiring citations.

### Statistical Claims

```
Patterns:
- Percentages: "X% of patients...", "approximately X%..."
- Numbers: "X million people...", "X-fold increase..."
- Comparisons: "significantly higher/lower...", "X times more likely..."
- Ranges: "between X and Y..."

Examples:
- "Approximately 50% of patients with diabetes develop complications"
- "The mortality rate increased 3-fold"

Priority: HIGH
```

### Factual Assertions

```
Patterns:
- Cause-effect: "X causes Y", "X leads to Y"
- Mechanism: "X inhibits/activates Y", "X binds to Y"
- Properties: "X is characterized by Y"

Examples:
- "Metformin inhibits hepatic gluconeogenesis"
- "CRISPR-Cas9 enables precise genome editing"

Priority: HIGH
```

### Background Statements

```
Patterns:
- Prevalence: "X is a leading cause of...", "X affects millions..."
- Historical: "Since the discovery of X...", "X was first described..."
- General: "It is well established that...", "X is known to..."

Examples:
- "Cancer is a leading cause of death worldwide"
- "The human genome contains approximately 20,000 genes"

Priority: MEDIUM (may be common knowledge)
```

### Methodological Claims

```
Patterns:
- "X is the gold standard for..."
- "X has been validated for..."
- "According to established protocols..."

Examples:
- "PCR is the gold standard for pathogen detection"
- "Flow cytometry enables single-cell analysis"

Priority: MEDIUM
```

### Common Knowledge Assessment

```
Flag as potential "common knowledge" if:
- Statement is fundamental to the field
- Would be found in introductory textbooks
- Does not include specific numbers or recent findings

Examples that may not need citations:
- "DNA is the genetic material of most organisms"
- "Proteins are made of amino acids"

Action: Flag separately, ask user to confirm
```

## Step 3: Extract and Catalog Claims

```
For each identified claim, record:

1. Claim text (the sentence or phrase)
2. Location: section name, paragraph number, line number
3. Claim type (statistical / factual / background / methodological)
4. Priority (HIGH / MEDIUM)
5. Search keywords (key scientific terms extracted from the claim)
6. Whether it already has a citation
```

## Step 4: Identify Shared Reference Opportunities

```
1. Group claims by topic/keywords
2. Identify claims that could share the same reference:
   - Claims in the same paragraph about related topics
   - Sequential statements building on the same concept
   - Statistics from the same study

3. Note groups for the user:
   "Claims #3, #4, and #5 discuss related topics and may share a reference."
```

## Step 5: Flag Common Knowledge

```
Present potential common knowledge to user:

"The following statements may not need citations:

1. [Line 23] 'DNA contains the genetic information of organisms'
2. [Line 45] 'The immune system protects against pathogens'

Options:
a) Skip these (no citation needed)
b) Add citations anyway
c) Review each individually"
```

## Step 6: Generate Summary

```
Display:

"## Claim Detection Summary

| Type | Count | Priority |
|------|-------|----------|
| Statistical claims | {n} | HIGH |
| Factual assertions | {n} | HIGH |
| Background statements | {n} | MEDIUM |
| Methodological claims | {n} | MEDIUM |
| Common knowledge | {n} | REVIEW |

Total claims identified: {total}
Claims grouped for shared references: {grouped}

Ready to proceed to existing reference check?"
```

## Step 7: User Confirmation

```
Allow user to:
- Add claims manually: "I also want to cite: [text]"
- Remove claims: "Remove claim #5"
- Change priority: "Claim #3 is common knowledge"
- Proceed: "Continue" or "Looks good"

Process modifications, then proceed to Workflow 03.
```

## Error Handling

### No Claims Found
```
"No statements requiring citations were identified."
Ask if user wants to add claims manually.
```

### Too Many Claims
```
If claims > 100:
"Found {count} potential claims. Would you like to:
a) Focus on high-priority claims first
b) Limit to specific sections
c) Process all"
```
