# GitHub Repository Setup Instructions

Complete guide to setting up your GitHub repository with the Gmail Invoice Processor skill.

## Repository Structure

```
skills/                                    # Your repository root
├── .github/
│   └── workflows/
│       └── release.yml                    # Automated releases
├── docs/
│   ├── INSTALLATION.md                    # Installation guide
│   ├── EXAMPLES.md                        # Usage examples
│   └── (add more as needed)
├── gmail-invoice-processor/               # Skill source code
│   ├── SKILL.md                          # Core skill instructions
│   ├── scripts/
│   │   ├── extract_invoice_data.py       # PDF extraction
│   │   └── gmail_attachment_helper.py    # Multi-layer utilities
│   └── references/
│       └── workflow.md                   # Technical documentation
├── .gitignore                            # Git ignore rules
├── CHANGELOG.md                          # Version history
├── CONTRIBUTING.md                       # Contribution guidelines
├── LICENSE                               # MIT License
├── QUICKSTART.md                         # 5-minute setup guide
├── README.md                             # Main documentation
├── RELEASE_NOTES_v2.0.md                # Release notes
└── gmail-invoice-processor.skill         # Packaged skill file
```

## Initial Setup

### 1. Create GitHub Repository

**Option A: GitHub Web Interface**

1. Go to https://github.com/new
2. Repository name: `skills`
3. Description: "Claude AI skills for automation and productivity"
4. Visibility: Public (recommended) or Private
5. ✅ Initialize with README (will be replaced)
6. Add .gitignore: Python
7. Add license: MIT License
8. Click "Create repository"

**Option B: GitHub CLI**

```bash
gh repo create skills --public --description "Claude AI skills" --license mit
```

### 2. Clone and Setup

```bash
# Clone your new repo
git clone https://github.com/erafat/skills.git
cd skills

# Copy all files from the package
cp -r /path/to/github-repo-package/* .

# Verify structure
ls -la
```

### 3. Initial Commit

```bash
# Add all files
git add .

# Commit
git commit -m "Initial commit: Gmail Invoice Processor v2.0

- Multi-layered PDF extraction
- Email body parsing fallback  
- Enhanced Excel output
- Comprehensive documentation
"

# Push to GitHub
git push origin main
```

## Creating First Release

### Option 1: GitHub Web Interface

1. Go to your repo: https://github.com/erafat/skills
2. Click "Releases" (right sidebar)
3. Click "Create a new release"
4. Fill in:
   - **Tag**: `v2.0.0`
   - **Release title**: `v2.0.0 - Enhanced Multi-Layer Extraction`
   - **Description**: Copy from `RELEASE_NOTES_v2.0.md`
   - **Attach file**: Upload `gmail-invoice-processor.skill`
5. Click "Publish release"

### Option 2: Using Git Tags

```bash
# Create and push tag
git tag -a v2.0.0 -m "Gmail Invoice Processor v2.0.0"
git push origin v2.0.0

# GitHub Actions will automatically create release (if workflow is set up)
```

### Option 3: GitHub CLI

```bash
# Create release with file
gh release create v2.0.0 \
  gmail-invoice-processor.skill \
  --title "v2.0.0 - Enhanced Multi-Layer Extraction" \
  --notes-file RELEASE_NOTES_v2.0.md
```

## Configuring Repository

### Branch Protection

Recommended settings for `main` branch:

1. Settings → Branches → Add branch protection rule
2. Branch name pattern: `main`
3. Enable:
   - ✅ Require pull request reviews before merging
   - ✅ Require status checks to pass
   - ✅ Require branches to be up to date
4. Save changes

### GitHub Pages (Optional)

Host documentation:

1. Settings → Pages
2. Source: Deploy from branch
3. Branch: `main`, Folder: `/docs`
4. Save
5. Access at: https://erafat.github.io/skills/

### Issue Templates

Create `.github/ISSUE_TEMPLATE/` with:

**bug_report.md:**
```yaml
---
name: Bug Report
about: Report a problem with the skill
title: '[BUG] '
labels: bug
---

**Describe the bug**
A clear description...

**To Reproduce**
Steps to reproduce...

**Expected behavior**
What should happen...
```

**feature_request.md:**
```yaml
---
name: Feature Request
about: Suggest a new feature
title: '[FEATURE] '
labels: enhancement
---

**Feature Description**
What feature would you like...

**Use Case**
Why is this useful...
```

### Dependabot (Security)

Create `.github/dependabot.yml`:

```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
```

## Repository Settings

### Description
```
Claude AI skills for automation and productivity. Currently includes Gmail Invoice Processor for automated invoice extraction and Excel reporting.
```

### Topics (Tags)
```
claude-ai, automation, invoice-processing, gmail, python, excel, pdf-extraction
```

### Website
```
https://erafat.github.io/skills
```

### Social Preview
Upload a preview image (1280x640px recommended):
- Show Excel output example
- Include skill name and tagline
- Add Claude logo

## Maintenance

### Regular Updates

1. **Weekly**: Check issues and discussions
2. **Monthly**: Review pull requests
3. **Quarterly**: Update documentation
4. **Annually**: Review and update dependencies

### Version Management

Follow semantic versioning:

- **Major (v3.0.0)**: Breaking changes
- **Minor (v2.1.0)**: New features, backward compatible
- **Patch (v2.0.1)**: Bug fixes

### Release Process

1. Update CHANGELOG.md
2. Update version in SKILL.md
3. Create release notes
4. Tag and release
5. Announce (Twitter, blog, etc.)

## Promotion

### README Badges

Add to top of README:

```markdown
[![GitHub Release](https://img.shields.io/github/v/release/erafat/skills)](https://github.com/erafat/skills/releases)
[![Downloads](https://img.shields.io/github/downloads/erafat/skills/total)](https://github.com/erafat/skills/releases)
[![Stars](https://img.shields.io/github/stars/erafat/skills)](https://github.com/erafat/skills/stargazers)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
```

### Announcement Templates

**Twitter/X:**
```
🎉 Just released Gmail Invoice Processor v2.0!

✨ Multi-layer extraction
📊 Enhanced Excel output  
🤖 85% automation rate

Perfect for freelancers, small businesses, and anyone drowning in invoice emails.

Download: github.com/erafat/skills

#Claude #Automation #Productivity
```

**Reddit (r/ClaudeAI):**
```
Title: [Release] Gmail Invoice Processor v2.0 - Automated Invoice Extraction

I built a Claude skill that processes invoice emails and creates Excel summaries. 

Key features:
- Multi-layered PDF extraction
- Email body parsing as fallback
- Professional Excel output
- 85% success rate

Open source and free: github.com/erafat/skills

Feedback welcome!
```

## Security

### Secrets Management

Never commit:
- API keys
- Passwords
- Access tokens
- Personal data

Use `.gitignore` and GitHub Secrets for sensitive data.

### Security Policy

Create `SECURITY.md`:

```markdown
# Security Policy

## Reporting Vulnerabilities

Email: erafatmd@gmail.com

**Do not** open public issues for security vulnerabilities.

## Supported Versions

| Version | Supported |
|---------|-----------|
| 2.0.x   | ✅        |
| 1.0.x   | ❌        |
```

## Analytics (Optional)

Track usage and popularity:

1. **GitHub Insights**: Built-in traffic and clone stats
2. **Download Counter**: Track .skill file downloads
3. **Issue/PR Activity**: Monitor community engagement

## Community Building

### Enable Discussions

1. Settings → General → Features
2. Enable "Discussions"
3. Create categories:
   - 💡 Ideas
   - 🙏 Q&A
   - 📣 Announcements
   - 🐛 Bug Reports

### Welcome Message

`.github/welcome.yml`:

```yaml
newIssueWelcomeComment: >
  Thanks for opening your first issue! We'll look into this soon.

newPRWelcomeComment: >
  Thanks for your first contribution! We'll review this shortly.
```

## Backup Strategy

### Automated Backups

1. GitHub automatically backs up your code
2. Consider additional backup to:
   - Local drive (git clone regularly)
   - Cloud storage (Dropbox, etc.)
   - Secondary Git host (GitLab, Bitbucket)

## Next Steps

After setup:

1. ✅ Verify all files committed
2. ✅ Create first release (v2.0.0)
3. ✅ Test download link works
4. ✅ Update README with actual links
5. ✅ Announce release
6. ✅ Monitor issues/discussions

---

**Your GitHub repo is ready!** 🎉

Visit: https://github.com/erafat/skills
