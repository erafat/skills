# Installation Guide

Complete guide to installing and configuring the Gmail Invoice Processor skill.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Install](#quick-install)
- [Manual Install](#manual-install)
- [Gmail Setup](#gmail-setup)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### Required
- **Claude.ai account** (Free or Pro)
- **Gmail account** (Personal or Workspace)
- **Web browser** (Chrome, Firefox, Safari, or Edge)

### Optional (for development)
- **Python 3.8+** 
- **pip** package manager
- **Git** for cloning repository

## Quick Install

### Step 1: Download the Skill

Choose one method:

**Option A: Direct Download**
1. Go to [Releases](https://github.com/erafat/skills/releases/latest)
2. Download `gmail-invoice-processor.skill`
3. Save to your Downloads folder

**Option B: Using wget**
```bash
wget https://github.com/erafat/skills/releases/download/v2.0/gmail-invoice-processor.skill
```

**Option C: Using curl**
```bash
curl -L -O https://github.com/erafat/skills/releases/download/v2.0/gmail-invoice-processor.skill
```

### Step 2: Install in Claude

1. **Open Claude.ai**
   - Go to [claude.ai](https://claude.ai)
   - Sign in to your account

2. **Access Settings**
   - Click your profile picture (top-right)
   - Select "Settings" from dropdown

3. **Navigate to Skills**
   - Click "Skills" in the left sidebar
   - Or directly go to Settings → Skills

4. **Add the Skill**
   - Click "Add Skill" or "Import Skill" button
   - Select the downloaded `.skill` file
   - Click "Upload" or "Install"

5. **Confirm Installation**
   - You should see "Gmail Invoice Processor" in your skills list
   - Status should show as "Active" or "Enabled"

### Step 3: Connect Gmail

1. **Go to Integrations**
   - Settings → Integrations
   - Or Settings → Connected Services

2. **Find Gmail**
   - Look for "Gmail" in the list
   - Click "Connect" button

3. **Authorize Access**
   - Sign in to your Google account
   - Review permissions requested:
     - Read emails
     - Search mailbox
     - Access attachments
   - Click "Allow" or "Grant Access"

4. **Verify Connection**
   - Gmail should show as "Connected"
   - Green indicator or checkmark

### Step 4: Test the Skill

Ask Claude:
```
"Process my Gmail invoices from the last 30 days"
```

You should see:
1. Claude searching your Gmail
2. Processing invoice emails
3. Creating an Excel summary
4. Providing download link

## Manual Install

### For Developers or Custom Setup

#### Clone the Repository

```bash
# Clone the repo
git clone https://github.com/erafat/skills.git
cd skills
cd gmail-invoice-processor

# Or download ZIP
wget https://github.com/erafat/skills/archive/refs/heads/main.zip
unzip main.zip
cd skills-main
cd gmail-invoice-processor
```

#### Install Dependencies (Optional)

Only needed if you want to run scripts locally:

```bash
# Install Python packages
pip install pdfplumber openpyxl --break-system-packages

# Verify installation
python -c "import pdfplumber; import openpyxl; print('Dependencies OK')"
```

#### Build the Skill

If you need to rebuild the `.skill` file:

```bash
# You'll need the packaging script from Claude Skills SDK
python /path/to/package_skill.py ./gmail-invoice-processor ./dist

# This creates: ./dist/gmail-invoice-processor.skill
```

Then follow Step 2 above to install in Claude.

## Gmail Setup

### Personal Gmail Account

1. **Enable IMAP** (usually enabled by default)
   - Gmail → Settings → Forwarding and POP/IMAP
   - Enable IMAP
   - Save changes

2. **App Password** (if using 2FA)
   - Not required for Claude integration
   - OAuth handles authentication

### Google Workspace Account

1. **Admin May Need to Enable**
   - Admin console → Apps → Google Workspace
   - Enable Claude.ai access
   - Grant necessary permissions

2. **User Authorization**
   - Individual users still need to connect
   - Follow Gmail connection steps above

### Permission Details

The skill needs these Gmail permissions:

| Permission | Purpose | Required |
|------------|---------|----------|
| **Read emails** | Search for invoices | ✅ Yes |
| **View attachments** | Download PDFs | ✅ Yes |
| **View metadata** | Get subjects, senders, dates | ✅ Yes |

**Not required**:
- ❌ Send emails
- ❌ Delete emails
- ❌ Modify emails
- ❌ Manage labels

## Verification

### Test the Installation

#### Test 1: Basic Search
```
"Search my Gmail for invoices"
```
Expected: Claude finds invoice emails

#### Test 2: Date Filtering
```
"Find invoices from last week"
```
Expected: Claude filters by date

#### Test 3: Full Processing
```
"Process invoices and create Excel"
```
Expected: Excel file generated and provided

### Verify Components

Check that all skill components are working:

```bash
# If installed locally, test scripts:

# Test PDF extraction
python scripts/extract_invoice_data.py sample.pdf

# Test Gmail helper
python scripts/gmail_attachment_helper.py

# Both should run without errors
```

## Troubleshooting

### Issue: Skill not appearing in Claude

**Solutions:**
1. Refresh Claude.ai page
2. Clear browser cache
3. Try different browser
4. Re-upload the `.skill` file
5. Check file wasn't corrupted during download

### Issue: Gmail won't connect

**Solutions:**

1. **Check Google Account Settings**
   - Go to myaccount.google.com
   - Security → Third-party apps
   - Ensure Claude is allowed

2. **Re-authorize**
   - Disconnect Gmail in Claude
   - Reconnect and grant permissions again

3. **Try Incognito/Private Window**
   - Rules out browser extension conflicts

4. **Check Workspace Restrictions**
   - If using Google Workspace, admin may need to enable

### Issue: No invoices found

**Solutions:**

1. **Verify Email Format**
   - Emails need "invoice" in subject
   - Or use custom search: `subject:bill`

2. **Check Date Range**
   - Default may be too restrictive
   - Try: "all invoices" or specific date range

3. **Test Gmail Connection**
   - Ask: "What's in my Gmail inbox?"
   - Verifies connection works

### Issue: PDF extraction fails

**Expected Behavior:**
- Skill should still work using email body extraction
- Check Excel "Extraction Method" column

**If Completely Failing:**
1. Check PDF isn't password-protected
2. Verify PDF contains text (not scanned image)
3. Try different invoice

### Issue: Excel file won't download

**Solutions:**
1. Check browser download settings
2. Disable download blockers
3. Try different browser
4. Check available disk space

### Issue: Permission errors

**Solutions:**
1. Re-authorize Gmail connection
2. Check Google Account permissions
3. Try disconnecting/reconnecting
4. Contact support if persistent

## Getting Help

If issues persist:

1. **Check Documentation**
   - [README.md](../README.md)
   - [API Reference](API.md)
   - [FAQ](FAQ.md)

2. **GitHub Issues**
   - Search existing issues
   - Create new issue with details
   - Include error messages

3. **Contact**
   - Email: erafatmd@gmail.com
   - GitHub: [@erafat](https://github.com/erafat)

## Next Steps

After installation:
1. Read [Usage Guide](USAGE.md)
2. Try [Example Queries](EXAMPLES.md)
3. Explore [Advanced Features](ADVANCED.md)

---

**Installation complete!** 🎉

Ready to process your first batch of invoices.
