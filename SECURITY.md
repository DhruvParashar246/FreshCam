# Security Guidelines

## 🔐 Sensitive Information

This project uses several API keys and secrets that must be kept secure:

### Protected Files (Never Commit!)
- ✅ `.env` files (already in `.gitignore`)
- ✅ `ngrok.exe` (already in `.gitignore`)
- ✅ `*.sqlite` / `*.db` files (already in `.gitignore`)
- ✅ API keys, tokens, passwords

### API Keys Used
1. **Google Gemini API Key** - For AI-powered fruit analysis
2. **Roboflow API Key** - For computer vision model
3. **ngrok Auth Token** - For secure tunneling (temporary)

## 🛡️ Setup Instructions

### 1. Environment Variables

Create a `backend/.env` file (use `backend/.env.example` as template):

```env
# Google Gemini API Configuration
GEMINI_API_KEY=your_actual_gemini_key_here

# Roboflow API Configuration
ROBOFLOW_URL=https://detect.roboflow.com
ROBOFLOW_API_KEY=your_actual_roboflow_key_here
```

**Important**: Never commit this file! It's already in `.gitignore`.

### 2. ngrok Configuration

If using ngrok for tunneling:

```bash
cd backend
.\ngrok.exe config add-authtoken YOUR_NGROK_TOKEN
.\ngrok.exe http 8000
```

The ngrok URL changes each time you restart, so update `frontend/app/result.tsx` accordingly.

## 🚨 Before Pushing to GitHub

Run this checklist:

```bash
# 1. Check git status
git status

# 2. Verify .env is NOT listed
# If you see .env, run:
git rm --cached backend/.env

# 3. Verify no API keys in staged files
git diff --cached

# 4. Search for exposed secrets
git grep -i "AIzaSy"  # Gemini keys start with this
git grep -i "api_key"
```

## 🔍 Files Already Secured

The following files have been cleaned and are safe to commit:
- ✅ `docs/BACKEND_SPOONACULAR_SETUP.md` - Placeholders only
- ✅ `docs/BACKEND_TEST_RESULTS.md` - Placeholders only
- ✅ `backend/.env.example` - Template with placeholders
- ✅ `.gitignore` - Comprehensive exclusions

## 📝 Safe to Commit

These files are safe and should be committed:
- Source code (`.py`, `.tsx`, `.ts` files)
- Documentation (`.md` files with placeholders)
- Configuration templates (`.env.example`)
- `.gitignore`
- `requirements.txt`
- `package.json`

## ⚠️ If You Accidentally Commit Secrets

If you've already committed API keys:

1. **Immediately revoke the exposed keys** from the provider's dashboard
2. Generate new API keys
3. Update your local `.env` file
4. Remove sensitive commits from git history:

```bash
# Remove file from all git history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch backend/.env" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (only if repository is private and you're the only contributor)
git push origin --force --all
```

## 🎯 Best Practices

1. **Never hardcode API keys** in source code
2. **Always use environment variables** via `.env` files
3. **Keep `.env` in `.gitignore`** 
4. **Use `.env.example`** as a template for others
5. **Rotate keys regularly** if they might be exposed
6. **Use separate keys** for development and production
7. **Review git diff** before committing

## 🆘 Getting API Keys

- **Gemini API**: https://makersuite.google.com/app/apikey
- **Roboflow API**: https://roboflow.com (after creating account/project)
- **ngrok Auth Token**: https://dashboard.ngrok.com/get-started/your-authtoken

---

**Remember**: Security is everyone's responsibility! 🔒
