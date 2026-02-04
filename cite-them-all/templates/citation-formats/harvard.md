# Harvard Citation Format

Note: Harvard referencing has many institutional variations. This template follows the most common conventions.

## Inline Citation Format

### Single Author
```
(Author, Year)
```
Example: (Smith, 2024)

### Two Authors
```
(Author and Author, Year)
```
Example: (Smith and Jones, 2024)

### Three or More Authors
```
(First Author et al., Year)
```
Example: (Smith et al., 2024)

### Multiple Citations
Chronological order:
```
(Author, Year; Author, Year)
```
Example: (Jones, 2022; Smith, 2024)

### Multiple Works, Same Author, Same Year
```
(Author, Yeara, Yearb)
```
Example: (Smith, 2024a, 2024b)

### Page Numbers
```
(Author, Year, p. X)
(Author, Year, pp. X-Y)
```
Example: (Smith, 2024, p. 45)

### Author in Text
```
Author (Year) states that...
According to Author (Year)...
```
Example: Smith (2024) argues that...

### Secondary Citation (Cite with Caution)
```
(Original Author, Year, cited in Author, Year)
```

## Reference List Format

### Journal Article
```
Author, A.A., Author, B.B. and Author, C.C. (Year) 'Title of article', Journal Name, Volume(Issue), pp. Pages. Available at: https://doi.org/xxxxx.
```

Example:
```
Smith, J.A., Jones, B.C. and Williams, D.E. (2024) 'The effects of climate change on coral reef ecosystems', Nature Climate Change, 14(3), pp. 234-245. Available at: https://doi.org/10.1038/s41558-024-01234-5.
```

### Journal Article (More than 3 Authors)
Some Harvard variants:
- List all authors
- List first 3, then "et al."

Follow your institution's guidelines. Default: List all for reference list.

### Preprint (bioRxiv/medRxiv)
```
Author, A.A. and Author, B.B. (Year) 'Title of preprint', bioRxiv [Preprint]. Available at: https://doi.org/xxxxx (Accessed: Day Month Year).
```

Example:
```
Smith, J.A. and Jones, B.C. (2024) 'Novel therapeutic targets in Alzheimer's disease', bioRxiv [Preprint]. Available at: https://doi.org/10.1101/2024.01.15.123456 (Accessed: 15 March 2024).
```

### Review Article
Same format as journal article. Optionally note [Review] after title.

## Formatting Rules

1. **Author names**: Surname, Initials format
2. **Ampersand vs "and"**: Use "and" (not &) between authors
3. **Article titles**: Single quotation marks, sentence case
4. **Journal names**: Italicized, title case
5. **Hanging indent**: Second and subsequent lines indented
6. **Alphabetical order**: By first author's surname
7. **Year placement**: In parentheses after authors
8. **Page numbers**: Use "pp." prefix
9. **Available at**: Include for electronic sources
10. **Full stops**: End each reference with a period

## Variations by Institution

Harvard style varies significantly. Key differences:
- Quotation marks: Single (UK) vs Double (US)
- "and" vs "&" between authors
- Date format in "Accessed" note
- Capitalization of "Available at"

Always check your institution's specific guidelines.

## Template Variables

- `{authors}` - Formatted author list (Surname, Initials)
- `{authors_inline}` - Authors for inline citation
- `{year}` - Publication year
- `{year_suffix}` - Suffix for same-author-same-year (a, b, c)
- `{title}` - Article title (sentence case)
- `{journal}` - Journal name (title case, italicized)
- `{volume}` - Volume number
- `{issue}` - Issue number
- `{pages}` - Page range
- `{doi}` - Full DOI URL
- `{accessed_date}` - Access date for online sources

### Inline Template
```
({authors_inline}, {year}{year_suffix})
```

### Reference Template
```
{authors} ({year}{year_suffix}) '{title}', {journal}, {volume}({issue}), pp. {pages}. Available at: {doi}.
```
