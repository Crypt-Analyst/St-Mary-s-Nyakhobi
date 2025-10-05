# Production Deployment Checklist
## St. Mary's Nyakhobi Senior School Website

---

## 🚀 Pre-Deployment Preparation

### 1. Code Repository
- [ ] All code committed to Git
- [ ] No sensitive data in repository
- [ ] `.gitignore` configured properly
- [ ] README.md updated
- [ ] Requirements.txt up to date
- [ ] Git tags created for version

### 2. Environment Configuration
- [ ] `.env.example` file created
- [ ] Production `.env` file prepared (DO NOT commit)
- [ ] All environment variables documented
- [ ] Secret keys generated:
  ```bash
  python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
  ```

### 3. Django Settings
- [ ] `DEBUG = False` in production
- [ ] `SECRET_KEY` from environment variable
- [ ] `ALLOWED_HOSTS` set to production domains
- [ ] Database configured (PostgreSQL/Supabase)
- [ ] Static files configuration verified
- [ ] Media files configuration verified
- [ ] Email backend configured (SMTP)
- [ ] Security settings enabled (HTTPS, HSTS, etc.)

### 4. Database
- [ ] PostgreSQL instance created (Supabase)
- [ ] Database credentials secured
- [ ] Database migrations up to date
- [ ] Test data removed
- [ ] Backup strategy configured
- [ ] SSL/TLS connection enabled

### 5. Dependencies
- [ ] All dependencies listed in requirements.txt
- [ ] Compatible versions verified
- [ ] Security vulnerabilities checked:
  ```bash
  pip install safety
  safety check
  ```

---

## 🌐 Hosting Setup

### Option A: PythonAnywhere (Recommended for Django)

#### Account Setup
- [ ] Create account: https://www.pythonanywhere.com
- [ ] Choose appropriate plan ($5/month for Hacker plan)
- [ ] Verify email address

#### Upload Code
- [ ] Method 1: Git clone
  ```bash
  cd ~
  git clone https://github.com/Crypt-Analyst/St-Mary-s-Nyakhobi.git
  cd St-Mary-s-Nyakhobi
  ```
- [ ] Method 2: Upload via Files tab

#### Virtual Environment
```bash
cd ~/St-Mary-s-Nyakhobi
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Environment Variables
- [ ] Create `.env` file in project root
- [ ] Copy from `.env.example` and fill in values
- [ ] Set in PythonAnywhere dashboard:
  - Dashboard → Web → Environment variables

#### Database Setup
- [ ] Configure PostgreSQL connection in `.env`
- [ ] Run migrations:
  ```bash
  python manage.py migrate
  ```
- [ ] Create superuser:
  ```bash
  python manage.py createsuperuser
  ```

#### Static Files
```bash
python manage.py collectstatic --no-input
```

#### WSGI Configuration
- [ ] Go to Web tab → WSGI configuration file
- [ ] Update paths to your project
- [ ] Example configuration:
  ```python
  import os
  import sys
  
  path = '/home/yourusername/St-Mary-s-Nyakhobi'
  if path not in sys.path:
      sys.path.insert(0, path)
  
  os.environ['DJANGO_SETTINGS_MODULE'] = 'st_marys_school.settings'
  
  from django.core.wsgi import get_wsgi_application
  application = get_wsgi_application()
  ```

#### Force HTTPS
- [ ] Web tab → Force HTTPS → Enabled

#### Set Domain
- [ ] Add domain: www.nyakhobi.ac.ke
- [ ] Configure DNS at registrar

---

### Option B: Railway.app (Alternative)

#### Setup
- [ ] Create account: https://railway.app
- [ ] Connect GitHub repository
- [ ] Add PostgreSQL plugin
- [ ] Configure environment variables

#### Environment Variables
```
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=nyakhobi.ac.ke,www.nyakhobi.ac.ke
DATABASE_URL=postgres://...
```

#### Deploy
- [ ] Push to main branch triggers auto-deploy
- [ ] Monitor build logs
- [ ] Run migrations via Railway CLI

---

### Option C: Traditional VPS (DigitalOcean/Linode)

#### Server Setup
- [ ] Create Ubuntu 22.04 LTS droplet/server
- [ ] Set up SSH keys
- [ ] Update system:
  ```bash
  sudo apt update && sudo apt upgrade -y
  ```

#### Install Dependencies
```bash
sudo apt install python3.10 python3.10-venv python3-pip nginx postgresql postgresql-contrib
sudo apt install certbot python3-certbot-nginx
```

#### Application Setup
```bash
cd /var/www
sudo git clone https://github.com/Crypt-Analyst/St-Mary-s-Nyakhobi.git
cd St-Mary-s-Nyakhobi
sudo python3.10 -m venv venv
source venv/bin/activate
sudo pip install -r requirements.txt
sudo pip install gunicorn
```

#### Gunicorn Service
- [ ] Create `/etc/systemd/system/stmarys.service`:
  ```ini
  [Unit]
  Description=St Marys Gunicorn daemon
  After=network.target

  [Service]
  User=www-data
  Group=www-data
  WorkingDirectory=/var/www/St-Mary-s-Nyakhobi
  Environment="PATH=/var/www/St-Mary-s-Nyakhobi/venv/bin"
  ExecStart=/var/www/St-Mary-s-Nyakhobi/venv/bin/gunicorn \
            --workers 3 \
            --bind unix:/var/www/St-Mary-s-Nyakhobi/stmarys.sock \
            st_marys_school.wsgi:application

  [Install]
  WantedBy=multi-user.target
  ```

#### Nginx Configuration
- [ ] Create `/etc/nginx/sites-available/stmarys`:
  ```nginx
  server {
      listen 80;
      server_name nyakhobi.ac.ke www.nyakhobi.ac.ke;

      location = /favicon.ico { access_log off; log_not_found off; }
      
      location /static/ {
          alias /var/www/St-Mary-s-Nyakhobi/staticfiles/;
      }
      
      location /media/ {
          alias /var/www/St-Mary-s-Nyakhobi/media/;
      }

      location / {
          proxy_set_header Host $http_host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_set_header X-Forwarded-Proto $scheme;
          proxy_pass http://unix:/var/www/St-Mary-s-Nyakhobi/stmarys.sock;
      }
  }
  ```

#### Enable Services
```bash
sudo systemctl start stmarys
sudo systemctl enable stmarys
sudo systemctl restart nginx
```

#### SSL Certificate
```bash
sudo certbot --nginx -d nyakhobi.ac.ke -d www.nyakhobi.ac.ke
```

---

## 🔐 Security Configuration

### 1. SSL/TLS Certificate
- [ ] Certificate installed and valid
- [ ] Auto-renewal configured
- [ ] Test at https://www.ssllabs.com/ssltest/

### 2. Cloudflare Setup
- [ ] Account created: https://cloudflare.com
- [ ] Website added to Cloudflare
- [ ] Nameservers updated at registrar:
  - Check current nameservers
  - Update to Cloudflare nameservers
  - Wait for propagation (24-48 hours)
- [ ] SSL/TLS mode: Full (strict)
- [ ] Always Use HTTPS: Enabled
- [ ] Automatic HTTPS Rewrites: Enabled
- [ ] Minimum TLS Version: 1.2
- [ ] WAF (Firewall Rules):
  - Enable OWASP rules
  - Enable Cloudflare Managed Rules
  - Rate limiting: 100 req/min per IP
- [ ] Page Rules configured:
  - Cache everything for static assets
  - Force HTTPS
- [ ] DDoS protection: Auto-enabled

### 3. Django Security Headers
All configured in settings.py when `DEBUG = False`:
- [ ] SECURE_SSL_REDIRECT = True
- [ ] SESSION_COOKIE_SECURE = True
- [ ] CSRF_COOKIE_SECURE = True
- [ ] SECURE_HSTS_SECONDS = 31536000
- [ ] Test at https://securityheaders.com

### 4. Database Security
- [ ] Strong password set (20+ characters)
- [ ] SSL/TLS enabled for connections
- [ ] Access restricted to application server IPs
- [ ] Regular backups configured

### 5. Access Control
- [ ] Admin URL changed (edit urls.py)
- [ ] Strong admin passwords
- [ ] 2FA enabled (if available)
- [ ] Regular user audit schedule

---

## 📊 Monitoring Setup

### 1. UptimeRobot
- [ ] Account created: https://uptimerobot.com
- [ ] Monitor added: https://www.nyakhobi.ac.ke
- [ ] Check interval: 5 minutes
- [ ] Alert contacts configured:
  - Primary: nyakhobisecsch@gmail.com
  - Secondary: [Add phone number for SMS]
- [ ] Public status page created (optional)

### 2. Google Analytics (Optional)
- [ ] Account created
- [ ] Tracking code added to base.html
- [ ] Goals configured
- [ ] Privacy policy updated

### 3. Google Search Console
- [ ] Property added and verified
- [ ] Sitemap submitted
- [ ] Mobile usability checked
- [ ] Core Web Vitals monitored

---

## 💾 Backup Configuration

### Automated Backups
- [ ] Database backups: Daily at 2 AM
- [ ] Media files backups: Weekly
- [ ] Backup retention: 30 days
- [ ] Backup locations:
  - Primary: Hosting provider
  - Secondary: Supabase
  - Tertiary: External (Google Drive)

### Backup Testing
- [ ] Initial restoration test completed
- [ ] Monthly restoration test scheduled
- [ ] Recovery procedure documented
- [ ] Recovery time objective (RTO): < 4 hours
- [ ] Recovery point objective (RPO): < 24 hours

---

## 🎯 Google reCAPTCHA

### Setup
- [ ] Visit: https://www.google.com/recaptcha/admin
- [ ] Create new site
- [ ] Select reCAPTCHA v2 "I'm not a robot"
- [ ] Add domains: nyakhobi.ac.ke, www.nyakhobi.ac.ke
- [ ] Copy Site Key and Secret Key
- [ ] Add to production `.env`:
  ```
  RECAPTCHA_PUBLIC_KEY=your_site_key
  RECAPTCHA_PRIVATE_KEY=your_secret_key
  ```

---

## 📧 Email Configuration

### SMTP Setup (Gmail)
- [ ] Create dedicated school Gmail account
- [ ] Enable 2-Step Verification
- [ ] Generate App Password
- [ ] Configure in `.env`:
  ```
  EMAIL_HOST=smtp.gmail.com
  EMAIL_PORT=587
  EMAIL_USE_TLS=True
  EMAIL_HOST_USER=info@stmarysnyakhobi.ac.ke
  EMAIL_HOST_PASSWORD=app_password_here
  ```
- [ ] Test email sending:
  ```bash
  python manage.py shell
  >>> from django.core.mail import send_mail
  >>> send_mail('Test', 'Test message', 'info@stmarysnyakhobi.ac.ke', ['nyakhobisecsch@gmail.com'])
  ```

### Alternative: SendGrid (Recommended for production)
- [ ] Create SendGrid account
- [ ] Verify sender identity
- [ ] Generate API key
- [ ] Install: `pip install sendgrid`
- [ ] Configure in settings

---

## 🧪 Testing

### Pre-Launch Testing
- [ ] All pages load without errors
- [ ] Forms submit successfully
- [ ] Contact form sends emails
- [ ] reCAPTCHA works
- [ ] Admin panel accessible
- [ ] Static files loading
- [ ] Media files accessible
- [ ] Mobile responsiveness
- [ ] Cross-browser testing:
  - Chrome
  - Firefox
  - Safari
  - Edge
- [ ] Page load speed < 3 seconds
- [ ] SSL certificate valid
- [ ] Security headers present
- [ ] 404 page works
- [ ] 500 page works

### Security Testing
- [ ] SQL injection tests
- [ ] XSS attempts blocked
- [ ] CSRF protection working
- [ ] Rate limiting functional
- [ ] File upload restrictions
- [ ] Admin brute force protection
- [ ] Run OWASP ZAP scan
- [ ] Check for exposed secrets

---

## 🌍 DNS Configuration

### At Domain Registrar
- [ ] A Record: @ → Server IP (or Cloudflare IP)
- [ ] A Record: www → Server IP (or Cloudflare IP)
- [ ] MX Records (for email)
- [ ] TXT Record (for SPF/DKIM if using email)
- [ ] Nameservers: Cloudflare nameservers

### Example DNS Records
```
Type    Name    Content             TTL
A       @       104.21.xxx.xxx      Auto
A       www     104.21.xxx.xxx      Auto
CNAME   mail    mail.google.com     Auto
```

### Verification
```bash
nslookup nyakhobi.ac.ke
nslookup www.nyakhobi.ac.ke
```

---

## 📱 Post-Deployment

### Immediate Checks (Within 1 hour)
- [ ] Website loads over HTTPS
- [ ] HTTP redirects to HTTPS
- [ ] All pages accessible
- [ ] Contact form working
- [ ] No console errors in browser
- [ ] Uptime monitor showing "Up"
- [ ] Admin panel accessible
- [ ] Email notifications working

### First 24 Hours
- [ ] Monitor for errors in logs
- [ ] Check uptime status
- [ ] Test backup job ran successfully
- [ ] Monitor traffic (should see activity)
- [ ] Check for any security alerts

### First Week
- [ ] Daily log review
- [ ] Monitor uptime statistics
- [ ] Check Google Search Console
- [ ] Review Cloudflare analytics
- [ ] Test backup restoration
- [ ] Gather user feedback

### First Month
- [ ] Weekly security scans
- [ ] Review all monitoring metrics
- [ ] Optimize slow pages
- [ ] Update documentation
- [ ] Staff training on CMS
- [ ] Schedule security audit

---

## 📋 Launch Communication

### Stakeholders to Notify
- [ ] Principal
- [ ] School Board
- [ ] Teachers/Staff
- [ ] Parents (via email/SMS)
- [ ] Students
- [ ] IT team

### Launch Announcement Template
```
Subject: St. Mary's Nyakhobi New Website Launch

Dear [Stakeholder],

We are pleased to announce the launch of our new school website at:
https://www.nyakhobi.ac.ke

Features include:
- Modern, mobile-friendly design
- Academic information and programs
- Online admissions inquiry
- News and events updates
- Faculty directory
- Student portal (coming soon)

For any issues or feedback, please contact:
nyakhobisecsch@gmail.com

Thank you for your support!

St. Mary's Nyakhobi Senior School
```

---

## 🔧 Troubleshooting

### Common Issues

**Website not loading:**
- Check DNS propagation: https://dnschecker.org
- Verify nameservers point to Cloudflare
- Check hosting server status
- Review nginx/gunicorn logs

**Static files not loading:**
```bash
python manage.py collectstatic --no-input
```

**Database connection error:**
- Verify DATABASE_URL in environment variables
- Check database server status
- Verify SSL/TLS settings
- Check firewall rules

**Email not sending:**
- Test SMTP credentials
- Check spam folder
- Verify Gmail app password
- Review email logs

**500 Internal Server Error:**
```bash
# Check logs
tail -f logs/django.log

# Restart services
sudo systemctl restart stmarys
sudo systemctl restart nginx
```

---

## ✅ Final Verification Checklist

### Security
- [ ] HTTPS working with valid certificate
- [ ] Security headers present
- [ ] Cloudflare active
- [ ] WAF rules enabled
- [ ] Rate limiting configured
- [ ] Backups running
- [ ] Monitoring active
- [ ] Admin URL changed
- [ ] Strong passwords enforced

### Functionality
- [ ] All pages load
- [ ] Forms work
- [ ] Emails send
- [ ] reCAPTCHA works
- [ ] Admin accessible
- [ ] Mobile responsive
- [ ] Fast page loads

### Documentation
- [ ] SECURITY.md reviewed
- [ ] README.md updated
- [ ] Environment variables documented
- [ ] Recovery procedures documented
- [ ] Emergency contacts updated

### Compliance
- [ ] Privacy policy present (if required)
- [ ] Cookie notice (if required)
- [ ] Terms of service (if required)
- [ ] Data protection measures

---

## 📞 Support Contacts

- **Web Developer**: [Your contact]
- **Hosting Provider**: [Provider support]
- **Domain Registrar**: [Registrar support]
- **Cloudflare**: https://support.cloudflare.com
- **School IT**: nyakhobisecsch@gmail.com

---

## 🎉 Congratulations!

If all items are checked, your website is ready for production!

**Remember:**
- Regular backups
- Security updates
- Log monitoring
- User feedback
- Continuous improvement

---

**Deployment Date**: __________
**Deployed By**: __________
**Version**: 1.0
**Next Review**: __________

