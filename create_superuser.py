#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'st_marys_school.settings')
django.setup()

from django.contrib.auth.models import User

# Create superuser
username = 'admin'
email = 'admin@stmarysnyakhobi.ac.ke'
password = 'admin123'

if User.objects.filter(username=username).exists():
    print(f"Superuser '{username}' already exists")
else:
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser '{username}' created successfully!")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"Email: {email}")