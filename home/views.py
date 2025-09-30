from django.shortcuts import render
from .models import SchoolInfo, HomePageSlider, QuickLink
from events.models import News

def home(request):
    """Homepage view"""
    try:
        school_info = SchoolInfo.objects.first()
    except:
        school_info = None
    
    slider_images = HomePageSlider.objects.filter(is_active=True)
    quick_links = QuickLink.objects.filter(is_active=True)
    
    # Get latest news only (events removed from home page)
    try:
        latest_news = News.objects.filter(is_published=True).order_by('-created_at')[:3]
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