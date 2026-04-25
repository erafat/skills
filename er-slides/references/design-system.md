# Design System — er-slides

All presentations use this design system exactly. Do not deviate from these values.

## Color Tokens

```css
--bg-primary: #f4f2ec;                        /* warm cream — page and slide background */
--bg-panel: rgba(255, 255, 255, 0.78);        /* frosted card surface */
--ink: #101010;                               /* near-black text */
--muted: rgba(16, 16, 16, 0.65);             /* secondary text, labels */
--line: rgba(16, 16, 16, 0.14);              /* borders, dividers */
--accent: #ff4b1f;                            /* coral-orange — use sparingly for emphasis */
--accent-soft: rgba(255, 75, 31, 0.08);      /* tinted accent background */
```

## Typography

### Font Stack

```html
<!-- Always include in <head> -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
```

```css
--font-display: "Archivo", sans-serif;   /* headings — tight tracking, heavy weight */
--font-body:    "IBM Plex Sans", sans-serif;
--font-mono:    "IBM Plex Mono", monospace;  /* kickers, labels, code */
```

### Type Scale (all use clamp for responsive scaling)

```css
--title-size:  clamp(1.8rem, 4.9vw, 4.8rem);
--h2-size:     clamp(1.45rem, 3.4vw, 2.9rem);
--h3-size:     clamp(1.05rem, 2vw, 1.5rem);
--body-size:   clamp(1.22rem, 1.4vw, 1.72rem);
--small-size:  clamp(1.06rem, 1.08vw, 1.22rem);
```

### Heading Rules

```css
h1, h2, h3 {
    font-family: var(--font-display);
    letter-spacing: -0.02em;
    text-wrap: balance;
}
h1 { font-size: var(--title-size); line-height: 0.95; max-width: 14ch; }
h2 { font-size: var(--h2-size);    line-height: 1.02; max-width: 22ch; }
h3 { font-size: var(--h3-size);    line-height: 1.1; }
p  { font-size: var(--body-size);  line-height: 1.56; color: var(--muted); max-width: 72ch; }
```

Kicker (eyebrow label above headings):
```css
.kicker {
    font: 600 var(--small-size)/1 var(--font-mono);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
}
```

## Spacing Tokens

```css
--slide-padding:  clamp(1.1rem, 2.6vw, 2.5rem);   /* inner slide padding */
--content-gap:    clamp(0.65rem, 1.25vw, 1.2rem);  /* gap between major blocks */
--element-gap:    clamp(0.35rem, 0.72vw, 0.72rem); /* gap between small elements */
--stage-margin:   clamp(1rem, 2.8vw, 3rem);        /* margin around 16:9 stage */

/* Content box insets (inside the stage) */
--content-box-top:    clamp(3.9rem, 7vh, 5.1rem);
--content-box-right:  clamp(3.55rem, 5.6vw, 5.7rem);
--content-box-bottom: clamp(4rem, 7.4vh, 5.4rem);
--content-box-left:   clamp(3.55rem, 5.6vw, 5.7rem);
```

## Slide Structure

Every slide uses a **viewport → stage → content** nesting:

```
.slide          100vw × 100dvh, overflow:hidden, scroll-snap-align:start
  └─ .slide-stage   16:9 box constrained to viewport (see below)
       └─ .slide-content  flex column, padding, gap
```

### Stage CSS (16:9 within viewport)

```css
.slide-stage {
    width:  min(calc(100vw - (var(--stage-margin) * 2)), calc((100dvh - (var(--stage-margin) * 2)) * 16 / 9));
    height: min(calc(100dvh - (var(--stage-margin) * 2)), calc((100vw - (var(--stage-margin) * 2)) * 9 / 16));
    max-width: 100vw;
    max-height: 100dvh;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    position: relative;
}
```

### Slide Background

Every `.slide` gets this background (the subtle grid pattern):

```css
.slide {
    background:
        linear-gradient(rgba(16,16,16,0.1) 1px, transparent 1px),
        linear-gradient(90deg, rgba(16,16,16,0.1) 1px, transparent 1px),
        radial-gradient(circle at 18% 15%, rgba(255,255,255,0.72), transparent 38%),
        var(--bg-primary);
    background-size: 4.6vw 4.6vw, 4.6vw 4.6vw, auto, auto;
}
```

## Card Component

```css
.card {
    border: 1px solid var(--ink);
    background: var(--bg-panel);
    backdrop-filter: blur(8px);
    padding: clamp(0.95rem, 1.4vw, 1.6rem);
    display: flex;
    flex-direction: column;
    gap: var(--element-gap);
    box-shadow: 6px 6px 0 rgba(16, 16, 16, 0.06);
}
```

## Reveal Animation

Add `.reveal` to any element to animate it in when the slide becomes visible:

```css
.reveal {
    opacity: 0;
    transform: translateY(1.4rem);
    transition: opacity 0.6s cubic-bezier(0.16,1,0.3,1), transform 0.6s cubic-bezier(0.16,1,0.3,1);
}
.slide.visible .reveal { opacity: 1; transform: translateY(0); }

/* Stagger children using nth-child delay */
.slide.visible .reveal:nth-child(1) { transition-delay: 0.05s; }
.slide.visible .reveal:nth-child(2) { transition-delay: 0.15s; }
.slide.visible .reveal:nth-child(3) { transition-delay: 0.25s; }
.slide.visible .reveal:nth-child(4) { transition-delay: 0.35s; }
.slide.visible .reveal:nth-child(5) { transition-delay: 0.45s; }
```

## Fullscreen Mode

```css
body.is-fullscreen { --stage-margin: clamp(0.3rem, 0.9vw, 0.8rem); }

/* Progress bar and nav dots fade in fullscreen */
body.is-fullscreen #progress,
body.is-fullscreen #navDots { opacity: 0; pointer-events: none; }
```

Keyboard: `F` toggles fullscreen, `Esc` exits.

## Laptop Media Query

Add this block after all base styles. Populate with per-slide tightening as needed:

```css
@media (min-width: 901px) and (max-width: 1440px),
       (min-width: 901px) and (max-height: 860px) {
    :root {
        --title-size: clamp(1.6rem, 4.2vw, 4rem);
        --h2-size:    clamp(1.25rem, 2.9vw, 2.4rem);
        --body-size:  clamp(1.05rem, 1.2vw, 1.45rem);
        --small-size: clamp(0.9rem, 0.94vw, 1.05rem);
        --slide-padding: clamp(0.9rem, 2vw, 2rem);
        --content-gap:   clamp(0.5rem, 0.95vw, 0.95rem);
        --element-gap:   clamp(0.28rem, 0.58vw, 0.58rem);
        --stage-margin:  clamp(0.75rem, 1.7vw, 1.7rem);
    }
    /* Slide-specific overrides go here */
}
```

## Progress Bar + Nav Dots HTML

Always place before the closing `</body>`:

```html
<div id="progress" style="position:fixed;top:0;left:0;height:2px;background:var(--accent);width:0;z-index:100;transition:width 0.3s ease;"></div>
<div id="navDots" style="position:fixed;bottom:1.4rem;left:50%;transform:translateX(-50%);display:flex;gap:0.55rem;z-index:100;"></div>
<button id="fullscreenToggle" style="position:fixed;top:1rem;right:1.4rem;z-index:100;background:rgba(255,255,255,0.82);border:1px solid var(--line);padding:0.45rem 1rem;font:600 0.82rem/1 var(--font-mono);letter-spacing:0.06em;text-transform:uppercase;cursor:pointer;color:var(--muted);">Full screen</button>
```

Nav dot CSS:
```css
#navDots button {
    width: 0.5rem; height: 0.5rem; border-radius: 50%;
    border: 1px solid var(--muted); background: transparent; cursor: pointer;
    transition: background 0.2s, transform 0.2s;
}
#navDots button.active { background: var(--ink); transform: scale(1.3); }
```
