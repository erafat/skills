# Workflow 02: Claim Detection

## Overview

This workflow identifies statements in the manuscript that require citations, categorizes them, and identifies opportunities for reference sharing.

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

2. Note section types for context:
   - Methods sections: focus on methodological claims
   - Results sections: usually cite own data, fewer external refs needed
   - Introduction/Discussion: typically need most citations

3. Update progress:
   "[████████░░░░░░░░░░░░░░░░░░░░░░] 20% - Analyzing document structure"
```

## Step 2: Identify Claim Types

Scan the manuscript for statements requiring citations. Categorize each claim:

### 2a. Statistical Claims

```
Patterns to detect:
- Percentages: "X% of patients...", "approximately X%..."
- Numbers: "X million people...", "X-fold increase..."
- Comparisons: "significantly higher/lower...", "X times more likely..."
- Ranges: "between X and Y...", "ranging from X to Y..."

Examples:
- "Approximately 50% of patients with diabetes develop complications"
- "The mortality rate increased 3-fold"
- "Between 10-15% of the population is affected"

Flag for citation: HIGH PRIORITY
```

### 2b. Factual Assertions

```
Patterns to detect:
- Cause-effect: "X causes Y", "X leads to Y", "X results in Y"
- Mechanism: "X inhibits/activates Y", "X binds to Y"
- Properties: "X is characterized by Y", "X exhibits Y"
- Definitions: "X is defined as Y", "X refers to Y"

Examples:
- "Metformin inhibits hepatic gluconeogenesis"
- "CRISPR-Cas9 enables precise genome editing"
- "Inflammation leads to tissue damage"

Flag for citation: HIGH PRIORITY
```

### 2c. Background Statements

```
Patterns to detect:
- Disease prevalence: "X is a leading cause of...", "X affects millions..."
- Historical context: "Since the discovery of X...", "X was first described..."
- General facts: "It is well established that...", "X is known to..."

Examples:
- "Cancer is a leading cause of death worldwide"
- "Antibiotics have revolutionized medicine since the 1940s"
- "The human genome contains approximately 20,000 genes"

Flag for citation: MEDIUM PRIORITY (may be common knowledge)
```

### 2d. Methodological Claims

```
Patterns to detect:
- Gold standards: "X is the gold standard for...", "X is widely used for..."
- Validation: "X has been validated for...", "X is a reliable method..."
- Protocol references: "According to established protocols..."

Examples:
- "PCR is the gold standard for pathogen detection"
- "Western blotting is commonly used to detect proteins"
- "Flow cytometry enables single-cell analysis"

Flag for citation: MEDIUM PRIORITY
```

### 2e. Common Knowledge Assessment

```
Flag as potential "common knowledge" if:
- Statement is fundamental to the field
- Would be found in introductory textbooks
- Does not include specific numbers or recent findings
- Is generally accepted without controversy

Examples that MAY not need citations:
- "DNA is the genetic material of most organisms"
- "The heart pumps blood through the body"
- "Proteins are made of amino acids"

Action: Flag separately, ask user to confirm if citation needed
```

## Step 3: Extract and Catalog Claims

```
For each identified claim:

1. Extract claim text (the sentence or phrase)
2. Record location:
   - Section name
   - Paragraph number
   - Line number (for .md) or paragraph index (for .docx)
3. Assign claim type
4. Assess priority (HIGH/MEDIUM/LOW)
5. Generate search keywords

Store in session state:
{
  "claims": [
    {
      "id": 1,
      "text": "Approximately 50% of patients with diabetes develop neuropathy",
      "type": "statistical",
      "priority": "high",
      "location": {
        "section": "Introduction",
        "paragraph": 3,
        "line": 45
      },
      "search_keywords": ["diabetes", "neuropathy", "prevalence", "complications"],
      "status": "pending",
      "common_knowledge": false
    }
  ]
}

Update progress after each 10 claims:
"[██████████░░░░░░░░░░░░░░░░░░░░] 30% - Identified {count} claims..."
```

## Step 4: Identify Shared Reference Opportunities

```
1. Group claims by topic/keywords
2. Identify claims that could share the same reference:
   - Claims in the same paragraph about related topics
   - Sequential statements building on the same concept
   - Statistics from the same study

3. Mark claim groups:
{
  "claim_groups": [
    {
      "group_id": 1,
      "claim_ids": [3, 4, 5],
      "shared_topic": "diabetes complications",
      "suggested_action": "May share single comprehensive reference"
    }
  ]
}

4. Display to user:
"Note: Claims #3, #4, and #5 discuss related topics and may share a reference."
```

## Step 5: Flag Common Knowledge

```
1. Review claims flagged as potential common knowledge
2. Present to user for confirmation:

Display:
"The following statements may be common knowledge and might not require citations:

1. [Line 23] 'DNA contains the genetic information of organisms'
2. [Line 45] 'The immune system protects against pathogens'

Would you like to:
a) Skip these (no citation needed)
b) Add citations anyway
c) Review each individually

Enter your choice:"

3. Update claim status based on user input
```

## Step 6: Generate Summary Report

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

**Total claims identified:** {total}
**Claims grouped for shared references:** {grouped}

### High Priority Claims (require citations):
1. [Intro, Line 15] "50% of patients develop complications..."
2. [Intro, Line 23] "Drug X inhibits pathway Y..."
...

### Claims for Your Review:
- {n} statements flagged as potential common knowledge
- {n} claims may share references

Ready to proceed to existing reference check?
"
```

## Step 7: User Confirmation

```
1. Allow user to:
   - Add claims manually: "I also want to cite: [text]"
   - Remove claims: "Remove claim #5"
   - Change priority: "Claim #3 is common knowledge"
   - Proceed: "Continue" or "Looks good"

2. Process any modifications

3. Update session state:
   - current_phase: "existing_refs_check"
   - claims: [updated list]
   - last_updated: timestamp

4. Display:
   "[████████████░░░░░░░░░░░░░░░░░░] 35% - Claim detection complete. {total} claims identified."
```

## Completion

```
1. Save session state
2. Proceed to Workflow 03: Existing References Check
```

## Error Handling

### No Claims Found
```
Display: "No statements requiring citations were identified."
Action:
- Ask user if they want to add claims manually
- Or verify the manuscript contains the expected content
```

### Too Many Claims
```
If claims > 100:
Display: "Found {count} potential claims. This is a large number."
Action:
- Offer to focus on high-priority claims first
- Ask if user wants to limit scope (e.g., specific sections only)
```

### Parse Errors
```
Display: "Warning: Could not parse section starting at line {n}. Content may be malformed."
Action: Continue with parseable content, note skipped sections
```
