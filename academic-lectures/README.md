# academic-lectures

A Codex-oriented skill for building complete medical academic lecture presentations as `.pptx` files.

## Purpose

This skill handles the full lecture workflow:
- structured intake
- audience and duration calibration
- medicine-specific slide architecture
- speaker notes
- optional light PubMed search
- optional AI-generated visuals
- optional deadline-aware staged preparation

## Usage

Invoke it when you want Claude to create a medical teaching presentation or lecture deck, for example:

```text
make a lecture on insular epilepsy
create a lecture on status epilepticus for fellows
prepare a talk on epilepsy surgery outcomes
```

## Current Scope

This skill now assumes Codex-first behavior:
- intake should use `request_user_input` when Codex is in Plan mode, otherwise normal chat intake
- AI image generation should prefer the bundled local Gemini script in `scripts/gemini_image_gen.py`
- Baoyu image generation is fallback only when those skills are actually installed in the current Codex environment
- PPTX assembly may still need a local workflow selection if the Claude-specific PPTX path is unavailable

## Repository Contents

```text
academic-lectures/
├── SKILL.md
├── scripts/
│   ├── gemini_image_gen.py
│   └── gemini_image_gen.sh
└── references/
    ├── scheduled-prep.md
    └── slide-structure.md
```

## Key References

- [`SKILL.md`](./SKILL.md)
- [`references/slide-structure.md`](./references/slide-structure.md)
- [`references/scheduled-prep.md`](./references/scheduled-prep.md)
