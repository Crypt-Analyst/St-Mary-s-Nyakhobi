# News Display Issue - Troubleshooting Guide

## Issue Reported
"2 news articles featured, but on site it doesn't show on the news of latest news place"

## Root Cause Analysis

The news wasn't displaying because the template was trying to access `news_item.summary` but the `NewsAnnouncement` model didn't have a `summary` field or method.

## ✅ What Was Fixed

### 1. Added `summary()` Method to NewsAnnouncement Model

**File**: `admin_portal/models.py`

Added a method that returns the first 150 characters of the news content:

```python
def summary(self):
    """Return first 150 characters of content as summary"""
    if len(self.content) > 150:
        return self.content[:150] + '...'
    return self.content
```

This allows the homepage template to display news summaries properly.

**Status**: ✅ Committed and pushed to GitHub (commit 3c99d11)

---

## How News Display Works

### Frontend (Homepage)

**Template**: `templates/home/index.html` (lines 650-676)

```html
{% for news_item in latest_news %}
<div class="news-item">
    <h6><a href="#" class="text-decoration-none">{{ news_item.title }}</a></h6>
    <p class="text-muted">{{ news_item.summary }}</p>
    <div class="news-meta">
        <small class="text-muted">
            <i class="fas fa-clock"></i> {{ news_item.created_at|date:"M d, Y" }}
        </small>
    </div>
</div>
{% empty %}
<div class="card">
    <div class="card-body text-center text-muted">
        <i class="fas fa-newspaper fa-3x mb-3"></i>
        <p>No news available at the moment.</p>
    </div>
</div>
{% endfor %}
```

### Backend (View)

**File**: `home/views.py` (lines 16-18)

```python
# Get latest news from admin portal
latest_news = NewsAnnouncement.objects.filter(published=True).order_by('-created_at')[:3]
```

**What it does**:
- Fetches news from the `NewsAnnouncement` model
- Only shows news where `published=True`
- Orders by newest first (`-created_at`)
- Shows maximum 3 latest news items

---

## Checklist: Why News Might Not Display

### ✅ Check 1: Is the News Published?

In the admin portal, each news item has a **"Published"** checkbox:

1. Go to **Admin Portal > News & Announcements**
2. Click on your news item
3. Make sure **"Published"** checkbox is **CHECKED** ✓
4. Click **"Save"**

**Common mistake**: Creating news without checking the "Published" box!

### ✅ Check 2: Does the News Have Content?

News items need:
- **Title**: Required
- **Content**: Required (the summary is generated from this)
- **Image**: Optional but recommended
- **Published**: Must be checked
- **Featured**: Optional (for highlighting special news)

### ✅ Check 3: Database Connection

The production site must be using the correct database (Supabase PostgreSQL, not SQLite).

**How to verify**:
1. Check Render environment variables
2. `DATABASE_URL` should be set to: 
   ```
   postgresql://postgres.gctpjhhxnfbqlydnpfwu:F2QLPdltqZJ4n8vI@aws-1-eu-north-1.pooler.supabase.com:5432/postgres
   ```

### ✅ Check 4: Code Deployed

After making changes in the admin:
1. No need to redeploy! Content changes are stored in the database
2. Just refresh the homepage

After code changes (like adding the `summary()` method):
1. Render will auto-deploy from GitHub (~5 minutes)
2. Watch deployment progress at: https://dashboard.render.com

---

## Testing the Fix

### On Production (Render):

1. **Wait for deployment** to complete (~5 minutes after push)

2. **Add news in admin**:
   - Go to: https://st-mary-s-nyakhobi-1.onrender.com/admin/
   - Navigate to **News & Announcements**
   - Click **"Add News Announcement +"**
   - Fill in:
     - Title: "Welcome Back Students"
     - Content: "We are excited to welcome all students back for the new term..."
     - Category: News
     - **✓ Published** (IMPORTANT!)
     - Featured: Optional
   - Click **"Save"**

3. **View homepage**:
   - Go to: https://st-mary-s-nyakhobi-1.onrender.com/
   - Scroll to **"Latest News"** section
   - Your news should appear with:
     - Title as heading
     - First 150 characters of content as summary
     - Date published

4. **If still not showing**:
   - Hard refresh: `Ctrl+F5` (Windows) or `Cmd+Shift+R` (Mac)
   - Clear browser cache
   - Check browser console for errors (F12)

---

## Understanding the News System

### Two News Models (Legacy vs New)

The system has TWO news models:

1. **Old Model**: `events.models.News` (Legacy, not used anymore)
2. **New Model**: `admin_portal.models.NewsAnnouncement` (Active, used everywhere)

The homepage uses the **NEW** model from admin_portal.

### Featured vs Published

- **Published**: Controls if news shows on the site at all
  - Unchecked = Hidden from everyone
  - Checked = Visible on homepage and news page

- **Featured**: Highlights important news
  - Makes news stand out visually
  - Can be used for special announcements
  - News can be published without being featured

### News Lifecycle

1. **Create** → Admin adds news in admin portal
2. **Save** → News is stored in database
3. **Publish** → Check "Published" box
4. **Display** → Homepage automatically shows latest 3 published news
5. **Update** → Edit anytime, changes appear immediately
6. **Archive** → Uncheck "Published" to hide (keeps in database)

---

## Quick Commands Reference

### Check News in Database (Local Development)

First install missing dependencies:
```bash
pip install cloudinary django-cloudinary-storage
```

Then check news:
```bash
python manage.py shell
```

```python
from admin_portal.models import NewsAnnouncement

# Count all news
print(f"Total news: {NewsAnnouncement.objects.count()}")

# Count published news
published = NewsAnnouncement.objects.filter(published=True)
print(f"Published news: {published.count()}")

# List all news
for news in NewsAnnouncement.objects.all():
    print(f"- {news.title} (published={news.published})")

# Exit shell
exit()
```

---

## Common Admin Tasks

### Adding News

1. Admin Portal > News & Announcements > **Add News Announcement +**
2. Fill in title and content
3. Upload image (optional)
4. **Check "Published"** ✓
5. Check "Featured" for important news (optional)
6. Click **"Save"**

### Editing News

1. Admin Portal > News & Announcements
2. Click on the news item
3. Make changes
4. Click **"Save"**

### Hiding News Temporarily

1. Edit the news item
2. **Uncheck "Published"**
3. Click **"Save"**

News is hidden but not deleted - you can republish it anytime.

### Deleting News

1. Admin Portal > News & Announcements
2. **Check the box** next to news items to delete
3. Select **"Delete selected items"** from dropdown
4. Click **"Go"**
5. Confirm deletion

---

## URLs Reference

- **Homepage**: https://st-mary-s-nyakhobi-1.onrender.com/
- **Admin Portal**: https://st-mary-s-nyakhobi-1.onrender.com/admin/
- **News List Page**: https://st-mary-s-nyakhobi-1.onrender.com/events/news/
- **Render Dashboard**: https://dashboard.render.com

---

## Expected Behavior After Fix

✅ **Homepage displays**:
- Latest 3 published news items
- Each showing: title, summary (150 chars), and date
- "View All" button links to full news page
- If no news: Shows "No news available" message

✅ **News page displays**:
- All published news
- Full content (not just summary)
- Images if uploaded
- Pagination if more than 10 items

✅ **Admin portal allows**:
- Adding new news
- Editing existing news
- Publishing/unpublishing
- Deleting news
- Featuring important news

---

## Troubleshooting Checklist

Before reporting issues, verify:

- [ ] News item has "Published" checkbox checked
- [ ] News has title and content filled in
- [ ] Render deployment completed successfully
- [ ] Browser cache cleared (Ctrl+F5)
- [ ] Viewing correct URL (https://st-mary-s-nyakhobi-1.onrender.com/)
- [ ] DATABASE_URL environment variable is set on Render
- [ ] No errors in browser console (F12 → Console tab)

---

## Database Schema

**NewsAnnouncement Model Fields**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | CharField(200) | Yes | News headline |
| category | Choice | Yes | news/announcement/event/achievement |
| content | TextField | Yes | Full news content |
| image | ImageField | No | News photo |
| published | BooleanField | Yes | Show on site? |
| featured | BooleanField | No | Highlight this news? |
| created_by | ForeignKey | No | Who created it |
| created_at | DateTime | Auto | When created |
| updated_at | DateTime | Auto | When last edited |

**Methods**:
- `__str__()` → Returns title
- `summary()` → Returns first 150 chars of content

---

## Next Steps

1. ✅ **Wait for Render deployment** (~5 minutes)
2. ✅ **Add test news** in admin portal with "Published" checked
3. ✅ **Verify news appears** on homepage
4. ✅ **Test editing** and republishing
5. ✅ **Add more news** as needed

---

**Last Updated**: October 5, 2025
**Status**: Fix deployed, awaiting Render auto-deployment
