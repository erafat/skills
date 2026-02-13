# Quick Start Guide

Get up and running with Gmail Invoice Processor in 5 minutes.

## Prerequisites

- ✅ Claude.ai account
- ✅ Gmail account  
- ✅ Web browser

## Installation (2 minutes)

### 1. Download Skill
```bash
# Direct download
https://github.com/erafat/skills/releases/download/v2.0/gmail-invoice-processor.skill

# Or using wget
wget https://github.com/erafat/skills/releases/download/v2.0/gmail-invoice-processor.skill
```

### 2. Install in Claude
1. Go to [claude.ai](https://claude.ai)
2. Settings → Skills → Add Skill
3. Upload `gmail-invoice-processor.skill`
4. Click Install

### 3. Connect Gmail
1. Settings → Integrations → Gmail
2. Click Connect
3. Sign in and grant permissions

## First Use (1 minute)

### Try These Commands:

**Basic:**
```
"Process my Gmail invoices from the last 30 days"
```

**With Date Filter:**
```
"Get all invoices from January 2026"
```

**Specific Vendor:**
```
"Find invoices from Acme Corp"
```

## What You Get

### Excel Output with:
- ✅ Vendor names
- ✅ Invoice amounts  
- ✅ Currencies
- ✅ Extraction method
- ✅ Color-coded status
- ✅ Detailed notes

### Example Output:

| Date | Subject | Vendor | Amount | Status |
|------|---------|--------|--------|--------|
| 2026-02-03 | Invoice #123 | Acme Corp | $1,250.00 | 🟢 Extracted |
| 2026-02-03 | Bill from Services | Services Inc | N/A | 🟡 Manual Review |

## Common Issues

### "No invoices found"
- Check emails have "invoice" in subject
- Try broader date range
- Verify Gmail connected

### "PDF not accessible"  
- Normal! Skill flags for manual download
- Data extracted from email body when possible
- See Excel notes for details

### "Gmail won't connect"
- Try disconnecting and reconnecting
- Check Google account permissions
- Use different browser if needed

## Next Steps

1. 📖 Read [Full Documentation](README.md)
2. 🎯 Try [More Examples](docs/EXAMPLES.md)  
3. 🔧 Explore [Advanced Features](docs/ADVANCED.md)

## Need Help?

- 🐛 [Report Issue](https://github.com/erafat/skills/issues)
- 💬 [Ask Question](https://github.com/erafat/skills/discussions)
- 📧 [Email Support](mailto:erafatmd@gmail.com)

---

**Ready to process invoices!** 🚀

Try: `"Process my invoices from last week"`
