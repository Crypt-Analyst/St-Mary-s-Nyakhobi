#!/usr/bin/env python
"""
Script to update St. Mary's Nyakhobi School information with official details from document
"""
import os
import sys
import django

# Add the project directory to the Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_dir)

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'st_marys_school.settings')
django.setup()

from home.models import SchoolInfo

def update_school_information():
    """Update school information with official details"""
    print("🏫 Updating St. Mary's Nyakhobi School Information...")
    
    # Get or create school info
    school_info, created = SchoolInfo.objects.get_or_create(
        id=1,
        defaults={
            'name': "St. Mary's Nyakhobi Senior School",
            'tagline': "Sacrifice for Success",
            'welcome_message': "St. Mary's Nyakhobi Senior School (formerly Nyakhobi Secondary School) is located in Nyakhobi Sub-location, Namboboto Location, Samia Sub-County, Busia County, Kenya. The school is sponsored by ACK Church Nambale Diocese and started in 1983 with 6 students.",
            'mission_statement': "To consistently provide quality secondary education.",
            'vision_statement': "To be an institution of excellence in pursuit of quality and holistic education.",
            'established_year': 1983,
            'phone': "+254 719 831 346",
            'email': "nyakhobisecsch@gmail.com",
            'address': "P.O. Box 254-50406, Funyula, Nyakhobi Sub-location, Namboboto Location, Samia Sub-County, Busia County, Kenya"
        }
    )
    
    if not created:
        # Update existing record
        school_info.name = "St. Mary's Nyakhobi Senior School"
        school_info.tagline = "Sacrifice for Success"
        school_info.welcome_message = "St. Mary's Nyakhobi Senior School (formerly Nyakhobi Secondary School) is located in Nyakhobi Sub-location, Namboboto Location, Samia Sub-County, Busia County, Kenya. The school is sponsored by ACK Church Nambale Diocese and started in 1983 with 6 students."
        school_info.mission_statement = "To consistently provide quality secondary education."
        school_info.vision_statement = "To be an institution of excellence in pursuit of quality and holistic education."
        school_info.established_year = 1983
        school_info.phone = "+254 719 831 346"
        school_info.email = "nyakhobisecsch@gmail.com"
        school_info.address = "P.O. Box 254-50406, Funyula, Nyakhobi Sub-location, Namboboto Location, Samia Sub-County, Busia County, Kenya"
        school_info.save()
        print("✅ Updated existing school information")
    else:
        print("✅ Created new school information")
    
    print(f"📋 School Name: {school_info.name}")
    print(f"📅 Established: {school_info.established_year}")
    print(f"📞 Phone: {school_info.phone}")
    print(f"📧 Email: {school_info.email}")
    print(f"📍 Address: {school_info.address}")
    print(f"🎯 Motto: {school_info.tagline}")
    
    print("\n🎉 School information updated successfully!")

if __name__ == '__main__':
    update_school_information()