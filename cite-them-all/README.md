# cite-them-all

An AI-powered academic reference agent that automatically identifies claims in your manuscript, searches PubMed/bioRxiv/medRxiv for supporting references, and adds properly formatted citations.

## Features

- **Claim Detection**: Automatically identifies statements requiring citations (statistical claims, factual assertions, methodological claims, background statements)
- **Smart Search**: Searches PubMed and optionally bioRxiv/medRxiv for relevant references
- **Existing Reference Verification**: Optionally verifies that your current references actually support their claims
- **Reference Reuse**: Identifies opportunities to reuse existing references for new claims
- **Interactive Review**: Presents candidates with relevance explanations for your approval
- **Multiple Citation Formats**: Supports APA, Vancouver, Chicago, Harvard, and custom formats
- **Session Resume**: Save progress and continue later - never lose your work
- **Track Changes**: All modifications are tracked for easy review
- **Cross-Model Compatible**: Works with Claude, Codex, GPT 5.2, and other AI assistants

## Installation

The skill is installed at `~/.claude/skills/cite-them-all/`

Configuration is stored at `~/.config/cite-them-all/config.json`

## Usage

### Basic Usage

```bash
# Auto-detect manuscript in current context
/cite-them-all

# Specify manuscript path
/cite-them-all path/to/manuscript.docx
/cite-them-all path/to/manuscript.md

# Resume previous session
/cite-them-all --resume
```

### Supported File Formats

- Microsoft Word (`.docx`)
- Markdown (`.md`)

## Workflow

### 1. Initialization
- Detects or requests manuscript file
- Creates timestamped backup
- Loads/creates user preferences
- First-run setup for citation format, bibliography location, etc.

### 2. Claim Detection
- Scans manuscript for statements requiring citations
- Categorizes claims (statistical, factual, methodological, background)
- Flags potential common knowledge
- Identifies claims that could share references

### 3. Existing Reference Check
- Detects existing citation format
- Parses current bibliography
- Optionally verifies references support their claims
- Identifies reuse opportunities for new claims

### 4. Reference Search
- Searches PubMed (default) and optionally bioRxiv/medRxiv
- Retrieves 5 candidates per claim (10 in in-depth mode)
- Ranks by relevance, citation count, journal reputation
- Flags controversial claims with conflicting evidence

### 5. Interactive Review
- Presents claims with suggested references
- Shows relevance explanations and quality metrics
- Approve, reject, request alternatives, or skip each claim
- Iterates until all references approved

### 6. Apply Changes
- Inserts citations in chosen format
- Generates bibliography (end of file or .bib)
- Tracks all changes
- Provides rollback instructions

## Configuration

Configuration file: `~/.config/cite-them-all/config.json`

```json
{
  "model": "opus",
  "citation_format": "apa",
  "bibliography_location": "end_of_file",
  "search_sources": {
    "pubmed": true,
    "biorxiv": false,
    "medrxiv": false
  },
  "search_depth": "standard",
  "reference_preferences": {
    "prefer_recent": true,
    "recent_years": 10,
    "prefer_reviews": false,
    "min_citation_count": 0,
    "preferred_journals": [],
    "excluded_journals": []
  },
  "backup": {
    "location": "same_directory",
    "auto_cleanup": false
  },
  "progress_display": "visual"
}
```

### Configuration Options

| Option | Values | Description |
|--------|--------|-------------|
| `model` | opus, sonnet, codex, gpt-5.2 | AI model being used |
| `citation_format` | apa, vancouver, chicago, harvard, custom | Citation style |
| `bibliography_location` | end_of_file, separate_bib | Where to place references |
| `search_depth` | standard, in-depth | 5 or 10 candidates per claim |
| `progress_display` | minimal, detailed, visual | Progress update verbosity |

## Citation Formats

### APA (7th Edition)
```
(Smith & Jones, 2024)
Smith, J. A., & Jones, B. C. (2024). Title of article. Journal Name, 14(3), 234–245. https://doi.org/xxxxx
```

### Vancouver
```
[1]
1. Smith JA, Jones BC. Title of article. J Name. 2024;14(3):234-245. doi:xxxxx
```

### Chicago (Author-Date)
```
(Smith and Jones 2024)
Smith, John A., and Brian C. Jones. 2024. "Title of Article." Journal Name 14 (3): 234–245.
```

### Harvard
```
(Smith and Jones, 2024)
Smith, J.A. and Jones, B.C. (2024) 'Title of article', Journal Name, 14(3), pp. 234-245.
```

## Session Management

Sessions are automatically saved to `~/.config/cite-them-all/sessions/`

Session state includes:
- Manuscript path and content hash
- Current workflow phase
- All identified claims
- Search results and rankings
- User decisions and feedback
- Approved references

To resume: Simply run `/cite-them-all` and you'll be prompted to continue your previous session.

## Backup and Safety

- **Automatic backups**: Created before any modifications
- **Backup naming**: `{filename}_backup_{YYYY-MM-DD_HHMMSS}.{ext}`
- **Backup location**: Same directory as manuscript
- **No auto-cleanup**: Backups are preserved indefinitely

### Rollback

To restore your original manuscript:
```bash
cp "manuscript_backup_2026-01-29_143022.docx" "manuscript.docx"
```

## Quality Indicators

For each suggested reference, the skill provides:

| Indicator | Description |
|-----------|-------------|
| 📊 Citations | Citation count and percentile in field |
| 📚 Type | Review article vs primary research |
| 🏆 Journal | Journal reputation indicator |
| 🔓 Access | Open access availability |
| ⭐ Recommended | Best match based on combined score |

## Error Handling

The skill handles common errors gracefully:

- **PubMed unreachable**: Retry with backoff, offer preprint-only search
- **Rate limiting**: Automatic exponential backoff
- **No results found**: Suggests query refinement, allows manual input
- **Parse errors**: Reports issues, continues with parseable content
- **Session corruption**: Attempts recovery, offers fresh start

## Directory Structure

```
~/.claude/skills/cite-them-all/
├── SKILL.md                      # Main skill instructions
├── README.md                     # This file
├── config/
│   ├── schema.json              # Configuration validation
│   └── defaults.json            # Default settings
├── templates/
│   ├── review-report.md         # Interactive report format
│   ├── citation-formats/
│   │   ├── apa.md
│   │   ├── vancouver.md
│   │   ├── chicago.md
│   │   └── harvard.md
│   └── bibliography/
│       ├── inline.md            # End-of-file format
│       └── bibtex.md            # .bib file format
├── workflows/
│   ├── 01-initialization.md
│   ├── 02-claim-detection.md
│   ├── 03-existing-refs-check.md
│   ├── 04-reference-search.md
│   ├── 05-interactive-review.md
│   └── 06-apply-changes.md
└── examples/
    ├── sample-manuscript.md
    ├── sample-report.md
    └── sample-output.md
```

## Limitations

- Only searches biomedical/life sciences literature (PubMed scope)
- Requires internet connection for reference searches
- Cannot access paywalled full-text articles (uses abstracts)
- Citation counts may not be available for very recent papers

## Tips for Best Results

1. **Be specific in claims**: Vague statements yield vague references
2. **Use standard terminology**: Medical/scientific terms improve search accuracy
3. **Review common knowledge flags**: Some obvious statements may not need citations
4. **Provide feedback**: If suggestions aren't relevant, describe what you need
5. **Check controversial claims**: Consider citing multiple perspectives

## Support

For issues or feature requests, please refer to the skill documentation or contact the skill maintainer.

## License

This skill is provided as-is for academic and research purposes.
