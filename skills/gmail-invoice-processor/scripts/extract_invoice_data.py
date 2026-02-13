#!/usr/bin/env python3
"""
Extract vendor name and invoice amount from PDF invoices.
"""

import sys
import re
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    print("Error: pdfplumber not installed. Install with: pip install pdfplumber --break-system-packages")
    sys.exit(1)


def extract_invoice_data(pdf_path):
    """
    Extract vendor name and amount from an invoice PDF.
    
    Returns:
        dict: {'vendor': str, 'amount': float, 'currency': str, 'filename': str}
    """
    result = {
        'vendor': None,
        'amount': None,
        'currency': 'USD',
        'filename': Path(pdf_path).name
    }
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Extract text from first few pages (invoices typically have key info on first page)
            text = ""
            for page in pdf.pages[:3]:  # Check first 3 pages
                text += page.extract_text() + "\n"
            
            if not text.strip():
                return result
            
            # Extract vendor name (usually at the top of the invoice)
            # Look for common patterns: company names are often in all caps or title case at the top
            lines = text.split('\n')
            for i, line in enumerate(lines[:15]):  # Check first 15 lines
                line = line.strip()
                # Skip very short lines, dates, and numbers
                if len(line) < 3 or re.match(r'^\d+[/\-]\d+', line) or line.isdigit():
                    continue
                # Potential vendor name: longer text, possibly in caps or title case
                if len(line) > 5 and not line.startswith(('Invoice', 'INVOICE', 'Date', 'DATE')):
                    # Clean up common invoice header terms
                    cleaned = re.sub(r'\b(Invoice|INVOICE|Bill|BILL|Statement|STATEMENT)\b', '', line).strip()
                    if cleaned and len(cleaned) > 3:
                        result['vendor'] = cleaned
                        break
            
            # Extract amount - look for common patterns
            # Pattern 1: "Total: $1,234.56" or "Amount Due: $1,234.56"
            amount_patterns = [
                r'(?:Total|TOTAL|Amount Due|AMOUNT DUE|Balance Due|BALANCE DUE|Grand Total|GRAND TOTAL)[\s:]*\$?\s*([\d,]+\.?\d*)',
                r'\$\s*([\d,]+\.\d{2})\s*(?:USD|CAD|EUR)?',  # $1,234.56
                r'(?:USD|CAD|EUR)\s*([\d,]+\.\d{2})',  # USD 1,234.56
            ]
            
            amounts_found = []
            for pattern in amount_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    # Clean and convert
                    clean_amount = match.replace(',', '')
                    try:
                        amount_value = float(clean_amount)
                        if amount_value > 0:
                            amounts_found.append(amount_value)
                    except ValueError:
                        continue
            
            # Use the largest amount found (typically the total)
            if amounts_found:
                result['amount'] = max(amounts_found)
            
            # Try to detect currency
            if re.search(r'\bEUR\b|€', text):
                result['currency'] = 'EUR'
            elif re.search(r'\bGBP\b|£', text):
                result['currency'] = 'GBP'
            elif re.search(r'\bCAD\b', text):
                result['currency'] = 'CAD'
    
    except Exception as e:
        print(f"Error processing {pdf_path}: {str(e)}", file=sys.stderr)
    
    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_invoice_data.py <pdf_file> [pdf_file2 ...]")
        sys.exit(1)
    
    results = []
    for pdf_path in sys.argv[1:]:
        if not Path(pdf_path).exists():
            print(f"File not found: {pdf_path}", file=sys.stderr)
            continue
        
        data = extract_invoice_data(pdf_path)
        results.append(data)
    
    # Output as simple format for easy parsing
    print("FILENAME|VENDOR|AMOUNT|CURRENCY")
    for r in results:
        vendor = r['vendor'] or 'Unknown'
        amount = r['amount'] if r['amount'] is not None else 'N/A'
        print(f"{r['filename']}|{vendor}|{amount}|{r['currency']}")


if __name__ == "__main__":
    main()
