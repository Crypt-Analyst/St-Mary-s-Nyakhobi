from django.shortcuts import render, get_object_or_404
from .models import Event, News  # OLD models (keeping for now)
from admin_portal.models import NewsAnnouncement, SchoolEvent  # NEW admin portal models

def events_list(request):
    """Display all events - now using admin portal"""
    events = SchoolEvent.objects.filter(published=True).order_by('-start_date')
    
    context = {
        'events': events,
    }
    return render(request, 'events/calendar.html', context)

def event_detail(request, event_id):
    """Display event details - now using admin portal"""
    event = get_object_or_404(SchoolEvent, id=event_id, published=True)
    
    context = {
        'event': event,
    }
    return render(request, 'events/event_detail.html', context)

def news_list(request):
    """Display all news - now using admin portal"""
    news_items = NewsAnnouncement.objects.filter(published=True).order_by('-created_at')
    
    context = {
        'news_items': news_items,
    }
    return render(request, 'events/news_list.html', context)

def news_detail(request, news_id):
    """Display news details - now using admin portal"""
    news_item = get_object_or_404(NewsAnnouncement, id=news_id, published=True)
    
    context = {
        'news_item': news_item,
    }
    return render(request, 'events/news_detail.html', context)

def testimonials(request):
    """Display testimonials and videos"""
    context = {}
    return render(request, 'events/testimonials.html', context)
