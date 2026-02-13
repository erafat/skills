# Changelog

All notable changes to the Gmail Invoice Processor skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-02-03

### Added
- **Multi-layered PDF access strategy** with three fallback layers
- **Email body extraction** as fallback when PDFs aren't accessible
- **Smart PDF detection** using MIME type, size, and content analysis
- **`gmail_attachment_helper.py`** utility script with comprehensive functions:
  - `detect_attachment_presence()` - Detects PDFs even when API doesn't return them
  - `extract_invoice_from_email_body()` - Extracts vendor/amount from email text
  - `process_gmail_message()` - Main processing function
  - `get_recommendation()` - Provides actionable guidance
- **Enhanced Excel output** with:
  - "Extraction Method" column showing which layer was used
  - Color-coded status indicators (green/yellow/red)
  - Detailed notes with specific action items
  - Summary statistics at bottom
  - Larger row heights for readability
- **Comprehensive error handling** for Gmail API limitations
- **Pattern matching improvements** for vendor and amount detection
- **Multi-currency support** (USD, EUR, GBP, CAD)

### Changed
- **SKILL.md** extensively rewritten with three-layer approach documentation
- **workflow.md** updated with complete multi-layer examples
- **Excel column structure** expanded from 7 to 9 columns
- **Status reporting** now uses color-coded cells instead of text-only
- **Error messages** are now more specific and actionable

### Fixed
- **Gmail API attachment limitation** - Now detects when PDFs exist but aren't returned
- **Empty parts array issue** - Skill no longer fails silently when attachments missing
- **Vendor extraction accuracy** - Better pattern matching with false positive filtering
- **Amount detection** - Handles more currency formats and invoice layouts

### Technical Details
- Added size-based detection (emails > 10KB likely have attachments)
- Implemented base64 decoding for email body content
- Enhanced regex patterns for vendor/amount extraction
- Added MIME type checking for attachment detection

## [1.0.0] - 2026-02-03

### Added
- Initial release of Gmail Invoice Processor skill
- Gmail search functionality with subject line filtering
- PDF download and text extraction using pdfplumber
- Basic vendor and amount extraction
- Excel summary generation with openpyxl
- Professional formatting (headers, borders, fonts)
- Date filtering support
- Basic error handling

### Components
- `extract_invoice_data.py` - PDF extraction script
- `SKILL.md` - Core skill instructions
- `workflow.md` - Technical workflow documentation

### Features
- Search Gmail for "invoice" in subject lines
- Download PDF attachments
- Extract vendor names and amounts
- Create formatted Excel spreadsheet
- Support for multiple invoices in batch

### Known Limitations
- Requires PDF attachments to be accessible via Gmail API
- Limited error handling when PDFs not available
- Basic pattern matching for data extraction

---

## Version Comparison

| Feature | v1.0 | v2.0 |
|---------|------|------|
| PDF Extraction | ✅ | ✅ |
| Email Body Extraction | ❌ | ✅ |
| PDF Detection | ❌ | ✅ |
| Multi-layer Fallback | ❌ | ✅ |
| Color-coded Status | ❌ | ✅ |
| Extraction Method Tracking | ❌ | ✅ |
| Enhanced Error Messages | ❌ | ✅ |
| Gmail API Workarounds | ❌ | ✅ |

## Upgrade Guide

### From v1.0 to v2.0

**Breaking Changes**: None - v2.0 is fully backward compatible

**New Features Available**:
1. Skill now extracts data from email bodies when PDFs unavailable
2. Better detection of PDF presence
3. Enhanced Excel output with more columns

**Migration Steps**:
1. Remove v1.0 skill from Claude settings
2. Install v2.0 `.skill` file
3. No configuration changes needed
4. Existing workflows continue to work

**What You'll Notice**:
- More invoices successfully processed automatically
- Clearer feedback on why some invoices need manual review
- Better Excel formatting with color-coded status

## Future Roadmap

### v2.1 (Planned)
- [ ] Support for more email providers (Outlook, Yahoo)
- [ ] Invoice duplicate detection
- [ ] Automatic currency conversion
- [ ] Machine learning-based extraction (experimental)

### v3.0 (Future)
- [ ] Integration with accounting software APIs (QuickBooks, Xero)
- [ ] OCR support for scanned invoices
- [ ] Bulk processing optimization
- [ ] Custom extraction rules per vendor

---

For detailed release notes, see [Releases](https://github.com/erafat/skills/releases).
