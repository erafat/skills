# Usage Examples

Real-world examples of using the Gmail Invoice Processor skill.

## Table of Contents

- [Basic Usage](#basic-usage)
- [Date Filtering](#date-filtering)
- [Vendor-Specific](#vendor-specific)
- [Advanced Queries](#advanced-queries)
- [Batch Processing](#batch-processing)
- [Error Handling](#error-handling)

## Basic Usage

### Example 1: Process All Recent Invoices

**Query:**
```
"Process my Gmail invoices from the last 30 days"
```

**What Claude Does:**
1. Searches Gmail: `subject:invoice newer_than:30d`
2. Finds all invoice emails from past month
3. Downloads PDFs or extracts from email body
4. Creates Excel summary with all data

**Expected Output:**
- Excel file: `invoice_summary_YYYYMMDD.xlsx`
- Contains all invoices with vendor, amount, currency
- Color-coded status for each invoice

---

### Example 2: Quick Invoice Check

**Query:**
```
"Do I have any new invoices?"
```

**What Claude Does:**
1. Searches recent emails (last 7 days by default)
2. Lists invoices found
3. Asks if you want Excel summary

**Sample Response:**
```
I found 3 invoices from the last week:
1. Acme Corp - $1,250.00 (Feb 1)
2. Tech Services - $450.50 (Feb 2)
3. Office Supplies Inc - $127.99 (Feb 3)

Would you like me to create an Excel summary?
```

---

### Example 3: Simple Excel Generation

**Query:**
```
"Create a spreadsheet of my invoice emails"
```

**What Claude Does:**
1. Searches all emails with "invoice" in subject
2. Extracts available data
3. Generates Excel with professional formatting

**Excel Columns:**
| Date | Subject | From | Vendor | Amount | Currency | Status | Notes |
|------|---------|------|--------|--------|----------|--------|-------|

---

## Date Filtering

### Example 4: Last Month's Invoices

**Query:**
```
"Get all invoices from January 2026"
```

**Gmail Search Used:**
```
subject:invoice after:2026/01/01 before:2026/02/01
```

**Use Case:**
- Monthly expense reports
- Tax preparation
- Budget tracking

---

### Example 5: Quarter Review

**Query:**
```
"Show me all Q4 2025 invoices"
```

**Gmail Search Used:**
```
subject:invoice after:2025/10/01 before:2026/01/01
```

**Output:**
- Quarterly expense summary
- Grouped by vendor if multiple invoices
- Total amount per currency

---

### Example 6: Year-End Summary

**Query:**
```
"Process all 2025 invoices for tax purposes"
```

**What You Get:**
- Complete year of invoices
- Sorted by date
- Totals by vendor
- Ready for tax filing

---

## Vendor-Specific

### Example 7: Single Vendor Analysis

**Query:**
```
"Find all invoices from Acme Corp in 2025"
```

**Gmail Search Used:**
```
from:@acmecorp.com subject:invoice after:2025/01/01
```

**Output:**
- All Acme Corp invoices
- Total amount paid
- Payment frequency

---

### Example 8: Vendor Comparison

**Query:**
```
"Compare invoices from AWS vs Azure in 2025"
```

**What Claude Does:**
1. Searches both vendors separately
2. Creates Excel with vendor column
3. Calculates totals for each
4. Provides summary comparison

**Sample Summary:**
```
AWS: 12 invoices, Total: $15,432.00
Azure: 8 invoices, Total: $12,890.00
```

---

## Advanced Queries

### Example 9: High-Value Invoices

**Query:**
```
"Find invoices over $1000 from last quarter"
```

**What Claude Does:**
1. Gets all Q4 invoices
2. Filters amounts > $1000
3. Creates focused Excel report

**Use Case:**
- Expense approval workflows
- Budget threshold monitoring
- Large purchase tracking

---

### Example 10: Multiple Search Terms

**Query:**
```
"Get invoices OR receipts OR bills from December"
```

**Gmail Search Used:**
```
subject:(invoice OR receipt OR bill) after:2025/12/01
```

**Captures:**
- Various invoice formats
- Receipts
- Bills
- Payment notifications

---

### Example 11: Exclude Certain Vendors

**Query:**
```
"Get all invoices except from Amazon"
```

**Gmail Search Used:**
```
subject:invoice -from:amazon.com
```

**Use Case:**
- Focus on specific expense categories
- Exclude personal purchases
- Business-only expenses

---

## Batch Processing

### Example 12: Weekly Batch

**Query:**
```
"Process last week's invoices every Monday"
```

**Workflow:**
1. Every Monday, ask Claude
2. Gets previous 7 days
3. Consistent Excel format
4. Track weekly expenses

---

### Example 13: Multiple Currencies

**Query:**
```
"Process international invoices - I have USD, EUR, and GBP"
```

**What Claude Does:**
1. Detects all three currencies
2. Separates in Excel
3. Provides subtotals per currency
4. Notes exchange rates needed

**Excel Structure:**
```
USD Invoices: $5,230.00
EUR Invoices: €2,450.00
GBP Invoices: £1,890.00
```

---

### Example 14: Travel Expenses

**Query:**
```
"Get all flight and hotel invoices from business trips"
```

**Gmail Search Used:**
```
subject:(invoice OR receipt) (flight OR hotel OR airline OR booking)
```

**Output:**
- Travel-specific invoices
- Grouped by trip if possible
- Ready for expense reports

---

## Error Handling

### Example 15: No Invoices Found

**Query:**
```
"Get invoices from November 2026"
```

**Claude Response:**
```
I searched for invoices in November 2026 but didn't find any. 
This could be because:
- The date is in the future
- No emails have "invoice" in the subject
- Different search terms might be needed

Would you like me to try:
1. A different date range?
2. Different search terms like "bill" or "receipt"?
```

---

### Example 16: PDF Not Accessible

**Query:**
```
"Process this invoice email"
```

**Claude Response:**
```
I found the invoice email from Acme Corp (Feb 1):
- Subject: Invoice #12345
- From: billing@acmecorp.com

However, I detected a PDF attachment (48KB) that I couldn't 
access through the Gmail API. 

I've flagged this in the Excel with status "Manual Review Required" 
and a note to download the PDF manually.

Would you like me to:
1. Continue processing other invoices?
2. Try extracting data from the email body instead?
```

---

### Example 17: Partial Extraction

**Query:**
```
"Process all invoices"
```

**Claude Report:**
```
Processed 10 invoices:
✅ 7 successfully extracted (vendors + amounts)
⚠️ 2 need manual review (PDFs not accessible)
❌ 1 not an invoice (promotional email)

Total extracted: $8,450.00 USD

Excel file includes notes on which invoices need follow-up.
```

---

## Combining Features

### Example 18: Monthly Report with Filtering

**Query:**
```
"Create a January 2026 expense report, exclude amounts under $50, group by vendor"
```

**What Claude Does:**
1. Gets January invoices
2. Filters out < $50
3. Groups by vendor
4. Adds summary totals
5. Professional formatting

**Excel Output:**
- Vendor groups with subtotals
- Grand total at bottom
- Filtered as requested
- Ready for reporting

---

### Example 19: Custom Format Request

**Query:**
```
"Process invoices but I need columns: Date, Vendor, Amount, Tax, Total"
```

**Claude Response:**
```
I'll create an Excel with your custom columns. However, I can 
typically only extract:
- Date (from email)
- Vendor (from PDF/email)
- Amount (total)

Tax breakdown is rarely available in the invoice data I can 
access. I'll include a "Tax" column but it may need manual entry.

Proceed with this format?
```

---

### Example 20: Integration with Other Tools

**Query:**
```
"Process invoices and prepare data for QuickBooks import"
```

**What Claude Does:**
1. Extracts invoice data
2. Formats Excel for QuickBooks
3. Includes required fields:
   - Vendor name
   - Invoice number
   - Date
   - Amount
   - Category (if detectable)

**Output:**
- QuickBooks-compatible CSV/Excel
- Import instructions included
- Ready for upload

---

## Tips for Best Results

### 1. Be Specific with Dates
```
Good: "Get invoices from January 1-15, 2026"
Better: "Get invoices from 2026/01/01 to 2026/01/15"
```

### 2. Use Vendor Names
```
Good: "Find invoices from that cloud provider"
Better: "Find invoices from AWS or Amazon Web Services"
```

### 3. Specify Output Needs
```
Good: "Make a spreadsheet"
Better: "Create an Excel summary with vendor, amount, and date columns"
```

### 4. Handle Large Batches
```
Good: "Get all my invoices ever"
Better: "Get 2025 invoices first, then we can do 2024"
```

---

## Common Workflows

### Workflow 1: Weekly Expense Tracking
```
Monday: "Process last week's invoices"
→ Review Excel
→ Update accounting system
→ File for records
```

### Workflow 2: Monthly Close
```
First Monday of month: "Get all last month's invoices"
→ Verify amounts
→ Check for missing invoices
→ Submit expense report
```

### Workflow 3: Tax Preparation
```
January: "Get all 2025 invoices"
→ Group by category
→ Calculate totals
→ Send to accountant
```

---

For more examples, see [Advanced Usage Guide](ADVANCED.md).
