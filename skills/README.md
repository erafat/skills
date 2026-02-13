# Skills Catalog

This folder contains all individual skill projects in this repository.

Each skill is self-contained with its own `SKILL.md` and supporting files.

## Available Skills

| Skill | Purpose | Entry Files |
|---|---|---|
| [`cite-them-all`](./cite-them-all/) | Academic citation assistant for Markdown manuscripts. Detects claims that need references and helps add vetted citations. | [`SKILL.md`](./cite-them-all/SKILL.md), [`README.md`](./cite-them-all/README.md) |
| [`gmail-invoice-processor`](./gmail-invoice-processor/) | Processes Gmail invoices and generates structured Excel summaries with extraction notes. | [`SKILL.md`](./gmail-invoice-processor/SKILL.md), [`README.md`](./gmail-invoice-processor/README.md) |
| [`md-to-xhs-cards`](./md-to-xhs-cards/) | Converts Markdown into Xiaohongshu-style image cards while preserving structure and embedded images. | [`SKILL.md`](./md-to-xhs-cards/SKILL.md), [`references/render-spec.md`](./md-to-xhs-cards/references/render-spec.md) |

## Folder Layout

```text
skills/
├── README.md
├── cite-them-all/
├── gmail-invoice-processor/
└── md-to-xhs-cards/
```

## Notes

- Keep each skill in its own folder.
- Put detailed docs in each skill folder (`README.md`, `references/`, `scripts/`).
- Keep `SKILL.md` as the main instruction entry point for Codex/Claude.
