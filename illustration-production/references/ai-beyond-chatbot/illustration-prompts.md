# Illustration Prompts

## Style Reference
All illustrations use the Swiss editorial flat style established in slide 3.
**Key style descriptor:**
> Swiss editorial flat illustration, warm off-white and cream palette, muted ink outlines, minimal color fills (ochre, slate, cream), no gradients, no texture. Professional, academic tone. No text in the image.

---

## Slide 3 — Original (the style reference)
**File:** `slide3-illustration.png`
**Model:** image-generation workflow, 16:9, high quality
**Prompt:**
```
Clean flat editorial illustration, wide landscape format (16:9). A senior physician (attending, older, white coat) stands in a bright clinical hallway and turns briefly toward a younger physician (fellow, late 20s, white coat). The attending says one short phrase — represented by a small minimal speech bubble with just a few words. The fellow stands listening, but radiating outward from his head is a structured thought-map: four labeled branches expanding cleanly — Audience, Format, Deadline, Tasks — each with a short note. The thought-map is rendered as a clean diagram, not a bubble cloud. No realistic anatomical detail. Style: Swiss editorial flat illustration, warm off-white and cream palette, muted ink outlines, minimal color fills (ochre, slate, cream), no gradients, no texture. Professional, academic tone. No text in the image.
```

---

## Slide 4 — Approved final
**File:** `slide4-new-image.png`
**Model:** imagen-4.0-generate-001, 4:3
**Prompt:**
```
Flat editorial illustration, 4:3 aspect ratio, warm cream background filling entire frame edge to edge. Left to right: FAR LEFT — an attending physician in a white coat with warm brown skin, standing and gesturing toward the right. CENTER — three workers in business casual dark clothing with warm brown skin seated at a long shared desk: first person using a magnifying glass over papers, second person writing on a notepad, third person at a desktop computer. FAR RIGHT — a large monitor displaying a clean PowerPoint presentation. Subtle left-to-right flow. Warm cream background, slate grey and ochre accents only on furniture and objects not clothing, bold clean ink outlines, flat editorial illustration style, no gradients. No text, no labels, no words anywhere.
```

## Slide 4 — Replacement prompt (match slide 3 style)
**File:** `slide4-illustration-v2.png`
**Recommended model:** Gemini / Imagen, landscape 16:9
**Prompt:**
```
Clean flat editorial illustration, wide landscape format (16:9). Show the idea of one short physician request becoming autonomous work. Left side: an attending physician in a white coat stands in a calm academic-clinical setting and gestures toward a younger physician or AI-enabled clinician. Center: the request transforms into a compact working scene with three distinct stages flowing left to right, but without any words or labels. Stage 1 suggests literature search and review: one person scanning papers or a journal article. Stage 2 suggests outline and slide drafting: one person organizing notes or slide thumbnails at a desk. Stage 3 suggests verification and finalization: one person reviewing a presentation on a monitor. The whole composition should feel like a single clean process, not separate comic panels. Use subtle directional cues and composition to imply Request -> Agent Work -> Finished Output, but do not include arrows, labels, UI text, or any readable words. Keep the people and environment in the same Swiss editorial flat illustration style as slide 3: warm off-white and cream palette, muted ink outlines, minimal color fills with mostly cream and slate, and only very restrained soft ochre accents. Avoid bright orange, saturated mustard, strong warm highlights, or high-contrast accent blocks. No gradients, no texture, professional academic tone. No text in the image.
```

**Tighter variant if the model keeps drifting into a generic office scene:**
```
Swiss editorial flat illustration, wide 16:9. A physician in a white coat on the far left gives one brief request with a very small empty speech bubble. Across the rest of the frame, the work unfolds autonomously in one continuous academic scene: a researcher reviewing a paper, a planner arranging slide cards or notes, and a reviewer checking a final presentation on a monitor. Keep the scene minimal, elegant, and diagram-like rather than busy. Professional medical-academic context, warm cream background, muted slate and cream tones, with only sparse low-saturation ochre accents. Avoid bright orange clothing, bold amber furniture, or any high-contrast warm color dominance. Clean ink outlines, flat fills only, no gradients, no texture, no text anywhere.
```

**4:3 variant with softer palette**
```
Swiss editorial flat illustration, 4:3 aspect ratio. Match the visual language of the other deck illustrations: warm off-white and cream palette, muted ink outlines, minimal color fills with mostly cream and slate, and only subtle low-saturation ochre accents. Avoid bright orange, saturated yellow-orange, strong warm contrast, heavy shading, glossy UI, or realistic office rendering. On the far left, an attending physician in a white coat gives one brief request with a very small empty speech bubble. Across the rest of the frame, the work unfolds autonomously in one continuous, minimal academic-clinical scene: one person reviewing a paper, one person arranging slide cards or notes, and one person checking a final presentation on a monitor. Keep the composition calm, sparse, elegant, and diagram-like. No text anywhere.
```

---

## Slide 6 Panels — Current (v3, matching slide 3 style)
**Model:** imagen-4.0-generate-001, 1:1

**Panel 1 — IOM Billing Master** (`slide6_test_panel.png`)
```
Clean flat editorial illustration. A physician in a white coat sits at a clean minimal desk in side profile, looking at a monitor showing a structured billing grid — simple rows and a small bar chart. A second physician in a white coat stands nearby in the background, glancing at the screen. The figures are positioned to the right of the frame with generous open negative space on the left. Minimal clinical office setting — a subtle doorway or wall panel visible in background. Style: Swiss editorial flat illustration, warm off-white and cream palette, muted ink outlines, minimal color fills (slate, cream only — no orange, no yellow), no gradients, no texture. Professional academic tone. No text in the image.
```

**Panel 2 — Waiting Room Comics** (`slide6_panel2_test.png`)
```
Clean flat editorial illustration. A patient in casual clothing sits in a waiting room chair, holding and reading a small comic booklet — the comic cover clearly shows the title 'First Neurology Visit' with a simple illustrated figure on the cover. A second patient sits nearby also waiting, glancing over. Minimal waiting room setting — subtle wall, window, and a plant in background. Style: Swiss editorial flat illustration, warm off-white and cream palette, muted ink outlines, minimal color fills (slate, cream only — no orange, no yellow), no gradients, no texture. Professional academic tone. Only text allowed is 'First Neurology Visit' on the comic cover.
```

**Panel 3 — LLM Semantic Analysis** (`slide6_panel3_test.png`)
```
Clean flat editorial illustration. A small diverse group of physicians in white coats stands around a conference table in discussion — including one Asian physician and one Black physician clearly visible among the group. One physician gestures toward a large wall-mounted screen showing a sagittal brain MRI cross-section. To the side of the screen, an EEG trace panel shows horizontal waveform lines. Floating above the group in the air, abstract speech-to-text visualization — soft radiating sound waves or floating text fragments representing spoken words being transcribed, conveying the idea of a recorded multidisciplinary discussion. The overall scene feels like a working clinical conference being captured. Style: Swiss editorial flat illustration, warm off-white and cream palette, muted ink outlines, minimal color fills (slate, cream only — no orange, no yellow), no gradients, no texture. Professional academic tone. No readable text in the image.
```
