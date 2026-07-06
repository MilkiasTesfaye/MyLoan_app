# 👨‍💼 Loan Bot - Admin & Management Guide

## Overview
This guide helps administrators manage applications, monitor bot activity, and maintain the loan database.

---

## Application Management

### Tracking Applications

**Where Applications Are Stored:**
- Console logs (real-time)
- `bot.log` file (requires configuration)
- Can be extended to database or email

**Current Setup:**
Applications print to console with full details:
```
New Application: {
  'timestamp': '2024-01-15 10:30:45',
  'user_id': 123456789,
  'username': 'john_kamau',
  'full_name': 'John Kamau',
  'school_name': 'St. Augustine Primary',
  'country': 'Kenya',
  'location': 'Nairobi',
  'phone': '+254-703-456789',
  'email': 'john@school.ke',
  'loan_type': 'LOAN001',
  'loan_amount': 5000,
  'repayment_period': 36,
  'priority': 'High',
  'comments': 'Need urgently'
}
```

### Application Number System

**Format:** `APP[YYYYMMDDHHMMSS]`

**Example:** `APP20240115103045` = Application from 2024-01-15 at 10:30:45

**Usage:**
- Unique identifier for each application
- Users reference this when following up
- Easy to track in spreadsheet/database

---

## Monitoring & Analytics

### Key Metrics to Track

**Daily:**
- Number of new applications
- Loan types requested
- Total amounts requested
- Countries (geographic distribution)

**Weekly:**
- Approval rate
- Average loan size
- MFI distribution
- Response times

**Monthly:**
- User engagement
- Feature usage
- System issues
- Trend analysis

### Creating an Application Log

**Option 1: Console to File**
```bash
# Run bot and save output to file
python loan_bot.py > bot_output.log 2>&1

# View last 50 applications
tail -100 bot_output.log | grep "New Application"

# Count applications per day
grep "2024-01-15" bot_output.log | grep "New Application" | wc -l
```

**Option 2: Auto-save to Excel (Enhancement)**

Add this to `loan_bot.py` to auto-save applications:

```python
import openpyxl
from datetime import datetime

def save_application_to_excel(app_data):
    """Save each application to Excel file"""
    file_path = 'applications.xlsx'
    
    try:
        wb = openpyxl.load_workbook(file_path)
        ws = wb.active
    except:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(['Timestamp', 'User ID', 'Name', 'School', 'Country', 
                  'Phone', 'Email', 'Loan Type', 'Amount', 'Period', 'Priority'])
    
    ws.append([
        app_data['timestamp'],
        app_data['user_id'],
        app_data['full_name'],
        app_data['school_name'],
        app_data['country'],
        app_data['phone'],
        app_data['email'],
        app_data['loan_type'],
        app_data['loan_amount'],
        app_data['repayment_period'],
        app_data['priority']
    ])
    
    wb.save(file_path)
```

---

## Database Management

### Current Data Structure

**7 MFIs across 4 countries:**

| Country | MFI Name | Phone |
|---------|----------|-------|
| Ethiopia | Peace Microfinance | +251-911-234567 |
| Ethiopia | VisionFund MFI | +251-912-345678 |
| Kenya | DIMKES SACCO | +254-703-456789 |
| Rwanda | Goshen MFI | +250-788-567890 |
| Rwanda | ACB | +250-789-678901 |
| Uganda | Saviour MFI | +256-704-789012 |
| Uganda | Lubaga Teachers SACCO | +256-705-890123 |

### Adding New MFI

1. Open `Loan_Bot_Database_NEW.xlsx`
2. Go to **MFI Master Data** sheet
3. Add new row:
   ```
   MFI008 | New Bank Name | Ethiopia | Description | email@mfi.et | +251-9XX-XXXXXX
   ```
4. Save file
5. Restart bot: `Ctrl+C` then `python loan_bot.py`
6. New MFI appears in bot

### Updating Interest Rates

1. Open `Loan_Bot_Database_NEW.xlsx`
2. Go to **Interest Rates & Terms** sheet
3. Update rates:
   ```
   For LOAN001 (EdTech):     Change "18" to new rate
   For LOAN002 (School Dev): Change "24" to new rate
   For LOAN003 (Development): Change "24" to new rate
   ```
4. Update min/max amounts as needed
5. Update processing fee if needed
6. Save file
7. Restart bot

### Updating Requirements

1. Open `Loan_Bot_Database_NEW.xlsx`
2. Go to **Requirements** sheet
3. Modify requirements:
   ```
   Old: School must be operating for minimum 1 year
   New: School must be operating for minimum 2 years
   ```
4. Save file
5. Restart bot
6. Changes appear immediately for users

### Adding New Loan Product

1. Open `Loan_Bot_Database_NEW.xlsx`
2. Go to **Loan Types** sheet
3. Add row:
   ```
   LOAN004 | Teacher Training Loan | For teacher professional development | All MFIs
   ```
4. Go to **Interest Rates & Terms** sheet
5. Add rates for LOAN004
6. Go to **Requirements** sheet
7. Add any specific requirements for LOAN004
8. Save file
9. Restart bot
10. New loan type appears in calculator and registration

---

## Bot Performance Monitoring

### Resource Usage

**CPU:**
- Typically <5% when idle
- Spikes to 15-25% during active conversations

**Memory:**
- ~100-150 MB usage
- Grows slightly with more concurrent users

**Network:**
- Minimal bandwidth (mostly text)
- ~1-2 MB per 1000 messages

### Checking Bot Status

```bash
# Check if process is running
ps aux | grep loan_bot

# Kill bot if needed (use -9 for force)
kill -9 <process_id>

# Check for errors in logs
tail -50 bot.log | grep ERROR
```

### Common Issues & Solutions

**Issue: Bot responds slowly**
- Solution: Check internet connection, restart bot

**Issue: High CPU usage**
- Solution: Too many concurrent users, upgrade server

**Issue: Memory leak**
- Solution: Restart bot daily during low usage

**Issue: Buttons not updating**
- Solution: Clear Telegram app cache, restart bot

---

## User Support

### Common Support Requests

**"I forgot my application number"**
→ Check user_id in logs, help reconstruct it

**"I didn't receive MFI contact"**
→ Verify phone number was correct, ask user to check status

**"Wrong information submitted"**
→ Get application number, ask user to contact MFI directly with number

**"Calculator gave wrong result"**
→ Check Excel Interest Rates sheet values, verify math

### Response Templates

**Confirmation Email Template:**
```
Subject: Loan Application Received - APP20240115103045

Dear John,

Thank you for submitting your loan application through our bot!

Your Application Number: APP20240115103045
School Name: St. Augustine Primary
Loan Type: EdTech Loan
Amount Requested: $5,000

Next Steps:
1. Our team will review your application
2. We will contact you at +254-703-456789 within 24-48 hours
3. If approved, we'll schedule an interview
4. We may request additional documents

If you have questions, please reply to this email or contact us:
📞 +254-703-456789
📧 info@loanbot.ke

Best regards,
Loan Bot Team
```

---

## System Maintenance

### Daily Tasks
- ✅ Check application count
- ✅ Review any error messages
- ✅ Monitor bot responsiveness

### Weekly Tasks
- ✅ Archive old logs
- ✅ Update statistics
- ✅ Check MFI contact info is current
- ✅ Verify all links work

### Monthly Tasks
- ✅ Update interest rates if changed
- ✅ Add new MFIs if partnered
- ✅ Review user feedback
- ✅ Optimize bot responses
- ✅ Backup database and logs

### Quarterly Tasks
- ✅ Update eligibility requirements
- ✅ Review calculator accuracy
- ✅ Audit submitted applications
- ✅ Test all bot features end-to-end

### Annual Tasks
- ✅ Full security audit
- ✅ Update documentation
- ✅ Plan new features
- ✅ Review cost/benefit analysis

---

## Backup & Recovery

### Backing Up Data

```bash
# Create backup folder
mkdir backups

# Backup Excel database
cp Loan_Bot_Database_NEW.xlsx backups/Loan_Bot_Database_$(date +%Y%m%d).xlsx

# Backup logs
cp bot.log backups/bot_$(date +%Y%m%d).log

# Backup entire project
tar -czf backups/loan_bot_$(date +%Y%m%d).tar.gz loan_bot/
```

### Restoring from Backup

```bash
# Restore Excel file
cp backups/Loan_Bot_Database_20240115.xlsx Loan_Bot_Database_NEW.xlsx

# Restore from full backup
tar -xzf backups/loan_bot_20240115.tar.gz

# Restart bot
python loan_bot.py
```

---

## Security Best Practices

### Protecting Bot Token
- ✅ Store in environment variable (not in code)
- ✅ Never share token publicly
- ✅ Rotate token if compromised
- ✅ Use different token for testing vs production

### Data Privacy
- ✅ Inform users their data is collected
- ✅ Only store necessary information
- ✅ Don't share data with third parties
- ✅ Comply with local data protection laws
- ✅ Have clear privacy policy

### Server Security (if self-hosted)
- ✅ Use firewall
- ✅ Keep OS updated
- ✅ Use strong passwords
- ✅ Enable SSH key authentication
- ✅ Monitor for unauthorized access

---

## Advanced Features to Add

### 1. Email Notifications
```python
import smtplib
from email.mime.text import MIMEText

def send_email(to_address, subject, body):
    # Send confirmation email to applicant
    # Send alert email to admin
```

### 2. Database Integration
```python
import psycopg2  # PostgreSQL
import sqlite3   # SQLite

def save_to_database(app_data):
    # Persistent storage
    # Query applications
    # Generate reports
```

### 3. Admin Dashboard
- Web interface to view applications
- Filter by country, loan type, status
- Export reports
- Manage MFI data

### 4. SMS Notifications
```python
from twilio.rest import Client

def send_sms(phone, message):
    # Alert applicant of approval/denial
    # Send MFI notifications
```

### 5. Multi-Language Support
```python
MESSAGES = {
    'en': {'start': 'Welcome...'},
    'am': {'start': 'ደህና መጡ...'},  # Amharic
    'sw': {'start': 'Karibu...'},   # Swahili
}
```

---

## Analytics & Reporting

### Report Templates

**Daily Report:**
```
Date: 2024-01-15
New Applications: 12
- EdTech: 5
- School Dev: 4
- Development: 3
Top Country: Kenya (5 apps)
Total Amount Requested: $45,000
```

**Monthly Report:**
```
Total Applications: 284
Approval Rate: 78%
Average Loan: $8,750
Total Money Requested: $2,485,000
MFI Distribution:
  - Peace: 45 apps
  - VisionFund: 38 apps
  - DIMKES: 52 apps
  - Others: 149 apps
```

---

## Troubleshooting

### Debug Mode

```python
# Add to loan_bot.py for detailed logging
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Check Specific User

```bash
# Find all messages from user 123456789
grep "123456789" bot.log

# Track user's journey through bot
grep "123456789" bot.log | grep -E "(START|country|MFI|Calculator|Register)"
```

### Test Calculator Math

```python
# Verify loan calculations are correct
amount = 10000
rate = 18
period = 36
payment = calculate_monthly_payment(amount, rate, period)
# Should be around $325.50
```

---

## Cost Analysis (if using cloud servers)

| Service | Cost/Month | Usage |
|---------|-----------|-------|
| Heroku | Free (deprecated) | Legacy support |
| Render.com | $7-20 | Recommended free tier |
| Railway | $5-20 | Good value |
| AWS | $0-50 | Pay per use |
| DigitalOcean | $5-40 | Reliable |
| Replit | Free | Simple projects |

---

## Escalation Procedures

**For User Issues:**
1. Check application number in logs
2. Verify data submitted
3. Contact MFI if application lost
4. Re-submit if necessary

**For Bot Issues:**
1. Check error logs
2. Restart bot
3. Check Excel file integrity
4. Review dependencies

**For MFI Issues:**
1. Verify contact information is current
2. Update if needed
3. Notify other admins
4. Plan mitigation

---

## Contact & Support

**For Technical Issues:**
- Check SETUP_GUIDE.md
- Review bot logs
- Test bot functionality

**For User Support:**
- Provide quick response
- Reference application number
- Escalate to MFI if needed

**For Database Updates:**
- Only one admin edits at a time
- Test changes before deploying
- Restart bot after updates
- Verify changes took effect

---

## Checklist: Weekly Admin Tasks

- [ ] Review new applications (count, trends)
- [ ] Check for error messages
- [ ] Verify bot responsiveness (test /start)
- [ ] Backup database and logs
- [ ] Update MFI contact info if needed
- [ ] Response to any user inquiries
- [ ] Monitor server performance
- [ ] Archive old logs
- [ ] Review analytics
- [ ] Plan for next week

---

This guide covers administrative duties. For user support, share FEATURE_GUIDE.md with them.

**Remember:** Good application tracking = Better user experience!
