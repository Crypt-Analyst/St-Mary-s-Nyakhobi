#!/usr/bin/env python
"""
Script to populate St. Mary's Nyakhobi School gallery with sample data
"""
import os
import sys
import django
from datetime import datetime, date, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'st_marys_school.settings')
django.setup()

from gallery.models import GalleryCategory, PhotoAlbum, GallerySettings
from django.contrib.auth.models import User

def create_gallery_categories():
    """Create gallery categories"""
    print("📁 Creating gallery categories...")
    
    categories_data = [
        {
            'name': 'School Events',
            'slug': 'school-events',
            'description': 'Special events, ceremonies, and celebrations at our school',
            'icon': 'fas fa-calendar-alt'
        },
        {
            'name': 'Academic Activities',
            'slug': 'academic-activities', 
            'description': 'Classroom activities, science fairs, academic competitions',
            'icon': 'fas fa-graduation-cap'
        },
        {
            'name': 'Sports & Games',
            'slug': 'sports-games',
            'description': 'Athletic competitions, sports days, and physical education',
            'icon': 'fas fa-trophy'
        },
        {
            'name': 'Cultural Activities',
            'slug': 'cultural-activities',
            'description': 'Music, dance, drama, and cultural celebrations',
            'icon': 'fas fa-masks-theater'
        },
        {
            'name': 'Community Service',
            'slug': 'community-service',
            'description': 'Outreach programs and community engagement activities',
            'icon': 'fas fa-hands-helping'
        },
        {
            'name': 'School Infrastructure',
            'slug': 'school-infrastructure',
            'description': 'Campus buildings, facilities, and learning environments',
            'icon': 'fas fa-building'
        }
    ]
    
    for category_data in categories_data:
        category, created = GalleryCategory.objects.get_or_create(
            slug=category_data['slug'],
            defaults=category_data
        )
        if created:
            print(f"   ✅ Created category: {category.name}")
        else:
            print(f"   ℹ️  Category already exists: {category.name}")

def create_sample_albums():
    """Create sample photo albums"""
    print("📸 Creating sample photo albums...")
    
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
    categories = {cat.slug: cat for cat in GalleryCategory.objects.all()}
    
    albums_data = [
        {
            'title': 'KCSE Graduation Ceremony 2024',
            'slug': 'kcse-graduation-ceremony-2024',
            'description': 'Celebrating our Form 4 students as they complete their secondary education journey. A momentous day filled with pride, achievements, and new beginnings for the Class of 2024.',
            'category': categories['school-events'],
            'event_date': date(2024, 11, 15),
            'is_featured': True,
            'is_published': True
        },
        {
            'title': 'Annual Science Fair 2024',
            'slug': 'annual-science-fair-2024',
            'description': 'Students showcase innovative science projects and experiments. Our young scientists demonstrate creativity, research skills, and scientific thinking through impressive displays.',
            'category': categories['academic-activities'],
            'event_date': date(2024, 10, 20),
            'is_featured': True,
            'is_published': True
        },
        {
            'title': 'Inter-House Sports Competition',
            'slug': 'inter-house-sports-competition',
            'description': 'Annual athletics competition between school houses. Students compete in various track and field events, fostering teamwork, sportsmanship, and healthy competition.',
            'category': categories['sports-games'],
            'event_date': date(2024, 9, 28),
            'is_featured': False,
            'is_published': True
        },
        {
            'title': 'Cultural Day Celebration 2024',
            'slug': 'cultural-day-celebration-2024',
            'description': 'A vibrant celebration of Kenyan culture featuring traditional dances, music performances, poetry, and cultural displays from various ethnic communities.',
            'category': categories['cultural-activities'],
            'event_date': date(2024, 8, 12),
            'is_featured': True,
            'is_published': True
        },
        {
            'title': 'Tree Planting Initiative',
            'slug': 'tree-planting-initiative',
            'description': 'Students and staff participate in environmental conservation by planting indigenous trees around the school compound and in the local community.',
            'category': categories['community-service'],
            'event_date': date(2024, 7, 5),
            'is_featured': False,
            'is_published': True
        },
        {
            'title': 'New Classroom Block Opening',
            'slug': 'new-classroom-block-opening',
            'description': 'Official opening of our new modern classroom block, featuring improved learning spaces with better lighting, ventilation, and educational resources.',
            'category': categories['school-infrastructure'],
            'event_date': date(2024, 6, 10),
            'is_featured': False,
            'is_published': True
        },
        {
            'title': 'Mathematics Competition 2024',
            'slug': 'mathematics-competition-2024',
            'description': 'Regional mathematics competition hosted at our school, bringing together talented students from across Busia County to compete in mathematical challenges.',
            'category': categories['academic-activities'],
            'event_date': date(2024, 5, 18),
            'is_featured': False,
            'is_published': True
        },
        {
            'title': 'Drama Festival Performance',
            'slug': 'drama-festival-performance',
            'description': 'Our drama club\'s outstanding performance at the regional schools drama festival, showcasing theatrical talent and creative storytelling.',
            'category': categories['cultural-activities'],
            'event_date': date(2024, 4, 22),
            'is_featured': False,
            'is_published': True
        },
        {
            'title': 'Career Guidance Week 2024',
            'slug': 'career-guidance-week-2024',
            'description': 'Week-long career guidance sessions featuring guest speakers from various professions, university representatives, and career counseling for students.',
            'category': categories['academic-activities'],
            'event_date': date(2024, 3, 14),
            'is_featured': False,
            'is_published': True
        },
        {
            'title': 'Community Health Outreach',
            'slug': 'community-health-outreach',
            'description': 'Students participate in health education and awareness programs in partnership with local health facilities, promoting community wellness.',
            'category': categories['community-service'],
            'event_date': date(2024, 2, 8),
            'is_featured': False,
            'is_published': True
        }
    ]
    
    for album_data in albums_data:
        album_data['created_by'] = admin_user
        album, created = PhotoAlbum.objects.get_or_create(
            slug=album_data['slug'],
            defaults=album_data
        )
        if created:
            print(f"   ✅ Created album: {album.title}")
        else:
            print(f"   ℹ️  Album already exists: {album.title}")

def create_gallery_settings():
    """Create gallery settings"""
    print("⚙️ Creating gallery settings...")
    
    settings, created = GallerySettings.objects.get_or_create(
        pk=1,
        defaults={
            'photos_per_page': 12,
            'albums_per_page': 9,
            'allow_photo_download': False,
            'watermark_enabled': True,
            'watermark_text': 'St. Mary\'s Nyakhobi School',
            'max_photo_size_mb': 5,
            'thumbnail_quality': 85
        }
    )
    
    if created:
        print(f"   ✅ Gallery settings created")
    else:
        print(f"   ℹ️  Gallery settings already exist")

def main():
    """Main function to populate gallery"""
    print("🎨 POPULATING ST. MARY'S NYAKHOBI SCHOOL GALLERY")
    print("=" * 60)
    
    try:
        create_gallery_categories()
        create_sample_albums()
        create_gallery_settings()
        
        print("\n" + "=" * 60)
        print("✅ GALLERY POPULATION COMPLETED SUCCESSFULLY!")
        print("\n📊 Gallery Statistics:")
        print(f"   📁 Categories: {GalleryCategory.objects.count()}")
        print(f"   📸 Albums: {PhotoAlbum.objects.count()}")
        print(f"   ⭐ Featured Albums: {PhotoAlbum.objects.filter(is_featured=True).count()}")
        print(f"   📅 Published Albums: {PhotoAlbum.objects.filter(is_published=True).count()}")
        
        print("\n🌐 Next Steps:")
        print("   1. Access gallery at: http://127.0.0.1:8000/gallery/")
        print("   2. Upload photos via admin: http://127.0.0.1:8000/admin/gallery/")
        print("   3. Manage albums and categories in admin panel")
        print("   4. Add real school photos to showcase events and activities")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)