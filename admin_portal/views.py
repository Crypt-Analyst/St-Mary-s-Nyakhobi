from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from .models import (
    NewsAnnouncement, GalleryImage, TeacherProfile,
    SchoolEvent, DownloadableFile, ContactMessage
)


@staff_member_required
def dashboard_overview(request):
    """Custom admin dashboard with statistics"""
    context = {
        'total_news': NewsAnnouncement.objects.count(),
        'published_news': NewsAnnouncement.objects.filter(published=True).count(),
        'total_gallery': GalleryImage.objects.count(),
        'total_teachers': TeacherProfile.objects.filter(is_active=True).count(),
        'upcoming_events': SchoolEvent.objects.filter(published=True).count(),
        'total_downloads': DownloadableFile.objects.filter(published=True).count(),
        'unread_messages': ContactMessage.objects.filter(read=False).count(),
        'total_messages': ContactMessage.objects.count(),
        
        # Recent items
        'recent_news': NewsAnnouncement.objects.all()[:5],
        'recent_messages': ContactMessage.objects.all()[:10],
        'upcoming_events_list': SchoolEvent.objects.filter(published=True)[:5],
    }
    return render(request, 'admin_portal/dashboard.html', context)
