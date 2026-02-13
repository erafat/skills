#!/usr/bin/env python3
"""
Enhanced Gmail PDF attachment detection and extraction helper
"""

import base64
import re
from pathlib import Path


def detect_attachment_presence(message):
    """
    Detect if a message likely has attachments even if parts array is empty.
    
    Returns:
        dict: {
            'has_attachment': bool,
            'likely_pdf': bool,
            'size_estimate': int,
            'mime_type': str
        }
    """
    payload = message.get('payload', {})
    mime_type = payload.get('mimeType', '')
    size = message.get('sizeEstimate', 0)
    parts = payload.get('parts', [])
    
    # Check for attachment indicators
    has_multipart = mime_type in ['multipart/mixed', 'multipart/related']
    has_size = size > 10000  # Larger than typical text-only email
    has_empty_parts = len(parts) == 0
    
    # Check subject/snippet for PDF mentions
    subject = next((h['value'] for h in payload.get('headers', []) if h['name'] == 'Subject'), '')
    snippet = message.get('snippet', '')
    mentions_pdf = bool(re.search(r'\b(pdf|invoice|attachment)\b', subject + snippet, re.IGNORECASE))
    
    return {
        'has_attachment': has_multipart and has_size,
        'likely_pdf': has_multipart and has_size and mentions_pdf,
        'size_estimate': size,
        'mime_type': mime_type,
        'parts_empty': has_empty_parts
    }


def extract_invoice_from_email_body(message):
    """
    Extract invoice data from email body when PDF is not accessible.
    
    Returns:
        dict: {
            'vendor': str or None,
            'amount': float or None,
            'invoice_number': str or None,
            'source': 'email_body'
        }
    """
    result = {
        'vendor': None,
        'amount': None,
        'invoice_number': None,
        'source': 'email_body'
    }
    
    # Get email body text
    payload = message.get('payload', {})
    body_data = payload.get('body', {}).get('data', '')
    
    if not body_data:
        # Check parts for text/plain or text/html
        for part in payload.get('parts', []):
            if part.get('mimeType') in ['text/plain', 'text/html']:
                body_data = part.get('body', {}).get('data', '')
                if body_data:
                    break
    
    if not body_data:
        return result
    
    try:
        # Decode body
        decoded = base64.urlsafe_b64decode(body_data).decode('utf-8', errors='ignore')
    except:
        return result
    
    # Extract vendor (look for common patterns)
    vendor_patterns = [
        r'(?:from|vendor|billed by|company)[:\s]+([A-Za-z0-9\s&.,\'-]+?)(?:\n|<br|$)',
        r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+(?:Inc|LLC|Ltd|Corp|Company|Co)\.?))',
    ]
    
    for pattern in vendor_patterns:
        match = re.search(pattern, decoded, re.IGNORECASE | re.MULTILINE)
        if match:
            vendor = match.group(1).strip()
            # Clean up common false positives
            if len(vendor) > 3 and vendor.lower() not in ['invoice', 'total', 'amount', 'dear']:
                result['vendor'] = vendor
                break
    
    # Extract amount
    amount_patterns = [
        r'\$\s*([0-9]{1,3}(?:,?[0-9]{3})*\.[0-9]{2})',  # $1,234.56
        r'(?:total|amount due|amount|balance|bill amount)[:\s]*\$?\s*([0-9,]+\.[0-9]{2})',
        r'([0-9]{1,3}(?:,?[0-9]{3})*\.[0-9]{2})\s*(?:USD|CAD|EUR)',
    ]
    
    amounts_found = []
    for pattern in amount_patterns:
        matches = re.findall(pattern, decoded, re.IGNORECASE)
        for match in matches:
            clean_amount = match.replace(',', '')
            try:
                amount_val = float(clean_amount)
                if 0 < amount_val < 1000000:  # Sanity check
                    amounts_found.append(amount_val)
            except:
                continue
    
    # Use largest amount found (typically the total)
    if amounts_found:
        result['amount'] = max(amounts_found)
    
    # Extract invoice number
    invoice_patterns = [
        r'(?:invoice|inv|reference)[\s#:]+([A-Za-z0-9-]+)',
        r'#([A-Za-z0-9-]{4,})',
    ]
    
    for pattern in invoice_patterns:
        match = re.search(pattern, decoded, re.IGNORECASE)
        if match:
            result['invoice_number'] = match.group(1).strip()
            break
    
    return result


def process_gmail_message(message):
    """
    Main processing function for a Gmail message.
    Attempts multiple approaches to extract invoice data.
    
    Returns:
        dict: Complete invoice extraction result
    """
    detection = detect_attachment_presence(message)
    
    # Try to extract from email body
    email_data = extract_invoice_from_email_body(message)
    
    # Get subject for context
    payload = message.get('payload', {})
    subject = next((h['value'] for h in payload.get('headers', []) if h['name'] == 'Subject'), 'Unknown')
    sender = next((h['value'] for h in payload.get('headers', []) if h['name'] == 'From'), 'Unknown')
    
    return {
        'message_id': message.get('id'),
        'subject': subject,
        'sender': sender,
        'detection': detection,
        'extracted_data': email_data,
        'recommendation': get_recommendation(detection, email_data)
    }


def get_recommendation(detection, email_data):
    """
    Provide recommendation on how to handle this invoice.
    """
    if email_data['amount'] and email_data['vendor']:
        return "Data extracted from email body successfully"
    elif detection['likely_pdf'] and detection['parts_empty']:
        return "PDF attachment detected but not accessible - manual download required"
    elif not detection['has_attachment']:
        return "No PDF attachment detected - may be notification email only"
    else:
        return "Unable to extract data - manual review needed"


if __name__ == "__main__":
    print("Gmail PDF Attachment Detection and Extraction Helper")
    print("=" * 60)
    print("\nThis script provides utilities for:")
    print("1. Detecting PDF attachments even when parts array is empty")
    print("2. Extracting invoice data from email body text")
    print("3. Providing recommendations for handling different scenarios")
    print("\nUsage: Import functions in your main processing script")
