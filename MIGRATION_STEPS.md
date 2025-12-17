# Migration from Vercel to Railway

## Quick Migration Steps

### 1. Update Your Codebase
```bash
# Rename files to use refactored versions
mv app_refactored.py app.py.backup
mv app_refactored.py app.py
mv routes_refactored.py routes.py
mv requirements_production.txt requirements.txt

# Commit changes
git add .
git commit -m "Migrate to Railway production setup"
git push origin main
```

### 2. Deploy to Railway (5 minutes)
```bash
# Go to https://railway.app
# Click "New Project" → "Deploy from GitHub"
# Select your repository
# Add PostgreSQL database
# Set environment variables (see env_example.txt)
# Deploy automatically starts
```

### 3. Environment Variables (Copy-Paste)
```
SECRET_KEY=<generate with: python -c "import secrets; print(secrets.token_urlsafe(32))">
RESEND_API_KEY=<your_resend_key>
ADMIN_EMAIL=<your_email>
FLASK_ENV=production
```

### 4. Verify Deployment
```bash
curl https://your-app.railway.app/api/health
# Should return: {"status":"healthy"}
```

### 5. Update Frontend (if separate)
```javascript
// Change API base URL from Vercel to Railway
const API_URL = 'https://your-app.railway.app/api';
```

---

## File Structure (Production)

```
project/
├── app.py                    # Main application (refactored)
├── routes.py                 # Routes with blueprints
├── config.py                 # Configuration classes
├── models.py                 # Database models (unchanged)
├── forms.py                  # WTForms (unchanged)
├── email_service.py          # Email sender (unchanged)
├── pdf_generator.py          # PDF generator (unchanged)
├── requirements.txt          # Python dependencies
├── Procfile                  # Gunicorn start command
├── railway.json              # Railway configuration
├── nixpacks.toml             # Build configuration
├── DEPLOYMENT.md             # Full deployment guide
├── templates/                # HTML templates
├── static/                   # Static assets
└── instance/                 # Local DB (ignored in production)
```

---

## What Changed

### ✓ Fixed Issues
- ❌ `init_app()` on import → ✅ Application factory pattern
- ❌ CSRF on API routes → ✅ Exempt API endpoints
- ❌ SQLite on serverless → ✅ PostgreSQL on Railway
- ❌ Module-level imports → ✅ Blueprint registration
- ❌ 10s timeout → ✅ Traditional server (no limits)

### ✓ New Features
- ✅ Health check endpoint: `/api/health`
- ✅ Proper logging with log levels
- ✅ CORS support for frontend
- ✅ Production/Development configs
- ✅ Gunicorn multi-worker setup
- ✅ Connection pooling for PostgreSQL
- ✅ Error handling without crashes

---

## Cost Comparison

| Platform | Free Tier | Paid |
|----------|-----------|------|
| **Railway** | $5 credit/month | $5/month + usage |
| **Vercel** | Serverless (crashes with DB) | Not suitable for backend |
| **DigitalOcean** | No free tier | $5/month (App Platform) |

**Recommendation**: Railway (best for full-stack Flask apps)

---

## Troubleshooting

### Database connection fails
```bash
# Check DATABASE_URL format
echo $DATABASE_URL
# Should be: postgresql://user:pass@host:5432/db
```

### App crashes on startup
```bash
# Check logs
railway logs

# Common issues:
# - Missing SECRET_KEY
# - Wrong DATABASE_URL format
# - Missing dependencies in requirements.txt
```

### Cannot reach API
```bash
# Verify deployment
railway status

# Check health endpoint
curl https://your-app.railway.app/api/health
```

---

## Rollback to Vercel (if needed)
```bash
git checkout HEAD~1 app.py routes.py
git commit -m "Rollback to Vercel version"
git push origin main
```

(Not recommended - Vercel not suitable for database-backed Flask apps)

