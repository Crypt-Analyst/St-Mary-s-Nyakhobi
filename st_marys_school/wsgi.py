"""
WSGI config for st_marys_school project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'st_marys_school.settings')

application = get_wsgi_application()