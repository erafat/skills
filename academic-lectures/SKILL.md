---
name: academic-lectures
description: >
  Build complete medical academic lecture presentations as .pptx files. Handles the full lecture lifecycle - structured intake, medicine-specific slide architecture, speaker notes, AI image generation via Gemini, light PubMed reference search, and optional phased preparation when a deadline is provided. Trigger when user says "make a lecture on X", "create a lecture on X", "build a lecture on X", "prepare a talk on X", "lecture on X", or any request to create a medical teaching presentation or lecture slide deck.
---

# Academic Lectures Skill

Builds structured medical lecture .pptx presentations with speaker notes, evidence-based content, and optional AI-generated visuals. Always run in full mode — no shortcuts.

## Step 1: Intake

Use AskUserQuestion to collect all of the following at once:

1. **Topic** — What is the lecture topic?
2. **Audience** — Who is the audience? Options: medical students / residents / fellows / attendings / mixed clinical (nurses, techs, other staff)
3. **Duration** — How long is the talk? (e.g., 20 min, 30 min, 45 min, 60 min) → slide count will be recommended
4. **Deadline** — When is this due? (date or relative, e.g., "next Friday", "in 2 weeks")
5. **Output path** — Where should the project folder and final .pptx be saved?
6. **Speaker notes style** — Bullet-point talking points (default) or full narrative script?
7. **References** — Will you provide your own? Or should I run a light PubMed search?
8. **Images** — Should I generate AI illustrations for relevant slides, or will you provide your own?
9. **Take-home points placement** — Best practice: show take-home points right after learning objectives AND repeat them at the end. Keep this default? (yes/no)

## Step 2: Slide Count Recommendation

Recommend based on duration at ~1.5 min/slide:

| Duration | Recommended slides |
|----------|--------------------|
| 20 min   | 13–14              |
| 30 min   | 18–20              |
| 45 min   | 28–30              |
| 60 min   | 38–40              |

Present the recommendation and ask the user to confirm or adjust before proceeding.

## Step 3: Project Folder Setup

Create a project subfolder at the user's specified output path:

```
lecture-[topic-slug]/
├── lecture-brief.md        ← human-editable direction file (user can update anytime)
├── outline.md              ← structured slide-by-slide content
├── progress.md             ← LQS log (phased prep only)
├── resources/
│   ├── references.md       ← collected or user-provided references
│   ├── daily-YYYY-MM-DD.md ← Phase 1 daily collection logs (phased prep only)
│   └── synthesis.md        ← end-of-Phase-1 synthesis (phased prep only)
└── [topic-slug]-lecture.pptx
```

Slugify the topic: lowercase, hyphens, no special characters (e.g., "Atrial Fibrillation" → `atrial-fibrillation`).

**Always create `lecture-brief.md`** at setup using the template in `references/scheduled-prep.md` — even for immediate development. It anchors the lecture goals and the user can edit it to redirect at any time.

## Step 4: References

**User-provided:** Ask them to paste references now or drop them into `resources/references.md`. Use Vancouver/AMA numeric citation format.

**Light PubMed search:** Use WebSearch to find 5–8 key papers. Search query format: `site:pubmed.ncbi.nlm.nih.gov [topic] [relevant subtopics]`. Save results to `resources/references.md` with title, authors, journal, year, PMID. Flag to user that citations must be verified before delivery.

## Step 5: Deadline Check → Phased Preparation

Ask the user:

> "Do you want to **sleep on it** — let me collect resources and build the outline over multiple days so the slides are ~80% ready when you sit down to review? Or should I **develop the slides now**?"

- **Sleep on it** → activate phased preparation. See `references/scheduled-prep.md` for full setup. Uses the deadline provided in intake to calculate phase lengths.
- **Develop now** → skip to Step 6 immediately.

If the user chose "sleep on it" but gave no deadline or a deadline ≤2 days away, flag that phased prep requires at least 3 days and offer to proceed with immediate development instead.

## Step 6: Generate Outline

Build `outline.md` using the medicine-specific slide structure. See `references/slide-structure.md` for full structure, slide types, visual recommendations, and audience calibration guidance.

**Key rules:**
- Calibrate vocabulary and depth to the specified audience
- Take-home points appear twice: after learning objectives AND at the end (unless user opted out)
- Every slide entry includes: title, bullet content, speaker notes, and image recommendation

Format each slide in `outline.md`:

```markdown
## Slide N: [Title]
**Type:** [slide type from slide-structure.md]
**Content:**
- bullet 1
- bullet 2

**Speaker Notes:**
- talking point 1
- talking point 2

**Image:** [None | anatomical diagram: description | pathophysiology flowchart: description | data visualization: description | clinical scenario illustration: description]
```

## Step 7: Image Generation

If user opted for AI-generated images:

1. Review `outline.md` — identify all slides with a non-None image recommendation
2. Eligible types: anatomical diagram, pathophysiology flowchart, data visualization, clinical scenario illustration
3. Skip: title, agenda, learning objectives, take-home points, references, and pure text/table slides
4. For each eligible slide, craft a detailed Gemini image prompt: medically accurate, clean educational style, appropriately labeled, white/light background
5. Invoke `baoyu-danger-gemini-web` skill for each image
6. Save images to `resources/` and update the image field in `outline.md` with the filename

## Step 8: Assemble .pptx

Invoke `anthropic-skills:pptx` to build the final presentation from `outline.md`.

Instructions to pass:
- Ask user for template preference or let pptx skill choose a clean professional academic theme
- Map each slide entry in `outline.md` directly to a slide
- Speaker notes go in the notes pane of each slide
- Embed generated images in their respective slides at a visually prominent position
- Save as `[topic-slug]-lecture.pptx` inside the project folder

## Step 9: Confirm and Summarize

After generation, report:
- Full path of saved .pptx
- Total slide count
- Which slides have AI-generated images
- Any placeholders requiring user attention (missing data, unverified citations, open questions)
- If phased prep was configured: the schedule and what to expect each day

---

## Reference Files

- `references/slide-structure.md` — full medicine-specific slide architecture, types, ordering, and audience calibration
- `references/scheduled-prep.md` — phased preparation workflow for deadline-driven lectures
