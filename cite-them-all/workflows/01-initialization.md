# Workflow 01: Initialization

## Overview

This workflow handles file detection, backup creation, preference setup, and manuscript parsing.

## Step 1: Detect or Request Manuscript

```
1. Check if $ARGUMENTS contains a file path
   - If yes: Use provided path
   - If no: Continue to detection

2. Look for .md files in the current working directory:
   - If single .md file found: Propose it to user
   - If multiple .md files found: List them and ask user to choose
   - If no .md files found: Ask user to provide path

3. Confirm with user:
   "I found {filename}. Is this the manuscript you want to add references to?"
   - Wait for confirmation
   - If no: Ask for correct path

4. Validate file:
   - Check file exists and is readable
   - Check file extension is .md
   - If .docx: Suggest converting with pandoc:
     "This is a Word file. I recommend converting to Markdown first:
      pandoc input.docx -o input.md
      Then run cite-them-all on the .md file."
```

## Step 2: Create Backup

```
1. Generate timestamp: YYYY-MM-DD_HHMMSS format
2. Construct backup filename: {original_name}_backup_{timestamp}.md
3. Copy the file to the backup location (same directory)
4. Confirm: "Backup created: {backup_path}"
```

## Step 3: Ask Preferences

Ask the user three quick questions. These are asked each run (not persisted).

### Citation Format

```
"Which citation format?

1. APA (7th Edition) - Author-date, common in social sciences
2. Vancouver - Numbered, common in medical journals
3. Chicago (Author-Date) - Common in sciences and humanities
4. Harvard - Author-date with variations

Enter your choice (1-4):"
```

### Bibliography Location

```
"Where should the bibliography go?

1. End of the manuscript file
2. Separate .bib file (for LaTeX/Pandoc)

Enter your choice (1-2):"
```

### Search Sources

```
"Which databases should I search?

1. PubMed only (recommended for most manuscripts)
2. PubMed + bioRxiv/medRxiv preprints

Note: Preprint servers can only be browsed by date and category,
not searched by keyword. PubMed is the primary search tool.

Enter your choice (1-2):"
```

## Step 4: Parse Manuscript Content

```
1. Read the manuscript file

2. Identify document sections:
   - Look for Markdown headings (##, ###)
   - Map section structure

3. Detect existing citations:
   - Look for numbered patterns: [1], [2], [1-3]
   - Look for author-date patterns: (Author, Year)
   - Look for a References/Bibliography section

4. Report to user:
   "Manuscript loaded: {word_count} words, {section_count} sections"
   If existing citations found:
   "Detected {count} existing citations in {format} format."
```

## Step 5: Proceed

```
Proceed to Workflow 02: Claim Detection
```

## Error Handling

### File Not Found
```
"Error: File not found at {path}. Please check the path."
```

### File Permission Denied
```
"Error: Cannot read {path}. Check file permissions."
```

### Invalid File Format
```
"Error: {filename} is not a .md file. For .docx files, convert first:
pandoc {filename} -o {name}.md"
```

### Backup Creation Failed
```
"Warning: Could not create backup. Reason: {error}
Proceed without backup? (not recommended)"
```
