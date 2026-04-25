# Illustration Guide — er-slides

## When to Generate Illustrations

Generate illustrations for:
- Two-column slides (pattern 3) — the right panel
- Three-panel grid slides (pattern 4) — one per panel
- Any slide where a visual makes the concept land faster than words

Skip illustrations for:
- Live demo slides
- Statement/quote slides with a strong headline
- Slides where data or a code snippet is the main content

---

## Generation Script

Use `scripts/gen_illustration.py`. It auto-appends the canonical style suffix.

```bash
# Generate a 4:3 illustration (default — use for all two-col and panel slides)
python3 ~/.claude/skills/er-slides/scripts/gen_illustration.py \
    "A physician in a white coat seated at a desk reviewing a dashboard" \
    slide_output.png

# 1:1 for square panels
python3 ~/.claude/skills/er-slides/scripts/gen_illustration.py \
    "Your subject description" output.png --ratio 1:1
```

API key is read from `~/.baoyu-skills/.env` as `GEMINI_API_KEY`.

---

## Embedding in HTML

Images must be embedded as base64 data URIs — no external file references.

```python
import base64
data = open("slide_output.png", "rb").read()
b64 = base64.b64encode(data).decode()
data_uri = f"data:image/png;base64,{b64}"
# Paste data_uri as the img src
```

HTML usage:
```html
<img src="data:image/png;base64,{{B64}}"
     alt=""
     style="width:100%; height:100%; object-fit:cover; object-position:center;">
```

Always use `object-fit: cover` and keep container aspect-ratio at `4/3`.

---

## The Swiss Editorial Flat Style

### What the script auto-appends

```
Swiss editorial flat illustration, warm ivory cream background filling the entire frame
edge to edge, thin refined ink outlines, muted desaturated palette — off-white coats,
warm cream walls, slate grey and muted gray-blue clothing, natural skin tones,
characters with clearly drawn faces (eyes, nose, mouth), soft natural expressions,
realistic human proportions, diverse representation, no orange no amber no yellow no ochre,
no gradients, no texture, no text, no labels.
```

### Writing good subject prompts

The script handles style — you only describe the subject. Rules:
- Describe **what characters are doing**, not how they look (style handles look)
- Describe **setting elements** (desk, conference table, waiting room chairs, monitor)
- Name the **viewpoint** (seated in profile, standing gesturing toward)
- For faces: add "with visible facial features — eyes nose mouth — " to ensure drawn faces
- Mention **diversity** explicitly if needed ("including one Asian physician and one Black physician")
- End without a period — the script adds a period before the style suffix

### Proven prompts (reference)

**Attending + fellow cognitive scaffold:**
```
A senior physician (white coat) stands in a clinical hallway and turns toward a younger physician
(fellow, white coat). The fellow listens, with a structured thought-map radiating outward from
his head: four labeled branches expanding cleanly. Rendered as a clean diagram, not a bubble cloud
```

**Agent pipeline (attending → team → output):**
```
FAR LEFT — an attending physician in a white coat with warm brown skin, standing and gesturing
toward the right. CENTER — three workers in business casual dark clothing seated at a long shared
desk: first using a magnifying glass over papers, second writing on a notepad, third at a desktop
computer. FAR RIGHT — a large monitor displaying a clean PowerPoint presentation. Subtle left-to-right flow
```

**Billing dashboard (IOM / admin):**
```
A neurophysiologist or clinician with visible facial features seated in profile at a minimal
clean desk, looking at a computer monitor showing a structured billing dashboard with rows of
data in muted gray-blue tones. White medical coat, muted gray-blue trousers. Warm cream wall
behind, subtle doorway or window in background for architectural depth
```

**Waiting room (patient education):**
```
A patient with visible facial features seated comfortably in a waiting room chair, holding and
reading a small illustrated comic pamphlet, gentle engaged expression. Soft waiting room setting
with subtle wall panels or window in background. White coat physician visible in background,
muted gray-blue seating, warm cream walls
```

**Multidisciplinary conference (research / LLM):**
```
Two or three clinicians with visible facial features seated around a small conference table,
one standing and pointing at a large display screen showing structured document cards and a
waveform visualization in muted gray-blue and cream tones. White coats, muted clothing,
warm cream conference room walls, subtle architectural depth
```

---

## Image Positioning Adjustments

If the artwork looks off-center in its container, use transform instead of object-position
(object-position has no effect when `object-fit:contain` and container matches image ratio exactly):

```css
.my-illustration img {
    transform: translate(5%, 3%) scale(1.05);
    transform-origin: center center;
    clip-path: inset(0 round 4px);  /* prevents overflow bleed */
}
```

If hotspots overlay the image, shift them by the same translate values:
```css
.hotspot-1 { left: calc(10% + 5%); top: calc(20% + 3%); }
```

---

## Iteration Tips

- If faces are blank/featureless: add "with visible facial features — eyes nose mouth —" before describing each character
- If there is unwanted text in the image: add "absolutely no text, no labels, no words, no letters anywhere in the image" at the end of your subject prompt
- If colors are too warm/yellow: the style suffix says "no orange no amber no yellow no ochre" — reinforce by adding "strictly neutral cream and slate tones only" to your subject prompt
- If composition is too centered/symmetric: describe an explicit spatial arrangement (left-to-right flow, figure positioned to right with negative space on left)
