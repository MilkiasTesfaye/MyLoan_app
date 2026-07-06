# 📋 GitHub & Cloud Configuration Guide

## Part 1: Setup GitHub Repository

### Step 1A: Create GitHub Account (if needed)
1. Go to **github.com**
2. Click "Sign up"
3. Create free account
4. Verify email
5. Done!

### Step 1B: Create Repository on GitHub.com

1. Go to **github.com** (logged in)
2. Click **`+`** icon (top right)
3. Select **"New repository"**
4. Fill in:
   ```
   Repository name: loan-bot
   Description: Telegram Bot for Educational Microfinance
   Visibility: Public (recommended)
   Initialize with README: No (we have our own)
   ```
5. Click **"Create repository"**
6. Copy the HTTPS URL shown (looks like: `https://github.com/YOUR-USERNAME/loan-bot.git`)

---

## Part 2: Push Code to GitHub

### Step 2A: Install Git (if needed)

**Windows:**
1. Download from https://git-scm.com/download/win
2. Run installer, accept defaults
3. Restart computer

**Mac:**
```bash
brew install git
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install git
```

### Step 2B: Configure Git (First Time Only)

```bash
# Replace with your info
git config --global user.name "Your Name"
git config --global user.email "your.email@gmail.com"

# Verify
git config --global user.name
git config --global user.email
```

### Step 2C: Initialize & Push Your Project

**In your loan_bot folder:**

```bash
# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Telegram Loan Bot with complete documentation"

# Add remote repository (replace URL with yours)
git remote add origin https://github.com/YOUR-USERNAME/loan-bot.git

# Create main branch and push
git branch -M main
git push -u origin main
```

### Step 2D: Verify on GitHub

1. Go to `https://github.com/YOUR-USERNAME/loan-bot`
2. Should see all your files
3. Green checkmark means CI/CD is working

---

## Part 3: Set Up Environment Variables

### For Local Development

Create `.env` file in your project folder:

```bash
# Create .env file
touch .env

# Edit it with your editor and add:
BOT_TOKEN=123456789:ABCDefGhIjKlMnOpQrStUvWxYz
DATABASE_PATH=/path/to/Loan_Bot_Database_NEW.xlsx
ENVIRONMENT=development
LOG_LEVEL=INFO
```

**Never commit .env to GitHub!** (Protected by .gitignore)

### For Cloud Deployment

**DO NOT put token in code!** Use environment variables provided by cloud service.

---

## Part 4: Setup Cloud Deployment

### Option 1: Render.com (Recommended) ⭐

#### Step 1: Create Render Account
1. Go to **render.com**
2. Click "Sign up"
3. Choose "Sign up with GitHub"
4. Authorize Render to access your GitHub
5. Done!

#### Step 2: Create Web Service
1. Dashboard → **"New +"** → **"Web Service"**
2. Connect your repository:
   - Select **loan-bot**
   - Click **"Connect"**
3. Configure service:
   ```
   Name: loan-bot
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python loan_bot.py
   ```
4. Click **"Create Web Service"**

#### Step 3: Add Environment Variables
1. Service Dashboard → **"Environment"**
2. Click **"Add Environment Variable"**
3. Add these variables:
   ```
   BOT_TOKEN = [paste your token here]
   DATABASE_PATH = /mnt/user-data/uploads/Loan_Bot_Database_NEW.xlsx
   ENVIRONMENT = production
   ```
4. Save (auto-deploys)

#### Step 4: Monitor Deployment
1. Click **"Logs"** tab
2. Wait for "Bot is running" message
3. Check bot in Telegram

**Cost:** Free tier or $7+/month

---

### Option 2: Railway.app

#### Step 1: Create Account
1. Go to **railway.app**
2. Sign up with GitHub
3. Authorize

#### Step 2: Create Project
1. Dashboard → **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose **loan-bot** repository
4. Done!

#### Step 3: Add Variables
1. Project → **"Variables"**
2. Add:
   - `BOT_TOKEN` = your token
   - `DATABASE_PATH` = database path
   - `ENVIRONMENT` = production
3. Deploy auto-starts

**Cost:** Free $5/month credit, then usage-based

---

### Option 3: Replit.com

#### Step 1: Create Account
1. Go to **replit.com**
2. Sign up with GitHub

#### Step 2: Import Repository
1. Click **"Create Repl"**
2. Choose **"Import from GitHub"**
3. Paste: `https://github.com/YOUR-USERNAME/loan-bot`
4. Click **"Import"**

#### Step 3: Set Environment
1. Create **`.env`** file with:
   ```
   BOT_TOKEN=your_token_here
   ```
2. Click **"Run"**
3. Done!

**Cost:** Free (with limitations)

---

### Option 4: Self-Hosted VPS

#### Step 1: Buy Server
- **DigitalOcean**: $5/month (referral: $100 credit)
- **Linode**: $5/month
- **Vultr**: $2.50/month
- **AWS EC2**: Free tier available

#### Step 2: SSH into Server
```bash
ssh root@your.server.ip
```

#### Step 3: Setup Environment
```bash
# Update system
apt-get update && apt-get upgrade -y

# Install dependencies
apt-get install -y git python3-pip

# Clone repository
git clone https://github.com/YOUR-USERNAME/loan-bot.git
cd loan-bot

# Install Python packages
pip install -r requirements.txt

# Create .env file
nano .env
# Add:
# BOT_TOKEN=your_token
# Press Ctrl+X, Y, Enter
```

#### Step 4: Run with Systemd (Permanent)
```bash
# Create service file
sudo nano /etc/systemd/system/loan-bot.service
```

Paste this:
```ini
[Unit]
Description=Telegram Loan Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/loan-bot
ExecStart=/usr/bin/python3 /root/loan-bot/loan_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then:
```bash
# Save: Ctrl+X, Y, Enter

# Enable and start
sudo systemctl enable loan-bot.service
sudo systemctl start loan-bot.service

# Check status
sudo systemctl status loan-bot.service

# View logs
sudo journalctl -u loan-bot.service -f
```

**Cost:** $5-40/month depending on usage

---

## Part 5: Deploy Secrets Management

### GitHub Secrets (for CI/CD)

If you want automatic deployment to cloud:

1. Repository → **Settings** → **Secrets and variables** → **Actions**
2. Click **"New repository secret"**
3. Name: `RENDER_DEPLOY_HOOK`
4. Value: (from Render.com settings)
5. Save

This allows `.github/workflows/deploy.yml` to auto-deploy when you push.

---

## Part 6: Database File Management

### Option A: Check into GitHub (Recommended for small databases)

```bash
git add Loan_Bot_Database_NEW.xlsx
git commit -m "Add MFI database"
git push origin main
```

### Option B: Use External Storage

If database is large, use cloud storage:

1. **Google Drive:**
   - Upload file
   - Get shareable link
   - Update `DATABASE_PATH` in environment variables

2. **AWS S3:**
   - Upload to S3 bucket
   - Get presigned URL
   - Use in `DATABASE_PATH`

3. **GitHub Releases:**
   - Upload as release asset
   - Download during deployment

---

## Part 7: Environment Variables Checklist

### Required Variables
- [ ] `BOT_TOKEN` - Your Telegram bot token
- [ ] `DATABASE_PATH` - Path to Excel file

### Optional Variables
- [ ] `ENVIRONMENT` - "development" or "production"
- [ ] `LOG_LEVEL` - DEBUG, INFO, WARNING, ERROR
- [ ] `SMTP_SERVER` - Email server (for future features)
- [ ] `SENDER_EMAIL` - Email for notifications

### How to Get Each:

**BOT_TOKEN:**
1. Open Telegram
2. Search `@BotFather`
3. Type `/start`, then `/newbot`
4. Follow instructions
5. Copy token

**DATABASE_PATH:**
```
/mnt/user-data/uploads/Loan_Bot_Database_NEW.xlsx  # If uploaded
./Loan_Bot_Database_NEW.xlsx                       # If local
https://github.com/you/loan-bot/raw/main/Loan_Bot_Database_NEW.xlsx  # GitHub raw
```

---

## Part 8: Testing Your Setup

### Test Locally First
```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
echo 'BOT_TOKEN=your_token' > .env

# Run bot
python loan_bot.py

# In another terminal, test:
python -c "from telegram import Bot; Bot('your_token').get_me()"
```

### Test on Cloud
1. Deploy to cloud service
2. Check logs
3. Open Telegram
4. Search for your bot
5. Send `/start`
6. Test each feature

---

## Part 9: Auto-Deployment (Optional)

### GitHub Actions to Render Webhook

1. Get Render webhook:
   - Render.com → Services → loan-bot → Settings
   - Copy "Deploy Hook" URL

2. Add to GitHub:
   - Repository → Settings → Secrets
   - Name: `RENDER_DEPLOY_HOOK`
   - Value: (paste webhook URL)

3. Update `.github/workflows/deploy.yml` to use it (already done!)

Now every push to main automatically deploys!

---

## Part 10: Troubleshooting

### "Bot token invalid"
- Verify token in `.env` or environment variables
- Check for extra spaces
- Get new token from BotFather

### "Database file not found"
- Verify file path is correct
- Check file exists on server
- Use absolute path or check working directory

### "Permission denied" when pushing
- Configure git: `git config --global user.name/email`
- Use HTTPS instead of SSH
- Create personal access token if needed

### "Bot not responding"
- Check logs in cloud dashboard
- Verify bot is running
- Restart service
- Check internet connection

### "Deployment failed"
- Check GitHub Actions logs
- Verify all environment variables set
- Check Python version compatibility
- Review error messages in logs

---

## Quick Commands Reference

```bash
# GitHub commands
git init                    # Initialize repo
git add .                   # Stage all files
git commit -m "message"     # Commit
git push origin main        # Push to GitHub
git pull origin main        # Pull latest
git status                  # Check status
git log --oneline           # View history

# Cloud deployment
git push origin main        # Auto-deploys if webhook configured
# Then check cloud dashboard for deployment status

# Testing
python loan_bot.py          # Run locally
python -m pytest            # Run tests (if configured)

# Environment
nano .env                   # Edit environment file
cat .env                    # View environment file
```

---

## File Checklist Before Pushing

- [ ] loan_bot.py (or loan_bot_cloud_ready.py)
- [ ] requirements.txt
- [ ] Loan_Bot_Database_NEW.xlsx
- [ ] README.md
- [ ] QUICKSTART.md
- [ ] SETUP_GUIDE.md
- [ ] FEATURE_GUIDE.md
- [ ] ADMIN_GUIDE.md
- [ ] .env.example (not .env!)
- [ ] .gitignore
- [ ] .github/workflows/deploy.yml

**NOT in GitHub:**
- [ ] .env (your real secrets)
- [ ] venv/ (virtual environment)
- [ ] __pycache__/ (Python cache)
- [ ] *.log (logs)
- [ ] .DS_Store (Mac)

---

## Success Indicators

✅ **Local Development:**
- Bot runs without errors: `python loan_bot.py`
- All features work in Telegram
- No undefined token errors

✅ **GitHub Repository:**
- All files visible on GitHub
- Green checkmark on Actions tab
- README renders properly

✅ **Cloud Deployment:**
- Service shows "running" status
- Logs show "Bot is running"
- Bot responds in Telegram
- Applications are logged

---

## Next Steps

1. ✅ Create GitHub account
2. ✅ Create repository
3. ✅ Push code to GitHub
4. ✅ Choose cloud platform
5. ✅ Deploy from GitHub
6. ✅ Test in Telegram
7. ✅ Share with users!

---

**Your bot is now production-ready and deployed on GitHub!** 🎉

For specific cloud platform docs:
- Render: https://render.com/docs
- Railway: https://docs.railway.app
- Replit: https://docs.replit.com
- DigitalOcean: https://docs.digitalocean.com
