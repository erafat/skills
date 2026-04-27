---
type: resource
scope: illustration_production_guide
created: 2026-04-27
updated: 2026-04-27
status: active
---

# Illustration Guide - Taste, Style, and Image Generation

## Core Principle

Illustration generation is not a prompt. It is a controlled visual production pipeline.

The job is to choose the right visual purpose, style lane, model/tool path, reference role, composition unit, text policy, and review gate before asking for pixels.

## Default Taste

BaseCamp's default house direction is:

**Warm Editorial Analog Clarity**

It should feel:

- editorial rather than cinematic
- tactile rather than glossy
- warm without becoming sentimental
- restrained rather than decorative
- designed rather than merely rendered
- medically calm and dignified when clinical subjects appear
- simple enough that one visual idea survives at a glance

Default visual preferences:

- one dominant compositional move
- one restrained palette family
- one material story
- generous negative space
- clear focal point
- readable silhouettes
- human warmth through body language and staging
- no generic glossy AI finish

## Purpose Gate

Start by naming the image's job.

Common jobs:

- `patient education`: reassuring, clear, bias-aware, low cognitive load
- `research / academic`: precise, restrained, abstract, not decorative
- `essay illustration`: metaphorical, editorial, emotionally intelligent
- `poster / infographic`: hierarchy, scanability, text discipline
- `podcast / brand cover`: memorable thumbnail, one idea, minimal text
- `website / app`: atmosphere and visual support without cluttering the interface
- `presentation visual`: fast comprehension from a distance, usually one claim or process

If the job is unclear, do not pick a style yet.

## Model Layer

Keep taste separate from model choice.

- Use OpenAI Image 2.0 as the default production image path across the vault for illustrations, covers, posters, typography-led concept art, visual examples, and style-lane samples.
- Use Gemini / Nano Banana mainly for exploration, rough concepting, or when explicitly requested.
- Do not default to deterministic HTML/SVG/PNG when the user asks for an image, poster, cover, or style example. Use deterministic code, SVG, HTML/CSS, PowerPoint, or layout tools only when the user explicitly requests deterministic/editable output, or when exact labels, charts, diagrams, UI, or final production typography are the deliverable.
- Use manual cleanup or design tools for final typography, print layout, and small corrections.

Do not ask an image model to solve layout, text, medical accuracy, character consistency, and composition in one pass.

## Reference Discipline

Every reference image needs a declared role:

- `style reference`
- `character reference`
- `composition reference`
- `palette reference`
- `mood reference`
- `medical/device reference`
- `negative reference`

Extract the principle, not the composition.

Allowed:

- "large negative space"
- "few elements"
- "warm cream palette"
- "simple abstract motif"
- "calm academic tone"

Avoid:

- copying layout geometry
- copying panel structure
- copying distinctive line placement
- copying color blocking so closely that the result feels derived

## Text Policy

Important text does not belong inside generated artwork.

Use generated images for:

- scene
- emotion
- body language
- metaphor
- atmosphere
- one conceptual beat

Use HTML/CSS, slides, Markdown cards, or design tools for:

- medical explanations
- labels
- legends
- captions
- patient instructions
- dense diagram text

Exceptions:

- tiny reviewed labels
- title-only cover art
- short episode labels such as `Ep.4`
- deliberate poster typography when exact rendering is reviewed

## Composition Units

Preferred units:

- `single scene card`: safest for patient education and narrative assets
- `cover / hero image`: safe when text is separate or minimal
- `abstract mark`: best for podcast covers and brand markers
- `presentation visual`: one concept or process, sized for distance
- `infographic`: use only when labels are simple and will be checked

High-risk units:

- full comic page
- multi-panel medical explainer
- speech-balloon-heavy patient education
- dense labeled diagrams rendered entirely by the model
- anything requiring recurring character identity plus exact text

## Character Consistency

Character consistency is a production mechanism, not a wish.

For recurring people, create or reference:

- character sheet image path
- locked descriptors for age, skin tone, hair, clothing, silhouette, posture, role
- versioned changes when the character design changes
- explicit "do not change" constraints

For patient education, consistency is trust and bias control. Reject outputs where a character drifts in race, age, role, authority, or emotional status.

Watch for authority drift:

- the clinician becomes more polished than patients
- patients become passive props
- one race/age group is stereotyped into a role
- the medical professional is centered when the patient story is the point

## Medical And Ethical Guardrails

Before generating patient-facing or clinical imagery, check:

- Is there only one clear visual idea?
- Is all important text outside the generated image?
- Does the staging preserve patient dignity and agency?
- Does the image avoid diagnostic disclosure in public-facing settings?
- Does it avoid medical horror cues, dramatic seizure imagery, fake charts, misleading devices, and hero-doctor/passive-patient staging?

Bias review is part of art direction, not a final compliance pass.

## Style Lanes

### Warm Editorial Analog Clarity

Default BaseCamp house style.

Use for:

- essays
- conceptual covers
- knowledge visuals
- reflective education pieces
- general-purpose visual direction

Style DNA:

- tactile analog texture
- warm paper or off-white ground
- restrained palette with 1-2 accents
- editorial composition
- clear hierarchy
- humanized but not stock-like figures

Prompt prefix:

```text
Art-directed editorial image with tactile analog texture, restrained palette, generous negative space, clear hierarchy, subtle paper grain, warm humanized finish, and composition that feels designed rather than generic AI glossy.
```

Primary reference:

- `references/openai-image-2-reference-style-guide.md`

### Patient Education Indie Comic

Use for:

- waiting-room comics
- first-visit explainers
- patient journey visuals
- clinic workflow education

Style DNA:

- warm human-centered storytelling
- tactile comic illustration
- calm clinic environments
- portrait/mobile scene cards
- body language over facial detail
- text outside the generated image

Canonical source:

- `Projects/Waiting Room Comics/comic/epilepsy-first-visit-mobile/prompts/00-style-system.md`

Core rules:

- generate one scene at a time
- use portrait composition for mobile cards
- keep all critical text outside the image
- avoid giant speech balloons and dense panel grids
- lock recurring characters with character sheets and descriptors

### Minimal Academic Cover

Use for:

- podcast covers
- episode art
- specialist publication markers
- abstract research themes

Style DNA:

- one abstract motif
- warm paper background
- restrained academic palette
- little to no text
- thumbnail legibility
- no literal medical collage

Canonical source:

- `Projects/AED/docs/episode-cover-design-philosophy-v1.md`

Core rules:

- use one visual idea per cover
- use only the episode number by default
- avoid people, skulls, hospital rooms, microphones, lightning, fake EEG clutter, and copied reference compositions

### Swiss Editorial Clinical Flat

Use for:

- clinical-academic slide illustrations
- process visuals in presentations
- simple professional medical scenes
- non-glossy workshop visuals

Style DNA:

- warm off-white / cream background
- clean muted ink outlines
- flat editorial figures
- minimal fills: cream, slate, muted blue-gray, restrained ochre
- calm academic or clinical space
- generous negative space
- simplified but recognizable medical objects
- professional, approachable, non-cinematic tone

Verified prompt source:

- `references/ai-beyond-chatbot/illustration-prompts.md`

Exemplar images:

- `assets/ai-beyond-chatbot/slide6-panel1.png`
- `assets/ai-beyond-chatbot/slide6-panel2.png`
- `assets/ai-beyond-chatbot/slide6-panel3.png`
- `assets/ai-beyond-chatbot/slide3-illustration.png`
- `assets/ai-beyond-chatbot/slide4-illustration.png`

House descriptor:

```text
Swiss editorial flat illustration, warm off-white and cream palette, muted ink outlines, minimal color fills (ochre, slate, cream), no gradients, no texture. Professional, academic tone. No text in the image.
```

Accepted nuance:

Prompt for flat fills and no gradients, but tolerate subtle model-added shading if it preserves the calm editorial style and does not become glossy, cinematic, or overly dimensional.

Reject conditions:

- generated body text or fake paragraphs
- bright orange or saturated yellow-orange dominance
- glossy UI or realistic office rendering
- busy background props
- medical scene becoming dramatic or heroic
- multiple competing focal points

### Semantic Typography Concept Poster

Use for:

- typography-led concept posters
- Chinese word / phrase / short-sentence visualizations
- essay or social-cover graphics where the main idea is a word becoming an image
- poster studies where type, metaphor, and image must operate as one field
- modern flat geometric type posters where the core word becomes a semantic visual symbol through grid, color fields, transparent layers, and symbolic geometry

Source reference:

- X Article by `@xiaoxiaodong01`: `https://x.com/xiaoxiaodong01/status/2048652673826869294`
- Article title: `GPT2: 字体美学+文字图鉴+大字报+瞳孔地震级 · 升级版`
- Verbatim prompt stored at `references/semantic-typography-concept-poster-verbatim-prompt.md`.
- Geometric typography option stored at `references/semantic-typography-geometric-poster-template.md`.
- Example for `神经内科` stored at `references/semantic-typography-geometric-poster-shenjingneike.md`.
- Prompt example for `Epilepsy` stored at `references/semantic-typography-epilepsy-poster-example.md`.
- Prompt example for `Neurology` stored at `references/semantic-typography-neurology-poster-example.md`.

Style DNA:

- giant readable Chinese title as the dominant visual structure
- type is not a caption; type becomes architecture, stage, terrain, barrier, atmosphere, or emotional carrier
- image and text coexist in one unified visual field rather than separate blocks
- one strong semantic metaphor extracted from the word or phrase
- restrained but high-impact poster design
- natural reading path: title first, metaphor second, small supporting text only if it deepens the concept
- strong negative space and breathing room
- color chosen from meaning and emotional temperature, usually 2-4 core colors
- exhibition-poster quality: minimal, controlled, memorable, emotionally charged

Core process:

1. Analyze the input text before designing.
- Surface meaning
- deeper implication
- emotional temperature
- cultural associations
- narrative tension
- historical or social context if relevant
- most visually powerful character, word, or phrase

2. Select one visual metaphor.
- The metaphor should feel inevitable once seen.
- Prefer a single precise symbolic relationship over many decorative ideas.
- Useful directions include scale contrast, pressure, distance, concealment, offering, loss, escape, collapse, waiting, collision, softness versus hardness, or time.

3. Make type and image interdependent.
- Let the subject stand before, enter, lean on, hide within, pass through, or be shaped by the main characters.
- Use the title as spatial structure, not as pasted lettering.
- If supporting words appear, embed them lightly into the visual field instead of making a sidebar.

4. Preserve readability.
- The main Chinese title must be large, complete, legible, and free of wrong characters.
- Important text must be reviewed manually.
- If text accuracy matters, consider rendering final typography outside the image model.

Prompt scaffold:

```text
Create a typography-led conceptual poster based on the input text.
First interpret the text's surface meaning, deeper implication, emotional tone, cultural associations, and hidden tension.
Make the main Chinese title "[INPUT TEXT]" huge, complete, legible, and structurally central.
The title should become the visual architecture of the poster, not a caption pasted beside an illustration.
Build one precise visual metaphor that grows from the meaning of the text.
Integrate image, type, negative space, color, and any small supporting text into one unified visual field.
Avoid separated columns, magazine-directory layout, generic decorative small text, random fake English, crowded collage, cheap gradients, and template-like commercial poster design.
Use restrained exhibition-poster aesthetics, strong typography, controlled color, high emotional memory, and a natural reading path.
Input text:
Language:
Optional context:
Optional emotional direction:
Optional cultural direction:
Forbidden elements:
Allow supporting text: yes/no
If yes, explain how supporting text deepens the theme:
```

Reject conditions:

- title is misspelled, incomplete, unreadable, or visually ambiguous
- image and type feel like separate layers
- poster becomes a multi-column information board
- random microtext, fake labels, fake coordinates, or meaningless English filler
- too many symbols competing with the core metaphor
- color feels template-like, cheap, or unrelated to meaning
- visual beauty overrides the word's actual meaning

## Prompt Architecture

Use this skeleton for new production prompts:

```text
Purpose:
Audience:
Asset type:
Model/tool path:
Style lane:
Reference roles:
Scene:
Subject:
Composition:
Palette:
Texture/material:
Text policy:
Character locks:
Medical/ethical constraints:
Avoid:
Review checklist:
```

For simple prompts, collapse unused lines, but do not omit purpose, style lane, composition, text policy, and avoid list.

## Pre-Generation Gate

Before generating, answer yes/no:

- Is the purpose and audience clear?
- Is exactly one style lane selected?
- Is there one dominant visual idea?
- Is the text policy explicit?
- Are reference roles labeled?
- Are medical/ethical constraints explicit when relevant?
- Is the output unit appropriate for the model?

If any answer is no, revise the prompt before generating.

## Post-Generation Review

Judge the output against:

- purpose fit
- one clear visual idea
- lane consistency
- composition clarity
- palette discipline
- character consistency and dignity
- bias/authority drift
- text accuracy or absence
- medical plausibility
- thumbnail or distance readability, if relevant

Record rejected examples with the failure mode:

- `glossy AI skin`
- `two competing focal points`
- `authority drift`
- `fake clinical text`
- `copied reference composition`
- `too much warm accent`
- `text embedded where it should be editable`

## Promotion Rule For New Lanes

Do not casually create new style lanes.

A new lane should be promoted only when it has:

- a repeated use case
- at least one accepted example
- a short style descriptor
- an avoid list
- a prompt prefix or recipe
- a reason it is not already covered by an existing lane

## Current Lesson

The strongest outputs in BaseCamp came from narrowing the unit of work:

- one scene
- one lane
- one palette
- one clear purpose
- one review gate

Consistency comes from production discipline, not from asking the model to "keep it consistent."
