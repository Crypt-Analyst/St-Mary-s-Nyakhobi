#!/usr/bin/env python
"""
Script to populate St. Mary's Nyakhobi Senior School database with realistic data
"""
import os
import sys
import django
from datetime import datetime, date

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'st_marys_school.settings')
django.setup()

from home.models import SchoolInfo, HomePageSlider, QuickLink
from faculty.models import Department, Faculty
from events.models import Event
from academics.models import GradeLevel, Subject, AcademicProgram

def create_school_info():
    """Create basic school information"""
    print("📚 Creating school information...")
    
    school_info, created = SchoolInfo.objects.get_or_create(
        pk=1,
        defaults={
            'name': 'St. Mary\'s Nyakhobi Senior School',
            'tagline': 'Excellence Through Discipline - Building Leaders for Tomorrow',
            'welcome_message': 'St. Mary\'s Nyakhobi Senior School is a prestigious mixed secondary school located in Funyula, Busia County, Kenya. Established in 2010, we have consistently delivered quality education and produced graduates who excel in various fields including medicine, engineering, business, and education.',
            'mission_statement': 'To provide quality, affordable, and accessible education that prepares students for success in their academic pursuits and future careers while instilling strong moral values, discipline, and leadership skills that will enable them to be responsible citizens and leaders in their communities.',
            'vision_statement': 'To be a leading educational institution in Kenya, recognized for academic excellence, innovation, character development, and producing graduates who are competitive in the global market and contribute positively to society.',
            'established_year': 2010,
            'phone': '+254 712 345 678 / +254 723 456 789',
            'email': 'info@stmarysnyakhobi.ac.ke',
            'address': 'Off Nambuku/Funyula Road, Funyula, P.O. Box 123, Funyula 50406, Busia County, Kenya'
        }
    )
    
    if created:
        print("   ✅ School information created")
    else:
        print("   ℹ️  School information already exists")

def create_departments():
    """Create academic departments"""
    print("🏫 Creating departments...")
    
    departments_data = [
        {
            'name': 'Mathematics Department',
            'description': 'Mathematics, Statistics, Computer Studies, and Business Studies with emphasis on problem-solving, analytical thinking, and practical applications in real-world scenarios.',
            'head_of_department': 'Mr. Samuel Kimani'
        },
        {
            'name': 'Sciences Department',
            'description': 'Physics, Chemistry, Biology, and Agriculture with focus on practical laboratory work, scientific research methods, and environmental conservation.',
            'head_of_department': 'Mrs. Mary Wanjiku'
        },
        {
            'name': 'Languages Department',
            'description': 'English, Kiswahili, Literature, French, and German with emphasis on communication skills, creative expression, and cultural appreciation.',
            'head_of_department': 'Mrs. Esther Mutindi'
        },
        {
            'name': 'Humanities Department',
            'description': 'History, Geography, Christian Religious Education, Islamic Religious Education, Hindu Religious Education, and Social Studies focusing on critical thinking and cultural understanding.',
            'head_of_department': 'Mr. David Mwangi'
        },
        {
            'name': 'Creative Arts Department',
            'description': 'Music, Art and Design, Drama, Physical Education, and Life Skills education promoting creativity, physical fitness, and holistic development.',
            'head_of_department': 'Mrs. Grace Adhiambo'
        }
    ]
    
    for dept_data in departments_data:
        dept, created = Department.objects.get_or_create(
            name=dept_data['name'],
            defaults={
                'description': dept_data['description'],
                'head_of_department': dept_data['head_of_department']
            }
        )
        if created:
            print(f"   ✅ Created {dept_data['name']}")
        else:
            print(f"   ℹ️  {dept_data['name']} already exists")

def create_faculty():
    """Create faculty members"""
    print("👨‍🏫 Creating faculty members...")
    
    # Get departments
    math_dept = Department.objects.get(name='Mathematics Department')
    science_dept = Department.objects.get(name='Sciences Department')
    lang_dept = Department.objects.get(name='Languages Department')
    hum_dept = Department.objects.get(name='Humanities Department')
    arts_dept = Department.objects.get(name='Creative Arts Department')
    
    faculty_data = [
        # Leadership Team
        {
            'first_name': 'Peter', 'last_name': 'Wanyama', 'position': 'principal',
            'department': math_dept, 'email': 'principal@stmarysnyakhobi.ac.ke',
            'phone': '+254 712 345 678',
            'bio': 'With over 15 years of experience in educational leadership and mathematics education, Mr. Wanyama has transformed St. Mary\'s Nyakhobi into one of the leading secondary schools in Busia County. He holds a Master\'s degree in Educational Leadership and is passionate about academic excellence and character development.',
            'qualifications': 'M.Ed Educational Leadership (University of Nairobi), B.Ed Mathematics & Physics (Kenyatta University), Diploma in Education Management',
            'experience_years': 15, 'subjects_taught': 'Mathematics, Educational Leadership',
            'joined_date': date(2020, 1, 15)
        },
        {
            'first_name': 'Grace', 'last_name': 'Adhiambo', 'position': 'vice_principal',
            'department': arts_dept, 'email': 'deputy@stmarysnyakhobi.ac.ke',
            'phone': '+254 723 456 789',
            'bio': 'Mrs. Adhiambo oversees academic programs and student affairs with 12 years of dedicated service in education. She ensures high standards of teaching and learning while promoting holistic student development through arts and co-curricular activities.',
            'qualifications': 'M.A Education (Maseno University), B.Ed Art & Design (Kenyatta University), Diploma in Guidance & Counseling',
            'experience_years': 12, 'subjects_taught': 'Art & Design, Academic Coordination',
            'joined_date': date(2021, 2, 1)
        },
        {
            'first_name': 'James', 'last_name': 'Ochieng', 'position': 'vice_principal',
            'department': math_dept, 'email': 'admin@stmarysnyakhobi.ac.ke',
            'phone': '+254 734 567 890',
            'bio': 'Mr. Ochieng manages administrative affairs and financial operations ensuring smooth running of all school activities. With a background in business management, he brings efficiency and strategic planning to school operations.',
            'qualifications': 'MBA Management (Maseno University), B.Com Business Administration (Moi University), CPA (K)',
            'experience_years': 10, 'subjects_taught': 'Business Studies, Administration',
            'joined_date': date(2022, 1, 10)
        },
        
        # Department Heads & Teachers
        {
            'first_name': 'Samuel', 'last_name': 'Kimani', 'position': 'teacher',
            'department': math_dept, 'email': 's.kimani@stmarysnyakhobi.ac.ke',
            'phone': '+254 745 678 901',
            'bio': 'Head of Mathematics Department with 12 years of teaching experience. Mr. Kimani specializes in KCSE preparation and has consistently produced excellent results in mathematics. He has mentored numerous students who have excelled in engineering and actuarial sciences.',
            'qualifications': 'B.Ed Mathematics & Physics (Kenyatta University), Diploma in Computer Studies',
            'experience_years': 12, 'subjects_taught': 'Mathematics, Physics, Computer Studies',
            'joined_date': date(2018, 3, 15)
        },
        {
            'first_name': 'Mary', 'last_name': 'Wanjiku', 'position': 'teacher',
            'department': science_dept, 'email': 'm.wanjiku@stmarysnyakhobi.ac.ke',
            'phone': '+254 756 789 012',
            'bio': 'Head of Sciences Department with 10 years of experience in science education. Mrs. Wanjiku is an expert in laboratory management and has led several students to victory in national science competitions. She promotes practical learning and scientific research.',
            'qualifications': 'B.Sc Chemistry (University of Nairobi), PGDE (Kenyatta University), Certificate in Laboratory Management',
            'experience_years': 10, 'subjects_taught': 'Chemistry, Biology',
            'joined_date': date(2019, 1, 20)
        },
        {
            'first_name': 'Joseph', 'last_name': 'Ouma', 'position': 'teacher',
            'department': science_dept, 'email': 'j.ouma@stmarysnyakhobi.ac.ke',
            'phone': '+254 767 890 123',
            'bio': 'Dedicated Physics and Mathematics teacher with 8 years of experience. Known for making complex physics concepts easy to understand through practical demonstrations and real-world applications. He coordinates the school\'s science fair annually.',
            'qualifications': 'B.Ed Physics & Mathematics (Moi University), Diploma in Electronics',
            'experience_years': 8, 'subjects_taught': 'Physics, Mathematics',
            'joined_date': date(2020, 2, 15)
        },
        {
            'first_name': 'Esther', 'last_name': 'Mutindi', 'position': 'teacher',
            'department': lang_dept, 'email': 'e.mutindi@stmarysnyakhobi.ac.ke',
            'phone': '+254 778 901 234',
            'bio': 'Head of Languages Department with 15 years of experience in language education. Mrs. Mutindi is the drama club coordinator and debate coach who has led the school to several victories in inter-school competitions. She promotes reading culture and creative writing.',
            'qualifications': 'B.A English & Literature (University of Nairobi), PGDE (Kenyatta University), Certificate in Drama & Theatre Arts',
            'experience_years': 15, 'subjects_taught': 'English, Literature',
            'joined_date': date(2017, 1, 10)
        },
        {
            'first_name': 'Hassan', 'last_name': 'Mohamed', 'position': 'teacher',
            'department': lang_dept, 'email': 'h.mohamed@stmarysnyakhobi.ac.ke',
            'phone': '+254 789 012 345',
            'bio': 'Experienced Kiswahili teacher with 9 years of dedication to language and cultural education. Mr. Mohamed has authored several educational materials and promotes African cultural values through language teaching. He coordinates cultural events and traditional dance competitions.',
            'qualifications': 'B.A Kiswahili & Literature (Pwani University), Diploma in Education, Certificate in African Cultural Studies',
            'experience_years': 9, 'subjects_taught': 'Kiswahili, Literature',
            'joined_date': date(2018, 8, 20)
        },
        {
            'first_name': 'David', 'last_name': 'Mwangi', 'position': 'teacher',
            'department': hum_dept, 'email': 'd.mwangi@stmarysnyakhobi.ac.ke',
            'phone': '+254 790 123 456',
            'bio': 'Head of Humanities Department with 11 years of experience in social studies education. Mr. Mwangi specializes in African history and has conducted research on local historical sites. He promotes civic education and social responsibility among students.',
            'qualifications': 'B.A History & Government (University of Nairobi), PGDE (Kenyatta University), Diploma in Conflict Resolution',
            'experience_years': 11, 'subjects_taught': 'History, Geography, Government',
            'joined_date': date(2019, 3, 10)
        },
        {
            'first_name': 'Susan', 'last_name': 'Akinyi', 'position': 'teacher',
            'department': hum_dept, 'email': 's.akinyi@stmarysnyakhobi.ac.ke',
            'phone': '+254 701 234 567',
            'bio': 'Geography and Environmental Studies teacher with 7 years of experience. Mrs. Akinyi leads the school\'s environmental club and tree planting initiatives. She is passionate about environmental conservation and sustainable development education.',
            'qualifications': 'B.Ed Geography (Masinde Muliro University), Diploma in Environmental Studies, Certificate in Climate Change Education',
            'experience_years': 7, 'subjects_taught': 'Geography, Environmental Studies',
            'joined_date': date(2021, 1, 15)
        }
    ]
    
    for faculty_info in faculty_data:
        faculty, created = Faculty.objects.get_or_create(
            email=faculty_info['email'],
            defaults=faculty_info
        )
        if created:
            print(f"   ✅ Created faculty: {faculty_info['first_name']} {faculty_info['last_name']}")
        else:
            print(f"   ℹ️  Faculty already exists: {faculty_info['first_name']} {faculty_info['last_name']}")

def create_events():
    """Create school events"""
    print("📅 Creating school events...")
    
    events_data = [
        {
            'title': 'Inter-School Athletics Championship 2025',
            'description': 'Annual athletics competition featuring schools from Busia County. Track and field events for all age groups including 100m, 200m, 400m, 800m, 1500m, 5000m races, relay competitions, long jump, high jump, shot put, and discus throw. Expected participation from over 20 schools with awards for top performers.',
            'event_date': datetime(2025, 10, 15, 8, 0),
            'end_date': datetime(2025, 10, 15, 17, 0),
            'location': 'St. Mary\'s Nyakhobi Sports Grounds',
            'event_type': 'sports'
        },
        {
            'title': 'Annual Science Fair 2025',
            'description': 'Students showcase innovative science projects and experiments across various categories including Physics, Chemistry, Biology, Mathematics, Computer Science, and Environmental Science. Open to parents, guardians, and the local community. Awards will be given for outstanding projects in each category.',
            'event_date': datetime(2025, 10, 22, 9, 0),
            'end_date': datetime(2025, 10, 22, 16, 0),
            'location': 'Science Laboratories & Assembly Hall',
            'event_type': 'academic'
        },
        {
            'title': 'Drama and Cultural Festival',
            'description': 'Annual celebration of arts and creativity featuring original plays, poetry recitations, traditional dances, and musical performances. Students from all forms participate in showcasing talents in drama, music, dance, and storytelling representing various Kenyan cultures and traditions.',
            'event_date': datetime(2025, 11, 5, 18, 0),
            'end_date': datetime(2025, 11, 5, 21, 0),
            'location': 'School Assembly Hall',
            'event_type': 'cultural'
        },
        {
            'title': 'Form 4 KCSE Mock Examinations',
            'description': 'Comprehensive mock examinations for Form 4 students in preparation for the national KCSE exams. Covers all subjects with proper examination conditions, professional invigilation, and marking schemes following KNEC standards. Results will be used for final preparation strategies.',
            'event_date': datetime(2025, 11, 12, 8, 0),
            'end_date': datetime(2025, 11, 22, 17, 0),
            'location': 'All Examination Rooms',
            'event_type': 'exam'
        },
        {
            'title': 'Parents Day & Academic Exhibition',
            'description': 'Parents and guardians meet with teachers for academic progress discussions, view student exhibitions, and participate in school activities. Includes presentation of student work, departmental displays, academic progress reports, and feedback sessions with subject teachers.',
            'event_date': datetime(2025, 11, 18, 9, 0),
            'end_date': datetime(2025, 11, 18, 15, 0),
            'location': 'Entire School Campus',
            'event_type': 'meeting'
        },
        {
            'title': 'Annual Awards Day & Prize Giving Ceremony',
            'description': 'Recognition of outstanding academic performance, sports achievements, leadership excellence, and exemplary conduct. Presentation of trophies, certificates, scholarships, and bursaries to deserving students. Features guest speaker from the education sector and entertainment by school clubs.',
            'event_date': datetime(2025, 12, 1, 10, 0),
            'end_date': datetime(2025, 12, 1, 13, 0),
            'location': 'School Assembly Hall',
            'event_type': 'academic'
        }
    ]
    
    for event_data in events_data:
        event, created = Event.objects.get_or_create(
            title=event_data['title'],
            defaults=event_data
        )
        if created:
            print(f"   ✅ Created event: {event_data['title']}")
        else:
            print(f"   ℹ️  Event already exists: {event_data['title']}")

def create_homepage_content():
    """Create homepage sliders and quick links"""
    print("🏠 Creating homepage content...")
    
    # Create sliders
    sliders_data = [
        {
            'title': 'Welcome to St. Mary\'s Nyakhobi Senior School',
            'description': 'Excellence Through Discipline - Nurturing tomorrow\'s leaders today with quality education, strong moral values, and character development in a conducive learning environment.',
            'link_text': 'Learn More About Us',
            'link_url': '/about/',
            'order': 1
        },
        {
            'title': 'Academic Excellence Since 2010',
            'description': '95% University Admission Rate - Preparing students for success in higher education and future careers through comprehensive curriculum and dedicated teaching staff.',
            'link_text': 'View Our Programs',
            'link_url': '/academics/',
            'order': 2
        },
        {
            'title': 'Join Our Growing Community',
            'description': 'Applications now open for 2026 Academic Year - Scholarships and bursaries available for qualified students. Experience quality education in a nurturing environment.',
            'link_text': 'Apply Today',
            'link_url': '/admissions/',
            'order': 3
        }
    ]
    
    for slider_data in sliders_data:
        slider, created = HomePageSlider.objects.get_or_create(
            title=slider_data['title'],
            defaults=slider_data
        )
        if created:
            print(f"   ✅ Created slider: {slider_data['title']}")
        else:
            print(f"   ℹ️  Slider already exists: {slider_data['title']}")
    
    # Create quick links
    quicklinks_data = [
        {'title': 'Admissions', 'description': 'Apply for 2026 academic year', 'icon': 'fas fa-graduation-cap', 'link_url': '/admissions/', 'order': 1},
        {'title': 'Academic Programs', 'description': 'Form 1-4 curriculum details', 'icon': 'fas fa-book-open', 'link_url': '/academics/', 'order': 2},
        {'title': 'Our Faculty', 'description': 'Meet our dedicated educators', 'icon': 'fas fa-chalkboard-teacher', 'link_url': '/faculty/', 'order': 3},
        {'title': 'School Events', 'description': 'Upcoming activities and calendar', 'icon': 'fas fa-calendar-alt', 'link_url': '/events/', 'order': 4},
        {'title': 'Contact Us', 'description': 'Get in touch with our team', 'icon': 'fas fa-phone-alt', 'link_url': '/contact/', 'order': 5},
        {'title': 'School Library', 'description': 'Access learning resources', 'icon': 'fas fa-book', 'link_url': '/library/', 'order': 6}
    ]
    
    for link_data in quicklinks_data:
        quicklink, created = QuickLink.objects.get_or_create(
            title=link_data['title'],
            defaults=link_data
        )
        if created:
            print(f"   ✅ Created quick link: {link_data['title']}")
        else:
            print(f"   ℹ️  Quick link already exists: {link_data['title']}")

def create_academic_data():
    """Create grade levels, subjects, and academic programs"""
    print("📖 Creating academic data...")
    
    # Create Grade Levels
    grade_levels_data = [
        {'name': 'Form 1', 'description': 'Foundation year focusing on core subjects and study skills development', 'age_range': '14-15 years'},
        {'name': 'Form 2', 'description': 'Skills development year with expanded curriculum including computer studies', 'age_range': '15-16 years'},
        {'name': 'Form 3', 'description': 'Specialization year where students choose between Sciences and Arts streams', 'age_range': '16-17 years'},
        {'name': 'Form 4', 'description': 'KCSE preparation year with intensive revision and mock examinations', 'age_range': '17-18 years'}
    ]
    
    grade_levels = []
    for grade_data in grade_levels_data:
        grade, created = GradeLevel.objects.get_or_create(
            name=grade_data['name'],
            defaults=grade_data
        )
        grade_levels.append(grade)
        if created:
            print(f"   ✅ Created grade level: {grade_data['name']}")
        else:
            print(f"   ℹ️  Grade level already exists: {grade_data['name']}")
    
    # Create Subjects
    subjects_data = [
        {'name': 'Mathematics', 'description': 'Pure and applied mathematics, statistics, and problem-solving skills'},
        {'name': 'English', 'description': 'Language and literature, communication skills, and creative writing'},
        {'name': 'Kiswahili', 'description': 'National language, literature, and cultural studies'},
        {'name': 'Biology', 'description': 'Life sciences, human biology, and environmental studies'},
        {'name': 'Chemistry', 'description': 'Chemical processes, laboratory work, and scientific analysis'},
        {'name': 'Physics', 'description': 'Physical sciences, mechanics, and scientific principles'},
        {'name': 'History', 'description': 'World history, African history, and historical analysis'},
        {'name': 'Geography', 'description': 'Physical geography, human geography, and environmental studies'},
        {'name': 'Computer Studies', 'description': 'Computer literacy, programming basics, and digital skills'},
        {'name': 'Business Studies', 'description': 'Business principles, entrepreneurship, and economic concepts'},
        {'name': 'Agriculture', 'description': 'Crop production, animal husbandry, and sustainable farming'},
        {'name': 'Art & Design', 'description': 'Creative arts, design principles, and artistic expression'}
    ]
    
    subjects = []
    for subject_data in subjects_data:
        subject, created = Subject.objects.get_or_create(
            name=subject_data['name'],
            defaults=subject_data
        )
        subjects.append(subject)
        if created:
            print(f"   ✅ Created subject: {subject_data['name']}")
        else:
            print(f"   ℹ️  Subject already exists: {subject_data['name']}")

def main():
    """Main function to populate database"""
    print("🎯 Starting St. Mary's Nyakhobi database population...")
    print("=" * 60)
    
    try:
        create_school_info()
        create_departments()
        create_faculty()
        create_events()
        create_homepage_content()
        create_academic_data()
        
        print("=" * 60)
        print("🎉 Database population completed successfully!")
        print("✅ All school data has been created.")
        print("\n📊 Summary:")
        print(f"   • School Info: {SchoolInfo.objects.count()}")
        print(f"   • Departments: {Department.objects.count()}")
        print(f"   • Faculty: {Faculty.objects.count()}")
        print(f"   • Events: {Event.objects.count()}")
        print(f"   • Homepage Sliders: {HomePageSlider.objects.count()}")
        print(f"   • Quick Links: {QuickLink.objects.count()}")
        print(f"   • Grade Levels: {GradeLevel.objects.count()}")
        print(f"   • Subjects: {Subject.objects.count()}")
        
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()