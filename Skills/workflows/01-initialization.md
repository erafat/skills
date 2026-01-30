# Workflow 01: Initialization

## Overview

This workflow handles session setup, file detection, backup creation, and preference configuration.

## Step 1: Check for Incomplete Sessions

```
1. Check if ~/.config/cite-them-all/sessions/ directory exists
2. If exists, scan for session files matching pattern: session_*.json
3. For each session file:
   a. Load session data
   b. Check if session_complete is false
   c. Check if manuscript file still exists
4. If incomplete session(s) found:
   - Display: "Found incomplete session from {timestamp} for {manuscript_name}"
   - Ask: "Would you like to resume this session? (yes/no)"
   - If yes: Load session state and jump to appropriate workflow phase
   - If no: Continue with new session
```

## Step 2: Detect or Request Manuscript

```
1. Check if $ARGUMENTS contains a file path
   - If yes: Use provided path
   - If no: Continue to detection

2. Attempt to detect open/current file:
   - Check current working context for .docx or .md files
   - If single file found: Propose it to user
   - If multiple files found: List them and ask user to choose
   - If no files found: Ask user to provide path

3. Confirm with user:
   - Display: "I found {filename}. Is this the manuscript you want to add references to?"
   - Wait for confirmation
   - If no: Ask for correct path

4. Validate file:
   - Check file exists
   - Check file extension (.docx or .md)
   - Check file is readable
   - If validation fails: Report error and ask for different file
```

## Step 3: Create Backup

```
1. Generate timestamp: YYYY-MM-DD_HHMMSS format
2. Construct backup filename: {original_name}_backup_{timestamp}.{extension}
3. Determine backup location: Same directory as original (per config)
4. Create backup copy
5. Confirm to user:
   - Display: "✓ Backup created: {backup_path}"

6. Store backup info in session state:
   {
     "original_path": "...",
     "backup_path": "...",
     "backup_timestamp": "..."
   }
```

## Step 4: Load or Initialize Configuration

```
1. Check if ~/.config/cite-them-all/ directory exists
   - If not: Create directory structure

2. Check if config.json exists
   - If yes: Load and validate against schema
   - If no: Create from defaults.json

3. Check if first_run_complete is false
   - If false: Proceed to first-run setup
   - If true: Skip to session initialization
```

## Step 5: First-Run Setup

Only execute if `first_run_complete` is false.

### 5a. Model Selection

```
Display:
"Which AI model are you using? This helps optimize the workflow.

1. Claude Opus
2. Claude Sonnet
3. Codex
4. GPT 5.2
5. Other

Enter your choice (1-5):"

Save selection to config.model
```

### 5b. Citation Format Selection

```
Display:
"Which citation format would you like to use?

1. APA (7th Edition) - Author-date style, common in social sciences
2. Vancouver - Numbered style, common in medical journals
3. Chicago (Author-Date) - Common in sciences and humanities
4. Harvard - Author-date style with variations
5. Custom - Define your own format

Enter your choice (1-5):"

If custom:
  - Ask for inline citation template
  - Ask for reference list template
  - Save to config.custom_citation_format

Save selection to config.citation_format
```

### 5c. Bibliography Location

```
Display:
"Where should the bibliography/reference list be placed?

1. End of the manuscript file
2. Separate .bib file (for LaTeX/Pandoc workflows)

Enter your choice (1-2):"

Save selection to config.bibliography_location
```

### 5d. Search Sources

```
Display:
"Which databases should I search for references?

PubMed is the default for peer-reviewed literature.
Preprint servers (bioRxiv/medRxiv) can provide cutting-edge research.

1. PubMed only (recommended for most manuscripts)
2. PubMed + bioRxiv (biology preprints)
3. PubMed + medRxiv (medical preprints)
4. PubMed + bioRxiv + medRxiv (all sources)

Enter your choice (1-4):"

Save selection to config.search_sources
```

### 5e. Save Configuration

```
1. Set config.first_run_complete = true
2. Write config to ~/.config/cite-them-all/config.json
3. Display: "✓ Preferences saved. You can change these anytime by editing ~/.config/cite-them-all/config.json"
```

## Step 6: Initialize Session State

```
1. Generate session ID: session_{manuscript_hash}_{timestamp}
2. Create session state object:

{
  "session_id": "...",
  "manuscript_path": "...",
  "manuscript_hash": "...",
  "backup_path": "...",
  "created_at": "...",
  "last_updated": "...",
  "current_phase": "initialization",
  "config_snapshot": { ... },
  "claims": [],
  "existing_references": [],
  "suggested_references": [],
  "approved_references": [],
  "user_feedback_history": [],
  "session_complete": false
}

3. Save session state to ~/.config/cite-them-all/sessions/{session_id}.json
4. Display progress:
   "[████░░░░░░░░░░░░░░░░░░░░░░░░░░] 10% - Initialization complete"
```

## Step 7: Parse Manuscript Content

```
1. Read manuscript file based on type:

   For .md files:
   - Read plain text content
   - Preserve section structure (headers)
   - Note line numbers for claims

   For .docx files:
   - Extract text content
   - Preserve paragraph structure
   - Note paragraph numbers for claims
   - Handle track changes if present

2. Store parsed content in session state:
   {
     "content": {
       "raw_text": "...",
       "sections": [
         {
           "title": "Introduction",
           "start_line": 10,
           "end_line": 45,
           "paragraphs": [...]
         }
       ],
       "word_count": 5000,
       "existing_citations_detected": true/false
     }
   }

3. Display:
   "✓ Manuscript loaded: {word_count} words, {section_count} sections"
```

## Completion

```
1. Update session state:
   - current_phase: "claim_detection"
   - last_updated: current timestamp

2. Save session state

3. Display:
   "[██████░░░░░░░░░░░░░░░░░░░░░░░░] 15% - Ready for claim detection"

4. Proceed to Workflow 02: Claim Detection
```

## Error Handling

### File Not Found
```
Display: "Error: File not found at {path}"
Action: Ask user for correct path or to check file location
```

### File Permission Denied
```
Display: "Error: Cannot read file at {path}. Permission denied."
Action: Ask user to check file permissions
```

### Invalid File Format
```
Display: "Error: {filename} is not a supported format. Please provide a .docx or .md file."
Action: Ask for different file
```

### Backup Creation Failed
```
Display: "Warning: Could not create backup at {path}. Reason: {error}"
Action: Ask user if they want to proceed without backup (not recommended)
```

### Config Corruption
```
Display: "Warning: Configuration file appears corrupted. Resetting to defaults."
Action: Backup old config, create fresh config from defaults
```
