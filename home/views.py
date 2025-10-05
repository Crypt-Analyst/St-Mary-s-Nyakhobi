from django.shortcuts import render
from .models import SchoolInfo, HomePageSlider, QuickLink
from events.models import News  # OLD model (keeping for compatibility)
from admin_portal.models import NewsAnnouncement  # NEW admin portal model

def home(request):
    """Homepage view"""
    try:
        school_info = SchoolInfo.objects.first()
    except:
        school_info = None
    
    slider_images = HomePageSlider.objects.filter(is_active=True)
    quick_links = QuickLink.objects.filter(is_active=True)
    
    # Get latest news from admin portal (NEW)
    try:
        latest_news = NewsAnnouncement.objects.filter(published=True).order_by('-created_at')[:3]
    except:
        latest_news = []
    
    context = {
        'school_info': school_info,
        'slider_images': slider_images,
        'quick_links': quick_links,
        'latest_news': latest_news,
    }
    return render(request, 'home/index.html', context)

def about(request):
    """About page view"""
    try:
        school_info = SchoolInfo.objects.first()
    except:
        school_info = None
    
    context = {
        'school_info': school_info,
    }
    return render(request, 'home/about.html', context)

def history(request):
    """School history page"""
    context = {}
    return render(request, 'home/history.html', context)

def mission_vision(request):
    """Mission and vision page"""
    context = {}
    return render(request, 'home/mission_vision.html', context)

def facilities(request):
    """School facilities page"""
    context = {}
    return render(request, 'home/facilities.html', context)

def achievements(request):
    """School achievements page"""
    context = {}
    return render(request, 'home/achievements.html', context)

def leadership(request):
    """School leadership page"""
    context = {}
    return render(request, 'home/leadership.html', context)