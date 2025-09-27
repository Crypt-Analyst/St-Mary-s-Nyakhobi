# St. Mary's School Website - Manual Setup Instructions

## Prerequisites
1. **Install Python 3.8+**
   - Download from: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"

## Setup Instructions

### 1. Create Virtual Environment
```bash
python -m venv venv
```

### 2. Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Admin Account
```bash
python manage.py createsuperuser
```
Follow the prompts to create your admin username, email, and password.

### 6. Collect Static Files
```bash
python manage.py collectstatic
```

### 7. Start Development Server
```bash
python manage.py runserver
```

## Access Your Website
- **Main Website:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/

## Adding Content
1. Access the admin panel using the superuser account you created
2. Add school information, faculty members, events, news, etc.
3. Upload images for sliders and gallery
4. Configure quick links and other homepage elements

## Project Structure
```
st_marys_school/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── st_marys_school/          # Main project settings
├── home/                     # Homepage app
├── academics/                # Academic programs
├── admissions/               # Admissions system
├── faculty/                  # Faculty management
├── events/                   # Events and news
├── contact/                  # Contact forms
├── templates/                # HTML templates
├── static/                   # CSS, JS, images
└── media/                    # Uploaded files
```

## Features Included
- **Responsive Design** - Works on all devices
- **Admin Panel** - Easy content management
- **Contact Forms** - Inquiry and admission forms
- **Event Calendar** - School events and news
- **Faculty Directory** - Staff profiles
- **Photo Gallery** - Image galleries
- **Academic Programs** - Course information
- **SEO Optimized** - Search engine friendly

## Customization
- Edit `templates/` for HTML changes
- Modify `static/css/style.css` for styling
- Update `static/js/main.js` for JavaScript
- Change colors in CSS `:root` variables

## Production Deployment
For production deployment:
1. Set `DEBUG = False` in settings.py
2. Configure proper database (PostgreSQL recommended)
3. Set up media file serving
4. Configure email settings for contact forms
5. Use a proper web server (Apache/Nginx)

## Support
- Django Documentation: https://docs.djangoproject.com/
- Bootstrap Documentation: https://getbootstrap.com/docs/