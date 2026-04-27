---
type: resource
scope: visual_style_guide
created: 2026-04-22
updated: 2026-04-22
source: "User-curated reference set in illustration-production/assets/style-guide/"
---

# OpenAI Image 2 Reference Style Guide

Reference set supplied by user and described as images from the OpenAI website introducing Image 2.0 / GPT Image 2.

## Source Set
- `assets/style-guide/ChatGPT_Image_Apr_20__2026__09_39_01_PM__1_.png.webp`
- `assets/style-guide/gpt_img__1___1_.png.webp`
- `assets/style-guide/images-2-design-trends.png.webp`
- `assets/style-guide/images-2-indie-comic.png.webp`
- `assets/style-guide/images-2-japanese-charicature.png.webp`
- `assets/style-guide/images-2-miami-comic.png.webp`
- `assets/style-guide/images-2-storybook.png.webp`

## What The Style Actually Is
The shared signature is not one fixed aesthetic. It is a controlled art direction system:

- tactile and analog rather than slick
- simple, readable compositions with one clear idea
- emotionally legible scenes and silhouettes
- restrained palettes with 1-2 accent colors
- generous negative space
- subtle paper grain, print wear, watercolor bloom, or halftone texture
- typography and layout treated as part of the composition
- polished enough for brand/editorial use, but never cold or sterile

## Repeating Visual Moves

### 1. Editorial restraint
Images feel designed, not merely rendered. They avoid clutter, over-detail, and noisy backgrounds.

### 2. Analog warmth
Even digital-looking compositions are softened by paper texture, grain, torn edges, worn ink, watercolor bleed, or vintage print imperfections.

### 3. Narrative clarity
Every image communicates a single concept fast. Comics are easy to read. Infographics have strict hierarchy. Storybook pieces center on one emotional path.

### 4. Intentional asymmetry
Layouts often use uneven crops, offset subjects, or strong vertical/horizontal flow, but still feel balanced.

### 5. Controlled color
Most pieces use soft neutrals plus a tight accent family:
- lavender / cobalt / periwinkle
- dusty coral / salmon / peach
- moss / olive / sage
- cream / off-white / sand
- black ink or charcoal for structure

### 6. Humanized finish
Faces, props, and environments are stylized enough to feel authored. Nothing feels like generic stock illustration.

## Practical Prompt Ingredients
These ingredients recur across the set and are worth reusing:

- medium cues: `editorial illustration`, `vintage comic`, `storybook watercolor`, `art-directed moodboard`, `print poster`, `paper collage`
- texture cues: `off-white paper`, `subtle grain`, `halftone`, `inked outlines`, `soft watercolor edges`, `light print wear`
- composition cues: `clear focal point`, `generous margins`, `modular grid`, `clean paneling`, `single winding path`, `large headline integrated into the scene`
- lighting cues: `soft daylight`, `diffuse ambient light`, `gentle shadows`, `matte surfaces`
- finish cues: `tasteful`, `brand-ready`, `designed not decorative`, `precise but warm`

## Reusable House Prefix
Use this at the start of future prompts when you want the same general discipline:

`Art-directed editorial image with tactile analog texture, restrained palette, generous negative space, clear hierarchy, subtle paper grain, warm humanized finish, and composition that feels designed rather than generic AI glossy.`

## Selection Protocol
When a future request asks for a website, visualization, presentation graphic, comic, poster, or other image-driven artifact, use this flow:

1. Classify the task:
   - website / UI surface
   - visualization / infographic
   - editorial illustration
   - comic / narrative sequence
   - moodboard / brand direction
2. Review the reference set in this folder before choosing a direction.
3. Pick the single best-fit reference or sub-style instead of blending everything together by default.
4. State the chosen direction briefly and why it fits the task.
5. Apply the style at the right layer:
   - code-only layout, typography, spacing, palette, and texture treatment for websites or HTML/CSS visualizations
   - generated raster artwork only when the deliverable needs custom illustrations, posters, mascots, scenes, or other non-code-native imagery
6. If image generation is needed, use the selected reference as the art-direction brief and pass that into the relevant image-generation workflow rather than prompting from scratch.
7. Keep outputs disciplined:
   - one dominant compositional move
   - one restrained palette family
   - one material story
   - no generic glossy AI finish

## Task-To-Style Routing
- website landing page or product page
  Usually start from `gpt_img__1___1_.png.webp` or `images-2-design-trends.png.webp`.
  Use moodboard/editorial layout language first; generate images only if the page needs bespoke art.
- infographic, framework, or visual summary
  Usually start from `images-2-design-trends.png.webp`.
  Favor modular grids, boxed hierarchy, shape-driven layout, and restrained accents.
- human-centered explainer or empathy-forward storytelling
  Usually start from `images-2-indie-comic.png.webp`.
  Favor warm environments, intimate scenes, and hand-inked comic clarity.
- travel, place, destination, or upbeat journey story
  Usually start from `images-2-miami-comic.png.webp`.
  Favor pastel print texture, sun-faded optimism, and retro travel energy.
- milestone path, learning ladder, patient journey, or reflective growth visual
  Usually start from `images-2-storybook.png.webp`.
  Favor whitespace, tiny vignettes, and path-based sequencing.
- team lineup, role comparison, or light humorous relational graphic
  Usually start from `images-2-japanese-charicature.png.webp`.
  Favor sparse staging and caricature through proportion.
- mascot-led educational page, playful poster, or children’s comic
  Usually start from `ChatGPT_Image_Apr_20__2026__09_39_01_PM__1_.png.webp`.
  Favor bold headline integration, strong panel readability, and charming retro energy.

## Reference Map
- `images-2-design-trends.png.webp`
  Core lesson: editorial layout discipline, modular hierarchy, texture used as accent rather than noise.
- `images-2-indie-comic.png.webp`
  Core lesson: intimate slice-of-life storytelling, warm environment detail, emotionally natural dialogue.
- `images-2-miami-comic.png.webp`
  Core lesson: retro travel-comic tone, sun-faded palette, vintage print charm.
- `images-2-storybook.png.webp`
  Core lesson: extreme restraint, tiny figures, poetic whitespace, path-based composition.
- `images-2-japanese-charicature.png.webp`
  Core lesson: minimal caricature, sparse staging, humor through proportion rather than detail.
- `gpt_img__1___1_.png.webp`
  Core lesson: art-directed brand moodboard, premium print objects, tactile launch-world building.
- `ChatGPT_Image_Apr_20__2026__09_39_01_PM__1_.png.webp`
  Core lesson: bold headline-led children’s adventure comic with strong mascot readability.

## Reusable Prompt Recipes

### 1. Analog + AI Editorial Collage
Use for concept covers, explainers, or AI x human craft themes.

`Art-directed editorial collage poster about [topic], handmade paper scraps, torn edges, rough pencil marks, photocopy texture, halftone portrait fragments, one intelligent accent color, off-white paper background, clean title hierarchy, analog craft meets modern AI polish, sophisticated magazine layout, restrained and brand-ready.`

### 2. Shape-Driven Design Board
Use for trend reports, strategic frameworks, or visual taxonomies.

`Editorial infographic poster about [topic], modular grid of boxed sections, bold geometric shapes, minimal icons, generous white space, crisp sans-serif and elegant serif pairing, soft neutral background with cobalt and sand accents, subtle paper grain, each panel communicating one idea clearly, clean but tactile design-system feel.`

### 3. Warm Indie Neighborhood Comic
Use for human scenes, lifestyle storytelling, medical empathy, community narratives.

`Slice-of-life indie comic page set in [setting], warm neighborhood atmosphere, expressive hand-inked linework, muted earth palette with soft teal and ochre accents, detailed but cozy environment, emotionally legible faces, natural dialogue balloons, subtle paper texture, sunlight filtered through trees, intimate and thoughtful rather than flashy.`

### 4. Retro Pastel Travel Comic
Use for place-based storytelling, city guides, journey narratives, destination explainers.

`Mid-century travel comic page about [place], faded pastel palette, weathered newsprint texture, clean comic panels, cheerful retro lettering, sun-washed atmosphere, simplified architecture and landmarks, vintage print imperfections, airy beach-town optimism, charming and collectible like an old illustrated travel pamphlet.`

### 5. Minimal Whimsical Storybook Path
Use for growth journeys, learning ladders, patient education, milestone maps.

`Vertical storybook illustration on a mostly white page, a winding path connecting small magical scenes about [journey], tiny watercolor characters and objects spaced far apart, handwritten text, gentle ink outlines, lots of breathing room, soft fairy-tale colors, emotionally encouraging, delicate and uncluttered, like a modern children’s book with poetic restraint.`

### 6. Minimal Character Caricature Strip
Use for team diagrams, role comparisons, light humor, group dynamics.

`Minimal caricature lineup of [group], simple white background, thin clean outlines, elongated proportions, understated expression, small stylized clothing details, gentle humor, Japanese editorial caricature feel, sparse composition, flat soft colors, very clean and readable with no extra scenery.`

### 7. Art-Directed Product Moodboard Spread
Use for launch decks, brand exploration, vision boards, creative direction.

`Luxury editorial moodboard spread for [product or brand], photographed printed materials pinned or arranged on a clean wall and shelf, monochrome and warm-neutral palette, one hero image, elegant serif typography, premium stationery mockups, quiet lighting, tactile paper stocks, understated sticky notes and reference cards, highly curated creative-director desk aesthetic.`

### 8. Vintage Adventure Comic For Children
Use for playful explainers, mascot storytelling, travel or science adventures.

`Vintage children’s adventure comic cover and page about [topic], lovable mascot characters, bold retro headline, saturated primary accents over warm paper tones, classic comic panel borders, expressive speech balloons, detailed props and scenery, slightly worn print texture, optimistic and kinetic but still clean and readable.`

## Style Control Knobs
When adapting these prompts, tune these variables explicitly:

- `density`: sparse / moderate / richly detailed
- `texture`: watercolor / grain / halftone / collage / aged print
- `palette`: warm earth / pastel coastal / editorial monochrome / lavender-tech
- `era`: contemporary editorial / mid-century / vintage children’s comic
- `typography integration`: none / subtle labels / headline-led / full poster hierarchy
- `emotional temperature`: calm / cozy / playful / optimistic / reflective

## Avoid List
If a result drifts, add these constraints:

- no glossy CGI surfaces
- no oversaturated neon cyberpunk palette
- no busy background clutter
- no generic stock-photo realism
- no over-rendered facial detail
- no random UI chrome unless compositionally justified
- no hyper-dramatic cinematic lighting
- no excessive lens flare or bokeh
- no soulless flat vector corporate illustration

## Fast Prompt Shortcuts

### Editorial Warmth
`restrained palette, off-white paper, subtle grain, elegant hierarchy, tactile analog finish`

### Human Comic Warmth
`slice-of-life comic, muted colors, expressive ink lines, cozy sunlight, intimate emotional clarity`

### Retro Print Energy
`aged newsprint, bold headline, worn comic borders, faded pastel inks, playful vintage optimism`

### Sparse Storybook Wonder
`tiny watercolor figures, large white space, handwritten text, winding path, gentle magical realism`

## Bottom Line
The strongest lesson from this reference set is not the subject matter. It is the discipline:

- one idea per image
- one dominant compositional gesture
- one restrained palette family
- one tactile material story

That combination is what makes the images feel authored, premium, and memorable.
