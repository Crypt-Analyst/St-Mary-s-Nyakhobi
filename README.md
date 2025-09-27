# St. Mary's Nyakhobi Senior School Website

A comprehensive school website built with Django, HTML, CSS, and JavaScript for St. Mary's Nyakhobi Senior School (formerly Nyakhobi Secondary School) located in Funyula, Busia County, Kenya.

## Features

- **Home Page** - Welcome message, school highlights, latest news
- **About Us** - School history, mission, vision, administration
- **Academics** - Programs, curriculum, academic calendar
- **Admissions** - Application process, requirements, online forms
- **Faculty & Staff** - Teacher profiles and departments
- **Student Life** - Activities, clubs, sports, student resources
- **Events & News** - School calendar and announcements
- **Contact** - Location, contact information, inquiry forms

## Technology Stack

- **Backend**: Python Django
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite (development), PostgreSQL (production)
- **Styling**: Bootstrap 5, Custom CSS
- **Forms**: Django Forms with Crispy Forms

## Installation

1. **Install Python 3.8+** (if not already installed)
   - Download from [python.org](https://www.python.org/downloads/)
   - Make sure to add Python to PATH during installation

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

7. **Access the Website**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Project Structure

```
st_marys_school/
├── manage.py
├── st_marys_school/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── home/                    # Home page app
├── academics/               # Academic programs app
├── admissions/              # Admissions app
├── faculty/                 # Faculty & staff app
├── events/                  # Events & news app
├── contact/                 # Contact forms app
├── static/                  # CSS, JS, images
└── templates/               # HTML templates
```

## Admin Panel

Access the Django admin panel to manage:
- School events and news
- Faculty profiles
- Academic programs
- Student inquiries
- Site content

## Deployment

Instructions for deploying to production servers will be provided separately.

## Support

For technical support, please contact the development team.