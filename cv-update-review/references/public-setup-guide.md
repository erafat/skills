# Public Setup Guide

Use this guide when configuring the skill for a new person.

## Setup Command

```bash
python3 .agents/skills/cv-update-review/scripts/setup_config.py \
  --output .cv-update-review/config.json
```

The setup script writes JSON so it works without third-party Python packages.

Prefer `${BASECAMP_ROOT}` for paths inside the vault rather than absolute
machine-specific iCloud paths. The helper scripts resolve `${BASECAMP_ROOT}`
from the environment when set, or from the nearest BaseCamp vault containing
`START_HERE.md` and `AGENTS.md`.

## Information To Collect

- display name for packets
- current Word CV path, preferably using `${BASECAMP_ROOT}` if it is inside the
  vault
- output folder for packets and dated CV copies, preferably using
  `${BASECAMP_ROOT}` if it is inside the vault
- PubMed author query or ORCID-style search terms
- optional NCBI API key environment variable name
- RSS/Atom feeds to check
- public website URLs to manually verify
- Google Scholar/profile URLs to manually verify
- local activity logs or project/status paths
- recurring-output policy, especially whether podcasts/newsletters should be
  treated as individual entries or milestone-only
- preferred review cadence: monthly, quarterly, ad hoc only, or custom
- whether the user wants a scheduled automation offered/configured

## Recommended Defaults

- eligibility: completed/public/accepted only
- cadence: monthly
- automation: off by default; if enabled, automation should generate a packet
  only and wait for user approval before Word edits
- output mode: dated Word copy
- recurring media: major milestones only
- confirmation: required before every Word edit
- original CV: never edit directly

## Public Distribution Note

Keep user-specific config files out of public repositories. Publish only:

- `SKILL.md`
- `scripts/`
- `references/`
- `profiles/example.json`
- optional README generated outside the skill if a repository needs one

Do not publish real CVs, packet outputs, or private activity logs.
