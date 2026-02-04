# Gmail Invoice Processor Skill

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.0-green.svg)](CHANGELOG.md)
[![Claude Compatible](https://img.shields.io/badge/claude-compatible-purple.svg)](https://claude.ai)

Automate your invoice workflow by extracting vendor names and amounts from Gmail invoice PDFs and creating organized Excel summaries.

## 🎯 What It Does

This skill enables Claude to:
- 🔍 Search your Gmail inbox for invoice emails
- 📧 Extract invoice data using multi-layered detection
- 💰 Pull vendor names and amounts from PDFs or email bodies
- 📊 Create professional Excel summaries with color-coded status
- 🤖 Automatically handle various invoice formats

## ✨ Key Features

### Multi-Layered PDF Access
- **Layer 1**: Direct PDF download and extraction
- **Layer 2**: Email body text parsing (fallback)
- **Layer 3**: Smart detection when PDFs aren't accessible

### Smart Data Extraction
- Vendor name recognition with pattern matching
- Amount detection in multiple currency formats (USD, EUR, GBP, CAD)
- Invoice number extraction
- Automatic currency detection

### Professional Excel Output
- Color-coded status indicators (🟢 Success, 🟡 Manual Review, 🔴 Not Invoice)
- Formatted amounts with proper decimals and separators
- Detailed notes for follow-up actions
- Summary statistics at bottom
- Frozen header rows for easy scrolling

## 📦 Installation

### Prerequisites
- Claude.ai account with Gmail connected
- Python 3.8+ (for development/testing)

### Quick Install

1. **Download the skill file**:
   ```bash
   wget https://github.com/erafat/skills/releases/download/v2.0/gmail-invoice-processor.skill
   ```

2. **Install in Claude**:
   - Go to Claude.ai → Settings → Skills
   - Click "Add Skill" or "Import Skill"
   - Upload `gmail-invoice-processor.skill`

3. **Connect Gmail**:
   - Go to Claude.ai → Settings → Integrations
   - Connect your Gmail account
   - Grant necessary permissions

## 🚀 Usage

### Basic Usage

Simply ask Claude:

```
"Process my Gmail invoices from the last 30 days"
```

```
"Find all invoice PDFs in my email and create an Excel summary"
```

```
"Search my Gmail for invoices and extract vendor and amount data"
```

### Advanced Usage

**Filter by date**:
```
"Process invoices from January 2026"
```

**Specific search**:
```
"Find invoices from vendor@company.com and summarize them"
```

**Custom date range**:
```
"Get all invoices between 2025-12-01 and 2026-01-31"
```

## 📊 Output Format

The skill creates an Excel file with the following structure:

| Date Processed | Email Subject | Email From | Vendor | Amount | Currency | Extraction Method | Status | Notes |
|----------------|---------------|------------|--------|--------|----------|-------------------|--------|-------|
| 2026-02-03 | Invoice #1234 | vendor@co.com | Acme Corp | 1,250.00 | USD | Layer 2: Email Body | Extracted | Successfully extracted |
| 2026-02-03 | Bill Due | bills@service.com | Services Inc | N/A | USD | Layer 3: Detection | Manual Review | PDF detected but not accessible |

### Status Indicators

- 🟢 **Extracted**: Data successfully extracted from PDF or email
- 🟡 **Manual Review Required**: PDF detected but needs manual download
- 🔴 **Not an Invoice**: Promotional or notification email

## 🛠️ How It Works

### Architecture

```
Gmail API → Multi-Layer Processor → Data Extractor → Excel Generator
              ↓                        ↓
        [Layer 1: PDF]          [Vendor/Amount]
        [Layer 2: Email]        [Currency/Invoice#]
        [Layer 3: Detect]       [Pattern Matching]
```

### Processing Layers

1. **Layer 1: Direct PDF Access**
   - Attempts to download PDF from Gmail API
   - Extracts text using pdfplumber
   - Parses vendor and amount with regex

2. **Layer 2: Email Body Extraction**
   - Decodes email HTML/text content
   - Pattern matches invoice details
   - Handles multiple formats

3. **Layer 3: Detection & Flagging**
   - Detects PDF presence via MIME type and size
   - Flags when API doesn't provide attachment data
   - Clear notes for manual follow-up

## 🧩 Components

### Scripts

- **`extract_invoice_data.py`**: PDF text extraction and parsing
- **`gmail_attachment_helper.py`**: Multi-layer detection and extraction utilities

### References

- **`workflow.md`**: Comprehensive technical guide with code examples
- **`SKILL.md`**: Core instructions for Claude

## 🔧 Development

### Local Testing

1. **Clone the repository**:
   ```bash
   git clone https://github.com/erafat/skills.git
   cd skills/gmail-invoice-processor
   ```

2. **Install dependencies**:
   ```bash
   pip install pdfplumber openpyxl --break-system-packages
   ```

3. **Test extraction script**:
   ```bash
   python scripts/extract_invoice_data.py sample_invoice.pdf
   ```

4. **Test Gmail helper**:
   ```bash
   python scripts/gmail_attachment_helper.py
   ```

### Building from Source

Package the skill for distribution:

```bash
python /path/to/package_skill.py ./gmail-invoice-processor ./dist
```

This creates `gmail-invoice-processor.skill` in the `./dist` directory.

## 📝 Examples

### Example 1: Monthly Expense Report

**User**: "Process all invoices from last month and create an expense report"

**Output**: Excel file with all December invoices, totals by vendor, and currency breakdown

### Example 2: Vendor Analysis

**User**: "Find all invoices from Acme Corp in 2025"

**Output**: Excel summary of all Acme Corp invoices with amounts and dates

### Example 3: Travel Expenses

**User**: "Get flight invoices from my email for Q4 2025"

**Output**: Filtered Excel with travel-related invoices only

## 🐛 Troubleshooting

### Issue: No invoices found

**Solution**: 
- Check Gmail connection in Claude settings
- Verify emails have "invoice" in subject line
- Try broader date range

### Issue: PDF not accessible

**Reason**: Gmail API limitation - doesn't always return attachment data

**Solution**: The skill detects this and flags in Excel with clear instructions to download manually

### Issue: Amount not extracted

**Possible causes**:
- Invoice uses unusual format
- Amount in image (not text)
- Complex multi-page layout

**Solution**: Marked in Excel Notes column for manual entry

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow existing code style
- Add tests for new features
- Update documentation
- Keep SKILL.md concise (< 500 lines)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built for Claude.ai by Anthropic
- Uses pdfplumber for PDF text extraction
- Uses openpyxl for Excel generation

## 📚 Additional Resources

- [Claude Skills Documentation](https://docs.claude.com)
- [Skill Development Guide](docs/DEVELOPMENT.md)
- [API Reference](docs/API.md)
- [Changelog](CHANGELOG.md)

## 💬 Support

- 🐛 [Report a Bug](https://github.com/erafat/skills/issues)
- 💡 [Request a Feature](https://github.com/erafat/skills/issues)
- 📧 [Email Support](mailto:erafatmd@gmail.com)

## 🔗 Links

- [GitHub Repository](https://github.com/erafat/skills)
- [Latest Release](https://github.com/erafat/skills/releases/latest)
- [Documentation](https://github.com/erafat/skills/tree/main/docs)

---

**Version**: 2.0  
**Last Updated**: February 2026  
**Maintained by**: [@erafat](https://github.com/erafat)
