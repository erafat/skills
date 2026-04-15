# Vancouver Citation Format

Also known as: ICMJE (International Committee of Medical Journal Editors) style, NLM (National Library of Medicine) style.

## Inline Citation Format

### Numbered Citations
Citations are numbered in order of appearance in the text.

```
[1]
```

### Multiple Citations
```
[1,2]
[1-3]
[1,3,5]
[1-3,7]
```

### Placement
- Place citation numbers in square brackets
- Position after punctuation (period, comma)
- Superscript is acceptable in some journals: ¹

Examples:
```
Studies have shown significant results [1].
Several authors have reported similar findings [2-5].
This has been confirmed by multiple groups [1,7,12].
```

## Reference List Format

### Journal Article (1-6 Authors)
```
Author AA, Author BB, Author CC. Title of article. Journal Name Abbreviated. Year;Volume(Issue):Pages. doi:xxxxx
```

Example:
```
Smith JA, Jones BC, Williams DE. The effects of climate change on coral reef ecosystems. Nat Clim Chang. 2024;14(3):234-245. doi:10.1038/s41558-024-01234-5
```

### Journal Article (More than 6 Authors)
List first 6 authors, then "et al."

```
Smith JA, Jones BC, Williams DE, Brown FG, Davis HI, Miller JK, et al. Title of article. Journal Name. Year;Volume(Issue):Pages.
```

### Preprint (bioRxiv/medRxiv)
```
Author AA, Author BB. Title of preprint. bioRxiv [Preprint]. Year [cited Date]. Available from: URL. doi:xxxxx
```

Example:
```
Smith JA, Jones BC. Novel therapeutic targets in Alzheimer's disease. bioRxiv [Preprint]. 2024 [cited 2024 Mar 15]. Available from: https://doi.org/10.1101/2024.01.15.123456
```

### Review Article
Same as journal article. Add "[Review]" after title if clarification needed.

## Formatting Rules

1. **Author names**: Surname followed by initials (no periods, no spaces)
2. **Journal abbreviations**: Use NLM/MEDLINE abbreviations
3. **No italics**: Vancouver style typically does not use italics
4. **Numbered list**: References numbered in order of first citation
5. **No hanging indent**: Standard paragraph format
6. **Periods**: Use periods to separate major elements
7. **Semicolons**: Separate year from volume

## Common Journal Abbreviations

| Full Name | Abbreviation |
|-----------|--------------|
| Nature | Nature |
| Science | Science |
| Cell | Cell |
| New England Journal of Medicine | N Engl J Med |
| The Lancet | Lancet |
| Journal of the American Medical Association | JAMA |
| British Medical Journal | BMJ |
| Proceedings of the National Academy of Sciences | Proc Natl Acad Sci U S A |
| PLoS ONE | PLoS One |
| Nature Medicine | Nat Med |

## Template Variables

- `{number}` - Citation number
- `{authors}` - Formatted author list (Surname Initials format)
- `{title}` - Article title
- `{journal_abbrev}` - Abbreviated journal name
- `{year}` - Publication year
- `{volume}` - Volume number
- `{issue}` - Issue number
- `{pages}` - Page range (use hyphen, not en-dash)
- `{doi}` - DOI (doi:xxxxx format)

### Inline Template
```
[{number}]
```

### Reference Template
```
{number}. {authors}. {title}. {journal_abbrev}. {year};{volume}({issue}):{pages}. doi:{doi}
```
