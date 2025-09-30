#!/usr/bin/env python
"""
Script to populate St. Mary's Nyakhobi School news system with sample data
"""
import os
import sys
import django
from datetime import datetime, date, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'st_marys_school.settings')
django.setup()

from news.models import NewsCategory, NewsArticle, Newsletter, NewsSettings
from django.contrib.auth.models import User

def create_news_categories():
    """Create news categories"""
    print("📁 Creating news categories...")
    
    categories_data = [
        {
            'name': 'School Announcements',
            'slug': 'school-announcements',
            'description': 'Official announcements and important notices from school administration',
            'category_type': 'announcement',
            'color': '#dc3545',
            'icon': 'fas fa-bullhorn',
            'order': 1
        },
        {
            'name': 'Student Achievements',
            'slug': 'student-achievements',
            'description': 'Celebrating our students\' academic, sports, and extracurricular successes',
            'category_type': 'achievement',
            'color': '#ffc107',
            'icon': 'fas fa-trophy',
            'order': 2
        },
        {
            'name': 'Upcoming Events',
            'slug': 'upcoming-events',
            'description': 'Information about upcoming school events, competitions, and activities',
            'category_type': 'event',
            'color': '#17a2b8',
            'icon': 'fas fa-calendar-check',
            'order': 3
        },
        {
            'name': 'Academic News',
            'slug': 'academic-news',
            'description': 'Updates on curriculum, examinations, and academic programs',
            'category_type': 'academic',
            'color': '#28a745',
            'icon': 'fas fa-graduation-cap',
            'order': 4
        },
        {
            'name': 'Sports & Games',
            'slug': 'sports-games',
            'description': 'Sports competitions, results, and athletic achievements',
            'category_type': 'sports',
            'color': '#fd7e14',
            'icon': 'fas fa-medal',
            'order': 5
        },
        {
            'name': 'Community News',
            'slug': 'community-news',
            'description': 'Community outreach programs and partnerships',
            'category_type': 'community',
            'color': '#6f42c1',
            'icon': 'fas fa-hands-helping',
            'order': 6
        }
    ]
    
    for category_data in categories_data:
        category, created = NewsCategory.objects.get_or_create(
            slug=category_data['slug'],
            defaults=category_data
        )
        if created:
            print(f"   ✅ Created category: {category.name}")
        else:
            print(f"   ℹ️  Category already exists: {category.name}")

def create_news_articles():
    """Create sample news articles"""
    print("📰 Creating sample news articles...")
    
    # Get admin user
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        admin_user = User.objects.create_user(
            username='admin',
            email='admin@stmarysnyakhobi.ac.ke',
            password='admin123',
            is_superuser=True,
            is_staff=True
        )
    
    # Get categories
    categories = {cat.slug: cat for cat in NewsCategory.objects.all()}
    
    articles_data = [
        {
            'title': 'KCSE 2024 Results: Outstanding Performance by Our Students',
            'subtitle': 'St. Mary\'s Nyakhobi achieves 98% pass rate with remarkable improvements across all subjects',
            'content': '''<p>We are thrilled to announce that St. Mary's Nyakhobi Senior School has achieved exceptional results in the 2024 KCSE examinations, with a pass rate of 98% and significant improvements across all subject areas.</p>

<h3>Key Highlights:</h3>
<ul>
<li><strong>Mean Grade Improvement:</strong> Our school mean grade improved from 6.2 to 7.1, representing a significant leap in academic performance</li>
<li><strong>University Qualifications:</strong> 85% of our students qualified for direct university admission</li>
<li><strong>Subject Excellence:</strong> Outstanding performance in Mathematics (mean grade B+), English (mean grade B), and Sciences</li>
<li><strong>Top Performers:</strong> 15 students achieved mean grades of A and A-, with our top student achieving a mean grade of A (84 points)</li>
</ul>

<h3>Principal's Message</h3>
<p>"These results are a testament to the dedication of our students, the commitment of our teaching staff, and the support of parents and the community. We are particularly proud of the improvement shown by students who joined us with lower entry grades but have excelled through hard work and determination."</p>

<p>The school's success can be attributed to our comprehensive approach to education, including:</p>
<ul>
<li>Small class sizes allowing for individualized attention</li>
<li>Regular assessment and remedial programs</li>
<li>Strong emphasis on discipline and character development</li>
<li>Modern teaching methods and resources</li>
<li>Supportive learning environment</li>
</ul>

<p>We congratulate all our students and look forward to their continued success in their future endeavors.</p>''',
            'category': categories['student-achievements'],
            'tags': 'KCSE, results, academic excellence, university admission',
            'is_published': True,
            'is_featured': True,
            'priority': 'high',
            'published_date': datetime.now() - timedelta(days=2)
        },
        {
            'title': 'New Science Laboratory Complex Officially Opens',
            'subtitle': 'State-of-the-art facilities to enhance STEM education and practical learning',
            'content': '''<p>St. Mary's Nyakhobi Senior School proudly inaugurated its new Science Laboratory Complex, a milestone achievement that will significantly enhance our science education program and prepare students for the challenges of the 21st century.</p>

<h3>Facility Features:</h3>
<ul>
<li><strong>Three Modern Laboratories:</strong> Separate, fully-equipped labs for Biology, Chemistry, and Physics</li>
<li><strong>Advanced Equipment:</strong> Digital microscopes, spectrophotometers, and modern analytical instruments</li>
<li><strong>Safety Features:</strong> Emergency systems, fume hoods, and safety equipment meeting international standards</li>
<li><strong>Capacity:</strong> Each lab can accommodate 40 students comfortably</li>
</ul>

<h3>Impact on Learning</h3>
<p>The new laboratories will enable our students to:</p>
<ul>
<li>Conduct advanced practical experiments</li>
<li>Develop hands-on research skills</li>
<li>Better prepare for KCSE practical examinations</li>
<li>Pursue STEM careers with confidence</li>
</ul>

<p>The project was completed with support from the school management, Parents' Association, and generous donors from the community. We extend our gratitude to all who made this dream a reality.</p>

<h3>Official Opening</h3>
<p>The complex was officially opened by the County Director of Education, who commended the school's commitment to providing quality education and modern learning facilities.</p>''',
            'category': categories['school-announcements'],
            'tags': 'science laboratory, STEM education, facilities, infrastructure',
            'is_published': True,
            'is_featured': True,
            'priority': 'high',
            'published_date': datetime.now() - timedelta(days=5)
        },
        {
            'title': 'Inter-School Mathematics Competition Success',
            'subtitle': 'Our team secures second position in the regional mathematics olympiad',
            'content': '''<p>St. Mary's Nyakhobi Senior School's mathematics team has brought honor to our institution by securing second position in the Regional Mathematics Olympiad held at Busia County Headquarters last weekend.</p>

<h3>Competition Details</h3>
<p>The competition featured 24 schools from across Busia County, with participants tackling challenging problems in:</p>
<ul>
<li>Algebra and Number Theory</li>
<li>Geometry and Trigonometry</li>
<li>Calculus and Statistics</li>
<li>Problem Solving and Logic</li>
</ul>

<h3>Our Team Performance</h3>
<p>Our team consisted of four Form 3 and Form 4 students who demonstrated exceptional mathematical skills:</p>
<ul>
<li><strong>Jane Wanjiku (Form 4A):</strong> Individual third place overall</li>
<li><strong>Peter Ochieng (Form 4B):</strong> Excellence in Geometry</li>
<li><strong>Mary Akinyi (Form 3A):</strong> Outstanding in Algebra</li>
<li><strong>David Mwangi (Form 3B):</strong> Problem-solving champion</li>
</ul>

<h3>Preparation and Training</h3>
<p>The team's success is the result of months of dedicated preparation under the guidance of our Mathematics Department. Special training sessions were held every Saturday, focusing on advanced problem-solving techniques and competition strategies.</p>

<p>Congratulations to our team and their coaches for this outstanding achievement!</p>''',
            'category': categories['student-achievements'],
            'tags': 'mathematics competition, academic achievement, regional competition',
            'is_published': True,
            'is_featured': False,
            'priority': 'normal',
            'published_date': datetime.now() - timedelta(days=8)
        },
        {
            'title': 'Annual Cultural Week 2025: Celebrating Diversity',
            'subtitle': 'Join us for a week-long celebration of Kenyan culture and heritage',
            'content': '''<p>St. Mary's Nyakhobi Senior School invites the entire school community and visitors to participate in our Annual Cultural Week 2025, scheduled for March 10-14, 2025.</p>

<h3>Week Schedule</h3>
<ul>
<li><strong>Monday, March 10:</strong> Traditional Dress Day and Cultural Exhibition</li>
<li><strong>Tuesday, March 11:</strong> Traditional Music and Dance Performances</li>
<li><strong>Wednesday, March 12:</strong> Cultural Food Festival</li>
<li><strong>Thursday, March 13:</strong> Art and Craft Exhibition</li>
<li><strong>Friday, March 14:</strong> Grand Cultural Show and Prize Giving</li>
</ul>

<h3>Participation Opportunities</h3>
<p>Students can participate in various activities:</p>
<ul>
<li>Traditional dance competitions</li>
<li>Poetry and storytelling in local languages</li>
<li>Art and craft exhibitions</li>
<li>Traditional cooking demonstrations</li>
<li>Cultural research presentations</li>
</ul>

<h3>Community Involvement</h3>
<p>We encourage parents and community members to participate by:</p>
<ul>
<li>Sharing cultural knowledge and stories</li>
<li>Providing traditional artifacts for display</li>
<li>Volunteering in organizing activities</li>
<li>Attending the grand cultural show</li>
</ul>

<p>This celebration aims to promote cultural awareness, preserve our heritage, and foster unity among our diverse school community.</p>''',
            'category': categories['upcoming-events'],
            'tags': 'cultural week, heritage, community event, diversity',
            'is_published': True,
            'is_featured': True,
            'priority': 'normal',
            'published_date': datetime.now() - timedelta(days=3)
        },
        {
            'title': 'New Academic Year Registration Guidelines',
            'subtitle': 'Important information for Form 1 admissions and continuing students',
            'content': '''<p>As we prepare for the 2025 academic year, St. Mary's Nyakhobi Senior School provides the following registration guidelines for new and continuing students.</p>

<h3>Form 1 Admissions (New Students)</h3>
<p><strong>Registration Period:</strong> January 15 - February 5, 2025</p>
<p><strong>Requirements:</strong></p>
<ul>
<li>KCPE certificate and result slip</li>
<li>Birth certificate</li>
<li>Primary school leaving certificate</li>
<li>Recent passport-size photographs (4 copies)</li>
<li>Medical certificate from a licensed medical practitioner</li>
</ul>

<h3>Continuing Students (Forms 2, 3, and 4)</h3>
<p><strong>Registration Period:</strong> January 20 - February 10, 2025</p>
<p><strong>Requirements:</strong></p>
<ul>
<li>Previous year's report form</li>
<li>School fees payment confirmation</li>
<li>Updated medical certificate</li>
</ul>

<h3>Fee Structure 2025</h3>
<ul>
<li><strong>Tuition:</strong> Ksh 25,000 per term</li>
<li><strong>Development Fund:</strong> Ksh 5,000 (annual)</li>
<li><strong>Activity Fee:</strong> Ksh 2,000 per term</li>
<li><strong>Examination Fee:</strong> Ksh 1,500 per term</li>
</ul>

<h3>Payment Methods</h3>
<p>Fees can be paid through:</p>
<ul>
<li>Bank deposit to our school account</li>
<li>M-Pesa Pay Bill Number: 522533</li>
<li>Direct payment at the school bursar's office</li>
</ul>

<p>For more information, contact the school office at +254 722 231798 or visit during office hours.</p>''',
            'category': categories['school-announcements'],
            'tags': 'registration, admissions, fees, academic year',
            'is_published': True,
            'is_featured': False,
            'priority': 'urgent',
            'published_date': datetime.now() - timedelta(days=1)
        }
    ]
    
    for article_data in articles_data:
        article_data['author'] = admin_user
        article, created = NewsArticle.objects.get_or_create(
            title=article_data['title'],
            defaults=article_data
        )
        if created:
            print(f"   ✅ Created article: {article.title}")
        else:
            print(f"   ℹ️  Article already exists: {article.title}")

def create_newsletters():
    """Create sample newsletters"""
    print("📑 Creating sample newsletters...")
    
    admin_user = User.objects.filter(is_superuser=True).first()
    
    newsletters_data = [
        {
            'title': 'Nyakhobi Times',
            'description': 'Monthly newsletter featuring school news, achievements, and upcoming events',
            'volume': 2024,
            'issue': 12,
            'publication_date': date(2024, 12, 1),
            'is_published': True,
            'is_featured': True
        },
        {
            'title': 'Nyakhobi Times',
            'description': 'November edition highlighting KCSE preparations and cultural activities',
            'volume': 2024,
            'issue': 11,
            'publication_date': date(2024, 11, 1),
            'is_published': True,
            'is_featured': False
        }
    ]
    
    for newsletter_data in newsletters_data:
        newsletter_data['created_by'] = admin_user
        newsletter, created = Newsletter.objects.get_or_create(
            volume=newsletter_data['volume'],
            issue=newsletter_data['issue'],
            defaults=newsletter_data
        )
        if created:
            print(f"   ✅ Created newsletter: {newsletter.title} Vol.{newsletter.volume} Issue {newsletter.issue}")
        else:
            print(f"   ℹ️  Newsletter already exists: {newsletter.title} Vol.{newsletter.volume} Issue {newsletter.issue}")

def create_news_settings():
    """Create news system settings"""
    print("⚙️ Creating news settings...")
    
    settings, created = NewsSettings.objects.get_or_create(
        pk=1,
        defaults={
            'articles_per_page': 10,
            'allow_comments': True,
            'moderate_comments': True,
            'show_author_info': True,
            'enable_social_sharing': True,
            'newsletter_signup_enabled': True,
            'site_name': "St. Mary's Nyakhobi School News",
            'default_meta_description': "Latest news, announcements, and updates from St. Mary's Nyakhobi School in Funyula, Busia County"
        }
    )
    
    if created:
        print(f"   ✅ News settings created")
    else:
        print(f"   ℹ️  News settings already exist")

def main():
    """Main function to populate news system"""
    print("📰 POPULATING ST. MARY'S NYAKHOBI SCHOOL NEWS SYSTEM")
    print("=" * 60)
    
    try:
        create_news_categories()
        create_news_articles()
        create_newsletters()
        create_news_settings()
        
        print("\n" + "=" * 60)
        print("✅ NEWS SYSTEM POPULATION COMPLETED SUCCESSFULLY!")
        print("\n📊 News Statistics:")
        print(f"   📁 Categories: {NewsCategory.objects.count()}")
        print(f"   📰 Articles: {NewsArticle.objects.count()}")
        print(f"   ⭐ Featured Articles: {NewsArticle.objects.filter(is_featured=True).count()}")
        print(f"   📅 Published Articles: {NewsArticle.objects.filter(is_published=True).count()}")
        print(f"   📑 Newsletters: {Newsletter.objects.count()}")
        
        print("\n🌐 Next Steps:")
        print("   1. Access news at: http://127.0.0.1:8000/news/")
        print("   2. Manage articles via admin: http://127.0.0.1:8000/admin/news/")
        print("   3. Add news navigation to main menu")
        print("   4. Upload featured images for articles")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)