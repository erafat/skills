---
name: baoyu-post-to-wechat
description: Posts content to WeChat Official Account (微信公众号) via Chrome CDP automation. Supports article posting (文章) with full markdown formatting and image-text posting (图文) with multiple images. Use when user mentions "发布公众号", "post to wechat", "微信公众号", or "图文/文章".
---

# Post to WeChat Official Account

## Script Directory

**Agent Execution**: Determine this SKILL.md directory as `SKILL_DIR`, then use `${SKILL_DIR}/scripts/<name>.ts`.

| Script | Purpose |
|--------|---------|
| `scripts/wechat-browser.ts` | Image-text posts (图文) |
| `scripts/wechat-article.ts` | Article posting (文章) |
| `scripts/md-to-wechat.ts` | Markdown → WeChat HTML |

## Preferences (EXTEND.md)

Use Bash to check EXTEND.md existence (priority order):

```bash
# Check project-level first
test -f .baoyu-skills/baoyu-post-to-wechat/EXTEND.md && echo "project"

# Then user-level (cross-platform: $HOME works on macOS/Linux/WSL)
test -f "$HOME/.baoyu-skills/baoyu-post-to-wechat/EXTEND.md" && echo "user"
```

┌────────────────────────────────────────────────────────┬───────────────────┐
│                          Path                          │     Location      │
├────────────────────────────────────────────────────────┼───────────────────┤
│ .baoyu-skills/baoyu-post-to-wechat/EXTEND.md           │ Project directory │
├────────────────────────────────────────────────────────┼───────────────────┤
│ $HOME/.baoyu-skills/baoyu-post-to-wechat/EXTEND.md     │ User home         │
└────────────────────────────────────────────────────────┴───────────────────┘

┌───────────┬───────────────────────────────────────────────────────────────────────────┐
│  Result   │                                  Action                                   │
├───────────┼───────────────────────────────────────────────────────────────────────────┤
│ Found     │ Read, parse, apply settings                                               │
├───────────┼───────────────────────────────────────────────────────────────────────────┤
│ Not found │ Use defaults                                                              │
└───────────┴───────────────────────────────────────────────────────────────────────────┘

**EXTEND.md Supports**: Default theme | Auto-submit preference | Chrome profile path

## Usage

### Image-Text (图文)

```bash
npx -y bun ${SKILL_DIR}/scripts/wechat-browser.ts --markdown article.md --images ./images/
npx -y bun ${SKILL_DIR}/scripts/wechat-browser.ts --title "标题" --content "内容" --image img.png --submit
```

### Article (文章)

```bash
npx -y bun ${SKILL_DIR}/scripts/wechat-article.ts --markdown article.md --theme grace
```

## Detailed References

| Topic | Reference |
|-------|-----------|
| Image-text parameters, auto-compression | [references/image-text-posting.md](references/image-text-posting.md) |
| Article themes, image handling | [references/article-posting.md](references/article-posting.md) |

## Feature Comparison

| Feature | Image-Text | Article |
|---------|------------|---------|
| Multiple images | ✓ (up to 9) | ✓ (inline) |
| Markdown support | Title/content extraction | Full formatting |
| Auto compression | ✓ (title: 20, content: 1000 chars) | ✗ |
| Themes | ✗ | ✓ (default, grace, simple) |

## Prerequisites

- Google Chrome
- First run: log in to WeChat Official Account (session preserved)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Not logged in | First run opens browser - scan QR to log in |
| Chrome not found | Set `WECHAT_BROWSER_CHROME_PATH` env var |
| Paste fails | Check system clipboard permissions |

## Extension Support

Custom configurations via EXTEND.md. See **Preferences** section for paths and supported options.
