# 📸 Fix Media Files (Photos) on Render - Cloudinary Setup

## ❌ The Problem

Your photos aren't showing because Render's free plan has **ephemeral filesystem**:
- ✅ Code persists (from GitHub)
- ✅ Database persists (Supabase PostgreSQL)
- ❌ **Media files DON'T persist** (deleted on every redeploy)

Every time Render redeploys, the `media/` folder is wiped clean!

---

## ✅ The Solution: Use Cloudinary (Free Cloud Storage)

**Cloudinary Free Tier:**
- ✅ 25GB storage
- ✅ 25GB bandwidth/month
- ✅ FREE forever
- ✅ No credit card required
- ✅ Perfect for school website images

---

## 🚀 Setup Steps (10 minutes)

### Step 1: Create Cloudinary Account

1. **Go to:** https://cloudinary.com/users/register/free
2. **Sign up** with your email
3. **Verify** your email
4. **Login** to dashboard

### Step 2: Get Your Credentials

Once logged in to Cloudinary dashboard:

1. You'll see **"Product Environment Credentials"**
2. Copy these 3 values:
   - **Cloud Name:** (e.g., `dxxxxxxxxxxxx`)
   - **API Key:** (e.g., `123456789012345`)
   - **API Secret:** (e.g., `abcdefghijklmnopqrstuvwxyz`)

---

### Step 3: Add to Render Environment Variables

1. **Go to:** Render Dashboard → Your Web Service
2. **Click:** "Environment" tab
3. **Add 3 new environment variables:**

**Variable 1:**
```
Key: CLOUDINARY_CLOUD_NAME
Value: [Your Cloud Name from Cloudinary]
```

**Variable 2:**
```
Key: CLOUDINARY_API_KEY
Value: [Your API Key from Cloudinary]
```

**Variable 3:**
```
Key: CLOUDINARY_API_SECRET
Value: [Your API Secret from Cloudinary]
```

4. **Click "Save Changes"**

Render will automatically redeploy!

---

### Step 4: Add to Local .env File (Optional)

Update your local `.env` file to test Cloudinary locally:

```env
# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=your_cloud_name_here
CLOUDINARY_API_KEY=your_api_key_here
CLOUDINARY_API_SECRET=your_api_secret_here
```

---

## 📊 What's Been Changed:

### Files Updated:

1. **requirements.txt** ✅
   - Added: `cloudinary==1.41.0`
   - Added: `django-cloudinary-storage==0.3.0`

2. **settings.py** ✅
   - Added Cloudinary to INSTALLED_APPS
   - Added Cloudinary configuration
   - Set DEFAULT_FILE_STORAGE to use Cloudinary when configured

---

## 🎯 How It Works:

### Before (Without Cloudinary):
```
User uploads photo
    ↓
Saves to media/ folder on Render
    ↓
Render redeploys
    ↓
❌ Photo deleted! (ephemeral filesystem)
```

### After (With Cloudinary):
```
User uploads photo
    ↓
Automatically uploaded to Cloudinary cloud
    ↓
Render redeploys
    ↓
✅ Photo still there! (stored in cloud)
```

---

## 🔄 After Setup:

### 1. Redeploy Will Happen Automatically (~10 min)

Watch the logs for:
```bash
==> Running build command...
Installing collected packages: cloudinary, django-cloudinary-storage...
✅ Successfully installed cloudinary-1.41.0 django-cloudinary-storage-0.3.0
```

### 2. Re-upload Your Photos

**Important:** Existing photos in the `media/` folder are gone (they were deleted by Render).

You need to:
1. Login to admin: `https://st-mary-s-nyakhobi-1.onrender.com/admin/`
2. Re-upload all images:
   - Teacher photos
   - Gallery images
   - News images
   - Event images
   - School logo
   - Banner images

### 3. New Photos Will Persist

From now on, any photo uploaded through the admin portal will:
- ✅ Upload to Cloudinary automatically
- ✅ Persist forever (even after redeployments)
- ✅ Load fast from Cloudinary's CDN
- ✅ Work on mobile and desktop

---

## ✅ Success Indicators:

### Check Cloudinary Dashboard:
- Go to: https://cloudinary.com/console
- Click "Media Library"
- You should see uploaded images

### Check Your Site:
- Photos load without errors
- Image URLs start with `https://res.cloudinary.com/...`
- Gallery shows images
- Teacher profiles show photos
- News articles show images

---

## 📸 Image URLs:

### Before (Local Storage):
```
https://st-mary-s-nyakhobi-1.onrender.com/media/teachers/john.jpg
❌ Broken after redeploy
```

### After (Cloudinary):
```
https://res.cloudinary.com/YOUR_CLOUD_NAME/image/upload/teachers/john.jpg
✅ Always works!
```

---

## 🔧 Troubleshooting:

### Photos Still Don't Show:

1. **Check Environment Variables:**
   - Render Dashboard → Environment
   - Verify all 3 Cloudinary variables are set
   - No typos in keys or values

2. **Check Build Logs:**
   - Look for `Successfully installed cloudinary`
   - Check for any import errors

3. **Re-upload Images:**
   - Old images are gone (from before Cloudinary setup)
   - Upload new images through admin portal

### Cloudinary Not Working:

1. **Verify Credentials:**
   - Login to Cloudinary dashboard
   - Check that Cloud Name, API Key, API Secret match

2. **Check settings.py:**
   - INSTALLED_APPS should have `'cloudinary_storage'` and `'cloudinary'`
   - DEFAULT_FILE_STORAGE should be set

---

## 💡 Best Practices:

### Image Optimization:
- Upload reasonable image sizes (not 10MB photos!)
- Recommended: 1920x1080 max for banners
- Recommended: 800x800 max for teacher photos
- Cloudinary automatically optimizes images

### Organization:
- Cloudinary creates folders automatically
- Structure: `teachers/`, `gallery/`, `news/`, `events/`
- You can browse in Cloudinary dashboard

### Bandwidth:
- Free tier: 25GB/month bandwidth
- School website typically uses 1-5GB/month
- Monitor in Cloudinary dashboard

---

## 🎉 Benefits:

✅ **Photos persist forever** (no more disappearing images!)
✅ **Fast CDN delivery** (images load quickly worldwide)
✅ **Automatic optimization** (Cloudinary compresses images)
✅ **Transformation API** (resize, crop, effects available)
✅ **Free forever** (25GB is plenty for school website)
✅ **Easy management** (view all images in one dashboard)

---

## 📋 Deployment Checklist:

- [x] ✅ Updated requirements.txt with Cloudinary packages
- [x] ✅ Updated settings.py with Cloudinary configuration
- [ ] ⏳ Committed and pushed to GitHub
- [ ] ⏳ Created Cloudinary account
- [ ] ⏳ Added 3 environment variables to Render
- [ ] ⏳ Waited for redeploy (~10 min)
- [ ] ⏳ Re-uploaded all images through admin
- [ ] ⏳ Verified images show on website

---

## 🚀 Do This Now:

1. **Create Cloudinary account:** https://cloudinary.com/users/register/free
2. **Copy your 3 credentials** (Cloud Name, API Key, API Secret)
3. **Add to Render Environment variables**
4. **Save and wait for redeploy**
5. **Re-upload all images through admin portal**
6. **Celebrate!** 🎉

---

**Document:** Media Files Fix - Cloudinary Setup  
**Issue:** Photos not showing after Render deployment  
**Solution:** Use Cloudinary cloud storage  
**Time Required:** 10 minutes  
**Cost:** FREE
