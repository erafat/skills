# Skills Repository

Reusable skills for Codex and Claude.

This repository contains multiple self-contained skills. Each skill has its own `SKILL.md` and support files (`scripts/`, `references/`, templates, examples).

## Available Skills

### `cite-them-all`
- Location: [`/Users/er/skills/cite-them-all`](./cite-them-all)
- Purpose: Detects claims in Markdown manuscripts that need citations and helps add references from biomedical sources.
- Entry: [`/Users/er/skills/cite-them-all/SKILL.md`](./cite-them-all/SKILL.md)

### `gmail-invoice-processor`
- Location: [`/Users/er/skills/gmail-invoice-processor`](./gmail-invoice-processor)
- Purpose: Processes Gmail invoice emails, extracts vendor/amount data, and generates structured summaries.
- Entry: [`/Users/er/skills/gmail-invoice-processor/SKILL.md`](./gmail-invoice-processor/SKILL.md)

### `md-to-xhs-cards`
- Location: [`/Users/er/skills/md-to-xhs-cards`](./md-to-xhs-cards)
- Purpose: Converts Markdown into Xiaohongshu image cards while preserving structure and embedded local images.
- Entry: [`/Users/er/skills/md-to-xhs-cards/SKILL.md`](./md-to-xhs-cards/SKILL.md)

## Repository Layout

```text
skills/
├── cite-them-all/
├── gmail-invoice-processor/
├── md-to-xhs-cards/
├── docs/
└── .github/
```

## Development

```bash
git clone https://github.com/erafat/skills.git
cd skills
```

Then work inside the individual skill folder you want to update.

## References

- Installation docs: [`/Users/er/skills/docs/INSTALLATION.md`](./docs/INSTALLATION.md)
- Examples: [`/Users/er/skills/docs/EXAMPLES.md`](./docs/EXAMPLES.md)
- Contributing: [`/Users/er/skills/CONTRIBUTING.md`](./CONTRIBUTING.md)
