# Chicago Citation Format (17th Edition)

Chicago offers two systems: Notes-Bibliography (humanities) and Author-Date (sciences). This template covers Author-Date, which is more common in scientific writing.

## Author-Date System

### Inline Citation Format

#### Single Author
```
(Author Year)
```
Example: (Smith 2024)

#### Two Authors
```
(Author and Author Year)
```
Example: (Smith and Jones 2024)

#### Three Authors
```
(Author, Author, and Author Year)
```
Example: (Smith, Jones, and Williams 2024)

#### Four or More Authors
```
(First Author et al. Year)
```
Example: (Smith et al. 2024)

#### Multiple Citations
```
(Author Year; Author Year)
```
Example: (Smith 2024; Jones 2023)

#### Page Numbers
```
(Author Year, page)
```
Example: (Smith 2024, 45)

#### Author in Text
```
Author (Year) argues that...
```
Example: Smith (2024) demonstrates that...

## Reference List Format

### Journal Article
```
Author, First Name, First Name Author, and First Name Author. Year. "Title of Article." Journal Name Volume (Issue): Pages. https://doi.org/xxxxx.
```

Example:
```
Smith, John A., Brian C. Jones, and Diana E. Williams. 2024. "The Effects of Climate Change on Coral Reef Ecosystems." Nature Climate Change 14 (3): 234–245. https://doi.org/10.1038/s41558-024-01234-5.
```

### Journal Article (More than 10 Authors)
List first 7 authors, then "et al."

### Preprint (bioRxiv/medRxiv)
```
Author, First Name, and First Name Author. Year. "Title of Preprint." bioRxiv. https://doi.org/xxxxx.
```

Example:
```
Smith, John A., and Brian C. Jones. 2024. "Novel Therapeutic Targets in Alzheimer's Disease." bioRxiv. https://doi.org/10.1101/2024.01.15.123456.
```

### Review Article
Same format as journal article. No special designation required.

## Formatting Rules

1. **Author names**: Full first names preferred (initials acceptable)
2. **First author**: Last name, First name format
3. **Subsequent authors**: First name Last name format
4. **Titles**: Headline-style capitalization for article titles
5. **Journal names**: Italicized, headline capitalization
6. **Hanging indent**: 0.5 inches for subsequent lines
7. **Alphabetical order**: By first author's surname
8. **Date placement**: After author names
9. **Quotation marks**: Around article titles
10. **Period placement**: After DOI URL

## Notes-Bibliography System (Alternative)

For humanities contexts, use footnotes/endnotes with a bibliography.

### Footnote Format
```
1. First Name Author, First Name Author, and First Name Author, "Title of Article," Journal Name Volume, no. Issue (Year): Page, https://doi.org/xxxxx.
```

### Bibliography Format
Same as Author-Date reference list format.

## Template Variables

- `{authors_full}` - Authors with full first names
- `{authors_short}` - Authors for inline citation
- `{year}` - Publication year
- `{title}` - Article title (headline case, in quotes)
- `{journal}` - Journal name (headline case, italicized)
- `{volume}` - Volume number
- `{issue}` - Issue number
- `{pages}` - Page range (use en-dash)
- `{doi}` - Full DOI URL

### Inline Template (Author-Date)
```
({authors_short} {year})
```

### Reference Template (Author-Date)
```
{authors_full}. {year}. "{title}." {journal} {volume} ({issue}): {pages}. {doi}.
```
