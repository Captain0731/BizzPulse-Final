# Vercel Deployment Guide

## ✅ Optimized for Vercel Serverless

**Changes Made:**
- ✅ Removed database dependencies (SQLite, SQLAlchemy)
- ✅ Disabled CSRF for serverless APIs
- ✅ Simplified form validation (no Flask-WTF)
- ✅ Single `/api/app.py` entry point
- ✅ No cold-start DB initialization
- ✅ Lightweight dependencies
- ✅ Email-only functionality (no DB storage)

---

## 🚀 Deploy Now

### 1. Push to GitHub
```bash
git add .
git commit -m "Vercel-optimized serverless deployment"
git push origin main
```

### 2. Deploy to Vercel

**Option A: Vercel Dashboard (Recommended)**
1. Go to https://vercel.com
2. Click "Add New Project"
3. Import from GitHub: `BizzPulse-Final`
4. Vercel auto-detects configuration from `vercel.json`
5. Add environment variables:
   ```
   SECRET_KEY=your-secret-key
   RESEND_API_KEY=your-resend-api-key
   ADMIN_EMAIL=your-email@example.com
   ```
6. Click "Deploy"

**Option B: Vercel CLI**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

---

## 🔧 Environment Variables

Set in Vercel Dashboard → Project → Settings → Environment Variables:

| Variable | Value | Required |
|----------|-------|----------|
| `SECRET_KEY` | Random string | Yes |
| `RESEND_API_KEY` | Your Resend API key | Yes (for emails) |
| `ADMIN_EMAIL` | Your email address | Yes |

Generate SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 📊 Available Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Homepage |
| `/api/health` | GET | Health check |
| `/api/contact` | POST | Contact form (sends emails) |
| `/api/newsletter` | POST | Newsletter subscription |
| `/api/generate-pdf` | GET | Generate portfolio PDF |

---

## ✅ Test Deployment

```bash
# Health check
curl https://your-app.vercel.app/api/health

# Should return:
# {"status":"healthy","platform":"vercel"}

# Test contact form
curl -X POST https://your-app.vercel.app/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "message": "Test message"
  }'
```

---

## 🎯 What Works on Vercel

✅ Contact form (sends emails via Resend)
✅ Newsletter subscription (logs email)
✅ PDF generation
✅ All static pages
✅ Health check endpoint
✅ No cold-start crashes
✅ Fast response times

---

## ❌ What's Removed (Serverless Limitations)

❌ Database storage (SQLite/PostgreSQL)
❌ Contact history (no DB)
❌ Newsletter subscriber list (no DB)
❌ Admin dashboard (no DB data)

**Note:** Contact form still works - emails are sent to admin. No data is stored on Vercel.

---

## 🔄 Add Database (Optional)

If you need data storage, connect external database:

### Option 1: Vercel Postgres (Paid)
```bash
vercel postgres create
# Follow prompts, DATABASE_URL auto-set
```

### Option 2: Supabase (Free tier)
```bash
# Sign up: https://supabase.com
# Get PostgreSQL connection string
# Add to Vercel env vars: DATABASE_URL
```

Then update `api/app.py` to initialize SQLAlchemy with DATABASE_URL.

---

## 🐛 Troubleshooting

### 500 Error
- Check Vercel logs: Dashboard → Deployments → View Function Logs
- Verify environment variables are set
- Check RESEND_API_KEY is valid

### Contact form not working
- Verify RESEND_API_KEY in environment variables
- Check email_service.py has correct sender email
- View function logs for errors

### PDF generation fails
- Check if reportlab is in requirements.txt
- Verify static/img/ files are included in deployment
- Check function timeout (Vercel: 10s on free tier)

---

## 📝 Custom Domain (Optional)

1. Vercel Dashboard → Project → Settings → Domains
2. Add domain: `yourdomain.com`
3. Update DNS:
   ```
   A     @     76.76.21.21
   CNAME www   cname.vercel-dns.com
   ```

---

## 🔄 Update Deployment

```bash
# Make changes
git add .
git commit -m "Update"
git push origin main

# Vercel auto-deploys on push
```

---

## 📊 Monitoring

**View Logs:**
- Vercel Dashboard → Deployments → Select deployment → "View Function Logs"

**Metrics:**
- Dashboard → Analytics
- See requests, response times, errors

---

## ⚡ Performance

- Cold start: ~1-2s
- Warm response: ~100-300ms
- Function timeout: 10s (free tier)
- Max payload: 4.5MB

**Optimize:**
- Keep dependencies minimal ✅
- Remove database operations ✅
- Use edge functions for static content ✅

---

## 🎉 Success Checklist

- [x] Code pushed to GitHub
- [ ] Vercel project created
- [ ] Environment variables set (SECRET_KEY, RESEND_API_KEY, ADMIN_EMAIL)
- [ ] Deployment successful
- [ ] Health check returns 200: `/api/health`
- [ ] Contact form sends emails
- [ ] PDF generation works
- [ ] All pages load correctly

---

**Your app will be live at**: `https://your-project-name.vercel.app`

