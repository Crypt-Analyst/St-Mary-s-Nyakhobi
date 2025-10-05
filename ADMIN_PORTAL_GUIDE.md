# 🎯 Admin Portal Setup Guide
## St. Mary's Nyakhobi Senior School

---

## ✅ What Has Been Fixed & Added

### 1. **Deployment Issue FIXED** ✔
- **Problem**: Pillow 10.0.1 incompatible with Python 3.13
- **Solution**: Updated to Pillow 10.3.0
- **Also Updated**: psycopg2-binary to 2.9.9
- **Status**: Ready for deployment on Render/PythonAnywhere

### 2. **Admin Portal Created** ✔
Complete Content Management System with all requested features!

---

## 📦 Admin Portal Features

### ✅ Core Features Implemented

#### 1. **Secure Login System**
- Uses Django's built-in authentication
- Username + password protected
- Staff-only access
- Session management

#### 2. **Dashboard Overview**
Located at: `/admin/`
- Quick statistics
- Recent activity
- Unread messages counter
- Upcoming events
- Content summaries

#### 3. **School Settings Management**
Manage:
- ✅ School name and motto
- ✅ School logo upload
- ✅ Contact information (email, phone, address)
- ✅ Social media links (Facebook, Twitter, Instagram, YouTube)
- ✅ About Us content
- ✅ Vision statement
- ✅ Mission statement

#### 4. **News & Announcements Manager**
Features:
- ✅ Add/edit/delete news articles
- ✅ Categories (News, Announcement, Event, Achievement)
- ✅ Image uploads
- ✅ Publish/unpublish control
- ✅ Featured article marking
- ✅ Search and filtering
- ✅ Date-based organization

#### 5. **Gallery Management**
Features:
- ✅ Upload/delete photos
- ✅ Add video URLs (YouTube, etc.)
- ✅ Image previews in admin
- ✅ Category organization
- ✅ Featured items
- ✅ Descriptions and titles
- ✅ Search functionality

#### 6. **Teachers/Staff Management**
Features:
- ✅ Add teacher profiles
- ✅ Photo uploads
- ✅ Position and department assignment
- ✅ Subject assignments
- ✅ Qualifications and bio
- ✅ Contact information
- ✅ Active/inactive status
- ✅ Display order control

#### 7. **Events Calendar**
Features:
- ✅ Add school events
- ✅ Event types (Academic, Sports, Cultural, etc.)
- ✅ Start and end dates
- ✅ Time management
- ✅ Location tracking
- ✅ All-day event support
- ✅ Publish control
- ✅ Calendar view

#### 8. **Downloads Section**
Features:
- ✅ Upload timetables
- ✅ Upload newsletters
- ✅ Upload circulars
- ✅ Upload forms and policies
- ✅ File size display
- ✅ Download counter
- ✅ Category organization
- ✅ Publish control

#### 9. **Contact Message Management**
Features:
- ✅ View all contact form submissions
- ✅ Read/unread status tracking
- ✅ Reply status marking
- ✅ Reply notes field
- ✅ Email and phone display
- ✅ Search messages
- ✅ Filter by status and date
- ✅ Cannot be manually created (form-only)

---

## 🚀 Setup Instructions

### Step 1: Install Dependencies
```bash
cd "c:\Users\Afronic\Desktop\St Mary's WEB"
pip install -r requirements.txt
```

### Step 2: Create Database Tables
```bash
python manage.py makemigrations admin_portal
python manage.py migrate
```

### Step 3: Create Admin User
```bash
python manage.py createsuperuser
```
You'll be prompted for:
- Username (e.g., `admin`)
- Email (e.g., `nyakhobisecsch@gmail.com`)
- Password (use strong password!)

### Step 4: Run Server
```bash
python manage.py runserver
```

### Step 5: Access Admin Portal
1. Open browser: `http://127.0.0.1:8000/admin/`
2. Login with superuser credentials
3. Start managing content!

---

## 📋 Admin Portal Structure

### Main Sections in Admin

```
St. Mary's Nyakhobi Admin Portal
├── AUTHENTICATION AND AUTHORIZATION
│   ├── Users (manage admin accounts)
│   └── Groups (permissions)
│
├── ADMIN PORTAL
│   ├── School Settings (global settings)
│   ├── News & Announcements (add/edit news)
│   ├── Gallery Items (photos & videos)
│   ├── Teacher Profiles (staff management)
│   ├── School Events (calendar)
│   ├── Downloadable Files (documents)
│   └── Contact Messages (form submissions)
│
└── OTHER APPS
    └── (your other Django apps)
```

---

## 🎨 Admin Features

### Rich Interface
- **List Views**: Sortable columns, filters, search
- **Image Previews**: See photos before clicking
- **Bulk Actions**: Edit multiple items at once
- **Date Hierarchy**: Navigate by date
- **Inline Editing**: Edit directly in list view
- **Status Indicators**: Visual read/unread markers

### Smart Features
- **Auto File Size**: Calculates file sizes automatically
- **Download Tracking**: Counts file downloads
- **Read Status**: Tracks who read messages when
- **Single Settings**: Only one school settings instance
- **Order Control**: Arrange teachers by display order
- **Media Management**: Integrated image/file uploads

---

## 📊 Usage Examples

### Adding News Article
1. Go to **Admin Portal → News & Announcements**
2. Click **Add News & Announcement**
3. Fill in:
   - Title
   - Category (News/Announcement/Event/Achievement)
   - Content
   - Upload image (optional)
   - Check "Published" to make live
   - Check "Featured" for homepage
4. Click **Save**

### Uploading Gallery Photo
1. Go to **Admin Portal → Gallery Items**
2. Click **Add Gallery Item**
3. Fill in:
   - Title and description
   - Media type (Photo)
   - Upload image
   - Set category
   - Check "Featured" for homepage
4. Click **Save**

### Adding Teacher Profile
1. Go to **Admin Portal → Teacher Profiles**
2. Click **Add Teacher Profile**
3. Fill in:
   - Name and position
   - Department
   - Upload photo
   - Email and phone
   - Subjects (comma-separated)
   - Qualifications and bio
   - Set display order
4. Click **Save**

### Managing Contact Messages
1. Go to **Admin Portal → Contact Messages**
2. See all submissions with status
3. Click on message to view details
4. Check "Read" to mark as read
5. Check "Replied" when responded
6. Add reply notes for tracking

---

## 🔐 Security Features

### Built-in Security
- ✅ Login required for all admin pages
- ✅ Staff-only access
- ✅ CSRF protection
- ✅ Session management
- ✅ Password hashing
- ✅ Audit trail (created_by, updated_at)

### Permissions
- Only staff users can access admin
- Only superusers can add other admins
- File uploads validated
- Input sanitization enabled

---

## 🎯 Next Steps

### Immediate (Before Using)
1. ✅ Run migrations (`python manage.py migrate`)
2. ✅ Create superuser account
3. ✅ Login to admin portal
4. ✅ Configure School Settings first
5. ✅ Add initial content

### Optional Enhancements
- Create additional admin users (staff accounts)
- Set up user groups with specific permissions
- Configure email notifications
- Add custom dashboard widgets
- Integrate with frontend templates

### Frontend Integration
To display admin content on your website:
1. Query models in views (e.g., `NewsAnnouncement.objects.filter(published=True)`)
2. Pass to templates
3. Display with Bootstrap styling

Example view:
```python
from admin_portal.models import NewsAnnouncement

def home(request):
    news = NewsAnnouncement.objects.filter(published=True)[:5]
    return render(request, 'home.html', {'news': news})
```

Example template:
```html
{% for item in news %}
    <h3>{{ item.title }}</h3>
    <p>{{ item.content }}</p>
    {% if item.image %}
        <img src="{{ item.image.url }}" alt="{{ item.title }}">
    {% endif %}
{% endfor %}
```

---

## 📱 Mobile-Friendly Admin

The Django admin is responsive and works on:
- ✅ Desktop computers
- ✅ Tablets
- ✅ Mobile phones

---

## 🆘 Troubleshooting

### Can't Access Admin?
- Make sure you created a superuser
- Ensure user has `is_staff=True`
- Check you're using correct URL: `/admin/`

### Migrations Error?
```bash
python manage.py makemigrations
python manage.py migrate
```

### Permission Denied?
- Login with superuser account
- Or grant staff status: `user.is_staff = True; user.save()`

### File Upload Issues?
- Check `MEDIA_ROOT` and `MEDIA_URL` in settings
- Ensure `media/` directory exists
- Verify file permissions

---

## 📞 Admin Portal Access

### Default Credentials (After Creating)
- **URL**: `http://yoursite.com/admin/` (or `http://127.0.0.1:8000/admin/` locally)
- **Username**: (what you created)
- **Password**: (what you created)

### For Production
1. Always use strong passwords
2. Enable 2FA if available
3. Limit admin user accounts
4. Change admin URL for security
5. Use HTTPS only

---

## 🎉 Summary

**✅ Deployment Issue**: FIXED (Pillow updated to 10.3.0)  
**✅ Admin Portal**: COMPLETE with all requested features  
**✅ Content Management**: Ready to use  
**✅ Security**: Built-in Django authentication  
**✅ User-Friendly**: Rich admin interface  

### What You Can Do Now:
1. Manage school information
2. Post news and announcements
3. Upload photos and videos
4. Add teacher profiles
5. Schedule events
6. Upload documents
7. View contact messages
8. Control what's published

### Total Features:
- **9 major sections**
- **8 content types**
- **25+ management features**
- **Full CRUD operations**
- **Search and filtering**
- **Image uploads**
- **File management**
- **Message tracking**

---

**Ready to manage your school website!** 🎓

**Next**: Run migrations, create superuser, and start adding content!

