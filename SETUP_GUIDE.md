# 🤖 Telegram Loan Bot - Setup & Deployment Guide

## Overview
This is a fully functional Telegram bot that helps schools find microfinance institutions (MFIs), calculate loans, and register for educational financing programs across East Africa (Ethiopia, Kenya, Rwanda, Uganda).

## Features
✅ **MFI Directory** - Browse all microfinance institutions by country  
✅ **Loan Calculator** - Calculate monthly payments, interest, and amortization schedules  
✅ **Registration System** - Complete loan application form with validation  
✅ **Interest Rate Information** - View loan terms and eligibility requirements  
✅ **Multi-country Support** - Ethiopia, Kenya, Rwanda, Uganda  
✅ **Professional Formatting** - Clean, user-friendly interface with inline buttons

---

## Prerequisites

### 1. Get a Telegram Bot Token
1. Open Telegram and search for **@BotFather**
2. Type `/newbot` and follow the instructions
3. You'll receive a token like: `123456789:ABCDefGhIjKlMnOpQrStUvWxYz`
4. Save this token securely

### 2. System Requirements
- Python 3.8 or higher
- pip (Python package manager)
- 100MB free disk space
- Internet connection

---

## Installation Steps

### Step 1: Clone/Download Files
```bash
# Create a project directory
mkdir loan_bot
cd loan_bot

# Copy these files into the directory:
# - loan_bot.py
# - requirements.txt
# - Loan_Bot_Database_NEW.xlsx
# - SETUP_GUIDE.md (this file)
```

### Step 2: Install Dependencies
```bash
# Create virtual environment (recommended)
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### Step 3: Add Your Bot Token
Open `loan_bot.py` and find this line (around line 600):
```python
application = Application.builder().token("YOUR_BOT_TOKEN_HERE").build()
```

Replace `YOUR_BOT_TOKEN_HERE` with your actual token from BotFather:
```python
application = Application.builder().token("123456789:ABCDefGhIjKlMnOpQrStUvWxYz").build()
```

### Step 4: Verify Excel File Path
The bot expects the Excel file at:
```
/mnt/user-data/uploads/Loan_Bot_Database_NEW.xlsx
```

If you're running locally, update the path in `loan_bot.py` (line ~110):
```python
EXCEL_DATA = load_excel_data('/path/to/your/Loan_Bot_Database_NEW.xlsx')
```

### Step 5: Run the Bot
```bash
python loan_bot.py
```

You should see:
```
2024-01-15 10:30:45 - telegram.ext - INFO - Application started
```

---

## Usage Guide

### Starting the Bot
1. Open Telegram
2. Search for your bot by name (as you named it with BotFather)
3. Send `/start` command
4. You'll see the main menu with 4 options:
   - 🏦 MFI List
   - 📊 Loan Calculator
   - 📋 Register
   - ❓ FAQ

### Main Features

#### 1. **MFI List** 🏦
```
Flow:
1. Select Country (Ethiopia, Kenya, Rwanda, Uganda)
2. View all MFIs in that country with contact details
3. Select an MFI to see loan products
4. View loan details, interest rates, and requirements
```

#### 2. **Loan Calculator** 📊
```
Flow:
1. Select loan type (EdTech, School Development, Development)
2. Enter loan amount (USD 1,000 - 50,000)
3. Select repayment period (24, 36, 48, 60 months)
4. View:
   - Monthly payment amount
   - Total interest charged
   - Total amount to repay
   - First 6 months payment schedule
```

**Example Output:**
```
💰 Loan Calculation Results

Loan Details:
Original Amount: $10,000
Processing Fee (5%): $500
Total Principal: $10,500
Annual Interest Rate: 18%
Repayment Period: 36 months

Monthly Payment: $325.50
Total Interest: $2,718
Total Amount to Pay: $12,718

📋 First 6 Months Schedule:
Month 1: Payment $325.50 | Principal $181.50 | Interest $144.00
Month 2: Payment $325.50 | Principal $183.64 | Interest $141.86
...
```

#### 3. **Register** 📋
Collects the following information:
- Full name
- School name
- Country
- District/Zone/City
- Phone number
- Email address
- Preferred loan type
- Loan amount
- Repayment period
- Application priority (High/Medium/Low)
- Optional comments

**After submission:**
- Displays application number
- Shows submitted information
- Confirms next steps

#### 4. **FAQ** ❓
Quick answers to common questions:
- What is a loan calculator?
- What are eligibility requirements?
- Can I change loan details after applying?

---

## Data Structure

### Excel Sheets
The bot reads data from these sheets:

1. **MFI Master Data** - All microfinance institutions
2. **Loan Types** - Available loan products
3. **Requirements** - Eligibility criteria
4. **Interest Rates & Terms** - Pricing information
5. **Calculator Settings** - Configuration
6. **Registration Fields** - Form field definitions
7. **Countries** - Country codes and currencies

### Current Data
```
MFIs: 7 institutions across 4 countries
- Ethiopia: Peace Microfinance, VisionFund MFI
- Kenya: DIMKES SACCO
- Rwanda: Goshen MFI, ACB
- Uganda: Saviour MFI, Lubaga Teachers SACCO

Loan Types: 3
- EdTech Loan (18% APR)
- School Development Loan (24% APR)
- Development Loan (24% APR)

Loan Range: USD 1,000 - 50,000
Repayment: 24 - 60 months
```

---

## Deployment Options

### Option 1: Local Machine (Development)
```bash
python loan_bot.py
```
✓ Easy for testing
✗ Bot stops when you close the terminal

### Option 2: Cloud Server (Recommended for Production)

#### Deploy on **Heroku** (Free tier no longer available)
Use **Render.com** or **Railway.app** instead:

1. Create account on Render.com
2. Push code to GitHub
3. Connect repository to Render
4. Set environment variable:
   ```
   BOT_TOKEN=your_token_here
   ```
5. Deploy

#### Deploy on **AWS EC2** or **DigitalOcean**
1. Rent a virtual server ($5-10/month)
2. SSH into server
3. Install Python, clone your code
4. Use `nohup python loan_bot.py &` or **systemd service**

#### Deploy on **Replit** (Free, simple)
1. Go to replit.com
2. Create new Python project
3. Upload files
4. Click Run
5. Bot runs continuously

---

## Configuration

### Customize Bot Messages
Edit strings in `loan_bot.py`:
- Welcome message (line ~200)
- MFI descriptions (update Excel file)
- Loan requirements (update Excel file)

### Modify Loan Terms
Update **Interest Rates & Terms** sheet in Excel:
- Interest rates
- Min/max amounts
- Repayment periods
- Processing fees

### Add/Remove MFIs
Edit **MFI Master Data** sheet:
- Add new MFI rows
- Bot automatically displays them

### Update Requirements
Edit **Requirements** sheet:
- Add/remove eligibility requirements
- Bot displays them in loan details

---

## Troubleshooting

### Issue: "Bot token not recognized"
**Solution:** Double-check your token from BotFather, ensure no extra spaces

### Issue: "Excel file not found"
**Solution:** Verify file path in line ~110, ensure file exists in that location

### Issue: "Bot doesn't respond"
**Solutions:**
1. Check internet connection
2. Ensure bot is running (no errors in terminal)
3. Try `/start` command
4. Restart the bot

### Issue: "Keyboard buttons not showing"
**Solution:** Telegram sometimes needs app restart. Try:
1. Force close Telegram
2. Reopen and send `/start`

### Issue: "Calculator giving wrong results"
**Solution:** Check Excel Interest Rates sheet, ensure numeric values (not text)

---

## Security Notes

⚠️ **Important:**
- **Never** share your bot token publicly
- Store token in environment variables for production
- Don't commit token to GitHub

```python
# Better approach using environment variables:
import os
token = os.getenv('BOT_TOKEN')
application = Application.builder().token(token).build()
```

---

## Monitoring & Maintenance

### View Bot Activity
Applications are logged to console. In production, save to file:

```python
# Add to main() function:
logging.basicConfig(
    filename='bot.log',
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

### Update MFI Data
1. Edit Loan_Bot_Database_NEW.xlsx
2. Restart bot: `Ctrl+C` then `python loan_bot.py`
3. Changes take effect immediately

### Regular Tasks
- Weekly: Review submitted applications
- Monthly: Update interest rates if needed
- As needed: Add new MFIs or loan products

---

## API References

### Telegram Bot API
- Full documentation: https://core.telegram.org/bots/api
- Python library: https://python-telegram-bot.readthedocs.io/

### Loan Calculation Formula
Monthly Payment = P × [r(1+r)^n] / [(1+r)^n - 1]

Where:
- P = Principal amount
- r = Monthly interest rate (annual ÷ 12)
- n = Number of months

---

## Support & Contact

### Getting Help
1. Check the Troubleshooting section above
2. Review Telegram Bot documentation
3. Check Python-telegram-bot GitHub issues
4. Review bot logs for error messages

### Common Commands for Users
- `/start` - Start the bot
- `/cancel` - Cancel current action
- `/help` - Show help (optional, add if needed)

---

## Future Enhancements

Potential features to add:
- 💾 Save draft applications
- 📧 Email confirmation of applications
- 🔐 User authentication & dashboard
- 📱 WhatsApp bot integration
- 🌐 Web portal for reviewing applications
- 📊 Admin dashboard
- 🔔 Push notifications for application status
- 🗣️ Multi-language support

---

## File Structure
```
loan_bot/
├── loan_bot.py                          # Main bot code
├── requirements.txt                     # Python dependencies
├── Loan_Bot_Database_NEW.xlsx           # Database
├── SETUP_GUIDE.md                       # This file
├── bot.log                              # Activity logs (auto-created)
└── venv/                               # Virtual environment
```

---

## License & Usage
This bot is designed for educational microfinance institutions across East Africa.
Modify and redistribute as needed for your use case.

---

**Last Updated:** January 2024  
**Version:** 1.0  
**Status:** Production Ready ✅

Good luck with your loan bot! 🚀
