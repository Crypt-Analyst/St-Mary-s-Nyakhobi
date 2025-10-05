# 🗄️ Database Connection Details - Supabase PostgreSQL

## 📍 Your Supabase Database Credentials

### Connection String (DATABASE_URL):
```
postgresql://postgres.gctpjhhxnfbqlydnpfwu:F2QLPdltqZJ4n8vI@aws-1-eu-north-1.pooler.supabase.com:5432/postgres
```

### Individual Credentials:
```
Engine:   django.db.backends.postgresql
Database: postgres
User:     postgres.gctpjhhxnfbqlydnpfwu
Password: F2QLPdltqZJ4n8vI
Host:     aws-1-eu-north-1.pooler.supabase.com
Port:     5432
SSL Mode: require
```

---

## 📂 Where Your Database Credentials Are Saved:

### 1. **Local `.env` File** ✅
- **Location:** `C:\Users\Afronic\Desktop\St Mary's WEB\.env`
- **Status:** Updated with Supabase credentials
- **Use:** Local development on your computer
- **Security:** ❌ NOT pushed to GitHub (in `.gitignore`)

### 2. **settings.py (Commented Out)** 
- **Location:** `st_marys_school/settings.py` lines 104-120
- **Status:** Commented out (currently using SQLite)
- **Note:** Credentials are hardcoded but commented

### 3. **Render Environment Variables** ⏳
- **Location:** Render Dashboard → Your Web Service → Environment tab
- **Status:** ❌ NOT YET ADDED - You need to add `DATABASE_URL`
- **Use:** Production deployment on Render

---

## 🚀 For Render Deployment - Add DATABASE_URL:

### Step 1: Go to Render Dashboard
1. Visit: https://dashboard.render.com
2. Click on your web service: `St-Mary-s-Nyakhobi`

### Step 2: Add DATABASE_URL Environment Variable
1. Click **"Environment"** tab (left sidebar)
2. Click **"Add Environment Variable"**
3. **Key:** `DATABASE_URL`
4. **Value:** 
   ```
   postgresql://postgres.gctpjhhxnfbqlydnpfwu:F2QLPdltqZJ4n8vI@aws-1-eu-north-1.pooler.supabase.com:5432/postgres
   ```
5. Click **"Save Changes"**

### Step 3: Wait for Auto-Redeploy
- Render will automatically redeploy (~5-10 minutes)
- Migrations will run automatically
- Database tables will be created in Supabase
- Your site will use Supabase PostgreSQL! ✅

---

## 🔧 How Your Settings Work:

### Current settings.py Logic (Lines 252-260):
```python
# Production database configuration (Render with DATABASE_URL)
if 'DATABASE_URL' in os.environ:
    import dj_database_url
    DATABASES['default'] = dj_database_url.config(
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require=True,
    )
```

This means:
- ✅ **If `DATABASE_URL` exists** → Use that database (Supabase on Render)
- ❌ **If `DATABASE_URL` doesn't exist** → Use SQLite (local dev)

---

## 🎯 What Happens After Adding DATABASE_URL to Render:

### During Build (Automatic):
```bash
==> Running build command...
Installing dependencies...
✅ Successfully installed Django, psycopg2-binary, etc.

Collecting static files...
✅ 174 static files copied to staticfiles/

Running migrations...
✅ Applying contenttypes.0001_initial... OK
✅ Applying auth.0001_initial... OK
✅ Applying admin.0001_initial... OK
✅ Applying admin_portal.0001_initial... OK
✅ Applying admin_portal.0002_academicdepartment_homepagebanner... OK
✅ Applying home.0001_initial... OK
✅ Applying events.0001_initial... OK
✅ Applying news.0001_initial... OK
✅ [All migrations applied to Supabase database]

Creating initial superuser...
✅ Successfully created superuser: admin
   Password: StMarys2025!Change

==> Build successful 🎉
==> Deploy live
```

### After Deployment:
- ✅ Site loads at: `https://st-mary-s-nyakhobi-1.onrender.com`
- ✅ All data stored in Supabase PostgreSQL (persistent!)
- ✅ Database survives redeployments
- ✅ Admin portal works
- ✅ Can login with: `admin` / `StMarys2025!Change`

---

## 🔐 Security Notes:

### ✅ Good Security Practices:
1. `.env` file is in `.gitignore` (not pushed to GitHub)
2. DATABASE_URL set as environment variable on Render
3. SSL mode required for database connection
4. Credentials not exposed in public code

### ⚠️ Current Issues:
1. **Hardcoded credentials in settings.py (commented)** 
   - Should be removed after confirming Supabase works
   - Line 104-120 in settings.py

### 🔧 Recommendation:
After confirming Supabase works on Render, clean up settings.py:

**Remove these lines** (104-120):
```python
# Uncomment below to use Supabase PostgreSQL when connection issues are resolved
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'postgres',
#         'USER': 'postgres.gctpjhhxnfbqlydnpfwu',
#         'PASSWORD': 'F2QLPdltqZJ4n8vI',
#         'HOST': 'aws-1-eu-north-1.pooler.supabase.com',
#         'PORT': '5432',
#         'OPTIONS': {
#             'sslmode': 'require',
#         },
#     }
# }
```

---

## 📊 Database Configuration Summary:

### Local Development:
- **Database:** Supabase PostgreSQL (via `.env` file)
- **Connection:** Uses `DATABASE_URL` from `.env`
- **Data:** Persistent in cloud
- **Use:** For local testing with production database

### Production (Render):
- **Database:** Supabase PostgreSQL (via environment variable)
- **Connection:** Uses `DATABASE_URL` from Render Environment
- **Data:** Persistent in cloud
- **Use:** Live website

### Both environments use the SAME Supabase database! 🎯

---

## ✅ Next Steps - DO THIS NOW:

### 1. Add DATABASE_URL to Render (5 minutes)
- Dashboard → Your Service → Environment tab
- Add: `DATABASE_URL` = `postgresql://postgres.gctpjhhxnfbqlydnpfwu:F2QLPdltqZJ4n8vI@aws-1-eu-north-1.pooler.supabase.com:5432/postgres`
- Save

### 2. Wait for Deployment (5-10 minutes)
- Watch logs for migration success
- Look for "Deploy live" message

### 3. Test Your Site
- Visit: `https://st-mary-s-nyakhobi-1.onrender.com`
- Should load without "no such table" errors
- Try admin: `/admin/`
- Login: `admin` / `StMarys2025!Change`

### 4. Verify Database
- Login to admin portal
- Check that all 17 models appear
- Try adding some content
- Verify data persists after reload

### 5. Update Superuser Password (IMPORTANT!)
- Login to admin
- Change password from `StMarys2025!Change` to something secure
- Remember your new password!

---

## 🎉 Benefits of Using Supabase:

✅ **Free PostgreSQL database** (500 MB storage)
✅ **Data persists** across deploys
✅ **Same database** for local dev and production
✅ **Automatic backups** by Supabase
✅ **SSL encrypted** connections
✅ **No credit card** required
✅ **Cloud hosted** - reliable uptime

---

## 📞 Troubleshooting:

### If site still shows "no such table" error:
1. Check Render logs for migration errors
2. Verify DATABASE_URL is set correctly
3. Look for "Applying migrations..." messages in logs
4. Confirm psycopg2-binary is in requirements.txt ✅

### If can't connect to Supabase:
1. Check if Supabase project is active
2. Verify credentials haven't changed
3. Ensure SSL mode is set to 'require'
4. Check Supabase dashboard for connection issues

---

**Document:** Database Connection Details  
**Database:** Supabase PostgreSQL  
**Region:** EU North (Sweden)  
**Type:** Pooler connection  
**SSL:** Required  
**Status:** Ready to use  
**Created:** October 5, 2025
