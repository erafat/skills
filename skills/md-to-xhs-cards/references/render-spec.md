# Render Spec

## Output Defaults

- Card size: `1080x1440` (3:4)
- Background: `#f7f6f2` (soft warm neutral)
- Text: Songti-style serif body by default, with readable leading
- Output names: `01-card.png`, `02-card.png`, ...
- Manifest: `manifest.json`
- Cover mode: `auto` (uses first image + inferred title/subtitle when available)

## Markdown Support

- Headings: `#` to `######` (larger typography for higher levels)
- Paragraphs: plain text blocks
- Lists: ordered and unordered
- Quotes: `>` blocks with left accent bar
- Code: fenced blocks with neutral container
- Horizontal rule: `---`, `***`, `___`, and wide dash lines (`———`)
- Images: Markdown `![alt](path)` and Obsidian embeds `![[path]]` / `![[path|caption]]`
- Inline markdown (`**bold**`, `_italic_`, `` `code` ``, links): normalized to plain text
- Optional cover metadata: `--title`, `--subtitle`, `--author`, `--cover-image`
- Optional typography tuning: `--line-height-scale` (default `1.80`)
- Signature options: `--signature-text` and `--cover-author` (cover author is off by default)

## Image Rules

- Resolve relative image paths from the markdown file directory
- If unresolved, try vault-root-relative path and then basename lookup within the vault
- Keep source order exactly as in markdown
- Scale to fit card width and a max card-height ratio
- Draw a subtle border
- Render `alt` text as caption when present
- If image is missing or remote URL is blocked, emit a placeholder text block and record in `manifest.json.missing_images`

## Recommended Commands

Basic:

```bash
scripts/run_md_to_xhs_cards.sh path/to/post.md
```

Tune card style:

```bash
scripts/run_md_to_xhs_cards.sh path/to/post.md \
  --width 1242 --height 1660 \
  --background "#f3f3f3" \
  --text-color "#161616"
```

Soft tone preset:

```bash
scripts/run_md_to_xhs_cards.sh path/to/post.md \
  --background "#faf9f6" \
  --quote-bg "#f4f2eb" \
  --quote-border "#e8e3d7" \
  --quote-accent "#7a756a"
```

Signature-at-end preset:

```bash
scripts/run_md_to_xhs_cards.sh path/to/post.md \
  --author "鹿不角" \
  --signature-text "-- 鹿不角"
```
