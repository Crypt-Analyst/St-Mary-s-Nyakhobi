# 🔧 Render Build Commands - Copy & Paste

## ⚠️ If build.sh doesn't work, use these commands directly in Render dashboard

---

## Build Command (Copy this):

```bash
pip install --upgrade pip && pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate
```

---

## Start Command (Copy this):

```bash
gunicorn st_marys_school.wsgi:application
```

---

## Environment Variables:

### 1. PYTHON_VERSION
```
3.13.4
```

### 2. SECRET_KEY
Click "Generate" button in Render dashboard

### 3. DEBUG
```
False
```

### 4. ALLOWED_HOSTS
```
.onrender.com
```

---

## Full Setup Instructions:

### Step 1: Delete Static Site
1. Go to Render Dashboard
2. Click on your static site
3. Settings → Delete Service

### Step 2: Create New Web Service
1. Click "New +" → "Web Service"
2. Connect GitHub repo: `Crypt-Analyst/St-Mary-s-Nyakhobi`
3. Branch: `master`

### Step 3: Configure Service

**Name:**
```
st-marys-nyakhobi
```

**Runtime:**
```
Python 3
```

**Build Command:** (Copy and paste this entire line)
```bash
pip install --upgrade pip && pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate
```

**Start Command:**
```bash
gunicorn st_marys_school.wsgi:application
```

**Root Directory:**
```
(Leave blank)
```

### Step 4: Add Environment Variables

Click "Advanced" → "Add Environment Variable"

**Add these 4 variables:**

1. **PYTHON_VERSION**
   - Key: `PYTHON_VERSION`
   - Value: `3.13.4`

2. **SECRET_KEY**
   - Key: `SECRET_KEY`
   - Click "Generate" button (let Render generate it)

3. **DEBUG**
   - Key: `DEBUG`
   - Value: `False`

4. **ALLOWED_HOSTS**
   - Key: `ALLOWED_HOSTS`
   - Value: `.onrender.com`

### Step 5: Select Plan
- Select: **Free**

### Step 6: Create Service
- Click "Create Web Service"
- Wait 10-15 minutes for build

---

## ✅ What This Does:

### Build Command Breakdown:
```bash
pip install --upgrade pip          # Update pip
&&                                  # Then (if successful)
pip install -r requirements.txt    # Install all packages
&&                                  # Then
python manage.py collectstatic     # Collect CSS/JS files
&&                                  # Then
python manage.py migrate           # Create database tables
```

### Start Command:
```bash
gunicorn st_marys_school.wsgi:application
```
This starts the web server to handle requests.

---

## 🐛 Troubleshooting

### If Build Fails:

**Check Build Logs for:**

1. **Python version error:**
   - Make sure `PYTHON_VERSION=3.13.4` is set

2. **Package installation error:**
   - Check that all packages in `requirements.txt` are valid

3. **Static files error:**
   - Usually safe to ignore warnings

4. **Migration error:**
   - Check database connection
   - Ensure DATABASE_URL is set (Render does this automatically)

### Common Errors:

**"No module named 'gunicorn'"**
- ✅ Fixed: Already in requirements.txt

**"DisallowedHost at /"**
- Fix: Update ALLOWED_HOSTS environment variable with your actual Render URL

**"Application failed to respond"**
- Check Start Command is correct
- Check logs for Python errors

---

## 📝 After Deployment

### 1. Update ALLOWED_HOSTS

Once you get your URL (e.g., `st-marys-nyakhobi.onrender.com`):

**Option A: Environment Variable (Recommended)**
1. Go to Render Dashboard → Your Service
2. Environment → Add Variable
3. Key: `ALLOWED_HOSTS`
4. Value: `st-marys-nyakhobi.onrender.com,.onrender.com`
5. Save Changes

**Option B: Update settings.py**
```python
ALLOWED_HOSTS = ['st-marys-nyakhobi.onrender.com', '.onrender.com', '127.0.0.1', 'localhost']
```

### 2. Create Superuser

1. In Render Dashboard → Your Service
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

### 3. Test Your Site

**Homepage:**
```
https://st-marys-nyakhobi.onrender.com
```

**Admin Portal:**
```
https://st-marys-nyakhobi.onrender.com/admin/
```

---

## 🎯 Success Checklist

- [ ] Static site deleted
- [ ] New web service created
- [ ] Build command added (one long line)
- [ ] Start command added
- [ ] Environment variables set (4 total)
- [ ] Build completed successfully
- [ ] Site loads at Render URL
- [ ] Admin portal accessible
- [ ] Superuser created
- [ ] Can login to admin

---

## 💡 Why Use One Long Command?

Instead of using `build.sh` file, we combine all commands into one line using `&&`.

**Advantages:**
- ✅ No file permission issues
- ✅ Works on all systems
- ✅ Clear what's happening
- ✅ Easy to modify
- ✅ No script execution issues

**The `&&` operator means:**
- "Run this command AND if it succeeds, run the next one"
- If any command fails, the whole build fails
- This ensures each step completes before moving to next

---

## 📞 Still Having Issues?

### Check These:

1. **Branch is correct:** `master`
2. **Root directory is blank:** Don't put anything there
3. **Build command is ONE line:** No line breaks
4. **All environment variables set:** Should have 4 variables
5. **Python version:** Must be `3.13.4`

### View Logs:
```
Render Dashboard → Your Service → Logs
```

Look for:
- ✅ "Build successful"
- ✅ "Deploy live"
- ✅ "Booting worker with pid"

---

## 🎉 Expected Output

### Successful Build Log:
```
==> Installing Python version 3.13.4...
==> Running build command...
Collecting Django==4.2.7
...
Installing collected packages: ...
Successfully installed Django-4.2.7 ...
Collecting static files...
174 static files copied
Running migrations...
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, ...
Running migrations:
  Applying admin_portal.0001_initial... OK
  Applying admin_portal.0002_academicdepartment... OK
  ...
==> Build successful
==> Deploy live
[2025-10-05 12:00:00] [1] [INFO] Starting gunicorn 21.2.0
[2025-10-05 12:00:00] [1] [INFO] Listening at: http://0.0.0.0:10000
[2025-10-05 12:00:00] [1] [INFO] Using worker: sync
[2025-10-05 12:00:01] [8] [INFO] Booting worker with pid: 8
```

---

**Document:** Render Build Commands  
**Version:** 1.0  
**Date:** October 5, 2025  
**Updated:** With single-line build command solution
