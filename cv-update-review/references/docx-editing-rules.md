# DOCX Editing Rules

Follow these rules after the user approves exact CV entries.

## Safety

- Never edit the original CV.
- Create a dated `.docx` copy first.
- Keep the original path and copy path visible in the final summary.
- If an overwrite would occur, create `_v2`, `_v3`, etc. unless the user
  explicitly authorizes overwrite.

## Style Preservation

Before editing, extract examples near each target section. Match the local
conventions for:

- bullets and indentation
- paragraph style
- title quotation
- author punctuation
- journal abbreviation and DOI style
- date and location order
- table/list structure

Do not reformat unrelated sections.

## Preferred Edit Path

Use dedicated document-editing/rendering tools when available. If editing OOXML
directly, keep the change minimal:

- modify only `word/document.xml`
- insert paragraphs by cloning a nearby paragraph from the same section
- replace text inside the clone rather than constructing styles from scratch
- do not change numbering, styles, relationships, headers, footers, or document
  settings unless required

## Verification

After editing:

- extract text from the dated copy
- confirm every approved entry appears
- confirm no unapproved entry appears
- confirm the original CV file was not modified
- render or visually inspect the document when possible

If visual rendering is unavailable, report that only text verification was done.
