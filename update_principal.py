#!/usr/bin/env python
import os
import sys
import django

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'st_marys_school.settings')
    django.setup()
    
    from faculty.models import Faculty
    
    try:
        # Find and update the principal record
        principal = Faculty.objects.filter(position='principal').first()
        if principal:
            principal.first_name = "Dan"
            principal.last_name = "F. Olopi"
            principal.save()
            print(f"✅ Updated principal name to: {principal.full_name}")
        else:
            # Create the principal record if it doesn't exist
            principal = Faculty.objects.create(
                first_name="Dan",
                last_name="F. Olopi",
                position="principal",
                bio="Principal of St. Mary's Nyakhobi Senior School",
                is_active=True
            )
            print(f"✅ Created principal record: {principal.full_name}")
            
    except Exception as e:
        print(f"❌ Error: {e}")