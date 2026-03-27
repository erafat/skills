# academic-lectures

A Claude-oriented skill for building complete medical academic lecture presentations as `.pptx` files.

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

This is the original Claude version of the skill. It assumes Claude-side behaviors such as:
- structured intake via Claude question flow
- `.pptx` assembly through a Claude PPTX workflow

## Repository Contents

```text
academic-lectures/
├── SKILL.md
└── references/
    ├── scheduled-prep.md
    └── slide-structure.md
```

## Key References

- [`SKILL.md`](./SKILL.md)
- [`references/slide-structure.md`](./references/slide-structure.md)
- [`references/scheduled-prep.md`](./references/scheduled-prep.md)
