# 📖 Loan Bot - Complete Feature Guide

## Feature Overview

### 1. 🏦 MFI List & Details

**What it does:**
Browse all microfinance institutions by country and view their loan products and terms.

**How to use:**
1. Tap "🏦 MFI List" from main menu
2. Select your country:
   - 🇪🇹 Ethiopia
   - 🇰🇪 Kenya
   - 🇷🇼 Rwanda
   - 🇺🇬 Uganda
3. View all MFIs in that country with:
   - MFI name & description
   - Phone number
4. Tap an MFI name to see their loan products
5. View loan details including:
   - Interest rates
   - Min/max loan amounts
   - Repayment periods
   - Processing fees
   - Eligibility requirements

**Example:**
```
🏦 MFIs in Ethiopia

• Peace Microfinance
  Leading MFI in Ethiopia
  📞 +251-911-234567

• VisionFund MFI
  Leading MFI in Ethiopia
  📞 +251-912-345678
```

**Current MFIs:**
```
Ethiopia (2):
- Peace Microfinance
- VisionFund MFI

Kenya (1):
- DIMKES SACCO

Rwanda (2):
- Goshen MFI
- ACB

Uganda (2):
- Saviour MFI
- Lubaga Teachers SACCO

Total: 7 MFIs
```

---

### 2. 📊 Loan Calculator

**What it does:**
Calculate monthly payments, total interest, and see a payment schedule for any loan amount.

**How to use:**
1. Tap "📊 Loan Calculator" from main menu
2. Choose loan type:
   - **EdTech Loan** (18% annual interest)
     - For buying educational technology
   - **School Development Loan** (24% annual interest)
     - For school improvement projects
   - **Development Loan** (24% annual interest)
     - For infrastructure development
3. Enter the loan amount (USD 1,000 - 50,000)
4. Select repayment period:
   - 24 months (2 years)
   - 36 months (3 years) - default
   - 48 months (4 years)
   - 60 months (5 years)
5. See the results:

**Example Calculation:**
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
Month 3: Payment $325.50 | Principal $185.80 | Interest $139.70
Month 4: Payment $325.50 | Principal $187.98 | Interest $137.52
Month 5: Payment $325.50 | Principal $190.17 | Interest $135.33
Month 6: Payment $325.50 | Principal $192.38 | Interest $133.12
```

**What the numbers mean:**
- **Monthly Payment** - You pay this amount every month
- **Principal** - Part of payment going toward the loan
- **Interest** - Part of payment going to the lender
- **Total Interest** - Sum of all interest paid over loan period

**Pro Tips:**
- ✅ Longer periods = Lower monthly payment but more total interest
- ✅ Shorter periods = Higher monthly payment but less total interest
- ✅ Larger amounts = Higher monthly payments
- ✅ Use this to plan your school budget

---

### 3. 📋 Registration System

**What it does:**
Submit a complete loan application directly through Telegram.

**Information Collected:**

**Personal Details:**
- Full name (max 100 characters)
- School name (max 150 characters)
- Country
- District/Zone/City
- Phone number (format: +XXX-XXX-XXXXXX)
- Email address (valid email format)

**Loan Request:**
- Loan type (EdTech, School Development, Development)
- Loan amount (must be within min/max range)
- Preferred repayment period (24, 36, 48, 60 months)
- Application priority (High, Medium, Low)

**Optional:**
- Additional comments (max 500 characters)

**How to Register:**
1. Tap "📋 Register" from main menu
2. Answer each question as prompted:
   - The bot guides you step-by-step
   - Use buttons for easy selection
   - Type text for open-ended questions
3. Review your application summary
4. Tap "✅ Confirm & Submit"
5. Get your application number
6. Next steps are shown

**After Submission:**
✅ You receive:
- Application number (for reference)
- Confirmation of submission
- Summary of your loan details
- Expected next steps

📞 The MFI will contact you within 24-48 hours at:
- The phone number you provided
- Details will be sent to your email

**Example Registration Flow:**
```
Step 1: Full Name?
→ John Kamau

Step 2: School Name?
→ St. Augustine Primary School

Step 3: Country?
→ [Select: Kenya]

Step 4: District/Zone/City?
→ Nairobi Central

Step 5: Phone Number?
→ +254-703-456789

Step 6: Email Address?
→ john.kamau@school.ke

Step 7: Loan Type?
→ [Select: EdTech Loan]

Step 8: Loan Amount?
→ 5000

Step 9: Repayment Period?
→ [Select: 36 months]

Step 10: Priority?
→ [Select: High]

Step 11: Comments?
→ Need to upgrade computer lab

✅ Application Submitted!
Application Number: APP20240115103045
```

**Priority Levels:**
- 🔴 **High** - Urgent need
- 🟡 **Medium** - Normal processing
- 🟢 **Low** - Flexible timeline

---

### 4. ❓ FAQ Section

**What it covers:**
Quick answers to common questions about loans and eligibility.

**Questions Answered:**

**Q: What is a loan calculator?**
A: It helps you estimate how much you'll pay each month, total interest, and see a payment schedule before you apply.

**Q: What are the eligibility requirements?**
A: Your school must:
- ✅ Be registered with Ministry of Education
- ✅ Be operating for at least 1 year
- ✅ Have a bank account
- ✅ Have at least 5 teaching staff
- ✅ Have at least 100 students
- ✅ Provide 6 months of financial records

**Q: Can I change loan details after applying?**
A: You can modify before final submission. After submission, contact the MFI directly using the phone number in the confirmation.

---

## Loan Types Explained

### 1. EdTech Loan 💻
**Annual Interest Rate:** 18%
**Min Amount:** USD 1,000
**Max Amount:** USD 10,000
**Typical Uses:**
- Computers & laptops
- Projectors & smart boards
- Tablets for students
- Educational software
- Internet/connectivity

### 2. School Development Loan (SIP) 🏫
**Annual Interest Rate:** 24%
**Min Amount:** USD 1,000
**Max Amount:** USD 30,000
**Typical Uses:**
- Classroom renovation
- Furniture & desks
- Laboratory equipment
- Science/art materials
- Facility improvements

### 3. Development Loan 🏗️
**Annual Interest Rate:** 24%
**Min Amount:** USD 2,000
**Max Amount:** USD 50,000
**Typical Uses:**
- Building new classrooms
- Construction projects
- Infrastructure development
- Security fencing
- Water & sanitation facilities

---

## Interest Rates Explained

**What is APR (Annual Percentage Rate)?**
The percentage of your loan amount charged as interest per year.

**Example:**
- Loan: $10,000
- Interest: 18% APR
- Year 1 interest (if unpaid): $1,800

**How Monthly Payments Work:**
The loan calculator automatically figures out your monthly payment so that:
- Each payment includes principal (what you borrowed)
- Plus interest (cost of borrowing)
- Principal decreases monthly
- Interest decreases monthly
- You pay the same amount each month

**Processing Fee:**
- **5%** of loan amount charged upfront
- Added to your principal
- Included in monthly payment calculations

---

## Payment Schedule Example

**Loan Details:**
- Amount: $5,000
- Processing Fee: $250 (5%)
- Principal: $5,250
- Interest Rate: 18%
- Period: 24 months

**Results:**
- Monthly Payment: **$268.57**
- Total Interest: **$893.68**
- Total Paid: **$6,143.68**

**First 3 Months:**
```
Month 1: Payment $268.57 | Principal $210.58 | Interest $57.99
Month 2: Payment $268.57 | Principal $211.79 | Interest $56.78
Month 3: Payment $268.57 | Principal $212.99 | Interest $55.58
...
Month 24: Payment $268.57 | Principal $266.93 | Interest $1.64
```

Notice:
- ✅ Principal increases over time
- ✅ Interest decreases over time
- ✅ Payment stays constant

---

## Step-by-Step Examples

### Example 1: Finding an MFI

**Scenario:** You're in Uganda and need a school development loan.

**Steps:**
```
1. Send /start
2. Click "🏦 MFI List"
3. Click "🇺🇬 Uganda"
4. See two options:
   - Saviour MFI
   - Lubaga Teachers SACCO
5. Click "Saviour MFI"
6. See three loan types
7. Click "School Development Loan"
8. View:
   - Interest rate: 24%
   - Amount range: $1,000-$30,000
   - Period: 36 months
   - Eligibility requirements
9. Call +256-704-789012 or apply through bot
```

### Example 2: Calculating a Loan

**Scenario:** Calculate payment for $8,000 EdTech loan over 36 months.

**Steps:**
```
1. Click "📊 Loan Calculator"
2. Select "EdTech Loan (18%)"
3. Type: 8000
4. Select: "36 months"
5. See results:
   - Monthly: $263.67
   - Total Interest: $1,492.12
   - Total Paid: $9,492.12
6. Decide if affordable
7. Use "📋 Apply Now" button to register
```

### Example 3: Submitting Application

**Scenario:** Register for $15,000 Development Loan.

**Steps:**
```
1. Click "📋 Register"
2. Enter: John Mwangi
3. Enter: Bright Future Secondary
4. Select: Kenya
5. Enter: Kisumu
6. Enter: +254-703-456789
7. Enter: john@brightfuture.ke
8. Select: Development Loan
9. Enter: 15000
10. Select: 48 months
11. Select: High priority
12. Enter: Need renovations urgently
13. Review summary
14. Click "✅ Confirm & Submit"
15. Get: APP20240115103045
16. MFI contacts you within 24-48 hours
```

---

## Navigation Tips

**Buttons:**
- 🔘 Tap colored buttons for quick selection
- ⬅️ "Back" buttons always available
- Numbers in buttons (📊, 💰, etc.) show features

**Text Input:**
- Type when asked for names, amounts, phone
- Use keyboard that appears
- Check validation messages

**Flow:**
- Each question builds on previous
- Can't skip questions
- Easy to go back with "Back" button

---

## Common Questions & Answers

**Q: Is this bot secure?**
A: Telegram uses encryption. Don't share sensitive passwords. Information is processed securely.

**Q: Can multiple people use the same bot?**
A: Yes! Each user has their own conversation and data is separate.

**Q: How do I reset/start over?**
A: Send `/start` command or click "Back to Menu" buttons.

**Q: Can I get a copy of my application?**
A: Your application number is provided. Save it. Share with the MFI you apply to.

**Q: How long does approval take?**
A: MFI contacts you within 24-48 hours. Approval depends on application review.

**Q: Can I apply to multiple MFIs?**
A: Yes! You can submit separate applications to different MFIs for comparison.

**Q: What if I enter wrong information?**
A: Contact the MFI directly with your application number to request corrections.

**Q: Is there a maximum loan amount?**
A: Yes, varies by loan type (see details above). Max is $50,000.

**Q: Can I change my mind after submitting?**
A: Contact the MFI directly before they process your application.

---

## Data Validation Rules

The bot ensures:
- ✅ Names ≤ 100 characters
- ✅ School names ≤ 150 characters
- ✅ Loan amounts within min/max range
- ✅ Phone numbers in correct format
- ✅ Valid email addresses
- ✅ Comments ≤ 500 characters

If you enter invalid data, the bot tells you and asks again.

---

## Keyboard Shortcuts (if using Telegram Desktop)

- Tab: Next field
- Shift+Tab: Previous field
- Enter: Select button
- Escape: Cancel

---

## Tips for Best Results

💡 **Before Applying:**
1. Calculate expected monthly payment
2. Ensure your school can afford payments
3. Gather required documents
4. Contact MFI to confirm requirements

💡 **During Application:**
1. Use correct school name and registration
2. Use primary contact phone
3. Be honest about timeline
4. Ask any questions before submitting

💡 **After Application:**
1. Save your application number
2. Keep your phone available
3. Prepare documents when MFI contacts
4. Ask about next steps if you don't hear back in 48 hours

---

This guide covers all features. For technical questions, see SETUP_GUIDE.md
