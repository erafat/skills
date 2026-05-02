# Skills Repository

Reusable skills for Codex and Claude.

This repository contains multiple self-contained skills. Each skill has its own `SKILL.md` and support files (`scripts/`, `references/`, templates, examples).

## Available Skills

### `cite-them-all`
- Location: [`cite-them-all/`](./cite-them-all)
- Purpose: Detects claims in Markdown manuscripts that need citations and helps add references from biomedical sources.
- Entry: [`cite-them-all/SKILL.md`](./cite-them-all/SKILL.md)

### `md-to-xhs-cards`
- Location: [`md-to-xhs-cards/`](./md-to-xhs-cards)
- Purpose: Converts Markdown into Xiaohongshu image cards while preserving structure and embedded local images.
- Entry: [`md-to-xhs-cards/SKILL.md`](./md-to-xhs-cards/SKILL.md)

### `manuscript-production`
- Location: [`manuscript-production/`](./manuscript-production)
- Purpose: Runs scholarly and clinical manuscripts as a staged production workflow from brief and source packet through drafting, verification, revision, and submission readiness.
- Entry: [`manuscript-production/SKILL.md`](./manuscript-production/SKILL.md)

## Repository Layout

```text
repo-root/
├── cite-them-all/
├── manuscript-production/
├── md-to-xhs-cards/
└── .github/
```

## Development

```bash
git clone https://github.com/erafat/skills.git
cd skills
```

Then work inside the individual skill folder you want to update.
