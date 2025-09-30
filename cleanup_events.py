#!/usr/bin/env python
"""
Script to clean up sample events from the database since events are no longer shown on home page
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

from events.models import Event

def cleanup_sample_events():
    """Remove sample/test events from the database"""
    print("🧹 Cleaning up sample events...")
    
    # Count existing events
    total_events = Event.objects.count()
    print(f"📊 Found {total_events} events in database")
    
    if total_events > 0:
        # Delete all sample events (you can be more selective if needed)
        sample_events = Event.objects.filter(
            title__icontains='sample'
        ) | Event.objects.filter(
            title__icontains='test'
        ) | Event.objects.filter(
            description__icontains='sample'
        )
        
        sample_count = sample_events.count()
        if sample_count > 0:
            sample_events.delete()
            print(f"🗑️ Deleted {sample_count} sample events")
        
        # Optionally, you can delete all events if they are all sample data
        # Uncomment the next 3 lines if you want to remove ALL events
        # Event.objects.all().delete()
        # print(f"🗑️ Deleted all {total_events} events")
        
        remaining_events = Event.objects.count()
        print(f"📈 {remaining_events} events remaining in database")
    else:
        print("✅ No events found in database")
    
    print("✅ Event cleanup completed!")

if __name__ == '__main__':
    cleanup_sample_events()