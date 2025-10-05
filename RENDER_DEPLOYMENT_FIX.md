# Fix "Not Found" Error - Deploy Django on Render (Web Service)

## ❌ Problem: Deployed as Static Site

You deployed your Django app as a **Static Site**, which only works for HTML/CSS/JS files. Django is a **dynamic Python web application** that needs a Python server to run.

---

## ✅ Solution: Deploy as Web Service

### Step-by-Step Fix:

#### 1. Delete the Static Site Deployment

**Go to Render Dashboard:**
1. Visit: https://dashboard.render.com
2. Find your static site deployment
3. Click on it
4. Go to "Settings" (bottom of left sidebar)
5. Scroll down to "Danger Zone"
6. Click "Delete Static Site"
7. Confirm deletion

---

#### 2. Create New Web Service Deployment

**Option A: Use Render Dashboard (Manual)**

1. **Go to Render Dashboard:**
   - https://dashboard.render.com

2. **Click "New +" → "Web Service"**

3. **Connect GitHub Repository:**
   - Select: `Crypt-Analyst/St-Mary-s-Nyakhobi`
   - Click "Connect"

4. **Configure Web Service:**
   ```
   Name: st-marys-nyakhobi
   Runtime: Python 3
   Region: Oregon (or closest to Kenya)
   Branch: master
   
   Build Command: 
   ./build.sh
   
   Start Command:
   gunicorn st_marys_school.wsgi:application
   
   Instance Type: Free
   ```

5. **Add Environment Variables:**
   Click "Advanced" → "Add Environment Variable"
   
   ```
   Key: PYTHON_VERSION
   Value: 3.13.4
   
   Key: SECRET_KEY
   Value: [Click "Generate" button]
   
   Key: DEBUG
   Value: False
   
   Key: ALLOWED_HOSTS
   Value: .onrender.com
   
   Key: DATABASE_URL
   Value: [Leave empty for now, will use SQLite]
   ```

6. **Click "Create Web Service"**

7. **Wait for Build** (5-10 minutes)
   - Watch the logs
   - Should see: "Build successful"
   - Then: "Deploy live"

---

**Option B: Use render.yaml (Automatic)**

1. **Files Already Created:**
   - ✅ `build.sh` (build commands)
   - ✅ `render.yaml` (configuration)

2. **Commit and Push:**
   ```bash
   git add build.sh render.yaml
   git commit -m "Add Render deployment configuration for web service"
   git push origin master
   ```

3. **Create Web Service from Blueprint:**
   - Go to: https://dashboard.render.com
   - Click "New +" → "Blueprint"
   - Select your repository
   - Render will detect `render.yaml`
   - Click "Apply"

---

#### 3. Update Settings for Production

**File: `st_marys_school/settings.py`**

Add this at the bottom:

```python
# Production settings
if not DEBUG:
    # Security settings
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Allowed hosts
    ALLOWED_HOSTS = ['.onrender.com', 'stmarysnyakhobi.ac.ke']
    
    # Database (use PostgreSQL if available)
    import dj_database_url
    DATABASES['default'] = dj_database_url.config(
        conn_max_age=600,
        ssl_require=True
    )
```

**Install dj-database-url:**

Add to `requirements.txt`:
```
dj-database-url==2.1.0
```

---

#### 4. Update Allowed Hosts After Deployment

Once deployed, Render gives you a URL like:
```
https://st-marys-nyakhobi.onrender.com
```

**Update `st_marys_school/settings.py`:**
```python
ALLOWED_HOSTS = [
    'st-marys-nyakhobi.onrender.com',  # Your Render URL
    '.onrender.com',
    '127.0.0.1',
    'localhost',
]
```

**Commit and push:**
```bash
git add st_marys_school/settings.py
git commit -m "Update allowed hosts for Render deployment"
git push origin master
```

Render will automatically redeploy!

---

## 🔧 Build Configuration Files

### `build.sh` (Already Created)
```bash
#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

### `render.yaml` (Already Created)
```yaml
services:
  - type: web
    name: st-marys-nyakhobi
    runtime: python
    buildCommand: "./build.sh"
    startCommand: "gunicorn st_marys_school.wsgi:application"
    envVars:
      - key: PYTHON_VERSION
        value: 3.13.4
```

---

## 🐛 Common Issues & Solutions

### Issue 1: "Application failed to respond"

**Cause:** Wrong start command

**Fix:** Ensure start command is:
```
gunicorn st_marys_school.wsgi:application
```

---

### Issue 2: "Pillow build failed"

**Status:** ✅ Fixed! (We updated to Pillow 10.4.0)

---

### Issue 3: "DisallowedHost" error

**Cause:** Your Render URL not in ALLOWED_HOSTS

**Fix:** Update `settings.py`:
```python
ALLOWED_HOSTS = ['your-app.onrender.com', '.onrender.com']
```

---

### Issue 4: "Static files not loading"

**Cause:** Collectstatic not run

**Fix:** Ensure `build.sh` includes:
```bash
python manage.py collectstatic --no-input
```

---

### Issue 5: "Database tables don't exist"

**Cause:** Migrations not run

**Fix:** Ensure `build.sh` includes:
```bash
python manage.py migrate
```

---

## 📋 Pre-Deployment Checklist

Before deploying, ensure:

- [x] ✅ `requirements.txt` has all dependencies
- [x] ✅ Pillow version updated (10.4.0)
- [x] ✅ `gunicorn` in requirements.txt
- [x] ✅ `build.sh` created
- [x] ✅ `render.yaml` created
- [ ] ⏳ Update ALLOWED_HOSTS with Render URL
- [ ] ⏳ Set DEBUG=False in production
- [ ] ⏳ Generate SECRET_KEY for production
- [ ] ⏳ Set up PostgreSQL database (optional)
- [ ] ⏳ Configure email settings

---

## 🚀 Quick Deployment (Right Now)

### Step 1: Commit Configuration Files
```bash
git add build.sh render.yaml requirements.txt
git commit -m "Add Render web service deployment configuration"
git push origin master
```

### Step 2: Create Web Service on Render
1. Go to: https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repo: `St-Mary-s-Nyakhobi`
4. Configure:
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn st_marys_school.wsgi:application`
   - **Python Version:** 3.13.4
5. Add Environment Variables:
   - `DEBUG` = `False`
   - `SECRET_KEY` = [Generate new key]
   - `ALLOWED_HOSTS` = `.onrender.com`
6. Click "Create Web Service"

### Step 3: Wait for Build
- Takes 5-10 minutes
- Watch logs for errors
- Should see "Deploy live" when ready

### Step 4: Update ALLOWED_HOSTS
1. Copy your Render URL (e.g., `st-marys-nyakhobi.onrender.com`)
2. Update `settings.py` with exact URL
3. Commit and push
4. Render auto-redeploys

### Step 5: Create Superuser (After Deployment)
```bash
# From Render dashboard, go to "Shell"
python manage.py createsuperuser
```

---

## 🎯 What Happens After Deployment

### 1. Your Website URLs:
```
Main Site: https://st-marys-nyakhobi.onrender.com
Admin Portal: https://st-marys-nyakhobi.onrender.com/admin/
```

### 2. First Visit:
- Site loads successfully ✅
- Homepage displays
- Admin portal accessible
- Static files (CSS/JS) work

### 3. Content Management:
- Login to admin portal
- Add news, events, photos
- Content appears on public site
- Everything works like local development

---

## 📊 Differences: Static Site vs Web Service

### Static Site (❌ Wrong for Django):
```
✗ Only serves HTML/CSS/JS files
✗ No Python code execution
✗ No database access
✗ No admin portal
✗ No dynamic content
✗ Results in "Not Found" errors
```

### Web Service (✅ Correct for Django):
```
✓ Runs Python/Django application
✓ Executes Python code
✓ Database connections work
✓ Admin portal accessible
✓ Dynamic content generation
✓ Forms and user interactions work
```

---

## 🔍 How to Check Current Deployment Type

**Static Site (Wrong):**
- URL looks like: `username-sitename.netlify.app` or `username.github.io`
- Only shows static files
- Returns 404 for `/admin/`
- No Python execution

**Web Service (Correct):**
- URL looks like: `appname.onrender.com` or `appname.herokuapp.com`
- Django app runs
- `/admin/` works
- Database queries execute

---

## 💡 Why Static Site Didn't Work

### What Happened:
1. You deployed Django as static site
2. Render/Netlify only copied HTML files
3. No Python interpreter running
4. No Django framework loaded
5. Result: "Not Found" for all pages

### What Should Happen:
1. Deploy as web service
2. Render runs Python server
3. Gunicorn starts Django
4. Database connects
5. Pages load dynamically
6. Admin portal works

---

## 🎓 Quick Commands Reference

### Local Development:
```bash
python manage.py runserver
```

### Production (Render):
```bash
gunicorn st_marys_school.wsgi:application
```

### Create Superuser (Production):
```bash
# From Render Shell
python manage.py createsuperuser
```

### Run Migrations (Production):
```bash
# From Render Shell
python manage.py migrate
```

### Collect Static Files (Production):
```bash
# From Render Shell or build.sh
python manage.py collectstatic --no-input
```

---

## ✅ Success Indicators

Your deployment is successful when:

1. ✅ Build completes without errors
2. ✅ "Deploy live" message appears
3. ✅ Homepage loads at your Render URL
4. ✅ Admin portal accessible at `/admin/`
5. ✅ Static files (CSS/JS) load correctly
6. ✅ Can login to admin
7. ✅ Can add/edit content
8. ✅ Changes appear on website

---

## 📞 Need Help?

### Check Logs:
1. Go to Render Dashboard
2. Click on your web service
3. Click "Logs" tab
4. Look for error messages

### Common Log Messages:

**Success:**
```
Build successful
Deploy live
Booting worker with pid: 123
```

**Error:**
```
Application failed to respond
DisallowedHost at /
ModuleNotFoundError: No module named 'gunicorn'
```

---

## 🎉 Next Steps After Successful Deployment

1. **Update DNS (if you have domain):**
   - Point `stmarysnyakhobi.ac.ke` to Render
   - Add custom domain in Render settings

2. **Set up SSL (automatic on Render):**
   - HTTPS enabled by default
   - No configuration needed

3. **Create superuser:**
   - Use Render Shell
   - Run `createsuperuser` command

4. **Add initial content:**
   - Login to admin portal
   - Add school information
   - Upload photos
   - Create news articles

5. **Monitor performance:**
   - Check Render metrics
   - Review error logs
   - Set up uptime monitoring

---

**Document:** Render Deployment Fix Guide  
**Version:** 1.0  
**Date:** October 5, 2025  
**Status:** Ready to Deploy

**Next Action:** Delete static site, create web service on Render!
