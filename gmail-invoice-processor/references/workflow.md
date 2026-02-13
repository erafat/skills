# Gmail Invoice Processing Workflow

This document provides detailed guidance for processing invoice PDFs from Gmail and creating Excel summaries.

## Complete Workflow Steps

### 1. Search Gmail for Invoice PDFs

Use the `search_gmail_messages` tool with the query parameter to find emails containing invoices:

```python
# Search for emails with "invoice" or "invoices" in subject line
query = 'subject:(invoice OR invoices) has:attachment filename:pdf'
```

Key search operators:
- `subject:(invoice OR invoices)` - Matches subject line
- `has:attachment` - Only emails with attachments
- `filename:pdf` - Only PDF attachments
- Add date filters if needed: `after:YYYY/MM/DD before:YYYY/MM/DD`

### 2. Extract Message and Thread Information

For each message returned:
- Get the message ID from results
- Use `read_gmail_thread` tool to get full thread details including attachments
- Look for PDF attachments in the message parts

### 3. Download PDF Attachments

PDF attachments in Gmail can be challenging due to API limitations. Use a multi-layered approach:

#### Layer 1: Direct Attachment Access (Ideal)

```python
import base64
from pathlib import Path

# Check if parts array has PDF attachments
for part in message['payload'].get('parts', []):
    if part.get('mimeType') == 'application/pdf':
        attachment_id = part['body'].get('attachmentId')
        filename = part.get('filename', 'invoice.pdf')
        
        # If data is present directly
        if 'data' in part.get('body', {}):
            attachment_data = part['body']['data']
            pdf_bytes = base64.urlsafe_b64decode(attachment_data)
            output_path = Path('/home/claude') / filename
            output_path.write_bytes(pdf_bytes)
```

#### Layer 2: Detect Attachment Presence (When parts array is empty)

Use the bundled `scripts/gmail_attachment_helper.py`:

```python
from scripts.gmail_attachment_helper import detect_attachment_presence

detection = detect_attachment_presence(message)

if detection['likely_pdf'] and detection['parts_empty']:
    # PDF exists but not accessible via API
    # Flag for manual processing
    note = f"PDF detected ({detection['size_estimate']} bytes) but not accessible - requires manual download"
```

#### Layer 3: Extract from Email Body (Fallback)

```python
from scripts.gmail_attachment_helper import extract_invoice_from_email_body

email_data = extract_invoice_from_email_body(message)

if email_data['vendor'] and email_data['amount']:
    # Successfully extracted from email
    vendor = email_data['vendor']
    amount = email_data['amount']
    invoice_number = email_data['invoice_number']
```

**Complete example:**

```python
# Try all approaches
pdfs_downloaded = []
invoice_data = []

for message in messages:
    # Approach 1: Try direct attachment
    pdf_saved = False
    for part in message['payload'].get('parts', []):
        if part.get('mimeType') == 'application/pdf' and 'data' in part.get('body', {}):
            # Download PDF
            filename = save_pdf_attachment(part)
            pdfs_downloaded.append(filename)
            pdf_saved = True
            break
    
    # Approach 2: Extract from email body
    if not pdf_saved:
        email_data = extract_invoice_from_email_body(message)
        if email_data['amount']:
            invoice_data.append({
                'source': 'email_body',
                'vendor': email_data['vendor'],
                'amount': email_data['amount'],
                'subject': get_subject(message)
            })
        else:
            # Approach 3: Flag for manual processing
            detection = detect_attachment_presence(message)
            invoice_data.append({
                'source': 'manual_required',
                'note': f"PDF detected but not accessible",
                'subject': get_subject(message)
            })
```

### 4. Extract Invoice Data

Use the bundled `scripts/extract_invoice_data.py` script:

```bash
python scripts/extract_invoice_data.py invoice1.pdf invoice2.pdf invoice3.pdf
```

The script outputs a pipe-delimited format:
```
FILENAME|VENDOR|AMOUNT|CURRENCY
invoice1.pdf|Acme Corp|1250.00|USD
invoice2.pdf|Tech Supplies Inc|3500.50|USD
```

**Manual Extraction Alternative**: If the script doesn't extract data accurately, manually extract using pdfplumber:

```python
import pdfplumber

with pdfplumber.open('invoice.pdf') as pdf:
    text = pdf.pages[0].extract_text()
    # Parse text for vendor and amount
```

### 5. Create Excel Summary

Use openpyxl to create a professional Excel spreadsheet with:
- Header row with bold formatting
- Columns: Date Processed, Filename, Vendor, Amount, Currency, Status/Notes
- Professional styling (fonts, borders, column widths)
- Data validation or formatting rules

**Excel Structure**:
```
| Date Processed | Email Subject | Filename | Vendor | Amount | Currency | Notes |
|----------------|---------------|----------|--------|---------|----------|-------|
| 2026-02-03     | Invoice #1234 | inv.pdf  | Acme   | 1250.00 | USD      |       |
```

### 6. Save and Present Results

- Save Excel file to `/mnt/user-data/outputs/`
- Use `present_files` tool to share with user
- Provide summary of results (number of invoices processed, total amounts, any issues)

## Error Handling

### PDF Extraction Issues
- If vendor name unclear: Mark as "Unknown - Review Required"
- If amount not found: Mark as "N/A - Manual Review Needed"
- Include original filename for reference

### Gmail API Limitations
- Attachment data might be truncated; check `body.size` field
- Some large PDFs may need special handling
- Respect rate limits when processing many emails

## Tips for Better Results

1. **Date Filtering**: Use Gmail date operators to limit search scope
2. **Batch Processing**: Process PDFs in batches if many results
3. **Validation**: Cross-check extracted amounts make sense (not too large/small)
4. **Currency Handling**: Note different currencies; don't mix in totals without conversion
5. **Duplicate Detection**: Check for duplicate filenames or invoice numbers
