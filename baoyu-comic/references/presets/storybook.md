# storybook

Storybook预设 - Cozy patient-education comic with watercolor warmth

## Base Configuration

| Dimension | Value |
|-----------|-------|
| Art Style | storybook-watercolor (default) |
| Tone | warm |
| Layout | standard (default) |

Equivalent to: `--art storybook-watercolor --tone warm`

Variant for stronger cartoon linework: `--art cozy-hand-drawn-storybook-cartoon --tone warm`

## Unique Rules

When `--style storybook` is used, ALL rules below must be applied.

### Anti-Realism Guardrails (CRITICAL)

- Keep the look clearly illustrated and non-photorealistic.
- No cinematic lighting, no 3D render look, no realistic skin pores/wrinkles.
- Simplified facial features (dot/oval eyes, minimal nose/mouth lines).
- Minimal shading (one soft shadow tone max); no glossy highlights.

### Warm Paper + Paint Feel

- Subtle warm paper texture in the background (never busy).
- Soft watercolor/gouache fills with gentle edges.
- Calm palette: warm neutrals + one or two accent colors per page.

### Reassurance-First Composition

- Prioritize friendly expressions and open body language.
- Avoid “scary” medical imagery (no blood, no harsh red alarms).
- Keep diagrams icon-based and uncluttered (4–6 elements max).
- Use narrator boxes for detail; keep in-image labels short.

### Text Legibility (Gemini-Friendly)

- Prefer large printed SANS-SERIF for all text.
- Keep wording EXACT; if text would be unreadable, leave the bubble/box blank rather than garble.

## Quality Markers

- ✓ Looks like a modern children’s-book illustration
- ✓ Warm, calm, reassuring mood
- ✓ Minimal detail; no uncanny realism
- ✓ Clear reading flow and strong focal points
- ✓ Text is readable or intentionally omitted

## Reference

- Art style details: `references/art-styles/storybook-watercolor.md`
- Alternate art style details: `references/art-styles/cozy-hand-drawn-storybook-cartoon.md`
