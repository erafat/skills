# Gemini Image Prompting Guide

Optimizations for Gemini image generation models (Nano Banana Pro and similar).

## When to Apply

Apply this guide when:
- User specifies `--model gemini` or `--gen gemini`
- Using Gemini-based image generation backend
- User requests "Gemini-optimized" prompts

## Prompt Structure

Every generated prompt MUST follow this structure:

```
1. PREAMBLE (Gemini constraints as comment block)
2. CHARACTER REFERENCE instruction
3. STYLE + ASPECT RATIO line
4. PANEL-BY-PANEL specifications
5. LAST CHECK section (1-3 bullets)
6. STYLE CLOSING note
```

## Preamble Template

Prepend this comment block to EVERY prompt file:

```markdown
# Gemini Image Generation Best Practices (reduce distortion)
# Model: Gemini image generation (Nano Banana Pro)
# Use with: attach `{comic-dir}/characters/characters.png` as strict character reference
#
# STYLE (IMPORTANT — avoid "too real"):
# - {art-style} style, {tone} tone.
# - If {art-style} is `storybook-watercolor`: cozy hand-drawn storybook cartoon, warm paper texture, slightly wobbly ink lines (subtle line-weight variation), soft watercolor/gouache fills, minimal shading, simplified facial features (NOT realistic).
# - If {art-style} is `cozy-hand-drawn-storybook-cartoon`: cozy hand-drawn storybook cartoon with clearer outlines, warm paper texture, flat-to-soft gouache fills, minimal shading, simplified facial features (NOT realistic).
#
# TEXT QUALITY (IMPORTANT):
# - Render text in plain printed SANS-SERIF.
# - Keep wording EXACT; do not invent or paraphrase.
# - Use LARGE font; avoid tiny labels.
# - If any text would be unreadable, LEAVE THAT BOX BLANK rather than garbling.
#
# IDENTITY LOCK (IMPORTANT):
# - Character identity must match the attached character sheet exactly (same face shape, hair, eye color, baseline skin tone).
# - Serious/dim lighting must not change baseline skin tone; use shading while preserving the base hue (no "recasting" by mood).
# - Do not swap characters or reinterpret casting; all characters must remain the same individuals across all pages.
#
# CAST LOCK (IMPORTANT):
# - Use exact character references consistently (tokens preferred; exact names acceptable for small casts):
{cast-lock-tokens}
# - Do not change face shape, hairstyle, eye color, outfit colors, or baseline skin tone across pages.
#
# DIAGRAMS:
# - Prefer simple icons + short labels (≤6 words per label).
# - Put numbers in large callout cards, not tiny on-map labels.
# - Replace long "study: result" text with compact stat cards (1-2 lines max).
#
# AVOID (IMPORTANT — especially for `storybook-watercolor` and `cozy-hand-drawn-storybook-cartoon`):
# - No photorealism, no 3D render look, no cinematic lighting, no detailed skin pores/wrinkles.
```

### Cast Lock Names (Small Cast)

If the cast is small (≤4) and you are not using tokens, you MAY use exact names only:

```
# CAST LOCK (IMPORTANT):
# - Use these exact names whenever referencing characters: {Name 1}, {Name 2}, {Name 3}.
# - Do not swap characters; keep hair/eye color/outfits/skin tone consistent with the character sheet.
```

Tokens are still preferred for Gemini consistency, but exact-name cast lock is acceptable for simple patient-education comics.

### Cast Lock Token Format

For each character, generate a token line:

```
#   - {Name} [CHAR_{NAME_UPPER}]: {age}, {hair}, {eyes}, {skin tone}; {outfit}; {accessories}.
```

Example:
```
#   - Marcus [CHAR_MARCUS]: 35, short brown hair, hazel eyes, light neutral skin; gray t-shirt + jeans; medical alert bracelet.
#   - Dr. Chen [CHAR_CHEN]: 45, black hair with gray temples, dark brown eyes, medium warm skin; white coat over blue scrubs; ID badge + pen.
```

## Panel Specification Format

Each panel MUST include:

```markdown
Panel {N} ({size}, {position}): {shot type} {scene description}.
- Camera: {angle}
- Characters: {who} [CHAR_TOKEN] {action/expression}
- Props/BG: {key elements}
- Dialogue {Speaker} [CHAR_TOKEN]: "{exact text}"
- Narrator: "{narration text}"
- Caption: "{caption text}"
```

### Size/Position Values
- `top 1/6`, `top 1/5`, `top 1/4`, `top 1/3`
- `center 1/3`, `center 1/2`, `center 2/3`
- `bottom 1/6`, `bottom 1/4`, `bottom 1/3`
- `SPLASH` for full/half page impact panels

### Shot Types
- Wide shot, Medium shot, Close-up, Extreme close-up
- Low angle, High angle, Bird's eye, Eye level

## Last Check Section

End EVERY prompt with a "Last Check" section:

```markdown
---
LAST CHECK BEFORE RENDERING:
- [ ] {count constraint, e.g., "Exactly 4 mechanism labels, no more"}
- [ ] {character constraint, e.g., "ONLY ONE instance of each character per panel"}
- [ ] {text constraint, e.g., "All dialogue uses exact wording above"}
- [ ] {visual constraint, e.g., "Flowchart arrows point LEFT-TO-RIGHT only"}
```

## Failure Mode Prevention

### Text Quality
| Problem | Prevention Rule |
|---------|-----------------|
| Garbled text | "If text would be unreadable, LEAVE BLANK" |
| Tiny labels | "Use LARGE font" |
| Invented text | "Keep wording EXACT" |
| Wrong font | "Plain printed SANS-SERIF" |

### Character Consistency
| Problem | Prevention Rule |
|---------|-----------------|
| Character swaps | Include [CHAR_TOKEN] with every mention (preferred); otherwise use exact character names consistently |
| Skin tone drift | "Lighting must not change baseline skin tone" |
| Outfit changes | Lock outfit colors in cast tokens |
| Duplicate characters | "ONLY ONE instance of each character" in Last Check |

### Layout Clarity
| Problem | Prevention Rule |
|---------|-----------------|
| Contradictory flow | Pick ONE direction: "top-down" OR "left-to-right", never both |
| Crowded diagrams | Cap at 4-6 major elements per diagram |
| Dense labels | Max 6-10 words per label; move details to narration |

### Diagram Best Practices
| Instead of... | Use... |
|---------------|--------|
| "Smith et al. 2020: 2.36x increased risk" | Stat card: "OSA Risk: 2.36x" |
| Long explanation labels | Icon + short label + narrator box for details |
| Multiple study citations in image | Single summary stat + "Multiple studies confirm" in narration |

## Style Line Format

After the preamble, include a single style line:

```markdown
Educational manga page, {art-style} style, {aspect} aspect ratio.
```

Examples:
- `Educational manga page, ohmsha style, 3:4 portrait.`
- `Educational comic page, ligne-claire style, 3:4 portrait.`
- `Educational comic page, storybook-watercolor style, 3:4 portrait.`
- `Educational comic page, cozy-hand-drawn-storybook-cartoon style, 3:4 portrait.`
- `Knowledge comic page, realistic style, 4:3 landscape.`

## Closing Note Format

End each prompt with a brief style reminder:

```markdown
{Visual approach summary}, {key techniques}, {mood/action focus}.
```

Examples:
- `Clean manga style, dramatic visual metaphors, no talking heads.`
- `Mechanistic visual metaphors, action-focused.`
- `Iceberg metaphor, systems view, discovery action, scale emphasis.`
