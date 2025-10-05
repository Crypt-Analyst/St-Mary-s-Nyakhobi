# St. Mary's Nyakhobi Senior School - Security Implementation Guide

## Overview
This document outlines the security measures implemented for the St. Mary's Nyakhobi Senior School website and provides guidelines for maintaining a secure online presence.

---

## ✅ Implemented Security Features

### 1. Django Security Settings
- **HTTPS/SSL Redirect**: Forces all HTTP traffic to HTTPS in production
- **Secure Cookies**: Session and CSRF cookies marked as secure
- **HSTS (HTTP Strict Transport Security)**: 1-year policy with subdomain inclusion
- **XSS Protection**: Browser XSS filter enabled
- **Content Type Sniffing**: Disabled to prevent MIME-type attacks
- **Clickjacking Protection**: X-Frame-Options set to DENY
- **Referrer Policy**: Strict origin policy for cross-origin requests

### 2. Password Security
- **Minimum Length**: 12 characters required
- **Complexity Checks**: 
  - User attribute similarity validation
  - Common password detection
  - Numeric-only password prevention
- **Validators**: Django's built-in password validators enabled

### 3. Form Protection
- **CSRF Protection**: Enabled on all forms
- **reCAPTCHA**: Integrated on contact form to prevent spam
- **Input Validation**: Server-side validation on all user inputs
- **XSS Prevention**: Django's template auto-escaping enabled

### 4. Session Management
- **Session Timeout**: 1 hour of inactivity
- **HTTP Only Cookies**: JavaScript cannot access session cookies
- **Same-Site Cookies**: Protection against CSRF attacks
- **Secure Storage**: Sessions stored server-side

### 5. Environment Variables
- **Sensitive Data**: All secrets stored in environment variables
- **Configuration**: `.env` file for local, environment vars for production
- **Secret Key**: Moved to environment variable
- **Database Credentials**: Stored securely

### 6. Logging & Monitoring
- **Application Logs**: Rotating file logs (15MB max, 10 backups)
- **Security Logs**: Separate security event logging
- **Error Tracking**: Warning and error level logging
- **Log Location**: `logs/django.log` and `logs/security.log`

---

## 🔐 Production Deployment Checklist

### Pre-Deployment
- [ ] Set `DEBUG = False` in production environment
- [ ] Generate strong SECRET_KEY (use: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`)
- [ ] Configure all environment variables in `.env` file
- [ ] Set correct `ALLOWED_HOSTS` for production domain
- [ ] Set up PostgreSQL database (Supabase configured)
- [ ] Configure email settings for SMTP server
- [ ] Obtain and configure Google reCAPTCHA keys

### SSL/TLS Certificate
- [ ] Purchase or obtain free SSL certificate (Let's Encrypt recommended)
- [ ] Install certificate on web server/hosting platform
- [ ] Verify HTTPS is working correctly
- [ ] Enable auto-renewal for certificate
- [ ] Test SSL configuration: https://www.ssllabs.com/ssltest/

### Web Application Firewall (WAF)
**Recommended: Cloudflare (Free Plan Available)**
- [ ] Create Cloudflare account: https://www.cloudflare.com
- [ ] Add website to Cloudflare
- [ ] Update nameservers at domain registrar
- [ ] Enable WAF rules:
  - OWASP Core Ruleset
  - Cloudflare Managed Rules
  - Rate limiting (100 requests/minute per IP)
- [ ] Enable DDoS protection
- [ ] Configure page rules for caching
- [ ] Enable Always Use HTTPS
- [ ] Set SSL/TLS mode to "Full (strict)"

### Database Security
- [ ] Use strong database password (20+ characters)
- [ ] Enable SSL/TLS for database connections
- [ ] Restrict database access to application server IPs only
- [ ] Enable automated backups (daily recommended)
- [ ] Test backup restoration process
- [ ] Set up point-in-time recovery if available

### Backup Strategy
**Recommended Schedule:**
- **Database**: Daily automatic backups (retain 30 days)
- **Media Files**: Weekly backups (retain 4 weeks)
- **Code**: Version controlled via Git (GitHub)

**Backup Locations:**
- Primary: Hosting provider's backup system
- Secondary: Supabase automatic backups
- Tertiary: External storage (Google Drive/Dropbox)

**Testing:**
- [ ] Perform monthly backup restoration tests
- [ ] Document recovery procedures
- [ ] Maintain recovery time objective (RTO) < 4 hours

### Monitoring & Alerts
**Uptime Monitoring (UptimeRobot - Free Plan)**
- [ ] Create account: https://uptimerobot.com
- [ ] Add HTTP(S) monitor for: `https://www.nyakhobi.ac.ke`
- [ ] Set check interval: 5 minutes
- [ ] Configure alert contacts:
  - Email: IT administrator
  - SMS: Principal (optional)
- [ ] Add status page for public visibility

**Log Monitoring:**
- [ ] Review logs weekly for anomalies
- [ ] Set up log rotation (configured: 15MB max, 10 files)
- [ ] Monitor for:
  - Failed login attempts (>5 in 10 minutes)
  - 404 errors (potential scanning)
  - 500 errors (application issues)
  - CSRF failures (attack attempts)

### File Integrity Monitoring
- [ ] Take initial snapshot of application files
- [ ] Use Git to track changes
- [ ] Monitor for unauthorized file modifications
- [ ] Set up alerts for changes to critical files:
  - settings.py
  - urls.py
  - wsgi.py
  - Database files

### Access Control
**Admin Panel (/admin/):**
- [ ] Use strong, unique passwords (12+ characters)
- [ ] Limit admin user accounts (2-3 maximum)
- [ ] Enable two-factor authentication (2FA) if possible
- [ ] Change admin URL path (e.g., `/secure-admin/`)
- [ ] Restrict admin access by IP if possible

**User Roles:**
- [ ] Define role-based permissions
- [ ] Principle of least privilege
- [ ] Regular audit of user accounts
- [ ] Disable/remove inactive accounts

### Security Headers
All configured in production mode:
```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

Test headers: https://securityheaders.com

---

## 🛡️ Regular Security Maintenance

### Daily Tasks
- Monitor uptime alerts
- Check for critical security notifications

### Weekly Tasks
- Review application logs for anomalies
- Check failed login attempts
- Verify backups are running
- Review website uptime reports

### Monthly Tasks
- Test backup restoration
- Review and update passwords
- Check for Django security updates
- Scan for vulnerabilities
- Review user access permissions
- Update dependencies (`pip list --outdated`)

### Quarterly Tasks
- Full security audit
- Penetration testing (if budget allows)
- Review and update security policies
- Staff security training
- Update emergency response procedures

---

## 🚨 Incident Response Procedures

### 1. Detection
**Signs of Security Incident:**
- Unusual traffic patterns
- Unexplained downtime
- Defaced pages
- Unauthorized access alerts
- Database anomalies
- User complaints about suspicious activity

### 2. Initial Response (Within 15 minutes)
1. **Document Everything**: Note time, symptoms, affected systems
2. **Notify Key Personnel**:
   - Principal: nyakhobisecsch@gmail.com
   - IT Administrator
   - School Board (if serious)
3. **Assess Impact**: 
   - What data is affected?
   - How many users impacted?
   - Is attack ongoing?

### 3. Containment (Within 1 hour)
1. **For Defacement**:
   - Take screenshots for evidence
   - Restore from last known good backup
   - Change all admin passwords
   
2. **For Data Breach**:
   - Isolate affected systems
   - Preserve logs and evidence
   - Engage legal counsel if student data compromised
   
3. **For DDoS Attack**:
   - Enable Cloudflare "Under Attack" mode
   - Contact hosting provider
   - Increase rate limiting

### 4. Eradication
- Identify and fix vulnerability
- Remove malicious code/accounts
- Patch security holes
- Update all credentials

### 5. Recovery
- Restore services from backups
- Monitor for recurring issues
- Verify data integrity
- Gradually restore normal operations

### 6. Post-Incident Review
- Conduct thorough analysis
- Document lessons learned
- Update security procedures
- Implement preventive measures
- Staff debriefing and training

### Emergency Contacts
- **Hosting Provider Support**: [Add contact info]
- **Domain Registrar**: [Add contact info]
- **Cloudflare Support**: https://support.cloudflare.com
- **Local Cybercrime Unit**: [Add contact info]
- **Legal Counsel**: [Add contact info]

---

## 🔍 Vulnerability Scanning

### Tools for Regular Scanning

**1. OWASP ZAP (Free, Open Source)**
```bash
# Installation
pip install zaproxy

# Basic scan
zap-cli quick-scan --self-contained https://www.nyakhobi.ac.ke
```

**2. Nikto (Free, Open Source)**
```bash
# Installation (Linux/Mac)
sudo apt install nikto  # or brew install nikto

# Basic scan
nikto -h https://www.nyakhobi.ac.ke
```

**3. Online Tools (Free)**
- SSL Test: https://www.ssllabs.com/ssltest/
- Security Headers: https://securityheaders.com
- Mozilla Observatory: https://observatory.mozilla.org

### Recommended Scan Schedule
- **Weekly**: Automated basic scans
- **Monthly**: Full vulnerability assessment
- **After Updates**: Scan after major changes

---

## 📊 Security Metrics to Track

### Key Performance Indicators (KPIs)
1. **Uptime Percentage**: Target 99.9%
2. **Failed Login Attempts**: Monitor for brute force
3. **Response Time**: Alert if >5 seconds
4. **SSL Certificate Expiry**: Alert 30 days before
5. **Backup Success Rate**: Should be 100%
6. **Vulnerability Count**: Track and remediate
7. **Time to Patch**: Target <24 hours for critical

### Monthly Security Report Template
```
St. Mary's Nyakhobi - Security Report
Month: [Month Year]

1. Uptime: [XX.XX%]
2. Security Incidents: [Count]
3. Failed Login Attempts: [Count]
4. Backup Success Rate: [XX%]
5. Vulnerabilities Found: [Count]
6. Vulnerabilities Fixed: [Count]
7. Software Updates Applied: [Count]
8. Average Response Time: [X.XX seconds]

Actions Required:
- [Action item 1]
- [Action item 2]

Recommendations:
- [Recommendation 1]
- [Recommendation 2]
```

---

## 🎓 Security Best Practices for Staff

### For Website Administrators
1. Use password manager (LastPass, 1Password, Bitwarden)
2. Enable 2FA on all accounts
3. Never share passwords
4. Log out after each session
5. Use private/incognito mode on shared computers
6. Be cautious of phishing emails
7. Report suspicious activity immediately
8. Keep software updated
9. Use VPN when working remotely
10. Regular security training

### For Content Managers
1. Verify file uploads are from trusted sources
2. Scan files for viruses before uploading
3. Use strong, unique passwords
4. Don't install unauthorized plugins/extensions
5. Report any unusual behavior

### Email Security
1. Verify sender before clicking links
2. Don't open suspicious attachments
3. Use school email for official communications
4. Report phishing attempts to IT
5. Enable spam filters

---

## 📞 Support and Resources

### Django Security Resources
- Official Security Docs: https://docs.djangoproject.com/en/4.2/topics/security/
- Security Releases: https://www.djangoproject.com/weblog/
- Security Mailing List: django-announce@googlegroups.com

### External Resources
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- Django Security Checklist: https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
- Mozilla Web Security Guidelines: https://infosec.mozilla.org/guidelines/web_security

### Getting Help
1. **Django Community**: https://forum.djangoproject.com/
2. **Stack Overflow**: https://stackoverflow.com/questions/tagged/django
3. **Professional Security Audit**: Consider annual external audit

---

## ✅ Security Compliance Checklist

Use this checklist for quarterly security reviews:

### Application Security
- [ ] DEBUG = False in production
- [ ] Strong SECRET_KEY in use
- [ ] All secrets in environment variables
- [ ] ALLOWED_HOSTS properly configured
- [ ] HTTPS enforced (SECURE_SSL_REDIRECT = True)
- [ ] Security headers configured
- [ ] CSRF protection enabled
- [ ] XSS protection enabled
- [ ] SQL injection protection (using ORM)
- [ ] File upload restrictions in place

### Infrastructure Security
- [ ] SSL/TLS certificate valid and auto-renewing
- [ ] WAF (Cloudflare) active and configured
- [ ] DDoS protection enabled
- [ ] Rate limiting configured
- [ ] Database encrypted in transit
- [ ] Database access restricted by IP
- [ ] Server OS updated
- [ ] Firewall rules configured

### Access Control
- [ ] Admin accounts use strong passwords
- [ ] 2FA enabled where available
- [ ] Regular user access review
- [ ] Inactive accounts disabled
- [ ] Principle of least privilege followed
- [ ] Admin URL changed from default

### Monitoring & Logging
- [ ] Uptime monitoring active
- [ ] Log files being generated
- [ ] Log rotation configured
- [ ] Security logs reviewed weekly
- [ ] Alerts configured and tested
- [ ] Backup monitoring active

### Backups & Recovery
- [ ] Daily database backups configured
- [ ] Backup restoration tested this quarter
- [ ] Multiple backup locations
- [ ] Recovery procedures documented
- [ ] RTO/RPO defined and achievable

### Compliance & Documentation
- [ ] Security documentation up to date
- [ ] Incident response plan current
- [ ] Emergency contacts current
- [ ] Staff trained on security procedures
- [ ] Vulnerability scan completed
- [ ] Dependencies updated
- [ ] Security audit findings addressed

---

## Document Version Control
- **Version**: 1.0
- **Last Updated**: October 5, 2025
- **Next Review**: January 5, 2026
- **Maintained By**: IT Department
- **Contact**: nyakhobisecsch@gmail.com

---

*This document should be reviewed and updated quarterly or after any significant security incident.*
