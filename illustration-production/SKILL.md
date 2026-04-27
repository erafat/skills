---
name: illustration-production
description: Use when the user asks to create, revise, review, prompt, art-direct, style-match, or make consistent BaseCamp illustrations and image-generation assets. Trigger for requests mentioning illustration prompts, image prompts, visual style guide, house style, style lane, taste, art direction, poster, cover art, comic panels, patient-education visuals, workshop/presentation visuals, OpenAI Image 2.0, generated images, visual examples, reference images, or rejected/accepted image outputs where consistent taste, guardrails, references, and review matter.
---

# Illustration Production

## Purpose

Create controlled, reviewable illustration assets and image-generation prompts for BaseCamp.

Core principle:

> Illustration generation is not a prompt. It is a controlled visual production pipeline.

## Trigger Cues

Use this skill when the user asks for any of the following:

- "make an illustration", "generate an image", "create a visual", "make a cover", "make a poster", "make a comic panel"
- "write an image prompt", "improve this image prompt", "prompt for OpenAI Image 2.0", "prompt for DALL-E", "prompt for Nano Banana"
- "use our house style", "make it match our style", "style lane", "style guide", "taste", "art direction", "visual philosophy"
- "use these images as reference", "what examples do we have", "accepted/rejected examples", "why did this output fail"
- "patient education visual", "waiting room comic", "AI Beyond Chatbot illustration", "presentation visual", "AED cover"

Do not use this skill for ordinary prose editing, non-visual research, deterministic UI implementation without custom illustration needs, or simple file organization unless visual taste/style/prompting is part of the task.

## Canonical Guide

Read the guide first for any new or materially changed visual task:

- `references/illustration-guide.md`

Use existing project-local rules when they are more specific:

- project `AGENTS.md`, `STATUS.md`, and local prompt files
- established cover, comic, deck, or illustration design docs
- AI Beyond Chatbot examples: `references/ai-beyond-chatbot/illustration-prompts.md`

## Intake Gate

Ask a specific intake before creating or materially revising an illustration, prompt system, style lane, or visual asset.

Ask 4-5 focused questions, usually:

1. Purpose and audience: what should this image do, and who is it for?
2. Asset type and destination: cover, scene card, slide visual, poster, infographic, website asset, etc.; where will it live?
3. Style lane or reference: use an existing lane/example, or create a new direction?
4. Constraints and guardrails: text policy, medical/ethical concerns, character consistency, privacy, brand limits, size/aspect ratio.
5. Autonomy level: should the agent choose and execute, or return options for sign-off first?

Do not implement skill file changes without intake. For ordinary asset work, if the user explicitly says to proceed with defaults, use the guide defaults and continue.

## Style Lane Registry

Current lanes:

- `Warm Editorial Analog Clarity`: default house style for editorial/conceptual visuals.
- `Patient Education Indie Comic`: clinic/patient education scenes, especially Waiting Room Comics.
- `Minimal Academic Cover`: AED-style abstract specialist cover art.
- `Swiss Editorial Clinical Flat`: clinical-academic slide illustrations and workshop visuals.
- `Semantic Typography Concept Poster`: typography-led concept posters where a word or phrase becomes the image structure.

Do not invent a new lane casually. Promote a new lane only when it has a repeated use case, accepted example, descriptor, avoid list, and a reason existing lanes do not fit.

## Workflow

1. Read the smallest relevant context.
- For new work, read the canonical guide.
- For project work, read the nearest `AGENTS.md` and project `STATUS.md`.
- For a named lane, read that lane's canonical source.

2. Classify the task.
- new asset
- prompt only
- style direction
- iteration on existing asset
- review/rejection pass
- lane creation

3. Select one style lane.
- Pick one lane by default.
- Do not blend lanes unless the user explicitly asks or the task clearly requires it.
- State the chosen lane and why it fits.

4. Choose the tool path.
- Default to OpenAI Image 2.0 for AI raster production through the Codex-native image generation tool.
- When the user asks for Image 2.0, call the native Image 2.0 generation path directly. Do not require or check `OPENAI_API_KEY`, and do not route through CLI/API wrappers, BaoYu tooling, Gemini/Nano Banana, browser hacks, local drawing, SVG, canvas, or deterministic placeholder art.
- If the native Image 2.0 tool is not exposed or callable in the current session, stop and report that exact tool-surface blocker. Do not substitute another renderer or create a lower-quality fallback unless the user explicitly authorizes that fallback after being told it is not Image 2.0.
- Use Gemini / Nano Banana only when requested, when a verified project path requires it, or when OpenAI Image 2.0 is unsuitable; Gemini should run through the project-approved script/API path with credentials from environment, local untracked config, or macOS Keychain.
- Use code/SVG/HTML/CSS/slides only for labels, layout, charts, diagrams, UI, or geometry that should remain deterministic, not as a replacement for requested Image 2.0 raster art.

5. Label references by role.
- style reference
- character reference
- composition reference
- palette reference
- mood reference
- medical/device reference
- negative reference

6. Draft the production prompt.
- Include purpose, audience, asset type, style lane, composition, palette, text policy, constraints, and avoid list.
- Use the guide's prompt architecture.
- Keep important text outside generated artwork unless explicitly approved.

7. Run the pre-generation gate.
- purpose clear
- one lane selected
- one visual idea
- text policy explicit
- reference roles labeled
- medical/ethical guardrails explicit when relevant
- output unit appropriate for the model

8. Generate, draw, or hand off.
- For raster image generation, use the Codex-native OpenAI Image 2.0 generation path and save accepted outputs into the project workspace.
- Never answer an Image 2.0 request by creating local vector drawings, CSS/SVG approximations, placeholder PNGs, or API-key-based substitutes.
- If native Image 2.0 generation is unavailable, hand off with the final prompt set, reference roles, and blocker instead of silently downgrading.
- For prompt-only tasks, deliver the prompt plus review checklist.
- For deterministic visuals, build the visual in code or the appropriate document/presentation tool.

9. Review the output.
- Check purpose fit, lane consistency, composition, palette, character consistency, bias/authority drift, text policy, medical plausibility, and thumbnail/distance readability.
- Save accepted project-bound assets in the workspace or project folder, not only in a temporary/generated location.
- Log rejected examples with a one-line failure mode when useful.

## Iteration Path

For an existing asset, do not restart from scratch by default.

1. Identify the accepted lane and source prompt.
2. Name the exact failure: composition, palette, character drift, text, medical cue, density, or tone.
3. Make one targeted change.
4. Re-run the review gate.

## Output Contract

When producing prompts or assets, report:

- selected style lane
- model/tool path
- reference roles used
- final prompt or prompt delta
- review checklist result
- saved asset paths, if any

Keep the response concise unless the user asks for a full art-direction packet.
