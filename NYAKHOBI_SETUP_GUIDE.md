# St. Mary's Nyakhobi Senior School Website - Complete Setup Guide

## About This Project
This website was created for St. Mary's Nyakhobi Senior School (formerly Nyakhobi Secondary School) located in Funyula, Busia County, Kenya.

**School Details:**
- **Principal:** Mr. Dan F. Olopi
- **Location:** Off Nambuku/Funyula Rd, Funyula
- **Address:** P.O. Box 254, Funyula 50406, Busia County
- **Phone:** +254 722 231798 / +254 723 273109
- **Email:** nyakhobisecondaryschool@gmail.com
- **Type:** Mixed Day, Sub-County Public Secondary School

## Quick Start (Windows)

### 1. Install Python (First Time Only)
1. Download Python 3.8+ from: https://www.python.org/downloads/
2. During installation, **CHECK** "Add Python to PATH"
3. Restart your computer after installation

### 2. Set Up the Website
Open PowerShell in the project folder and run:

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\Activate.ps1

# Install required packages
pip install -r requirements.txt

# Set up database
python manage.py makemigrations
python manage.py migrate

# Load sample school data
python manage.py loaddata sample_data.json

# Create admin account (you'll be prompted for username/password)
python manage.py createsuperuser

# Start the website
python manage.py runserver
```

### 3. Access Your Website
- **Main Website:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/

## What's Included

### ✅ **School-Specific Features:**
- **Home Page** with school statistics and news
- **About Page** with Principal's welcome message
- **Academics** with Kenyan curriculum (Form 1-4)
- **Admissions** with KCPE-based application system
- **Faculty Management** with department structure
- **Events & News** featuring community activities
- **Contact Information** with accurate school details
- **Photo Gallery** ready for school events
- **Mobile-Responsive** design

### 📱 **Real Content Already Added:**
- Principal: Mr. Dan F. Olopi
- School location and contact details
- Academic departments (Sciences, Languages, Humanities, Technical)
- Sample news about NACADA programs
- Form 1-4 grade levels
- Kenyan curriculum subjects
- School statistics and quick facts

## Managing Content

### Admin Panel Access
1. Go to http://127.0.0.1:8000/admin/
2. Login with your superuser account
3. You can manage:
   - School information
   - Faculty profiles
   - Events and news
   - Student inquiries
   - Academic programs
   - Photo galleries

### Adding Content
- **News & Events:** Add school activities, KCSE results, etc.
- **Faculty:** Update teacher profiles and qualifications
- **Gallery:** Upload photos from school events
- **Quick Links:** Customize homepage shortcuts
- **Contact Forms:** Review student/parent inquiries

## Website Pages Structure

```
Homepage (/)
├── About Us (/about/)
├── Academics (/academics/)
│   ├── Programs
│   └── Academic Calendar
├── Admissions (/admissions/)
│   ├── Information
│   ├── Apply Online
│   └── Requirements
├── Faculty (/faculty/)
├── School Life
│   ├── Events (/events/)
│   ├── News (/events/news/)
│   └── Gallery (/events/gallery/)
└── Contact (/contact/)
```

## Customization for Your School

### Update School Information
1. Login to admin panel
2. Go to "Home" → "School Information"
3. Edit contact details, mission statement, etc.

### Add Your Faculty
1. Go to "Faculty" → "Faculty"
2. Add teacher profiles with photos and qualifications
3. Organize by departments

### Post School News
1. Go to "Events" → "News"
2. Add announcements, KCSE results, achievements
3. Mark important news as "Featured"

### Upload Photos
1. Go to "Events" → "Gallery"
2. Upload event photos, school activities
3. Organize by events

## Technical Support

### Common Issues
- **Python not found:** Reinstall Python and check "Add to PATH"
- **Port already in use:** Change port: `python manage.py runserver 8001`
- **Database errors:** Delete `db.sqlite3` and run migrations again

### Getting Help
- Django Documentation: https://docs.djangoproject.com/
- Contact the developer for technical issues
- Check the Facebook page for community support

## Production Deployment
For hosting on a live server:
1. Set `DEBUG = False` in settings.py
2. Configure proper database (PostgreSQL)
3. Set up media file serving
4. Use Apache/Nginx web server
5. Configure email for contact forms

---

**Built for St. Mary's Nyakhobi Senior School**  
*Building Leaders for Tomorrow*

Contact: nyakhobisecondaryschool@gmail.com  
Facebook: Nyakhobi Secondary School