# Gmail Invoice Processor Skill

A Claude skill that automates the workflow of finding invoice PDFs in Gmail, extracting key information (vendor names and amounts), and creating organized Excel summaries.

## Features

### 🔍 Smart Invoice Detection
- Searches Gmail for emails with "invoice" in the subject line
- Identifies PDF attachments even when Gmail API doesn't return them
- Detects invoice data in email bodies as a fallback

### 📊 Multi-Layered Data Extraction

**Layer 1: PDF Direct Access**
- Downloads PDF attachments when available via API
- Extracts vendor names and amounts using pattern recognition

**Layer 2: Email Body Parsing**
- Extracts invoice details directly from email text when PDFs aren't accessible
- Smart pattern matching for various invoice formats
- Finds vendor names, amounts, invoice numbers

**Layer 3: Detection & Flagging**
- Identifies when PDFs exist but aren't accessible
- Provides clear recommendations for manual processing
- Includes size estimates and context

### 📈 Professional Excel Output

Creates formatted spreadsheets with:
- Date processed, email subject, sender
- Vendor name and invoice amount
- Extraction method used (PDF, email body, or manual)
- Color-coded status indicators
- Detailed notes for follow-up actions
- Summary statistics

## Installation

1. Download the `gmail-invoice-processor.skill` file
2. In Claude.ai, go to Settings → Skills
3. Click "Add Skill" and upload the file
4. Connect your Gmail account if not already connected

## Usage

Once installed, simply ask Claude:

```
"Process my Gmail invoices and create an Excel summary"
"Find all invoices from the last 30 days"
"Download invoice PDFs from my email and summarize them"
```

## Components

### Scripts

**`extract_invoice_data.py`**
- Automated vendor and amount extraction from PDF files
- Uses pdfplumber for PDF parsing
- Pattern matching for common invoice formats

**`gmail_attachment_helper.py`**
- Enhanced Gmail PDF detection
- Email body text extraction
- Multi-layered processing recommendations

### References

**`workflow.md`**
- Complete step-by-step processing guide
- Code examples for each extraction layer
- Error handling patterns
- Best practices and tips

### Documentation

**`SKILL.md`**
- Main skill instructions for Claude
- Workflow steps and decision trees
- Bundled resources documentation

## Excel Output Format

| Date Processed | Email Subject | Email From | Vendor | Amount | Currency | Extraction Method | Status | Notes |
|----------------|---------------|------------|--------|--------|----------|-------------------|--------|-------|
| 2026-02-03 | Invoice #1234 | Acme Corp | Acme Corporation | 1,250.00 | USD | Layer 2: Email Body | Extracted | Successfully extracted |

**Status Indicators:**
- 🟢 **Extracted** - Data successfully retrieved
- 🟡 **Manual Review Required** - PDF detected but not accessible
- 🔴 **Not an Invoice** - Promotional or notification email

## Requirements

- Python 3.8+
- pdfplumber (`pip install pdfplumber --break-system-packages`)
- openpyxl (automatically installed)
- Gmail account connected to Claude

## Technical Details

### Pattern Recognition

**Vendor Detection:**
- Company name patterns with common suffixes (Inc, LLC, Ltd, Corp)
- Position-based extraction (typically at top of invoice)
- False positive filtering

**Amount Detection:**
- Multiple currency formats ($1,234.56, USD 1234.56)
- "Total", "Amount Due", "Balance Due" patterns
- Selects largest amount as invoice total

**PDF Detection:**
- MIME type analysis (multipart/mixed)
- Size estimation (emails >10KB likely have attachments)
- Subject/snippet keyword matching

## Limitations

- Gmail API may not return PDF attachments in some cases (handled by fallback layers)
- Invoice formats vary widely - some may require manual review
- External invoice links (e.g., on vendor websites) cannot be accessed automatically
- Works only with Gmail accounts

## Version History

**v2.0** (February 2026)
- Added multi-layered extraction approach
- Enhanced PDF detection even when API doesn't return data
- Email body parsing as fallback
- Improved Excel formatting with status colors
- Added extraction method tracking

**v1.0** (February 2026)
- Initial release
- Basic Gmail search and PDF download
- Simple extraction script
- Excel summary generation

## License

See LICENSE.txt for complete terms.

## Contributing

This skill was created for use with Claude.ai. Feedback and suggestions welcome!

## Support

For issues or questions:
1. Check the SKILL.md documentation
2. Review the workflow.md reference guide
3. Provide feedback through Claude's interface

---

**Created by:** Claude AI Assistant  
**Last Updated:** February 3, 2026  
**Compatible with:** Claude.ai with Gmail integration
