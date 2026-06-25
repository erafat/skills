---
name: cv-update-review
description: >
  Run a confirmation-gated CV update workflow for Word CV documents: set up a
  reusable profile, scan configured local activity sources plus public evidence
  such as PubMed through NCBI E-utilities and configured website/RSS feeds,
  prepare a CV update packet, ask the user to approve completed/public/accepted
  items, create a dated `.docx` copy, and update or verify the copy while
  preserving the existing CV's section-specific conventions. Use when asked to
  update a CV/resume, run a monthly CV review, gather publications/lectures/
  professional activities, or create a public reusable CV updater for colleagues.
---

# CV Update Review

## Overview

Run a public, profile-driven CV update workflow. The skill discovers candidate
activities, drafts a review packet, requires explicit user approval, then edits
only a dated copy of the Word CV.

This skill is intentionally confirm-first. It must never silently decide that an
item belongs on the CV.

## Public-First Design

Do not hard-code private file paths, employer details, author identities, or CV
section names in this skill. Use a local config file instead.

Default config path:

```bash
.cv-update-review/config.json
```

Configs may use `${BASECAMP_ROOT}` for vault-relative paths, especially when an
iCloud/Obsidian vault lives under different usernames on different machines. The
helper scripts resolve `${BASECAMP_ROOT}` from the environment when set, or from
the nearest vault containing `START_HERE.md` and `AGENTS.md`.

If no config exists, run setup:

```bash
python3 .agents/skills/cv-update-review/scripts/setup_config.py \
  --output .cv-update-review/config.json
```

Use `profiles/example.json` as a public-safe example only. Do not edit it with
real personal data.

## Eligibility Rule

Default eligibility is strict:

- include only completed, public, or accepted activities
- include PubMed-indexed or accepted publications
- include public/accepted lectures, invited talks, presentations, public media,
  publicly released digital scholarship, and completed service/leadership items
- exclude planned, drafted, submitted-but-not-accepted, internal-only, or
  speculative work
- exclude routine recurring items unless the profile marks them as milestones

For podcasts, newsletters, websites, or recurring educational media, default to
major milestones rather than every routine release unless the user explicitly
changes the rule.

See `references/eligibility-rules.md` before resolving borderline items.

## Monthly Workflow

### 1) Resolve the Window

Use the system-local date for relative dates.

Use `review_schedule.cadence` from the config when present.

Default monthly window:

- start: first day of the prior completed calendar month
- end: last day of the prior completed calendar month

Quarterly window:

- start: first day of the prior completed calendar quarter
- end: last day of the prior completed calendar quarter

Ad hoc only:

- ask the user for the target month or date range before scanning

Custom cadence:

- follow `review_schedule.custom_cadence` if it is concrete enough to resolve a
  date window; otherwise ask the user before scanning

If the user names a month or date range, use that exact range.

### 2) Load Configuration

Read `.cv-update-review/config.json` or the user-supplied config path.

Required fields:

- `cv_document`
- `output_dir`
- at least one evidence source:
  - `pubmed.author_queries`
  - `rss_feeds`
  - `website_urls`
  - `local_activity_paths`
  - `local_search_roots`
  - `manual_scholar_sources`

If required fields are missing, run setup or ask for the missing values before
scanning.

If `review_schedule.offer_automation` is true and no automation exists yet,
offer to configure one. A CV automation must run in
`packet_only_until_user_approval` mode: it may scan sources and prepare the
review packet, but it must not create or edit a Word CV copy until the user
approves exact entries, sections, wording, and evidence sufficiency.

### 3) Gather Evidence

Use the smallest source set that can answer the request.

Local sources:

- configured activity logs
- configured project/status files
- configured journal or worklog paths
- configured folders containing releases, talks, manuscripts, abstracts, or
  teaching artifacts

Optional helper:

```bash
python3 .agents/skills/cv-update-review/scripts/scan_local_activity.py \
  --config .cv-update-review/config.json \
  --start YYYY-MM-DD \
  --end YYYY-MM-DD \
  --output .cv-update-review/evidence/local_YYYY-MM.json
```

Public sources:

- PubMed through NCBI E-utilities:

```bash
python3 .agents/skills/cv-update-review/scripts/scan_pubmed.py \
  --config .cv-update-review/config.json \
  --start YYYY-MM-DD \
  --end YYYY-MM-DD \
  --output .cv-update-review/evidence/pubmed_YYYY-MM.json
```

- configured RSS/Atom feeds:

```bash
python3 .agents/skills/cv-update-review/scripts/scan_rss.py \
  --config .cv-update-review/config.json \
  --start YYYY-MM-DD \
  --end YYYY-MM-DD \
  --output .cv-update-review/evidence/rss_YYYY-MM.json
```

- Google Scholar/profile checks:
  - use configured profile/search URLs as a manual or browser verification
    source
  - do not build a fragile Scholar scraper into the required workflow
  - if a colleague configures a permitted third-party provider, record that as a
    profile-specific source and cite it in the packet

Collaboration and mentoring sources:

- scan configured project/status files for collaborator names, trainee roles,
  student/fellow/resident labels, observerships, mentoring language, and
  supervised deliverables
- identify whether a project involved a junior collaborator or mentee who may
  belong under Mentoring Activities even if the project itself is not yet a
  completed CV work
- keep mentoring candidates separate from project-output candidates; do not
  treat an unfinished project as CV-ready just because it reveals a mentoring
  relationship

### 4) Show Candidate Preview

Before asking for private recall, show the user the actual candidate items found
by source. Do not provide only counts.

For each source, include:

- short candidate label/title
- activity type and proposed or provisional CV section
- evidence pointer: URL, file path and line number, PMID, or feed name
- eligibility status

Keep the preview concise enough to scan. Group clear duplicates or repeated
project-status heartbeat lines when needed, but preserve enough evidence detail
for the user to decide what is missing or wrongly included.

### 5) Category And Section Cross-Check

Before finalizing the packet, classify each candidate by activity type:

- manuscript or journal publication
- abstract or poster
- talk, invited lecture, course/session lecture, or conference presentation
- teaching aid, public media, website, software, or educational artifact
- mentoring, supervision, observership, or trainee collaboration
- service, committee, leadership, review, grant, or award

Use the activity type to choose the CV section. Titles alone are not enough.
When two items share a similar title, keep them separate if their activity types
differ. For example, a conference talk and a journal article with similar titles
must be evaluated and placed independently: the talk belongs with talks or
conference presentations, while the journal article belongs with manuscripts or
published research articles.

If the same publication list appears in more than one CV location, inspect both
locations and decide whether both need the new item to preserve the existing CV
structure. Record that decision in the packet.

### 6) Collaboration/Mentee Review

Before the recall prompt, ask whether configured collaboration projects include
junior collaborators, trainees, students, residents, fellows, visiting scholars,
or observers who should be considered under Mentoring Activities.

Show any names and roles already found from project/status evidence. For each,
include:

- name
- inferred role or level
- project or activity source
- proposed mentoring wording
- confidence and what still needs confirmation

Do not insert mentoring entries until the user confirms the person, role,
institution, supervision years, and wording.

### 7) Prompt For Private Recall

Before finalizing the packet, ask:

```text
What completed, public, or accepted professional activities from <window> may be missing from public records or local files? Examples: accepted manuscripts, invited talks, delivered lectures, committee/service work, peer review, mentorship milestones, grants/awards, public media, or completed institutional activities.
```

If the user provides items, ask for enough evidence to classify them:

- date
- activity type
- title/name
- role
- venue/institution/platform
- public URL, acceptance notice, program, email, certificate, or local file path

Do not include private recall items in the confirmed update list until the user
supplies sufficient evidence or explicitly accepts a low-evidence packet note.

### 8) Build The Review Packet

Create a dated Markdown packet before any Word edit:

```bash
python3 .agents/skills/cv-update-review/scripts/build_update_packet.py \
  --config .cv-update-review/config.json \
  --start YYYY-MM-DD \
  --end YYYY-MM-DD \
  --evidence .cv-update-review/evidence/local_YYYY-MM.json \
  --evidence .cv-update-review/evidence/pubmed_YYYY-MM.json \
  --evidence .cv-update-review/evidence/rss_YYYY-MM.json \
  --output <output-dir>/cv-update-packet_YYYY-MM-DD.md
```

Use the packet shape in `references/packet-template.md`.

Each candidate must show:

- activity type
- proposed CV section
- draft wording
- evidence
- confidence
- eligibility status
- unresolved questions

### 9) Stop For Approval

Stop after the packet unless the user has already approved specific entries in
the current conversation.

Require approval at entry level:

- include/exclude
- final CV section
- final wording
- whether evidence is sufficient

Do not treat "looks good" as approval if the packet still contains unresolved
section or wording questions.

### 10) Extract CV Style Before Editing

Before editing a Word CV, inspect the current document's conventions near the
target sections:

```bash
python3 .agents/skills/cv-update-review/scripts/extract_cv_style.py \
  --docx "/path/to/cv.docx" \
  --section "Published and Accepted Research Articles" \
  --section "Formal Teaching"
```

Match the existing CV, including:

- author order and punctuation
- journal abbreviations, years, volume/issue/pages, DOI style
- abstract database wording
- lecture title quotation style
- venue/date/location order
- mentorship table or list format
- capitalization quirks already present in that section

Do not globally normalize the CV unless the user explicitly asks.

### 11) Create A Dated Word Copy

Never edit the original CV directly.

Create a dated copy:

```bash
python3 .agents/skills/cv-update-review/scripts/copy_dated_cv.py \
  --config .cv-update-review/config.json \
  --date YYYY-MM-DD
```

Then edit the dated copy only. Prefer the dedicated document-editing tools when
available. If editing the `.docx` package directly, follow
`references/docx-editing-rules.md`.

### 12) Verify The Updated Copy

After editing:

- extract text from the dated copy and confirm approved entries appear exactly
- confirm excluded entries do not appear
- confirm original CV remains unchanged
- render or visually inspect the Word/PDF output when possible
- return a concise changelog with the dated copy path

## Output Contract

After a discovery run, return:

- packet path
- source window
- number of candidates by eligibility status
- items requiring user confirmation
- whether no Word document was edited

After an approved Word update, return:

- dated CV copy path
- entries inserted, grouped by section
- verification performed
- any residual uncertainty

## Failure Handling

- If config is missing, run setup or ask for setup values.
- If PubMed is unavailable, continue with local/RSS/manual sources and mark
  PubMed unavailable in the packet.
- If RSS parsing fails for one feed, continue with other feeds and record the
  failed feed.
- If Google Scholar cannot be checked safely, leave it as a manual verification
  task in the packet.
- If the CV document is missing, stop before packet application and report the
  missing path.
- If a dated copy already exists, create a suffix such as `_v2` unless the user
  explicitly authorizes overwrite.
- If visual verification cannot run, report the next best text extraction check.

## References

- `references/public-setup-guide.md`: setup flow for colleagues
- `references/eligibility-rules.md`: include/exclude decisions
- `references/packet-template.md`: review packet structure
- `references/docx-editing-rules.md`: Word copy and edit safety rules
