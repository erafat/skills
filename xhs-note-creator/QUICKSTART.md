# xhs-note-creator Quick Start

## Installation Complete ✅

The skill has been successfully installed and all dependencies are ready.

## How to Use

### Invoke the skill
Simply say:
- "Create a Xiaohongshu note about..."
- "Generate XHS content for..."
- "Make a RedNote post about..."

Or use the skill command:
```
/xhs-note-creator
```

## What This Skill Does

1. **Content Writing**: Creates engaging Xiaohongshu-style content with:
   - Eye-catching titles (max 20 characters)
   - Well-formatted body text with emojis
   - SEO-friendly tags

2. **Image Card Generation**: Renders professional cards with:
   - 8 visual themes (default, geometric, neo-brutalism, botanical, professional, retro, terminal, sketch)
   - 4 pagination modes (separator, auto-fit, auto-split, dynamic)
   - Cover image + content cards (1080×1440px, 3:4 ratio)

3. **Publishing** (Optional): Can publish directly to Xiaohongshu
   - Requires XHS_COOKIE configuration

## Themes Available

- `default` - Purple gradient style
- `playful-geometric` - Memphis design style
- `neo-brutalism` - Bold, flat design
- `botanical` - Natural, botanical theme
- `professional` - Business style
- `retro` - Vintage aesthetic
- `terminal` - Command-line style
- `sketch` - Hand-drawn style

## Pagination Modes

- `separator` - Manual page breaks with `---`
- `auto-fit` - Auto-scale text to fit fixed size
- `auto-split` - Auto-split based on content height
- `dynamic` - Dynamic height adjustment (max 4320px)

## Example Usage

The skill will automatically:
1. Write engaging XHS content based on your input
2. Generate a properly formatted Markdown file with YAML frontmatter
3. Render beautiful image cards using Playwright
4. Optionally publish to Xiaohongshu (if configured)

## Technical Details

- **Location**: `~/.claude/skills/xhs-note-creator/`
- **Scripts**:
  - `scripts/render_xhs.py` - Python rendering
  - `scripts/render_xhs.js` - Node.js rendering
  - `scripts/publish_xhs.py` - Publishing script
- **Dependencies**: All installed (markdown, PyYAML, playwright, xhs, etc.)
- **Browser**: Chromium installed via Playwright

## Optional: Publishing Setup

To enable publishing, create a `.env` file:
```bash
XHS_COOKIE=your_cookie_here
```

Get your cookie by:
1. Login to xiaohongshu.com in browser
2. Open DevTools (F12) > Network tab
3. Copy the Cookie header from any request

---

Ready to create amazing Xiaohongshu content! 🚀
