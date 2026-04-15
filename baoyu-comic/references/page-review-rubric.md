# Page Review Rubric

Automated quality gate for multi-page comic generation. Applied after every page is generated.

## When to Use

Apply rubric review for **multi-page projects (4+ pages)**. Ask the user to confirm or customize the rubric during Step 2 confirmation.

---

## Default Rubric Template

Presented to user for confirmation/customization at Step 2. Save finalized rubric as `rubric.md` in the comic output directory.

### 1. Character Fidelity
- [ ] All characters match the reference sheet (hair, clothing, skin tone)
- [ ] Skin tone consistency — no drift from reference across characters
- [ ] Character-specific identifiers present (glasses, accessories, signature clothing)

### 2. Style
- [ ] Art style matches selected style (e.g., storybook-watercolor, manga, ligne-claire)
- [ ] Faces match simplicity level specified (e.g., dot eyes only, no detailed features)
- [ ] Mood/tone matches selected tone (e.g., warm, neutral, dramatic)

### 3. Readability ⛔ HARD BLOCKER
- [ ] All speech bubbles legible — exact wording readable
- [ ] All narrator boxes legible — exact wording readable
- [ ] Panel flow clear — unambiguous reading order (left→right, top→bottom)
- [ ] Scene matches storyboard — correct characters, setting, and action

### 4. Tone & Content
- [ ] Emotional tone appropriate for audience
- [ ] No unintended alarming or offensive imagery

---

## Domain-Specific Extensions

When content signals suggest a specialized domain, prompt the user with relevant extension criteria. Examples:

### Medical / Patient Education
- [ ] Clinical environment looks safe and approachable (not sterile/frightening)
- [ ] No alarming imagery (no harsh red alarms, no blood unless clinically necessary)
- [ ] Medical procedures depicted accurately per storyboard

### Seizure / Neurology Content
- [ ] No stigmatizing visuals (no tongue-biting, foaming, dramatic Hollywood-style convulsions)
- [ ] Seizure type depicted accurately per storyboard (tonic-clonic, focal, absence)
- [ ] Patient shown on safe surface if falling — not suspended mid-air dramatically
- [ ] Bystander body language shows calm concern, not panic or horror

### Children's / Educational Content
- [ ] Age-appropriate visuals throughout
- [ ] Concepts clearly simplified — no jargon visible in panel text

---

## Rubric File Format

Save as `rubric.md` in the comic output directory. Format:

```markdown
# Page Review Rubric — {Comic Title}

## Hard Blockers ⛔
These criteria must pass. Auto-regenerate on failure.
- [ ] {criterion}

## Standard Criteria
All should pass. Auto-regenerate once on failure; escalate to user if still failing.
- [ ] {criterion}

## Decision Logic
- ✅ All pass → log results, proceed to next page
- ❌ Hard blocker fails → auto-regenerate, re-run rubric
- ❌ Any standard criterion fails → auto-regenerate once, re-run rubric
- ❌ Still failing after one regeneration → flag to user with specific failures before proceeding
```

---

## Step 2 Script (Multi-Page Projects)

When project has 4+ pages, include this in the Step 2 confirmation message:

> **Page Review Rubric**
> For multi-page projects I apply a quality rubric after each page — auto-regenerating if it fails, and only flagging you if it fails twice.
>
> Here's the default rubric for this project. Would you like to add, remove, or adjust any criteria before we start generating?
>
> [show default rubric + any domain-specific extensions detected]
>
> Reply "looks good" to use as-is, or tell me what to change.

---

## Step 7 Integration

After each page is generated:

1. Run rubric check against the image
2. Log result: `✅ Page N — all criteria passed` or `❌ Page N — failed: [list specific failures]`
3. On failure: adjust prompt targeting the specific failures, regenerate, re-check
4. On second failure: pause and surface to user with annotated failures before continuing
5. On pass: compress image if needed, proceed to next page
