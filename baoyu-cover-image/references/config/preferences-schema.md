---
name: preferences-schema
description: EXTEND.md YAML schema for baoyu-cover-image user preferences
---

# Preferences Schema

## Full Schema

```yaml
---
version: 2

watermark:
  enabled: false
  content: ""
  position: bottom-right  # bottom-right|bottom-left|bottom-center|top-right

preferred_type: null      # hero|conceptual|typography|metaphor|scene|minimal or null for auto-select

preferred_style: null     # Built-in style name or null for auto-select

preferred_text: title-only  # none|title-only|title-subtitle|text-rich

preferred_mood: balanced    # subtle|balanced|bold

default_aspect: "2.35:1"  # 2.35:1|16:9|1:1

quick_mode: false         # Skip confirmation when true

language: null            # zh|en|ja|ko|auto (null = auto-detect)

custom_styles:
  - name: my-style
    description: "Style description"
    color_palette:
      primary: ["#1E3A5F", "#4A90D9"]
      background: "#F5F7FA"
      accents: ["#00B4D8"]
    visual_elements: "Clean lines, geometric shapes"
    typography: "Modern sans-serif"
    best_for: "Business, tech content"
---
```

## Field Reference

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `version` | int | 2 | Schema version |
| `watermark.enabled` | bool | false | Enable watermark |
| `watermark.content` | string | "" | Watermark text (@username or custom) |
| `watermark.position` | enum | bottom-right | Position on image |
| `preferred_type` | string | null | Type name or null for auto |
| `preferred_style` | string | null | Style name or null for auto |
| `preferred_text` | string | title-only | Text density level |
| `preferred_mood` | string | balanced | Mood intensity level |
| `default_aspect` | string | "2.35:1" | Default aspect ratio |
| `quick_mode` | bool | false | Skip confirmation step |
| `language` | string | null | Output language (null = auto-detect) |
| `custom_styles` | array | [] | User-defined styles |

## Type Options

| Value | Description |
|-------|-------------|
| `hero` | Large visual impact, title overlay |
| `conceptual` | Concept visualization, abstract core ideas |
| `typography` | Text-focused layout, prominent title |
| `metaphor` | Visual metaphor, concrete expressing abstract |
| `scene` | Atmospheric scene, narrative feel |
| `minimal` | Minimalist composition, generous whitespace |

## Text Options

| Value | Description |
|-------|-------------|
| `none` | Pure visual, no text elements |
| `title-only` | Single headline (≤8 characters) |
| `title-subtitle` | Title + subtitle (≤15 characters) |
| `text-rich` | Title + subtitle + keyword tags (2-4) |

## Mood Options

| Value | Description |
|-------|-------------|
| `subtle` | Low contrast, muted colors, calm aesthetic |
| `balanced` | Medium contrast, normal saturation, versatile |
| `bold` | High contrast, vivid colors, dynamic energy |

## Position Options

| Value | Description |
|-------|-------------|
| `bottom-right` | Lower right corner (default, most common) |
| `bottom-left` | Lower left corner |
| `bottom-center` | Bottom center |
| `top-right` | Upper right corner |

## Aspect Ratio Options

| Value | Description | Best For |
|-------|-------------|----------|
| `2.35:1` | Cinematic widescreen | Article headers, blog covers |
| `16:9` | Standard widescreen | Presentations, video thumbnails |
| `1:1` | Square | Social media, profile images |

## Custom Style Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique style identifier (kebab-case) |
| `description` | Yes | What the style conveys |
| `color_palette.primary` | No | Main colors (array) |
| `color_palette.background` | No | Background color |
| `color_palette.accents` | No | Accent colors (array) |
| `visual_elements` | No | Decorative elements |
| `typography` | No | Font/lettering style |
| `best_for` | No | Recommended content types |

## Example: Minimal Preferences

```yaml
---
version: 2
watermark:
  enabled: true
  content: "@myhandle"
preferred_type: null
preferred_style: elegant
preferred_text: title-only
preferred_mood: balanced
quick_mode: false
---
```

## Example: Full Preferences

```yaml
---
version: 2
watermark:
  enabled: true
  content: "myblog.com"
  position: bottom-right

preferred_type: conceptual

preferred_style: blueprint

preferred_text: title-subtitle

preferred_mood: subtle

default_aspect: "16:9"

quick_mode: true

language: en

custom_styles:
  - name: corporate-tech
    description: "Professional B2B tech style"
    color_palette:
      primary: ["#1E3A5F", "#4A90D9"]
      background: "#F5F7FA"
      accents: ["#00B4D8", "#48CAE4"]
    visual_elements: "Clean lines, subtle gradients, circuit patterns"
    typography: "Modern sans-serif, professional"
    best_for: "SaaS, enterprise, technical"
---
```

## Migration from v1

When loading v1 schema, auto-upgrade:

| v1 Field | v2 Field | Default Value |
|----------|----------|---------------|
| (missing) | `version` | 2 |
| (missing) | `preferred_text` | title-only |
| (missing) | `preferred_mood` | balanced |
| (missing) | `quick_mode` | false |

v1 `--no-title` flag maps to `preferred_text: none`.
