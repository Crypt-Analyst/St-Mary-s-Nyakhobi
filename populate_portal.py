#!/usr/bin/env python3
"""
Population script for St. Mary's Nyakhobi School Portal System
This script creates sample data for testing the student portal functionality
"""

import os
import sys
import django
from datetime import datetime, timedelta, date
from decimal import Decimal
import random

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'st_marys_school.settings')
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from portal.models import (
    AcademicYear, Class, Subject, ClassSubject, UserProfile, Teacher, Student,
    Parent, Term, Assignment, AssignmentSubmission, Grade, Attendance,
    ProgressReport, Communication, PortalSettings
)

def create_academic_year():
    """Create current academic year"""
    print("Creating academic year...")
    academic_year, created = AcademicYear.objects.get_or_create(
        name="2024-2025",
        defaults={
            'start_date': date(2024, 1, 1),
            'end_date': date(2024, 12, 31),
            'is_current': True
        }
    )
    if created:
        print(f"✓ Created academic year: {academic_year.name}")
    else:
        print(f"✓ Academic year already exists: {academic_year.name}")
    return academic_year

def create_terms(academic_year):
    """Create terms for the academic year"""
    print("Creating terms...")
    terms_data = [
        {
            'term_number': 1,
            'name': 'Term 1 - 2024',
            'start_date': date(2024, 1, 15),
            'end_date': date(2024, 4, 5),
            'is_current': True
        },
        {
            'term_number': 2,
            'name': 'Term 2 - 2024',
            'start_date': date(2024, 5, 6),
            'end_date': date(2024, 8, 9),
            'is_current': False
        },
        {
            'term_number': 3,
            'name': 'Term 3 - 2024',
            'start_date': date(2024, 9, 2),
            'end_date': date(2024, 11, 22),
            'is_current': False
        }
    ]
    
    terms = []
    for term_data in terms_data:
        term, created = Term.objects.get_or_create(
            academic_year=academic_year,
            term_number=term_data['term_number'],
            defaults=term_data
        )
        if created:
            print(f"✓ Created term: {term.name}")
        else:
            print(f"✓ Term already exists: {term.name}")
        terms.append(term)
    
    return terms

def create_subjects():
    """Create subjects"""
    print("Creating subjects...")
    subjects_data = [
        # Primary subjects
        ('Mathematics', 'MATH', True),
        ('English', 'ENG', True),
        ('Kiswahili', 'KIS', True),
        ('Science', 'SCI', True),
        ('Social Studies', 'SST', True),
        ('Christian Religious Education', 'CRE', True),
        
        # Secondary subjects
        ('Biology', 'BIO', True),
        ('Chemistry', 'CHEM', True),
        ('Physics', 'PHY', True),
        ('History', 'HIST', True),
        ('Geography', 'GEO', True),
        ('Computer Studies', 'COMP', False),
        ('Agriculture', 'AGR', False),
        ('Home Science', 'HS', False),
        ('Art and Design', 'ART', False),
        ('Music', 'MUS', False),
        ('Physical Education', 'PE', False),
    ]
    
    subjects = []
    for name, code, is_core in subjects_data:
        subject, created = Subject.objects.get_or_create(
            name=name,
            defaults={
                'code': code,
                'is_core': is_core,
                'description': f'{name} curriculum for St. Mary\'s Nyakhobi School'
            }
        )
        if created:
            print(f"✓ Created subject: {subject.name} ({subject.code})")
        else:
            print(f"✓ Subject already exists: {subject.name}")
        subjects.append(subject)
    
    return subjects

def create_classes(academic_year):
    """Create classes"""
    print("Creating classes...")
    classes_data = [
        ('PP1', 'Pre-Primary 1', 1),
        ('PP2', 'Pre-Primary 2', 2),
        ('Grade1', 'Grade 1', 3),
        ('Grade2', 'Grade 2', 4),
        ('Grade3', 'Grade 3', 5),
        ('Grade4', 'Grade 4', 6),
        ('Grade5', 'Grade 5', 7),
        ('Grade6', 'Grade 6', 8),
        ('Grade7', 'Grade 7', 9),
        ('Grade8', 'Grade 8', 10),
        ('Form1', 'Form 1', 11),
        ('Form2', 'Form 2', 12),
        ('Form3', 'Form 3', 13),
        ('Form4', 'Form 4', 14),
    ]
    
    classes = []
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
            print(f"✓ Created class: {class_obj.display_name}")
        else:
            print(f"✓ Class already exists: {class_obj.display_name}")
        classes.append(class_obj)
    
    return classes

def create_users_and_profiles():
    """Create users and their profiles"""
    print("Creating users and profiles...")
    
    # Create admin user
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
        admin_user.set_password('admin123')
        admin_user.save()
        print("✓ Created admin user")
    
    # Create admin profile
    admin_profile, created = UserProfile.objects.get_or_create(
        user=admin_user,
        defaults={
            'user_type': 'admin',
            'phone': '+254700000000',
            'address': 'St. Mary\'s Nyakhobi School'
        }
    )
    if created:
        print("✓ Created admin profile")
    
    # Create teachers
    teachers_data = [
        ('john.doe', 'John', 'Doe', 'john.doe@stmarysnyakhobi.ac.ke', '+254700000001'),
        ('mary.smith', 'Mary', 'Smith', 'mary.smith@stmarysnyakhobi.ac.ke', '+254700000002'),
        ('peter.king', 'Peter', 'King', 'peter.king@stmarysnyakhobi.ac.ke', '+254700000003'),
        ('grace.wanjiku', 'Grace', 'Wanjiku', 'grace.wanjiku@stmarysnyakhobi.ac.ke', '+254700000004'),
        ('james.mwangi', 'James', 'Mwangi', 'james.mwangi@stmarysnyakhobi.ac.ke', '+254700000005'),
    ]
    
    teachers = []
    for username, first_name, last_name, email, phone in teachers_data:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'email': email
            }
        )
        if created:
            user.set_password('teacher123')
            user.save()
        
        profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'user_type': 'teacher',
                'phone': phone,
                'address': f'{first_name}\'s Address, Nyakhobi',
                'date_of_birth': date(1980 + random.randint(0, 15), random.randint(1, 12), random.randint(1, 28))
            }
        )
        
        teacher, created = Teacher.objects.get_or_create(
            profile=profile,
            defaults={
                'employee_id': f'TCH{1000 + len(teachers)}',
                'employment_status': 'permanent',
                'hire_date': date(2015 + random.randint(0, 8), random.randint(1, 12), random.randint(1, 28)),
                'qualifications': 'Bachelor of Education, Diploma in Teaching',
                'salary': Decimal('50000.00')
            }
        )
        if created:
            print(f"✓ Created teacher: {teacher.full_name}")
        
        teachers.append(teacher)
    
    # Create parents
    parents_data = [
        ('parent1', 'David', 'Kamau', 'david.kamau@email.com', '+254700000010', 'father'),
        ('parent2', 'Sarah', 'Njeri', 'sarah.njeri@email.com', '+254700000011', 'mother'),
        ('parent3', 'Michael', 'Ochieng', 'michael.ochieng@email.com', '+254700000012', 'father'),
        ('parent4', 'Rose', 'Wanjiru', 'rose.wanjiru@email.com', '+254700000013', 'mother'),
        ('parent5', 'Joseph', 'Kiprotich', 'joseph.kiprotich@email.com', '+254700000014', 'guardian'),
    ]
    
    parents = []
    for username, first_name, last_name, email, phone, relationship in parents_data:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'email': email
            }
        )
        if created:
            user.set_password('parent123')
            user.save()
        
        profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'user_type': 'parent',
                'phone': phone,
                'address': f'{first_name}\'s Home, Nyakhobi Area',
                'date_of_birth': date(1970 + random.randint(0, 20), random.randint(1, 12), random.randint(1, 28))
            }
        )
        
        parent, created = Parent.objects.get_or_create(
            profile=profile,
            defaults={
                'relationship': relationship,
                'occupation': random.choice(['Teacher', 'Business', 'Farmer', 'Doctor', 'Engineer']),
                'workplace': f'{first_name}\'s Workplace',
                'national_id': f'{random.randint(20000000, 39999999)}'
            }
        )
        if created:
            print(f"✓ Created parent: {parent.full_name}")
        
        parents.append(parent)
    
    # Create students
    students_data = [
        ('student1', 'Alice', 'Kamau', 'alice.kamau@student.com', 'F', 'Grade4'),
        ('student2', 'Brian', 'Njeri', 'brian.njeri@student.com', 'M', 'Grade5'),
        ('student3', 'Christine', 'Ochieng', 'christine.ochieng@student.com', 'F', 'Grade6'),
        ('student4', 'Daniel', 'Wanjiru', 'daniel.wanjiru@student.com', 'M', 'Form1'),
        ('student5', 'Elizabeth', 'Kiprotich', 'elizabeth.kiprotich@student.com', 'F', 'Form2'),
        ('student6', 'Felix', 'Mwangi', 'felix.mwangi@student.com', 'M', 'Grade3'),
        ('student7', 'Grace', 'Akinyi', 'grace.akinyi@student.com', 'F', 'Grade7'),
        ('student8', 'Henry', 'Rotich', 'henry.rotich@student.com', 'M', 'Form3'),
    ]
    
    students = []
    classes = list(Class.objects.all())
    for i, (username, first_name, last_name, email, gender, class_name) in enumerate(students_data):
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'email': email
            }
        )
        if created:
            user.set_password('student123')
            user.save()
        
        profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'user_type': 'student',
                'phone': f'+2547000000{20 + i}',
                'address': f'{first_name}\'s Home Address',
                'date_of_birth': date(2010 + random.randint(0, 8), random.randint(1, 12), random.randint(1, 28))
            }
        )
        
        # Find the class
        try:
            current_class = Class.objects.get(name=class_name)
        except Class.DoesNotExist:
            current_class = random.choice(classes)
        
        student, created = Student.objects.get_or_create(
            profile=profile,
            defaults={
                'admission_number': f'STD{2024}{1000 + i}',
                'current_class': current_class,
                'gender': gender,
                'admission_date': date(2020 + random.randint(0, 3), random.randint(1, 12), random.randint(1, 28)),
                'parent_guardian': parents[i % len(parents)] if i < len(parents) else None
            }
        )
        if created:
            print(f"✓ Created student: {student.full_name} - {student.admission_number}")
        
        # Add student to parent's children
        if student.parent_guardian:
            student.parent_guardian.children.add(student)
        
        students.append(student)
    
    return teachers, parents, students

def assign_subjects_to_teachers(teachers, subjects):
    """Assign subjects to teachers"""
    print("Assigning subjects to teachers...")
    for teacher in teachers:
        # Assign 2-3 random subjects to each teacher
        teacher_subjects = random.sample(subjects, random.randint(2, 3))
        teacher.subjects.set(teacher_subjects)
        print(f"✓ Assigned {len(teacher_subjects)} subjects to {teacher.full_name}")

def create_class_subjects(classes, subjects, teachers):
    """Create class-subject relationships"""
    print("Creating class-subject relationships...")
    for class_obj in classes:
        # Assign appropriate subjects based on class level
        if class_obj.level <= 8:  # Primary classes
            class_subjects = [s for s in subjects if s.code in ['MATH', 'ENG', 'KIS', 'SCI', 'SST', 'CRE']]
        else:  # Secondary classes
            class_subjects = subjects
        
        for subject in class_subjects:
            # Find a teacher who teaches this subject
            teacher = None
            for t in teachers:
                if subject in t.subjects.all():
                    teacher = t
                    break
            
            class_subject, created = ClassSubject.objects.get_or_create(
                class_obj=class_obj,
                subject=subject,
                defaults={
                    'teacher': teacher,
                    'lessons_per_week': random.randint(3, 6)
                }
            )
            if created:
                print(f"✓ Added {subject.name} to {class_obj.display_name}")

def create_assignments(teachers, classes, subjects):
    """Create sample assignments"""
    print("Creating assignments...")
    assignment_types = ['homework', 'project', 'quiz', 'test', 'exam']
    
    for teacher in teachers:
        teacher_classes = Class.objects.filter(
            class_subjects__teacher=teacher
        ).distinct()
        
        for class_obj in teacher_classes:
            for subject in teacher.subjects.filter(subject_classes__class_obj=class_obj):
                # Create 3-5 assignments per subject per class
                for i in range(random.randint(3, 5)):
                    assignment, created = Assignment.objects.get_or_create(
                        title=f"{subject.name} - Assignment {i + 1}",
                        class_obj=class_obj,
                        teacher=teacher,
                        subject=subject,
                        defaults={
                            'description': f'Complete the {subject.name} exercises and submit on time.',
                            'assignment_type': random.choice(assignment_types),
                            'due_date': timezone.now() + timedelta(days=random.randint(1, 30)),
                            'max_marks': random.choice([20, 30, 40, 50, 100]),
                            'instructions': f'Please complete all questions in your {subject.name} textbook pages 10-15.',
                            'status': 'published'
                        }
                    )
                    if created:
                        print(f"✓ Created assignment: {assignment.title}")

def create_sample_grades(students, subjects, terms):
    """Create sample grades for students"""
    print("Creating sample grades...")
    grade_types = ['assignment', 'test', 'exam', 'quiz', 'project']
    
    for student in students:
        if not student.current_class:
            continue
            
        # Get subjects for this student's class
        class_subjects = ClassSubject.objects.filter(class_obj=student.current_class)
        
        for class_subject in class_subjects:
            subject = class_subject.subject
            teacher = class_subject.teacher
            
            if not teacher:
                continue
            
            for term in terms:
                # Create 3-5 grades per subject per term
                for i in range(random.randint(3, 5)):
                    grade, created = Grade.objects.get_or_create(
                        student=student,
                        subject=subject,
                        term=term,
                        teacher=teacher,
                        grade_type=random.choice(grade_types),
                        title=f'{subject.name} {random.choice(grade_types).title()} {i + 1}',
                        defaults={
                            'marks_obtained': Decimal(str(random.randint(15, 95))),
                            'max_marks': Decimal('100'),
                            'weight': Decimal('1.0'),
                            'comments': random.choice([
                                'Good work!',
                                'Excellent performance',
                                'Needs improvement',
                                'Well done',
                                'Keep it up'
                            ]),
                            'date_recorded': term.start_date + timedelta(days=random.randint(1, 60))
                        }
                    )
                    if created and i == 0:  # Only print first grade for each subject/term
                        print(f"✓ Created grades for {student.full_name} - {subject.name}")

def create_attendance_records(students, terms):
    """Create attendance records"""
    print("Creating attendance records...")
    statuses = ['present', 'absent', 'late', 'excused']
    
    for student in students:
        for term in terms:
            # Create attendance for school days in the term
            current_date = term.start_date
            while current_date <= min(term.end_date, timezone.now().date()):
                # Skip weekends
                if current_date.weekday() < 5:  # Monday = 0, Friday = 4
                    status = random.choices(
                        statuses,
                        weights=[85, 5, 8, 2],  # Mostly present
                        k=1
                    )[0]
                    
                    attendance, created = Attendance.objects.get_or_create(
                        student=student,
                        date=current_date,
                        defaults={
                            'status': status,
                            'time_in': datetime.combine(current_date, timezone.now().time().replace(hour=8, minute=random.randint(0, 30))).time() if status in ['present', 'late'] else None,
                            'time_out': datetime.combine(current_date, timezone.now().time().replace(hour=15, minute=random.randint(0, 30))).time() if status in ['present', 'late'] else None,
                            'marked_by': None  # Would be assigned in real scenario
                        }
                    )
                
                current_date += timedelta(days=1)
    
    print(f"✓ Created attendance records for {len(students)} students")

def create_portal_settings():
    """Create portal settings"""
    print("Creating portal settings...")
    settings, created = PortalSettings.objects.get_or_create(
        id=1,
        defaults={
            'school_year_start_month': 1,
            'grading_scale': {
                'A': {'min': 90, 'max': 100},
                'B': {'min': 80, 'max': 89},
                'C': {'min': 70, 'max': 79},
                'D': {'min': 60, 'max': 69},
                'E': {'min': 0, 'max': 59}
            },
            'attendance_required': True,
            'parent_access_enabled': True,
            'assignment_submission_enabled': True,
            'communication_enabled': True,
            'report_generation_enabled': True
        }
    )
    if created:
        print("✓ Created portal settings")
    else:
        print("✓ Portal settings already exist")

def main():
    """Main function to populate the portal system"""
    print("🚀 Starting Portal System Population...")
    print("=" * 50)
    
    try:
        # Create academic structure
        academic_year = create_academic_year()
        terms = create_terms(academic_year)
        subjects = create_subjects()
        classes = create_classes(academic_year)
        
        # Create users and profiles
        teachers, parents, students = create_users_and_profiles()
        
        # Create relationships
        assign_subjects_to_teachers(teachers, subjects)
        create_class_subjects(classes, subjects, teachers)
        
        # Create academic data
        create_assignments(teachers, classes, subjects)
        create_sample_grades(students, subjects, terms)
        create_attendance_records(students, terms)
        
        # Create system settings
        create_portal_settings()
        
        print("\n" + "=" * 50)
        print("✅ Portal system populated successfully!")
        print("\nSample Login Credentials:")
        print("Admin: username='admin', password='admin123'")
        print("Teacher: username='john.doe', password='teacher123'")
        print("Parent: username='parent1', password='parent123'")
        print("Student: username='student1', password='student123'")
        print("\n🎓 Access the portal at: http://localhost:8000/portal/")
        
    except Exception as e:
        print(f"\n❌ Error populating portal system: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)