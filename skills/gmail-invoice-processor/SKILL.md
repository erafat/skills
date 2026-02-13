---
name: gmail-invoice-processor
description: "Process invoice PDFs from Gmail inbox and create Excel summaries. Use this skill when the user wants to: (1) Download PDF invoices from Gmail, (2) Extract vendor names and amounts from invoice PDFs, (3) Create or update Excel spreadsheets summarizing invoice data, (4) Search for invoices in Gmail by subject line (containing 'invoice' or 'invoices'), (5) Automate invoice tracking or expense reporting from email. Trigger when user mentions Gmail invoices, PDF invoices in email, expense tracking from Gmail, or creating invoice summaries in Excel."
---

# Gmail Invoice Processor

Automate the workflow of finding invoice PDFs in Gmail, extracting key information (vendor name and amount), and creating organized Excel summaries.

## Quick Start

1. Search Gmail for invoice emails
2. Download PDF attachments
3. Extract vendor and amount data
4. Create formatted Excel summary
5. Present results to user

## Workflow Steps

### Step 1: Search Gmail for Invoices

Use `search_gmail_messages` with search query targeting subject lines:

```python
query = 'subject:(invoice OR invoices) has:attachment filename:pdf'
```

Add date filters if needed: `after:2025/01/01` or `newer_than:30d`

### Step 2: Download PDF Attachments

**IMPORTANT**: Gmail API attachment handling has known limitations. Attachments may not be returned in the parts array even when they exist.

#### Approach A: Check for Attachment Parts (Preferred)
For each message with PDFs:
1. Use `read_gmail_thread` or `read_gmail_message` to get message details
2. Check if `payload.parts` array contains items with `mimeType: 'application/pdf'`
3. If found, decode base64 attachment data and save to `/home/claude/`

Example:
```python
import base64
from pathlib import Path

# Check message payload for parts
if message['payload'].get('parts'):
    for part in message['payload']['parts']:
        if part.get('mimeType') == 'application/pdf' or part.get('filename', '').endswith('.pdf'):
            # Extract attachment
            if 'data' in part.get('body', {}):
                attachment_data = part['body']['data']
                pdf_bytes = base64.urlsafe_b64decode(attachment_data)
                filename = part.get('filename', 'invoice.pdf')
                Path(filename).write_bytes(pdf_bytes)
```

#### Approach B: Extract Data from Email Body (Fallback)
When PDFs aren't accessible via API, extract invoice data directly from email text:

```python
import re

email_body = message['payload']['body'].get('data', '')
if email_body:
    # Decode email body
    decoded_body = base64.urlsafe_b64decode(email_body).decode('utf-8', errors='ignore')
    
    # Search for common invoice patterns
    vendor_match = re.search(r'(?:from|vendor|company)[:\s]+([A-Za-z0-9\s&.,]+)', decoded_body, re.IGNORECASE)
    amount_match = re.search(r'\$\s*([0-9,]+\.[0-9]{2})', decoded_body)
    
    vendor = vendor_match.group(1).strip() if vendor_match else 'Unknown'
    amount = amount_match.group(1).replace(',', '') if amount_match else 'N/A'
```

#### Approach C: Detect and Flag for Manual Processing
If neither approach works:
1. Check `mimeType: 'multipart/mixed'` and `sizeEstimate` to confirm attachments exist
2. Note in Excel: "PDF attachment exists but not accessible via API - manual download required"
3. Include email subject and sender for reference

**Detection logic:**
```python
has_attachment = (
    message['payload'].get('mimeType') in ['multipart/mixed', 'multipart/related'] and
    message.get('sizeEstimate', 0) > 10000 and  # Larger than text-only
    not message['payload'].get('parts')  # But parts array is empty
)

if has_attachment:
    note = "PDF attachment detected but not accessible - manual download required"
```

### Step 3: Extract Invoice Data

Use the bundled extraction script for automated parsing:

```bash
python scripts/extract_invoice_data.py invoice1.pdf invoice2.pdf
```

Output format: `FILENAME|VENDOR|AMOUNT|CURRENCY`

The script uses pattern matching to find:
- **Vendor**: Company name (typically at top of first page)
- **Amount**: Total/Amount Due/Balance Due values
- **Currency**: USD (default), EUR, GBP, CAD

**If extraction quality is poor**, manually extract using pdfplumber and regex patterns.

### Step 4: Create Excel Summary

Create a professional Excel file with:

**Required columns:**
- Date Processed (when you processed it)
- Email Subject (subject line of the email)
- Filename (original PDF name)
- Vendor (extracted company name)
- Amount (invoice total)
- Currency (USD, EUR, etc.)
- Notes (for manual review flags or issues)

**Formatting standards:**
- Header row: Bold, filled background (light blue/gray)
- Font: Arial or similar professional font
- Column widths: Auto-fit to content
- Amount column: Number format with 2 decimals, thousands separator
- Borders: Light borders around all cells

**Use openpyxl** for creation:
```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment

wb = Workbook()
ws = wb.active
ws.title = "Invoice Summary"

# Headers
headers = ['Date Processed', 'Email Subject', 'Filename', 'Vendor', 'Amount', 'Currency', 'Notes']
ws.append(headers)

# Style header row
for cell in ws[1]:
    cell.font = Font(bold=True)
    cell.fill = PatternFill(start_color="D3D3D3", fill_type="solid")
```

Save to `/mnt/user-data/outputs/invoice_summary_YYYYMMDD.xlsx`

### Step 5: Present Results

1. Use `present_files` tool to share the Excel file
2. Provide concise summary:
   - Number of invoices processed
   - Total amount (by currency if multiple)
   - Any invoices needing manual review

## Bundled Resources

### Scripts
- **scripts/extract_invoice_data.py**: Automated vendor and amount extraction from invoice PDFs
  - Requires: pdfplumber (`pip install pdfplumber --break-system-packages`)
  - Usage: `python extract_invoice_data.py file1.pdf file2.pdf ...`
  - Returns pipe-delimited output for easy parsing

- **scripts/gmail_attachment_helper.py**: Enhanced Gmail PDF detection and email body extraction
  - Detects PDF attachments even when Gmail API parts array is empty
  - Extracts invoice data from email body text as fallback
  - Provides recommendations for handling different scenarios
  - Usage: Import functions in main processing workflow

### References
- **references/workflow.md**: Comprehensive step-by-step guide with code examples, error handling, multi-layered PDF access strategies, and tips for better results

## Error Handling

**PDF attachments not accessible**: 
- Gmail API may not return attachment data in parts array even when attachments exist
- Indicators: `mimeType: 'multipart/mixed'`, large `sizeEstimate`, but empty `parts` array
- Solutions:
  1. Extract data from email body text if invoice details are included
  2. Flag in Excel with note: "PDF detected but not accessible - manual download required"
  3. Advise user to download PDF manually from Gmail for processing

**Missing data**: If vendor or amount cannot be extracted, mark as "Unknown - Review Required" or "N/A - Manual Review Needed" in Excel with note

**Large attachments**: Some Gmail attachments may be truncated; check attachment size and handle appropriately

**Multiple currencies**: List separately by currency; don't sum different currencies together

**Email body extraction**: When PDFs aren't accessible, parse email body HTML/text for invoice details:
```python
# Common patterns in email bodies
patterns = {
    'amount': r'\$\s*([0-9,]+\.[0-9]{2})',
    'total': r'(?:total|amount due|balance)[:\s]*\$?\s*([0-9,]+\.?[0-9]*)',
    'vendor': r'(?:from|vendor|company)[:\s]+([A-Za-z0-9\s&.,]+)',
    'invoice_number': r'(?:invoice|inv|ref)[\s#:]+([A-Za-z0-9-]+)'
}
```

## Tips

- Start with date-filtered searches to avoid processing old invoices: `newer_than:30d`
- Use multi-layered approach for PDF access: try direct attachment → extract from email body → flag for manual download
- Test the `gmail_attachment_helper.py` script to detect attachment presence even when parts array is empty
- Invoice formats vary widely; some may need manual data entry in Excel
- Save original filenames and email subjects for traceability
- When PDFs aren't accessible via API, parse email body HTML/text for invoice details
- Create clear notes in Excel for items requiring manual review to track follow-up needed
