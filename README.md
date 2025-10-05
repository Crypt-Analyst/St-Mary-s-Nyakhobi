# 🏫 St. Mary's Nyakhobi Senior School Website

[![Django](https://img.shields.io/badge/Django-4.2.7-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Cloud-blue.svg)](https://supabase.com/)
[![Security](https://img.shields.io/badge/Security-Hardened-brightgreen.svg)](SECURITY.md)
[![License](https://img.shields.io/badge/License-Educational-yellow.svg)](LICENSE)

> **Official website for St. Mary's Nyakhobi Senior School - Empowering minds, building futures in Funyula, Busia County, Kenya.**

## 🔐 Security Features

**Enterprise-grade security implemented!** This website includes:
- ✅ HTTPS/SSL encryption with HSTS
- ✅ Secure session management & cookies
- ✅ CSRF & XSS protection
- ✅ Strong password policies (12+ characters)
- ✅ reCAPTCHA spam protection
- ✅ Automated logging & monitoring
- ✅ Environment variable configuration
- ✅ Complete security documentation

**📚 Documentation:**
- [SECURITY.md](SECURITY.md) - Comprehensive security guide
- [DEPLOYMENT.md](DEPLOYMENT.md) - Production deployment checklist
- [QUICKSTART_SECURITY.md](QUICKSTART_SECURITY.md) - Quick security setup

## 🌟 About St. Mary's Nyakhobi Senior School

St. Mary's Nyakhobi Senior School (formerly Nyakhobi Secondary School) is a prestigious educational institution located in Funyula, Busia County, Kenya. We are committed to providing quality education that nurtures academic excellence, character development, and holistic growth of our students.

### 🎯 Our Mission
To provide quality, affordable, and accessible education that prepares students for success in their academic pursuits and future careers while instilling strong moral values.

### 🏆 Our Vision  
To be a leading educational institution in Kenya, recognized for academic excellence, innovation, and character development.

## 🚀 Website Features

### 📚 Academic Management
- **Course Information**: Comprehensive details about all academic programs
- **Subject Offerings**: Complete curriculum overview for all levels
- **Academic Calendar**: Important dates, terms, and examination schedules
- **Performance Tracking**: Academic achievement and progress monitoring

### 👥 Faculty & Staff
- **Teacher Profiles**: Detailed information about our qualified educators
- **Department Structure**: Organized by subject areas and specializations
- **Staff Directory**: Contact information and office hours
- **Professional Development**: Continuous learning and training programs

### 🎓 Student Services
- **Admissions Portal**: Online application and enrollment process
- **Requirements**: Clear admission criteria and documentation needed
- **Fee Structure**: Transparent pricing for all academic programs
- **Student Life**: Extracurricular activities and school culture

### 📞 Communication Hub
- **Contact Information**: Multiple ways to reach the school
- **Location Details**: Campus address and directions
- **Inquiry Forms**: Direct communication with administration
- **Emergency Contacts**: Important numbers for parents and students

### 📅 Events & News
- **School Calendar**: Upcoming events and important dates
- **News Updates**: Latest announcements and achievements
- **Photo Gallery**: School activities and memorable moments
- **Alumni Network**: Connecting graduates and current students

## 💻 Technical Specifications

### 🛠️ Built With
- **Backend Framework**: Django 4.2.7 (Python 3.13)
- **Database**: PostgreSQL (Cloud-hosted on Supabase)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Styling**: Custom maroon and white theme (school colors)
- **Forms**: Django Crispy Forms with Bootstrap integration
- **Media Handling**: Pillow for image processing
- **Static Files**: WhiteNoise for production deployment

### 📱 Responsive Design
- Mobile-first approach for accessibility on all devices
- Optimized for smartphones, tablets, and desktop computers
- Cross-browser compatibility (Chrome, Firefox, Safari, Edge)
- Fast loading times and SEO optimization

### 🔒 Security Features
- CSRF protection on all forms
- Secure database connections with SSL encryption
- Input validation and sanitization
- Admin panel with role-based access control

## 🚀 Installation & Setup

### Prerequisites
- Python 3.11+ installed on your system
- Git for version control
- Internet connection for database access

### Quick Start
1. **Clone the repository**
   ```bash
   git clone https://github.com/Crypt-Analyst/St-Mary-s-Nyakhobi.git
   cd St-Mary-s-Nyakhobi
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Load sample data** *(optional)*
   ```bash
   python manage.py loaddata sample_data.json
   ```

6. **Create admin user**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the website**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

### 📋 Dependencies
```
Django==4.2.7
psycopg2-binary==2.9.10
django-crispy-forms==2.3
crispy-bootstrap5==2024.10
Pillow==11.0.0
whitenoise==6.8.2
```

## 📁 Project Structure

```
St-Mary-s-Nyakhobi/
├── 🏠 home/              # Homepage and general info
├── 📚 academics/         # Academic programs & courses
├── 🎓 admissions/        # Student enrollment system
├── 👩‍🏫 faculty/           # Staff and teacher profiles
├── 📅 events/            # School events and calendar
├── 📞 contact/           # Contact forms and information
├── 🎨 templates/         # HTML templates
├── 📱 static/            # CSS, JavaScript, images
├── ⚙️ st_marys_school/   # Main Django configuration
├── 📊 sample_data.json   # Initial data fixtures
├── 📋 requirements.txt   # Python dependencies
└── 📖 README.md          # This file
```

## 🌐 Deployment

### Production Deployment Options
1. **Heroku**: Easy deployment with GitHub integration
2. **Railway**: Modern hosting platform with automatic deployments
3. **DigitalOcean App Platform**: Scalable cloud hosting
4. **AWS Elastic Beanstalk**: Enterprise-grade deployment

### Environment Variables
```bash
DEBUG=False
SECRET_KEY=your_secret_key_here
DATABASE_URL=your_postgresql_connection_string
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

## 🤝 Contributing

We welcome contributions from developers, educators, and community members who want to help improve St. Mary's Nyakhobi Senior School's digital presence.

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style Guidelines
- Follow PEP 8 Python style guide
- Use meaningful variable and function names
- Add comments for complex logic
- Write unit tests for new features
- Ensure mobile responsiveness for UI changes

## 📞 Contact & Support

### School Administration
- **Principal**: Mr. Dan F. Olopi
- **Phone**: 0719 831 346
- **Email**: admin@stmarysnyakhobi.ac.ke
- **Address**: Funyula, Busia County, Kenya

### Technical Support
- **Developer**: Crypt-Analyst
- **Email**: bilfordderek917@gmail.com
- **GitHub**: [@Crypt-Analyst](https://github.com/Crypt-Analyst)

### Website Issues
If you encounter any issues with the website, please:
1. Check our [Issues](https://github.com/Crypt-Analyst/St-Mary-s-Nyakhobi/issues) page
2. Create a new issue with detailed description
3. Contact technical support via email

## 📊 Project Status

- ✅ **Phase 1**: Core website structure and design (Completed)
- ✅ **Phase 2**: Database integration and admin panel (Completed)  
- ✅ **Phase 3**: Content management system (Completed)
- 🚧 **Phase 4**: Online payment integration (In Progress)
- 📋 **Phase 5**: Student portal and parent dashboard (Planned)
- 📋 **Phase 6**: Mobile application (Future)

## 📜 License

This project is developed for educational purposes for St. Mary's Nyakhobi Senior School. All rights reserved to the school administration.

## 🙏 Acknowledgments

- **St. Mary's Nyakhobi Senior School** - For trusting us with their digital presence
- **Django Community** - For the amazing web framework
- **Bootstrap Team** - For the responsive CSS framework
- **Supabase** - For reliable database hosting
- **GitHub** - For version control and collaboration platform

## 🔄 Changelog

### Version 1.0.0 (2025-09-27)
- Initial release with complete website functionality
- PostgreSQL database integration
- Responsive design with school branding
- Admin panel for content management
- All core modules implemented

---

<div align="center">

**🎓 Empowering Education Through Technology 🎓**

*Built with ❤️ for St. Mary's Nyakhobi Senior School*

[Website](http://stmarysnyakhobi.ac.ke) | [Admin Panel](http://stmarysnyakhobi.ac.ke/admin) | [Contact](mailto:admin@stmarysnyakhobi.ac.ke)

</div>