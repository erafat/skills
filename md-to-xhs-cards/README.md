# md-to-xhs-cards

Convert Markdown into Xiaohongshu (小红书 / RedNote) image cards with deterministic layout, local image support, and optional direct XHS publishing.

## What It Does

- Converts `.md` content into 3:4 card images (`1080x1440` by default)
- Preserves source order (headings, paragraphs, lists, quotes, code, images)
- Supports Markdown images and Obsidian embeds (`![[...]]`)
- Generates a cover card and ending signature
- Optionally publishes generated cards to Xiaohongshu

## Quick Start

```bash
scripts/run_md_to_xhs_cards.sh path/to/post.md
```

Output:
- `NN-card.png` files
- `manifest.json`

## Render + Publish to XHS

```bash
scripts/run_md_to_xhs_cards.sh path/to/post.md \
  --publish-xhs \
  --publish-title "标题" \
  --publish-desc "正文摘要"
```

Dry-run publish:

```bash
scripts/run_md_to_xhs_cards.sh path/to/post.md \
  --publish-xhs \
  --publish-dry-run
```

## Cookie Configuration

Publishing reads cookie in this order:
1. `--publish-cookie`
2. `XHS_COOKIE` environment variable
3. `.env` in current directory or skill directory

## Files

- `SKILL.md` - skill instructions for Codex/Claude
- `scripts/md_to_xhs_cards.py` - renderer
- `scripts/publish_xhs.py` - publisher
- `references/render-spec.md` - render options/spec

## Keywords

Xiaohongshu, RedNote, 小红书, markdown to image cards, XHS publishing, Codex skill, Claude skill.
