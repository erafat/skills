---
name: baoyu-comic
description: Knowledge comic creator supporting multiple art styles and tones. Creates original educational comics with detailed panel layouts and sequential image generation. Use when user asks to create "知识漫画", "教育漫画", "biography comic", "tutorial comic", or "Logicomix-style comic".
---

# Knowledge Comic Creator

Create original knowledge comics with flexible art style × tone combinations.

## Usage

```bash
/baoyu-comic posts/turing-story/source.md
/baoyu-comic article.md --art manga --tone warm
/baoyu-comic  # then paste content
```

## Options

### Visual Dimensions

| Option | Values | Description |
|--------|--------|-------------|
| `--art` | storybook-watercolor (default), cozy-hand-drawn-storybook-cartoon, ligne-claire, manga, realistic, ink-brush, chalk | Art style / rendering technique |
| `--tone` | warm (default), neutral, dramatic, romantic, energetic, vintage, action | Mood / atmosphere |
| `--layout` | standard (default), cinematic, dense, splash, mixed, webtoon | Panel arrangement |
| `--aspect` | 3:4 (default, portrait), 4:3 (landscape), 16:9 (widescreen) | Page aspect ratio |
| `--lang` | auto (default), zh, en, ja, etc. | Output language |
| `--model` | default, gemini | Image generation model; `gemini` applies Nano Banana Pro optimizations |

### Partial Workflow Options

| Option | Description |
|--------|-------------|
| `--storyboard-only` | Generate storyboard only, skip prompts and images |
| `--prompts-only` | Generate storyboard + prompts, skip images |
| `--images-only` | Generate images from existing prompts directory |
| `--regenerate N` | Regenerate specific page(s) only (e.g., `3` or `2,5,8`) |

Details: [references/partial-workflows.md](references/partial-workflows.md)

### Art Styles (画风)

| Style | 中文 | Description |
|-------|------|-------------|
| `ligne-claire` | 清线 | Uniform lines, flat colors, European comic tradition (Tintin, Logicomix) |
| `storybook-watercolor` | 童书水彩 | Cozy children’s-book / editorial cartoon look: slightly wobbly ink lines, warm paper texture, soft watercolor/gouache fills, simplified facial features (NOT realistic) |
| `cozy-hand-drawn-storybook-cartoon` | 温馨手绘童书卡通 | Cozy hand-drawn storybook cartoon: clearer ink outlines, warm paper texture, flat-to-soft gouache fills, minimal shading, simplified facial features (NOT realistic) |
| `manga` | 日漫 | Large eyes, manga conventions, expressive emotions |
| `realistic` | 写实 | Digital painting, realistic proportions, sophisticated |
| `ink-brush` | 水墨 | Chinese brush strokes, ink wash effects |
| `chalk` | 粉笔 | Chalkboard aesthetic, hand-drawn warmth |

### Tones (基调)

| Tone | 中文 | Description |
|------|------|-------------|
| `neutral` | 中性 | Balanced, rational, educational |
| `warm` | 温馨 | Nostalgic, personal, comforting |
| `dramatic` | 戏剧 | High contrast, intense, powerful |
| `romantic` | 浪漫 | Soft, beautiful, decorative elements |
| `energetic` | 活力 | Bright, dynamic, exciting |
| `vintage` | 复古 | Historical, aged, period authenticity |
| `action` | 动作 | Speed lines, impact effects, combat |

### Preset Shortcuts

Presets with special rules beyond art+tone:

| Preset | Equivalent | Special Rules |
|--------|-----------|---------------|
| `--style ohmsha` | `--art manga --tone neutral` | Visual metaphors, NO talking heads, gadget reveals |
| `--style wuxia` | `--art ink-brush --tone action` | Qi effects, combat visuals, atmospheric elements |
| `--style shoujo` | `--art manga --tone romantic` | Decorative elements, eye details, romantic beats |
| `--style storybook` | `--art storybook-watercolor --tone warm` | Soft storybook feel, simplified features, warm paper texture, minimal shading; avoid photorealism/3D/cinematic lighting |

### Compatibility Matrix

| Art Style | ✓✓ Best | ✓ Works | ✗ Avoid |
|-----------|---------|---------|---------|
| ligne-claire | neutral, warm | dramatic, vintage, energetic | romantic, action |
| storybook-watercolor | warm, neutral | energetic, vintage | dramatic, action |
| cozy-hand-drawn-storybook-cartoon | warm, neutral | energetic, vintage | dramatic, action |
| manga | neutral, romantic, energetic, action | warm, dramatic | vintage |
| realistic | neutral, warm, dramatic, vintage | action | romantic, energetic |
| ink-brush | neutral, dramatic, action, vintage | warm | romantic, energetic |
| chalk | neutral, warm, energetic | vintage | dramatic, action, romantic |

Details: [references/auto-selection.md](references/auto-selection.md)

## Gemini Model Optimization

When `--model gemini` is specified (or user requests Gemini-optimized output), apply special prompt formatting from [references/gemini-image-prompting.md](references/gemini-image-prompting.md).

### Key Requirements

**Every prompt file MUST include:**
1. **Preamble block** - Gemini constraints as comment header
2. **Cast lock section** - tokens preferred; for small casts, exact names are acceptable
3. **Last check section** - Validation checklist at end of each prompt

### Preamble Structure

```
# Gemini Image Generation Best Practices (reduce distortion)
# Model: Gemini image generation (Nano Banana Pro)
# Use with: attach `{comic-dir}/characters/characters.png`
#
# TEXT QUALITY: Sans-serif, LARGE font, exact wording, leave blank if unreadable
# IDENTITY LOCK: Match character sheet exactly, preserve skin tone in lighting
# CAST LOCK: tokens preferred; exact names ok for small casts
# DIAGRAMS: Icons + short labels (≤6 words), large stat cards
```

### Failure Mode Prevention

| Problem | Rule |
|---------|------|
| Garbled text | "If unreadable, LEAVE BLANK" |
| Character swaps | Include `[CHAR_TOKEN]` with every mention (preferred); otherwise use exact character names consistently |
| Skin tone drift | "Lighting must not change baseline skin tone" |
| Contradictory layout | Pick ONE flow direction (top-down OR left-to-right) |
| Dense labels | Max 6-10 words per label; details go to narration |
| Duplicate characters | Add to Last Check: "ONLY ONE instance per panel" |

### Last Check Section

End every prompt with:
```
---
LAST CHECK BEFORE RENDERING:
- [ ] {count constraint}
- [ ] {character constraint}
- [ ] {text/visual constraint}
```

Full guide: [references/gemini-image-prompting.md](references/gemini-image-prompting.md)

### Gemini API Setup (`--model gemini`)

For `--model gemini`, use Gemini/Google API credentials:

| Variable | Required | Notes |
|----------|----------|-------|
| `GEMINI_API_KEY` | Yes (or `GOOGLE_API_KEY`) | Preferred variable name |
| `GOOGLE_API_KEY` | Yes (or `GEMINI_API_KEY`) | Fully equivalent fallback |
| `GOOGLE_IMAGE_MODEL` | No | Defaults to `gemini-3-pro-image-preview` |
| `GOOGLE_BASE_URL` | No | Custom Google-compatible endpoint |

Quick setup in skill env file:

```bash
mkdir -p .baoyu-skills
cat >> .baoyu-skills/.env <<'EOF'
GEMINI_API_KEY=your_key_here
# Optional:
# GOOGLE_IMAGE_MODEL=gemini-3-pro-image-preview
EOF
```

## Auto Selection

Content signals determine default art + tone + layout (or preset):

| Content Signals | Recommended |
|-----------------|-------------|
| Tutorial, how-to, programming, educational | **ohmsha** preset |
| Pre-1950, classical, ancient | realistic + vintage |
| Personal story, mentor | ligne-claire + warm |
| Patient education, reassurance, anxiety-reducing, clinic visits | **storybook** preset (or cozy-hand-drawn-storybook-cartoon + warm) |
| Martial arts, wuxia | **wuxia** preset |
| Romance, school life | **shoujo** preset |
| Biography, balanced | ligne-claire + neutral |

**When preset is recommended**: Load `references/presets/{preset}.md` and apply all special rules.

Details: [references/auto-selection.md](references/auto-selection.md)

## Script Directory

**Important**: All scripts are located in the `scripts/` subdirectory of this skill.

**Agent Execution Instructions**:
1. Determine this SKILL.md file's directory path as `SKILL_DIR`
2. Script path = `${SKILL_DIR}/scripts/<script-name>.ts`
3. Replace all `${SKILL_DIR}` in this document with the actual path

**Script Reference**:
| Script | Purpose |
|--------|---------|
| `scripts/merge-to-pdf.ts` | Merge comic pages into PDF |
| `scripts/gemini-image.ts` | Gemini API wrapper for page generation (forces Google provider) |

## File Structure

Output directory: `comic/{topic-slug}/`
- Slug: 2-4 words kebab-case from topic (e.g., `alan-turing-bio`)
- Conflict: append timestamp (e.g., `turing-story-20260118-143052`)

**Contents**:
| File | Description |
|------|-------------|
| `source-{slug}.{ext}` | Source files |
| `analysis.md` | Content analysis |
| `storyboard.md` | Storyboard with panel breakdown |
| `characters/characters.md` | Character definitions |
| `characters/characters.png` | Character reference sheet |
| `prompts/NN-{cover\|page}-[slug].md` | Generation prompts |
| `NN-{cover\|page}-[slug].png` | Generated images |
| `{topic-slug}.pdf` | Final merged PDF |

## Language Handling

**Detection Priority**:
1. `--lang` flag (explicit)
2. EXTEND.md `language` setting
3. User's conversation language
4. Source content language

**Rule**: Use user's input language or saved language preference for ALL interactions:
- Storyboard outlines and scene descriptions
- Image generation prompts
- User selection options and confirmations
- Progress updates, questions, errors, summaries

Technical terms remain in English.

## Workflow

### Progress Checklist

```
Comic Progress:
- [ ] Step 1: Setup & Analyze (1.1 Preferences, 1.2 Analyze, 1.3 Check existing)
- [ ] Step 2: Confirmation - Style & options ⚠️ REQUIRED
  - [ ] 2a: Confirm style/tone/layout/reviews
  - [ ] 2b: Confirm page review rubric (multi-page projects only) → rubric.md
- [ ] Step 3: Generate storyboard + characters
- [ ] Step 4: Review outline (conditional)
- [ ] Step 5: Generate prompts
- [ ] Step 6: Review prompts (conditional)
- [ ] Step 7: Generate images ⚠️ CHARACTER REF REQUIRED
  - [ ] 7.1 Generate character sheet FIRST → characters/characters.png
  - [ ] 7.2 For each page: generate → rubric check → pass or regenerate → next
- [ ] Step 8: Merge to PDF
- [ ] Step 9: Completion report
```

### Flow

```
Input → Preferences → Analyze → [Check Existing?] → [Confirm: Style + Reviews + Rubric?] → Storyboard → [Review?] → Prompts → [Review?] → Images (per-page: generate → rubric check → pass/regenerate) → PDF → Complete
```

### Step Summary

| Step | Action | Key Output |
|------|--------|------------|
| 1.1 | Load EXTEND.md preferences | Config loaded |
| 1.2 | Analyze content | `analysis.md` |
| 1.3 | Check existing directory | Handle conflicts |
| 2a | Confirm style, focus, audience, reviews | User preferences |
| 2b | Confirm page review rubric (4+ pages) | `rubric.md` |
| 3 | Generate storyboard + characters | `storyboard.md`, `characters/` |
| 4 | Review outline (if requested) | User approval |
| 5 | Generate prompts (apply Gemini preamble if `--model gemini`) | `prompts/*.md` |
| 6 | Review prompts (if requested) | User approval |
| **7.1** | **Generate character sheet FIRST** | `characters/characters.png` |
| **7.2** | Generate each page → rubric check → pass or regenerate | `*.png` files |
| 8 | Merge to PDF | `{slug}.pdf` |
| 9 | Completion report | Summary |

### Step 7: Image Generation ⚠️ CRITICAL

**Character reference is MANDATORY for visual consistency.**

**7.1 Generate character sheet first**:
```bash
# Use Reference Sheet Prompt from characters/characters.md
npx -y bun ${SKILL_DIR}/../baoyu-image-gen/scripts/main.ts \
  --promptfiles characters/characters.md \
  --image characters/characters.png --ar 4:3
```

If `--model gemini`:
```bash
npx -y bun ${SKILL_DIR}/scripts/gemini-image.ts \
  --promptfiles characters/characters.md \
  --image characters/characters.png --ar 4:3
```

**Compress character sheet** (recommended):
Compress to reduce token usage when used as reference image:
- Use available image compression skill (if any)
- Or system tools: `pngquant`, `optipng`, `sips` (macOS)
- **Keep PNG format**, lossless compression preferred

**7.2 Generate each page WITH character reference**:

| Skill Capability | Strategy |
|------------------|----------|
| Supports `--ref` | Pass `characters/characters.png` with EVERY page |
| No `--ref` support | Prepend character descriptions to EVERY prompt file |

```bash
# Example: ALWAYS include --ref for consistency
npx -y bun ${SKILL_DIR}/../baoyu-image-gen/scripts/main.ts \
  --promptfiles prompts/01-page-xxx.md \
  --image 01-page-xxx.png --ar 3:4 \
  --ref characters/characters.png
```

If `--model gemini`:
```bash
npx -y bun ${SKILL_DIR}/scripts/gemini-image.ts \
  --promptfiles prompts/01-page-xxx.md \
  --image 01-page-xxx.png --ar 3:4 \
  --ref characters/characters.png
```

**Full workflow details**: [references/workflow.md](references/workflow.md)

### Step 7.2: Per-Page Rubric Review

After each page is generated, run the rubric check autonomously:

```
1. Read rubric.md from the comic output directory
2. Review the generated image against every criterion
3. Log result clearly:
   ✅ Page N — all criteria passed → compress + proceed
   ❌ Page N — failed: [list specific failures] → adjust prompt + regenerate
4. After regeneration, re-run rubric check
5. If still failing after one regeneration → pause, show user the image + specific failures
```

Full rubric guide: [references/page-review-rubric.md](references/page-review-rubric.md)

### EXTEND.md Paths

| Path | Location |
|------|----------|
| `.baoyu-skills/baoyu-comic/EXTEND.md` | Project directory |
| `$HOME/.baoyu-skills/baoyu-comic/EXTEND.md` | User home |

**EXTEND.md Supports**: Watermark | Preferred art/tone/layout | Custom style definitions | Character presets | Language preference

Schema: [references/config/preferences-schema.md](references/config/preferences-schema.md)

## References

**Core Templates**:
- [analysis-framework.md](references/analysis-framework.md) - Deep content analysis
- [character-template.md](references/character-template.md) - Character definition format
- [storyboard-template.md](references/storyboard-template.md) - Storyboard structure
- [ohmsha-guide.md](references/ohmsha-guide.md) - Ohmsha manga specifics
- [gemini-image-prompting.md](references/gemini-image-prompting.md) - Gemini/Nano Banana Pro optimization
- [page-review-rubric.md](references/page-review-rubric.md) - Per-page quality rubric template + autonomous review logic

**Style Definitions**:
- `references/art-styles/` - Art styles (storybook-watercolor, cozy-hand-drawn-storybook-cartoon, ligne-claire, manga, realistic, ink-brush, chalk)
- `references/tones/` - Tones (neutral, warm, dramatic, romantic, energetic, vintage, action)
- `references/presets/` - Presets with special rules (ohmsha, wuxia, shoujo)
- `references/layouts/` - Layouts (standard, cinematic, dense, splash, mixed, webtoon)

**Workflow**:
- [workflow.md](references/workflow.md) - Full workflow details
- [auto-selection.md](references/auto-selection.md) - Content signal analysis
- [partial-workflows.md](references/partial-workflows.md) - Partial workflow options

**Config**:
- [config/preferences-schema.md](references/config/preferences-schema.md) - EXTEND.md schema
- [config/first-time-setup.md](references/config/first-time-setup.md) - First-time setup
- [config/watermark-guide.md](references/config/watermark-guide.md) - Watermark configuration

## Notes

- Image generation: 10-30 seconds per page
- Auto-retry once on generation failure
- Use stylized alternatives for sensitive public figures
- Maintain style consistency via session ID
- **Step 2 confirmation required** - do not skip
- **Steps 4/6 conditional** - only if user requested in Step 2
- **Step 7.1 character sheet MUST be generated before pages** - ensures consistency
- **Step 7.2 EVERY page MUST reference characters** - use `--ref` or embed descriptions
- Watermark/language configured once in EXTEND.md
