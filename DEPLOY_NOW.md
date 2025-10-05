# 🚀 Fix "Not Found" - Quick Deployment Guide

## ❌ The Problem

You deployed Django as a **Static Site** but Django needs a **Web Service** with Python.

```
Static Site (Wrong):          Web Service (Correct):
├─ Only HTML/CSS/JS          ├─ Runs Python code
├─ No database               ├─ Database connected
├─ No admin portal           ├─ Admin portal works
└─ Result: "Not Found"       └─ Result: Website works!
```

---

## ✅ The Fix (3 Steps)

### Step 1: Delete Static Site Deployment

1. Go to: **https://dashboard.render.com**
2. Click on your **static site**
3. Settings → Danger Zone
4. **Delete Static Site**

---

### Step 2: Create Web Service

1. **Go to Render Dashboard**
   - https://dashboard.render.com

2. **Click "New +" → "Web Service"**

3. **Connect GitHub Repository**
   - Repository: `Crypt-Analyst/St-Mary-s-Nyakhobi`
   - Branch: `master`
   - Click "Connect"

4. **Configure Web Service:**
   ```
   Name: st-marys-nyakhobi
   
   Runtime: Python 3
   
   Build Command:
   chmod +x build.sh && ./build.sh
   
   Start Command:
   gunicorn st_marys_school.wsgi:application
   
   Root Directory: (leave blank)
   ```

5. **Add Environment Variables:**
   
   Click "Advanced" → "Add Environment Variable"
   
   **Variable 1:**
   ```
   Key: PYTHON_VERSION
   Value: 3.13.4
   ```
   
   **Variable 2:**
   ```
   Key: SECRET_KEY
   Value: [Click "Generate" button]
   ```
   
   **Variable 3:**
   ```
   Key: DEBUG
   Value: False
   ```
   
   **Variable 4:**
   ```
   Key: ALLOWED_HOSTS
   Value: .onrender.com
   ```

6. **Select Free Plan**

7. **Click "Create Web Service"**

---

### Step 3: Wait for Deployment

**What You'll See:**
```
Building... (5-10 minutes)
├─ Installing dependencies
├─ Running migrations
├─ Collecting static files
└─ Starting gunicorn

✅ Deploy live!
```

**Your Site URL:**
```
https://st-marys-nyakhobi.onrender.com
```

---

## 🎯 After Deployment

### 1. Update ALLOWED_HOSTS

Once you get your Render URL (e.g., `st-marys-nyakhobi.onrender.com`):

**Edit: `st_marys_school/settings.py`**

Find this line:
```python
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost', cast=Csv())
```

Change to:
```python
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='st-marys-nyakhobi.onrender.com,.onrender.com,127.0.0.1,localhost', cast=Csv())
```

**OR** add in Render environment variables:
```
Key: ALLOWED_HOSTS
Value: st-marys-nyakhobi.onrender.com,.onrender.com
```

**Commit and push:**
```bash
git add st_marys_school/settings.py
git commit -m "Add Render URL to ALLOWED_HOSTS"
git push origin master
```

Render will automatically redeploy!

---

### 2. Create Superuser

**In Render Dashboard:**
1. Go to your web service
2. Click "Shell" tab
3. Run:
```bash
python manage.py createsuperuser
```

Follow prompts:
```
Username: admin
Email: admin@stmarysnyakhobi.ac.ke
Password: [your secure password]
```

---

### 3. Access Your Site

**Main Website:**
```
https://st-marys-nyakhobi.onrender.com
```

**Admin Portal:**
```
https://st-marys-nyakhobi.onrender.com/admin/
```

---

## 🐛 Troubleshooting

### Issue: "DisallowedHost"

**Error:**
```
DisallowedHost at /
Invalid HTTP_HOST header: 'st-marys-nyakhobi.onrender.com'
```

**Fix:**
Update `ALLOWED_HOSTS` in settings.py or environment variables

---

### Issue: "Application failed to respond"

**Possible Causes:**
1. Wrong start command
2. Missing dependencies
3. Database connection error

**Check Logs:**
- Render Dashboard → Your Service → Logs
- Look for error messages

**Common Fix:**
Ensure `gunicorn` is in `requirements.txt` ✅ (already there)

---

### Issue: Static files not loading

**Fix:**
Check that `build.sh` runs:
```bash
python manage.py collectstatic --no-input
```
✅ Already in build.sh

---

### Issue: Admin portal shows 404

**Fix:**
Check that migrations ran:
```bash
python manage.py migrate
```
✅ Already in build.sh

---

## 📋 Deployment Checklist

### Before Deployment:
- [x] ✅ Created `build.sh`
- [x] ✅ Created `render.yaml`
- [x] ✅ Updated `requirements.txt`
- [x] ✅ Added production database config
- [x] ✅ Pushed to GitHub

### During Deployment:
- [ ] ⏳ Delete static site
- [ ] ⏳ Create web service
- [ ] ⏳ Add environment variables
- [ ] ⏳ Wait for build to complete

### After Deployment:
- [ ] ⏳ Update ALLOWED_HOSTS
- [ ] ⏳ Create superuser
- [ ] ⏳ Test admin portal
- [ ] ⏳ Add content

---

## 🎉 Success Indicators

Your site works when you see:

1. ✅ Build completes successfully
2. ✅ "Deploy live" message
3. ✅ Site loads at Render URL
4. ✅ Admin portal accessible
5. ✅ Can login to admin
6. ✅ Static files (CSS/JS) load
7. ✅ Can add/edit content

---

## 📊 What Changed

### Files Added:
```
✅ build.sh              - Build commands for Render
✅ render.yaml           - Deployment configuration
✅ requirements.txt      - Added dj-database-url
```

### Files Updated:
```
✅ settings.py           - Added production database config
```

---

## 🔍 Quick Check

### Is it deployed correctly?

**Test 1: Homepage**
- Visit: `https://your-app.onrender.com`
- Should see: School homepage
- ❌ If "Not Found": Still using static site

**Test 2: Admin Portal**
- Visit: `https://your-app.onrender.com/admin/`
- Should see: Django admin login
- ❌ If 404: Not deployed as web service

**Test 3: Static Files**
- Homepage should have CSS styling
- Images should load
- ❌ If no styling: collectstatic didn't run

---

## 💰 Cost

**Render Free Plan:**
- ✅ FREE for web services
- ✅ 750 hours/month free
- ✅ Auto-sleep after 15 min inactivity
- ✅ Perfect for school website
- ⚠️ First load after sleep: 30-60 seconds

**No credit card needed for free plan!**

---

## ⏱️ Timeline

```
Now:          Delete static site (2 min)
+5 min:       Create web service (setup)
+15 min:      Build completes
+16 min:      Site is LIVE! ✅
+20 min:      Update ALLOWED_HOSTS
+25 min:      Fully functional!
```

---

## 🎯 Do This Now

### Immediate Actions:

1. **Open browser tabs:**
   - Tab 1: https://dashboard.render.com
   - Tab 2: Your GitHub repo
   - Tab 3: This guide

2. **Delete static site:**
   - 2 minutes
   
3. **Create web service:**
   - 5 minutes setup
   - 10 minutes build time
   
4. **Test site:**
   - Visit your Render URL
   - Check admin portal
   - Create superuser

**Total Time: ~20 minutes** ⏱️

---

## 📞 Need Help?

### Check Logs:
```
Render Dashboard → Your Service → Logs
```

### Common Success Messages:
```
✅ "Build successful"
✅ "Deploy live"
✅ "Booting worker with pid:"
```

### Common Error Messages:
```
❌ "Application failed to respond"
   → Check start command
   
❌ "DisallowedHost"
   → Update ALLOWED_HOSTS
   
❌ "ModuleNotFoundError: No module named 'gunicorn'"
   → Already fixed in requirements.txt
```

---

## ✅ What You Get

After successful deployment:

```
✅ Live website at .onrender.com
✅ Working admin portal
✅ Database persistence
✅ File uploads work
✅ Contact forms work
✅ SSL/HTTPS enabled (free)
✅ Automatic redeployments on push
✅ Environment variable management
✅ Logs and monitoring
```

---

**Ready? Let's deploy! 🚀**

**Step 1:** Go to https://dashboard.render.com  
**Step 2:** Delete static site  
**Step 3:** Create web service  
**Step 4:** Wait 15 minutes  
**Step 5:** Your site is LIVE!

---

**Document:** Quick Deployment Fix  
**Version:** 1.0  
**Date:** October 5, 2025  
**Time Needed:** 20 minutes  
**Cost:** FREE
