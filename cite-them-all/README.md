# cite-them-all

An academic reference agent for Claude Code that identifies claims needing citations in Markdown manuscripts, searches PubMed/bioRxiv/medRxiv via MCP tools, and adds properly formatted references.

## Features

- **Claim Detection**: Identifies statements requiring citations (statistical claims, factual assertions, methodological claims, background statements)
- **PubMed Search**: Keyword search via `search_articles` with full PubMed query syntax
- **Preprint Browsing**: Optional bioRxiv/medRxiv browsing by date and category (no keyword search available)
- **Existing Reference Verification**: Verifies current references via `lookup_article_by_citation` and `get_article_metadata`
- **Reference Reuse**: Identifies opportunities to reuse existing references for new claims
- **Interactive Review**: Presents candidates with relevance explanations for approval
- **Multiple Citation Formats**: APA, Vancouver, Chicago, Harvard

## Usage

```bash
# Specify manuscript path
/cite-them-all path/to/manuscript.md

# Auto-detect manuscript in current context
/cite-them-all
```

Supported format: Markdown (`.md`). For Word documents, convert with `pandoc input.docx -o input.md` first.

## Workflow

### 1. Initialization
- Detects or requests manuscript file
- Creates timestamped backup
- Asks citation format, bibliography location, and search sources

### 2. Claim Detection
- Scans manuscript for statements requiring citations
- Categorizes claims (statistical, factual, methodological, background)
- Flags potential common knowledge
- Identifies claims that could share references

### 3. Existing Reference Check
- Parses current bibliography
- Resolves references using `lookup_article_by_citation`, `convert_article_ids`, `get_article_metadata`
- Verifies references support their claims (full text via `get_full_text_article` when available)
- Identifies reuse opportunities for new claims

### 4. Reference Search
- Searches PubMed via `search_articles` with field-tagged queries
- Uses `find_related_articles` as fallback when keyword search yields few results
- Optionally browses bioRxiv/medRxiv by date+category via `search_preprints`
- Ranks by abstract relevance, recency, and article type
- Flags controversial claims with conflicting evidence

### 5. Interactive Review
- Presents claims with suggested references
- Shows relevance explanations, article type, open access status
- Approve, reject, request alternatives, or skip each claim

### 6. Apply Changes
- Inserts citations in chosen format
- Generates bibliography (end of file or .bib)
- Provides rollback instructions via backup file

## Citation Formats

### APA (7th Edition)
```
(Smith & Jones, 2024)
Smith, J. A., & Jones, B. C. (2024). Title of article. Journal Name, 14(3), 234-245. https://doi.org/xxxxx
```

### Vancouver
```
[1]
1. Smith JA, Jones BC. Title of article. J Name. 2024;14(3):234-245. doi:xxxxx
```

### Chicago (Author-Date)
```
(Smith and Jones 2024)
Smith, John A., and Brian C. Jones. 2024. "Title of Article." Journal Name 14 (3): 234-245.
```

### Harvard
```
(Smith and Jones, 2024)
Smith, J.A. and Jones, B.C. (2024) 'Title of article', Journal Name, 14(3), pp. 234-245.
```

## MCP Tools Used

| Tool | Purpose |
|------|---------|
| `search_articles` | PubMed keyword search with field tags |
| `get_article_metadata` | Full metadata for articles by PMID |
| `lookup_article_by_citation` | Match partial citation details to PMID |
| `find_related_articles` | Find similar articles by PMID |
| `convert_article_ids` | Convert between PMID, PMCID, DOI |
| `get_full_text_article` | Retrieve full text from PMC |
| `get_copyright_status` | Check open access / licensing |
| `search_preprints` | Browse bioRxiv/medRxiv by date+category |
| `get_preprint` | Full metadata for preprint by DOI |
| `search_published_preprints` | Find preprints published in journals |

## Limitations

- **Biomedical scope only**: PubMed indexes life sciences and medicine; for physics, CS, math, use other databases
- **No bioRxiv keyword search**: Preprint browsing is limited to date range + subject category
- **No citation counts or impact factors**: MCP tools do not return these metrics
- **Markdown only**: `.docx` files must be converted via pandoc first
- **No full text for most articles**: Only ~6M articles in PMC have full text available
- **Abstracts for ranking**: Reference relevance is judged from abstracts, not full papers

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

## Tips for Best Results

1. **Be specific in claims**: Vague statements yield vague references
2. **Use standard terminology**: Medical/scientific terms improve search accuracy
3. **Review common knowledge flags**: Some obvious statements may not need citations
4. **Provide feedback**: If suggestions aren't relevant, describe what you need
5. **Check controversial claims**: Consider citing multiple perspectives
