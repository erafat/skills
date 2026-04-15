---
name: frontend-slides
description: Create stunning, animation-rich HTML presentations from scratch or by converting PowerPoint files. Use when the user wants to build a presentation, convert a PPT/PPTX to web, or create slides for a talk/pitch. Helps non-designers discover their aesthetic through visual exploration rather than abstract choices.
---

# Frontend Slides Skill

Create zero-dependency, animation-rich HTML presentations that run entirely in the browser. This skill helps non-designers discover their preferred aesthetic through visual exploration ("show, don't tell"), then generates production-quality slide decks.

## Core Philosophy

1. **Zero Dependencies** — Single HTML files with inline CSS/JS. No npm, no build tools.
2. **Show, Don't Tell** — People don't know what they want until they see it. Generate visual previews, not abstract choices.
3. **Distinctive Design** — Avoid generic "AI slop" aesthetics. Every presentation should feel custom-crafted.
4. **Production Quality** — Code should be well-commented, accessible, and performant.
5. **Viewport Fitting (CRITICAL)** — Every slide MUST fit exactly within the viewport. No scrolling within slides, ever. This is non-negotiable.

---

## CRITICAL: Viewport Fitting Requirements

**This section is mandatory for ALL presentations. Every slide must be fully visible without scrolling on any screen size.**

### The Golden Rule

```
Each slide = exactly one viewport height (100vh/100dvh)
Content overflows? → Split into multiple slides or reduce content
Never scroll within a slide.
```

### Content Density Limits

To guarantee viewport fitting, enforce these limits per slide:

| Slide Type | Maximum Content |
|------------|-----------------|
| Title slide | 1 heading + 1 subtitle + optional tagline |
| Content slide | 1 heading + 4-6 bullet points OR 1 heading + 2 paragraphs |
| Feature grid | 1 heading + 6 cards maximum (2x3 or 3x2 grid) |
| Code slide | 1 heading + 8-10 lines of code maximum |
| Quote slide | 1 quote (max 3 lines) + attribution |
| Image slide | 1 heading + 1 image (max 60vh height) |

**If content exceeds these limits → Split into multiple slides**

### Required CSS Architecture

Every presentation MUST include this base CSS for viewport fitting:

```css
/* ===========================================
   VIEWPORT FITTING: MANDATORY BASE STYLES
   These styles MUST be included in every presentation.
   They ensure slides fit exactly in the viewport.
   =========================================== */

/* 1. Lock html/body to viewport */
html, body {
    height: 100%;
    overflow-x: hidden;
}

html {
    scroll-snap-type: y mandatory;
    scroll-behavior: smooth;
}

/* 2. Each slide = exact viewport height */
.slide {
    width: 100vw;
    height: 100vh;
    height: 100dvh; /* Dynamic viewport height for mobile browsers */
    overflow: hidden; /* CRITICAL: Prevent ANY overflow */
    scroll-snap-align: start;
    display: flex;
    flex-direction: column;
    position: relative;
}

/* 3. Content container with flex for centering */
.slide-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    max-height: 100%;
    overflow: hidden; /* Double-protection against overflow */
    padding: var(--slide-padding);
}

/* 4. ALL typography uses clamp() for responsive scaling */
:root {
    /* Titles scale from mobile to desktop */
    --title-size: clamp(1.5rem, 5vw, 4rem);
    --h2-size: clamp(1.25rem, 3.5vw, 2.5rem);
    --h3-size: clamp(1rem, 2.5vw, 1.75rem);

    /* Body text */
    --body-size: clamp(0.75rem, 1.5vw, 1.125rem);
    --small-size: clamp(0.65rem, 1vw, 0.875rem);

    /* Spacing scales with viewport */
    --slide-padding: clamp(1rem, 4vw, 4rem);
    --content-gap: clamp(0.5rem, 2vw, 2rem);
    --element-gap: clamp(0.25rem, 1vw, 1rem);
}

/* 5. Cards/containers use viewport-relative max sizes */
.card, .container, .content-box {
    max-width: min(90vw, 1000px);
    max-height: min(80vh, 700px);
}

/* 6. Lists auto-scale with viewport */
.feature-list, .bullet-list {
    gap: clamp(0.4rem, 1vh, 1rem);
}

.feature-list li, .bullet-list li {
    font-size: var(--body-size);
    line-height: 1.4;
}

/* 7. Grids adapt to available space */
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(min(100%, 250px), 1fr));
    gap: clamp(0.5rem, 1.5vw, 1rem);
}

/* 8. Images constrained to viewport */
img, .image-container {
    max-width: 100%;
    max-height: min(50vh, 400px);
    object-fit: contain;
}

/* ===========================================
   RESPONSIVE BREAKPOINTS
   Aggressive scaling for smaller viewports
   =========================================== */

/* Short viewports (< 700px height) */
@media (max-height: 700px) {
    :root {
        --slide-padding: clamp(0.75rem, 3vw, 2rem);
        --content-gap: clamp(0.4rem, 1.5vw, 1rem);
        --title-size: clamp(1.25rem, 4.5vw, 2.5rem);
        --h2-size: clamp(1rem, 3vw, 1.75rem);
    }
}

/* Very short viewports (< 600px height) */
@media (max-height: 600px) {
    :root {
        --slide-padding: clamp(0.5rem, 2.5vw, 1.5rem);
        --content-gap: clamp(0.3rem, 1vw, 0.75rem);
        --title-size: clamp(1.1rem, 4vw, 2rem);
        --body-size: clamp(0.7rem, 1.2vw, 0.95rem);
    }

    /* Hide non-essential elements */
    .nav-dots, .keyboard-hint, .decorative {
        display: none;
    }
}

/* Extremely short (landscape phones, < 500px height) */
@media (max-height: 500px) {
    :root {
        --slide-padding: clamp(0.4rem, 2vw, 1rem);
        --title-size: clamp(1rem, 3.5vw, 1.5rem);
        --h2-size: clamp(0.9rem, 2.5vw, 1.25rem);
        --body-size: clamp(0.65rem, 1vw, 0.85rem);
    }
}

/* Narrow viewports (< 600px width) */
@media (max-width: 600px) {
    :root {
        --title-size: clamp(1.25rem, 7vw, 2.5rem);
    }

    /* Stack grids vertically */
    .grid {
        grid-template-columns: 1fr;
    }
}

/* ===========================================
   REDUCED MOTION
   Respect user preferences
   =========================================== */
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.2s !important;
    }

    html {
        scroll-behavior: auto;
    }
}
```

### Overflow Prevention Checklist

Before generating any presentation, mentally verify:

1. ✅ Every `.slide` has `height: 100vh; height: 100dvh; overflow: hidden;`
2. ✅ All font sizes use `clamp(min, preferred, max)`
3. ✅ All spacing uses `clamp()` or viewport units
4. ✅ Content containers have `max-height` constraints
5. ✅ Images have `max-height: min(50vh, 400px)` or similar
6. ✅ Grids use `auto-fit` with `minmax()` for responsive columns
7. ✅ Breakpoints exist for heights: 700px, 600px, 500px
8. ✅ No fixed pixel heights on content elements
9. ✅ Content per slide respects density limits

### When Content Doesn't Fit

If you find yourself with too much content:

**DO:**
- Split into multiple slides
- Reduce bullet points (max 5-6 per slide)
- Shorten text (aim for 1-2 lines per bullet)
- Use smaller code snippets
- Create a "continued" slide

**DON'T:**
- Reduce font size below readable limits
- Remove padding/spacing entirely
- Allow any scrolling
- Cram content to fit

### Testing Viewport Fit

After generating, recommend the user test at these sizes:
- Desktop: 1920×1080, 1440×900, 1280×720
- Tablet: 1024×768, 768×1024 (portrait)
- Mobile: 375×667, 414×896
- Landscape phone: 667×375, 896×414

---

## Phase 0: Detect Mode

First, determine what the user wants:

**Mode A: New Presentation**
- User wants to create slides from scratch
- Proceed to Phase 1 (Content Discovery)

**Mode B: PPT Conversion**
- User has a PowerPoint file (.ppt, .pptx) to convert
- Proceed to Phase 4 (PPT Extraction)

**Mode C: Existing Presentation Enhancement**
- User has an HTML presentation and wants to improve it
- Read the existing file, understand the structure, then enhance

---

## Phase 1: Content Discovery (New Presentations)

Before designing, understand the content. Ask via AskUserQuestion:

### Step 1.1: Presentation Context

**Question 1: Purpose**
- Header: "Purpose"
- Question: "What is this presentation for?"
- Options:
  - "Pitch deck" — Selling an idea, product, or company to investors/clients
  - "Teaching/Tutorial" — Explaining concepts, how-to guides, educational content
  - "Conference talk" — Speaking at an event, tech talk, keynote
  - "Internal presentation" — Team updates, strategy meetings, company updates

**Question 2: Slide Count**
- Header: "Length"
- Question: "Approximately how many slides?"
- Options:
  - "Short (5-10)" — Quick pitch, lightning talk
  - "Medium (10-20)" — Standard presentation
  - "Long (20+)" — Deep dive, comprehensive talk

**Question 3: Content**
- Header: "Content"
- Question: "Do you have the content ready, or do you need help structuring it?"
- Options:
  - "I have all content ready" — Just need to design the presentation
  - "I have rough notes" — Need help organizing into slides
  - "I have a topic only" — Need help creating the full outline

If user has content, ask them to share it (text, bullet points, images, etc.).

---

## Phase 2: Style Discovery (Visual Exploration)

**CRITICAL: This is the "show, don't tell" phase.**

Most people can't articulate design preferences in words. Instead of asking "do you want minimalist or bold?", we generate mini-previews and let them react.

### How Users Choose Presets

Users can select a style in **two ways**:

**Option A: Guided Discovery (Default)**
- User answers mood questions
- Skill generates 3 preview files based on their answers
- User views previews in browser and picks their favorite
- This is best for users who don't have a specific style in mind

**Option B: Direct Selection**
- If user already knows what they want, they can request a preset by name
- Example: "Use the Bold Signal style" or "I want something like Dark Botanical"
- Skip to Phase 3 immediately

**Available Presets:**
| Preset | Vibe | Best For |
|--------|------|----------|
| Bold Signal | Confident, high-impact | Pitch decks, keynotes |
| Electric Studio | Clean, professional | Agency presentations |
| Creative Voltage | Energetic, retro-modern | Creative pitches |
| Dark Botanical | Elegant, sophisticated | Premium brands |
| Notebook Tabs | Editorial, organized | Reports, reviews |
| Pastel Geometry | Friendly, approachable | Product overviews |
| Split Pastel | Playful, modern | Creative agencies |
| Vintage Editorial | Witty, personality-driven | Personal brands |
| Neon Cyber | Futuristic, techy | Tech startups |
| Terminal Green | Developer-focused | Dev tools, APIs |
| Swiss Modern | Minimal, precise | Corporate, data, medical talks |
| Paper & Ink | Literary, thoughtful | Storytelling |

### Step 2.0: Style Path Selection

First, ask how the user wants to choose their style:

**Question: Style Selection Method**
- Header: "Style"
- Question: "How would you like to choose your presentation style?"
- Options:
  - "Show me options" — Generate 3 previews based on my needs (recommended for most users)
  - "I know what I want" — Let me pick from the preset list directly

**If "Show me options"** → Continue to Step 2.1 (Mood Selection)

**If "I know what I want"** → Show preset picker:

**Question: Pick a Preset**
- Header: "Preset"
- Question: "Which style would you like to use?"
- Options:
  - "Bold Signal" — Vibrant card on dark, confident and high-impact
  - "Dark Botanical" — Elegant dark with soft abstract shapes
  - "Notebook Tabs" — Editorial paper look with colorful section tabs
  - "Pastel Geometry" — Friendly pastels with decorative pills

(If user picks one, skip to Phase 3. If they want to see more options, show additional presets or proceed to guided discovery.)

### Step 2.1: Mood Selection (Guided Discovery)

**Question 1: Feeling**
- Header: "Vibe"
- Question: "What feeling should the audience have when viewing your slides?"
- Options:
  - "Impressed/Confident" — Professional, trustworthy, this team knows what they're doing
  - "Excited/Energized" — Innovative, bold, this is the future
  - "Calm/Focused" — Clear, thoughtful, easy to follow
  - "Inspired/Moved" — Emotional, storytelling, memorable
- multiSelect: true (can choose up to 2)

### Step 2.2: Generate Style Previews

Based on their mood selection, generate **3 distinct style previews** as mini HTML files in a temporary directory. Each preview should be a single title slide showing:

- Typography (font choices, heading/body hierarchy)
- Color palette (background, accent, text colors)
- Animation style (how elements enter)
- Overall aesthetic feel

**Preview Styles to Consider (pick 3 based on mood):**

| Mood | Style Options |
|------|---------------|
| Impressed/Confident | "Bold Signal", "Electric Studio", "Dark Botanical" |
| Excited/Energized | "Creative Voltage", "Neon Cyber", "Split Pastel" |
| Calm/Focused | "Notebook Tabs", "Paper & Ink", "Swiss Modern" |
| Inspired/Moved | "Dark Botanical", "Vintage Editorial", "Pastel Geometry" |

**IMPORTANT: Never use these generic patterns:**
- Purple gradients on white backgrounds
- Inter, Roboto, or system fonts
- Standard blue primary colors
- Predictable hero layouts

**Instead, use distinctive choices:**
- Unique font pairings (Clash Display, Satoshi, Cormorant Garamond, DM Sans, etc.)
- Cohesive color themes with personality
- Atmospheric backgrounds (gradients, subtle patterns, depth)
- Signature animation moments

### Step 2.3: Present Previews

Create the previews in: `.claude-design/slide-previews/`

```
.claude-design/slide-previews/
├── style-a.html   # First style option
├── style-b.html   # Second style option
├── style-c.html   # Third style option
└── assets/        # Any shared assets
```

Each preview file should be:
- Self-contained (inline CSS/JS)
- A single "title slide" showing the aesthetic
- Animated to demonstrate motion style
- ~50-100 lines, not a full presentation

Present to user:
```
I've created 3 style previews for you to compare:

**Style A: [Name]** — [1 sentence description]
**Style B: [Name]** — [1 sentence description]
**Style C: [Name]** — [1 sentence description]

Open each file to see them in action:
- .claude-design/slide-previews/style-a.html
- .claude-design/slide-previews/style-b.html
- .claude-design/slide-previews/style-c.html

Take a look and tell me:
1. Which style resonates most?
2. What do you like about it?
3. Anything you'd change?
```

Then use AskUserQuestion:

**Question: Pick Your Style**
- Header: "Style"
- Question: "Which style preview do you prefer?"
- Options:
  - "Style A: [Name]" — [Brief description]
  - "Style B: [Name]" — [Brief description]
  - "Style C: [Name]" — [Brief description]
  - "Mix elements" — Combine aspects from different styles

If "Mix elements", ask for specifics.

---

## Phase 3: Generate Presentation

Now generate the full presentation based on:
- Content from Phase 1
- Style from Phase 2

### File Structure

For single presentations:
```
presentation.html    # Self-contained presentation
assets/              # Images, if any
```

For projects with multiple presentations:
```
[presentation-name].html
[presentation-name]-assets/
```

### HTML Architecture

Follow this structure for all presentations:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Presentation Title</title>

    <!-- Fonts (use Fontshare or Google Fonts) -->
    <link rel="stylesheet" href="https://api.fontshare.com/v2/css?f[]=...">

    <style>
        /* ===========================================
           CSS CUSTOM PROPERTIES (THEME)
           Easy to modify: change these to change the whole look
           =========================================== */
        :root {
            /* Colors */
            --bg-primary: #0a0f1c;
            --bg-secondary: #111827;
            --text-primary: #ffffff;
            --text-secondary: #9ca3af;
            --accent: #00ffcc;
            --accent-glow: rgba(0, 255, 204, 0.3);

            /* Typography - MUST use clamp() for responsive scaling */
            --font-display: 'Clash Display', sans-serif;
            --font-body: 'Satoshi', sans-serif;
            --title-size: clamp(2rem, 6vw, 5rem);
            --subtitle-size: clamp(0.875rem, 2vw, 1.25rem);
            --body-size: clamp(0.75rem, 1.2vw, 1rem);

            /* Spacing - MUST use clamp() for responsive scaling */
            --slide-padding: clamp(1.5rem, 4vw, 4rem);
            --content-gap: clamp(1rem, 2vw, 2rem);

            /* Animation */
            --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
            --duration-normal: 0.6s;
        }

        /* ===========================================
           BASE STYLES
           =========================================== */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        html {
            scroll-behavior: smooth;
            scroll-snap-type: y mandatory;
            height: 100%;
        }

        body {
            font-family: var(--font-body);
            background: var(--bg-primary);
            color: var(--text-primary);
            overflow-x: hidden;
            height: 100%;
        }

        /* ===========================================
           SLIDE CONTAINER
           CRITICAL: Each slide MUST fit exactly in viewport
           - Use height: 100vh (NOT min-height)
           - Use overflow: hidden to prevent scroll
           - Content must scale with clamp() values
           =========================================== */
        .slide {
            width: 100vw;
            height: 100vh; /* EXACT viewport height - no scrolling */
            height: 100dvh; /* Dynamic viewport height for mobile */
            padding: var(--slide-padding);
            scroll-snap-align: start;
            display: flex;
            flex-direction: column;
            justify-content: center;
            position: relative;
            overflow: hidden; /* Prevent any content overflow */
        }

        /* Content wrapper that prevents overflow */
        .slide-content {
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            max-height: 100%;
            overflow: hidden;
        }

        /* ===========================================
           RESPONSIVE BREAKPOINTS
           Adjust content for different screen sizes
           =========================================== */
        @media (max-height: 600px) {
            :root {
                --slide-padding: clamp(1rem, 3vw, 2rem);
                --content-gap: clamp(0.5rem, 1.5vw, 1rem);
            }
        }

        @media (max-width: 768px) {
            :root {
                --title-size: clamp(1.5rem, 8vw, 3rem);
            }
        }

        @media (max-height: 500px) and (orientation: landscape) {
            /* Extra compact for landscape phones */
            :root {
                --title-size: clamp(1.25rem, 5vw, 2rem);
                --slide-padding: clamp(0.75rem, 2vw, 1.5rem);
            }
        }

        /* ===========================================
           ANIMATIONS
           Trigger via .visible class (added by JS on scroll)
           =========================================== */
        .reveal {
            opacity: 0;
            transform: translateY(30px);
            transition: opacity var(--duration-normal) var(--ease-out-expo),
                        transform var(--duration-normal) var(--ease-out-expo);
        }

        .slide.visible .reveal {
            opacity: 1;
            transform: translateY(0);
        }

        /* Stagger children */
        .reveal:nth-child(1) { transition-delay: 0.1s; }
        .reveal:nth-child(2) { transition-delay: 0.2s; }
        .reveal:nth-child(3) { transition-delay: 0.3s; }
        .reveal:nth-child(4) { transition-delay: 0.4s; }

        /* ... more styles ... */
    </style>
</head>
<body>
    <!-- Progress bar (optional) -->
    <div class="progress-bar"></div>

    <!-- Navigation dots (optional) -->
    <nav class="nav-dots">
        <!-- Generated by JS -->
    </nav>

    <!-- Slides -->
    <section class="slide title-slide">
        <h1 class="reveal">Presentation Title</h1>
        <p class="reveal">Subtitle or author</p>
    </section>

    <section class="slide">
        <h2 class="reveal">Slide Title</h2>
        <p class="reveal">Content...</p>
    </section>

    <!-- More slides... -->

    <script>
        /* ===========================================
           SLIDE PRESENTATION CONTROLLER
           Handles navigation, animations, and interactions
           =========================================== */

        class SlidePresentation {
            constructor() {
                // ... initialization
            }

            // ... methods
        }

        // Initialize
        new SlidePresentation();
    </script>
</body>
</html>
```

### Required JavaScript Features

Every presentation should include:

1. **SlidePresentation Class** — Main controller
   - Keyboard navigation (arrows, space)
   - Touch/swipe support
   - Mouse wheel navigation
   - Progress bar updates
   - Navigation dots

2. **Intersection Observer** — For scroll-triggered animations
   - Add `.visible` class when slides enter viewport
   - Trigger CSS animations efficiently

3. **Optional Enhancements** (based on style):
   - Custom cursor with trail
   - Particle system background (canvas)
   - Parallax effects
   - 3D tilt on hover
   - Magnetic buttons
   - Counter animations

### Code Quality Requirements

**Comments:**
Every section should have clear comments explaining:
- What it does
- Why it exists
- How to modify it

```javascript
/* ===========================================
   CUSTOM CURSOR
   Creates a stylized cursor that follows mouse with a trail effect.
   - Uses lerp (linear interpolation) for smooth movement
   - Grows larger when hovering over interactive elements
   =========================================== */
class CustomCursor {
    constructor() {
        // ...
    }
}
```

**Accessibility:**
- Semantic HTML (`<section>`, `<nav>`, `<main>`)
- Keyboard navigation works
- ARIA labels where needed
- Reduced motion support

```css
@media (prefers-reduced-motion: reduce) {
    .reveal {
        transition: opacity 0.3s ease;
        transform: none;
    }
}
```

**CSS Function Negation:**
- Never negate CSS functions directly — `-clamp()`, `-min()`, `-max()` are silently ignored by browsers with no console error
- Always use `calc(-1 * clamp(...))` instead. See STYLE_PRESETS.md → "CSS Gotchas" for details.

**Responsive & Viewport Fitting (CRITICAL):**

**See the "CRITICAL: Viewport Fitting Requirements" section above for complete CSS and guidelines.**

Quick reference:
- Every `.slide` must have `height: 100vh; height: 100dvh; overflow: hidden;`
- All typography and spacing must use `clamp()`
- Respect content density limits (max 4-6 bullets, max 6 cards, etc.)
- Include breakpoints for heights: 700px, 600px, 500px
- When content doesn't fit → split into multiple slides, never scroll

---

## Phase 4: PPT Conversion

When converting PowerPoint files:

### Step 4.1: Extract Content

Use Python with `python-pptx` to extract:

```python
from pptx import Presentation
from pptx.util import Inches, Pt
import json
import os
import base64

def extract_pptx(file_path, output_dir):
    """
    Extract all content from a PowerPoint file.
    Returns a JSON structure with slides, text, and images.
    """
    prs = Presentation(file_path)
    slides_data = []

    # Create assets directory
    assets_dir = os.path.join(output_dir, 'assets')
    os.makedirs(assets_dir, exist_ok=True)

    for slide_num, slide in enumerate(prs.slides):
        slide_data = {
            'number': slide_num + 1,
            'title': '',
            'content': [],
            'images': [],
            'notes': ''
        }

        for shape in slide.shapes:
            # Extract title
            if shape.has_text_frame:
                if shape == slide.shapes.title:
                    slide_data['title'] = shape.text
                else:
                    slide_data['content'].append({
                        'type': 'text',
                        'content': shape.text
                    })

            # Extract images
            if shape.shape_type == 13:  # Picture
                image = shape.image
                image_bytes = image.blob
                image_ext = image.ext
                image_name = f"slide{slide_num + 1}_img{len(slide_data['images']) + 1}.{image_ext}"
                image_path = os.path.join(assets_dir, image_name)

                with open(image_path, 'wb') as f:
                    f.write(image_bytes)

                slide_data['images'].append({
                    'path': f"assets/{image_name}",
                    'width': shape.width,
                    'height': shape.height
                })

        # Extract notes
        if slide.has_notes_slide:
            notes_frame = slide.notes_slide.notes_text_frame
            slide_data['notes'] = notes_frame.text

        slides_data.append(slide_data)

    return slides_data
```

### Step 4.2: Confirm Content Structure

Present the extracted content to the user:

```
I've extracted the following from your PowerPoint:

**Slide 1: [Title]**
- [Content summary]
- Images: [count]

**Slide 2: [Title]**
- [Content summary]
- Images: [count]

...

All images have been saved to the assets folder.

Does this look correct? Should I proceed with style selection?
```

### Step 4.3: Style Selection

Proceed to Phase 2 (Style Discovery) with the extracted content in mind.

### Step 4.4: Generate HTML

Convert the extracted content into the chosen style, preserving:
- All text content
- All images (referenced from assets folder)
- Slide order
- Any speaker notes (as HTML comments or separate file)

---

## Phase 5: Delivery

### Final Output

When the presentation is complete:

1. **Clean up temporary files**
   - Delete `.claude-design/slide-previews/` if it exists

2. **Open the presentation**
   - Use `open [filename].html` to launch in browser

3. **Provide summary**
```
Your presentation is ready!

📁 File: [filename].html
🎨 Style: [Style Name]
📊 Slides: [count]

**Navigation:**
- Arrow keys (← →) or Space to navigate
- Scroll/swipe also works
- Click the dots on the right to jump to a slide

**To customize:**
- Colors: Look for `:root` CSS variables at the top
- Fonts: Change the Fontshare/Google Fonts link
- Animations: Modify `.reveal` class timings

Would you like me to make any adjustments?
```

---

## Style Reference: Effect → Feeling Mapping

Use this guide to match animations to intended feelings:

### Dramatic / Cinematic
- Slow fade-ins (1-1.5s)
- Large scale transitions (0.9 → 1)
- Dark backgrounds with spotlight effects
- Parallax scrolling
- Full-bleed images

### Techy / Futuristic
- Neon glow effects (box-shadow with accent color)
- Particle systems (canvas background)
- Grid patterns
- Monospace fonts for accents
- Glitch or scramble text effects
- Cyan, magenta, electric blue palette

### Playful / Friendly
- Bouncy easing (spring physics)
- Rounded corners (large radius)
- Pastel or bright colors
- Floating/bobbing animations
- Hand-drawn or illustrated elements

### Professional / Corporate
- Subtle, fast animations (200-300ms)
- Clean sans-serif fonts
- Navy, slate, or charcoal backgrounds
- Precise spacing and alignment
- Minimal decorative elements
- Data visualization focus

### Calm / Minimal
- Very slow, subtle motion
- High whitespace
- Muted color palette
- Serif typography
- Generous padding
- Content-focused, no distractions

### Editorial / Magazine
- Strong typography hierarchy
- Pull quotes and callouts
- Image-text interplay
- Grid-breaking layouts
- Serif headlines, sans-serif body
- Black and white with one accent

---

## Animation Patterns Reference

### Entrance Animations

```css
/* Fade + Slide Up (most common) */
.reveal {
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.6s var(--ease-out-expo),
                transform 0.6s var(--ease-out-expo);
}

.visible .reveal {
    opacity: 1;
    transform: translateY(0);
}

/* Scale In */
.reveal-scale {
    opacity: 0;
    transform: scale(0.9);
    transition: opacity 0.6s, transform 0.6s var(--ease-out-expo);
}

/* Slide from Left */
.reveal-left {
    opacity: 0;
    transform: translateX(-50px);
    transition: opacity 0.6s, transform 0.6s var(--ease-out-expo);
}

/* Blur In */
.reveal-blur {
    opacity: 0;
    filter: blur(10px);
    transition: opacity 0.8s, filter 0.8s var(--ease-out-expo);
}
```

### Background Effects

```css
/* Gradient Mesh */
.gradient-bg {
    background:
        radial-gradient(ellipse at 20% 80%, rgba(120, 0, 255, 0.3) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 20%, rgba(0, 255, 200, 0.2) 0%, transparent 50%),
        var(--bg-primary);
}

/* Noise Texture */
.noise-bg {
    background-image: url("data:image/svg+xml,..."); /* Inline SVG noise */
}

/* Grid Pattern */
.grid-bg {
    background-image:
        linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
    background-size: 50px 50px;
}
```

### Interactive Effects

```javascript
/* 3D Tilt on Hover */
class TiltEffect {
    constructor(element) {
        this.element = element;
        this.element.style.transformStyle = 'preserve-3d';
        this.element.style.perspective = '1000px';
        this.bindEvents();
    }

    bindEvents() {
        this.element.addEventListener('mousemove', (e) => {
            const rect = this.element.getBoundingClientRect();
            const x = (e.clientX - rect.left) / rect.width - 0.5;
            const y = (e.clientY - rect.top) / rect.height - 0.5;

            this.element.style.transform = `
                rotateY(${x * 10}deg)
                rotateX(${-y * 10}deg)
            `;
        });

        this.element.addEventListener('mouseleave', () => {
            this.element.style.transform = 'rotateY(0) rotateX(0)';
        });
    }
}
```

---

## Advanced Patterns

Techniques developed through real production presentations. Use these when generic patterns won't suffice.

---

### Swiss Modern Preset — Full Specification

The Swiss Modern preset is minimal, editorial, and typographically precise. It works especially well for medical/academic talks where credibility matters.

**Fonts:**
```html
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;900&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
```

**CSS Variables:**
```css
:root {
    --bg: #F4F0E8;          /* warm cream background */
    --ink: #111111;          /* near-black text */
    --muted: #6B6B6B;        /* secondary text */
    --accent: #C0392B;       /* reserved for one emphasis element max */
    --line: rgba(0,0,0,0.12); /* borders and rules */
    --font-display: 'Archivo', sans-serif;
    --font-body: 'Archivo', sans-serif;
    --font-mono: 'IBM Plex Mono', monospace;
}
```

**Background grid pattern (signature Swiss Modern detail):**
```css
body {
    background-color: var(--bg);
    background-image:
        linear-gradient(rgba(0,0,0,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,0,0,0.04) 1px, transparent 1px);
    background-size: 40px 40px;
}
```

**Chip / label component:**
```css
.chip {
    display: inline-block;
    border: 1px solid var(--ink);
    padding: 0.24rem 0.5rem;
    font: 600 var(--small-size)/1.05 var(--font-mono);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    width: fit-content;
}

/* Semantic color variants — use sparingly, one color per panel */
.chip--blue   { background: rgba(30,90,180,0.1);  border-color: rgba(30,90,180,0.5);  color: rgba(20,60,140,0.9); }
.chip--orange { background: rgba(200,90,20,0.1);  border-color: rgba(200,90,20,0.5);  color: rgba(160,60,10,0.9); }
.chip--green  { background: rgba(30,140,80,0.1);  border-color: rgba(30,140,80,0.5);  color: rgba(20,100,50,0.9); }
.chip--red    { background: rgba(182,28,28,0.12); border-color: rgba(182,28,28,0.55); color: rgba(140,15,15,0.9); }
.chip--slate  { background: rgba(42,61,94,0.1);   border-color: rgba(42,61,94,0.52);  color: rgba(30,45,75,0.9); }
/* Inverted (dark fill) — for emphasis or "active" state */
.chip--dark   { background: rgba(16,16,16,0.88);  border-color: rgba(16,16,16,0.88);  color: #ffffff; }
```

Use one color variant per card/panel to signal category. Never use more than two chip colors on a single slide — it breaks the Swiss Modern restraint.

**Illustration style — Swiss editorial flat (production-tested)**

Validated across multiple professional workshop and academic decks. The style descriptor below is the fixed anchor — never change it. Only the scene description changes per slide.

**Generation setup:**
- Model: `imagen-4.0-generate-001` (via `baoyu-image-gen` skill or Google API)
- Higher-quality alternative: `nano-banana-pro-preview` (Gemini, via `baoyu-danger-gemini-web` skill)
- Aspect ratios: 16:9 for full-slide images, 4:3 for right-panel illustration boxes, 1:1 for grid panels

**Core style descriptor (append to ALL prompts — do not modify):**
```
Style: Swiss editorial flat illustration, warm off-white and cream palette, muted ink outlines, minimal color fills (ochre, slate, cream), no gradients, no texture. Professional, academic tone. No text in the image.
```

**Palette rules:**
- Background: warm cream / off-white only
- Accent colors: slate and ochre only — never orange, never bright colors, never gradients
- For panels inside a grid (1:1): use `slate, cream only — no orange, no yellow` to keep panels consistent

**Example outputs:** Save generated images to an `examples/` folder inside the project and reference them in `illustration-prompts.md`. Format for that log:
```markdown
## [Slide title] — [aspect ratio]
**File:** `examples/slide-N-illustration.png`
**Model:** imagen-4.0-generate-001
**Prompt:**
[full prompt here]
```

---

**Scene templates — adapt the scene, keep the style descriptor:**

**Scene type: Knowledge transfer / mentorship (16:9)**
Use when: explaining learning, handoff, structured thinking, context engineering.
```
Clean flat editorial illustration, wide landscape format (16:9). [A senior figure] stands in [a professional setting] and turns toward [a junior figure]. The senior says one short phrase — represented by a minimal speech bubble. The junior stands listening, with a structured thought-map radiating outward from their head — four labeled branches expanding cleanly, each with a short note. The thought-map is rendered as a clean diagram, not a bubble cloud. No realistic anatomical detail. Style: Swiss editorial flat illustration, warm off-white and cream palette, muted ink outlines, minimal color fills (ochre, slate, cream), no gradients, no texture. Professional, academic tone. No text in the image.
```
*Adapt: swap the professional roles, setting, and what the thought-map branches represent for your domain.*

**Scene type: Delegation / parallel workflow (4:3)**
Use when: showing AI-assisted workflows, team output, one-to-many delegation.
```
Flat editorial illustration, 4:3 aspect ratio, warm cream background filling entire frame edge to edge. Left to right: FAR LEFT — [a lead figure] standing and gesturing toward the right. CENTER — [two or three workers] at a shared desk: one reviewing documents, one writing, one at a computer. FAR RIGHT — [an output artifact: screen, document, chart]. Subtle left-to-right flow. Warm cream background, slate grey and ochre accents only on furniture and objects, bold clean ink outlines, flat editorial illustration style, no gradients. No text, no labels, no words anywhere.
```
*Adapt: change who is delegating, what workers are doing, what the final artifact is.*

**Scene type: Individual task at desk (1:1)**
Use when: showing a single-role workflow in a grid panel — documentation, analysis, review.
```
Clean flat editorial illustration. [A professional in domain-appropriate attire] sits at a clean minimal desk in side profile, looking at a monitor showing [a structured artifact — grid, chart, or form]. A second figure stands nearby in the background, glancing at the screen. Figures positioned to the right of the frame with generous open negative space on the left. Minimal office setting — a subtle doorway or wall panel in background. Style: Swiss editorial flat illustration, warm off-white and cream palette, muted ink outlines, minimal color fills (slate, cream only — no orange, no yellow), no gradients, no texture. Professional academic tone. No text in the image.
```
*Adapt: swap the professional role, the monitor content, the setting.*

**Scene type: Audience-facing / education (1:1)**
Use when: showing content being consumed — patient education, onboarding, training materials.
```
Clean flat editorial illustration. [A person in casual or professional clothing] sits in [a waiting or learning space], holding and reading [a printed artifact — booklet, report, handout]. A second person nearby glances over with interest. Minimal setting — wall, window, a plant in background. Style: Swiss editorial flat illustration, warm off-white and cream palette, muted ink outlines, minimal color fills (slate, cream only — no orange, no yellow), no gradients, no texture. Professional academic tone. Only text allowed is [a short title visible on the artifact cover].
```
*Adapt: change who is reading, what the artifact is, and the setting.*

**Scene type: Group discussion / conference (1:1)**
Use when: showing multidisciplinary collaboration, research review, live meeting capture.
```
Clean flat editorial illustration. A small diverse group of [professionals] stands around a conference table in discussion. One person gestures toward a large wall-mounted screen showing [a data artifact — chart, scan, graph]. Floating above the group: abstract [idea visualization — speech waves, floating text fragments, connection lines] suggesting [what is being captured or generated]. The scene conveys active collaboration. Style: Swiss editorial flat illustration, warm off-white and cream palette, muted ink outlines, minimal color fills (slate, cream only — no orange, no yellow), no gradients, no texture. Professional academic tone. No readable text in the image.
```
*Adapt: change the professional group, the screen artifact, and what the floating visual represents.*

**Rules for adapting any template:**
1. Keep the style descriptor verbatim at the end of every prompt — it is the style anchor.
2. Fill in the `[bracketed]` slots with domain-specific content.
3. For 1:1 grid panels, always restrict to `slate, cream only — no orange, no yellow`.
4. Specify aspect ratio explicitly in both the prompt text and the generation API call.
5. Name diversity explicitly — the model defaults to homogeneous figures otherwise.
6. Log every final prompt to `illustration-prompts.md` so you can reproduce or iterate.

---

### Scrollable Content Cells

Use when a slide needs to show dense content (code, clinical notes, long lists) without shrinking font to illegibility. The cell scrolls internally; the slide itself never scrolls.

```css
.content-cell {
    flex: 1;
    min-height: 0;           /* CRITICAL: allows flex child to shrink */
    overflow-y: auto;
    border: 1px solid var(--line);
    border-radius: 8px;
    padding: 0.8rem 1rem;
    font: 400 clamp(0.7rem, 0.85vw, 0.88rem)/1.65 var(--font-mono);
    /* Custom scrollbar */
    scrollbar-width: thin;
    scrollbar-color: rgba(0,0,0,0.2) transparent;
}
```

**Key rule:** The parent must be a flex column with `min-height: 0`. Without this, the browser won't let the child shrink to trigger scroll — it just overflows.

```css
.slide-content {
    display: flex;
    flex-direction: column;
    height: 100%;
    min-height: 0;   /* propagate shrink down the chain */
}
```

---

### Image + Card Panels (Absolute Positioning Pattern)

For panels where an image fills the top and a card sits at the bottom — **do not use CSS grid height chains**. They resolve inconsistently across panels. Use absolute positioning instead.

```css
.panel {
    flex: 1;
    min-width: 0;
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid var(--line);
    position: relative;       /* establishes stacking context */
}

/* Image fills entire panel */
.panel > img {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}

/* Card is pinned to bottom — always consistent height */
.panel-card {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 10.5rem;          /* fixed height — always reliable */
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    gap: 0.6rem;
    padding: 0.85rem 1rem;
    background: var(--bg);
    border-top: 2px solid var(--line);
    overflow: hidden;
}
```

**Why:** `grid-template-rows: 1fr auto` on each panel resolves `1fr` differently per panel because the height chain is unreliable. Absolute positioning bypasses this entirely.

---

### Invisible Hotspots with Hover Tooltips

For illustration slides where you want to reveal context on hover without visible UI elements in the resting state.

```css
/* Hotspot — invisible until hover, cursor signals interactivity */
.hotspot {
    position: absolute;
    cursor: pointer;
    border-radius: 4px;
    /* No background, no border — completely invisible */
}

/* Tooltip — hidden by default, smooth reveal on hover */
.tooltip {
    position: absolute;
    left: 0; top: 0;
    width: clamp(240px, 34%, 320px);
    background: #FAFAF7;
    border: 1.5px solid rgba(60,80,120,0.25);
    border-radius: 6px;
    padding: 0.75rem 0.9rem;
    box-shadow: 6px 10px 28px rgba(16,16,16,0.15);
    opacity: 0;
    transform: translateY(8px);
    transition: opacity 0.22s ease, transform 0.22s ease;
    pointer-events: none;
    z-index: 10;
}

.hotspot:hover .tooltip {
    opacity: 1;
    transform: translateY(0);
}
```

**Positioning note:** Percentage values on `position: absolute` children are relative to the nearest positioned ancestor — the hotspot div, NOT the slide container. Use `calc(100% + 12px)` to push a tooltip outside the hotspot, or `left: 0; top: 0` to anchor inside it.

**Hotspot sizing:** Tune with `left`, `top`, `width`, `height` as percentages of the illustration container. Always test visually — illustration element positions vary.

---

### Mock Chat Interface Component

Two variants: **light** (generic/abstract AI tool) and **dark** (authentic Claude/ChatGPT desktop look). Use light when the tool identity doesn't matter; use dark when you're specifically demoing Claude or GPT.

#### Variant A — Light (generic AI tool)

```css
.chat-mock {
    display: flex;
    flex-direction: column;
    height: 100%;
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid var(--line);
}

.chat-mock-header {
    background: #1A1B1E;
    color: rgba(255,255,255,0.85);
    padding: 0.5rem 0.9rem;
    font: 600 0.72rem/1 var(--font-mono);
    letter-spacing: 0.05em;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.chat-mock-body {
    flex: 1;
    min-height: 0;
    overflow-y: auto;
    background: #F9F6EE;
    padding: 0.9rem 0.85rem;
    display: flex;
    flex-direction: column;
    gap: 0.7rem;
}

/* User message — right-aligned */
.chat-user {
    align-self: flex-end;
    max-width: 82%;
    background: #2B3A5C;
    color: #fff;
    border-radius: 10px 10px 2px 10px;
    padding: 0.55rem 0.75rem;
    font: 400 clamp(0.72rem, 0.9vw, 0.88rem)/1.55 var(--font-mono);
}

/* AI response — left-aligned */
.chat-ai {
    align-self: flex-start;
    max-width: 88%;
    background: #fff;
    border: 1px solid var(--line);
    border-radius: 2px 10px 10px 10px;
    padding: 0.55rem 0.75rem;
    font: 400 clamp(0.72rem, 0.9vw, 0.88rem)/1.55 var(--font-mono);
    color: var(--ink);
}
```

**Syntax highlighting for inline code in AI responses:**
```css
.hl-b  { color: #7AA4C8; font-weight: 600; }  /* blue — labels, keys */
.hl-g  { color: #7EB8A0; }                      /* green — values, scores */
.hl-y  { color: #D4A96A; }                      /* yellow — warnings, flags */
.hl-d  { color: rgba(255,255,255,0.4); }        /* dim — comments, metadata */
```

---

#### Variant B — Dark (authentic Claude / ChatGPT look)

Use for "skills in action" slides where you want to show Claude's actual desktop interface. The header mimics the Claude app chrome; the avatar dot uses Claude's coral color.

```css
/* Outer container */
.chat-dark {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.1);
    background: #18191C;
}

/* App chrome header */
.chat-dark-header {
    padding: 0.55rem 0.9rem;
    background: #111214;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* App logo dot — use #CC785C for Claude, #10A37F for ChatGPT */
.chat-dark-dot {
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: #CC785C;   /* Claude coral */
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font: 700 0.55rem/1 sans-serif;
    color: white;
}

.chat-dark-title {
    font: 600 0.75rem/1 var(--font-mono);
    color: rgba(255,255,255,0.8);
    letter-spacing: 0.04em;
}

/* Optional: active skill badge in header */
.chat-skill-badge {
    margin-left: auto;
    font: 600 0.62rem/1 var(--font-mono);
    color: #7EB8A0;
    background: rgba(126,184,160,0.12);
    border: 1px solid rgba(126,184,160,0.28);
    border-radius: 3px;
    padding: 0.18rem 0.42rem;
    letter-spacing: 0.05em;
}

/* Scrollable message area */
.chat-dark-body {
    flex: 1;
    min-height: 0;
    overflow-y: auto;
    padding: 0.9rem;
    display: flex;
    flex-direction: column;
    gap: 0.85rem;
}

/* User message bubble */
.chat-dark-user {
    align-self: flex-end;
    max-width: 88%;
    background: #2C3A5C;
    border-radius: 10px 10px 3px 10px;
    padding: 0.6rem 0.85rem;
    font: 400 clamp(0.68rem, 0.88vw, 0.86rem)/1.6 var(--font-mono);
    color: rgba(255,255,255,0.86);
}

/* Slash command highlight within user message */
.chat-dark-cmd { color: #7EB8A0; font-weight: 700; }

/* Claude/AI message row */
.chat-dark-ai-row {
    align-self: flex-start;
    max-width: 94%;
    display: flex;
    gap: 0.5rem;
    align-items: flex-start;
}

/* Avatar next to AI message */
.chat-dark-avatar {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: #CC785C;
    flex-shrink: 0;
    margin-top: 2px;
    display: flex;
    align-items: center;
    justify-content: center;
    font: 700 0.58rem/1 sans-serif;
    color: white;
}

/* AI message bubble */
.chat-dark-bubble {
    background: #232428;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 3px 10px 10px 10px;
    padding: 0.65rem 0.85rem;
    font: 400 clamp(0.68rem, 0.88vw, 0.86rem)/1.65 var(--font-mono);
    color: rgba(255,255,255,0.8);
}

/* Syntax highlight colors inside dark bubble */
.chat-dark-bubble .hl-g { color: #7EB8A0; }   /* green — success, values */
.chat-dark-bubble .hl-y { color: #D4A96A; }   /* yellow — warnings */
.chat-dark-bubble .hl-r { color: #C97070; }   /* red — errors, flags */
.chat-dark-bubble .hl-b { color: #7AA4C8; font-weight: 600; } /* blue — keys */
.chat-dark-bubble .hl-d { color: rgba(255,255,255,0.38); }    /* dim */

/* Horizontal rule inside bubble */
.chat-dark-divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.08);
    margin: 0.35rem 0;
}
```

**For ChatGPT variant:** swap `#CC785C` → `#10A37F` (OpenAI green) on the dot and avatar. Header background can stay the same.

**Pairing the dark chat with a light document panel:** A common layout is dark chat on the left showing the AI interaction, light document on the right showing the output artifact. Use `display: flex; gap: 1.2rem;` as the parent, each child `flex: 1; min-width: 0`.

---

### Before/After Comparison Slides

For demonstrating transformation (e.g., prompt engineering, before/after notes). Use a 3-column grid: row labels | before | after.

```css
.compare-grid {
    display: grid;
    grid-template-columns: 7rem 1fr 1fr;
    gap: 0.5rem;
    flex: 1;
    min-height: 0;
}

.compare-col-hdr {
    font: 700 clamp(0.7rem, 0.85vw, 0.88rem)/1 var(--font-mono);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    text-align: center;
    padding: 0.3rem;
}

.compare-row-label {
    display: flex;
    align-items: center;
    font: 600 0.7rem/1.2 var(--font-mono);
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: var(--muted);
}

.compare-cell {
    border-radius: 6px;
    padding: 0.6rem 0.8rem;
    font: 400 clamp(0.68rem, 0.78vw, 0.8rem)/1.65 var(--font-mono);
    overflow-y: auto;
    min-height: 0;
    scrollbar-width: thin;
}

.compare-cell--pre {
    background: #F5F0E6;
    border: 1px solid rgba(180,100,60,0.15);
    color: #444;
}

.compare-cell--post {
    background: #EEF3EF;
    border: 1px solid rgba(60,120,80,0.2);
    color: #222;
}
```

**When to use:** Use the 3-column compare-grid when you're comparing two complete documents or text blocks side-by-side (e.g., a whole prompt before/after). Each cell is one large scrollable block.

---

#### Variant: Row-per-Attribute Compare (structured data)

Use when comparing two states across multiple named dimensions — e.g., before/after a prompt template is applied to a clinical note, showing how each section changed. Works best with 3–5 rows.

```css
/* Container: fixed label column + two data columns */
.compare-rows {
    display: grid;
    grid-template-columns: 5.5rem 1fr 1fr;  /* adjust label width to fit your labels */
    grid-auto-rows: auto;                     /* rows size to content */
    gap: 0.4rem;
    flex: 1;
    min-height: 0;
}

/* Column headers (row 1) */
.compare-rows-hdr {
    font: 700 clamp(0.65rem, 0.8vw, 0.82rem)/1 var(--font-mono);
    letter-spacing: 0.07em;
    text-transform: uppercase;
    padding: 0.35rem 0.6rem;
    border-radius: 4px;
    text-align: center;
}
.compare-rows-hdr--pre  { background: rgba(180,90,30,0.1);  color: #7a3a08; }
.compare-rows-hdr--post { background: rgba(30,110,70,0.1);  color: #185a38; }

/* Row label (left column) */
.compare-rows-label {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding-right: 0.55rem;
    font: 700 clamp(0.58rem, 0.72vw, 0.72rem)/1.2 var(--font-mono);
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--muted);
    text-align: right;
}

/* Data cell — scrollable, sized by content */
.compare-rows-cell {
    border-radius: 6px;
    padding: 0.55rem 0.75rem;
    font: 400 clamp(0.64rem, 0.78vw, 0.78rem)/1.55 var(--font-body);
    overflow-y: auto;
    min-height: 0;
}
.compare-rows-cell--pre  { background: #F7F1E8; border: 1px solid rgba(180,90,30,0.18); color: #3a2808; }
.compare-rows-cell--post { background: #EDF4F0; border: 1px solid rgba(30,110,70,0.2);  color: #0e2818; }
.compare-rows-cell b { font-weight: 700; }
```

**HTML structure:**
```html
<div class="compare-rows">
  <!-- Row 0: column headers (label column is empty) -->
  <div></div>
  <div class="compare-rows-hdr compare-rows-hdr--pre">Before</div>
  <div class="compare-rows-hdr compare-rows-hdr--post">After</div>

  <!-- Row 1 -->
  <div class="compare-rows-label">HPI</div>
  <div class="compare-rows-cell compare-rows-cell--pre">Generic paragraph prose...</div>
  <div class="compare-rows-cell compare-rows-cell--post">Structured narrative with <b>onset, triggers, context</b>...</div>

  <!-- Row 2 -->
  <div class="compare-rows-label">Assessment</div>
  <div class="compare-rows-cell compare-rows-cell--pre">Short summary...</div>
  <div class="compare-rows-cell compare-rows-cell--post">ILAE-framed reasoning + plan...</div>

  <!-- Add more rows as needed (3–5 max for readability) -->
</div>
```

**Tip:** If a row needs more height, set `min-height` on the cells for that row. The `grid-auto-rows: auto` will size each row independently based on its tallest cell.

---

### AI Image Generation for Illustrations

When the presentation needs custom illustrations, use the Gemini API.

**Model choice:**
- `imagen-4.0-generate-001` — standard quality, fast
- `models/nano-banana-pro-preview:generateContent` — higher quality, better text rendering; use when illustration contains legible text or requires more visual fidelity

**Generation script (nano-banana-pro-preview):**
```python
import google.generativeai as genai
import base64, json, os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def generate_illustration(prompt, output_path, aspect_ratio="16:9"):
    model = genai.GenerativeModel("models/nano-banana-pro-preview")
    response = model.generate_content(
        contents=[{"role": "user", "parts": [{"text": prompt}]}],
        generation_config={"response_modalities": ["IMAGE", "TEXT"]}
    )
    for part in response.candidates[0].content.parts:
        if hasattr(part, "inline_data"):
            with open(output_path, "wb") as f:
                f.write(base64.b64decode(part.inline_data.data))
            return output_path
    raise ValueError("No image in response")
```

**After generating, embed as base64 in HTML** to keep the file self-contained:
```python
with open(image_path, "rb") as f:
    b64 = base64.b64encode(f.read()).decode()
img_tag = f'<img src="data:image/png;base64,{b64}" alt="...">'
```

**Prompt log:** Always save illustration prompts to `illustration-prompts.md` in the project folder so they can be reproduced or iterated on later.

---

### Medical / Clinical Presentation — De-identification Checklist

When building presentations for medical conferences or workshops that include example clinical notes:

Before inserting any clinical example text, verify:

- [ ] Patient name removed or replaced with initials (e.g., "A.M.")
- [ ] Specific dates replaced with relative timeframes ("4 months prior", "3 months later")
- [ ] State/jurisdiction references generalized ("state law" not "Georgia law")
- [ ] Specific times of day removed if identifying ("late evening" not "10–11 PM")
- [ ] Hospital-specific app names generalized ("patient portal" not "MyChart")
- [ ] Medication brand names → generic names where possible
- [ ] Age, sex, and clinical details kept — these are educational, not identifying in isolation

The combination of all identifiers (name + exact date + state + specific medications + age) is what creates identifiability, not any single detail.

---

### Laptop Presentation Media Query

For medical/academic presentations that will be shown on a mirrored laptop display or smaller window, add a compact responsive mode. This is separate from mobile breakpoints — it targets the 13–15" laptop-as-projector scenario.

```css
@media (min-width: 901px) and (max-width: 1440px),
       (min-width: 901px) and (max-height: 860px) {

    /* Tighten global scales — everything derives from these */
    :root {
        --title-size: clamp(1.6rem, 4vw, 3.2rem);
        --h2-size: clamp(1.2rem, 2.8vw, 2.2rem);
        --body-size: clamp(0.72rem, 1.15vw, 1rem);
        --small-size: clamp(0.62rem, 0.85vw, 0.85rem);
        --slide-padding: clamp(0.9rem, 2.5vw, 2.5rem);
        --content-gap: clamp(0.5rem, 1.2vw, 1.2rem);
        --element-gap: clamp(0.25rem, 0.7vw, 0.7rem);
        --stage-margin: clamp(0.75rem, 1.7vw, 1.7rem);
    }

    /* Slide-specific compression — add per slide as needed */
    /* Example: tighten a panel layout */
    .panel-grid {
        gap: clamp(0.5rem, 0.9vw, 1rem);
    }
}
```

**Interaction with fullscreen:** The laptop query provides base compact sizing. Fullscreen then adds `--stage-margin: clamp(0.3rem, 0.9vw, 0.8rem)` to reclaim the outer frame. Typography and component sizes still come from the laptop query — they don't change when entering fullscreen.

**Best tuning order if deck still feels cramped:**
1. Adjust root variables inside the laptop media query first
2. Then add slide-specific overrides inside the same query
3. Only touch base desktop styles (outside the query) as a last resort

---

### Transform-Based Image Positioning

When `object-position` does nothing to visually move an image, it's because the image ratio exactly matches the container's `aspect-ratio` with `object-fit: contain` — there's no free internal space to shift into.

**The fix: use `transform` instead.**

```css
.illustration-frame {
    aspect-ratio: 1408 / 768;   /* must match actual image pixel ratio */
    position: relative;
    overflow: visible;           /* allow tooltip/hotspot overflow */

    /* CSS variables for easy tuning */
    --art-shift-x: 10%;
    --art-shift-y: 5%;
    --art-scale: 1.1;
}

.illustration-frame img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    object-position: 50% 50%;
    border-radius: inherit;

    /* Move/scale the art using transform */
    transform: translate(var(--art-shift-x), var(--art-shift-y)) scale(var(--art-scale));
    transform-origin: center center;

    /* Clip excess from scale/shift so edges don't peek out */
    clip-path: inset(0 round 8px);
}
```

**CSS variable art-shift + hotspot sync:** If the slide has interactive hotspots overlaid on the illustration, their `left`/`top` must reference the same shift variables — otherwise hoverable regions no longer align with the visual art after shifting.

```css
.hotspot {
    position: absolute;
    /* Base position + art shift applied consistently */
    left: calc(2.6% + var(--art-shift-x));
    top: calc(8% + var(--art-shift-y));
    width: 14%;
    height: 82%;
}
```

**Tuning guide:**
| If… | Then… |
|-----|-------|
| Art looks too far left | Increase `--art-shift-x` |
| Art overlaps the slide title | Decrease `--art-scale` or decrease `--art-shift-y` |
| Frame background peeks through after scaling | Increase `--art-scale` slightly; keep `clip-path` |
| Hotspots no longer match the art | Update `left`/`top` in `.hotspot` using the same shift variables |

---

### Fullscreen Mode

Every presentation should support fullscreen. This eliminates browser chrome during delivery and gives the cleanest experience when presenting from a laptop.

**Keyboard trigger (`F` key) + button:**

```javascript
// In your SlidePresentation class or standalone

setupFullscreen() {
    // F key toggles fullscreen
    document.addEventListener('keydown', (e) => {
        if (e.key === 'f' || e.key === 'F') {
            this.toggleFullscreen();
        }
        // ESC is handled natively by the browser — no need to wire it
    });

    // Optional: click a button
    const btn = document.getElementById('fullscreenBtn');
    if (btn) btn.addEventListener('click', () => this.toggleFullscreen());
}

toggleFullscreen() {
    if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(err => {
            console.warn('Fullscreen request failed:', err);
        });
    } else {
        document.exitFullscreen();
    }
}
```

**Visual indicator (optional — small hint in corner):**

```css
.fullscreen-hint {
    position: fixed;
    bottom: 1.2rem;
    right: 1.5rem;
    font: 500 0.65rem/1 var(--font-mono);
    color: rgba(0,0,0,0.25);
    letter-spacing: 0.06em;
    text-transform: uppercase;
    pointer-events: none;
    z-index: 100;
    transition: opacity 0.3s;
}

/* Hide hint once user has gone fullscreen once */
:fullscreen .fullscreen-hint { display: none; }
```

```html
<div class="fullscreen-hint">Press F for fullscreen</div>
```

**Fullscreen CSS adjustments** — some layouts need tweaking in fullscreen:

```css
/* Target fullscreen state */
:fullscreen .slide {
    height: 100vh;
    height: 100dvh;
}

/* Firefox prefix */
:-moz-full-screen .slide {
    height: 100vh;
}

/* Safari prefix */
:-webkit-full-screen .slide {
    height: 100vh;
}
```

**Note:** The browser handles ESC to exit fullscreen natively — don't override it. Only wire F (or a button) for entering. Attempting to intercept ESC breaks expected browser behavior.

---

### Pipeline Flow Layout

**When to use:** Automatically use this layout when slide content describes a linear workflow with 2–4 named stages (e.g., "Input → Process → Output", "Capture → Transform → Validate → Document"). Look for signal words: "pipeline", "workflow", "stages", "steps", "flow".

A horizontal grid of nodes connected by arrow connectors. The middle and last nodes can be accent-colored to signal the focal step. On narrow screens, nodes stack vertically and connectors rotate 90°.

```css
/* ── Pipeline Flow ──
   grid: node — connector — node — connector — node
   For 2 nodes: grid-template-columns: 1fr auto 1fr
   For 3 nodes: grid-template-columns: 1fr auto 1fr auto 1fr
   Add more pairs for longer pipelines.
*/
.pipeline-flow {
    display: grid;
    grid-template-columns: 1fr auto 1fr auto 1fr;
    align-items: stretch;
    min-height: 0;
    flex: 1 1 auto;
    padding-top: clamp(0.35rem, 0.8vh, 0.6rem);
    border-top: 1px solid rgba(16,16,16,0.12);
}

/* Each step box */
.pipeline-node {
    border: 1px solid var(--ink);
    background: var(--bg-panel);
    backdrop-filter: blur(8px);
    padding: clamp(0.9rem, 1.35vw, 1.6rem);
    display: flex;
    flex-direction: column;
    gap: var(--element-gap);
    min-height: 0;
    box-shadow: 6px 6px 0 rgba(16,16,16,0.06);
}

/* Accent the focal node (e.g., the "AI" step) */
.pipeline-node--accent {
    border-left: 4px solid var(--accent);
    background: linear-gradient(180deg, var(--accent-soft), rgba(255,255,255,0.84));
}

/* Secondary accent (e.g., "output" step) */
.pipeline-node--warm {
    border-left: 4px solid rgba(122,80,20,0.62);
    background: linear-gradient(180deg, rgba(122,80,20,0.10), rgba(255,255,255,0.88));
}

/* Label above the node heading */
.pipeline-node-label {
    font: 700 clamp(0.78rem, 0.9vw, 1rem)/1 var(--font-mono);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--muted);
}

/* Main node heading */
.pipeline-node-heading {
    font: 700 clamp(1.1rem, 1.4vw, 1.4rem)/1.22 var(--font-display);
    letter-spacing: -0.01em;
    color: var(--ink);
}

/* Supporting rows (label: value pairs) */
.pipeline-node-rows { display: flex; flex-direction: column; flex: 1; justify-content: center; }
.pipeline-node-row {
    display: flex;
    align-items: baseline;
    gap: 0.65rem;
    padding: clamp(0.36rem, 0.6vw, 0.6rem) 0;
    border-bottom: 1px solid var(--line);
}
.pipeline-node-row:first-child { border-top: 1px solid var(--line); }
.pipeline-node-row-label {
    font: 600 clamp(0.78rem, 0.88vw, 0.98rem)/1 var(--font-mono);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--muted);
    min-width: 4.8rem;
    flex-shrink: 0;
}
.pipeline-node-row-value {
    font: 500 clamp(0.9rem, 1vw, 1.1rem)/1.3 var(--font-body);
    color: var(--ink);
}

/* Footer note */
.pipeline-node-footer {
    margin-top: auto;
    padding-top: 0.55rem;
    border-top: 1px solid var(--line);
    font: 500 clamp(0.76rem, 0.82vw, 0.9rem)/1.3 var(--font-mono);
    color: var(--muted);
    letter-spacing: 0.03em;
}

/* Arrow connector between nodes */
.pipeline-connector {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0 clamp(0.4rem, 0.7vw, 0.8rem);
    flex-shrink: 0;
}
.pipeline-connector-inner {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.3rem;
}
.pipeline-connector-line {
    width: clamp(1.6rem, 2.6vw, 3rem);
    height: 1px;
    background: rgba(16,16,16,0.3);
}
.pipeline-connector-arrow {
    font-size: clamp(0.9rem, 1.2vw, 1.3rem);
    color: rgba(16,16,16,0.5);
    line-height: 1;
    margin-top: calc(-1 * 0.5rem);
}

/* Responsive: stack vertically on narrow screens */
@media (max-width: 900px) {
    .pipeline-flow { grid-template-columns: 1fr; }
    .pipeline-connector { transform: rotate(90deg); padding: 0.4rem 0; }
}
```

**HTML structure:**
```html
<div class="pipeline-flow">
  <div class="pipeline-node">
    <div class="pipeline-node-label">Step 01</div>
    <div class="pipeline-node-heading">Input</div>
    <div class="pipeline-node-rows">
      <div class="pipeline-node-row">
        <span class="pipeline-node-row-label">Source</span>
        <span class="pipeline-node-row-value">De-identified case note</span>
      </div>
      <div class="pipeline-node-row">
        <span class="pipeline-node-row-label">Format</span>
        <span class="pipeline-node-row-value">Plain text, no PHI</span>
      </div>
    </div>
    <div class="pipeline-node-footer">Clinician provides</div>
  </div>

  <div class="pipeline-connector">
    <div class="pipeline-connector-inner">
      <div class="pipeline-connector-line"></div>
      <div class="pipeline-connector-arrow">↓</div>
    </div>
  </div>

  <div class="pipeline-node pipeline-node--accent">
    <div class="pipeline-node-label">Step 02</div>
    <div class="pipeline-node-heading">AI Transform</div>
    <!-- ... rows ... -->
  </div>

  <div class="pipeline-connector"> <!-- same as above --> </div>

  <div class="pipeline-node pipeline-node--warm">
    <div class="pipeline-node-label">Step 03</div>
    <div class="pipeline-node-heading">Output</div>
    <!-- ... rows ... -->
  </div>
</div>
```

**Scaling:** For 2-node pipelines, use `grid-template-columns: 1fr auto 1fr`. For 4-node, add another `auto 1fr` pair. Don't exceed 4 nodes — the cells become too narrow at typical laptop widths.

---

### Live Demo Slide + Helper Server

**When to use:** When the user asks for a live demo slide — a slide where the presenter clicks a button to launch an external app (Claude, ChatGPT, a browser URL) mid-presentation.

This pattern uses a tiny local Python server to bridge the HTML slide to macOS `open` commands, since browsers can't launch desktop apps directly.

#### The slide (HTML)

```html
<!-- Big centered label -->
<div class="live-demo-label">LIVE DEMO</div>

<!-- Optional subtitle -->
<div class="live-demo-sub">Skill: /your-skill-name</div>

<!-- Launch buttons -->
<div style="display:flex; gap:1rem; justify-content:center; margin-top:2rem;">
  <button class="live-demo-btn" id="openClaudeBtn" onclick="launchClaude()">
    ✦ Open Claude
  </button>
  <a class="live-demo-btn" href="https://chatgpt.com" target="_blank">
    ✦ Open ChatGPT
  </a>
</div>

<!-- Status line shown during launch -->
<div class="live-demo-status" id="demoStatus"></div>
```

```css
.live-demo-label {
    font: 900 clamp(3.5rem, 8vw, 7.5rem)/1.05 var(--font-display);
    letter-spacing: -0.04em;
    color: var(--ink);
    text-align: center;
    text-transform: uppercase;
}

.live-demo-sub {
    font: 500 clamp(1rem, 1.3vw, 1.3rem)/1.5 var(--font-mono);
    color: var(--muted);
    text-align: center;
    letter-spacing: 0.02em;
    margin-top: 1.5rem;
}

.live-demo-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.6rem;
    padding: clamp(0.7rem, 1.1vw, 1.1rem) clamp(1.6rem, 2.8vw, 2.8rem);
    background: var(--ink);
    color: var(--bg-primary);
    font: 700 clamp(0.9rem, 1.1vw, 1.1rem)/1 var(--font-mono);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    text-decoration: none;
    transition: opacity 0.15s;
}
.live-demo-btn:hover { opacity: 0.75; }
.live-demo-btn.is-launching { opacity: 0.6; pointer-events: none; }

.live-demo-status {
    min-height: 1.4em;
    margin-top: 0.9rem;
    font: 500 clamp(0.72rem, 0.92vw, 0.92rem)/1.35 var(--font-mono);
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: var(--muted);
    text-align: center;
}
```

```javascript
async function launchClaude() {
    const btn = document.getElementById('openClaudeBtn');
    const status = document.getElementById('demoStatus');
    btn.classList.add('is-launching');
    status.textContent = 'Launching Claude…';
    try {
        const res = await fetch('http://127.0.0.1:8765/open/claude', { method: 'POST' });
        const data = await res.json();
        status.textContent = data.ok ? 'Claude is open.' : 'Could not open Claude — start slide_helper_server.py';
    } catch {
        status.textContent = 'Helper server not running — see slide_helper_server.py';
    } finally {
        btn.classList.remove('is-launching');
    }
}
```

#### The helper server (`slide_helper_server.py`)

Generate this file alongside the presentation whenever a live demo slide is requested.

```python
#!/usr/bin/env python3
"""
Slide helper server — bridges HTML presentation buttons to macOS 'open' commands.
Run before presenting: python3 slide_helper_server.py
"""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import subprocess

HOST = "127.0.0.1"
PORT = 8765

APPS = {
    "/open/claude": ["open", "-a", "Claude"],
    "/open/chatgpt": ["open", "-a", "ChatGPT"],
    # Add more routes as needed: "/open/browser": ["open", "https://example.com"]
}

class SlideHelperHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self._send_json(200, {"ok": True})

    def do_POST(self):
        cmd = APPS.get(self.path)
        if not cmd:
            self._send_json(404, {"ok": False, "error": "unknown route"})
            return
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            self._send_json(200, {"ok": True})
        except subprocess.CalledProcessError as e:
            self._send_json(500, {"ok": False, "error": e.stderr.strip()})

    def log_message(self, fmt, *args):
        return  # silence request logs during presentation

def main():
    server = ThreadingHTTPServer((HOST, PORT), SlideHelperHandler)
    print(f"Slide helper listening on http://{HOST}:{PORT}", flush=True)
    print("Press Ctrl+C to stop.", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

if __name__ == "__main__":
    main()
```

**Setup instructions to include in a comment at the top of the generated HTML:**
```html
<!--
  LIVE DEMO SLIDE — requires slide_helper_server.py
  Before presenting, open a terminal and run:
    python3 slide_helper_server.py
  Leave it running. Press Ctrl+C to stop after the talk.
-->
```

**Extending for other actions:** Add new entries to the `APPS` dict in the server and new buttons + handlers in the slide. To open a URL in the default browser: `["open", "https://example.com"]`. To open a file: `["open", "/path/to/file"]`.

---

### Per-Slide Accent Color System

**When to use:** Opt in when building a deck with 6+ content slides and you want visual rhythm — each slide feels distinct without breaking the overall design system.

Each slide gets a unique `border-left` color on its highlighted card, plus a matching tinted background and chip. Use the same hue palette across all slides but rotate through it.

```css
/* Pattern: .slide-N .card--accent { border-left-color: ...; background: ...; }
   Use rgba with low opacity to stay within the Swiss Modern palette.
   The accent color is the only per-slide variable — everything else stays global.
*/

/* Template for each slide — swap in your own hue */
.slide-1 .card--accent {
    border-left: 4px solid rgba(255, 75, 31, 0.72);     /* warm red-orange */
    background: linear-gradient(180deg, rgba(255,75,31,0.08), rgba(255,255,255,0.88));
}
.slide-1 .card--accent .chip {
    background: rgba(255,75,31,0.12);
    border-color: rgba(255,75,31,0.6);
    color: rgba(16,16,16,0.92);
}

.slide-2 .card--accent {
    border-left: 4px solid rgba(28, 66, 116, 0.62);     /* slate blue */
    background: linear-gradient(180deg, rgba(28,66,116,0.10), rgba(255,255,255,0.90));
}
.slide-2 .card--accent .chip {
    background: rgba(28,66,116,0.10);
    border-color: rgba(28,66,116,0.55);
    color: rgba(16,16,16,0.94);
}

.slide-3 .card--accent {
    border-left: 4px solid rgba(35, 90, 55, 0.62);      /* forest green */
    background: linear-gradient(180deg, rgba(35,90,55,0.10), rgba(255,255,255,0.90));
}
.slide-3 .card--accent .chip {
    background: rgba(35,90,55,0.10);
    border-color: rgba(35,90,55,0.55);
    color: rgba(16,16,16,0.94);
}

.slide-4 .card--accent {
    border-left: 4px solid rgba(122, 80, 20, 0.66);     /* warm ochre */
    background: linear-gradient(180deg, rgba(122,80,20,0.12), rgba(255,255,255,0.90));
}
/* ... continue pattern for remaining slides */
```

**Hue rotation palette (Swiss Modern safe — no neons, no pastels):**
| Slide | Border color | Feel |
|-------|-------------|------|
| 1 | `rgba(255,75,31,0.72)` | Alert / call to action |
| 2 | `rgba(28,66,116,0.62)` | Calm / informational |
| 3 | `rgba(35,90,55,0.62)` | Positive / go |
| 4 | `rgba(122,80,20,0.66)` | Warm / historical |
| 5 | `rgba(182,28,28,0.68)` | Caution / risk |
| 6 | `rgba(42,61,94,0.64)` | Authoritative |
| 7 | `rgba(16,16,16,0.54)` | Neutral / black |

**Rules:**
- Only apply to the *one* accent card per slide (`.card--accent`), not global cards.
- Keep the opacity low (0.06–0.15 for background gradient) — the tint should be felt, not seen.
- Don't repeat the same hue on adjacent slides.
- For dark-fill chips (inverted), use `background: rgba(16,16,16,0.88); color: #fff` — overrides the hue entirely for maximum contrast.

---

### Hard Shadow Image Frame

**When to use:** For featuring a single illustration, screenshot, or diagram in the Swiss Modern style. The flat (no-blur) hard shadow is a Swiss design signature — it grounds the image without softness.

Distinct from the `card` component: this frame uses a solid offset shadow instead of `backdrop-filter`, and `object-fit: contain` instead of `cover`, so illustrations aren't cropped.

```css
.img-showcase {
    min-height: 0;
    padding-top: clamp(0.35rem, 0.8vh, 0.6rem);
    border-top: 1px solid rgba(16,16,16,0.12);
    overflow: hidden;
    display: flex;
    align-items: stretch;
}

.img-frame {
    flex: 1;
    border: 1px solid var(--ink);
    background: rgba(255,255,255,0.52);
    backdrop-filter: blur(10px);
    box-shadow: 8px 8px 0 rgba(16,16,16,0.08); /* flat hard shadow — no blur radius */
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
}

.img-frame img {
    width: 100%;
    height: 100%;
    object-fit: contain;      /* never crop — show full illustration */
    object-position: center;
    display: block;
}
```

**Usage in a slide:**
```html
<div class="slide-content">
  <div class="kicker">Section Label</div>
  <h2>Slide Heading</h2>
  <div class="img-showcase">
    <div class="img-frame">
      <img src="examples/your-illustration.png" alt="Description">
    </div>
  </div>
</div>
```

**Tuning the shadow:** `8px 8px 0` is the default. For smaller frames, reduce to `5px 5px 0`. For a more dramatic editorial feel, increase to `12px 12px 0`. The zero blur radius is non-negotiable — it's what makes it Swiss, not generic.

---

### Syntax Token Coloring for Prompts and Markdown

**When to use:** When showing a structured prompt, skill file, or markdown document inside a slide — and you want to visually differentiate keys, values, trigger words, and comments without a full syntax highlighter library.

Use `<span>` tags with `.tok-*` classes directly inside a `<pre>` or monospace code block.

```css
/* Applied to a monospace container (e.g., .slide-code-block) */
.tok-key     { color: #3a5fa0; font-weight: 600; }  /* frontmatter keys, YAML keys */
.tok-val     { color: #5a3a00; }                     /* string values */
.tok-comment { color: #9a9a9a; font-style: italic; } /* # comments, metadata */
.tok-trigger { color: #1a7a5a; font-weight: 600; }  /* trigger words, conditions */
.tok-section { color: var(--ink); font-weight: 700; } /* markdown ## headings */
.tok-muted   { color: rgba(16,16,16,0.4); }          /* de-emphasized text */
```

**Example — styled skill file excerpt:**
```html
<pre class="slide-code-block">
<span class="tok-comment">---</span>
<span class="tok-key">name:</span> <span class="tok-val">your-skill</span>
<span class="tok-key">description:</span> <span class="tok-val">Does X when Y happens.</span>
<span class="tok-comment">---</span>

<span class="tok-section">## When to Use</span>
<span class="tok-trigger">TRIGGER when:</span> user asks for X, Y, or Z.
<span class="tok-muted"># This section is read by the AI, not the user</span>

<span class="tok-section">## Steps</span>
1. <span class="tok-key">Step 1</span> — <span class="tok-val">Do something specific</span>
2. <span class="tok-key">Step 2</span> — <span class="tok-val">Then do this</span>
</pre>
```

**Container CSS:**
```css
.slide-code-block {
    flex: 1;
    min-height: 0;
    overflow-y: auto;
    background: #F2EDE3;
    border: 1px solid rgba(60,80,120,0.14);
    border-radius: 8px;
    padding: clamp(0.7rem, 1.1vw, 1.1rem) clamp(0.9rem, 1.3vw, 1.3rem);
    font: 400 clamp(0.72rem, 0.88vw, 0.88rem)/1.6 var(--font-mono);
    color: #2a3550;
    white-space: pre-wrap;
    word-break: break-word;
}
```

**For dark backgrounds (dark chat bubble, dark slide):** Invert the palette — use the `hl-*` classes from the Mock Chat section instead.

---

## Troubleshooting

### Common Issues

**Fonts not loading:**
- Check Fontshare/Google Fonts URL
- Ensure font names match in CSS

**Animations not triggering:**
- Verify Intersection Observer is running
- Check that `.visible` class is being added

**Scroll snap not working:**
- Ensure `scroll-snap-type` on html/body
- Each slide needs `scroll-snap-align: start`

**Mobile issues:**
- Disable heavy effects at 768px breakpoint
- Test touch events
- Reduce particle count or disable canvas

**Performance issues:**
- Use `will-change` sparingly
- Prefer `transform` and `opacity` animations
- Throttle scroll/mousemove handlers

---

## Related Skills

- **learn** — Generate FORZARA.md documentation for the presentation
- **frontend-design** — For more complex interactive pages beyond slides
- **design-and-refine:design-lab** — For iterating on component designs

---

## Example Session Flow

1. User: "I want to create a pitch deck for my AI startup"
2. Skill asks about purpose, length, content
3. User shares their bullet points and key messages
4. Skill asks about desired feeling (Impressed + Excited)
5. Skill generates 3 style previews
6. User picks Style B (Neon Cyber), asks for darker background
7. Skill generates full presentation with all slides
8. Skill opens the presentation in browser
9. User requests tweaks to specific slides
10. Final presentation delivered

---

## Conversion Session Flow

1. User: "Convert my slides.pptx to a web presentation"
2. Skill extracts content and images from PPT
3. Skill confirms extracted content with user
4. Skill asks about desired feeling/style
5. Skill generates style previews
6. User picks a style
7. Skill generates HTML presentation with preserved assets
8. Final presentation delivered
