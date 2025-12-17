# Production Deployment Guide

## Railway Deployment (Recommended)

### 1. Prerequisites
- GitHub repository
- Railway account (https://railway.app)

### 2. Setup Database
```bash
# Railway will automatically provision PostgreSQL
# Database URL will be available as: $DATABASE_URL
```

### 3. Deploy to Railway

#### Option A: GitHub Integration (Recommended)
1. Push code to GitHub:
   ```bash
   git add .
   git commit -m "Production-ready refactor"
   git push origin main
   ```

2. Railway Dashboard:
   - Go to https://railway.app
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway auto-detects Python and uses `railway.json`

3. Add PostgreSQL:
   - Click "New" → "Database" → "Add PostgreSQL"
   - Railway automatically sets `DATABASE_URL`

4. Set Environment Variables:
   ```
   SECRET_KEY=generate-a-secure-random-key
   RESEND_API_KEY=your_resend_api_key
   ADMIN_EMAIL=admin@yourdomain.com
   FLASK_ENV=production
   ```

5. Deploy:
   - Railway automatically deploys on push
   - Get your domain: `https://your-app.railway.app`

#### Option B: Railway CLI
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Add PostgreSQL
railway add postgresql

# Deploy
railway up
```

### 4. Verify Deployment
```bash
# Check health
curl https://your-app.railway.app/api/health

# Should return: {"status": "healthy"}
```

### 5. Database Migration (First Time)
```bash
# Railway automatically runs db.create_all() on startup
# Tables are created from models.py
```

---

## Alternative: DigitalOcean App Platform

### 1. Create App
```bash
# Push to GitHub first
git push origin main
```

### 2. DigitalOcean Dashboard
- Go to "Apps" → "Create App"
- Connect GitHub repository
- Select branch: `main`

### 3. Configure
```yaml
# App Spec (auto-generated)
name: bizzpulse-backend
services:
- name: web
  github:
    repo: your-username/your-repo
    branch: main
  run_command: gunicorn app_refactored:app --workers 4 --bind 0.0.0.0:8080
  environment_slug: python
  instance_size_slug: basic-xxs
  instance_count: 1
  http_port: 8080
  
databases:
- name: bizzpulse-db
  engine: PG
  version: "15"
```

### 4. Environment Variables
```
DATABASE_URL=${db.DATABASE_URL}
SECRET_KEY=your-secret-key
RESEND_API_KEY=your-resend-key
ADMIN_EMAIL=admin@yourdomain.com
```

---

## Environment Variables Required

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| `SECRET_KEY` | Flask secret key (generate random) | `your-secret-key-here` |
| `RESEND_API_KEY` | Resend email API key | `re_xxxxxxxxxxxx` |
| `ADMIN_EMAIL` | Admin email for notifications | `admin@example.com` |
| `FLASK_ENV` | Environment (production/development) | `production` |
| `PORT` | Server port (auto-set by Railway) | `8080` |

---

## Generate SECRET_KEY

```python
import secrets
print(secrets.token_urlsafe(32))
```

Or:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## Post-Deployment Checklist

- [ ] Health check returns 200: `/api/health`
- [ ] Homepage loads: `/`
- [ ] Contact form works: `POST /api/contact`
- [ ] Newsletter works: `POST /api/newsletter`
- [ ] PDF generation works: `/api/generate-pdf`
- [ ] Database tables created
- [ ] Environment variables set
- [ ] SSL enabled (automatic on Railway/DigitalOcean)

---

## Monitoring & Logs

### Railway
```bash
# View logs
railway logs

# Or in dashboard: Project → Deployments → View Logs
```

### DigitalOcean
- App Platform → Your App → "Runtime Logs"

---

## Custom Domain (Optional)

### Railway
1. Project Settings → "Domains"
2. Add custom domain: `api.yourdomain.com`
3. Update DNS:
   ```
   CNAME api -> your-app.railway.app
   ```

### DigitalOcean
1. App Settings → "Domains"
2. Add domain and follow DNS instructions

---

## Rollback

### Railway
```bash
# Dashboard → Deployments → Select previous deployment → "Redeploy"
```

### DigitalOcean
- App → Deployments → "Roll Back"

