# Contributing to Gmail Invoice Processor

First off, thanks for taking the time to contribute! 🎉

The following is a set of guidelines for contributing to the Gmail Invoice Processor skill. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Skill Development Guidelines](#skill-development-guidelines)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Style Guides](#style-guides)

## Code of Conduct

This project and everyone participating in it is governed by our commitment to fostering an open and welcoming environment. Please be respectful and constructive in your interactions.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When you create a bug report, include as many details as possible:

**Bug Report Template**:

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce:
1. Ask Claude to '...'
2. See error '...'

**Expected behavior**
What you expected to happen.

**Screenshots/Excel Output**
If applicable, attach the generated Excel file or screenshots.

**Environment:**
- Claude.ai version
- Gmail account type (personal/workspace)
- Date range of invoices tested

**Additional context**
Any other context about the problem.
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. Create an issue and provide:

- **Clear title and description** of the enhancement
- **Use case**: Why is this enhancement useful?
- **Proposed solution**: How should it work?
- **Alternatives considered**: What other approaches did you think about?

### Pull Requests

1. Fork the repo and create your branch from `main`
2. Make your changes following our style guides
3. Test your changes thoroughly
4. Update documentation as needed
5. Submit a pull request

## Development Setup

### Prerequisites

```bash
# Required
- Python 3.8+
- pip

# For testing
- Gmail account
- Sample invoice PDFs
```

### Installation

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/skills.git
cd skills
cd gmail-invoice-processor

# Install dependencies
pip install pdfplumber openpyxl --break-system-packages

# Verify installation
python scripts/extract_invoice_data.py --help
```

### Testing Locally

```bash
# Test PDF extraction
python scripts/extract_invoice_data.py test_invoices/*.pdf

# Test Gmail helper (without API calls)
python scripts/gmail_attachment_helper.py
```

## Skill Development Guidelines

### Keep SKILL.md Concise

- SKILL.md should be < 500 lines
- Move detailed documentation to `references/`
- Use progressive disclosure pattern

### Script Requirements

All scripts in `scripts/` must:
- Have clear docstrings
- Include usage examples in docstring
- Handle errors gracefully
- Work without loading into context (when possible)

### Reference Files

Files in `references/` should:
- Be loaded only when needed
- Contain detailed documentation
- Include code examples
- Be well-organized with clear sections

## Testing

### Manual Testing Checklist

Before submitting, test with:

- [ ] Emails with PDF attachments
- [ ] Emails without attachments (email body only)
- [ ] Various invoice formats (different vendors)
- [ ] Date filtering
- [ ] Empty search results
- [ ] Multiple currencies
- [ ] Large PDFs (> 1MB)

### Test Cases to Add

When adding new features, include test cases in your PR description:

```python
# Example test case
def test_vendor_extraction():
    """Test that vendor names are correctly extracted"""
    email_body = "Invoice from Acme Corp..."
    result = extract_invoice_from_email_body(email_body)
    assert result['vendor'] == 'Acme Corp'
```

## Submitting Changes

### Commit Messages

Use clear, descriptive commit messages:

```
Good:
✅ Add multi-currency support to extraction script
✅ Fix vendor name regex to handle special characters
✅ Update SKILL.md with Layer 3 detection examples

Bad:
❌ Fixed bug
❌ Update
❌ asdf
```

Format: `<type>: <description>`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style changes (formatting)
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance tasks

### Pull Request Process

1. **Update documentation**: README, CHANGELOG, etc.
2. **Test thoroughly**: Include test results in PR description
3. **Update version**: Follow semantic versioning
4. **Request review**: Tag maintainers
5. **Address feedback**: Respond to review comments

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe testing performed:
- [ ] Manual testing with sample invoices
- [ ] Edge cases tested
- [ ] Different invoice formats

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] No breaking changes (or documented)
- [ ] Tests pass locally
```

## Style Guides

### Python Style

Follow PEP 8 with these specifics:

```python
# Good
def extract_vendor_name(text: str) -> str:
    """
    Extract vendor name from invoice text.
    
    Args:
        text: Raw invoice text
        
    Returns:
        Vendor name or 'Unknown' if not found
    """
    pattern = r'(?:from|vendor)[:\s]+([A-Za-z0-9\s&.,\'-]+)'
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else 'Unknown'

# Bad
def extract_vendor(t):
    p=r'(?:from|vendor)[:\s]+([A-Za-z0-9\s&.,\'-]+)'
    m=re.search(p,t,re.IGNORECASE)
    return m.group(1).strip() if m else 'Unknown'
```

### Markdown Style

- Use descriptive headers
- Include code examples in fenced blocks
- Use tables for structured data
- Keep line length reasonable (~100 chars)

### SKILL.md Style

- Use imperative/infinitive form ("Extract data", not "Extracts data")
- Keep instructions concise
- Include code examples inline
- Reference other files when appropriate

## Recognition

Contributors will be recognized in:
- README.md Contributors section
- Release notes for their contributions
- GitHub contributor graph

## Questions?

Feel free to:
- Open an issue with the `question` label
- Email: erafatmd@gmail.com
- Start a discussion in GitHub Discussions

---

Thank you for contributing! 🙌
