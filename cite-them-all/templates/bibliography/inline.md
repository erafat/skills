# Inline Bibliography Template

This template generates a bibliography/references section at the end of the manuscript file.

## Section Headers by Format

### APA
```markdown
## References
```

### Vancouver
```markdown
## References
```

### Chicago
```markdown
## Bibliography
```
or
```markdown
## References
```

### Harvard
```markdown
## Reference List
```

## Structure

```markdown
---

## References

1. [First reference entry]

2. [Second reference entry]

...

```

## Formatting Guidelines

```markdown
---

## References

Smith, J.A., Jones, B.C. and Williams, D.E. (2024) 'The effects of climate change on coral reef ecosystems', *Nature Climate Change*, 14(3), pp. 234-245. Available at: https://doi.org/10.1038/s41558-024-01234-5.

Jones, B.C. and Smith, J.A. (2023) 'Marine biodiversity under threat', *Science*, 382(6671), pp. 567-572. Available at: https://doi.org/10.1126/science.abc1234.

```

Notes for Markdown:
- Use `*text*` for italics (journal names)
- Separate entries with blank lines
- Use horizontal rule (`---`) to separate from main text
- DOIs as clickable links where possible

## Numbered vs Author-Date

### Numbered Format (Vancouver)

```markdown
## References

1. Smith JA, Jones BC, Williams DE. The effects of climate change on coral reef ecosystems. Nat Clim Chang. 2024;14(3):234-245. doi:10.1038/s41558-024-01234-5

2. Jones BC, Smith JA. Marine biodiversity under threat. Science. 2023;382(6671):567-572. doi:10.1126/science.abc1234

```

### Author-Date Format (APA, Chicago, Harvard)

```markdown
## References

Jones, B. C., & Smith, J. A. (2023). Marine biodiversity under threat. *Science*, *382*(6671), 567–572. https://doi.org/10.1126/science.abc1234

Smith, J. A., Jones, B. C., & Williams, D. E. (2024). The effects of climate change on coral reef ecosystems. *Nature Climate Change*, *14*(3), 234–245. https://doi.org/10.1038/s41558-024-01234-5

```

Note: Author-date formats are sorted alphabetically by first author.

## Insertion Point

Insert the bibliography:
1. After the main text content
2. Before appendices (if any)
3. Before supplementary materials (if any)

## Template Code

```
{separator}

## {section_title}

{references_formatted}
```

Variables:
- `{separator}`: Horizontal rule or page break indicator
- `{section_title}`: "References", "Bibliography", or "Reference List"
- `{references_formatted}`: All references formatted according to chosen style
