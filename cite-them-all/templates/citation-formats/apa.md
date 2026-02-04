# APA Citation Format (7th Edition)

## Inline Citation Format

### Single Author
```
(Author, Year)
```
Example: (Smith, 2024)

### Two Authors
```
(Author1 & Author2, Year)
```
Example: (Smith & Jones, 2024)

### Three or More Authors
```
(First Author et al., Year)
```
Example: (Smith et al., 2024)

### Multiple Citations
```
(Author1, Year; Author2, Year)
```
Example: (Smith, 2024; Jones, 2023)

### Direct Quote
```
(Author, Year, p. X)
```
Example: (Smith, 2024, p. 15)

### Author in Text
```
Author (Year) stated that...
```
Example: Smith (2024) demonstrated that...

## Reference List Format

### Journal Article
```
Author, A. A., Author, B. B., & Author, C. C. (Year). Title of article. Title of Periodical, volume(issue), page–page. https://doi.org/xxxxx
```

Example:
```
Smith, J. A., Jones, B. C., & Williams, D. E. (2024). The effects of climate change on coral reef ecosystems. Nature Climate Change, 14(3), 234–245. https://doi.org/10.1038/s41558-024-01234-5
```

### Journal Article (More than 20 Authors)
List first 19 authors, insert ellipsis (...), then final author.

### Preprint (bioRxiv/medRxiv)
```
Author, A. A., & Author, B. B. (Year). Title of preprint. bioRxiv. https://doi.org/10.1101/xxxxx
```

Example:
```
Smith, J. A., & Jones, B. C. (2024). Novel therapeutic targets in Alzheimer's disease. bioRxiv. https://doi.org/10.1101/2024.01.15.123456
```

### Review Article
Same as journal article format. Note: APA does not distinguish review articles in the citation format.

## Formatting Rules

1. **Hanging indent**: Second and subsequent lines indented 0.5 inches
2. **Double-spacing**: Between all lines
3. **Alphabetical order**: By first author's surname
4. **DOI format**: Use https://doi.org/xxxxx format (no "Retrieved from")
5. **Title case**: For journal names
6. **Sentence case**: For article titles (capitalize first word and proper nouns only)
7. **Italics**: Journal name and volume number

## Template Variables

When generating citations, use these placeholders:

- `{authors}` - Formatted author list
- `{year}` - Publication year
- `{title}` - Article title (sentence case)
- `{journal}` - Journal name (title case, italicized)
- `{volume}` - Volume number (italicized)
- `{issue}` - Issue number (in parentheses, not italicized)
- `{pages}` - Page range
- `{doi}` - DOI URL

### Inline Template
```
({authors_short}, {year})
```

### Reference Template
```
{authors}. ({year}). {title}. {journal}, {volume}({issue}), {pages}. {doi}
```
