#!/usr/bin/env python3
"""
Telegram Loan Bot for Educational Institutions
Deploy-ready version with environment variable support
"""

import logging
import json
import re
import os
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
import pandas as pd
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, ContextTypes, filters
from telegram.constants import ParseMode

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration from environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
DATABASE_PATH = os.getenv('DATABASE_PATH', '/mnt/user-data/uploads/Loan_Bot_Database_NEW.xlsx')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Validate bot token
if not BOT_TOKEN:
    logger.error("❌ BOT_TOKEN not found! Set it as environment variable or in .env file")
    raise ValueError("BOT_TOKEN is required. Set in environment variables or .env file")

# Validate database file exists
if not os.path.exists(DATABASE_PATH):
    logger.error(f"❌ Database file not found at: {DATABASE_PATH}")
    raise FileNotFoundError(f"Database file not found at: {DATABASE_PATH}")

logger.info(f"✅ Bot Token: {BOT_TOKEN[:10]}...")
logger.info(f"✅ Database: {DATABASE_PATH}")
logger.info(f"✅ Environment: {ENVIRONMENT}")

# Conversation states
class State(Enum):
    START = 0
    SELECT_COUNTRY = 1
    SELECT_MFI = 2
    SELECT_LOAN_TYPE = 3
    VIEW_LOAN_INFO = 4
    LOAN_CALCULATOR = 5
    REGISTRATION = 6
    REG_NAME = 7
    REG_SCHOOL = 8
    REG_COUNTRY = 9
    REG_LOCATION = 10
    REG_PHONE = 11
    REG_EMAIL = 12
    REG_LOAN_TYPE = 13
    REG_AMOUNT = 14
    REG_PERIOD = 15
    REG_PRIORITY = 16
    REG_COMMENTS = 17

# Load data from Excel
def load_excel_data(filepath):
    """Load all data from Excel file"""
    logger.info(f"Loading data from: {filepath}")
    excel_file = pd.ExcelFile(filepath)
    data = {}
    
    for sheet in excel_file.sheet_names:
        data[sheet] = pd.read_excel(filepath, sheet_name=sheet).fillna('').to_dict('records')
        logger.info(f"  ✅ Loaded {sheet}: {len(data[sheet])} records")
    
    return data

# Convert data to JSON-friendly format
EXCEL_DATA = load_excel_data(DATABASE_PATH)

# Build lookups
COUNTRIES = {item['Country Code']: item['Country Name'] for item in EXCEL_DATA['Countries']}
COUNTRY_NAMES = {v: k for k, v in COUNTRIES.items()}

MFI_DATA = {item['MFI ID']: item for item in EXCEL_DATA['MFI Master Data']}
MFIS_BY_COUNTRY = {}
for mfi in EXCEL_DATA['MFI Master Data']:
    country = mfi['Country']
    if country not in MFIS_BY_COUNTRY:
        MFIS_BY_COUNTRY[country] = []
    MFIS_BY_COUNTRY[country].append(mfi)

LOAN_TYPES = {item['Loan Type ID']: item for item in EXCEL_DATA['Loan Types']}
LOAN_TYPES_LIST = EXCEL_DATA['Loan Types']

REQUIREMENTS = EXCEL_DATA['Requirements']
RATES = EXCEL_DATA['Interest Rates & Terms'][0]
CALC_SETTINGS = {item['Setting']: item['Value'] for item in EXCEL_DATA['Calculator Settings']}

logger.info("✅ All data loaded successfully!")

# Helper functions
def get_loan_type_name(loan_type_id):
    """Get loan type name from ID"""
    for loan in LOAN_TYPES_LIST:
        if loan['Loan Type ID'] == loan_type_id:
            return loan['Loan Type Name']
    return loan_type_id

def format_currency(amount, currency='USD'):
    """Format currency with appropriate symbol"""
    symbols = {'USD': '$', 'ETB': 'Br', 'KES': 'Ksh', 'RWF': 'FRw', 'UGX': 'Ush'}
    symbol = symbols.get(currency, currency)
    return f"{symbol}{amount:,.0f}"

def calculate_monthly_payment(principal, annual_rate, months):
    """Calculate monthly payment using loan formula"""
    monthly_rate = annual_rate / 100 / 12
    if monthly_rate == 0:
        return principal / months
    payment = principal * (monthly_rate * (1 + monthly_rate)**months) / ((1 + monthly_rate)**months - 1)
    return payment

def calculate_amortization_schedule(principal, annual_rate, months):
    """Generate amortization schedule"""
    schedule = []
    monthly_rate = annual_rate / 100 / 12
    remaining = principal
    
    for month in range(1, min(months + 1, 13)):
        payment = calculate_monthly_payment(principal, annual_rate, months)
        interest = remaining * monthly_rate
        principal_payment = payment - interest
        remaining -= principal_payment
        
        schedule.append({
            'month': month,
            'payment': payment,
            'principal': principal_payment,
            'interest': interest,
            'remaining': max(0, remaining)
        })
    
    return schedule

# Telegram Bot Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and show main menu"""
    logger.info(f"User {update.effective_user.id} started bot")
    
    keyboard = [
        [InlineKeyboardButton("🏦 MFI List", callback_data='menu_mfis')],
        [InlineKeyboardButton("📊 Loan Calculator", callback_data='menu_calculator')],
        [InlineKeyboardButton("📋 Register", callback_data='menu_register')],
        [InlineKeyboardButton("❓ FAQ", callback_data='menu_faq')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🤖 *Welcome to Loan Bot* 🤖\n\n"
        "I help schools find microfinance institutions (MFIs) and calculate loans for "
        "educational technology, infrastructure, and development projects.\n\n"
        "What would you like to do?",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    
    return State.START.value

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle main menu selection"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'menu_mfis':
        keyboard = [[InlineKeyboardButton(country, callback_data=f'country_{country}')] 
                   for country in MFIS_BY_COUNTRY.keys()]
        keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data='back_menu')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "*Select Your Country* 🌍\n\n",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        return State.SELECT_COUNTRY.value
    
    elif query.data == 'menu_calculator':
        keyboard = [
            [InlineKeyboardButton("EdTech Loan (18%)", callback_data='calc_LOAN001')],
            [InlineKeyboardButton("School Development Loan (24%)", callback_data='calc_LOAN002')],
            [InlineKeyboardButton("Development Loan (24%)", callback_data='calc_LOAN003')],
            [InlineKeyboardButton("⬅️ Back", callback_data='back_menu')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "*Loan Calculator* 📊\n\n"
            "Select a loan type to calculate monthly payments:",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        return State.LOAN_CALCULATOR.value
    
    elif query.data == 'menu_register':
        context.user_data['registration'] = {}
        await query.edit_message_text(
            "*📋 Registration Form*\n\n"
            "Let's start your loan application. What's your full name?",
            parse_mode=ParseMode.MARKDOWN
        )
        return State.REG_NAME.value
    
    elif query.data == 'menu_faq':
        await query.edit_message_text(
            "*❓ Frequently Asked Questions*\n\n"
            "*What is a loan calculator?*\n"
            "It helps you estimate monthly payments, total interest, and repayment schedule.\n\n"
            "*What are the eligibility requirements?*\n"
            "• School registered with Ministry of Education\n"
            "• Operating for minimum 1 year\n"
            "• Bank account for the school\n"
            "• Minimum 5 teaching staff\n"
            "• Minimum 100 students\n"
            "• 6 months financial records\n\n"
            "*Can I change my loan amount later?*\n"
            "You can modify during registration. Once submitted, contact the MFI directly.\n\n",
            parse_mode=ParseMode.MARKDOWN
        )
        keyboard = [[InlineKeyboardButton("⬅️ Back", callback_data='back_menu')]]
        await query.edit_message_reply_markup(InlineKeyboardMarkup(keyboard))
        return State.START.value
    
    elif query.data == 'back_menu':
        await start(update, context)
        return State.START.value

async def select_country(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle country selection"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'back_menu':
        await start(update, context)
        return State.START.value
    
    country = query.data.replace('country_', '')
    context.user_data['country'] = country
    
    mfis = MFIS_BY_COUNTRY.get(country, [])
    
    message = f"*🏦 MFIs in {country}* 🏦\n\n"
    keyboard = []
    
    for mfi in mfis:
        message += f"• *{mfi['MFI Name']}*\n  {mfi['Description']}\n  📞 {mfi['Phone Number']}\n\n"
        keyboard.append([InlineKeyboardButton(mfi['MFI Name'], callback_data=f"mfi_{mfi['MFI ID']}")])
    
    keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data='back_country')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        message,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    
    return State.SELECT_MFI.value

async def select_mfi(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle MFI selection"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'back_country':
        keyboard = [[InlineKeyboardButton(country, callback_data=f'country_{country}')] 
                   for country in MFIS_BY_COUNTRY.keys()]
        keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data='back_menu')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "*Select Your Country* 🌍",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        return State.SELECT_COUNTRY.value
    
    mfi_id = query.data.replace('mfi_', '')
    mfi = MFI_DATA[mfi_id]
    context.user_data['mfi_id'] = mfi_id
    context.user_data['mfi_name'] = mfi['MFI Name']
    
    message = f"*{mfi['MFI Name']}*\n\n" \
              f"Contact: {mfi['Phone Number']}\n" \
              f"Country: {mfi['Country']}\n\n" \
              f"*Available Loan Products:*\n\n"
    
    keyboard = []
    for loan in LOAN_TYPES_LIST:
        message += f"💰 *{loan['Loan Type Name']}*\n{loan['Description']}\n\n"
        keyboard.append([InlineKeyboardButton(
            loan['Loan Type Name'],
            callback_data=f"loan_{loan['Loan Type ID']}"
        )])
    
    keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data='back_mfi')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        message,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    
    return State.SELECT_LOAN_TYPE.value

async def select_loan_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show loan information"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'back_mfi':
        country = context.user_data.get('country')
        mfis = MFIS_BY_COUNTRY.get(country, [])
        
        message = f"*🏦 MFIs in {country}*\n\n"
        keyboard = []
        
        for mfi in mfis:
            message += f"• *{mfi['MFI Name']}*\n  {mfi['Description']}\n  📞 {mfi['Phone Number']}\n\n"
            keyboard.append([InlineKeyboardButton(mfi['MFI Name'], callback_data=f"mfi_{mfi['MFI ID']}")])
        
        keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data='back_country')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            message,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        return State.SELECT_MFI.value
    
    loan_id = query.data.replace('loan_', '')
    loan = LOAN_TYPES[loan_id]
    mfi_name = context.user_data.get('mfi_name', 'MFI')
    context.user_data['loan_type_id'] = loan_id
    context.user_data['loan_type_name'] = loan['Loan Type Name']
    
    message = f"*{loan['Loan Type Name']} @ {mfi_name}*\n\n" \
              f"{loan['Description']}\n\n" \
              f"*📊 Loan Terms:*\n" \
              f"• Annual Interest Rate: *{RATES['Annual Interest Rate (%)']}%*\n" \
              f"• Min Amount: {format_currency(RATES['Min Amount (USD)'])}\n" \
              f"• Max Amount: {format_currency(RATES['Max Amount (USD)'])}\n" \
              f"• Repayment Period: *{RATES['Repayment Period (Months)']} months*\n" \
              f"• Processing Fee: *{RATES['Processing Fee (%)']}%*\n\n" \
              f"*✅ Eligibility Requirements:*\n"
    
    for req in REQUIREMENTS:
        message += f"• {req['Requirement']}: {req['Description']}\n"
    
    keyboard = [
        [InlineKeyboardButton("🧮 Calculate Monthly Payment", callback_data=f'calc_detail_{loan_id}')],
        [InlineKeyboardButton("📋 Apply Now", callback_data='menu_register')],
        [InlineKeyboardButton("⬅️ Back", callback_data='back_loan')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        message,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    
    return State.VIEW_LOAN_INFO.value

async def loan_calculator(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle loan calculator"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'back_loan' or query.data == 'back_menu':
        await start(update, context)
        return State.START.value
    
    if query.data.startswith('calc_'):
        loan_id = query.data.replace('calc_', '').replace('LOAN', 'LOAN')
    else:
        loan_id = query.data.replace('calc_detail_', '')
    
    loan = LOAN_TYPES.get(loan_id, {})
    context.user_data['calc_loan_id'] = loan_id
    
    message = f"*🧮 Loan Calculator - {loan.get('Loan Type Name', 'Loan')}*\n\n" \
              f"Annual Interest Rate: *{RATES['Annual Interest Rate (%)']}%*\n" \
              f"Processing Fee: *{RATES['Processing Fee (%)']}%*\n\n" \
              f"Enter the loan amount (in USD) you want to borrow:\n\n" \
              f"(Between {format_currency(RATES['Min Amount (USD)'])} and " \
              f"{format_currency(RATES['Max Amount (USD)'])})"
    
    keyboard = [[InlineKeyboardButton("⬅️ Back", callback_data='back_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        message,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    
    await update.callback_query.message.reply_text(
        "Please enter the loan amount (numbers only):",
        reply_markup=ReplyKeyboardRemove()
    )
    
    return State.LOAN_CALCULATOR.value

async def calculator_amount_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Process loan amount input for calculator"""
    try:
        amount = float(update.message.text.replace(',', ''))
        
        if amount < RATES['Min Amount (USD)'] or amount > RATES['Max Amount (USD)']:
            await update.message.reply_text(
                f"❌ Amount must be between {format_currency(RATES['Min Amount (USD)'])} "
                f"and {format_currency(RATES['Max Amount (USD)'])}\n\n"
                f"Please enter a valid amount:"
            )
            return State.LOAN_CALCULATOR.value
        
        context.user_data['calc_amount'] = amount
        loan_id = context.user_data.get('calc_loan_id', 'LOAN001')
        loan = LOAN_TYPES.get(loan_id, {})
        
        keyboard = [
            [InlineKeyboardButton("24 months", callback_data='period_24')],
            [InlineKeyboardButton("36 months (Default)", callback_data='period_36')],
            [InlineKeyboardButton("48 months", callback_data='period_48')],
            [InlineKeyboardButton("60 months", callback_data='period_60')],
            [InlineKeyboardButton("⬅️ Back", callback_data='back_menu')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"Selected Amount: *{format_currency(amount)}*\n\n"
            f"Select repayment period:",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
        return State.LOAN_CALCULATOR.value
    
    except ValueError:
        await update.message.reply_text(
            "❌ Please enter a valid number (numbers only, no spaces or letters)"
        )
        return State.LOAN_CALCULATOR.value

async def calculator_period_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Process repayment period selection"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'back_menu':
        await start(update, context)
        return State.START.value
    
    period = int(query.data.replace('period_', ''))
    amount = context.user_data.get('calc_amount', 10000)
    interest_rate = RATES['Annual Interest Rate (%)']
    processing_fee = RATES['Processing Fee (%)']
    
    fee_amount = amount * (processing_fee / 100)
    principal = amount + fee_amount if CALC_SETTINGS.get('Include Processing Fee in Principal', 'Yes') == 'Yes' else amount
    
    monthly_payment = calculate_monthly_payment(principal, interest_rate, period)
    total_paid = monthly_payment * period
    total_interest = total_paid - amount
    
    message = f"*💰 Loan Calculation Results*\n\n" \
              f"*Loan Details:*\n" \
              f"Original Amount: {format_currency(amount)}\n" \
              f"Processing Fee ({processing_fee}%): {format_currency(fee_amount)}\n" \
              f"Total Principal: {format_currency(principal)}\n" \
              f"Annual Interest Rate: {interest_rate}%\n" \
              f"Repayment Period: {period} months\n\n" \
              f"*Monthly Payment: {format_currency(monthly_payment)}*\n" \
              f"Total Interest: {format_currency(total_interest)}\n" \
              f"Total Amount to Pay: {format_currency(total_paid)}\n\n"
    
    if CALC_SETTINGS.get('Show Amortization Schedule', 'Yes') == 'Yes':
        message += "*📋 First 6 Months Schedule:*\n"
        schedule = calculate_amortization_schedule(principal, interest_rate, period)
        
        for payment in schedule[:6]:
            message += f"Month {payment['month']}: " \
                      f"Payment {format_currency(payment['payment'])} " \
                      f"| Principal {format_currency(payment['principal'])} " \
                      f"| Interest {format_currency(payment['interest'])}\n"
    
    keyboard = [
        [InlineKeyboardButton("📋 Register for this Loan", callback_data='menu_register')],
        [InlineKeyboardButton("🔄 Calculate Another", callback_data='menu_calculator')],
        [InlineKeyboardButton("⬅️ Back to Menu", callback_data='back_menu')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        message,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    
    return State.LOAN_CALCULATOR.value

# Registration handlers
async def registration_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Get full name for registration"""
    name = update.message.text
    
    if len(name) > 100:
        await update.message.reply_text("❌ Name too long (max 100 characters). Please try again:")
        return State.REG_NAME.value
    
    context.user_data['registration']['full_name'] = name
    
    await update.message.reply_text(
        "Thank you! What's your school name?"
    )
    return State.REG_SCHOOL.value

async def registration_school(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Get school name"""
    school = update.message.text
    
    if len(school) > 150:
        await update.message.reply_text("❌ School name too long (max 150 characters). Please try again:")
        return State.REG_SCHOOL.value
    
    context.user_data['registration']['school_name'] = school
    
    keyboard = [[InlineKeyboardButton(country, callback_data=f'reg_country_{country}')] 
               for country in MFIS_BY_COUNTRY.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Which country is your school located in?",
        reply_markup=reply_markup
    )
    return State.REG_COUNTRY.value

async def registration_country(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Get country"""
    query = update.callback_query
    await query.answer()
    
    country = query.data.replace('reg_country_', '')
    context.user_data['registration']['country'] = country
    
    await query.edit_message_text(
        "What's your district/zone/city?"
    )
    await query.message.reply_text(
        "Please enter your location:",
        reply_markup=ReplyKeyboardRemove()
    )
    
    return State.REG_LOCATION.value

async def registration_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Get location"""
    location = update.message.text
    
    if len(location) > 50:
        await update.message.reply_text("❌ Location too long (max 50 characters). Please try again:")
        return State.REG_LOCATION.value
    
    context.user_data['registration']['location'] = location
    
    await update.message.reply_text(
        "What's your phone number?\n(Format: +XXX-XXX-XXXXXX)"
    )
    return State.REG_PHONE.value

async def registration_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Get phone number"""
    phone = update.message.text
    
    if not re.match(r'^\+?\d{1,3}[-.\s]?\d{1,14}$', phone) or len(phone) > 14:
        await update.message.reply_text(
            "❌ Invalid phone number format. Please use format like +256-704-789012"
        )
        return State.REG_PHONE.value
    
    context.user_data['registration']['phone'] = phone
    
    await update.message.reply_text(
        "What's your email address?"
    )
    return State.REG_EMAIL.value

async def registration_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Get email"""
    email = update.message.text
    
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        await update.message.reply_text(
            "❌ Invalid email format. Please enter a valid email."
        )
        return State.REG_EMAIL.value
    
    context.user_data['registration']['email'] = email
    
    keyboard = [[InlineKeyboardButton(loan['Loan Type Name'], callback_data=f'reg_loan_{loan["Loan Type ID"]}')] 
               for loan in LOAN_TYPES_LIST]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Which loan type are you interested in?",
        reply_markup=reply_markup
    )
    return State.REG_LOAN_TYPE.value

async def registration_loan_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Get loan type"""
    query = update.callback_query
    await query.answer()
    
    loan_id = query.data.replace('reg_loan_', '')
    context.user_data['registration']['loan_type'] = loan_id
    
    await query.edit_message_text(
        f"Enter the loan amount you need (USD):\n"
        f"(Between {format_currency(RATES['Min Amount (USD)'])} and {format_currency(RATES['Max Amount (USD)'])})"
    )
    await query.message.reply_text(
        "Please enter the loan amount (numbers only):",
        reply_markup=ReplyKeyboardRemove()
    )
    
    return State.REG_AMOUNT.value

async def registration_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Get loan amount"""
    try:
        amount = float(update.message.text.replace(',', ''))
        
        if amount < RATES['Min Amount (USD)'] or amount > RATES['Max Amount (USD)']:
            await update.message.reply_text(
                f"❌ Amount must be between {format_currency(RATES['Min Amount (USD)'])} "
                f"and {format_currency(RATES['Max Amount (USD)'])}\n"
                f"Please try again:"
            )
            return State.REG_AMOUNT.value
        
        context.user_data['registration']['loan_amount'] = amount
        
        keyboard = [
            [InlineKeyboardButton("24 months", callback_data='reg_period_24')],
            [InlineKeyboardButton("36 months", callback_data='reg_period_36')],
            [InlineKeyboardButton("48 months", callback_data='reg_period_48')],
            [InlineKeyboardButton("60 months", callback_data='reg_period_60')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "Select preferred repayment period:",
            reply_markup=reply_markup
        )
        return State.REG_PERIOD.value
    
    except ValueError:
        await update.message.reply_text("❌ Please enter a valid number")
        return State.REG_AMOUNT.value

async def registration_period(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Get repayment period"""
    query = update.callback_query
    await query.answer()
    
    period = int(query.data.replace('reg_period_', ''))
    context.user_data['registration']['repayment_period'] = period
    
    keyboard = [
        [InlineKeyboardButton("🔴 High", callback_data='reg_priority_High')],
        [InlineKeyboardButton("🟡 Medium", callback_data='reg_priority_Medium')],
        [InlineKeyboardButton("🟢 Low", callback_data='reg_priority_Low')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "What's your application priority?",
        reply_markup=reply_markup
    )
    return State.REG_PRIORITY.value

async def registration_priority(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Get application priority"""
    query = update.callback_query
    await query.answer()
    
    priority = query.data.replace('reg_priority_', '')
    context.user_data['registration']['priority'] = priority
    
    await query.edit_message_text(
        "Any additional comments or notes? (Optional - you can skip by typing 'NONE')"
    )
    await query.message.reply_text(
        "Enter your comments (or 'NONE' to skip):",
        reply_markup=ReplyKeyboardRemove()
    )
    
    return State.REG_COMMENTS.value

async def registration_comments(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Get comments and submit"""
    comments = update.message.text
    
    if comments.upper() != 'NONE':
        if len(comments) > 500:
            await update.message.reply_text("❌ Comments too long (max 500 characters). Please try again:")
            return State.REG_COMMENTS.value
        context.user_data['registration']['comments'] = comments
    
    reg = context.user_data['registration']
    loan_type_name = get_loan_type_name(reg['loan_type'])
    
    summary = f"*📋 Application Summary*\n\n" \
              f"*Personal Information:*\n" \
              f"Full Name: {reg['full_name']}\n" \
              f"School: {reg['school_name']}\n" \
              f"Location: {reg['location']}, {reg['country']}\n" \
              f"Phone: {reg['phone']}\n" \
              f"Email: {reg['email']}\n\n" \
              f"*Loan Details:*\n" \
              f"Loan Type: {loan_type_name}\n" \
              f"Amount Requested: {format_currency(reg['loan_amount'])}\n" \
              f"Repayment Period: {reg['repayment_period']} months\n" \
              f"Interest Rate: {RATES['Annual Interest Rate (%)']}%\n" \
              f"Application Priority: {reg['priority']}\n"
    
    if 'comments' in reg:
        summary += f"\nComments: {reg['comments']}\n"
    
    keyboard = [
        [InlineKeyboardButton("✅ Confirm & Submit", callback_data='confirm_submit')],
        [InlineKeyboardButton("❌ Cancel", callback_data='cancel_submit')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        summary + "\n\nPlease review and confirm your application:",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    
    return State.REGISTRATION.value

async def registration_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle final submission confirmation"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'cancel_submit':
        await query.edit_message_text(
            "❌ Application cancelled. Thank you for your interest!"
        )
        await start(update, context)
        return State.START.value
    
    reg = context.user_data['registration']
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    application_data = {
        'timestamp': timestamp,
        'user_id': update.effective_user.id,
        'username': update.effective_user.username or 'N/A',
        **reg
    }
    
    logger.info(f"New Application: {json.dumps(application_data, indent=2)}")
    
    loan_type_name = get_loan_type_name(reg['loan_type'])
    
    success_message = f"*✅ Application Submitted Successfully!*\n\n" \
                     f"Thank you for submitting your loan application!\n\n" \
                     f"*Next Steps:*\n" \
                     f"1. We will review your application\n" \
                     f"2. Contact you at {reg['phone']} within 24-48 hours\n" \
                     f"3. Schedule an interview if approved\n\n" \
                     f"*Your Application Number:* APP{timestamp.replace('-', '').replace(':', '').replace(' ', '')}\n\n" \
                     f"*Quick Summary:*\n" \
                     f"School: {reg['school_name']}\n" \
                     f"Loan Type: {loan_type_name}\n" \
                     f"Amount: {format_currency(reg['loan_amount'])}\n" \
                     f"Period: {reg['repayment_period']} months\n"
    
    keyboard = [[InlineKeyboardButton("🏠 Back to Menu", callback_data='back_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        success_message,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    
    return State.START.value

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the conversation"""
    await update.message.reply_text("Conversation cancelled.")
    return ConversationHandler.END

def main():
    """Start the bot"""
    logger.info("🚀 Starting Loan Bot...")
    
    # Verify bot token before creating app
    if not BOT_TOKEN or BOT_TOKEN == 'your_bot_token_here':
        logger.error("❌ ERROR: Invalid or missing BOT_TOKEN!")
        logger.error("Set BOT_TOKEN as environment variable or in .env file")
        raise ValueError("BOT_TOKEN is required and must be valid")
    
    application = Application.builder().token(BOT_TOKEN).build()
    logger.info("✅ Application created successfully")
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            State.START.value: [CallbackQueryHandler(main_menu)],
            State.SELECT_COUNTRY.value: [CallbackQueryHandler(select_country)],
            State.SELECT_MFI.value: [CallbackQueryHandler(select_mfi)],
            State.SELECT_LOAN_TYPE.value: [CallbackQueryHandler(select_loan_type)],
            State.VIEW_LOAN_INFO.value: [CallbackQueryHandler(loan_calculator)],
            State.LOAN_CALCULATOR.value: [
                CallbackQueryHandler(calculator_period_selection, pattern='^period_'),
                CallbackQueryHandler(loan_calculator),
                MessageHandler(filters.TEXT & ~filters.COMMAND, calculator_amount_input)
            ],
            State.REG_NAME.value: [MessageHandler(filters.TEXT & ~filters.COMMAND, registration_name)],
            State.REG_SCHOOL.value: [MessageHandler(filters.TEXT & ~filters.COMMAND, registration_school)],
            State.REG_COUNTRY.value: [CallbackQueryHandler(registration_country)],
            State.REG_LOCATION.value: [MessageHandler(filters.TEXT & ~filters.COMMAND, registration_location)],
            State.REG_PHONE.value: [MessageHandler(filters.TEXT & ~filters.COMMAND, registration_phone)],
            State.REG_EMAIL.value: [MessageHandler(filters.TEXT & ~filters.COMMAND, registration_email)],
            State.REG_LOAN_TYPE.value: [CallbackQueryHandler(registration_loan_type)],
            State.REG_AMOUNT.value: [MessageHandler(filters.TEXT & ~filters.COMMAND, registration_amount)],
            State.REG_PERIOD.value: [CallbackQueryHandler(registration_period)],
            State.REG_PRIORITY.value: [CallbackQueryHandler(registration_priority)],
            State.REG_COMMENTS.value: [MessageHandler(filters.TEXT & ~filters.COMMAND, registration_comments)],
            State.REGISTRATION.value: [CallbackQueryHandler(registration_confirm)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    application.add_handler(conv_handler)
    
    logger.info("✅ Bot configured successfully")
    logger.info("🚀 Bot is now running...")
    logger.info(f"Environment: {ENVIRONMENT}")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
