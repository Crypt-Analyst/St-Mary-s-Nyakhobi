# Admin Portal - Website Content Management Guide

**St. Mary's Nyakhobi Senior School**  
**Last Updated:** October 5, 2025

---

## 🎯 Overview

Your admin portal is **fully integrated** with the website. Any content you add, edit, or delete in the admin portal **instantly appears** on the public website.

---

## ✅ What's Working Now

### 1. **News & Announcements** 
- **Admin Portal:** http://127.0.0.1:8000/admin/admin_portal/newsannouncement/
- **Public Display:** 
  - Homepage (latest 3): http://127.0.0.1:8000/
  - News Page (all): http://127.0.0.1:8000/events/news/

### 2. **School Events**
- **Admin Portal:** http://127.0.0.1:8000/admin/admin_portal/schoolevent/
- **Public Display:** http://127.0.0.1:8000/events/

### 3. **Gallery Images & Videos**
- **Admin Portal:** http://127.0.0.1:8000/admin/admin_portal/galleryimage/
- **Public Display:** Will appear on gallery page (needs template)

### 4. **Teacher Profiles**
- **Admin Portal:** http://127.0.0.1:8000/admin/admin_portal/teacherprofile/
- **Public Display:** Will appear on faculty page (needs template)

### 5. **Downloadable Files**
- **Admin Portal:** http://127.0.0.1:8000/admin/admin_portal/downloadablefile/
- **Public Display:** Will appear on downloads page (needs template)

### 6. **Contact Messages**
- **Admin Portal:** http://127.0.0.1:8000/admin/admin_portal/contactmessage/
- **Submission:** Contact form on website

### 7. **School Settings**
- **Admin Portal:** http://127.0.0.1:8000/admin/admin_portal/schoolsettings/
- **Usage:** Global school information (name, motto, contact, social media)

---

## 📝 How to Add/Edit Content

### Adding News Article

**Step 1:** Go to Admin Portal
```
http://127.0.0.1:8000/admin/
```

**Step 2:** Navigate to "News & Announcements"
- Click on "Admin Portal" section
- Click on "News & Announcements"
- Click "ADD NEWS & ANNOUNCEMENT" button (top right)

**Step 3:** Fill in the Form
- **Title:** Main headline (e.g., "School Reopening Date Announced")
- **Category:** Choose from:
  - News
  - Announcement
  - Event
  - Achievement
- **Content:** Full article text (supports formatting)
- **Image:** Upload photo (optional, JPG/PNG)
- **Published:** ✅ Check this box to make it visible on website
- **Featured:** ✅ Check to highlight on homepage

**Step 4:** Click "SAVE"

**Step 5:** View on Website
- Go to: http://127.0.0.1:8000/events/news/
- Your article appears instantly!

---

### Editing Existing Content

**Step 1:** Go to Admin Portal
```
http://127.0.0.1:8000/admin/admin_portal/newsannouncement/
```

**Step 2:** Find the Article
- Use search box at top
- Use filters on right side
- Click on the article title

**Step 3:** Make Changes
- Edit any field
- Upload new image
- Change published status

**Step 4:** Click "SAVE"

**Step 5:** Refresh Website
- Changes appear immediately
- No need to rebuild or redeploy

---

### Hiding Content (Without Deleting)

**Option 1:** Unpublish
- Open the article in admin
- Uncheck "Published" checkbox
- Click "SAVE"
- Article is hidden from public but still in database

**Option 2:** Bulk Unpublish
- Go to list view: `/admin/admin_portal/newsannouncement/`
- Check boxes next to articles
- Uncheck "Published" column
- Articles disappear from website

---

### Deleting Content

**Warning:** This permanently removes content!

**Step 1:** Go to list view
**Step 2:** Check box next to item(s) to delete
**Step 3:** Select "Delete selected" from dropdown
**Step 4:** Click "Go"
**Step 5:** Confirm deletion

---

## 🎨 Content Display Rules

### What Appears on Public Website

#### Homepage (`/`)
- Shows **3 latest** news articles
- Only shows items where `Published = ✅`
- Ordered by newest first

#### News Page (`/events/news/`)
- Shows **all** published news
- Filtered by `Published = ✅`
- Ordered by newest first
- Shows title, category, image, excerpt
- "Read More" links to full article

#### Individual News Article
- URL: `/events/news/<id>/`
- Shows full content
- Shows uploaded image
- Shows published date
- Shows author (if available)

---

## 🔄 Real-Time Testing Workflow

### Test 1: Add News Article

1. **Admin Portal:**
   - Add new article: "School Sports Day Announced"
   - Category: Event
   - Content: "Join us on October 15th..."
   - Published: ✅
   - SAVE

2. **Website:**
   - Go to: http://127.0.0.1:8000/events/news/
   - **Result:** Article appears in list
   - Click "Read More"
   - **Result:** Full article displays

3. **Homepage:**
   - Go to: http://127.0.0.1:8000/
   - Scroll to "Latest News" section
   - **Result:** Article appears if in top 3

---

### Test 2: Edit Content

1. **Admin Portal:**
   - Open existing article
   - Change title to "UPDATED: Sports Day Postponed"
   - Change content
   - SAVE

2. **Website:**
   - Refresh news page
   - **Result:** Updated title and content appear immediately

---

### Test 3: Hide Content

1. **Admin Portal:**
   - Open article
   - Uncheck "Published"
   - SAVE

2. **Website:**
   - Refresh news page
   - **Result:** Article no longer visible
   - Still exists in admin (can republish later)

---

### Test 4: Upload Image

1. **Admin Portal:**
   - Edit article
   - Click "Choose File" under Image
   - Select photo from computer
   - SAVE

2. **Website:**
   - Refresh news page
   - **Result:** Image appears with article

---

## 🎯 Admin Portal Features

### List View Features

**Search:** 
- Search by title or content
- Located at top of page

**Filters:**
- Category (News, Announcement, Event, Achievement)
- Published status
- Featured status
- Created date

**Quick Edit:**
- Change "Published" status directly in list
- Change "Featured" status directly in list
- No need to open full form

**Bulk Actions:**
- Select multiple items
- Delete all at once
- Change status for all

**Date Hierarchy:**
- Navigate by year/month/day
- Located at top of list

---

### Form Features

**Rich Text Editor:**
- Format text (bold, italic, lists)
- Add links
- Structure content

**Image Upload:**
- Drag & drop support
- Preview uploaded images
- Replace existing images

**Auto-Save:**
- Draft saved automatically
- "Created by" tracked automatically
- Timestamps recorded

**Preview:**
- See who created it
- See when it was created/updated
- Check publish status

---

## 📊 Admin Dashboard

Access: http://127.0.0.1:8000/admin/

### Statistics Shown:
- Total news articles
- Published vs unpublished
- Gallery images count
- Active teachers count
- Upcoming events
- Total downloads
- Unread contact messages

### Quick Links:
- Recent news (last 5)
- Recent messages (last 10)
- Upcoming events (next 5)

---

## 🔐 Security & Permissions

### Who Can Access Admin Portal?

**Superuser:**
- Full access to everything
- Can add/edit/delete all content
- Can manage users
- Can change site settings

**Staff User:**
- Can add/edit content
- Cannot delete important items
- Cannot manage users
- Limited settings access

### Creating Admin Users

```bash
# Create superuser
python manage.py createsuperuser

# Follow prompts:
# Username: admin
# Email: admin@stmarysnyakhobi.ac.ke
# Password: [strong password]
```

---

## 🎨 Content Best Practices

### News Articles

**Title:**
- Keep under 100 characters
- Be specific and clear
- Use action words

**Content:**
- Start with most important info
- Use paragraphs (5-7 lines max)
- Include dates, times, locations
- End with call-to-action

**Images:**
- Landscape orientation works best
- Minimum 800x600 pixels
- Maximum 5MB file size
- Use JPG for photos, PNG for graphics

**Categories:**
- **News:** General school updates
- **Announcement:** Important notices
- **Event:** Upcoming activities
- **Achievement:** Awards, competitions, success stories

---

### School Events

**Details to Include:**
- Clear event name
- Full date and time
- Exact location
- Event description
- Contact person (if applicable)

**Event Types:**
- Academic (exams, parent meetings)
- Sports (games, tournaments)
- Cultural (drama, music)
- Holiday (breaks, celebrations)
- Other

---

## 🐛 Troubleshooting

### "Content not appearing on website"

**Check 1:** Is "Published" checked?
- Go to admin
- Open the item
- Verify "Published" is ✅

**Check 2:** Clear browser cache
- Press Ctrl+F5 (hard refresh)
- Or use incognito/private window

**Check 3:** Check filters
- Make sure date is not in future
- Verify category is correct

---

### "Image not showing"

**Check 1:** Image uploaded?
- Go to admin
- Verify image field shows filename

**Check 2:** Image size
- Keep under 5MB
- Use JPG or PNG format

**Check 3:** Media settings
- Check `settings.py` has correct MEDIA_ROOT
- Verify media folder exists

---

### "Can't login to admin"

**Solution 1:** Reset password
```bash
python manage.py changepassword admin
```

**Solution 2:** Create new superuser
```bash
python manage.py createsuperuser
```

---

## 📱 Mobile Management

### Admin Portal on Mobile

The admin portal works on mobile devices:
- Responsive design
- Touch-friendly buttons
- Mobile image upload
- Easy navigation

**Recommended:** Use tablet or desktop for better experience

---

## 🎓 Training Checklist

### Basic Admin Training

- [ ] Login to admin portal
- [ ] Navigate to News & Announcements
- [ ] Add new news article
- [ ] Upload image
- [ ] View article on website
- [ ] Edit existing article
- [ ] Hide article (unpublish)
- [ ] Delete article
- [ ] Use search and filters
- [ ] Bulk edit multiple items

### Advanced Features

- [ ] Add school event
- [ ] Upload gallery images
- [ ] Manage teacher profiles
- [ ] Upload downloadable files
- [ ] View contact messages
- [ ] Update school settings
- [ ] Create new admin users
- [ ] Export data

---

## 🚀 Quick Reference

### Common Admin URLs

```
Main Admin: 
http://127.0.0.1:8000/admin/

News Management:
http://127.0.0.1:8000/admin/admin_portal/newsannouncement/

Events Management:
http://127.0.0.1:8000/admin/admin_portal/schoolevent/

Gallery Management:
http://127.0.0.1:8000/admin/admin_portal/galleryimage/

Teachers Management:
http://127.0.0.1:8000/admin/admin_portal/teacherprofile/

Contact Messages:
http://127.0.0.1:8000/admin/admin_portal/contactmessage/

School Settings:
http://127.0.0.1:8000/admin/admin_portal/schoolsettings/
```

### Common Website URLs

```
Homepage:
http://127.0.0.1:8000/

News Page:
http://127.0.0.1:8000/events/news/

Events Calendar:
http://127.0.0.1:8000/events/

Contact Form:
http://127.0.0.1:8000/contact/
```

---

## 📞 Support

### Need Help?

1. **Check this guide** - Most questions answered here
2. **Check ADMIN_PORTAL_GUIDE.md** - Technical details
3. **Check ADMIN_PORTAL_INTEGRATION.md** - Advanced integration
4. **Contact IT support** - For technical issues

---

## ✅ Daily Admin Workflow

### Morning Routine

1. **Login to admin portal**
2. **Check contact messages** (unread count on dashboard)
3. **Review scheduled content** (upcoming events)
4. **Moderate comments** (if enabled)

### Adding Content

1. **Plan content** (what to post today?)
2. **Prepare media** (photos, documents)
3. **Write in admin** (clear, concise)
4. **Preview** (check spelling, formatting)
5. **Publish** (make live)
6. **Verify** (view on website)

### Weekly Tasks

- Review old content (unpublish outdated)
- Update upcoming events
- Check for broken images
- Archive past events
- Backup important content

---

## 🎉 Success Checklist

You're ready when you can:

- [x] Admin portal fully integrated with website
- [x] News articles appear on website immediately
- [x] Events display on events page
- [x] Content editing reflects instantly
- [x] Unpublishing hides content
- [x] Images upload and display correctly
- [x] Contact messages are received
- [ ] Gallery page displays uploaded images (template needed)
- [ ] Faculty page shows teacher profiles (template needed)
- [ ] Downloads page shows uploaded files (template needed)

---

**Document Version:** 1.0  
**Last Updated:** October 5, 2025  
**Author:** GitHub Copilot  
**For:** St. Mary's Nyakhobi Senior School Website Admin Team
