"""
Django settings for st_marys_nyakhobi_school project.
"""

from pathlib import Path
import os
from decouple import config, Csv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# Use environment variable in production
SECRET_KEY = config('SECRET_KEY', default='django-insecure-your-secret-key-change-this-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='st-mary-s-nyakhobi-1.onrender.com,.onrender.com,127.0.0.1,localhost', cast=Csv())

# Security Settings for Production
if not DEBUG:
    # HTTPS/SSL Settings
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    # Additional Security Headers
    SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'axes',  # Login attempt tracking and brute-force protection
    'cloudinary_storage',
    'cloudinary',
    'crispy_forms',
    'crispy_bootstrap5',
    # 'captcha',  # django-recaptcha - uncomment after pip install django-recaptcha
    
    # Local apps
    'home',
    'academics',
    'admissions',
    'faculty',
    'events',
    'contact',
    'news',
    'portal',
    'admin_portal',  # Custom admin portal
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Axes middleware for tracking login attempts (must be last)
    'axes.middleware.AxesMiddleware',
]

ROOT_URLCONF = 'st_marys_school.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'st_marys_school.wsgi.application'

# Database - Temporarily using SQLite for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Uncomment below to use Supabase PostgreSQL when connection issues are resolved
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'postgres',
#         'USER': 'postgres.gctpjhhxnfbqlydnpfwu',
#         'PASSWORD': 'F2QLPdltqZJ4n8vI',
#         'HOST': 'aws-1-eu-north-1.pooler.supabase.com',
#         'PORT': '5432',
#         'OPTIONS': {
#             'sslmode': 'require',
#         },
#     }
# }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 12,  # Strong password requirement
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Email settings (for contact forms)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Development only

# Production Email Settings (uncomment when ready for production)
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'info@stmarysnyakhobi.ac.ke'  # School email
# EMAIL_HOST_PASSWORD = 'your-email-password'  # Use environment variable in production
# DEFAULT_FROM_EMAIL = 'St. Mary\'s Nyakhobi Senior School <info@stmarysnyakhobi.ac.ke>'

# Contact form settings
ADMINS = [
    ('Principal', 'nyakhobisecsch@gmail.com'),
    ('Admin Office', 'nyakhobisecsch@gmail.com'),
]

# Email configuration for different purposes
CONTACT_EMAIL = 'nyakhobisecsch@gmail.com'
ADMISSIONS_EMAIL = 'nyakhobisecsch@gmail.com' 
PRINCIPAL_EMAIL = 'nyakhobisecsch@gmail.com'

# Google reCAPTCHA Settings
RECAPTCHA_PUBLIC_KEY = config('RECAPTCHA_PUBLIC_KEY', default='')
RECAPTCHA_PRIVATE_KEY = config('RECAPTCHA_PRIVATE_KEY', default='')
# For testing, you can use these test keys that always validate
# RECAPTCHA_PUBLIC_KEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
# RECAPTCHA_PRIVATE_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'
SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']

# Session Security
SESSION_COOKIE_AGE = 3600  # 1 hour
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_SAVE_EVERY_REQUEST = True

# CSRF Protection
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_USE_SESSIONS = False

# Logging Configuration
# Create logs directory if it doesn't exist
import os
LOGS_DIR = BASE_DIR / 'logs'
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR / 'django.log',
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'security_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR / 'security.log',
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
        'django.security': {
            'handlers': ['security_file'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}

# Production Database Configuration
# Use PostgreSQL in production if DATABASE_URL is provided
import dj_database_url
if 'DATABASE_URL' in os.environ:
    DATABASES['default'] = dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require=True
    )

# Cloudinary Configuration for Media Storage
# Use Cloudinary in production to persist uploaded images
import cloudinary
import cloudinary.uploader
import cloudinary.api

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME', default=''),
    'API_KEY': config('CLOUDINARY_API_KEY', default=''),
    'API_SECRET': config('CLOUDINARY_API_SECRET', default=''),
}

# Use Cloudinary for media files if configured
if CLOUDINARY_STORAGE['CLOUD_NAME']:
    cloudinary.config(
        cloud_name=CLOUDINARY_STORAGE['CLOUD_NAME'],
        api_key=CLOUDINARY_STORAGE['API_KEY'],
        api_secret=CLOUDINARY_STORAGE['API_SECRET'],
        secure=True
    )
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
else:
    # Fall back to local storage for development
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'


# ============================================================================
# DJANGO-AXES CONFIGURATION - BRUTE FORCE PROTECTION
# ============================================================================

# Authentication backends (required for django-axes)
AUTHENTICATION_BACKENDS = [
    # AxesStandaloneBackend should be the first backend in the AUTHENTICATION_BACKENDS list.
    'axes.backends.AxesStandaloneBackend',
    
    # Django ModelBackend is the default authentication backend.
    'django.contrib.auth.backends.ModelBackend',
]

# Django-Axes Settings for Login Protection
AXES_ENABLED = True  # Enable axes
AXES_FAILURE_LIMIT = 5  # Lock after 5 failed attempts
AXES_COOLOFF_TIME = 1  # Lock for 1 hour (in hours)
AXES_LOCKOUT_TEMPLATE = None  # Use default lockout message
AXES_LOCKOUT_URL = None  # Redirect to same page with error message

# NEW: Updated lockout tracking settings (replaces deprecated settings)
# Track by both username AND IP address for stronger security
AXES_LOCKOUT_PARAMETERS = [['username', 'ip_address']]

AXES_RESET_ON_SUCCESS = True  # Reset counter on successful login
AXES_ONLY_ADMIN_SITE = False  # Protect all login pages (admin + portal)
AXES_VERBOSE = True  # Show detailed messages

# What to track
AXES_LOCK_OUT_AT_FAILURE = True  # Enable lockout
AXES_USERNAME_FORM_FIELD = 'username'  # Form field name for username
AXES_PASSWORD_FORM_FIELD = 'password'  # Form field name for password

# Security enhancements
AXES_RESET_COOL_OFF_ON_FAILURE_DURING_LOCKOUT = False  # Don't extend lockout on attempts
AXES_NEVER_LOCKOUT_WHITELIST = False  # No whitelist bypass
AXES_NEVER_LOCKOUT_GET = False  # Protect GET requests too
AXES_IPWARE_PROXY_COUNT = 1  # For reverse proxy setups (Render, etc.)
AXES_IPWARE_META_PRECEDENCE_ORDER = [
    'HTTP_X_FORWARDED_FOR',
    'HTTP_X_REAL_IP',
    'REMOTE_ADDR',
]

# Failure messages
AXES_COOLOFF_MESSAGE = (
    'Account locked: too many login attempts. '
    'Try again after %(cooloff_time)s.'
)

# ============================================================================
# SESSION SECURITY ENHANCEMENTS
# ============================================================================

# Session timeout (auto-logout after 1 hour of inactivity)
SESSION_COOKIE_AGE = 3600  # 1 hour in seconds
SESSION_SAVE_EVERY_REQUEST = True  # Extend session on every request
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Keep session if browser closes

# Additional session security
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to session cookie
SESSION_COOKIE_SECURE = not DEBUG  # HTTPS only in production
SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection

# ============================================================================
# PASSWORD STRENGTH REQUIREMENTS (Enhanced)
# ============================================================================

# Already defined above but adding comment for clarity
# Passwords must be:
# - At least 8 characters
# - Not too similar to other personal info
# - Not a commonly used password
# - Not entirely numeric
# - Must contain mix of characters (via CommonPasswordValidator)

