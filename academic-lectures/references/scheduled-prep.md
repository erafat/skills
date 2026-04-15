# Phased Lecture Preparation — AutoResearch Loop

Inspired by Karpathy's AutoResearch: each day runs a **fixed-budget iteration** against a **single quality metric**. The agent reads a human-editable brief, makes bounded improvements, scores itself, and logs the result. Only improvements that raise the score are committed. By assembly day, the outline is ~80% done.

---

## Core Analogy

| AutoResearch | This Skill |
|---|---|
| `program.md` | `lecture-brief.md` — human edits this to direct the agent |
| `train.py` | `outline.md` — the artifact the agent iterates on |
| `val_bpb` metric | Lecture Quality Score (LQS) — single number to beat each day |
| 5-min training run | Fixed daily budget: 3 PubMed searches, max 5 papers each |
| keep/discard loop | Only commit content that raises LQS |
| experiment log | `progress.md` — user reviews this between iterations |

---

## Lecture Quality Score (LQS)

Score 0–100, computed by the agent at the end of each daily iteration:

| Dimension | Max pts | How to score |
|---|---|---|
| Slide coverage | 30 | (slides with content / total target slides) × 30 |
| Evidence density | 25 | (slides with ≥1 citation / content slides) × 25 |
| Subtopic coverage | 25 | (key subtopics addressed / total key subtopics identified in brief) × 25 |
| Audience calibration | 10 | Self-assess: is vocabulary/depth right for [audience]? (0, 5, or 10) |
| Case vignette readiness | 10 | 0 = no case identified; 5 = case identified; 10 = case fully written |

**Rule:** Only commit today's changes to `outline.md` if LQS ≥ yesterday's LQS. If not, log the attempt and try a different angle tomorrow. Append score to `progress.md` regardless.

---

## Phase Calculation

```
days_remaining = deadline - today
phase1_end = today + floor(days_remaining * 0.5)
phase2_end = deadline - 1 day  (final day = assembly + review)
```

Example: 14-day deadline → Phase 1 = days 1–7, Phase 2 = days 8–13, Day 14 = assembly.

---

## Project Folder Structure

```
lecture-[topic-slug]/
├── lecture-brief.md              ← human-editable direction file (= program.md)
├── outline.md                    ← evolving artifact, built in Phase 2 (= train.py)
├── progress.md                   ← daily LQS log + experiment notes
├── resources/
│   ├── references.md             ← curated references (Vancouver format)
│   ├── daily-YYYY-MM-DD.md       ← Phase 1 daily collection
│   └── synthesis.md              ← end-of-Phase-1 synthesis
└── [topic-slug]-lecture.pptx     ← generated on assembly day
```

---

## lecture-brief.md Template

Create this file at project setup. The user can edit it at any time to redirect the agent:

```markdown
# Lecture Brief: [Topic]

## Core Goal
One sentence: what should the audience be able to do differently after this talk?

## Target Audience
[audience] — calibrate vocabulary and depth accordingly.

## Duration / Slide Target
[N] minutes → ~[M] slides

## Key Messages (3–5)
-
-
-

## Subtopics to Cover
List all subtopics the lecture must address. Agent uses this as the subtopic coverage checklist.
-
-

## Emphasis / Angle
What perspective or framing should this lecture take? (e.g., "focus on surgical decision-making", "emphasize what's changed in last 5 years", "build toward a single clinical pearl")

## Known Gaps / Open Questions
Agent will prioritize filling these:
-

## References to Anchor On
Paste any must-include papers here. Agent builds around these.
```

---

## Phase 1: Resource Collection (Daily Loop)

**Goal:** Fill `resources/daily-*.md` with raw material. Fixed budget per day — no open-ended searching.

**Daily focus rotation (7-day example):**

| Day | Focus area |
|---|---|
| 1 | Epidemiology + pathophysiology |
| 2 | Clinical presentation + diagnosis |
| 3 | Management + treatment guidelines |
| 4 | Landmark trials + evidence base |
| 5 | Controversies + unresolved questions |
| 6 | Audience-specific angle (what does [audience] most need?) |
| 7 | Synthesis — read all daily files, write `synthesis.md` |

**Each day's task prompt (fill in brackets):**

```
Academic lecture prep — Phase 1 Day [N] for "[topic]" lecture.
Audience: [audience]. Deadline: [date].
Project folder: [path]/lecture-[topic-slug]/

INSTRUCTIONS:
1. Read lecture-brief.md — note the key messages, subtopics, emphasis, and known gaps.
2. Run exactly 3 PubMed/web searches on today's focus area: [focus area].
   Collect the top 5 results per search. Budget = 15 papers max.
3. For each paper: extract title, authors, year, PMID/URL, and 1–2 sentence relevance note.
4. Save all findings to resources/daily-[YYYY-MM-DD].md.
5. Cross-reference with previous daily files — note connections, recurring themes, new gaps.
6. Append a "Connections" section: 2–3 sentences linking today's findings to prior days.
7. Add new citations to resources/references.md (Vancouver format).
8. Compute LQS for current project state and append to progress.md:
   "Day [N] | LQS: [score] | Focus: [area] | Papers added: [N] | Notes: [brief note]"
```

**Day 7 / last Phase 1 day — synthesis task (add to prompt):**

```
After completing the above:
9. Read all resources/daily-*.md files.
10. Extract the 10–15 most important concepts for this lecture.
11. Identify the strongest case vignette candidate (patient demographics, presenting symptoms,
    key decision point, teaching moment).
12. Flag which slides will need visuals (anatomy, pathophysiology, flowchart, data).
13. Write resources/synthesis.md — structured pre-outline with themes, evidence anchors,
    case vignette, visual slots, and any gaps that Phase 2 must fill.
```

---

## Phase 2: Outline Development (Daily Loop)

**Goal:** Build `outline.md` incrementally. Each day improves the outline and must raise LQS to commit.

Distribute slides evenly:
```
slides_per_day = ceil(total_slides / phase2_days)
```

**Each day's task prompt:**

```
Academic lecture prep — Phase 2 Day [N] for "[topic]" lecture.
Audience: [audience]. Total slides: [M].
Project folder: [path]/lecture-[topic-slug]/

INSTRUCTIONS:
1. Read lecture-brief.md — the direction file. This overrides your priors.
2. Read outline.md (current state) and resources/synthesis.md.
3. Compute yesterday's LQS from progress.md.
4. Write or improve slides [start]–[end] in outline.md using the slide format.
   For each slide: content bullets, speaker notes (bullet talking points), image recommendation.
   Ground every factual claim in resources/daily-*.md or resources/references.md.
   Mark gaps: [NEEDS USER INPUT: description].
5. Compute today's LQS.
6. If today's LQS ≥ yesterday's LQS: commit changes (write updated outline.md).
   If today's LQS < yesterday's LQS: log the attempt, revert to yesterday's outline.md,
   and note what to try differently tomorrow.
7. Append to progress.md:
   "Day [N] | LQS: [score] (was [prev]) | Slides: [start]–[end] | Committed: yes/no | Notes: [why]"
8. Update the progress header in outline.md:
   "Progress: [N]/[total] slides | LQS: [score] | Last updated: [date]"
```

---

## Assembly Day

When user invokes the skill on or near the deadline:

1. Read `outline.md` — confirm complete (flag any `[NEEDS USER INPUT]` slides)
2. Read `lecture-brief.md` — confirm final outline still matches goals; adjust if not
3. Read `resources/references.md`
4. Show user the final LQS and progress.md summary
5. Proceed to Step 7 (Image Generation) and Step 8 (PPTX Assembly) of SKILL.md
6. Intake already captured — skip re-asking unless user wants changes

---

## Setting Up Scheduled Tasks

Use `mcp__scheduled-tasks__create_scheduled_task`. Key parameters:
- **name:** `lecture-[topic-slug]-p1-day-N` or `lecture-[topic-slug]-p2-day-N`
- **schedule:** specific date at consistent time (e.g., 9:00 AM)
- **prompt:** fully filled-in task prompt above

Confirm with user after setup:
- Phase 1 dates + focus areas
- Phase 2 slide distribution per day
- Assembly date
- Remind: they can update `lecture-brief.md` at any time to redirect the agent
