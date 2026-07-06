# 🚀 Deploy Loan Bot from GitHub

## Step 1: Create GitHub Repository

### Option A: Using GitHub Web Interface

1. **Go to GitHub.com** and sign in (create account if needed)
2. **Create new repository:**
   - Click `+` icon → "New repository"
   - Name: `loan-bot` (or any name you prefer)
   - Description: "Telegram Loan Bot for Educational Institutions"
   - Choose "Public" (to share) or "Private" (for internal use)
   - Initialize with README (GitHub will create one, but we have ours)
   - Click "Create repository"

### Option B: Using Git Command Line

```bash
# Navigate to your loan_bot folder
cd loan_bot

# Initialize git repo
git init

# Add remote (replace USERNAME with your GitHub username)
git remote add origin https://github.com/USERNAME/loan-bot.git

# Create main branch
git branch -M main
```

---

## Step 2: Add Files to GitHub

### Setup Git (First Time Only)

```bash
# Configure git with your info
git config --global user.name "Your Name"
git config --global user.email "your.email@gmail.com"
```

### Push All Files to GitHub

```bash
# Navigate to your project folder
cd loan_bot

# Stage all files
git add .

# Create commit message
git commit -m "Initial commit: Complete Telegram Loan Bot with documentation"

# Push to GitHub (replace main if using different branch)
git push -u origin main
```

### What Gets Uploaded?

✅ **Uploaded to GitHub:**
- loan_bot.py
- requirements.txt
- .gitignore
- .env.example
- All documentation files (README.md, SETUP_GUIDE.md, etc.)
- Database file (Loan_Bot_Database_NEW.xlsx)
- .github/workflows/ (CI/CD configuration)

❌ **NOT Uploaded (protected by .gitignore):**
- .env (your actual bot token)
- bot.log (activity logs)
- venv/ (virtual environment)
- __pycache__/ (Python cache)

---

## Step 3: Verify on GitHub

1. Go to `https://github.com/USERNAME/loan-bot`
2. You should see all your files
3. GitHub automatically renders README.md on the main page
4. All guides are visible as markdown files

---

## Step 4: Deploy to Cloud Services

### Option 1: Deploy to Render.com ⭐ (Recommended)

#### Step 1: Create Render Account
1. Go to **render.com**
2. Sign up with GitHub (easier)
3. Click "Authorize" to connect GitHub

#### Step 2: Create Web Service
1. Click "New +" → "Web Service"
2. Select your GitHub repository `loan-bot`
3. Click "Connect"

#### Step 3: Configure Service
```
Name: loan-bot
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: python loan_bot.py
```

#### Step 4: Add Environment Variables
1. Click "Environment" 
2. Add new variable:
   - Key: `BOT_TOKEN`
   - Value: (paste your bot token from @BotFather)
3. Click "Deploy"

#### Step 5: Wait for Deployment
- Render will build and start your bot
- Check "Logs" tab for any errors
- When you see "Bot is running", it's live!

**Cost:** Free (with limitations) or $7+/month for production

---

### Option 2: Deploy to Railway.app

#### Step 1: Create Railway Account
1. Go to **railway.app**
2. Sign up with GitHub

#### Step 2: New Project
1. Click "Create Project"
2. Select "Deploy from GitHub repo"
3. Select `loan-bot` repository

#### Step 3: Configure
1. Add Plugin → PostgreSQL (if using database)
2. Environment Variables:
   - BOT_TOKEN: (your token)
3. Click "Deploy"

**Cost:** Free $5 credit monthly, then pay-as-you-go

---

### Option 3: Deploy to Heroku (if still available)

⚠️ **Note:** Heroku free tier ended in 2022. Use Render or Railway instead.

---

### Option 4: Deploy to Replit

#### Step 1: Open Replit
1. Go to **replit.com**
2. Click "Create Repl"
3. Select "Import from GitHub"
4. Paste: `https://github.com/USERNAME/loan-bot`

#### Step 2: Configure
1. Create `.env` file with:
   ```
   BOT_TOKEN=your_token_here
   ```
2. Click "Run"

**Cost:** Free (with limitations)

---

### Option 5: Self-Hosted on VPS

#### Step 1: Get a Server
- DigitalOcean: $5/month
- Linode: $5/month
- AWS EC2: Free tier or pay-per-use
- Vultr: $2.50/month

#### Step 2: SSH into Server
```bash
ssh root@your.server.ip
```

#### Step 3: Clone Repository
```bash
# Install git
apt-get update && apt-get install git python3-pip

# Clone your repo
git clone https://github.com/USERNAME/loan-bot.git
cd loan-bot

# Install dependencies
pip install -r requirements.txt
```

#### Step 4: Create .env File
```bash
nano .env
# Paste:
# BOT_TOKEN=your_token_here
# Press Ctrl+X, Y, Enter
```

#### Step 5: Run Bot with Systemd (Permanent)
```bash
# Create service file
sudo nano /etc/systemd/system/loan-bot.service

# Paste:
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

# Save: Ctrl+X, Y, Enter

# Enable and start service
sudo systemctl enable loan-bot.service
sudo systemctl start loan-bot.service

# Check status
sudo systemctl status loan-bot.service
```

**Cost:** $5-40/month depending on server

---

## Step 5: Update Code on GitHub

### Making Changes

1. **Edit files locally**
   ```bash
   # Edit loan_bot.py or other files
   nano loan_bot.py
   ```

2. **Stage and commit changes**
   ```bash
   git add .
   git commit -m "Update interest rates in calculator"
   ```

3. **Push to GitHub**
   ```bash
   git push origin main
   ```

4. **Cloud service auto-deploys** (usually in 1-5 minutes)

### Branching (Best Practice)

```bash
# Create feature branch
git checkout -b feature/new-feature-name

# Make changes, commit, push
git add .
git commit -m "Add new feature"
git push origin feature/new-feature-name

# On GitHub, create Pull Request to merge to main
# After review, merge to main
# GitHub Actions tests automatically
# Deployment happens automatically
```

---

## Step 6: Monitor Your Bot

### Check Logs

**On Render:**
1. Dashboard → Select "loan-bot"
2. Click "Logs" tab
3. See real-time activity

**On Railway:**
1. Dashboard → Select project
2. Click "Logs"
3. View console output

**On Self-Hosted:**
```bash
# SSH into server
ssh root@your.server.ip

# Check service status
sudo systemctl status loan-bot.service

# View logs
sudo journalctl -u loan-bot.service -f

# Or check bot.log file
cat /root/loan-bot/bot.log
```

---

## Step 7: Set Up CI/CD (Automatic Testing)

GitHub Actions is already configured in `.github/workflows/deploy.yml`

### What It Does Automatically:
✅ Tests code when you push
✅ Checks for syntax errors
✅ Verifies Excel file exists
✅ Deploys to cloud if tests pass

### View Results:
1. Go to GitHub repo
2. Click "Actions" tab
3. See build status
4. Click on a run to see details

### Deploy Hooks (Optional Advanced)

To auto-deploy when you push:

**For Render:**
1. Settings → Deploy Hook
2. Copy the webhook URL
3. On GitHub: Settings → Secrets → New secret
4. Name: `RENDER_DEPLOY_HOOK`
5. Value: (paste webhook URL)

**For Railway:**
1. Settings → Deploy Triggers
2. Copy GitHub deploy token
3. Same process as above

---

## Step 8: Keep Your Code Updated

### Pull Latest Changes
```bash
# If someone else made changes on GitHub
git pull origin main
```

### Update Dependencies
```bash
# When new versions are available
pip install --upgrade -r requirements.txt

# Update requirements.txt
pip freeze > requirements.txt

# Commit and push
git add requirements.txt
git commit -m "Update dependencies"
git push origin main
```

### Regular Maintenance
```bash
# Check git status
git status

# See commit history
git log --oneline

# See branches
git branch -a
```

---

## Complete Workflow Example

### Scenario: Update Interest Rates

```bash
# Step 1: Pull latest
git pull origin main

# Step 2: Create feature branch
git checkout -b update/interest-rates

# Step 3: Edit Excel file (Loan_Bot_Database_NEW.xlsx)
# Edit interest rates in the spreadsheet

# Step 4: Update and commit
git add Loan_Bot_Database_NEW.xlsx
git commit -m "Update interest rates for Q1 2024"

# Step 5: Push changes
git push origin update/interest-rates

# Step 6: On GitHub, create Pull Request
# - Go to GitHub
# - Click "Compare & pull request"
# - Add description
# - Click "Create pull request"

# Step 7: Review (optional)
# - CI/CD tests run automatically
# - If tests pass, merge to main

# Step 8: Deployment
# - Cloud service auto-deploys
# - Changes live in 1-5 minutes
```

---

## GitHub Repository Features

### 1. Issues (Bug Reports & Requests)
```
GitHub → Issues → New Issue
Title: "Calculator showing wrong monthly payment"
Description: Details and steps to reproduce
Label: bug, help wanted, etc.
```

### 2. Discussions (Questions & Ideas)
```
GitHub → Discussions → New Discussion
Category: Ideas, Help, etc.
Engage with community
```

### 3. Wiki (Documentation)
```
GitHub → Wiki → New Page
Can create additional documentation
Link from README
```

### 4. Releases (Version Management)
```
GitHub → Releases → Create new release
Tag: v1.0, v1.1, etc.
Add release notes
Users can download specific versions
```

### 5. Projects (Kanban Board)
```
GitHub → Projects → New Project
Organize tasks and features
Track progress visually
```

---

## Troubleshooting GitHub Deployment

### Issue: "Permission denied" when pushing
```bash
# Use HTTPS instead of SSH (or configure SSH keys)
git remote set-url origin https://github.com/USERNAME/loan-bot.git
git push origin main
```

### Issue: "Repository not found"
- Check GitHub username is correct
- Verify repository exists
- Check if private (need access token)

### Issue: Merge conflicts
```bash
# Check status
git status

# Resolve conflicts manually in files
# Then:
git add .
git commit -m "Resolve merge conflicts"
git push origin main
```

### Issue: Bot not starting on cloud
1. Check environment variables (BOT_TOKEN set?)
2. Check logs for error messages
3. Verify Excel file path is correct
4. Ensure requirements.txt is in repo

### Issue: Want to undo last commit
```bash
# Before pushing (local only)
git reset --soft HEAD~1

# After pushing (create new commit)
git revert HEAD
git push origin main
```

---

## Best Practices

### ✅ Do:
- ✅ Commit messages should be descriptive
- ✅ Create branches for new features
- ✅ Test locally before pushing
- ✅ Use .gitignore to protect secrets
- ✅ Keep README updated
- ✅ Regular commits (not huge changes)

### ❌ Don't:
- ❌ Push bot token to GitHub
- ❌ Commit large files without need
- ❌ Force push to main branch
- ❌ Merge without reviewing changes
- ❌ Leave sensitive data in code comments

---

## Quick Reference Commands

```bash
# Clone repository
git clone https://github.com/USERNAME/loan-bot.git

# Check status
git status

# See changes
git diff

# Stage changes
git add .
git add file.txt          # Specific file

# Commit
git commit -m "Your message"

# Push to GitHub
git push origin main

# Pull latest
git pull origin main

# Create branch
git checkout -b feature-name

# Switch branch
git checkout main

# Delete branch
git branch -d feature-name

# See all branches
git branch -a

# Merge branch to main
git checkout main
git merge feature-name

# Undo last commit (before push)
git reset --soft HEAD~1

# View commit history
git log --oneline
```

---

## Monitor Your Bot in Production

### Useful Commands (after SSH to server)

```bash
# View bot logs
tail -f bot.log

# Check if running
ps aux | grep loan_bot

# Restart bot
sudo systemctl restart loan-bot.service

# See recent activity
grep "New Application" bot.log | tail -20

# Count applications today
grep "$(date +%Y-%m-%d)" bot.log | grep "New Application" | wc -l

# Check memory usage
free -h

# Check disk space
df -h
```

---

## GitHub Repository URL Structure

Once you create your repository:

**Main Page:**
```
https://github.com/USERNAME/loan-bot
```

**Clone URL (HTTPS):**
```
https://github.com/USERNAME/loan-bot.git
```

**Clone URL (SSH - requires setup):**
```
git@github.com:USERNAME/loan-bot.git
```

---

## Sharing Your Bot

### Share With Others:
1. Repository is public
2. Send them: `https://github.com/USERNAME/loan-bot`
3. They can clone and deploy themselves

### Collaboration:
1. Add collaborators: Settings → Manage access
2. They can clone, branch, and create pull requests
3. You review and merge changes

---

## Getting Help

### Resources:
- **Git Documentation:** https://git-scm.com/doc
- **GitHub Help:** https://docs.github.com
- **Render Docs:** https://render.com/docs
- **Railway Docs:** https://docs.railway.app

### Common Questions:
- **"How do I update my local code?"** → `git pull origin main`
- **"How do I deploy changes?"** → Push to main, cloud auto-deploys
- **"How do I revert changes?"** → `git revert HEAD` then push
- **"How do I backup my code?"** → GitHub is your backup!

---

## Summary

1. ✅ Create GitHub account
2. ✅ Create new repository
3. ✅ Push all files to GitHub
4. ✅ Choose cloud service (Render recommended)
5. ✅ Deploy from GitHub
6. ✅ Add bot token as environment variable
7. ✅ Your bot is LIVE! 🚀

**Your code is safe on GitHub, your bot runs in the cloud, and you can update it anytime!**

---

**Need help?** Refer back to these steps or check the specific cloud service documentation.

**Ready to go live?** You now have a professional GitHub repository with automated CI/CD! 🎉
