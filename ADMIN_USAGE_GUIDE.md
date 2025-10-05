# Admin Portal Usage Guide

## Fixed Issues

### ✅ NoReverseMatch Error - FIXED
**Issue**: `/events/news/` was showing error: "Reverse for 'index' not found"

**Solution**: Changed `{% url 'home:index' %}` to `{% url 'home:home' %}` in templates
- Fixed in: `templates/events/news_list.html`
- Fixed in: `templates/portal/login.html`

**Status**: Committed and pushed to GitHub. Render will auto-deploy in ~5 minutes.

---

## How to Use the Admin Portal

### 1. Adding New Content (News, Faculty, Events, etc.)

When you want to add NEW content:

1. Go to the admin page (e.g., News and Announcements)
2. Click the **"Add News Announcement +"** button at the top right
3. Fill in all the fields (title, content, image, etc.)
4. Click **"Save"** or **"Save and continue editing"** or **"Save and add another"**

### 2. Editing Existing Content

When you want to EDIT existing content:

1. Go to the admin page
2. Click on the item you want to edit in the list
3. Make your changes
4. Click **"Save"** button

### 3. The "Action" Dropdown (NOT for saving!)

**IMPORTANT**: The action dropdown at the bottom is for **bulk operations**, NOT for saving individual items!

#### What the Error Message Means:

> "You have selected an action, and you haven't made any changes on individual fields. You're probably looking for the Go button rather than the Save button."

This means:
- You selected an action from the dropdown (like "Delete selected items")
- But you didn't check any checkboxes for items to apply the action to
- OR you're trying to use it to save, which is NOT what it's for

#### How to Use Actions Correctly:

1. **To delete multiple items**:
   - ☑️ Check the boxes next to items you want to delete
   - Select "Delete selected items" from the action dropdown
   - Click **"Go"** button (not Save!)
   - Confirm deletion

2. **To publish multiple items**:
   - ☑️ Check the boxes next to items
   - Select "Publish selected items" from dropdown
   - Click **"Go"** button

3. **To unpublish multiple items**:
   - ☑️ Check the boxes next to items
   - Select "Unpublish selected items" from dropdown
   - Click **"Go"** button

---

## Common Admin Tasks

### Adding News/Announcements

1. Navigate to **Admin Portal > News and Announcements**
2. Click **"Add News Announcement +"**
3. Fill in:
   - Title: Headline of the news
   - Content: Full article (rich text editor available)
   - Image: Upload a relevant photo
   - Is Featured: Check if you want it on homepage
   - Published Date: Date to display
4. Click **"Save"**

### Adding Faculty/Staff

1. Navigate to **Admin Portal > Teacher Profiles**
2. Click **"Add Teacher Profile +"**
3. Fill in:
   - Name: Full name
   - Title: Position (e.g., "Head of Mathematics")
   - Department: Select from dropdown
   - Bio: Brief description
   - Email: Contact email
   - Photo: Upload professional photo
4. Click **"Save"**

### Adding Events

1. Navigate to **Admin Portal > School Events**
2. Click **"Add School Event +"**
3. Fill in:
   - Title: Event name
   - Description: Event details
   - Date: When it happens
   - Time: Start time
   - Location: Where it takes place
   - Image: Event poster/photo
   - Is Featured: Check for homepage
4. Click **"Save"**

### Adding Gallery Images

1. Navigate to **Admin Portal > Gallery Images**
2. Click **"Add Gallery Image +"**
3. Fill in:
   - Title: Photo description
   - Image: Upload the photo
   - Category: Select category (Events, Facilities, etc.)
   - Description: Optional details
4. Click **"Save"**

### Managing Downloads (Documents, Forms)

1. Navigate to **Admin Portal > Downloadable Files**
2. Click **"Add Downloadable File +"**
3. Fill in:
   - Title: Document name
   - Description: What the document is about
   - File: Upload PDF/DOC/etc.
   - Category: Academic, Admission, etc.
4. Click **"Save"**

---

## Important Admin Settings

### School Settings (One-time setup)

Navigate to **Admin Portal > School Settings**:
- School name, motto, address, contacts
- Logo and branding
- Social media links
- Operating hours
- Email addresses

Only one School Settings record should exist. Edit it, don't create new ones!

---

## Tips & Tricks

### ✅ DO:
- Click **"Save"** after making changes to an individual item
- Use **"Save and continue editing"** if you want to stay on the page
- Use **"Save and add another"** when adding multiple similar items
- Check boxes + use Actions for **bulk operations**
- Click **"Go"** button when using the Actions dropdown

### ❌ DON'T:
- Click "Save" without making changes (use actions dropdown instead)
- Use Actions dropdown for saving individual items
- Click "Go" without selecting checkboxes first
- Create duplicate School Settings
- Forget to mark items as "Published" or "Is Featured"

---

## Troubleshooting

### "You have selected an action..." Error
**Problem**: Clicked Save while action dropdown was selected
**Solution**: 
- If editing an item: Just fill in the fields and click Save (ignore the dropdown)
- If doing bulk action: Check the boxes first, select action, then click "Go"

### Changes Not Showing on Website
**Problem**: Item not published
**Solution**: 
1. Edit the item
2. Check the "Is Published" checkbox
3. Click "Save"

### Images Not Uploading
**Problem**: File too large or wrong format
**Solution**:
- Keep images under 5MB
- Use JPG, PNG formats
- Resize large photos before uploading

### Can't Delete Item
**Problem**: Item is referenced elsewhere
**Solution**: Check if it's being used in related content first

---

## Quick Reference

| Task | Button to Click |
|------|----------------|
| Save new item | **Save** |
| Save edited item | **Save** |
| Keep editing after save | **Save and continue editing** |
| Add another after save | **Save and add another** |
| Delete multiple items | Check boxes → Select action → **Go** |
| Publish multiple items | Check boxes → Select action → **Go** |
| Cancel without saving | **Cancel** or browser back button |

---

## Need Help?

If you encounter any issues:
1. Check this guide first
2. Try refreshing the page
3. Clear browser cache
4. Log out and log back in
5. Contact technical support

---

**Last Updated**: October 5, 2025
**Admin URL**: https://st-mary-s-nyakhobi-1.onrender.com/admin/
