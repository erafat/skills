---
name: er-slides
description: >-
  Create professional HTML slide decks in the Swiss Modern editorial style: warm cream
  background, Archivo + IBM Plex fonts, coral accent, flat editorial illustrations via
  Imagen 4. Use when building any new presentation, talk, lecture, workshop deck, or
  adding slides to an existing presentation. Style is pre-decided, no discovery phase
  needed. Outputs a single self-contained HTML file with fullscreen mode, keyboard
  navigation, scroll-snap, and laptop media query baked in. Also handles illustration
  generation via Imagen 4 API and image embedding as base64 data URIs.
---

# er-slides

Build a single-file HTML presentation in the Swiss Modern editorial style established in the AI Beyond Chatbot Workshop deck.

## Quick Start

1. Copy `assets/base-template.html` to the target directory and rename it.
2. Read `references/design-system.md` and `references/slide-patterns.md`.
3. Build slides using the patterns. Each slide = `.slide > .slide-stage > .slide-content`.
4. Generate illustrations if needed — see `references/illustration-guide.md`.
5. Run the curly-quote fix after any JS edits (see below).

## Workflow

### Step 1 — Brief

Collect from the user (or infer from context):
- Slide list or outline
- Presenter name, role, institution, date
- Which slides need illustrations
- Output file path

If the brief is incomplete, ask only for what is blocking you — do not ask for everything upfront.

### Step 2 — Build slides

Always start from `assets/base-template.html`. Never start from scratch.

Available patterns (read `references/slide-patterns.md` for full HTML + CSS):
| Pattern | Use case |
|---|---|
| Title | First slide, presenter info |
| Statement / Quote | One-idea punchy slide |
| Two-col text + illustration | Workhorse layout — process steps with image |
| Three-panel grid | "Three projects / points" |
| Live demo | Pause for live tool demo |
| Full-bleed image + hotspots | Interactive image with tooltips |
| Evidence / comparison grid | Before/after, side-by-side stats |
| Mocked chat UI | Show chatbot before/after demo |

Rules:
- Every slide fits in one viewport — no scrolling within a slide, ever.
- Add `.reveal` to elements that should animate in on scroll.
- Kicker to h2 to body copy is the standard hierarchy.
- Use `clamp()` for all sizes — never fixed `px` for typography or spacing.
- Illustration containers: `aspect-ratio: 4/3`, `overflow: hidden`.

### Step 3 — Illustrations

Read `references/illustration-guide.md` before generating any image.

Generate via script:
```bash
python3 ~/.claude/skills/er-slides/scripts/gen_illustration.py \
    "Subject description" output.png
```

Embed as base64 data URI — no external file refs in the final HTML:
```python
import base64
b64 = base64.b64encode(open("output.png","rb").read()).decode()
# use f"data:image/png;base64,{b64}" as img src
```

### Step 4 — Post-edit fix (mandatory after any JS edit)

Run the curly-quote sed fix to prevent JS parse errors from smart quotes:
```bash
sed -i '' 's/\xe2\x80\x98/'"'"'/g; s/\xe2\x80\x99/'"'"'/g; s/\xe2\x80\x9c/"/g; s/\xe2\x80\x9d/"/g' "path/to/file.html"
```

### Step 5 — Laptop tuning

If slides feel cramped on a 13-15 inch laptop, add per-slide CSS overrides inside the laptop media query block at the bottom of `<style>`. Adjust in this order:
1. Root variable overrides (already in the block)
2. Per-slide typography and spacing
3. Grid column ratios
4. Only then touch base desktop styles

## Design Rules (non-negotiable)

- **Colors**: use only the token set. No new colors. `--accent` sparingly.
- **Fonts**: Archivo for display, IBM Plex Sans for body, IBM Plex Mono for labels/kickers.
- **Images**: always base64-embedded, `object-fit: cover`, `aspect-ratio: 4/3`.
- **No JS libraries** — vanilla JS only, zero dependencies.
- **No inline `px` for typography or layout** — `clamp()` or CSS variables only.

## References

- `references/design-system.md` — full token set, CSS architecture, component CSS
- `references/slide-patterns.md` — all layout patterns with HTML + CSS examples
- `references/illustration-guide.md` — Imagen 4 API, Swiss editorial style, proven prompts
- `assets/base-template.html` — the starting point for every deck
- `scripts/gen_illustration.py` — illustration generation script
