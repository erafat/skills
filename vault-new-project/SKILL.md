---
name: vault-new-project
description: Use when the user asks to make/create a new project folder under AI Vault; read `CLAUDE.md` first, then scaffold the folder with `README.md` and `STATUS.md`, and update the project table in `CLAUDE.md`.
---

# AI Vault: New Project Scaffold

## When to use
Trigger for requests like:
- “make a new project folder”
- “create a new project under AI Vault”
- “start a new project called X”

## Workflow (do in order)

### 1) Read the vault rules
- Open `/Users/er/Documents/AI Vault/CLAUDE.md`.
- Follow any “New rule” / project-tracking instructions found there.

### 2) Confirm inputs (ask only if missing)
- **Project name** (folder name).
- **Owner** (default: `Erafat`).
- **Status** (default: `active`).
- **One-line note** for the project list in `CLAUDE.md`.

### 3) Create the project folder
- Create `/Users/er/Documents/AI Vault/<Project Name>/`.
- If the folder already exists, do not delete or rename anything.

### 4) Scaffold required files
Create (or add if missing) inside the project folder:

- `README.md`
  - First line: `# <Project Name>`
  - Second line: `Status tracker: \`STATUS.md\``
  - Include a short overview and “what belongs here” so the folder is understandable without opening other files.

- `STATUS.md`
  - Title: `# <Project Name> - Status`
  - Include a **Snapshot** section with:
    - `Status: <active|paused|complete>`
    - `Owner: <Owner>`
    - `Start date: YYYY-MM-DD`
    - `Last updated: YYYY-MM-DD`
  - Include: `Goals`, `Current Focus`, `Next Actions`, `Risks / Blockers`.

**Dates**
- Use today’s date for `Start date` (only if new) and always for `Last updated`.

### 5) Update AI Vault memory
- In `/Users/er/Documents/AI Vault/CLAUDE.md`, add (or update) one row in the **Projects** table:
  - Project column should link to `<Project Name>/STATUS.md`.
  - Set status/owner/last updated.
  - Add the one-line note.

### 6) Initialize git version control
Every new project folder must be a git repository.

```bash
cd "/Users/er/Documents/AI Vault/<Project Name>"
git init
git add README.md STATUS.md
git commit -m "init: scaffold <Project Name>"
```

- If the folder is already inside a parent git repo, still run `git init` to create a nested repo (so project history is self-contained).
- Do not push to remote unless the user asks.
- Add a `.gitignore` with at minimum:
  ```
  .DS_Store
  *.zip
  **/node_modules/
  ```

### 7) Verify
- Confirm the folder contains at least `README.md` and `STATUS.md`.
- Confirm the `CLAUDE.md` table includes the new project row.
- Confirm `git log --oneline` shows the initial commit.

## Guardrails
- Keep changes minimal: don’t reorganize other projects.
- Don’t overwrite existing project content; only add missing scaffold files and append/update the `CLAUDE.md` row.
- Treat the vault as sensitive: avoid PHI unless explicitly requested.
