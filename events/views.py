from django.shortcuts import render, get_object_or_404
from .models import Event, News, Gallery

def events_list(request):
    """Display all events"""
    events = Event.objects.filter(is_published=True).order_by('-event_date')
    
    context = {
        'events': events,
    }
    return render(request, 'events/events_list.html', context)

def event_detail(request, event_id):
    """Display event details"""
    event = get_object_or_404(Event, id=event_id, is_published=True)
    
    context = {
        'event': event,
    }
    return render(request, 'events/event_detail.html', context)

def news_list(request):
    """Display all news"""
    news = News.objects.filter(is_published=True).order_by('-created_at')
    
    context = {
        'news': news,
    }
    return render(request, 'events/news_list.html', context)

def news_detail(request, news_id):
    """Display news details"""
    news_item = get_object_or_404(News, id=news_id, is_published=True)
    
    context = {
        'news_item': news_item,
    }
    return render(request, 'events/news_detail.html', context)

def gallery(request):
    """Display photo gallery"""
    gallery_items = Gallery.objects.all().order_by('-uploaded_at')
    
    context = {
        'gallery_items': gallery_items,
    }
    return render(request, 'events/gallery.html', context)