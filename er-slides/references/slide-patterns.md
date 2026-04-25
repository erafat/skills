# Slide Patterns — er-slides

All patterns use the `.slide > .slide-stage > .slide-content` shell. Only the inner content structure varies.

---

## 1. Title Slide

Left-aligned title shell on a clean background. Used for the first slide.

```html
<section class="slide slide-title" aria-label="Slide 1">
    <div class="slide-stage">
    <div class="slide-content" style="align-items:flex-start; justify-content:center; padding:var(--content-box-top) var(--content-box-right) var(--content-box-bottom) var(--content-box-left);">
        <div class="title-shell reveal">
            <p class="kicker">Your Kicker · Date</p>
            <h1>Your Title Here</h1>
            <div class="subtitle-block">
                <p class="subtitle">One-line subtitle or framing statement.</p>
            </div>
            <div class="presenter-line">
                <span>Presenter Name</span>
                <span>Role · Institution</span>
            </div>
        </div>
    </div>
    </div>
</section>
```

```css
.slide-title .title-shell {
    width: min(100%, clamp(30rem, 42vw, 46rem));
    display: grid;
    grid-template-rows: auto auto auto;
    align-content: center;
    gap: clamp(1rem, 1.8vw, 1.6rem);
    padding: clamp(1.8rem, 3vw, 2.8rem);
}
.slide-title h1 { font-size: clamp(2.6rem, 6vw, 5.6rem); line-height: 0.92; max-width: 12ch; }
.presenter-line {
    display: flex; flex-direction: column; gap: 0.28rem;
    margin-top: clamp(2.35rem, 4.2vh, 3.9rem);
    padding-top: clamp(0.75rem, 1.2vw, 1rem);
    border-top: 1px solid rgba(16,16,16,0.22);
    font-size: clamp(0.98rem, 1.15vw, 1.18rem); line-height: 1.3;
}
.presenter-line span:last-child { color: var(--muted); }
```

---

## 2. Statement / Quote Slide

Big headline with optional body copy. Use for one-idea punchy slides.

```html
<section class="slide" aria-label="Slide N">
    <div class="slide-stage">
    <div class="slide-content" style="justify-content:center;">
        <p class="kicker reveal">Section · Context</p>
        <h2 class="reveal">One sentence. A full cognitive scaffold.</h2>
        <p class="reveal">Supporting paragraph — one or two sentences max.</p>
    </div>
    </div>
</section>
```

---

## 3. Two-Column: Text Stack + Illustration (the workhorse)

Left: vertical stack of cards or text blocks. Right: 4:3 illustration panel.
Grid ratio `0.66fr / 1.34fr` gives illustration more room.

```html
<section class="slide" aria-label="Slide N">
    <div class="slide-stage">
    <div class="slide-content">
        <p class="kicker reveal">Section Label</p>
        <h2 class="reveal">Slide Headline</h2>
        <div class="twocol-layout reveal">
            <!-- Left: cards or text blocks -->
            <div class="twocol-left">
                <div class="card node-card">
                    <div class="node-title">Step Label</div>
                    <div class="node-body">Description of this step.</div>
                </div>
                <div class="twocol-arrow">↓</div>
                <div class="card node-card">
                    <div class="node-title">Step Label</div>
                    <div class="node-body">Description.</div>
                </div>
            </div>
            <!-- Right: illustration -->
            <div class="twocol-illustration">
                <img src="data:image/png;base64,..." alt="" style="width:100%;height:100%;object-fit:cover;object-position:center;">
            </div>
        </div>
    </div>
    </div>
</section>
```

```css
.twocol-layout {
    display: grid;
    grid-template-columns: minmax(0, 0.66fr) minmax(0, 1.34fr);
    gap: clamp(1.2rem, 1.9vw, 2rem);
    width: 100%; min-height: 0; align-items: stretch; align-self: center;
}
.twocol-left {
    display: flex; flex-direction: column; gap: clamp(0.5rem, 0.9vw, 0.9rem);
    min-height: 0;
}
.twocol-arrow {
    text-align: center; font-size: var(--h3-size); color: var(--muted);
    height: clamp(1rem, 1.4vh, 1.6rem); line-height: 1;
}
.twocol-illustration { aspect-ratio: 4 / 3; overflow: hidden; }
.node-title { font: 700 clamp(0.94rem, 1.16vw, 1.16rem)/1 var(--font-mono); }
.node-body  { font: 600 clamp(1.1rem, 1.38vw, 1.36rem)/1.28 var(--font-body); margin-top: clamp(0.68rem, 0.98vw, 0.9rem); }
```

---

## 4. Three-Panel Grid

Three equal cards side by side, each with an optional illustration. Used for "three projects" or "three points" slides.

```html
<section class="slide" aria-label="Slide N">
    <div class="slide-stage">
    <div class="slide-content">
        <p class="kicker reveal">Section Label</p>
        <h2 class="reveal">Three Things.</h2>
        <div class="threepanel-grid reveal">
            <div class="card panel-card">
                <div class="panel-illustration">
                    <img src="data:image/png;base64,..." alt="" style="width:100%;height:100%;object-fit:cover;">
                </div>
                <div class="panel-label">Panel Title</div>
                <div class="panel-desc">One or two sentence description.</div>
            </div>
            <!-- repeat × 3 -->
        </div>
    </div>
    </div>
</section>
```

```css
.threepanel-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: clamp(0.8rem, 1.2vw, 1.2rem);
    min-height: 0; flex: 1 1 auto;
}
.panel-card { justify-content: flex-start; padding: clamp(0.7rem, 1vw, 1.1rem); }
.panel-illustration { aspect-ratio: 4/3; overflow: hidden; border-radius: 4px; margin-bottom: var(--element-gap); }
.panel-label { font: 700 clamp(1rem, 1.2vw, 1.2rem)/1.1 var(--font-display); letter-spacing: -0.01em; }
.panel-desc  { font: 400 clamp(0.88rem, 0.96vw, 1rem)/1.4 var(--font-body); color: var(--muted); margin-top: 0.4rem; }
```

---

## 5. Live Demo Slide

Centered label + launch button. Used for presentation pauses where you switch to live tool.

```html
<section class="slide slide-central" aria-label="Slide N">
    <div class="slide-stage">
    <div class="slide-content" style="justify-content:center; align-items:center; padding-top:12%;">
        <p class="kicker live-demo-label reveal">Live Demo</p>
        <div class="live-demo-sub reveal">Brief description of what you will show.</div>
        <button type="button" class="live-demo-btn reveal" id="openDemoBtn"
            data-url="https://example.com">
            <span>▶</span> Open Tool
        </button>
    </div>
    </div>
</section>
```

```css
.live-demo-label { font-size: clamp(2rem, 5vw, 5rem); font-family: var(--font-display); font-weight: 800; color: var(--ink); margin-bottom: 0.8rem; }
.live-demo-sub   { font-size: var(--body-size); color: var(--muted); max-width: 52ch; text-align: center; margin-bottom: 2rem; }
.live-demo-btn {
    display: inline-flex; align-items: center; gap: 0.7rem;
    padding: clamp(0.72rem, 1.1vw, 1.1rem) clamp(1.4rem, 2vw, 2rem);
    background: var(--ink); color: #fff;
    border: none; border-radius: 4px; cursor: pointer;
    font: 600 clamp(0.9rem, 1.05vw, 1.05rem)/1 var(--font-body);
    transition: opacity 0.2s;
}
.live-demo-btn:hover { opacity: 0.82; }
.live-demo-btn.is-launching { opacity: 0.6; pointer-events: none; }
```

JS to wire the button (opens in new tab):
```js
document.getElementById('openDemoBtn')?.addEventListener('click', function() {
    const url = this.dataset.url;
    const a = document.createElement('a');
    a.href = url; a.target = '_blank'; a.rel = 'noopener noreferrer';
    a.style.display = 'none';
    document.body.appendChild(a); a.click(); a.remove();
});
```

---

## 6. Full-Bleed Image with Hotspot Tooltips

Image fills the right half or full stage. Hotspot `<div>` elements overlay clickable areas.

```html
<section class="slide" aria-label="Slide N">
    <div class="slide-stage">
    <div class="slide-content" style="grid-template-rows: auto minmax(0,1fr); display:grid; overflow:visible;">
        <p class="kicker reveal">Label</p>
        <div class="hotspot-layout reveal">
            <img src="data:image/png;base64,..." alt=""
                style="width:100%;height:100%;object-fit:contain;display:block;">
            <div class="hotspot" data-tip="Tooltip text here" style="left:10%;top:15%;width:20%;height:60%;"></div>
        </div>
    </div>
    </div>
</section>
```

```css
.hotspot-layout { position: relative; min-height: 0; align-self: center; justify-self: center; height: 100%; overflow: visible; }
.hotspot { position: absolute; cursor: pointer; }
.hotspot::after {
    content: attr(data-tip);
    position: absolute; left: 105%; top: 50%; transform: translateY(-50%);
    background: var(--ink); color: #fff;
    padding: 0.55rem 0.85rem; border-radius: 6px;
    font: 500 clamp(0.82rem, 0.9vw, 0.96rem)/1.35 var(--font-body);
    white-space: nowrap; opacity: 0; pointer-events: none;
    transition: opacity 0.2s;
}
.hotspot:hover::after { opacity: 1; }
```

---

## 7. Evidence / Comparison Grid (2 columns)

Two cards side by side for before/after, compare/contrast, or stat pairs.

```html
<div class="evidence-grid">
    <div class="card">
        <p class="kicker">Before</p>
        <h3>Left heading</h3>
        <p>Content.</p>
    </div>
    <div class="card">
        <p class="kicker">After</p>
        <h3>Right heading</h3>
        <p>Content.</p>
    </div>
</div>
```

```css
.evidence-grid {
    display: grid;
    grid-template-columns: 1.1fr 0.9fr;
    gap: var(--content-gap);
    align-items: stretch; min-height: 0;
}
```

---

## 8. Mocked Chat UI Slide

Full-slide interactive chatbot mockup. Used to demonstrate before/after chatbot usage.
This pattern is complex — see the workshop's `presentation.html` slide-1 as the reference implementation.

Key elements:
- `.chat-shell`: `grid-template-columns: sidebar-width 1fr`
- `.chat-sidebar`: conversation list, brand mark, "New chat" button
- `.chat-main`: `grid-template-rows: topbar thread composer`
- `.sidebar-item[data-chat-id]`: clickable conversation items
- JS `initChatMock()`: wires sidebar buttons to swap `mockUserPrompt` / `mockAssistantOutput` innerHTML

Use this when you need a live-feeling demo of chatbot interactions on a slide.

---

## Slash Decoration

The accent diagonal slash element used in some slides:

```html
<div class="slash" aria-hidden="true"></div>
```

```css
.slash {
    width: clamp(6rem, 19vw, 13rem);
    height: clamp(0.55rem, 1.15vw, 1.12rem);
    background: var(--accent);
    transform: rotate(-34deg);
    margin-left: auto; margin-top: auto;
}
```
