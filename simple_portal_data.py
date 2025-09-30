#!/usr/bin/env python3
"""
Simple Portal Population Script for St. Mary's Nyakhobi School
"""

import os
import sys
import django
from datetime import date, timedelta
from decimal import Decimal

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'st_marys_school.settings')
django.setup()

from django.contrib.auth.models import User
from portal.models import (
    AcademicYear, Class, Subject, UserProfile, Teacher, Student,
    Parent, Term, PortalSettings
)

def main():
    """Create basic portal data"""
    print("🚀 Creating basic portal data...")
    
    # Create academic year
    academic_year, created = AcademicYear.objects.get_or_create(
        name="2024-2025",
        defaults={
            'start_date': date(2024, 1, 1),
            'end_date': date(2024, 12, 31),
            'is_current': True
        }
    )
    print(f"✓ Academic year: {academic_year.name}")
    
    # Create term
    term, created = Term.objects.get_or_create(
        academic_year=academic_year,
        term_number=1,
        defaults={
            'name': 'Term 1 - 2024',
            'start_date': date(2024, 1, 15),
            'end_date': date(2024, 4, 5),
            'is_current': True
        }
    )
    print(f"✓ Term: {term.name}")
    
    # Create subjects
    subjects_data = [
        ('Mathematics', 'MATH'),
        ('English', 'ENG'),
        ('Kiswahili', 'KIS'),
        ('Science', 'SCI'),
    ]
    
    for name, code in subjects_data:
        subject, created = Subject.objects.get_or_create(
            name=name,
            defaults={'code': code, 'is_core': True}
        )
        if created:
            print(f"✓ Subject: {subject.name}")
    
    # Create classes
    classes_data = [
        ('Grade4', 'Grade 4', 6),
        ('Grade5', 'Grade 5', 7),
        ('Form1', 'Form 1', 11),
    ]
    
    for name, display_name, level in classes_data:
        class_obj, created = Class.objects.get_or_create(
            name=name,
            academic_year=academic_year,
            defaults={
                'display_name': display_name,
                'level': level,
                'capacity': 40
            }
        )
        if created:
            print(f"✓ Class: {class_obj.display_name}")
    
    # Create simple users without complex password hashing
    # Admin user
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'first_name': 'System',
            'last_name': 'Administrator',
            'email': 'admin@stmarysnyakhobi.ac.ke',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin')
        admin_user.save()
        print("✓ Admin user created")
    
    # Admin profile
    admin_profile, created = UserProfile.objects.get_or_create(
        user=admin_user,
        defaults={
            'user_type': 'admin',
            'phone': '0719 831 346'
        }
    )
    
    # Teacher user
    teacher_user, created = User.objects.get_or_create(
        username='teacher',
        defaults={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'teacher@stmarysnyakhobi.ac.ke'
        }
    )
    if created:
        teacher_user.set_password('teacher')
        teacher_user.save()
        print("✓ Teacher user created")
    
    # Teacher profile
    teacher_profile, created = UserProfile.objects.get_or_create(
        user=teacher_user,
        defaults={
            'user_type': 'teacher',
            'phone': '0719 831 346'
        }
    )
    
    # Teacher record
    teacher, created = Teacher.objects.get_or_create(
        profile=teacher_profile,
        defaults={
            'employee_id': 'TCH001',
            'employment_status': 'permanent',
            'hire_date': date(2020, 1, 1),
            'qualifications': 'Bachelor of Education'
        }
    )
    if created:
        print("✓ Teacher record created")
    
    # Student user
    student_user, created = User.objects.get_or_create(
        username='student',
        defaults={
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'student@stmarysnyakhobi.ac.ke'
        }
    )
    if created:
        student_user.set_password('student')
        student_user.save()
        print("✓ Student user created")
    
    # Student profile
    student_profile, created = UserProfile.objects.get_or_create(
        user=student_user,
        defaults={
            'user_type': 'student',
            'phone': '0719 831 346'
        }
    )
    
    # Student record
    grade4_class = Class.objects.get(name='Grade4')
    student, created = Student.objects.get_or_create(
        profile=student_profile,
        defaults={
            'admission_number': 'STD001',
            'current_class': grade4_class,
            'gender': 'F',
            'admission_date': date(2022, 1, 1)
        }
    )
    if created:
        print("✓ Student record created")
    
    # Parent user
    parent_user, created = User.objects.get_or_create(
        username='parent',
        defaults={
            'first_name': 'Mary',
            'last_name': 'Smith',
            'email': 'parent@stmarysnyakhobi.ac.ke'
        }
    )
    if created:
        parent_user.set_password('parent')
        parent_user.save()
        print("✓ Parent user created")
    
    # Parent profile
    parent_profile, created = UserProfile.objects.get_or_create(
        user=parent_user,
        defaults={
            'user_type': 'parent',
            'phone': '0719 831 346'
        }
    )
    
    # Parent record
    parent, created = Parent.objects.get_or_create(
        profile=parent_profile,
        defaults={
            'relationship': 'mother',
            'occupation': 'Teacher'
        }
    )
    if created:
        parent.children.add(student)
        print("✓ Parent record created")
    
    # Portal settings
    settings, created = PortalSettings.objects.get_or_create(
        id=1,
        defaults={
            'attendance_required': True,
            'parent_access_enabled': True,
            'assignment_submission_enabled': True
        }
    )
    if created:
        print("✓ Portal settings created")
    
    print("\n✅ Basic portal data created successfully!")
    print("\nLogin Credentials:")
    print("Admin: username='admin', password='admin'")
    print("Teacher: username='teacher', password='teacher'")
    print("Student: username='student', password='student'")
    print("Parent: username='parent', password='parent'")
    print("\nAccess portal at: http://localhost:8000/portal/")

if __name__ == '__main__':
    main()